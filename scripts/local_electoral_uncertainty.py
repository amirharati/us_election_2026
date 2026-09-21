"""Independent local Student priors conditional on one Gaussian national factor."""
import numpy as np
from scipy.special import gammaln,logsumexp,roots_hermitenorm,ndtr
from scipy.stats import norm
from scipy.optimize import brentq
import simple_bayesian_polling as v1
import coverage_balance as scoring


def local_fit(test,mu,local,g,poll,df,national_nodes=65,scale_nodes=225,bound=28.,intervals=True):
    if df<=2:raise ValueError('Student df must exceed two')
    local=np.asarray(local,float);mu=np.asarray(mu,float)
    if g<0 or (local<=0).any():raise ValueError('Invalid prior variances')
    n=len(test);obs=test.q_pp.notna().to_numpy();si=np.array([v1.STATES.index(x) for x in test.geography]);bias=poll['bias_mean'][si]
    P=poll['covariance'][np.ix_(si,si)]+poll['bias_covariance'][np.ix_(si,si)]
    if not np.allclose(P,np.diag(np.diag(P))):raise ValueError('Independent polling likelihood required')
    R=np.diag(P).copy();R[obs]+=16/test.firm_mass.to_numpy()[obs]
    y=test.q_pp.to_numpy()-bias;field=mu-100*test.prior.to_numpy();f=float(field.mean());base=mu-f
    if not np.allclose(field,f):raise ValueError('Shared national mean required')
    # Shift the Gaussian quadrature proposal toward the Gaussian posterior;
    # use up to twice the Gaussian posterior SD, capped at the prior SD,
    # for efficient coverage; correct the proposal by its density ratio.
    precision=np.sum(1/(local[obs]+R[obs]));rhs=np.sum((y[obs]-mu[obs])/(local[obs]+R[obs]));proposal_mean=f+(g/(1+g*precision))*rhs
    if g>0:
        proposal_sd=np.sqrt(min(g,4*g/(1+g*precision)))
        roots,weights=roots_hermitenorm(national_nodes);N=proposal_mean+proposal_sd*roots
        ln=np.log(weights)-.5*np.log(2*np.pi)+norm.logpdf(N,f,np.sqrt(g))-norm.logpdf(N,proposal_mean,proposal_sd)
    else:N=np.array([f]);ln=np.array([0.])
    z=np.linspace(-bound,bound,scale_nodes);scales=np.exp(z);shape=df/2;rate=(df-2)/2
    ls=shape*np.log(rate)-gammaln(shape)-shape*z-rate/scales+np.log(z[1]-z[0]);ls[[0,-1]]-=np.log(2)
    lv=scales[:,None]*local[None,:];prior_center=base[None,None,:]+N[:,None,None]
    # Conditional independent local updates and their scale evidences.
    cm=np.broadcast_to(prior_center,(len(N),scale_nodes,n)).copy();cv=np.broadcast_to(lv[None,:,:],cm.shape).copy();ll=np.zeros_like(cm)
    if obs.any():
        S=lv[:,obs]+R[obs];delta=y[obs][None,None,:]-prior_center[:,:,obs]
        gain=lv[:,obs]/S;cm[:,:,obs]+=gain[None,:,:]*delta;cv[:,:,obs]=lv[:,obs]*R[obs]/S
        ll[:,:,obs]=-.5*(np.log(2*np.pi*S)[None,:,:]+delta**2/S[None,:,:])
    raw=ll+ls[None,:,None];evidence=logsumexp(raw,axis=1);cw=np.exp(raw-evidence[:,None,:])
    lN=ln+evidence[:,obs].sum(axis=1);log_evidence=float(logsumexp(lN));nw=np.exp(lN-log_evidence)
    conditional_mean=np.sum(cw*cm,axis=1);conditional_var=np.sum(cw*(cv+(cm-conditional_mean[:,None,:])**2),axis=1)
    mean=nw@conditional_mean;cov=np.diag(nw@conditional_var)+(conditional_mean-mean).T@(nw[:,None]*(conditional_mean-mean))
    mw=cw*nw[:,None,None];sd=np.sqrt(cv);prob=np.sum(mw*ndtr(cm/sd),axis=(0,1))
    p=test.copy();p['prediction_pp']=mean;p['prediction']=mean/100;p['p_dem']=prob;p['posterior_sd_pp']=np.sqrt(np.diag(cov))
    nm=float(nw@N);p['national_movement_pp']=nm;p['local_electoral_update_pp']=mean-100*p.prior-nm
    p['historical_bias_pp']=bias;p['corrected_poll_pp']=p.q_pp-bias;p['feature_shifted_prior_pp']=mu
    with np.errstate(divide='ignore'):p['log_predictive_density']=logsumexp(np.log(mw)+norm.logpdf(100*p.actual.to_numpy()[None,None,:],cm,sd),axis=(0,1))
    if intervals:
        quantiles=[('median_pp',.5)]+[(f'{side}{level}_pp',(1-level/100)/2 if side=='lo' else (1+level/100)/2) for level in scoring.LEVELS for side in ['lo','hi']]
        for name,probability in quantiles:
            vals=[]
            for j in range(n):
                w=mw[:,:,j].ravel();m=cm[:,:,j].ravel();s=sd[:,:,j].ravel();width=20*np.sqrt(cov[j,j]);lo=mean[j]-width;hi=mean[j]+width
                fun=lambda x:float(w@ndtr((x-m)/s))-probability
                while fun(lo)>0 or fun(hi)<0:width*=2;lo=mean[j]-width;hi=mean[j]+width
                vals.append(brentq(fun,lo,hi,xtol=1e-9))
            p[name]=vals
        p=scoring.score_rows(p)
    d=dict(mean=mean,covariance=cov,N=N,nw=nw,cm=cm,cv=cv,cw=cw,log_evidence=log_evidence,national_mean=nm,national_sd=float(np.sqrt(nw@((N-nm)**2))),prior_scale_mass=float(np.exp(logsumexp(ls))),prior_scale_mean=float(np.exp(logsumexp(ls+z))),national_edge_mass=float(nw[:2].sum()+nw[-2:].sum()) if len(nw)>4 else 0.,scale_edge_mass=float(np.max(cw[:,:2,:].sum(axis=1)+cw[:,-2:,:].sum(axis=1))))
    return p,d


def sample(d,z,un,us):
    ids=np.minimum(np.searchsorted(np.cumsum(d['nw']),un),len(d['nw'])-1);draws=np.empty_like(z)
    for i in np.unique(ids):
        sel=np.flatnonzero(ids==i)
        for j in range(z.shape[1]):
            k=np.minimum(np.searchsorted(np.cumsum(d['cw'][i,:,j]),us[sel,j]),d['cw'].shape[1]-1)
            draws[sel,j]=d['cm'][i,k,j]+np.sqrt(d['cv'][i,k,j])*z[sel,j]
    return draws
