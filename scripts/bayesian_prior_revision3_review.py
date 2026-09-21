"""Tables, plots and reproducibility checks for the prior-construction experiment."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import bayesian_prior_revision3 as model
import simple_bayesian_polling as v1


def load(out):
    v1.verify(out)
    return {p.stem:pd.read_parquet(p) for p in Path(out).glob('*.parquet')}


def performance(f,group='all',period='recent_2016_2024'):
    q=f['metrics'].query('group==@group and period==@period').copy()
    q['Model']=q.model.map(model.LABELS);q['Correct']=q.correct.astype(str)+'/'+q.n.astype(str)
    q['Coverage95_pct']=100*q.coverage95
    q=q[['scenario','Model','Correct','mae_pp','brier','Coverage95_pct','mean95_width_pp']]
    return q.round(3)


def prior_scores(f,period='recent'):
    h=f['prior_predictions'];h=h[h.actual.notna()&h.cycle.ge(2016 if period=='recent' else 2012)]
    rows=[]
    for (s,family),g in h.groupby(['scenario','family']):
        e=g.prior_error_pp
        state_means=e.groupby(g.geography).mean()
        rows.append(dict(Horizon=s,Prior=family,Contests=len(g),Correct=int(((g.prior>0)==(g.actual>0)).sum()),
                         MAE_pp=float(e.abs().groupby(g.cycle).mean().mean()),
                         Mean_error_actual_minus_prior_pp=float(e.groupby(g.cycle).mean().mean()),
                         Mean_abs_state_error_pp=float(state_means.abs().mean()),Fallbacks=int(g.prior_fallback.sum())))
    return pd.DataFrame(rows).round(3)


def cycles(f):
    rows=[]
    for (s,y,m),g in f['predictions'].query('cycle<2026').groupby(['scenario','cycle','model']):
        rows.append(dict(Horizon=s,Cycle=y,Model=model.LABELS[m],N=len(g),Correct=int(((g.prediction_pp>0)==(g.actual>0)).sum()),
                         MAE_pp=float(abs(g.prediction_pp-100*g.actual).mean()),
                         Marginal_NLPD=float(-g.log_predictive_density.mean()) if g.log_predictive_density.notna().all() else np.nan))
    return pd.DataFrame(rows).round(3)


def states(f,year=2026,scenario='matched_live'):
    q=f['predictions'].query('cycle==@year and scenario==@scenario');base=q[q.model.eq('v3_decay_tuned')].set_index('target_id')
    result=pd.DataFrame(dict(State=base.geography+np.where(base.special,' special',''),Actual_pp=100*base.actual,
                             Old_prior_pp=100*base.source_prior,New_prior_pp=100*base.prior,Raw_poll_pp=base.q_pp,
                             Decay_tuned_pp=base.prediction_pp,D_probability=base.p_dem,Low95_pp=base.lo95_pp,High95_pp=base.hi95_pp))
    for key in ['v2_linked','nonbayes_bias','v3_current_tuned','v3_latest_fixed','v3_latest_tuned','v3_decay_fixed']:
        result[key+'_pp']=q[q.model.eq(key)].set_index('target_id').prediction_pp
    return result.reset_index().sort_values('State').round(3)


def seats(f,out):
    settings=json.loads((Path(out)/'settings.json').read_text());source=Path(settings['source'])
    old=pd.read_parquet(source/'seat_comparison.parquet')
    old=old[old.Model.isin([model.LABELS[k] for k in ['v2_linked','v1_linked','nonbayes_bias','nonbayes_momentum','raw30']])]
    q=f['seats'];t=pd.DataFrame(dict(Horizon=q.scenario,Cycle=q.cycle,Model=q.model.map(model.LABELS),D=q.point_D,R=q.point_R,
                                   Actual_D=q.actual_D,Expected_D=q.expected_D_exact,D_low70=q.D_lo70,D_high70=q.D_hi70,
                                   D_low95=q.D_lo95,D_high95=q.D_hi95,D_at_least_51=q.p_D_at_least_51,
                                   Unmodeled_contest_completions=q.unmodeled_contested))
    return pd.concat([t,old],ignore_index=True).round(3)


def withholding(f):
    rows=[]
    for (s,y,m),g in f['masked_predictions'].query('cycle<2026').groupby(['scenario','cycle','model']):
        rows.append(dict(Horizon=s,Cycle=y,Model=model.LABELS[m],N=len(g),MAE_pp=float(abs(g.prediction_pp-100*g.actual).mean()),
                         Correct=int(((g.prediction_pp>0)==(g.actual>0)).sum())))
    return pd.DataFrame(rows).round(3)


def audit(f,out,lab):
    out,lab=Path(out),Path(lab);settings=json.loads((out/'settings.json').read_text());source=Path(settings['source'])
    checks={}
    checks['frozen_revision2_unchanged']=v1.verify(source)==settings['source_manifest_sha256']
    checks['original_inputs_unchanged']=all(v1.sha(p)==s for p,s in settings['provenance']['paths'].items())
    checks['earlier_notebooks_unchanged']=all(v1.sha(lab/p)==s for p,s in settings['old_notebook_hashes'].items())
    w=f['prior_weights'];checks['all_prior_sources_strictly_earlier']=bool((w.source_cycle<w.forecast_cycle).all())
    checks['prior_weights_normalized']=bool(np.allclose(w.groupby(['scenario','target_id','recipe']).weight.sum(),1))
    pp=f['prepared_histories'];nohistory=pp.prior_fallback
    checks['no_history_fallbacks_unchanged']=bool(np.allclose(pp.loc[nohistory,'prior'],pp.loc[nohistory,'source_prior']))
    s=f['selected'];checks['outer_fits_strictly_earlier']=bool((s.training_max_cycle<s.cycle).all())
    t=f['covariance_tuning'];checks['covariance_tuning_strictly_earlier']=bool(((t.fit_max_cycle<t.validation_cycle)&(t.validation_cycle<t.forecast_cycle)).all())
    t=f['half_life_tuning'];checks['mean_tuning_strictly_earlier']=bool(((t.validation_cycle<t.forecast_cycle)&(t.max_prior_source_cycle<t.validation_cycle)).all())
    t=f['strength_tuning'];checks['strength_tuning_strictly_earlier']=bool(((t.fit_max_cycle<t.validation_cycle)&(t.validation_cycle<t.forecast_cycle)).all())
    # Each decay-strength validation recipe must be selected for that validation year,
    # never copied from the outer target's selected half-life.
    half=f['half_life_tuning'];choice={}
    for (scenario,y),g in half.groupby(['scenario','forecast_cycle']):
        scores=g.groupby('half_life').prior_mae_pp.mean()
        h=min(scores.index,key=lambda x:(scores.loc[x],{8.:0,16.:1,4.:2}[x]));choice[(scenario,y)]=f'decay{h:g}'
    checks['strength_validation_reselects_mean_past_only']=all(r.validation_recipe==choice[(r.scenario,r.validation_cycle)] for r in t[t.family.eq('decay')].itertuples())
    selected_a=[]
    for r in s.itertuples():
        rows=t[t.scenario.eq(r.scenario)&t.forecast_cycle.eq(r.cycle)&t.family.eq(r.family)]
        a,status=model.select_multiplier(rows.to_dict('records'));selected_a.append(a==r.variance_multiplier and status==r.strength_status)
    checks['strength_selection_reconstructed']=all(selected_a)
    d=f['fit_diagnostics'];checks['all_em_fits_converged']=bool(d.converged.all())
    checks['all_fit_covariances_positive']=bool((d.min_eigenvalue>0).all())
    checks['em_objectives_monotone']=bool((d.min_objective_increment>=-1e-5).all())
    pred=f['predictions'];new=pred[pred.model.isin(model.MODELS)]
    checks['identical_cases_for_all_models']=all(len({tuple(sorted(b.target_id)) for _,b in g.groupby('model')})==1 for _,g in pred.groupby(['scenario','cycle']))
    keys=['scenario','cycle','target_id'];old=pred[pred.model.eq('v2_linked')].set_index(keys).sort_index();current=pred[pred.model.eq('v3_current_fixed')].set_index(keys).sort_index()
    cols=['prediction_pp','posterior_sd_pp','p_dem','lo95_pp','hi95_pp']
    checks['unmodified_recipe_reproduces_revision2']=bool(np.allclose(current[cols],old[cols],atol=1e-9))
    same=[]
    for _,g in new.groupby('model'):
        g=g.set_index(keys).sort_index();same.append(np.allclose(g[['actual','q_pp','firm_mass','sample_count']],old[['actual','q_pp','firm_mass','sample_count']],equal_nan=True))
    checks['outcomes_and_poll_inputs_unchanged']=all(same)
    checks['finite_valid_predictions']=bool(np.isfinite(new[cols]).all().all() and new.p_dem.between(0,1).all())
    eig=[];drawmeans=[];scale=[];reconstruct=[]
    for (scenario,year,m),g in new.groupby(['scenario','cycle','model']):
        z=np.load(out/'draws'/f'{scenario}_{year}_{m}.npz');g=g.set_index('target_id').loc[z['target_ids']]
        eig.append(np.linalg.eigvalsh(z['covariance_pp2']).min()>0)
        se=g.posterior_sd_pp.to_numpy()/np.sqrt(len(z['margins_pp']))
        drawmeans.append(np.all(abs(z['margins_pp'].mean(axis=0)-g.prediction_pp.to_numpy())<6*se+.02))
        if m.endswith('_tuned'):
            fixed=np.load(out/'draws'/f'{scenario}_{year}_{m.replace("_tuned","_fixed")}.npz')
            scale.append(np.allclose(z['prior_covariance_pp2'],fixed['prior_covariance_pp2']*g.variance_multiplier.iloc[0]))
        # Reconstruct every forecast independently from saved covariance and bias fits.
        family=m.split('_')[1];r=s[s.scenario.eq(scenario)&s.cycle.eq(year)&s.family.eq(family)].iloc[0]
        movement=d.query('recipe==@r.recipe and scenario=="all" and cycle==@year and component=="movement" and kappa==@r.movement_kappa').iloc[0]
        polling=d.query('recipe=="current" and scenario==@scenario and cycle==@year and component=="poll" and kappa==@r.poll_kappa').iloc[0]
        mm=np.load(out/movement.path);pol=np.load(out/polling.path)
        p,c,_=model.scaled_predict(g.reset_index(),dict(covariance=mm['covariance']),dict(covariance=pol['covariance'],bias_mean=pol['bias_mean'],bias_covariance=pol['bias_covariance']),float(g.variance_multiplier.iloc[0]))
        reconstruct.append(np.allclose(p.prediction_pp,g.prediction_pp) and np.allclose(c,z['covariance_pp2']))
    checks['all_posterior_covariances_positive']=all(eig);checks['joint_draws_match_means']=all(drawmeans)
    checks['multiplier_scales_whole_prior_covariance']=all(scale);checks['all_forecasts_reconstructed']=all(reconstruct)
    result=dict(passed=all(checks.values()),checks=checks,new_forecasts=len(new),outer_folds=len(s)//3,cached_component_fits=len(d),
                new_component_fits=int((~d.reused_v2).sum()),maximum_out_of_bounds_probability=float(new.outside_margin_bounds_probability.max()),
                shared_strength=True,state_specific_strength=False,selection_uncertainty_included=False)
    v1.json_write(out/'completion_audit.json',result)
    if not result['passed']:raise AssertionError(result)
    return result


def plots(f,out):
    out=Path(out);paths=[]
    fig,axes=plt.subplots(1,2,figsize=(13,4.5))
    p=prior_scores(f)
    for ax,s in zip(axes,['matched_live','oct31']):
        g=p[p.Horizon.eq(s)];ax.bar(g.Prior,g.MAE_pp,color=['#9eacb1','#36829b','#9caf71'])
        ax.set(title=s,ylabel='Prior-only MAE (pp)')
    fig.suptitle('Prior centers before using polls: 2016–2024');fig.tight_layout();paths.append(out/'prior_mae.png');fig.savefig(paths[-1],dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(14,6));keys=['v2_linked','v3_current_tuned','v3_latest_fixed','v3_latest_tuned','v3_decay_fixed','v3_decay_tuned','nonbayes_bias']
    q=f['metrics'].query('period=="recent_2016_2024" and group=="all"')
    for ax,s in zip(axes,['matched_live','oct31']):
        g=q[q.scenario.eq(s)].set_index('model').loc[keys];ax.barh([model.LABELS[k] for k in keys],g.mae_pp,color='#367f96');ax.invert_yaxis();ax.set(title=s,xlabel='Posterior MAE (pp), equal cycle weight')
    fig.tight_layout();paths.append(out/'posterior_mae.png');fig.savefig(paths[-1],dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.5));q=f['selected']
    for ax,s in zip(axes,['matched_live','oct31']):
        for family,g in q[q.scenario.eq(s)].groupby('family'):ax.plot(g.cycle,g.variance_multiplier,marker='o',label=family)
        ax.set_yscale('log',base=2);ax.set_yticks(model.CONFIG['variance_multipliers'],model.CONFIG['variance_multipliers']);ax.axhline(1,color='black',ls=':',lw=1);ax.set(title=s,xlabel='Forecast cycle',ylabel='Selected prior variance multiplier');ax.legend()
    fig.tight_layout();paths.append(out/'selected_strength.png');fig.savefig(paths[-1],dpi=145);plt.close(fig)
    h=f['prior_predictions'].query('scenario=="matched_live" and cycle>=2000');fig,axes=plt.subplots(1,2,figsize=(13,4.5))
    for ax,state in zip(axes,['AL','OH']):
        g=h[h.geography.eq(state)]
        for fam,b in g.groupby('family'):ax.plot(b.cycle,100*b.prior,marker='o',label=fam)
        a=g[g.family.eq('current')];ax.scatter(a.cycle,100*a.actual,color='black',marker='x',s=55,label='Actual')
        ax.axhline(0,color='grey',lw=.7);ax.set(title=state,ylabel='D−R margin (pp)',xlabel='Cycle');ax.legend(fontsize=8)
    fig.suptitle('Historical starting points, before current polls');fig.tight_layout();paths.append(out/'alabama_ohio_priors.png');fig.savefig(paths[-1],dpi=145);plt.close(fig)
    q=f['predictions'].query('cycle==2026 and model=="v3_decay_tuned"').sort_values('prediction_pp');fig,ax=plt.subplots(figsize=(9,10));y=np.arange(len(q))
    ax.hlines(y,q.lo95_pp,q.hi95_pp,color='#bacbd1',lw=2);ax.hlines(y,q.lo70_pp,q.hi70_pp,color='#337c91',lw=4);ax.scatter(q.prediction_pp,y,s=18,color='#234959');ax.axvline(0,color='black',lw=.6)
    ax.set_yticks(y,q.geography+np.where(q.special,' special',''));ax.set(title='Decay prior + tuned shared strength: frozen September 17, 2026',xlabel='D−R margin (pp); central 70% / 95% intervals');fig.tight_layout();paths.append(out/'current_ranges.png');fig.savefig(paths[-1],dpi=145);plt.close(fig)
    return paths


def report(lab,out):
    lab,out=Path(lab),Path(out);f=load(out);a=audit(f,out,lab);paths=plots(f,out)
    st=seats(f,out);st.to_parquet(out/'seat_comparison.parquet',index=False)
    cs=cycles(f);cs.to_parquet(out/'cycle_scores.parquet',index=False)
    allstates=pd.concat([states(f,int(y),s).assign(Cycle=y,Horizon=s) for s,y in f['predictions'][['scenario','cycle']].drop_duplicates().itertuples(index=False,name=None)],ignore_index=True)
    allstates.to_parquet(out/'all_state_tables.parquet',index=False)
    text='# Prior Revision 3 — results\n\n'
    text+='Separate notebook: `BAYESIAN_PRIOR_REVISION3.ipynb`. Exact design: `BAYESIAN_PRIOR_REVISION3.md`. Frozen September 17, 2026 inputs; no data refresh. Each recipe has a fixed-strength control and a shared, past-only tuned variance multiplier. Values below 1 strengthen the prior; above 1 weaken it. State-specific multipliers are deferred.\n\n'
    text+='## Prior centers before polling\n\nPositive actual-minus-prior error means the prior understated Democrats. MAE and mean error give each cycle equal weight; absolute state mean error exposes cancellation across states.\n\n'+prior_scores(f).to_markdown(index=False)+'\n\n'
    text+='## Recent posterior performance\n\n2016–2024, identical cases. Correct winners pool contests; MAE averages cycles equally. Non-Bayesian references have no invented probability metrics.\n\n'+performance(f).to_markdown(index=False)+'\n\n'
    text+='## Competitive states\n\n'+performance(f,'competitive').to_markdown(index=False)+'\n\n'
    text+='## Noncompetitive states\n\n'+performance(f,'noncompetitive').to_markdown(index=False)+'\n\n'
    text+='## Parameters selected using earlier cycles\n\nThe shared variance multiplier is equivalent to precision penalty 1/a. Boundary choices warrant follow-up; the grid was not expanded after seeing results.\n\n'+f['selected'].round(3).to_markdown(index=False)+'\n\n'
    text+='## Alabama and Ohio diagnostics\n\nResidual statistics describe historical prior errors under the selected fixed recipe; they are not intrinsic state volatility. No-history states retain existing fallbacks.\n\n'+f['state_parameters'].query('state in ["AL","OH"]').round(3).to_markdown(index=False)+'\n\n'
    text+='## Historical cycle scores\n\n'+cs.to_markdown(index=False)+'\n\n'
    text+='## Current states\n\nMargins are D minus R in percentage points. Current actuals are missing.\n\n'+states(f).to_markdown(index=False)+'\n\n'
    text+='## Full chamber totals\n\nD includes mapped Democratic-caucusing independents. Existing ballot/rule and unmodeled-contest completion assumptions remain. Expected seats sum marginal win probabilities; point seats count positive mean margins.\n\n'+st.to_markdown(index=False)+'\n\n'
    text+='## Withheld state polls\n\nThe target state has its polling removed; other state polls remain.\n\n'+withholding(f).to_markdown(index=False)+'\n\n'
    text+='## Audit\n\n'+pd.DataFrame([dict(Check=k,Passed=v) for k,v in a['checks'].items()]).to_markdown(index=False)+'\n\n'
    text+='## Limits\n\nThese are empirical-Bayes conditional intervals: covariance and hyperparameter-selection uncertainty are excluded. Priors/strength were selected on few earlier cycles; no new state-specific tuning or claim of general superiority. The existing historical admission gaps (AK/GA/LA/ME), candidate/seat differences and Gaussian support outside physical margin bounds remain. Compare prior-only performance, posterior calibration, per-cycle and competitive/noncompetitive results before promoting any model.\n'
    (lab/'BAYESIAN_PRIOR_REVISION3_RESULTS.md').write_text(text);(out/'BAYESIAN_PRIOR_REVISION3_RESULTS.md').write_text(text)
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes());v1.manifest(out)
    v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return f,paths,a


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('out',type=Path);p.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args();report(a.lab,a.out)
