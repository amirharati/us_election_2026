# Reproduction and validation guide

## Three distinct operations

1. **Frozen numerical reproduction** (`run.py reproduce`): recompute all 15 main
   Gaussian posteriors and original joint seat simulations, refit each retained
   non-Bayesian state bias with its earlier-cycle selected shrinkage, and translate
   means for the blend grid. Saved Student research output is verified and shown.
2. **Training reproduction** (`run.py train` and `run.py student`): reconstruct
   chronological prior means/training blocks and score normalizers; reproduce
   earlier-fold selections; refit covariance, feature coefficients, signed
   loadings and polling variance. Student runs actual converged MCMC. The training
   notebook does this for 2026; CLI flags expose all included historical folds.
3. **Live inference** (`run.py live`): acquire/prepare current evidence, recompute
   aggregates/feature scores and compute new forecasts using the frozen 2026
   model checkpoint, without overwriting it. This
   does not reselect hyperparameters every day or score unknown current labels.

## Chronology and weights

Historical test cycles are 2012–2024 at matched September and October 31 horizons;
2026 is forecast-only. There are 198 admitted historical contests per horizon,
140 in the recent 2016–2024 subset. Earlier outcome cycles contribute to fitting
where available. Some very early folds have insufficient prior evaluated cycles
for the non-Bayesian probability calibration, so probability counts are shown.

Prior centers always use earlier same-state outcomes. Training normalizers use
only training cycles. National features are shared across states, so states are
not independent extra observations of the national economic environment.

The bundled selection surfaces support exact recalculation of:

- feature-coefficient prior scale tau from previous three cycles' chamber CRPS;
- local/shared prior variance multipliers from previous three cycles' WIS;
- signed-factor lambda from previous three cycles' state WIS;
- non-Bayesian polling/bias settings chosen on the preceding cycle.

The **blend weights** are user-specified experiments. They are not learned on
2026 or automatically selected from the historical comparison. The finer grid is
5/10/20/30/40/50%; additional plain/corrected 70% comparisons are retained in the
overview. No time-varying blend schedule has been validated.

## Expected frozen checks

For the main Gaussian, recent 2016–2024:

| Horizon | Mean-cycle MAE, pp | Correct calls |
|---|---:|---:|
| September | 6.3067 | 128/140 |
| October 31 | 5.2060 | 132/140 |

The 50% corrected blend gives October MAE 4.9394 and 133/140 calls; September
MAE 6.5649 and 129/140 calls. Low September blend weights barely improve MAE while
worsening probability/chamber scores. Late gains are concentrated in 2020/2024;
no-poll cases can worsen even when the aggregate improves.

Frozen 2026 main:51 D/49 R point count,50.4262 expected D seats,48.27% D-control
probability and 49–52 D 70% range. Live forecasts can differ and are labeled with
their own cutoff. Control probabilities are simulation estimates, not exact
decimal constants; frozen paired seeds make reproduction deterministic.

## Automated checks

`python run.py audit` verifies bundled checksums, portable frozen inputs, all 15
chronological selections, and saved reproduction comparisons. Numerical tests
cover weight orientation, unchanged covariance, Student Gaussian control,
offline acquisition, explicit stale-cache failure handling and retention of
gasoline data in fallback caches.

Release validation now runs all ten notebooks and tests a copied folder under
an unrelated directory, with access to the original research tree forbidden by
an audit hook. That test checks frozen reproduction and cached live inference.
The snapshot/registry is local to this folder, with no symlink to the research lab.

## Deliberate limits

This is an educational research release, not a certified candidate-level election
forecast. Remaining limitations are recorded rather than hidden:

- Small number of independent national cycles and repeated architecture exploration.
- Empirical-Bayes covariance/hyperparameter uncertainty is not fully integrated.
- Latest-revised historical economic series and incomplete release-date vintages.
- D/R margin proxies for some independent-candidate contests; caucus/runoff/RCV
  assumptions affect seat interpretation.
- Historical chamber totals use explicit fixed completion for unmodeled contests.
- Missing-poll priors can be broad; blending may hurt those cases.
- The extraordinary-event flag is a threshold proxy, not a curated event catalog;
  it missed the intended 2008 case in the prior audit. It is not an active final
  national-feature coefficient in this two-score main model.
- Fat-tail helper architecture differs from the main model, so its comparison
  does not isolate distribution shape alone.
- Live political control is explicitly carried forward past its review date.
- Model calibration/normalizers remain fixed within2026. A different forecast
  horizon does not trigger a silent fresh historical architecture search.

## Sharing and package layout

Share the Git-tracked files in this project, including `data/compact/` and `assets/`.
This folder is the deliverable; no ZIP is needed. Do not copy just the notebooks:
they intentionally rely on this folder's scripts, config and audited input cache.
Install `requirements.txt` in a clean Python 3.11 environment. Exclude virtual
environments and Python/Numba caches. Preserve `PACKAGE_MANIFEST.json`, raw source
attribution and the data-policy documents.

`scripts/` contains inherited research modules as implementation dependencies;
some legacy `build()` routines mention unbundled old experiments. All supported
entry points are `run.py`, `election_lab.py` and the ten notebooks. Those
paths are tested independently of the original repo.

The package manifest protects immutable compact frozen inputs, code, configuration and documentation.
Mutable `data/compact/current/` is verified with its own manifest; ignored raw
archives are unnecessary for runtime verification. See [compact storage](GIT_STORAGE.md).
Mutable output runs, cache pointers and notebook execution outputs are excluded.
`NOTEBOOK_SOURCES.json` separately verifies notebook code and explanatory cells,
so rerunning and saving outputs does not invalidate the source audit. Deliberate
source edits require regenerating the corresponding release checksums.
