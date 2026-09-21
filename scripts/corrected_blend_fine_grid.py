"""Fixed 5/10/20/30/40/50% corrected polling means with Bayesian covariance."""
from pathlib import Path
from datetime import datetime, timezone
import json
import shutil
import numpy as np
import pandas as pd
from scipy.stats import norm
from mean_only_blend_weights import blend_mean, METRICS
from mean_only_polling_blend import rescore, translate_draws
from plain_polling_blend import verify
from calibrate_margin_uncertainty import sha, finalize

SOURCE = 'reports/mean_only_blend_weights/20260920T171747.972660Z'
WEIGHTS = [0., .05, .10, .20, .30, .40, .50]
KEY = ['scenario', 'cycle', 'target_id']


def build(lab):
    lab = Path(lab).resolve(); source = lab/SOURCE
    verify(source)
    notebooks = {p.name:sha(p) for p in lab.glob('*.ipynb')}
    working = sha(lab/'WORKING_MODEL.json')
    source_hash = sha(source/'manifest.json')
    old = pd.read_parquet(source/'predictions.parquet')
    base = old[old.model.eq('Bayesian')].copy()
    ref_seats = pd.read_parquet(source/'seats.parquet')
    frames = []
    for w in WEIGHTS:
        f = base.copy()
        f['model'] = 'Bayesian' if w == 0 else f'Corrected {w*100:g}%'
        f['weight_pct'] = 100*w
        f['nonbayesian_weight'] = w
        f['component'] = 'bayesian_pp' if w == 0 else 'nonbayesian_pp'
        f['margin_pp'] = blend_mean(f.bayesian_pp,f.nonbayesian_pp,w)
        f = rescore(f)
        f['lo95_pp'] = f.margin_pp-norm.ppf(.975)*f.sigma_pp
        f['hi95_pp'] = f.margin_pp+norm.ppf(.975)*f.sigma_pp
        f['coverage95'] = ((f.actual_pp>=f.lo95_pp)&(f.actual_pp<=f.hi95_pp)).astype(float).where(f.actual_pp.notna())
        frames.append(f)
    pred = pd.concat(frames,ignore_index=True)
    for name in ['Bayesian','Corrected 20%','Corrected 50%']:
        chk = pred[pred.model.eq(name)].merge(old[old.model.eq(name)],on=KEY,validate='one_to_one',suffixes=('','_old'))
        for col in ['margin_pp','p_dem','sigma_pp','width70_pp']:
            assert np.allclose(chk[col],chk[col+'_old'])
    out = lab/'reports/corrected_blend_fine_grid'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    (out/'forecasts').mkdir(parents=True)
    seats, frequencies, checks = [], [], []
    for (sc,cycle),b in base.groupby(['scenario','cycle']):
        a = np.load(source/'forecasts'/f'{sc}_{cycle}_Bayesian.npz')
        mu,cov,ids = a['mean'],a['covariance'],a['target_ids'].astype(str)
        n_draws,seed = int(a['draws']),int(a['seed'])
        draws = mu+np.random.default_rng(seed).standard_normal((n_draws,len(ids)))@np.linalg.cholesky(cov).T
        ref = ref_seats[ref_seats.scenario.eq(sc)&ref_seats.cycle.eq(cycle)&ref_seats.model.eq('Bayesian')].iloc[0]
        for w in WEIGHTS:
            f = pred[pred.scenario.eq(sc)&pred.cycle.eq(cycle)&pred.weight_pct.eq(w*100)].set_index('target_id').loc[ids]
            new = f.margin_pp.to_numpy(); name=f.model.iloc[0]
            assert np.allclose(f.bayesian_pp,mu) and np.allclose(f.sigma_pp,np.sqrt(np.diag(cov)))
            samples = translate_draws(draws,mu,new)
            assert np.allclose(samples-new,draws-mu,atol=1e-12)
            assert np.allclose(np.cov(samples,rowvar=False),np.cov(draws,rowvar=False),atol=1e-10)
            counts = int(ref.fixed_D)+(samples>0).sum(axis=1)
            freq = np.bincount(counts,minlength=101)
            if w in [0.,.2,.5]:
                saved = np.load(source/'forecasts'/f'{sc}_{cycle}_{name.replace(" ","_").replace("%","")}.npz')
                assert np.array_equal(freq,saved['seat_count_frequency'])
            point = int(ref.fixed_D)+int((new>0).sum())
            expected = ref.fixed_D+f.p_dem.sum()
            lo,hi = np.quantile(counts,[.15,.85],method='inverted_cdf')
            actual = ref.actual_D
            seats.append(dict(scenario=sc,cycle=int(cycle),model=name,weight_pct=w*100,
                point_D=point,point_R=100-point,expected_D=expected,expected_R=100-expected,
                p_D_control=float((counts>=51).mean()),D_lo70=int(lo),D_hi70=int(hi),actual_D=actual,
                expected_seat_error=abs(expected-actual),fixed_D=int(ref.fixed_D),unmodeled_contested=int(ref.unmodeled_contested),
                seat_crps=np.nan if pd.isna(actual) else float(np.square(np.cumsum(freq/n_draws)-(np.arange(101)>=actual)).sum())))
            frequencies.extend(dict(scenario=sc,cycle=int(cycle),model=name,weight_pct=w*100,D_seats=i,probability=float(v/n_draws)) for i,v in enumerate(freq) if v)
            np.savez_compressed(out/'forecasts'/f'{sc}_{cycle}_{w*100:g}.npz',mean=new,covariance=cov,
                target_ids=ids,seed=seed,draws=n_draws,seat_count_frequency=freq)
        checks.append(dict(scenario=sc,cycle=int(cycle),all_covariances_unchanged=True,previous_0_20_50_reproduced=True))
    seats=pd.DataFrame(seats)
    history=pred[pred.actual_pp.notna()]
    group=['scenario','cycle','model','weight_pct']
    cycles=history.groupby(group)[METRICS].mean().reset_index().merge(
        history.groupby(group).agg(n=('target_id','size'),correct=('correct','sum')).reset_index())
    summary=[]
    for start in [2012,2016]:
        for (sc,name,w),g in cycles[cycles.cycle.ge(start)].groupby(['scenario','model','weight_pct']):
            chamber=seats[seats.scenario.eq(sc)&seats.model.eq(name)&seats.cycle.between(start,2024)]
            summary.append(dict(first_cycle=start,scenario=sc,model=name,weight_pct=w,cycles=len(g),n=int(g.n.sum()),correct=int(g.correct.sum()),
                **g[METRICS].mean().to_dict(),expected_seat_mae=chamber.expected_seat_error.mean(),seat_crps=chamber.seat_crps.mean()))
    summary=pd.DataFrame(summary).sort_values(['first_cycle','scenario','weight_pct'])
    groups=[]
    for (sc,name,w),g in history[history.cycle.ge(2016)].groupby(['scenario','model','weight_pct']):
        for label,f in {'competitive':g[g.history_selection_10pp.eq('competitive')],
            'not_selected':g[g.history_selection_10pp.eq('not_selected')], 'unknown_history':g[g.history_selection_10pp.eq('unknown_history')],
            'polled':g[g.q_pp.notna()],'no_polls':g[g.q_pp.isna()]}.items():
            if len(f):groups.append(dict(scenario=sc,model=name,weight_pct=w,group=label,n=len(f),correct=int(f.correct.sum()),**f.groupby('cycle')[METRICS].mean().mean().to_dict()))
    current=pred[pred.cycle.eq(2026)].copy()
    assert len(current)==35*7 and current.actual_pp.isna().all() and current.brier.isna().all()
    current['State']=current.geography+np.where(current.special,' (special)','')
    current['p_dem_pct']=current.p_dem*100
    tables=dict(predictions=pred,cycle_scores=cycles,summary=summary,seats=seats,seat_distributions=pd.DataFrame(frequencies),
        subgroups=pd.DataFrame(groups),current=current,
        current_margins=current.pivot(index='State',columns='weight_pct',values='margin_pp').reset_index(),
        current_probabilities=current.pivot(index='State',columns='weight_pct',values='p_dem_pct').reset_index())
    for name,table in tables.items():table.to_parquet(out/(name+'.parquet'),index=False)
    assert sha(source/'manifest.json')==source_hash
    assert sha(lab/'WORKING_MODEL.json')==working
    assert all(sha(lab/k)==v for k,v in notebooks.items())
    settings=dict(source=SOURCE,source_manifest_sha256=source_hash,weights=WEIGHTS,data_as_of='2026-09-17',
        bayesian_model='repaired_both__selected',component='Retained bias-corrected polling benchmark',
        no_refit=True,no_selection=True,no_refresh=True,no_promotion=True,
        old_notebooks=notebooks,working_sha256=working)
    (out/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
    (out/'audit.json').write_text(json.dumps(dict(passed=True,folds=checks,old_notebooks_preserved=len(notebooks)),indent=2)+'\n')
    report='''# Corrected polling: finer mean-only blend weights

Fixed 5%, 10%, 20%, 30%, 40%, 50% non-Bayesian shares; 0% is the same Bayesian reference. State mean = (1-w)*Bayesian + w*corrected-polling mean. Preserve the complete Bayesian margin covariance, SDs and interval widths, using translated paired joint simulations. No new fitting, weight optimization, refresh, or model promotion. September17 frozen data. No interpolation between forecast dates is tested.

Historical component forecasts used earlier-cycle training/tuning. Repeated architecture exploration makes the historical assessment exploratory, not untouched validation. Positive D-R margins favor Democrats. MAE/Brier/CRPS: lower is better; coverage targets are70/95%. Metrics average cycles equally; correct calls pool contests. Recent2016–24 covers140 contests per horizon; full2012–24 covers198. Current outcomes stay missing. No-poll forecasts retain the saved historical fallback. Historical chamber totals retain fixed completion of unmodeled contests; current independent-candidate proxy conventions remain. Chamber probabilities preserve correlated draws; control requires51D under the existing ledger convention. Fixed margin covariance does not imply fixed seat-count uncertainty.

'''
    for title,table in [('Recent history',summary[summary.first_cycle.eq(2016)]),('All historical summary',summary),
        ('Current seats',seats[seats.cycle.eq(2026)]),('Each historical cycle',cycles),('Historical chamber totals',seats[seats.cycle.lt(2026)]),
        ('Subgroups',tables['subgroups']),('Current margins by blend weight (%)',tables['current_margins']),('Current P(D) percent',tables['current_probabilities'])]:
        report+='\n\n## '+title+'\n\n'+table.round(4).to_markdown(index=False)
    (out/'RESULTS.md').write_text(report)
    shutil.copy2(__file__,out/Path(__file__).name)
    finalize(out)
    print('OUTPUT',out)
    print(summary[summary.first_cycle.eq(2016)].round(4).to_string(index=False))
    print(seats[seats.cycle.eq(2026)].round(4).to_string(index=False))
    return out


if __name__=='__main__':build(Path(__file__).resolve().parents[1])
