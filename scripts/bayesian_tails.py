"""Variance-matched Student-t latent errors and Gaussian scale sensitivities.

Student-t replaces common movement F, idiosyncratic movement eta, common polling
B and race polling R. Loadings/bias priors and aggregation noise remain Gaussian.
This is a factor model of t components, not an unrestricted multivariate t.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
import pandas as pd
from numba import njit
from scipy.special import ndtr,logsumexp
import bayesian_gaussian as base
from bayesian_gaussian_review import manifest
from bayesian_corrections import seat_summary

LABELS={'gaussian':'Original Gaussian','gaussian_prior150':'Gaussian movement SD ×1.5','gaussian_poll150':'Gaussian polling SD ×1.5','gaussian_both150':'Gaussian both SDs ×1.5','student5':'Student-t df=5','nonbayes_bias':'Non-Bayesian corrected polling','nonbayes_momentum':'Non-Bayesian corrected polling + momentum'}
@njit(cache=True)
def student_chain(si,yi,typ,res,psi,pyi,ptyp,err,noise,nstates,nyears,cfg,seed,nu):
    np.random.seed(seed)
    warm,draws,thin=int(cfg[0]),int(cfg[1]),int(cfg[2]);ldvar=cfg[3]**2
    lam=np.ones(nstates)*(2.+seed%7);ell=5.;f=np.random.normal(0,1,nyears)
    sigma=np.full(4,100.);bias=np.random.normal(0,1,nstates);mu=0.;tb=4.
    national=np.zeros(nyears);tn=np.full(4,9.);tr=np.full(4,16.);race=np.zeros(len(err))
    # lambda_s, b_s, ell, mu_b, tau_b^2, sigma_[mid,pres]^2,
    # tau_N_[mid,pres]^2, tau_R_[mid,pres]^2
    out=np.empty((draws,2*nstates+15));j=0
    h=(nu-2.)/nu if nu>2 else 1.
    wf=np.ones(nyears);we=np.ones(len(res));wn=np.ones(nyears);wr=np.ones(len(err))
    for it in range(warm+draws*thin):
        precision=wf/h;rhs=np.zeros(nyears)
        for i in range(len(res)):
            v=sigma[typ[i]]*h/we[i];precision[yi[i]]+=lam[si[i]]**2/v;rhs[yi[i]]+=lam[si[i]]*res[i]/v
        for y in range(nyears):f[y]=rhs[y]/precision[y]+np.random.normal()/np.sqrt(precision[y])
        precision=np.ones(nstates)/ldvar;rhs=np.ones(nstates)*ell/ldvar
        for i in range(len(res)):
            v=sigma[typ[i]]*h/we[i];precision[si[i]]+=f[yi[i]]**2/v;rhs[si[i]]+=f[yi[i]]*res[i]/v
        for s in range(nstates):lam[s]=rhs[s]/precision[s]+np.random.normal()/np.sqrt(precision[s])
        pe=nstates/ldvar+1/25.;me=lam.sum()/ldvar/pe
        ell=me+np.random.normal()/np.sqrt(pe)
        while ell<0:ell=me+np.random.normal()/np.sqrt(pe)
        for t in range(4):
            count=0;ss=0.
            for i in range(len(res)):
                if typ[i]==t:count+=1;ss+=(res[i]-lam[si[i]]*f[yi[i]])**2*we[i]/h
            sigma[t]=1/np.random.gamma(3+count/2.,1/(200.+ss/2.))
        # Poll residual = state bias + common cycle error + race error + known noise.
        for i in range(len(err)):
            pr=wr[i]/(h*tr[ptyp[i]])+1/noise[i];mr=(err[i]-bias[psi[i]]-national[pyi[i]])/noise[i]/pr
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
                pp=precision[y]+wn[y]/(h*tn[tt]);national[y]=rhs[y]/pp+np.random.normal()/np.sqrt(pp)
        for t in range(4):
            count=0;ss=0.;nc=0;ns=0.
            for i in range(len(err)):
                if ptyp[i]==t:count+=1;ss+=race[i]**2*wr[i]/h
            for y in range(nyears):
                if counts[y]>0:
                    tt=0
                    for i in range(len(err)):
                        if pyi[i]==y:tt=ptyp[i];break
                    if tt==t:nc+=1;ns+=national[y]**2*wn[y]/h
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
                pr+=wn[y]/(h*tn[tt]);rhs+=national[y]*wn[y]/(h*tn[tt])
        shift=rhs/pr+np.random.normal()/np.sqrt(pr)
        mu+=shift;bias+=shift
        for y in range(nyears):
            if counts[y]>0:national[y]-=shift
        if nu>2:
            for y in range(nyears):wf[y]=np.random.gamma((nu+1)/2.,2./(nu+f[y]**2/h))
            for i in range(len(res)):we[i]=np.random.gamma((nu+1)/2.,2./(nu+(res[i]-lam[si[i]]*f[yi[i]])**2/(h*sigma[typ[i]])))
            for i in range(len(err)):wr[i]=np.random.gamma((nu+1)/2.,2./(nu+race[i]**2/(h*tr[ptyp[i]])))
            for y in range(nyears):
                if counts[y]>0:
                    tt=0
                    for i in range(len(err)):
                        if pyi[i]==y:tt=ptyp[i];break
                    wn[y]=np.random.gamma((nu+1)/2.,2./(nu+national[y]**2/(h*tn[tt])))
        if it>=warm and (it-warm)%thin==0:
            out[j,:nstates]=lam;out[j,nstates:2*nstates]=bias
            out[j,2*nstates:]=np.concatenate((np.array([ell,mu,tb]),sigma,tn,tr))
            j+=1
    return out

def fit(history,year,cfg,nu=5):
    arrays,info=base.prepare(history,year,cfg);chosen=dict(cfg)
    names=['loading_'+s for s in base.STATES]+['bias_'+s for s in base.STATES]+['loading_common','bias_common','bias_variance']+[c+'_'+e+'_'+t for c in ['state_variance','national_poll_variance','race_poll_variance'] for e in ['older','recent'] for t in ['midterm','presidential']]
    for attempt in range(4):
        args=np.array([chosen['warmup'],chosen['draws'],chosen['thin'],chosen['loading_deviation_sd_pp']])
        chains=np.stack([student_chain(*arrays,args,cfg['seed']+year*17+c*7907,nu) for c in range(4)])
        diag=base.diagnostics(chains,names)
        print(f'  t{nu} attempt {attempt+1}: Rhat {diag.rhat.max():.4f}, ESS {diag.bulk_ess.min():.0f}',flush=True)
        if diag.rhat.max()<1.01 and min(diag.bulk_ess.min(),diag.tail_ess.min())>=400:break
        chosen.update(warmup=chosen['warmup']*2,draws=chosen['draws']*2)
    else:raise RuntimeError('Student-t convergence gate failed')
    info.update(config=chosen,nu=nu,variance_matching='t scale squared = variance * (nu-2)/nu',max_rhat=float(diag.rhat.max()),min_bulk_ess=float(diag.bulk_ess.min()),min_tail_ess=float(diag.tail_ess.min()))
    return chains,info,diag

@njit(cache=True)
def conditional(flat,si,typ,m,obs,q,noise,fscale,escale,bscale,rscale):
    n=len(si);d=len(flat);means=np.empty((d,n));covs=np.empty((d,n,n));logs=np.empty(d)
    for j in range(d):
        row=flat[j];lam=row[si]*np.sqrt(fscale[j]);sv=row[103+typ];nv=row[107+typ]*bscale[j];rv=row[111+typ]
        statev=sv*escale[j];k=np.diag(statev)+np.outer(lam,lam)
        if len(obs)==0:
            means[j]=m;covs[j]=k;logs[j]=0.;continue
        diag=statev[obs]+rv*rscale[j,obs]+noise;invd=1/diag
        u1=lam[obs];u2=np.ones(len(obs))*np.sqrt(nv)
        a=1+(u1*u1*invd).sum();b=(u1*u2*invd).sum();c=1+(u2*u2*invd).sum();det=a*c-b*b
        v1=u1*invd;v2=u2*invd
        inv=np.diag(invd)-(c*np.outer(v1,v1)-b*(np.outer(v1,v2)+np.outer(v2,v1))+a*np.outer(v2,v2))/det
        delta=q-m[obs]-row[50+si[obs]];cross=k[:,obs].copy()
        means[j]=m+cross@(inv@delta);v=k-cross@inv@cross.T;covs[j]=(v+v.T)/2
        logs[j]=-.5*(len(obs)*np.log(2*np.pi)+np.log(diag).sum()+np.log(det)+delta@inv@delta)
    return means,covs,logs

def forecast(chains,test,cfg,nu=0,prior_sd=1.,poll_sd=1.,repeat=1,seed=2026):
    # Independent latent-scale draws per hyperparameter draw. Integrate using
    # forecast polls, never forecast outcomes. Chunk covariance work for memory.
    original=chains.reshape(-1,chains.shape[-1]);flat=np.tile(original,(repeat,1));d=len(flat);n=len(test)
    rng=np.random.default_rng(seed);h=(nu-2)/nu if nu else 1.
    def scale(shape):return h/rng.gamma(nu/2,2/nu,size=shape) if nu else np.ones(shape)
    fs=scale(d)*prior_sd**2;es=scale((d,n))*prior_sd**2;bs=scale(d)*poll_sd**2;rs=scale((d,n))*poll_sd**2
    si=np.array([base.STATES.index(s) for s in test.geography]);typ=2+int(test.is_presidential_cycle.iloc[0]);m=100*test.prior.to_numpy(float)
    obs=np.flatnonzero(test.poll_mean.notna()&test.n_samples.gt(0));q=100*test.poll_mean.to_numpy()[obs]
    noise=cfg['aggregation_sd_pp']**2/np.maximum(test.data_weight.to_numpy()[obs],.25)*poll_sd**2
    means=np.empty((d,n));sd=np.empty((d,n));logs=np.empty(d)
    for start in range(0,d,1024):
        sl=slice(start,min(d,start+1024));a,c,l=conditional(flat[sl],si,typ,m,obs,q,noise,fs[sl],es[sl],bs[sl],rs[sl])
        means[sl]=a;sd[sl]=np.sqrt(np.diagonal(c,axis1=1,axis2=2));logs[sl]=l
    weights=np.exp(logs-logsumexp(logs));pdem=weights@ndtr(means/sd);mean=weights@means;variance=weights@(sd**2+means**2)-mean**2
    # Saved joint draws preserve common movement/poll errors and mix uncertainty.
    take=rng.choice(d,size=d,p=weights);samples=np.empty((d,n))
    for start in range(0,d,1024):
        end=min(d,start+1024);ix=take[start:end]
        a,c,_=conditional(flat[ix],si,typ,m,obs,q,noise,fs[ix],es[ix],bs[ix],rs[ix])
        samples[start:end]=a+np.einsum('dij,dj->di',np.linalg.cholesky(c),rng.normal(size=(len(ix),n)))
    result=test.copy();result['prediction']=mean/100;result['prediction_pp']=mean;result['posterior_sd_pp']=np.sqrt(variance);result['p_dem']=pdem
    for name,val in zip(['lo50','hi50','lo80','hi80','lo95','hi95'],np.quantile(samples,[.25,.75,.1,.9,.025,.975],axis=0)):result[name+'_pp']=val
    result['importance_ess']=1/(weights@weights)
    actual=100*test.actual.to_numpy();result['log_predictive_density']=np.where(np.isfinite(actual),logsumexp(np.log(weights[:,None]+1e-300)-np.log(sd)-.5*np.log(2*np.pi)-.5*((actual[None,:]-means)/sd)**2,axis=0),np.nan)
    result['outside_margin_bounds_probability']=weights@(ndtr((-100-means)/sd)+1-ndtr((100-means)/sd))
    pw=weights.reshape(repeat,len(original)).sum(axis=0)
    diagnostics=dict(importance_ess=float(1/(weights@weights)),parameter_weight_ess=float(1/(pw@pw)),maximum_weight=float(weights.max()),maximum_parameter_weight=float(pw.max()),latent_scale_repeats=repeat,nu=nu,prior_sd_multiplier=prior_sd,poll_sd_multiplier=poll_sd)
    return result,samples,diagnostics

def point_metrics(pred):
    rows=[]
    for (scenario,model),q in pred[pred.actual.notna()].groupby(['scenario','model']):
        for period,a in [('recent_2016_2024',q[q.cycle.between(2016,2024)]),('all_scored',q)]:
            for group,g in [('all',a),('competitive',a[a.history_selection_10pp.eq('competitive')]),('noncompetitive',a[a.history_selection_10pp.eq('not_selected')]),('polled',a[a.n_samples.gt(0)]),('no_polls',a[a.n_samples.eq(0)])]:
                if not len(g):continue
                rows.append(dict(scenario=scenario,model=model,period=period,group=group,n=len(g),cycles=g.cycle.nunique(),correct=int(((g.prediction>0)==(g.actual>0)).sum()),accuracy=float(((g.prediction>0)==(g.actual>0)).mean()),mae_pp=float((100*(g.prediction-g.actual).abs()).groupby(g.cycle).mean().mean())))
    return pd.DataFrame(rows)

def build(lab,source,years=None):
    lab,source=Path(lab).resolve(),Path(source).resolve();sha=base.verify_manifest(source);s=json.loads((source/'settings.json').read_text());cfg=s['config']
    assert all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in s['source_inputs'].values())
    old=pd.read_parquet(source/'predictions.parquet').query("model=='learned_covariance'")
    if years is not None:old=old[old.cycle.isin(years)]
    h=pd.read_parquet(s['source_inputs']['history']['path']);h=h[h.base.eq('fixed5_8')]
    refs=pd.read_parquet(s['source_inputs']['references']['path']);roster=pd.read_parquet(Path(s['source'])/'full_seat_ledger.parquet').query("model=='polling'")
    out=lab/'reports/bayesian_tails'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True);(out/'chains').mkdir();(out/'draws').mkdir()
    parts=[old.assign(model='gaussian')];seats=[];diags=[];fits=[];forecasts=[];stability=[]
    refseats=pd.read_parquet(source/'seat_distributions.parquet').query("model=='learned_covariance'")
    if years is not None:refseats=refseats[refseats.cycle.isin(years)]
    seats.extend(refseats.assign(model='gaussian').to_dict('records'))
    for (scenario,year),o in old.groupby(['scenario','cycle']):
        test=h[(h.scenario==scenario)&(h.cycle==year)].merge(o[['target_id','history_selection_10pp']],on='target_id',validate='one_to_one')
        assert list(test.target_id)==list(o.target_id)
        r=roster[(roster.scenario==scenario)&(roster.cycle==year)]
        print(f'{scenario} {year}',flush=True)
        gaussian=np.load(source/'chains'/f'{scenario}_{year}.npz')['chains']
        student,info,diag=fit(h[h.scenario.eq(scenario)],int(year),cfg,5);fits.append(dict(scenario=scenario,**info));diags.append(diag.assign(scenario=scenario,cycle=year))
        np.savez_compressed(out/'chains'/f'{scenario}_{year}_student5.npz',chains=student)
        for model,chain,nu,ps,qs in [('gaussian_prior150',gaussian,0,1.5,1.),('gaussian_poll150',gaussian,0,1.,1.5),('gaussian_both150',gaussian,0,1.5,1.5),('student5',student,5,1.,1.)]:
            repeat=4 if nu else 1
            pred,draw,d=forecast(chain,test,cfg,nu,ps,qs,repeat,cfg['seed']+int(year))
            if nu and d['importance_ess']<400:
                repeat=8;pred,draw,d=forecast(chain,test,cfg,nu,ps,qs,repeat,cfg['seed']+int(year))
            # Independent predictive integration replicate, not another fit.
            if nu:
                check,_,dd=forecast(chain,test,cfg,nu,ps,qs,repeat,cfg['seed']+int(year)+991)
                stability.append(dict(scenario=scenario,cycle=int(year),max_mean_difference_pp=float((pred.prediction_pp-check.prediction_pp).abs().max()),mean_absolute_difference_pp=float((pred.prediction_pp-check.prediction_pp).abs().mean()),max_probability_difference=float((pred.p_dem-check.p_dem).abs().max()),changed_mean_signs=int(((pred.prediction>0)!=(check.prediction>0)).sum()),changed_probability_calls=int(((pred.p_dem>.5)!=(check.p_dem>.5)).sum()),replicate_importance_ess=dd['importance_ess']))
            pred['model']=model;parts.append(pred);forecasts.append(dict(scenario=scenario,cycle=int(year),model=model,**d))
            seats.append(seat_summary(r,test,pred,draw,scenario,year,model));np.savez_compressed(out/'draws'/f'{scenario}_{year}_{model}.npz',margins_pp=draw,target_ids=test.target_id.to_numpy(str))
            print(f'  {model}: integration ESS {d["importance_ess"]:.0f}, parameter-weight ESS {d["parameter_weight_ess"]:.0f}',flush=True)
        for oldname,newname in [('bias','nonbayes_bias'),('bias__momentum','nonbayes_momentum')]:
            rr=refs[(refs.scenario==scenario)&(refs.cycle==year)&(refs.model==oldname)]
            q=test.merge(rr[['target_id','prediction']],on='target_id',validate='one_to_one');assert len(q)==len(test)
            q['model']=newname;q['prediction_pp']=100*q.prediction;parts.append(q)
    p=pd.concat(parts,ignore_index=True);frames=dict(predictions=p,point_metrics=point_metrics(p),probability_metrics=base.metrics(p[p.model.str.startswith(('gaussian','student'))]),seat_distributions=pd.DataFrame(seats),diagnostics=pd.concat(diags,ignore_index=True),forecast_diagnostics=pd.DataFrame(forecasts),integration_stability=pd.DataFrame(stability))
    for name,f in frames.items():f.to_parquet(out/(name+'.parquet'),index=False)
    (out/'fits.json').write_text(json.dumps(fits,indent=2)+'\n')
    (out/'settings.json').write_text(json.dumps(dict(source=str(source),source_manifest_sha256=sha,source_inputs=s['source_inputs'],as_of=s['as_of'],config=cfg,nu=5,student_components=['common_movement','race_movement','common_poll_error','race_poll_error'],student_scale='sqrt((nu-2)/nu) times Gaussian component SD; same variance-parameter priors, all parameters refitted',unchanged='same input margins, priors, mean formula, Gaussian loading/bias priors, Gaussian aggregation noise, historical admission and age/election-type groups; no extra features',gaussian_scale_controls='forecast-only SD multipliers 1.5 on movement, polling (including aggregation), or both; historical posterior unchanged; likelihood weights recomputed; not tuned or refitted models',point_accuracy='sign of posterior mean margin for all models; probability-majority accuracy also retained for Bayesian models',selection='df5 and scale1.5 fixed before inspection; no held-out optimization or per-cycle best-model selection',promotion=False),indent=2)+'\n')
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes());manifest(out);return out,frames
