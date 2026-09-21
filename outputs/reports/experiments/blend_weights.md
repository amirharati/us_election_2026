# Blend-weight comparison

[Complete supporting results](../../results/experiments/blend_weights/) · [Run settings](../../results/experiments/blend_weights/run.json)

Latest execution: `20260921T044206.550359Z`. Forecast cutoff: **frozen historical/reference inputs**.

Margins are Democratic minus Republican percentage points. Experiments do not replace the active model or automatically select blend weights.

## Historical comparison

| Horizon           | Model                  |   Races |   Correct calls |   Margin MAE (pp) |   Brier score |
|:------------------|:-----------------------|--------:|----------------:|------------------:|--------------:|
| Matched September | Bayesian               |     140 |             128 |             6.307 |         0.055 |
| Matched September | Corrected 10%          |     140 |             129 |             6.286 |         0.056 |
| Matched September | Corrected 20%          |     140 |             129 |             6.277 |         0.056 |
| Matched September | Corrected 30%          |     140 |             129 |             6.336 |         0.057 |
| Matched September | Corrected 40%          |     140 |             129 |             6.437 |         0.057 |
| Matched September | Corrected 5%           |     140 |             129 |             6.296 |         0.056 |
| Matched September | Corrected 50%          |     140 |             129 |             6.565 |         0.059 |
| Matched September | Non-Bayesian corrected |     140 |             127 |             7.472 |         0.078 |
| October 31        | Bayesian               |     140 |             132 |             5.206 |         0.050 |
| October 31        | Corrected 10%          |     140 |             133 |             5.114 |         0.049 |
| October 31        | Corrected 20%          |     140 |             133 |             5.035 |         0.048 |
| October 31        | Corrected 30%          |     140 |             133 |             4.983 |         0.047 |
| October 31        | Corrected 40%          |     140 |             133 |             4.956 |         0.047 |
| October 31        | Corrected 5%           |     140 |             132 |             5.158 |         0.050 |
| October 31        | Corrected 50%          |     140 |             133 |             4.939 |         0.046 |
| October 31        | Non-Bayesian corrected |     140 |             133 |             5.220 |         0.037 |

## Chamber results

| Horizon           | Model                  |   D seats (mean winners) |   R seats (mean winners) |   Expected D seats |   D control % |   D seats: 70% low |   D seats: 70% high |
|:------------------|:-----------------------|-------------------------:|-------------------------:|-------------------:|--------------:|-------------------:|--------------------:|
| Matched September | Bayesian               |                       51 |                       49 |             50.426 |        48.270 |                 49 |                  52 |
| Matched September | Corrected 5%           |                       51 |                       49 |             50.364 |        46.723 |                 49 |                  52 |
| Matched September | Corrected 10%          |                       51 |                       49 |             50.300 |        44.980 |                 49 |                  52 |
| Matched September | Corrected 20%          |                       51 |                       49 |             50.166 |        41.833 |                 49 |                  52 |
| Matched September | Corrected 30%          |                       51 |                       49 |             50.024 |        38.773 |                 48 |                  52 |
| Matched September | Corrected 40%          |                       51 |                       49 |             49.874 |        35.637 |                 48 |                  52 |
| Matched September | Corrected 50%          |                       51 |                       49 |             49.717 |        32.617 |                 48 |                  51 |
| Matched September | Non-Bayesian corrected |                       49 |                       51 |             48.463 |        17.300 |                 46 |                  51 |

For all scenarios, per-state tables, sampler diagnostics and exact provenance, see the [complete result bundle](../../results/experiments/blend_weights/).
