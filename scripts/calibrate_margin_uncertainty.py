"""Past-only pooled Gaussian uncertainty for saved point forecasts; margins stay fixed."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import shutil

import numpy as np
import pandas as pd
from scipy.stats import norm

SOURCE = 'reports/bayesian_nonbayesian_blend/20260920T055636.585382Z'
MODELS = {'Bayesian': 'bayesian_pp', 'Non-Bayesian': 'nonbayesian_pp', '50/50 blend': 'blend_pp'}
MIN_CYCLES = 3


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fit_scale(data, scenario, cycle, margin_column):
    """Equal cycle weight, mean fixed to zero; second moment retains bias in error budget."""
    h = data[data.scenario.eq(scenario) & data.cycle.lt(cycle) & data.actual_pp.notna()].copy()
    if h.duplicated(['cycle', 'target_id']).any():
        raise ValueError('Duplicate calibration contests')
    if not np.isfinite(h[[margin_column, 'actual_pp']]).all().all():
        raise ValueError('Invalid historical prediction or outcome')
    years = sorted(map(int, h.cycle.unique()))
    info = dict(scenario=scenario, cycle=int(cycle), margin_column=margin_column,
                calibration_cycles=','.join(map(str, years)), n_cycles=len(years), n_contests=len(h),
                training_max_cycle=max(years) if years else None, sigma_pp=np.nan,
                residual_mean_pp=np.nan, status='insufficient_prior_cycles')
    if len(years) < MIN_CYCLES:
        return info
    residual = h.actual_pp-h[margin_column]
    sigma = np.sqrt((residual**2).groupby(h.cycle).mean().mean())
    if not np.isfinite(sigma) or sigma <= 0:
        raise ValueError('Positive historical error scale required')
    info.update(sigma_pp=float(sigma), residual_mean_pp=float(residual.groupby(h.cycle).mean().mean()), status='calibrated')
    return info


def calibrate(data):
    rows, fits = [], []
    for (scenario, year), q in data.groupby(['scenario', 'cycle']):
        for name, col in MODELS.items():
            pred = q[['scenario','cycle','target_id','geography','special','as_of','q_pp',
                      'actual_pp','history_selection_10pp']].copy()
            pred['model'] = name
            pred['margin_pp'] = q[col]
            if name == 'Bayesian':
                pred['sigma_pp'] = q.posterior_sd_pp
                pred['status'] = 'original_bayesian'
            else:
                fit = fit_scale(data, scenario, year, col)
                fits.append(dict(model=name, **fit))
                pred['sigma_pp'] = fit['sigma_pp']
                pred['status'] = fit['status']
            pred['p_dem'] = norm.cdf(pred.margin_pp/pred.sigma_pp)
            pred['lo70_pp'] = pred.margin_pp-norm.ppf(.85)*pred.sigma_pp
            pred['hi70_pp'] = pred.margin_pp+norm.ppf(.85)*pred.sigma_pp
            pred['absolute_error_pp'] = (pred.margin_pp-pred.actual_pp).abs()
            valid = pred.actual_pp.notna() & pred.p_dem.notna()
            outcome = pred.actual_pp.gt(0)
            pred['correct'] = pred.margin_pp.gt(0).eq(outcome).astype(float).where(pred.actual_pp.notna())
            pred['brier'] = ((pred.p_dem-outcome)**2).where(valid)
            pred['coverage70'] = ((pred.actual_pp>=pred.lo70_pp)&(pred.actual_pp<=pred.hi70_pp)).astype(float).where(valid)
            pred['width70_pp'] = pred.hi70_pp-pred.lo70_pp
            pred['interval_score70_pp'] = (pred.width70_pp + 2/.3 * (
                (pred.lo70_pp-pred.actual_pp).clip(lower=0)+(pred.actual_pp-pred.hi70_pp).clip(lower=0))).where(valid)
            rows.append(pred)
    return pd.concat(rows, ignore_index=True), pd.DataFrame(fits)


def current_tables(predictions):
    q = predictions[predictions.cycle.eq(2026)]
    rows, intervals = [], []
    def probability(p):
        return '<0.1%' if p < .001 else '>99.9%' if p > .999 else f'{100*p:.1f}%'
    for tid, g in q.groupby('target_id', sort=True):
        first = g.iloc[0]
        label = first.geography + (' (special)' if first.special else '')
        row = {'State':label, 'Poll margin': '—' if pd.isna(first.q_pp) else f'{first.q_pp:+.2f}'}
        interval = {'State':label}
        for name in MODELS:
            r = g[g.model.eq(name)].iloc[0]
            row[name+' margin'] = f'{r.margin_pp:+.2f}'
            row[name+' P(D)'] = probability(r.p_dem)
            interval[name+' 70% interval'] = f'[{r.lo70_pp:+.1f}, {r.hi70_pp:+.1f}]'
        rows.append(row)
        intervals.append(interval)
    return pd.DataFrame(rows), pd.DataFrame(intervals)


def build(lab):
    lab = Path(lab).resolve()
    source = lab/SOURCE
    manifest = json.loads((source/'manifest.json').read_text())
    assert all(sha(source/k)==v for k,v in manifest.items())
    source_settings = json.loads((source/'settings.json').read_text())
    for name, info in source_settings['sources'].items():
        assert sha(lab/info['path']) == info['sha256'], name
    notebooks = {p.name:sha(p) for p in lab.glob('*.ipynb')}
    work_sha = sha(lab/'WORKING_MODEL.json')
    data = pd.read_parquet(source/'paired_predictions.parquet')
    predictions, fits = calibrate(data)
    # All three models must be evaluable on every row used for comparative probability metrics.
    valid = predictions[predictions.p_dem.notna() & predictions.actual_pp.notna()]
    keys = ['scenario','cycle','target_id']
    complete = valid.groupby(keys).model.nunique().eq(3)
    matched = valid.merge(complete[complete].reset_index()[keys], on=keys, validate='many_to_one')
    metrics = ['absolute_error_pp','brier','coverage70','width70_pp','interval_score70_pp']
    cycle_scores = matched.groupby(['scenario','cycle','model'])[metrics].mean().reset_index()
    counts = matched.groupby(['scenario','cycle','model']).agg(n=('target_id','size'),correct=('correct','sum')).reset_index()
    cycle_scores = cycle_scores.merge(counts, validate='one_to_one')
    summary = cycle_scores.groupby(['scenario','model'])[metrics].mean().reset_index()
    sizes = cycle_scores.groupby(['scenario','model']).agg(cycles=('cycle','size'),n=('n','sum'),correct=('correct','sum')).reset_index()
    summary = summary.merge(sizes, validate='one_to_one')
    subsets = []
    for (scenario, model), q in matched.groupby(['scenario','model']):
        for group, g in {'polled':q[q.q_pp.notna()], 'no_polls':q[q.q_pp.isna()],
                         'competitive':q[q.history_selection_10pp.eq('competitive')]}.items():
            if len(g):
                subsets.append(dict(scenario=scenario,model=model,group=group,n=len(g),
                                    **g.groupby('cycle')[metrics].mean().mean().to_dict()))
    matched = matched.copy()
    matched['probability_bin'] = pd.cut(matched.p_dem, [0,.2,.4,.6,.8,1], include_lowest=True).astype(str)
    matched['actual_D'] = matched.actual_pp.gt(0).astype(float)
    reliability = matched.groupby(['scenario','model','probability_bin']).agg(
        n=('target_id','size'),mean_predicted_probability=('p_dem','mean'),D_win_fraction=('actual_D','mean')).reset_index()
    current, intervals = current_tables(predictions)
    assert len(current)==35 and 'correlation' not in ' '.join(current.columns).lower()
    assert not predictions.duplicated(keys+['model']).any()
    assert predictions[predictions.cycle.eq(2026)][['actual_pp','brier','coverage70']].isna().all().all()
    assert fits[fits.status.eq('calibrated')].training_max_cycle.lt(fits[fits.status.eq('calibrated')].cycle).all()
    assert np.isfinite(predictions.loc[predictions.cycle.eq(2026),['margin_pp','p_dem','lo70_pp','hi70_pp']]).all().all()
    for name, col in MODELS.items():
        q = predictions[predictions.model.eq(name)].merge(data[keys+[col,'bayesian_p_dem']],on=keys,validate='one_to_one')
        assert np.allclose(q.margin_pp,q[col]), 'Point margin changed'
        if name=='Bayesian':
            assert np.allclose(q.p_dem,q.bayesian_p_dem), 'Bayesian probability changed'
    assert np.allclose(data.blend_pp, .5*(data.bayesian_pp+data.nonbayesian_pp))
    assert predictions.loc[predictions.p_dem.notna(),'p_dem'].between(0,1).all()
    assert all(sha(lab/p)==h for p,h in notebooks.items()) and sha(lab/'WORKING_MODEL.json')==work_sha
    out = lab/'reports/margin_probability_calibration'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    out.mkdir(parents=True)
    for name, table in dict(predictions=predictions,calibration_fits=fits,cycle_scores=cycle_scores,
                            summary=summary,subgroup_scores=pd.DataFrame(subsets),reliability=reliability,
                            current_table=current,current_intervals=intervals).items():
        table.to_parquet(out/f'{name}.parquet',index=False)
    settings = dict(source=SOURCE,source_manifest_sha256=sha(source/'manifest.json'),data_as_of='2026-09-17',
                    minimum_prior_cycles=MIN_CYCLES,calibration='zero-centered Gaussian; sigma=sqrt(mean_cycle(mean_contest((actual-prediction)^2)))',
                    residual_location_fixed=0,cycle_weighting='equal, all earlier available cycles',separate_horizons=True,
                    state_pooling='one shared scale per model and horizon',point_predictions_unchanged=True,
                    parameters_per_fit=1,blend_errors='computed directly from paired blended forecasts',
                    calibration_first_test_cycle=2018,current_calibration_cycles=list(range(2012,2026,2)),
                    uncertainty='plug-in marginal prediction intervals; no joint seat distribution or parameter uncertainty',
                    no_refresh=True,no_promotion=True,old_notebooks=notebooks,working_sha256=work_sha)
    (out/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
    audit = dict(passed=True,rows=len(predictions),matched_historical_rows=len(matched),current_rows=105,
                 checks=['Source manifest and upstream files verified','Exact contest keys','Point margins unchanged',
                         'Bayesian probabilities unchanged','Past-only calibration with three-cycle minimum',
                         'Same evaluable folds for all models','Current outcomes remain missing',
                         'Finite current probabilities and intervals','All prior notebooks and designation preserved'])
    (out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    shutil.copy2(__file__,out/Path(__file__).name)
    report = '''# Marginal probability and interval calibration

The non-Bayesian and 50/50 blend margins stay exactly as saved. Their uncertainty is now a **zero-centered Gaussian error model**. One pooled scale per model and forecast horizon is the square root of the average earlier-cycle mean squared out-of-sample error. Cycles receive equal weight, then contests within each cycle share that cycle's weight. All earlier available cycles are included. This uses RMS error, not residual standard deviation after subtracting bias: persistent bias remains in the error budget, and the measured residual mean is reported diagnostically. We do not add a new mean correction.

The blend is calibrated from its own paired errors, preserving the two components' empirical error dependence; variances or win probabilities are not independently averaged. Bayesian means, probabilities and intervals are retained from the existing Gaussian posterior.

For mean m and fitted scale s: P(D)=Phi(m/s), and the central 70% prediction interval is m +/- 1.03643*s. These are approximate marginal prediction intervals, not confidence intervals for the mean and not distribution-free coverage guarantees. The scale estimate's own uncertainty and cross-state dependence are not modeled here. There is no newly calibrated Senate-seat distribution.

Historical calibration uses only earlier cycles at the same horizon and requires at least three. Consequently 2012–2016 have no calibrated non-Bayesian/blend probabilities; 2018–2024 provide the matched comparison, with 111 contests over four cycles per horizon. For 2026, the seven 2012–2024 cycles contribute 198 contests. State errors within a cycle are not independent national-election replications. This remains exploratory after prior architecture reviews.

## Matched historical metrics, 2018–2024

Brier and interval score are lower-is-better. Coverage is a fraction, ideally near .70; excessive coverage with wide intervals is not automatically better. Metrics average cycles equally, while counts pool contests.

'''+summary.round(4).to_markdown(index=False)
    report += '\n\n## Current calibration scales and observed residual means\n\n'+fits[fits.cycle.eq(2026)].round(4).to_markdown(index=False)
    report += '\n\n## Current probabilities and margins\n\n'+current.to_markdown(index=False)
    report += '\n\n## Current 70% prediction intervals (D−R points)\n\n'+intervals.to_markdown(index=False)
    report += '\n\nFrozen September 17 inputs. No usable poll remains missing in the poll column; model-specific prior fallbacks remain. Nebraska retains the independent-candidate proxy caveat. Correlation columns are removed from the new current table. Source point seat counts remain unchanged; summing marginal probabilities does not supply seat intervals. Individual cycle, polling-coverage/competitive subset and reliability tables are saved alongside this report. No model promotion.\n'
    (out/'RESULTS.md').write_text(report)
    finalize(out)
    print('OUTPUT',out)
    print(summary.round(4).to_string(index=False))
    print(fits[fits.cycle.eq(2026)].round(4).to_string(index=False))
    return out


def finalize(out):
    files = {str(p.relative_to(out)):sha(p) for p in out.rglob('*') if p.is_file() and p.name!='manifest.json'}
    (out/'manifest.json').write_text(json.dumps(files,indent=2)+'\n')
    (out.parent/'latest.json').write_text(json.dumps(dict(artifact=out.name,manifest_sha256=sha(out/'manifest.json')),indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1])
    build(parser.parse_args().lab)
