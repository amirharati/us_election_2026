"""Chronological poll-age tuning, then a matched no-U Student likelihood study."""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import ndtr
import simple_bayesian_polling as v1
import bayesian_revision2 as v2
import simple_national_model as normal
import working_election_model as working
import national_factor_review as national
import national_tails_waves as chamber
import coverage_balance as scoring
import student_polling_likelihood as student

SOURCE='20260920T000314.601869Z'
HALVES=[14,30,60,90]
TIMING_ORDER=['gaussian30','gaussian14','gaussian60','gaussian90']
TAIL_ORDER=['timing_selected','student5','student10']
CONFIG=dict(half_lives_days=HALVES,student_df=[5,10],validation_cycles=3,selection_metric='seat_crps',
    draws=30000,seed=197139,as_of='2026-09-17',nodes=257,log_scale_bound=16.)
AGG=['q_pp','firm_mass','sample_count','firm_count','reported_n_total','unknown_release_count']


def aggregate(targets,waves,half):
    if not np.isfinite(half) or half<=0:raise ValueError('Positive finite half-life required')
    if targets.target_id.duplicated().any() or waves.duplicated(['target_id','sample_key']).any():raise ValueError('Duplicate target or sample')
    if len(waves) and ((waves.age_days<0).any() or not np.isfinite(waves[['age_days','margin']]).all().all()):raise ValueError('Invalid or future sample')
    if len(waves) and pd.to_datetime(waves.available_date).gt(pd.to_datetime(waves.cutoff)).any():raise ValueError('Future publication')
    groups=dict(tuple(waves.groupby('target_id')));rows=[]
    for t in targets.itertuples():
        w=groups.get(t.target_id);r=dict(target_id=t.target_id,q_pp=np.nan,firm_mass=0.,sample_count=0,firm_count=0,reported_n_total=0.,unknown_release_count=0,weighted_age_days=np.nan)
        if w is not None and len(w):
            a=np.exp2(-w.age_days.to_numpy(float)/half)/w.groupby('firm').firm.transform('size').to_numpy();mass=float(a.sum())
            if mass<=0:raise ValueError('Numerical weight underflow')
            r.update(q_pp=float(a@w.margin*100/mass),firm_mass=mass,sample_count=len(w),firm_count=w.firm.nunique(),
                reported_n_total=float(w.reported_n.sum()),unknown_release_count=int(w.publication_unknown.sum()),weighted_age_days=float(a@w.age_days/mass))
        rows.append(r)
    return pd.DataFrame(rows)


def replace_aggregate(h,a):
    result=h.drop(columns=[c for c in AGG+['weighted_age_days'] if c in h]).merge(a,on='target_id',how='left',validate='one_to_one')
    if result.firm_mass.isna().any():raise ValueError('Missing aggregate target')
    return result


def choose(scores,year,order):
    q=scores[scores.cycle.lt(year)&scores.model.isin(order)];years=sorted(q.cycle.unique())[-3:]
    if len(years)<3:return order[0],years,'early_fixed_fallback'
    q=q[q.cycle.isin(years)]
    if len(q)!=len(order)*3 or q.duplicated(['cycle','model']).any():raise ValueError('Incomplete chronological validation grid')
    vals=q.groupby('model').seat_crps.mean()
    if not np.isfinite(vals).all():raise ValueError('Nonfinite validation score')
    return min(order,key=lambda name:(vals[name],order.index(name))),years,'last_three_past_cycles_seat_CRPS'


def student_summary(test,d):
    p=student.summarize(test,d);means=d['means'];sd=np.sqrt(np.diagonal(d['covs'],axis1=1,axis2=2));w=d['weights']
    p['median_pp']=[brentq(lambda x:w@ndtr((x-means[:,j])/sd[:,j])-.5,float((means[:,j]-12*sd[:,j]).min()),float((means[:,j]+12*sd[:,j]).max())) for j in range(len(p))]
    return scoring.score_rows(p)


def build(lab):
    lab=Path(lab).resolve();designation,source,wt=working.load(lab)
    if source.name!=SOURCE or designation['model_id']!='no_U_K1':raise ValueError('Pinned no-U source required')
    src=json.loads((source/'settings.json').read_text());up=Path(src['upstream']);prior=Path(src['prior_source'])
    hashes={str(p):v1.verify(p) for p in [source,up,prior]}
    h=pd.read_parquet(up/'history.parquet');waves=pd.read_parquet(up/'samples.parquet');roster=pd.read_parquet(up/'full_seat_ledger.parquet')
    out=lab/'reports/poll_timing_student'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for name in ['fits','forecasts','recipe']:(out/name).mkdir(parents=True,exist_ok=True)
    print('OUTPUT',out,flush=True)
    settings=dict(config=CONFIG,sources=hashes,source=str(source),upstream=str(up),prior_source=str(prior),
        working_sha256=v1.sha(lab/'WORKING_MODEL.json'),old_notebook_hashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='POLL_TIMING_STUDENT.ipynb'},promotion=False,data_refreshed=False)
    v1.json_write(out/'settings.json',settings)
    histories={};aggregates=[];initial=[]
    for sc,hh in h.groupby('scenario'):
        ww=waves[waves.scenario.eq(sc)]
        for half in HALVES:
            a=aggregate(hh,ww,half);histories[(sc,half)]=replace_aggregate(hh,a);aggregates.append(a.assign(scenario=sc,half_life_days=half))
            if half==30:initial.append(np.allclose(a.q_pp,hh.q_pp,equal_nan=True) and np.allclose(a.firm_mass,hh.firm_mass))
    pd.concat(aggregates,ignore_index=True).to_parquet(out/'aggregates.parquet',index=False)
    predictions=[];seats=[];folds=[];calibration=[];fitdiag=[];tuning=[];integration=[];reproductions=[];fitcache={half:{} for half in HALVES};banks={}
    def save(name,half,test,p,cov,stats,meta,r,poll,draws,distribution=None):
        p=p.assign(model=name,half_life_days=half);predictions.append(p)
        ss,counts=chamber.seat_summary(roster[roster.scenario.eq(r.scenario)&roster.cycle.eq(r.cycle)],test,p,draws)
        ss.update(scenario=r.scenario,cycle=int(r.cycle),model=name,half_life_days=half);frequency=np.bincount(counts,minlength=101);seats.append(scoring.seat_scores(ss,frequency))
        path=f'forecasts/{r.scenario}_{r.cycle}_{name}.npz';arr=dict(target_ids=test.target_id.to_numpy(str),mean=p.prediction_pp.to_numpy(),covariance=cov,prior_covariance=meta['prior_covariance'],seat_count_frequency=frequency)
        if distribution is not None:arr.update({k:distribution[k] for k in ['means','covs','weights','scales']})
        np.savez_compressed(out/path,**arr)
        folds.append(dict(scenario=r.scenario,cycle=int(r.cycle),model=name,half_life_days=half,N_variance=r.N_variance,
            U_variance=0.,forecast_path=path,poll_path=f'fits/{r.scenario}_{r.cycle}_h{half}_noU.npz',**stats))
    # Stage 1: all four Gaussian timing candidates, with nested historical calibration.
    for r in wt['folds'].sort_values(['scenario','cycle']).itertuples():
        sc,year=r.scenario,int(r.cycle);original=wt['predictions'][wt['predictions'].scenario.eq(sc)&wt['predictions'].cycle.eq(year)].sort_values('target_id').reset_index(drop=True)
        movement=dict(np.load(source/f'fits/{sc}_{year}_movement_K1.npz'));budget=movement['budget'];rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));z=rng.standard_normal((CONFIG['draws'],len(original)))
        banks[(sc,year)]=dict(row=r,original=original,budget=budget,z=z,variants={})
        for half in HALVES:
            hist=histories[(sc,half)];a=aggregate(original,waves[waves.scenario.eq(sc)&waves.target_id.isin(original.target_id)],half);test=replace_aggregate(original,a)
            fit,trace=v2.choose_fit(hist,year,'poll',fitcache[half]);calibration.extend(dict(**x,half_life_days=half) for x in trace)
            x,noise,w,years,_=v2.blocks(hist,year,'poll');P=np.diag(fit['covariance'])+4.;poll=normal.fixed_common(x,noise,w,P,0.,9.)
            np.savez_compressed(out/f'fits/{sc}_{year}_h{half}_noU.npz',**poll,training_values=x,training_noise=noise,training_weights=w,years=years,kappa=fit['kappa'],raw_covariance=fit['covariance'])
            fitdiag.append(dict(scenario=sc,cycle=year,half_life_days=half,kappa=fit['kappa'],training_min_cycle=int(years.min()),training_max_cycle=int(years.max()),training_cycles=len(years),training_values=int(np.isfinite(x).sum()),iterations=fit['iterations'],converged=fit['converged']))
            p,cov,stats,meta=normal.predict(test,budget,r.N_variance,poll);stats.update(df=0,scale_mean=1.,p_scale_gt1=0.);draws=p.prediction_pp.to_numpy()+z@np.linalg.cholesky(cov).T
            save(f'gaussian{half}',half,test,p,cov,stats,meta,r,poll,draws)
            banks[(sc,year)]['variants'][half]=(test,p,cov,stats,meta,poll)
            if half==30:
                oldp=dict(np.load(source/f'fits/{sc}_{year}_poll.npz'));oldfreq=np.load(source/r.forecast_path)['seat_count_frequency'];frequency=np.bincount((draws>0).sum(axis=1)+seats[-1]['fixed_D'],minlength=101)
                ok=np.allclose(p[['prediction_pp','p_dem','lo70_pp','hi95_pp']],original[['prediction_pp','p_dem','lo70_pp','hi95_pp']],atol=1e-8) and np.array_equal(oldfreq,frequency) and np.allclose(P,oldp['budget']) and np.array_equal(x,oldp['training_values'],equal_nan=True)
                reproductions.append(dict(scenario=sc,cycle=year,passed=bool(ok),max_mean_difference_pp=float(abs(p.prediction_pp-original.prediction_pp).max())))
        print('TIMING',sc,year,'four half-lives calibrated and predicted',flush=True)
    # Persist and inspectable checkpoint before Student stage.
    pd.DataFrame(fitdiag).to_parquet(out/'calibration_fits.parquet',index=False);pd.DataFrame(calibration).to_parquet(out/'calibration_selection.parquet',index=False)
    v1.json_write(out/'reproduction.json',dict(passed=bool(all(initial) and all(x['passed'] for x in reproductions)),folds=reproductions))
    if not all(initial) or not all(x['passed'] for x in reproductions):raise AssertionError('30-day control failed reproduction')
    for (sc,year),bank in banks.items():
        s=pd.DataFrame(seats);chosen,years,status=choose(s[s.scenario.eq(sc)],year,TIMING_ORDER);half=int(chosen.removeprefix('gaussian'))
        test,p,cov,stats,meta,poll=bank['variants'][half];r=bank['row'];bank['selected_half']=half
        for name in TIMING_ORDER:
            q=s[s.scenario.eq(sc)&s.cycle.isin(years)&s.model.eq(name)]
            tuning.append(dict(stage='timing',scenario=sc,forecast_cycle=year,candidate=name,selected_model=chosen,validation_cycles=','.join(map(str,years)),status=status,mean_validation_CRPS=q.seat_crps.mean()))
        for table in [predictions,seats,folds]:
            if table is predictions:
                table.append(p.assign(model='timing_selected',half_life_days=half,selected_model=chosen))
            else:
                row=next(x for x in table if x['scenario']==sc and x['cycle']==year and x['model']==chosen);table.append(dict(row,model='timing_selected',selected_model=chosen))
    pd.concat(predictions,ignore_index=True).to_parquet(out/'timing_predictions.parquet',index=False);pd.DataFrame(seats).to_parquet(out/'timing_seats.parquet',index=False)
    print('TIMING COMPLETE; starting matched Student comparison',flush=True)
    # Stage 2 uses only the fold's previously selected timing recipe.
    for (sc,year),bank in banks.items():
        half=bank['selected_half'];test,gp,gcov,gstats,meta,poll=bank['variants'][half];r=bank['row'];k=meta['prior_covariance']
        gaussian=student.fit(test,k,poll,df=0);np.testing.assert_allclose(gaussian['mean'],gp.prediction_pp,atol=1e-9);np.testing.assert_allclose(gaussian['covariance'],gcov,atol=1e-9)
        rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));z=rng.standard_normal((CONFIG['draws'],len(test)));u=rng.random(CONFIG['draws'])
        for df in [5,10]:
            d=student.fit(test,k,poll,df=df);p=student_summary(test,d)
            for label,nodes,bound in [('double_nodes',513,16.),('wider_domain',321,20.)]:
                other=student.fit(test,k,poll,df=df,nodes=nodes,bound=bound)
                integration.append(dict(scenario=sc,cycle=year,df=df,check=label,edge_mass=d['edge_mass'],prior_grid_mass=d['prior_grid_mass'],**student.integration_check(test,d,other)))
            if d['edge_mass']>1e-8:raise AssertionError('Student grid edge mass')
            # E[N] conditional on each scale, then integrate; U remains zero.
            obs=np.flatnonzero(test.q_pp.notna());si=np.array([v1.STATES.index(x) for x in test.geography.iloc[obs]])
            fixed=poll['bias_covariance'][np.ix_(si,si)]+np.diag(16/test.firm_mass.to_numpy()[obs]);systematic=poll['covariance'][np.ix_(si,si)];surprise=test.q_pp.to_numpy()[obs]-poll['bias_mean'][si]-100*test.prior.to_numpy()[obs]
            nmeans=[];nvars=[]
            for scale in d['scales']:
                S=k[np.ix_(obs,obs)]+fixed+scale*systematic
                nmeans.append(r.N_variance*np.linalg.solve(S,surprise).sum() if len(obs) else 0.)
                nvars.append(r.N_variance-r.N_variance**2*np.linalg.solve(S,np.ones(len(obs))).sum() if len(obs) else r.N_variance)
            nm=float(d['weights']@nmeans);nv=float(d['weights']@(np.array(nvars)+np.array(nmeans)**2)-nm**2)
            stats=dict(N_mean_pp=nm,N_sd_pp=np.sqrt(max(nv,0)),U_mean_pp=0.,df=df,scale_mean=d['scale_mean'],p_scale_gt1=d['p_scale_gt1'],log_evidence=d['log_evidence'])
            p['historical_bias_pp']=poll['bias_mean'][[v1.STATES.index(x) for x in test.geography]];p['corrected_poll_pp']=p.q_pp-p.historical_bias_pp
            p['national_movement_pp']=nm;p['national_poll_error_pp']=0.
            p['poll_surprise_pp']=p.corrected_poll_pp-100*p.prior
            p['poll_local_sd_pp']=np.sqrt(poll['budget'][[v1.STATES.index(x) for x in test.geography]])
            # Gaussian-only conditional component columns inherited from test are invalid for mixtures.
            p=p.drop(columns=[c for c in ['local_electoral_update_pp','bias_posterior_adjustment_pp','local_poll_error_pp','old_historical_bias_pp','bias_change_pp'] if c in p])
            save(f'student{df}',half,test,p,d['covariance'],stats,meta,r,poll,student.sample(d,z,u),d)
        print('STUDENT',sc,year,'selected half-life',half,'df5/10 checked',flush=True)
    s=pd.DataFrame(seats)
    for (sc,year),bank in banks.items():
        chosen,years,status=choose(s[s.scenario.eq(sc)],year,TAIL_ORDER)
        for name in TAIL_ORDER:
            q=s[s.scenario.eq(sc)&s.cycle.isin(years)&s.model.eq(name)]
            tuning.append(dict(stage='distribution',scenario=sc,forecast_cycle=year,candidate=name,selected_model=chosen,validation_cycles=','.join(map(str,years)),status=status,mean_validation_CRPS=q.seat_crps.mean()))
        pp=pd.concat(predictions,ignore_index=True);predictions.append(pp[pp.scenario.eq(sc)&pp.cycle.eq(year)&pp.model.eq(chosen)].assign(model='distribution_selected',selected_model=chosen))
        for table in [seats,folds]:
            row=next(x for x in table if x['scenario']==sc and x['cycle']==year and x['model']==chosen);table.append(dict(row,model='distribution_selected',selected_model=chosen))
    for half,cache in fitcache.items():
        for (sc,year,kind,kappa),fit in cache.items():
            x,noise,w,years,_=v2.blocks(histories[(sc,half)],year,'poll');path=f'fits/calibration_{sc}_{year}_h{half}_k{kappa:g}.npz'
            np.savez_compressed(out/path,**{k:v for k,v in fit.items() if isinstance(v,np.ndarray)},training_values=x,training_noise=noise,training_weights=w)
    p=pd.concat(predictions,ignore_index=True);s=pd.DataFrame(seats);f=pd.DataFrame(folds)
    tables=dict(predictions=p,seats=s,folds=f,tuning=pd.DataFrame(tuning),integration_checks=pd.DataFrame(integration),summary=scoring.summarize_scores(p),chamber_summary=national.chamber_summary(s))
    for name,table in tables.items():table.to_parquet(out/(name+'.parquet'),index=False)
    for path in (lab/'scripts').glob('*.py'):(out/'recipe'/path.name).write_bytes(path.read_bytes())
    (out/'POLL_TIMING_STUDENT.md').write_bytes((lab/'POLL_TIMING_STUDENT.md').read_bytes())
    v1.manifest(out);audit(out,lab);report(out,lab)
    v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    print('COMPLETE',out,flush=True);return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);settings=json.loads((out/'settings.json').read_text())
    p=pd.read_parquet(out/'predictions.parquet');s=pd.read_parquet(out/'seats.parquet');f=pd.read_parquet(out/'folds.parquet');t=pd.read_parquet(out/'tuning.parquet');c=pd.read_parquet(out/'calibration_selection.parquet');fits=pd.read_parquet(out/'calibration_fits.parquet');integ=pd.read_parquet(out/'integration_checks.parquet');a=pd.read_parquet(out/'aggregates.parquet')
    _,source,wt=working.load(lab)
    checks=dict(sources_unchanged=all(v1.verify(path)==digest for path,digest in settings['sources'].items()),working_unchanged=v1.sha(lab/'WORKING_MODEL.json')==settings['working_sha256'],
        older_notebooks_preserved=all(v1.sha(lab/name)==digest for name,digest in settings['old_notebook_hashes'].items()),
        thirty_day_control_reproduces=json.loads((out/'reproduction.json').read_text())['passed'],historical_fit_past_only=bool(fits.training_max_cycle.lt(fits.cycle).all()),
        calibration_selection_nested=bool(c.fit_max_cycle.lt(c.validation_cycle).all() and c.validation_cycle.lt(c.forecast_cycle).all()),
        calibration_converged=bool(fits.converged.all()),unique_forecasts=not p.duplicated(['scenario','target_id','model']).any(),
        current_outcomes_missing=bool(p[p.cycle.eq(2026)][['actual','wis_pp','brier']].isna().all().all() and s[s.cycle.eq(2026)][['actual_D','seat_crps']].isna().all().all()),
        no_additive_shared_error=bool(f.U_variance.eq(0).all() and f.U_mean_pp.eq(0).all()),
        probability_bounds=bool(p.p_dem.between(0,1).all()),
        polling_surprise_columns_consistent=bool(np.allclose(p.poll_surprise_pp,p.q_pp-p.historical_bias_pp-100*p.prior,equal_nan=True)),
        integration_converges=bool(integ.max_mean_difference_pp.lt(1e-5).all() and integ.max_probability_difference.lt(1e-7).all() and integ.relative_covariance_difference.lt(1e-6).all() and integ.joint_nll_difference.lt(1e-7).all() and integ.edge_mass.lt(1e-8).all()),
        longer_decay_increases_information=bool(a.pivot(index=['scenario','target_id'],columns='half_life_days',values='firm_mass').diff(axis=1).iloc[:,1:].ge(-1e-10).all().all()))
    recon=[];priorok=[];seatok=[];selection=[];match=[]
    for r in f.itertuples():
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id').reset_index(drop=True);original=wt['predictions'][wt['predictions'].scenario.eq(r.scenario)&wt['predictions'].cycle.eq(r.cycle)].sort_values('target_id')
        z=np.load(out/r.forecast_path);poll=dict(np.load(out/r.poll_path));movement=dict(np.load(source/f'fits/{r.scenario}_{r.cycle}_movement_K1.npz'))
        priorok.append(np.array_equal(q.target_id,original.target_id) and np.array_equal(q.prior,original.prior) and np.array_equal(q.actual,original.actual,equal_nan=True) and np.allclose(z['prior_covariance'],normal.split_covariance(movement['budget'][[v1.STATES.index(x) for x in q.geography]],r.N_variance)))
        if 'weights' in z:
            d=dict(means=z['means'],covs=z['covs'],weights=z['weights'],mean=z['mean'],covariance=z['covariance']);expected=student_summary(q,d)
            fresh=student.fit(q,z['prior_covariance'],poll,df=int(r.df));recon.append(np.allclose(fresh['mean'],z['mean'],atol=1e-9) and np.allclose(fresh['covariance'],z['covariance'],atol=1e-9))
        else:
            expected,cov,_,_=normal.predict(q,movement['budget'],r.N_variance,poll);recon.append(np.allclose(cov,z['covariance'],atol=1e-9))
        recon.append(np.allclose(q[['prediction_pp','median_pp','p_dem','lo70_pp','hi95_pp']],expected[['prediction_pp','median_pp','p_dem','lo70_pp','hi95_pp']],atol=1e-8))
        ss=s[s.scenario.eq(r.scenario)&s.cycle.eq(r.cycle)&s.model.eq(r.model)].iloc[0];seatok.append(abs(ss.expected_D_exact-ss.fixed_D-q.p_dem.sum())<1e-9 and z['seat_count_frequency'].sum()==CONFIG['draws'] and ss.point_D==ss.fixed_D+q.prediction_pp.gt(0).sum())
        if r.model in ['student5','student10']:
            g=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq('timing_selected')].sort_values('target_id');match.append(r.half_life_days==g.half_life_days.iloc[0] and np.array_equal(q.q_pp,g.q_pp,equal_nan=True) and np.allclose(q.historical_bias_pp,g.historical_bias_pp))
    for r in t.drop_duplicates(['stage','scenario','forecast_cycle']).itertuples():
        chosen,years,status=choose(s[s.scenario.eq(r.scenario)],r.forecast_cycle,TIMING_ORDER if r.stage=='timing' else TAIL_ORDER)
        alias='timing_selected' if r.stage=='timing' else 'distribution_selected'
        qa=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq(alias)].sort_values('target_id');qb=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq(chosen)].sort_values('target_id')
        selection.append(chosen==r.selected_model and ','.join(map(str,years))==r.validation_cycles and status==r.status and np.allclose(qa[['half_life_days','prediction_pp','p_dem']],qb[['half_life_days','prediction_pp','p_dem']]))
    checks.update(priors_targets_labels_preserved=all(priorok),forecasts_reconstructed=all(recon),joint_seat_accounting=all(seatok),past_only_selection_reconstructed=all(selection),matched_student_inputs=all(match))
    result=dict(passed=all(checks.values()),checks=checks,forecast_rows=len(p),calibration_fits=len(fits),integration_comparisons=len(integ),older_notebooks=len(settings['old_notebook_hashes']))
    v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError([k for k,v in checks.items() if not v])
    v1.manifest(out);return result


def report(out,lab):
    out,lab=Path(out),Path(lab);p=pd.read_parquet(out/'predictions.parquet');s=pd.read_parquet(out/'seats.parquet');f=pd.read_parquet(out/'folds.parquet');t=pd.read_parquet(out/'tuning.parquet');summary=pd.read_parquet(out/'summary.parquet');cs=pd.read_parquet(out/'chamber_summary.parquet')
    cyc=p[p.actual.notna()].groupby(['scenario','cycle','model'],as_index=False).agg(n=('actual','size'),correct=('correct','sum'),mae_pp=('absolute_error_pp','mean'),wis_pp=('wis_pp','mean'),brier=('brier','mean'))
    cyc.to_parquet(out/'cycle_scores.parquet',index=False)
    text='# Poll timing and matched Student likelihood: results\n\nFrozen September 17 data. No-U national structure and electoral priors fixed. Timing and distribution selectors use the last three earlier held-out cycles; early forecasts retain 30 days/Gaussian.\n\n'
    cols=['scenario','model','n','correct','absolute_error_pp','wis_pp','brier','coverage70','coverage95']
    for period in ['recent_2016_2024','tuned_2018_2024','all_2012_2024']:
        text+='## '+period+'\n\n'+summary[summary.period.eq(period)&summary.group.eq('all')][cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Recent chamber scores\n\n'+cs[cs.period.eq('recent_2016_2024')].round(4).to_markdown(index=False)+'\n\n'
    text+='## Past-only selection\n\n'+t.drop_duplicates(['stage','scenario','forecast_cycle'])[['stage','scenario','forecast_cycle','selected_model','validation_cycles','status']].to_markdown(index=False)+'\n\n'
    text+='## Current forecasts\n\n'+s[s.cycle.eq(2026)][['model','half_life_days','point_D','point_R','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current national factor / tail scale\n\n'+f[f.cycle.eq(2026)][['model','half_life_days','N_mean_pp','N_sd_pp','df','scale_mean']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current state margins (D−R pp)\n\n'+p[p.cycle.eq(2026)].pivot(index='geography',columns='model',values='prediction_pp').round(3).to_markdown()+'\n\n'
    text+='## Per-cycle accuracy and margin error\n\n'+cyc.round(4).to_markdown(index=False)+'\n\n'
    text+='## Limits\n\nOnly five recent cycles; repeated exploratory selection. Student uses covariance-matched errors with one shared volatility scale, introducing tail dependence but no additive national polling bias. Historical calibration remains Gaussian empirical Bayes. Sampling time decay changes both the aggregate and its information mass, not just a moving average. No explicit election-day random walk or new polls/features. Inherited sample publication, candidate/ballot and seat-completion assumptions remain.\n'
    (lab/'POLL_TIMING_STUDENT_RESULTS.md').write_text(text);(out/'POLL_TIMING_STUDENT_RESULTS.md').write_text(text)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=cs[cs.period.eq('recent_2016_2024')&cs.scenario.eq(sc)].set_index('model');ax.plot(HALVES,[q.loc[f'gaussian{x}','seat_crps'] for x in HALVES],marker='o');ax.set(title=sc,xlabel='Poll-age half-life (days)',ylabel='Mean chamber CRPS (lower is better)')
    fig.tight_layout();fig.savefig(out/'timing_chamber.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=summary[summary.period.eq('recent_2016_2024')&summary.scenario.eq(sc)&summary.group.eq('all')].set_index('model')
        for name in ['gaussian30','timing_selected','student5','student10']:
            ax.plot([50,70,80,95],[100*q.loc[name,'coverage'+str(x)] for x in [50,70,80,95]],marker='o',label=name)
        ax.plot([50,95],[50,95],'k--');ax.set(title=sc,xlabel='Nominal interval (%)',ylabel='Observed coverage (%)');ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(out/'coverage.png',dpi=145);plt.close(fig)
    v1.manifest(out)


if __name__=='__main__':build(Path(__file__).resolve().parents[1])
