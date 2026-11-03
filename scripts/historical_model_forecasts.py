"""Dated retrospective inference with frozen earlier-cycle fits; no AI calls."""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import election_lab as lab
from load_final_dataset import open_dataset
from contextual_baselines import make_store, calendar_inputs
from simple_baselines import prepare_inputs, poll_predict
from state_poll_bias import fit_bias
from model_portfolio import additions
from polymarket_backtest import MODELS, PROVENANCE
from download_polymarket_history import OUT
from release_alternatives import OLD_GAUSSIAN, OLD_STUDENT

HISTORICAL_MODELS={**MODELS,OLD_GAUSSIAN:'OG',OLD_STUDENT:'OS'}

DATES=('06-01','07-01','08-01','09-01','09-05','09-15','09-17','09-20','10-01','10-15','10-31','11-03')
CACHE=OUT/'historical_inference'


def prepare(cutoff):
    cutoff=pd.Timestamp(cutoff);year=cutoff.year;sc='matched_live'
    if year not in (2022,2024):raise ValueError('Only reviewed 2022/2024 folds')
    data=open_dataset(lab.FROZEN)
    store=make_store(data)
    inputs,calendar,_=calendar_inputs(data,store,sc,{year:cutoff})
    targets,waves,audit,_=prepare_inputs(data,inputs)
    targets=targets[targets.kind.eq('senate')&targets.cycle.eq(year)].sort_values('target_id').reset_index(drop=True)
    saved=pd.read_parquet(lab.ASSETS/'main/predictions.parquet')
    q=saved[saved.scenario.eq(sc)&saved.cycle.eq(year)].sort_values('target_id').reset_index(drop=True).copy()
    if list(q.target_id)!=list(targets.target_id):raise ValueError('Historical contest roster changed')
    agg=lab.gaussian.aggregate(targets,waves)
    for col in agg:
        if col!='target_id':q[col]=agg.set_index('target_id').loc[q.target_id,col].to_numpy()
    q['as_of']=q['context_id']=str(cutoff.date())
    # Keep outcome labels out of inference; restore only after all forecasts finish.
    actual=q.actual.copy();q['actual']=np.nan
    targets=targets.copy();targets['actual']=np.nan
    cal=pd.read_parquet(lab.ASSETS/'training/calendars.parquet');cal=cal[cal.scenario.eq(sc)].copy()
    current=calendar[calendar.cycle.eq(year)]
    for col in current:cal.loc[cal.cycle.eq(year),col]=current[col].iloc[0]
    folds=pd.read_parquet(lab.ASSETS/'main/folds.parquet')
    fold=folds[folds.scenario.eq(sc)&folds.cycle.eq(year)].iloc[0]
    fit=dict(np.load(lab.ASSETS/'main'/fold.fit_path));fit['a']=float(fit['a'])
    if fit['years'].max()>=year:raise ValueError('Future training data')
    design,_,z,*_=lab.features.prepare_design(cal,fit['years'],fit['training_weights'],year)
    fit['z']=z[[design.active.index(t) for t in fit['terms']]]
    return q,fit,fold,cal,targets,waves,audit,actual,pd.DataFrame(store.ledger)


def infer(cutoff,destination):
    q,fit,fold,cal,targets,waves,audit,actual,ledger=prepare(cutoff)
    year=int(q.cycle.iloc[0]);sc='matched_live'
    pred,_,arrays=lab.signed.predict(q,fit,lab.load_poll(sc,year),fit['loading'],fold.lambda_value)
    pp=lab.scored(pred,'Bayesian')
    draws=arrays['mean']+np.random.default_rng(lab.SEED+year).standard_normal((lab.DRAWS,len(q)))@np.linalg.cholesky(arrays['covariance']).T
    h=pd.read_parquet(lab.ASSETS/'training/history.parquet');h=h[h.scenario.eq(sc)];old=h[h.cycle.eq(year)]
    nb=poll_predict(targets,waves,float(old.poll_half_life.iloc[0]),float(old.poll_prior_strength.iloc[0])).rename(columns={'prediction':'poll_baseline'})
    nb=targets.merge(nb,on='target_id',validate='one_to_one')
    means,*_=fit_bias(h[h.cycle.lt(year)],nb,5,8.,'state',float(old.bias_shrinkage.iloc[0]))
    polling=pp.copy();polling['margin_pp']=100*means
    refs=pd.read_parquet(lab.ASSETS/'main/seats.parquet');ref=refs[refs.scenario.eq(sc)&refs.cycle.eq(year)].iloc[0].copy();ref['actual_D']=np.nan
    extra=additions(pp,fit,float(fold.lambda_value),cal,draws,arrays['covariance'],polling,ref,True)
    rows=pd.concat([pp,*extra['predictions']],ignore_index=True)
    rows=rows[rows.model.isin(HISTORICAL_MODELS)].copy()
    rows['actual']=rows.target_id.map(dict(zip(q.target_id,actual)))
    rows['model_code']=rows.model.map(HISTORICAL_MODELS);rows['forecast_date']=pd.Timestamp(cutoff,tz='UTC')
    rows['provenance']=PROVENANCE
    destination.mkdir(parents=True,exist_ok=True)
    rows.to_parquet(destination/'predictions.parquet',index=False)
    audit[audit.cycle.eq(year)].to_parquet(destination/'poll_audit.parquet',index=False)
    ledger.to_parquet(destination/'feature_ledger.parquet',index=False)
    pd.concat(extra['diagnostics'],ignore_index=True).to_parquet(destination/'diagnostics.parquet',index=False)
    return rows


def fingerprint():
    paths=[*lab.FROZEN.rglob('*'),*lab.ASSETS.rglob('*'),*[p for p in (lab.ROOT/'scripts').glob('*.py') if not p.name.startswith(('polymarket','historical_market','download','prepare_historical'))],lab.ROOT/'election_lab.py',lab.ROOT/'config/ensemble_v1.json']
    digest=hashlib.sha256(json.dumps(HISTORICAL_MODELS,sort_keys=True).encode())
    for p in sorted(paths):
        if p.is_file():digest.update(str(p.relative_to(lab.ROOT)).encode());digest.update(p.read_bytes())
    return digest.hexdigest()


def build_forecasts(dates=DATES,force=False):
    key=fingerprint();rows=[]
    for year in (2022,2024):
        for date in dates:
            cutoff=f'{year}-{date}';destination=CACHE/cutoff;receipt=destination/'receipt.json'
            if not force and receipt.exists() and json.loads(receipt.read_text()).get('fingerprint')==key:
                result=pd.read_parquet(destination/'predictions.parquet')
            else:
                print('Historical inference:',cutoff,flush=True)
                result=infer(cutoff,destination)
                receipt.write_text(json.dumps(dict(fingerprint=key,cutoff=cutoff,trained_before=year,
                    calibration_horizon='Frozen September 17 folds reused at every date',provenance=PROVENANCE),indent=2)+'\n')
            rows.append(result)
    result=pd.concat(rows,ignore_index=True)
    result.to_parquet(OUT/'dated_forecasts.parquet',index=False)
    return result

if __name__=='__main__':build_forecasts()
