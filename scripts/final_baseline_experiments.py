"""Bounded local/event/horizon uncertainty and adaptive-feature comparisons."""
from pathlib import Path
from datetime import datetime,timezone
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import simple_bayesian_polling as v1
import simple_national_model as normal
import student_polling_likelihood as student
import coverage_balance as scoring
import national_factor_review as national
import national_tails_waves as chamber
import local_electoral_uncertainty as local_t

FEATURE='20260920T013619.322700Z';ADAPTIVE='20260920T011823.097731Z'
CONFIG=dict(seed=197139,draws=30000,as_of='2026-09-17',validation_cycles=3,local_df=[5,3],variance_multipliers=[1,1.5,2],drift_sd30=[0,1,2],adaptive_k=3)
SELECTORS={'local':['base','local_g1.5','local_g2','local_t5','local_t3'],'event':['base','event1.5','event2'],'constant':['base','constant1.5','constant2'],'horizon':['base','drift_local1','drift_local2','drift_common1','drift_common2'],'timing':['base','adaptive3']}


def gaussian(test,mu,K,poll,extra=None):
    obs=np.flatnonzero(test.q_pp.notna());ids=np.array([v1.STATES.index(x) for x in test.geography]);so=ids[obs]
    R=poll['covariance'][np.ix_(so,so)]+poll['bias_covariance'][np.ix_(so,so)]+np.diag(16/test.firm_mass.to_numpy()[obs]);values=test.q_pp.to_numpy()[obs]-poll['bias_mean'][so]
    mean,cov,ll=v1.normal_update(mu,K,obs,values,R)
    if extra is not None:cov=cov+extra
    d=dict(mean=mean,covariance=cov,means=mean[None,:],covs=cov[None,:,:],weights=np.ones(1))
    p=student.summarize(test,d);p['median_pp']=mean;p['historical_bias_pp']=poll['bias_mean'][ids];p['corrected_poll_pp']=p.q_pp-p.historical_bias_pp
    return scoring.score_rows(p),d


def drift_covariance(days,sd30,kind):
    days=np.asarray(days,float)
    if not np.isfinite(days).all() or np.any(days<0) or sd30<0:raise ValueError('Nonnegative finite horizon required')
    if kind=='local':return np.diag(sd30**2*days/30)
    if kind=='common':return sd30**2*np.minimum.outer(days,days)/30
    raise ValueError('Unknown drift kind')


def select(cycle_scores,seats,scenario,year,family,selector):
    order=SELECTORS[selector];models=[family+'__'+x for x in order];metric='seat_crps' if selector=='timing' else 'wis_pp';q=seats if selector=='timing' else cycle_scores
    q=q[q.cycle.lt(year)&q.model.isin(models)]
    if selector!='horizon':q=q[q.scenario.eq(scenario)]
    years=sorted(q.cycle.unique())[-3:]
    if len(years)<3:return models[0],years,'early_base_fallback',{}
    q=q[q.cycle.isin(years)]
    expected=len(models)*3*(2 if selector=='horizon' else 1)
    if len(q)!=expected or q.duplicated(['scenario','cycle','model']).any():raise ValueError('Incomplete earlier validation grid')
    # Pool horizons with equal weight, then give each validation cycle equal weight.
    val=q.groupby(['cycle','model'])[metric].mean().groupby('model').mean().to_dict()
    if not np.isfinite(list(val.values())).all():raise ValueError('Missing scores')
    chosen=min(models,key=lambda name:(val[name],models.index(name)))
    return chosen,years,'last_three_past_cycles_'+metric,val


def build(lab):
    lab=Path(lab).resolve();src=lab/'reports/national_feature_prior'/FEATURE;adaptive=lab/'reports/adaptive_poll_decay'/ADAPTIVE
    fs=json.loads((src/'settings.json').read_text());working=Path(fs['source']);up=Path(fs['upstream'])
    out=lab/'reports/final_baseline_experiments'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for x in ['forecasts','recipe']:(out/x).mkdir(parents=True,exist_ok=True)
    st=dict(config=CONFIG,source=str(src),adaptive=str(adaptive),working=str(working),upstream=str(up),sources={str(x):v1.verify(x) for x in [src,adaptive,working,up]},old_notebook_hashes={x.name:v1.sha(x) for x in lab.glob('*.ipynb') if x.name!='FINAL_BASELINE_EXPERIMENTS.ipynb'},working_sha256=v1.sha(lab/'WORKING_MODEL.json'),promotion=False,data_refreshed=False)
    v1.json_write(out/'settings.json',st);print('OUTPUT',out,flush=True)
    orig=pd.read_parquet(src/'predictions.parquet');sf=pd.read_parquet(src/'folds.parquet');sf=sf[sf.model.isin(['none','both','approval'])]
    ap=pd.read_parquet(adaptive/'predictions.parquet');af=pd.read_parquet(adaptive/'folds.parquet');cal=pd.read_parquet(up/'calendars.parquet');roster=pd.read_parquet(up/'full_seat_ledger.parquet')
    cal[['scenario','cycle','extraordinary_event_any_4y']].to_parquet(out/'event_ledger.parquet',index=False)
    preds=[];seats=[];folds=[];checks=[];reproduced=[]
    for (sc,year),group in sf.groupby(['scenario','cycle']):
        pf=np.load(working/f'fits/{sc}_{year}_poll.npz');poll=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        ar=af[af.scenario.eq(sc)&af.cycle.eq(year)&af.model.eq('adaptive3')].iloc[0];adaptive_poll=dict(np.load(adaptive/ar.poll_path))
        at=ap[ap.scenario.eq(sc)&ap.cycle.eq(year)&ap.model.eq('adaptive3')].sort_values('target_id').reset_index(drop=True)
        event=float(cal[cal.scenario.eq(sc)&cal.cycle.eq(year)].extraordinary_event_any_4y.iloc[0])
        for r in group.itertuples():
            family=r.model;test=orig[orig.scenario.eq(sc)&orig.cycle.eq(year)&orig.model.eq(family)].sort_values('target_id').reset_index(drop=True)
            fit=np.load(src/r.fit_path);a=float(fit['a']);prior=np.load(src/r.forecast_path);mu=prior['prior_mean'];K=prior['prior_covariance'];g=float(K[0,1]);fv=g-a;local=np.diag(K)-g
            days=test.forecast_days_to_election.to_numpy(float)
            rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));z=rng.standard_normal((CONFIG['draws'],len(test)));un=rng.random(CONFIG['draws']);us=rng.random(z.shape)
            variants=['base','adaptive3'] if family=='approval' else list(dict.fromkeys(x for xs in SELECTORS.values() for x in xs))
            for variant in variants:
                q=test.copy();pp=poll;kk=K.copy();extra=None;islocal=variant.startswith('local_t');mult=1.;sd30=0.;kind='none'
                if variant.startswith('local_g'):mult=float(variant[7:]);kk=np.diag(local*mult)+g*np.ones_like(K)
                elif variant.startswith('event') or variant.startswith('constant'):
                    requested=float(variant[5:] if variant.startswith('event') else variant[8:]);mult=requested if variant.startswith('constant') or event==1 else 1.
                    kk=np.diag(local*mult)+(a*mult+fv)*np.ones_like(K)
                elif variant.startswith('drift_'):
                    kind='local' if 'local' in variant else 'common';sd30=float(variant[-1]);extra=drift_covariance(days,sd30,kind)
                elif variant=='adaptive3':
                    assert np.array_equal(q.target_id,at.target_id)
                    for col in ['q_pp','firm_mass','sample_count','firm_count','half_life_days','recent_firms']:q[col]=at[col].to_numpy()
                    pp=adaptive_poll
                if islocal:
                    df=int(variant[-1]);p,d=local_t.local_fit(q,mu,local,g,pp,df)
                    for label,nn,ns,bound in [('double_nodes',129,449,28.),('wider_scale',65,289,36.)]:
                        other,e=local_t.local_fit(q,mu,local,g,pp,df,national_nodes=nn,scale_nodes=ns,bound=bound,intervals=False)
                        checks.append(dict(scenario=sc,cycle=year,family=family,variant=variant,check=label,max_mean_pp=float(np.max(abs(d['mean']-e['mean']))),max_probability=float(np.max(abs(p.p_dem-other.p_dem))),relative_covariance=float(np.max(abs(d['covariance']-e['covariance']))/max(1,np.max(abs(d['covariance'])))),national_edge=d['national_edge_mass'],scale_edge=d['scale_edge_mass']))
                    draws=local_t.sample(d,z,un,us)
                else:
                    p,d=gaussian(q,mu,kk,pp,extra);draws=d['mean']+z@np.linalg.cholesky(d['covariance']).T
                p=p.drop(columns=[x for x in ['national_movement_pp','local_electoral_update_pp'] if x in p]);model=family+'__'+variant;p=p.assign(model=model,family=family,variant=variant,event_flag=event,feature_shifted_prior_pp=mu)
                preds.append(p);ss,counts=chamber.seat_summary(roster[roster.scenario.eq(sc)&roster.cycle.eq(year)],q,p,draws);freq=np.bincount(counts,minlength=101)
                seats.append(scoring.seat_scores(dict(ss,scenario=sc,cycle=year,model=model,family=family,variant=variant),freq))
                path=f'forecasts/{sc}_{year}_{model}.npz';np.savez_compressed(out/path,target_ids=q.target_id.to_numpy(str),mean=d['mean'],covariance=d['covariance'],prior_mean=mu,prior_covariance=kk,extra_covariance=np.zeros_like(K) if extra is None else extra,seat_count_frequency=freq)
                folds.append(dict(scenario=sc,cycle=year,model=model,family=family,variant=variant,event_flag=event,variance_multiplier=mult,drift_sd30=sd30,drift_kind=kind,source_forecast_path=r.forecast_path,source_fit_path=r.fit_path,forecast_path=path,adaptive_poll_path=ar.poll_path,feature_tau=r.tau,training_max_cycle=int(fit['years'].max())))
                if variant=='base':reproduced.append(np.allclose(p[['prediction_pp','p_dem','lo70_pp','hi95_pp']],test[['prediction_pp','p_dem','lo70_pp','hi95_pp']],atol=1e-8) and np.array_equal(freq,prior['seat_count_frequency']))
                if variant=='adaptive3' and family=='none':reproduced.append(np.allclose(p[['prediction_pp','p_dem']],at[['prediction_pp','p_dem']],atol=1e-8))
        print(sc,year,'local/event/horizon/combination complete',flush=True)
    p=pd.concat(preds,ignore_index=True);s=pd.DataFrame(seats);f=pd.DataFrame(folds);cs=cycle_metrics(p);selectedp=[];selecteds=[];selectedf=[];trace=[]
    for (sc,year,family),group in p.groupby(['scenario','cycle','family']):
        for selector in (['timing'] if family=='approval' else SELECTORS):
            chosen,years,status,values=select(cs,s,sc,year,family,selector);name=family+'__'+selector+'_selected'
            for table,dest in [(p,selectedp),(s,selecteds),(f,selectedf)]:dest.append(table[table.scenario.eq(sc)&table.cycle.eq(year)&table.model.eq(chosen)].assign(model=name,selected_model=chosen))
            for candidate in SELECTORS[selector]:
                model=family+'__'+candidate;trace.append(dict(scenario=sc,forecast_cycle=year,family=family,selector=selector,candidate=model,selected_model=chosen,validation_cycles=','.join(map(str,years)),status=status,score=values.get(model,np.nan),pooled_horizons=selector=='horizon'))
    p=pd.concat([p,*selectedp],ignore_index=True);s=pd.concat([s,*selecteds],ignore_index=True);f=pd.concat([f,*selectedf],ignore_index=True)
    for name,table in dict(predictions=p,seats=s,folds=f,cycle_scores=cycle_metrics(p),summary=scoring.summarize_scores(p),chamber_summary=national.chamber_summary(s),tuning=pd.DataFrame(trace),integration_checks=pd.DataFrame(checks)).items():table.to_parquet(out/f'{name}.parquet',index=False)
    v1.json_write(out/'reproduction.json',dict(passed=bool(all(reproduced)),comparisons=len(reproduced)))
    for path in (lab/'scripts').glob('*.py'):(out/'recipe'/path.name).write_bytes(path.read_bytes())
    (out/'FINAL_BASELINE_EXPERIMENTS.md').write_bytes((lab/'FINAL_BASELINE_EXPERIMENTS.md').read_bytes())
    v1.manifest(out);audit(out,lab);report(out,lab);v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)));print('COMPLETE',out,flush=True);return out


def cycle_metrics(p):
    return p[p.actual.notna()].groupby(['scenario','cycle','model'],as_index=False).agg(n=('actual','size'),correct=('correct','sum'),mae_pp=('absolute_error_pp','mean'),wis_pp=('wis_pp','mean'),brier=('brier','mean'),coverage70=('coverage70','mean'),coverage95=('coverage95','mean'))


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);st=json.loads((out/'settings.json').read_text());src=Path(st['source']);up=Path(st['upstream']);ad=Path(st['adaptive']);working=Path(st['working'])
    p=pd.read_parquet(out/'predictions.parquet');s=pd.read_parquet(out/'seats.parquet');f=pd.read_parquet(out/'folds.parquet');cs=pd.read_parquet(out/'cycle_scores.parquet');tr=pd.read_parquet(out/'tuning.parquet');integ=pd.read_parquet(out/'integration_checks.parquet');orig=pd.read_parquet(src/'predictions.parquet');cal=pd.read_parquet(up/'calendars.parquet');ap=pd.read_parquet(ad/'predictions.parquet')
    c=dict(sources_unchanged=all(v1.verify(x)==h for x,h in st['sources'].items()),old_notebooks_preserved=all(v1.sha(lab/x)==h for x,h in st['old_notebook_hashes'].items()),working_unchanged=v1.sha(lab/'WORKING_MODEL.json')==st['working_sha256'],baselines_reproduce=json.loads((out/'reproduction.json').read_text())['passed'],past_training=bool(f.training_max_cycle.lt(f.cycle).all()),current_unknown=bool(p[p.cycle.eq(2026)][['actual','wis_pp','brier']].isna().all().all() and s[s.cycle.eq(2026)][['actual_D','seat_crps']].isna().all().all()),unique_forecasts=not p.duplicated(['scenario','target_id','model']).any(),integration_converged=bool(integ.max_mean_pp.lt(.002).all() and integ.max_probability.lt(2e-5).all() and integ.relative_covariance.lt(2e-4).all()),integration_edges=bool(integ.national_edge.lt(1e-8).all() and integ.scale_edge.lt(1e-8).all()))
    preserved=[];recon=[];account=[];events=[];horizons=[];selection=[];variants=[];polls={};fixed=f[~f.model.str.endswith('_selected')]
    for r in fixed.itertuples():
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id').reset_index(drop=True);old=orig[orig.scenario.eq(r.scenario)&orig.cycle.eq(r.cycle)&orig.model.eq(r.family)].sort_values('target_id').reset_index(drop=True);z=np.load(out/r.forecast_path);g=np.load(src/r.source_forecast_path)
        preserved.append(np.array_equal(q.target_id,old.target_id) and np.array_equal(q.actual,old.actual,equal_nan=True) and np.array_equal(q.prior,old.prior) and np.array_equal(z['prior_mean'],g['prior_mean']))
        key=(r.scenario,r.cycle,r.variant=='adaptive3')
        if key not in polls:
            if key[-1]:polls[key]=dict(np.load(ad/r.adaptive_poll_path))
            else:
                pf=np.load(working/f'fits/{r.scenario}_{r.cycle}_poll.npz');polls[key]=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        if r.variant=='adaptive3':raw=ap[ap.scenario.eq(r.scenario)&ap.cycle.eq(r.cycle)&ap.model.eq('adaptive3')].sort_values('target_id')
        else:raw=old
        preserved.append(np.array_equal(q.q_pp,raw.q_pp,equal_nan=True) and np.array_equal(q.firm_mass,raw.firm_mass))
        if not r.variant.startswith('local_t'):
            expected,d=gaussian(q,z['prior_mean'],z['prior_covariance'],polls[key],z['extra_covariance']);recon.append(np.allclose(expected[['prediction_pp','p_dem','lo70_pp','hi95_pp']],q[['prediction_pp','p_dem','lo70_pp','hi95_pp']],atol=1e-9))
        else:
            local=np.diag(g['prior_covariance'])-g['prior_covariance'][0,1];expected,d=local_t.local_fit(q,g['prior_mean'],local,float(g['prior_covariance'][0,1]),polls[key],int(r.variant[-1]),intervals=False)
            recon.append(np.allclose(expected.prediction_pp,q.prediction_pp,atol=1e-9) and np.allclose(expected.p_dem,q.p_dem,atol=1e-9) and np.allclose(d['covariance'],z['covariance']))
        baseK=g['prior_covariance'];common=float(baseK[0,1]);local=np.diag(baseK)-common;fit=np.load(src/r.source_fit_path);a=float(fit['a']);fv=common-a
        want=baseK
        if r.variant.startswith('local_g'):want=np.diag(local*float(r.variant[7:]))+common*np.ones_like(baseK)
        elif r.variant.startswith('event') or r.variant.startswith('constant'):
            m=float(r.variant[5:] if r.variant.startswith('event') else r.variant[8:])
            if r.variant.startswith('event') and r.event_flag!=1:m=1.
            want=np.diag(local*m)+(a*m+fv)*np.ones_like(baseK)
        variants.append(np.allclose(z['prior_covariance'],want,atol=1e-10))
        flag=float(cal[cal.scenario.eq(r.scenario)&cal.cycle.eq(r.cycle)].extraordinary_event_any_4y.iloc[0]);events.append((pd.isna(flag) and pd.isna(r.event_flag)) or flag==r.event_flag)
        if r.variant.startswith('event') and flag!=1:events.append(np.array_equal(z['prior_covariance'],g['prior_covariance']))
        if r.variant.startswith('drift_'):
            horizons.append(np.allclose(z['extra_covariance'],drift_covariance(q.forecast_days_to_election,r.drift_sd30,r.drift_kind)) and np.allclose(q.prediction_pp,old.prediction_pp,atol=1e-9))
        ss=s[s.scenario.eq(r.scenario)&s.cycle.eq(r.cycle)&s.model.eq(r.model)].iloc[0];account.append(z['seat_count_frequency'].sum()==CONFIG['draws'] and abs(ss.expected_D_exact-ss.fixed_D-q.p_dem.sum())<1e-9 and ss.point_D==ss.fixed_D+q.prediction_pp.gt(0).sum())
    for r in tr.drop_duplicates(['scenario','forecast_cycle','family','selector']).itertuples():
        chosen,years,status,_=select(cs,s,r.scenario,r.forecast_cycle,r.family,r.selector);q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq(r.family+'__'+r.selector+'_selected')].sort_values('target_id');other=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq(chosen)].sort_values('target_id')
        selection.append(chosen==r.selected_model and ','.join(map(str,years))==r.validation_cycles and status==r.status and np.allclose(q.prediction_pp,other.prediction_pp) and np.allclose(q.lo70_pp,other.lo70_pp))
    nb=pd.read_parquet(up/'nonbayesian_predictions.parquet');base=p[p.model.eq('none__base')][['scenario','cycle','target_id','actual']];matched=nb[nb.model.isin(['bias','polling'])].merge(base,on=['scenario','cycle','target_id'],suffixes=('','_checked'),validate='many_to_one')
    c.update(nonbayesian_same_targets_and_labels=bool(len(matched)==2*len(base) and np.allclose(matched.actual,matched.actual_checked,equal_nan=True)),prior_variance_variants_reconstructed=all(variants),inputs_labels_feature_means_preserved=all(preserved),predictions_reconstructed=all(recon),event_flags_and_inactive_control=all(events),horizon_changes_only_uncertainty=all(horizons),seat_accounting=all(account),past_only_selection_reconstructed=all(selection))
    result=dict(passed=all(c.values()),checks=c,rows=len(p),fixed_forecasts=len(fixed),integration_comparisons=len(integ));v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError([k for k,v in c.items() if not v])
    v1.manifest(out);return result


def report(out,lab):
    out,lab=Path(out),Path(lab);st=json.loads((out/'settings.json').read_text());up=Path(st['upstream']);p=pd.read_parquet(out/'predictions.parquet');s=pd.read_parquet(out/'seats.parquet');su=pd.read_parquet(out/'summary.parquet');ch=pd.read_parquet(out/'chamber_summary.parquet');cs=pd.read_parquet(out/'cycle_scores.parquet')
    # Existing non-Bayesian point forecasts, exact target/label join.
    nb=pd.read_parquet(up/'nonbayesian_predictions.parquet');baseline=p[p.model.eq('none__base')][['scenario','cycle','target_id','actual','history_selection_10pp']]
    nb=nb[nb.model.isin(['polling','bias'])].merge(baseline,on=['scenario','cycle','target_id'],suffixes=('','_checked'),validate='many_to_one')
    assert len(nb)==2*len(baseline) and np.allclose(nb.actual,nb.actual_checked,equal_nan=True)
    nb['prediction_pp']=100*nb.prediction;nb['mae_pp']=(nb.prediction_pp-100*nb.actual).abs();nb['correct']=np.where(nb.actual.notna(),nb.prediction.gt(0)==nb.actual.gt(0),np.nan)
    nb.to_parquet(out/'nonbayesian_matched.parquet',index=False)
    rows=[]
    for name,table in [('Bayesian',p),('Non-Bayesian',nb)]:
        for (sc,year,model),q in table.groupby(['scenario','cycle','model']):
            seat=s[s.scenario.eq(sc)&s.cycle.eq(year)&s.model.eq('none__base')].iloc[0];point=int(seat.fixed_D+q.prediction_pp.gt(0).sum())
            rows.append(dict(kind=name,scenario=sc,cycle=year,model=model,n=len(q),correct=q.correct.sum() if q.actual.notna().any() else np.nan,mae_pp=float((q.prediction_pp-100*q.actual).abs().mean()),point_D=point,actual_D=seat.actual_D,point_seat_error=abs(point-seat.actual_D) if pd.notna(seat.actual_D) else np.nan))
    comparison=pd.DataFrame(rows);comparison.to_parquet(out/'point_comparison.parquet',index=False)
    pointrows=[]
    for (sc,model),q in comparison[comparison.cycle.between(2016,2024)].groupby(['scenario','model']):
        pointrows.append(dict(scenario=sc,model=model,cycles=len(q),n=int(q.n.sum()),correct=int(q.correct.sum()),cycle_mean_MAE_pp=q.mae_pp.mean(),pooled_state_MAE_pp=float(np.average(q.mae_pp,weights=q.n)),point_seat_MAE=q.point_seat_error.mean()))
    points=pd.DataFrame(pointrows);points.to_parquet(out/'point_summary.parquet',index=False)
    text='# Final bounded experiments: results\n\nLocal/event/horizon calibration selected by earlier-cycle state WIS; adaptive combination by earlier-cycle chamber CRPS. Horizon selector pools horizons. Frozen September17 data; no new holdout. Event flags are on for all recent cycles, so event specificity cannot be inferred from recent performance alone.\n\n'
    keep=lambda names:names.eq('none__base')|names.eq('both__base')|names.eq('approval__base')|names.str.endswith('_selected')|names.str.endswith('__adaptive3')
    for title,tab in [('Recent state metrics',su[su.period.eq('recent_2016_2024')&su.group.eq('all')&keep(su.model)][['scenario','model','n','correct','absolute_error_pp','wis_pp','brier','coverage70','coverage95']]),('Recent chamber metrics',ch[ch.period.eq('recent_2016_2024')&keep(ch.model)]),('Current seats',s[s.cycle.eq(2026)&keep(s.model)][['model','point_D','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95']])]:text+='## '+title+'\n\n'+tab.round(4).to_markdown(index=False)+'\n\n'
    (lab/'FINAL_BASELINE_EXPERIMENTS_RESULTS.md').write_text(text);(out/'FINAL_BASELINE_EXPERIMENTS_RESULTS.md').write_text(text)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    models=['both__base','both__local_selected','both__event_selected','both__horizon_selected','both__adaptive3']
    fig,axes=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    for ax,sc in zip(axes,['matched_live','oct31']):
        for model in models:
            q=cs[cs.scenario.eq(sc)&cs.model.eq(model)&cs.cycle.ge(2016)];ax.plot(q.cycle,q.coverage70,marker='o',label=model.replace('both__',''))
        ax.axhline(.7,color='black',ls='--');ax.set_ylim(0,1.05);ax.set_title('September' if sc=='matched_live' else 'October31');ax.set_ylabel('Observed 70% coverage');ax.set_xticks([2016,2018,2020,2022,2024])
    handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside lower center',ncol=5,fontsize=8);fig.savefig(out/'coverage_comparison.png',dpi=150);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=ch[ch.period.eq('recent_2016_2024')&ch.scenario.eq(sc)&ch.model.isin(models)].set_index('model').reindex(models);ax.bar(np.arange(len(q)),q.seat_crps);ax.set_xticks(np.arange(len(q)),[x.replace('both__','').replace('_selected','') for x in models],rotation=15);ax.set_title('September' if sc=='matched_live' else 'October31');ax.set_ylabel('Chamber CRPS (lower is better)')
    fig.savefig(out/'chamber_comparison.png',dpi=150);plt.close(fig)


def load(lab):
    root=Path(lab)/'reports/final_baseline_experiments';ptr=json.loads((root/'latest.json').read_text());out=root/ptr['artifact'];assert v1.verify(out)==ptr['manifest_sha256'];return out,{p.stem:pd.read_parquet(p) for p in out.glob('*.parquet')}

if __name__=='__main__':build(Path(__file__).resolve().parents[1])
