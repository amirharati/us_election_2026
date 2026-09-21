"""Tables for explicitly separated historical priors and feature signals."""
from pathlib import Path
import pandas as pd
from separate_feature_adjustments import LABELS, NEW
from seat_review_tables import margin,seats
from run_combination_diagnostics import refresh

ORDER=['bias','blend_90','outcome_signal_10','outcome_signal_50','residual_signal_10','residual_signal_50']

def performance(f,group='all'):
 rows=[]
 for model in ORDER:
  row={'Model':LABELS[model]}
  for scenario,name in [('matched_live','Sep17'),('oct31','Oct31')]:
   r=f['groups'].query('model == @model and scenario == @scenario and group == @group').iloc[0]
   row[name+' correct']=f'{r.correct}/{r.n}';row[name+' MAE (pp)']=round(r.mae_pp,3)
  rows.append(row)
 return pd.DataFrame(rows)

def cycles(f,scenario):
 rows=[]
 for year in range(2006,2026,2):
  q=f['seat_totals'].query('cycle == @year and scenario == @scenario').set_index('model')
  row={'Cycle':year,'Status':'Scored' if len(q) else 'Warm-up'}
  for m in ORDER:
   row[LABELS[m]]='—' if q.empty else f'{int(q.loc[m,"modeled_correct"])}/{int(q.loc[m,"modeled_contests"])}'
  rows.append(row)
 return pd.DataFrame(rows)

def states(f,year=2026,scenario='matched_live'):
 p=f['predictions'].query('cycle == @year and scenario == @scenario');v=p.pivot(index='target_id',columns='model',values='prediction')*100
 b=p.query("model == 'bias'").set_index('target_id');rows=[]
 for target,r in b.iterrows():
  row={'State':r.geography+(' special' if '-special-' in target else ''),'Poll samples':int(r.n_samples),'Actual':'Pending' if pd.isna(r.actual) else margin(100*r.actual)}
  row.update({LABELS[m]:margin(v.loc[target,m]) for m in ORDER});rows.append(row)
 return pd.DataFrame(rows).sort_values('State')

def seat_table(f):
 rows=[]
 for (year,scenario),g in f['seat_totals'].groupby(['cycle','scenario']):
  g=g.set_index('model');r=g.loc['bias'];row={'Cycle':year,'Horizon':scenario,'Actual':'Pending' if pd.isna(r.actual_D) else seats(r.actual_D,r.actual_R),'Unmodeled completion assumptions':int(r.unmodeled_contests)}
  row.update({LABELS[m]:seats(g.loc[m,'completion_D'],g.loc[m,'completion_R']) for m in ORDER});rows.append(row)
 return pd.DataFrame(rows)

def report(lab,out):
 lab,out=Path(lab),Path(out);f={p.stem:pd.read_parquet(p) for p in out.glob('*.parquet')}
 text='''# Separate historical priors from economic and approval contributions

Notebook Sections110–112. This corrects the interpretation/architecture of the earlier "fundamentals blend"; the earlier arithmetic was valid for a blend of two complete forecasts, but that was not a feature-only adjustment.

## Explicit components

- **P:** historical state prior. It remains in the existing polling regularization/fallback where already used, and in the outcome-model training offset. It is not inserted again by the new feature layer.
- **C:** existing polling forecast plus decayed state forecast-error correction.
- **a:** feature-regression intercept, recorded separately and excluded from the new adjustment.
- **G:** momentum coefficient × standardized economic-momentum score + approval coefficient × standardized presidential-approval score. Both scores account for White House party. Training-only centering/scaling/filling is preserved. Zero signal is the fitted training-average context, not a claim of objectively neutral economic conditions. Coefficients are learned, not forced to favor either party.

The old outcome forecast was `F = clip(P + a + G)`. The old90/10 blend `0.9*C + 0.1*F` therefore mixed state historical lean into the forecast again. The new formula is **`clip(C + strength*G)`**, equivalently a blend between C and C+G before final clipping. We retain C at full weight, rather than shrinking it toward a zero-centered feature value.

Two sources of G are kept explicit: **outcome contribution** reuses slopes trained on actual minus historical prior; **residual contribution** reuses the zero-intercept slopes trained on actual minus chronological corrected polling. The latter targets what remains unexplained by polls. Transferring outcome slopes onto polling is only a sensitivity: polls may already include that information. Removing an intercept from a fitted outcome regression changes its calibration, so historical performance is evaluated rather than presumed.

Fixed strengths10% and50% are applied to each, with no new search or tuning. The slopes and their ridge choices come only from earlier-cycle fits/Y−2 validation, with existing8-year history decay. For this controlled comparison only polled targets receive the adjustment; no-poll targets retain exactly the C fallback, avoiding another simultaneous policy change. Thus there is no new historical-state mixing or generic intercept in either feature-only layer.

## Recent2016–2024 results

'''+performance(f).to_markdown(index=False)+'\n\n### Historically competitive targets\n\n'+performance(f,'competitive').to_markdown(index=False)
 for scenario,title in [('matched_live','September17'),('oct31','October31')]:text+='\n\n## '+title+': correct modeled winner calls by cycle\n\n'+cycles(f,scenario).to_markdown(index=False)
 text+='''

2006/2008/2010 remain warm-up; the experiment requires six polled training cycles before the previous-cycle validation. All seven scored cycles2012–2024 are retained; recent five are emphasized. MAE is D−R percentage-point error averaged equally across cycles. Calls pool modeled contests, not100seats. These are repeatedly examined exploratory outcomes, not untouched confirmation data.

## Current decomposition and predictions

The outcome fit gives **+0.411pp momentum +3.256pp approval = +3.667pp feature contribution**. Its separate intercept is−2.553pp, leaving the previously reported+1.114pp net adjustment on top of a state prior. That+1.114was not pure feature contribution. At10% the new outcome-feature layer adds+0.367pp to C.

The residual fit gives **+0.447pp momentum +0.585pp approval = +1.032pp**, with zero extra intercept. At10% it adds+0.103pp. These two G values differ because their training targets, histories and normalization differ. Neither reintroduces state prior P.

All four new current feature-only variants retain **50D/50R**. Alaska and Texas remain D; the old90/10full-forecast blend's R flips disappear. Michigan remains R under these strengths because its existing historical polling-error correction is large; this change does not remove that correction or force a preferred current outcome.

'''+states(f).to_markdown(index=False)+'\n\n## Complete seat scenarios, with historical actuals\n\n'+seat_table(f).to_markdown(index=False)+'''

D includes Democratic-caucusing independents. Historical totals retain explicit incumbent-caucus completion assumptions for unmodeled races; those assumptions are excluded from model accuracy. Actual totals use following-January31 membership. Current totals remain conditional on ballot/independent/RCV/runoff assumptions; not expected seats or calibrated control probabilities.

The10% residual layer preserves recent winner calls125/138early and132/138late. MAE slightly improves early7.364→7.348pp and slightly worsens late5.230→5.264pp. This fixes the hidden state-prior contribution, without establishing a new accuracy improvement. The old complete-forecast blend remains clearly labeled as a historical control.

## Audit

Thirty component fits independently reconstructed from training-only designs using augmented least squares; stored feature contributions match. The old outcome forecast is recovered exactly from prior + intercept + both features, with clipping. Additive identity and unchanged no-poll fallbacks are checked for every new forecast. Tests check intercept/prior independence, centering/missing values, fixed-base/no-poll behavior and positive-signal direction. Artifacts include every component, prediction, actual and full100-seat ledger. Prior notebook outputs are retained; new cells were evaluated in-process inside the sandbox without launching a kernel.

'''+f'Artifacts: `{out.relative_to(lab)}`. Scripts: `separate_feature_adjustments.py`, `separate_feature_tables.py`.\n'
 (lab/'SEPARATED_FEATURE_RESULTS.md').write_text(text);(out/'SEPARATED_FEATURE_RESULTS.md').write_text(text)
 (out/'separate_feature_tables.py').write_bytes(Path(__file__).read_bytes());refresh(out)
 return f
