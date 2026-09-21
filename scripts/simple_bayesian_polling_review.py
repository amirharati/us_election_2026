"""Tables, plots and consistency audit for the transparent polling notebook."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import simple_bayesian_polling as model


def load(out):
    model.verify(out)
    return {p.stem:pd.read_parquet(p) for p in Path(out).glob('*.parquet')}


def performance(f,group='all',period='recent_2016_2024'):
    q=f['metrics'].query('group==@group and period==@period').copy()
    q['Model']=q.model.map(model.LABELS)
    q['Calls correct']=q.correct.astype(str)+'/'+q.n.astype(str)
    q['95% coverage']=100*q.coverage95
    return q[['scenario','Model','Calls correct','mae_pp','brier','95% coverage']].round(3)


def cycle_scores(f):
    q=f['predictions'].query('cycle<2026');rows=[]
    for (s,y,m),g in q.groupby(['scenario','cycle','model']):
        rows.append(dict(Horizon=s,Cycle=y,Model=model.LABELS[m],Contests=len(g),
                         Correct=int(((g.prediction_pp>0)==(100*g.actual>0)).sum()),
                         MAE_pp=float((g.prediction_pp-100*g.actual).abs().mean())))
    return pd.DataFrame(rows).round(3)


def state_table(f,cycle=2026,scenario='matched_live'):
    q=f['predictions'].query('cycle==@cycle and scenario==@scenario')
    base=q.query("model=='linked'").copy().set_index('target_id')
    t=pd.DataFrame({'State':base.geography+np.where(base.special,' special',''),
                    'Poll samples':base.sample_count.astype(int),'Firms':base.firm_count.astype(int),
                    'Prior pp':100*base.prior,'Raw polls pp':base.q_pp,'New linked pp':base.prediction_pp,
                    'D win %':100*base.p_dem,'95% low pp':base.lo95_pp,'95% high pp':base.hi95_pp,
                    'Actual pp':100*base.actual})
    for key,label in [('local','New local pp'),('gaussian','Old Gaussian pp'),('student5','Old Student-t pp'),('nonbayes_bias','Corrected polls pp')]:
        t[label]=q.query('model==@key').set_index('target_id').prediction_pp
    return t.reset_index().round(2).sort_values(['State','target_id'])


def seat_comparison(f,out):
    settings=json.loads((Path(out)/'settings.json').read_text())
    path=next(p for p in settings['provenance']['paths'] if p.endswith('state_surprise/20260919T011532.132689Z/full_seat_ledger.parquet'))
    roster=pd.read_parquet(path).query("model=='polling'")
    rows=[]
    for (s,y,m),g in f['predictions'].groupby(['scenario','cycle','model']):
        r=roster[(roster.scenario==s)&(roster.cycle==y)]
        fixed=r[~r.target_id.isin(g.target_id)]
        point=int(fixed.caucus.eq('D').sum()+(g.prediction_pp>0).sum())
        row=dict(Horizon=s,Cycle=y,Model=model.LABELS[m],D=point,R=100-point,
                 Actual_D=int(r.actual_caucus.eq('D').sum()) if y<2026 else np.nan,
                 Completed_unmodeled_contests=int(fixed.contested.sum()))
        if m in ['linked','local']:
            seat=f['seats'].query('scenario==@s and cycle==@y and model==@m').iloc[0]
            row.update(Expected_D=seat.expected_D,D_low95=seat.D_lo95,D_high95=seat.D_hi95)
        rows.append(row)
    return pd.DataFrame(rows).round(2)


def withholding(f):
    rows=[]
    for (s,y,m),g in f['masked_predictions'].groupby(['scenario','cycle','model']):
        q=g[g.actual.notna()]
        rows.append(dict(Horizon=s,Cycle=y,Model=model.LABELS[m],Withheld_contests=len(g),
                         Mean_absolute_move_from_history_pp=float((g.prediction_pp-g.prior_pp).abs().mean()),
                         MAE_pp=float((q.prediction_pp-100*q.actual).abs().mean()) if len(q) else np.nan,
                         Correct=int(((q.prediction_pp>0)==(q.actual>0)).sum()) if len(q) else np.nan))
    return pd.DataFrame(rows).round(3)


def grid_summary(f,cycle=2026):
    g=f['grid_weights'].query("cycle==@cycle and model=='linked'");parts=[]
    for field in ['history_sd','poll_sd','rho']:
        p=g.groupby(['scenario','stage',field],dropna=False).weight.sum().reset_index().rename(columns={field:'Value'})
        p['Setting']=field;parts.append(p)
    return pd.concat(parts,ignore_index=True)[['scenario','stage','Setting','Value','weight']].round(5)


def plot(f,out):
    out=Path(out);paths=[]
    q=f['metrics'].query("period=='recent_2016_2024' and group=='all'")
    keys=['raw30','nonbayes_bias','gaussian','local','linked']
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for ax,scenario,title in zip(axes,['matched_live','oct31'],['Earlier saved cutoffs','October 31']):
        g=q[q.scenario==scenario].set_index('model').reindex(keys)
        ax.barh([model.LABELS[k] for k in keys],g.mae_pp,color=['#bbb','#777','#8495b9','#73a6be','#207797'])
        ax.invert_yaxis();ax.set(xlabel='MAE, percentage points (equal cycle weight)',title=title)
    fig.suptitle('2016–2024: new simple model versus frozen benchmarks');fig.tight_layout()
    p=out/'margin_error.png';fig.savefig(p,dpi=145);plt.close(fig);paths.append(p)
    q=f['predictions'].query("cycle==2026 and model=='linked'").sort_values('prediction_pp')
    fig,ax=plt.subplots(figsize=(9,11));y=np.arange(len(q))
    ax.hlines(y,q.lo95_pp,q.hi95_pp,color='#a8becb',lw=2,label='95% interval')
    ax.hlines(y,q.lo50_pp,q.hi50_pp,color='#246d8e',lw=5,label='50% interval')
    ax.scatter(q.prediction_pp,y,c=np.where(q.prediction_pp>0,'#2867ad','#b34743'),zorder=3,label='Posterior mean')
    ax.axvline(0,color='black',lw=.8);ax.set_yticks(y,q.geography+np.where(q.special,' special',''))
    ax.set(xlabel='Final Democratic minus Republican margin, pp',title='Simple linked model — frozen September 17, 2026 inputs')
    ax.legend(loc='lower right');fig.tight_layout();p=out/'current_ranges.png';fig.savefig(p,dpi=145);plt.close(fig);paths.append(p)
    d=f['current_decomposition'].set_index('target_id').loc[q.target_id]
    fig,ax=plt.subplots(figsize=(10,5))
    selected=d[d.geography.isin(['AK','MI','NH','TX','CO','WV'])]
    x=np.arange(len(selected));bottom=selected.prior_pp.to_numpy()
    ax.scatter(x,bottom,color='#666',marker='s',label='History center')
    ax.scatter(x,bottom+selected.own_poll_update_pp,color='#d89439',label='After own polls only')
    ax.scatter(x,selected.posterior_pp,color='#247492',label='After all states’ polls')
    for i,row in enumerate(selected.itertuples()):ax.plot([i,i],[row.prior_pp,row.posterior_pp],color='#999',alpha=.5)
    ax.axhline(0,color='black',lw=.8);ax.set_xticks(x,selected.geography);ax.set(ylabel='D−R margin, pp',title='Where the current prediction comes from');ax.legend();fig.tight_layout()
    p=out/'current_updates.png';fig.savefig(p,dpi=145);plt.close(fig);paths.append(p)
    fig,ax=plt.subplots(figsize=(9,4.5))
    for state,g in f['arrival_trace'].groupby('geography'):ax.plot(g.samples_seen,g.mean_pp,marker='.',label=state)
    ax.axhline(0,color='black',lw=.8);ax.set(xlabel='Samples revealed across all current races (availability order)',ylabel='Posterior D−R margin, pp',title='Fixed-cutoff replay — field-end proxy where release date is unknown')
    ax.legend();fig.tight_layout();p=out/'arrival_replay.png';fig.savefig(p,dpi=145);plt.close(fig);paths.append(p)
    fig,ax=plt.subplots(figsize=(8,4.5))
    for m in ['linked','local']:
        a=np.load(out/'draws'/f'matched_live_2026_{m}.npz');fixed=int(f['seats'].query('cycle==2026 and model==@m').fixed_D.iloc[0])
        count=fixed+(a['margins_pp']>0).sum(axis=1)
        ax.hist(count,bins=np.arange(34.5,65.5),density=True,histtype='step',lw=2,label=model.LABELS[m])
    ax.axvline(50.5,color='black',ls='--',lw=.8);ax.set(xlabel='Total Democratic-caucus seats',ylabel='Probability mass',title='2026 conditional full-chamber distribution');ax.legend();fig.tight_layout()
    p=out/'current_seats.png';fig.savefig(p,dpi=145);plt.close(fig);paths.append(p)
    fig,ax=plt.subplots(figsize=(7,4.5))
    for scenario in ['matched_live','oct31']:
        for name in ['linked','gaussian']:
            r=f['metrics'].query("period=='recent_2016_2024' and group=='all' and scenario==@scenario and model==@name").iloc[0]
            ax.plot([50,80,95],[100*r['coverage'+str(c)] for c in [50,80,95]],marker='o',label=f'{name}: {scenario}')
    ax.plot([40,100],[40,100],'k--',alpha=.5);ax.set(xlabel='Nominal coverage (%)',ylabel='Historical coverage (%)',title='Predictive interval check, 2016–2024');ax.legend(fontsize=8);fig.tight_layout()
    p=out/'coverage.png';fig.savefig(p,dpi=145);plt.close(fig);paths.append(p)
    return paths


def audit(f,out,lab):
    out,lab=Path(out),Path(lab)
    settings=json.loads((out/'settings.json').read_text());checks={}
    checks['all_source_hashes_unchanged']=all(model.sha(p)==s for p,s in settings['provenance']['paths'].items())
    checks['all_previous_notebooks_unchanged']=all(model.sha(lab/p)==s for p,s in settings['old_notebook_hashes'].items())
    checks['strict_earlier_cycle_training']=bool((f['fits'].training_max_cycle<f['fits'].cycle).all())
    checks['sample_counts_and_raw_polls_reproduced']=all(x['original_raw_averages_reproduced'] and x['original_sample_counts_reproduced'] for x in settings['provenance']['sample_checks'])
    w=f['samples'];checks['one_row_per_underlying_sample']=not w.duplicated(['scenario','target_id','sample_key']).any()
    checks['no_future_field_or_known_release']=bool((w.field_end<=w.cutoff).all() and (w.available_date<=w.cutoff).all())
    q=f['predictions'].query("model in ['linked','local']")
    checks['finite_predictions_and_ranges']=bool(np.isfinite(q[['prediction_pp','posterior_sd_pp','p_dem','lo95_pp','hi95_pp']]).all().all())
    checks['valid_probabilities_intervals']=bool(q.p_dem.between(0,1).all() and (q.lo95_pp<q.lo80_pp).all() and (q.lo80_pp<q.lo50_pp).all() and (q.lo50_pp<q.hi50_pp).all() and (q.hi50_pp<q.hi80_pp).all() and (q.hi80_pp<q.hi95_pp).all())
    grid=f['grid_weights'];group=['scenario','cycle','model','stage','target_id']
    checks['normalized_grid_weights']=bool(np.allclose(grid.groupby(group,dropna=False).weight.sum(),1))
    checks['current_decomposition_reconstructs_mean']=bool(np.allclose(f['current_decomposition'].eval('prior_pp+own_poll_update_pp+other_poll_update_pp'),f['current_decomposition'].posterior_pp))
    masked=f['masked_predictions'].query("model=='local'")
    checks['local_without_polls_retains_history_mean']=bool(np.allclose(masked.prediction_pp,masked.prior_pp))
    trace=f['arrival_trace'];last=trace[trace.samples_seen==trace.samples_seen.max()]
    current=q.query("cycle==2026 and model=='linked'").set_index('geography')
    checks['arrival_replay_reconstructs_final']=bool(np.allclose(last.mean_pp,current.loc[last.geography].prediction_pp))
    covchecks=[];drawchecks=[]
    for file in (out/'draws').glob('*.npz'):
        a=np.load(file);covchecks.append(np.linalg.eigvalsh(a['covariance_pp2']).min()>0)
        scenario,yr,mod=file.stem.rsplit('_',2);yr=int(yr)
        pp=q.query('scenario==@scenario and cycle==@yr and model==@mod').set_index('target_id').loc[a['target_ids']]
        # Monte Carlo cross-check, six standard errors plus tolerance.
        mcse=pp.posterior_sd_pp.to_numpy()/np.sqrt(len(a['margins_pp']))
        drawchecks.append(np.all(abs(a['margins_pp'].mean(axis=0)-pp.prediction_pp.to_numpy())<6*mcse+.02))
    checks['positive_definite_joint_covariances']=all(covchecks)
    checks['draws_match_exact_mixture_means']=all(drawchecks)
    result=dict(checks=checks,passed=all(checks.values()),new_models_rows=len(q),historical_folds=14,current_folds=1,
                max_probability_outside_margin_bounds=float(q.outside_margin_bounds_probability.max()),
                release_dates='All selected samples lack at least one documented release date. Replay is a proxy, not strict publication-time validation.',
                scope='Numerical integrity and provenance, not proof of predictive calibration or real-time vintage completeness.')
    if not result['passed']:raise AssertionError(result)
    model.json_write(out/'completion_audit.json',result)
    return result


def report(lab,out):
    lab,out=Path(lab),Path(out);f=load(out);paths=plot(f,out);checks=audit(f,out,lab)
    seats=seat_comparison(f,out);seats.to_parquet(out/'seat_comparison.parquet',index=False)
    cs=cycle_scores(f);cs.to_parquet(out/'cycle_scores.parquet',index=False)
    table=state_table(f)
    text='# Simple Bayesian polling restart — results\n\nNew notebook: `SIMPLE_BAYESIAN_POLLING.ipynb`. Model specification: `SIMPLE_BAYESIAN_POLLING_MODEL.md`. Existing notebooks remain unchanged. Inputs are frozen September 17, 2026; execution does not refresh sources.\n\n'
    text+='## What this experiment establishes\n\nExact finite-grid Bayesian updates work with sparse polling and a small declared common interstate relationship. The new model does not beat the existing corrected-polling point forecasts. The linked and local controls have similar historical errors; this is not evidence that a useful map of state-specific relationships has been learned. Interval coverage is closer to nominal, but larger intervals can improve coverage mechanically: retain Brier scores and the full coverage plot.\n\n'
    text+='The model integrates three uncertain global grid settings and up to50 regularized bias variables. No feature coefficients or learned state loadings are present. The 30-day poll decay, 8-year history decay and other fixed constants remain assumptions. The local control is a declared forecast ablation, not an independently refitted model.\n\n'
    text+='## Recent matched comparison\n\nMAE is mean absolute D−R margin error in percentage points, averaged equally across cycles. Correct calls pool eligible contests; positive margin means Democratic-caucus side. Brier is mean squared error of D-win probabilities; smaller is better. Blank probability metrics mean no comparable probability forecast exists.\n\n'+performance(f).to_markdown(index=False)+'\n\n'
    text+='## Competitive cases\n\nExisting past-only competitiveness membership is unchanged.\n\n'+performance(f,'competitive').to_markdown(index=False)+'\n\n'
    text+='## Training and cutoffs\n\nEach cycle provides a partially observed vector, not50 independent national cycles. State contest rows are listed separately. The earlier horizon uses saved context dates exactly; do not infer a fixed days-to-election offset from its name.\n\n'+f['fits'].to_markdown(index=False)+'\n\n'
    text+='## 2026 forecast\n\nPoint seats count the signs of posterior mean margins; expected seats sum probabilities (Monte Carlo estimate shown). These are different summaries, especially when many races are near zero. All counts include noncontested seats and explicitly labeled incumbent completions for any omitted historical contests. D means Democratic caucus, including mapped independents; scalar D/R and ballot assumptions remain.\n\n'+seats.query('Cycle==2026').to_markdown(index=False)+'\n\n'+table.to_markdown(index=False)+'\n\n'
    text+='## Grid uncertainty and boundary check\n\nCurrent posterior puts about68% mass at rho=.30, the largest permitted correlation. The history SD sits almost entirely on20pp; this coarse grid provides limited scale resolution. Do not interpret this as precisely estimating either quantity. Grid expansion and fixed-constant sensitivity are the next focused checks before promoting this model.\n\n'+grid_summary(f).to_markdown(index=False)+'\n\n'
    text+='## No-poll stress test\n\nWithhold all current-cycle polls in each tested state, including both contests if two seats are running. Local predictions retain their history means. Linked models may borrow from other states; these tests do not simulate the real reasons why polling is missing.\n\n'+withholding(f).to_markdown(index=False)+'\n\n'
    text+='## Arrival replay and provenance limits\n\nAt a fixed final cutoff, reveal eligible samples in availability order and recompute from the historical prior. All selected samples have unknown publication information, so field-end is an explicit proxy. This is an algebra/evidence-accounting demonstration, not an authentic historical publication-time backtest. More recent snapshots must be prepared and matched explicitly; this notebook is pinned to the existing dataset.\n\n'
    text+='## Checks and remaining work\n\n'+pd.DataFrame([{'Check':k,'Passed':v} for k,v in checks['checks'].items()]).to_markdown(index=False)+'\n\nHistorical/current forecasts, state-by-state actuals, posterior intervals, all-cycle seat counts and arrival replay are saved. Next: review this transparent baseline and its assumptions; then check grid/fixed-scale sensitivity. Add economic/approval surprise features only after that review. No model has been promoted.\n'
    (lab/'SIMPLE_BAYESIAN_POLLING_RESULTS.md').write_text(text);(out/'SIMPLE_BAYESIAN_POLLING_RESULTS.md').write_text(text)
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes());model.manifest(out)
    model.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=model.sha(out/'manifest.json')))
    return f,paths,checks
