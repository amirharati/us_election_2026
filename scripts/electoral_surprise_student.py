"""Variance-matched Student national electoral surprises with Gaussian polling."""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
import simple_bayesian_polling as v1
import simple_national_model as normal
import student_polling_likelihood as student
import poll_timing_student as timing
import coverage_balance as scoring
import national_factor_review as national
import national_tails_waves as chamber

SOURCE='20260920T013619.322700Z'
FAMILIES=['none','both']
DISTS={'gaussian':0,'student10':10,'student5':5,'student3':3}
CONFIG=dict(draws=30000,seed=197139,validation_cycles=3,df=[0,10,5,3],nodes=513,bound=32.,as_of='2026-09-17',half_life_days=30)


def predict(test,prior_mean,k,poll,df,a,nodes=513,bound=32.):
    """Integrate only residual national electoral variance; polling stays Gaussian.

    Condition on the scalar national factor analytically, avoiding unstable
    subtraction of very large covariance matrices at extreme mixing scales.
    """
    from scipy.special import gammaln,logsumexp
    if df!=0 and df<=2: raise ValueError('Finite-variance Student requires df>2')
    if not np.isfinite(a) or a<0: raise ValueError('Invalid national variance')
    mu=np.asarray(prior_mean,float);k=np.asarray(k,float);n=len(test)
    if n<2: raise ValueError('This experiment requires at least two targets to recover the saved national covariance')
    common=float(k[0,1]);fv=common-a;local=np.diag(k)-common
    if fv < -1e-8 or np.any(local<=0) or not np.allclose(k,np.diag(local)+common*np.ones((n,n))): raise ValueError('Expected diagonal local plus shared national covariance')
    fv=max(fv,0.)
    obs=np.flatnonzero(test.q_pp.notna());so=np.array([v1.STATES.index(x) for x in test.geography.iloc[obs]],int)
    R=poll['covariance'][np.ix_(so,so)]+poll['bias_covariance'][np.ix_(so,so)]+np.diag(16/test.firm_mass.to_numpy()[obs])
    values=test.q_pp.to_numpy()[obs]-poll['bias_mean'][so]
    D=np.diag(local);H=D[np.ix_(obs,obs)]+R
    if len(obs):
        inv=np.linalg.inv(H);cross=D[:,obs];gain=cross@inv;localcov=D-gain@cross.T;loading=np.ones(n)-gain@np.ones(len(obs))
        innovation=values-mu[obs];h=float(np.ones(len(obs))@inv@np.ones(len(obs)));b=float(np.ones(len(obs))@inv@innovation)
        const=-.5*(len(obs)*np.log(2*np.pi)+np.linalg.slogdet(H)[1]+innovation@inv@innovation)
        localmean=mu+gain@innovation
    else:
        localcov=D;loading=np.ones(n);h=b=const=0.;localmean=mu
    if df==0 or a==0:
        scales=np.ones(1);logs=np.zeros(1);prior_mass=1.
    else:
        grid=np.linspace(-bound,bound,nodes);scales=np.exp(grid);shape=df/2;rate=(df-2)/2
        logs=shape*np.log(rate)-gammaln(shape)-shape*grid-rate/scales+np.log(grid[1]-grid[0]);logs[[0,-1]]-=np.log(2)
        prior_mass=float(np.exp(logsumexp(logs)))
    g=fv+a*scales;nv=g/(1+g*h);shift=nv*b
    evidence=const-.5*np.log1p(g*h)+.5*nv*b*b
    lw=logs+evidence;ll=float(logsumexp(lw));w=np.exp(lw-ll)
    means=localmean[None,:]+shift[:,None]*loading[None,:]
    covs=localcov[None,:,:]+nv[:,None,None]*np.outer(loading,loading)[None,:,:]
    mean=w@means;centered=means-mean;cov=np.einsum('k,kij->ij',w,covs)+np.einsum('k,ki,kj->ij',w,centered,centered)
    feature_mean=float(np.mean(mu-100*test.prior.to_numpy()));national_means=feature_mean+shift
    nm=float(w@national_means);nvar=float(w@(nv+(national_means-nm)**2))
    d=dict(means=means,covs=covs,weights=w,scales=scales,mean=mean,covariance=cov,log_evidence=ll,scale_mean=float(w@scales),p_scale_gt1=float(w[scales>1].sum()+(.5*w[scales==1].sum() if len(w)>1 else 0.)),edge_mass=float(w[:3].sum()+w[-3:].sum()) if len(w)>6 else 0.,prior_grid_mass=prior_mass,df=df,N_mean_pp=nm,N_sd_pp=np.sqrt(max(nvar,0.)),feature_mean_pp=feature_mean,coefficient_variance=fv,residual_variance=a)
    p=timing.student_summary(test,d);p['feature_shifted_prior_pp']=mu;p['national_movement_pp']=nm
    p['local_electoral_update_pp']=p.prediction_pp-100*p.prior-nm
    return p,d


def build(lab):
    lab=Path(lab).resolve();source=lab/'reports/national_feature_prior'/SOURCE
    st=json.loads((source/'settings.json').read_text());working=Path(st['source']);up=Path(st['upstream'])
    out=lab/'reports/electoral_surprise_student'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for sub in ['forecasts','recipe']:(out/sub).mkdir(parents=True,exist_ok=True)
    settings=dict(config=CONFIG,source=str(source),working=str(working),upstream=str(up),sources={str(x):v1.verify(x) for x in [source,working,up]},working_sha256=v1.sha(lab/'WORKING_MODEL.json'),old_notebook_hashes={x.name:v1.sha(x) for x in lab.glob('*.ipynb') if x.name!='ELECTORAL_SURPRISE_STUDENT.ipynb'},data_refreshed=False,promotion=False)
    v1.json_write(out/'settings.json',settings)
    orig=pd.read_parquet(source/'predictions.parquet');fold=pd.read_parquet(source/'folds.parquet');fold=fold[fold.model.isin(FAMILIES)];roster=pd.read_parquet(up/'full_seat_ledger.parquet')
    predictions=[];seats=[];folds=[];checks=[];reproductions=[]
    print('OUTPUT',out,flush=True)
    for (sc,year),ff in fold.groupby(['scenario','cycle']):
        pf=np.load(working/f'fits/{sc}_{year}_poll.npz');poll=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        for r in ff.itertuples():
            family=r.model;test=orig[orig.scenario.eq(sc)&orig.cycle.eq(year)&orig.model.eq(family)].sort_values('target_id').reset_index(drop=True)
            prior=np.load(source/r.forecast_path);mu=prior['prior_mean'];k=prior['prior_covariance'];fit=np.load(source/r.fit_path);a=float(fit['a'])
            rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));z=rng.standard_normal((CONFIG['draws'],len(test)));u=rng.random(CONFIG['draws'])
            for dist,df in DISTS.items():
                p,d=predict(test,mu,k,poll,df,a);name=f'{family}_{dist}';p=p.assign(model=name,family=family,distribution=dist,df=df);predictions.append(p)
                if not df:
                    cols=['prediction_pp','p_dem','lo70_pp','hi95_pp'];reproductions.append(bool(np.allclose(p[cols],test[cols],atol=1e-8) and np.allclose(d['covariance'],prior['covariance'])))
                else:
                    for label,nodes,bound in [('double_nodes',1025,32.),('wider_domain',641,40.)]:
                        _,other=predict(test,mu,k,poll,df,a,nodes=nodes,bound=bound)
                        checks.append(dict(scenario=sc,cycle=year,model=name,check=label,edge_mass=d['edge_mass'],prior_grid_mass=d['prior_grid_mass'],**student.integration_check(test,d,other)))
                draws=student.sample(d,z,u);ss,counts=chamber.seat_summary(roster[roster.scenario.eq(sc)&roster.cycle.eq(year)],test,p,draws);freq=np.bincount(counts,minlength=101)
                if not df:reproductions.append(bool(np.array_equal(freq,prior['seat_count_frequency'])))
                seats.append(scoring.seat_scores(dict(ss,scenario=sc,cycle=year,model=name,family=family,distribution=dist,df=df),freq))
                path=f'forecasts/{sc}_{year}_{name}.npz'
                np.savez_compressed(out/path,target_ids=test.target_id.to_numpy(str),prior_mean=mu,prior_covariance=k,seat_count_frequency=freq,**{x:d[x] for x in ['mean','covariance','means','covs','weights','scales']})
                folds.append(dict(scenario=sc,cycle=year,model=name,family=family,distribution=dist,df=df,feature_tau=r.tau,source_fit_path=r.fit_path,source_forecast_path=r.forecast_path,forecast_path=path,scale_mean=d['scale_mean'],p_scale_gt1=d['p_scale_gt1'],log_evidence=d['log_evidence'],N_mean_pp=d['N_mean_pp'],N_sd_pp=d['N_sd_pp'],feature_mean_pp=d['feature_mean_pp'],coefficient_variance=d['coefficient_variance'],residual_variance=a,joint_nll=student.joint_nll(100*test.actual.to_numpy(),d)))
        print(sc,year,'two families x four electoral-tail distributions complete',flush=True)
    p=pd.concat(predictions,ignore_index=True);s=pd.DataFrame(seats);f=pd.DataFrame(folds);trace=[];pp=[];ss=[];ff=[]
    for (sc,year,family),group in p.groupby(['scenario','cycle','family']):
        order=[f'{family}_{x}' for x in DISTS];chosen,years,status=timing.choose(s[s.scenario.eq(sc)],year,order)
        for table,dest in [(p,pp),(s,ss),(f,ff)]:dest.append(table[table.scenario.eq(sc)&table.cycle.eq(year)&table.model.eq(chosen)].assign(model=f'{family}_selected',selected_model=chosen))
        for candidate in order:
            q=s[s.scenario.eq(sc)&s.cycle.isin(years)&s.model.eq(candidate)];trace.append(dict(scenario=sc,forecast_cycle=year,family=family,candidate=candidate,selected_model=chosen,validation_cycles=','.join(map(str,years)),status=status,validation_crps=q.seat_crps.mean()))
    p=pd.concat([p,*pp],ignore_index=True);s=pd.concat([s,*ss],ignore_index=True);f=pd.concat([f,*ff],ignore_index=True)
    cyc=p[p.actual.notna()].groupby(['scenario','cycle','model'],as_index=False).agg(n=('actual','size'),correct=('correct','sum'),mae_pp=('absolute_error_pp','mean'),wis_pp=('wis_pp','mean'),brier=('brier','mean'))
    tables=dict(predictions=p,seats=s,folds=f,tuning=pd.DataFrame(trace),integration_checks=pd.DataFrame(checks),summary=scoring.summarize_scores(p),chamber_summary=national.chamber_summary(s),cycle_scores=cyc)
    for name,table in tables.items():table.to_parquet(out/f'{name}.parquet',index=False)
    v1.json_write(out/'reproduction.json',dict(passed=all(reproductions),checks=len(reproductions)))
    for path in (lab/'scripts').glob('*.py'):(out/'recipe'/path.name).write_bytes(path.read_bytes())
    (out/'ELECTORAL_SURPRISE_STUDENT.md').write_bytes((lab/'ELECTORAL_SURPRISE_STUDENT.md').read_bytes())
    v1.manifest(out);audit(out,lab);report(out,lab);v1.manifest(out)
    v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)))
    print('COMPLETE',out,flush=True);return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);st=json.loads((out/'settings.json').read_text());src=Path(st['source']);working=Path(st['working'])
    p=pd.read_parquet(out/'predictions.parquet');s=pd.read_parquet(out/'seats.parquet');f=pd.read_parquet(out/'folds.parquet');t=pd.read_parquet(out/'tuning.parquet');i=pd.read_parquet(out/'integration_checks.parquet');orig=pd.read_parquet(src/'predictions.parquet')
    c=dict(sources_unchanged=all(v1.verify(x)==h for x,h in st['sources'].items()),old_notebooks_preserved=all(v1.sha(lab/x)==h for x,h in st['old_notebook_hashes'].items()),working_unchanged=v1.sha(lab/'WORKING_MODEL.json')==st['working_sha256'],gaussian_reproduces=json.loads((out/'reproduction.json').read_text())['passed'],unique_forecasts=not p.duplicated(['scenario','target_id','model']).any(),current_labels_missing=bool(p[p.cycle.eq(2026)][['actual','wis_pp','brier']].isna().all().all() and s[s.cycle.eq(2026)][['actual_D','seat_crps']].isna().all().all()),integration_converged=bool(i.max_mean_difference_pp.lt(1e-5).all() and i.max_probability_difference.lt(1e-7).all() and i.relative_covariance_difference.lt(1e-6).all() and i.joint_nll_difference.lt(1e-7).all()),integration_mass=bool(i.edge_mass.lt(1e-8).all() and (i.prior_grid_mass-1).abs().lt(1e-8).all()),zero_shared_error=bool(p.national_poll_error_pp.eq(0).all()))
    recon=[];frozen=[];seatok=[];mass=[];chrono=[];selection=[];pollcache={}
    for r in f[~f.model.str.endswith('_selected')].itertuples():
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id').reset_index(drop=True);old=orig[orig.scenario.eq(r.scenario)&orig.cycle.eq(r.cycle)&orig.model.eq(r.family)].sort_values('target_id').reset_index(drop=True);z=np.load(out/r.forecast_path);g=np.load(src/r.source_forecast_path);fit=np.load(src/r.source_fit_path)
        chrono.append(fit['years'].max()<r.cycle)
        key=(r.scenario,r.cycle)
        if key not in pollcache:
            pf=np.load(working/f'fits/{r.scenario}_{r.cycle}_poll.npz');pollcache[key]=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        expected,d=predict(old,g['prior_mean'],g['prior_covariance'],pollcache[key],r.df,float(fit['a']))
        cols=['prediction_pp','p_dem','lo70_pp','hi95_pp'];recon.append(np.allclose(q[cols],expected[cols],atol=1e-9) and np.allclose(z['covariance'],d['covariance']))
        frozen.append(np.array_equal(g['prior_mean'],z['prior_mean']) and np.array_equal(g['prior_covariance'],z['prior_covariance']) and all(np.array_equal(q[x],old[x],equal_nan=True) for x in ['prior','q_pp','actual','historical_bias_pp','firm_mass']))
        mass.append(abs(z['weights'].sum()-1)<1e-10 and np.linalg.eigvalsh(z['covariance']).min()>0)
        sr=s[s.scenario.eq(r.scenario)&s.cycle.eq(r.cycle)&s.model.eq(r.model)].iloc[0];seatok.append(z['seat_count_frequency'].sum()==CONFIG['draws'] and abs(sr.expected_D_exact-sr.fixed_D-q.p_dem.sum())<1e-9 and sr.point_D==sr.fixed_D+q.prediction_pp.gt(0).sum())
    for r in t.drop_duplicates(['scenario','forecast_cycle','family']).itertuples():
        chosen,years,status=timing.choose(s[s.scenario.eq(r.scenario)],r.forecast_cycle,[f'{r.family}_{x}' for x in DISTS]);qa=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq(f'{r.family}_selected')].sort_values('target_id');qb=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq(chosen)].sort_values('target_id')
        selection.append(chosen==r.selected_model and ','.join(map(str,years))==r.validation_cycles and status==r.status and np.allclose(qa.prediction_pp,qb.prediction_pp))
    c.update(national_variance_only=bool(f.residual_variance.ge(0).all() and f.coefficient_variance.ge(0).all()),predictions_reconstructed=all(recon),feature_priors_polls_labels_preserved=all(frozen),valid_mixture_covariance=all(mass),training_past_only=all(chrono),seat_accounting=all(seatok),past_only_selection_reconstructed=all(selection))
    result=dict(passed=all(c.values()),checks=c,forecast_rows=len(p),fixed_fits=len(recon),integration_comparisons=len(i));v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError([k for k,v in c.items() if not v])
    v1.manifest(out);return result


def report(out,lab):
    out,lab=Path(out),Path(lab);p=pd.read_parquet(out/'predictions.parquet');su=pd.read_parquet(out/'summary.parquet');ch=pd.read_parquet(out/'chamber_summary.parquet');seats=pd.read_parquet(out/'seats.parquet');folds=pd.read_parquet(out/'folds.parquet')
    cyc=p[p.actual.notna()].groupby(['scenario','cycle','model'],as_index=False).agg(n=('actual','size'),correct=('correct','sum'),mae_pp=('absolute_error_pp','mean'),wis_pp=('wis_pp','mean'),brier=('brier','mean'),coverage70=('coverage70','mean'),coverage95=('coverage95','mean'))
    cyc=cyc.merge(seats[['scenario','cycle','model','actual_D','point_D','expected_D_exact','seat_crps','expected_seat_error']],on=['scenario','cycle','model'],validate='one_to_one').merge(folds[['scenario','cycle','model','joint_nll','scale_mean']],on=['scenario','cycle','model'],validate='one_to_one')
    # Delta-method Monte Carlo SE of discrete CRPS from saved draw frequencies.
    # Not historical sampling uncertainty; paired model-difference SE is not estimated.
    ses=[]
    for r in folds.itertuples():
        sr=seats[seats.scenario.eq(r.scenario)&seats.cycle.eq(r.cycle)&seats.model.eq(r.model)].iloc[0]
        if pd.isna(sr.actual_D):se=np.nan
        else:
            freq=np.load(out/r.forecast_path)['seat_count_frequency'];prob=freq/freq.sum();cdf=prob.cumsum();res=cdf-(np.arange(len(cdf))>=sr.actual_D)
            influence=2*(np.cumsum(res[::-1])[::-1]-np.dot(res,cdf));se=float(np.sqrt(np.dot(prob,influence**2)/freq.sum()))
        ses.append(dict(scenario=r.scenario,cycle=r.cycle,model=r.model,seat_crps_mcse=se))
    cyc=cyc.merge(pd.DataFrame(ses),on=['scenario','cycle','model'],validate='one_to_one')
    cyc.to_parquet(out/'cycle_comparison.parquet',index=False)
    periods={'earlier_2012_2014':[2012,2014],'comparison_2016_2018':[2016,2018],'focus_2020_2022':[2020,2022],'focus_2024':[2024]}
    groups=[]
    for label,years in periods.items():
        q=cyc[cyc.cycle.isin(years)]
        for (sc,model),g in q.groupby(['scenario','model']):
            groups.append(dict(period=label,scenario=sc,model=model,cycles=len(g),n=int(g.n.sum()),correct=int(g.correct.sum()),mae_pp=float(np.average(g.mae_pp,weights=g.n)),wis_pp=float(np.average(g.wis_pp,weights=g.n)),coverage70=float(np.average(g.coverage70,weights=g.n)),coverage95=float(np.average(g.coverage95,weights=g.n)),seat_crps=g.seat_crps.mean(),seat_mae=g.expected_seat_error.mean(),joint_nll=g.joint_nll.mean()))
    groups=pd.DataFrame(groups);groups.to_parquet(out/'period_comparison.parquet',index=False)
    text='# Student-t national electoral surprises: results\n\nOnly the national electoral residual has Student tails. Polling and local movement stay Gaussian. Feature fits and prior variances are frozen. Descriptive year groups are not labels used in training.\n\n'
    for title,tab in [('Recent state metrics',su[su.period.eq('recent_2016_2024')&su.group.eq('all')][['scenario','model','n','correct','absolute_error_pp','wis_pp','brier','coverage70','coverage95']]),('Recent chamber metrics',ch[ch.period.eq('recent_2016_2024')]),('Per-cycle comparison',cyc),('Descriptive period groups',groups),('Current seats',seats[seats.cycle.eq(2026)][['model','point_D','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95']]),('Current national movement',folds[folds.cycle.eq(2026)][['model','feature_tau','df','scale_mean','p_scale_gt1','feature_mean_pp','N_mean_pp','N_sd_pp']])]:
        text+='## '+title+'\n\n'+tab.round(4).to_markdown(index=False)+'\n\n'
    (out/'ELECTORAL_SURPRISE_STUDENT_RESULTS.md').write_text(text);(lab/'ELECTORAL_SURPRISE_STUDENT_RESULTS.md').write_text(text)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    for metric,label,file in [('seat_crps','Chamber CRPS (lower is better)','cycle_seat_crps.png'),('coverage70','State 70% interval coverage','cycle_coverage.png')]:
        fig,axes=plt.subplots(2,2,figsize=(12,7),layout='constrained')
        for row,family in enumerate(FAMILIES):
            for col,sc in enumerate(['matched_live','oct31']):
                ax=axes[row,col];q=cyc[cyc.scenario.eq(sc)&cyc.model.str.startswith(family+'_')&cyc.cycle.ge(2016)]
                for dist in DISTS:
                    g=q[q.model.eq(f'{family}_{dist}')].sort_values('cycle');ax.plot(g.cycle,g[metric],marker='o',label=dist)
                ax.set_title(('No features' if family=='none' else 'Momentum + approval')+' / '+('September' if sc=='matched_live' else 'October 31'));ax.set_xticks([2016,2018,2020,2022,2024]);ax.set_ylabel(label);ax.grid(alpha=.2)
                if metric=='coverage70':ax.axhline(.7,color='black',ls='--',lw=1);ax.set_ylim(0,1.05)
        handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside lower center',ncol=4)
        fig.savefig(out/file,dpi=150);plt.close(fig)


def load(lab):
    lab=Path(lab);root=lab/'reports/electoral_surprise_student';ptr=json.loads((root/'latest.json').read_text());out=root/ptr['artifact'];assert v1.verify(out)==ptr['manifest_sha256'];return out,{x.stem:pd.read_parquet(x) for x in out.glob('*.parquet')}

if __name__=='__main__':build(Path(__file__).resolve().parents[1])
