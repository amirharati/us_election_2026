"""Train-only final-score scaling and prespecified single-factor Senate regressions.

Keeps the original unstandardized implementation intact for comparison. All models
correct the same state priors and give equal squared-loss weight to each cycle.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from score_baselines import ScoreDesign,ALPHAS
from feature_scores import MODEL_COLUMNS
from cycle_cv import fold_ledger,MIN_INNER_CYCLES

VARIANTS={
    'four_standardized':list(MODEL_COLUMNS),
    'conditions_only':['economy_conditions_wh'],
    'momentum_only':['economy_momentum_wh'],
    'approval_only':['approval_wh'],
    'disruption_only':['disruption_any'],
}


class StandardizedDesign(ScoreDesign):
    def __init__(self,columns):
        self.requested=list(columns)
        if not self.requested or len(set(self.requested))!=len(self.requested) or not set(self.requested)<=set(MODEL_COLUMNS):
            raise ValueError('Choose distinct fixed score columns')

    def fit(self,calendars):
        super().fit(calendars)
        self.active=[c for c in self.requested if c in self.active]
        self.dropped={c:v for c,v in self.dropped.items() if c in self.requested}
        self.fills={c:v for c,v in self.fills.items() if c in self.requested}
        self.missing={c:v for c,v in self.missing.items() if c in self.requested}
        scores,_=self.summary.transform(calendars)
        self.centers={c:float(scores[c].fillna(self.fills[c]).mean()) for c in self.active}
        self.scales={c:float(scores[c].fillna(self.fills[c]).std(ddof=0)) for c in self.active}
        return self

    def transform(self,calendars,require_later=False):
        raw,scores,components=super().transform(calendars,require_later)
        x=(raw-np.array([self.centers[c] for c in self.active]))/np.array([self.scales[c] for c in self.active]) if self.active else raw
        return x,scores,components

    def metadata(self):
        result=super().metadata()
        result.update(requested_terms=self.requested,score_centers=self.centers,score_scales=self.scales,
            score_scaling='after train-cycle median fill: training mean zero, population variance one; includes binary; no second clipping',
            coefficient_units='standardized coefficients per one training SD; raw-score equivalents also retained')
        return result


def fit_standardized(train,test,calendars,alpha,variant):
    if variant not in VARIANTS:raise ValueError('Unknown standardized variant')
    if train.empty or train.actual.isna().any():raise ValueError('Known training labels required')
    if train.cycle.max()>=test.cycle.min():raise ValueError('Training must precede forecast cycles')
    if not train.kind.eq('senate').all() or not test.kind.eq('senate').all():raise ValueError('Senate only')
    if calendars.cycle.duplicated().any():raise ValueError('One calendar per cycle required')
    residual=(train.actual-train.prior).groupby(train.cycle).mean().sort_index()
    indexed=calendars.set_index('cycle',drop=False)
    train_cal=indexed.loc[residual.index].reset_index(drop=True)
    test_cal=indexed.loc[sorted(test.cycle.unique())].reset_index(drop=True)
    design=StandardizedDesign(VARIANTS[variant]).fit(train_cal)
    x,training_scores,_=design.transform(train_cal)
    z,scores,components=design.transform(test_cal,require_later=True)
    intercept=float(residual.mean());coeff={c:0. for c in VARIANTS[variant]}
    if design.active:
        fitted=Ridge(alpha=alpha).fit(x,residual.to_numpy())
        intercept=float(fitted.intercept_);coeff.update(dict(zip(design.active,map(float,fitted.coef_))))
        corrections=fitted.predict(z)
    else:corrections=np.full(len(test_cal),intercept)
    raw_coeff={c:coeff[c]/design.scales[c] if c in design.active else 0. for c in VARIANTS[variant]}
    raw_intercept=intercept-sum(raw_coeff[c]*design.centers[c] for c in design.active)
    by_cycle=pd.Series(corrections,index=test_cal.cycle)
    raw=test.prior.to_numpy()+test.cycle.map(by_cycle).to_numpy()
    info=dict(model=variant,alpha=float(alpha),status='fitted' if design.active else 'intercept_only_no_variable_selected_scores',
        training_cycles=len(residual),training_rows=len(train),training_max_cycle=int(train.cycle.max()),
        training_cycle_ids=list(map(int,residual.index)),fit_target='cycle mean(actual - prior)',
        intercept=intercept,coefficients=coeff,raw_intercept=raw_intercept,raw_coefficients=raw_coeff,
        fitted_parameters=len(design.active)+1,clipped_predictions=int((np.abs(raw)>1).sum()),**design.metadata())
    info['training_score_rows']=training_scores[['cycle']+VARIANTS[variant]].replace({np.nan:None}).to_dict('records')
    info['test_missing_scores']={str(int(r.cycle)):[c for c in VARIANTS[variant] if pd.isna(getattr(r,c))] for r in scores.itertuples()}
    ledger=[]
    for i,row in enumerate(scores.to_dict('records')):
        for c in VARIANTS[variant]:
            active=c in design.active;filled=row[c] if pd.notna(row[c]) else design.fills.get(c,np.nan)
            standardized=float(z[i,design.active.index(c)]) if active else np.nan
            ledger.append(dict(cycle=int(row['cycle']),model=variant,term=c,raw_score=row[c],filled_score=filled,
                imputed=bool(pd.isna(row[c]) and active),active=active,center=design.centers.get(c,np.nan),
                scale=design.scales.get(c,np.nan),standardized_score=standardized,coefficient_pp=100*coeff[c],
                raw_coefficient_pp=100*raw_coeff[c],contribution_pp=100*coeff[c]*standardized if active else 0.,
                intercept_pp=100*intercept,raw_intercept_pp=100*raw_intercept,correction_pp=100*corrections[i]))
    components=components[components.component.isin([c for c,s in design.summary.specs.items()
        if s['score']+'_wh' in VARIANTS[variant]])].copy()
    return np.clip(raw,-1,1),info,pd.DataFrame(ledger),components


def evaluate_standardized(targets,calendars,scenario,start_cycle=2002,min_inner_cycles=MIN_INNER_CYCLES,variants=None):
    names=list(VARIANTS) if variants is None else list(variants)
    if not names or len(set(names))!=len(names) or not set(names)<=set(VARIANTS):raise ValueError('Unknown or duplicate model')
    source=targets[targets.kind.eq('senate')].copy();cal=calendars[calendars.scenario.eq(scenario)].copy()
    folds=fold_ledger(source,scenario,min_inner_cycles,start_cycle)
    predictions=[];fits=[];grids=[];parts=[];audits=[]
    for fold in folds.itertuples():
        year=int(fold.cycle)
        if fold.status=='pending_cutoff':continue
        test=source[source.cycle.eq(year)]
        train=source[source.cycle.lt(year)&source.actual.notna()]
        inner=train[train.cycle.lt(year-2)];validation=train[train.cycle.eq(year-2)]
        eligible=inner.cycle.nunique()>=min_inner_cycles and len(validation)>0
        for variant in names:
            alpha=None
            if eligible:
                candidates=[]
                for a in ALPHAS:
                    pred,fit,_,_=fit_standardized(inner,validation,cal,a,variant)
                    loss=float(np.mean(np.abs(pred-validation.actual.to_numpy())))
                    candidates.append((loss,a))
                    grids.append(dict(scenario=scenario,cycle=year,model=variant,validation_cycle=year-2,
                        training_max_cycle=fit['training_max_cycle'],training_cycles=fit['training_cycles'],
                        alpha=a,validation_mae_pp=100*loss))
                alpha=min(candidates,key=lambda v:(round(v[0],12),-v[1]))[1]
                pred,fit,ledger,audit=fit_standardized(train,test,cal,alpha,variant)
                parts.append(ledger.assign(scenario=scenario))
                if len(audit):audits.append(audit.assign(model=variant,forecast_cycle=year))
            else:
                pred=test.prior.to_numpy();fit=dict(model=variant,status='warmup_prior_fallback',training_cycles=int(train.cycle.nunique()))
            fit.update(scenario=scenario,cycle=year,validation_cycle=year-2);fits.append(fit)
            out=test[['target_id','cycle','kind','geography','context_id','actual','prior','prior_basis']].copy()
            predictions.append(out.assign(scenario=scenario,model=variant,prediction=pred,selected_alpha=alpha))
    concat=lambda rows:pd.concat(rows,ignore_index=True) if rows else pd.DataFrame()
    return concat(predictions),pd.DataFrame(grids),fits,concat(parts),concat(audits),folds
