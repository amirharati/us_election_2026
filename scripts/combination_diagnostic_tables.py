"""Readable tables for the intercept and convex-blend experiment; no fitting."""
from pathlib import Path
import json
import pandas as pd
from combination_diagnostics import LABELS, MAIN, MODELS
from seat_review_tables import margin, seats
from run_combination_diagnostics import refresh

COMPARE = ['bias', 'original_both', 'zero_intercept', 'shrunk_intercept', 'blend_half', 'blend_90', 'blend_selected']
HORIZONS = {'matched_live': 'September 17', 'oct31': 'October 31'}


def load(out):
    return {p.stem: pd.read_parquet(p) for p in Path(out).glob('*.parquet')}


def performance(frames, group='all', period='2016_onward', models=MAIN):
    q = frames['groups']; rows = []
    for model in models:
        row = {'Model': LABELS[model]}
        for scenario, name in HORIZONS.items():
            r = q[q.model.eq(model) & q.scenario.eq(scenario) & q.group.eq(group) & q.period.eq(period)].iloc[0]
            row[name + ' correct'] = f'{r.correct}/{r.n}'
            row[name + ' MAE (pp)'] = round(r.mae_pp, 3)
        rows.append(row)
    return pd.DataFrame(rows)


def cycle_table(frames, scenario, metric='calls', models=COMPARE):
    assert metric in ['calls', 'mae', 'seats']
    totals = frames['seat_totals']; rows = []
    for year in range(2006, 2026, 2):
        g = totals[totals.cycle.eq(year) & totals.scenario.eq(scenario)].set_index('model')
        row = {'Cycle': year, 'Status': 'Scored' if len(g) else 'Warm-up'}
        if len(g):
            first = g.iloc[0]
            row['Scored / contested'] = f'{int(first.modeled_contests)}/{int(first.contested)}'
            if metric == 'seats':
                row['Actual'] = seats(first.actual_D, first.actual_R)
                row['Unmodeled completion assumptions'] = int(first.unmodeled_contests)
            for model in models:
                r = g.loc[model]
                row[LABELS[model]] = (f'{int(r.modeled_correct)}/{int(r.modeled_contests)}' if metric == 'calls'
                    else round(r.modeled_mae_pp, 3) if metric == 'mae' else seats(r.completion_D, r.completion_R))
        rows.append(row)
    return pd.DataFrame(rows).fillna('—')


def state_table(frames, year=2026, scenario='matched_live', models=None):
    models = models or ['polling', 'bias', 'zero_intercept', 'shrunk_intercept', 'fundamentals', 'blend_half', 'blend_90', 'blend_selected']
    q = frames['predictions']; q = q[q.cycle.eq(year) & q.scenario.eq(scenario)]
    if q.empty:
        return pd.DataFrame({'Status': ['Warm-up: no matched experiment forecasts']})
    vals = q.pivot(index='target_id', columns='model', values='prediction') * 100
    base = q[q.model.eq('bias')].set_index('target_id'); rows = []
    for target in vals.index:
        r = base.loc[target]
        row = {'State': r.geography + (' special' if '-special-' in target else ''),
               'Poll samples': int(r.n_samples), 'Actual margin': 'Pending' if pd.isna(r.actual) else margin(100*r.actual)}
        row.update({LABELS[m]: margin(vals.loc[target, m]) for m in models})
        rows.append(row)
    return pd.DataFrame(rows).sort_values('State').reset_index(drop=True)


def current_seats(frames, models=MAIN):
    q = frames['seat_totals']; q = q[q.cycle.eq(2026)].set_index('model')
    return pd.DataFrame([{'Model': LABELS[m], '2026 point-call total': seats(q.loc[m, 'completion_D'], q.loc[m, 'completion_R']),
                          'Actual': 'Pending'} for m in models])


def blend_weights(frames):
    q = frames['blend_selection']; q = q[q.selected].copy()
    q['Horizon'] = q.scenario.map(HORIZONS)
    return q[['cycle', 'Horizon', 'validation_cycle', 'polling_weight', 'validation_mae_pp']].rename(columns={
        'cycle': 'Forecast cycle', 'validation_cycle': 'Validation cycle', 'polling_weight': 'Corrected-polling weight',
        'validation_mae_pp': 'Previous-cycle MAE (pp)'}).round(3)


def write_report(lab, out):
    lab, out = Path(lab), Path(out); f = load(out)
    parts = ['''# Intercept controls and polling/fundamentals blends

Executed September 18, 2026; current inputs end September 17. Notebook Sections 106–109.

## Exactly what changed

**C = corrected polling**: the existing polling forecast plus decayed state forecast-error calibration. **F = fundamentals**: the existing historical state prior plus a shared momentum/approval regression predicting the remaining outcome margin. F has no current polling input; it does retain the state prior. Both scores account for White House party.

1. **Intercept controls:** fit actual minus C on the same two features, either without an extra intercept or with a strongly penalized intercept. The latter penalty is ten times training cycle-weight mass, so at fixed slope penalty it reduces the old intercept to one-eleventh. Inputs are centered using training data, so zero intercept means zero correction at the historical training-average feature context, not at an arbitrary raw score of zero. Slope ridge alpha is selected on Y−2; matched-original-alpha controls isolate intercept removal from retuning.
2. **Blend:** `w*C + (1−w)*F`. Compare fixed 50/50 and **90% polling / 10% fundamentals** with w selected from 0, .25, .5, .75, 1 using previous-cycle **polled** MAE; ties favor polling. Both validation constituents are forecasts trained before their validation outcome. Refit the current constituents using only earlier cycles. No 2026 outcomes exist or enter selection. The fixed 90/10 sensitivity was added at the user's request; .9 is not added to the selected-weight grid, so earlier selections remain directly comparable.

No-poll states retain their old prior in the intercept experiment. The blend uses F alone there. A **fallback-only control** uses C for every polled state and F for no-poll states, separating these effects. Thus w=1 is unchanged corrected polling on polled states, but not necessarily on all states.

Training uses all eligible earlier history, with the existing eight-year feature half-life; no new feature search. Require six polled training cycles before the previous-cycle validation fold. The requested ten-cycle window is 2006–2024: 2006/2008/2010 are explicitly warm-up, leaving seven scored cycles, 2012–2024. This avoids lowering the guard to manufacture older results. Fundamentals also use older outcome-only cycles; the reconstructed 2010 fundamentals forecast is used only for 2012 weight validation.

Margins are D−R percentage points. Accuracy is correct modeled-race winner calls, not seats and not national popular vote. Summary MAE averages per-cycle MAEs; correct calls pool contests. Both horizons use the same admitted target set, with separate fits and tuning. September 17 matches the live calendar date; October 31 is a later forecast with more information. These historical outcomes have already guided many exploratory experiments, so this is not a fresh confirmatory test.

## Recent cycles, 2016–2024

''', performance(f).to_markdown(index=False), '\n\n### Historically competitive states\n\n',
             performance(f, 'competitive').to_markdown(index=False), '\n\n### All seven scored cycles, 2012–2024\n\n',
             performance(f, period='2012_onward').to_markdown(index=False)]
    for scenario, label in HORIZONS.items():
        for metric, title in [('calls', 'Correct winner calls'), ('mae', 'Mean absolute margin error (pp)'), ('seats', 'Full chamber point-call totals')]:
            parts += [f'\n\n## {label}: {title}\n\n', cycle_table(f, scenario, metric).to_markdown(index=False)]
    parts += ['''

Full totals add continuing seats and explicitly assume unmodeled historical races retain their pre-cutoff incumbent caucus. Those assumptions are excluded from model accuracy; they are not validated forecasts. D includes Democratic-caucusing independents. Actual totals use following-January-31 membership, including 2020 Georgia runoffs. Current totals remain conditional on the unresolved independent/ballot/RCV/runoff treatment; these are not expected seats or control probabilities.

## Current 2026

''', current_seats(f).to_markdown(index=False), '\n\n', state_table(f).to_markdown(index=False), '''

The selected blend is **75% corrected polling / 25% fundamentals**. Michigan moves from R+3.78 to R+1.12; Maine from D+0.03 to D+2.03. Alaska and Texas move from narrowly D to R because their fundamentals retain Republican historical baselines. The current shared fundamentals adjustment is pro-D, but it does not erase those state baselines. Interpolation smooths disagreement between these two estimates; it need not move toward a tie or improve accuracy. Temporal forecast volatility has not been tested here.

The original extra correction is −1.117 pp; removing its intercept gives +1.032 pp after retuning, and shrinking it gives +0.174 pp. Both intercept controls keep the current 50D/50R calls. At the original alpha, removing the intercept gives +0.303 pp: the larger +1.032 change also reflects retuning, not just deleting a constant.

The fixed **90/10** blend gives 124/138 September calls and 130/138 October calls, versus bias-only 125/132. Its September MAE improves 7.364→7.266 pp, while October worsens 5.230→5.360 pp. Competitive calls are 42/52 and 47/52, versus 43/47. It is a gentler change in margins, but not a consistent winner-call improvement. Compared with bias alone it spoils MT2020 at September17, and MO2016/AZ2018 at October31; each forecast is close to zero. These changes occur in polled states, not from the no-poll fallback.

Current90/10 Michigan is R+2.72, Maine D+0.83, Alaska R+0.21 and Texas R+0.20. Even a10% fundamentals weight flips the narrow Alaska/Texas calls, producing48D/52R. The two nearly tied calls explain why a small margin change can move two seats. The fixed weight is not selected from current outcomes, and the original past-selected grid remains unchanged.

## Tuning and controls

''', blend_weights(f).to_markdown(index=False), '\n\n### Full control comparison, recent all-state targets\n\n',
        performance(f, models=MODELS).to_markdown(index=False), '\n\n### Polled targets only\n\n',
        performance(f, group='polled', models=['bias', 'fundamental_fallback', 'blend_half', 'blend_90', 'blend_selected']).to_markdown(index=False),
        '\n\n### No-poll targets only\n\n', performance(f, group='no_polls', models=['bias', 'fundamental_fallback', 'blend_half', 'blend_90', 'blend_selected']).to_markdown(index=False), '''

The selected blend improves the recent September total by one call (125→126) and a little MAE (7.364→7.313). At October 31 every selected historical weight is 100% polling: calls tie at 132 and the small MAE change comes only from the no-poll fundamentals fallback. Fixed 50/50 blending worsens both horizons overall. Intercept controls improve on the old extra-factor stack but do not beat bias-only winner calls (124/129 versus 125/132). No automatic model promotion follows these mixed results.

## Reproducibility and checks

The run contains every state prediction and actual (`predictions.parquet`), all 100 seats per model/cycle (`full_seat_ledger.parquet`), fold counts, fitting coefficients, all validation candidates and source hashes. State tables in notebook Section108 can display any scored cycle/horizon. Missing outcomes remain missing. Scripts: `combination_diagnostics.py`, `run_combination_diagnostics.py`, `combination_diagnostic_tables.py`.

''']
    settings = json.loads((out/'settings.json').read_text())
    parts += [f"Independent augmented least-squares audit: {settings['audit_final_fits']} final fits, {settings['audit_inner_candidates']} inner candidates; {settings['audit_blend_candidates']} blend validation losses and all convex bounds checked. Six reference models each reproduce all 427 saved forecasts. Tests cover future-label perturbation, missing features, exact intercept shrinkage, blend endpoints and historical seat reconstruction.\n\nArtifacts: `{out.relative_to(lab)}`.\n"]
    report = ''.join(parts)
    (lab/'COMBINATION_DIAGNOSTICS_RESULTS.md').write_text(report)
    (out/'COMBINATION_DIAGNOSTICS_RESULTS.md').write_text(report)
    (out/'combination_diagnostic_tables.py').write_bytes(Path(__file__).read_bytes())
    refresh(out)
    return f
