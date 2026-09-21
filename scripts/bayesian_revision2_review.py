"""Readable analyses and numerical/provenance audits for revision 2."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import bayesian_revision2 as model
import simple_bayesian_polling as v1


def load(out):
    v1.verify(out)
    return {p.stem:pd.read_parquet(p) for p in Path(out).glob('*.parquet')}


def performance(f,group='all',period='recent_2016_2024'):
    q=f['metrics'].query('group==@group and period==@period').copy()
    q['Model']=q.model.map(model.LABELS);q['Correct']=q.correct.astype(str)+'/'+q.n.astype(str)
    q['95% coverage']=100*q.coverage95
    return q[['scenario','Model','Correct','mae_pp','brier','95% coverage','mean95_width_pp']].round(3)


def cycle_scores(f):
    rows=[]
    for (s,y,m),g in f['predictions'].query('cycle<2026').groupby(['scenario','cycle','model']):
        rows.append(dict(Horizon=s,Cycle=y,Model=model.LABELS[m],Contests=len(g),
                         Correct=int(((g.prediction_pp>0)==(g.actual>0)).sum()),
                         MAE_pp=float(abs(g.prediction_pp-100*g.actual).mean())))
    return pd.DataFrame(rows).round(3)


def states(f,cycle=2026,scenario='matched_live'):
    q=f['predictions'].query('cycle==@cycle and scenario==@scenario')
    base=q.query("model=='v2_linked'").set_index('target_id')
    t=pd.DataFrame(dict(State=base.geography+np.where(base.special,' special',''),Poll_samples=base.sample_count.astype(int),
                        Prior_pp=100*base.prior,Raw_poll_pp=base.q_pp,V2_pp=base.prediction_pp,
                        D_win_pct=100*base.p_dem,Low95_pp=base.lo95_pp,High95_pp=base.hi95_pp,Actual_pp=100*base.actual))
    for key,label in [('v2_local','V2_local_pp'),('v1_linked','V1_pp'),('nonbayes_bias','Corrected_poll_pp')]:
        t[label]=q.query('model==@key').set_index('target_id').prediction_pp
    return t.reset_index().round(3).sort_values('State')


def current_parameters(f):
    a=f['state_parameters'].query("cycle==2026 and component=='movement'").set_index('state')
    b=f['state_parameters'].query("cycle==2026 and component=='poll'").set_index('state')
    return pd.DataFrame(dict(State=a.index,Prior_SD_pp=a.process_sd_pp,Outcome_cycles=a.observed_cycles,
                            Prior_residual_mean_pp=a.residual_mean_pp,Prior_residual_RMS_pp=a.residual_rms_pp,
                            Poll_process_SD_pp=b.process_sd_pp,Polled_cycles=b.observed_cycles,
                            Poll_bias_pp=b.bias_poll_minus_final_pp,Bias_SD_pp=b.bias_sd_pp)).reset_index(drop=True).round(3)


def seat_table(f,out):
    settings=json.loads((Path(out)/'settings.json').read_text())
    ledger=next(Path(p) for p in settings['provenance']['paths'] if p.endswith('state_surprise/20260919T011532.132689Z/full_seat_ledger.parquet'))
    roster=pd.read_parquet(ledger).query("model=='polling'")
    old=pd.read_parquet(Path(settings['source'])/'seats.parquet').replace({'model':{'linked':'v1_linked','local':'v1_local'}})
    seats=pd.concat([f['seats'],old],ignore_index=True)
    rows=[]
    for (s,y,m),g in f['predictions'].groupby(['scenario','cycle','model']):
        r=roster[(roster.scenario==s)&(roster.cycle==y)];fixed=r[~r.target_id.isin(g.target_id)]
        d=int(fixed.caucus.eq('D').sum()+(g.prediction_pp>0).sum())
        row=dict(Horizon=s,Cycle=y,Model=model.LABELS[m],D=d,R=100-d,
                 Actual_D=int(r.actual_caucus.eq('D').sum()) if y<2026 else np.nan,
                 Unmodeled_contest_completions=int(fixed.contested.sum()))
        z=seats.query('scenario==@s and cycle==@y and model==@m')
        if len(z):
            a=z.iloc[0]
            row.update(Expected_D=a.get('expected_D_exact',np.nan) if pd.notna(a.get('expected_D_exact',np.nan)) else a.expected_D,
                       D_low95=a.D_lo95,D_high95=a.D_hi95,D_low70=a.get('D_lo70',np.nan),D_high70=a.get('D_hi70',np.nan),
                       D_at_least_51=a.p_D_at_least_51)
        rows.append(row)
    return pd.DataFrame(rows).round(3)


def withholding(f):
    rows=[]
    for (s,y,m),g in f['masked_predictions'].groupby(['scenario','cycle','model']):
        historical=g[g.actual.notna()]
        rows.append(dict(Horizon=s,Cycle=y,Model=model.LABELS[m],Contests=len(g),
                         Mean_abs_move_from_prior_pp=float(abs(g.prediction_pp-g.prior_pp).mean()),
                         MAE_pp=float(abs(historical.prediction_pp-100*historical.actual).mean()) if len(historical) else np.nan,
                         Correct=int(((historical.prediction_pp>0)==(historical.actual>0)).sum()) if len(historical) else np.nan))
    return pd.DataFrame(rows).round(3)


def plot(f,out):
    out=Path(out);paths=[]
    q=f['metrics'].query("period=='recent_2016_2024' and group=='all'")
    keys=['nonbayes_bias','v1_linked','v2_local','v2_movement_diagonal','v2_linked']
    fig,axes=plt.subplots(1,2,figsize=(13,4.5))
    for ax,s in zip(axes,['matched_live','oct31']):
        g=q[q.scenario==s].set_index('model').reindex(keys)
        ax.barh([model.LABELS[k] for k in keys],g.mae_pp,color=['#666','#9bafbf','#90bab6','#5f999c','#23687f'])
        ax.invert_yaxis();ax.set(xlabel='MAE, percentage points; equal cycle weight',title='September 17' if s=='matched_live' else 'October 31')
    fig.suptitle('2016–2024: covariance changes versus frozen references');fig.tight_layout()
    p=out/'performance.png';fig.savefig(p,dpi=145);plt.close(fig);paths.append(p)
    fcur=f['state_parameters'].query("cycle==2026 and component=='movement'").sort_values('process_sd_pp')
    fig,ax=plt.subplots(figsize=(10,11))
    ax.barh(fcur.state,fcur.process_sd_pp,color=np.where(fcur.observed_cycles==0,'#aaa','#31788f'))
    ax.set(xlabel='Prior SD (percentage points)',title='State-specific uncertainty around the unchanged historical mean\nGrey: no admitted local outcome history; pooled fallback')
    ax.tick_params(axis='y',labelsize=8);fig.tight_layout();p=out/'state_uncertainty.png';fig.savefig(p,dpi=145);plt.close(fig);paths.append(p)
    fig,axes=plt.subplots(1,2,figsize=(14,7))
    for ax,component in zip(axes,['movement','poll']):
        a=f['current_pairs'].query('component==@component');corr=pd.DataFrame(np.eye(50),index=model.STATES,columns=model.STATES)
        for r in a.itertuples():corr.loc[r.state_a,r.state_b]=corr.loc[r.state_b,r.state_a]=r.correlation
        im=ax.imshow(corr.to_numpy(),vmin=-1,vmax=1,cmap='RdBu_r')
        ax.set_xticks(range(50),model.STATES,rotation=90,fontsize=5);ax.set_yticks(range(50),model.STATES,fontsize=5)
        ax.set_title('Historical electoral movement' if component=='movement' else 'Historical residual polling error')
    fig.subplots_adjust(right=.9,top=.9,bottom=.12,wspace=.2);cax=fig.add_axes([.92,.2,.015,.6]);fig.colorbar(im,cax=cax,label='Correlation')
    p=out/'learned_correlations.png';fig.savefig(p,dpi=160);plt.close(fig);paths.append(p)
    q=f['predictions'].query("cycle==2026 and model=='v2_linked'").sort_values('prediction_pp')
    fig,ax=plt.subplots(figsize=(9,11));y=np.arange(len(q))
    ax.hlines(y,q.lo95_pp,q.hi95_pp,color='#adc0c9',lw=2,label='95% interval')
    ax.hlines(y,q.lo70_pp,q.hi70_pp,color='#33778d',lw=5,label='70% interval')
    ax.scatter(q.prediction_pp,y,c=np.where(q.prediction_pp>0,'#2867ad','#b44d47'),s=22,zorder=3)
    ax.axvline(0,color='black',lw=.7);ax.set_yticks(y,q.geography+np.where(q.special,' special',''))
    ax.set(xlabel='D−R margin, percentage points',title='Revision 2 — September 17, 2026 inputs\nIntervals conditional on fitted covariances');ax.legend();fig.tight_layout()
    p=out/'current_ranges.png';fig.savefig(p,dpi=145);plt.close(fig);paths.append(p)
    fig,ax=plt.subplots(figsize=(9,4.5))
    for m in model.MODELS:
        z=np.load(out/'draws'/f'matched_live_2026_{m}.npz');fixed=int(f['seats'].query('cycle==2026 and model==@m').fixed_D.iloc[0]);counts=fixed+(z['margins_pp']>0).sum(axis=1)
        ax.hist(counts,bins=np.arange(29.5,65.5),histtype='step',density=True,lw=2,label=model.LABELS[m])
    ax.set(xlabel='Total Democratic-caucus seats',ylabel='Probability mass',title='Conditional full-chamber distributions');ax.legend(fontsize=8);fig.tight_layout()
    p=out/'current_seats.png';fig.savefig(p,dpi=145);plt.close(fig);paths.append(p)
    fig,ax=plt.subplots(figsize=(8,4.5))
    for m in ['v1_linked','v2_linked','v2_local']:
        for scenario in ['matched_live','oct31']:
            r=f['metrics'].query("period=='recent_2016_2024' and group=='all' and model==@m and scenario==@scenario").iloc[0]
            ax.plot([50,80,95],[100*r['coverage'+str(c)] for c in [50,80,95]],marker='o',ls='-' if scenario=='oct31' else '--',label=f'{model.LABELS[m]}: {scenario}')
    ax.plot([40,100],[40,100],'k:',alpha=.5);ax.set(xlabel='Nominal coverage (%)',ylabel='Historical coverage (%)',title='Interval coverage, 2016–2024');ax.legend(fontsize=7);fig.tight_layout()
    p=out/'coverage.png';fig.savefig(p,dpi=145);plt.close(fig);paths.append(p)
    fig,ax=plt.subplots(figsize=(9,4.5))
    for state,g in f['arrival_trace'].groupby('geography'):ax.plot(g.samples_seen,g.prediction_pp,label=state)
    ax.axhline(0,color='black',lw=.7);ax.set(xlabel='Current samples revealed at a fixed cutoff',ylabel='Posterior D−R margin, pp',title='Poll-arrival replay; unknown releases use field-end proxies');ax.legend();fig.tight_layout()
    p=out/'arrival_replay.png';fig.savefig(p,dpi=145);plt.close(fig);paths.append(p)
    return paths


def audit(f,out,lab):
    out,lab=Path(out),Path(lab);settings=json.loads((out/'settings.json').read_text())
    checks={}
    checks['revision1_artifact_unchanged']=v1.verify(settings['source'])==settings['source_manifest_sha256']
    checks['source_hashes_unchanged']=all(v1.sha(p)==s for p,s in settings['provenance']['paths'].items())
    checks['all_previous_notebooks_unchanged']=all(v1.sha(lab/p)==s for p,s in settings['old_notebook_hashes'].items())
    checks['past_only_final_fits']=bool((f['fits'].training_max_cycle<f['fits'].cycle).all())
    t=f['tuning'];checks['past_only_nested_tuning']=bool(((t.fit_max_cycle<t.validation_cycle)&(t.validation_cycle<t.forecast_cycle)).all())
    checks['every_em_fit_converged']=bool(f['fit_diagnostics'].converged.all())
    checks['all_fitted_covariances_positive']=bool((f['fit_diagnostics'].min_eigenvalue>0).all())
    checks['em_objective_monotone']=bool((f['fit_diagnostics'].min_objective_increment>=-1e-5).all())
    pred=f['predictions'];q=pred[pred.model.isin(model.MODELS)]
    checks['finite_probabilities_intervals']=bool(np.isfinite(q[['prediction_pp','p_dem','posterior_sd_pp','lo95_pp','hi95_pp']]).all().all() and q.p_dem.between(0,1).all())
    checks['identical_comparison_cases']=all(len({tuple(sorted(g.target_id)) for _,g in block.groupby('model')})==1 for _,block in pred.groupby(['scenario','cycle']))
    checks['current_means_reconstructed']=bool(np.allclose(f['current_decomposition'].eval('prior_pp+own_poll_update_pp+other_poll_update_pp'),f['current_decomposition'].posterior_pp))
    d=f['current_decomposition'].set_index('geography');c=f['current_gain_contributions'].groupby('target_state').contribution_pp.sum()
    checks['gain_contributions_reconstruct_means']=bool(np.allclose(d.loc[c.index].posterior_pp-d.loc[c.index].prior_pp,c))
    m=f['masked_predictions'].query("model=='v2_local'");checks['local_no_poll_retains_prior']=bool(np.allclose(m.prediction_pp,m.prior_pp))
    trace=f['arrival_trace'];last=trace[trace.samples_seen==trace.samples_seen.max()];current=q.query("cycle==2026 and model=='v2_linked'").set_index('geography')
    checks['arrival_replay_reconstructs_final']=bool(np.allclose(last.prediction_pp,current.loc[last.geography].prediction_pp))
    checks['heterogeneous_state_variances']=bool(f['state_parameters'].query("cycle==2026 and component=='movement'").process_sd_pp.std()>1e-3)
    pairs=f['current_pairs'].query("component=='movement' and shared_cycles>=3")
    checks['both_positive_and_negative_supported_links']=bool((pairs.correlation>.01).any() and (pairs.correlation<-.01).any())
    mc=[];eig=[]
    for p in (out/'draws').glob('*.npz'):
        z=np.load(p);prefix=p.stem
        chosen=next(m for m in model.MODELS if prefix.endswith('_'+m));prefix=prefix[:-(len(chosen)+1)];scenario,year=prefix.rsplit('_',1);year=int(year)
        g=q.query('scenario==@scenario and cycle==@year and model==@chosen').set_index('target_id').loc[z['target_ids']]
        se=g.posterior_sd_pp.to_numpy()/np.sqrt(len(z['margins_pp']))
        mc.append(np.all(abs(z['margins_pp'].mean(axis=0)-g.prediction_pp.to_numpy())<6*se+.02))
        eig.append(np.linalg.eigvalsh(z['covariance_pp2']).min()>0)
    checks['joint_draws_match_exact_means']=all(mc);checks['all_forecast_covariances_positive']=all(eig)
    result=dict(passed=all(checks.values()),checks=checks,forecast_folds=len(f['fits'])//2,
                new_prediction_rows=len(q),cached_component_fits=len(f['fit_diagnostics']),
                covariance_parameter_uncertainty_included=False,
                maximum_out_of_bounds_probability=float(q.outside_margin_bounds_probability.max()))
    if not result['passed']:raise AssertionError(result)
    v1.json_write(out/'completion_audit.json',result)
    return result


def report(lab,out):
    lab,out=Path(lab),Path(out);f=load(out);paths=plot(f,out);a=audit(f,out,lab)
    seats=seat_table(f,out);seats.to_parquet(out/'seat_comparison.parquet',index=False)
    cycle_scores(f).to_parquet(out/'cycle_scores.parquet',index=False)
    allstates=[]
    for scenario,year in f['predictions'].query("model=='v2_linked'")[['scenario','cycle']].drop_duplicates().itertuples(index=False,name=None):
        allstates.append(states(f,year,scenario).assign(Cycle=year,Horizon=scenario))
    pd.concat(allstates,ignore_index=True).to_parquet(out/'all_state_tables.parquet',index=False)
    pars=current_parameters(f);pairs=f['current_pairs'].query("component=='movement' and shared_cycles>=3")
    text='# Bayesian Revision 2 — results and integrity review\n\n'
    text+='New notebook: `BAYESIAN_REVISION2.ipynb`. Estimator: `BAYESIAN_REVISION2_ESTIMATOR.md`. Frozen September17,2026 inputs; no source refresh. Existing notebooks and revision1 artifacts remain unchanged.\n\n'
    text+='## What changed\n\nState-specific prior variances and signed state relationships are learned from older outcome-minus-prior residual vectors. Separate residual polling covariance and persistent bias are calibrated from poll-minus-final errors. Missing values are integrated, not zero-filled. Regularization is selected using earlier-cycle validation. There is no additional national movement factor and no discrete sigma/rho grid. This is empirical Bayes: covariance-estimation uncertainty is not included in forecast intervals. Bias uncertainty is integrated. The3pp initial bias scale,4pp fresh-firm noise convention, historical mean recipe and8-year/type weighting remain explicit fixed comparison choices.\n\n'
    text+='Covariance is fitted around the unchanged zero-mean residual model. A persistent error in the historical prior therefore contributes to the fitted second moment; these SDs must not be interpreted as pure intrinsic state volatility. The residual-mean table exposes that distinction. States without admitted outcomes get pooled variance and no invented historical links.\n\n'
    text+='## Recent performance\n\nMAE averages each cycle equally; correct calls pool the eligible contests. Positive margins mean D. Probability metrics are blank for point-only references. Controls use the same fitted parameters: movement-links-off preserves polling correlations; local removes all forecast cross-state links. These are forecast ablations, not independent refits.\n\n'+performance(f).to_markdown(index=False)+'\n\n'
    text+='## Competitive cases\n\n'+performance(f,'competitive').to_markdown(index=False)+'\n\n'
    text+='## Selected regularization and history\n\n'+f['fits'].round(5).to_markdown(index=False)+'\n\n'
    text+='## Learned state uncertainty and bias\n\nCounts are admitted historical cycles, not poll samples. Missing outcome history arises from the existing outcome/rule restrictions; it is not proof a state has never held an election.\n\n'+pars.to_markdown(index=False)+'\n\n'
    text+='## Signed relationships with at least three shared historical cycles\n\nThese are fitted, regularized relationships; no confidence intervals for covariance parameters are claimed. Missing or weak overlap requires caution.\n\n'+pd.concat([pairs.nsmallest(8,'correlation'),pairs.nlargest(8,'correlation')]).round(4).to_markdown(index=False)+'\n\n'
    text+='## Current state and chamber forecasts\n\nD denotes Democratic caucus including mapped independents. Historical omitted contests retain incumbent completion outside accuracy scoring. Seat intervals are conditional on the covariance estimates and existing ballot/caucus approximations. Expected seats sum marginal probabilities; point seats count signs.\n\n'+states(f).to_markdown(index=False)+'\n\n'+seats.query('Cycle==2026').to_markdown(index=False)+'\n\n'
    text+='## No-poll stress test\n\n'+withholding(f).to_markdown(index=False)+'\n\n'
    text+='## Implementation checks\n\n'+pd.DataFrame([dict(Check=k,Passed=v) for k,v in a['checks'].items()]).to_markdown(index=False)+'\n\n'
    text+='## Remaining interpretation limits\n\nNo automatic model promotion. Review changes by cycle and state, not only an aggregate score. Check systematic errors of the unchanged historical mean, dependence on recent-cycle validation, sparse pair support, fixed measurement/bias scales and omitted covariance-estimation uncertainty. All publication timestamps are incomplete; replay uses field-end proxies. The broad historical exploration is retrospective, not a fresh untouched test. Features and tail changes remain deferred.\n'
    (lab/'BAYESIAN_REVISION2_RESULTS.md').write_text(text);(out/'BAYESIAN_REVISION2_RESULTS.md').write_text(text)
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes());v1.manifest(out)
    v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return f,paths,a
