"""Faster chronological priors, with a separate shrunk mean-error correction."""
from pathlib import Path
from datetime import datetime,timezone
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import bayesian_revision2 as v2
import bayesian_prior_revision3 as v3
import bayesian_state_penalty as v4
import simple_bayesian_polling as v1

R3='20260919T152739.765073Z';R4='20260919T154537.126999Z'
CONFIG=dict(half_lives=[2.,4.,8.,16.],shared_correction_sd_pp=3.,state_correction_sd_pp=5.,
            seed=519926,draws=20000)
FAMILIES=['fast','corrected'];MODES=['fixed','shared','state']
MODELS=[f'v5_{f}_{m}' for f in FAMILIES for m in MODES]
LABELS={**v4.LABELS,**{f'v5_{f}_{m}':('Faster prior' if f=='fast' else 'Faster + mean correction')+' / '+m for f in FAMILIES for m in MODES}}


def correction_prior(d=50):
    return np.eye(d)*CONFIG['state_correction_sd_pp']**2+np.ones((d,d))*CONFIG['shared_correction_sd_pp']**2


def bias_posterior(c,x,noise,weights,B):
    precision,ldB=v2.inverse(B);rhs=np.zeros(len(B));constant=0.;cache=[]
    for row,v,w in zip(x,noise,weights):
        obs=np.flatnonzero(np.isfinite(row));value=row[obs]
        inv,ld=v2.inverse(c[np.ix_(obs,obs)]+np.diag(v[obs]))
        precision[np.ix_(obs,obs)]+=w*inv;rhs[obs]+=w*inv@value
        constant-=.5*w*(len(obs)*np.log(2*np.pi)+ld+value@inv@value)
        cache.append((obs,inv))
    bvar,ldprecision=v2.inverse(precision);bmean=bvar@rhs
    evidence=constant-.5*ldB-.5*ldprecision+.5*rhs@bmean
    return bmean,bvar,float(evidence),cache


def fit_corrected_covariance(x,noise,weights,kappa,B):
    x,noise,weights,B=map(np.asarray,[x,noise,weights,B])
    if x.shape!=noise.shape or len(weights)!=len(x) or B.shape!=(x.shape[1],x.shape[1]):raise ValueError('Invalid dimensions')
    if not np.array_equal(np.isfinite(x),np.isfinite(noise)) or not (weights>0).all():raise ValueError('Invalid mask/weights')
    if (noise[np.isfinite(noise)]<0).any() or not np.isfinite(weights).all() or kappa<=0:raise ValueError('Invalid variance/weights/regularization')
    np.linalg.cholesky(B)
    target,meta=v2.make_target(x,noise,weights,kappa,float(np.diag(B).mean()))
    c=target.copy();objectives=[];converged=False
    for iteration in range(v2.CONFIG['max_iterations']):
        mean,var,ll,cache=bias_posterior(c,x,noise,weights,B)
        inv,ld=v2.inverse(c);obj=float(ll-.5*kappa*(ld+np.trace(target@inv)));objectives.append(obj)
        if len(objectives)>1 and obj<objectives[-2]-1e-7*max(1,abs(obj)):raise RuntimeError('Corrected EM objective decreased')
        scatter=np.zeros_like(c)
        for row,w,(obs,inv) in zip(x,weights,cache):
            gain=c[:,obs]@inv;m=gain@(row[obs]-mean[obs])
            conditional=c-gain@c[obs,:]+gain@var[np.ix_(obs,obs)]@gain.T
            scatter+=w*(conditional+np.outer(m,m))
        new=(scatter+kappa*target)/(weights.sum()+kappa);new=(new+new.T)/2
        relative=np.linalg.norm(new-c)/max(np.linalg.norm(c),1e-12);c=new
        if relative<v2.CONFIG['convergence_tolerance']:converged=True;break
    if not converged:raise RuntimeError(f'Corrected EM did not converge: {relative}')
    mean,var,ll,_=bias_posterior(c,x,noise,weights,B);inv,ld=v2.inverse(c)
    objectives.append(float(ll-.5*kappa*(ld+np.trace(target@inv))))
    return dict(covariance=c,bias_mean=mean,bias_covariance=var,target=target,objective=np.array(objectives),
                correction_prior_covariance=B,iterations=iteration+1,relative_change=float(relative),
                min_eigenvalue=float(np.linalg.eigvalsh(c).min()),converged=True,**meta)


def decay_two(history):
    h=history.copy();h['source_prior']=h.prior;h['prior_recipe']='decay2';h['prior_history_n']=0;h['prior_effective_n']=0.
    h['prior_source_max_cycle']=np.nan;h['prior_fallback']=True
    if h.duplicated(['scenario','cycle','geography']).any():raise ValueError('Duplicate state/cycle')
    for (_,state),g in h.groupby(['scenario','geography']):
        for idx,r in g.iterrows():
            p=g[g.cycle.lt(r.cycle)&g.actual.notna()].sort_values('cycle')
            if len(p):
                w=np.exp2(-(r.cycle-p.cycle.to_numpy())/2);w/=w.sum()
                h.loc[idx,['prior','prior_history_n','prior_effective_n','prior_source_max_cycle','prior_fallback']]=[float(w@p.actual.to_numpy()),len(p),1/(w@w),p.cycle.max(),False]
    return h


def choose_half(histories,year):
    h=histories['current'];years=sorted(h.loc[h.actual.notna()&h.cycle.lt(year),'cycle'].unique());valid=years[4:][-3:]
    rows=[];rank={8.:0,16.:1,4.:2,2.:3};scores=[]
    for half in CONFIG['half_lives']:
        recipe=f'decay{half:g}';h=histories[recipe];values=[]
        for vy in valid:
            g=h[h.cycle.eq(vy)&h.actual.notna()];value=float(abs(100*(g.actual-g.prior)).mean());values.append(value)
            rows.append(dict(forecast_cycle=int(year),validation_cycle=int(vy),half_life=half,recipe=recipe,n=len(g),prior_mae_pp=value,max_prior_source_cycle=float(g.prior_source_max_cycle.max())))
        scores.append((np.mean(values) if values else 0.,rank[half],recipe))
    return min(scores)[2],rows


class Experiment:
    def __init__(self,source,out):
        self.source,self.out=Path(source),Path(out)
        histories=pd.read_parquet(self.source/'prepared_histories.parquet')
        self.histories={k:g.copy() for k,g in histories.groupby('prior_recipe')}
        current=self.histories['current'].copy();current['prior']=current.source_prior
        self.histories['decay2']=decay_two(current)
        self.source_diag=pd.read_parquet(self.source/'fit_diagnostics.parquet')
        self.cache={};self.choice_cache={};self.base_cache={};self.half_cache={};self.strength_cache={}
        self.half_tuning=[];self.cov_tuning=[];self.strength_tuning=[];self.state_tuning=[];self.fit_records=[]

    def hist(self,recipe,scenario):
        h=self.histories[recipe.removesuffix('_corrected')];return h[h.scenario.eq(scenario)]

    def get_fit(self,recipe,scenario,year,kind,k):
        if kind=='poll':recipe='current'
        cs=scenario if kind=='poll' else 'all';key=(recipe,cs,int(year),kind,float(k))
        if key in self.cache:return self.cache[key]
        h=self.hist(recipe,scenario);x,noise,w,years,tr=v2.blocks(h,year,kind)
        if len(years)<(3 if kind=='poll' else 4):raise ValueError('Insufficient history')
        d=self.source_diag;old=d[d.recipe.eq(recipe)&d.scenario.eq(cs)&d.cycle.eq(year)&d.component.eq(kind)&d.kappa.eq(k)]
        if len(old):
            row=old.iloc[0];z=np.load(self.source/row.path);f={name:z[name] for name in z.files}
            f.update(iterations=int(row.iterations),relative_change=float(row.get("relative_change",np.nan)),min_eigenvalue=float(row.min_eigenvalue),converged=True);reused=True
        elif recipe.endswith('_corrected'):
            f=fit_corrected_covariance(x,noise,w,k,correction_prior());reused=False
        else:f=v2.fit_component(h,year,kind,k);reused=False
        mass=(np.isfinite(x)*w[:,None]).sum(axis=0)
        means=np.divide(np.nansum(x*w[:,None],axis=0),mass,out=np.full(50,np.nan),where=mass>0)
        f.update(kappa=k,training_max_cycle=int(years.max()),training_cycles=len(years),years=years,
                 observed_weight=mass,residual_means=means,pair_support=np.isfinite(x).astype(int).T@np.isfinite(x).astype(int))
        path=f'fits/{recipe}_{cs}_{year}_{kind}_k{k:g}.npz';f['path']=path
        np.savez_compressed(self.out/path,**{name:value for name,value in f.items() if isinstance(value,np.ndarray)})
        self.fit_records.append(dict(recipe=recipe,scenario=cs,cycle=int(year),component=kind,kappa=k,
                                     training_max_cycle=f['training_max_cycle'],training_cycles=len(years),reused=reused,
                                     iterations=f['iterations'],converged=f['converged'],min_eigenvalue=f['min_eigenvalue'],
                                     min_objective_increment=float(np.diff(f['objective']).min()),path=path))
        self.cache[key]=f
        if len(self.cache)%25==0:print('Cached components:',len(self.cache),flush=True)
        return f

    def choose_fit(self,recipe,scenario,year,kind):
        if kind=='poll':recipe='current'
        key=(recipe,scenario,int(year),kind)
        if key in self.choice_cache:return self.choice_cache[key]
        h=self.hist(recipe,scenario);_,_,_,years,_=v2.blocks(h,year,kind)
        valid=years[3 if kind=='poll' else 4:][-3:];candidates=[]
        for k in v2.CONFIG['regularization_candidates']:
            scores=[]
            for vy in valid:
                f=self.get_fit(recipe,scenario,int(vy),kind,k)
                if recipe.endswith('_corrected'):
                    _,_,_,_,rows=v2.blocks(h,int(vy)+1,'movement');g=rows[rows.cycle.eq(vy)]
                    ix=[v2.STATES.index(s) for s in g.geography];mean=f['bias_mean'][ix]
                    cov=(f['covariance']+f['bias_covariance'])[np.ix_(ix,ix)];inv,ld=v2.inverse(cov);delta=g.value.to_numpy()-mean
                    score=float(.5*(len(g)*np.log(2*np.pi)+ld+delta@inv@delta)/len(g));n=len(g)
                else:score,n=v2.validation_score(h,int(vy),kind,f)
                scores.append(score);self.cov_tuning.append(dict(recipe=recipe,scenario=scenario,forecast_cycle=int(year),validation_cycle=int(vy),component=kind,kappa=k,fit_max_cycle=f['training_max_cycle'],n=n,nld_per_state=score))
            candidates.append((np.mean(scores) if scores else 0.,-k,k))
        f=self.get_fit(recipe,scenario,year,kind,min(candidates)[2]);self.choice_cache[key]=f;return f

    def base(self,family,scenario,year):
        key=(family,scenario,int(year))
        if key in self.base_cache:return self.base_cache[key]
        hk=(scenario,int(year))
        if hk not in self.half_cache:
            recipe,rows=choose_half({k:self.hist(k,scenario) for k in self.histories},year)
            self.half_cache[hk]=recipe;self.half_tuning.extend([dict(scenario=scenario,**r) for r in rows])
        recipe=self.half_cache[hk];fitrecipe=recipe+('_corrected' if family=='corrected' else '')
        test=self.hist(recipe,scenario);test=test[test.cycle.eq(year)].sort_values('target_id').reset_index(drop=True).copy()
        f=self.choose_fit(fitrecipe,scenario,year,'movement');poll=self.choose_fit('current',scenario,year,'poll')
        test['base_prior_pp']=100*test.prior;test['mean_correction_pp']=0.
        mov=f
        if family=='corrected':
            ix=[v2.STATES.index(s) for s in test.geography];test['mean_correction_pp']=f['bias_mean'][ix];test['prior']+=test.mean_correction_pp/100
            mov={**f,'process_covariance':f['covariance'],'correction_covariance':f['bias_covariance'],'covariance':f['covariance']+f['bias_covariance']}
        else:mov={**f,'process_covariance':f['covariance'],'correction_covariance':np.zeros_like(f['covariance'])}
        val=(test,mov,poll,fitrecipe);self.base_cache[key]=val;return val

    def strength(self,family,scenario,year):
        key=(family,scenario,int(year))
        if key in self.strength_cache:return self.strength_cache[key]
        h=self.hist('current',scenario);years=sorted(h.loc[h.actual.notna()&h.cycle.lt(year),'cycle'].unique());valid=[]
        for vy in years:
            _,_,_,ym,_=v2.blocks(h,vy,'movement');_,_,_,yp,_=v2.blocks(h,vy,'poll')
            if len(ym)>=4 and len(yp)>=3:valid.append(int(vy))
        valid=valid[-3:];rows=[]
        for vy in valid:
            test,mov,poll,recipe=self.base(family,scenario,vy)
            for a in v3.CONFIG['variance_multipliers']:
                pred,cov,_=v3.scaled_predict(test,mov,poll,a)
                rows.append(dict(family=family,scenario=scenario,forecast_cycle=int(year),validation_cycle=vy,validation_recipe=recipe,
                                 fit_max_cycle=max(mov['training_max_cycle'],poll['training_max_cycle']),variance_multiplier=a,n=len(test),nld_per_state=v3.predictive_score(pred,cov)))
        self.strength_tuning.extend(rows);a,status=v3.select_multiplier(rows);value=(a,status,valid);self.strength_cache[key]=value;return value

    def state_strength(self,family,scenario,year):
        shared,status,years=self.strength(family,scenario,year);rows=[]
        for vy in years:
            test,mov,poll,recipe=self.base(family,scenario,vy)
            weight=float(np.exp2(-(max(years)-vy)/v4.CONFIG['recent_half_life_years']))
            for i,t in test[test.actual.notna()].iterrows():
                si=v2.STATES.index(t.geography)
                for candidate in v4.CONFIG['variance_candidates']:
                    a=np.full(50,shared);a[si]=candidate;pred,_,_=v4.state_predict(test,mov,poll,a);p=pred.iloc[i]
                    rows.append(dict(family=family,scenario=scenario,forecast_cycle=int(year),validation_cycle=vy,state=t.geography,target_id=t.target_id,
                                     validation_recipe=recipe,fit_max_cycle=max(mov['training_max_cycle'],poll['training_max_cycle']),shared_multiplier=shared,candidate=candidate,weight=weight,
                                     actual_pp=100*t.actual,prediction_pp=p.prediction_pp,sd_pp=p.posterior_sd_pp,nld=float(-norm.logpdf(100*t.actual,p.prediction_pp,p.posterior_sd_pp))))
        surface=pd.DataFrame(rows);a,profile=v4.shrink_state_scores(surface,shared,year);self.state_tuning.extend(rows)
        return a,profile.assign(family=family,scenario=scenario,cycle=int(year))


def input_review(lab,out,history):
    snap=lab/'data/final/snapshots/20260918T040848.452707Z';meta=json.loads((snap/'manifest.json').read_text())
    paths=[snap/'tables'/f'{n}.parquet' for n in ['labels','contest_inputs_reference']]
    for path in paths:
        if v1.sha(path)!=meta['files'][str(path.relative_to(snap))]['sha256']:raise ValueError('Changed input audit source')
    labels,contests=map(pd.read_parquet,paths)
    q=contests.merge(labels,on='target_id',suffixes=('','_label'))
    q=q[q.geography.isin(['MI','WV','SD'])&q.cycle.between(2000,2024)]
    cols=['target_id','cycle','geography','stage','special','dem_rep_margin','diagnostic_eligible','status','review_reasons','historical_horizon_comparable']
    q=q[cols].drop_duplicates();q['admitted_to_frozen_history']=q.target_id.isin(history.target_id)
    q.to_parquet(out/'prior_input_review.parquet',index=False)
    rows=[dict(target_id='2018-WV-regular-gen',official_dem=290510,official_rep=271113,official_other=24411,
               official_url='https://www.fec.gov/documents/2705/federalelections2018.pdf',verification='FEC PDF pages 32–33 (PDF pages 37–38), direct web text'),
          dict(target_id='2020-SD-regular-gen',official_dem=143987,official_rep=276232,official_other=0,
               official_url='https://sdsos.gov/elections-voting/assets/2020%20Assests/2020GeneralStateCanvassFinal%26Certificate.pdf',verification='Secretary of State official canvass indexed table; direct PDF retrieval failed')]
    audit=pd.DataFrame(rows);audit['official_margin_pp']=100*(audit.official_dem-audit.official_rep)/(audit.official_dem+audit.official_rep+audit.official_other)
    audit=audit.merge(q[['target_id','dem_rep_margin','review_reasons']],on='target_id',validate='one_to_one');audit['frozen_margin_pp']=100*audit.dem_rep_margin
    audit['difference_pp']=audit.official_margin_pp-audit.frozen_margin_pp;audit['admission_changed']=False
    audit.to_parquet(out/'official_result_followups.parquet',index=False)
    v1.json_write(out/'input_review_sources.json',{str(p):v1.sha(p) for p in paths})


def build(lab):
    lab=Path(lab).resolve();source=lab/'reports/bayesian_prior_revision3'/R3;reference=lab/'reports/bayesian_state_penalty'/R4
    hashes={str(p):v1.verify(p) for p in [source,reference]};settings=json.loads((source/'settings.json').read_text())
    old_hashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='BAYESIAN_PRIOR_REVISION5.ipynb'}
    refs=pd.read_parquet(reference/'predictions.parquet');cases=refs[refs.model.eq('v4_decay_state')][['scenario','cycle','target_id','history_selection_10pp']]
    ledger=next(Path(p) for p in settings['provenance']['paths'] if p.endswith('state_surprise/20260919T011532.132689Z/full_seat_ledger.parquet'));roster=pd.read_parquet(ledger).query("model=='polling'")
    out=lab/'reports/bayesian_prior_revision5'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');(out/'fits').mkdir(parents=True);(out/'draws').mkdir()
    ex=Experiment(source,out);input_review(lab,out,ex.histories['current']);predictions=[];folds=[];profiles=[];priors=[];seats=[];params=[];masked=[]
    for (scenario,year),case in cases.groupby(['scenario','cycle']):
        for family in FAMILIES:
            test,mov,poll,recipe=ex.base(family,scenario,int(year));test=test.merge(case[['target_id','history_selection_10pp']],on='target_id',validate='one_to_one').sort_values('target_id').reset_index(drop=True)
            if set(test.target_id)!=set(case.target_id):raise ValueError('Different cases')
            shared,status,valid=ex.strength(family,scenario,int(year));a,profile=ex.state_strength(family,scenario,int(year));profiles.append(profile)
            folds.append(dict(scenario=scenario,cycle=int(year),family=family,recipe=recipe,half_life=float(recipe.removesuffix('_corrected')[5:]),shared_multiplier=shared,strength_status=status,
                              movement_path=mov['path'],poll_path=poll['path'],training_max_cycle=max(mov['training_max_cycle'],poll['training_max_cycle']),movement_kappa=mov['kappa'],poll_kappa=poll['kappa']))
            priors.append(test[['target_id','scenario','cycle','geography','actual','base_prior_pp','mean_correction_pp','prior']].assign(family=family,recipe=recipe))
            for i,s in enumerate(v2.STATES):
                params.append(dict(scenario=scenario,cycle=int(year),family=family,state=s,correction_pp=float(mov['bias_mean'][i]) if family=='corrected' else 0.,
                                   correction_sd_pp=float(np.sqrt(mov['correction_covariance'][i,i])),process_sd_pp=float(np.sqrt(mov['process_covariance'][i,i])),
                                   total_prior_sd_pp=float(np.sqrt(mov['covariance'][i,i])),observed_cycles=int(mov['pair_support'][i,i])))
            for mode,mult in [('fixed',np.ones(50)),('shared',np.full(50,shared)),('state',a)]:
                model=f'v5_{family}_{mode}';pred,cov,meta=v4.state_predict(test,mov,poll,mult);pred['model']=model;predictions.append(pred)
                rng=np.random.default_rng(CONFIG['seed']+int(year)+(scenario=='oct31')*10000)
                draws=pred.prediction_pp.to_numpy()+rng.standard_normal((CONFIG['draws'],len(test)))@np.linalg.cholesky(cov).T
                np.savez_compressed(out/'draws'/f'{scenario}_{year}_{model}.npz',margins_pp=draws,covariance_pp2=cov,prior_covariance_pp2=meta['prior_covariance'],multipliers_all_states=mult,target_ids=test.target_id.to_numpy(str))
                rr=roster[roster.scenario.eq(scenario)&roster.cycle.eq(year)];seat=v1.seat_counts(rr,test,pred,draws);counts=seat['fixed_D']+(draws>0).sum(axis=1)
                lo,hi=np.quantile(counts,[.15,.85],method='inverted_cdf');seat.update(expected_D_exact=float(seat['fixed_D']+pred.p_dem.sum()),D_lo70=int(lo),D_hi70=int(hi));seats.append(dict(scenario=scenario,cycle=int(year),model=model,**seat))
                if year in [2020,2024,2026] and mode=='state':
                    for i,t in test[test.q_pp.notna()].iterrows():
                        hidden=test.copy();hidden.loc[i,'q_pp']=np.nan;p,_,_=v4.state_predict(hidden,mov,poll,mult);r=p.iloc[i]
                        masked.append(dict(scenario=scenario,cycle=int(year),model=model,target_id=t.target_id,geography=t.geography,actual=t.actual,prior_pp=100*t.prior,prediction_pp=r.prediction_pp,p_dem=r.p_dem))
            print(f'{scenario} {year} {family}: {recipe}, shared a={shared:g}',flush=True)
    pred=pd.concat(predictions+[refs],ignore_index=True);pred.to_parquet(out/'predictions.parquet',index=False);v1.scores(pred).to_parquet(out/'metrics.parquet',index=False)
    frames=dict(folds=pd.DataFrame(folds),state_penalties=pd.concat(profiles,ignore_index=True),prior_predictions=pd.concat(priors,ignore_index=True),
                state_parameters=pd.DataFrame(params),seats=pd.DataFrame(seats),masked_predictions=pd.DataFrame(masked),
                half_life_tuning=pd.DataFrame(ex.half_tuning),covariance_tuning=pd.DataFrame(ex.cov_tuning),strength_tuning=pd.DataFrame(ex.strength_tuning),local_tuning=pd.DataFrame(ex.state_tuning),fit_diagnostics=pd.DataFrame(ex.fit_records))
    for name,f in frames.items():f.to_parquet(out/f'{name}.parquet',index=False)
    pd.concat(ex.histories.values(),ignore_index=True).to_parquet(out/'prepared_histories.parquet',index=False)
    v1.json_write(out/'settings.json',dict(config=CONFIG,v2_config=v2.CONFIG,v4_config=v4.CONFIG,source=str(source),reference=str(reference),source_hashes=hashes,
                                        provenance=settings['provenance'],old_notebook_hashes=old_hashes,as_of=settings['as_of'],
                                        correction_uncertainty_included=True,covariance_and_selection_uncertainty_included=False,promotion=False))
    for name in ['bayesian_prior_revision5.py','bayesian_state_penalty.py','bayesian_prior_revision3.py','bayesian_revision2.py','simple_bayesian_polling.py']:(out/name).write_bytes((lab/'scripts'/name).read_bytes())
    (out/'BAYESIAN_PRIOR_REVISION5.md').write_bytes((lab/'BAYESIAN_PRIOR_REVISION5.md').read_bytes());v1.manifest(out);return out


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1]);print(build(p.parse_args().lab))
