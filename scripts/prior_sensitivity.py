"""Chronological prior calibration and one-at-a-time sensitivity, fixed polls."""
from pathlib import Path
from datetime import datetime,timezone
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import simple_bayesian_polling as v1
import bayesian_revision2 as v2
import bayesian_prior_revision3 as v3
import bayesian_state_penalty as v4

SOURCE='20260919T172552.860612Z'
PROFILES={'control':(8.,.5),'history4':(4.,.5),'history16':(16.,.5),'type_equal':(8.,1.)}
CONFIG=dict(profiles=PROFILES,shrinkage_masses=[1.,2.,4.],mean_half_lives=[4.,8.,16.],
            variance_multipliers=[.25,.5,1.,2.,4.],validation_cycles=3,local_half_life=4.,draws=20000,seed=719926,
            solver_max_iterations=16000,solver_tolerance=1e-6)


def training_blocks(history,year,kind,half=8.,other=.5):
    if half<=0 or not 0<other<=1:raise ValueError('Invalid relevance parameters')
    x,noise,_,years,rows=v2.blocks(history,year,kind)
    w=np.exp2(-(year-years)/half)*np.where(years%4==year%4,1.,other)
    return x,noise,w,years,rows


def shrink(scores,shared,year,mass=2.):
    if mass<=0:raise ValueError('Positive shrinkage mass required')
    _,p=v4.shrink_state_scores(scores,shared,year)
    p['shrinkage_mass']=mass
    p['local_fraction']=p.recent_mass/(p.recent_mass+mass)
    p['variance_multiplier']=np.exp((1-p.local_fraction)*np.log(shared)+p.local_fraction*np.log(p.raw_multiplier))
    p['penalty_strength']=1/p.variance_multiplier
    return p.variance_multiplier.to_numpy(),p


class Experiment:
    def __init__(self,source,out):
        self.source,self.out=Path(source),Path(out)
        self.prepared=pd.read_parquet(self.source/'prepared_histories.parquet')
        self.histories={r:g.copy() for r,g in self.prepared.groupby('prior_recipe')}
        self.diag=pd.read_parquet(self.source/'fit_diagnostics.parquet')
        self.fit_cache={};self.choice_cache={};self.base_cache={};self.mean_cache={};self.strength_cache={};self.surface_cache={};self.joint_cache={}
        self.fit_records=[];self.cov_tuning=[];self.mean_tuning=[];self.strength_tuning=[];self.local_tuning=[];self.joint_tuning=[]

    def hist(self,recipe,scenario):
        h=self.histories[recipe];return h[h.scenario.eq(scenario)]

    def component(self,profile,recipe,scenario,year,kind,k):
        if kind=='poll':profile='poll_fixed';recipe='current'
        cs=scenario if kind=='poll' else 'all';key=(profile,recipe,cs,int(year),kind,float(k))
        if key in self.fit_cache:return self.fit_cache[key]
        half,other=(8.,.5) if kind=='poll' else PROFILES[profile]
        x,noise,w,years,rows=training_blocks(self.hist(recipe,scenario),year,kind,half,other)
        if len(years)<(3 if kind=='poll' else 4):raise ValueError('Insufficient fit history')
        old=self.diag[self.diag.recipe.eq(recipe)&self.diag.scenario.eq(cs)&self.diag.cycle.eq(year)&self.diag.component.eq(kind)&self.diag.kappa.eq(k)] if profile in ['control','poll_fixed'] else self.diag.iloc[:0]
        if len(old):
            assert len(old)==1;r=old.iloc[0];z=np.load(self.source/r.path);f={n:z[n] for n in z.files}
            f.update(iterations=int(r.iterations),converged=bool(r.converged),min_eigenvalue=float(r.min_eigenvalue));reused=True;source_path=str(self.source/r.path)
        else:
            # Sequential fit: allow slower newly explored covariance fits to
            # converge to the SAME tolerance/objective; restore module config.
            old_cap=v2.CONFIG['max_iterations']
            try:
                v2.CONFIG['max_iterations']=CONFIG['solver_max_iterations']
                f=v2.fit_covariance(x,noise,w,k,v2.CONFIG['bias_prior_sd_pp']**2 if kind=='poll' else None)
            finally:v2.CONFIG['max_iterations']=old_cap
            reused=False;source_path=''
        f.update(kappa=float(k),years=years,training_max_cycle=int(years.max()),training_cycles=len(years),
                 training_rows=len(rows),observed_weight=(np.isfinite(x)*w[:,None]).sum(axis=0),
                 pair_support=np.isfinite(x).astype(int).T@np.isfinite(x).astype(int))
        path=f'fits/{profile}_{recipe}_{cs}_{year}_{kind}_k{k:g}.npz';f['path']=path
        arrays={name:value for name,value in f.items() if isinstance(value,np.ndarray)}
        arrays.update(training_values=x,training_noise=noise,training_weights=w)
        np.savez_compressed(self.out/path,**arrays)
        self.fit_records.append(dict(profile=profile,recipe=recipe,scenario=cs,cycle=int(year),component=kind,kappa=float(k),
                                     history_half_life=half,other_type_weight=other,training_max_cycle=int(years.max()),training_cycles=len(years),training_rows=len(rows),
                                     reused=reused,source_path=source_path,iterations=f['iterations'],converged=f['converged'],min_eigenvalue=f['min_eigenvalue'],
                                     min_objective_increment=float(np.diff(f['objective']).min()),path=path))
        self.fit_cache[key]=f
        if len(self.fit_cache)%25==0:print('Components',len(self.fit_cache),flush=True)
        return f

    def choose_component(self,profile,recipe,scenario,year,kind):
        if kind=='poll':profile='poll_fixed';recipe='current'
        key=(profile,recipe,scenario,int(year),kind)
        if key in self.choice_cache:return self.choice_cache[key]
        h=self.hist(recipe,scenario);_,_,_,years,_=v2.blocks(h,year,kind)
        valid=years[3 if kind=='poll' else 4:][-3:];candidates=[]
        for k in v2.CONFIG['regularization_candidates']:
            scores=[]
            for vy in valid:
                fit=self.component(profile,recipe,scenario,int(vy),kind,k)
                score,n=v2.validation_score(h,int(vy),kind,fit);scores.append(score)
                self.cov_tuning.append(dict(profile=profile,recipe=recipe,scenario=scenario,forecast_cycle=year,validation_cycle=int(vy),
                                           component=kind,kappa=k,n=n,fit_max_cycle=fit['training_max_cycle'],score=score))
            candidates.append((np.mean(scores) if scores else 0.,-k,k))
        f=self.component(profile,recipe,scenario,year,kind,min(candidates)[2]);self.choice_cache[key]=f;return f

    def selected_mean(self,scenario,year):
        key=(scenario,int(year))
        if key not in self.mean_cache:
            recipe,rows=v3.choose_half_life({r:self.hist(r,scenario) for r in v3.RECIPES},year)
            self.mean_cache[key]=recipe;self.mean_tuning.extend([dict(scenario=scenario,**r) for r in rows])
        return self.mean_cache[key]

    def base(self,profile,scenario,year,recipe=None):
        recipe=recipe or self.selected_mean(scenario,year);key=(profile,scenario,int(year),recipe)
        if key in self.base_cache:return self.base_cache[key]
        h=self.hist(recipe,scenario);test=h[h.cycle.eq(year)].sort_values('target_id').reset_index(drop=True).copy()
        movement=self.choose_component(profile,recipe,scenario,year,'movement');poll=self.choose_component(profile,'current',scenario,year,'poll')
        result=(test,movement,poll,recipe);self.base_cache[key]=result;return result

    def validation_years(self,scenario,year):
        h=self.hist('current',scenario);years=sorted(h.loc[h.actual.notna()&h.cycle.lt(year),'cycle'].unique());valid=[]
        for vy in years:
            _,_,_,ym,_=v2.blocks(h,vy,'movement');_,_,_,yp,_=v2.blocks(h,vy,'poll')
            if len(ym)>=4 and len(yp)>=3:valid.append(int(vy))
        return valid[-3:]

    def strength(self,profile,scenario,year):
        key=(profile,scenario,int(year))
        if key in self.strength_cache:return self.strength_cache[key]
        years=self.validation_years(scenario,year);rows=[]
        for vy in years:
            test,mov,poll,recipe=self.base(profile,scenario,vy)
            for a in CONFIG['variance_multipliers']:
                pred,cov,_=v3.scaled_predict(test,mov,poll,a)
                rows.append(dict(profile=profile,scenario=scenario,forecast_cycle=int(year),validation_cycle=vy,recipe=recipe,
                                 fit_max_cycle=max(mov['training_max_cycle'],poll['training_max_cycle']),variance_multiplier=a,n=len(test),nld_per_state=v3.predictive_score(pred,cov)))
        self.strength_tuning.extend(rows);a,status=v3.select_multiplier(rows);result=(a,status,years);self.strength_cache[key]=result;return result

    def joint_choice(self,scenario,year):
        key=(scenario,int(year))
        if key in self.joint_cache:return self.joint_cache[key]
        years=self.validation_years(scenario,year);candidates=[]
        for half in CONFIG['mean_half_lives']:
            recipe=f'decay{half:g}'
            for a in CONFIG['variance_multipliers']:
                scores=[]
                for vy in years:
                    test,mov,poll,_=self.base('control',scenario,vy,recipe)
                    pred,cov,_=v3.scaled_predict(test,mov,poll,a);score=v3.predictive_score(pred,cov);scores.append(score)
                    self.joint_tuning.append(dict(scenario=scenario,forecast_cycle=int(year),validation_cycle=vy,recipe=recipe,half_life=half,variance_multiplier=a,
                                                 fit_max_cycle=max(mov['training_max_cycle'],poll['training_max_cycle']),score=score,n=len(test)))
                candidates.append((np.mean(scores) if scores else 0.,{8.:0,16.:1,4.:2}[half],abs(np.log2(a)),a,recipe))
        if len(years)<3:recipe,a,status='decay8',1.,'fallback_insufficient_validation'
        else:
            best=min(candidates);a,recipe=best[3:];status='joint_last_three_cycles_log_score'
        result=(recipe,a,status,years);self.joint_cache[key]=result;return result

    def local_surface(self,profile,scenario,year,joint=False):
        key=(profile,scenario,int(year),joint)
        if key in self.surface_cache:return self.surface_cache[key]
        if joint:_,shared,_,years=self.joint_choice(scenario,year)
        else:shared,_,years=self.strength(profile,scenario,year)
        rows=[]
        for vy in years:
            recipe=self.joint_choice(scenario,vy)[0] if joint else None
            test,mov,poll,recipe=self.base(profile,scenario,vy,recipe)
            weight=float(np.exp2(-(max(years)-vy)/CONFIG['local_half_life']))
            for i,t in test[test.actual.notna()].iterrows():
                si=v2.STATES.index(t.geography)
                for candidate in CONFIG['variance_multipliers']:
                    a=np.full(50,shared);a[si]=candidate;p,_,_=v4.state_predict(test,mov,poll,a);r=p.iloc[i]
                    rows.append(dict(profile=profile,joint=joint,scenario=scenario,forecast_cycle=int(year),validation_cycle=vy,validation_recipe=recipe,
                                     fit_max_cycle=max(mov['training_max_cycle'],poll['training_max_cycle']),state=t.geography,target_id=t.target_id,shared_multiplier=shared,
                                     candidate=candidate,weight=weight,nld=float(-norm.logpdf(100*t.actual,r.prediction_pp,r.posterior_sd_pp))))
        self.local_tuning.extend(rows);surface=pd.DataFrame(rows);self.surface_cache[key]=(shared,surface);return shared,surface


def prior_prediction(test,cov,model,scaling):
    mean=100*test.prior.to_numpy();sd=np.sqrt(np.diag(cov));p=test.copy()
    p['model']=model;p['prior_scaling']=scaling;p['prediction_pp']=mean;p['prediction']=mean/100;p['posterior_sd_pp']=sd;p['p_dem']=norm.cdf(mean/sd)
    for level in [50,70,80,95]:
        z=norm.ppf((1+level/100)/2);p[f'lo{level}_pp']=mean-z*sd;p[f'hi{level}_pp']=mean+z*sd
    p['standardized_error']=(100*p.actual-mean)/sd
    p['log_predictive_density']=norm.logpdf(100*p.actual,mean,sd)
    p['outside_margin_bounds_probability']=norm.cdf((-100-mean)/sd)+norm.sf((100-mean)/sd)
    return p


def build(lab,include_joint=True):
    lab=Path(lab).resolve();source=lab/'reports/official_repair_review'/SOURCE;sourcehash=v1.verify(source)
    oldhashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='PRIOR_CALIBRATION_SENSITIVITY.ipynb'}
    out=lab/'reports/prior_sensitivity'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');(out/'fits').mkdir(parents=True);(out/'forecasts').mkdir()
    print('OUTPUT',out,flush=True);ex=Experiment(source,out)
    roster=pd.read_parquet(source/'full_seat_ledger.parquet');old=pd.read_parquet(source/'predictions.parquet');cases=old[old.model.eq('decay_state')][['scenario','cycle','target_id']]
    predictions=[];priors=[];seats=[];profiles=[];folds=[];checks=[]
    def forecast(profile,scenario,year,test,mov,poll,recipe,model,a,mass,shared,status,joint=False):
        pred,cov,meta=v4.state_predict(test,mov,poll,a);pred['model']=model;predictions.append(pred)
        priors.append(prior_prediction(test,meta['prior_covariance'],model,model.rsplit('_',1)[-1]))
        rng=np.random.default_rng(CONFIG['seed']+int(year)+(scenario=='oct31')*10000)
        draws=pred.prediction_pp.to_numpy()+rng.standard_normal((CONFIG['draws'],len(test)))@np.linalg.cholesky(cov).T
        rr=roster[roster.scenario.eq(scenario)&roster.cycle.eq(year)];seat=v1.seat_counts(rr,test,pred,draws);counts=seat['fixed_D']+(draws>0).sum(axis=1)
        lo,hi=np.quantile(counts,[.15,.85],method='inverted_cdf');seat.update(expected_D_exact=float(seat['fixed_D']+pred.p_dem.sum()),D_lo70=int(lo),D_hi70=int(hi))
        seats.append(dict(scenario=scenario,cycle=year,model=model,**seat))
        path=f'forecasts/{scenario}_{year}_{model}.npz'
        np.savez_compressed(out/path,target_ids=test.target_id.to_numpy(str),means_pp=pred.prediction_pp.to_numpy(),posterior_covariance=cov,prior_covariance=meta['prior_covariance'],multipliers=a,seat_count_frequency=np.bincount(counts,minlength=101),mc_mean=draws.mean(axis=0))
        checks.append(dict(scenario=scenario,cycle=year,model=model,min_eigenvalue=float(np.linalg.eigvalsh(cov).min()),max_mc_mean_z=float(np.max(abs(draws.mean(axis=0)-pred.prediction_pp)/np.sqrt(np.diag(cov)/CONFIG['draws'])))))
        folds.append(dict(profile=profile,scenario=scenario,cycle=int(year),model=model,recipe=recipe,joint=joint,shrinkage_mass=mass,shared_multiplier=shared,
                          status=status,movement_path=mov['path'],poll_path=poll['path'],forecast_path=path,training_max_cycle=max(mov['training_max_cycle'],poll['training_max_cycle'])))
    for (scenario,year),case in cases.groupby(['scenario','cycle']):
        year=int(year)
        for profile in PROFILES:
            test,mov,poll,recipe=ex.base(profile,scenario,year);assert set(test.target_id)==set(case.target_id)
            shared,status,_=ex.strength(profile,scenario,year);_,surface=ex.local_surface(profile,scenario,year)
            a,p=shrink(surface,shared,year,2.);profiles.append(p.assign(profile=profile,joint=False,scenario=scenario,cycle=year,model=profile+'_state'))
            for mode,mult in [('fixed',np.ones(50)),('shared',np.full(50,shared)),('state',a)]:
                forecast(profile,scenario,year,test,mov,poll,recipe,profile+'_'+mode,mult,2. if mode=='state' else np.nan,shared,status)
            if profile=='control':
                for mass in [1.,4.]:
                    a,p=shrink(surface,shared,year,mass);model=f'shrink{mass:g}_state';profiles.append(p.assign(profile=profile,joint=False,scenario=scenario,cycle=year,model=model))
                    forecast(profile,scenario,year,test,mov,poll,recipe,model,a,mass,shared,status)
            print(scenario,year,profile,recipe,'a',shared,flush=True)
        if include_joint:
            recipe,shared,status,_=ex.joint_choice(scenario,year);test,mov,poll,_=ex.base('control',scenario,year,recipe)
            _,surface=ex.local_surface('control',scenario,year,joint=True);a,p=shrink(surface,shared,year,2.)
            profiles.append(p.assign(profile='control',joint=True,scenario=scenario,cycle=year,model='joint_state'))
            for mode,mult in [('shared',np.full(50,shared)),('state',a)]:forecast('control',scenario,year,test,mov,poll,recipe,'joint_'+mode,mult,2. if mode=='state' else np.nan,shared,status,joint=True)
            print(scenario,year,'joint',recipe,'a',shared,flush=True)
    pred=pd.concat(predictions,ignore_index=True);prior=pd.concat(priors,ignore_index=True)
    for name,f in dict(predictions=pred,prior_predictions=prior,posterior_metrics=v1.scores(pred),prior_metrics=v1.scores(prior),
                       folds=pd.DataFrame(folds),state_penalties=pd.concat(profiles,ignore_index=True),seats=pd.DataFrame(seats),
                       covariance_tuning=pd.DataFrame(ex.cov_tuning),mean_tuning=pd.DataFrame(ex.mean_tuning),strength_tuning=pd.DataFrame(ex.strength_tuning),
                       local_tuning=pd.DataFrame(ex.local_tuning),joint_tuning=pd.DataFrame(ex.joint_tuning),fit_diagnostics=pd.DataFrame(ex.fit_records),simulation_checks=pd.DataFrame(checks)).items():f.to_parquet(out/(name+'.parquet'),index=False)
    ex.prepared.to_parquet(out/'prepared_histories.parquet',index=False)
    v1.json_write(out/'settings.json',dict(config=CONFIG,source=str(source),source_sha256=sourcehash,old_notebook_hashes=oldhashes,as_of='2026-09-17',
                                        polling_fixed=True,include_joint=include_joint,decision='Exploratory sensitivity; no automatic promotion',
                                        joint_reason='Prior-only calibration and documented posterior undercoverage warrant checking staged versus joint mean/strength objectives; fixed original grids, no new features.',
                                        covariance_and_selection_uncertainty_included=False))
    for p in [Path(__file__),lab/'PRIOR_CALIBRATION_SENSITIVITY.md']:(out/p.name).write_bytes(p.read_bytes())
    v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    print('COMPLETE',out,flush=True);return out


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--without-joint',action='store_true');a=p.parse_args();build(a.lab,not a.without_joint)
