"""Chronological prior-center alternatives and recalibrated electoral variance."""
from pathlib import Path
from datetime import datetime,timezone
import json
import numpy as np
import pandas as pd
from scipy.stats import norm
import simple_bayesian_polling as v1
import bayesian_revision2 as v2
import national_feature_prior as feat
import simple_national_model as normal
import national_tails_waves as chamber
import national_factor_review as national
import coverage_balance as scoring
from final_baseline_experiments import cycle_metrics

RECIPES=['decay4','latest','same_seat','decay4_centered','same_seat_centered']
SCALES=[.25,.5,1.,2.,4.]
CONFIG=dict(kappa=8.,mean_error_half_life=4.,mean_error_shrink_mass=2.,variance_half_life=8.,other_cycle_weight=.5,validation_cycles=3,penalty_shrink_mass=2.,draws=30000,seed=197139)

def histories(prepared):
    base={r:prepared[prepared.prior_recipe.eq(r)].copy().reset_index(drop=True) for r in ['decay4','latest']};same=base['latest'].copy();same['same_seat_source_cycle']=np.nan;same['same_seat_fallback']=True
    for (sc,state),g in same.groupby(['scenario','geography']):
        for i,r in g.iterrows():
            if bool(r.special):continue
            past=g[g.cycle.lt(r.cycle)&g.actual.notna()&~g.special.fillna(False).astype(bool)&((r.cycle-g.cycle)%6).eq(0)].sort_values('cycle')
            if len(past):
                a=past.iloc[-1];same.loc[i,'prior']=a.actual;same.loc[i,'prior_source_max_cycle']=a.cycle;same.loc[i,'same_seat_source_cycle']=a.cycle;same.loc[i,'same_seat_fallback']=False
    base['same_seat']=same;ledger=[]
    for recipe in ['decay4','same_seat']:
        h=base[recipe].copy();h['base_prior']=h.prior;h['prior_center_shift_pp']=0.;h['center_mass']=0.;h['center_max_cycle']=np.nan
        for (sc,state),g in h.groupby(['scenario','geography']):
            for i,r in g.iterrows():
                past=g[g.cycle.lt(r.cycle)&g.actual.notna()&g.prior_latest_cycle.notna()&g.prior_latest_cycle.lt(g.cycle)].sort_values('cycle')
                if not len(past):continue
                w=np.exp2(-(r.cycle-past.cycle.to_numpy())/CONFIG['mean_error_half_life']);err=100*(past.actual-past.base_prior).to_numpy();shift=float(w@err/(w.sum()+CONFIG['mean_error_shrink_mass']))
                h.loc[i,'prior']=r.base_prior+shift/100;h.loc[i,'prior_center_shift_pp']=shift;h.loc[i,'center_mass']=w.sum();h.loc[i,'center_max_cycle']=past.cycle.max()
                for t,ww,e in zip(past.itertuples(),w,err):ledger.append(dict(recipe=recipe+'_centered',scenario=sc,target_id=r.target_id,forecast_cycle=r.cycle,state=state,source_cycle=t.cycle,weight=ww,error_pp=e,contribution_pp=ww*e/(w.sum()+CONFIG['mean_error_shrink_mass'])))
        base[recipe+'_centered']=h
    for r,h in base.items():
        h['prior_recipe']=r
        if 'base_prior' not in h:h['base_prior']=h.prior;h['prior_center_shift_pp']=0.;h['center_mass']=0.;h['center_max_cycle']=np.nan
    return base,pd.DataFrame(ledger)

def choose_scales(scores,year):
    earlier=scores[scores.cycle.lt(year)] if len(scores) else scores
    years=sorted(earlier.cycle.unique())[-3:] if len(earlier) else []
    shared=1.
    if len(years)==3:
        z=earlier[earlier.cycle.isin(years)].groupby(['scale','cycle']).wis_pp.mean().groupby('scale').mean();shared=float(min(z.index,key=lambda a:(z.loc[a],abs(np.log2(a)),a)))
    rows=[];mult=[]
    for state in v1.STATES:
        q=earlier[earlier.cycle.isin(years)&earlier.geography.eq(state)] if len(earlier) else earlier
        if len(q):
            q=q.assign(weight=np.exp2(-(max(years)-q.cycle)/4));z=q.assign(loss=q.weight*q.wis_pp).groupby('scale').agg(loss=('loss','sum'),mass=('weight','sum'));z['score']=z.loss/z.mass;raw=float(min(z.index,key=lambda a:(z.loc[a,'score'],abs(np.log(a/shared)),a)));ev=q[['cycle','weight']].drop_duplicates();mass=ev.weight.sum();n=len(ev)
        else:raw=shared;mass=0.;n=0
        local=mass/(mass+2);a=float(np.exp((1-local)*np.log(shared)+local*np.log(raw)));mult.append(a);rows.append(dict(state=state,shared=shared,raw=raw,multiplier=a,local_fraction=local,mass=mass,validation_n=n,validation_years=','.join(map(str,years)),forecast_cycle=year))
    return shared,np.array(mult),pd.DataFrame(rows)

def build(lab):
    lab=Path(lab).resolve();src=lab/'reports/national_feature_prior/20260920T013619.322700Z';work=lab/'reports/simple_national_model/20260920T000314.601869Z';up=lab/'reports/official_repair_review/20260919T172552.860612Z'
    out=lab/'reports/prior_center_repair'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for d in ['fits','forecasts','recipe']:(out/d).mkdir(parents=True,exist_ok=True)
    st=dict(config=CONFIG,source=str(src),working=str(work),upstream=str(up),sources={str(p):v1.verify(p) for p in [src,work,up]},old_notebooks={p.name:v1.sha(p) for p in lab.glob('*.ipynb')},working_hash=v1.sha(lab/'WORKING_MODEL.json'),data_as_of='2026-09-17',promotion=False)
    v1.json_write(out/'settings.json',st);print('OUTPUT',out,flush=True)
    old=pd.read_parquet(src/'predictions.parquet');fold=pd.read_parquet(src/'folds.parquet');cal=pd.read_parquet(up/'calendars.parquet');roster=pd.read_parquet(up/'full_seat_ledger.parquet');hs,ledger=histories(pd.read_parquet(up/'prepared_histories.parquet'))
    pd.concat(hs.values(),ignore_index=True).to_parquet(out/'histories.parquet',index=False);ledger.to_parquet(out/'center_ledger.parquet',index=False)
    preds=[];seats=[];folds=[];surfaces=[];penalties=[];diag=[];moments=[];cache={};repro=[]
    def save(q,V,poll,fit,z,sc,year,family,recipe,mode,scale,fp):
        p,C,stats,meta=feat.predict(q,V,poll,fit,z);name=family+'__'+recipe+'__'+mode;p=p.assign(model=name,family=family,recipe=recipe,mode=mode,scale=scale);p['prior_sd_pp']=np.sqrt(np.diag(meta['prior_covariance']));preds.append(p)
        rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));draws=p.prediction_pp.to_numpy()+rng.standard_normal((CONFIG['draws'],len(q)))@np.linalg.cholesky(C).T
        ss,counts=chamber.seat_summary(roster[roster.scenario.eq(sc)&roster.cycle.eq(year)],q,p,draws);freq=np.bincount(counts,minlength=101);ss.update(scenario=sc,cycle=year,model=name,family=family,recipe=recipe,mode=mode);seats.append(scoring.seat_scores(ss,freq));path=f'forecasts/{sc}_{year}_{name}.npz'
        np.savez_compressed(out/path,target_ids=q.target_id.to_numpy(str),mean=p.prediction_pp.to_numpy(),covariance=C,prior_covariance=meta['prior_covariance'],seat_count_frequency=freq)
        folds.append(dict(scenario=sc,cycle=year,model=name,family=family,recipe=recipe,mode=mode,fit_path=fp,forecast_path=path,**stats));return p,C
    for sc,year in fold[['scenario','cycle']].drop_duplicates().sort_values(['scenario','cycle']).itertuples(index=False,name=None):
        year=int(year);pf=dict(np.load(work/f'fits/{sc}_{year}_poll.npz'));poll=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        for family in ['none','both']:
            sourcefold=fold[fold.scenario.eq(sc)&fold.cycle.eq(year)&fold.model.eq(family)].iloc[0];q=old[old.scenario.eq(sc)&old.cycle.eq(year)&old.model.eq(family)].sort_values('target_id').reset_index(drop=True);f=dict(np.load(src/sourcefold.fit_path));f['a']=float(f['a']);fp=f'fits/{sc}_{year}_{family}_baseline.npz';np.savez_compressed(out/fp,**f)
            p,C=save(q,f['budget'],poll,f,f['z'],sc,year,family,'baseline','fixed',1.,fp);repro.append(bool(np.allclose(p[['prediction_pp','p_dem']],q[['prediction_pp','p_dem']])&np.allclose(C,np.load(src/sourcefold.forecast_path)['covariance'])))
        for recipe in RECIPES:
            h=hs[recipe];h=h[h.scenario.eq(sc)];x,noise,w,years,rr=v2.blocks(h,year,'movement');key=(recipe,year)
            if key not in cache:
                v2.CONFIG['max_iterations']=16000;f=v2.fit_covariance(x,noise,w,8.);cache[key]=f
                np.savez_compressed(out/f'fits/movement_{recipe}_{year}.npz',**{k:v for k,v in f.items() if isinstance(v,np.ndarray)},training_values=x,training_noise=noise,training_weights=w,years=years)
                diag.append(dict(recipe=recipe,cycle=year,training_max_cycle=int(years.max()),training_cycles=len(years),iterations=f['iterations'],converged=f['converged'],min_eigenvalue=f['min_eigenvalue']))
            f=cache[key];V=np.diag(f['covariance']);mask=np.isfinite(x);mass=(mask*w[:,None]).sum(0);avg=np.divide(np.nansum(x*w[:,None],0),mass,out=np.zeros(50),where=mass>0);var=np.divide(np.nansum((x-avg)**2*w[:,None],0),mass,out=np.full(50,np.nan),where=mass>0)
            for i,state in enumerate(v1.STATES):moments.append(dict(scenario=sc,cycle=year,recipe=recipe,state=state,n=int(mask[:,i].sum()),mass=mass[i],mean_pp=avg[i] if mass[i] else np.nan,centered_sd_pp=np.sqrt(var[i]),rms_pp=np.sqrt(var[i]+avg[i]**2),raw_sd_pp=np.sqrt(V[i])))
            design,X,z,_,_,_=feat.prepare_design(cal[cal.scenario.eq(sc)],years,w,year)
            for family in ['none','both']:
                orig=fold[fold.scenario.eq(sc)&fold.cycle.eq(year)&fold.model.eq(family)].iloc[0];of=np.load(src/orig.fit_path);ids=[design.active.index(term) for term in of['terms']];xx=X[:,ids];zz=z[ids];tau=float(of['tau']);q=h[h.cycle.eq(year)].sort_values('target_id').reset_index(drop=True).copy();expected=old[old.scenario.eq(sc)&old.cycle.eq(year)&old.model.eq(family)].sort_values('target_id');assert list(q.target_id)==list(expected.target_id)
                fixedrows=[]
                for scale in SCALES:
                    budget=V*scale;fit=feat.fit_feature(x,noise,w,budget,xx,tau);p,C,stats,meta=feat.predict(q,budget,poll,fit,zz);p=p.assign(scale=scale,recipe=recipe,family=family,fit_max_cycle=int(years.max()));fixedrows.append(p[['scenario','cycle','target_id','geography','recipe','family','scale','fit_max_cycle','wis_pp','actual']]);
                    if scale==1:unit=fit
                prior=pd.concat(surfaces,ignore_index=True) if surfaces else pd.DataFrame();prior=prior[prior.scenario.eq(sc)&prior.recipe.eq(recipe)&prior.family.eq(family)] if len(prior) else prior
                shared,mult,pen=choose_scales(prior,year);penalties.append(pen.assign(scenario=sc,recipe=recipe,family=family));surfaces.extend(fixedrows)
                for mode,a in [('fixed',np.ones(50)),('shared',np.full(50,shared)),('state',mult)]:
                    budget=V*a;fit=unit if mode=='fixed' else feat.fit_feature(x,noise,w,budget,xx,tau);fp=f'fits/{sc}_{year}_{family}_{recipe}_{mode}.npz'
                    np.savez_compressed(out/fp,**{k:v for k,v in fit.items() if isinstance(v,np.ndarray)},a=fit['a'],budget=budget,z=zz,X=xx,tau=tau,training_values=x,training_noise=noise,training_weights=w,years=years,multipliers=a,terms=of['terms'])
                    save(q,budget,poll,fit,zz,sc,year,family,recipe,mode,shared,fp)
            print(sc,year,recipe,flush=True)
    p=pd.concat(preds,ignore_index=True);s=pd.DataFrame(seats);f=pd.DataFrame(folds);tuning=[];sp=[];ss=[];sf=[]
    for (sc,year,family),g in p.groupby(['scenario','cycle','family']):
        years=sorted(p.loc[p.scenario.eq(sc)&p.cycle.lt(year)&p.actual.notna(),'cycle'].unique())[-3:];order=[family+'__baseline__fixed']+[family+'__'+r+'__'+m for r in RECIPES for m in ['fixed','shared','state']]
        history=p[p.scenario.eq(sc)&p.cycle.isin(years)&p.family.eq(family)];scores=history.groupby(['model','cycle']).wis_pp.mean().groupby('model').mean();chosen=min(order,key=lambda n:(scores[n],order.index(n))) if len(years)==3 else order[0]
        sp.append(g[g.model.eq(chosen)].assign(model=family+'__selected',selected_model=chosen));ss.append(s[s.scenario.eq(sc)&s.cycle.eq(year)&s.model.eq(chosen)].assign(model=family+'__selected',selected_model=chosen));sf.append(f[f.scenario.eq(sc)&f.cycle.eq(year)&f.model.eq(chosen)].assign(model=family+'__selected',selected_model=chosen));tuning.append(dict(scenario=sc,cycle=year,family=family,chosen=chosen,validation_years=','.join(map(str,years))))
    p=pd.concat([p,*sp],ignore_index=True);s=pd.concat([s,*ss],ignore_index=True);f=pd.concat([f,*sf],ignore_index=True)
    for name,df in dict(predictions=p,seats=s,folds=f,scale_surface=pd.concat(surfaces,ignore_index=True),penalties=pd.concat(penalties,ignore_index=True),fit_diagnostics=pd.DataFrame(diag),residual_moments=pd.DataFrame(moments),tuning=pd.DataFrame(tuning),summary=scoring.summarize_scores(p),chamber_summary=national.chamber_summary(s),cycle_scores=cycle_metrics(p)).items():df.to_parquet(out/f'{name}.parquet',index=False)
    v1.json_write(out/'reproduction.json',dict(passed=all(repro),checks=len(repro)))
    for path in (lab/'scripts').glob('*.py'):(out/'recipe'/path.name).write_bytes(path.read_bytes())
    v1.manifest(out);audit(out,lab);v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)));print('COMPLETE',out,flush=True);return out

def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);st=json.loads((out/'settings.json').read_text());p=pd.read_parquet(out/'predictions.parquet');f=pd.read_parquet(out/'folds.parquet');s=pd.read_parquet(out/'seats.parquet');led=pd.read_parquet(out/'center_ledger.parquet');di=pd.read_parquet(out/'fit_diagnostics.parquet');su=pd.read_parquet(out/'scale_surface.parquet');pen=pd.read_parquet(out/'penalties.parquet');h=pd.read_parquet(out/'histories.parquet')
    c=dict(sources=all(v1.verify(x)==hh for x,hh in st['sources'].items()),old_notebooks=all(v1.sha(lab/n)==hh for n,hh in st['old_notebooks'].items()),working=v1.sha(lab/'WORKING_MODEL.json')==st['working_hash'],baseline=json.loads((out/'reproduction.json').read_text())['passed'],past_centers=bool(led.source_cycle.lt(led.forecast_cycle).all()),past_fit=bool(di.training_max_cycle.lt(di.cycle).all()&su.fit_max_cycle.lt(su.cycle).all()),converged=bool(di.converged.all()),current_missing=bool(p[p.cycle.eq(2026)][['actual','wis_pp','brier']].isna().all().all()),unique=not p.duplicated(['scenario','model','target_id']).any(),probabilities=bool(p.p_dem.between(0,1).all()))
    rec=[];account=[];inputs=[];cache={};old=pd.read_parquet(Path(st['source'])/'predictions.parquet')
    for r in f.itertuples():
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id').reset_index(drop=True);key=(r.scenario,r.cycle)
        if key not in cache:
            pf=np.load(Path(st['working'])/f'fits/{r.scenario}_{r.cycle}_poll.npz');cache[key]=normal.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        fit=dict(np.load(out/r.fit_path));fit['a']=float(fit['a']);expected,C,_,_=feat.predict(q,fit['budget'],cache[key],fit,fit['z']);z=np.load(out/r.forecast_path);rec.append(np.allclose(expected.prediction_pp,q.prediction_pp)&np.allclose(C,z['covariance']));seat=s[s.scenario.eq(r.scenario)&s.cycle.eq(r.cycle)&s.model.eq(r.model)].iloc[0];account.append(abs(seat.expected_D_exact-seat.fixed_D-q.p_dem.sum())<1e-8 and z['seat_count_frequency'].sum()==CONFIG['draws']);o=old[old.scenario.eq(r.scenario)&old.cycle.eq(r.cycle)&old.model.eq(r.family)].sort_values('target_id');inputs.append(np.array_equal(q.q_pp,o.q_pp,equal_nan=True)&np.array_equal(q.actual,o.actual,equal_nan=True)&np.allclose(q.firm_mass,o.firm_mass))
    c.update(reconstruction=all(rec),seat_accounting=all(account),polls_labels_preserved=all(inputs));result=dict(passed=bool(all(c.values())),checks={k:bool(x) for k,x in c.items()},forecasts=len(f),rows=len(p),movement_fits=len(di),older_notebooks=len(st['old_notebooks']));v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError(c)
    return result
if __name__=='__main__':build(Path(__file__).resolve().parents[1])
