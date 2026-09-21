"""Coverage-adaptive decay with chronological calibration and held-out selection."""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
import poll_timing_student as timing
import simple_bayesian_polling as v1
import bayesian_revision2 as v2
import simple_national_model as normal
import working_election_model as working
import national_factor_review as national
import national_tails_waves as chamber
import coverage_balance as scoring

TIMING_SOURCE='20260920T010213.228282Z'
ORDER=['adaptive3','adaptive1','adaptive6']
KS=[1,3,6]
BASELINES=['gaussian30','gaussian90','timing_selected']
CONFIG=dict(k_choices=KS,count_window_days=60,min_half_life_days=30,max_half_life_days=90,validation_cycles=3,draws=30000,seed=197139,as_of='2026-09-17')


def half_life(n,k):
    if not np.isfinite(k) or k<=0:raise ValueError('Positive k required')
    n=np.asarray(n,float)
    if not np.isfinite(n).all() or np.any(n<0):raise ValueError('Nonnegative finite count required')
    return 30+60/(1+n/k)


def aggregate(targets,waves,k):
    # Reuse the existing validation and information-weight implementation per target.
    if targets.target_id.duplicated().any() or waves.duplicated(['target_id','sample_key']).any():raise ValueError('Duplicate target/sample')
    half_life(0,k)
    groups=dict(tuple(waves.groupby('target_id')));rows=[]
    for idx,t in targets.iterrows():
        w=groups.get(t.target_id,waves.iloc[:0]);n=int(w.loc[w.age_days.le(60),'firm'].nunique());half=float(half_life(n,k))
        a=timing.aggregate(targets.loc[[idx]],w,half).iloc[0].to_dict()
        a.update(recent_firms=n,half_life_days=half,k=k);rows.append(a)
    return pd.DataFrame(rows)


def coverage_group(n):
    n=np.asarray(n);return np.select([n==0,n<=2,n<=5],['0','1-2','3-5'],default='6+')


def build(lab):
    lab=Path(lab).resolve();_,source,wt=working.load(lab);baseline=lab/'reports/poll_timing_student'/TIMING_SOURCE
    bsettings=json.loads((baseline/'settings.json').read_text());up=Path(bsettings['upstream']);h=pd.read_parquet(up/'history.parquet');waves=pd.read_parquet(up/'samples.parquet');roster=pd.read_parquet(up/'full_seat_ledger.parquet')
    if str(source)!=bsettings['source']:raise ValueError('Mismatched working/timing source')
    out=lab/'reports/adaptive_poll_decay'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for name in ['fits','forecasts','recipe']:(out/name).mkdir(parents=True,exist_ok=True)
    print('OUTPUT',out,flush=True)
    settings=dict(config=CONFIG,source=str(source),baseline=str(baseline),upstream=str(up),sources={str(p):v1.verify(p) for p in [source,baseline,up]},
        working_sha256=v1.sha(lab/'WORKING_MODEL.json'),old_notebook_hashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='ADAPTIVE_POLL_DECAY.ipynb'},promotion=False,data_refreshed=False)
    v1.json_write(out/'settings.json',settings)
    aggregates=[];histories={};cache={k:{} for k in KS}
    for sc,hh in h.groupby('scenario'):
        ww=waves[waves.scenario.eq(sc)]
        for k in KS:
            a=aggregate(hh,ww,k);histories[(sc,k)]=timing.replace_aggregate(hh,a);aggregates.append(a.assign(scenario=sc))
    ag=pd.concat(aggregates,ignore_index=True);ag.to_parquet(out/'aggregates.parquet',index=False)
    predictions=[];seats=[];folds=[];cal=[];diag=[]
    for r in wt['folds'].sort_values(['scenario','cycle']).itertuples():
        sc,year=r.scenario,int(r.cycle);original=wt['predictions'][wt['predictions'].scenario.eq(sc)&wt['predictions'].cycle.eq(year)].sort_values('target_id').reset_index(drop=True)
        budget=np.load(source/f'fits/{sc}_{year}_movement_K1.npz')['budget'];rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));z=rng.standard_normal((CONFIG['draws'],len(original)))
        for k in KS:
            name=f'adaptive{k}';hist=histories[(sc,k)];a=ag[ag.scenario.eq(sc)&ag.k.eq(k)&ag.target_id.isin(original.target_id)].drop(columns='scenario');test=timing.replace_aggregate(original,a)
            fit,trace=v2.choose_fit(hist,year,'poll',cache[k]);cal.extend(dict(**x,k=k) for x in trace)
            x,noise,w,years,_=v2.blocks(hist,year,'poll');P=np.diag(fit['covariance'])+4.;poll=normal.fixed_common(x,noise,w,P,0.,9.)
            fp=f'fits/{sc}_{year}_k{k}_noU.npz';np.savez_compressed(out/fp,**poll,training_values=x,training_noise=noise,training_weights=w,years=years,kappa=fit['kappa'],raw_covariance=fit['covariance'])
            diag.append(dict(scenario=sc,cycle=year,k=k,kappa=fit['kappa'],training_max_cycle=int(years.max()),training_cycles=len(years),iterations=fit['iterations'],converged=fit['converged']))
            p,cov,stats,meta=normal.predict(test,budget,r.N_variance,poll);p['model']=name;predictions.append(p)
            draws=p.prediction_pp.to_numpy()+z@np.linalg.cholesky(cov).T;ss,counts=chamber.seat_summary(roster[roster.scenario.eq(sc)&roster.cycle.eq(year)],test,p,draws);ss.update(scenario=sc,cycle=year,model=name,k=k)
            frequency=np.bincount(counts,minlength=101);seats.append(scoring.seat_scores(ss,frequency));path=f'forecasts/{sc}_{year}_{name}.npz'
            np.savez_compressed(out/path,target_ids=test.target_id.to_numpy(str),mean=p.prediction_pp.to_numpy(),covariance=cov,prior_covariance=meta['prior_covariance'],seat_count_frequency=frequency)
            folds.append(dict(scenario=sc,cycle=year,model=name,k=k,artifact=str(out),forecast_path=path,poll_path=fp,N_variance=r.N_variance,U_variance=0.,half_life_min=float(p.half_life_days.min()),half_life_max=float(p.half_life_days.max()),**stats))
        print(sc,year,'k1/3/6 complete',flush=True)
    p=pd.concat(predictions,ignore_index=True);s=pd.DataFrame(seats);f=pd.DataFrame(folds);tuning=[];selected=[];sselected=[];fselected=[]
    for (sc,year),q in p.groupby(['scenario','cycle']):
        chosen,years,status=timing.choose(s[s.scenario.eq(sc)],year,ORDER)
        selected.append(q[q.model.eq(chosen)].assign(model='adaptive_selected',selected_model=chosen));sselected.append(s[s.scenario.eq(sc)&s.cycle.eq(year)&s.model.eq(chosen)].assign(model='adaptive_selected',selected_model=chosen));fselected.append(f[f.scenario.eq(sc)&f.cycle.eq(year)&f.model.eq(chosen)].assign(model='adaptive_selected',selected_model=chosen))
        for name in ORDER:
            vals=s[s.scenario.eq(sc)&s.cycle.isin(years)&s.model.eq(name)]
            tuning.append(dict(scenario=sc,forecast_cycle=year,candidate=name,selected_model=chosen,validation_cycles=','.join(map(str,years)),status=status,mean_validation_CRPS=vals.seat_crps.mean()))
    p=pd.concat([p,*selected],ignore_index=True);s=pd.concat([s,*sselected],ignore_index=True);f=pd.concat([f,*fselected],ignore_index=True)
    bp=pd.read_parquet(baseline/'predictions.parquet');bs=pd.read_parquet(baseline/'seats.parquet');bf=pd.read_parquet(baseline/'folds.parquet')
    counts=ag[ag.k.eq(3)][['scenario','target_id','recent_firms']]
    bp=bp[bp.model.isin(BASELINES)].merge(counts,on=['scenario','target_id'],validate='many_to_one');bf=bf[bf.model.isin(BASELINES)].assign(artifact=str(baseline))
    p=pd.concat([p,bp],ignore_index=True);p['recent_coverage_group']=coverage_group(p.recent_firms.to_numpy());s=pd.concat([s,bs[bs.model.isin(BASELINES)]],ignore_index=True);f=pd.concat([f,bf],ignore_index=True)
    subgroup=[]
    for period,first in [('recent_2016_2024',2016),('all_2012_2024',2012)]:
        for (sc,name,group),q in p[p.cycle.between(first,2024)].groupby(['scenario','model','recent_coverage_group']):
            metrics=q.groupby('cycle')[['absolute_error_pp','wis_pp','brier']].mean().mean().to_dict()
            subgroup.append(dict(period=period,scenario=sc,model=name,recent_firms=group,n=len(q),cycles=q.cycle.nunique(),correct=int(q.correct.sum()),**metrics))
    cyc=p[p.actual.notna()].groupby(['scenario','cycle','model'],as_index=False).agg(n=('actual','size'),correct=('correct','sum'),mae_pp=('absolute_error_pp','mean'),wis_pp=('wis_pp','mean'),brier=('brier','mean'))
    for k,c in cache.items():
        for (sc,year,kind,kappa),fit in c.items():
            x,noise,w,years,_=v2.blocks(histories[(sc,k)],year,'poll')
            np.savez_compressed(out/f'fits/calibration_{sc}_{year}_k{k}_reg{kappa:g}.npz',**{key:v for key,v in fit.items() if isinstance(v,np.ndarray)},training_values=x,training_noise=noise,training_weights=w)
    tables=dict(predictions=p,seats=s,folds=f,tuning=pd.DataFrame(tuning),calibration_selection=pd.DataFrame(cal),calibration_fits=pd.DataFrame(diag),summary=scoring.summarize_scores(p),chamber_summary=national.chamber_summary(s),coverage_groups=pd.DataFrame(subgroup),cycle_scores=cyc)
    for name,table in tables.items():table.to_parquet(out/(name+'.parquet'),index=False)
    for path in (lab/'scripts').glob('*.py'):(out/'recipe'/path.name).write_bytes(path.read_bytes())
    (out/'ADAPTIVE_POLL_DECAY.md').write_bytes((lab/'ADAPTIVE_POLL_DECAY.md').read_bytes())
    v1.manifest(out);audit(out,lab);report(out,lab);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    print('COMPLETE',out,flush=True);return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);st=json.loads((out/'settings.json').read_text());source=Path(st['source']);baseline=Path(st['baseline']);up=Path(st['upstream'])
    p=pd.read_parquet(out/'predictions.parquet');s=pd.read_parquet(out/'seats.parquet');f=pd.read_parquet(out/'folds.parquet');a=pd.read_parquet(out/'aggregates.parquet');t=pd.read_parquet(out/'tuning.parquet');cal=pd.read_parquet(out/'calibration_selection.parquet');fd=pd.read_parquet(out/'calibration_fits.parquet')
    h=pd.read_parquet(up/'history.parquet');waves=pd.read_parquet(up/'samples.parquet');_,_,wt=working.load(lab)
    c=dict(sources_unchanged=all(v1.verify(path)==digest for path,digest in st['sources'].items()),working_unchanged=v1.sha(lab/'WORKING_MODEL.json')==st['working_sha256'],older_notebooks_preserved=all(v1.sha(lab/name)==digest for name,digest in st['old_notebook_hashes'].items()),
        current_labels_missing=bool(p[p.cycle.eq(2026)][['actual','wis_pp','brier']].isna().all().all() and s[s.cycle.eq(2026)][['actual_D','seat_crps']].isna().all().all()),
        unique_forecasts=not p.duplicated(['scenario','target_id','model']).any(),adaptive_bounds=bool(a.half_life_days.between(30,90).all()),
        adaptive_formula=bool(np.allclose(a.half_life_days,30+60/(1+a.recent_firms/a.k))),historical_fit_past_only=bool(fd.training_max_cycle.lt(fd.cycle).all()),nested_calibration_past_only=bool(cal.fit_max_cycle.lt(cal.validation_cycle).all() and cal.validation_cycle.lt(cal.forecast_cycle).all()),
        calibration_converged=bool(fd.converged.all()),no_additive_U=bool(f.U_variance.eq(0).all() and f.U_mean_pp.eq(0).all()),probability_bounds=bool(p.p_dem.between(0,1).all()),no_poll_remains_missing=bool(a[a.sample_count.eq(0)].q_pp.isna().all() and a[a.sample_count.eq(0)].firm_mass.eq(0).all()))
    aggok=[];histories={};countok=[]
    for (sc,k),q in a.groupby(['scenario','k']):
        ww=waves[waves.scenario.eq(sc)];hh=h[h.scenario.eq(sc)];expected=aggregate(hh,ww,k).set_index('target_id').sort_index();q=q.set_index('target_id').sort_index()
        aggok.append(np.allclose(q[['q_pp','firm_mass','half_life_days','recent_firms']],expected[['q_pp','firm_mass','half_life_days','recent_firms']],equal_nan=True))
        independent=ww[ww.age_days.between(0,60)].groupby('target_id').firm.nunique().reindex(q.index,fill_value=0);countok.append(np.array_equal(independent,q.recent_firms))
        histories[(sc,k)]=timing.replace_aggregate(hh,expected.reset_index())
    recon=[];seatok=[];priorok=[];fitok=[];baselineok=[];selection=[];inputok=[]
    bp=pd.read_parquet(baseline/'predictions.parquet')
    for r in f.itertuples():
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id').reset_index(drop=True);z=np.load(Path(r.artifact)/r.forecast_path);poll=dict(np.load(Path(r.artifact)/r.poll_path));budget=np.load(source/f'fits/{r.scenario}_{r.cycle}_movement_K1.npz')['budget']
        original=wt['predictions'][wt['predictions'].scenario.eq(r.scenario)&wt['predictions'].cycle.eq(r.cycle)].sort_values('target_id')
        priorok.append(np.array_equal(q.target_id,original.target_id) and np.array_equal(q.prior,original.prior) and np.array_equal(q.actual,original.actual,equal_nan=True) and np.allclose(z['prior_covariance'],normal.split_covariance(budget[[v1.STATES.index(x) for x in q.geography]],r.N_variance)))
        expected,cov,_,_=normal.predict(q,budget,r.N_variance,poll);cols=['prediction_pp','p_dem','lo70_pp','hi95_pp']
        recon.append(np.allclose(q[cols],expected[cols],atol=1e-9) and np.allclose(cov,z['covariance'],atol=1e-9))
        ss=s[s.scenario.eq(r.scenario)&s.cycle.eq(r.cycle)&s.model.eq(r.model)].iloc[0]
        seatok.append(abs(ss.expected_D_exact-ss.fixed_D-q.p_dem.sum())<1e-9 and z['seat_count_frequency'].sum()==CONFIG['draws'] and ss.point_D==ss.fixed_D+q.prediction_pp.gt(0).sum())
        if r.model in BASELINES:
            old=bp[bp.scenario.eq(r.scenario)&bp.cycle.eq(r.cycle)&bp.model.eq(r.model)].sort_values('target_id');baselineok.append(np.allclose(q[cols+['q_pp','firm_mass']],old[cols+['q_pp','firm_mass']],equal_nan=True))
        else:
            raw=a[a.scenario.eq(r.scenario)&a.k.eq(r.k)].set_index('target_id').loc[q.target_id]
            inputok.append(np.allclose(q[['q_pp','firm_mass','half_life_days','recent_firms']],raw[['q_pp','firm_mass','half_life_days','recent_firms']],equal_nan=True))
            x,noise,w,years,_=v2.blocks(histories[(r.scenario,r.k)],r.cycle,'poll');fitok.append(all(np.array_equal(v,poll[key],equal_nan=True) for v,key in zip([x,noise,w,years],['training_values','training_noise','training_weights','years'])))
            bias=normal.fixed_common(x,noise,w,poll['budget'],0.,9.);fitok.append(np.allclose(bias['bias_mean'],poll['bias_mean']) and np.allclose(bias['bias_covariance'],poll['bias_covariance']))
    for r in t.drop_duplicates(['scenario','forecast_cycle']).itertuples():
        chosen,years,status=timing.choose(s[s.scenario.eq(r.scenario)],r.forecast_cycle,ORDER)
        qa=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq('adaptive_selected')].sort_values('target_id');qb=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq(chosen)].sort_values('target_id')
        selection.append(chosen==r.selected_model and ','.join(map(str,years))==r.validation_cycles and status==r.status and np.allclose(qa[['k','half_life_days','prediction_pp','p_dem']],qb[['k','half_life_days','prediction_pp','p_dem']]))
    c.update(forecast_inputs_match_aggregates=all(inputok),aggregate_reconstruction=all(aggok),independent_recent_counts=all(countok),fixed_baselines_preserved=all(baselineok),priors_targets_labels_preserved=all(priorok),forecasts_reconstructed=all(recon),past_calibration_arrays_and_bias_reconstructed=all(fitok),joint_seat_accounting=all(seatok),past_only_selector_reconstructed=all(selection))
    result=dict(passed=all(c.values()),checks=c,forecast_rows=len(p),calibration_fits=len(fd),older_notebooks=len(st['old_notebook_hashes']))
    v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError([key for key,value in c.items() if not value])
    v1.manifest(out);return result


def report(out,lab):
    out,lab=Path(out),Path(lab);p=pd.read_parquet(out/'predictions.parquet');s=pd.read_parquet(out/'seats.parquet');t=pd.read_parquet(out/'tuning.parquet');su=pd.read_parquet(out/'summary.parquet');ch=pd.read_parquet(out/'chamber_summary.parquet')
    text='# Adaptive poll decay: results\n\nGaussian no-U model and frozen September17 inputs. k3 is the illustrative rule; adaptive_selected tunes k using earlier-cycle chamber CRPS. Fixed baselines are unchanged.\n\n'
    cols=['scenario','model','n','correct','absolute_error_pp','wis_pp','brier','coverage70','coverage95']
    for period in ['recent_2016_2024','tuned_2018_2024','all_2012_2024']:
        text+='## '+period+'\n\n'+su[su.period.eq(period)&su.group.eq('all')][cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Recent chamber scores\n\n'+ch[ch.period.eq('recent_2016_2024')].round(4).to_markdown(index=False)+'\n\n'
    text+='## Chronological selection\n\n'+t.drop_duplicates(['scenario','forecast_cycle'])[['scenario','forecast_cycle','selected_model','validation_cycles','status']].to_markdown(index=False)+'\n\n'
    text+='## Current seats\n\n'+s[s.cycle.eq(2026)][['model','point_D','point_R','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95']].round(4).to_markdown(index=False)+'\n\n'
    current=p[p.cycle.eq(2026)&p.model.eq('adaptive_selected')]
    text+='## Current selected rule by state\n\n'+current[['geography','recent_firms','k','half_life_days','q_pp','firm_mass','prediction_pp','p_dem']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current state predictions\n\n'+p[p.cycle.eq(2026)].pivot(index='geography',columns='model',values='prediction_pp').round(3).to_markdown()+'\n\n'
    text+='## Limits\n\nFive recent cycles and substantial prior experimentation; small differences are exploratory. Distinct firms are a coverage proxy, not independent observations. Counts use known samples at each cutoff and field-end age; historical unknown publication dates retain the documented fallback. Age weights affect both averages and confidence. Gaussian calibration, candidate context and fixed seat completion assumptions remain. No explicit election-day drift, data refresh or model promotion.\n'
    (lab/'ADAPTIVE_POLL_DECAY_RESULTS.md').write_text(text);(out/'ADAPTIVE_POLL_DECAY_RESULTS.md').write_text(text)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(8,4));ns=np.arange(0,21)
    for k in KS:ax.plot(ns,half_life(ns,k),label=f'k={k}')
    ax.set(xlabel='Distinct firms with polls in preceding 60 days',ylabel='Half-life (days)',title='Adaptive decay rule');ax.legend();fig.tight_layout();fig.savefig(out/'adaptive_rule.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=ch[ch.period.eq('recent_2016_2024')&ch.scenario.eq(sc)].set_index('model');names=['gaussian30','gaussian90','adaptive1','adaptive3','adaptive6','adaptive_selected'];ax.barh(names,[q.loc[name,'seat_crps'] for name in names]);ax.set(title=sc,xlabel='Mean chamber CRPS (lower is better)')
    fig.tight_layout();fig.savefig(out/'chamber_comparison.png',dpi=145);plt.close(fig);v1.manifest(out)


if __name__=='__main__':build(Path(__file__).resolve().parents[1])
