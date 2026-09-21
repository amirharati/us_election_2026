"""Recent state-specific prior penalties, shrunk toward a learned shared fallback."""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import bayesian_prior_revision3 as v3
import bayesian_revision2 as v2
import simple_bayesian_polling as v1

SOURCE_NAME='20260919T152739.765073Z'
CONFIG=dict(recent_half_life_years=4.,shrinkage_mass=2.,variance_candidates=[.25,.5,1.,2.,4.],
            seed=419926,draws=20000)
FAMILIES=v3.FAMILIES
MODELS=[f'v4_{f}_state' for f in FAMILIES]
LABELS={**v3.LABELS,**{f'v4_{f}_state':f'{f.title()} prior / state-shrunk strength' for f in FAMILIES}}


def state_predict(test,movement,poll,multipliers,observe_ids=None):
    a=np.asarray(multipliers,float)
    if a.shape!=(len(v2.STATES),) or not np.isfinite(a).all() or (a<=0).any():
        raise ValueError('Need one finite positive multiplier per state')
    d=np.sqrt(a);cov=movement['covariance']*np.outer(d,d)
    pred,c,meta=v2.predict(test,{**movement,'covariance':cov},poll,observe_ids=observe_ids)
    idx=[v2.STATES.index(s) for s in pred.geography]
    pred['variance_multiplier']=a[idx];pred['prior_penalty_strength']=1/a[idx]
    pred['prior_sd_pp']=np.sqrt(np.diag(meta['prior_covariance']))
    return pred,c,meta


def shrink_state_scores(scores,shared,forecast_year):
    """Recent training surface -> shrunken per-state scale; no future outcomes accepted."""
    if shared<=0 or not np.isfinite(shared):raise ValueError('Invalid shared multiplier')
    if not scores.empty:
        if (scores.validation_cycle>=forecast_year).any():raise ValueError('Future validation label')
        if (scores.fit_max_cycle>=scores.validation_cycle).any():raise ValueError('Nonchronological validation fit')
        if not np.isfinite(scores[['weight','nld','candidate']]).all().all() or (scores.weight<=0).any():raise ValueError('Invalid tuning score')
        if scores.duplicated(['state','validation_cycle','candidate']).any():raise ValueError('Duplicate state/cycle candidate')
    rows=[];a=np.full(len(v2.STATES),shared)
    for idx,s in enumerate(v2.STATES):
        g=scores[scores.state.eq(s)] if not scores.empty else scores
        if g.empty:
            rows.append(dict(state=s,shared_multiplier=shared,raw_multiplier=shared,variance_multiplier=shared,
                             penalty_strength=1/shared,validation_n=0,validation_years='',recent_mass=0.,local_fraction=0.,
                             status='shared_fallback_no_recent_outcomes',raw_at_grid_edge=False))
            continue
        sizes=g.groupby('candidate').validation_cycle.apply(lambda x:tuple(sorted(x)))
        if set(sizes.index)!=set(CONFIG['variance_candidates']) or len(set(sizes))!=1:raise ValueError('Unequal candidate evidence')
        evidence=g[['validation_cycle','weight']].drop_duplicates('validation_cycle')
        mass=float(evidence.weight.sum());n=len(evidence)
        candidate_scores=g.assign(weighted=lambda x:x.weight*x.nld).groupby('candidate').weighted.sum()/mass
        raw=float(min(candidate_scores.index,key=lambda x:(candidate_scores.loc[x],abs(np.log(x/shared)),x)))
        r=mass/(mass+CONFIG['shrinkage_mass'])
        final=float(np.exp((1-r)*np.log(shared)+r*np.log(raw)));a[idx]=final
        rows.append(dict(state=s,shared_multiplier=shared,raw_multiplier=raw,variance_multiplier=final,
                         penalty_strength=1/final,validation_n=n,validation_years=','.join(map(str,sorted(evidence.validation_cycle.astype(int)))),
                         recent_mass=mass,local_fraction=r,status='state_preference_shrunk_to_shared',
                         raw_at_grid_edge=raw in [min(CONFIG['variance_candidates']),max(CONFIG['variance_candidates'])]))
    return a,pd.DataFrame(rows)


class FrozenBases:
    """Recover the exact nested fits/mean choices already validated in Revision 3."""
    def __init__(self,source):
        self.source=Path(source);v1.verify(self.source)
        self.history=pd.read_parquet(self.source/'prepared_histories.parquet')
        self.cov_tuning=pd.read_parquet(self.source/'covariance_tuning.parquet')
        self.half_tuning=pd.read_parquet(self.source/'half_life_tuning.parquet')
        self.diag=pd.read_parquet(self.source/'fit_diagnostics.parquet')
        self.selected=pd.read_parquet(self.source/'selected.parquet')
        self.strength_tuning=pd.read_parquet(self.source/'strength_tuning.parquet')
        self.cache={};self.used={}

    def component(self,recipe,scenario,year,kind):
        if kind=='poll':recipe='current'
        t=self.cov_tuning
        t=t[t.recipe.eq(recipe)&t.scenario.eq(scenario)&t.forecast_cycle.eq(year)&t.component.eq(kind)]
        if t.empty:raise ValueError('Missing frozen nested covariance choice')
        scores=t.groupby('kappa').nld_per_state.mean();k=float(min(scores.index,key=lambda k:(scores.loc[k],-k)))
        cs=scenario if kind=='poll' else 'all';d=self.diag
        row=d[d.recipe.eq(recipe)&d.scenario.eq(cs)&d.cycle.eq(year)&d.component.eq(kind)&d.kappa.eq(k)]
        if len(row)!=1:raise ValueError('Missing/duplicate frozen component')
        row=row.iloc[0];key=str(row.path)
        if key not in self.cache:
            z=np.load(self.source/key);self.cache[key]={name:z[name] for name in z.files}
        f={**self.cache[key],'kappa':k,'training_max_cycle':int(row.training_max_cycle),'path':key}
        self.used[key]=dict(recipe=recipe,scenario=cs,cycle=int(year),component=kind,kappa=k,
                            training_max_cycle=int(row.training_max_cycle),path=key,sha256=v1.sha(self.source/key))
        return f

    def base(self,family,scenario,year):
        recipe=family
        if family=='decay':
            t=self.half_tuning;t=t[t.scenario.eq(scenario)&t.forecast_cycle.eq(year)]
            scores=t.groupby('half_life').prior_mae_pp.mean()
            half=min(scores.index,key=lambda h:(scores.loc[h],{8.:0,16.:1,4.:2}[h]));recipe=f'decay{half:g}'
        h=self.history;test=h[h.prior_recipe.eq(recipe)&h.scenario.eq(scenario)&h.cycle.eq(year)].sort_values('target_id').reset_index(drop=True)
        if test.empty or test.geography.duplicated().any():raise ValueError('Missing/duplicate target state')
        return test,self.component(recipe,scenario,year,'movement'),self.component('current',scenario,year,'poll'),recipe

    def tune(self,family,scenario,year):
        s=self.selected;s=s[s.family.eq(family)&s.scenario.eq(scenario)&s.cycle.eq(year)]
        if len(s)!=1:raise ValueError('Missing shared selection')
        shared=float(s.iloc[0].variance_multiplier)
        t=self.strength_tuning;t=t[t.family.eq(family)&t.scenario.eq(scenario)&t.forecast_cycle.eq(year)]
        reconstructed,status=v3.select_multiplier(t.to_dict('records'))
        if reconstructed!=shared or status!=s.iloc[0].strength_status:raise ValueError('Shared choice reconstruction failed')
        years=sorted(t.validation_cycle.unique());rows=[]
        for vy in years:
            if vy>=year:raise ValueError('Future tuning year')
            test,mov,poll,recipe=self.base(family,scenario,int(vy))
            weight=float(np.exp2(-(max(years)-vy)/CONFIG['recent_half_life_years']))
            for i,r in test[test.actual.notna()].iterrows():
                si=v2.STATES.index(r.geography)
                for candidate in CONFIG['variance_candidates']:
                    a=np.full(50,shared);a[si]=candidate
                    pred,_,_=state_predict(test,mov,poll,a);p=pred.iloc[i]
                    rows.append(dict(family=family,scenario=scenario,forecast_cycle=int(year),validation_cycle=int(vy),
                                     state=r.geography,target_id=r.target_id,validation_recipe=recipe,
                                     fit_max_cycle=max(mov['training_max_cycle'],poll['training_max_cycle']),
                                     shared_multiplier=shared,candidate=candidate,weight=weight,
                                     actual_pp=100*r.actual,prediction_pp=p.prediction_pp,sd_pp=p.posterior_sd_pp,
                                     nld=float(-norm.logpdf(100*r.actual,p.prediction_pp,p.posterior_sd_pp))))
        surface=pd.DataFrame(rows)
        a,profile=shrink_state_scores(surface,shared,year)
        return a,profile.assign(family=family,scenario=scenario,cycle=int(year)),surface


def build(lab):
    lab=Path(lab).resolve();source=lab/'reports/bayesian_prior_revision3'/SOURCE_NAME
    source_hash=v1.verify(source);settings=json.loads((source/'settings.json').read_text())
    old_hashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='BAYESIAN_STATE_PENALTY.ipynb'}
    for p,s in settings['provenance']['paths'].items():
        if v1.sha(p)!=s:raise ValueError('Source changed: '+p)
    refs=pd.read_parquet(source/'predictions.parquet')
    cases=refs[refs.model.eq('v3_decay_fixed')][['scenario','cycle','target_id','history_selection_10pp']]
    ledger=next(Path(p) for p in settings['provenance']['paths'] if p.endswith('state_surprise/20260919T011532.132689Z/full_seat_ledger.parquet'))
    roster=pd.read_parquet(ledger).query("model=='polling'")
    out=lab/'reports/bayesian_state_penalty'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    (out/'draws').mkdir(parents=True)
    bases=FrozenBases(source);predictions=[];profiles=[];surfaces=[];seats=[];folds=[];masked=[]
    for (scenario,year),case in cases.groupby(['scenario','cycle']):
        for family in FAMILIES:
            test,mov,poll,recipe=bases.base(family,scenario,int(year))
            test=test.merge(case[['target_id','history_selection_10pp']],on='target_id',validate='one_to_one').sort_values('target_id').reset_index(drop=True)
            if set(test.target_id)!=set(case.target_id):raise ValueError('Different forecast cases')
            a,profile,surface=bases.tune(family,scenario,int(year));profiles.append(profile);surfaces.append(surface)
            model=f'v4_{family}_state';pred,cov,meta=state_predict(test,mov,poll,a);pred['model']=model;predictions.append(pred)
            shared=float(profile.shared_multiplier.iloc[0]);control,_,_=state_predict(test,mov,poll,np.full(50,shared))
            old=refs[refs.model.eq(f'v3_{family}_tuned')&refs.scenario.eq(scenario)&refs.cycle.eq(year)].set_index('target_id').loc[test.target_id]
            control_error=float(np.max(abs(control.prediction_pp.to_numpy()-old.prediction_pp.to_numpy())))
            if control_error>1e-9:raise ValueError('Shared reference differs')
            folds.append(dict(scenario=scenario,cycle=int(year),family=family,recipe=recipe,shared_multiplier=shared,
                              movement_path=mov['path'],poll_path=poll['path'],training_max_cycle=max(mov['training_max_cycle'],poll['training_max_cycle']),
                              shared_control_max_error_pp=control_error,states_with_recent_evidence=int((profile.validation_n>0).sum()),
                              fallback_states=int((profile.validation_n==0).sum())))
            rng=np.random.default_rng(CONFIG['seed']+int(year)+(scenario=='oct31')*10000)
            draws=pred.prediction_pp.to_numpy()+rng.standard_normal((CONFIG['draws'],len(test)))@np.linalg.cholesky(cov).T
            np.savez_compressed(out/'draws'/f'{scenario}_{year}_{model}.npz',margins_pp=draws,covariance_pp2=cov,
                                prior_covariance_pp2=meta['prior_covariance'],multipliers_all_states=a,target_ids=test.target_id.to_numpy(str))
            rr=roster[roster.scenario.eq(scenario)&roster.cycle.eq(year)];seat=v1.seat_counts(rr,test,pred,draws)
            counts=seat['fixed_D']+(draws>0).sum(axis=1);lo,hi=np.quantile(counts,[.15,.85],method='inverted_cdf')
            seat.update(expected_D_exact=float(seat['fixed_D']+pred.p_dem.sum()),D_lo70=int(lo),D_hi70=int(hi))
            seats.append(dict(scenario=scenario,cycle=int(year),model=model,**seat))
            if year in [2020,2024,2026]:
                for idx,t in test[test.q_pp.notna()].iterrows():
                    hidden=test.copy();hidden.loc[idx,'q_pp']=np.nan
                    pr,_,_=state_predict(hidden,mov,poll,a);r=pr.iloc[idx]
                    masked.append(dict(scenario=scenario,cycle=int(year),model=model,target_id=t.target_id,geography=t.geography,
                                       actual=t.actual,prior_pp=100*t.prior,prediction_pp=r.prediction_pp,p_dem=r.p_dem))
            print(f'{scenario} {year} {family}: shared a={shared:g}, state a range {a.min():.3f}–{a.max():.3f}; {sum(profile.validation_n==0)} fallbacks',flush=True)
    pred=pd.concat(predictions+[refs],ignore_index=True);pred.to_parquet(out/'predictions.parquet',index=False)
    v1.scores(pred).to_parquet(out/'metrics.parquet',index=False)
    frames=dict(state_penalties=pd.concat(profiles,ignore_index=True),local_tuning=pd.concat(surfaces,ignore_index=True),
                folds=pd.DataFrame(folds),seats=pd.DataFrame(seats),masked_predictions=pd.DataFrame(masked),
                used_components=pd.DataFrame(list(bases.used.values())))
    for name,f in frames.items():f.to_parquet(out/f'{name}.parquet',index=False)
    v1.json_write(out/'settings.json',dict(config=CONFIG,source=str(source),source_manifest_sha256=source_hash,
                                        provenance=settings['provenance'],old_notebook_hashes=old_hashes,as_of=settings['as_of'],
                                        inference='Empirical-Bayes Gaussian update with two-stage state log-scale shrinkage',
                                        selection_uncertainty=False,promotion=False,new_covariance_fits=0))
    for name in ['bayesian_state_penalty.py','bayesian_prior_revision3.py','bayesian_revision2.py','simple_bayesian_polling.py']:
        (out/name).write_bytes((lab/'scripts'/name).read_bytes())
    (out/'BAYESIAN_STATE_PENALTY.md').write_bytes((lab/'BAYESIAN_STATE_PENALTY.md').read_bytes())
    v1.manifest(out)
    return out


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1]);print(build(p.parse_args().lab))
