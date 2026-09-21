"""Recent Gaussian shared/state polling bias, fixed priors, rolling penalty selection."""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
from scipy.linalg import cho_factor, cho_solve
import poll_update_review as update_model
import simple_bayesian_polling as v1

SOURCE = '20260919T181021.670795Z'
RECIPES = dict(existing=('zero',8.), zero8=('zero',8.), shared8=('shared',8.),
               state8=('state',8.), shared4=('shared',4.), state4=('state',4.))
PRIORS = update_model.PRIORS
SCALES = [1.,2.,4.]
CONFIG = dict(recipes=RECIPES, priors=PRIORS, scales=SCALES, lookback_calendar_cycles=5,
              marginal_bias_prior_variance_pp2=9., shared_fraction=.5, other_type_weight=.5,
              validation_cycles=3, draws=20000, seed=190926, as_of='2026-09-17',
              selection_objective='equal_cycle_mean_marginal_negative_log_density')


def inv(a):
    return cho_solve(cho_factor(a, lower=True), np.eye(len(a)))


def bias_posterior(cov, values, noise, weights, architecture):
    """Exact conditional Gaussian posterior; row weights are power-likelihood weights."""
    cov, values, noise, weights = map(np.asarray, (cov,values,noise,weights))
    n = len(cov)
    if values.shape != noise.shape or values.shape != (len(weights),n):
        raise ValueError('Incompatible historical array dimensions')
    if not np.array_equal(np.isfinite(values),np.isfinite(noise)):
        raise ValueError('Mismatched historical missingness')
    if (weights<=0).any() or not np.isfinite(weights).all() or (noise[np.isfinite(noise)]<0).any():
        raise ValueError('Invalid weights/noise')
    if architecture=='zero':
        design=np.eye(n); variances=np.full(n,9.)
    elif architecture=='shared':
        design=np.ones((n,1)); variances=np.array([9.])
    elif architecture=='state':
        design=np.column_stack([np.ones(n),np.eye(n)]);variances=np.full(n+1,4.5)
    else:
        raise ValueError('Unknown architecture')
    precision=np.diag(1/variances);rhs=np.zeros(len(variances))
    for x,v,w in zip(values,noise,weights):
        obs=np.flatnonzero(np.isfinite(x))
        if not len(obs):
            continue
        a=design[obs]
        precision_obs=inv(cov[np.ix_(obs,obs)]+np.diag(v[obs]))
        precision+=w*(a.T@precision_obs@a)
        rhs+=w*(a.T@precision_obs@x[obs])
    coefficient_covariance=inv(precision)
    coefficients=coefficient_covariance@rhs
    bcov=design@coefficient_covariance@design.T
    return dict(bias_mean=design@coefficients, bias_covariance=(bcov+bcov.T)/2,
                coefficients=coefficients, coefficient_covariance=coefficient_covariance,
                design=design, coefficient_prior_variances=variances)


def fit_bias(saved, year, recipe):
    architecture, half = RECIPES[recipe]
    years=saved['years'];mask=years<year
    if recipe!='existing':mask &= years>=year-2*CONFIG['lookback_calendar_cycles']
    years=years[mask]
    x=saved['training_values'][mask];noise=saved['training_noise'][mask]
    weights=np.exp2(-(year-years)/half)*np.where(years%4==year%4,1.,CONFIG['other_type_weight'])
    post=bias_posterior(saved['covariance'],x,noise,weights,architecture)
    if recipe=='existing':
        if not (np.allclose(post['bias_mean'],saved['bias_mean'],atol=1e-9) and
                np.allclose(post['bias_covariance'],saved['bias_covariance'],atol=1e-9)):
            raise AssertionError('Existing bias reconstruction differs')
        # Retain the original stored arrays exactly for the control.
        post['bias_mean']=saved['bias_mean'].copy();post['bias_covariance']=saved['bias_covariance'].copy()
    return dict(**post,covariance=saved['covariance'].copy(),training_values=x,training_noise=noise,
                training_weights=weights,years=years,local_n=np.isfinite(x).sum(axis=0),
                local_weight_mass=(np.isfinite(x)*weights[:,None]).sum(axis=0))


def choose(scores, year, recipes, scales):
    eligible=scores[(scores.cycle<year)&scores.recipe.isin(recipes)&scores.variance_scale.isin(scales)]
    years=sorted(eligible.cycle.unique())[-3:]
    preferred=next((r for r in recipes if r.endswith('8')),recipes[0])
    if len(years)<3:
        return preferred,1.,years,'fallback_fewer_than_three_saved_cycles'
    eligible=eligible[eligible.cycle.isin(years)]
    if len(eligible)!=len(years)*len(recipes)*len(scales) or eligible.duplicated(['cycle','recipe','variance_scale']).any():
        raise ValueError('Incomplete or duplicate selection grid')
    means=eligible.groupby(['recipe','variance_scale']).marginal_nll.mean()
    if not np.isfinite(means).all():raise ValueError('Invalid validation scores')
    r,s=min(means.index,key=lambda k:(means.loc[k],k[0]!=preferred,k[1]))
    return r,float(s),years,'last_three_saved_past_cycles'


def selection_specs():
    specs={r+'_R_selected':([r],SCALES) for r in RECIPES}
    for family in ['shared','state']:
        specs[family+'_half_selected_R1']=([family+'8',family+'4'],[1.])
        specs[family+'_joint_selected']=([family+'8',family+'4'],SCALES)
    return specs


def build(lab):
    lab=Path(lab).resolve();source=lab/'reports/prior_sensitivity'/SOURCE
    source_sha=v1.verify(source);source_settings=json.loads((source/'settings.json').read_text())
    upstream=Path(source_settings['source']);upstream_sha=v1.verify(upstream)
    oldhash={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='RECENT_POLL_BIAS.ipynb'}
    out=lab/'reports/recent_poll_bias'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for name in ['fits','forecasts','recipe']:(out/name).mkdir(parents=True,exist_ok=True)
    print('OUTPUT',out,flush=True)
    old=pd.read_parquet(source/'predictions.parquet')
    folds=pd.read_parquet(source/'folds.parquet');folds=folds[folds.model.isin(PRIORS)]
    roster=pd.read_parquet(upstream/'full_seat_ledger.parquet')
    source_cols=['target_id','cycle','geography','scenario','actual','prior','q_pp','firm_mass',
                 'history_selection_10pp','prior_source_max_cycle','prior_history_n','n_samples','firm_count']
    fits={};records=[];candidates=[];scores=[];seats=[];tuning=[];fold_records=[];bias_rows=[];fit_records=[]
    for (sc,prior_model), group in folds.groupby(['scenario','model']):
        for fold in group.sort_values('cycle').itertuples():
            year=int(fold.cycle)
            test=old[old.scenario.eq(sc)&old.model.eq(prior_model)&old.cycle.eq(year)].sort_values('target_id')[source_cols].reset_index(drop=True)
            z=np.load(source/fold.forecast_path);assert np.array_equal(test.target_id.to_numpy(str),z['target_ids'])
            prior_cov=z['prior_covariance'];saved=dict(np.load(source/fold.poll_path))
            bank={}
            for recipe in RECIPES:
                key=(sc,year,recipe)
                if key not in fits:
                    fitted=fit_bias(saved,year,recipe);fits[key]=fitted
                    path=f'fits/{sc}_{year}_{recipe}.npz';np.savez_compressed(out/path,**fitted)
                    fit_records.append(dict(scenario=sc,cycle=year,recipe=recipe,path=path,source_poll=fold.poll_path,
                        training_max_cycle=int(fitted['years'].max()) if len(fitted['years']) else -1,
                        training_cycles=len(fitted['years']),training_rows=int(np.isfinite(fitted['training_values']).sum())))
                    for i,state in enumerate(v1.STATES):
                        bias_rows.append(dict(scenario=sc,cycle=year,recipe=recipe,geography=state,
                            bias_poll_minus_actual_pp=float(fitted['bias_mean'][i]),correction_pp=float(-fitted['bias_mean'][i]),
                            bias_sd_pp=float(np.sqrt(fitted['bias_covariance'][i,i])),local_n=int(fitted['local_n'][i]),
                            local_weight_mass=float(fitted['local_weight_mass'][i]),
                            shared_bias_pp=float(fitted['coefficients'][0]) if RECIPES[recipe][0]!='zero' else np.nan))
                fit=fits[key];assert np.array_equal(fit['covariance'],saved['covariance'])
                for scale in SCALES:
                    pred,cov,diag=update_model.update(test,prior_cov,fit,scale)
                    bank[(recipe,scale)]=(pred,cov,diag)
                    candidates.append(pred.assign(prior_model=prior_model,recipe=recipe,variance_scale=scale,model=recipe))
            past=pd.DataFrame([s for s in scores if s['scenario']==sc and s['prior_model']==prior_model],
                              columns=['scenario','prior_model','cycle','recipe','variance_scale','marginal_nll'])
            choices={r+'_R1':(r,1.,[],'fixed') for r in RECIPES}
            for name,(recipes,scales) in selection_specs().items():
                choice=choose(past,year,recipes,scales);choices[name]=choice
                selected_recipe,selected_scale,years,status=choice
                rows=past[past.cycle.isin(years)&past.recipe.isin(recipes)&past.variance_scale.isin(scales)]
                for r in rows.to_dict('records'):
                    tuning.append(dict(**r,forecast_cycle=year,validation_cycle=r['cycle'],model=name,
                                       selected_recipe=selected_recipe,selected_scale=selected_scale,status=status))
            for (recipe,scale),(pred,_,_) in bank.items():
                if year<2026:
                    scores.append(dict(scenario=sc,prior_model=prior_model,cycle=year,recipe=recipe,
                                       variance_scale=scale,marginal_nll=float(-pred.log_predictive_density.mean())))
            normal=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31')).standard_normal((CONFIG['draws'],len(test)))
            for model,(recipe,scale,years,status) in choices.items():
                pred,cov,diag=bank[(recipe,scale)]
                pred=pred.assign(prior_model=prior_model,recipe=recipe,variance_scale=scale,model=model)
                pred['correction_pp']=-diag.bias_pp.to_numpy()
                pred['corrected_poll_pp']=diag.corrected_poll_pp.to_numpy()
                records.append(pred)
                draws=pred.prediction_pp.to_numpy()+normal@np.linalg.cholesky(cov).T
                rr=roster[roster.scenario.eq(sc)&roster.cycle.eq(year)]
                seat=v1.seat_counts(rr,test,pred,draws);counts=seat['fixed_D']+(draws>0).sum(axis=1)
                lo,hi=np.quantile(counts,[.15,.85],method='inverted_cdf')
                seats.append(dict(scenario=sc,cycle=year,prior_model=prior_model,model=model,recipe=recipe,variance_scale=scale,
                    **seat,expected_D_exact=float(seat['fixed_D']+pred.p_dem.sum()),D_lo70=int(lo),D_hi70=int(hi)))
                path=f'forecasts/{sc}_{year}_{prior_model}_{model}.npz'
                np.savez_compressed(out/path,target_ids=test.target_id.to_numpy(str),means_pp=pred.prediction_pp.to_numpy(),
                    posterior_covariance=cov,prior_covariance=prior_cov,seat_count_frequency=np.bincount(counts,minlength=101))
                fold_records.append(dict(scenario=sc,cycle=year,prior_model=prior_model,model=model,recipe=recipe,variance_scale=scale,
                    source_forecast=fold.forecast_path,source_poll=fold.poll_path,forecast_path=path,
                    validation_cycles=','.join(map(str,years)),tuning_status=status))
            print(sc,prior_model,year,'complete',flush=True)
    p=pd.concat(records,ignore_index=True)
    tables=dict(predictions=p,candidate_predictions=pd.concat(candidates,ignore_index=True),
                validation_scores=pd.DataFrame(scores),tuning=pd.DataFrame(tuning),seats=pd.DataFrame(seats),
                folds=pd.DataFrame(fold_records),bias_estimates=pd.DataFrame(bias_rows),fits=pd.DataFrame(fit_records),
                calibration=update_model.metrics(p))
    for name,t in tables.items():t.to_parquet(out/(name+'.parquet'),index=False)
    v1.json_write(out/'settings.json',dict(config=CONFIG,source=str(source),source_sha256=source_sha,upstream=str(upstream),
        upstream_sha256=upstream_sha,old_notebook_hashes=oldhash,promotion=False,polling_refreshed=False,
        conditional_covariance_note='Saved residual covariance fixed; bias covariance replaced, not stacked. Covariance fitting uncertainty omitted.'))
    for f in (lab/'scripts').glob('*.py'):(out/'recipe'/f.name).write_bytes(f.read_bytes())
    (out/'RECENT_POLL_BIAS.md').write_bytes((lab/'RECENT_POLL_BIAS.md').read_bytes())
    v1.manifest(out)
    audit(out,lab)
    report(out,lab)
    v1.manifest(out)
    v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out)
    s=json.loads((out/'settings.json').read_text());source=Path(s['source'])
    p=pd.read_parquet(out/'predictions.parquet');cp=pd.read_parquet(out/'candidate_predictions.parquet')
    f=pd.read_parquet(out/'folds.parquet');fits=pd.read_parquet(out/'fits.parquet')
    old=pd.read_parquet(source/'predictions.parquet');scores=pd.read_parquet(out/'validation_scores.parquet')
    seats=pd.read_parquet(out/'seats.parquet');t=pd.read_parquet(out/'tuning.parquet')
    c=dict(source_unchanged=v1.verify(source)==s['source_sha256'],upstream_unchanged=v1.verify(s['upstream'])==s['upstream_sha256'],
           old_notebooks_unchanged=all(v1.sha(lab/n)==h for n,h in s['old_notebook_hashes'].items()),
           unique_predictions=not p.duplicated(['scenario','prior_model','model','target_id']).any(),
           unique_candidates=not cp.duplicated(['scenario','prior_model','recipe','variance_scale','target_id']).any(),
           future_labels_blank=bool(p[p.cycle.eq(2026)].actual.isna().all() and cp[cp.cycle.eq(2026)].actual.isna().all()),
           bias_training_past_only=bool(fits.training_max_cycle.lt(fits.cycle).all()),
           tuning_past_only=bool(t.validation_cycle.lt(t.forecast_cycle).all()),
           finite_forecasts=bool(np.isfinite(p[['prediction_pp','posterior_sd_pp','p_dem']]).all().all()),
           valid_probabilities=bool(p.p_dem.between(0,1).all()),
           same_cases=all(g.groupby('model').target_id.apply(frozenset).nunique()==1 for _,g in p.groupby(['scenario','cycle','prior_model'])))
    fit_ok=[];same_cov=[];fallback=[];fit_cache={}
    for r in fits.itertuples():
        oldfit=dict(np.load(source/r.source_poll));z=dict(np.load(out/r.path));again=fit_bias(oldfit,r.cycle,r.recipe)
        fit_ok.append(all(np.allclose(z[k],again[k],atol=1e-10,equal_nan=True) for k in again))
        same_cov.append(np.array_equal(z['covariance'],oldfit['covariance']))
        if RECIPES[r.recipe][0]=='state':
            fallback.append(np.allclose(z['bias_mean'][z['local_n']==0],z['coefficients'][0]))
        fit_cache[(r.scenario,r.cycle,r.recipe)]=z
    c.update(bias_fits_reconstructed=all(fit_ok),residual_covariance_unchanged=all(same_cov),state_no_history_shared_fallback=all(fallback))
    controls=[];recon=[];frozen=[];selection=[];seatok=[];positive=[];candidate_ok=[]
    cols=['prediction_pp','posterior_sd_pp','p_dem','lo70_pp','hi70_pp','lo95_pp','hi95_pp']
    for r in f.itertuples():
        test=old[old.scenario.eq(r.scenario)&old.cycle.eq(r.cycle)&old.model.eq(r.prior_model)].sort_values('target_id').reset_index(drop=True)
        oldz=np.load(source/r.source_forecast);z=np.load(out/r.forecast_path)
        fit=fit_cache[(r.scenario,r.cycle,r.recipe)]
        expected,cov,_=update_model.update(test,oldz['prior_covariance'],fit,r.variance_scale)
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.prior_model.eq(r.prior_model)&p.model.eq(r.model)].sort_values('target_id')
        recon.append(np.allclose(expected[cols],q[cols],atol=1e-10) and np.allclose(cov,z['posterior_covariance'],atol=1e-10))
        frozen.append(np.array_equal(q.prior.to_numpy(),test.prior.to_numpy()) and np.array_equal(z['prior_covariance'],oldz['prior_covariance']))
        positive.append(np.linalg.eigvalsh(cov).min()>0)
        if r.model=='existing_R1':controls.append(np.allclose(q[cols],test[cols],atol=1e-10))
        if r.model in selection_specs():
            recipes,scales=selection_specs()[r.model]
            a,b,years,status=choose(scores[scores.scenario.eq(r.scenario)&scores.prior_model.eq(r.prior_model)],r.cycle,recipes,scales)
            selection.append((a,b,','.join(map(str,years)),status)==(r.recipe,r.variance_scale,r.validation_cycles,r.tuning_status))
        seat=seats[seats.scenario.eq(r.scenario)&seats.cycle.eq(r.cycle)&seats.prior_model.eq(r.prior_model)&seats.model.eq(r.model)].iloc[0]
        seatok.append(z['seat_count_frequency'].sum()==CONFIG['draws'] and abs(seat.expected_D_exact-seat.fixed_D-q.p_dem.sum())<1e-10 and seat.point_D==seat.fixed_D+(q.prediction_pp>0).sum())
    for (sc,year,pm,recipe,scale),q in cp.groupby(['scenario','cycle','prior_model','recipe','variance_scale']):
        q=q.sort_values('target_id').reset_index(drop=True)
        src=f[f.scenario.eq(sc)&f.cycle.eq(year)&f.prior_model.eq(pm)].iloc[0]
        k=np.load(source/src.source_forecast)['prior_covariance']
        expected,_,_=update_model.update(q,k,fit_cache[(sc,year,recipe)],scale)
        candidate_ok.append(np.allclose(expected[cols],q[cols],atol=1e-10))
    c.update(existing_control_reproduces=all(controls),forecasts_reconstructed=all(recon),all_priors_frozen=all(frozen),
             all_selection_reconstructed=all(selection),seat_accounting=all(seatok),positive_covariances=all(positive),
             all_candidates_reconstructed=all(candidate_ok))
    score_keys=['scenario','prior_model','cycle','recipe','variance_scale']
    expected_scores=cp[cp.cycle.lt(2026)].groupby(score_keys).log_predictive_density.mean().mul(-1).rename('expected').reset_index()
    joined=scores.merge(expected_scores,on=score_keys,validate='one_to_one')
    c['validation_scores_recomputed_from_candidates']=bool(len(joined)==len(scores)==len(expected_scores) and np.allclose(joined.marginal_nll,joined.expected,atol=1e-12))
    result=dict(passed=all(c.values()),checks=c,forecast_rows=len(p),candidate_rows=len(cp),bias_fits=len(fits))
    v1.json_write(out/'completion_audit.json',result)
    if not result['passed']:raise AssertionError([k for k,v in c.items() if not v])
    v1.manifest(out)
    return result


def report(out,lab):
    out,lab=Path(out),Path(lab)
    p=pd.read_parquet(out/'predictions.parquet');cal=pd.read_parquet(out/'calibration.parquet')
    cycles=[]
    for (sc,y,pm,model),q in p[p.actual.notna()].groupby(['scenario','cycle','prior_model','model']):
        e=100*q.actual-q.prediction_pp
        cycles.append(dict(scenario=sc,cycle=y,prior_model=pm,model=model,n=len(q),correct=int(((q.actual>0)==(q.prediction_pp>0)).sum()),
            mae_pp=float(e.abs().mean()),signed_error_pp=float(e.mean()),marginal_nll=float(-q.log_predictive_density.mean()),
            brier=float(((q.p_dem-(q.actual>0))**2).mean()),coverage95=float((e.abs()<=1.959963984540054*q.posterior_sd_pp).mean())))
    pd.DataFrame(cycles).to_parquet(out/'cycle_scores.parquet',index=False)
    # One paired row per model/cycle, avoiding a significance claim from dependent states.
    cycle=pd.DataFrame(cycles);base=cycle[cycle.model.eq('existing_R1')]
    paired=cycle.merge(base[['scenario','cycle','prior_model','mae_pp','correct','marginal_nll']],on=['scenario','cycle','prior_model'],suffixes=('','_baseline'),validate='many_to_one')
    for name in ['mae_pp','correct','marginal_nll']:paired['delta_'+name]=paired[name]-paired[name+'_baseline']
    paired.to_parquet(out/'paired_cycle_changes.parquet',index=False)
    # Inspect bias itself without confusing it with the subsequent prior update.
    bias_only=[]
    polled=p[p.actual.notna()&p.q_pp.notna()&p.prior_model.eq('control_state')&p.model.isin([r+'_R1' for r in RECIPES])]
    for period,first in [('recent_2016_2024',2016),('all_2012_2024',2012)]:
        for (sc,recipe),g in polled[polled.cycle.ge(first)].groupby(['scenario','recipe']):
            for stage,center in [('raw_poll','q_pp'),('corrected_poll','corrected_poll_pp')]:
                e=100*g.actual-g[center]
                bias_only.append(dict(period=period,scenario=sc,recipe=recipe,stage=stage,n=len(g),
                    mae_pp=float(e.abs().groupby(g.cycle).mean().mean()),signed_error_pp=float(e.groupby(g.cycle).mean().mean())))
    bias_only=pd.DataFrame(bias_only);bias_only.to_parquet(out/'poll_only_errors.parquet',index=False)
    base=p[p.model.eq('existing_R1')][['scenario','prior_model','target_id','prediction_pp','p_dem']]
    comparison=p.merge(base,on=['scenario','prior_model','target_id'],suffixes=('','_baseline'),validate='many_to_one')
    comparison['margin_change_pp']=comparison.prediction_pp-comparison.prediction_pp_baseline
    comparison['changed_call']=(comparison.prediction_pp>0)!=(comparison.prediction_pp_baseline>0)
    comparison=comparison[comparison.changed_call&comparison.actual.notna()].copy()
    comparison['was_correct']=(comparison.prediction_pp_baseline>0)==(comparison.actual>0)
    comparison['now_correct']=(comparison.prediction_pp>0)==(comparison.actual>0)
    comparison['actual_pp']=100*comparison.actual
    comparison[['scenario','cycle','geography','target_id','prior_model','model','actual_pp','prediction_pp_baseline','prediction_pp','was_correct','now_correct']].to_parquet(out/'changed_calls.parquet',index=False)
    seats=pd.read_parquet(out/'seats.parquet');folds=pd.read_parquet(out/'folds.parquet');bias=pd.read_parquet(out/'bias_estimates.parquet')
    focus=['existing_R1','zero8_R1','shared8_R1','state8_R1','shared4_R1','state4_R1','existing_R_selected','shared_half_selected_R1','state_half_selected_R1','shared_joint_selected','state_joint_selected']
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(13,5))
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=cal[cal.period.eq('recent_2016_2024')&cal.group.eq('all')&cal.prior_model.eq('control_state')&cal.scenario.eq(sc)].set_index('model').loc[focus]
        ax.barh(q.index,q.mae_pp,color='#327c9b');ax.invert_yaxis();ax.set(title=sc,xlabel='Margin MAE (pp)')
    fig.tight_layout();fig.savefig(out/'mae_comparison.png',dpi=140);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=cal[cal.period.eq('recent_2016_2024')&cal.group.eq('all')&cal.prior_model.eq('control_state')&cal.scenario.eq(sc)].set_index('model')
        for model in ['existing_R1','state8_R1','state_joint_selected','shared_joint_selected']:
            row=q.loc[model];ax.plot([50,70,80,95],[100*row['coverage'+str(n)] for n in [50,70,80,95]],marker='o',label=model)
        ax.plot([50,95],[50,95],'k--');ax.set(title=sc,xlabel='Nominal interval (%)',ylabel='Observed coverage (%)');ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(out/'coverage_comparison.png',dpi=140);plt.close(fig)
    cols=['scenario','model','n','correct','mae_pp','brier','marginal_nll','coverage70','coverage95']
    text='# Recent polling bias and reliability penalty — results\n\n'
    text+='Frozen September17 inputs and exact election priors. Positive bias means polls overestimate Democrats; correction = minus bias. New bias posterior uncertainty replaces the old one. Residual covariance remains fixed; lambda scales the total likelihood covariance once. No automatic promotion.\n\n'
    text+='MAE and negative log density average cycles equally. Calls/coverage/Brier pool contests. Smaller MAE/NLL/Brier is better. Historical cycles are repeatedly explored; no statistical-significance or untouched-test claim. See RECENT_POLL_BIAS.md for the full fixed Gaussian hierarchy, recency, selection and fallback contract.\n\n'
    text+='## Review conclusion\n\nRecent-only zero-centered bias is the smallest change: reference-prior September MAE6.9802→6.9769 and October5.2503→5.2447pp, with calls unchanged129/131 out of140. These gains are tiny. Fixed four-year pooled-state bias gives September6.9361/128calls and October5.2571/132calls; it does not dominate. Four-year shared bias with a tuned penalty gives September6.9205/129 and October5.3039/134: more late winner calls, but worse late margin MAE and marginal probability score. Its late competitive calls improve47→49/54; noncompetitive67→68/68. Only one of its three additional late calls is after2016.\n\nThe penalty is not a reliable universal improvement after bias correction. Keep the current reference and treat recent-zero8 as a small-change challenger; retain shared4 with selected penalty as a winner-call challenger. No automatic inclusion decision. Joint decay/penalty selection does not consistently outperform the fixed alternatives. The same broad tradeoff appears with the two frozen prior challengers, although individual calls differ. Covariance recentering, prior bias variance/pooling strength, dynamic shared-cycle errors and prospective validation remain separate follow-ups rather than extra searches in this run.\n\n'
    for period in ['recent_2016_2024','tuned_2018_2024','all_2012_2024']:
        text+='## '+period+' — reference prior\n\n'+cal[cal.period.eq(period)&cal.group.eq('all')&cal.prior_model.eq('control_state')][cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Prior challengers, recent cycles\n\n'+cal[cal.period.eq('recent_2016_2024')&cal.group.eq('all')&cal.model.isin(['existing_R1','shared8_R1','state8_R1','shared_joint_selected','state_joint_selected'])][['prior_model']+cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Reference-prior groups\n\n'+cal[cal.period.eq('recent_2016_2024')&cal.group.ne('all')&cal.prior_model.eq('control_state')&cal.model.isin(['existing_R1','shared8_R1','state8_R1','shared_joint_selected','state_joint_selected'])][['group']+cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Per-cycle results\n\n'+cycle[cycle.prior_model.eq('control_state')&cycle.model.isin(focus)].round(4).to_markdown(index=False)+'\n\n'
    text+='## Poll-only error before the prior update\n\nSame admitted polled cases; raw polling repeats identically across recipes. Positive signed error means the actual outcome was more Democratic than predicted.\n\n'+bias_only.query('period=="recent_2016_2024"').round(4).to_markdown(index=False)+'\n\n'
    text+='## Winner calls changed from the reference\n\n'+comparison[comparison.prior_model.eq('control_state')&comparison.cycle.ge(2016)&comparison.model.isin(['zero8_R1','shared4_R_selected','state4_R1','state_joint_selected'])][['scenario','cycle','geography','model','actual_pp','prediction_pp_baseline','prediction_pp','was_correct','now_correct']].round(3).to_markdown(index=False)+'\n\n'
    text+='## Current selected settings\n\n'+folds[folds.cycle.eq(2026)][['prior_model','model','recipe','variance_scale','validation_cycles','tuning_status']].to_markdown(index=False)+'\n\n'
    text+='## Current full chamber scenarios\n\nD includes Democratic-caucusing independents; existing continuing/completion seats and scalar ballot assumptions remain. These are conditional scenarios, with no current October forecast invented.\n\n'+seats[seats.cycle.eq(2026)][['prior_model','model','point_D','point_R','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95']].round(3).to_markdown(index=False)+'\n\n'
    current=p[p.cycle.eq(2026)&p.prior_model.eq('control_state')]
    table=current.pivot(index='geography',columns='model',values='prediction_pp')
    table=table.join(current[current.model.eq('existing_R1')].set_index('geography')[['q_pp','prior']]);table['prior_pp']=100*table.pop('prior')
    table.reset_index().to_parquet(out/'current_states.parquet',index=False)
    text+='## Current state margins, reference prior\n\n'+table[focus+['q_pp','prior_pp']].round(3).to_markdown()+'\n\n'
    text+='## Current bias estimates and local support\n\n'+bias[bias.cycle.eq(2026)].round(3).to_markdown(index=False)+'\n\n'
    text+='## Limits and decision\n\nHold all candidates as experiments until reviewed. The fixed covariance was estimated under the original bias specification, so these are conditional mean-model comparisons; a later recenter/refit sensitivity may matter. Bias prior SD remains3pp marginal, with a fixed half-shared/half-state variance split in the pooled model. Five calendar cycles do not mean five observations in each state. Empty local history uses shared bias with retained local uncertainty. Last-three-fold selection first operates in2018; earlier cycles use declared8year/lambda1 fallback. Bias uncertainty is integrated, but covariance/hyperparameter selection uncertainty is not.\n'
    (out/'RECENT_POLL_BIAS_RESULTS.md').write_text(text);(lab/'RECENT_POLL_BIAS_RESULTS.md').write_text(text)
    (out/'recipe'/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    v1.manifest(out)
    return out


if __name__=='__main__':
    build(Path(__file__).resolve().parents[1])
