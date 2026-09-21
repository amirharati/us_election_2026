"""Frozen, paired evaluation of a fixed 50/50 state-margin average. No refitting."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import shutil

import numpy as np
import pandas as pd
from model_labels import label_frame
from scipy.stats import norm

BAYES_SOURCE = 'reports/signed_state_factor/20260920T052241.012596Z'
NONBAYES_SOURCE = 'reports/official_repair_review/20260919T172552.860612Z'
BAYES_MODEL = 'repaired_both__selected'
KEY = ['scenario', 'cycle', 'target_id']
MODELS = {'Bayesian': 'bayesian_pp', 'Non-Bayesian': 'nonbayesian_pp', '50/50 blend': 'blend_pp'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def current_display(current):
    def margin(x):
        return '—' if pd.isna(x) else f'{x:+.2f}'
    def probability(p):
        return '<0.01%' if p < .0001 else '>99.99%' if p > .9999 else f'{100*p:.2f}%'
    rows = []
    for r in current.itertuples():
        rows.append({'State': r.geography + (' (special)' if r.special else ''),
                     'Bayesian P(D)': probability(r.bayesian_p_dem),
                     'Poll margin': margin(r.q_pp), 'Bayesian margin': margin(r.bayesian_pp),
                     'Non-Bayesian margin': margin(r.nonbayesian_pp), '50/50 margin': margin(r.blend_pp),
                     'Positive partner (rho)': f'{r.positive_partner} ({r.positive_rho:+.4f})'})
    return pd.DataFrame(rows)


def build(lab):
    lab = Path(lab).resolve()
    bayes, nonbayes = lab / BAYES_SOURCE, lab / NONBAYES_SOURCE
    sources = {name: path for name, path in [
        ('bayes_predictions', bayes / 'predictions.parquet'),
        ('bayes_seats', bayes / 'seats.parquet'),
        ('bayes_tuning', bayes / 'tuning.parquet'),
        ('bayes_links', bayes / 'current_links.parquet'),
        ('bayes_current_joint', bayes / 'forecasts/scenario_selected_unconditioned.npz'),
        ('nonbayes_predictions', nonbayes / 'nonbayesian_predictions.parquet'),
        ('nonbayes_folds', nonbayes / 'nonbayesian_folds.parquet'),
        ('nonbayes_history', nonbayes / 'history.parquet'),
        ('working_designation', lab / 'WORKING_MODEL.json')]}
    digests = {k: sha(v) for k, v in sources.items()}
    old_notebooks = {p.name: sha(p) for p in lab.glob('*.ipynb')}
    b = pd.read_parquet(sources['bayes_predictions']).query('model == @BAYES_MODEL').copy()
    n = pd.read_parquet(sources['nonbayes_predictions']).query('model == "bias"').copy()
    cols = KEY + ['geography', 'special', 'as_of', 'actual', 'history_selection_10pp',
                  'q_pp', 'sample_count', 'prediction_pp', 'p_dem', 'posterior_sd_pp']
    b = b[cols].rename(columns={'prediction_pp': 'bayesian_pp', 'p_dem': 'bayesian_p_dem'})
    n = n[KEY + ['actual', 'q_pp', 'prediction_pp', 'prediction', 'n_samples']].rename(
        columns={'prediction_pp': 'nonbayesian_pp', 'n_samples': 'nonbayesian_n_samples'})
    paired = b.merge(n, on=KEY, how='outer', validate='one_to_one', suffixes=('', '_nb'), indicator=True)
    assert paired._merge.eq('both').all(), 'Unmatched forecast keys: never silently drop targets'
    paired = paired.drop(columns='_merge')
    assert np.allclose(paired.actual, paired.actual_nb, equal_nan=True), 'Outcome mismatch'
    assert np.allclose(paired.q_pp, paired.q_pp_nb, equal_nan=True), 'Poll snapshot mismatch'
    assert np.allclose(paired.nonbayesian_pp, 100*paired.prediction), 'Non-Bayesian units mismatch'
    assert np.isfinite(paired[['bayesian_pp', 'nonbayesian_pp']]).all().all()
    assert paired.loc[paired.cycle.eq(2026), 'actual'].isna().all()
    assert np.allclose(paired.bayesian_p_dem, norm.cdf(paired.bayesian_pp/paired.posterior_sd_pp))
    # Preserve missing polls. The complete component predictions already have their own fallbacks.
    paired['blend_pp'] = .5*paired.bayesian_pp + .5*paired.nonbayesian_pp
    paired['actual_pp'] = 100*paired.actual
    assert not (paired[['bayesian_pp', 'nonbayesian_pp', 'blend_pp']].eq(0)).any().any(), 'Explicit tie policy needed'
    for name, col in MODELS.items():
        paired[col + '_call'] = np.where(paired[col] > 0, 'D', 'R')
    paired['models_disagree'] = paired.bayesian_pp_call.ne(paired.nonbayesian_pp_call)
    paired['no_bayesian_polls'] = paired.q_pp.isna()
    paired['nonbayesian_prior_fallback'] = paired.nonbayesian_n_samples.eq(0)
    # Both pipelines use the same forecast dates; each retains its original aggregation recipe.
    nf = pd.read_parquet(sources['nonbayes_folds'])
    dates = paired.merge(nf[['scenario', 'cycle', 'cutoff_first', 'cutoff_last']],
                         on=['scenario', 'cycle'], validate='many_to_one')
    assert (pd.to_datetime(dates.as_of) == pd.to_datetime(dates.cutoff_first)).all()
    assert (pd.to_datetime(dates.as_of) == pd.to_datetime(dates.cutoff_last)).all()
    assert nf.refit_last.lt(nf.cycle).all() and nf.validation_cycle.lt(nf.cycle).all()
    bt = pd.read_parquet(sources['bayes_tuning']).query('base_model == "repaired_both"')
    for r in bt.itertuples():
        assert all(int(y) < r.cycle for y in str(r.validation_years).split(',') if y and y != 'nan')
    history = pd.read_parquet(sources['nonbayes_history'])
    for col in ['bias_training_max_cycle', 'bias_validation_cycle', 'poll_validation_cycle']:
        v = history[history[col].notna()]
        assert v[col].lt(v.cycle).all(), col
    hist = paired[paired.actual.notna()]
    cycles, groups = [], []
    for (sc, year), q in hist.groupby(['scenario', 'cycle']):
        for name, col in MODELS.items():
            errors = q[col]-q.actual_pp
            correct = (q[col].gt(0) == q.actual_pp.gt(0))
            cycles.append(dict(scenario=sc, cycle=int(year), model=name, n=len(q),
                               correct=int(correct.sum()), accuracy_pct=100*correct.mean(),
                               mae_pp=errors.abs().mean(), rmse_pp=np.sqrt((errors**2).mean()),
                               mean_error_pp=errors.mean()))
    cycles = pd.DataFrame(cycles)
    for first in [2012, 2016]:
        for sc, q in hist[hist.cycle.ge(first)].groupby('scenario'):
            subsets = {'all': q, 'competitive': q[q.history_selection_10pp.eq('competitive')],
                       'other_or_unknown_competitiveness': q[~q.history_selection_10pp.eq('competitive')],
                       'polled': q[q.q_pp.notna()], 'no_polls': q[q.q_pp.isna()]}
            for group, g in subsets.items():
                if g.empty:
                    continue
                for name, col in MODELS.items():
                    errors = g[col]-g.actual_pp
                    groups.append(dict(first_cycle=first, scenario=sc, group=group, model=name,
                                       cycles=g.cycle.nunique(), n=len(g),
                                       correct=int((g[col].gt(0)==g.actual_pp.gt(0)).sum()),
                                       mae_pp=errors.abs().mean(),
                                       mean_cycle_mae_pp=errors.abs().groupby(g.cycle).mean().mean()))
    groups = pd.DataFrame(groups)
    ss = pd.read_parquet(sources['bayes_seats']).query('model == @BAYES_MODEL')
    seat_rows = []
    for (sc, year), q in paired.groupby(['scenario', 'cycle']):
        ref = ss[ss.scenario.eq(sc) & ss.cycle.eq(year)].iloc[0]
        assert int(ref.fixed_D + q.bayesian_pp.gt(0).sum()) == ref.point_D
        for name, col in MODELS.items():
            d = int(ref.fixed_D + q[col].gt(0).sum())
            seat_rows.append(dict(scenario=sc, cycle=int(year), model=name, point_D=d, point_R=100-d,
                                  actual_D=ref.actual_D, fixed_D=int(ref.fixed_D), modeled_contests=len(q),
                                  unmodeled_contested=int(ref.unmodeled_contested)))
    seats = pd.DataFrame(seat_rows)
    current = paired[paired.cycle.eq(2026)].sort_values('target_id').copy()
    links = pd.read_parquet(sources['bayes_links']).query('model == @BAYES_MODEL')
    current = current.merge(links[['state', 'most_positive_state', 'positive_rho']],
                            left_on='geography', right_on='state', validate='one_to_one').rename(
                                columns={'most_positive_state': 'positive_partner'})
    assert len(current) == 35 and current.positive_partner.isin(current.geography).all()
    joint = np.load(sources['bayes_current_joint'])
    ordered = current.set_index('target_id').loc[joint['target_ids'].astype(str)]
    assert np.allclose(ordered.bayesian_pp, joint['joint_mean'][:-2])
    assert np.allclose(ordered.bayesian_p_dem, joint['p_dem'])
    assert all(sha(sources[k]) == h for k, h in digests.items())
    assert all(sha(lab/n) == h for n, h in old_notebooks.items())
    out = lab/'reports/bayesian_nonbayesian_blend'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    out.mkdir(parents=True)
    tables = dict(paired_predictions=paired, cycle_scores=cycles, group_scores=groups, seats=seats,
                  current_states=current, current_display=current_display(current),
                  historical_disagreements=hist[hist.models_disagree])
    for name, table in tables.items():
        table.to_parquet(out/f'{name}.parquet', index=False)
    settings = dict(data_as_of='2026-09-17', bayesian_model=BAYES_MODEL, nonbayesian_model='bias',
                    bayesian_weight=.5, nonbayesian_weight=.5, fitted_new_parameters=0,
                    refit=False, refresh=False, promotion=False, probability_policy='Only Bayesian probabilities are shown; no blend probability or interval is assigned.',
                    sources={k:dict(path=str(v.relative_to(lab)), sha256=digests[k]) for k,v in sources.items()},
                    old_notebook_hashes=old_notebooks)
    (out/'settings.json').write_text(json.dumps(settings, indent=2)+'\n')
    audit = dict(passed=True, paired_rows=len(paired), historical_rows=len(hist), current_rows=len(current),
                 historical_cycles=sorted(map(int,hist.cycle.unique())),
                 checks=['Exact one-to-one keys and labels', 'Matching poll snapshots and forecast dates',
                         'Percentage-point units verified', 'No missing component predictions',
                         'Current labels remain missing', 'Current Bayesian posterior reproduces',
                         'Saved component tuning uses earlier cycles', 'No blend parameters fitted',
                         'Seat count baseline reproduces', 'Current-cycle correlation partners only',
                         'Source files and existing notebooks unchanged'])
    (out/'audit.json').write_text(json.dumps(audit, indent=2)+'\n')
    recent = groups.query('first_cycle == 2016 and group == "all"')
    report = '''# Bayesian/non-Bayesian equal-margin blend

Fixed rule per contest: blend = 0.5 × Bayesian mean margin + 0.5 × non-Bayesian margin.
All margins are D−R percentage points; positive predicts D. Zero new fitted parameters.

The Bayesian component is the same experimental repaired-prior + momentum/approval + signed-factor model used in the current state table (`repaired_both__selected`). Its factor strength is selected using earlier cycles. It has not replaced the designated working model.
The non-Bayesian component is the retained `bias` benchmark, with its existing recency/firm-weighted polling baseline, already-selected prior blend/fallback, and historical correction for polled races. It is not simply the displayed raw poll aggregate plus a correction.

These are frozen September17 inputs. Earlier historical forecasts are September17 of each cycle; late forecasts are October31. Matched contest keys, outcomes and dates are required. Missing polls stay missing; complete component predictions retain their existing fallback. Only Bayesian probabilities/correlations are shown: averaging point forecasts does not establish the blend's uncertainty. Two components share data, so treating their errors as independent would be inappropriate.

Saved chronological component forecasts are reused for 2012–2024, with identical fixed 50/50 weights in each fold and 2026. Prior architecture exploration on these outcomes means this is exploratory evaluation, not an untouched test. No new best-weight search or model promotion.

## Recent performance, 2016–2024

MAE is absolute margin error in percentage points (lower is better). `mae_pp` pools contests; `mean_cycle_mae_pp` gives each cycle equal weight. Correct calls use the sign of the unrounded margin. Each horizon has 140 matched contests across 5 cycles.

'''
    report += label_frame(recent.round(4)).to_markdown(index=False)
    report += '\n\n## Every historical cycle\n\n'+label_frame(cycles.round(4)).to_markdown(index=False)
    report += '\n\n## Current state table\n\n'+label_frame(tables['current_display']).to_markdown(index=False)
    report += '\n\n## Current point seat totals\n\n'+label_frame(seats[seats.cycle.eq(2026)]).to_markdown(index=False)
    report += '''\n\nSeat totals count margin-sign winners plus the same fixed-seat ledger for all models. These are point seat counts, not expected seats or control probabilities. Historical totals retain the source's explicit incumbent-caucus completion assumptions for unmodeled contests; those are excluded from state accuracy. Current 35 contests are all modeled. Existing independent-proxy and ballot-system caveats remain, including Nebraska; these outputs do not repair that admission policy.

Additional polled/no-poll and past-results-only competitive subsets are saved in `group_scores.parquet` and displayed in the notebook. The recipe, source hashes and audit are archived alongside outputs.
'''
    (out/'RESULTS.md').write_text(report)
    shutil.copy2(__file__, out/Path(__file__).name)
    files = {str(p.relative_to(out)): sha(p) for p in out.rglob('*') if p.is_file()}
    (out/'manifest.json').write_text(json.dumps(files, indent=2)+'\n')
    (out.parent/'latest.json').write_text(json.dumps(dict(artifact=out.name, manifest_sha256=sha(out/'manifest.json')),indent=2)+'\n')
    print('OUTPUT', out)
    print(recent[['scenario','model','n','correct','mae_pp','mean_cycle_mae_pp']].to_string(index=False))
    print(seats[seats.cycle.eq(2026)][['model','point_D','point_R']].to_string(index=False))
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lab', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    build(args.lab)
