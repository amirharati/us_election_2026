"""Calibration, sensitivity and reconstruction checks for the prior study."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import prior_sensitivity as m
import simple_bayesian_polling as v1

FOCUS=['control_fixed','control_shared','control_state','history4_state','history16_state','type_equal_state','shrink1_state','shrink4_state','joint_shared','joint_state']


def load(out):
    out=Path(out);v1.verify(out);return {p.stem:pd.read_parquet(p) for p in out.glob('*.parquet')}


def calibration(f):
    rows=[]
    for stage,key in [('prior','prior_predictions'),('posterior','predictions')]:
        p=f[key];p=p[p.actual.notna()]
        for period,first in [('recent_2016_2024',2016),('all_2012_2024',2012)]:
            for (sc,model),g in p[p.cycle.between(first,2024)].groupby(['scenario','model']):
                groups={'all':np.ones(len(g),bool),'competitive':g.history_selection_10pp.eq('competitive'),'noncompetitive':g.history_selection_10pp.eq('not_selected'),
                        'unknown_history_screen':g.history_selection_10pp.eq('unknown_history'),'polled':g.q_pp.notna(),'no_polls':g.q_pp.isna(),
                        'at_most_two_prior_outcomes':g.prior_history_n.le(2),'last_outcome_at_least_six_years_old':(g.cycle-g.prior_source_max_cycle).ge(6)}
                for group,mask in groups.items():
                    q=g[mask];e=100*q.actual-q.prediction_pp;sd=q.posterior_sd_pp;z=e/sd
                    rec=dict(stage=stage,period=period,scenario=sc,model=model,group=group,n=len(q),cycles=q.cycle.nunique(),
                             correct=int(((q.prediction_pp>0)==(q.actual>0)).sum()),mae_pp=float(e.abs().groupby(q.cycle).mean().mean()),
                             signed_error_pp=float(e.groupby(q.cycle).mean().mean()),mean_z=float(z.mean()),rms_z=float(np.sqrt((z*z).mean())),
                             brier=float(((q.p_dem-(q.actual>0))**2).mean()),marginal_nll=float((-q.log_predictive_density).groupby(q.cycle).mean().mean()),
                             mean_sd_pp=float(sd.mean()),mean95_width_pp=float((q.hi95_pp-q.lo95_pp).mean()))
                    for level in [50,70,80,95]:rec['coverage'+str(level)]=float(((100*q.actual>=q[f'lo{level}_pp'])&(100*q.actual<=q[f'hi{level}_pp'])).mean())
                    rows.append(rec)
    return pd.DataFrame(rows)


def cycle_scores(f):
    rows=[]
    for stage,key in [('prior','prior_predictions'),('posterior','predictions')]:
        for (sc,y,model),g in f[key][f[key].actual.notna()].groupby(['scenario','cycle','model']):
            e=100*g.actual-g.prediction_pp
            rows.append(dict(stage=stage,scenario=sc,cycle=y,model=model,n=len(g),correct=int(((g.prediction_pp>0)==(g.actual>0)).sum()),mae_pp=float(e.abs().mean()),signed_error_pp=float(e.mean()),
                             coverage70=float(((100*g.actual>=g.lo70_pp)&(100*g.actual<=g.hi70_pp)).mean()),coverage95=float(((100*g.actual>=g.lo95_pp)&(100*g.actual<=g.hi95_pp)).mean()),
                             marginal_nll=float((-g.log_predictive_density).mean())))
    return pd.DataFrame(rows)


def state_errors(f):
    rows=[]
    for stage,key in [('prior','prior_predictions'),('posterior','predictions')]:
        for (sc,model,state),g in f[key].query('2016<=cycle<=2024').groupby(['scenario','model','geography']):
            e=100*g.actual-g.prediction_pp;z=e/g.posterior_sd_pp
            rows.append(dict(stage=stage,scenario=sc,model=model,state=state,n=len(g),mae_pp=float(e.abs().mean()),signed_error_pp=float(e.mean()),
                             mean_z=float(z.mean()),rms_z=float(np.sqrt((z*z).mean())),mean_sd_pp=float(g.posterior_sd_pp.mean()),
                             coverage95=float(((100*g.actual>=g.lo95_pp)&(100*g.actual<=g.hi95_pp)).mean())))
    return pd.DataFrame(rows)


def audit(out,lab):
    out,lab=Path(out),Path(lab);f=load(out);settings=json.loads((out/'settings.json').read_text());source=Path(settings['source']);c={}
    c['original_artifact_unchanged']=v1.verify(source)==settings['source_sha256']
    c['earlier_notebooks_unchanged']=all(v1.sha(lab/n)==h for n,h in settings['old_notebook_hashes'].items())
    pd.testing.assert_frame_equal(f['prepared_histories'],pd.read_parquet(source/'prepared_histories.parquet'));c['all_history_data_and_means_unchanged']=True
    old=pd.read_parquet(source/'predictions.parquet');p=f['predictions'];q=f['prior_predictions'];cols=['prediction_pp','posterior_sd_pp','p_dem','lo95_pp','hi95_pp']
    controls=[]
    for a,b in [('control_fixed','decay_fixed'),('control_shared','decay_shared'),('control_state','decay_state')]:
        x=p[p.model.eq(a)].merge(old[old.model.eq(b)],on=['scenario','target_id'],suffixes=('_new','_old'),validate='one_to_one')
        controls.append(all(np.allclose(x[k+'_new'],x[k+'_old'],atol=1e-10) for k in cols))
    c['fixed_shared_state_controls_reproduce']=all(controls)
    c['one_forecast_per_model_target']=not p.duplicated(['scenario','model','target_id']).any()
    c['identical_comparison_cases']=all(g.groupby('model').target_id.apply(frozenset).nunique()==1 for _,g in p.groupby(['scenario','cycle']))
    c['future_labels_blank']=bool(p[p.cycle.eq(2026)].actual.isna().all())
    c['finite_predictions_and_valid_probabilities']=bool(np.isfinite(p[cols]).all().all() and p.p_dem.between(0,1).all())
    fits=f['fit_diagnostics'];c['component_training_past_only']=bool(fits.training_max_cycle.lt(fits.cycle).all())
    c['all_em_converged']=bool(fits.converged.all());c['objectives_monotone']=bool(fits.min_objective_increment.ge(-1e-5).all());c['positive_process_covariances']=bool(fits.min_eigenvalue.gt(0).all())
    blocks=[];reused=[]
    for r in fits.itertuples():
        h=f['prepared_histories'];sc=r.scenario if r.scenario!='all' else 'matched_live';h=h[h.prior_recipe.eq(r.recipe)&h.scenario.eq(sc)]
        values,noise,w,years,_=m.training_blocks(h,r.cycle,r.component,r.history_half_life,r.other_type_weight)
        z=np.load(out/r.path);blocks.append(all(np.array_equal(z[n],a,equal_nan=True) for n,a in [('training_values',values),('training_noise',noise),('training_weights',w),('years',years)]))
        if r.reused:
            oldz=np.load(r.source_path);reused.append(all(np.array_equal(z[n],oldz[n],equal_nan=True) for n in ['covariance','bias_mean','bias_covariance','objective']))
    c['training_weights_and_masks_reconstructed']=all(blocks);c['reused_components_unchanged']=all(reused)
    pollfits=fits[fits.component.eq('poll')]
    c['polling_history_specification_fixed']=bool(pollfits.profile.eq('poll_fixed').all() and pollfits.history_half_life.eq(8).all() and pollfits.other_type_weight.eq(.5).all())
    for name in ['covariance_tuning','strength_tuning','local_tuning','joint_tuning']:
        t=f[name];c[name+'_chronological']=bool((t.fit_max_cycle.lt(t.validation_cycle)&t.validation_cycle.lt(t.forecast_cycle)).all())
    t=f['mean_tuning'];c['mean_tuning_chronological']=bool((t.max_prior_source_cycle.lt(t.validation_cycle)&t.validation_cycle.lt(t.forecast_cycle)).all())
    profiles=f['state_penalties'];profileok=[]
    for (model,sc,y),g in profiles.groupby(['model','scenario','cycle']):
        t=f['local_tuning'];t=t[t.profile.eq(g.profile.iloc[0])&t.joint.eq(g.joint.iloc[0])&t.scenario.eq(sc)&t.forecast_cycle.eq(y)]
        a,_=m.shrink(t,float(g.shared_multiplier.iloc[0]),int(y),float(g.shrinkage_mass.iloc[0]))
        profileok.append(np.allclose(a,g.set_index('state').loc[m.v2.STATES].variance_multiplier))
    c['state_shrinkage_reconstructed']=all(profileok)
    joint_nested=[]
    for (sc,vy),g in f['local_tuning'].query('joint==True').groupby(['scenario','validation_cycle']):
        jt=f['joint_tuning'];jt=jt[jt.scenario.eq(sc)&jt.forecast_cycle.eq(vy)]
        if jt.validation_cycle.nunique()<3:expected='decay8'
        else:
            scores=jt.groupby(['recipe','variance_multiplier']).score.mean()
            expected=min(scores.index,key=lambda x:(scores.loc[x],{'decay8':0,'decay16':1,'decay4':2}[x[0]],abs(np.log2(x[1])),x[1]))[0]
        joint_nested.append(g.validation_recipe.eq(expected).all())
    c['joint_local_validation_reselects_mean_using_earlier_cycles']=all(joint_nested)
    jointok=[];strengthok=[];forecastok=[];priorok=[];seatok=[];pollsame=[];jointnested=[];covchoices=[]
    ref_folds=pd.read_parquet(source/'folds.parquet').query('family=="decay"').set_index(['scenario','cycle'])
    for r in f['folds'].itertuples():
        t=f['covariance_tuning'];t=t[t.profile.eq(r.profile)&t.recipe.eq(r.recipe)&t.scenario.eq(r.scenario)&t.forecast_cycle.eq(r.cycle)&t.component.eq('movement')]
        scores=t.groupby('kappa').score.mean();k=float(min(scores.index,key=lambda k:(scores.loc[k],-k))) if len(scores) else 8.
        covchoices.append(fits.set_index('path').loc[r.movement_path].kappa==k)
        if r.joint:
            t=f['joint_tuning'];t=t[t.scenario.eq(r.scenario)&t.forecast_cycle.eq(r.cycle)]
            scores=t.groupby(['recipe','variance_multiplier']).score.mean()
            choice=min(scores.index,key=lambda x:(scores.loc[x],{'decay8':0,'decay16':1,'decay4':2}[x[0]],abs(np.log2(x[1])),x[1]))
            jointok.append(choice==(r.recipe,r.shared_multiplier))
        else:
            t=f['strength_tuning'];t=t[t.profile.eq(r.profile)&t.scenario.eq(r.scenario)&t.forecast_cycle.eq(r.cycle)]
            choice,status=m.v3.select_multiplier(t.to_dict('records'));strengthok.append(choice==r.shared_multiplier and status==r.status)
        test=p[p.model.eq(r.model)&p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)].sort_values('target_id').reset_index(drop=True)
        z=np.load(out/r.movement_path);mov={n:z[n] for n in z.files};z=np.load(out/r.poll_path);poll={n:z[n] for n in z.files};draw=np.load(out/r.forecast_path)
        pred,cov,meta=m.v4.state_predict(test,mov,poll,draw['multipliers']);np.linalg.cholesky(cov)
        forecastok.append(all(np.allclose(pred[k],test[k],atol=1e-10) for k in cols) and np.allclose(cov,draw['posterior_covariance']))
        saved=q[q.model.eq(r.model)&q.scenario.eq(r.scenario)&q.cycle.eq(r.cycle)].sort_values('target_id').reset_index(drop=True)
        exp=m.prior_prediction(test,meta['prior_covariance'],r.model,'test')
        priorok.append(all(np.allclose(exp[k],saved[k],atol=1e-10) for k in cols+['lo70_pp','hi70_pp']) and np.allclose(meta['prior_covariance'],draw['prior_covariance']))
        ref=np.load(source/ref_folds.loc[(r.scenario,r.cycle),'poll_path']);pollsame.append(all(np.array_equal(poll[k],ref[k],equal_nan=True) for k in ['covariance','bias_mean','bias_covariance']))
        seat=f['seats'];seat=seat[seat.model.eq(r.model)&seat.scenario.eq(r.scenario)&seat.cycle.eq(r.cycle)].iloc[0]
        freq=draw['seat_count_frequency'];seatok.append(freq.sum()==m.CONFIG['draws'] and abs(seat.expected_D_exact-(seat.fixed_D+test.p_dem.sum()))<1e-12)
    c['covariance_hyperparameters_reconstructed']=all(covchoices);c['shared_strength_reconstructed']=all(strengthok);c['joint_mean_strength_reconstructed']=all(jointok)
    c['all_posterior_forecasts_reconstructed']=all(forecastok);c['all_prior_forecasts_reconstructed']=all(priorok)
    c['same_poll_bias_covariance_for_every_variant']=all(pollsame);c['seat_probability_accounting']=all(seatok)
    sim=f['simulation_checks'];c['positive_forecast_covariances']=bool(sim.min_eigenvalue.gt(0).all());c['joint_draw_means_within_6se']=bool(sim.max_mc_mean_z.lt(6).all())
    # Changing uncertainty hyperparameters must not change staged prior centers.
    center=q[~q.model.str.startswith('joint')].groupby(['scenario','target_id']).prediction_pp.agg(['min','max'])
    c['sensitivity_prior_means_identical']=bool((center['max']-center['min']).abs().lt(1e-10).all())
    result=dict(passed=all(c.values()),checks=c,models=p.model.nunique(),forecasts=len(p),new_fits=int((~fits.reused).sum()),reused_fits=int(fits.reused.sum()),maximum_iterations=int(fits.iterations.max()),
                maximum_posterior_outside_margin_mass=float(p.outside_margin_bounds_probability.max()),maximum_prior_outside_margin_mass=float(q.outside_margin_bounds_probability.max()))
    v1.json_write(out/'completion_audit.json',result)
    if not result['passed']:raise ValueError([k for k,v in c.items() if not v])
    return result


def report(out,lab):
    out,lab=Path(out),Path(lab);f=load(out);cal=calibration(f);cycles=cycle_scores(f);states=state_errors(f)
    for name,t in [('calibration',cal),('cycle_scores',cycles),('state_errors',states)]:t.to_parquet(out/(name+'.parquet'),index=False)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axs=plt.subplots(1,2,figsize=(13,5))
    for ax,sc in zip(axs,['matched_live','oct31']):
        g=cal[cal.period.eq('recent_2016_2024')&cal.group.eq('all')&cal.scenario.eq(sc)&cal.model.eq('control_state')]
        for stage,row in g.set_index('stage').iterrows():ax.plot([50,70,80,95],[100*row['coverage'+str(n)] for n in [50,70,80,95]],marker='o',label=stage)
        ax.plot([50,95],[50,95],'k--',label='nominal');ax.set(xlabel='Nominal interval (%)',ylabel='Observed coverage (%)',title=sc,ylim=(35,101));ax.legend()
    fig.tight_layout();fig.savefig(out/'prior_posterior_coverage.png',dpi=145);plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(14,5));order=FOCUS
    for ax,sc in zip(axs,['matched_live','oct31']):
        q=cal[cal.stage.eq('posterior')&cal.period.eq('recent_2016_2024')&cal.group.eq('all')&cal.scenario.eq(sc)].set_index('model').reindex(order)
        ax.barh(np.arange(len(q)),q.mae_pp,color='#357d99');ax.set_yticks(np.arange(len(q)),q.index);ax.invert_yaxis();ax.set(title=sc,xlabel='Posterior margin MAE (pp)')
    fig.tight_layout();fig.savefig(out/'sensitivity_mae.png',dpi=145);plt.close(fig)
    p=f['predictions'];current=p[p.cycle.eq(2026)];base=current[current.model.eq('control_state')].set_index('target_id');table=base[['geography','q_pp','prior','actual']].copy();table['prior_pp']=100*table.pop('prior')
    for name in [n for n in FOCUS if n.endswith('state')]:table[name+'_pp']=current[current.model.eq(name)].set_index('target_id').prediction_pp
    table=table.reset_index().sort_values('geography');table.to_parquet(out/'current_states.parquet',index=False)
    text='# Prior calibration and sensitivity — results\n\nFrozen September17,2026 polling/features, repaired official historical admissions. All variants use identical targets. The control reproduces the previous repaired-data Bayesian decay/state model. No likelihood/feature/data changes or automatic promotion. Positive signed error means actual results were more Democratic than the prediction. MAE averages cycles equally; coverage/correct calls pool contests.\n\n'
    text+='## Prior versus posterior calibration\n\n'+cal.query('period=="recent_2016_2024" and group=="all" and model in ["control_fixed","control_shared","control_state"]')[['stage','scenario','model','n','mae_pp','signed_error_pp','coverage70','coverage95','mean95_width_pp','rms_z','marginal_nll']].round(4).to_markdown(index=False)+'\n\n'
    text+='## One-at-a-time sensitivity and joint tuning\n\nHistory4/16 change movement-covariance history half-life only; type_equal gives other election types full weight. Shared/state strengths and covariance regularization are retuned chronologically for these changes. Shrink1/4 change local pooling mass only, keeping the base covariance and shared/raw state preferences fixed. Joint_shared/state choose mean half-life and shared strength together on historical final predictive density, keeping the original4/8/16 mean grid. Polling components are identical for every variant.\n\n'
    for period in ['recent_2016_2024','all_2012_2024']:
        for group in ['all','competitive','noncompetitive','no_polls','polled']:
            q=cal[cal.period.eq(period)&cal.group.eq(group)&cal.stage.eq('posterior')&cal.model.isin(FOCUS)]
            text+=f'## Posterior: {period}, {group}\n\n'+q[['scenario','model','n','correct','mae_pp','brier','coverage70','coverage95','marginal_nll']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Prior sparse/stale/no-poll groups\n\nEmpty groups have N0 and missing metrics, not invented evidence.\n\n'+cal[cal.period.eq('recent_2016_2024')&cal.stage.eq('prior')&cal.model.eq('control_state')][['scenario','group','n','mae_pp','signed_error_pp','coverage70','coverage95','rms_z']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Prior state errors\n\nFew held-out outcomes per state; these are descriptive, not well-estimated state calibration rates.\n\n'+states.query('stage=="prior" and scenario=="matched_live" and model=="control_state"').sort_values('mae_pp',ascending=False).round(3).to_markdown(index=False)+'\n\n'
    text+='## Cycle comparisons\n\n'+cycles[cycles.model.isin(FOCUS)&cycles.stage.eq('posterior')].round(3).to_markdown(index=False)+'\n\n'
    text+='## Current choices\n\n'+f['folds'].query('cycle==2026')[['model','recipe','shared_multiplier','shrinkage_mass']].round(3).to_markdown(index=False)+'\n\n'
    text+='## Current state margins\n\n'+table.round(3).to_markdown(index=False)+'\n\n'
    text+='## Full Senate scenarios\n\nD includes mapped Democratic-caucusing independents and existing incumbent-caucus completions for unmodeled contested seats. Current35contests are modeled conditionally on the existing scalar ballot/rule assumptions. These are not a newly certified election forecast.\n\n'+f['seats'][f['seats'].model.isin(FOCUS)][['scenario','cycle','model','point_D','point_R','actual_D','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95','unmodeled_contested']].round(3).to_markdown(index=False)+'\n\n'
    text+='## Limits\n\nPrior and posterior coverage are different diagnostics. Overcoverage before polling and undercoverage afterward do not by themselves isolate which likelihood/covariance/model assumptions are responsible. No new state-specific hyperparameters are added; fixed state validation decay/window and covariance/selection uncertainty remain. The optimizer cap is increased to16000 for slower new covariance fits, preserving the1e−6 convergence tolerance and the same objective. Joint tuning tests15combinations on the same few earlier validation cycles and may be unstable; it is not untouched evidence for a winner. Older models/artifacts remain intact.\n'
    (lab/'PRIOR_CALIBRATION_SENSITIVITY_RESULTS.md').write_text(text);(out/'PRIOR_CALIBRATION_SENSITIVITY_RESULTS.md').write_text(text)
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes());v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return f,cal
