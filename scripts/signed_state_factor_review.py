"""Factor stability, exact outcome scenarios and artifact reconstruction."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import signed_state_factor as sf
import simple_bayesian_polling as v1
import simple_national_model as normal
import national_tails_waves as chamber
from current_conditional_scenarios import sqrt_psd,gaussian_prob


def get_poll(work,sc,year):
    pf=np.load(work/f'fits/{sc}_{year}_poll.npz');return normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)

def condition_joint(mean,cov,ids,values):
    ids=np.asarray(ids,int);values=np.asarray(values,float);res=values-mean[ids];S=cov[np.ix_(ids,ids)];distance=float(res@np.linalg.solve(S,res));m,C,_=v1.normal_update(mean,cov,ids,values,np.zeros((len(ids),len(ids))));m[ids]=values;C[ids,:]=0;C[:,ids]=0
    return m,(C+C.T)/2,distance


def build(out,lab):
    out,lab=Path(out),Path(lab);st=json.loads((out/'settings.json').read_text());work=Path(st['working']);roster=pd.read_parquet(Path(st['upstream'])/'full_seat_ledger.parquet');p=pd.read_parquet(out/'predictions.parquet');f=pd.read_parquet(out/'folds.parquet');cur=f[f.cycle.eq(2026)];poll=get_poll(work,'matched_live',2026);stability=[];stability_loadings=[];stability_starts=[];stability_predictions=[]
    for base in sorted(cur.base_model.unique()):
        r=cur[cur.model.eq(base+'__selected')].iloc[0];q=p[p.cycle.eq(2026)&p.model.eq(r.model)].sort_values('target_id').reset_index(drop=True);fit=dict(np.load(out/r.fit_path));fit['a']=float(fit['a']);b=fit['loading'];xx=fit['training_values'];noise=fit['training_noise'];weights=fit['training_weights'];years=fit['years'];fm=fit['factor_training_means']
        for omit in years[-3:]:
            keep=years!=omit;new=sf.fit_loading(xx[keep],noise[keep],weights[keep],fit['budget'],fit['a'],fm[keep]);nb=new['b'];sign=-1 if np.dot(b,nb)<0 else 1;nb=sign*nb;u=nb/np.sqrt(fit['budget']-fit['a']);den=np.linalg.norm(b)*np.linalg.norm(nb);cosine=float(b@nb/den) if den else np.nan
            path=f'fits/stability_{base}_omit{omit}.npz';np.savez_compressed(out/path,b=nb,u=u,years=years[keep],training_values=xx[keep],training_noise=noise[keep],training_weights=weights[keep],feature_means=fm[keep]);stability_starts.extend(dict(base_model=base,omitted_cycle=int(omit),**x) for x in new['starts']);stability_loadings.extend(dict(base_model=base,omitted_cycle=int(omit),state=s,baseline_loading_pp=b[i],deleted_loading_pp=nb[i],difference_pp=nb[i]-b[i]) for i,s in enumerate(v1.STATES))
            for label,lam in [('selected',float(r.lambda_value)),('fixed025',.25)]:
                oldpred,_,oldarrays=sf.predict(q,fit,poll,b,lam);newpred,stats,arrays=sf.predict(q,fit,poll,nb,lam);R0=oldarrays['covariance']/np.sqrt(np.outer(np.diag(oldarrays['covariance']),np.diag(oldarrays['covariance'])));R=arrays['covariance']/np.sqrt(np.outer(np.diag(arrays['covariance']),np.diag(arrays['covariance'])));rr=roster[roster.scenario.eq('matched_live')&roster.cycle.eq(2026)];rng=np.random.default_rng(sf.CONFIG['seed']+2026);draws=newpred.prediction_pp.to_numpy()+rng.normal(size=(30000,len(q)))@np.linalg.cholesky(arrays['covariance']).T;ss,counts=chamber.seat_summary(rr,q,newpred,draws)
                stability.append(dict(base_model=base,omitted_cycle=int(omit),version=label,lambda_value=lam,loading_cosine=cosine,max_loading_change_pp=float(abs(nb-b).max()),sign_changes_over1pp=int(((nb*b<0)&(abs(b)>1)&(abs(nb)>1)).sum()),max_margin_change_pp=float(abs(newpred.prediction_pp-oldpred.prediction_pp).max()),max_probability_change_pp=float(100*abs(newpred.p_dem-oldpred.p_dem).max()),max_correlation_change=float(abs(R-R0).max()),objective_gain=new['zero_objective']-new['objective'],fit_path=path,expected_D_exact=ss['expected_D_exact'],point_D=ss['point_D'],D_lo70=ss['D_lo70'],D_hi70=ss['D_hi70']))
                stability_predictions.append(newpred[['target_id','geography','prediction_pp','p_dem','posterior_sd_pp']].assign(base_model=base,omitted_cycle=int(omit),version=label,lambda_value=lam))
        print('stability',base,flush=True)
    # Exact conditioning of the posterior, including the latent national and signed factors.
    scenarios=[];scenario_states=[];scenario_checks=[];base='repaired_both';selected=cur[cur.model.eq(base+'__selected')].iloc[0]
    for label,name in [('baseline',base+'__lambda0'),('fixed025',base+'__lambda0.25'),('selected',base+'__selected')]:
        r=cur[cur.model.eq(name)].iloc[0];q=p[p.cycle.eq(2026)&p.model.eq(name)].sort_values('target_id').reset_index(drop=True);z=np.load(out/r.forecast_path);m=z['joint_mean'];C=z['joint_covariance'];fit=np.load(out/r.fit_path);h=np.sqrt(float(r.lambda_value))*fit['loading'][[v1.STATES.index(s) for s in q.geography]];n=len(q);tx=int(np.flatnonzero(q.geography.eq('TX'))[0]);oh=int(np.flatnonzero(q.geography.eq('OH'))[0]);rng=np.random.default_rng(292026);draw_z=rng.normal(size=(sf.CONFIG['scenario_draws'],n));baseprob=q.p_dem.to_numpy();rr=roster[roster.scenario.eq('matched_live')&roster.cycle.eq(2026)]
        conditions=[('unconditioned',[],[])]+[(f'TX_Dplus{v}',[tx],[float(v)]) for v in [1,5,10]]+[('TX_OH_both_surprise_D5',[tx,oh],[m[tx]+5,m[oh]+5]),('TX_D5_OH_R5_surprises',[tx,oh],[m[tx]+5,m[oh]-5])]
        for name,ids,values in conditions:
            cm,cc,md2=condition_joint(m,C,ids,values) if ids else (m.copy(),C.copy(),0.);prob=gaussian_prob(cm[:n],cc[:n,:n]);draws=cm[:n]+draw_z@sqrt_psd(cc[:n,:n]).T;pred=q.copy();pred['prediction_pp']=cm[:n];pred['p_dem']=prob;ss,counts=chamber.seat_summary(rr,q,pred,draws);own=float((prob-baseprob)[ids].sum());others=float((prob-baseprob).sum()-own);Nshift=cm[-2]-m[-2];Zshift=cm[-1]-m[-1]
            scenarios.append(dict(version=label,lambda_value=r.lambda_value,scenario=name,conditioned_states=','.join(q.geography.iloc[ids]),values_pp=','.join(map(str,values)),mahalanobis_distance=np.sqrt(md2),N_mean_pp=cm[-2],N_shift_pp=Nshift,Z_mean=cm[-1],Z_shift=Zshift,N_sd_pp=np.sqrt(max(cc[-2,-2],0)),Z_sd=np.sqrt(max(cc[-1,-1],0)),own_expected_seat_change=own,other_expected_seat_change=others,expected_D_exact=ss['expected_D_exact'],point_D=ss['point_D'],D_lo70=ss['D_lo70'],D_hi70=ss['D_hi70']))
            sq=q[['target_id','geography']].copy();sq=sq.assign(version=label,lambda_value=r.lambda_value,scenario=name,baseline_mean_pp=m[:n],prediction_pp=cm[:n],margin_change_pp=cm[:n]-m[:n],p_dem=prob,probability_change_pp=100*(prob-baseprob),national_shift_pp=Nshift,pattern_shift_pp=h*Zshift,local_shift_pp=cm[:n]-m[:n]-Nshift-h*Zshift);scenario_states.append(sq)
            err=abs((draws>0).mean(0)-prob);se=np.sqrt(prob*(1-prob)/len(draws));scenario_checks.append(dict(version=label,scenario=name,passed=bool(np.linalg.eigvalsh(cc).min()>-1e-8 and np.all(err<6*se+.0002) and np.allclose(cm[ids],values) and abs(ss['expected_D_exact']-ss['fixed_D']-prob.sum())<1e-8)))
            np.savez_compressed(out/f'forecasts/scenario_{label}_{name}.npz',joint_mean=cm,joint_covariance=cc,target_ids=q.target_id.to_numpy(str),p_dem=prob,seat_count_frequency=np.bincount(counts,minlength=101))
        print('scenarios',label,flush=True)
    # Current strongest positive and strongest-magnitude links, with signed correlations.
    links=[]
    for r in cur.itertuples():
        q=p[p.cycle.eq(2026)&p.model.eq(r.model)].sort_values('target_id').reset_index(drop=True);a=np.load(out/r.forecast_path);C=a['covariance'];R=C/np.sqrt(np.outer(np.diag(C),np.diag(C)));pos=R.copy();np.fill_diagonal(pos,-np.inf);ab=abs(R);np.fill_diagonal(ab,-np.inf);jp=pos.argmax(1);ja=ab.argmax(1)
        for i,t in enumerate(q.itertuples()):links.append(dict(model=r.model,base_model=r.base_model,lambda_value=r.lambda_value,state=t.geography,p_dem=t.p_dem,mean_pp=t.prediction_pp,most_positive_state=q.geography.iloc[jp[i]],positive_rho=R[i,jp[i]],strongest_absolute_state=q.geography.iloc[ja[i]],signed_rho=R[i,ja[i]],negative_links=int((np.delete(R[i],i)<0).sum())))
    for name,table in dict(stability=pd.DataFrame(stability),stability_loadings=pd.DataFrame(stability_loadings),stability_starts=pd.DataFrame(stability_starts),stability_predictions=pd.concat(stability_predictions,ignore_index=True),scenario_summary=pd.DataFrame(scenarios),scenario_states=pd.concat(scenario_states,ignore_index=True),scenario_checks=pd.DataFrame(scenario_checks),current_links=pd.DataFrame(links)).items():table.to_parquet(out/f'{name}.parquet',index=False)
    v1.manifest(out);audit(out,lab)
    from signed_state_factor_checks import complete
    complete(out,lab)
    v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)));print('REVIEW COMPLETE',out,flush=True)

def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);st=json.loads((out/'settings.json').read_text());p=pd.read_parquet(out/'predictions.parquet');f=pd.read_parquet(out/'folds.parquet');s=pd.read_parquet(out/'seats.parquet');di=pd.read_parquet(out/'fit_diagnostics.parquet');starts=pd.read_parquet(out/'optimizer_starts.parquet');load=pd.read_parquet(out/'loadings.parquet');t=pd.read_parquet(out/'tuning.parquet');checks=dict(sources=all(v1.verify(path)==h for path,h in st['sources'].items()),previous_notebooks=all(v1.sha(lab/n)==h for n,h in st['old_notebooks'].items()),working_designation=v1.sha(lab/'WORKING_MODEL.json')==st['working_sha256'],zero_reproduction=json.loads((out/'reproduction.json').read_text())['passed'],training_past=bool(di.training_max_cycle.lt(di.cycle).all()),current_labels_missing=bool(p[p.cycle.eq(2026)][['actual','wis_pp','brier']].isna().all().all()),unique=not p.duplicated(['scenario','model','target_id']).any(),probabilities=bool(p.p_dem.between(0,1).all()),centered_loadings=bool(load.groupby(['base','scenario','cycle']).loading_pp.sum().abs().lt(1e-6).all()),unsupported_zero=bool(load[~load.eligible].loading_pp.eq(0).all()),bounded=bool(load.standardized_loading.abs().le(.950001).all()),nonzero_optimizer_success=bool(starts[starts.start.ne('zero')].groupby(['base','scenario','cycle']).success.any().all()))
    reconstruction=[];marginals=[];account=[];originals=[];objective=[];optimizer=[];cache={};sourcecache={}
    for r in di.itertuples():
        fit=np.load(out/r.path);source=np.load(Path(r.source)/r.source_fit);originals.append(all(np.array_equal(fit[k],source[k],equal_nan=True) for k in ['budget','training_values','training_noise','training_weights','years','X','z','beta_mean','beta_covariance']));blocks=[];y=fit['training_values']-fit['factor_training_means'][:,None]
        for row,n,w in zip(y,fit['training_noise'],fit['training_weights']):
            ids=np.flatnonzero(np.isfinite(row));blocks.append((ids,row[ids],n[ids],w))
        value,_=sf.factor_objective(fit['loading_u'],blocks,fit['budget']-float(fit['a']),float(fit['a']));objective.append(np.isclose(value,r.objective,atol=1e-6));sg=starts[starts.base.eq(r.base)&starts.scenario.eq(r.scenario)&starts.cycle.eq(r.cycle)&starts.success];optimizer.append(abs(sg.objective.min()-r.objective)<1e-6)
    for r in f.itertuples():
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id').reset_index(drop=True);fit=dict(np.load(out/r.fit_path));fit['a']=float(fit['a']);key=(r.scenario,r.cycle)
        if key not in cache:cache[key]=get_poll(Path(st['working']),*key)
        expected,stats,z=sf.predict(q,fit,cache[key],fit['loading'],float(r.lambda_value));saved=np.load(out/r.forecast_path);reconstruction.append(np.allclose(expected[['prediction_pp','p_dem']],q[['prediction_pp','p_dem']]) and np.allclose(z['joint_covariance'],saved['joint_covariance']) and np.linalg.eigvalsh(saved['joint_covariance']).min()>-1e-8);ids=[v1.STATES.index(x) for x in q.geography];fv=float(fit['z']@fit['beta_covariance']@fit['z']);marginals.append(np.allclose(np.diag(saved['prior_covariance']),fit['budget'][ids]+fv));ss=s[s.scenario.eq(r.scenario)&s.cycle.eq(r.cycle)&s.model.eq(r.model)].iloc[0];account.append(abs(ss.expected_D_exact-ss.fixed_D-q.p_dem.sum())<1e-8 and saved['seat_count_frequency'].sum()==sf.CONFIG['draws'])
    selected=[]
    for r in t.itertuples():
        years=sorted(p.loc[p.base_model.eq(r.base_model)&p.scenario.eq(r.scenario)&p.cycle.lt(r.cycle)&p.actual.notna(),'cycle'].unique())[-3:];order=[r.base_model+f'__lambda{x:g}' for x in sf.LAMBDAS];hist=p[p.base_model.eq(r.base_model)&p.scenario.eq(r.scenario)&p.cycle.isin(years)&p.model.isin(order)];scores=hist.groupby(['model','cycle']).wis_pp.mean().groupby('model').mean();chosen=min(order,key=lambda x:(scores[x],order.index(x))) if len(years)==3 else order[0];selected.append(chosen==r.selected_model and ','.join(map(str,years))==r.validation_years)
    checks.update(source_parameters_preserved=bool(all(originals)),objective_reproduces=bool(all(objective)),best_converged_start=bool(all(optimizer)),forecasts_reproduce=bool(all(reconstruction)),marginal_prior_variance_preserved=bool(all(marginals)),seat_accounting=bool(all(account)),past_selector_reproduces=bool(all(selected)),scenario_checks=bool(pd.read_parquet(out/'scenario_checks.parquet').passed.all()))
    result=dict(passed=bool(all(checks.values())),checks={k:bool(v) for k,v in checks.items()},forecasts=len(f),state_rows=len(p),factor_fits=len(di),stability_fits=pd.read_parquet(out/'stability.parquet')[['base_model','omitted_cycle']].drop_duplicates().shape[0],scenario_count=len(pd.read_parquet(out/'scenario_summary.parquet')),old_notebooks=len(st['old_notebooks']));v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError(checks)
    print(result,flush=True);return result
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('artifact',type=Path);a=p.parse_args();build(a.artifact,Path(__file__).resolve().parents[1])
