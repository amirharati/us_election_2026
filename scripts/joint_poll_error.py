"""Fit a shared residual covariance scale with integrated Gaussian polling bias."""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize_scalar
import recent_poll_bias as bias
import poll_update_review as update
import simple_bayesian_polling as v1

SOURCE='20260919T185908.315208Z'
CONFIG=dict(alpha_bounds=[1/16,16.],log_grid_points=33,optimizer_xatol=1e-7,
            recipes=list(bias.RECIPES),priors=bias.PRIORS,draws=20000,seed=192026,
            lambda_fixed=1.,as_of='2026-09-17',selection='historical_integrated_bias_marginal_likelihood')


class Objective:
    """Negative log integral of prior(beta) times weighted Gaussian likelihoods."""
    def __init__(self, saved, architecture):
        n=len(saved['covariance'])
        if architecture=='zero':a=np.eye(n);variances=np.full(n,9.)
        elif architecture=='shared':a=np.ones((n,1));variances=np.array([9.])
        elif architecture=='state':a=np.column_stack([np.ones(n),np.eye(n)]);variances=np.full(n+1,4.5)
        else:raise ValueError('Unknown architecture')
        self.a=a;self.variances=variances;self.rows=[];self.evaluations={}
        for x,noise,w in zip(saved['training_values'],saved['training_noise'],saved['training_weights']):
            obs=np.flatnonzero(np.isfinite(x))
            if not np.array_equal(np.isfinite(x),np.isfinite(noise)) or not np.isfinite(w) or w<=0:
                raise ValueError('Invalid historical arrays')
            if not len(obs):continue
            self.rows.append((x[obs],noise[obs],float(w),a[obs],saved['covariance'][np.ix_(obs,obs)]))

    def __call__(self, logalpha):
        logalpha=float(logalpha)
        if logalpha in self.evaluations:return self.evaluations[logalpha]
        alpha=np.exp(logalpha);precision=np.diag(1/self.variances);rhs=np.zeros(len(self.variances));constant=0.
        for x,noise,w,a,c in self.rows:
            v=alpha*c+np.diag(noise)
            chol=cho_factor(v,lower=True)
            ia=cho_solve(chol,a);ix=cho_solve(chol,x)
            constant+=w*(len(x)*np.log(2*np.pi)+2*np.log(np.diag(chol[0])).sum()+x@ix)
            precision+=w*(a.T@ia);rhs+=w*(a.T@ix)
        chol=cho_factor(precision,lower=True)
        result=.5*(constant+np.log(self.variances).sum()+2*np.log(np.diag(chol[0])).sum()-rhs@cho_solve(chol,rhs))
        if not np.isfinite(result):raise ValueError('Nonfinite marginal objective')
        self.evaluations[logalpha]=float(result)
        return float(result)


def fit_scale(saved, architecture, learned=True):
    objective=Objective(saved,architecture)
    grid=np.linspace(*np.log(CONFIG['alpha_bounds']),CONFIG['log_grid_points'])
    values=np.array([objective(x) for x in grid])
    candidates=[(objective(0.),0.)]
    candidates.extend(zip(values,grid))
    refinements=[]
    if learned:
        for i in range(1,len(grid)-1):
            if values[i]<=values[i-1] and values[i]<=values[i+1]:
                r=minimize_scalar(objective,bounds=(grid[i-1],grid[i+1]),method='bounded',options={'xatol':CONFIG['optimizer_xatol']})
                if not r.success:raise RuntimeError('Scale optimization failed: '+r.message)
                refinements.append([r.x,r.fun]);candidates.append((float(r.fun),float(r.x)))
        value,logalpha=min(candidates,key=lambda z:(z[0],abs(z[1])))
    else:value,logalpha=objective(0.),0.
    alpha=float(np.exp(logalpha))
    posterior=bias.bias_posterior(alpha*saved['covariance'],saved['training_values'],saved['training_noise'],saved['training_weights'],architecture)
    fitted=dict(**posterior,covariance=alpha*saved['covariance'],base_covariance=saved['covariance'].copy(),
        training_values=saved['training_values'].copy(),training_noise=saved['training_noise'].copy(),
        training_weights=saved['training_weights'].copy(),years=saved['years'].copy(),alpha=np.array(alpha),
        objective=np.array(value),objective_at_one=np.array(objective(0.)),grid_logalpha=grid,grid_objectives=values,
        refinements=np.asarray(refinements).reshape(-1,2),evaluations=np.array(sorted(objective.evaluations.items())),
        at_boundary=np.array(bool(np.isclose(logalpha,grid[0],atol=1e-5) or np.isclose(logalpha,grid[-1],atol=1e-5))))
    return fitted


def build(lab):
    lab=Path(lab).resolve();source=lab/'reports/recent_poll_bias'/SOURCE;source_sha=v1.verify(source)
    oldsettings=json.loads((source/'settings.json').read_text());prior_source=Path(oldsettings['source']);upstream=Path(oldsettings['upstream'])
    prior_sha=v1.verify(prior_source);upstream_sha=v1.verify(upstream)
    out=lab/'reports/joint_poll_error'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for name in ['fits','forecasts','recipe']:(out/name).mkdir(parents=True,exist_ok=True)
    print('OUTPUT',out,flush=True)
    oldhash={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='JOINT_POLL_ERROR.ipynb'}
    source_fits=pd.read_parquet(source/'fits.parquet');fit_records=[];cache={};bias_rows=[]
    for r in source_fits.itertuples():
        saved=dict(np.load(source/r.path));arch=bias.RECIPES[r.recipe][0]
        for method in ['fixed','learned']:
            f=fit_scale(saved,arch,method=='learned');cache[(r.scenario,r.cycle,r.recipe,method)]=f
            if method=='fixed':
                assert np.allclose(f['bias_mean'],saved['bias_mean'],atol=1e-9)
                assert np.allclose(f['bias_covariance'],saved['bias_covariance'],atol=1e-9)
            path=f'fits/{r.scenario}_{r.cycle}_{r.recipe}_{method}.npz';np.savez_compressed(out/path,**f)
            fit_records.append(dict(scenario=r.scenario,cycle=r.cycle,recipe=r.recipe,method=method,path=path,
                source_fit=r.path,alpha=float(f['alpha']),objective=float(f['objective']),objective_at_one=float(f['objective_at_one']),
                at_boundary=bool(f['at_boundary']),training_max_cycle=r.training_max_cycle,training_cycles=r.training_cycles,
                training_rows=r.training_rows,evaluations=len(f['evaluations']),refinements=len(f['refinements'])))
            for i,state in enumerate(v1.STATES):
                bias_rows.append(dict(scenario=r.scenario,cycle=r.cycle,recipe=r.recipe,method=method,geography=state,
                    correction_pp=float(-f['bias_mean'][i]),bias_sd_pp=float(np.sqrt(f['bias_covariance'][i,i])),
                    residual_sd_pp=float(np.sqrt(f['covariance'][i,i])),local_n=int(np.isfinite(f['training_values'][:,i]).sum())))
        print('fit',r.scenario,r.cycle,r.recipe,'alpha',round(float(f['alpha']),4),flush=True)
    oldp=pd.read_parquet(source/'predictions.parquet');oldfolds=pd.read_parquet(source/'folds.parquet')
    roster=pd.read_parquet(upstream/'full_seat_ledger.parquet');predictions=[];seats=[];folds=[]
    basefolds=oldfolds[oldfolds.model.eq('existing_R1')]
    for row in basefolds.itertuples():
        sc,year,pm=row.scenario,int(row.cycle),row.prior_model
        test=oldp[oldp.scenario.eq(sc)&oldp.cycle.eq(year)&oldp.prior_model.eq(pm)&oldp.model.eq('existing_R1')].sort_values('target_id').reset_index(drop=True)
        test=test.drop(columns=['model','recipe','variance_scale','correction_pp','corrected_poll_pp'])
        z=np.load(source/row.forecast_path);assert np.array_equal(z['target_ids'],test.target_id.to_numpy(str))
        k=z['prior_covariance']
        normal=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31')).standard_normal((CONFIG['draws'],len(test)))
        for recipe in bias.RECIPES:
            for method in ['fixed','learned']:
                f=cache[(sc,year,recipe,method)];model=recipe+'_'+method
                p,cov,d=update.update(test,k,f,1.)
                p=p.assign(model=model,recipe=recipe,method=method,alpha=float(f['alpha']),variance_scale=1.,
                    correction_pp=-d.bias_pp.to_numpy(),corrected_poll_pp=d.corrected_poll_pp.to_numpy())
                predictions.append(p)
                draws=p.prediction_pp.to_numpy()+normal@np.linalg.cholesky(cov).T
                rr=roster[roster.scenario.eq(sc)&roster.cycle.eq(year)];seat=v1.seat_counts(rr,test,p,draws)
                counts=seat['fixed_D']+(draws>0).sum(axis=1);lo,hi=np.quantile(counts,[.15,.85],method='inverted_cdf')
                seats.append(dict(scenario=sc,cycle=year,prior_model=pm,model=model,recipe=recipe,method=method,
                    **seat,expected_D_exact=float(seat['fixed_D']+p.p_dem.sum()),D_lo70=int(lo),D_hi70=int(hi)))
                path=f'forecasts/{sc}_{year}_{pm}_{model}.npz'
                np.savez_compressed(out/path,target_ids=p.target_id.to_numpy(str),means_pp=p.prediction_pp.to_numpy(),
                    posterior_covariance=cov,prior_covariance=k,seat_count_frequency=np.bincount(counts,minlength=101))
                folds.append(dict(scenario=sc,cycle=year,prior_model=pm,model=model,recipe=recipe,method=method,
                    forecast_path=path,source_forecast=row.forecast_path,source_poll=row.source_poll,fit_path=f'fits/{sc}_{year}_{recipe}_{method}.npz'))
    p=pd.concat(predictions,ignore_index=True)
    tables=dict(predictions=p,calibration=update.metrics(p),seats=pd.DataFrame(seats),folds=pd.DataFrame(folds),
                fits=pd.DataFrame(fit_records),bias_estimates=pd.DataFrame(bias_rows))
    for name,t in tables.items():t.to_parquet(out/(name+'.parquet'),index=False)
    v1.json_write(out/'settings.json',dict(config=CONFIG,source=str(source),source_sha256=source_sha,
        prior_source=str(prior_source),prior_source_sha256=prior_sha,upstream=str(upstream),upstream_sha256=upstream_sha,
        old_notebook_hashes=oldhash,promotion=False,polling_refreshed=False,
        fitting='Integrated Gaussian bias marginal likelihood with cycle power weights; alpha estimated, no inner validation selector.'))
    for f in (lab/'scripts').glob('*.py'):(out/'recipe'/f.name).write_bytes(f.read_bytes())
    (out/'JOINT_POLL_ERROR.md').write_bytes((lab/'JOINT_POLL_ERROR.md').read_bytes())
    v1.manifest(out);audit(out,lab);report(out,lab)
    v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);s=json.loads((out/'settings.json').read_text());source=Path(s['source'])
    p=pd.read_parquet(out/'predictions.parquet');oldp=pd.read_parquet(source/'predictions.parquet')
    fits=pd.read_parquet(out/'fits.parquet');folds=pd.read_parquet(out/'folds.parquet');seats=pd.read_parquet(out/'seats.parquet')
    checks=dict(source_unchanged=v1.verify(source)==s['source_sha256'],prior_source_unchanged=v1.verify(s['prior_source'])==s['prior_source_sha256'],
        upstream_unchanged=v1.verify(s['upstream'])==s['upstream_sha256'],
        old_notebooks_unchanged=all(v1.sha(lab/n)==h for n,h in s['old_notebook_hashes'].items()),
        bias_scale_training_past_only=bool(fits.training_max_cycle.lt(fits.cycle).all()),
        whole_likelihood_penalty_fixed_one=bool(p.variance_scale.eq(1).all()),
        unique_forecasts=not p.duplicated(['scenario','prior_model','model','target_id']).any(),
        future_labels_blank=bool(p[p.cycle.eq(2026)].actual.isna().all()),
        finite_probabilities=bool(np.isfinite(p[['prediction_pp','posterior_sd_pp','p_dem']]).all().all() and p.p_dem.between(0,1).all()),
        equal_comparison_cases=all(g.groupby('model').target_id.apply(frozenset).nunique()==1 for _,g in p.groupby(['scenario','cycle','prior_model'])))
    fitok=[];trainingok=[];shapeok=[];optok=[];priorbiasok=[]
    for r in fits.itertuples():
        z=dict(np.load(out/r.path));old=dict(np.load(source/r.source_fit));arch=bias.RECIPES[r.recipe][0]
        obj=Objective(old,arch);expected=bias.bias_posterior(r.alpha*old['covariance'],old['training_values'],old['training_noise'],old['training_weights'],arch)
        fitok.append(all(np.allclose(z[k],expected[k],atol=1e-10) for k in expected) and np.isclose(obj(np.log(r.alpha)),r.objective,atol=1e-10))
        trainingok.append(all(np.array_equal(z[k],old[k],equal_nan=True) for k in ['years','training_values','training_noise','training_weights']))
        shapeok.append(np.allclose(z['covariance'],r.alpha*old['covariance'],atol=1e-12) and np.array_equal(z['base_covariance'],old['covariance']))
        priorbiasok.append(np.allclose(np.diag(z['design']@np.diag(z['coefficient_prior_variances'])@z['design'].T),9.))
        # Local score perturbations and stored full grid verify the selected numerical solution.
        if r.method=='learned':
            grid=np.array([obj(x) for x in z['grid_logalpha']]);x=np.log(r.alpha)
            probes=np.clip([x-1e-4,x+1e-4],*np.log(CONFIG['alpha_bounds']))
            optok.append(np.allclose(grid,z['grid_objectives'],atol=1e-10) and r.objective<=grid.min()+1e-8 and
                r.objective<=r.objective_at_one+1e-8 and all(r.objective<=obj(t)+1e-7 for t in probes))
    checks.update(bias_and_objective_reconstructed=all(fitok),historical_arrays_unchanged=all(trainingok),
                  covariance_shape_preserved=all(shapeok),marginal_bias_prior_variance_unchanged=all(priorbiasok),
                  optimized_score_verified=all(optok))
    controls=[];recon=[];frozen=[];seatok=[];positive=[]
    cols=['prediction_pp','posterior_sd_pp','p_dem','lo70_pp','hi70_pp','lo95_pp','hi95_pp']
    for r in folds.itertuples():
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.prior_model.eq(r.prior_model)&p.model.eq(r.model)].sort_values('target_id').reset_index(drop=True)
        ref=oldp[oldp.scenario.eq(r.scenario)&oldp.cycle.eq(r.cycle)&oldp.prior_model.eq(r.prior_model)&oldp.model.eq(r.recipe+'_R1')].sort_values('target_id').reset_index(drop=True)
        z=np.load(out/r.forecast_path);oldz=np.load(source/r.source_forecast);fit=dict(np.load(out/r.fit_path))
        pred,cov,_=update.update(ref,oldz['prior_covariance'],fit,1.)
        recon.append(np.allclose(pred[cols],q[cols],atol=1e-10) and np.allclose(cov,z['posterior_covariance'],atol=1e-10))
        frozen.append(np.array_equal(q.prior.to_numpy(),ref.prior.to_numpy()) and np.array_equal(z['prior_covariance'],oldz['prior_covariance']))
        if r.method=='fixed':controls.append(np.allclose(q[cols],ref[cols],atol=1e-9))
        positive.append(np.linalg.eigvalsh(cov).min()>0)
        seat=seats[seats.scenario.eq(r.scenario)&seats.cycle.eq(r.cycle)&seats.prior_model.eq(r.prior_model)&seats.model.eq(r.model)].iloc[0]
        seatok.append(z['seat_count_frequency'].sum()==CONFIG['draws'] and abs(seat.expected_D_exact-seat.fixed_D-q.p_dem.sum())<1e-10 and seat.point_D==seat.fixed_D+(q.prediction_pp>0).sum())
    checks.update(all_fixed_controls_reproduce=all(controls),all_forecasts_reconstructed=all(recon),all_election_priors_unchanged=all(frozen),
                  full_chamber_accounting=all(seatok),positive_posterior_covariance=all(positive))
    result=dict(passed=all(checks.values()),checks=checks,forecast_rows=len(p),bias_scale_fits=int(fits.method.eq('learned').sum()),
                boundary_fits=int(fits[fits.method.eq('learned')].at_boundary.sum()))
    v1.json_write(out/'completion_audit.json',result)
    if not result['passed']:raise AssertionError([k for k,v in checks.items() if not v])
    v1.manifest(out);return result


def report(out,lab):
    out,lab=Path(out),Path(lab)
    p=pd.read_parquet(out/'predictions.parquet');cal=pd.read_parquet(out/'calibration.parquet');seats=pd.read_parquet(out/'seats.parquet');fits=pd.read_parquet(out/'fits.parquet')
    cycles=[]
    for (sc,y,pm,model,recipe,method),g in p[p.actual.notna()].groupby(['scenario','cycle','prior_model','model','recipe','method']):
        e=100*g.actual-g.prediction_pp
        cycles.append(dict(scenario=sc,cycle=y,prior_model=pm,model=model,recipe=recipe,method=method,n=len(g),
            correct=int(((g.prediction_pp>0)==(g.actual>0)).sum()),mae_pp=float(e.abs().mean()),signed_error_pp=float(e.mean()),
            marginal_nll=float(-g.log_predictive_density.mean()),brier=float(((g.p_dem-(g.actual>0))**2).mean()),
            coverage70=float((e.abs()<=1.0364333894937898*g.posterior_sd_pp).mean()),coverage95=float((e.abs()<=1.959963984540054*g.posterior_sd_pp).mean())))
    cycles=pd.DataFrame(cycles);cycles.to_parquet(out/'cycle_scores.parquet',index=False)
    paired=cycles.merge(cycles[cycles.method.eq('fixed')][['scenario','cycle','prior_model','recipe','mae_pp','correct','marginal_nll']],on=['scenario','cycle','prior_model','recipe'],suffixes=('','_fixed'),validate='many_to_one')
    for k in ['mae_pp','correct','marginal_nll']:paired['delta_'+k]=paired[k]-paired[k+'_fixed']
    paired.to_parquet(out/'paired_cycle_changes.parquet',index=False)
    base=p[p.model.eq('existing_fixed')][['scenario','prior_model','target_id','prediction_pp']]
    changed=p.merge(base,on=['scenario','prior_model','target_id'],suffixes=('','_reference'),validate='many_to_one')
    changed=changed[((changed.prediction_pp>0)!=(changed.prediction_pp_reference>0))&changed.actual.notna()].copy()
    changed['was_correct']=(changed.prediction_pp_reference>0)==(changed.actual>0)
    changed['now_correct']=(changed.prediction_pp>0)==(changed.actual>0)
    changed['actual_pp']=100*changed.actual
    changed[['scenario','cycle','geography','prior_model','model','actual_pp','prediction_pp_reference','prediction_pp','was_correct','now_correct']].to_parquet(out/'changed_calls.parquet',index=False)
    current=p[p.cycle.eq(2026)&p.prior_model.eq('control_state')]
    table=current.pivot(index='geography',columns='model',values='prediction_pp').join(current[current.model.eq('existing_fixed')].set_index('geography')[['q_pp','prior']])
    table['prior_pp']=100*table.pop('prior');table.reset_index().to_parquet(out/'current_states.parquet',index=False)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for ax,sc in zip(axes,['matched_live','oct31']):
        g=fits[fits.scenario.eq(sc)&fits.method.eq('learned')]
        for recipe,q in g.groupby('recipe'):ax.plot(q.cycle,q.alpha,marker='o',label=recipe)
        ax.axhline(1,color='black',ls='--');ax.set_yscale('log');ax.set(title=sc,xlabel='Forecast cycle',ylabel='Fitted residual variance scale alpha');ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(out/'fitted_scales.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for ax,sc in zip(axes,['matched_live','oct31']):
        q=cal[cal.period.eq('recent_2016_2024')&cal.group.eq('all')&cal.prior_model.eq('control_state')&cal.scenario.eq(sc)].set_index('model')
        delta=[q.loc[r+'_learned','mae_pp']-q.loc[r+'_fixed','mae_pp'] for r in bias.RECIPES]
        ax.barh(list(bias.RECIPES),delta,color=['#327c9b' if d<0 else '#b95842' for d in delta]);ax.axvline(0,color='black',lw=.8)
        ax.set(title=sc,xlabel='MAE change vs same bias, fixed alpha (pp)');ax.invert_yaxis()
    fig.tight_layout();fig.savefig(out/'paired_mae.png',dpi=145);plt.close(fig)
    cols=['scenario','model','n','correct','mae_pp','brier','marginal_nll','coverage70','coverage95']
    text='# Joint bias and residual scale — results\n\nFrozen September17,2026 inputs. Fit one residual covariance multiplier alpha per horizon/cycle/bias recipe, integrating the Gaussian bias coefficients. Election priors, correlation patterns, relative state residual variances and fresh-firm noise remain fixed. Whole-likelihood penalty lambda=1. This is conditional empirical Bayes, not a new free covariance fit.\n\n'
    text+='## How to interpret this experiment\n\nUnlike the earlier penalty selected on three validation cycles, alpha maximizes the integrated historical polling-error likelihood using the recipe\'s earlier training window. Its training score must improve or stay equal; held-out final-election scores need not improve. There is no new inner validation selection. Alpha uncertainty and covariance-shape estimation uncertainty are omitted. A new bias posterior is computed at alpha, so mean corrections can change as well as forecast uncertainty.\n\n'
    text+='## Review conclusion\n\nDo not promote the fitted-scale variants as probability forecasts. All90fitted scales are below1 (range0.2984–0.8907), with no boundary hits. Training fit improves, but all six reference-prior recipes have worse recent held-out marginal NLL at both horizons. Earlier margin MAE improves slightly; late MAE and winner calls are mixed. Brier scores can improve while margin-density scores and interval coverage worsen because they evaluate different predictive quantities.\n\nFor state4, learned alpha changes September MAE6.9361→6.8675 with128/140calls unchanged, and October5.2571→5.2443 with132/140unchanged. Its95%coverage falls92.86→90.71% earlier and92.14→87.86% late. Shared4 late coverage falls90.71→79.29%, while MAE worsens5.2727→5.3052. The original-bias model gains two late calls131→133 but loses95%coverage92.14→87.86%. These are not convincing calibrated replacements.\n\nThe earlier whole-likelihood penalty selected from final-election validation sometimes preferred4; the new residual-only parameter fitted to historical polling-error likelihood prefers values below1. They scale different components and use different objectives. Their disagreement illustrates a training-fit versus predictive-calibration problem, not evidence that either setting is definitively correct. Bias uncertainty is integrated, but the inherited covariance shape and scale estimates are still treated as known. Effective firm information, common-cycle residuals and forecast-horizon drift remain possible missing structure; this experiment does not identify their relative responsibility.\n\nReference current forecast remains49D/51R by calls, expected48.481D,70%47–50D. Experiments have different means and seat distributions; do not select one because its2026 result looks more plausible. State covariance can shrink while a discrete seat range widens as means move toward zero; seat quantiles are not a direct measure of individual-state SD.\n\n'
    for period in ['recent_2016_2024','all_2012_2024']:
        text+='## '+period+' — reference prior\n\n'+cal[cal.period.eq(period)&cal.group.eq('all')&cal.prior_model.eq('control_state')][cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Recent results under all frozen priors\n\n'+cal[cal.period.eq('recent_2016_2024')&cal.group.eq('all')][['prior_model']+cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Reference-prior groups\n\n'+cal[cal.period.eq('recent_2016_2024')&cal.group.ne('all')&cal.prior_model.eq('control_state')][['group']+cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Fitted scales and boundary checks\n\n'+fits[fits.method.eq('learned')][['scenario','cycle','recipe','alpha','objective','objective_at_one','at_boundary','training_cycles','training_rows']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Paired cycle changes\n\nNegative delta MAE/NLL is improvement; positive delta correct means additional correct calls.\n\n'+paired[paired.prior_model.eq('control_state')&paired.method.eq('learned')].round(4).to_markdown(index=False)+'\n\n'
    text+='## Changed winner calls\n\n'+changed[changed.prior_model.eq('control_state')&changed.cycle.ge(2016)][['scenario','cycle','geography','model','actual_pp','prediction_pp_reference','prediction_pp','was_correct','now_correct']].round(3).to_markdown(index=False)+'\n\n'
    text+='## Current full chamber scenarios\n\nD includes Democratic-caucusing independents. Continuing and completion seats, exceptional-ballot/scalar-outcome and candidate assumptions are retained. No October2026 forecast is invented. These are model scenarios, not new outcome observations.\n\n'+seats[seats.cycle.eq(2026)][['prior_model','model','point_D','point_R','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95']].round(3).to_markdown(index=False)+'\n\n'
    text+='## Current state margins, reference prior\n\n'+table.round(3).to_markdown()+'\n\n'
    text+='## Decision boundary\n\nNo automatic promotion. A shared residual scale does not resolve effective pollster information, dynamic common-cycle errors, election-day drift or heavy tails. The inherited covariance shape was estimated under the old bias specification from historical data; this study conditions on that estimate. Numerical bounds are fixed at1/16 and16, with any boundary hits disclosed. Historical periods are repeatedly explored, so rankings are exploratory and prospective evaluation remains important.\n'
    (out/'JOINT_POLL_ERROR_RESULTS.md').write_text(text);(lab/'JOINT_POLL_ERROR_RESULTS.md').write_text(text)
    (out/'recipe'/Path(__file__).name).write_bytes(Path(__file__).read_bytes());v1.manifest(out)
    return out


if __name__=='__main__':build(Path(__file__).resolve().parents[1])
