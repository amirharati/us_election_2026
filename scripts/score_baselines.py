"""Senate prior corrections from four fixed domain scores, with chronological tuning.

Component normalization and score imputation are fitted within each training fold.
One equally weighted cycle-mean residual is equivalent to the earlier cycle-balanced
state-row squared loss. No outcome-fitted internal score weights or extra interactions.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from feature_scores import FixedFeatureScores,MODEL_COLUMNS
from cycle_cv import fold_ledger,MIN_INNER_CYCLES

ALPHAS=[.1,1.,10.,100.]


class ScoreDesign:
    def fit(self, calendars):
        self.summary=FixedFeatureScores().fit(calendars)
        scores,_=self.summary.transform(calendars)
        self.fills={};self.active=[];self.dropped={};self.missing={}
        for c in MODEL_COLUMNS:
            q=scores[c].astype(float);self.missing[c]=int(q.isna().sum())
            if q.notna().any():
                self.fills[c]=float(q.median())
                if q.fillna(self.fills[c]).std(ddof=0)>1e-12:self.active.append(c)
                else:self.dropped[c]='constant_after_training_median_fill'
            else:self.dropped[c]='all_missing_training'
        return self

    def transform(self, calendars, require_later=False):
        scores,components=self.summary.transform(calendars,require_later=require_later)
        matrix=np.column_stack([scores[c].fillna(self.fills[c]).to_numpy(dtype=float) for c in self.active]) if self.active else np.zeros((len(scores),0))
        return matrix,scores,components

    def metadata(self):
        return dict(normalizer=self.summary.metadata(),score_fills=self.fills,active_terms=self.active,
                    dropped_terms=self.dropped,training_missing_cycles=self.missing,
                    score_scaling='already dimensionless fixed scores; no second rescaling; binary remains 0/1',
                    imputation='training-cycle medians; no missing indicators or partial ingredient weights')


def fit_correction(train,test,calendars,alpha=10.,model='four_scores'):
    if model not in ('four_scores','constant'):raise ValueError('Unknown correction model')
    if train.empty or train.actual.isna().any():raise ValueError('Known training labels required')
    if train.cycle.max()>=test.cycle.min():raise ValueError('Training must precede forecast cycles')
    if not train.kind.eq('senate').all() or not test.kind.eq('senate').all():raise ValueError('Senate only')
    if calendars.cycle.duplicated().any():raise ValueError('One calendar per cycle required')
    # Averaging residuals within each cycle preserves the cycle-balanced ridge optimum.
    residual=(train.actual-train.prior).groupby(train.cycle).mean().sort_index()
    info=dict(model=model,alpha=float(alpha) if model=='four_scores' else None,
              training_cycles=len(residual),training_rows=len(train),training_max_cycle=int(train.cycle.max()),
              training_cycle_ids=list(map(int,residual.index)),fit_target='cycle mean(actual - prior)',
              coefficients={c:0. for c in MODEL_COLUMNS},intercept=float(residual.mean()))
    contributions=pd.DataFrame();audit=pd.DataFrame()
    if model=='constant':correction=np.full(len(test),residual.mean())
    else:
        indexed=calendars.set_index('cycle',drop=False)
        train_cal=indexed.loc[residual.index].reset_index(drop=True)
        test_cal=indexed.loc[sorted(test.cycle.unique())].reset_index(drop=True)
        design=ScoreDesign().fit(train_cal)
        x,training_scores,_=design.transform(train_cal)
        z,test_scores,audit=design.transform(test_cal,require_later=True)
        info.update(design.metadata())
        if design.active:
            fitted=Ridge(alpha=alpha).fit(x,residual.to_numpy())
            coeff=dict(zip(design.active,map(float,fitted.coef_)))
            info['coefficients'].update(coeff);info['intercept']=float(fitted.intercept_)
            by_cycle=pd.Series(fitted.predict(z),index=test_cal.cycle)
        else:by_cycle=pd.Series(residual.mean(),index=test_cal.cycle)
        correction=test.cycle.map(by_cycle).to_numpy()
        info['fitted_parameters']=len(design.active)+1
        info['test_missing_scores']={str(int(r.cycle)):[c for c in MODEL_COLUMNS if pd.isna(getattr(r,c))] for r in test_scores.itertuples()}
        contributions=test_scores[['cycle']+MODEL_COLUMNS].copy()
        for c in MODEL_COLUMNS:
            contributions[c+'__filled']=test_scores[c].fillna(design.fills[c]) if c in design.active else 0.
            contributions[c+'__contribution_pp']=100*contributions[c+'__filled']*info['coefficients'][c]
        contributions['intercept_pp']=100*info['intercept']
        contributions['correction_pp']=100*test_scores.cycle.map(by_cycle)
        info['training_score_rows']=training_scores[['cycle']+MODEL_COLUMNS].replace({np.nan:None}).to_dict('records')
    raw=test.prior.to_numpy()+correction
    info['clipped_predictions']=int((np.abs(raw)>1).sum())
    return np.clip(raw,-1,1),info,contributions,audit


def evaluate_scores(targets,calendars,scenario,start_cycle=2002,min_inner_cycles=MIN_INNER_CYCLES):
    source=targets[targets.kind.eq('senate')].copy()
    cal=calendars[calendars.scenario.eq(scenario)].copy()
    folds=fold_ledger(source,scenario,min_inner_cycles,start_cycle)
    predictions=[];fits=[];grids=[];parts=[];audits=[]
    for fold in folds.itertuples():
        year=int(fold.cycle)
        if fold.status=='pending_cutoff':continue
        test=source[source.cycle.eq(year)]
        train=source[source.cycle.lt(year)&source.actual.notna()]
        inner=train[train.cycle.lt(year-2)];validation=train[train.cycle.eq(year-2)]
        eligible=inner.cycle.nunique()>=min_inner_cycles and len(validation)>0
        alpha=10.
        if eligible:
            candidates=[]
            for a in ALPHAS:
                pred,fit,_,_=fit_correction(inner,validation,cal,a)
                loss=float(np.mean(np.abs(pred-validation.actual.to_numpy())))
                candidates.append((loss,a))
                grids.append(dict(scenario=scenario,cycle=year,validation_cycle=year-2,
                    training_max_cycle=fit['training_max_cycle'],training_cycles=fit['training_cycles'],
                    alpha=a,validation_mae_pp=100*loss))
            alpha=min(candidates,key=lambda v:(round(v[0],12),-v[1]))[1]
        for model in ['constant','four_scores']:
            if not eligible:
                pred=test.prior.to_numpy();fit=dict(model=model,status='warmup_prior_fallback',training_cycles=int(train.cycle.nunique()))
                contribution=pd.DataFrame();audit=pd.DataFrame()
            else:
                pred,fit,contribution,audit=fit_correction(train,test,cal,alpha,model)
                fit['status']='fitted'
            fit.update(scenario=scenario,cycle=year,validation_cycle=year-2);fits.append(fit)
            out=test[['target_id','cycle','kind','geography','context_id','actual','prior','prior_basis']].copy()
            out=out.assign(scenario=scenario,model=model,prediction=pred,selected_alpha=alpha if model=='four_scores' and eligible else np.nan)
            predictions.append(out)
            if len(contribution):parts.append(contribution.assign(scenario=scenario))
            if len(audit):audits.append(audit.assign(forecast_cycle=year))
    concat=lambda rows:pd.concat(rows,ignore_index=True) if rows else pd.DataFrame()
    return concat(predictions),pd.DataFrame(grids),fits,concat(parts),concat(audits),folds
