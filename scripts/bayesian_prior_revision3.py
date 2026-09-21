"""Chronological prior means and nested shared prior-strength calibration.

See BAYESIAN_PRIOR_REVISION3.md. Frozen sources; empirical Bayes.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import bayesian_revision2 as v2
import simple_bayesian_polling as v1

CONFIG=dict(half_lives=[4.,8.,16.],variance_multipliers=[.25,.5,1.,2.,4.],validation_cycles=3,
            seed=319926,draws=20000)
RECIPES=['current','latest','decay4','decay8','decay16']
FAMILIES=['current','latest','decay']
MODELS=[f'v3_{r}_{a}' for r in FAMILIES for a in ['fixed','tuned']]
LABELS={**v2.LABELS,**{f'v3_{r}_{a}':f'{r.title()} prior / '+('fixed strength' if a=='fixed' else 'tuned strength') for r in FAMILIES for a in ['fixed','tuned']}}
SOURCE_NAME='20260919T150107.375010Z'


def construct_history(history, recipe):
    """Each row's center uses only earlier same-state outcomes; no-history fallback unchanged."""
    if recipe not in RECIPES:raise ValueError('Unknown recipe')
    h=history.copy()
    if h.duplicated(['scenario','cycle','geography']).any():raise ValueError('Duplicate state/cycle outcomes require a multiseat model')
    h['source_prior']=h.prior
    h['prior_recipe']=recipe
    h['prior_effective_n']=0.
    h['prior_history_n']=0
    h['prior_source_max_cycle']=np.nan
    h['prior_fallback']=True
    weights=[]
    for (scenario,state),g in h.groupby(['scenario','geography']):
        g=g.sort_values('cycle')
        for idx,row in g.iterrows():
            past=g[g.cycle.lt(row.cycle)&g.actual.notna()]
            if past.empty:continue
            if recipe=='current':
                w=np.full(len(past),.5/len(past));w[-1]+=.5
            elif recipe=='latest':
                w=np.zeros(len(past));w[-1]=1.
            else:
                half=float(recipe.removeprefix('decay'))
                w=np.exp2(-(row.cycle-past.cycle.to_numpy())/half);w/=w.sum()
            prior=float(w@past.actual.to_numpy())
            if recipe=='current' and not np.isclose(prior,row.prior,atol=1e-12):
                raise ValueError('Current chronological prior does not match frozen source')
            h.loc[idx,['prior','prior_effective_n','prior_history_n','prior_source_max_cycle','prior_fallback']]=[prior,1/(w@w),len(past),past.cycle.max(),False]
            for t,weight in zip(past.itertuples(),w):
                weights.append(dict(scenario=scenario,target_id=row.target_id,state=state,forecast_cycle=int(row.cycle),
                                    recipe=recipe,source_cycle=int(t.cycle),source_target_id=t.target_id,
                                    source_margin_pp=100*t.actual,weight=float(weight)))
    return h,pd.DataFrame(weights)


def choose_half_life(histories,year):
    h=histories['current'];years=sorted(h.loc[h.actual.notna()&h.cycle.lt(year),'cycle'].unique())
    valid=years[4:][-CONFIG['validation_cycles']:]
    rows=[];candidates=[]
    for half in CONFIG['half_lives']:
        recipe=f'decay{half:g}';x=histories[recipe];scores=[]
        for vy in valid:
            g=x[x.cycle.eq(vy)&x.actual.notna()]
            score=float(abs(100*(g.actual-g.prior)).mean());scores.append(score)
            rows.append(dict(forecast_cycle=int(year),validation_cycle=int(vy),half_life=half,recipe=recipe,
                             n=len(g),prior_mae_pp=score,max_prior_source_cycle=float(g.prior_source_max_cycle.max())))
        rank={8.:0,16.:1,4.:2}[half]
        candidates.append((np.mean(scores) if scores else 0.,rank,recipe))
    return min(candidates)[2],rows


def scaled_predict(test,movement,poll,a=1.,observe_ids=None):
    if not np.isfinite(a) or a<=0:raise ValueError('Positive variance multiplier required')
    mov={**movement,'covariance':a*movement['covariance']}
    pred,cov,meta=v2.predict(test,mov,poll,observe_ids=observe_ids)
    pred['variance_multiplier']=a;pred['prior_penalty_strength']=1/a
    pred['prior_sd_pp']=np.sqrt(np.diag(meta['prior_covariance']))
    return pred,cov,meta


def predictive_score(pred,cov):
    g=pred.actual.notna().to_numpy();delta=100*pred.actual.to_numpy()[g]-pred.prediction_pp.to_numpy()[g]
    if not len(delta):raise ValueError('No outcomes for scoring')
    inv,ld=v2.inverse(cov[np.ix_(g,g)])
    return float(.5*(len(delta)*np.log(2*np.pi)+ld+delta@inv@delta)/len(delta))


def select_multiplier(rows):
    table=pd.DataFrame(rows)
    if table.empty or table.validation_cycle.nunique()<CONFIG['validation_cycles']:
        return 1.,'fallback_insufficient_validation'
    scores=table.groupby('variance_multiplier').nld_per_state.mean()
    a=min(scores.index,key=lambda a:(scores.loc[a],abs(np.log2(a)),a))
    return float(a),'last_three_cycles_joint_log_score'


class Experiment:
    def __init__(self,history,source,out=None):
        self.source=Path(source);self.out=Path(out) if out else None
        self.histories={};self.weights=[]
        for recipe in RECIPES:
            h,w=construct_history(history,recipe);self.histories[recipe]=h;self.weights.append(w)
        self.fit_cache={};self.choice_cache={};self.base_cache={};self.half_cache={}
        self.cov_tuning=[];self.half_tuning=[];self.scale_tuning=[];self.diagnostics=[]
        self.source_diag=pd.read_parquet(self.source/'fit_diagnostics.parquet')

    def hist(self,recipe,scenario):
        h=self.histories[recipe];return h[h.scenario.eq(scenario)]

    def get_fit(self,recipe,scenario,year,kind,k):
        # Outcome residuals do not depend on poll horizon: share those exact fits.
        cache_s=scenario if kind=='poll' else 'all'
        cache_r='current' if kind=='poll' else recipe
        key=(cache_r,cache_s,int(year),kind,float(k))
        if key in self.fit_cache:return self.fit_cache[key]
        h=self.hist(cache_r,scenario)
        old=self.source_diag.query('scenario==@scenario and cycle==@year and component==@kind and kappa==@k') if cache_r=='current' else pd.DataFrame()
        reused=False
        if len(old):
            row=old.iloc[0];z=np.load(self.source/row.path)
            x,noise,w,years,tr=v2.blocks(h,year,kind)
            mass=(np.isfinite(x)*w[:,None]).sum(axis=0)
            mean=np.divide(np.nansum(x*w[:,None],axis=0),mass,out=np.full(50,np.nan),where=mass>0)
            rms=np.sqrt(np.divide(np.nansum(x*x*w[:,None],axis=0),mass,out=np.full(50,np.nan),where=mass>0))
            f={name:z[name] for name in z.files}
            f.update(kappa=k,training_max_cycle=int(years.max()),training_first_cycle=int(years.min()),
                     training_cycles=len(years),training_rows=len(tr),iterations=int(row.iterations),
                     relative_change=float(row.relative_change),min_eigenvalue=float(row.min_eigenvalue),converged=True,
                     observed_weight=mass,residual_means=mean,observed_rms=rms)
            reused=True
        else:f=v2.fit_component(h,year,kind,k)
        self.fit_cache[key]=f
        path=f'fits/{cache_r}_{cache_s}_{year}_{kind}_k{k:g}.npz'
        if self.out:
            arrays={name:value for name,value in f.items() if isinstance(value,np.ndarray)}
            np.savez_compressed(self.out/path,**arrays)
        self.diagnostics.append(dict(recipe=cache_r,scenario=cache_s,cycle=int(year),component=kind,kappa=k,
                                     training_max_cycle=f['training_max_cycle'],training_cycles=f['training_cycles'],
                                     iterations=f['iterations'],converged=f['converged'],min_eigenvalue=f['min_eigenvalue'],
                                     min_objective_increment=float(np.diff(f['objective']).min()),reused_v2=reused,path=path))
        if len(self.fit_cache)%25==0:print(f'  Cached {len(self.fit_cache)} component fits',flush=True)
        return f

    def choose_fit(self,recipe,scenario,year,kind):
        recipe='current' if kind=='poll' else recipe
        key=(recipe,scenario,int(year),kind)
        if key in self.choice_cache:return self.choice_cache[key]
        h=self.hist(recipe,scenario);_,_,_,years,_=v2.blocks(h,year,kind)
        minimum=3 if kind=='poll' else 4
        valid=years[minimum:][-v2.CONFIG['validation_cycles']:]
        candidates=[]
        for k in v2.CONFIG['regularization_candidates']:
            scores=[]
            for vy in valid:
                fit=self.get_fit(recipe,scenario,int(vy),kind,k)
                score,n=v2.validation_score(h,int(vy),kind,fit);scores.append(score)
                self.cov_tuning.append(dict(recipe=recipe,scenario=scenario,forecast_cycle=int(year),component=kind,kappa=k,
                                           validation_cycle=int(vy),fit_max_cycle=fit['training_max_cycle'],n=n,nld_per_state=score))
            candidates.append((np.mean(scores) if scores else 0.,-k,k))
        k=min(candidates)[2];f=self.get_fit(recipe,scenario,year,kind,k)
        self.choice_cache[key]=f
        return f

    def base(self,family,scenario,year):
        key=(family,scenario,int(year))
        if key in self.base_cache:return self.base_cache[key]
        recipe=family
        if family=='decay':
            hk=(scenario,int(year))
            if hk not in self.half_cache:
                r,rows=choose_half_life({k:self.hist(k,scenario) for k in RECIPES},year)
                self.half_cache[hk]=r;self.half_tuning.extend([dict(scenario=scenario,**row) for row in rows])
            recipe=self.half_cache[hk]
        h=self.hist(recipe,scenario);test=h[h.cycle.eq(year)].sort_values('target_id').reset_index(drop=True)
        if test.empty:raise ValueError('No targets')
        mov=self.choose_fit(recipe,scenario,year,'movement');poll=self.choose_fit('current',scenario,year,'poll')
        value=(test,mov,poll,recipe);self.base_cache[key]=value;return value

    def strength(self,family,scenario,year):
        h=self.hist('current',scenario)
        years=sorted(h.loc[h.cycle.lt(year)&h.actual.notna(),'cycle'].unique());valid=[]
        for vy in years:
            _,_,_,ym,_=v2.blocks(h,vy,'movement');_,_,_,yp,_=v2.blocks(h,vy,'poll')
            if len(ym)>=4 and len(yp)>=3:valid.append(int(vy))
        valid=valid[-CONFIG['validation_cycles']:];rows=[]
        if len(valid)<CONFIG['validation_cycles']:return 1.,'fallback_insufficient_validation',valid
        for vy in valid:
            test,mov,poll,recipe=self.base(family,scenario,vy)
            for a in CONFIG['variance_multipliers']:
                pred,cov,_=scaled_predict(test,mov,poll,a)
                rows.append(dict(family=family,scenario=scenario,forecast_cycle=int(year),validation_cycle=vy,
                                 validation_recipe=recipe,fit_max_cycle=max(mov['training_max_cycle'],poll['training_max_cycle']),
                                 movement_kappa=mov['kappa'],poll_kappa=poll['kappa'],variance_multiplier=a,
                                 n=len(test),nld_per_state=predictive_score(pred,cov),mae_pp=float(abs(pred.prediction_pp-100*pred.actual).mean())))
        self.scale_tuning.extend(rows);a,status=select_multiplier(rows);return a,status,valid


def build(lab):
    lab=Path(lab).resolve();source=lab/'reports/bayesian_revision2'/SOURCE_NAME
    source_hash=v1.verify(source);settings=json.loads((source/'settings.json').read_text())
    notebooks={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='BAYESIAN_PRIOR_REVISION3.ipynb'}
    history=pd.read_parquet(source/'prepared_history.parquet')
    old=pd.read_parquet(source/'predictions.parquet');old=old[old.model.isin(['v2_linked','v1_linked','nonbayes_bias','nonbayes_momentum','raw30'])]
    cases=old[old.model.eq('v2_linked')][['scenario','cycle','target_id','history_selection_10pp']]
    ledger=next(Path(p) for p in settings['provenance']['paths'] if p.endswith('state_surprise/20260919T011532.132689Z/full_seat_ledger.parquet'))
    roster=pd.read_parquet(ledger).query("model=='polling'")
    out=lab/'reports/bayesian_prior_revision3'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    (out/'fits').mkdir(parents=True);(out/'draws').mkdir()
    ex=Experiment(history,source,out);preds=[];seats=[];selected=[];priors=[];statepars=[];masked=[]
    for (scenario,year),case in cases.groupby(['scenario','cycle']):
        for family in FAMILIES:
            test,mov,poll,recipe=ex.base(family,scenario,int(year))
            test=test.merge(case[['target_id','history_selection_10pp']],on='target_id',validate='one_to_one').sort_values('target_id').reset_index(drop=True)
            if set(test.target_id)!=set(case.target_id):raise ValueError('Mismatched targets')
            a,status,valid=ex.strength(family,scenario,int(year))
            selected.append(dict(scenario=scenario,cycle=int(year),family=family,recipe=recipe,half_life=float(recipe[5:]) if recipe.startswith('decay') else np.nan,
                                 variance_multiplier=a,prior_penalty_strength=1/a,strength_status=status,validation_cycles=','.join(map(str,valid)),
                                 movement_kappa=mov['kappa'],poll_kappa=poll['kappa'],training_max_cycle=max(mov['training_max_cycle'],poll['training_max_cycle']),
                                 strength_at_grid_edge=a in [min(CONFIG['variance_multipliers']),max(CONFIG['variance_multipliers'])]))
            p=test[['scenario','cycle','target_id','geography','actual','prior','source_prior','prior_effective_n','prior_history_n','prior_source_max_cycle','prior_fallback']].copy()
            p['family']=family;p['recipe']=recipe;p['prior_error_pp']=100*(p.actual-p.prior);priors.append(p)
            if year==2026:
                for i,s in enumerate(v2.STATES):
                    statepars.append(dict(state=s,family=family,recipe=recipe,base_prior_sd_pp=np.sqrt(mov['covariance'][i,i]),
                                          tuned_prior_sd_pp=np.sqrt(a*mov['covariance'][i,i]),observed_cycles=int(mov['pair_support'][i,i]),
                                          residual_mean_pp=mov['residual_means'][i],residual_rms_pp=mov['observed_rms'][i],
                                          centered_residual_sd_pp=np.sqrt(max(0,mov['observed_rms'][i]**2-mov['residual_means'][i]**2)) if np.isfinite(mov['observed_rms'][i]) else np.nan))
            for mode,mult in [('fixed',1.),('tuned',a)]:
                model=f'v3_{family}_{mode}';pred,cov,meta=scaled_predict(test,mov,poll,mult);pred['model']=model;preds.append(pred)
                rng=np.random.default_rng(CONFIG['seed']+int(year)+(scenario=='oct31')*10000)
                draws=pred.prediction_pp.to_numpy()+rng.standard_normal((CONFIG['draws'],len(test)))@np.linalg.cholesky(cov).T
                np.savez_compressed(out/'draws'/f'{scenario}_{year}_{model}.npz',margins_pp=draws,covariance_pp2=cov,
                                    prior_covariance_pp2=meta['prior_covariance'],target_ids=test.target_id.to_numpy(str))
                rr=roster[roster.scenario.eq(scenario)&roster.cycle.eq(year)];seat=v1.seat_counts(rr,test,pred,draws)
                counts=seat['fixed_D']+(draws>0).sum(axis=1);lo,hi=np.quantile(counts,[.15,.85],method='inverted_cdf')
                seat.update(expected_D_exact=float(seat['fixed_D']+pred.p_dem.sum()),D_lo70=int(lo),D_hi70=int(hi))
                seats.append(dict(scenario=scenario,cycle=int(year),model=model,**seat))
                if year in [2020,2024,2026]:
                    for idx,t in test[test.q_pp.notna()].iterrows():
                        hidden=test.copy();hidden.loc[idx,'q_pp']=np.nan
                        pr,_,_=scaled_predict(hidden,mov,poll,mult);r=pr.iloc[idx]
                        masked.append(dict(scenario=scenario,cycle=int(year),model=model,target_id=t.target_id,geography=t.geography,
                                           actual=t.actual,prior_pp=100*t.prior,prediction_pp=r.prediction_pp,p_dem=r.p_dem,posterior_sd_pp=r.posterior_sd_pp))
            print(f'{scenario} {year}: {family} -> {recipe}, variance multiplier {a:g}',flush=True)
    allpred=pd.concat(preds+[old],ignore_index=True);allpred.to_parquet(out/'predictions.parquet',index=False)
    v1.scores(allpred).to_parquet(out/'metrics.parquet',index=False)
    frames=dict(selected=pd.DataFrame(selected),prior_predictions=pd.concat(priors,ignore_index=True),state_parameters=pd.DataFrame(statepars),
                seats=pd.DataFrame(seats),masked_predictions=pd.DataFrame(masked),half_life_tuning=pd.DataFrame(ex.half_tuning),
                strength_tuning=pd.DataFrame(ex.scale_tuning),covariance_tuning=pd.DataFrame(ex.cov_tuning),
                fit_diagnostics=pd.DataFrame(ex.diagnostics),prior_weights=pd.concat(ex.weights,ignore_index=True))
    for name,f in frames.items():f.to_parquet(out/f'{name}.parquet',index=False)
    pd.concat(ex.histories.values(),ignore_index=True).to_parquet(out/'prepared_histories.parquet',index=False)
    v1.json_write(out/'settings.json',dict(config=CONFIG,v2_config=v2.CONFIG,source=str(source),source_manifest_sha256=source_hash,
                                        provenance=settings['provenance'],as_of=settings['as_of'],old_notebook_hashes=notebooks,
                                        inference='Empirical Bayes; shared variance multiplier selected on last three earlier cycles',
                                        uncertainty_in_covariance_and_hyperparameter_selection=False,promotion=False))
    for name in ['bayesian_prior_revision3.py','bayesian_revision2.py','simple_bayesian_polling.py']:
        (out/name).write_bytes((lab/'scripts'/name).read_bytes())
    (out/'BAYESIAN_PRIOR_REVISION3.md').write_bytes((lab/'BAYESIAN_PRIOR_REVISION3.md').read_bytes())
    v1.manifest(out)
    # A completed/audited report publishes latest.json, not a partial fit run.
    return out


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1])
    print(build(parser.parse_args().lab))
