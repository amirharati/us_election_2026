# All-model comparison and mixtures

[Complete supporting results](../../results/experiments/portfolio/) · [Run settings](../../results/experiments/portfolio/run.json)

Latest execution: `20260921T185943.532983Z`. Forecast cutoff: **frozen historical/reference inputs**.

Margins are Democratic minus Republican percentage points. Experiments do not replace the active model or automatically select blend weights.

## Historical comparison

| Horizon           | Model                     |   Races |   Correct calls |   Margin MAE (pp) |   Brier score |
|:------------------|:--------------------------|--------:|----------------:|------------------:|--------------:|
| Matched September | Gaussian Bayesian         |     140 |             128 |             6.307 |         0.055 |
| Matched September | Four-model mixture        |     140 |             129 |             6.512 |         0.056 |
| Matched September | Matched Student-t (df5)   |     140 |             129 |             6.344 |         0.055 |
| Matched September | Mixture + polling 10%     |     140 |             129 |             6.498 |         0.056 |
| Matched September | Mixture + polling 20%     |     140 |             129 |             6.512 |         0.057 |
| Matched September | Mixture + polling 30%     |     140 |             129 |             6.567 |         0.057 |
| Matched September | Mixture + polling 40%     |     140 |             129 |             6.638 |         0.058 |
| Matched September | Mixture + polling 5%      |     140 |             129 |             6.501 |         0.056 |
| Matched September | Mixture + polling 50%     |     140 |             128 |             6.721 |         0.059 |
| Matched September | Non-Bayesian corrected    |     140 |             127 |             7.472 |         0.078 |
| Matched September | Older Gaussian            |     140 |             129 |             6.808 |         0.059 |
| Matched September | Student-t research helper |     140 |             129 |             6.801 |         0.058 |
| October 31        | Gaussian Bayesian         |     140 |             132 |             5.206 |         0.050 |
| October 31        | Four-model mixture        |     140 |             132 |             5.275 |         0.050 |
| October 31        | Matched Student-t (df5)   |     140 |             132 |             5.224 |         0.049 |
| October 31        | Mixture + polling 10%     |     140 |             133 |             5.180 |         0.048 |
| October 31        | Mixture + polling 20%     |     140 |             133 |             5.097 |         0.047 |
| October 31        | Mixture + polling 30%     |     140 |             133 |             5.058 |         0.046 |
| October 31        | Mixture + polling 40%     |     140 |             133 |             5.022 |         0.046 |
| October 31        | Mixture + polling 5%      |     140 |             132 |             5.227 |         0.049 |
| October 31        | Mixture + polling 50%     |     140 |             133 |             4.990 |         0.045 |
| October 31        | Non-Bayesian corrected    |     140 |             133 |             5.220 |         0.037 |
| October 31        | Older Gaussian            |     140 |             133 |             5.344 |         0.050 |
| October 31        | Student-t research helper |     140 |             131 |             5.357 |         0.049 |

## Chamber results

| Horizon           | Model                     |   D seats (mean winners) |   R seats (mean winners) |   Expected D seats |   D control % |   D seats: 70% low |   D seats: 70% high |
|:------------------|:--------------------------|-------------------------:|-------------------------:|-------------------:|--------------:|-------------------:|--------------------:|
| Matched September | Gaussian Bayesian         |                       51 |                       49 |             50.320 |        45.520 |             49.000 |              52.000 |
| Matched September | Non-Bayesian corrected    |                       48 |                       52 |             48.373 |        16.354 |             46.000 |              51.000 |
| Matched September | Older Gaussian            |                       50 |                       50 |             51.090 |        61.997 |             49.000 |              53.000 |
| Matched September | Student-t research helper |                       50 |                       50 |             51.115 |        63.006 |             49.000 |              53.000 |
| Matched September | Matched Student-t (df5)   |                       51 |                       49 |             50.476 |        50.028 |             49.000 |              52.000 |
| Matched September | Four-model mixture        |                       50 |                       50 |             50.748 |        55.138 |             49.000 |              53.000 |
| Matched September | Mixture + polling 5%      |                       50 |                       50 |             50.669 |        53.236 |             49.000 |              52.000 |
| Matched September | Mixture + polling 10%     |                       50 |                       50 |             50.589 |        51.313 |             49.000 |              52.000 |
| Matched September | Mixture + polling 20%     |                       50 |                       50 |             50.419 |        47.381 |             49.000 |              52.000 |
| Matched September | Mixture + polling 30%     |                       51 |                       49 |             50.243 |        43.563 |             48.000 |              52.000 |
| Matched September | Mixture + polling 40%     |                       51 |                       49 |             50.058 |        39.824 |             48.000 |              52.000 |
| Matched September | Mixture + polling 50%     |                       50 |                       50 |             49.866 |        35.955 |             48.000 |              52.000 |

For all scenarios, per-state tables, sampler diagnostics and exact provenance, see the [complete result bundle](../../results/experiments/portfolio/).
