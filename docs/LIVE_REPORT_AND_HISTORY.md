# Saved live reports and cutoff history

Notebook04 now saves a current-only report before starting the cutoff replay,
then a complete report once the replay succeeds. Each is an immutable timestamped
directory under `outputs/live_reports/`; `latest.json` points to the latest
completed report. The self-contained `report.html` embeds its chart. Adjacent
Parquet files preserve the current predictions, chamber probabilities, watchlist,
and cutoff-history tables; the chart is also available as PNG. No ZIP is created.

## What the timeline means

Each point asks: **what would our current trained models predict with evidence
restricted to this cutoff?** It is not an archived forecast issued on that date.
The roster, candidate screening decisions, historical fits, model selection,
normalizers, priors, error corrections, covariance assumptions and blend weights
remain fixed. The models were calibrated for September/October horizons; January
probabilities have not been separately validated for that longer horizon.

Default cutoffs start January 1, 2026, every 30 days, plus the last 3 calendar days,
including the current forecast date. The grid is date arithmetic, not calendar
month ends or trading days. Duplicate dates are removed. Set
`HISTORY_EVERY_DAYS=7` for a weekly grid or 1 for every day. Lines between grid points
are visual connections, not newly evaluated forecasts.

Every retained model in the current live run is included: final/older Gaussian,
matched/older Student, corrected-polling helper, Gaussian mean-only blends, the
four-model mixture and all retained mixture mean shifts. If the user explicitly
runs live inference without Student models, the timeline mirrors that reduced
model roster and does not silently substitute approximations.

## Evidence and chronology

For each cutoff, the existing polling cleanup/screening and sample grouping run
again. A poll must have finished fieldwork by the cutoff, and a known release date
must also be no later than the cutoff. Unknown release dates use field-end dates;
the evidence table counts those question versions explicitly. Tied questions from
one sample do not count as separate model observations. The model's existing
two-year election-cycle window remains in force, so a January 2026 point can use
eligible 2025 polls. Decay ages are recomputed at each cutoff, including days with
no new polls.

`HISTORY_FEATURE_MODE='dated'` recomputes current-cycle feature contexts and changes
from the existing dated sources. Complete reference periods end by the cutoff,
and missing values follow the existing training-time strategy. The feature
ledger is saved with each newly computed forecast. **Reference-period eligibility
is not publication-date availability:** this uses today's revised historical data
and the model's reference view. Thus it cannot certify a strictly real-time
backtest. Current source archives and screening can also omit or reclassify
polls/candidates that were relevant earlier in 2026.

`'fixed_latest'` deliberately holds today's feature context fixed and changes
polling cutoffs only. This is a sensitivity experiment, not historical information
availability. The final endpoint in either mode is the exact current live run.
Changing the cutoff never changes the pinned dataset on disk or the latest-live
pointer; intermediate forecasts live under `outputs/cutoff_forecasts/`.

## Control probabilities and uncertainty

The Democratic bloc includes caucusing independents according to existing seat
accounting. D control is `P(D seats >= 51)`; R control is its complement and
includes 50–50 under the assumed Republican vice-president's tie-break. These are
control probabilities, not both parties' strict-majority probabilities.

Joint Gaussian/Student/mixture distributions generate chamber results with their
existing state dependencies. The non-Bayesian helper retains its explicitly
independent-state chamber approximation. Student runs keep the actual samplers
and convergence checks, rather than substituting a Gaussian or merely widening
intervals. All models keep their existing random-seed policy. Small daily changes
may reflect numerical Monte Carlo variation; do not interpret tiny wiggles as
politically meaningful shifts.

The history table includes both-party probabilities, expected/point seat counts,
the existing 70% seat interval, change in probability (percentage points) since the
previous evaluated cutoff, and the number of days between those points. A
30-day change and a 1-day change must not be compared as equal-duration changes.

## Caching, reports and audit

`scripts/live_forecast_report.py` supplies `run_history`, `history_figure`,
`recent_table` and `save_report`. `election_lab.prepare_live_evidence` prepares
cutoff inputs without inference. Model code/config/assets and actual prepared
inputs key the cutoff cache. New later polls need not invalidate an unchanged
earlier cutoff. A changed value, age, sample multiplicity, feature mode, model
setting or checkpoint invalidates the relevant cache. Cached artifacts and
manifests are verified before reuse; there is no silent fallback to a failed
Student fit. In case of interruption, completed individual cutoffs remain cached.

History artifacts save the parent live manifest, model hash, exact source run for
each cutoff, computation/cache status, coverage and convergence diagnostics.
Reports save the current live/history manifests and watchlist settings. Historical
inference artifacts are never overwritten when a new report is created.

Validation checks include the cutoff schedule, cache invalidation, future poll
field/release exclusion, future feature reference-period exclusion, chronological
training, both-party probability complements, no duplicate cutoff/model rows,
and equality of every model's current endpoint to the saved live forecast.
