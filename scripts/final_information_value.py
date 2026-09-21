"""Expected information about control from a hypothetical final-margin measurement.

This auxiliary observation has independent, explicitly nonzero error for the
noisy cases. It is not the original model's likelihood for a real future poll.
"""
import numpy as np
import pandas as pd
from scipy.stats import norm, qmc
from scipy.special import xlogy
from numpy.polynomial.legendre import leggauss


def entropy(p):
    p=np.clip(np.asarray(p),0,1)
    return -(xlogy(p,p)+xlogy(1-p,1-p))/np.log(2)


def quadrature(mean_i, variance_i, noise_variance, order=24):
    """Integrate over measurement CDF; split at zero conditional state mean.

    The split integrates the known-state winner discontinuity exactly when
    observation noise is zero. Endpoints never feed infinities to norm.ppf.
    """
    S=variance_i+noise_variance
    cut=float(norm.cdf(-mean_i*np.sqrt(S)/variance_i))
    x,w=leggauss(order);nodes=[];weights=[]
    for lo,hi in [(0.,cut),(cut,1.)]:
        if hi-lo<1e-14:continue
        u=lo+(x+1)*(hi-lo)/2
        nodes.extend(norm.ppf(np.clip(u,1e-15,1-1e-15)))
        weights.extend(w*(hi-lo)/2)
    return np.asarray(nodes),np.asarray(weights)


def one_state(mu,C,noise,extra,i,measurement_sd,baseline_p,baseline_variance,order=24):
    variance=float(C[i,i]);S=variance+measurement_sd**2;gain=C[:,i]/S
    posterior_cov=C-np.outer(C[:,i],C[i,:])/S
    np.testing.assert_allclose(posterior_cov,posterior_cov.T,atol=1e-12)
    assert np.linalg.eigvalsh(posterior_cov).min()>-1e-8
    residual=noise-(noise[:,i]+measurement_sd*extra)[:,None]*gain
    if measurement_sd==0:residual[:,i]=0.
    z,w=quadrature(mu[i],variance,measurement_sd**2,order)
    assert abs(w.sum()-1)<1e-12
    post_sd=np.sqrt(np.maximum(np.diag(posterior_cov),0))
    e_entropy=e_var=e_control=e_seats=e_second=0.
    for zi,wi in zip(z,w):
        m=mu+gain*np.sqrt(S)*zi
        counts=34+(residual+m>0).sum(axis=1)
        p=float((counts>=51).mean());e_control+=wi*p
        e_entropy+=wi*float(entropy(p));e_var+=wi*float(counts.var())
        probabilities=norm.cdf(np.divide(m,post_sd,out=np.zeros_like(m),where=post_sd>1e-10))
        probabilities[post_sd<=1e-10]=(m[post_sd<=1e-10]>0)
        e_seats+=wi*(34+probabilities.sum())
        e_second+=wi*float(counts.mean()**2)
    return dict(control_entropy_before=float(entropy(baseline_p)),control_entropy_after=e_entropy,
        information_bits=float(entropy(baseline_p))-e_entropy,
        seat_variance_before=baseline_variance,seat_variance_after=e_var,
        seat_variance_reduction=baseline_variance-e_var,
        averaged_control_probability=e_control,baseline_control_probability=baseline_p,
        control_recovery_error=e_control-baseline_p,
        averaged_expected_D=e_seats,exact_expected_D=float(34+norm.cdf(mu/np.sqrt(np.diag(C))).sum()),
        mean_recovery_error=e_seats-float(34+norm.cdf(mu/np.sqrt(np.diag(C))).sum()))


def run(out,cache,power=13,order=24):
    q,mean,C,blend,_,poll,si=cache[('matched_live',2026)]
    # A floor includes historical systematic poll error, bias uncertainty, and
    # one fresh firm's noise; the lower-quality case doubles the effective SD.
    sd=float(np.median(np.sqrt(np.diag(poll['covariance'])[si]+np.diag(poll['bias_covariance'])[si]+16)))
    quality=[('perfect_final_margin',0.),('calibrated_error_floor',sd),('twice_error_floor',2*sd)]
    z=norm.ppf(qmc.Sobol(len(mean)+1,scramble=True,seed=80371).random_base2(power))
    noise=z[:,:-1]@np.linalg.cholesky(C).T;extra=z[:,-1]
    rows=[]
    for name,mu in [('Bayesian',mean),('Mean-only blend',blend)]:
        baseline=34+(mu+noise>0).sum(1);bp=float((baseline>=51).mean());bv=float(baseline.var())
        for i,r in q.iterrows():
            for label,s in quality:
                result=one_state(mu,C,noise,extra,i,s,bp,bv,order)
                rows.append(dict(model=name,state=r.geography,measurement=label,measurement_sd_pp=s,
                    marginal_sd_pp=float(np.sqrt(C[i,i])),p_dem=float(norm.cdf(mu[i]/np.sqrt(C[i,i]))),
                    polled=bool(np.isfinite(r.q_pp)),structural_proxy=r.geography in ['ID','MT','NE','SD'],
                    qmc_draws=2**power,quadrature_order_per_half=order,**result))
            print('Information',name,r.geography,flush=True)
    result=pd.DataFrame(rows)
    result['rank']=result.groupby(['model','measurement']).information_bits.rank(ascending=False,method='min')
    result.to_parquet(out/'information_value.parquet',index=False)
    # Independent scrambled repeat for the union of top-five states in each model
    # at the realistic-error benchmark. Rank changes are reported, not hidden.
    top=result[result.measurement.eq('calibrated_error_floor')&result['rank'].le(5)].state.unique()
    zz=norm.ppf(qmc.Sobol(len(mean)+1,scramble=True,seed=91647).random_base2(power+1))
    nn=zz[:,:-1]@np.linalg.cholesky(C).T;ee=zz[:,-1];repeat=[]
    for name,mu in [('Bayesian',mean),('Mean-only blend',blend)]:
        baseline=34+(mu+nn>0).sum(1);bp=float((baseline>=51).mean());bv=float(baseline.var())
        for state in top:
            i=int(q.index[q.geography.eq(state)][0])
            repeat.append(dict(model=name,state=state,measurement='calibrated_error_floor',qmc_draws=2**(power+1),
                **one_state(mu,C,nn,ee,i,sd,bp,bv,order+8)))
    repeated=pd.DataFrame(repeat);repeated.to_parquet(out/'information_repeat.parquet',index=False)
    # These tolerances cover deterministic quadrature and finite conditional QMC,
    # not model calibration. Raw discrepancies are always saved.
    assert result.control_recovery_error.abs().max()<.012
    assert result.mean_recovery_error.abs().max()<.01
    assert result.information_bits.min()>-.015
    return result
