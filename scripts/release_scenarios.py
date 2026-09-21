"""Transparent current-forecast sensitivity, without refitting or new downloads.

wave_pp is an additional D-minus-R final-margin shift, applied after inference.
poll_error_pp is polls minus truth: positive values overstate Democratic support.
Deterministic errors shift current likelihood means through the exact Gaussian
update. Random errors are extra stress uncertainty, not calibrated replacements.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm
import election_lab as lab


def responses(q, prior_covariance, posterior_covariance):
    """Return observation indices and exact d(posterior mean)/d(poll margin)."""
    obs=np.flatnonzero(q.q_pp.notna())
    state_ids=np.array([lab.gaussian.STATES.index(s) for s in q.geography])[obs]
    poll=lab.load_poll('matched_live',2026)
    R=(poll['covariance'][np.ix_(state_ids,state_ids)]
       +poll['bias_covariance'][np.ix_(state_ids,state_ids)]
       +np.diag(16/q.firm_mass.to_numpy()[obs]))
    K=prior_covariance
    gain=np.linalg.solve(K[np.ix_(obs,obs)]+R,K[:,obs].T).T
    np.testing.assert_allclose(K-gain@K[obs,:],posterior_covariance,atol=1e-8)
    return obs,gain,R


def summarize(mean, covariance, residual_draws, fixed_D):
    """Analytic marginal probabilities; paired joint simulation for chamber."""
    sd=np.sqrt(np.diag(covariance));p=norm.cdf(mean/sd)
    counts=fixed_D+(residual_draws+mean>0).sum(axis=1)
    lo,hi=np.quantile(counts,[.15,.85],method='inverted_cdf')
    control=float(np.mean(counts>=51));point=fixed_D+int((mean>0).sum())
    return dict(point_D=point,point_R=100-point,expected_D=float(fixed_D+p.sum()),
                expected_R=float(100-fixed_D-p.sum()),p_D_control=control,
                D_lo70=int(lo),D_hi70=int(hi),control_mc_se=float(np.sqrt(control*(1-control)/len(counts)))),p,sd


def run(source=None, waves=range(11), errors=range(-5,6), weights=(0.,.2,.5),
        random_sigmas=(1.,2.,3.), draws=30000):
    """Use latest verified live run. Run notebook04 first to refresh evidence."""
    if draws<1000:raise ValueError('Use at least 1,000 chamber draws')
    if any(not 0<=w<=1 for w in weights):raise ValueError('Blend weights must be in [0,1]')
    if any(s<=0 for s in random_sigmas):raise ValueError('Random error SD must be positive')
    source=lab.latest_run('live') if source is None else lab.verify_run(Path(source))
    import json
    meta=json.loads((source/'run.json').read_text())
    all_rows=pd.read_parquet(source/'predictions.parquet')
    q=all_rows[all_rows.model.eq('Bayesian')].sort_values('target_id').reset_index(drop=True)
    nb=all_rows[all_rows.model.eq('Non-Bayesian corrected')].set_index('target_id').loc[q.target_id]
    joint=np.load(source/'main_joint.npz');C=joint['covariance'];K=joint['prior_covariance']
    assert list(joint['target_ids'])==list(q.target_id)
    np.testing.assert_allclose(q.margin_pp,joint['mean'],atol=1e-10)
    obs,G,R=responses(q,K,C)
    history=pd.read_parquet(lab.ASSETS/'training/history.parquet')
    selected=history[history.cycle.eq(2026)&history.scenario.eq('matched_live')]
    # Both current aggregators have 30-day decay and identical admitted samples.
    # A uniform per-state shift survives weighting; no-poll history stays fixed.
    half=float(selected.poll_half_life.iloc[0]);strength=float(selected.poll_prior_strength.iloc[0])
    if half!=30.:raise ValueError('Update helper response for a different polling half-life')
    B=np.zeros_like(G)
    mass=q.firm_mass.to_numpy()[obs]
    B[obs,np.arange(len(obs))]=mass/(mass+strength)
    fixed=int(pd.read_parquet(source/'seats.parquet').query('model == "Bayesian"').fixed_D.iloc[0])
    seed=lab.SEED+2026
    residuals=np.random.default_rng(seed).standard_normal((draws,len(q)))@np.linalg.cholesky(C).T
    # Reuse residuals and random shocks across models for paired comparisons.
    rng=np.random.default_rng(seed+919)
    common=rng.standard_normal((draws,1));independent=rng.standard_normal((draws,len(obs)))
    rows=[];states=[];checks=[];maps=[]
    out=lab.new_run('scenarios')
    for weight in weights:
        model='Bayesian' if weight==0 else f'Corrected {100*weight:g}%'
        mu=(1-weight)*q.margin_pp.to_numpy()+weight*nb.margin_pp.to_numpy()
        T=(1-weight)*G+weight*B
        sensitivity=T@np.ones(len(obs))
        maps.append(pd.DataFrame(dict(target_id=q.target_id,geography=q.geography,model=model,
                                     has_poll=q.q_pp.notna(),mean_pp=mu,poll_error_response_pp_per_pp=-sensitivity)))
        def save(wave,error,mode='none',sigma=0.):
            mean=mu+wave-error*sensitivity
            if mode=='shared':
                shock=-sigma*common*sensitivity[None,:]
                cov=C+sigma**2*np.outer(sensitivity,sensitivity)
            elif mode=='independent':
                shock=-sigma*independent@T.T;cov=C+sigma**2*T@T.T
            else:shock=0.;cov=C
            seat,p,sd=summarize(mean,cov,residuals+shock,fixed)
            keys=dict(model=model,blend_weight=weight,wave_pp=float(wave),poll_error_pp=float(error),random_mode=mode,random_sd_pp=float(sigma))
            rows.append(dict(**keys,**seat))
            state=pd.DataFrame(dict(target_id=q.target_id,geography=q.geography,margin_pp=mean,p_dem=p,
                                    sd_pp=sd,lo70_pp=mean-norm.ppf(.85)*sd,hi70_pp=mean+norm.ppf(.85)*sd))
            for key,value in keys.items():state[key]=value
            states.append(state)
            return seat
        for wave in waves:
            for error in errors:save(wave,error)
        for sigma in random_sigmas:
            for mode in ['shared','independent']:
                for wave in [0,2,4,6,8,10]:save(wave,0,mode,sigma)
        # Zero stress must reproduce stored outputs, not merely be plausible.
        baseline,_p,_sd=summarize(mu,C,residuals,fixed)
        saved=pd.read_parquet(source/'seats.parquet')
        if model in set(saved.model) and draws==lab.DRAWS:
            ref=saved[saved.model.eq(model)].iloc[0]
            for key in ['point_D','expected_D','p_D_control','D_lo70','D_hi70']:
                np.testing.assert_allclose(baseline[key],ref[key],atol=1e-10)
        # A finite-difference likelihood refit must match the response matrix.
        value=q.q_pp.to_numpy()[obs]-lab.load_poll('matched_live',2026)['bias_mean'][np.array([lab.gaussian.STATES.index(s) for s in q.geography])[obs]]
        prior=joint['prior_mean'];actual,check_cov,_=lab.gaussian.normal_update(prior,K,obs,value-1,R)
        np.testing.assert_allclose(check_cov,C,atol=1e-8)
        np.testing.assert_allclose(actual,joint['mean']-G.sum(axis=1),atol=1e-8)
        checks.append(dict(model=model,zero_stress_reproduced=True,gaussian_response_verified=True))
    seats=pd.DataFrame(rows);state_rows=pd.concat(states,ignore_index=True)
    # Uniform extra final-margin waves cannot reduce any state's win probability.
    for _,g in seats[seats.random_mode.eq('none')].groupby(['model','poll_error_pp']):
        assert (np.diff(g.sort_values('wave_pp').expected_D)>=-1e-10).all()
        assert (np.diff(g.sort_values('wave_pp').p_D_control)>=-1e-10).all()
    seats.to_parquet(out/'seats.parquet',index=False);seats.to_csv(out/'seats.csv',index=False)
    state_rows.to_parquet(out/'states.parquet',index=False)
    pd.concat(maps,ignore_index=True).to_csv(out/'poll_sensitivity.csv',index=False)
    return lab.finish(out,dict(kind='scenario_stress_test',source=str(source.relative_to(lab.ROOT)),
                              source_manifest_sha256=lab.sha(source/'manifest.json'),as_of=meta['as_of'],
                              freshness=meta['freshness'],draws=draws,seed=seed,weights=list(weights),
                              waves=list(waves),poll_errors=list(errors),random_sigmas=list(random_sigmas),checks=checks,
                              wave_definition='Additional final D-minus-R margin pp, after inference; not conditioning on latent N',
                              error_definition='Extra polls-minus-truth pp beyond learned bias; positive overstates Democrats',
                              random_definition='Extra zero-mean Gaussian stress, not a calibrated replacement for existing uncertainty',
                              refit=False,new_downloads=False))
