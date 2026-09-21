"""History-calibrated, missing-data Gaussian covariance; empirical Bayes.

See BAYESIAN_REVISION2_ESTIMATOR.md. No state-pair correlation grid or extra
national factor. Covariance uncertainty is NOT integrated in this revision.
"""
from pathlib import Path
from datetime import datetime,timezone
import json
import numpy as np
import pandas as pd
from scipy.linalg import cho_factor,cho_solve
from scipy.stats import norm
from scipy.optimize import minimize_scalar
import simple_bayesian_polling as v1

STATES=v1.STATES
CONFIG=dict(history_half_life_years=8.,other_type_weight=.5,bias_prior_sd_pp=3.,
            fresh_firm_sd_pp=4.,regularization_candidates=[.5,2.,8.],validation_cycles=3,
            max_iterations=4000,convergence_tolerance=1e-6,seed=291926,draws=20000)
MODELS=['v2_linked','v2_movement_diagonal','v2_local']
LABELS={**v1.LABELS,'v1_linked':'Revision 1 linked','v1_local':'Revision 1 local',
        'v2_linked':'Revision 2 linked','v2_movement_diagonal':'Revision 2 movement links off',
        'v2_local':'Revision 2 local'}


def inverse(a):
    ch=cho_factor(a,lower=True,check_finite=False)
    return cho_solve(ch,np.eye(len(a)),check_finite=False),2*np.log(np.diag(ch[0])).sum()


def blocks(history,year,kind):
    h=history[history.cycle.lt(year)&history.actual.notna()&history.prior_latest_cycle.notna()&history.prior_latest_cycle.lt(history.cycle)].copy()
    if kind=='poll':h=h[h.q_pp.notna()&h.firm_mass.gt(0)].copy()
    if h.duplicated(['cycle','geography']).any():
        raise ValueError('Multiple admitted contests per state/cycle need an explicit multiseat model')
    h['value']=h.q_pp-100*h.actual if kind=='poll' else 100*(h.actual-h.prior)
    h['noise']=CONFIG['fresh_firm_sd_pp']**2/h.firm_mass if kind=='poll' else 0.
    years=np.sort(h.cycle.unique())
    x=h.pivot(index='cycle',columns='geography',values='value').reindex(index=years,columns=STATES).to_numpy()
    noise=h.pivot(index='cycle',columns='geography',values='noise').reindex(index=years,columns=STATES).to_numpy()
    weights=np.array([v1.relevance(int(y),year) for y in years])
    return x,noise,weights,years,h


def make_target(x,noise,weights,kappa,bias_prior_variance):
    mask=np.isfinite(x); mass=(weights[:,None]*mask).sum(axis=0)
    # A cycle-balanced marginal likelihood gives a continuous pooled process
    # scale. Known measurement variance makes stale polls weak information.
    marginal_weights=weights[:,None]/mask.sum(axis=1)[:,None]
    def objective(v):
        total=v+noise+(bias_prior_variance or 0.)
        return .5*np.nansum(marginal_weights*(np.log(total)+x*x/total))
    upper=max(float(np.nanmax(x*x))*2,1.)
    result=minimize_scalar(objective,bounds=(1e-6,upper),method='bounded',options={'xatol':1e-8})
    if not result.success:raise RuntimeError('Pooled variance optimization failed')
    pool=max(float(result.x),1e-6)
    pilot=np.zeros(x.shape[1]);pilot_var=np.zeros(x.shape[1])
    if bias_prior_variance is not None:
        precision=1/bias_prior_variance+np.nansum(weights[:,None]/(pool+noise),axis=0)
        pilot_var=1/precision
        pilot=pilot_var*np.nansum(weights[:,None]*x/(pool+noise),axis=0)
    gain=pool/(pool+noise)
    conditional_second=pool*(1-gain)+gain**2*((x-pilot)**2+pilot_var)
    d=(np.nansum(weights[:,None]*conditional_second,axis=0)+kappa*pool)/(mass+kappa)
    d=np.maximum(d,1e-6)
    return np.diag(d),dict(pooled_variance=pool,pilot_bias=pilot,observed_weight=mass)


def posterior_bias_and_evidence(c,x,noise,weights,bias_prior_variance):
    d=c.shape[0]
    precision=np.eye(d)/bias_prior_variance if bias_prior_variance is not None else None
    rhs=np.zeros(d);constant=0.;cache=[]
    for row,v,w in zip(x,noise,weights):
        obs=np.flatnonzero(np.isfinite(row));value=row[obs]
        r=c[np.ix_(obs,obs)]+np.diag(v[obs])
        inv,ld=inverse(r)
        constant-=.5*w*(len(obs)*np.log(2*np.pi)+ld+value@inv@value)
        if precision is not None:
            precision[np.ix_(obs,obs)]+=w*inv;rhs[obs]+=w*(inv@value)
        cache.append((obs,inv))
    if precision is None:return np.zeros(d),np.zeros((d,d)),float(constant),cache
    bvar,logdet_precision=inverse(precision);bmean=bvar@rhs
    evidence=constant-.5*d*np.log(bias_prior_variance)-.5*logdet_precision+.5*rhs@bmean
    return bmean,bvar,float(evidence),cache


def fit_covariance(x,noise,weights,kappa,bias_prior_variance=None):
    """Penalized EM with exact missing/measurement/bias conditional moments."""
    x=np.asarray(x,float);noise=np.asarray(noise,float);weights=np.asarray(weights,float)
    if x.ndim!=2 or x.shape!=noise.shape or len(weights)!=len(x):raise ValueError('Invalid dimensions')
    if (weights<=0).any() or not np.isfinite(weights).all():raise ValueError('Invalid weights')
    if not np.array_equal(np.isfinite(x),np.isfinite(noise)):raise ValueError('Missing noise/value mismatch')
    if (noise[np.isfinite(noise)]<0).any() or (np.isfinite(x).sum(axis=1)==0).any():raise ValueError('Invalid observed data')
    if kappa<=0:raise ValueError('Regularization must be positive')
    target,meta=make_target(x,noise,weights,kappa,bias_prior_variance)
    c=target.copy();objective=[];converged=False
    for iteration in range(CONFIG['max_iterations']):
        bmean,bvar,ll,cache=posterior_bias_and_evidence(c,x,noise,weights,bias_prior_variance)
        inv_c,logdet_c=inverse(c)
        obj=ll-.5*kappa*(logdet_c+np.trace(target@inv_c));objective.append(float(obj))
        if len(objective)>1 and obj<objective[-2]-1e-7*max(1,abs(obj)):
            raise RuntimeError('Penalized EM objective decreased')
        scatter=np.zeros_like(c)
        for row,w,(obs,inv) in zip(x,weights,cache):
            gain=c[:,obs]@inv
            m=gain@(row[obs]-bmean[obs])
            conditional=c-gain@c[obs,:]
            conditional+=gain@bvar[np.ix_(obs,obs)]@gain.T
            scatter+=w*(conditional+np.outer(m,m))
        new=(scatter+kappa*target)/(weights.sum()+kappa);new=(new+new.T)/2
        relative=np.linalg.norm(new-c)/max(np.linalg.norm(c),1e-12)
        c=new
        if relative<CONFIG['convergence_tolerance']:
            converged=True;break
    if not converged:raise RuntimeError(f'EM did not converge in {iteration+1} iterations: {relative}')
    bmean,bvar,ll,_=posterior_bias_and_evidence(c,x,noise,weights,bias_prior_variance)
    inv_c,ld=inverse(c);objective.append(float(ll-.5*kappa*(ld+np.trace(target@inv_c))))
    return dict(covariance=c,bias_mean=bmean,bias_covariance=bvar,target=target,
                objective=np.array(objective),iterations=iteration+1,relative_change=float(relative),
                min_eigenvalue=float(np.linalg.eigvalsh(c).min()),converged=converged,**meta)


def fit_component(history,year,kind,kappa):
    x,noise,w,years,h=blocks(history,year,kind)
    minimum=3 if kind=='poll' else 4
    if len(years)<minimum:raise ValueError('Insufficient earlier cycles')
    fit=fit_covariance(x,noise,w,kappa,CONFIG['bias_prior_sd_pp']**2 if kind=='poll' else None)
    mask=np.isfinite(x);support=mask.astype(int).T@mask.astype(int)
    weighted_pairs=(mask*w[:,None]).T@mask
    means=np.nansum(x*w[:,None],axis=0)/np.maximum(fit['observed_weight'],1e-12)
    means[fit['observed_weight']==0]=np.nan
    rms=np.sqrt(np.nansum(x*x*w[:,None],axis=0)/np.maximum(fit['observed_weight'],1e-12))
    rms[fit['observed_weight']==0]=np.nan
    fit.update(year=int(year),kind=kind,kappa=float(kappa),years=years,
               training_first_cycle=int(years.min()),training_max_cycle=int(years.max()),
               training_cycles=len(years),training_rows=len(h),pair_support=support,
               weighted_pair_support=weighted_pairs,residual_means=means,
               observed_rms=rms)
    return fit


def validation_score(history,year,kind,fit):
    _,_,_,_,h=blocks(history,year+1,kind)
    h=h[h.cycle==year]
    if h.empty:return None
    si=np.array([STATES.index(s) for s in h.geography])
    c=fit['covariance'][np.ix_(si,si)]+np.diag(h.noise.to_numpy())
    mean=fit['bias_mean'][si] if kind=='poll' else np.zeros(len(h))
    if kind=='poll':c+=fit['bias_covariance'][np.ix_(si,si)]
    inv,ld=inverse(c);delta=h.value.to_numpy()-mean
    nld=.5*(len(si)*np.log(2*np.pi)+ld+delta@inv@delta)/len(si)
    return float(nld),len(si)


def choose_fit(history,year,kind,cache):
    _,_,_,years,_=blocks(history,year,kind)
    minimum=3 if kind=='poll' else 4
    validation=[int(y) for i,y in enumerate(years) if i>=minimum][-CONFIG['validation_cycles']:]
    scenario=str(history.scenario.iloc[0]);rows=[];scores=[]
    def get(y,k):
        key=(scenario,int(y),kind,float(k))
        if key not in cache:cache[key]=fit_component(history,int(y),kind,float(k))
        return cache[key]
    for k in CONFIG['regularization_candidates']:
        vals=[]
        for vy in validation:
            f=get(vy,k);score,n=validation_score(history,vy,kind,f);vals.append(score)
            rows.append(dict(scenario=scenario,forecast_cycle=int(year),kind=kind,kappa=k,
                             validation_cycle=vy,fit_max_cycle=f['training_max_cycle'],n_states=n,nld_per_state=score))
        scores.append((float(np.mean(vals)) if vals else 0.,-k,k))
    chosen=min(scores)[2]
    result=get(year,chosen)
    result={**result,'validation_cycles':validation,'selection_score':min(scores)[0]}
    return result,rows


def predict(test,movement,poll,model='v2_linked',observe_ids=None):
    if test.geography.duplicated().any():raise ValueError('Multiple target contests in one state require multiseat extension')
    si=np.array([STATES.index(s) for s in test.geography]);prior=100*test.prior.to_numpy()
    k=movement['covariance'][np.ix_(si,si)].copy()
    if model in ['v2_movement_diagonal','v2_local']:k=np.diag(np.diag(k))
    obs=np.flatnonzero(test.q_pp.notna().to_numpy())
    if observe_ids is not None:obs=np.array([i for i in obs if test.target_id.iloc[i] in observe_ids],int)
    if len(obs):
        so=si[obs]
        r=poll['covariance'][np.ix_(so,so)]+poll['bias_covariance'][np.ix_(so,so)]
        r+=np.diag(CONFIG['fresh_firm_sd_pp']**2/test.firm_mass.to_numpy()[obs])
        if model=='v2_local':r=np.diag(np.diag(r))
        values=test.q_pp.to_numpy()[obs]-poll['bias_mean'][so]
        mean,cov,ll=v1.normal_update(prior,k,obs,values,r)
        gain=k[:,obs]@np.linalg.inv(k[np.ix_(obs,obs)]+r)
    else:mean,cov,ll=prior,k,0.;gain=np.zeros((len(test),0));r=np.empty((0,0))
    sd=np.sqrt(np.diag(cov))
    pred=test.copy().reset_index(drop=True)
    pred['prediction_pp']=mean;pred['prediction']=mean/100;pred['posterior_sd_pp']=sd
    pred['p_dem']=norm.cdf(mean/sd)
    for level in [50,70,80,95]:
        z=norm.ppf((1+level/100)/2)
        pred[f'lo{level}_pp']=mean-z*sd;pred[f'hi{level}_pp']=mean+z*sd
    pred['model']=model
    pred['log_predictive_density']=norm.logpdf(100*pred.actual,mean,sd)
    pred['outside_margin_bounds_probability']=norm.cdf((-100-mean)/sd)+norm.sf((100-mean)/sd)
    return pred,cov,dict(prior_covariance=k,observation_covariance=r,observed=obs,gain=gain,log_evidence=ll)


def build(lab):
    lab=Path(lab).resolve()
    source=lab/'reports/simple_bayesian_polling/20260919T044810.372303Z'
    source_hash=v1.verify(source)
    notebook_hashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='BAYESIAN_REVISION2.ipynb'}
    settings=json.loads((source/'settings.json').read_text())
    for p,digest in settings['provenance']['paths'].items():
        if v1.sha(p)!=digest:raise ValueError('Changed source: '+p)
    history=pd.read_parquet(source/'prepared_history.parquet')
    samples=pd.read_parquet(source/'samples.parquet')
    refs=pd.read_parquet(source/'predictions.parquet').replace({'model':{'linked':'v1_linked','local':'v1_local'}})
    ledger_path=next(Path(p) for p in settings['provenance']['paths'] if p.endswith('state_surprise/20260919T011532.132689Z/full_seat_ledger.parquet'))
    roster=pd.read_parquet(ledger_path).query("model=='polling'")
    out=lab/'reports/bayesian_revision2'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    out.mkdir(parents=True);(out/'fits').mkdir();(out/'draws').mkdir()
    cache={};tuning=[];fits=[];predictions=[];seats=[];state_stats=[];pairs=[];decomp=[];masked=[];gain_rows=[];trace=[]
    for (scenario,year),old in refs.query("model=='v1_linked'").groupby(['scenario','cycle']):
        hist=history[history.scenario==scenario]
        test=hist[hist.cycle==year].merge(old[['target_id','history_selection_10pp']],on='target_id',validate='one_to_one').sort_values('target_id').reset_index(drop=True)
        if set(test.target_id)!=set(old.target_id):raise ValueError('Unequal forecast cases')
        movement,rows=choose_fit(hist,int(year),'movement',cache);tuning.extend(rows)
        poll,rows=choose_fit(hist,int(year),'poll',cache);tuning.extend(rows)
        for component,f in [('movement',movement),('poll',poll)]:
            fits.append(dict(scenario=scenario,cycle=int(year),component=component,
                             **{k:f[k] for k in ['kappa','training_first_cycle','training_max_cycle','training_cycles','training_rows','iterations','relative_change','min_eigenvalue','pooled_variance','selection_score']},
                             validation_cycles=','.join(map(str,f['validation_cycles']))))
            sd=np.sqrt(np.diag(f['covariance']));corr=f['covariance']/np.outer(sd,sd)
            for i,s in enumerate(STATES):
                state_stats.append(dict(scenario=scenario,cycle=int(year),component=component,state=s,
                                        process_sd_pp=sd[i],target_sd_pp=np.sqrt(f['target'][i,i]),
                                        observed_cycles=int(f['pair_support'][i,i]),observed_weight=f['observed_weight'][i],
                                        residual_mean_pp=f['residual_means'][i],residual_rms_pp=f['observed_rms'][i],
                                        bias_poll_minus_final_pp=f['bias_mean'][i],bias_sd_pp=np.sqrt(f['bias_covariance'][i,i])))
                if year==2026:
                    for j in range(i+1,len(STATES)):
                        pairs.append(dict(component=component,state_a=s,state_b=STATES[j],correlation=corr[i,j],
                                          covariance_pp2=f['covariance'][i,j],shared_cycles=int(f['pair_support'][i,j]),
                                          shared_weight=f['weighted_pair_support'][i,j]))
        rr=roster[(roster.scenario==scenario)&(roster.cycle==year)]
        for mi,model in enumerate(MODELS):
            pred,cov,meta=predict(test,movement,poll,model)
            predictions.append(pred)
            rng=np.random.default_rng(CONFIG['seed']+int(year)+mi*101+(0 if scenario=='matched_live' else 555))
            draws=pred.prediction_pp.to_numpy()+rng.standard_normal((CONFIG['draws'],len(test)))@np.linalg.cholesky(cov).T
            np.savez_compressed(out/'draws'/f'{scenario}_{year}_{model}.npz',margins_pp=draws,covariance_pp2=cov,
                                prior_covariance_pp2=meta['prior_covariance'],target_ids=test.target_id.to_numpy(str))
            seat=v1.seat_counts(rr,test,pred,draws)
            counts=seat['fixed_D']+(draws>0).sum(axis=1)
            lo,hi=np.quantile(counts,[.15,.85],method='inverted_cdf')
            seat.update(expected_D_exact=float(seat['fixed_D']+pred.p_dem.sum()),D_lo70=int(lo),D_hi70=int(hi),
                        mass_in_70_interval=float(((counts>=lo)&(counts<=hi)).mean()))
            seats.append(dict(scenario=scenario,cycle=int(year),model=model,**seat))
            if year==2026 and model=='v2_linked':
                for i,t in test.iterrows():
                    own,_,_=predict(test,movement,poll,model,observe_ids={t.target_id})
                    decomp.append(dict(target_id=t.target_id,geography=t.geography,prior_pp=100*t.prior,raw_poll_pp=t.q_pp,
                                       own_poll_update_pp=float(own.prediction_pp.iloc[i]-100*t.prior),
                                       other_poll_update_pp=float(pred.prediction_pp.iloc[i]-own.prediction_pp.iloc[i]),
                                       posterior_pp=float(pred.prediction_pp.iloc[i]),prior_sd_pp=float(np.sqrt(meta['prior_covariance'][i,i])),
                                       posterior_sd_pp=float(pred.posterior_sd_pp.iloc[i]),sample_count=int(t.sample_count)))
                    for j,oi in enumerate(meta['observed']):
                        source_state=test.geography.iloc[oi];bi=STATES.index(source_state)
                        surprise=test.q_pp.iloc[oi]-100*test.prior.iloc[oi]-poll['bias_mean'][bi]
                        gain_rows.append(dict(target_state=t.geography,poll_state=source_state,gain=float(meta['gain'][i,j]),
                                              corrected_poll_surprise_pp=float(surprise),contribution_pp=float(meta['gain'][i,j]*surprise)))
        if year in [2020,2024,2026]:
            for i,t in test[test.q_pp.notna()].iterrows():
                hidden=test.copy();hidden.loc[hidden.geography.eq(t.geography),'q_pp']=np.nan
                for model in MODELS:
                    pred,_,_=predict(hidden,movement,poll,model)
                    record=pred.iloc[i][['prediction_pp','posterior_sd_pp','p_dem','lo95_pp','hi95_pp']].to_dict()
                    masked.append(dict(scenario=scenario,cycle=int(year),model=model,target_id=t.target_id,geography=t.geography,
                                       actual=t.actual,prior_pp=100*t.prior,**record))
        if year==2026:
            w=samples[(samples.scenario==scenario)&samples.target_id.isin(test.target_id)].sort_values(['available_date','target_id','sample_key']).reset_index(drop=True)
            checkpoints=sorted(set([0,len(w)]+list(range(1,len(w)+1,10))))
            for count in checkpoints:
                a=v1.aggregate(test,w.iloc[:count]);replay=test.drop(columns=a.columns.drop('target_id')).merge(a,on='target_id',validate='one_to_one')
                pred,_,_=predict(replay,movement,poll)
                for _,t in pred[pred.geography.isin(['AK','MI','NH','TX','CO'])].iterrows():
                    trace.append(dict(samples_seen=count,geography=t.geography,prediction_pp=t.prediction_pp,own_samples=int(t.sample_count),cutoff=t.context_id))
        print(f'{scenario} {year}: movement k={movement["kappa"]}, poll k={poll["kappa"]}; {len(test)} targets',flush=True)
    allpred=pd.concat(predictions+[refs],ignore_index=True)
    for _,g in allpred.groupby(['scenario','cycle']):
        sets=g.groupby('model').target_id.apply(set)
        if any(s!=sets.iloc[0] for s in sets):raise ValueError('Mismatched benchmark cases')
    allpred.to_parquet(out/'predictions.parquet',index=False)
    v1.scores(allpred).to_parquet(out/'metrics.parquet',index=False)
    for name,rows in [('fits',fits),('tuning',tuning),('seats',seats),('state_parameters',state_stats),('current_pairs',pairs),
                      ('current_decomposition',decomp),('masked_predictions',masked),('current_gain_contributions',gain_rows),('arrival_trace',trace)]:
        pd.DataFrame(rows).to_parquet(out/(name+'.parquet'),index=False)
    diagnostics=[]
    for (scenario,year,kind,kappa),f in cache.items():
        name=f'{scenario}_{year}_{kind}_k{str(kappa).replace(".","p")}.npz'
        np.savez_compressed(out/'fits'/name,**{k:f[k] for k in ['covariance','bias_mean','bias_covariance','target','objective','years','pair_support','weighted_pair_support']})
        diagnostics.append(dict(scenario=scenario,cycle=year,component=kind,kappa=kappa,training_max_cycle=f['training_max_cycle'],
                                iterations=f['iterations'],relative_change=f['relative_change'],converged=f['converged'],
                                min_eigenvalue=f['min_eigenvalue'],min_objective_increment=float(np.diff(f['objective']).min()),path='fits/'+name))
    pd.DataFrame(diagnostics).to_parquet(out/'fit_diagnostics.parquet',index=False)
    history.to_parquet(out/'prepared_history.parquet',index=False)
    v1.json_write(out/'settings.json',dict(config=CONFIG,source=str(source),source_manifest_sha256=source_hash,
                                        as_of=settings['as_of'],provenance=settings['provenance'],old_notebook_hashes=notebook_hashes,
                                        inference='Empirical Bayes: fixed penalized covariance estimates, integrated Gaussian state-bias uncertainty',
                                        covariance_parameter_uncertainty=False,features=False,promotion=False))
    for name in ['BAYESIAN_REVISION2_ESTIMATOR.md','CURRENT_BAYESIAN_MODEL.md']:(out/name).write_bytes((lab/name).read_bytes())
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    (out/'simple_bayesian_polling.py').write_bytes((lab/'scripts/simple_bayesian_polling.py').read_bytes())
    for name,digest in notebook_hashes.items():
        if v1.sha(lab/name)!=digest:raise RuntimeError('Existing notebook changed during run: '+name)
    v1.manifest(out)
    v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return out


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1])
    print(build(parser.parse_args().lab))
