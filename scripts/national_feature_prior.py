"""Small Bayesian feature prior for national movement; exact Gaussian integration."""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.stats import norm
import simple_bayesian_polling as v1
import simple_national_model as normal
import working_election_model as working
import coverage_balance as scoring
import national_factor_review as national
import national_tails_waves as chamber
import poll_timing_student as timing
from recency_state_baselines import WeightedScoreDesign
from feature_scores import CONFIG_PATH

FAMILIES={'momentum':['economy_momentum_wh'],'approval':['approval_wh'],'both':['economy_momentum_wh','approval_wh']}
TAUS=[0,1,3,6]
CONFIG=dict(tau_sd_pp=TAUS,validation_cycles=3,seed=197139,draws=30000,profile_points=33,as_of='2026-09-17',working_poll_half_life=30)


def regression_at_a(values,noise,weights,budget,X,tau,a):
    """Integrated beta evidence from one joint Gaussian block per historical cycle."""
    y=np.asarray(values,float);noise=np.asarray(noise,float);w=np.asarray(weights,float);V=np.asarray(budget,float);X=np.asarray(X,float)
    if y.shape!=noise.shape or y.ndim!=2 or X.ndim!=2 or len(X)!=len(y) or len(w)!=len(y) or y.shape[1]!=len(V):raise ValueError('Inconsistent arrays')
    if not np.array_equal(np.isfinite(y),np.isfinite(noise)) or not np.isfinite(X).all() or not np.isfinite(w).all() or np.any(w<=0) or np.any(noise[np.isfinite(noise)]<0):raise ValueError('Invalid training data')
    if not np.isfinite(tau) or tau<0 or a<0 or a>=V.min():raise ValueError('Invalid scale/allocation')
    mask=np.isfinite(y);d=V[None,:]-a+noise;inv=np.where(mask,1/d,0.);yy=np.nan_to_num(y)
    sums=inv.sum(axis=1);rhs=(inv*yy).sum(axis=1);quad=(inv*yy*yy).sum(axis=1);den=1+a*sums
    ld=np.where(mask,np.log(d),0.).sum(axis=1)+np.log(den)
    constant=-.5*np.sum(w*(mask.sum(axis=1)*np.log(2*np.pi)+ld+quad-a*rhs*rhs/den))
    precision_per_cycle=sums/den;rhs_per_cycle=rhs/den;k=X.shape[1]
    if tau==0 or k==0:
        beta=np.zeros(k);cov=np.zeros((k,k));ll=constant
    else:
        precision=np.eye(k)/tau**2+X.T@((w*precision_per_cycle)[:,None]*X);b=X.T@(w*rhs_per_cycle)
        cov=np.linalg.inv(precision);beta=cov@b
        ll=constant-.5*k*np.log(tau**2)-.5*np.linalg.slogdet(precision)[1]+.5*b@beta
    return dict(beta_mean=beta,beta_covariance=cov,log_evidence=float(ll),cycle_precision=precision_per_cycle,cycle_observation=rhs_per_cycle/precision_per_cycle)


def fit_feature(values,noise,weights,budget,X,tau):
    if tau==0 or X.shape[1]==0:
        old=normal.fit_common(values,noise,weights,budget)
        d=regression_at_a(values,noise,weights,budget,X,0,old['common_variance'])
        return dict(**d,a=old['common_variance'],profile_grid=old['profile_grid'],profile_nll=old['profile_nll'],optimizer_success=old['optimizer_success'],at_lower=old['at_lower'],at_upper=old['at_upper'])
    upper=float(np.min(budget)*(1-1e-8));grid=np.linspace(0,upper,CONFIG['profile_points'])
    objective=lambda a:-regression_at_a(values,noise,weights,budget,X,tau,a)['log_evidence']
    scores=np.array([objective(a) for a in grid]);options=[(scores[0],0.),(scores[-1],upper)];ok=[]
    for i in range(1,len(grid)-1):
        if scores[i]<=scores[i-1] and scores[i]<=scores[i+1]:
            r=minimize_scalar(objective,bounds=(grid[i-1],grid[i+1]),method='bounded',options={'xatol':1e-8});options.append((r.fun,r.x));ok.append(r.success)
    _,a=min(options);d=regression_at_a(values,noise,weights,budget,X,tau,a)
    return dict(**d,a=float(a),profile_grid=grid,profile_nll=scores,optimizer_success=all(ok),at_lower=bool(a<1e-6),at_upper=bool(upper-a<max(1e-6,upper*1e-5)))


def predict(test,budget,poll,fit,z):
    si=np.array([v1.STATES.index(st) for st in test.geography]);obs=np.flatnonzero(test.q_pp.notna());so=si[obs]
    base=100*test.prior.to_numpy();z=np.asarray(z,float);f=float(z@fit['beta_mean']);fv=float(z@fit['beta_covariance']@z);a=fit['a'];g=a+fv;local=budget[si]-a
    K=np.diag(local)+g*np.ones((len(test),len(test)));mu=base+f
    R=poll['covariance'][np.ix_(so,so)]+poll['bias_covariance'][np.ix_(so,so)]+np.diag(16/test.firm_mass.to_numpy()[obs]);values=test.q_pp.to_numpy()[obs]-poll['bias_mean'][so]
    mean,cov,ll=v1.normal_update(mu,K,obs,values,R)
    total=0.;prec=0.;local_update=np.zeros(len(test))
    if len(obs):
        S=K[np.ix_(obs,obs)]+R;sol=np.linalg.solve(S,values-mu[obs]);total=float(sol.sum());prec=float(np.linalg.solve(S,np.ones(len(obs))).sum());local_update[obs]=local[obs]*sol
    N=f+g*total;Nvar=max(g-g*g*prec,0.)
    np.testing.assert_allclose(base+N+local_update,mean,atol=1e-9)
    p=test.copy();sd=np.sqrt(np.diag(cov));p['prediction_pp']=mean;p['prediction']=mean/100;p['median_pp']=mean;p['posterior_sd_pp']=sd;p['p_dem']=norm.cdf(mean/sd);p['log_predictive_density']=norm.logpdf(100*p.actual,mean,sd)
    for level in scoring.LEVELS:
        width=norm.ppf((1+level/100)/2)*sd;p[f'lo{level}_pp']=mean-width;p[f'hi{level}_pp']=mean+width
    p['feature_prior_mean_pp']=f;p['feature_prior_sd_pp']=np.sqrt(max(fv,0));p['national_movement_pp']=N;p['local_electoral_update_pp']=local_update
    p['historical_bias_pp']=poll['bias_mean'][si];p['corrected_poll_pp']=p.q_pp-p.historical_bias_pp;p['national_poll_error_pp']=0.
    p=p.drop(columns=[c for c in ['bias_posterior_adjustment_pp','local_poll_error_pp','old_historical_bias_pp','bias_change_pp','prior_local_sd_pp'] if c in p])
    stats=dict(feature_mean_pp=f,feature_variance_pp2=fv,residual_N_variance=a,N_prior_variance=g,N_mean_pp=N,N_sd_pp=np.sqrt(Nvar),feature_posterior_mean_pp=f+fv*total,residual_N_posterior_mean_pp=a*total,U_mean_pp=0.,log_evidence=ll)
    return scoring.score_rows(p),cov,stats,dict(prior_covariance=K,prior_mean=mu,observation_covariance=R)


def prepare_design(cal,years,weights,year):
    indexed=cal.set_index('cycle',drop=False)
    if indexed.index.duplicated().any():raise ValueError('Duplicate feature context')
    train=indexed.loc[years].reset_index(drop=True);future=indexed.loc[[year]].reset_index(drop=True)
    if train.cycle.max()>=year:raise ValueError('Future training context')
    design=WeightedScoreDesign().fit(train,weights);X,scores=design.transform(train);z,future_scores=design.transform(future,require_later=True)
    _,ledger=design.summary.transform(pd.concat([train,future],ignore_index=True))
    return design,X,z[0],scores,future_scores,ledger


def build(lab):
    lab=Path(lab).resolve();_,source,wt=working.load(lab);src=json.loads((source/'settings.json').read_text());up=Path(src['upstream'])
    if source.name!='20260920T000314.601869Z':raise ValueError('Pinned source required')
    cal=pd.read_parquet(up/'calendars.parquet');roster=pd.read_parquet(up/'full_seat_ledger.parquet')
    out=lab/'reports/national_feature_prior'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for name in ['fits','forecasts','recipe']:(out/name).mkdir(parents=True,exist_ok=True)
    print('OUTPUT',out,flush=True)
    st=dict(config=CONFIG,source=str(source),upstream=str(up),sources={str(p):v1.verify(p) for p in [source,up]},score_config_sha256=v1.sha(CONFIG_PATH),working_sha256=v1.sha(lab/'WORKING_MODEL.json'),old_notebook_hashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='NATIONAL_FEATURE_PRIOR.ipynb'},promotion=False,data_refreshed=False)
    v1.json_write(out/'settings.json',st);v1.json_write(out/'score_config.json',json.loads(CONFIG_PATH.read_text()))
    preds=[];seats=[];folds=[];coefs=[];scores=[];components=[];metadata=[];fitrows=[];profiles=[];reproductions=[]
    for r in wt['folds'].sort_values(['scenario','cycle']).itertuples():
        sc,year=r.scenario,int(r.cycle);test=wt['predictions'][wt['predictions'].scenario.eq(sc)&wt['predictions'].cycle.eq(year)].sort_values('target_id').reset_index(drop=True)
        mov=dict(np.load(source/f'fits/{sc}_{year}_movement_K1.npz'));pf=dict(np.load(source/f'fits/{sc}_{year}_poll.npz'));poll=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        values,noise,w,V,years=[mov[key] for key in ['training_values','training_noise','training_weights','budget','years']]
        design,X,z,train_scores,future_scores,ledger=prepare_design(cal[cal.scenario.eq(sc)],years,w,year)
        metadata.append(dict(scenario=sc,forecast_cycle=year,**design.metadata()))
        components.append(ledger.assign(forecast_cycle=year));scores.append(pd.concat([train_scores.assign(role='train'),future_scores.assign(role='forecast')],ignore_index=True).assign(forecast_cycle=year))
        rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));normal_draws=rng.standard_normal((CONFIG['draws'],len(test)))
        basefit=fit_feature(values,noise,w,V,np.empty((len(years),0)),0)
        for family,requested in [('none',[]),*FAMILIES.items()]:
            active=[c for c in requested if c in design.active];indices=[design.active.index(c) for c in active];xx=X[:,indices];zz=z[indices]
            for tau in ([0] if family=='none' else TAUS):
                fit=basefit if family=='none' else (dict(basefit,beta_mean=np.zeros(len(active)),beta_covariance=np.zeros((len(active),len(active)))) if tau==0 else fit_feature(values,noise,w,V,xx,tau))
                name='none' if family=='none' else f'{family}_tau{tau}';fp=f'fits/{sc}_{year}_{name}.npz'
                np.savez_compressed(out/fp,**{key:value for key,value in fit.items() if isinstance(value,np.ndarray)},a=fit['a'],tau=tau,training_values=values,training_noise=noise,training_weights=w,years=years,budget=V,X=xx,z=zz,terms=np.array(active,str))
                fitrows.append(dict(scenario=sc,cycle=year,model=name,family=family,tau=tau,parameters=len(active),training_cycles=len(years),training_max_cycle=int(years.max()),history_weight_sum=float(w.sum()),history_effective_cycles=float(w.sum()**2/(w@w)),a=fit['a'],optimizer_success=fit['optimizer_success'],at_lower=fit['at_lower'],at_upper=fit['at_upper'],log_evidence=fit['log_evidence']))
                profiles.extend(dict(scenario=sc,cycle=year,model=name,a=float(aa),nll=float(ll)) for aa,ll in zip(fit['profile_grid'],fit['profile_nll']))
                for j,term in enumerate(active):
                    raw=float(future_scores.iloc[0][term]);coefs.append(dict(scenario=sc,cycle=year,model=name,term=term,raw_score=raw,imputed=bool(pd.isna(raw)),fill=design.fills[term],center=design.centers[term],scale=design.scales[term],standardized_score=float(zz[j]),coefficient_mean_pp=float(fit['beta_mean'][j]),coefficient_sd_pp=float(np.sqrt(fit['beta_covariance'][j,j])),contribution_pp=float(zz[j]*fit['beta_mean'][j])))
                p,cov,stats,meta=predict(test,V,poll,fit,zz);p=p.assign(model=name,family=family,tau=tau);preds.append(p)
                draws=p.prediction_pp.to_numpy()+normal_draws@np.linalg.cholesky(cov).T;ss,counts=chamber.seat_summary(roster[roster.scenario.eq(sc)&roster.cycle.eq(year)],test,p,draws);ss.update(scenario=sc,cycle=year,model=name,family=family,tau=tau)
                freq=np.bincount(counts,minlength=101);seats.append(scoring.seat_scores(ss,freq));path=f'forecasts/{sc}_{year}_{name}.npz'
                np.savez_compressed(out/path,target_ids=test.target_id.to_numpy(str),mean=p.prediction_pp.to_numpy(),covariance=cov,prior_mean=meta['prior_mean'],prior_covariance=meta['prior_covariance'],seat_count_frequency=freq)
                folds.append(dict(scenario=sc,cycle=year,model=name,family=family,tau=tau,fit_path=fp,forecast_path=path,**stats))
                if family=='none':
                    cols=['prediction_pp','p_dem','lo70_pp','hi95_pp'];oldfreq=np.load(source/r.forecast_path)['seat_count_frequency']
                    reproductions.append(dict(scenario=sc,cycle=year,passed=bool(np.allclose(p[cols],test[cols],atol=1e-8) and np.array_equal(freq,oldfreq)),max_mean_difference_pp=float(abs(p.prediction_pp-test.prediction_pp).max())))
        print(sc,year,'no-features + three feature sets calibrated',flush=True)
    cp=pd.concat(preds,ignore_index=True);cs=pd.DataFrame(seats);cf=pd.DataFrame(folds);cc=pd.DataFrame(coefs);selectedp=[cp[cp.model.eq('none')]];selecteds=[cs[cs.model.eq('none')]];selectedf=[cf[cf.model.eq('none')]];selectedc=[];tuning=[]
    for (sc,year),group in cp.groupby(['scenario','cycle']):
        for family in FAMILIES:
            order=[f'{family}_tau{tau}' for tau in TAUS];chosen,years,status=timing.choose(cs[cs.scenario.eq(sc)],year,order);name=family
            selectedp.append(group[group.model.eq(chosen)].assign(model=name,selected_model=chosen));selecteds.append(cs[cs.scenario.eq(sc)&cs.cycle.eq(year)&cs.model.eq(chosen)].assign(model=name,selected_model=chosen));selectedf.append(cf[cf.scenario.eq(sc)&cf.cycle.eq(year)&cf.model.eq(chosen)].assign(model=name,selected_model=chosen));selectedc.append(cc[cc.scenario.eq(sc)&cc.cycle.eq(year)&cc.model.eq(chosen)].assign(model=name,selected_model=chosen))
            for candidate in order:
                q=cs[cs.scenario.eq(sc)&cs.cycle.isin(years)&cs.model.eq(candidate)];tuning.append(dict(scenario=sc,forecast_cycle=year,family=family,candidate=candidate,selected_model=chosen,validation_cycles=','.join(map(str,years)),status=status,mean_validation_CRPS=q.seat_crps.mean()))
    p=pd.concat(selectedp,ignore_index=True);s=pd.concat(selecteds,ignore_index=True);f=pd.concat(selectedf,ignore_index=True)
    tables=dict(predictions=p,seats=s,folds=f,candidates=cp,candidate_seats=cs,candidate_folds=cf,coefficients=pd.concat(selectedc,ignore_index=True),candidate_coefficients=cc,tuning=pd.DataFrame(tuning),fit_diagnostics=pd.DataFrame(fitrows),fit_profiles=pd.DataFrame(profiles),scores=pd.concat(scores,ignore_index=True),components=pd.concat(components,ignore_index=True),summary=scoring.summarize_scores(p),chamber_summary=national.chamber_summary(s))
    for name,table in tables.items():table.to_parquet(out/(name+'.parquet'),index=False)
    v1.json_write(out/'normalizers.json',metadata);v1.json_write(out/'reproduction.json',dict(passed=all(x['passed'] for x in reproductions),folds=reproductions))
    for path in (lab/'scripts').glob('*.py'):(out/'recipe'/path.name).write_bytes(path.read_bytes())
    (out/'NATIONAL_FEATURE_PRIOR.md').write_bytes((lab/'NATIONAL_FEATURE_PRIOR.md').read_bytes())
    v1.manifest(out);audit(out,lab);report(out,lab);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    print('COMPLETE',out,flush=True);return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);st=json.loads((out/'settings.json').read_text());source=Path(st['source']);p=pd.read_parquet(out/'predictions.parquet');cp=pd.read_parquet(out/'candidates.parquet');s=pd.read_parquet(out/'candidate_seats.parquet');f=pd.read_parquet(out/'candidate_folds.parquet');t=pd.read_parquet(out/'tuning.parquet');fd=pd.read_parquet(out/'fit_diagnostics.parquet');norms=json.loads((out/'normalizers.json').read_text());co=pd.read_parquet(out/'candidate_coefficients.parquet')
    _,_,wt=working.load(lab)
    c=dict(sources_unchanged=all(v1.verify(path)==digest for path,digest in st['sources'].items()),working_unchanged=v1.sha(lab/'WORKING_MODEL.json')==st['working_sha256'],score_recipe_unchanged=v1.sha(CONFIG_PATH)==st['score_config_sha256'],older_notebooks_preserved=all(v1.sha(lab/name)==digest for name,digest in st['old_notebook_hashes'].items()),
        no_feature_reproduction=json.loads((out/'reproduction.json').read_text())['passed'],training_past_only=bool(fd.training_max_cycle.lt(fd.cycle).all()),normalization_past_only=all(max(n['normalizer']['training_cycles'])<n['forecast_cycle'] for n in norms),optimizers_succeeded=bool(fd.optimizer_success.all()),
        unique_forecasts=not cp.duplicated(['scenario','target_id','model']).any(),current_labels_missing=bool(cp[cp.cycle.eq(2026)][['actual','wis_pp','brier']].isna().all().all() and s[s.cycle.eq(2026)][['actual_D','seat_crps']].isna().all().all()),zero_shared_error=bool(cp.national_poll_error_pp.eq(0).all()),probability_bounds=bool(cp.p_dem.between(0,1).all()))
    recon=[];priorok=[];fitok=[];seatok=[];zero=[];chosenok=[];varok=[];contrib=[];designok=[];design_cache={}
    calendars=pd.read_parquet(Path(st['upstream'])/'calendars.parquet')
    for r in f.itertuples():
        q=cp[cp.scenario.eq(r.scenario)&cp.cycle.eq(r.cycle)&cp.model.eq(r.model)].sort_values('target_id').reset_index(drop=True);original=wt['predictions'][wt['predictions'].scenario.eq(r.scenario)&wt['predictions'].cycle.eq(r.cycle)].sort_values('target_id');z=np.load(out/r.forecast_path);fit=dict(np.load(out/r.fit_path));fit['a']=float(fit['a'])
        key=(r.scenario,r.cycle)
        if key not in design_cache:
            design_cache[key]=prepare_design(calendars[calendars.scenario.eq(r.scenario)],fit['years'],fit['training_weights'],r.cycle)[:3]
        des,xx,zz=design_cache[key];ids=[des.active.index(term) for term in fit['terms']]
        designok.append(np.allclose(xx[:,ids],fit['X']) and np.allclose(zz[ids],fit['z']))
        pf=np.load(source/f'fits/{r.scenario}_{r.cycle}_poll.npz');poll=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        dd=regression_at_a(fit['training_values'],fit['training_noise'],fit['training_weights'],fit['budget'],fit['X'],r.tau,fit['a'])
        fitok.append(np.allclose(dd['beta_mean'],fit['beta_mean']) and np.allclose(dd['beta_covariance'],fit['beta_covariance']))
        expected,cov,stats,meta=predict(q,fit['budget'],poll,fit,fit['z']);cols=['prediction_pp','p_dem','lo70_pp','hi95_pp']
        recon.append(np.allclose(expected[cols],q[cols],atol=1e-9) and np.allclose(z['covariance'],cov,atol=1e-9))
        priorok.append(np.array_equal(q.target_id,original.target_id) and np.array_equal(q.prior,original.prior) and np.array_equal(q.actual,original.actual,equal_nan=True) and np.array_equal(q.q_pp,original.q_pp,equal_nan=True) and np.allclose(q.historical_bias_pp,original.historical_bias_pp))
        variance=float(fit['z']@fit['beta_covariance']@fit['z']);baseV=fit['budget'][[v1.STATES.index(x) for x in q.geography]];varok.append(variance>=-1e-10 and np.allclose(np.diag(meta['prior_covariance']),baseV+variance))
        if r.tau==0:zero.append(np.allclose(q[cols],original[cols],atol=1e-8) and np.allclose(fit['beta_covariance'],0))
        ss=s[s.scenario.eq(r.scenario)&s.cycle.eq(r.cycle)&s.model.eq(r.model)].iloc[0];seatok.append(abs(ss.expected_D_exact-ss.fixed_D-q.p_dem.sum())<1e-9 and z['seat_count_frequency'].sum()==CONFIG['draws'])
        if r.family!='none':
            cc=co[co.scenario.eq(r.scenario)&co.cycle.eq(r.cycle)&co.model.eq(r.model)];contrib.append(abs(cc.contribution_pp.sum()-r.feature_mean_pp)<1e-9)
    for r in t.drop_duplicates(['scenario','forecast_cycle','family']).itertuples():
        order=[f'{r.family}_tau{tau}' for tau in TAUS];chosen,years,status=timing.choose(s[s.scenario.eq(r.scenario)],r.forecast_cycle,order)
        qa=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq(r.family)].sort_values('target_id');qb=cp[cp.scenario.eq(r.scenario)&cp.cycle.eq(r.forecast_cycle)&cp.model.eq(chosen)].sort_values('target_id')
        chosenok.append(chosen==r.selected_model and status==r.status and ','.join(map(str,years))==r.validation_cycles and np.allclose(qa.prediction_pp,qb.prediction_pp))
    c.update(normalization_design_reconstructed=all(designok),regression_posterior_reconstructed=all(fitok),predictions_reconstructed=all(recon),state_priors_polls_labels_preserved=all(priorok),coefficient_uncertainty_added_once=all(varok),zero_shrinkage_reproduces_control=all(zero),seat_accounting=all(seatok),feature_contributions_sum=all(contrib),past_only_selection_reconstructed=all(chosenok))
    result=dict(passed=all(c.values()),checks=c,forecast_rows=len(p),candidate_rows=len(cp),fits=len(fd),older_notebooks=len(st['old_notebook_hashes']))
    v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError([key for key,value in c.items() if not value])
    v1.manifest(out);return result


def report(out,lab):
    out,lab=Path(out),Path(lab);p=pd.read_parquet(out/'predictions.parquet');s=pd.read_parquet(out/'seats.parquet');f=pd.read_parquet(out/'folds.parquet');su=pd.read_parquet(out/'summary.parquet');ch=pd.read_parquet(out/'chamber_summary.parquet');t=pd.read_parquet(out/'tuning.parquet');co=pd.read_parquet(out/'coefficients.parquet')
    cyc=p[p.actual.notna()].groupby(['scenario','cycle','model'],as_index=False).agg(n=('actual','size'),correct=('correct','sum'),mae_pp=('absolute_error_pp','mean'),wis_pp=('wis_pp','mean'),brier=('brier','mean'));cyc.to_parquet(out/'cycle_scores.parquet',index=False)
    text='# National feature prior: results\n\nGaussian working polling model, frozen September17 inputs. Features shift the national prior; current polls update the same factor. Coefficient uncertainty is propagated; residual national variance re-estimated. All shrinkage selections use earlier cycles.\n\n'
    for period in ['recent_2016_2024','tuned_2018_2024','all_2012_2024']:
        text+='## '+period+'\n\n'+su[su.period.eq(period)&su.group.eq('all')][['scenario','model','n','correct','absolute_error_pp','wis_pp','brier','coverage70','coverage95']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Recent chamber scores\n\n'+ch[ch.period.eq('recent_2016_2024')].round(4).to_markdown(index=False)+'\n\n'
    text+='## Selection\n\n'+t.drop_duplicates(['scenario','forecast_cycle','family'])[['scenario','forecast_cycle','family','selected_model','validation_cycles','status']].to_markdown(index=False)+'\n\n'
    text+='## Current seats\n\n'+s[s.cycle.eq(2026)][['model','tau','point_D','point_R','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current national prior and polling update\n\n'+f[f.cycle.eq(2026)][['model','tau','feature_mean_pp','feature_variance_pp2','residual_N_variance','N_mean_pp','N_sd_pp']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current score contributions\n\n'+co[co.cycle.eq(2026)].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current state predictions\n\n'+p[p.cycle.eq(2026)].pivot(index='geography',columns='model',values='prediction_pp').round(3).to_markdown()+'\n\n'
    text+='## Limits\n\nFew recent national contexts and repeated exploration. Historical feature revisions/vintages and training median imputation remain limitations; imputation uncertainty is not integrated. Coefficient uncertainty is integrated conditional on empirical-Bayes residual variance and selected shrinkage. State marginal budgets and candidate/ballot/completion assumptions remain inherited. No automatic promotion or refresh.\n'
    (lab/'NATIONAL_FEATURE_PRIOR_RESULTS.md').write_text(text);(out/'NATIONAL_FEATURE_PRIOR_RESULTS.md').write_text(text)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=ch[ch.period.eq('recent_2016_2024')&ch.scenario.eq(sc)].set_index('model');names=['none',*FAMILIES];ax.bar(names,[q.loc[name,'seat_crps'] for name in names]);ax.set(title=sc,ylabel='Mean chamber CRPS (lower is better)')
    fig.tight_layout();fig.savefig(out/'chamber_scores.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for ax,sc in zip(axes,['matched_live','oct31']):
        for name in FAMILIES:
            q=f[f.scenario.eq(sc)&f.model.eq(name)].sort_values('cycle');ax.plot(q.cycle,q.feature_mean_pp,marker='o',label=name)
        ax.axhline(0,color='black',lw=.7);ax.set(title=sc,ylabel='Feature-informed national prior mean (D−R pp)',xlabel='Cycle');ax.legend()
    fig.tight_layout();fig.savefig(out/'feature_prior_by_cycle.png',dpi=145);plt.close(fig);v1.manifest(out)


if __name__=='__main__':build(Path(__file__).resolve().parents[1])
