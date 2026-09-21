"""Trace sparse-poll uncertainty to historical residuals and calibrated multipliers."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import simple_bayesian_polling as v1


def weighted_moments(values,weights):
    known=np.isfinite(values);x=values[known];w=weights[known]
    if not len(x):return dict(history_n=0,history_effective_n=0.,weighted_mean_pp=np.nan,centered_sd_pp=np.nan,rms_pp=np.nan,mean_square_fraction=np.nan)
    mean=float(np.average(x,weights=w));variance=float(np.average((x-mean)**2,weights=w));rms2=float(np.average(x*x,weights=w))
    return dict(history_n=len(x),history_effective_n=float(w.sum()**2/(w@w)),weighted_mean_pp=mean,centered_sd_pp=np.sqrt(variance),rms_pp=np.sqrt(rms2),mean_square_fraction=mean*mean/rms2 if rms2 else 0.)


def build(out,lab):
    out,lab=Path(out),Path(lab);st=json.loads((out/'settings.json').read_text());source=Path(st['source']);work=Path(st['working']);prior=Path(st['prior']);folds=pd.read_parquet(source/'folds.parquet');pred=pd.read_parquet(source/'predictions.parquet');prfold=pd.read_parquet(prior/'folds.parquet');prfold=prfold[prfold.model.eq('control_state')];pen=pd.read_parquet(prior/'state_penalties.parquet');pen=pen[pen.model.eq('control_state')];hist=pd.read_parquet(prior/'prepared_histories.parquet');ag=pd.read_parquet(out/'aggregates.parquet');ag=ag[ag.variant.eq('baseline')]
    rows=[];residuals=[];checks=[]
    for r in folds[folds.model.isin(['none','both'])].itertuples():
        q=pred[pred.scenario.eq(r.scenario)&pred.cycle.eq(r.cycle)&pred.model.eq(r.model)].sort_values('target_id');ps=prfold[prfold.scenario.eq(r.scenario)&prfold.cycle.eq(r.cycle)].iloc[0];raw=np.load(prior/ps.movement_path);mov=np.load(work/f'fits/{r.scenario}_{r.cycle}_movement_K1.npz');fit=np.load(source/r.fit_path);saved=np.load(source/r.forecast_path);pp=pen[pen.scenario.eq(r.scenario)&pen.cycle.eq(r.cycle)].set_index('state');coverage=ag[ag.scenario.eq(r.scenario)].set_index('target_id');h=hist[hist.scenario.eq(r.scenario)&hist.prior_recipe.eq(ps.recipe)].set_index(['cycle','geography'])
        checks.append(bool(np.array_equal(raw['training_values'],mov['training_values'],equal_nan=True)&np.array_equal(raw['training_weights'],mov['training_weights'])))
        for j,t in enumerate(q.itertuples()):
            i=v1.STATES.index(t.geography);x=mov['training_values'][:,i];weights=mov['training_weights'];stats=weighted_moments(x,weights);mult=float(pp.loc[t.geography,'variance_multiplier']);rawvar=raw['covariance'][i,i];budget=mov['budget'][i];priorvar=saved['prior_covariance'][j,j];postvar=saved['covariance'][j,j];a=float(fit['a']);fv=float(fit['z']@fit['beta_covariance']@fit['z']);co=coverage.loc[t.target_id];mean=t.prediction_pp;sd=t.posterior_sd_pp
            checks.append(bool(np.isclose(rawvar*mult,budget)&np.isclose(priorvar,budget+fv)&np.isclose(postvar,sd**2)))
            past_local=h.loc[(h.index.get_level_values(0)<r.cycle)&(h.index.get_level_values(1)==t.geography)].sort_index().actual.dropna()
            latest=100*past_local.iloc[-1] if len(past_local) else np.nan
            row=dict(model=r.model,scenario=r.scenario,cycle=r.cycle,target_id=t.target_id,state=t.geography,sample_count=int(co.sample_count),recent_firms=int(co.recent_firms),firm_mass=co.firm_mass,weighted_poll_age_days=co.weighted_age_days,coverage_group='no_polls' if co.sample_count==0 else 'low_recent_0_2_firms' if co.recent_firms<=2 else 'recent_3plus_firms',independent_proxy=t.geography in ['ID','MT','NE','SD'],prior_mean_pp=100*t.prior,latest_state_result_pp=latest,latest_state_result_status='available' if len(past_local) else 'no_admitted_earlier_state_result',raw_movement_sd_pp=np.sqrt(rawvar),variance_multiplier=mult,raw_preferred_multiplier=pp.loc[t.geography,'raw_multiplier'],multiplier_validation_n=int(pp.loc[t.geography,'validation_n']),multiplier_validation_years=pp.loc[t.geography,'validation_years'],prior_sd_pp=np.sqrt(priorvar),posterior_sd_pp=sd,variance_reduction_fraction=1-postvar/priorvar,local_electoral_variance_pp2=budget-a,national_prior_variance_pp2=a+fv,national_posterior_variance_pp2=r.N_sd_pp**2,prediction_pp=mean,p_dem=t.p_dem,actual_pp=100*t.actual,absolute_error_pp=abs(mean-100*t.actual),wis_pp=t.wis_pp,brier=t.brier,coverage70=t.coverage70,coverage95=t.coverage95,outside_physical_margin_probability=float(norm.cdf((-100-mean)/sd)+norm.sf((100-mean)/sd)),**stats)
            rows.append(row)
            if r.cycle==2026 and r.model=='both':
                for year,value,weight in zip(mov['years'],x,weights):
                    if not np.isfinite(value):continue
                    hh=h.loc[(int(year),t.geography)];checks.append(bool(np.isclose(value,100*(hh.actual-hh.prior))))
                    residuals.append(dict(state=t.geography,cycle=int(year),actual_pp=100*hh.actual,prior_pp=100*hh.prior,residual_pp=value,weight=weight,weighted_squared_residual=weight*value*value,prior_recipe=ps.recipe))
    allq=pd.DataFrame(rows);current=allq[allq.cycle.eq(2026)];rs=pd.DataFrame(residuals);groups=[]
    for first in [2012,2016]:
        for (sc,model,group),q in allq[allq.cycle.between(first,2024)].groupby(['scenario','model','coverage_group']):
            groups.append(dict(first_cycle=first,scenario=sc,model=model,coverage_group=group,n=len(q),cycles=q.cycle.nunique(),mean_sd_pp=q.posterior_sd_pp.mean(),mean_variance_reduction=q.variance_reduction_fraction.mean(),mae_pp=q.groupby('cycle').absolute_error_pp.mean().mean(),brier=q.groupby('cycle').brier.mean().mean(),wis_pp=q.groupby('cycle').wis_pp.mean().mean(),coverage70=q.coverage70.mean(),coverage95=q.coverage95.mean()))
    local=pd.read_parquet(prior/'local_tuning.parquet');local=local[local.profile.eq('control')&~local.joint&local.forecast_cycle.eq(2026)&local.scenario.eq('matched_live')]
    for name,table in dict(sparse_variance_all=allq,sparse_variance_current=current,sparse_residual_history=rs,sparse_calibration_groups=pd.DataFrame(groups),current_multiplier_validation=local).items():table.to_parquet(out/f'{name}.parquet',index=False)
    result=dict(passed=bool(all(checks)),reconstruction_checks=len(checks),rows=len(allq),current_rows=len(current));v1.json_write(out/'sparse_audit.json',result)
    if not result['passed']:raise AssertionError(result)
    v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)));print(result);print(current[current.model.eq('both')].sort_values('posterior_sd_pp',ascending=False)[['state','sample_count','recent_firms','prior_mean_pp','prediction_pp','raw_movement_sd_pp','variance_multiplier','posterior_sd_pp','p_dem','variance_reduction_fraction']].head(12).round(4).to_string(index=False));return result

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('artifact',type=Path);a=p.parse_args();build(a.artifact,Path(__file__).resolve().parents[1])
