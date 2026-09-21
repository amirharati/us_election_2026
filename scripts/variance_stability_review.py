"""Delete recent residual blocks and refit exact original variance estimators."""
from pathlib import Path
from datetime import datetime,timezone
import json,re
import numpy as np
import pandas as pd
import simple_bayesian_polling as v1
import bayesian_revision2 as v2
import simple_national_model as normal
import national_feature_prior as features
import coverage_balance as scoring
import national_tails_waves as chamber
import national_factor_review as national
from final_baseline_experiments import cycle_metrics

FEATURE='20260920T013619.322700Z'
CONFIG=dict(seed=197139,draws=30000,omit_recent_cycles=3,as_of='2026-09-17')

def omit(raw,year):
 mask=raw['years']!=year
 if mask.all():raise ValueError('Omitted cycle absent')
 return {k:raw[k][mask] for k in ['training_values','training_noise','training_weights','years']}

def refit(raw,kappa,kind,omit_year=None):
 data=raw if omit_year is None else omit(raw,omit_year)
 fit=v2.fit_covariance(data['training_values'],data['training_noise'],data['training_weights'],kappa,9. if kind=='poll' else None)
 return dict(fit,**{k:data[k] for k in ['training_values','training_noise','training_weights','years']})

def build(lab):
 lab=Path(lab).resolve();src=lab/'reports/national_feature_prior'/FEATURE;fs=json.loads((src/'settings.json').read_text());work=Path(fs['source']);up=Path(fs['upstream']);prior=Path(json.loads((work/'settings.json').read_text())['prior_source'])
 out=lab/'reports/variance_stability'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
 for x in ['fits','forecasts','recipe']:(out/x).mkdir(parents=True,exist_ok=True)
 st=dict(config=CONFIG,source=str(src),working=str(work),upstream=str(up),prior=str(prior),sources={str(x):v1.verify(x) for x in [src,work,up,prior]},old_notebook_hashes={x.name:v1.sha(x) for x in lab.glob('*.ipynb') if x.name!='VARIANCE_AND_PUBLISHED_REVIEW.ipynb'},working_sha256=v1.sha(lab/'WORKING_MODEL.json'),promotion=False,data_refreshed=False,interpretation='residual-block deletion sensitivity, not parameter posterior or new full-pipeline CV')
 v1.json_write(out/'settings.json',st);print('OUTPUT',out,flush=True)
 orig=pd.read_parquet(src/'predictions.parquet');sf=pd.read_parquet(src/'folds.parquet');sf=sf[sf.model.isin(['none','both'])];pf=pd.read_parquet(prior/'folds.parquet');pf=pf[pf.model.eq('control_state')];roster=pd.read_parquet(up/'full_seat_ledger.parquet')
 preds=[];seats=[];folds=[];fits=[];covchecks=[];parameters=[];repro=[]
 for (sc,year),group in sf.groupby(['scenario','cycle']):
  r=pf[pf.scenario.eq(sc)&pf.cycle.eq(year)].iloc[0];raw={kind:dict(np.load(prior/r[kind+'_path'])) for kind in ['movement','poll']};ks={kind:float(re.search(r'_k([\d.]+)\.npz$',r[kind+'_path'])[1]) for kind in raw}
  baseV=np.load(work/f'fits/{sc}_{year}_movement_K1.npz')['budget'];mult=baseV/np.diag(raw['movement']['covariance'])
  for kind in raw:
   fit=refit(raw[kind],ks[kind],kind);covchecks.append(dict(scenario=sc,cycle=year,kind=kind,max_covariance_difference=float(abs(fit['covariance']-raw[kind]['covariance']).max())))
  recent=sorted(set(raw['movement']['years'])&set(raw['poll']['years']))[-3:][::-1]
  cache={}
  for lag,omitted in enumerate(recent,1):
   for kind in raw:
    z=refit(raw[kind],ks[kind],kind,omitted);cache[kind,omitted]=z;path=f'fits/{sc}_{year}_{kind}_omit{omitted}.npz';np.savez_compressed(out/path,**{k:v for k,v in z.items() if isinstance(v,np.ndarray)})
    fits.append(dict(scenario=sc,cycle=year,kind=kind,omitted_cycle=int(omitted),lag=lag,kappa=ks[kind],training_max_cycle=int(z['years'].max()),iterations=z['iterations'],relative_change=z['relative_change'],path=path))
  for sr in group.itertuples():
   family=sr.model;test=orig[orig.scenario.eq(sc)&orig.cycle.eq(year)&orig.model.eq(family)].sort_values('target_id').reset_index(drop=True);oldfit=dict(np.load(src/sr.fit_path));q=np.load(src/sr.forecast_path)
   variants=[('base',0,None)]+[(kind+f'_drop{lag}',lag,om) for lag,om in enumerate(recent,1) for kind in ['movement','poll','both']]
   for variant,lag,om in variants:
    usemov=variant.startswith(('movement','both'));usepoll=variant.startswith(('poll','both'));mz=cache['movement',om] if usemov else raw['movement'];pz=cache['poll',om] if usepoll else raw['poll'];V=np.diag(mz['covariance'])*mult;P=np.diag(pz['covariance'])+4.
    poll=normal.fixed_common(pz['training_values'],pz['training_noise'],pz['training_weights'],P,0.,9.)
    if usemov:
     mask=oldfit['years']!=om;fit=features.fit_feature(mz['training_values'],mz['training_noise'],mz['training_weights'],V,oldfit['X'][mask],float(oldfit['tau']))
    else:fit=dict(oldfit,a=float(oldfit['a']))
    p,cov,stats,meta=features.predict(test,V,poll,fit,oldfit['z']);model=family+'__'+variant
    p=p.drop(columns=[c for c in ['selected_model','outside_margin_bounds_probability'] if c in p]).assign(model=model,family=family,variant=variant,omitted_cycle=om,omission_lag=lag,prior_sd_pp=np.sqrt(np.diag(meta['prior_covariance'])))
    preds.append(p);rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));draws=p.prediction_pp.to_numpy()+rng.standard_normal((CONFIG['draws'],len(test)))@np.linalg.cholesky(cov).T
    ss,counts=chamber.seat_summary(roster[roster.scenario.eq(sc)&roster.cycle.eq(year)],test,p,draws);freq=np.bincount(counts,minlength=101);seats.append(scoring.seat_scores(dict(ss,scenario=sc,cycle=year,model=model,family=family,variant=variant,omitted_cycle=om),freq))
    path=f'forecasts/{sc}_{year}_{model}.npz';np.savez_compressed(out/path,target_ids=test.target_id.to_numpy(str),mean=p.prediction_pp.to_numpy(),covariance=cov,prior_mean=meta['prior_mean'],prior_covariance=meta['prior_covariance'],poll_budget=P,movement_budget=V,seat_count_frequency=freq,beta_mean=fit['beta_mean'],beta_covariance=fit['beta_covariance'])
    folds.append(dict(scenario=sc,cycle=year,model=model,family=family,variant=variant,omitted_cycle=om,omission_lag=lag,forecast_path=path,source_fit_path=sr.fit_path,source_forecast_path=sr.forecast_path,**stats))
    for i,state in enumerate(v1.STATES):parameters.append(dict(scenario=sc,cycle=year,model=model,geography=state,movement_variance=V[i],poll_variance=P[i],poll_bias=poll['bias_mean'][i]))
    if variant=='base':repro.append(np.allclose(p[['prediction_pp','p_dem','lo70_pp','hi95_pp']],test[['prediction_pp','p_dem','lo70_pp','hi95_pp']],atol=1e-8) and np.array_equal(freq,q['seat_count_frequency']))
  print(sc,year,'deleted',recent,'complete',flush=True)
 p=pd.concat(preds,ignore_index=True);s=pd.DataFrame(seats);f=pd.DataFrame(folds);base=p[p.variant.eq('base')][['scenario','cycle','family','target_id','prediction_pp','p_dem','posterior_sd_pp']]
 delta=p.merge(base,on=['scenario','cycle','family','target_id'],suffixes=('','_base'),validate='many_to_one');delta['mean_change_pp']=delta.prediction_pp-delta.prediction_pp_base;delta['probability_change']=delta.p_dem-delta.p_dem_base;delta['sd_ratio']=delta.posterior_sd_pp/delta.posterior_sd_pp_base
 stability=delta[delta.variant.ne('base')].groupby(['scenario','cycle','family','geography','target_id'],as_index=False).agg(min_prediction_pp=('prediction_pp','min'),max_prediction_pp=('prediction_pp','max'),max_abs_change_pp=('mean_change_pp',lambda x:abs(x).max()),min_p_dem=('p_dem','min'),max_p_dem=('p_dem','max'),min_sd_ratio=('sd_ratio','min'),max_sd_ratio=('sd_ratio','max'))
 for name,tab in dict(predictions=p,seats=s,folds=f,fit_diagnostics=pd.DataFrame(fits),parameters=pd.DataFrame(parameters),deltas=delta,stability=stability,cycle_scores=cycle_metrics(p),summary=scoring.summarize_scores(p),chamber_summary=national.chamber_summary(s),covariance_reproduction=pd.DataFrame(covchecks)).items():tab.to_parquet(out/f'{name}.parquet',index=False)
 v1.json_write(out/'reproduction.json',dict(passed=bool(all(repro)),comparisons=len(repro)))
 for path in (lab/'scripts').glob('*.py'):(out/'recipe'/path.name).write_bytes(path.read_bytes())
 (out/'VARIANCE_STABILITY_REVIEW.md').write_bytes((lab/'VARIANCE_STABILITY_REVIEW.md').read_bytes());v1.manifest(out);audit(out,lab);v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)));print('COMPLETE',out,flush=True)
 return out

def audit(out,lab):
 out,lab=Path(out),Path(lab);v1.verify(out);st=json.loads((out/'settings.json').read_text());p=pd.read_parquet(out/'predictions.parquet');f=pd.read_parquet(out/'folds.parquet');s=pd.read_parquet(out/'seats.parquet');fit=pd.read_parquet(out/'fit_diagnostics.parquet');cv=pd.read_parquet(out/'covariance_reproduction.parquet')
 checks=dict(sources_preserved=all(v1.verify(path)==h for path,h in st['sources'].items()),notebooks_preserved=all(v1.sha(lab/n)==h for n,h in st['old_notebook_hashes'].items()),designation_preserved=v1.sha(lab/'WORKING_MODEL.json')==st['working_sha256'],baseline_reproduces=json.loads((out/'reproduction.json').read_text())['passed'],original_covariance_reproduces=bool(cv.max_covariance_difference.lt(1e-8).all()),past_training=bool(fit.training_max_cycle.lt(fit.cycle).all() and fit.omitted_cycle.lt(fit.cycle).all()),converged=bool(fit.relative_change.lt(v2.CONFIG['convergence_tolerance']).all()),unique_rows=not p.duplicated(['scenario','target_id','model']).any(),current_unknown=bool(p[p.cycle.eq(2026)][['actual','wis_pp','brier']].isna().all().all()),valid_predictions=bool(np.isfinite(p[['prediction_pp','p_dem','lo95_pp','hi95_pp']]).all().all() and p.p_dem.between(0,1).all()),consistent_units=bool(np.allclose(p.prediction*100,p.prediction_pp)))
 deleted=[];account=[];cov=[]
 for r in fit.itertuples():
  z=np.load(out/r.path);deleted.append(r.omitted_cycle not in z['years'] and z['years'].max()<r.cycle)
 for r in f.itertuples():
  z=np.load(out/r.forecast_path);q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id');ss=s[s.scenario.eq(r.scenario)&s.cycle.eq(r.cycle)&s.model.eq(r.model)].iloc[0]
  account.append(z['seat_count_frequency'].sum()==CONFIG['draws'] and abs(ss.expected_D_exact-ss.fixed_D-q.p_dem.sum())<1e-9 and ss.point_D==ss.fixed_D+q.prediction_pp.gt(0).sum());cov.append(np.linalg.eigvalsh(z['covariance']).min()>0)
 inputs=[];channels=[]
 for r in f.itertuples():
  q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id');base=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.family+'__base')].sort_values('target_id')
  inputs.append(all(np.array_equal(q[c],base[c],equal_nan=True) for c in ['actual','prior','q_pp','firm_mass']))
  br=f[f.scenario.eq(r.scenario)&f.cycle.eq(r.cycle)&f.model.eq(r.family+'__base')].iloc[0];z=np.load(out/r.forecast_path);b=np.load(out/br.forecast_path)
  if r.variant.startswith('movement'):channels.append(np.array_equal(z['poll_budget'],b['poll_budget']))
  if r.variant.startswith('poll'):channels.append(np.array_equal(z['movement_budget'],b['movement_budget']) and np.array_equal(z['prior_mean'],b['prior_mean']))
 checks.update(forecast_inputs_labels_preserved=all(inputs),component_isolation=all(channels))
 checks.update(omitted_block_absent=all(deleted),seat_accounting=all(account),positive_covariance=all(cov));result=dict(passed=all(checks.values()),checks=checks,forecasts=len(f),variance_refits=len(fit),rows=len(p));v1.json_write(out/'audit.json',result)
 if not result['passed']:raise AssertionError([k for k,v in checks.items() if not v])
 return result

def load(lab):
 root=Path(lab)/'reports/variance_stability';ptr=json.loads((root/'latest.json').read_text());out=root/ptr['artifact'];assert v1.verify(out)==ptr['manifest_sha256'];return out,{p.stem:pd.read_parquet(p) for p in out.glob('*.parquet')}

if __name__=='__main__':build(Path(__file__).resolve().parents[1])
