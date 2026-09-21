"""Supported, portable API for the final election lab.

Research numerical helpers live in scripts/. This module supplies explicit
inputs and paths; their old experiment builders are not used by this release.
"""
from pathlib import Path
from datetime import date, datetime, timezone
import hashlib
import json
import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import norm

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'scripts'))
import simple_bayesian_polling as gaussian
import simple_national_model as national
import signed_state_factor as signed
import national_feature_prior as features
import national_tails_waves as chamber
from mean_only_polling_blend import rescore, translate_draws
from mean_only_blend_weights import blend_mean
from calibrate_margin_uncertainty import fit_scale

ASSETS = ROOT/'assets'
FROZEN = ROOT/'data/compact/frozen'
WEIGHTS = [.05, .10, .20, .30, .40, .50, .70]
SEED = 197139
DRAWS = 30000


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def write_json(path, value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value,indent=2,default=str,allow_nan=False)+'\n')
    temporary.replace(path)


def new_run(kind):
    p=ROOT/'cache/runs'/kind/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    p.mkdir(parents=True);return p


def finish(out, metadata, publish=True):
    write_json(out/'run.json',metadata)
    manifest={str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='manifest.json'}
    write_json(out/'manifest.json',manifest)
    write_json(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=sha(out/'manifest.json')))
    if publish:
        publish_run(out)
    return out


def publish_run(out):
    from output_publication import publish
    publish(ROOT, out)


def verify_run(path):
    path=Path(path)
    for rel,h in json.loads((path/'manifest.json').read_text()).items():
        p=(path/rel).resolve()
        if not p.is_relative_to(path.resolve()) or sha(p)!=h:raise ValueError('Invalid artifact: '+rel)
    return path


def latest_run(kind):
    from output_publication import result_path
    root=ROOT/'cache/runs'/kind
    if (root/'latest.json').exists():
        pointer=json.loads((root/'latest.json').read_text());p=root/pointer['artifact']
        if sha(p/'manifest.json')!=pointer['manifest_sha256']:raise ValueError('Changed run manifest')
        return verify_run(p)
    return verify_run(result_path(ROOT,kind))


def dataset_for_run(metadata):
    """Resolve exact inputs locally or from the committed compact current bundle."""
    requested=(ROOT/metadata['dataset']).resolve()
    if not requested.is_relative_to(ROOT):raise ValueError('Dataset outside project')
    for path in [requested,ROOT/'data/compact/current',FROZEN]:
        if (path/'manifest.json').exists() and sha(path/'manifest.json')==metadata['dataset_manifest_sha256']:
            return path
    raise ValueError('Exact inputs for this older run are unavailable; reports remain readable. Run live to refresh current inputs.')


def load_poll(scenario, year):
    a=dict(np.load(ASSETS/'poll'/f'{scenario}_{year}.npz'))
    return national.fixed_common(a['training_values'],a['training_noise'],a['training_weights'],a['budget'],0.,9.)


def scored(pred, model):
    p=pred.copy();p['model']=model
    p['margin_pp']=p.prediction_pp;p['sigma_pp']=p.posterior_sd_pp;p['actual_pp']=100*p.actual
    # For Student output keep sampled marginal probabilities and quantiles.
    if model!='Student-t research helper':p=rescore(p)
    else:
        valid=p.actual_pp.notna();p['absolute_error_pp']=(p.margin_pp-p.actual_pp).abs()
        p['correct']=p.margin_pp.gt(0).eq(p.actual_pp.gt(0)).astype(float).where(valid)
        p['brier']=((p.p_dem-p.actual_pp.gt(0))**2).where(valid)
        p['coverage70']=((p.actual_pp>=p.lo70_pp)&(p.actual_pp<=p.hi70_pp)).astype(float).where(valid)
        p['width70_pp']=p.hi70_pp-p.lo70_pp
    return p


def summarize(pred):
    hist=pred[pred.actual_pp.notna()]
    metrics=['absolute_error_pp','brier','coverage70','width70_pp']
    cycle=hist.groupby(['scenario','cycle','model'])[metrics].mean().reset_index()
    cycle=cycle.merge(hist.groupby(['scenario','cycle','model']).agg(n=('target_id','size'),correct=('correct','sum')).reset_index())
    rows=[]
    for start in [2012,2016,2018]:
        for (sc,model),g in cycle[cycle.cycle.ge(start)].groupby(['scenario','model']):
            rows.append(dict(first_cycle=start,scenario=sc,model=model,cycles=len(g),n=int(g.n.sum()),correct=int(g.correct.sum()),
                             probability_cycles=int(g.brier.notna().sum()),**g[metrics].mean().to_dict()))
    return cycle,pd.DataFrame(rows)


def seat_row(q, draws, model, reference, method='Bayesian joint covariance'):
    fixed=int(reference.fixed_D);counts=fixed+(draws>0).sum(axis=1)
    freq=np.bincount(counts,minlength=101);lo,hi=np.quantile(counts,[.15,.85],method='inverted_cdf')
    point=fixed+int(q.margin_pp.gt(0).sum());expected=fixed+q.p_dem.sum()
    return dict(scenario=q.scenario.iloc[0],cycle=int(q.cycle.iloc[0]),model=model,point_D=point,point_R=100-point,
                expected_D=float(expected),expected_R=float(100-expected),p_D_control=float((counts>=51).mean()),
                D_lo70=int(lo),D_hi70=int(hi),fixed_D=fixed,unmodeled_contested=int(reference.unmodeled_contested),
                actual_D=float(reference.actual_D),method=method),freq


def reproduce(include_student=True, weights=WEIGHTS, plain_weights=(.2,.5,.7), output_kind='reproduction'):
    """Recompute Gaussian posteriors, non-Bayesian corrections and mean blends.

Uses bundled historical training fits, never the parent lab. Student historical
MCMC output is verified and loaded; rerun it explicitly with rerun_student().
"""
    from state_poll_bias import fit_bias
    folds=pd.read_parquet(ASSETS/'main/folds.parquet')
    saved=pd.read_parquet(ASSETS/'main/predictions.parquet')
    reference=pd.read_parquet(ASSETS/'main/seats.parquet')
    nb=pd.read_parquet(ASSETS/'reference_blends/predictions.parquet').query('model == "Bayesian"')
    hist=pd.read_parquet(ASSETS/'training/history.parquet')
    out=new_run(output_kind);(out/'forecasts').mkdir()
    predictions=[];seats=[];checks=[]
    for fold in folds.itertuples():
        sc,year=fold.scenario,int(fold.cycle)
        q=saved[saved.scenario.eq(sc)&saved.cycle.eq(year)].sort_values('target_id').reset_index(drop=True)
        fit=dict(np.load(ASSETS/'main'/fold.fit_path));fit['a']=float(fit['a'])
        p,_,arrays=signed.predict(q,fit,load_poll(sc,year),fit['loading'],fold.lambda_value)
        original=np.load(ASSETS/'main'/fold.forecast_path)
        np.testing.assert_allclose(p.prediction_pp,q.prediction_pp,atol=1e-10)
        np.testing.assert_allclose(arrays['covariance'],original['covariance'],atol=1e-10)
        prior=hist[hist.scenario.eq(sc)&hist.cycle.lt(year)]
        current=hist[hist.scenario.eq(sc)&hist.cycle.eq(year)].set_index('target_id').loc[q.target_id].reset_index()
        corrected,_,_=fit_bias(prior,current,5,8.,'state',float(current.bias_shrinkage.iloc[0]))
        np.testing.assert_allclose(corrected,current.bias_prediction,atol=1e-12)
        pp=scored(p,'Bayesian');predictions.append(pp)
        seed=SEED+year+10000*(sc=='oct31')
        draws=arrays['mean']+np.random.default_rng(seed).standard_normal((DRAWS,len(q)))@np.linalg.cholesky(arrays['covariance']).T
        ref=reference[reference.scenario.eq(sc)&reference.cycle.eq(year)].iloc[0]
        row,freq=seat_row(pp,draws,'Bayesian',ref);seats.append(row)
        assert np.array_equal(freq,original['seat_count_frequency'])
        np.savez_compressed(out/'forecasts'/f'{sc}_{year}.npz',**arrays,target_ids=q.target_id.to_numpy(str),seed=seed,draws=DRAWS)
        for label,means,grid in [('Corrected',100*corrected,weights),('Plain',100*current.poll_baseline.to_numpy(),plain_weights)]:
            for w in grid:
                name=f'{label} {100*w:g}%';bp=pp.copy()
                bp['margin_pp']=blend_mean(pp.margin_pp,means,w);bp['model']=name
                bp['prediction_pp']=bp.margin_pp;bp['prediction']=bp.margin_pp/100;bp['median_pp']=bp.margin_pp
                bp=rescore(bp);bp['lo95_pp']=bp.margin_pp-norm.ppf(.975)*bp.sigma_pp;bp['hi95_pp']=bp.margin_pp+norm.ppf(.975)*bp.sigma_pp
                predictions.append(bp)
                shifted=translate_draws(draws,pp.margin_pp,bp.margin_pp)
                np.testing.assert_allclose(shifted-bp.margin_pp.to_numpy(),draws-pp.margin_pp.to_numpy(),atol=1e-12)
                row,_=seat_row(bp,shifted,name,ref);seats.append(row)
        # This helper's own probabilities use earlier-cycle pooled residual RMS.
        scale=fit_scale(nb,sc,year,'nonbayesian_pp')
        npred=pp.copy();npred['margin_pp']=100*corrected;npred['prediction_pp']=npred.margin_pp;npred['prediction']=corrected
        npred['model']='Non-Bayesian corrected';npred['sigma_pp']=scale['sigma_pp'];npred['posterior_sd_pp']=npred.sigma_pp
        npred=rescore(npred);npred['median_pp']=npred.margin_pp;npred['lo95_pp']=npred.margin_pp-norm.ppf(.975)*npred.sigma_pp;npred['hi95_pp']=npred.margin_pp+norm.ppf(.975)*npred.sigma_pp
        predictions.append(npred)
        if npred.sigma_pp.notna().all():
            from plain_polling_blend import independent_seats
            ss,_=independent_seats(npred.p_dem.to_numpy(),int(ref.fixed_D))
            point=int(ref.fixed_D)+int(npred.margin_pp.gt(0).sum())
            seats.append(dict(scenario=sc,cycle=year,model='Non-Bayesian corrected',point_D=point,point_R=100-point,
                              actual_D=ref.actual_D,fixed_D=ref.fixed_D,unmodeled_contested=ref.unmodeled_contested,
                              method='Independent-state approximation; helper only',**ss))
        checks.append(dict(scenario=sc,cycle=year,gaussian_reproduced=True,nonbayesian_reproduced=True,covariance_preserved=True))
    if include_student:
        p=pd.read_parquet(ASSETS/'student/predictions.parquet');predictions.append(scored(p,'Student-t research helper'))
        s=pd.read_parquet(ASSETS/'student/seats.parquet').copy()
        s['model']='Student-t research helper';s['expected_D']=s.expected_D_exact;s['expected_R']=100-s.expected_D
        s['point_R']=100-s.point_D;s['p_D_control']=s.p_D_at_least_51;s['method']='Research MCMC; separate earlier architecture'
        seats.extend(s.to_dict('records'))
    predictions=pd.concat(predictions,ignore_index=True);seats=pd.DataFrame(seats)
    cycle,summary=summarize(predictions)
    for name,table in dict(predictions=predictions,seats=seats,cycle_scores=cycle,summary=summary).items():table.to_parquet(out/(name+'.parquet'),index=False)
    return finish(out,dict(kind='frozen_reproduction',data_as_of='2026-09-17',main='repaired_both__selected',weights=list(weights),plain_weights=list(plain_weights),
                          checks=checks,student='verified saved research MCMC output' if include_student else 'omitted',trained_on='earlier cycles only',new_tuning=False))


def refit_main(scenario='matched_live', year=2026):
    """Refit the main model's empirical-Bayes stages from saved training blocks.

The chosen hyperparameters are frozen; their earlier-fold selection surfaces
are bundled. This refits movement variance, feature coefficients, and loadings.
"""
    import bayesian_revision2 as covariance
    import bayesian_prior_revision3 as prior_recipe
    import prior_center_repair as centers
    folds=pd.read_parquet(ASSETS/'main/folds.parquet')
    r=folds[folds.scenario.eq(scenario)&folds.cycle.eq(year)].iloc[0]
    f=dict(np.load(ASSETS/'main'/r.fit_path))
    if int(f['years'].max())>=year:raise ValueError('Future training cycle')
    h=pd.read_parquet(ASSETS/'training/history.parquet')
    histories=pd.concat([prior_recipe.construct_history(h,recipe)[0] for recipe in ['decay4','latest']],ignore_index=True)
    repaired,_=centers.histories(histories)
    hh=repaired['decay4_centered'];hh=hh[hh.scenario.eq(scenario)]
    x,noise,w,years,_=covariance.blocks(hh,year,'movement')
    for actual,expected in [(x,f['training_values']),(noise,f['training_noise']),(w,f['training_weights']),(years,f['years'])]:
        np.testing.assert_allclose(actual,expected,equal_nan=True)
    cal=pd.read_parquet(ASSETS/'training/calendars.parquet')
    design,X,z,_,_,_=features.prepare_design(cal[cal.scenario.eq(scenario)],years,w,year)
    ids=[design.active.index(t) for t in f['terms']]
    np.testing.assert_allclose(X[:,ids],f['X']);np.testing.assert_allclose(z[ids],f['z'])
    surface=pd.read_parquet(ASSETS/'selection/scale_surface.parquet')
    surface=surface[surface.scenario.eq(scenario)&surface.recipe.eq('decay4_centered')&surface.family.eq('both')]
    _,multipliers,_=centers.choose_scales(surface,year)
    np.testing.assert_allclose(multipliers,f['multipliers'])
    selection_checks=verify_selection(scenario,year)
    covariance.CONFIG['max_iterations']=16000
    raw=covariance.fit_covariance(f['training_values'],f['training_noise'],f['training_weights'],8.)
    budget=np.diag(raw['covariance'])*f['multipliers']
    np.testing.assert_allclose(budget,f['budget'],rtol=1e-7,atol=1e-7)
    learned=features.fit_feature(f['training_values'],f['training_noise'],f['training_weights'],budget,f['X'],float(f['tau']))
    np.testing.assert_allclose(learned['beta_mean'],f['beta_mean'],rtol=1e-6,atol=1e-6)
    loading=signed.fit_loading(f['training_values'],f['training_noise'],f['training_weights'],budget,learned['a'],f['X']@learned['beta_mean'])
    np.testing.assert_allclose(loading['b'],f['loading'],rtol=1e-4,atol=1e-4)
    pf=np.load(ASSETS/'poll'/f'{scenario}_{year}.npz')
    choices=pd.read_parquet(ASSETS/'selection/poll_variance_choices.parquet')
    choice=choices[choices.scenario.eq(scenario)&choices.cycle.eq(year)].iloc[0]
    kappa=float(choice.source_poll.rsplit('_k',1)[1].removesuffix('.npz'))
    poll_fit=covariance.fit_covariance(pf['training_values'],pf['training_noise'],pf['training_weights'],kappa,9.)
    np.testing.assert_allclose(np.diag(poll_fit['covariance'])+4.,pf['budget'],rtol=1e-6,atol=1e-6)
    out=new_run('training');np.savez_compressed(out/'fit.npz',budget=budget,beta_mean=learned['beta_mean'],beta_covariance=learned['beta_covariance'],a=learned['a'],loading=loading['b'])
    return finish(out,dict(scenario=scenario,cycle=year,training_cycles=f['years'].tolist(),tau=float(f['tau']),signed_lambda=float(r.lambda_value),
                          movement_kappa=8.,poll_kappa=kappa,movement_iterations=raw['iterations'],passed=True,
                          selection_checks=selection_checks,selection='Reproduced earlier-cycle choices; not reselected on this test outcome'))


def verify_selection(scenario,year):
    """Recompute tau and signed-factor choices from bundled earlier-fold scores."""
    import poll_timing_student as timing
    candidates=pd.read_parquet(ASSETS/'selection/feature_candidate_seats.parquet')
    order=[f'both_tau{t}' for t in features.TAUS]
    tau_name,years,_=timing.choose(candidates[candidates.scenario.eq(scenario)],year,order)
    folds=pd.read_parquet(ASSETS/'main/folds.parquet')
    row=folds[folds.scenario.eq(scenario)&folds.cycle.eq(year)].iloc[0]
    fit=np.load(ASSETS/'main'/row.fit_path)
    assert float(tau_name.removeprefix('both_tau'))==float(fit['tau'])
    scores=pd.read_parquet(ASSETS/'selection/signed_candidate_scores.parquet')
    scores=scores[scores.scenario.eq(scenario)&scores.cycle.lt(year)&scores.actual.notna()]
    years=sorted(scores.cycle.unique())[-3:]
    names=[f'repaired_both__lambda{x:g}' for x in signed.LAMBDAS]
    loss=scores[scores.cycle.isin(years)].groupby(['model','cycle']).wis_pp.mean().groupby('model').mean()
    chosen=min(names,key=lambda n:(loss[n],names.index(n))) if len(years)==3 else names[0]
    assert chosen==row.selected_model
    return dict(feature_tau=tau_name,signed_factor=chosen,validation_cycles=list(map(int,years)))


def rerun_student(scenario='matched_live', year=2026, test=None, feature_z=None):
    """Run the actual research Student-t sampler, including convergence checks."""
    import combined_student_model as student
    folds=pd.read_parquet(ASSETS/'student/folds.parquet')
    r=folds[folds.scenario.eq(scenario)&folds.cycle.eq(year)].iloc[0]
    saved=pd.read_parquet(ASSETS/'student/base_predictions.parquet')
    q=saved[saved.scenario.eq(scenario)&saved.cycle.eq(year)].sort_values('target_id').reset_index(drop=True) if test is None else test
    f=dict(np.load(ASSETS/'student_base'/r.source_fit_path));f['a']=float(f['a'])
    if feature_z is not None:f['z']=feature_z
    _,_,_,prior=features.predict(q,f['budget'],load_poll(scenario,year),f,f['z'])
    args=student.inputs(q,f,prior,load_poll(scenario,year),1)
    p,d=student.student_predict(q,args,5,int(r.seed),warmup=int(r.warmup),draws=int(r.draws_per_chain),chains=int(r.chains))
    return scored(p,'Student-t research helper'),d


def display_tables(path):
    path=verify_run(path)
    pred=pd.read_parquet(path/'predictions.parquet');seats=pd.read_parquet(path/'seats.parquet')
    now=pred[pred.cycle.eq(2026)].copy();now['State']=now.geography+np.where(now.special,' (special)','')
    now['P(D) %']=100*now.p_dem
    return dict(summary=pd.read_parquet(path/'summary.parquet') if (path/'summary.parquet').exists() else pd.DataFrame(),
                seats=seats[seats.cycle.eq(2026)],margins=now.pivot(index='State',columns='model',values='margin_pp'),
                probabilities=now.pivot(index='State',columns='model',values='P(D) %'))


def weight_experiment():
    """One fixed grid; no selecting weights on the cycle being scored."""
    return reproduce(include_student=False,weights=[.05,.10,.20,.30,.40,.50],plain_weights=(),output_kind='blend_weights')


def prepare_live_evidence(snapshot, as_of=None, feature_mode='dated'):
    """Prepare one cutoff without inference; keep historical fits fixed.

    Backdated inputs are a latest-vintage reconstruction, not archived forecasts.
    Known poll release dates are screened; missing releases use field-end dates.
    Features retain the reference-date convention used by the live models.
    """
    from load_final_dataset import open_dataset
    from contextual_baselines import make_store, calendar_inputs
    from simple_baselines import prepare_inputs, poll_predict
    from state_poll_bias import fit_bias
    data=open_dataset(snapshot)
    if pd.Timestamp(data.policy['as_of']).year!=2026:raise ValueError('This release forecasts2026 only')
    snapshot_as_of=data.policy['as_of']
    cutoff=pd.Timestamp(as_of or snapshot_as_of).normalize()
    if cutoff.year!=2026 or cutoff>pd.Timestamp(snapshot_as_of):
        raise ValueError('Cutoff must be in2026 and no later than the snapshot')
    if feature_mode not in {'dated','fixed_latest'}:raise ValueError('Unknown feature mode')
    # Local policy override only: never mutate the pinned dataset on disk.
    data.policy={**data.policy,'as_of':str(cutoff.date()) if feature_mode=='dated' else snapshot_as_of}
    store=make_store(data)
    political_review=store.political['reviewed_through']
    political_carried=pd.Timestamp(data.policy['as_of'])>pd.Timestamp(political_review)
    if political_carried:
        # Explicit scenario assumption, never relabel the source as reverified.
        # Restricted to the forecast cycle; users can update the reviewed config.
        store.political={**store.political,'reviewed_through':data.policy['as_of']}
        print('Political context: carrying forward the',political_review,'review; not independently reverified.',flush=True)
    inputs,calendar,endpoints=calendar_inputs(data,store,'matched_live')
    # In polling-only sensitivity mode, keep today's feature context but use the
    # requested cutoff for screening and aging every current-cycle poll.
    inputs.loc[inputs.cycle.eq(2026),'context_id']=str(cutoff.date())
    data.policy={**data.policy,'as_of':str(cutoff.date())}
    targets,waves,poll_audit,_=prepare_inputs(data,inputs)
    targets=targets[targets.kind.eq('senate')&targets.cycle.eq(2026)].sort_values('target_id').reset_index(drop=True)
    folds=pd.read_parquet(ASSETS/'main/folds.parquet');fold=folds[folds.scenario.eq('matched_live')&folds.cycle.eq(2026)].iloc[0]
    saved=pd.read_parquet(ASSETS/'main/predictions.parquet')
    q=saved[saved.scenario.eq('matched_live')&saved.cycle.eq(2026)].sort_values('target_id').reset_index(drop=True).copy()
    if list(q.target_id)!=list(targets.target_id):raise ValueError('Contest roster changed; explicit model/seat mapping review required')
    agg=gaussian.aggregate(targets,waves)
    for col in agg.columns:
        if col!='target_id':q[col]=agg.set_index('target_id').loc[q.target_id,col].to_numpy()
    q['as_of']=data.policy['as_of'];q['context_id']=data.policy['as_of'];q['actual']=np.nan
    cal=pd.read_parquet(ASSETS/'training/calendars.parquet');cal=cal[cal.scenario.eq('matched_live')].copy()
    current_context=calendar[calendar.cycle.eq(2026)]
    for col in current_context.columns:cal.loc[cal.cycle.eq(2026),col]=current_context[col].iloc[0]
    fit=dict(np.load(ASSETS/'main'/fold.fit_path));fit['a']=float(fit['a'])
    design,_,z,_,future_scores,_=features.prepare_design(cal,fit['years'],fit['training_weights'],2026)
    fit['z']=z[[design.active.index(t) for t in fit['terms']]]
    return dict(data=data,targets=targets,waves=waves,poll_audit=poll_audit,q=q,cal=cal,
                fit=fit,fold=fold,current_context=current_context,future_scores=future_scores,
                political_review=political_review,political_carried=political_carried,
                feature_ledger=pd.DataFrame(store.ledger),snapshot_as_of=snapshot_as_of,
                feature_mode=feature_mode)


def live_forecast(snapshot, include_student=True, weights=(.1,.2,.4,.5), freshness=None,
                  as_of=None, feature_mode='dated', output_kind='live', prepared=None):
    """Update evidence with fixed historical fits; optionally replay a past cutoff."""
    from simple_baselines import poll_predict
    from state_poll_bias import fit_bias
    e=prepared if prepared is not None else prepare_live_evidence(snapshot,as_of,feature_mode)
    data=e['data'];targets=e['targets'];waves=e['waves'];poll_audit=e['poll_audit']
    q=e['q'];cal=e['cal'];fit=e['fit'];fold=e['fold']
    current_context=e['current_context'];future_scores=e['future_scores']
    political_review=e['political_review'];political_carried=e['political_carried']
    p,_,arrays=signed.predict(q,fit,load_poll('matched_live',2026),fit['loading'],fold.lambda_value)
    pp=scored(p,'Bayesian');seed=SEED+2026
    draws=arrays['mean']+np.random.default_rng(seed).standard_normal((DRAWS,len(q)))@np.linalg.cholesky(arrays['covariance']).T
    refs=pd.read_parquet(ASSETS/'main/seats.parquet');ref=refs[refs.scenario.eq('matched_live')&refs.cycle.eq(2026)].iloc[0]
    rows=[];seats=[];row,freq=seat_row(pp,draws,'Bayesian',ref);rows.append(pp);seats.append(row)
    history=pd.read_parquet(ASSETS/'training/history.parquet');history=history[history.scenario.eq('matched_live')]
    old=history[history.cycle.eq(2026)]
    nb=poll_predict(targets,waves,float(old.poll_half_life.iloc[0]),float(old.poll_prior_strength.iloc[0])).rename(columns={'prediction':'poll_baseline'})
    nb=targets.merge(nb,on='target_id',validate='one_to_one')
    means,_,_=fit_bias(history[history.cycle.lt(2026)],nb,5,8.,'state',float(old.bias_shrinkage.iloc[0]))
    for w in weights:
        name=f'Corrected {100*w:g}%';bp=pp.copy();bp['model']=name
        bp['margin_pp']=blend_mean(pp.margin_pp,100*means,w);bp['prediction_pp']=bp.margin_pp;bp['prediction']=bp.margin_pp/100
        bp['median_pp']=bp.margin_pp
        bp=rescore(bp);bp['lo95_pp']=bp.margin_pp-norm.ppf(.975)*bp.sigma_pp;bp['hi95_pp']=bp.margin_pp+norm.ppf(.975)*bp.sigma_pp
        rows.append(bp);row,_=seat_row(bp,translate_draws(draws,pp.margin_pp,bp.margin_pp),name,ref);seats.append(row)
    paired=pd.read_parquet(ASSETS/'reference_blends/predictions.parquet').query('model == "Bayesian"')
    sigma=fit_scale(paired,'matched_live',2026,'nonbayesian_pp')['sigma_pp']
    npred=pp.copy();npred['model']='Non-Bayesian corrected';npred['margin_pp']=100*means;npred['prediction_pp']=npred.margin_pp;npred['prediction']=means
    npred['sigma_pp']=sigma;npred['posterior_sd_pp']=sigma;npred=rescore(npred)
    npred['median_pp']=npred.margin_pp;npred['lo95_pp']=npred.margin_pp-norm.ppf(.975)*sigma;npred['hi95_pp']=npred.margin_pp+norm.ppf(.975)*sigma
    rows.append(npred)
    from plain_polling_blend import independent_seats
    ss,_=independent_seats(npred.p_dem.to_numpy(),int(ref.fixed_D));point=int(ref.fixed_D)+int((means>0).sum())
    seats.append(dict(scenario='matched_live',cycle=2026,model='Non-Bayesian corrected',point_D=point,point_R=100-point,method='Independent-state approximation',**ss))
    out=new_run(output_kind)
    from model_portfolio import additions,configuration
    extra=additions(pp,fit,float(fold.lambda_value),cal,draws,arrays['covariance'],npred,ref,include_student)
    rows.extend(extra['predictions']);seats.extend(extra['seats'])
    if extra['diagnostics']:
        diagnostics=pd.concat(extra['diagnostics'],ignore_index=True)
        diagnostics.to_parquet(out/'all_model_diagnostics.parquet',index=False)
        diagnostics[diagnostics.model.eq('Student-t research helper')].to_parquet(out/'student_diagnostics.parquet',index=False)
    (out/'model_forecasts').mkdir()
    for i,(name,moments) in enumerate(extra['moments'].items()):
        np.savez_compressed(out/'model_forecasts'/f'{i}.npz',model=name,target_ids=q.target_id.to_numpy(str),**moments)
    write_json(out/'ensemble_checks.json',extra['checks'])
    predictions=pd.concat(rows,ignore_index=True)
    assert predictions.actual_pp.isna().all()
    predictions.to_parquet(out/'predictions.parquet',index=False);pd.DataFrame(seats).to_parquet(out/'seats.parquet',index=False)
    np.savez_compressed(out/'main_joint.npz',**arrays,target_ids=q.target_id.to_numpy(str),seat_count_frequency=freq)
    poll_audit[poll_audit.cycle.eq(2026)].to_parquet(out/'poll_audit.parquet',index=False)
    future_scores.to_parquet(out/'feature_scores.parquet',index=False)
    current_context.to_parquet(out/'feature_context.parquet',index=False)
    e['feature_ledger'].to_parquet(out/'feature_ledger.parquet',index=False)
    return finish(out,dict(kind=output_kind,as_of=data.policy['as_of'],dataset=str(Path(snapshot).resolve().relative_to(ROOT)),dataset_manifest_sha256=sha(Path(snapshot)/'manifest.json'),
        snapshot_as_of=e['snapshot_as_of'],feature_mode=e['feature_mode'],
        reconstruction=bool(data.policy['as_of']!=e['snapshot_as_of']),
        availability_policy='Known poll release cutoff; unknown releases use field end. Features use latest-vintage reference periods, not publication-vintage reconstruction.',
        main='repaired_both__selected',reference_model='Bayesian',ensemble=configuration() if include_student else None,
        validation='Chronological earlier-cycle validation; architecture selection reused evaluation years',
        trained_through=2024,calibration_horizon='frozen September17 historical forecasts',
        refreshed_hyperparameters=False,weights=list(weights),freshness=freshness or {},
        missing_current_feature_scores=future_scores.columns[future_scores.isna().any()].tolist(),
        political_reference_reviewed_through=political_review,political_context_carried_forward=bool(political_carried)),publish=output_kind!='live')


def refresh(**kwargs):
    from release_refresh import refresh_live
    return refresh_live(**kwargs)


def run_logged(function, *args, **kwargs):
    """Keep notebooks short; save verbose progress instead of discarding it."""
    import contextlib
    import io
    stream=io.StringIO();log=ROOT/'cache/logs'/f'{function.__name__}_{datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")}.txt'
    log.parent.mkdir(parents=True,exist_ok=True)
    try:
        with contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream):
            result=function(*args,**kwargs)
    finally:log.write_text(stream.getvalue())
    print('Run log:',log.relative_to(ROOT))
    return result
