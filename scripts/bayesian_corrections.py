"""Joint Bayesian polling-bias/feature correction and explicit bias ablations.

Reuse the independent historical movement posterior; refit polling likelihoods.
Shared features predict positive actual-minus-poll surprise, hence enter the
polling equation with a minus sign. Never apply the old correction a second time.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
import pandas as pd
from scipy.special import logsumexp
from numba import njit
import bayesian_gaussian as base
from recency_state_baselines import WeightedScoreDesign
from bayesian_gaussian_review import manifest

FEATURES=['economy_momentum_wh','approval_wh']
LABELS={'covariance_off_original':'Original Bayesian covariance off','original':'Original Bayesian bias','bias_off_fixed':'Bias off: same fitted scales','bias_off_refit':'Bias off: refitted scales','features':'Bias + shared economy/approval','features_off':'Features off: same joint fit'}
PRIMARY=['covariance_off_original','original','bias_off_refit','features']
BETA_SD=2.


def feature_design(history,calendars,year):
    # Match exactly the polling training population admitted by base.prepare.
    tr=history[history.cycle.lt(year)&history.actual.notna()&history.prior_latest_cycle.notna()&history.prior_latest_cycle.lt(history.cycle)]
    pol=tr[tr.poll_mean.notna()&tr.n_samples.gt(0)]
    years=sorted(tr.cycle.unique());polyears=sorted(pol.cycle.unique())
    cal=calendars.set_index('cycle',drop=False)
    traincal=cal.loc[polyears].reset_index(drop=True);testcal=cal.loc[[year]].reset_index(drop=True)
    design=WeightedScoreDesign().fit(traincal,np.ones(len(traincal)))
    z,scores=design.transform(traincal);v,future=design.transform(testcal,require_later=True)
    x=np.zeros((len(years),2));fx=np.zeros(2);active=[]
    for j,name in enumerate(FEATURES):
        if name in design.active:
            active.append(name);col=design.active.index(name)
            for i,y in enumerate(polyears):x[years.index(y),j]=z[i,col]
            fx[j]=v[0,col]
    ledger=scores[['cycle']+FEATURES].copy();ledger['role']='train'
    future=future[['cycle']+FEATURES].copy();future['role']='forecast';ledger=pd.concat([ledger,future],ignore_index=True)
    for j,name in enumerate(FEATURES):
        ledger[name+'_z']=[x[years.index(y),j] if y in years else fx[j] for y in ledger.cycle]
        ledger[name+'_imputed']=ledger[name].isna()
    metadata=dict(training_cycles=list(map(int,polyears)),training_max_cycle=int(max(polyears)),active=active,nominal_coefficients=2,
                  coefficient_prior_sd_pp=BETA_SD,normalization='one row per past polled cycle; equal cycle weight; fixed score recipe; median fill and standardization fitted on training only; no decay',**design.metadata())
    return x,fx,metadata,ledger

@njit(cache=True)
def poll_chain(psi,pyi,ptyp,err,noise,x,nstates,nyears,warm,draws,thin,seed,use_bias,use_features,beta_sd):
    np.random.seed(seed)
    bias=np.random.normal(0,1,nstates) if use_bias else np.zeros(nstates);mu=0.;tb=4. if use_bias else 0.
    nat=np.zeros(nyears);tn=np.full(4,9.);tr=np.full(4,16.);race=np.zeros(len(err));beta=np.zeros(2)
    out=np.zeros((draws,nstates+12));j=0
    counts=np.zeros(nyears);types=np.zeros(nyears,np.int64)
    for i in range(len(err)):counts[pyi[i]]+=1;types[pyi[i]]=ptyp[i]
    for it in range(warm+draws*thin):
        xb=x@beta
        for i in range(len(err)):
            pr=1/tr[ptyp[i]]+1/noise[i];mr=(err[i]-bias[psi[i]]-nat[pyi[i]]+xb[pyi[i]])/noise[i]/pr
            race[i]=mr+np.random.normal()/np.sqrt(pr)
        if use_bias:
            precision=np.ones(nstates)/tb;rhs=np.ones(nstates)*mu/tb
            for i in range(len(err)):
                precision[psi[i]]+=1/noise[i];rhs[psi[i]]+=(err[i]-nat[pyi[i]]-race[i]+xb[pyi[i]])/noise[i]
            for s in range(nstates):bias[s]=rhs[s]/precision[s]+np.random.normal()/np.sqrt(precision[s])
            pr=nstates/tb+1/25.;mu=bias.sum()/tb/pr+np.random.normal()/np.sqrt(pr)
            tb=1/np.random.gamma(3+nstates/2.,1/(8.+((bias-mu)**2).sum()/2.))
        precision=np.zeros(nyears);rhs=np.zeros(nyears)
        for i in range(len(err)):
            y=pyi[i];precision[y]+=1/noise[i];rhs[y]+=(err[i]-bias[psi[i]]-race[i])/noise[i]
        # Block beta and national cycle errors: integrate B when sampling beta,
        # then sample B conditional on beta. Only a two-dimensional solve.
        if use_features:
            gram=np.eye(2)/(beta_sd**2);r=np.zeros(2)
            for y in range(nyears):
                if counts[y]>0:
                    scale=1+precision[y]*tn[types[y]]
                    gram+=precision[y]/scale*np.outer(x[y],x[y]);r-=x[y]*rhs[y]/scale
            l=np.linalg.cholesky(gram)
            beta=np.linalg.solve(gram,r)+np.linalg.solve(l.T,np.random.normal(0,1,2))
            xb=x@beta
        for y in range(nyears):
            if counts[y]>0:
                pp=precision[y]+1/tn[types[y]];nat[y]=(rhs[y]+precision[y]*xb[y])/pp+np.random.normal()/np.sqrt(pp)
        for t in range(4):
            n=0;ss=0.;nc=0;ns=0.
            for i in range(len(err)):
                if ptyp[i]==t:n+=1;ss+=race[i]**2
            for y in range(nyears):
                if counts[y]>0 and types[y]==t:nc+=1;ns+=nat[y]**2
            tr[t]=1/np.random.gamma(3+n/2.,1/(32.+ss/2.))
            tn[t]=1/np.random.gamma(3+nc/2.,1/(18.+ns/2.))
        if use_bias:
            pr=1/25.;rhs_shift=-mu/25.
            for y in range(nyears):
                if counts[y]>0:pr+=1/tn[types[y]];rhs_shift+=nat[y]/tn[types[y]]
            shift=rhs_shift/pr+np.random.normal()/np.sqrt(pr);mu+=shift;bias+=shift
            for y in range(nyears):
                if counts[y]>0:nat[y]-=shift
        if it>=warm and (it-warm)%thin==0:
            out[j,:nstates]=bias
            out[j,nstates:]=np.concatenate((np.array([mu,tb]),tn,tr,beta));j+=1
    return out


def poll_fit(history,cal,year,cfg,features):
    arrays,info=base.prepare(history,year,cfg);_,_,_,_,psi,pyi,ptyp,err,noise,ns,ny=arrays
    x,fx,design,ledger=feature_design(history,cal,year)
    names=['bias_'+s for s in base.STATES]+['bias_common','bias_variance']+[c+'_'+era+'_'+kind for c in ['national_poll_variance','race_poll_variance'] for era in ['older','recent'] for kind in ['midterm','presidential']]+['beta_momentum','beta_approval']
    chosen=dict(cfg)
    for attempt in range(3):
        warm=chosen['warmup'];draws=chosen['draws'];thin=chosen['thin']
        chain=np.stack([poll_chain(psi,pyi,ptyp,err,noise,x,ns,ny,warm,draws,thin,cfg['seed']+year*13+7907*c+(313 if features else 991),features,features,BETA_SD) for c in range(cfg['chains'])])
        diag=base.diagnostics(chain,names)
        if diag.rhat.max()<1.01 and min(diag.bulk_ess.min(),diag.tail_ess.min())>=400:break
        chosen=dict(chosen,warmup=warm*2,draws=draws*2)
    else:raise RuntimeError('Poll sampler did not meet convergence gate')
    info.update(config=chosen,feature_design=design if features else None,features=features,use_persistent_bias=features,max_rhat=float(diag.rhat.max()),min_bulk_ess=float(diag.bulk_ess.min()),min_tail_ess=float(diag.tail_ess.min()),movement='reused independent saved historical movement posterior; no new outcome model')
    return chain,fx,info,diag,ledger


def combine_posteriors(movement,poll,seed):
    """Historical posterior factorizes given observed final outcomes.

    Keep each posterior's MCMC diagnostics separate. Independent sampling of the
    saved movement posterior does not manufacture extra effective movement draws.
    """
    rng=np.random.default_rng(seed);old=movement.reshape(-1,movement.shape[-1]);n=poll.shape[0]*poll.shape[1];ns=len(base.STATES)
    choose=rng.choice(len(old),size=n,replace=n>len(old));merged=old[choose].reshape(poll.shape[:2]+(old.shape[-1],)).copy()
    merged[:,:,ns:2*ns]=poll[:,:,:ns];merged[:,:,2*ns+1:2*ns+3]=poll[:,:,ns:ns+2]
    merged[:,:,2*ns+7:2*ns+11]=poll[:,:,ns+2:ns+6];merged[:,:,2*ns+11:2*ns+15]=poll[:,:,ns+6:ns+10]
    return merged,poll[:,:,ns+10:ns+12]


def effective_chain(chain,beta=None,x=None,remove_bias=False,remove_features=False):
    z=chain.copy();ns=len(base.STATES)
    if remove_bias:z[:,:,ns:2*ns]=0.
    if beta is not None and not remove_features:
        surprise=beta@np.asarray(x,float)
        z[:,:,ns:2*ns]-=surprise[:,:,None]
    return z


def forecast_weights(chain,test,cfg):
    flat=chain.reshape(-1,chain.shape[-1]);si=np.array([base.STATES.index(s) for s in test.geography]);obs=np.flatnonzero(test.poll_mean.notna()&test.n_samples.gt(0))
    noise=cfg['aggregation_sd_pp']**2/np.maximum(test.data_weight.to_numpy()[obs],.25)
    _,_,ll=base.conditional_batch(flat,si,2+int(test.is_presidential_cycle.iloc[0]),100*test.prior.to_numpy(),obs,100*test.poll_mean.to_numpy()[obs],noise,True)
    return np.exp(ll-logsumexp(ll))


def components(chain,beta,x,test,weights,model,year,scenario):
    ns=len(base.STATES);raw=chain.reshape(-1,chain.shape[-1]);bb=beta.reshape(-1,2) if beta is not None else np.zeros((len(raw),2))
    contributions=bb*np.asarray(x)[None,:];rows=[]
    for r in test.itertuples():
        i=base.STATES.index(r.geography);known=r.n_samples>0
        rows.append(dict(scenario=scenario,cycle=int(year),target_id=r.target_id,state=r.geography,model=model,n_samples=int(r.n_samples),
            raw_poll_pp=100*r.poll_mean,prior_pp=100*r.prior,legacy_regularized_poll_pp=100*r.poll_baseline,legacy_corrected_poll_pp=100*r.bias_prediction,
            legacy_regularization_pull_pp=100*(r.poll_baseline-r.poll_mean) if known else np.nan,
            legacy_bias_correction_pp=100*(r.bias_prediction-r.poll_baseline) if known else np.nan,
            history_bayesian_bias_correction_pp=-raw[:,ns+i].mean(),updated_bayesian_bias_correction_pp=-weights@raw[:,ns+i],
            history_momentum_surprise_pp=contributions[:,0].mean(),history_approval_surprise_pp=contributions[:,1].mean(),
            updated_momentum_surprise_pp=weights@contributions[:,0],updated_approval_surprise_pp=weights@contributions[:,1],
            direct_polling_adjustment_pp=float(weights@(-raw[:,ns+i]+contributions.sum(axis=1))) if known else np.nan,
            direct_adjustment_status='polling_likelihood_equivalent_adjustment_not_final_margin_change' if known else 'no_poll_likelihood; indirect_cross_state_updates_possible'))
    return pd.DataFrame(rows)


def seat_summary(roster,test,pred,draws,scenario,year,model):
    fixed=roster[~roster.target_id.isin(test.target_id)];fixedD=int(fixed.caucus.eq('D').sum());counts=fixedD+(draws>0).sum(axis=1)
    lo,hi=np.quantile(counts,[.025,.975]);return dict(scenario=scenario,cycle=int(year),model=model,expected_D=float(counts.mean()),expected_R=float(100-counts.mean()),D_lo95=int(lo),D_hi95=int(hi),p_D_at_least_51=float((counts>=51).mean()),p_D_exactly_50=float((counts==50).mean()),point_D=int(fixedD+(pred.p_dem>.5).sum()),actual_D=int(roster.actual_caucus.eq('D').sum()) if year<2026 else np.nan,unmodeled_completion_assumptions=int((roster.contested&~roster.target_id.isin(test.target_id)).sum()),status='conditional_ballot_caucus_scalar_DR_scenario',importance_ess=float(pred.importance_ess.iloc[0]))


def build(lab,source,years=None):
    lab,source=Path(lab).resolve(),Path(source).resolve();source_hash=base.verify_manifest(source)
    settings=json.loads((source/'settings.json').read_text());cfg=settings['config'];inputs=settings['source_inputs']
    assert all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in inputs.values())
    h=pd.read_parquet(inputs['history']['path']);h=h[h.base.eq('fixed5_8')]
    cal=pd.read_parquet(inputs['calendars']['path']);allold=pd.read_parquet(source/'predictions.parquet');old=allold.query("model=='learned_covariance'")
    oldseats=pd.read_parquet(source/'seat_distributions.parquet').query("model=='learned_covariance'")
    roster=pd.read_parquet(Path(settings['source'])/'full_seat_ledger.parquet').query("model=='polling'")
    out=lab/'reports/bayesian_corrections'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True);(out/'chains').mkdir();(out/'draws').mkdir()
    control=allold.query("model=='covariance_off_control'").assign(model='covariance_off_original')
    controlseats=pd.read_parquet(source/'seat_distributions.parquet').query("model=='covariance_off_control'").assign(model='covariance_off_original')
    if years is not None:control=control[control.cycle.isin(years)];controlseats=controlseats[controlseats.cycle.isin(years)]
    parts=[control];seats=controlseats.to_dict('records');comp=[];fits=[];diags=[];feature_rows=[];coefs=[];forecast_diags=[]
    for (scenario,year),o in old.groupby(['scenario','cycle']):
        if years is not None and year not in years:continue
        hist=h[h.scenario.eq(scenario)];test=hist[hist.cycle.eq(year)].merge(o[['target_id','history_selection_10pp']],on='target_id',validate='one_to_one')
        assert list(test.target_id)==list(o.target_id)
        oldchain=np.load(source/'chains'/f'{scenario}_{year}.npz')['chains']
        r=roster[(roster.scenario==scenario)&(roster.cycle==year)]
        parts.append(o.assign(model='original'));seats.append(oldseats[(oldseats.scenario==scenario)&(oldseats.cycle==year)].assign(model='original').iloc[0].to_dict())
        weights=forecast_weights(oldchain,test,cfg);comp.append(components(oldchain,None,[0,0],test,weights,'original',year,scenario))
        arms=[('bias_off_fixed',effective_chain(oldchain,remove_bias=True),None,None)]
        print(f'{scenario} {year}: refitting no-bias and shared-feature polling models',flush=True)
        for features,model in [(False,'bias_off_refit'),(True,'features')]:
            poll,x,info,diag,ledger=poll_fit(hist,cal[cal.scenario.eq(scenario)],int(year),cfg,features)
            combined,beta=combine_posteriors(oldchain,poll,cfg['seed']+int(year)+int(features))
            fits.append(dict(scenario=scenario,model=model,**info));diags.append(diag.assign(scenario=scenario,cycle=year,model=model))
            np.savez_compressed(out/'chains'/f'{scenario}_{year}_{model}.npz',poll_chain=poll,combined=combined,beta=beta,future_x=x)
            eff=effective_chain(combined,beta,x) if features else combined
            arms.append((model,eff,combined,beta if features else None))
            if features:
                feature_rows.append(ledger.assign(scenario=scenario,forecast_cycle=year))
                arms.append(('features_off',effective_chain(combined,beta,x,remove_features=True),None,None))
                flat=beta.reshape(-1,2)
                for j,name in enumerate(FEATURES):coefs.append(dict(scenario=scenario,cycle=int(year),term=name,history_mean_pp_per_sd=float(flat[:,j].mean()),history_lo95=float(np.quantile(flat[:,j],.025)),history_hi95=float(np.quantile(flat[:,j],.975)),forecast_standardized_score=float(x[j]),history_contribution_pp=float(flat[:,j].mean()*x[j])))
        for model,eff,raw,beta in arms:
            pred,draws,extra=base.forecast(eff,test,cfg,True,seed=cfg['seed']+int(year));pred['model']=model;parts.append(pred)
            weights=forecast_weights(eff,test,cfg)
            assert np.isclose(1/(weights@weights),extra['importance_ess'])
            if raw is not None:comp.append(components(raw,beta,x if beta is not None else [0,0],test,weights,model,year,scenario))
            seats.append(seat_summary(r,test,pred,draws,scenario,year,model))
            np.savez_compressed(out/'draws'/f'{scenario}_{year}_{model}.npz',margins_pp=draws,target_ids=test.target_id.to_numpy(str))
            forecast_diags.append(dict(scenario=scenario,cycle=int(year),model=model,importance_ess=extra['importance_ess'],maximum_weight=extra['max_weight']))
            print(f'  {model}: update ESS {extra["importance_ess"]:.0f}, D seats {seats[-1]["expected_D"]:.2f}',flush=True)
    frames=dict(predictions=pd.concat(parts,ignore_index=True),seat_distributions=pd.DataFrame(seats),components=pd.concat(comp,ignore_index=True),diagnostics=pd.concat(diags,ignore_index=True),feature_scores=pd.concat(feature_rows,ignore_index=True),coefficients=pd.DataFrame(coefs),forecast_diagnostics=pd.DataFrame(forecast_diags))
    frames['metrics']=base.metrics(frames['predictions'])
    for name,q in frames.items():q.to_parquet(out/(name+'.parquet'),index=False)
    (out/'fits.json').write_text(json.dumps(fits,indent=2,allow_nan=False,default=lambda v:v.item() if isinstance(v,np.generic) else v.tolist() if isinstance(v,np.ndarray) else str(v))+'\n')
    (out/'settings.json').write_text(json.dumps(dict(source=str(source),source_manifest_sha256=source_hash,config=cfg,beta_prior_sd_pp=BETA_SD,source_inputs=inputs,as_of=settings['as_of'],
        equation='poll = final + state_bias - (beta_momentum*x_momentum + beta_approval*x_approval) + common_poll_error + race_poll_error + aggregation_noise',
        no_bias='persistent state/shared mean bias fixed at zero; common cycle polling error retained; refit its scales',
        controls='bias_off_fixed suppresses bias at forecast only using original fitted scales; features_off suppresses beta*x at forecast only using joint-fit bias/scales; both labeled sensitivities',
        movement_reuse='posterior factorizes given historical observed outcomes; independently combine saved movement draws and refitted polling draws; reused draw count does not increase movement ESS',
        normalization='one row per older polled cycle; train-only equal-weight score normalization, median fill, standardization; no feature intercept',
        feature_training='all older admitted polled errors; same older/recent and presidential/midterm error scales; two shared coefficients jointly estimated with bias and error scales',
        no_poll='no direct feature adjustment without a polling likelihood; indirect changes via state covariance and parameter inference are possible',
        status='exploratory Gaussian comparison; calibration not assumed accepted',promotion=False),indent=2)+'\n')
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes());manifest(out);return out,frames
