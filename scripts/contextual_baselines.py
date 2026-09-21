"""Party-conditional ridge and dated changes, preserving the simple baseline."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from alignment_features import FeatureStore
from data_utils import LAB
from simple_baselines import CONTINUOUS, BINARY, prepare_inputs

CHANGE_FEATURES = [f'{c}__change_{anchor}' for c in CONTINUOUS for anchor in ['jan01','previous_oct31']]
VARIANTS = ['additive', 'interactions', 'interactions_changes']
ALPHAS = [.1, 1., 10., 100.]


def calendar_dates(year, as_of, scenario):
    """October target; current-only partial date never pretends October occurred."""
    as_of=pd.Timestamp(as_of).normalize()
    if year>as_of.year:raise ValueError('Cycle is after dataset date')
    desired=pd.Timestamp(year,10,31)
    if scenario=='matched_live':
        month,day=min((as_of.month,as_of.day),(10,31))
        end=pd.Timestamp(year,month,day)
    elif scenario=='oct31':end=desired
    else:raise ValueError('Unknown calendar scenario')
    end=min(end,as_of) if year==as_of.year else end
    return dict(start=pd.Timestamp(year,1,1),previous=pd.Timestamp(year-1,10,31),
                end=end,desired=desired,complete=end==desired)


def make_store(data):
    if hasattr(data, 'feature_store'): return data.feature_store()
    prov=data.provenance
    political=json.loads(((LAB/Path(prov['political_snapshot']))/'config.json').read_text())
    return FeatureStore((LAB/Path(prov['prepared_feature_snapshot'])),political,data.policy['as_of'])


def price_percent_change(end, base):
    """Index-base/currency invariant; unavailable/nonpositive endpoints stay missing."""
    if pd.isna(base) or pd.isna(end) or not np.isfinite(base) or not np.isfinite(end) or base<=0 or end<=0:
        return np.nan
    return 100*(end/base-1)


def calendar_inputs(data, store, scenario):
    """Rebuild reference contexts from pinned sources; export all endpoint evidence."""
    original=data.load_table('contest_inputs_reference')
    rows=[];endpoints=[]
    for year in sorted(original.cycle.unique()):
        dates=calendar_dates(int(year),data.policy['as_of'],scenario)
        contexts={name:store.at(dates[name])[0] for name in ['start','previous','end']}
        row=dict(cycle=int(year),**{k:v for k,v in contexts['end'].items() if k not in ['cycle']})
        row.update(scenario=scenario,desired_cutoff=str(dates['desired'].date()),
                   window_complete=dates['complete'],start_cutoff=str(dates['start'].date()),
                   previous_cutoff=str(dates['previous'].date()),
                   days_since_jan01=(dates['end']-dates['start']).days,
                   days_since_previous_oct31=(dates['end']-dates['previous']).days)
        # A delta remains missing if either endpoint is missing; no synthetic zero.
        for c in CONTINUOUS:
            row[c+'__start_jan01']=contexts['start'][c]
            row[c+'__previous_oct31']=contexts['previous'][c]
            row[c+'__change_jan01']=contexts['end'][c]-contexts['start'][c]
            row[c+'__change_previous_oct31']=contexts['end'][c]-contexts['previous'][c]
            for endpoint in ['start','previous','end']:
                evidence=next(r for r in reversed(store.ledger)
                              if r['context_id']==str(dates[endpoint].date()) and r['feature']==c)
                endpoints.append(dict(scenario=scenario,cycle=int(year),endpoint=endpoint,
                                      endpoint_cutoff=str(dates[endpoint].date()),**evidence))
        # Price-index ratios are dimensionless changes, not dollar/index differences.
        # These additions feed the fixed summarizer, not the existing regression variants.
        for c in ['cpi_level','gasoline_cpi_level']:
            for endpoint,anchor in [('start','jan01'),('previous','previous_oct31')]:
                base=contexts[endpoint][c];end=contexts['end'][c]
                row[c+'__pct_change_'+anchor]=price_percent_change(end,base)
            for endpoint in ['start','previous','end']:
                evidence=next(r for r in reversed(store.ledger)
                              if r['context_id']==str(dates[endpoint].date()) and r['feature']==c)
                endpoints.append(dict(scenario=scenario,cycle=int(year),endpoint=endpoint,
                                      endpoint_cutoff=str(dates[endpoint].date()),**evidence))
        rows.append(row)
    calendar=pd.DataFrame(rows)
    replace=[c for c in calendar if c in original and c!='cycle']
    joined=original.drop(columns=replace).merge(calendar,on='cycle',validate='many_to_one')
    election=pd.to_datetime(joined.election_date)
    cutoff=pd.to_datetime(joined.context_id)
    # Do not score a special/stage that already happened before this calendar cutoff.
    joined['historical_horizon_comparable']=joined.historical_horizon_comparable & election.gt(cutoff)
    joined['forecast_days_to_election']=(election-cutoff).dt.days
    return joined,calendar,pd.DataFrame(endpoints)


class ContextTransform:
    """Train-only normalization, followed by WH-sign interactions on those z-scores."""
    def __init__(self, variant):
        if variant not in VARIANTS:raise ValueError('Unknown variant')
        self.variant=variant
        self.continuous=CONTINUOUS+(CHANGE_FEATURES if variant=='interactions_changes' else [])

    def fit(self, frame):
        candidates=self.continuous+BINARY
        self.columns=[c for c in candidates if frame[c].notna().any()]
        self.dropped=[c for c in candidates if c not in self.columns]
        self.fills={};self.centers={};self.scales={};self.indicators=[]
        for c in self.columns:
            s=frame[c].astype(float)
            self.fills[c]=float(s.mode().iloc[0] if c in BINARY else s.median())
            q=s.fillna(self.fills[c])
            self.centers[c]=0. if c in BINARY else float(q.mean())
            sd=1. if c in BINARY else float(q.std(ddof=0))
            self.scales[c]=sd if sd>1e-12 else 1.
            if s.isna().any():self.indicators.append(c)
        self.interactions=([c for c in self.continuous if c in self.columns]
                           if self.variant!='additive' and 'wh_dem' in self.columns else [])
        self.names=self.columns+[c+'__missing' for c in self.indicators]+[c+'__x_wh_sign' for c in self.interactions]
        return self

    def transform(self, frame):
        normalized={c:(frame[c].astype(float).fillna(self.fills[c]).to_numpy()-self.centers[c])/self.scales[c] for c in self.columns}
        values=list(normalized.values())+[frame[c].isna().astype(float).to_numpy() for c in self.indicators]
        if self.interactions:
            sign=2*frame.wh_dem.astype(float).fillna(self.fills['wh_dem']).to_numpy()-1
            values += [normalized[c]*sign for c in self.interactions]
        return np.column_stack(values) if values else np.zeros((len(frame),0))


def predict_variant(train, test, alpha, variant):
    transform=ContextTransform(variant).fit(train)
    info=dict(variant=variant,alpha=float(alpha),training_rows=len(train),training_cycles=int(train.cycle.nunique()),
              training_max_cycle=int(train.cycle.max()) if len(train) else None,
              fills=transform.fills,centers=transform.centers,scales=transform.scales,
              dropped=transform.dropped,indicators=transform.indicators,interactions=transform.interactions,
              terms=transform.names)
    if train.cycle.nunique()<3 or not transform.names:
        info.update(status='insufficient_history_prior_only',intercept=0.,coefficients={})
        return test.prior.to_numpy(dtype=float),info
    weight=1/train.groupby('cycle').cycle.transform('size').to_numpy()
    model=Ridge(alpha=alpha).fit(transform.transform(train),train.actual-train.prior,sample_weight=weight)
    raw=test.prior.to_numpy()+model.predict(transform.transform(test))
    info.update(status='ridge_residual',intercept=float(model.intercept_),
                coefficients=dict(zip(transform.names,map(float,model.coef_))),clipped=int((np.abs(raw)>1).sum()))
    return np.clip(raw,-1,1),info


def evaluate_context(targets, scenario, start_cycle=2002):
    predictions=[];tuning=[];fits=[]
    for kind in ['senate','national']:
        source=targets[targets.kind.eq(kind)]
        for year in sorted(y for y in source.cycle.unique() if y>=start_cycle):
            # Before October, never mix a September current row with October training.
            if scenario=='oct31' and not source.loc[source.cycle.eq(year),'window_complete'].all():continue
            test=source[source.cycle.eq(year)]
            train=source[source.cycle.lt(year)&source.actual.notna()]
            validation=source[source.cycle.eq(year-2)&source.actual.notna()]
            inner=source[source.cycle.lt(year-2)&source.actual.notna()]
            for variant in VARIANTS:
                alpha=10.;status='default_insufficient_inner_history'
                if len(validation) and inner.cycle.nunique()>=3:
                    candidates=[]
                    for a in ALPHAS:
                        pred,_=predict_variant(inner,validation,a,variant)
                        score=float(np.mean(np.abs(pred-validation.actual.to_numpy())))
                        candidates.append((score,a))
                        tuning.append(dict(scenario=scenario,kind=kind,cycle=int(year),variant=variant,
                                           validation_cycle=int(year-2),fit_max_cycle=int(inner.cycle.max()),
                                           alpha=a,mae=score,n_validation=len(validation)))
                    alpha=min(candidates,key=lambda x:(round(x[0],12),-x[1]))[1]
                    status='last_cycle_tuned'
                pred,fit=predict_variant(train,test,alpha,variant)
                fit.update(scenario=scenario,kind=kind,cycle=int(year));fits.append(fit)
                result=test[['target_id','cycle','kind','geography','context_id','actual','prior','prior_basis','window_complete',
                             'desired_cutoff','days_since_jan01','days_since_previous_oct31']].copy()
                result['scenario']=scenario;result['variant']=variant;result['prediction']=pred;result['alpha']=alpha
                result['tuning_status']=status;result['training_max_cycle']=fit['training_max_cycle']
                result['validation_cycle']=year-2
                result['missing_raw_inputs']=test[CONTINUOUS+(CHANGE_FEATURES if variant=='interactions_changes' else [])+BINARY].isna().sum(axis=1).to_numpy()
                predictions.append(result)
    return pd.concat(predictions,ignore_index=True),pd.DataFrame(tuning),fits


def score_context(predictions):
    rows=[]
    for keys,g in predictions[predictions.actual.notna()].groupby(['scenario','kind','cycle','variant']):
        error=100*(g.prediction-g.actual)
        rows.append(dict(zip(['scenario','kind','cycle','variant'],keys),n=len(g),
                         mae_pp=float(error.abs().mean()),rmse_pp=float(np.sqrt(np.mean(error**2))),bias_pp=float(error.mean())))
    return pd.DataFrame(rows)
