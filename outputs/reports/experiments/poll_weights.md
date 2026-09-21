# Poll-weight experiments

[Complete supporting results](../../results/experiments/poll_weights/) · [Run settings](../../results/experiments/poll_weights/run.json)

Latest execution: `20260921T044728.506084Z`. Forecast cutoff: **2026-09-21**.

Margins are Democratic minus Republican percentage points. Experiments do not replace the active model or automatically select blend weights.

## Historical comparison

| Horizon           | Model                                        | Poll weighting                  |   Races |   Correct calls |   Margin MAE (pp) |   Brier score |
|:------------------|:---------------------------------------------|:--------------------------------|--------:|----------------:|------------------:|--------------:|
| Matched September | Equal polls, 30d | Refit bias                | Equal polls, 30d                |     140 |             128 |             6.330 |         0.057 |
| Matched September | Equal polls, no decay | Refit bias           | Equal polls, no decay           |     140 |             126 |             6.117 |         0.057 |
| Matched September | Firm + last-cycle rating mild | Refit bias   | Firm + last-cycle rating mild   |     140 |             128 |             6.300 |         0.055 |
| Matched September | Firm + last-cycle rating strong | Refit bias | Firm + last-cycle rating strong |     140 |             128 |             6.296 |         0.055 |
| Matched September | Firm balanced (reference) | Refit bias       | Firm balanced (reference)       |     140 |             128 |             6.307 |         0.055 |
| Matched September | Firm balanced + within-firm n | Refit bias   | Firm balanced + within-firm n   |     140 |             128 |             6.304 |         0.055 |
| Matched September | Respondent n, 30d | Refit bias               | Respondent n, 30d               |     140 |             128 |             6.338 |         0.058 |
| October 31        | Equal polls, 30d | Refit bias                | Equal polls, 30d                |     140 |             131 |             5.215 |         0.051 |
| October 31        | Equal polls, no decay | Refit bias           | Equal polls, no decay           |     140 |             130 |             5.138 |         0.051 |
| October 31        | Firm + last-cycle rating mild | Refit bias   | Firm + last-cycle rating mild   |     140 |             132 |             5.227 |         0.051 |
| October 31        | Firm + last-cycle rating strong | Refit bias | Firm + last-cycle rating strong |     140 |             132 |             5.250 |         0.051 |
| October 31        | Firm balanced (reference) | Refit bias       | Firm balanced (reference)       |     140 |             132 |             5.206 |         0.050 |
| October 31        | Firm balanced + within-firm n | Refit bias   | Firm balanced + within-firm n   |     140 |             132 |             5.210 |         0.050 |
| October 31        | Respondent n, 30d | Refit bias               | Respondent n, 30d               |     140 |             131 |             5.236 |         0.052 |

## Chamber results

| Horizon           | Model                                        | Poll weighting                  |   D seats (mean winners) |   R seats (mean winners) |   Expected D seats |   D control % |   D seats: 70% low |   D seats: 70% high |
|:------------------|:---------------------------------------------|:--------------------------------|-------------------------:|-------------------------:|-------------------:|--------------:|-------------------:|--------------------:|
| Matched September | Firm balanced (reference) | Refit bias       | Firm balanced (reference)       |                       51 |                       49 |             50.320 |        45.520 |                 49 |                  52 |
| Matched September | Equal polls, 30d | Refit bias                | Equal polls, 30d                |                       51 |                       49 |             50.363 |        46.547 |                 49 |                  52 |
| Matched September | Respondent n, 30d | Refit bias               | Respondent n, 30d               |                       51 |                       49 |             50.390 |        47.313 |                 49 |                  52 |
| Matched September | Firm balanced + within-firm n | Refit bias   | Firm balanced + within-firm n   |                       51 |                       49 |             50.308 |        45.217 |                 49 |                  52 |
| Matched September | Firm + last-cycle rating mild | Refit bias   | Firm + last-cycle rating mild   |                       51 |                       49 |             50.304 |        45.040 |                 49 |                  52 |
| Matched September | Firm + last-cycle rating strong | Refit bias | Firm + last-cycle rating strong |                       50 |                       50 |             50.289 |        44.643 |                 49 |                  52 |
| Matched September | Equal polls, no decay | Refit bias           | Equal polls, no decay           |                       50 |                       50 |             50.041 |        37.813 |                 48 |                  52 |

For all scenarios, per-state tables, sampler diagnostics and exact provenance, see the [complete result bundle](../../results/experiments/poll_weights/).
