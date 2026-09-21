"""Supplemental reconstruction, sparse-state diagnostics and saved review tables."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import simple_bayesian_polling as v1
import bayesian_revision2 as v2
import prior_center_repair as repair

def build(out,lab):
    out,lab=Path(out),Path(lab);st=json.loads((out/'settings.json').read_text());src=Path(st['source']);up=Path(st['upstream']);p=pd.read_parquet(out/'predictions.parquet');fold=pd.read_parquet(out/'folds.parquet');surface=pd.read_parquet(out/'scale_surface.parquet');pen=pd.read_parquet(out/'penalties.parquet');tuning=pd.read_parquet(out/'tuning.parquet');h=pd.read_parquet(out/'histories.parquet');di=pd.read_parquet(out/'fit_diagnostics.parquet');mom=pd.read_parquet(out/'residual_moments.parquet')
    hs,ledger=repair.histories(pd.read_parquet(up/'prepared_histories.parquet'));stored=pd.read_parquet(out/'center_ledger.parquet');checks=dict(ledger_reproduces=bool(stored.equals(ledger)));rh=pd.concat(hs.values(),ignore_index=True);checks['prior_history_reproduces']=bool(h.equals(rh));same=h[h.prior_recipe.eq('same_seat')&h.same_seat_fallback.eq(False)];checks['same_seat_past_regular']=bool(same.same_seat_source_cycle.lt(same.cycle).all()&((same.cycle-same.same_seat_source_cycle)%6).eq(0).all()&~same.special.astype(bool).any())
    train=[]
    for r in di.itertuples():
        a=h[h.prior_recipe.eq(r.recipe)&h.scenario.eq('matched_live')];x,n,w,years,_=v2.blocks(a,r.cycle,'movement');f=np.load(out/f'fits/movement_{r.recipe}_{r.cycle}.npz');train.append(np.array_equal(x,f['training_values'],equal_nan=True)&np.array_equal(n,f['training_noise'],equal_nan=True)&np.allclose(w,f['training_weights'])&np.array_equal(years,f['years']))
    checks['training_blocks_reproduced']=bool(all(train));penok=[];budgetok=[]
    for (sc,year,recipe,family),g in pen.groupby(['scenario','forecast_cycle','recipe','family']):
        surf=surface[surface.scenario.eq(sc)&surface.recipe.eq(recipe)&surface.family.eq(family)];shared,mult,pp=repair.choose_scales(surf,year);pp=pp.set_index('state');gg=g.set_index('state').loc[pp.index];penok.append(np.allclose(gg.multiplier,pp.multiplier)&np.allclose(gg.shared,pp.shared)&gg.validation_years.fillna('').eq(pp.validation_years.fillna('')).all());raw=np.load(out/f'fits/movement_{recipe}_{year}.npz');V=np.diag(raw['covariance'])
        for mode,a in [('fixed',np.ones(50)),('shared',np.full(50,shared)),('state',mult)]:
            fit=np.load(out/f'fits/{sc}_{year}_{family}_{recipe}_{mode}.npz');budgetok.append(np.allclose(fit['budget'],V*a)&np.allclose(fit['multipliers'],a))
    checks['penalty_selection_reproduces']=bool(all(penok));checks['variance_budgets_reproduce']=bool(all(budgetok));sel=[]
    for r in tuning.itertuples():
        years=sorted(p.loc[p.scenario.eq(r.scenario)&p.cycle.lt(r.cycle)&p.actual.notna(),'cycle'].unique())[-3:];order=[r.family+'__baseline__fixed']+[r.family+'__'+recipe+'__'+m for recipe in repair.RECIPES for m in ['fixed','shared','state']];past=p[p.scenario.eq(r.scenario)&p.cycle.isin(years)&p.family.eq(r.family)&p.model.isin(order)];scores=past.groupby(['model','cycle']).wis_pp.mean().groupby('model').mean();chosen=min(order,key=lambda n:(scores[n],order.index(n))) if len(years)==3 else order[0];sel.append(chosen==r.chosen and ','.join(map(str,years))==r.validation_years)
    checks['chronological_recipe_selector_reproduces']=bool(all(sel));trend=lab/'reports/poll_trend_review/20260920T041249.965124Z';ag=pd.read_parquet(trend/'aggregates.parquet');ag=ag[ag.variant.eq('baseline')][['scenario','target_id','sample_count','recent_firms']].rename(columns={'sample_count':'admitted_samples'});a=p.merge(ag,on=['scenario','target_id'],validate='many_to_one');assert a.admitted_samples.notna().all();a['coverage_group']=np.where(a.admitted_samples.eq(0),'no_polls',np.where(a.recent_firms.le(2),'low_recent_0_2_firms','recent_3plus_firms'));groups=[]
    for first in [2012,2016]:
        for (sc,model,group),g in a[a.cycle.between(first,2024)].groupby(['scenario','model','coverage_group']):
            metrics=g.groupby('cycle')[['absolute_error_pp','wis_pp','brier']].mean().mean().to_dict();groups.append(dict(first_cycle=first,scenario=sc,model=model,coverage_group=group,n=len(g),correct=int(g.correct.sum()),coverage70=g.coverage70.mean(),coverage95=g.coverage95.mean(),mean_sd_pp=g.posterior_sd_pp.mean(),**metrics))
    pd.DataFrame(groups).to_parquet(out/'coverage_scores.parquet',index=False)
    current=a[a.cycle.eq(2026)].copy();current=current.merge(mom[mom.cycle.eq(2026)].drop(columns='cycle').rename(columns={'state':'geography'}),on=['scenario','recipe','geography'],how='left',validate='many_to_one');current.to_parquet(out/'current_diagnostics.parquet',index=False)
    errors=h[h.actual.notna()].copy();errors['error_pp']=100*(errors.actual-errors.prior);errors[['target_id','cycle','scenario','geography','prior_recipe','actual','base_prior','prior','prior_center_shift_pp','error_pp','same_seat_source_cycle']].to_parquet(out/'prior_errors.parquet',index=False)
    ic=pd.read_parquet(out/'influence_checks.parquet');checks['conditional_influence_checks']=bool(ic.passed.all());checks['no_history_LA_center_preserved']=bool(current[current.geography.eq('LA')].prior.nunique()==1);checks['all_targets_coverage_matched']=bool(len(a)==len(p));result=dict(passed=bool(all(checks.values())),checks={k:bool(x) for k,x in checks.items()},conditional_checks=len(ic),training_reconstructions=len(train),penalty_reconstructions=len(penok),budget_reconstructions=len(budgetok));v1.json_write(out/'review_audit.json',result)
    if not result['passed']:raise AssertionError(result)
    v1.json_write(out/'review_sources.json',{str(trend):v1.verify(trend)});v1.manifest(out);v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.verify(out)));print(result);return result
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('artifact',type=Path);a=p.parse_args();build(a.artifact,Path(__file__).resolve().parents[1])
