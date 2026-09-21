"""Two explicit common factors with fixed state marginal variance budgets."""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.stats import norm
import simple_bayesian_polling as v1
import bayesian_revision2 as v2
import coverage_balance as scoring
import national_tails_waves as chamber

SOURCE='20260919T233523.454509Z'
CONFIG=dict(as_of='2026-09-17',K_multipliers=[1,2],bias_prior_sd_pp=3.,
    systematic_budget_extra_variance_pp2=4.,fresh_variance_pp2=16.,
    validation_cycles=3,draws=30000,seed=197139,profile_points=33)
CANDIDATES=['national_K1','national_K2']
CONTROLS=['reference','reference_K2','common2','df_selected_g2','df_selected_g2_K2']


def split_covariance(budget,common):
    budget=np.asarray(budget,float)
    if budget.ndim!=1 or not np.isfinite(budget).all() or np.any(budget<=0):
        raise ValueError('Positive finite marginal variance budgets required')
    if not np.isfinite(common) or common<0 or common>=budget.min():
        raise ValueError('Common variance must be below every marginal budget')
    return common*np.ones((len(budget),len(budget)))+np.diag(budget-common)


def fit_common(values,noise,weights,budget,bias_prior_variance=None):
    """Fit one common variance; integrate historical persistent biases if present."""
    values=np.asarray(values,float);noise=np.asarray(noise,float);weights=np.asarray(weights,float)
    if values.shape!=noise.shape or values.shape[1]!=len(budget) or len(values)!=len(weights):
        raise ValueError('Inconsistent training arrays')
    if not np.array_equal(np.isfinite(values),np.isfinite(noise)) or np.any(weights<=0):
        raise ValueError('Missing data/weight mismatch')
    upper=float(np.min(budget)*(1-1e-8))
    def objective(common):
        c=split_covariance(budget,common)
        return -v2.posterior_bias_and_evidence(c,values,noise,weights,bias_prior_variance)[2]
    grid=np.linspace(0,upper,CONFIG['profile_points']);scores=np.array([objective(x) for x in grid])
    candidates=[(scores[0],0.),(scores[-1],upper)];success=[]
    for i in range(1,len(grid)-1):
        if scores[i]<=scores[i-1] and scores[i]<=scores[i+1]:
            r=minimize_scalar(objective,bounds=(grid[i-1],grid[i+1]),method='bounded',options={'xatol':1e-8})
            success.append(bool(r.success));candidates.append((float(r.fun),float(r.x)))
    best,common=min(candidates)
    covariance=split_covariance(budget,common)
    b,B,log_evidence,_=v2.posterior_bias_and_evidence(covariance,values,noise,weights,bias_prior_variance)
    return dict(common_variance=common,budget=np.asarray(budget),covariance=covariance,
                bias_mean=b,bias_covariance=B,log_evidence=log_evidence,upper=upper,
                at_lower=bool(common<1e-6),at_upper=bool(upper-common<max(1e-6,upper*1e-5)),
                optimizer_success=all(success),profile_grid=grid,profile_nll=scores,
                objective=best,training_values=values,training_noise=noise,training_weights=weights)


def fixed_common(values,noise,weights,budget,common,bias_prior_variance):
    covariance=split_covariance(budget,common)
    b,B,ll,_=v2.posterior_bias_and_evidence(covariance,values,noise,weights,bias_prior_variance)
    return dict(common_variance=common,budget=np.asarray(budget),covariance=covariance,
                bias_mean=b,bias_covariance=B,log_evidence=ll)


def predict(test,budget,a,poll):
    """Exact Gaussian prediction and explicit N/U/local/bias decomposition."""
    if test.geography.duplicated().any():raise ValueError('Duplicate state targets need a multiseat extension')
    si=np.array([v1.STATES.index(s) for s in test.geography]);obs=np.flatnonzero(test.q_pp.notna())
    so=si[obs];mu=100*test.prior.to_numpy();V=np.asarray(budget)[si]
    K=split_covariance(V,a);u=float(poll['common_variance'])
    P=poll['budget'][si];local_var=V-a;bias=poll['bias_mean'][si];B=poll['bias_covariance'][np.ix_(si,si)]
    fresh=CONFIG['fresh_variance_pp2']/test.firm_mass.to_numpy()[obs]
    R=split_covariance(P[obs],u) if len(obs) else np.empty((0,0))
    R=R+B[np.ix_(obs,obs)]+np.diag(fresh)
    values=test.q_pp.to_numpy()[obs]-bias[obs]
    mean,cov,ll=v1.normal_update(mu,K,obs,values,R)
    nmean=umean=0.;nvar=a;uvar=u;nucov=0.
    local=np.zeros(len(test));bias_update=np.zeros(len(test));noise_mean=np.full(len(test),np.nan)
    gain=np.zeros((len(test),len(obs)))
    if len(obs):
        S=K[np.ix_(obs,obs)]+R;v=values-mu[obs];sol=np.linalg.solve(S,v)
        total=float(sol.sum());precision=float(np.linalg.solve(S,np.ones(len(obs))).sum())
        nmean=a*total;umean=u*total;nvar=a-a*a*precision;uvar=u-u*u*precision;nucov=-a*u*precision
        local[obs]=local_var[obs]*sol;bias_update=B[:,obs]@sol
        noise_mean[obs]=(P[obs]-u+fresh)*sol
        gain=np.linalg.solve(S,K[obs,:]).T
    np.testing.assert_allclose(mu+nmean+local,mean,atol=1e-9)
    np.testing.assert_allclose(mean[obs]+bias[obs]+bias_update[obs]+umean+noise_mean[obs],test.q_pp.to_numpy()[obs],atol=1e-9)
    p=test.copy();sd=np.sqrt(np.diag(cov))
    p['prediction_pp']=mean;p['prediction']=mean/100;p['median_pp']=mean;p['posterior_sd_pp']=sd;p['p_dem']=norm.cdf(mean/sd)
    p['log_predictive_density']=norm.logpdf(100*p.actual,mean,sd)
    for level in scoring.LEVELS:
        width=norm.ppf((1+level/100)/2)*sd;p[f'lo{level}_pp']=mean-width;p[f'hi{level}_pp']=mean+width
    p['prior_pp']=mu;p['national_movement_pp']=nmean;p['local_electoral_update_pp']=local
    p['historical_bias_pp']=bias;p['bias_posterior_adjustment_pp']=bias_update
    p['national_poll_error_pp']=umean;p['local_poll_error_pp']=noise_mean
    p['corrected_poll_pp']=test.q_pp.to_numpy()-bias
    p['poll_surprise_pp']=p.corrected_poll_pp-mu
    p['prior_local_sd_pp']=np.sqrt(local_var)
    p['poll_local_sd_pp']=np.sqrt(P-u)
    stats=dict(N_mean_pp=nmean,N_sd_pp=np.sqrt(max(nvar,0)),U_mean_pp=umean,U_sd_pp=np.sqrt(max(uvar,0)),
               NU_covariance_pp2=nucov,NU_correlation=nucov/np.sqrt(nvar*uvar) if nvar*uvar>0 else np.nan,
               prior_N_sd_pp=np.sqrt(a),prior_U_sd_pp=np.sqrt(u),log_evidence=ll,
               polled_states=len(obs))
    return scoring.score_rows(p),cov,stats,dict(prior_covariance=K,observation_covariance=R,gain=gain,
        observed=obs,national_posterior_covariance=np.array([[nvar,nucov],[nucov,uvar]]))


def build(lab):
    lab=Path(lab).resolve();source=lab/'reports/coverage_balance'/SOURCE;source_sha=v1.verify(source)
    settings=json.loads((source/'settings.json').read_text());prior=Path(settings['prior_source']);upstream=Path(settings['upstream'])
    sf=pd.read_parquet(prior/'folds.parquet');sf=sf[sf.model.eq('control_state')]
    old=pd.read_parquet(prior/'predictions.parquet');roster=pd.read_parquet(upstream/'full_seat_ledger.parquet')
    cached=pd.read_parquet(source/'predictions.parquet');cached_seats=pd.read_parquet(source/'seats.parquet')
    out=lab/'reports/simple_national_model'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for name in ['fits','forecasts','recipe']:(out/name).mkdir(parents=True,exist_ok=True)
    print('OUTPUT',out,flush=True)
    s=dict(config=CONFIG,source=str(source),source_sha256=source_sha,prior_source=str(prior),prior_source_sha256=v1.verify(prior),
        upstream=str(upstream),upstream_sha256=v1.verify(upstream),promotion=False,polling_refreshed=False,
        old_notebook_hashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='SIMPLE_NATIONAL_MODEL.ipynb'})
    v1.json_write(out/'settings.json',s)
    predictions=[];seats=[];folds=[];fit_rows=[];profiles=[];links=[];fitchecks=[]
    for row in sf.sort_values(['scenario','cycle']).itertuples():
        sc,year=row.scenario,int(row.cycle)
        test=old[old.scenario.eq(sc)&old.cycle.eq(year)&old.model.eq('control_state')].sort_values('target_id').reset_index(drop=True)
        mz=dict(np.load(prior/row.movement_path));pz=dict(np.load(prior/row.poll_path));z=np.load(prior/row.forecast_path)
        assert np.array_equal(z['target_ids'],test.target_id.to_numpy(str))
        base_budget=np.diag(mz['covariance'])*z['multipliers'];si=np.array([v1.STATES.index(x) for x in test.geography])
        np.testing.assert_allclose(base_budget[si],np.diag(z['prior_covariance']))
        poll_budget=np.diag(pz['covariance'])+CONFIG['systematic_budget_extra_variance_pp2']
        fits={}
        for component,mult,raw,budget,bprior in [('movement_K1',1,mz,base_budget,None),('movement_K2',2,mz,2*base_budget,None),('poll',1,pz,poll_budget,9.)]:
            fit=fit_common(raw['training_values'],raw['training_noise'],raw['training_weights'],budget,bprior)
            fits[component]=fit;path=f'fits/{sc}_{year}_{component}.npz'
            np.savez_compressed(out/path,**{k:v for k,v in fit.items() if isinstance(v,np.ndarray)},years=raw['years'])
            fit_rows.append(dict(scenario=sc,cycle=year,component=component,common_variance=fit['common_variance'],
                common_sd_pp=np.sqrt(fit['common_variance']),upper=fit['upper'],at_lower=fit['at_lower'],at_upper=fit['at_upper'],
                optimizer_success=fit['optimizer_success'],training_min_cycle=int(raw['years'].min()),training_max_cycle=int(raw['years'].max()),
                training_cycles=len(raw['years']),objective=fit['objective'],path=path))
            profiles.extend(dict(scenario=sc,cycle=year,component=component,common_variance=x,nll=y) for x,y in zip(fit['profile_grid'],fit['profile_nll']))
            fitchecks.append(fit['optimizer_success'] and fit['objective']<=fit['profile_nll'].min()+1e-6 and raw['years'].max()<year)
        poll0=fixed_common(pz['training_values'],pz['training_noise'],pz['training_weights'],poll_budget,0.,9.)
        rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));normal=rng.standard_normal((CONFIG['draws'],len(test)))
        configurations=[('national_K1',1,True,True),('national_K2',2,True,True),
                        ('no_U_K1',1,True,False),('no_U_K2',2,True,False),('no_N_K2',2,False,True)]
        for model,mult,use_N,use_U in configurations:
            a=fits[f'movement_K{mult}']['common_variance'] if use_N else 0.;poll=fits['poll'] if use_U else poll0
            p,cov,stats,meta=predict(test,mult*base_budget,a,poll);p['model']=model
            p['old_historical_bias_pp']=pz['bias_mean'][si];p['bias_change_pp']=p.historical_bias_pp-p.old_historical_bias_pp
            predictions.append(p)
            draws=p.prediction_pp.to_numpy()+normal@np.linalg.cholesky(cov).T
            rr=roster[roster.scenario.eq(sc)&roster.cycle.eq(year)];ss,counts=chamber.seat_summary(rr,test,p,draws)
            ss.update(scenario=sc,cycle=year,model=model);frequency=np.bincount(counts,minlength=101)
            seats.append(scoring.seat_scores(ss,frequency))
            path=f'forecasts/{sc}_{year}_{model}.npz';np.savez_compressed(out/path,target_ids=test.target_id.to_numpy(str),
                mean=p.prediction_pp.to_numpy(),covariance=cov,seat_count_frequency=frequency,**meta)
            folds.append(dict(scenario=sc,cycle=year,model=model,K_multiplier=mult,mean_recipe=row.recipe,
                N_variance=a,U_variance=poll['common_variance'],training_max_cycle=row.training_max_cycle,
                source_forecast=row.forecast_path,source_movement=row.movement_path,source_poll=row.poll_path,forecast_path=path,**stats))
            if year==2026:
                idx=int(np.flatnonzero(test.geography.eq('MI'))[0]);obs=meta['observed'];v=p.poll_surprise_pp.to_numpy()[obs]
                for j,other in enumerate(obs):links.append(dict(model=model,state=test.geography.iloc[other],surprise_pp=v[j],gain=meta['gain'][idx,j],contribution_pp=meta['gain'][idx,j]*v[j]))
        print(sc,year,'national SD',round(np.sqrt(fits['movement_K2']['common_variance']),3),'poll-error SD',round(np.sqrt(fits['poll']['common_variance']),3),flush=True)
    p=pd.concat(predictions,ignore_index=True);seats=pd.DataFrame(seats);folds=pd.DataFrame(folds)
    cycle=p[p.actual.notna()].groupby(['scenario','cycle','model'],as_index=False).agg(wis_pp=('wis_pp','mean'))
    trace=[];selected=[];selected_seats=[];selected_folds=[]
    for sc,group in p.groupby('scenario'):
        for year in sorted(group.cycle.unique()):
            chosen,years,status=scoring.choose(cycle[cycle.scenario.eq(sc)],year,CANDIDATES)
            selected.append(group[group.cycle.eq(year)&group.model.eq(chosen)].assign(model='national_selected',selected_model=chosen))
            selected_seats.append(seats[seats.scenario.eq(sc)&seats.cycle.eq(year)&seats.model.eq(chosen)].assign(model='national_selected',selected_model=chosen))
            selected_folds.append(folds[folds.scenario.eq(sc)&folds.cycle.eq(year)&folds.model.eq(chosen)].assign(model='national_selected',selected_model=chosen))
            for candidate in CANDIDATES:
                vals=cycle[cycle.scenario.eq(sc)&cycle.cycle.isin(years)&cycle.model.eq(candidate)]
                trace.append(dict(scenario=sc,forecast_cycle=year,selected_model=chosen,candidate=candidate,status=status,
                    validation_cycles=','.join(map(str,years)),validation_max_cycle=max(years) if years else np.nan,validation_wis=vals.wis_pp.mean()))
    p=pd.concat([p,*selected,cached[cached.model.isin(CONTROLS)]],ignore_index=True)
    seats=pd.concat([seats,*selected_seats,cached_seats[cached_seats.model.isin(CONTROLS)]],ignore_index=True)
    folds=pd.concat([folds,*selected_folds],ignore_index=True)
    summary=scoring.summarize_scores(p);ch=[]
    for period,first in [('recent_2016_2024',2016),('tuned_2018_2024',2018),('all_2012_2024',2012)]:
        for (sc,model),g in seats[seats.cycle.between(first,2024)].groupby(['scenario','model']):
            ch.append(dict(period=period,scenario=sc,model=model,cycles=len(g),**g[['seat_crps','seat_wis','expected_seat_error','coverage70','coverage95','width70','width95']].mean().to_dict()))
    nb=pd.read_parquet(upstream/'nonbayesian_predictions.parquet');nb=nb[nb.model.eq('bias')]
    rows=[]
    for (sc,year),q in nb[nb.cycle.between(2016,2024)].groupby(['scenario','cycle']):
        ref=p[p.scenario.eq(sc)&p.cycle.eq(year)&p.model.eq('national_K1')][['target_id','actual']]
        q=q.merge(ref,on='target_id',validate='one_to_one',suffixes=('','_ref'))
        assert len(q)==len(ref) and np.allclose(q.actual,q.actual_ref)
        rows.append(dict(scenario=sc,cycle=year,model='nonbayesian_bias',n=len(q),correct=int(((q.prediction_pp>0)==(q.actual>0)).sum()),mae_pp=float(abs(q.prediction_pp-100*q.actual).mean())))
    for name,table in dict(predictions=p,seats=seats,folds=folds,fit_diagnostics=pd.DataFrame(fit_rows),fit_profiles=pd.DataFrame(profiles),
        cycle_scores=cycle,summary=summary,chamber_summary=pd.DataFrame(ch),tuning=pd.DataFrame(trace),mi_links=pd.DataFrame(links),nonbayesian_cycles=pd.DataFrame(rows)).items():table.to_parquet(out/(name+'.parquet'),index=False)
    for path in (lab/'scripts').glob('*.py'):(out/'recipe'/path.name).write_bytes(path.read_bytes())
    (out/'SIMPLE_NATIONAL_MODEL.md').write_bytes((lab/'SIMPLE_NATIONAL_MODEL.md').read_bytes())
    v1.json_write(out/'fit_checks.json',dict(passed=all(fitchecks),fits=len(fitchecks)))
    v1.manifest(out);audit(out,lab);report(out,lab)
    v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);s=json.loads((out/'settings.json').read_text())
    p=pd.read_parquet(out/'predictions.parquet');f=pd.read_parquet(out/'folds.parquet');fits=pd.read_parquet(out/'fit_diagnostics.parquet');t=pd.read_parquet(out/'tuning.parquet');seats=pd.read_parquet(out/'seats.parquet');cycle=pd.read_parquet(out/'cycle_scores.parquet')
    q=p[p.model.isin(CANDIDATES+['no_U_K1','no_U_K2','no_N_K2','national_selected'])]
    c={name+'_unchanged':v1.verify(s[name])==s[name+'_sha256'] for name in ['source','prior_source','upstream']}
    c.update(old_notebooks_unchanged=all(v1.sha(lab/name)==digest for name,digest in s['old_notebook_hashes'].items()),
        past_training=bool(fits.training_max_cycle.lt(fits.cycle).all() and f.training_max_cycle.lt(f.cycle).all()),
        optimizers_passed=json.loads((out/'fit_checks.json').read_text())['passed'],
        latent_mean_identity=bool(np.allclose(q.prior_pp+q.national_movement_pp+q.local_electoral_update_pp,q.prediction_pp,atol=1e-9)),
        unpolled_local_update_zero=bool(q[q.q_pp.isna()].local_electoral_update_pp.eq(0).all()),
        future_labels_scores_blank=bool(p[p.cycle.eq(2026)][['actual','wis_pp','correct','brier']].isna().all().all()),
        future_seat_scores_blank=bool(seats[seats.cycle.eq(2026)][['actual_D','seat_wis','seat_crps']].isna().all().all()),
        finite_forecasts=bool(np.isfinite(p[['prediction_pp','p_dem','lo95_pp','hi95_pp']]).all().all()),
        equal_cases=all(g.groupby('model').target_id.apply(frozenset).nunique()==1 for _,g in p.groupby(['scenario','cycle'])),
        unique_forecasts=not p.duplicated(['scenario','model','target_id']).any())
    ids=q.q_pp.notna();c['observation_decomposition']=bool(np.allclose(q.loc[ids,'prediction_pp']+q.loc[ids,'historical_bias_pp']+q.loc[ids,'bias_posterior_adjustment_pp']+q.loc[ids,'national_poll_error_pp']+q.loc[ids,'local_poll_error_pp'],q.loc[ids,'q_pp'],atol=1e-9))
    pinball=np.zeros(len(p));y=100*p.actual.to_numpy()
    for prob,column in [(.5,'median_pp')]+[(prob,f'{side}{level}_pp') for level in scoring.LEVELS for side,prob in [('lo',(1-level/100)/2),('hi',(1+level/100)/2)]]:
        e=y-p[column].to_numpy();pinball+=2*np.maximum(prob*e,(prob-1)*e)/9
    c['wis_quantile_identity']=bool(np.allclose(pinball,p.wis_pp,equal_nan=True,atol=1e-10))
    prior=Path(s['prior_source']);original=pd.read_parquet(prior/'predictions.parquet');checks=[];seatchecks=[];reconstructed=[]
    for r in f[f.model.ne('national_selected')].itertuples():
        test=q[q.scenario.eq(r.scenario)&q.cycle.eq(r.cycle)&q.model.eq(r.model)].sort_values('target_id');z=np.load(out/r.forecast_path)
        old=np.load(prior/r.source_forecast);checks.append(np.allclose(np.diag(z['prior_covariance']),r.K_multiplier*np.diag(old['prior_covariance'])) and np.linalg.eigvalsh(z['covariance']).min()>0)
        orig=original[original.scenario.eq(r.scenario)&original.cycle.eq(r.cycle)&original.model.eq('control_state')].sort_values('target_id')
        checks.append(np.array_equal(test.target_id,orig.target_id) and np.array_equal(test.prior,orig.prior))
        mf=dict(np.load(out/f'fits/{r.scenario}_{r.cycle}_movement_K{r.K_multiplier}.npz'))
        pf=dict(np.load(out/f'fits/{r.scenario}_{r.cycle}_poll.npz'))
        if r.model.startswith('no_U'):
            pf=fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        else:pf['common_variance']=r.U_variance
        expected,cc,latent,mm=predict(orig,mf['budget'],r.N_variance,pf)
        reconstructed.append(np.allclose(expected.prediction_pp,test.prediction_pp,atol=1e-9) and np.allclose(cc,z['covariance'],atol=1e-9)
            and np.allclose(expected.p_dem,test.p_dem,atol=1e-10) and np.allclose(mm['gain'],z['gain'],atol=1e-10)
            and abs(latent['N_mean_pp']-r.N_mean_pp)<1e-9 and abs(latent['U_mean_pp']-r.U_mean_pp)<1e-9)
        ss=seats[seats.scenario.eq(r.scenario)&seats.cycle.eq(r.cycle)&seats.model.eq(r.model)].iloc[0]
        seatchecks.append(z['seat_count_frequency'].sum()==CONFIG['draws'] and abs(ss.expected_D_exact-ss.fixed_D-test.p_dem.sum())<1e-9)
    c['prior_budgets_centers_preserved']=all(checks);c['joint_seat_accounting']=all(seatchecks);c['forecasts_reconstructed']=all(reconstructed)
    selected=[]
    for r in t.drop_duplicates(['scenario','forecast_cycle']).itertuples():
        chosen,years,status=scoring.choose(cycle[cycle.scenario.eq(r.scenario)],r.forecast_cycle,CANDIDATES)
        a=q[q.scenario.eq(r.scenario)&q.cycle.eq(r.forecast_cycle)&q.model.eq('national_selected')].sort_values('target_id')
        b=q[q.scenario.eq(r.scenario)&q.cycle.eq(r.forecast_cycle)&q.model.eq(chosen)].sort_values('target_id')
        selected.append(chosen==r.selected_model and status==r.status and ','.join(map(str,years))==r.validation_cycles and all(year<r.forecast_cycle for year in years) and np.allclose(a.prediction_pp,b.prediction_pp))
    c['chronological_selection_reconstructed']=all(selected)
    result=dict(passed=all(c.values()),checks=c,forecast_rows=len(p),variance_fits=len(fits),older_notebooks=len(s['old_notebook_hashes']))
    v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError([name for name,value in c.items() if not value])
    v1.manifest(out);return result


def report(out,lab):
    out,lab=Path(out),Path(lab);p=pd.read_parquet(out/'predictions.parquet');summary=pd.read_parquet(out/'summary.parquet');seats=pd.read_parquet(out/'seats.parquet');f=pd.read_parquet(out/'folds.parquet');fits=pd.read_parquet(out/'fit_diagnostics.parquet');ch=pd.read_parquet(out/'chamber_summary.parquet');t=pd.read_parquet(out/'tuning.parquet')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=f[f.scenario.eq(sc)&f.model.eq('national_selected')]
        ax.errorbar(q.cycle-.12,q.N_mean_pp,yerr=1.036*q.N_sd_pp,fmt='o-',label='Real national shift N')
        ax.errorbar(q.cycle+.12,q.U_mean_pp,yerr=1.036*q.U_sd_pp,fmt='s-',label='National polling error U')
        ax.axhline(0,color='black',lw=.7);ax.set(title=sc,xlabel='Forecast cycle',ylabel='D−R percentage points; 70% intervals');ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(out/'national_components.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=summary[summary.period.eq('recent_2016_2024')&summary.group.eq('all')&summary.scenario.eq(sc)].set_index('model')
        for model in ['national_K1','national_K2','national_selected','reference','df_selected_g2_K2']:
            ax.plot(scoring.LEVELS,[100*q.loc[model,f'coverage{x}'] for x in scoring.LEVELS],marker='o',label=model)
        ax.plot([50,95],[50,95],'k--');ax.set(title=sc,xlabel='Nominal interval (%)',ylabel='Observed coverage (%)');ax.legend(fontsize=7)
    fig.tight_layout();fig.savefig(out/'coverage.png',dpi=145);plt.close(fig)
    text='# Simple national model: results\n\nFrozen September17 inputs; Gaussian common electoral movement N and common polling error U, independent local deviations. State variance budgets and historical centers preserved. Bias is refitted under the simpler error model. No promotion.\n\n'
    text+='## Review findings\n\nThe chronological WIS selector chooses national_K1 for every evaluated cycle, including2026. Current2020/22/24 validation WIS is4.0373 forK1 versus4.1885 forK2. No scalar variance fit reaches either bound.\n\nAcross2016–2024, the selected simple model improves all-state MAE to6.630pp earlier and5.040pp late, versus6.980/5.250 for the old Gaussian reference and6.872/5.146 for old StudentK1. Correct calls are129/140 earlier and132/140 late. State WIS4.047/2.971 improves versus both, and95%coverage is95.7%earlier/92.1%late. This is not uniform improvement: competitive-state WIS worsens to3.834/2.716 versus Gaussian3.615/2.626; competitive calls45/54earlier and49/54late. Recent late chamber CRPS1.031 and expected-seatMAE1.526 are worse than reference0.879/1.288 and StudentK2 0.856/1.264.\n\nThe new current forecast is45D/55R by individual mean signs,47.760expectedD,70%45–51D,95%43–53D. K2 sensitivity is51Dpoint/49.652expected/70%46–54. Expected seats differ materially from summing mean-sign winners in close races; neither is a guaranteed chamber outcome.\n\nThe selected model estimates real national movementN=+0.967pp (posteriorSD2.073) and common polling errorU=+4.723pp (SD3.010), posterior correlation−0.492. These are inferred components, not observed2026errors. Current historical priorSDs are2.219pp forN and4.906pp forU. Identical loadings make N/U mean ratio equal their prior variance ratio. Bias also changes under the simpler history model; MI bias mean−0.079 versusold−0.202.\n\nMichigan decomposes as priorD+5.023 + nationalD+0.967 + local−6.219 =R+0.229, P(D)=48.6%. Thus the national electoral factor helps Democrats; the inferred common overpolling leads to the Republican local correction needed to reconcile Michigan polls. Setting U=0 atK1 givesMI D+3.804 and51Dpoint/50.130expectedseats, but worsens recent late stateMAE5.040→5.374; it improves seatCRPS1.031→0.756. As before, state and chamber objectives favor different assumptions. Preserve this simple interpretable challenger and the old reference; discuss the allocation and objective before more features or factors.\n\n'
    cols=['scenario','model','n','correct','absolute_error_pp','wis_pp','brier','coverage70','coverage95','width95_pp']
    for period in ['recent_2016_2024','tuned_2018_2024','all_2012_2024']:
        text+='## '+period+'\n\n'+summary[summary.period.eq(period)&summary.group.eq('all')][cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Joint chamber results\n\n'+ch[ch.period.eq('recent_2016_2024')].round(4).to_markdown(index=False)+'\n\n'
    text+='## Fitted variance allocation\n\nBounds preserve every state marginal variance. At an upper bound the tightest state consumes nearly its entire variance budget in the common component; this is a structural restriction, not precise evidence about a national SD.\n\n'+fits[['scenario','cycle','component','common_sd_pp','at_lower','at_upper','training_min_cycle','training_max_cycle','training_cycles']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Selection\n\n'+t.drop_duplicates(['scenario','forecast_cycle'])[['scenario','forecast_cycle','selected_model','validation_cycles','status']].to_markdown(index=False)+'\n\n'
    text+='## National shift versus polling error\n\nBoth have identical+1 loadings; current polls inform their sum, while history assigns the split.\n\n'+f[f.model.eq('national_selected')][['scenario','cycle','N_mean_pp','N_sd_pp','U_mean_pp','U_sd_pp','NU_correlation','prior_N_sd_pp','prior_U_sd_pp']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current full chamber\n\n'+seats[seats.cycle.eq(2026)][['model','point_D','point_R','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95']].round(3).to_markdown(index=False)+'\n\n'
    q=p[p.cycle.eq(2026)&p.model.eq('national_selected')]
    text+='## Current state decomposition\n\nPrior+N+local electoral update=final; positive is Democratic.\n\n'+q[['geography','q_pp','historical_bias_pp','bias_change_pp','prior_pp','national_movement_pp','local_electoral_update_pp','prediction_pp','p_dem']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Michigan\n\n'+p[p.cycle.eq(2026)&p.geography.eq('MI')][['model','prediction_pp','p_dem','prior_pp','national_movement_pp','local_electoral_update_pp','historical_bias_pp','national_poll_error_pp']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Limits\n\nThis simplifies dependence rather than rebuilding historical mean/variance calibration. Two new scalar variances are plug-in empirical-Bayes estimates; inherited state budgets, recency weights and bias prior remain assumptions. National variance is bounded by the smallest state budget. N/U separation is prior/history-driven with identical loadings. Candidate effects, incomplete covariance-parameter uncertainty, extensive exploratory comparisons and fixed unmodeled-seat completion remain. No automatic promotion, no Student re-expansion, no new features.\n'
    (lab/'SIMPLE_NATIONAL_MODEL_RESULTS.md').write_text(text);(out/'SIMPLE_NATIONAL_MODEL_RESULTS.md').write_text(text);v1.manifest(out)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1]);args=parser.parse_args();build(args.lab)
