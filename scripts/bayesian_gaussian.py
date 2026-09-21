"""Small hierarchical Gaussian Senate model; conjugate Gibbs + Gaussian conditioning.

Units throughout inference are D-R percentage points. Historical final outcomes
are observed. State movement and polling error therefore have separate likelihoods.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
import pandas as pd
from scipy.special import ndtr,ndtri,logsumexp
from scipy.stats import rankdata
from numba import njit

STATES='AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split()
DEFAULT=dict(chains=4,warmup=2500,draws=2500,thin=2,seed=260919,
             aggregation_sd_pp=3.,loading_deviation_sd_pp=2.5)

@njit(cache=True)
def gibbs_chain(si,yi,typ,res,psi,pyi,ptyp,err,noise,nstates,nyears,cfg,seed):
    np.random.seed(seed)
    warm,draws,thin=int(cfg[0]),int(cfg[1]),int(cfg[2]);ldvar=cfg[3]**2
    lam=np.ones(nstates)*(2.+seed%7);ell=5.;f=np.random.normal(0,1,nyears)
    sigma=np.full(4,100.);bias=np.random.normal(0,1,nstates);mu=0.;tb=4.
    national=np.zeros(nyears);tn=np.full(4,9.);tr=np.full(4,16.);race=np.zeros(len(err))
    # lambda_s, b_s, ell, mu_b, tau_b^2, sigma_[mid,pres]^2,
    # tau_N_[mid,pres]^2, tau_R_[mid,pres]^2
    out=np.empty((draws,2*nstates+15));j=0
    for it in range(warm+draws*thin):
        precision=np.ones(nyears);rhs=np.zeros(nyears)
        for i in range(len(res)):
            v=sigma[typ[i]];precision[yi[i]]+=lam[si[i]]**2/v;rhs[yi[i]]+=lam[si[i]]*res[i]/v
        for y in range(nyears):f[y]=rhs[y]/precision[y]+np.random.normal()/np.sqrt(precision[y])
        precision=np.ones(nstates)/ldvar;rhs=np.ones(nstates)*ell/ldvar
        for i in range(len(res)):
            v=sigma[typ[i]];precision[si[i]]+=f[yi[i]]**2/v;rhs[si[i]]+=f[yi[i]]*res[i]/v
        for s in range(nstates):lam[s]=rhs[s]/precision[s]+np.random.normal()/np.sqrt(precision[s])
        pe=nstates/ldvar+1/25.;me=lam.sum()/ldvar/pe
        ell=me+np.random.normal()/np.sqrt(pe)
        while ell<0:ell=me+np.random.normal()/np.sqrt(pe)
        for t in range(4):
            count=0;ss=0.
            for i in range(len(res)):
                if typ[i]==t:count+=1;ss+=(res[i]-lam[si[i]]*f[yi[i]])**2
            sigma[t]=1/np.random.gamma(3+count/2.,1/(200.+ss/2.))
        # Poll residual = state bias + common cycle error + race error + known noise.
        for i in range(len(err)):
            pr=1/tr[ptyp[i]]+1/noise[i];mr=(err[i]-bias[psi[i]]-national[pyi[i]])/noise[i]/pr
            race[i]=mr+np.random.normal()/np.sqrt(pr)
        precision=np.ones(nstates)/tb;rhs=np.ones(nstates)*mu/tb
        for i in range(len(err)):
            precision[psi[i]]+=1/noise[i];rhs[psi[i]]+=(err[i]-national[pyi[i]]-race[i])/noise[i]
        for s in range(nstates):bias[s]=rhs[s]/precision[s]+np.random.normal()/np.sqrt(precision[s])
        pr=nstates/tb+1/25.;mu=bias.sum()/tb/pr+np.random.normal()/np.sqrt(pr)
        tb=1/np.random.gamma(3+nstates/2.,1/(8.+((bias-mu)**2).sum()/2.))
        # Include all historical cycles, even without polls. Their unobserved B
        # draws integrate out; exclude them from the scale update for mixing.
        precision=np.zeros(nyears);rhs=np.zeros(nyears);counts=np.zeros(nyears)
        for i in range(len(err)):
            y=pyi[i];precision[y]+=1/noise[i];rhs[y]+=(err[i]-bias[psi[i]]-race[i])/noise[i];counts[y]+=1
        for y in range(nyears):
            if counts[y]>0:
                tt=0
                for i in range(len(err)):
                    if pyi[i]==y:tt=ptyp[i];break
                pp=precision[y]+1/tn[tt];national[y]=rhs[y]/pp+np.random.normal()/np.sqrt(pp)
        for t in range(4):
            count=0;ss=0.;nc=0;ns=0.
            for i in range(len(err)):
                if ptyp[i]==t:count+=1;ss+=race[i]**2
            for y in range(nyears):
                if counts[y]>0:
                    tt=0
                    for i in range(len(err)):
                        if pyi[i]==y:tt=ptyp[i];break
                    if tt==t:nc+=1;ns+=national[y]**2
            tr[t]=1/np.random.gamma(3+count/2.,1/(32.+ss/2.))
            tn[t]=1/np.random.gamma(3+nc/2.,1/(18.+ns/2.))
        # Joint location move: likelihood and b_s-mu stay unchanged; this
        # samples the global shift conditional on all relative effects.
        pr=1/25.;rhs=-mu/25.
        for y in range(nyears):
            if counts[y]>0:
                tt=0
                for i in range(len(err)):
                    if pyi[i]==y:tt=ptyp[i];break
                pr+=1/tn[tt];rhs+=national[y]/tn[tt]
        shift=rhs/pr+np.random.normal()/np.sqrt(pr)
        mu+=shift;bias+=shift
        for y in range(nyears):
            if counts[y]>0:national[y]-=shift
        if it>=warm and (it-warm)%thin==0:
            out[j,:nstates]=lam;out[j,nstates:2*nstates]=bias
            out[j,2*nstates:]=np.concatenate((np.array([ell,mu,tb]),sigma,tn,tr))
            j+=1
    return out

def prepare(history,year,config):
    tr=history[history.cycle.lt(year)&history.actual.notna()].copy()
    # No neutral first-ever prior is treated as an observed state movement.
    tr=tr[tr.prior_latest_cycle.notna()&tr.prior_latest_cycle.lt(tr.cycle)].copy()
    if tr.cycle.nunique()<8:raise ValueError('At least eight historical cycles required')
    pol=tr[tr.poll_mean.notna()&tr.n_samples.gt(0)].copy()
    if pol.cycle.nunique()<6:raise ValueError('At least six polled historical cycles required')
    years=sorted(tr.cycle.unique());lookup={s:i for i,s in enumerate(STATES)};yl={y:i for i,y in enumerate(years)}
    if not set(tr.geography)<=set(STATES):raise ValueError('Unexpected geography')
    def index(q):return q.geography.map(lookup).to_numpy(np.int64),q.cycle.map(yl).to_numpy(np.int64),(q.is_presidential_cycle.astype(int)+2*q.cycle.ge(year-10).astype(int)).to_numpy(np.int64)
    si,yi,typ=index(tr);psi,pyi,ptyp=index(pol)
    noise=config['aggregation_sd_pp']**2/np.maximum(pol.data_weight.to_numpy(float),.25)
    arrays=(si,yi,typ,100*(tr.actual-tr.prior).to_numpy(),psi,pyi,ptyp,100*(pol.poll_mean-pol.actual).to_numpy(),noise,len(STATES),len(years))
    info=dict(cycle=int(year),training_first_cycle=int(tr.cycle.min()),training_max_cycle=int(tr.cycle.max()),training_cycles=int(tr.cycle.nunique()),training_rows=len(tr),
              polled_training_cycles=int(pol.cycle.nunique()),polled_training_rows=len(pol),training_states=int(tr.geography.nunique()),
              old_rows_before_2016=int(tr.cycle.lt(2016).sum()),missing_races='unobserved, never filled with zero',historical_weighting='all older eligible observations; stable pooled loadings/bias; separate old versus last-10-year scales; no likelihood power/decay',
              state_rows=tr.groupby('geography').size().to_dict(),polled_state_rows=pol.groupby('geography').size().to_dict())
    return arrays,info

def fit(history,year,config=None):
    cfg=dict(DEFAULT if config is None else config);arrays,info=prepare(history,year,cfg)
    args=np.array([cfg['warmup'],cfg['draws'],cfg['thin'],cfg['loading_deviation_sd_pp']])
    chains=np.stack([gibbs_chain(*arrays,args,cfg['seed']+int(year)*11+c*7919) for c in range(cfg['chains'])])
    names=['loading_'+s for s in STATES]+['bias_'+s for s in STATES]+['loading_common','bias_common','bias_variance']+[component+'_'+era+'_'+kind for component in ['state_variance','national_poll_variance','race_poll_variance'] for era in ['older','recent'] for kind in ['midterm','presidential']]
    diag=diagnostics(chains,names)
    info.update(config=cfg,max_rhat=float(diag.rhat.max()),min_bulk_ess=float(diag.bulk_ess.min()),min_tail_ess=float(diag.tail_ess.min()))
    return chains,info,diag

def split(x):
    n=x.shape[1]//2
    return np.concatenate([x[:,:n],x[:,-n:]],axis=0)

def basic_rhat(x):
    n=x.shape[1];w=x.var(axis=1,ddof=1).mean();b=n*x.mean(axis=1).var(ddof=1)
    return np.sqrt(((n-1)*w/n+b/n)/w) if w>0 else 1.

def ess(x):
    m,n=x.shape;means=x.mean(axis=1);v=x.var(axis=1,ddof=1);w=v.mean();vp=(n-1)*w/n+means.var(ddof=1)
    if vp<=0:return float(m*n)
    centered=x-means[:,None];nfft=1<<(2*n-1).bit_length()
    z=np.fft.rfft(centered,n=nfft,axis=1)
    ac=np.fft.irfft(z*z.conj(),n=nfft,axis=1)[:,:n]/n
    rho=1-(w-ac.mean(axis=0))/vp;rho[0]=1.
    pairs=[]
    for k in range(0,n-1,2):
        value=rho[k]+rho[k+1]
        if value<0:break
        pairs.append(min(value,pairs[-1]) if pairs else value)
    tau=max(1.,-1+2*sum(pairs))
    return float(min(m*n,m*n/tau))

def diagnostics(chains,names):
    rows=[]
    for j,name in enumerate(names):
        x=split(chains[:,:,j]);z=ndtri((rankdata(x.reshape(-1)).reshape(x.shape)-.375)/(x.size+.25))
        folded=np.abs(x-np.median(x));zf=ndtri((rankdata(folded.reshape(-1)).reshape(x.shape)-.375)/(x.size+.25))
        lo,hi=np.quantile(x,[.05,.95])
        rows.append(dict(parameter=name,rhat=max(basic_rhat(z),basic_rhat(zf)),bulk_ess=ess(z),tail_ess=min(ess((x<=lo).astype(float)),ess((x>=hi).astype(float)))))
    return pd.DataFrame(rows)

def gaussian_condition(mean,k,observed,values,bias,r):
    """Exact linear Gaussian update and marginal log likelihood of observations."""
    if len(observed)==0:return mean.copy(),k.copy(),0.
    v=k[np.ix_(observed,observed)]+r
    l=np.linalg.cholesky(v);delta=values-mean[observed]-bias
    solved=np.linalg.solve(l.T,np.linalg.solve(l,delta));cross=k[:,observed]
    postmean=mean+cross@solved
    a=np.linalg.solve(l,cross.T);postcov=k-a.T@a;postcov=(postcov+postcov.T)/2
    logp=-.5*(len(observed)*np.log(2*np.pi)+2*np.log(np.diag(l)).sum()+delta@solved)
    return postmean,postcov,float(logp)

@njit(cache=True)
def conditional_batch(flat,si,typ,m,obs,q,noise,correlated):
    n=len(si);ns=50;d=len(flat);means=np.empty((d,n));covs=np.empty((d,n,n));logs=np.empty(d)
    for j in range(d):
        row=flat[j];lam=row[si];sv=row[2*ns+3+typ];nv=row[2*ns+7+typ];rv=row[2*ns+11+typ]
        k=np.diag(np.full(n,sv))+(np.outer(lam,lam) if correlated else np.diag(lam**2))
        if len(obs)==0:
            means[j]=m;covs[j]=k;logs[j]=0.;continue
        diag=np.full(len(obs),sv+rv)+noise
        if not correlated:diag+=lam[obs]**2
        invd=1/diag;u1=lam[obs] if correlated else np.zeros(len(obs));u2=np.ones(len(obs))*np.sqrt(nv)
        a=1+(u1*u1*invd).sum();b=(u1*u2*invd).sum();c=1+(u2*u2*invd).sum();det=a*c-b*b
        v1=u1*invd;v2=u2*invd
        inv=np.diag(invd)-(c*np.outer(v1,v1)-b*(np.outer(v1,v2)+np.outer(v2,v1))+a*np.outer(v2,v2))/det
        delta=q-m[obs]-row[ns+si[obs]];cross=k[:,obs].copy()
        means[j]=m+cross@(inv@delta);v=k-cross@inv@cross.T;covs[j]=(v+v.T)/2
        logs[j]=-.5*(len(obs)*np.log(2*np.pi)+np.log(diag).sum()+np.log(det)+delta@inv@delta)
    return means,covs,logs

def forecast(chains,test,config,correlated=True,masked=None,seed=2026):
    """Update historical hyperposterior by test-poll marginal likelihood, then draw.

Importance weights are required: using equal historical weights after conditioning
would cut feedback from current polling into parameter uncertainty.
"""
    flat=chains.reshape(-1,chains.shape[-1]);n=len(test);ns=len(STATES)
    si=np.array([STATES.index(s) for s in test.geography]);typ=2+int(test.is_presidential_cycle.iloc[0]);m=100*test.prior.to_numpy(float)
    present=test.poll_mean.notna().to_numpy()&test.n_samples.gt(0).to_numpy()
    if masked is not None:present &= ~test.geography.isin(masked).to_numpy()
    obs=np.flatnonzero(present);q=100*test.poll_mean.to_numpy()[obs]
    noise=config['aggregation_sd_pp']**2/np.maximum(test.data_weight.to_numpy()[obs],.25)
    means,covs,logweights=conditional_batch(flat,si,typ,m,obs,q,noise,correlated)
    weights=np.exp(logweights-logsumexp(logweights))
    impess=float(1/(weights@weights));rng=np.random.default_rng(seed)
    take=rng.choice(len(flat),size=len(flat),p=weights);samples=np.empty((len(flat),n))
    for j,i in enumerate(take):samples[j]=means[i]+np.linalg.cholesky(covs[i])@rng.normal(size=n)
    sd=np.sqrt(np.diagonal(covs,axis1=1,axis2=2));pdem=weights@ndtr(means/sd)
    mean=weights@means;variance=weights@(sd**2+means**2)-mean**2
    lo50,hi50,lo80,hi80,lo95,hi95=np.quantile(samples,[.25,.75,.1,.9,.025,.975],axis=0)
    result=test.copy();result['prediction']=mean/100;result['prediction_pp']=mean;result['posterior_sd_pp']=np.sqrt(variance);result['p_dem']=pdem
    for col,val in [('lo50',lo50),('hi50',hi50),('lo80',lo80),('hi80',hi80),('lo95',lo95),('hi95',hi95)]:result[col+'_pp']=val
    result['model']='learned_covariance' if correlated else 'covariance_off_control';result['importance_ess']=impess
    actual=100*test.actual.to_numpy();result['log_predictive_density']=np.where(np.isfinite(actual),logsumexp(np.log(weights[:,None]+1e-300)-np.log(sd)-.5*np.log(2*np.pi)-.5*((actual[None,:]-means)/sd)**2,axis=0),np.nan)
    result['outside_margin_bounds_probability']=weights@(ndtr((-100-means)/sd)+1-ndtr((100-means)/sd))
    lam=flat[:,si];sv=flat[:,2*ns+3+typ];scaled=lam/np.sqrt(sv[:,None]+lam**2)
    corr=np.einsum('d,di,dj->ij',weights,scaled,scaled) if correlated else np.eye(n)
    np.fill_diagonal(corr,1.)
    pcov=np.einsum('d,dij->ij',weights,covs)+np.einsum('d,di,dj->ij',weights,means,means)-np.outer(mean,mean)
    pcorr=pcov/np.sqrt(np.outer(np.diag(pcov),np.diag(pcov)))
    return result,samples,dict(importance_ess=impess,importance_fraction=impess/len(flat),max_weight=float(weights.max()),prior_correlation=corr,posterior_correlation=pcorr)

def metrics(pred):
    rows=[]
    for (scenario,model),q in pred[pred.actual.notna()].groupby(['scenario','model']):
        for period,a in [('recent_2016_2024',q[q.cycle.between(2016,2024)]),('all_scored',q)]:
            for group,g in [('all',a),('competitive',a[a.history_selection_10pp.eq('competitive')]),('polled',a[a.n_samples.gt(0)]),('no_polls',a[a.n_samples.eq(0)])]:
                if not len(g):continue
                actual=100*g.actual;err=np.abs(g.prediction_pp-actual)
                row=dict(scenario=scenario,model=model,period=period,group=group,n=len(g),cycles=int(g.cycle.nunique()),correct=int(((g.p_dem>.5)==(actual>0)).sum()),mae_pp=float(err.groupby(g.cycle).mean().mean()),brier=float(((g.p_dem-(actual>0))**2).groupby(g.cycle).mean().mean()),negative_log_density=float((-g.log_predictive_density).groupby(g.cycle).mean().mean()))
                for level in [50,80,95]:row['coverage'+str(level)]=float(((actual>=g[f'lo{level}_pp'])&(actual<=g[f'hi{level}_pp'])).mean())
                row['mean_95_width_pp']=float((g.hi95_pp-g.lo95_pp).mean());rows.append(row)
    return pd.DataFrame(rows)

def verify_manifest(path):
    manifest=json.loads((path/'manifest.json').read_text())
    assert all(hashlib.sha256((path/k).read_bytes()).hexdigest()==v for k,v in manifest.items())
    return hashlib.sha256((path/'manifest.json').read_bytes()).hexdigest()

def build(lab,source,config=None,years=None):
    lab,source=Path(lab).resolve(),Path(source).resolve();cfg=dict(DEFAULT if config is None else config)
    source_hash=verify_manifest(source);settings=json.loads((source/'settings.json').read_text());shared=Path(settings['shared_source'])
    assert verify_manifest(shared)==settings['shared_manifest_sha256']
    original=Path(json.loads((shared/'settings.json').read_text())['source']);verify_manifest(original)
    src=json.loads((original/'settings.json').read_text())['sources']
    assert all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in src.values())
    h=pd.read_parquet(src['history']['path']);h=h[h.base.eq('fixed5_8')].copy()
    ref=pd.read_parquet(source/'predictions.parquet').query("model=='polling'")
    roster=pd.read_parquet(source/'full_seat_ledger.parquet').query("model=='polling'")
    out=lab/'reports/bayesian'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True)
    (out/'chains').mkdir();(out/'draws').mkdir();parts=[];diagnostic=[];infos=[];seatrows=[];covrows=[];masks=[]
    for scenario,history in h.groupby('scenario'):
        for year in sorted(ref.loc[ref.scenario.eq(scenario),'cycle'].unique()):
            if years is not None and year not in years:continue
            test=history[history.cycle.eq(year)].merge(ref.loc[(ref.scenario==scenario)&(ref.cycle==year),['target_id','history_selection_10pp']],on='target_id',validate='one_to_one')
            print(f'{scenario} {year}: fitting four Gibbs chains',flush=True)
            chains,info,diag=fit(history,int(year),cfg)
            # A fixed diagnostic gate; never extend chains based on predictive score.
            if info['max_rhat']>1.01 or min(info['min_bulk_ess'],info['min_tail_ess'])<400:
                longer=dict(cfg,warmup=cfg['warmup']*2,draws=cfg['draws']*2)
                print(f'  extending for MCMC diagnostics (Rhat {info["max_rhat"]:.3f}, ESS {info["min_bulk_ess"]:.0f})',flush=True)
                chains,info,diag=fit(history,int(year),longer)
            info['scenario']=scenario;infos.append(info);diagnostic.append(diag.assign(scenario=scenario,cycle=year))
            np.savez_compressed(out/'chains'/f'{scenario}_{year}.npz',chains=chains)
            r=roster[(roster.scenario==scenario)&(roster.cycle==year)]
            modeled=set(test.target_id);fixed=r[~r.target_id.isin(modeled)]
            fixedD=int(fixed.caucus.eq('D').sum());unmodeled=int((r.contested&~r.target_id.isin(modeled)).sum())
            for correlated in [False,True]:
                pred,draws,extra=forecast(chains,test,cfg,correlated,seed=cfg['seed']+int(year))
                parts.append(pred);model=pred.model.iloc[0]
                np.savez_compressed(out/'draws'/f'{scenario}_{year}_{model}.npz',margins_pp=draws,target_ids=test.target_id.to_numpy(str))
                counts=fixedD+(draws>0).sum(axis=1);lo,hi=np.quantile(counts,[.025,.975])
                seatrows.append(dict(scenario=scenario,cycle=int(year),model=model,expected_D=float(counts.mean()),expected_R=float(100-counts.mean()),D_lo95=int(lo),D_hi95=int(hi),p_D_at_least_51=float((counts>=51).mean()),p_D_exactly_50=float((counts==50).mean()),point_D=int(fixedD+(pred.p_dem>.5).sum()),actual_D=int(r.actual_caucus.eq('D').sum()) if year<2026 else np.nan,unmodeled_completion_assumptions=unmodeled,status='conditional_on_DR_scalar_and_ballot_caucus_completion_assumptions',importance_ess=extra['importance_ess']))
                if correlated:
                    for i,s in enumerate(test.target_id):
                        for j,t in enumerate(test.target_id):covrows.append(dict(scenario=scenario,cycle=int(year),target_a=s,target_b=t,state_a=test.geography.iloc[i],state_b=test.geography.iloc[j],prior_correlation=extra['prior_correlation'][i,j],posterior_correlation=extra['posterior_correlation'][i,j]))
                    print(f'  Rhat={info["max_rhat"]:.3f}; min ESS={info["min_bulk_ess"]:.0f}; poll-update ESS={extra["importance_ess"]:.0f}; D seats={counts.mean():.1f}',flush=True)
            # All-polled-state leave-one-state-out test, done on selected recent cycles.
            # Mask all same-state contests together; never condition on held-out outcomes.
            if year in [2020,2024,2026]:
                for state in sorted(test.loc[test.n_samples.gt(0),'geography'].unique()):
                    for correlated in [False,True]:
                        pp,_,ee=forecast(chains[::1,::5],test,cfg,correlated,masked=[state],seed=cfg['seed']+int(year))
                        q=pp[pp.geography.eq(state)].copy();q['masked_state']=state;q['mask_importance_ess']=ee['importance_ess'];masks.append(q)
    frames=dict(predictions=pd.concat(parts,ignore_index=True),diagnostics=pd.concat(diagnostic,ignore_index=True),seat_distributions=pd.DataFrame(seatrows),correlations=pd.DataFrame(covrows),masked_predictions=pd.concat(masks,ignore_index=True) if masks else pd.DataFrame())
    frames['metrics']=metrics(frames['predictions'])
    for name,q in frames.items():q.to_parquet(out/(name+'.parquet'),index=False)
    (out/'fits.json').write_text(json.dumps(infos,indent=2)+'\n')
    (out/'settings.json').write_text(json.dumps(dict(config=cfg,source=str(source),source_manifest_sha256=source_hash,source_inputs=src,as_of='2026-09-17',model='Gaussian one-factor state movement plus separate Gaussian polling-error factor',comparison='covariance-off forecast sensitivity with same historical hyperposterior and same marginal prior variances; common polling error retained; not independently refitted',stationarity='all older eligible outcomes retained without decay; state loadings/bias shared; older vs last-10-year and midterm/presidential noise scales differ',features='none in first model; economy/approval and disruption retained for later controlled extensions',posterior='Gibbs historical hyperposterior, importance update using forecast-poll marginal likelihood, exact conditional Gaussian forecasts and joint mixture draws',ballot_status='conditional scalar D/R approximation; not certified seat/control forecast',promotion=False),indent=2)+'\n')
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
    from run_combination_diagnostics import refresh
    refresh(out);return out,frames
