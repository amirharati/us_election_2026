"""Rebuild matched model comparisons after explicit official-result admission.

No new model recipes. Reuses a covariance fit only if its numerical training
blocks, measurement variances and relevance weights match exactly.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import numpy as np
import pandas as pd
import simple_bayesian_polling as v1
import bayesian_revision2 as v2
import bayesian_prior_revision3 as v3
import bayesian_prior_revision5 as v5
import bayesian_state_penalty as v4

REFERENCE='20260919T170530.015181Z'
FAMILIES=['current','latest','decay','fast','corrected']
MODES=['fixed','shared','state']
LABELS={f'{f}_{m}':f'{f.title()} prior / {m}' for f in FAMILIES for m in MODES}
LABELS.update(raw30='Raw 30-day polling', prior='Historical prior',polling='Tuned polling',bias='Polling + historical bias',
              movement_diagonal='Current prior / movement links off',local='Current prior / all links off')


def prepare(lab,snapshot,out):
    from load_final_dataset import open_dataset
    from contextual_baselines import calendar_inputs,make_store
    from simple_baselines import prepare_inputs
    from poll_error_baselines import build_poll_history
    from bias_momentum_stack import build_bias_history
    from competitive_evaluation import competitive_ledger
    data=open_dataset(snapshot=snapshot);store=make_store(data)
    histories=[];samples=[];audits=[];calendars=[];pollgrids=[];biasgrids=[];fits=[];members=[]
    for scenario in ['matched_live','oct31']:
        inp,cal,endpoints=calendar_inputs(data,store,scenario)
        targets,waves,audit,exclusions=prepare_inputs(data,inp)
        hist,grid=build_poll_history(targets,waves,scenario)
        h,bg,bf=build_bias_history(hist,scenario);h=h[h.base.eq('fixed5_8')].copy()
        release=audit.set_index('observation_id').release
        waves['available_date']=[max(r.field_end,release.reindex(r.observation_ids.split('|')).max()) if release.reindex(r.observation_ids.split('|')).notna().any() else r.field_end for r in waves.itertuples()]
        if waves.available_date.gt(waves.cutoff).any():raise ValueError('Future poll admitted')
        h=h.merge(v1.aggregate(h,waves),on='target_id',validate='one_to_one')
        comp=competitive_ledger(h,h,thresholds=(10.,));comp['scenario']=scenario
        h=h.merge(comp[['cycle','geography','selection']].rename(columns={'selection':'history_selection_10pp'}),on=['cycle','geography'],validate='many_to_one')
        histories.append(h);samples.append(waves.assign(scenario=scenario));audits.append(audit.assign(scenario=scenario));calendars.append(cal);members.append(comp)
        pollgrids.append(grid);biasgrids.append(bg);fits.extend(bf)
    h=pd.concat(histories,ignore_index=True);cal=pd.concat(calendars,ignore_index=True)
    for name,f in dict(history=h,samples=pd.concat(samples),sample_audit=pd.concat(audits),calendars=cal,
                       competitiveness=pd.concat(members),poll_tuning=pd.concat(pollgrids),bias_tuning=pd.concat(biasgrids)).items():f.to_parquet(out/(name+'.parquet'),index=False)
    v1.json_write(out/'bias_fits.json',fits)
    return h,cal,data.metadata()


class Experiment(v5.Experiment):
    def __init__(self,history,source,out):
        super().__init__(source,out)
        original_histories=self.histories
        self.histories={r:v3.construct_history(history,r)[0] for r in v3.RECIPES}
        self.histories['decay2']=v5.decay_two(history)
        valid=[]
        for i,row in self.source_diag.iterrows():
            recipe=row.recipe.removesuffix('_corrected')
            scenario=row.scenario if row.scenario!='all' else 'matched_live'
            a=v2.blocks(self.hist(recipe,scenario),int(row.cycle),row.component)
            oh=original_histories[recipe];b=v2.blocks(oh[oh.scenario.eq(scenario)],int(row.cycle),row.component)
            if all(np.array_equal(x,y,equal_nan=True) for x,y in zip(a[:4],b[:4])):valid.append(i)
        self.reuse_candidates=len(valid);self.source_diag=self.source_diag.loc[valid].copy()
        self.review_half_cache={}

    def base(self,family,scenario,year):
        if family in ['fast','corrected']:return super().base(family,scenario,year)
        key=(family,scenario,int(year))
        if key in self.base_cache:return self.base_cache[key]
        recipe=family
        if family=='decay':
            hk=(scenario,int(year))
            if hk not in self.review_half_cache:
                r,rows=v3.choose_half_life({k:self.hist(k,scenario) for k in v3.RECIPES},year)
                self.review_half_cache[hk]=r
                self.half_tuning.extend([dict(scenario=scenario,selector='original_grid',**row) for row in rows])
            recipe=self.review_half_cache[hk]
        test=self.hist(recipe,scenario);test=test[test.cycle.eq(year)].sort_values('target_id').reset_index(drop=True).copy()
        f=self.choose_fit(recipe,scenario,year,'movement');poll=self.choose_fit('current',scenario,year,'poll')
        test['base_prior_pp']=100*test.prior;test['mean_correction_pp']=0.
        mov={**f,'process_covariance':f['covariance'],'correction_covariance':np.zeros_like(f['covariance'])}
        value=(test,mov,poll,recipe);self.base_cache[key]=value;return value


def build(lab,snapshot):
    lab=Path(lab).resolve();snapshot=Path(snapshot).resolve()
    ref=lab/'reports/bayesian_prior_revision5'/REFERENCE;refhash=v1.verify(ref)
    notebook_hashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='OFFICIAL_REPAIR_MODEL_REVIEW.ipynb'}
    out=lab/'reports/official_repair_review'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    (out/'fits').mkdir(parents=True);(out/'draws').mkdir()
    print('OUTPUT',out,flush=True)
    h,cal,metadata=prepare(lab,snapshot,out)
    from momentum_approval_models import evaluate
    npred,nfolds,ngrid,nfits=evaluate(h,cal)
    npred=npred.merge(h[['scenario','target_id','history_selection_10pp','q_pp','firm_mass']],on=['scenario','target_id'],validate='many_to_one')
    npred['prediction_pp']=100*npred.prediction;npred['p_dem']=np.nan
    npred.to_parquet(out/'nonbayesian_predictions.parquet',index=False);nfolds.to_parquet(out/'nonbayesian_folds.parquet',index=False);ngrid.to_parquet(out/'feature_tuning.parquet',index=False);v1.json_write(out/'feature_fits.json',nfits)
    ex=Experiment(h,ref,out)
    oldsettings=json.loads((ref/'settings.json').read_text())
    ledger=next(Path(p) for p in oldsettings['provenance']['paths'] if p.endswith('state_surprise/20260919T011532.132689Z/full_seat_ledger.parquet'))
    roster=pd.read_parquet(ledger).query('model=="polling"')
    roster.to_parquet(out/'full_seat_ledger.parquet',index=False)
    cases=npred[npred.model.eq('bias')][['scenario','cycle','target_id']]
    predictions=[npred];folds=[];profiles=[];seats=[];priors=[]
    def save_prediction(pred,cov,meta,test,mult,model,scenario,year):
        pred['model']=model;predictions.append(pred)
        rng=np.random.default_rng(619926+int(year)+(scenario=='oct31')*10000)
        draws=pred.prediction_pp.to_numpy()+rng.standard_normal((20000,len(test)))@np.linalg.cholesky(cov).T
        np.savez_compressed(out/'draws'/f'{scenario}_{year}_{model}.npz',margins_pp=draws,covariance_pp2=cov,prior_covariance_pp2=meta['prior_covariance'],multipliers_all_states=mult,target_ids=test.target_id.to_numpy(str))
        rr=roster[roster.scenario.eq(scenario)&roster.cycle.eq(year)]
        s=v1.seat_counts(rr,test,pred,draws);counts=s['fixed_D']+(draws>0).sum(axis=1)
        lo,hi=np.quantile(counts,[.15,.85],method='inverted_cdf')
        s.update(expected_D_exact=float(s['fixed_D']+pred.p_dem.sum()),D_lo70=int(lo),D_hi70=int(hi))
        seats.append(dict(scenario=scenario,cycle=int(year),model=model,**s))
    for (scenario,year),case in cases.groupby(['scenario','cycle']):
        for family in FAMILIES:
            test,mov,poll,recipe=ex.base(family,scenario,int(year))
            assert set(test.target_id)==set(case.target_id)
            shared,status,valid=ex.strength(family,scenario,int(year));a,profile=ex.state_strength(family,scenario,int(year));profiles.append(profile)
            folds.append(dict(scenario=scenario,cycle=int(year),family=family,recipe=recipe,shared_multiplier=shared,strength_status=status,movement_path=mov['path'],poll_path=poll['path'],training_max_cycle=max(mov['training_max_cycle'],poll['training_max_cycle'])))
            priors.append(test[['scenario','cycle','target_id','geography','actual','prior','base_prior_pp','mean_correction_pp']].assign(family=family))
            for mode,mult in [('fixed',np.ones(50)),('shared',np.full(50,shared)),('state',a)]:
                pred,cov,meta=v4.state_predict(test,mov,poll,mult)
                save_prediction(pred,cov,meta,test,mult,f'{family}_{mode}',scenario,year)
            if family=='current':
                for name,mode in [('movement_diagonal','v2_movement_diagonal'),('local','v2_local')]:
                    pred,cov,meta=v2.predict(test,mov,poll,model=mode)
                    save_prediction(pred,cov,meta,test,np.ones(50),name,scenario,year)
                raw=test.copy();raw['prediction_pp']=raw.q_pp.fillna(100*raw.prior);raw['prediction']=raw.prediction_pp/100;raw['model']='raw30';raw['p_dem']=np.nan;predictions.append(raw)
            print(scenario,year,family,recipe,'a',shared,flush=True)
    pred=pd.concat(predictions,ignore_index=True)
    frames=dict(predictions=pred,metrics=v1.scores(pred),folds=pd.DataFrame(folds),state_penalties=pd.concat(profiles),
                prior_predictions=pd.concat(priors),seats=pd.DataFrame(seats),prepared_histories=pd.concat(ex.histories.values()),
                half_life_tuning=pd.DataFrame(ex.half_tuning),covariance_tuning=pd.DataFrame(ex.cov_tuning),strength_tuning=pd.DataFrame(ex.strength_tuning),local_tuning=pd.DataFrame(ex.state_tuning),fit_diagnostics=pd.DataFrame(ex.fit_records))
    for name,f in frames.items():f.to_parquet(out/(name+'.parquet'),index=False)
    v1.json_write(out/'settings.json',dict(dataset=metadata,reference=str(ref),reference_sha256=refhash,old_notebook_hashes=notebook_hashes,
                                        reuse_rule='Exact equality of training values, noise, weights and cycle ids',reuse_candidates=ex.reuse_candidates,
                                        configs=dict(v1=v1.CONFIG,v2=v2.CONFIG,v3=v3.CONFIG,v4=v4.CONFIG,v5=v5.CONFIG),
                                        as_of=metadata['as_of'],promotion=False,polling_and_features_refreshed=False))
    for name in ['official_repair_model_review.py','bayesian_prior_revision5.py','bayesian_prior_revision3.py','bayesian_state_penalty.py','bayesian_revision2.py','simple_bayesian_polling.py','momentum_approval_models.py','official_result_reviews.py']:
        (out/name).write_bytes((lab/'scripts'/name).read_bytes())
    v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    print('COMPLETE',out,flush=True);return out


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--snapshot',type=Path);p.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args()
    if a.snapshot is None:
        from load_final_dataset import resolve_snapshot
        a.snapshot=resolve_snapshot(a.lab/'data/final')
    build(a.lab,a.snapshot)
