"""Translate Bayesian forecasts to a 50/50 polling mean; preserve joint uncertainty."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import shutil

import numpy as np
import pandas as pd
from scipy.stats import norm

from calibrate_margin_uncertainty import sha, finalize
from plain_polling_blend import verify, BAYES_SOURCE

SOURCE = 'reports/plain_polling_blend/20260920T062747.520500Z'
NEW = 'Mean-only blend'
OLD = 'Blend with pooled uncertainty'
SEED = 197139
DRAWS = 30000
KEY = ['scenario', 'cycle', 'target_id']


def translate_draws(draws, original_mean, new_mean):
    """Constant translation of each state, with no rescaling or new random noise."""
    draws = np.asarray(draws, dtype=float)
    original_mean, new_mean = np.asarray(original_mean), np.asarray(new_mean)
    if draws.ndim != 2 or original_mean.shape != (draws.shape[1],) or new_mean.shape != original_mean.shape:
        raise ValueError('One aligned mean per draw column is required')
    if not all(np.isfinite(x).all() for x in [draws, original_mean, new_mean]):
        raise ValueError('Finite means and draws required')
    return draws + (new_mean-original_mean)


def rescore(pred):
    """Recompute every Gaussian interval/score after changing means or scales.

Do not inherit 50/80/95% intervals or WIS from the source model. Student
predictions use their sampled quantiles and do not call this Gaussian helper.
"""
    from coverage_balance import score_rows
    pred = pred.copy()
    pred['prediction_pp'] = pred.margin_pp
    pred['prediction'] = pred.margin_pp / 100
    pred['actual'] = pred.actual_pp / 100
    pred['median_pp'] = pred.margin_pp
    pred['posterior_sd_pp'] = pred.sigma_pp
    pred['p_dem'] = norm.cdf(pred.margin_pp / pred.sigma_pp)
    for level in [50, 70, 80, 95]:
        half_width = norm.ppf((1 + level/100)/2) * pred.sigma_pp
        pred[f'lo{level}_pp'] = pred.margin_pp - half_width
        pred[f'hi{level}_pp'] = pred.margin_pp + half_width
    pred = score_rows(pred)
    for level in [50, 70, 80, 95]:
        unavailable = pred[f'lo{level}_pp'].isna() | pred[f'hi{level}_pp'].isna()
        pred.loc[unavailable, f'coverage{level}'] = np.nan
    return pred


def build(lab):
    lab = Path(lab).resolve()
    source, bayes = lab/SOURCE, lab/BAYES_SOURCE
    verify(source)
    old_notebooks = {p.name:sha(p) for p in lab.glob('*.ipynb')}
    designation = sha(lab/'WORKING_MODEL.json')
    sources = [source/'manifest.json', bayes/'folds.parquet', bayes/'seats.parquet', bayes/'tuning.parquet']
    hashes = {str(p.relative_to(lab)):sha(p) for p in sources}
    paired = pd.read_parquet(source/'paired_inputs.parquet')
    previous = pd.read_parquet(source/'predictions.parquet')
    base = previous[previous.model.eq('Bayesian')].copy()
    new = base.merge(paired[KEY+['plain_pp']], on=KEY, validate='one_to_one')
    new['margin_pp'] = .5*(new.margin_pp+new.plain_pp)
    new['model'] = NEW
    new['status'] = 'translated_bayesian_joint_distribution'
    new = rescore(new)
    wide = previous[previous.model.eq('Bayes + plain (50/50)')].copy()
    wide['model'] = OLD
    compare = new.merge(wide, on=KEY, validate='one_to_one', suffixes=('','_old'))
    assert np.allclose(compare.margin_pp, compare.margin_pp_old)
    assert np.allclose(new.sigma_pp, base.sigma_pp)
    assert np.allclose(new.width70_pp, base.width70_pp)
    assert np.allclose(base.p_dem, norm.cdf(base.margin_pp/base.sigma_pp))
    predictions = pd.concat([base, wide, new], ignore_index=True)
    predictions['model'] = predictions.model.astype(str)
    folds = pd.read_parquet(bayes/'folds.parquet').query('model == "repaired_both__selected"')
    reference = pd.read_parquet(bayes/'seats.parquet').query('model == "repaired_both__selected"')
    tuning = pd.read_parquet(bayes/'tuning.parquet').query('base_model == "repaired_both"')
    for r in tuning.itertuples():
        assert all(int(y)<r.cycle for y in str(r.validation_years).split(',') if y and y!='nan')
    out = lab/'reports/mean_only_polling_blend'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    (out/'forecasts').mkdir(parents=True)
    seats, frequencies, checks = [], [], []
    for fold in folds.itertuples():
        path = bayes/fold.forecast_path
        hashes[str(path.relative_to(lab))] = sha(path)
        a = dict(np.load(path))
        ids = a['target_ids'].astype(str)
        q = base[base.scenario.eq(fold.scenario)&base.cycle.eq(fold.cycle)].set_index('target_id').loc[ids]
        n = new[new.scenario.eq(fold.scenario)&new.cycle.eq(fold.cycle)].set_index('target_id').loc[ids]
        mu, cov = a['mean'], a['covariance']
        assert len(q)==len(ids) and q.index.is_unique and n.index.equals(q.index)
        assert np.allclose(q.margin_pp,mu) and np.allclose(q.sigma_pp,np.sqrt(np.diag(cov)))
        seed = SEED+fold.cycle+10000*(fold.scenario=='oct31')
        draws = mu+np.random.default_rng(seed).standard_normal((DRAWS,len(ids)))@np.linalg.cholesky(cov).T
        shifted = translate_draws(draws,mu,n.margin_pp.to_numpy())
        assert np.allclose(shifted-n.margin_pp.to_numpy(),draws-mu,atol=1e-12)
        assert np.allclose(np.cov(shifted,rowvar=False),np.cov(draws,rowvar=False),atol=1e-10)
        ref = reference[reference.scenario.eq(fold.scenario)&reference.cycle.eq(fold.cycle)].iloc[0]
        fixed = int(ref.fixed_D)
        for name, frame, samples in [('Bayesian',q,draws),(NEW,n,shifted)]:
            counts = fixed+(samples>0).sum(axis=1)
            freq = np.bincount(counts,minlength=101)
            point = fixed+int(frame.margin_pp.gt(0).sum())
            if name=='Bayesian':
                assert np.array_equal(freq,a['seat_count_frequency']), 'Original simulation must reproduce exactly'
                assert point==ref.point_D
                assert np.isclose((counts>=51).mean(),ref.p_D_at_least_51)
            lo,hi = np.quantile(counts,[.15,.85],method='inverted_cdf')
            expected = fixed+frame.p_dem.sum()
            seats.append(dict(scenario=fold.scenario,cycle=int(fold.cycle),model=name,method='same_bayesian_joint_covariance',
                point_D=point,point_R=100-point,expected_D=expected,expected_R=100-expected,
                p_D_control=float((counts>=51).mean()),p_R_control=float((counts<=50).mean()),
                D_lo70=int(lo),D_hi70=int(hi),actual_D=ref.actual_D,fixed_D=fixed,
                unmodeled_contested=int(ref.unmodeled_contested),draws=DRAWS))
            frequencies.extend(dict(scenario=fold.scenario,cycle=int(fold.cycle),model=name,D_seats=i,probability=float(v/DRAWS))
                               for i,v in enumerate(freq) if v)
        new_joint_mean = a['joint_mean'].copy()
        new_joint_mean[:len(ids)] = n.margin_pp.to_numpy()
        np.savez_compressed(out/'forecasts'/f'{fold.scenario}_{fold.cycle}.npz',
            target_ids=ids,mean=n.margin_pp.to_numpy(),covariance=cov,
            joint_mean=new_joint_mean,joint_covariance=a['joint_covariance'],
            mean_shift=n.margin_pp.to_numpy()-mu,bayesian_mean=mu,seed=seed,draws=DRAWS,
            seat_count_frequency=np.bincount(fixed+(shifted>0).sum(axis=1),minlength=101))
        checks.append(dict(scenario=fold.scenario,cycle=int(fold.cycle),source=fold.forecast_path,
                           original_seat_simulation_reproduced=True,unchanged_covariance=True))
    seats = pd.DataFrame(seats)
    old_seats = pd.read_parquet(source/'seats.parquet').query('model == "Bayes + plain (50/50)"').copy()
    old_seats['model'] = OLD
    seats = pd.concat([seats,old_seats],ignore_index=True)
    history = predictions[predictions.actual_pp.notna()]
    metrics = ['absolute_error_pp','brier','coverage70','width70_pp','interval_score70_pp']
    cycles = history.groupby(['scenario','cycle','model'])[metrics].mean().reset_index()
    cycles = cycles.merge(history.groupby(['scenario','cycle','model']).agg(n=('target_id','size'),correct=('correct','sum')).reset_index())
    summary = []
    for start in [2012,2016,2018]:
        for (sc,name),g in cycles[cycles.cycle.ge(start)].groupby(['scenario','model']):
            if name==OLD and start<2018:
                continue  # Do not silently average partially missing probability metrics.
            summary.append(dict(first_cycle=start,scenario=sc,model=name,cycles=len(g),n=int(g.n.sum()),
                correct=int(g.correct.sum()),**g[metrics].mean().to_dict()))
    summary = pd.DataFrame(summary)
    groups = []
    for (sc,name),g in history[history.cycle.ge(2016)].groupby(['scenario','model']):
        for label,v in {'competitive':g[g.history_selection_10pp.eq('competitive')],
                        'polled':g[g.q_pp.notna()],'no_polls':g[g.q_pp.isna()]}.items():
            if len(v):groups.append(dict(scenario=sc,model=name,group=label,n=len(v),correct=int(v.correct.sum()),
                                         **v.groupby('cycle')[metrics].mean().mean().to_dict()))
    # Pooled-uncertainty probabilities begin in 2018; compare all three only on that range.
    current = predictions[predictions.cycle.eq(2026)]
    display,intervals = [],[]
    for tid,g in current.groupby('target_id'):
        r=g.iloc[0];row={'State':r.geography+(' (special)' if r.special else ''),'Poll margin':r.q_pp}
        interval={'State':row['State']}
        for name in ['Bayesian',NEW,OLD]:
            v=g[g.model.eq(name)].iloc[0]
            row[name+' margin']=v.margin_pp;row[name+' P(D) %']=100*v.p_dem
            interval[name]=f'[{v.lo70_pp:+.2f}, {v.hi70_pp:+.2f}]'
        display.append(row);intervals.append(interval)
    current_table = pd.DataFrame(display)
    assert len(current_table)==35
    assert current.actual_pp.isna().all()
    assert all(sha(lab/k)==h for k,h in hashes.items())
    assert all(sha(lab/k)==h for k,h in old_notebooks.items())
    assert sha(lab/'WORKING_MODEL.json')==designation
    tables=dict(predictions=predictions,cycle_scores=cycles,summary=summary,subgroups=pd.DataFrame(groups),
        seats=seats,seat_distributions=pd.DataFrame(frequencies),current_table=current_table,current_intervals=pd.DataFrame(intervals))
    for name,table in tables.items():table.to_parquet(out/(name+'.parquet'),index=False)
    settings=dict(source=SOURCE,bayesian_source=BAYES_SOURCE,bayesian_model='repaired_both__selected',
        data_as_of='2026-09-17',polling_weight=.5,new_fitted_parameters=0,seed=SEED,draws=DRAWS,
        rule='Y_new = Y_Bayes + 0.5*(plain_margin - Bayesian_mean); joint covariance unchanged',
        no_poll_rule='Retain saved plain-model prior fallback, as in previous blend',
        old_comparison='Pooled-uncertainty blend retains independent-state seat approximation',
        limitations='Hybrid translated forecast, not a newly derived posterior. Earlier architecture selection remains exploratory. '
                    'Historical unmodeled contests use existing fixed-seat completion; independent-candidate proxy caveats remain. '
                    'Repeated model experimentation is not untouched out-of-sample validation.',
        no_refresh=True,no_refit=True,no_promotion=True,sources=hashes,old_notebooks=old_notebooks,working_sha256=designation)
    (out/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
    (out/'audit.json').write_text(json.dumps(dict(passed=True,folds=checks,current_contests=35,
        unchanged_old_notebooks=len(old_notebooks),checks=['Source manifest verified','Exact keys and posterior matching',
        'All original joint seat simulations reproduced','Centered draws and covariance unchanged',
        'Same means as previous plain blend','70% interval widths unchanged','Earlier-only source tuning',
        'Current outcomes remain missing','Inputs/notebooks/designation preserved']),indent=2)+'\n')
    report='''# Mean-only polling blend with Bayesian uncertainty

This experiment uses the same fixed 50/50 Bayesian/plain-polling means as the previous blend, but keeps each fold's full Bayesian covariance. It translates the Bayesian joint simulations by the state-specific mean change, without rescaling or adding noise. State probabilities use the exact Gaussian marginal; chamber odds use 30,000 paired joint simulations. The original Bayesian simulation reproduces exactly in every fold.

No polling-based uncertainty estimate, new fitting, weight selection, data refresh or promotion. Frozen September 17 inputs. Current plain polling equals the raw aggregate where polled; its existing historical-prior fallback is retained for no-poll races. This is a hybrid forecast, not a new posterior derived from a likelihood. Preserving covariance does not guarantee calibration at the new mean. Earlier architecture exploration makes the historical review exploratory.

Positive margins are Democratic minus Republican percentage points; P(D) is win probability. D requires 51 seats, R wins a 50–50 tie under the existing ledger convention. Totals include continuing seats. Historical unmodeled contests retain fixed completion assumptions and are excluded from state accuracy; independent-candidate proxy conventions are unchanged.

## Current total seats

The two main rows use the same Bayesian joint covariance. The old pooled blend is shown only as a labeled reference: its joint method assumes independent states.

'''+seats[seats.cycle.eq(2026)].round(4).to_markdown(index=False)
    report+='\n\n## Recent historical evaluation, 2016–2024\n\nSame two models, 140 contests per horizon. MAE/Brier/interval score: lower is better. Coverage ideally equals70%; widths are in percentage points. Error metrics average cycles equally; correct calls and counts pool contests.\n\n'+summary.query('first_cycle == 2016 and model != @OLD').round(4).to_markdown(index=False)
    report+='\n\n## Matched comparison including old uncertainty, 2018–2024\n\n111 contests per horizon. All three models have probabilities for these cycles.\n\n'+summary.query('first_cycle == 2018').round(4).to_markdown(index=False)
    report+='\n\n## Every historical cycle\n\n'+cycles.round(4).to_markdown(index=False)
    report+='\n\n## All current races\n\n'+current_table.round(2).to_markdown(index=False)
    report+='\n\n## Current 70% margin intervals\n\n'+tables['current_intervals'].to_markdown(index=False)
    (out/'RESULTS.md').write_text(report)
    shutil.copy2(__file__,out/Path(__file__).name)
    finalize(out)
    print('OUTPUT',out)
    print(seats[seats.cycle.eq(2026)].round(4).to_string(index=False))
    print(summary.query('first_cycle == 2016 and model != @OLD').round(4).to_string(index=False))
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1])
    build(parser.parse_args().lab)
