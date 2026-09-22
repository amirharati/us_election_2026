"""Descriptive screening for room for a different outcome; no model fitting."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import election_lab as lab
from live_uncertainty_watchlist import build_watchlist

CORE_MODELS = ('Bayesian', 'Matched Student-t (df5)', 'Older Gaussian',
               'Student-t research helper', 'Non-Bayesian corrected')
METHOD = (
    'Reference-model winner, margin, 95% interval and other-winner probability describe the likely outcome and its alternatives. '
    'Disagreement is the mean absolute pairwise difference in core-model margins. '
    'Predictive SD is the square root of the mean within-model variance, not variance between model means. '
    'Blends/mixtures are excluded; the core models share evidence and are not independent votes. '
    'Within each polling group, select the top 3 races on each of disagreement, predictive SD, reference-model other-winner probability, and historical mean absolute error (at least two past races); '
    'take their union and order by other-winner probability. Ties are broken by contest name. '
    'This is a review screen, not a calibrated probability of surprising the public. '
    'History uses the last three completed state races in September backtests before the current cycle; '
    'it can include other Senate seats and special elections. These are reconstructed forecasts, not issued forecasts. '
    'Past errors are context and do not alter current probabilities.'
)


def historical_context(history, cutoff_year, scenario='matched_live'):
    h = history[(history.cycle < cutoff_year) & history.scenario.eq(scenario)
                & history.actual.notna()].copy()
    if 'historical_horizon_comparable' in h:
        h = h[h.historical_horizon_comparable.eq(True)]
    if h.duplicated(['target_id', 'scenario']).any():
        raise ValueError('Historical reference forecasts must be unique per race and horizon')
    h['error_pp'] = (h.prediction_pp - 100*h.actual).abs()
    h['interval_miss'] = (100*h.actual < h.lo95_pp) | (100*h.actual > h.hi95_pp)
    h['wrong_winner'] = (h.prediction_pp > 0) != (h.actual > 0)
    rows = []
    for state, races in h.groupby('geography'):
        recent = races.sort_values(['cycle','target_id']).tail(3)
        worst = recent.sort_values(['error_pp','cycle'], ascending=False).iloc[0]
        rows.append(dict(geography=state, historical_n=len(recent),
            historical_cycles=', '.join(str(int(x)) for x in recent.cycle),
            historical_mae_pp=recent.error_pp.mean(), worst_error_pp=worst.error_pp,
            worst_error_cycle=int(worst.cycle), interval_misses=int(recent.interval_miss.sum()),
            wrong_winners=int(recent.wrong_winner.sum())))
    return pd.DataFrame(rows, columns=['geography','historical_n','historical_cycles',
        'historical_mae_pp','worst_error_pp','worst_error_cycle','interval_misses','wrong_winners'])


def summarize(predictions, coverage, history, cutoff_year, top_n=3):
    if top_n < 1: raise ValueError('top_n must be positive')
    p = predictions[predictions.model.isin(CORE_MODELS)].copy()
    if p.duplicated(['target_id','model']).any(): raise ValueError('Duplicate race/model prediction')
    rows = []
    for target, frame in p.groupby('target_id'):
        reference = frame[frame.model.eq('Bayesian')]
        if len(reference) != 1: raise ValueError('Each contest needs a reference Bayesian prediction')
        ref = reference.iloc[0]
        means = frame.prediction_pp.dropna().to_numpy()
        diffs = np.abs(means[:,None]-means[None,:])[np.triu_indices(len(means),1)]
        sd = frame.posterior_sd_pp.dropna()
        rows.append(dict(target_id=target, geography=ref.geography,
            contest=ref.geography+(' special' if ref.special else ''),
            likely_winner='D' if ref.p_dem >= .5 else 'R', margin_pp=ref.prediction_pp,
            lo95_pp=ref.lo95_pp, hi95_pp=ref.hi95_pp,
            other_winner_pct=100*min(ref.p_dem,1-ref.p_dem),
            disagreement_pp=float(diffs.mean()) if len(diffs) else np.nan,
            predictive_variance_pp2=float((sd**2).mean()) if len(sd) else np.nan,
            predictive_sd_pp=float(np.sqrt((sd**2).mean())) if len(sd) else np.nan,
            model_count=len(means), uncertainty_model_count=len(sd),
            winner_split=bool((frame.p_dem > .5).any() and (frame.p_dem < .5).any()),
            interval_crosses_tie=bool(ref.lo95_pp <= 0 <= ref.hi95_pp)))
    if set(coverage.target_id) != set(p.target_id):
        raise ValueError('Polling coverage must include every predicted contest, including zero-poll races')
    all_rows = pd.DataFrame(rows).merge(coverage,on='target_id',validate='one_to_one')
    all_rows = all_rows.merge(historical_context(history,cutoff_year),on='geography',how='left',validate='many_to_one')
    all_rows['polling_group'] = np.where(all_rows.stronger_coverage,'Adequately polled','Thin/no recent polling')
    all_rows['selection_reason'] = ''
    metrics = [('disagreement_pp','model disagreement'),('predictive_sd_pp','predictive uncertainty'),
               ('other_winner_pct','other-winner probability'),
               ('historical_mae_pp','past margin error')]
    for _, group in all_rows.groupby('polling_group'):
        reasons = {i:[] for i in group.index}
        for metric,label in metrics:
            eligible = group[group[metric].notna() & group[metric].gt(0)]
            if metric == 'historical_mae_pp': eligible = eligible[eligible.historical_n.ge(2)]
            ranked = eligible.sort_values([metric,'contest'],ascending=[False,True])
            for rank,i in enumerate(ranked.head(top_n).index,1): reasons[i].append(f'{label.capitalize()} ranks #{rank} in this group.')
        for i, labels in reasons.items():
            if not labels: continue
            r = all_rows.loc[i]
            if r.winner_split: labels.append('Models disagree on the winner.')
            if r.recent_samples == 0: labels.append('There are no recent eligible polls.')
            elif not r.stronger_coverage: labels.append('Recent polling is limited.')
            if pd.notna(r.interval_misses) and r.interval_misses > 0:
                labels.append(f'{int(r.interval_misses)} of {int(r.historical_n)} past results fell outside the 95% range.')
            all_rows.loc[i,'selection_reason'] = ' '.join(labels)
    selected = all_rows[all_rows.selection_reason.ne('')].sort_values(['other_winner_pct','disagreement_pp','contest'],ascending=[False,False,True])
    return dict(all=all_rows, polled=selected[selected.stronger_coverage].copy(),
                thin=selected[~selected.stronger_coverage].copy())


def build_surprise_watchlist(run, recent_days=30, min_samples=3, min_firms=2, top_n=3):
    run = lab.verify_run(Path(run))
    meta = json.loads((run/'run.json').read_text())
    base = build_watchlist(run,CORE_MODELS,recent_days=recent_days,min_samples=min_samples,min_firms=min_firms)
    coverage = base['all_contests'].query("model == 'Bayesian'")[
        ['target_id','recent_samples','recent_firms','latest_poll','stronger_coverage']]
    history_path = lab.ASSETS/'main/predictions.parquet'
    result = summarize(pd.read_parquet(run/'predictions.parquet'),coverage,
                       pd.read_parquet(history_path),pd.Timestamp(meta['as_of']).year,top_n)
    result['parameters'] = dict(as_of=meta['as_of'],recent_days=recent_days,min_samples=min_samples,
        min_firms=min_firms,top_n=top_n,core_models=list(CORE_MODELS),
        available_models=[m for m in CORE_MODELS if m in pd.read_parquet(run/'predictions.parquet').model.values],
        history_sha256=lab.sha(history_path),historical_scope='state, not necessarily same Senate seat',
        historical_scenario='matched_live',source_manifest_sha256=lab.sha(run/'manifest.json'))
    return result


def display_table(frame):
    """Compact human-readable table; full numerical columns remain in Parquet."""
    out = pd.DataFrame(index=frame.index)
    out['Race'] = frame.contest
    out['Likely winner'] = frame.likely_winner
    out['D−R margin'] = frame.margin_pp.round(1)
    out['95% range (pp)'] = [f'{lo:.1f} to {hi:.1f}' for lo,hi in zip(frame.lo95_pp,frame.hi95_pp)]
    out['Other winner %'] = frame.other_winner_pct.map(lambda x: '<0.1' if 0 < x < .05 else f'{x:.1f}')
    out['Disagreement (pp)'] = frame.disagreement_pp.round(1)
    out['Predictive SD (pp)'] = frame.predictive_sd_pp.round(1)
    out['Recent polls / firms'] = [f'{n} / {f}' for n,f in zip(frame.recent_samples,frame.recent_firms)]
    out['Past state surprises'] = [
        'No comparable history is available.' if pd.isna(r.historical_n) else
        f'The largest miss was {r.worst_error_pp:.1f} pp in {int(r.worst_error_cycle)}. '
        f'{int(r.interval_misses)} of {int(r.historical_n)} results fell outside the 95% range. '
        f'It missed the winner in {int(r.wrong_winners)} of {int(r.historical_n)} races.'
        for r in frame.itertuples()]
    out['Why watch'] = frame.selection_reason
    return out.reset_index(drop=True)


def render_table(frame):
    """Notebook HTML with complete, wrapping text instead of pandas truncation."""
    from IPython.display import HTML
    table = display_table(frame).to_html(index=False, escape=True)
    style = '<style>.surprise-watchlist td,.surprise-watchlist th {white-space:normal;overflow-wrap:anywhere;vertical-align:top;text-align:left;} .surprise-watchlist td:nth-last-child(-n+2) {min-width:220px;max-width:340px;} .surprise-watchlist {overflow-x:auto;}</style>'
    return HTML(style+'<div class="surprise-watchlist">'+table+'</div>')
