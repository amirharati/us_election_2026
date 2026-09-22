Archived execution date (UTC): **2026-09-21**. Run: `20260921T190036.192117Z`. Same-day reruns replace this copy; other dates are retained.

# Older model alternatives

Complete supporting results · [Run settings](supporting_run.json)

Latest execution: `20260921T190036.192117Z`. Forecast cutoff: **frozen historical/reference inputs**.

Margins are Democratic minus Republican percentage points. Experiments do not replace the active model or automatically select blend weights.

## Historical comparison

| Horizon           | Model                     |   Races |   Correct calls |   Margin MAE (pp) |   Brier score |
|:------------------|:--------------------------|--------:|----------------:|------------------:|--------------:|
| Matched September | Gaussian Bayesian         |     140 |             128 |             6.307 |         0.055 |
| Matched September | Older Gaussian            |     140 |             129 |             6.808 |         0.059 |
| Matched September | Student-t research helper |     140 |             129 |             6.801 |         0.058 |
| October 31        | Gaussian Bayesian         |     140 |             132 |             5.206 |         0.050 |
| October 31        | Older Gaussian            |     140 |             133 |             5.344 |         0.050 |
| October 31        | Student-t research helper |     140 |             131 |             5.357 |         0.049 |

## Chamber results

| Horizon           | Model                     |   D seats (mean winners) |   R seats (mean winners) |   Expected D seats |   D control % |   D seats: 70% low |   D seats: 70% high |
|:------------------|:--------------------------|-------------------------:|-------------------------:|-------------------:|--------------:|-------------------:|--------------------:|
| Matched September | Gaussian Bayesian         |                       51 |                       49 |             50.320 |        45.520 |             49.000 |              52.000 |
| Matched September | Older Gaussian            |                       50 |                       50 |             51.090 |        61.997 |             49.000 |              53.000 |
| Matched September | Student-t research helper |                       50 |                       50 |             51.115 |        63.006 |             49.000 |              53.000 |

For all scenarios, per-state tables, sampler diagnostics and exact provenance, see the complete result bundle.
