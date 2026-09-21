"""Joint Student electoral/poll residuals; frozen empirical-Bayes historical fits."""
from pathlib import Path
from datetime import datetime,timezone
import json
import numpy as np
import pandas as pd
from numba import njit
from scipy.special import ndtr
import simple_bayesian_polling as v1
import simple_national_model as normal
import bayesian_gaussian as diagnostics_base
import coverage_balance as scoring
import national_tails_waves as chamber
import national_factor_review as national
from final_baseline_experiments import gaussian,cycle_metrics

FEATURE='20260920T013619.322700Z'
CONFIG=dict(seed=197139,chains=8,warmup=2000,draws=4000,validation_cycles=3,as_of='2026-09-17',df=[5,3],electoral_variance_multipliers=[1,2])
ORDER=['g1','g2','t5v1','t5v2','t3v1','t3v2']

@njit(cache=True)
def chain(mu,L,A,FV,obs,y,P,F,nu,warm,draws,seed):
    """Exact blocked Gibbs conditionals. nu=0 fixes all scales at one for tests."""
    np.random.seed(seed);n=len(mu);k=len(obs);sn=1.;h=1.;sl=np.ones(n)
    # theta, national total, r, c, log sn/h, local log scales, poll errors, seat sign count.
    traces=np.empty((draws,2*n+k+6));means=np.zeros(n);second=np.zeros((n,n));prob=np.zeros(n)
    for it in range(warm+draws):
        lv=L*sl;g=FV+A*sn;rv=P*h+F
        prec=0.;rhs=0.
        for j in range(k):
            i=obs[j];den=lv[i]+rv[j];prec+=1/den;rhs+=(y[j]-mu[i])/den
        vn=g/(1+g*prec);mn=vn*rhs;N=mn+np.sqrt(vn)*np.random.normal()
        cm=mu+mn;load=np.ones(n);cv=lv.copy();delta=np.empty(n)
        for i in range(n):delta[i]=np.sqrt(lv[i])*np.random.normal()
        for j in range(k):
            i=obs[j];gain=lv[i]/(lv[i]+rv[j]);load[i]=1-gain;cv[i]=lv[i]*(1-gain)
            cm[i]+=gain*(y[j]-mu[i]-mn)
            delta[i]=gain*(y[j]-mu[i]-N)+np.sqrt(cv[i])*np.random.normal()
        theta=mu+N+delta
        r=(A*sn/g)*N+np.sqrt(A*sn*FV/g)*np.random.normal() if g>0 else 0.
        c=N-r;e=np.empty(k)
        for j in range(k):
            v=P[j]*h;gain=v/(v+F[j]);e[j]=gain*(y[j]-theta[obs[j]])+np.sqrt(v*(1-gain))*np.random.normal()
        if it>=warm:
            t=it-warm;traces[t,:n]=theta;traces[t,n:n+5]=np.array([N,r,c,np.log(sn),np.log(h)])
            traces[t,n+5:2*n+5]=np.log(sl);traces[t,2*n+5:2*n+5+k]=e;traces[t,-1]=np.sum(theta>0)
            means+=cm
            for i in range(n):
                sd=np.sqrt(cv[i]+vn*load[i]**2)
                # normal CDF implemented through erf for numba.
                prob[i]+=.5*(1+__import_erf((cm[i])/sd/np.sqrt(2.)))
                for j in range(n):second[i,j]+=cm[i]*cm[j]+vn*load[i]*load[j]+(cv[i] if i==j else 0.)
        if nu>0:
            if A>0:sn=1/np.random.gamma((nu+1)/2,2/((nu-2)+r*r/A))
            else:sn=1.
            for i in range(n):
                # Unobserved local scales are independent prior draws conditional on all data.
                if i in obs:sl[i]=1/np.random.gamma((nu+1)/2,2/((nu-2)+delta[i]**2/L[i]))
                else:sl[i]=1/np.random.gamma(nu/2,2/(nu-2))
            h=1/np.random.gamma((nu+k)/2,2/((nu-2)+np.sum(e*e/P)))
    return traces,means/draws,second/draws,prob/draws

from math import erf as __import_erf


def sample(mu,L,A,FV,obs,y,P,F,nu,seed=1,warmup=2000,draws=4000,chains=8,check=True):
    mu,L,obs,y,P,F=np.asarray(mu,float),np.asarray(L,float),np.asarray(obs,np.int64),np.asarray(y,float),np.asarray(P,float),np.asarray(F,float)
    if np.any(L<=0) or np.any(P<=0) or np.any(F<=0) or A<0 or FV<0 or (nu!=0 and nu<=2):raise ValueError('Positive variances and nu>2 required')
    for attempt in range(4):
        runs=[chain(mu,L,A,FV,obs,y,P,F,nu,warmup,draws,seed+c*7919) for c in range(chains)]
        traces=np.stack([r[0] for r in runs]);n=len(mu)
        names=[f'margin_{i}' for i in range(n)]+['national','national_residual','feature_uncertainty','log_national_scale','log_poll_scale']+[f'log_local_scale_{i}' for i in range(n)]+[f'poll_error_{i}' for i in obs]+['contested_D_count']
        varying=np.ptp(traces.reshape(-1,traces.shape[-1]),axis=0)>1e-12
        diag=diagnostics_base.diagnostics(traces[:,:,varying],[x for x,v in zip(names,varying) if v])
        good=diag.rhat.max()<1.01 and min(diag.bulk_ess.min(),diag.tail_ess.min())>=400
        if good or not check:break
        print(' EXTEND',nu,attempt,float(diag.rhat.max()),float(diag.bulk_ess.min()),float(diag.tail_ess.min()),flush=True);warmup*=2;draws*=2
    else:raise RuntimeError('Combined Student convergence failed')
    mean=np.mean([r[1] for r in runs],axis=0);cov=np.mean([r[2] for r in runs],axis=0)-np.outer(mean,mean)
    prob=np.mean([r[3] for r in runs],axis=0);theta=traces[:,:,:n].reshape(-1,n)
    return dict(mean=mean,covariance=cov,p_dem=prob,samples=theta,diagnostics=diag,chain_means=np.stack([r[1] for r in runs]),chain_probabilities=np.stack([r[3] for r in runs]),warmup=warmup,draws=draws,chains=chains,seed=seed,trace_summary=np.quantile(traces.reshape(-1,traces.shape[-1]),[.025,.5,.975],axis=0),trace_names=np.array(names))


def inputs(test,fit,prior,poll,mult=1):
    ids=np.array([v1.STATES.index(x) for x in test.geography]);obs=np.flatnonzero(test.q_pp.notna());so=ids[obs]
    K=prior['prior_covariance'];g=float(K[0,1]);a=float(fit['a']);fv=max(0.,g-a);L=(np.diag(K)-g)*mult
    P=poll['covariance'][np.ix_(so,so)];B=poll['bias_covariance'][np.ix_(so,so)]
    if not np.allclose(P,np.diag(np.diag(P))) or not np.allclose(B,np.diag(np.diag(B))):raise ValueError('This experiment requires noU diagonal polling covariance')
    return prior['prior_mean'],L,a*mult,fv,obs,test.q_pp.to_numpy()[obs]-poll['bias_mean'][so],np.diag(P),np.diag(B)+16/test.firm_mass.to_numpy()[obs]


def student_predict(test,args,nu,seed,**kwargs):
    d=sample(*args,nu,seed=seed,**kwargs);p=test.copy();p['prediction_pp']=d['mean'];p['prediction']=d['mean']/100;p['p_dem']=d['p_dem'];p['median_pp']=np.median(d['samples'],axis=0);p['posterior_sd_pp']=np.sqrt(np.diag(d['covariance']))
    for level in scoring.LEVELS:
        lo,hi=np.quantile(d['samples'],[(1-level/100)/2,(1+level/100)/2],axis=0);p[f'lo{level}_pp']=lo;p[f'hi{level}_pp']=hi
    p['log_predictive_density']=np.nan
    return scoring.score_rows(p),d


def clean_output(p,mult,K):
    # Drop inherited source-model posterior decompositions, not input features.
    p=p.drop(columns=[x for x in ['selected_model','outside_margin_bounds_probability','national_movement_pp','local_electoral_update_pp','national_poll_error_pp','poll_surprise_pp'] if x in p]).copy()
    p['prediction']=p.prediction_pp/100;p['variance_multiplier']=mult;p['prior_sd_pp']=np.sqrt(np.diag(K))
    return p


def choose(cs,seats,sc,year,family,metric):
    q=seats if metric=='seat_crps' else cs;models=[family+'__'+x for x in ORDER];q=q[q.scenario.eq(sc)&q.cycle.lt(year)&q.model.isin(models)];years=sorted(q.cycle.unique())[-3:]
    if len(years)<3:return models[0],years,{}
    q=q[q.cycle.isin(years)]
    if len(q)!=3*len(models) or q.duplicated(['cycle','model']).any():raise ValueError('Incomplete prior validation grid')
    val=q.groupby('model')[metric].mean().to_dict();return min(models,key=lambda m:(val[m],models.index(m))),years,val


def build(lab):
    lab=Path(lab).resolve();src=lab/'reports/national_feature_prior'/FEATURE;fs=json.loads((src/'settings.json').read_text());working=Path(fs['source']);up=Path(fs['upstream'])
    out=lab/'reports/combined_student_model'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for x in ['forecasts','recipe']:(out/x).mkdir(parents=True,exist_ok=True)
    st=dict(config=CONFIG,source=str(src),working=str(working),upstream=str(up),sources={str(x):v1.verify(x) for x in [src,working,up]},old_notebook_hashes={x.name:v1.sha(x) for x in lab.glob('*.ipynb') if x.name!='COMBINED_STUDENT_MODEL.ipynb'},working_sha256=v1.sha(lab/'WORKING_MODEL.json'),promotion=False,data_refreshed=False,historical_fit='frozen Gaussian empirical-Bayes calibration')
    v1.json_write(out/'settings.json',st);print('OUTPUT',out,flush=True)
    orig=pd.read_parquet(src/'predictions.parquet');sf=pd.read_parquet(src/'folds.parquet');sf=sf[sf.model.isin(['none','both'])];roster=pd.read_parquet(up/'full_seat_ledger.parquet')
    preds=[];seats=[];folds=[];diags=[];reproduced=[]
    for (sc,year),group in sf.groupby(['scenario','cycle']):
        pf=np.load(working/f'fits/{sc}_{year}_poll.npz');poll=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        for r in group.itertuples():
            family=r.model;test=orig[orig.scenario.eq(sc)&orig.cycle.eq(year)&orig.model.eq(family)].sort_values('target_id').reset_index(drop=True);fit=np.load(src/r.fit_path);prior=np.load(src/r.forecast_path)
            for variant in ORDER:
                mult=int(variant[-1]);nu=0 if variant.startswith('g') else int(variant[1]);args=inputs(test,fit,prior,poll,mult);mu,L,A,FV,*_=args;K=np.diag(L)+(A+FV)*np.ones((len(L),len(L)));seed=CONFIG['seed']+year+10000*(sc=='oct31')
                if nu:
                    p,d=student_predict(test,args,nu,seed,warmup=CONFIG['warmup'],draws=CONFIG['draws'],chains=CONFIG['chains']);draws=d['samples'];diag=d['diagnostics'].assign(scenario=sc,cycle=year,family=family,variant=variant);diags.append(diag)
                    print(sc,year,family,variant,'Rhat',round(diag.rhat.max(),4),'ESS',round(min(diag.bulk_ess.min(),diag.tail_ess.min())),flush=True)
                else:
                    p,d=gaussian(test,mu,K,poll);draws=d['mean']+np.random.default_rng(seed).standard_normal((30000,len(test)))@np.linalg.cholesky(d['covariance']).T
                model=family+'__'+variant;p=clean_output(p,mult,K).assign(model=model,family=family,variant=variant);preds.append(p)
                ss,counts=chamber.seat_summary(roster[roster.scenario.eq(sc)&roster.cycle.eq(year)],test,p,draws);freq=np.bincount(counts,minlength=101)
                seats.append(scoring.seat_scores(dict(ss,scenario=sc,cycle=year,model=model,family=family,variant=variant),freq))
                path=f'forecasts/{sc}_{year}_{model}.npz';save=dict(target_ids=test.target_id.to_numpy(str),mean=d['mean'],covariance=d['covariance'],prior_mean=mu,prior_covariance=K,seat_count_frequency=freq)
                if nu:save.update(chain_means=d['chain_means'],chain_probabilities=d['chain_probabilities'],trace_summary=d['trace_summary'],trace_names=d['trace_names'])
                np.savez_compressed(out/path,**save)
                folds.append(dict(scenario=sc,cycle=year,model=model,family=family,variant=variant,df=nu,variance_multiplier=mult,source_fit_path=r.fit_path,source_forecast_path=r.forecast_path,forecast_path=path,feature_tau=r.tau,training_max_cycle=int(fit['years'].max()),seed=seed,warmup=d.get('warmup',0),draws_per_chain=d.get('draws',0),chains=d.get('chains',0),total_draws=len(draws)))
                if variant=='g1':reproduced.append(np.allclose(p[['prediction_pp','p_dem','lo70_pp','hi95_pp']],test[['prediction_pp','p_dem','lo70_pp','hi95_pp']],atol=1e-8) and np.array_equal(freq,prior['seat_count_frequency']))
    p=pd.concat(preds,ignore_index=True);s=pd.DataFrame(seats);f=pd.DataFrame(folds);cs=cycle_metrics(p);sp=[];ss=[];ff=[];tune=[]
    for sc,year,family in p[['scenario','cycle','family']].drop_duplicates().itertuples(index=False,name=None):
        for metric in ['seat_crps','wis_pp']:
            chosen,years,values=choose(cs,s,sc,year,family,metric);name=family+'__selected_'+metric
            for tab,dest in [(p,sp),(s,ss),(f,ff)]:dest.append(tab[tab.scenario.eq(sc)&tab.cycle.eq(year)&tab.model.eq(chosen)].assign(model=name,selected_model=chosen))
            for candidate in ORDER:tune.append(dict(scenario=sc,forecast_cycle=year,family=family,metric=metric,candidate=family+'__'+candidate,selected_model=chosen,validation_cycles=','.join(map(str,years)),score=values.get(family+'__'+candidate,np.nan)))
    p=pd.concat([p,*sp],ignore_index=True);s=pd.concat([s,*ss],ignore_index=True);f=pd.concat([f,*ff],ignore_index=True)
    for name,tab in dict(predictions=p,seats=s,folds=f,cycle_scores=cycle_metrics(p),summary=scoring.summarize_scores(p),chamber_summary=national.chamber_summary(s),tuning=pd.DataFrame(tune),diagnostics=pd.concat(diags,ignore_index=True)).items():tab.to_parquet(out/f'{name}.parquet',index=False)
    v1.json_write(out/'reproduction.json',dict(passed=bool(all(reproduced)),comparisons=len(reproduced)))
    for path in (lab/'scripts').glob('*.py'):(out/'recipe'/path.name).write_bytes(path.read_bytes())
    (out/'COMBINED_STUDENT_MODEL.md').write_bytes((lab/'COMBINED_STUDENT_MODEL.md').read_bytes());v1.manifest(out)
    audit(out,lab);v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)));print('COMPLETE',out,flush=True);return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);st=json.loads((out/'settings.json').read_text());p=pd.read_parquet(out/'predictions.parquet');s=pd.read_parquet(out/'seats.parquet');f=pd.read_parquet(out/'folds.parquet');d=pd.read_parquet(out/'diagnostics.parquet');cs=pd.read_parquet(out/'cycle_scores.parquet');tr=pd.read_parquet(out/'tuning.parquet');orig=pd.read_parquet(Path(st['source'])/'predictions.parquet')
    checks=dict(sources_unchanged=all(v1.verify(x)==h for x,h in st['sources'].items()),old_notebooks_preserved=all(v1.sha(lab/x)==h for x,h in st['old_notebook_hashes'].items()),working_unchanged=v1.sha(lab/'WORKING_MODEL.json')==st['working_sha256'],Gaussian_reproduction=json.loads((out/'reproduction.json').read_text())['passed'],past_training=bool(f.training_max_cycle.lt(f.cycle).all()),unique_predictions=not p.duplicated(['scenario','target_id','model']).any(),current_unknown=bool(p[p.cycle.eq(2026)][['actual','wis_pp','brier']].isna().all().all() and s[s.cycle.eq(2026)][['actual_D','seat_crps']].isna().all().all()),mcmc_converged=bool(d.rhat.lt(1.01).all() and d.bulk_ess.ge(400).all() and d.tail_ess.ge(400).all()),probabilities_valid=bool(p.p_dem.between(0,1).all()),prediction_units=bool(np.allclose(p.prediction*100,p.prediction_pp)))
    preserve=[];account=[];cov=[];selection=[]
    for r in f[~f.model.str.contains('selected')].itertuples():
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id');old=orig[orig.scenario.eq(r.scenario)&orig.cycle.eq(r.cycle)&orig.model.eq(r.family)].sort_values('target_id');z=np.load(out/r.forecast_path);pr=np.load(Path(st['source'])/r.source_forecast_path);fit=np.load(Path(st['source'])/r.source_fit_path);g=float(pr['prior_covariance'][0,1]);a=float(fit['a']);L=np.diag(pr['prior_covariance'])-g
        preserve.append(np.array_equal(q.target_id,old.target_id) and all(np.array_equal(q[x],old[x],equal_nan=True) for x in ['actual','prior','q_pp','firm_mass']) and np.array_equal(z['prior_mean'],pr['prior_mean']))
        cov.append(np.allclose(z['prior_covariance'],np.diag(L*r.variance_multiplier)+(a*r.variance_multiplier+g-a)*np.ones((len(L),len(L)))) and np.linalg.eigvalsh(z['covariance']).min()>0)
        seat=s[s.scenario.eq(r.scenario)&s.cycle.eq(r.cycle)&s.model.eq(r.model)].iloc[0];account.append(z['seat_count_frequency'].sum()==r.total_draws and abs(seat.expected_D_exact-seat.fixed_D-q.p_dem.sum())<1e-8 and seat.point_D==seat.fixed_D+q.prediction_pp.gt(0).sum())
    for r in tr.drop_duplicates(['scenario','forecast_cycle','family','metric']).itertuples():
        selected,years,_=choose(cs,s,r.scenario,r.forecast_cycle,r.family,r.metric);q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq(r.family+'__selected_'+r.metric)].sort_values('target_id');other=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq(selected)].sort_values('target_id');selection.append(selected==r.selected_model and ','.join(map(str,years))==r.validation_cycles and np.array_equal(q.prediction_pp,other.prediction_pp))
    checks.update(inputs_preserved=all(preserve),covariance_variants=all(cov),seat_accounting=all(account),past_only_selection=all(selection),interval_order=all(bool(p[f'lo{k}_pp'].le(p.median_pp).all() and p[f'hi{k}_pp'].ge(p.median_pp).all()) for k in scoring.LEVELS))
    if (out/'repeat_checks.parquet').exists():
        rep=pd.read_parquet(out/'repeat_checks.parquet');rd=pd.read_parquet(out/'repeat_diagnostics.parquet')
        checks.update(independent_repeat_convergence=bool(rd.rhat.lt(1.01).all() and rd.bulk_ess.ge(400).all() and rd.tail_ess.ge(400).all()),independent_repeat_means_probabilities=bool(rep.max_mean_pp.lt(.25).all() and rep.max_probability.lt(.01).all() and rep.expected_seat_difference.abs().lt(.05).all()))
    if (out/'nonbayesian_matched.parquet').exists():
        nb=pd.read_parquet(out/'nonbayesian_matched.parquet');checks['matched_nonbayesian']=bool(len(nb)==2*len(p[p.model.eq('none__g1')]) and np.allclose(nb.actual,nb.actual_checked,equal_nan=True))
    result=dict(passed=all(checks.values()),checks=checks,fixed_forecasts=int((~f.model.str.contains('selected')).sum()),rows=len(p),max_rhat=float(d.rhat.max()),min_bulk_ess=float(d.bulk_ess.min()),min_tail_ess=float(d.tail_ess.min()));v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError([k for k,v in checks.items() if not v])
    return result


def load(lab):
    root=Path(lab)/'reports/combined_student_model';ptr=json.loads((root/'latest.json').read_text());out=root/ptr['artifact'];assert v1.verify(out)==ptr['manifest_sha256'];return out,{p.stem:pd.read_parquet(p) for p in out.glob('*.parquet')}

if __name__=='__main__':build(Path(__file__).resolve().parents[1])
