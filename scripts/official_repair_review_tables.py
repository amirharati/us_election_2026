"""Audit and summarize the repaired-data comparison, with no outcome-based refits."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import simple_bayesian_polling as v1
import bayesian_revision2 as v2
import bayesian_state_penalty as v4
from official_repair_model_review import LABELS


def load(out):
    out=Path(out);v1.verify(out)
    return {p.stem:pd.read_parquet(p) for p in out.glob('*.parquet')}


def audit(out,lab,final_snapshot=None):
    out,lab=Path(out),Path(lab);f=load(out);s=json.loads((out/'settings.json').read_text());c={}
    snapshot=Path(s['dataset']['snapshot']);old=lab/'data/final/snapshots/20260918T040848.452707Z'
    from verify_final_dataset import verify
    from verify_accepted_data import verify as verify_accepted
    verify(snapshot);prov=json.loads((snapshot/'provenance.json').read_text());verify_accepted(Path(prov['accepted_snapshot']));c['dataset_and_official_sources_verified']=True
    c['previous_artifact_unchanged']=v1.verify(s['reference'])==s['reference_sha256']
    c['previous_notebooks_unchanged']=all(v1.sha(lab/n)==h for n,h in s['old_notebook_hashes'].items())
    before=pd.read_parquet(old/'tables/labels.parquet').set_index('target_id');after=pd.read_parquet(snapshot/'tables/labels.parquet').set_index('target_id')
    allowed=['2018-WV-regular-gen','2020-SD-regular-gen']
    pd.testing.assert_frame_equal(before.drop(allowed),after.drop(allowed),check_dtype=False)
    c['only_two_labels_changed']=True;c['official_labels_admitted']=bool(after.loc[allowed].diagnostic_eligible.all())
    c['future_labels_blank']=bool(after[after.cycle.eq(2026)][['dem_share','rep_share','dem_rep_margin']].isna().all().all())
    om=json.loads((old/'manifest.json').read_text());nm=json.loads((snapshot/'manifest.json').read_text())
    unmodified=['polls','answers','poll_inputs_reference','poll_inputs_observed','poll_metadata','poll_identity','national_contexts_reference','national_contexts_observed','feature_ledger','state_cycle_inputs_reference','seat_ledger','current_contests']
    c['poll_values_features_identities_and_seat_roster_unchanged']=all(om['files'][f'tables/{n}.parquet']['sha256']==nm['files'][f'tables/{n}.parquet']['sha256'] for n in unmodified)
    h=f['history'];orig=pd.read_parquet(Path(s['reference'])/'prepared_histories.parquet').query('prior_recipe=="current"')
    keys=['scenario','target_id'];a=h.set_index(keys);b=orig.set_index(keys)
    c['exactly_two_new_targets_per_horizon']=set(a.index)-set(b.index)=={(sc,t) for sc in ['matched_live','oct31'] for t in allowed}
    common=a.index.intersection(b.index)
    c['old_raw30_poll_aggregates_unchanged']=np.allclose(a.loc[common,'q_pp'],b.loc[common,'q_pp'],equal_nan=True)
    c['old_sample_counts_unchanged']=np.array_equal(a.loc[common,'sample_count'],b.loc[common,'sample_count'])
    c['no_future_poll_observations']=bool(f['samples'].available_date.le(f['samples'].cutoff).all())
    prepared=f['prepared_histories'];q=prepared[~prepared.prior_fallback]
    c['prior_mean_sources_past_only']=bool(q.prior_source_max_cycle.lt(q.cycle).all())
    d=f['fit_diagnostics'];c['component_fits_past_only']=bool(d.training_max_cycle.lt(d.cycle).all());c['em_converged']=bool(d.converged.all());c['positive_process_covariances']=bool(d.min_eigenvalue.gt(0).all())
    c['em_objective_monotone']=bool(d.min_objective_increment.ge(-1e-5).all())
    reuse=[]
    for row in d[d.reused].itertuples():
        recipe=row.recipe.removesuffix('_corrected');sc=row.scenario if row.scenario!='all' else 'matched_live'
        new=prepared[prepared.prior_recipe.eq(recipe)&prepared.scenario.eq(sc)]
        oldh=pd.read_parquet(Path(s['reference'])/'prepared_histories.parquet')
        oldh=oldh[oldh.prior_recipe.eq(recipe)&oldh.scenario.eq(sc)]
        a=v2.blocks(new,row.cycle,row.component);b=v2.blocks(oldh,row.cycle,row.component)
        reuse.append(all(np.array_equal(x,y,equal_nan=True) for x,y in zip(a[:4],b[:4])))
    c['reused_fits_have_identical_training_blocks']=all(reuse)
    for name in ['covariance_tuning','strength_tuning','local_tuning']:
        t=f[name];c[name+'_chronological']=bool((t.fit_max_cycle.lt(t.validation_cycle)&t.validation_cycle.lt(t.forecast_cycle)).all())
    t=f['half_life_tuning'];c['half_life_tuning_chronological']=bool((t.validation_cycle.lt(t.forecast_cycle)&t.max_prior_source_cycle.lt(t.validation_cycle)).all())
    t=f['feature_tuning'];c['feature_tuning_chronological']=bool((t.training_max_cycle.lt(t.validation_cycle)&t.validation_cycle.lt(t.cycle)).all())
    t=f['bias_tuning'];c['bias_tuning_chronological']=bool((t.training_max_cycle.lt(t.validation_cycle)&t.validation_cycle.lt(t.cycle)).all())
    p=f['predictions'];c['unique_forecasts']=not p.duplicated(['scenario','model','target_id']).any()
    c['identical_cases_all_models']=all(g.groupby('model').target_id.apply(frozenset).nunique()==1 for _,g in p.groupby(['scenario','cycle']))
    c['finite_predictions']=bool(np.isfinite(p.prediction_pp).all());bp=p[p.p_dem.notna()];c['valid_probabilities_and_intervals']=bool(bp.p_dem.between(0,1).all() and np.isfinite(bp[['posterior_sd_pp','lo95_pp','hi95_pp']]).all().all())
    reconstruct=[];draw_checks=[];profile_checks=[];strength_checks=[]
    for r in f['folds'].itertuples():
        ts=f['strength_tuning'];ts=ts[ts.scenario.eq(r.scenario)&ts.forecast_cycle.eq(r.cycle)&ts.family.eq(r.family)]
        import bayesian_prior_revision3 as v3
        strength_checks.append(v3.select_multiplier(ts.to_dict('records'))==(r.shared_multiplier,r.strength_status))
        local=f['local_tuning'];local=local[local.scenario.eq(r.scenario)&local.forecast_cycle.eq(r.cycle)&local.family.eq(r.family)]
        mult,prof=v4.shrink_state_scores(local,r.shared_multiplier,r.cycle)
        stored=f['state_penalties'];stored=stored[stored.scenario.eq(r.scenario)&stored.cycle.eq(r.cycle)&stored.family.eq(r.family)]
        profile_checks.append(np.allclose(prof.set_index('state').variance_multiplier,stored.set_index('state').variance_multiplier))
        z=np.load(out/r.movement_path);mov={n:z[n] for n in z.files};z=np.load(out/r.poll_path);poll={n:z[n] for n in z.files}
        if r.family=='corrected':mov['covariance']=mov['covariance']+mov['bias_covariance']
        for mode in ['fixed','shared','state']:
            model=r.family+'_'+mode;test=p[p.model.eq(model)&p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)].sort_values('target_id').reset_index(drop=True)
            a=np.ones(50) if mode=='fixed' else np.full(50,r.shared_multiplier) if mode=='shared' else mult
            pred,cov,meta=v4.state_predict(test,mov,poll,a)
            reconstruct.append(np.allclose(pred.prediction_pp,test.prediction_pp,atol=1e-10) and np.allclose(pred.p_dem,test.p_dem,atol=1e-12))
            draws=np.load(out/'draws'/f'{r.scenario}_{r.cycle}_{model}.npz')
            se=np.sqrt(np.diag(cov)/len(draws['margins_pp']));draw_checks.append(bool(np.max(abs(draws['margins_pp'].mean(axis=0)-test.prediction_pp)/se)<6))
            np.linalg.cholesky(cov)
    c['shared_strength_reconstructed']=all(strength_checks);c['state_strength_reconstructed']=all(profile_checks)
    c['all_prior_family_forecasts_reconstructed']=all(reconstruct);c['joint_draw_means_within_6mc_se']=all(draw_checks)
    mapping={**{f'{fam}_fixed':f'v3_{fam}_fixed' for fam in ['current','latest','decay']},**{f'{fam}_shared':f'v3_{fam}_tuned' for fam in ['current','latest','decay']},**{f'{fam}_state':f'v4_{fam}_state' for fam in ['current','latest','decay']},**{f'{fam}_{mode}':f'v5_{fam}_{mode}' for fam in ['fast','corrected'] for mode in ['fixed','shared','state']},'bias':'nonbayes_bias','bias__momentum':'nonbayes_momentum'}
    previous=pd.read_parquet(Path(s['reference'])/'predictions.parquet');pairs=[]
    for new,oldname in mapping.items():
        n=p[p.model.eq(new)];o=previous[previous.model.eq(oldname)]
        pair=n.merge(o,on=['scenario','target_id'],suffixes=('_new','_old'),validate='one_to_one')
        pair['change_pp']=pair.prediction_pp_new-pair.prediction_pp_old;pair['review_model']=new;pairs.append(pair)
    pairs=pd.concat(pairs,ignore_index=True);pairs.to_parquet(out/'paired_changes.parquet',index=False)
    prechange=float(pairs[pairs.cycle_new.lt(2018)].change_pp.abs().max())
    c['all_pre_2018_predictions_unchanged_within_1e_6_pp']=prechange<1e-6
    if final_snapshot is not None:
        final_snapshot=Path(final_snapshot);verify(final_snapshot);fm=json.loads((final_snapshot/'manifest.json').read_text())
        used=['contest_inputs_reference','labels','polls','poll_quality','poll_identity','poll_metadata']
        c['final_dataset_model_inputs_identical']=all(nm['files'][f'tables/{n}.parquet']['sha256']==fm['files'][f'tables/{n}.parquet']['sha256'] for n in used)
        av1=pd.read_parquet(snapshot/'tables/poll_availability.parquet');av2=pd.read_parquet(final_snapshot/'tables/poll_availability.parquet')
        pd.testing.assert_frame_equal(av1[['observation_id','documented_release_date']],av2[['observation_id','documented_release_date']])
        c['final_dataset_release_inputs_identical']=True
        prov=json.loads((final_snapshot/'provenance.json').read_text());cfg=json.loads((Path(prov['accepted_snapshot'])/'config.json').read_text())
        polls=pd.read_parquet(final_snapshot/'tables/polls.parquet');origins=polls.set_index('observation_id').origin_bundle
        dates={n:pd.Timestamp(json.loads((lab/cfg['snapshots'][n]['path']/'manifest.json').read_text())['retrieved_at']).tz_localize(None).normalize() for n in ['reviewed','refresh']}
        expected=av2.observation_id.map(origins).map(dates)
        c['poll_receipt_dates_preserved']=bool(av2.snapshot_observed_date.eq(expected).all())
        v1.json_write(out/'final_dataset_equivalence.json',dict(model_build_dataset=s['dataset'],final_dataset=str(final_snapshot),final_manifest_sha256=v1.sha(final_snapshot/'manifest.json'),identical_model_inputs=bool(c['final_dataset_model_inputs_identical']),difference='Final source-receipt metadata fix and explicit official-result audit table; modeled inputs and release-date field equal'))
    result=dict(passed=all(c.values()),checks=c,models=int(p.model.nunique()),forecasts=len(p),new_components=int((~d.reused).sum()),reused_components=int(d.reused.sum()),maximum_pre_2018_prediction_change_pp=prechange,maximum_outside_bounds_probability=float(bp.outside_margin_bounds_probability.max()))
    v1.json_write(out/'completion_audit.json',result)
    if not result['passed']:raise ValueError([k for k,v in c.items() if not v])
    return result


def cycle_scores(p):
    rows=[]
    for (s,y,m),g in p[p.actual.notna()].groupby(['scenario','cycle','model']):
        errors=g.prediction_pp-100*g.actual
        rows.append(dict(scenario=s,cycle=y,model=m,n=len(g),correct=int(((g.prediction_pp>0)==(g.actual>0)).sum()),mae_pp=float(errors.abs().mean()),bias_pp=float(errors.mean()),polled=int(g.n_samples.gt(0).sum())))
    return pd.DataFrame(rows)


def seat_table(f):
    s=f['seats'].copy();p=f['predictions'];roster=f['full_seat_ledger'];rows=[]
    for (sc,y,m),g in p[p.p_dem.isna()].groupby(['scenario','cycle','model']):
        rr=roster[roster.scenario.eq(sc)&roster.cycle.eq(y)];fixed=rr[~rr.target_id.isin(g.target_id)]
        assert len(fixed)+len(g)==100
        d=int((fixed.caucus=='D').sum()+(g.prediction_pp>0).sum())
        rows.append(dict(scenario=sc,cycle=y,model=m,point_D=d,point_R=100-d,actual_D=int((rr.actual_caucus=='D').sum()) if y<2026 else np.nan,unmodeled_contested=int(fixed.contested.sum())))
    return pd.concat([s,pd.DataFrame(rows)],ignore_index=True)


def state_table(p,year=2026,scenario='matched_live'):
    q=p[p.cycle.eq(year)&p.scenario.eq(scenario)]
    index=q[q.model.eq('decay_state')].set_index('target_id')
    t=index[['geography','actual','q_pp','n_samples']].copy();t['actual_pp']=100*t.pop('actual')
    for m in ['prior','polling','bias','bias__momentum','latest_fixed','latest_state','decay_state','fast_state','corrected_state']:
        g=q[q.model.eq(m)].set_index('target_id');t[m+'_pp']=g.prediction_pp
    for name in ['p_dem','lo70_pp','hi70_pp','lo95_pp','hi95_pp']:t['decay_state_'+name]=index[name]
    return t.reset_index().sort_values('geography')


def report(out,lab):
    out,lab=Path(out),Path(lab);f=load(out);p=f['predictions'];m=f['metrics']
    cycles=cycle_scores(p);seats=seat_table(f);states=state_table(p)
    for n,t in [('cycle_scores',cycles),('seat_comparison',seats),('current_states',states)]:t.to_parquet(out/(n+'.parquet'),index=False)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    chosen=['prior','polling','bias','bias__momentum','latest_fixed','latest_state','decay_state','fast_state','corrected_state']
    fig,axs=plt.subplots(1,2,figsize=(14,5))
    for ax,sc in zip(axs,['matched_live','oct31']):
        q=m[(m.period=='recent_2016_2024')&(m.group=='all')&(m.scenario==sc)&m.model.isin(chosen)].set_index('model').reindex(chosen)
        ax.barh(np.arange(len(q)),q.mae_pp,color=['#777777']*4+['#397d9a']*5);ax.set_yticks(np.arange(len(q)),q.index);ax.invert_yaxis();ax.set(title=sc,xlabel='Equal-cycle margin MAE (percentage points)')
    fig.tight_layout();fig.savefig(out/'recent_model_comparison.png',dpi=145);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,5))
    for model in ['bias','bias__momentum','latest_state','decay_state','corrected_state']:
        q=cycles[(cycles.scenario=='oct31')&(cycles.model==model)];ax.plot(q.cycle,q.mae_pp,marker='o',label=model)
    ax.set(xlabel='Held-out cycle',ylabel='Margin MAE (pp)',title='October forecasts, repaired data');ax.legend();fig.tight_layout();fig.savefig(out/'by_cycle_mae.png',dpi=145);plt.close(fig)
    text='# Official-result repair and full model review\n\n'
    text+='All current comparisons use repaired historical outcomes and the same frozen September 17, 2026 polling/feature data. No current polling download occurred. Positive margins favor Democrats; errors and MAE are percentage points. Each historical cycle is predicted using earlier cycles only, with tuning on earlier validation cycles. Summary MAE gives each cycle equal weight; winner calls pool contests. National output is the full Senate seat count, not a national popular-vote forecast.\n\n'
    text+='## Data repair\n\nWV2018 is now admitted with D290,510/R271,113/other24,411 (all-vote margin D+3.3099pp; changed by+0.06135pp). SD2020 is admitted with D143,987/R276,232 (R+31.4705pp; unchanged numeric margin). Poll errors and dispositions were rebuilt while preserving poll values, deduplication, population and date rules. Official PDFs are archived and checksummed. Unrelated special/unopposed/candidate restrictions remain. Sources: [FEC2018](https://www.fec.gov/documents/2705/federalelections2018.pdf), [FEC2020](https://www.fec.gov/resources/cms-content/documents/federalelections2020.pdf).\n\n'
    text+='## Model definitions\n\n- `prior`: half latest eligible state result, half older state mean.\n- `polling`: equal firm contributions before poll-age decay; poll half-life/prior blending selected on the preceding cycle.\n- `bias`: polling plus state polling-error correction, last five calendar cycles, eight-year decay, shrunk toward shared bias with preceding-cycle tuning.\n- `bias__momentum` and other `__` variants: shared feature correction on prequential offsets, training-only score scaling/missing-value treatment, eight-year history decay, preceding-cycle ridge tuning.\n- Bayesian `current`, `latest`, `decay`, `fast`: historical prior centers, respectively half-latest/half-history, latest result, selected4/8/16year decay, selected2/4/8/16year decay.\n- Bayesian `corrected`: fast prior plus shared/shrunk-state prior-mean-error correction with its posterior uncertainty.\n- `fixed`, `shared`, `state`: prior variance strength fixed1, tuned shared, or recent state-specific strengths shrunk to shared. All use the same 30-day firm-balanced polls, learned polling bias/error covariance and outcome covariance. `local` turns both interstate covariance links off; `movement_diagonal` turns outcome links off. These link ablations share the fitted marginal components.\n\n'
    for period in ['recent_2016_2024','all_2012_2024']:
        for group in ['all','competitive','noncompetitive']:
            q=m[(m.period==period)&(m.group==group)].copy();q['correct_over_n']=q.correct.astype(str)+'/'+q.n.astype(str)
            text+=f'## {period}: {group}\n\n'+q[['scenario','model','correct_over_n','mae_pp','brier','coverage95','mean95_width_pp']].round(4).to_markdown(index=False)+'\n\n'
    text+='## By cycle\n\n'+cycles[cycles.model.isin(chosen)].round(3).to_markdown(index=False)+'\n\n'
    text+='## Current states\n\n'+states.round(3).to_markdown(index=False)+'\n\n'
    text+='## Full chamber totals\n\nD includes mapped Democratic-caucusing independents. Unmodeled contests retain the existing, explicit incumbent-caucus completion rule and are excluded from modeled accuracy. Expected seats and joint intervals exist only for Bayesian models; point models have no fabricated probability. Current ballot/RCV/runoff/independent limitations remain.\n\n'+seats[seats.model.isin(chosen)].round(3).to_markdown(index=False)+'\n\n'
    text+='## Limitations and selection\n\nThese are repeated exploratory chronological tests on previously examined elections, not an untouched test set. A few cycles are the independent temporal evidence; 140 state contests are not 140 independent environments. No horizon-dependent switching chosen from held-out outcomes is presented as one model. A best margin model can differ from a best winner-call model. Covariance/hyperparameter-selection uncertainty is omitted from the empirical-Bayes intervals; correction-coefficient uncertainty is integrated in the corrected family. Very old Gaussian/Student-t and broader feature experiments remain archived on their original dataset; they were not silently relabeled as repaired-data reruns. No automatic promotion or new model complexity is introduced.\n'
    (lab/'OFFICIAL_REPAIR_MODEL_REVIEW_RESULTS.md').write_text(text);(out/'OFFICIAL_REPAIR_MODEL_REVIEW_RESULTS.md').write_text(text)
    v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return f
