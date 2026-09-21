"""Prior audit, matched performance and reconstruction for Revision 5."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import bayesian_prior_revision5 as model
import simple_bayesian_polling as v1


def load(out):
    v1.verify(out);return {p.stem:pd.read_parquet(p) for p in Path(out).glob('*.parquet')}


def performance(f,group='all',period='recent_2016_2024'):
    q=f['metrics'].query('group==@group and period==@period').copy();q['Model']=q.model.map(model.LABELS)
    q['Correct']=q.correct.astype(str)+'/'+q.n.astype(str);q['Coverage95_pct']=100*q.coverage95
    return q[['scenario','Model','Correct','mae_pp','brier','Coverage95_pct','mean95_width_pp']].round(3)


def prior_scores(f,out):
    source=Path(json.loads((Path(out)/'settings.json').read_text())['source']);old=pd.read_parquet(source/'prior_predictions.parquet')
    old=old.query('family=="decay"').copy();old['family']='previous_decay';old['mean_correction_pp']=0.
    q=pd.concat([f['prior_predictions'],old],ignore_index=True).query('scenario=="matched_live" and 2016<=cycle<=2024');rows=[]
    for family,g in q.groupby('family'):
        e=100*(g.actual-g.prior)
        rows.append(dict(Prior=family,N=len(g),Correct=int(((g.prior>0)==(g.actual>0)).sum()),MAE_pp=float(e.abs().groupby(g.cycle).mean().mean()),
                         Mean_error_pp=float(e.groupby(g.cycle).mean().mean()),Mean_abs_state_error_pp=float(e.groupby(g.geography).mean().abs().mean())))
    return pd.DataFrame(rows).round(3)


def cycles(f):
    rows=[]
    for (s,y,m),g in f['predictions'].query('cycle<2026').groupby(['scenario','cycle','model']):
        rows.append(dict(Horizon=s,Cycle=y,Model=model.LABELS[m],N=len(g),Correct=int(((g.prediction_pp>0)==(g.actual>0)).sum()),MAE_pp=float(abs(g.prediction_pp-100*g.actual).mean())))
    return pd.DataFrame(rows).round(3)


def states(f,year=2026,scenario='matched_live'):
    q=f['predictions'].query('cycle==@year and scenario==@scenario');b=q[q.model.eq('v5_corrected_state')].set_index('target_id')
    t=pd.DataFrame(dict(State=b.geography+np.where(b.special,' special',''),Actual_pp=100*b.actual,Base_prior_pp=b.base_prior_pp,Mean_correction_pp=b.mean_correction_pp,
                        Corrected_prior_pp=100*b.prior,Raw_poll_pp=b.q_pp,Corrected_state_pp=b.prediction_pp,D_probability=b.p_dem,Low95_pp=b.lo95_pp,High95_pp=b.hi95_pp))
    for m in ['v4_decay_state','v3_decay_fixed','v5_fast_fixed','v5_fast_shared','v5_fast_state','v5_corrected_fixed','v5_corrected_shared','nonbayes_bias']:
        t[m+'_pp']=q[q.model.eq(m)].set_index('target_id').prediction_pp
    return t.reset_index().sort_values('State').round(3)


def seats(f,out):
    s=json.loads((Path(out)/'settings.json').read_text());old=pd.read_parquet(Path(s['reference'])/'seat_comparison.parquet');q=f['seats']
    t=pd.DataFrame(dict(Horizon=q.scenario,Cycle=q.cycle,Model=q.model.map(model.LABELS),D=q.point_D,R=q.point_R,Actual_D=q.actual_D,
                        Expected_D=q.expected_D_exact,D_low70=q.D_lo70,D_high70=q.D_hi70,D_low95=q.D_lo95,D_high95=q.D_hi95,
                        D_at_least_51=q.p_D_at_least_51,Unmodeled_contest_completions=q.unmodeled_contested))
    return pd.concat([t,old],ignore_index=True).round(3)


def withholding(f,out):
    ref=Path(json.loads((Path(out)/'settings.json').read_text())['reference']);old=pd.read_parquet(ref/'masked_predictions.parquet')
    q=pd.concat([f['masked_predictions'],old],ignore_index=True).query('cycle<2026');rows=[]
    for (s,y,m),g in q.groupby(['scenario','cycle','model']):rows.append(dict(Horizon=s,Cycle=y,Model=model.LABELS[m],N=len(g),MAE_pp=float(abs(g.prediction_pp-100*g.actual).mean()),Correct=int(((g.prediction_pp>0)==(g.actual>0)).sum())))
    return pd.DataFrame(rows).round(3)


def audit(f,out,lab):
    out,lab=Path(out),Path(lab);settings=json.loads((out/'settings.json').read_text());checks={}
    checks['frozen_reference_artifacts_unchanged']=all(v1.verify(p)==digest for p,digest in settings['source_hashes'].items())
    checks['original_sources_unchanged']=all(v1.sha(p)==digest for p,digest in settings['provenance']['paths'].items())
    checks['previous_notebooks_unchanged']=all(v1.sha(lab/name)==digest for name,digest in settings['old_notebook_hashes'].items())
    checks['input_review_tables_unchanged']=all(v1.sha(p)==digest for p,digest in json.loads((out/'input_review_sources.json').read_text()).items())
    checks['no_admission_changes']=bool((~f['official_result_followups'].admission_changed).all())
    h=f['prepared_histories'];nonfallback=h[~h.prior_fallback];checks['prior_mean_sources_past_only']=bool((nonfallback.prior_source_max_cycle<nonfallback.cycle).all())
    fallback=h[h.prior_fallback];checks['uncorrected_no_history_fallback_unchanged']=bool(np.allclose(fallback.prior,fallback.source_prior))
    d=f['fit_diagnostics'];checks['component_training_past_only']=bool((d.training_max_cycle<d.cycle).all());checks['em_converged']=bool(d.converged.all())
    checks['em_objective_monotone']=bool((d.min_objective_increment>=-1e-5).all());checks['process_covariance_positive']=bool((d.min_eigenvalue>0).all())
    for key in ['covariance_tuning','strength_tuning','local_tuning']:
        t=f[key];checks[key+'_past_only']=bool(((t.fit_max_cycle<t.validation_cycle)&(t.validation_cycle<t.forecast_cycle)).all())
    t=f['half_life_tuning'];checks['half_life_tuning_past_only']=bool(((t.max_prior_source_cycle<t.validation_cycle)&(t.validation_cycle<t.forecast_cycle)).all())
    halfchoices={}
    for (s,y),g in t.groupby(['scenario','forecast_cycle']):
        sc=g.groupby('half_life').prior_mae_pp.mean();half=min(sc.index,key=lambda h:(sc.loc[h],{8.:0,16.:1,4.:2,2.:3}[h]));halfchoices[(s,y)]=f'decay{half:g}'
    checks['nested_mean_choices_reconstructed']=all(r.validation_recipe.removesuffix('_corrected')==halfchoices[(r.scenario,r.validation_cycle)] for r in f['strength_tuning'].itertuples())
    profile=f['state_penalties'];recon=[]
    for (s,y,fam),g in profile.groupby(['scenario','cycle','family']):
        t=f['local_tuning'];t=t[t.scenario.eq(s)&t.forecast_cycle.eq(y)&t.family.eq(fam)]
        _,p=model.v4.shrink_state_scores(t,float(g.shared_multiplier.iloc[0]),int(y))
        recon.append(np.allclose(p.set_index('state').sort_index().variance_multiplier,g.set_index('state').sort_index().variance_multiplier))
    checks['state_penalties_reconstructed']=all(recon)
    a=[]
    for r in f['folds'].itertuples():
        t=f['strength_tuning'];t=t[t.scenario.eq(r.scenario)&t.forecast_cycle.eq(r.cycle)&t.family.eq(r.family)]
        value,status=model.v3.select_multiplier(t.to_dict('records'));a.append(value==r.shared_multiplier and status==r.strength_status)
    checks['shared_penalties_reconstructed']=all(a)
    old=pd.read_parquet(Path(settings['reference'])/'predictions.parquet');pred=f['predictions'];new=pred[pred.model.isin(model.MODELS)]
    keep=pred[pred.model.isin(old.model.unique())];keys=['scenario','cycle','model','target_id']
    pd.testing.assert_frame_equal(keep[old.columns].sort_values(keys).reset_index(drop=True),old.sort_values(keys).reset_index(drop=True),check_dtype=False)
    checks['old_predictions_retained_exactly']=True
    checks['identical_comparison_cases']=all(len({tuple(sorted(g.target_id)) for _,g in b.groupby('model')})==1 for _,b in pred.groupby(['scenario','cycle']))
    checks['finite_predictions_and_probabilities']=bool(np.isfinite(new[['prediction_pp','posterior_sd_pp','p_dem','lo95_pp','hi95_pp']]).all().all() and new.p_dem.between(0,1).all())
    pp=f['prior_predictions'];checks['corrected_center_reconstructed']=bool(np.allclose(100*pp.prior,pp.base_prior_pp+pp.mean_correction_pp))
    pars=f['state_parameters'];checks['prior_uncertainty_decomposition']=bool(np.allclose(pars.total_prior_sd_pp**2,pars.process_sd_pp**2+pars.correction_sd_pp**2))
    fore=[];eig=[];mc=[];pollsame=[];sameinputs=[];correction_psd=[]
    for r in f['folds'].itertuples():
        mov=np.load(out/r.movement_path);poll=np.load(out/r.poll_path)
        proc=mov['covariance'];extra=mov['bias_covariance'] if r.family=='corrected' else np.zeros_like(proc)
        correction_psd.append(np.linalg.eigvalsh(extra).min()>-1e-9)
        oldpoll=np.load(Path(settings['source'])/r.poll_path);pollsame.append(all(np.allclose(poll[k],oldpoll[k],atol=1e-12) for k in ['covariance','bias_mean','bias_covariance']))
        for mode in model.MODES:
            m=f'v5_{r.family}_{mode}';g=new[new.scenario.eq(r.scenario)&new.cycle.eq(r.cycle)&new.model.eq(m)]
            z=np.load(out/'draws'/f'{r.scenario}_{r.cycle}_{m}.npz');g=g.set_index('target_id').loc[z['target_ids']].reset_index()
            p,c,meta=model.v4.state_predict(g,dict(covariance=proc+extra),dict(covariance=poll['covariance'],bias_mean=poll['bias_mean'],bias_covariance=poll['bias_covariance']),z['multipliers_all_states'])
            fore.append(np.allclose(p.prediction_pp,g.prediction_pp,atol=1e-10) and np.allclose(c,z['covariance_pp2']) and np.allclose(meta['prior_covariance'],z['prior_covariance_pp2']))
            eig.append(np.linalg.eigvalsh(c).min()>0 and np.linalg.eigvalsh(meta['prior_covariance']).min()>0)
            se=g.posterior_sd_pp.to_numpy()/np.sqrt(len(z['margins_pp']));mc.append(np.all(abs(z['margins_pp'].mean(axis=0)-g.prediction_pp.to_numpy())<6*se+.02))
            base=old[old.scenario.eq(r.scenario)&old.cycle.eq(r.cycle)&old.model.eq('v4_decay_state')].set_index('target_id').loc[g.target_id]
            sameinputs.append(np.allclose(g[['actual','q_pp','firm_mass','sample_count']],base[['actual','q_pp','firm_mass','sample_count']],equal_nan=True))
    checks['all_forecasts_reconstructed']=all(fore);checks['positive_forecast_covariances']=all(eig);checks['correction_covariance_psd']=all(correction_psd)
    checks['joint_draws_match_means']=all(mc);checks['polling_bias_covariance_unchanged']=all(pollsame);checks['labels_and_poll_inputs_unchanged']=all(sameinputs)
    result=dict(passed=all(checks.values()),checks=checks,new_forecasts=len(new),outer_folds=len(f['folds'])//2,cached_components=len(d),new_components=int((~d.reused).sum()),
                correction_uncertainty_included=True,covariance_and_selection_uncertainty_included=False,
                maximum_outside_bounds_probability=float(new.outside_margin_bounds_probability.max()))
    v1.json_write(out/'completion_audit.json',result)
    if not result['passed']:raise AssertionError(result)
    return result


def plots(f,out):
    out=Path(out);paths=[]
    prior=prior_scores(f,out);fig,ax=plt.subplots(figsize=(8,4));ax.bar(prior.Prior,prior.MAE_pp,color=['#3b8199','#8facb8','#b68d69']);ax.set(ylabel='Prior-only MAE (pp)',title='Starting points before polling: 2016–2024');fig.tight_layout();paths.append(out/'prior_mae.png');fig.savefig(paths[-1],dpi=145);plt.close(fig)
    q=f['metrics'].query('period=="recent_2016_2024" and group=="all"');keys=['v4_decay_state','v5_fast_fixed','v5_fast_shared','v5_fast_state','v5_corrected_fixed','v5_corrected_shared','v5_corrected_state','nonbayes_bias']
    fig,axes=plt.subplots(1,2,figsize=(14,6))
    for ax,s in zip(axes,['matched_live','oct31']):
        g=q[q.scenario.eq(s)].set_index('model').loc[keys];ax.barh([model.LABELS[k] for k in keys],g.mae_pp,color='#3b8097');ax.invert_yaxis();ax.set(title=s,xlabel='MAE (pp), equal cycle weight')
    fig.tight_layout();paths.append(out/'posterior_mae.png');fig.savefig(paths[-1],dpi=145);plt.close(fig)
    p=f['prior_predictions'].query('scenario=="matched_live"');fig,axes=plt.subplots(1,3,figsize=(15,4.5))
    for ax,s in zip(axes,['MI','WV','SD']):
        g=p[p.geography.eq(s)]
        for fam,b in g.groupby('family'):ax.plot(b.cycle,100*b.prior,marker='o',label=fam)
        b=g[g.family.eq('fast')];ax.scatter(b.cycle,100*b.actual,color='black',marker='x',label='Actual');ax.axhline(0,color='grey',lw=.7);ax.set(title=s,xlabel='Cycle',ylabel='D−R prior margin (pp)');ax.legend(fontsize=8)
    fig.tight_layout();paths.append(out/'reviewed_prior_states.png');fig.savefig(paths[-1],dpi=145);plt.close(fig)
    p=f['state_parameters'].query('cycle==2026 and family=="corrected"').sort_values('correction_pp');fig,ax=plt.subplots(figsize=(9,10));y=np.arange(len(p));ax.errorbar(p.correction_pp,y,xerr=1.96*p.correction_sd_pp,fmt='o',markersize=3,color='#337b93');ax.axvline(0,color='black',lw=.7);ax.set_yticks(y,p.state);ax.tick_params(axis='y',labelsize=8);ax.set(title='2026 prior-mean corrections with conditional 95% ranges',xlabel='Correction to base prior (pp); positive favors Democrats');fig.tight_layout();paths.append(out/'current_mean_corrections.png');fig.savefig(paths[-1],dpi=145);plt.close(fig)
    return paths


def report(lab,out):
    lab,out=Path(lab),Path(out);f=load(out);a=audit(f,out,lab);paths=plots(f,out);chamber=seats(f,out)
    chamber.to_parquet(out/'seat_comparison.parquet',index=False);cycles(f).to_parquet(out/'cycle_scores.parquet',index=False)
    pd.concat([states(f,int(y),s).assign(Cycle=y,Horizon=s) for s,y in f['folds'][['scenario','cycle']].drop_duplicates().itertuples(index=False,name=None)],ignore_index=True).to_parquet(out/'all_state_tables.parquet',index=False)
    text='# Prior Revision 5 — review and results\n\n'
    text+='Notebook: `BAYESIAN_PRIOR_REVISION5.ipynb`. Design: `BAYESIAN_PRIOR_REVISION5.md`. Frozen September 17, 2026 inputs. Faster prior adds a two-year half-life to the existing grid. The separate corrected variant learns a shared plus shrunk state mean-error correction jointly with residual covariance, carrying correction uncertainty into the prior. All variants retune strengths using earlier cycles only.\n\n'
    text+='## Targeted input review\n\nMichigan recent outcomes are admitted; its lag is present with those data available. West Virginia 2018 and South Dakota 2020 are excluded by existing unofficial-source flags. South Dakota 2010 lacks a unique D/R pair; West Virginia 2010 is special. These are distinct admission issues, not evidence that every large miss is corrupted polling data. The official result follow-ups below are documented without changing this matched experiment.\n\n'+f['prior_input_review'].to_markdown(index=False)+'\n\n'+f['official_result_followups'].round(5).to_markdown(index=False)+'\n\n'
    text+='Official support: [FEC Federal Elections 2018, WV pp. 32–33](https://www.fec.gov/documents/2705/federalelections2018.pdf); [South Dakota 2020 state canvass](https://sdsos.gov/elections-voting/assets/2020%20Assests/2020GeneralStateCanvassFinal%26Certificate.pdf). The latter totals were available in the official indexed table; direct PDF retrieval failed during this review. An admission refresh remains a separate dataset revision.\n\n'
    text+='## Prior-only recent performance\n\nMean error is actual minus prior. MAE averages cycles equally; absolute state mean error exposes directional errors that cancel across states.\n\n'+prior_scores(f,out).to_markdown(index=False)+'\n\n'
    for title,group in [('Recent final forecasts','all'),('Competitive states','competitive'),('Noncompetitive states','noncompetitive')]:text+=f'## {title}\n\n2016–2024; identical targets. Correct calls pool contests, MAE averages cycles equally.\n\n'+performance(f,group).to_markdown(index=False)+'\n\n'
    text+='## Selected half-lives and strengths\n\n'+f['folds'].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current prior-mean corrections and uncertainty\n\nTotal unscaled prior variance is process variance plus posterior correction variance. These are not polling-bias corrections. New shared/state correction prior SDs 3/5 pp are fixed assumptions, not independently validated hyperparameters.\n\n'+f['state_parameters'].query('cycle==2026').round(3).to_markdown(index=False)+'\n\n'
    text+='## By cycle\n\n'+cycles(f).to_markdown(index=False)+'\n\n## Current states\n\n'+states(f).to_markdown(index=False)+'\n\n'
    text+='## Full chamber totals\n\nD includes mapped Democratic-caucusing independents; original ballot/completion rules remain.\n\n'+chamber.to_markdown(index=False)+'\n\n'
    text+='## Withheld-state polls\n\n'+withholding(f,out).to_markdown(index=False)+'\n\n'
    text+='## Checks\n\n'+pd.DataFrame([dict(Check=k,Passed=v) for k,v in a['checks'].items()]).to_markdown(index=False)+'\n\n'
    text+='## Limits and decision\n\nNo automatic promotion. The correction posterior uncertainty is included, but process-covariance and hyperparameter-selection uncertainty are not. Current state corrections extrapolate a persistent-error assumption under historical relevance weighting. Candidate/seat effects and admission gaps remain. Compare prior-only versus final accuracy, horizon, competitive cases and coverage before interpreting a retrospective gain as general.\n'
    (lab/'BAYESIAN_PRIOR_REVISION5_RESULTS.md').write_text(text);(out/'BAYESIAN_PRIOR_REVISION5_RESULTS.md').write_text(text)
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes());v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return f,paths,a


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('out',type=Path);p.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args();report(a.lab,a.out)
