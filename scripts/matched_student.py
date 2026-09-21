"""Variance-matched Student surprises for the FINAL signed-factor Gaussian.

Freeze all historical fits and selections. Random inverse-gamma scales affect
national, signed-pattern, local electoral and shared polling residual variances.
Gaussian feature-coefficient uncertainty and bias/freshness noise are retained.
The nu=0 control fixes scales at one and must recover exact Gaussian moments.
"""
from math import erf
from pathlib import Path
import json
import numpy as np
import pandas as pd
from numba import njit
import election_lab as lab
from bayesian_gaussian import diagnostics
from coverage_balance import score_rows

LABEL='Matched Student-t (df5)'


@njit(cache=True)
def chain(mu,L,A,FV,h,obs,y,P,F,nu,warm,draws,seed):
    np.random.seed(seed)
    n=len(mu);k=len(obs)
    sn=1.;sz=1.;sp=1.;sl=np.ones(n)
    active_signed=np.any(h!=0.)
    trace=np.empty((draws,2*n+k+8))
    means=np.zeros(n);second=np.zeros((n,n));prob=np.zeros(n)
    for it in range(warm+draws):
        lv=L*sl;rv=P*sp+F;g=A*sn+FV
        # Exact two-factor conditional after integrating state-local residuals.
        s00=0.;s01=0.;s11=0.;r0=0.;r1=0.
        for j in range(k):
            i=obs[j];precision=1/(lv[i]+rv[j]);residual=y[j]-mu[i]
            s00+=precision;s01+=h[i]*precision;s11+=h[i]*h[i]*precision
            r0+=residual*precision;r1+=h[i]*residual*precision
        det=(1+g*s00)*(1+sz*s11)-g*sz*s01*s01
        c00=g*(1+sz*s11)/det;c11=sz*(1+g*s00)/det;c01=-g*sz*s01/det
        m0=c00*r0+c01*r1;m1=c01*r0+c11*r1
        if c00>0:
            u=np.random.normal();N=m0+np.sqrt(c00)*u
            Z=m1+c01/np.sqrt(c00)*u+np.sqrt(max(0.,c11-c01*c01/c00))*np.random.normal()
        else:N=m0;Z=m1+np.sqrt(c11)*np.random.normal()
        delta=np.empty(n);gain=np.zeros(n);local_cond=lv.copy();cm=mu+m0+h*m1
        for i in range(n):delta[i]=np.sqrt(lv[i])*np.random.normal()
        for j in range(k):
            i=obs[j];gain[i]=lv[i]/(lv[i]+rv[j]);local_cond[i]=lv[i]*(1-gain[i])
            delta[i]=gain[i]*(y[j]-mu[i]-N-h[i]*Z)+np.sqrt(local_cond[i])*np.random.normal()
            cm[i]+=gain[i]*(y[j]-mu[i]-m0-h[i]*m1)
        theta=mu+N+h*Z+delta
        national_residual=(A*sn/g)*N+np.sqrt(A*sn*FV/g)*np.random.normal() if g>0 else 0.
        feature_uncertainty=N-national_residual
        ep=np.empty(k)
        for j in range(k):
            v=P[j]*sp;pg=v/(v+F[j])
            ep[j]=pg*(y[j]-theta[obs[j]])+np.sqrt(v*(1-pg))*np.random.normal()
        if it>=warm:
            t=it-warm
            trace[t,:n]=theta
            trace[t,n:n+7]=np.array([N,national_residual,feature_uncertainty,Z,np.log(sn),np.log(sz),np.log(sp)])
            trace[t,n+7:2*n+7]=np.log(sl)
            trace[t,2*n+7:2*n+7+k]=ep
            trace[t,-1]=np.sum(theta>0)
            means+=cm
            # Rao-Blackwellize moments/probabilities over the Gaussian conditional.
            for i in range(n):
                wi=1-gain[i]
                var=local_cond[i]+wi*wi*(c00+2*h[i]*c01+h[i]*h[i]*c11)
                prob[i]+=.5*(1+erf(cm[i]/np.sqrt(2*var)))
                for j in range(n):
                    cov=wi*(1-gain[j])*(c00+(h[i]+h[j])*c01+h[i]*h[j]*c11)
                    second[i,j]+=cm[i]*cm[j]+cov+(local_cond[i] if i==j else 0.)
        if nu>0:
            sn=1/np.random.gamma((nu+1)/2,2/((nu-2)+national_residual**2/A)) if A>0 else 1.
            sz=1/np.random.gamma((nu+1)/2,2/((nu-2)+Z*Z)) if active_signed else 1.
            for i in range(n):
                if i in obs:sl[i]=1/np.random.gamma((nu+1)/2,2/((nu-2)+delta[i]**2/L[i]))
                else:sl[i]=1/np.random.gamma(nu/2,2/(nu-2))
            sp=1/np.random.gamma((nu+k)/2,2/((nu-2)+np.sum(ep*ep/P)))
    return trace,means/draws,second/draws,prob/draws


def sample(mu,L,A,FV,h,obs,y,P,F,nu=5,seed=1,warmup=2000,draws=4000,chains=8,check=True):
    mu,L,h,y,P,F=[np.asarray(v,float) for v in [mu,L,h,y,P,F]]
    obs=np.asarray(obs,np.int64);n=len(mu)
    if len(L)!=n or len(h)!=n or len(y)!=len(obs) or len(P)!=len(obs) or len(F)!=len(obs):raise ValueError('Mismatched shapes')
    if not all(np.isfinite(v).all() for v in [mu,L,h,y,P,F]) or np.any(L<=0) or np.any(P<=0) or np.any(F<=0) or A<0 or FV<0:raise ValueError('Invalid variances or inputs')
    if nu!=0 and nu<=2:raise ValueError('Finite-variance Student requires df>2')
    if len(set(obs))!=len(obs) or np.any(obs<0) or np.any(obs>=n):raise ValueError('Invalid observation mapping')
    for attempt in range(4):
        runs=[chain(mu,L,float(A),float(FV),h,obs,y,P,F,float(nu),warmup,draws,seed+c*7919) for c in range(chains)]
        traces=np.stack([r[0] for r in runs])
        names=[f'margin_{i}' for i in range(n)]+['national_total','national_residual','feature_uncertainty','signed_pattern','log_national_scale','log_signed_scale','log_poll_scale']+[f'log_local_scale_{i}' for i in range(n)]+[f'poll_error_{i}' for i in obs]+['contested_D_count']
        varying=np.ptp(traces.reshape(-1,traces.shape[-1]),axis=0)>1e-12
        diag=diagnostics(traces[:,:,varying],[s for s,v in zip(names,varying) if v])
        good=diag.rhat.max()<1.01 and min(diag.bulk_ess.min(),diag.tail_ess.min())>=400
        if good or not check:break
        print('Extending MCMC',nu,attempt,'Rhat',diag.rhat.max(),'ESS',min(diag.bulk_ess.min(),diag.tail_ess.min()),flush=True)
        warmup*=2;draws*=2
    else:raise RuntimeError('Matched Student convergence failed')
    mean=np.mean([r[1] for r in runs],axis=0)
    cov=np.mean([r[2] for r in runs],axis=0)-np.outer(mean,mean)
    return dict(mean=mean,covariance=cov,p_dem=np.mean([r[3] for r in runs],axis=0),
                samples=traces[:,:,:n].reshape(-1,n),diagnostics=diag,warmup=warmup,draws=draws,chains=chains,seed=seed,
                trace_names=np.array(names),trace_quantiles=np.quantile(traces.reshape(-1,traces.shape[-1]),[.025,.5,.975],axis=0))


def inputs(q,fit,lam,poll):
    ids=np.array([lab.gaussian.STATES.index(s) for s in q.geography])
    obs=np.flatnonzero(q.q_pp.notna());oi=ids[obs]
    z=fit['z'];A=float(fit['a']);FV=float(z@fit['beta_covariance']@z)
    h=np.sqrt(lam)*fit['loading'][ids];L=fit['budget'][ids]-A-h*h
    mu=100*q.prior.to_numpy()+float(z@fit['beta_mean'])
    P=poll['covariance'][np.ix_(oi,oi)];B=poll['bias_covariance'][np.ix_(oi,oi)]
    if not np.allclose(P,np.diag(np.diag(P))) or not np.allclose(B,np.diag(np.diag(B))):raise ValueError('Expected diagonal polling covariance')
    y=q.q_pp.to_numpy()[obs]-poll['bias_mean'][oi]
    return mu,L,A,FV,h,obs,y,np.diag(P),np.diag(B)+16/q.firm_mass.to_numpy()[obs]


def control(args):
    mu,L,A,FV,h,obs,y,P,F=args
    K=np.diag(L)+(A+FV)*np.ones((len(mu),len(mu)))+np.outer(h,h)
    return lab.gaussian.normal_update(mu,K,obs,y,np.diag(P+F))[:2],K


def scored(q,result):
    p=q[['scenario','cycle','target_id','geography','special','actual','q_pp','firm_mass','history_selection_10pp']].copy()
    p['model']=LABEL;p['prediction_pp']=result['mean'];p['prediction']=result['mean']/100
    p['median_pp']=np.median(result['samples'],axis=0);p['posterior_sd_pp']=np.sqrt(np.diag(result['covariance']));p['p_dem']=result['p_dem']
    for level in [50,70,80,95]:
        p[f'lo{level}_pp'],p[f'hi{level}_pp']=np.quantile(result['samples'],[(1-level/100)/2,(1+level/100)/2],axis=0)
    p=score_rows(p);p['margin_pp']=p.prediction_pp;p['sigma_pp']=p.posterior_sd_pp;p['actual_pp']=100*p.actual
    p['probability_correct']=np.where(p.actual.notna(),p.p_dem.gt(.5).eq(p.actual.gt(0)),np.nan)
    return p


def run(include_live=True,force=False):
    """Frozen 2012–2024 paired hindcasts, frozen2026, and latest saved live2026.

No downloads or fitting/tuning. Content-keyed completed runs may be reused.
"""
    from scipy.stats import norm
    live=lab.latest_run('live') if include_live else None
    inputs_paths=[lab.ROOT/'election_lab.py',lab.ASSETS/'main/predictions.parquet',lab.ASSETS/'main/folds.parquet']
    inputs_paths+=sorted((lab.ROOT/'scripts').glob('*.py'))+sorted(p for p in (lab.ROOT/'config').glob('*') if p.is_file())
    inputs_paths+=sorted((lab.ASSETS/'main').rglob('*.npz'))+sorted((lab.ASSETS/'poll').rglob('*.npz'))
    if live:inputs_paths += [live/'manifest.json',lab.ASSETS/'training/calendars.parquet']
    hashes={str(p.relative_to(lab.ROOT)):lab.sha(p) for p in inputs_paths}
    config=dict(df=5,chains=8,warmup=2000,draws_per_chain=4000,variance_multiplier=1.,seed=lab.SEED)
    key=__import__('hashlib').sha256(json.dumps(dict(hashes=hashes,config=config),sort_keys=True).encode()).hexdigest()
    index=lab.ROOT/'cache/matched_student'/f'{key}.json'
    if index.exists() and not force:
        cached=json.loads(index.read_text());out=lab.ROOT/cached['run']
        if lab.sha(out/'manifest.json')!=cached['manifest_sha256']:raise ValueError('Matched cache changed')
        print('Verified cached matched Student run',out.name,flush=True);return lab.verify_run(out)
    out=lab.new_run('matched_student');(out/'forecasts').mkdir()
    folds=pd.read_parquet(lab.ASSETS/'main/folds.parquet')
    baseline=pd.read_parquet(lab.ASSETS/'main/predictions.parquet')
    refs=pd.read_parquet(lab.ASSETS/'main/seats.parquet')
    predictions=[];seat_rows=[];diags=[];checks=[]
    cases=[]
    for r in folds.itertuples():
        q=baseline[baseline.scenario.eq(r.scenario)&baseline.cycle.eq(r.cycle)].sort_values('target_id').reset_index(drop=True)
        f=dict(np.load(lab.ASSETS/'main'/r.fit_path));f['a']=float(f['a'])
        expected=dict(np.load(lab.ASSETS/'main'/r.forecast_path))
        cases.append(('frozen',r,q,f,expected))
    if live:
        q=pd.read_parquet(live/'predictions.parquet').query('model=="Bayesian"').sort_values('target_id').reset_index(drop=True)
        r=next(r for r in folds.itertuples() if r.scenario=='matched_live' and r.cycle==2026)
        f=dict(np.load(lab.ASSETS/'main'/r.fit_path));f['a']=float(f['a'])
        cal=pd.read_parquet(lab.ASSETS/'training/calendars.parquet').query('scenario=="matched_live"').copy()
        ctx=pd.read_parquet(live/'feature_context.parquet')
        for c in ctx:cal.loc[cal.cycle.eq(2026),c]=ctx[c].iloc[0]
        design,_,z,*_=lab.features.prepare_design(cal,f['years'],f['training_weights'],2026)
        f['z']=z[[design.active.index(t) for t in f['terms']]]
        cases.append(('live',r,q,f,dict(np.load(live/'main_joint.npz'))))
    for evidence,r,q,f,expected in cases:
        year=int(r.cycle);sc=r.scenario
        assert f['years'].max()<year
        args=inputs(q,f,float(r.lambda_value),lab.load_poll(sc,year))
        (gm,gc),K=control(args)
        np.testing.assert_allclose(gm,expected['mean'],atol=1e-8)
        np.testing.assert_allclose(gc,expected['covariance'],atol=1e-8)
        np.testing.assert_allclose(K,expected['prior_covariance'],atol=1e-8)
        c=sample(*args,nu=0,seed=31,warmup=0,draws=32,chains=2,check=False)
        np.testing.assert_allclose(c['mean'],gm,atol=1e-8)
        np.testing.assert_allclose(c['covariance'],gc,atol=1e-8)
        np.testing.assert_allclose(c['p_dem'],norm.cdf(gm/np.sqrt(np.diag(gc))),atol=1e-10)
        seed=lab.SEED+year+10000*(sc=='oct31')
        result=sample(*args,nu=5,seed=seed)
        sp=scored(q,result);sp['evidence']=evidence
        gp=lab.scored(q,'Bayesian');gp['evidence']=evidence
        predictions.extend([gp,sp]);ref=refs[refs.scenario.eq(sc)&refs.cycle.eq(year)].iloc[0]
        gd=gm+np.random.default_rng(seed).standard_normal((30000,len(q)))@np.linalg.cholesky(gc).T
        gs,gfreq=lab.seat_row(gp,gd,'Bayesian',ref)
        ts,tfreq=lab.seat_row(sp,result['samples'],LABEL,ref,'Matched componentwise Student MCMC')
        from coverage_balance import seat_scores
        for row,freq in [(gs,gfreq),(ts,tfreq)]:
            row['expected_D_exact']=row['expected_D'];row=seat_scores(row,freq);row['evidence']=evidence;seat_rows.append(row)
        diag=result['diagnostics'].assign(evidence=evidence,scenario=sc,cycle=year);diags.append(diag)
        checks.append(dict(evidence=evidence,scenario=sc,cycle=year,prior_matched=True,gaussian_control=True,training_max_cycle=int(f['years'].max()),df=5,
                           chains=result['chains'],draws_per_chain=result['draws'],warmup=result['warmup'],max_rhat=float(diag.rhat.max()),min_ess=float(min(diag.bulk_ess.min(),diag.tail_ess.min()))))
        np.savez_compressed(out/'forecasts'/f'{evidence}_{sc}_{year}.npz',mean=result['mean'],covariance=result['covariance'],p_dem=result['p_dem'],
                            prior_mean=args[0],prior_covariance=K,gaussian_mean=gm,gaussian_covariance=gc,target_ids=q.target_id.to_numpy(str),
                            seat_count_frequency=tfreq,trace_names=result['trace_names'],trace_quantiles=result['trace_quantiles'])
        print(evidence,sc,year,'Rhat',round(diag.rhat.max(),4),'ESS',round(min(diag.bulk_ess.min(),diag.tail_ess.min())),flush=True)
    p=pd.concat(predictions,ignore_index=True);s=pd.DataFrame(seat_rows)
    cyc,summary=lab.summarize(p[p.evidence.eq('frozen')])
    for name,tab in dict(predictions=p,seats=s,cycle_scores=cyc,summary=summary,diagnostics=pd.concat(diags),checks=pd.DataFrame(checks)).items():tab.to_parquet(out/(name+'.parquet'),index=False)
    lab.finish(out,dict(kind='matched_final_gaussian_student',config=config,sources=hashes,source_live=str(live.relative_to(lab.ROOT)) if live else None,
                       live_metadata=json.loads((live/'run.json').read_text()) if live else None,checks=checks,
                       calibration='Frozen historical Gaussian fits and chronological selections; no Student retuning',
                       changed='df5 variance-standardized national/signed/local electoral scales and common polling scale',
                       retained='centers, loadings, variance budgets, feature fit/uncertainty, historical poll bias and Gaussian extra observation noise',
                       promotion=False))
    lab.write_json(index,dict(run=str(out.relative_to(lab.ROOT)),manifest_sha256=lab.sha(out/'manifest.json')))
    return out
