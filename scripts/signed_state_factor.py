"""One regularized signed movement factor; fixed marginal variances and national fit."""
from pathlib import Path
from datetime import datetime,timezone
import json
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm
import simple_bayesian_polling as v1
import simple_national_model as normal
import national_feature_prior as feature
import coverage_balance as scoring
import national_factor_review as national
import national_tails_waves as chamber
from final_baseline_experiments import cycle_metrics

LAMBDAS=[0.,.1,.25,.5]
CONFIG=dict(ridge=4.,loading_bound=.95,min_state_observations=3,fit_max_iterations=1500,fit_ftol=1e-9,seed=197139,draws=30000,stability_cycles=3,scenario_draws=100000)

def factor_objective(u,blocks,local,a,ridge=4.):
    """Exact marginal likelihood integrates the two cycle-specific Gaussian factors."""
    root=np.sqrt(local);b=u*root;value=.5*ridge*(u@u);grad=ridge*u.copy()
    for ids,y,noise,w in blocks:
        bb=b[ids];d=local[ids]-bb*bb+noise
        if np.any(d<=0):return 1e100,np.zeros_like(u)
        U=np.column_stack([np.full(len(ids),np.sqrt(a)),bb]);dinv=1/d;A=np.eye(2)+U.T@(dinv[:,None]*U);inv=np.diag(dinv)-(dinv[:,None]*U)@np.linalg.solve(A,(U.T*dinv));yy=inv@y
        value+=.5*w*(len(ids)*np.log(2*np.pi)+np.log(d).sum()+np.linalg.slogdet(A)[1]+y@yy)
        M=inv-np.outer(yy,yy);grad[ids]+=w*(M@bb-np.diag(M)*bb)*root[ids]
    return float(value),grad

def fit_loading(values,noise,weights,budget,a,feature_means=None,seed=291029):
    x=np.asarray(values,float);noise=np.asarray(noise,float);weights=np.asarray(weights,float);local=np.asarray(budget,float)-a
    if x.shape!=noise.shape or x.ndim!=2 or len(weights)!=len(x) or x.shape[1]!=len(local):raise ValueError('Invalid training shape')
    if not np.array_equal(np.isfinite(x),np.isfinite(noise)) or (local<=0).any() or (weights<=0).any():raise ValueError('Invalid missingness/variance/weights')
    fm=np.zeros(len(x)) if feature_means is None else np.asarray(feature_means,float)
    if fm.shape!=(len(x),) or not np.isfinite(fm).all():raise ValueError('Invalid conditional feature means')
    y=x-fm[:,None];counts=np.isfinite(y).sum(0);eligible=counts>=CONFIG['min_state_observations'];root=np.sqrt(local);mass=(np.isfinite(y)*weights[:,None]).sum(0);blocks=[]
    for row,n,w in zip(y,noise,weights):
        ids=np.flatnonzero(np.isfinite(row));blocks.append((ids,row[ids],n[ids],w))
    penalty=CONFIG['ridge'];zero=np.zeros(len(local));base,_=factor_objective(zero,blocks,local,a,penalty)
    if eligible.sum()<2:return dict(b=zero,u=zero,counts=counts,mass=mass,eligible=eligible,objective=base,zero_objective=base,success=True,starts=[dict(start='zero_only',objective=base,success=True,iterations=0)],feature_means=fm)
    constraint=root/root.sum();bounds=[(-CONFIG['loading_bound'],CONFIG['loading_bound']) if e else (0.,0.) for e in eligible]
    def start(v):
        b=root*v;b[~eligible]=0;b[eligible]-=b[eligible].mean();u=b/root;maximum=np.max(abs(u));return u*(.6/maximum) if maximum>0 else u
    # Only initialization uses conditional expected national residuals; fitting
    # always uses the full marginal likelihood above.
    residual=np.full_like(y,np.nan)
    for i,(ids,row,n,w) in enumerate(blocks):
        inv=1/(local[ids]+n);Nm=a*(inv@row)/(1+a*inv.sum());residual[i,ids]=(row-Nm)/root[ids]
    mask=np.isfinite(residual);z=np.nan_to_num(residual);den=(mask*weights[:,None]).T@mask;scatter=(z*weights[:,None]).T@z;scatter=np.divide(scatter,den,out=np.zeros_like(scatter),where=den>0);scatter[~eligible,:]=0;scatter[:,~eligible]=0
    _,ev=np.linalg.eigh((scatter+scatter.T)/2);rng=np.random.default_rng(seed);initial=[('zero',zero)]+[(f'eigen{k}',start(ev[:,-k])) for k in [1,2,3]]+[('random',start(rng.normal(size=len(local))))]
    candidates=[(base,zero.copy(),'zero')];records=[]
    for label,init in initial:
        if label=='zero':records.append(dict(start=label,objective=base,success=True,iterations=0,message='Exact no-factor stationary control'));continue
        result=minimize(lambda u:factor_objective(u,blocks,local,a,penalty),init,jac=True,method='SLSQP',bounds=bounds,constraints=[dict(type='eq',fun=lambda u:constraint@u,jac=lambda u:constraint)],options={'maxiter':CONFIG['fit_max_iterations'],'ftol':CONFIG['fit_ftol']})
        feasible=abs(constraint@result.x)<1e-7 and np.max(abs(result.x))<=CONFIG['loading_bound']+1e-7
        records.append(dict(start=label,objective=float(result.fun),success=bool(result.success and feasible),iterations=int(result.nit),message=str(result.message)))
        if result.success and feasible:candidates.append((float(result.fun),result.x.copy(),label))
    value,u,label=min(candidates,key=lambda t:t[0]);b=u*root
    if b[np.argmax(abs(b))]<0:b=-b;u=-u
    return dict(b=b,u=u,counts=counts,mass=mass,eligible=eligible,objective=value,zero_objective=base,success=True,selected_start=label,starts=records,feature_means=fm)

def predict(test,fit,poll,b,lam):
    if not 0<=lam<=1:raise ValueError('lambda must be in [0,1]')
    budget=fit['budget'];a=float(fit['a']);b=np.asarray(b,float)
    if b.shape!=budget.shape or np.any(b*b>budget-a+1e-8):raise ValueError('Loading exceeds local variance budget')
    si=np.array([v1.STATES.index(s) for s in test.geography]);obs=np.flatnonzero(test.q_pp.notna());so=si[obs];z=fit['z'];f=float(z@fit['beta_mean']);fv=float(z@fit['beta_covariance']@z);g=a+fv;h=np.sqrt(lam)*b[si];local=budget[si]-a-h*h
    K=np.diag(local)+g*np.ones((len(test),len(test)))+np.outer(h,h);mu=100*test.prior.to_numpy()+f
    R=poll['covariance'][np.ix_(so,so)]+poll['bias_covariance'][np.ix_(so,so)]+np.diag(16/test.firm_mass.to_numpy()[obs]);value=test.q_pp.to_numpy()[obs]-poll['bias_mean'][so]
    prior_cross=np.column_stack([np.full(len(test),g),h]);factor_prior=np.diag([g,1.]);factor_mean=np.array([f,0.]);joint_mu=np.r_[mu,factor_mean];joint_K=np.block([[K,prior_cross],[prior_cross.T,factor_prior]])
    joint_mean,joint_cov,ll=v1.normal_update(joint_mu,joint_K,obs,value,R);mean=joint_mean[:-2];C=joint_cov[:-2,:-2];latent_mean=joint_mean[-2:];latent_cov=joint_cov[-2:,-2:];sd=np.sqrt(np.diag(C))
    local_update=np.zeros(len(test))
    if len(obs):local_update[obs]=local[obs]*np.linalg.solve(K[np.ix_(obs,obs)]+R,value-mu[obs])
    np.testing.assert_allclose(mean,100*test.prior.to_numpy()+latent_mean[0]+h*latent_mean[1]+local_update,atol=1e-8)
    p=test.copy();drop=['prior_local_sd_pp','poll_surprise_pp','poll_local_sd_pp','bias_posterior_adjustment_pp','local_poll_error_pp','old_historical_bias_pp','bias_change_pp'];p=p.drop(columns=[k for k in drop if k in p]);p['prediction_pp']=mean;p['prediction']=mean/100;p['median_pp']=mean;p['posterior_sd_pp']=sd;p['p_dem']=norm.cdf(mean/sd);p['log_predictive_density']=norm.logpdf(100*p.actual,mean,sd);p['outside_margin_bounds_probability']=norm.cdf((-100-mean)/sd)+norm.sf((100-mean)/sd)
    for level in scoring.LEVELS:
        width=norm.ppf((1+level/100)/2)*sd;p[f'lo{level}_pp']=mean-width;p[f'hi{level}_pp']=mean+width
    p['prior_sd_pp']=np.sqrt(np.diag(K));p['national_movement_pp']=latent_mean[0];p['signed_loading_pp']=b[si];p['signed_pattern_contribution_pp']=h*latent_mean[1];p['local_electoral_update_pp']=local_update;p['historical_bias_pp']=poll['bias_mean'][si];p['corrected_poll_pp']=p.q_pp-p.historical_bias_pp;p['national_poll_error_pp']=0.;p['feature_prior_mean_pp']=f;p['feature_prior_sd_pp']=np.sqrt(fv)
    stats=dict(N_mean_pp=float(latent_mean[0]),N_sd_pp=float(np.sqrt(latent_cov[0,0])),Z_mean=float(latent_mean[1]),Z_sd=float(np.sqrt(latent_cov[1,1])),NZ_cov=float(latent_cov[0,1]),log_evidence=ll)
    arrays=dict(mean=mean,covariance=C,prior_mean=mu,prior_covariance=K,joint_mean=joint_mean,joint_covariance=joint_cov,loadings=b,local_variance=local)
    return scoring.score_rows(p),stats,arrays

def load_bases(lab):
    paths=dict(original=lab/'reports/national_feature_prior/20260920T013619.322700Z',repaired=lab/'reports/prior_center_repair/20260920T044021.105794Z');rows=[]
    for recipe,src in paths.items():
        p=pd.read_parquet(src/'predictions.parquet');f=pd.read_parquet(src/'folds.parquet')
        for family in ['none','both']:
            name=family if recipe=='original' else family+'__decay4_centered__state'
            for r in f[f.model.eq(name)].itertuples():
                q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(name)].sort_values('target_id').reset_index(drop=True);fit=dict(np.load(src/r.fit_path));fit['a']=float(fit['a']);rows.append(dict(base=recipe+'_'+family,family=family,recipe=recipe,scenario=r.scenario,cycle=int(r.cycle),test=q,fit=fit,source=str(src),source_fit=r.fit_path,source_forecast=r.forecast_path))
    return rows,paths

def build(lab):
    lab=Path(lab).resolve();bases,paths=load_bases(lab);work=lab/'reports/simple_national_model/20260920T000314.601869Z';up=lab/'reports/official_repair_review/20260919T172552.860612Z';roster=pd.read_parquet(up/'full_seat_ledger.parquet')
    out=lab/'reports/signed_state_factor'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for name in ['fits','forecasts','recipe']:(out/name).mkdir(parents=True,exist_ok=True)
    st=dict(config=CONFIG,lambdas=LAMBDAS,sources={str(x):v1.verify(x) for x in [*paths.values(),work,up]},working=str(work),upstream=str(up),old_notebooks={p.name:v1.sha(p) for p in lab.glob('*.ipynb')},working_sha256=v1.sha(lab/'WORKING_MODEL.json'),data_as_of='2026-09-17',promotion=False);v1.json_write(out/'settings.json',st);print('OUTPUT',out,flush=True)
    preds=[];seats=[];folds=[];diag=[];starts=[];loadings=[];repro=[];pollcache={}
    for case in sorted(bases,key=lambda r:(r['base'],r['scenario'],r['cycle'])):
        base,sc,year=case['base'],case['scenario'],case['cycle'];fit=case['fit'];q=case['test'];key=(sc,year)
        if key not in pollcache:
            pf=np.load(work/f'fits/{sc}_{year}_poll.npz');pollcache[key]=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        poll=pollcache[key];fm=fit['X']@fit['beta_mean'];learn=fit_loading(fit['training_values'],fit['training_noise'],fit['training_weights'],fit['budget'],fit['a'],fm)
        fp=f'fits/{base}_{sc}_{year}.npz';np.savez_compressed(out/fp,**fit,loading=learn['b'],loading_u=learn['u'],counts=learn['counts'],mass=learn['mass'],eligible=learn['eligible'],factor_training_means=fm)
        diag.append(dict(base=base,scenario=sc,cycle=year,training_max_cycle=int(fit['years'].max()),training_cycles=len(fit['years']),supported_states=int(learn['eligible'].sum()),objective=learn['objective'],zero_objective=learn['zero_objective'],improvement=learn['zero_objective']-learn['objective'],selected_start=learn.get('selected_start','zero'),all_nonzero_starts_converged=all(x['success'] for x in learn['starts']),path=fp,source=case['source'],source_fit=case['source_fit']))
        starts.extend(dict(base=base,scenario=sc,cycle=year,**x) for x in learn['starts'])
        loadings.extend(dict(base=base,scenario=sc,cycle=year,state=state,loading_pp=learn['b'][i],standardized_loading=learn['u'][i],n=int(learn['counts'][i]),mass=learn['mass'][i],eligible=bool(learn['eligible'][i])) for i,state in enumerate(v1.STATES))
        rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));z=rng.standard_normal((CONFIG['draws'],len(q)))
        for lam in LAMBDAS:
            p,stats,arrays=predict(q,fit,poll,learn['b'],lam);name=base+f'__lambda{lam:g}';p=p.assign(model=name,base_model=base,lambda_value=lam);preds.append(p);draws=p.prediction_pp.to_numpy()+z@np.linalg.cholesky(arrays['covariance']).T;ss,counts=chamber.seat_summary(roster[roster.scenario.eq(sc)&roster.cycle.eq(year)],q,p,draws);freq=np.bincount(counts,minlength=101);ss.update(scenario=sc,cycle=year,model=name,base_model=base,lambda_value=lam);seats.append(scoring.seat_scores(ss,freq));path=f'forecasts/{base}_{sc}_{year}_lambda{lam:g}.npz';np.savez_compressed(out/path,**arrays,target_ids=q.target_id.to_numpy(str),seat_count_frequency=freq)
            folds.append(dict(base_model=base,scenario=sc,cycle=year,model=name,lambda_value=lam,fit_path=fp,forecast_path=path,**stats))
            if lam==0:
                source=np.load(Path(case['source'])/case['source_forecast']);repro.append(dict(base=base,scenario=sc,cycle=year,passed=bool(np.allclose(p[['prediction_pp','p_dem']],q[['prediction_pp','p_dem']],atol=1e-9)&np.allclose(arrays['covariance'],source['covariance'])&np.array_equal(freq,source['seat_count_frequency']))))
        print(base,sc,year,'objective gain',round(learn['zero_objective']-learn['objective'],4),flush=True)
    p=pd.concat(preds,ignore_index=True);s=pd.DataFrame(seats);f=pd.DataFrame(folds);sp=[];ss=[];sf=[];tuning=[]
    for (base,sc,year),g in p.groupby(['base_model','scenario','cycle']):
        years=sorted(p.loc[p.base_model.eq(base)&p.scenario.eq(sc)&p.cycle.lt(year)&p.actual.notna(),'cycle'].unique())[-3:];order=[base+f'__lambda{x:g}' for x in LAMBDAS];past=p[p.base_model.eq(base)&p.scenario.eq(sc)&p.cycle.isin(years)];scores=past.groupby(['model','cycle']).wis_pp.mean().groupby('model').mean();chosen=min(order,key=lambda x:(scores[x],order.index(x))) if len(years)==3 else order[0]
        sp.append(g[g.model.eq(chosen)].assign(model=base+'__selected',selected_model=chosen));ss.append(s[s.scenario.eq(sc)&s.cycle.eq(year)&s.model.eq(chosen)].assign(model=base+'__selected',selected_model=chosen));sf.append(f[f.scenario.eq(sc)&f.cycle.eq(year)&f.model.eq(chosen)].assign(model=base+'__selected',selected_model=chosen));tuning.append(dict(base_model=base,scenario=sc,cycle=year,selected_model=chosen,validation_years=','.join(map(str,years))))
    p=pd.concat([p,*sp],ignore_index=True);s=pd.concat([s,*ss],ignore_index=True);f=pd.concat([f,*sf],ignore_index=True)
    for name,df in dict(predictions=p,seats=s,folds=f,fit_diagnostics=pd.DataFrame(diag),optimizer_starts=pd.DataFrame(starts),loadings=pd.DataFrame(loadings),tuning=pd.DataFrame(tuning),summary=scoring.summarize_scores(p),chamber_summary=national.chamber_summary(s),cycle_scores=cycle_metrics(p)).items():df.to_parquet(out/f'{name}.parquet',index=False)
    v1.json_write(out/'reproduction.json',dict(passed=all(x['passed'] for x in repro),folds=repro))
    for path in (lab/'scripts').glob('*.py'):(out/'recipe'/path.name).write_bytes(path.read_bytes())
    v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)));print('FORECASTS COMPLETE',out,flush=True);return out
if __name__=='__main__':build(Path(__file__).resolve().parents[1])
