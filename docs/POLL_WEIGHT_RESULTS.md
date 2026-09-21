# Poll-weight experiment results

Run: `cache/legacy_outputs/20260921T044037Z/poll_weights/20260920T224711.587511Z`. Current data as of September20,2026; no download was performed by the experiment. All comparisons use the saved live source and frozen historical cutoffs. The main model is unchanged.

## Historical2016–2024, bias re-estimated for each rule

| scenario     | variant                         |   correct |   n |   absolute_error_pp |   brier |
|:-------------|:--------------------------------|----------:|----:|--------------------:|--------:|
| matched_live | Equal polls, 30d                |       128 | 140 |              6.3302 |  0.0567 |
| matched_live | Equal polls, no decay           |       126 | 140 |              6.1165 |  0.0571 |
| matched_live | Firm + last-cycle rating mild   |       128 | 140 |              6.2998 |  0.0553 |
| matched_live | Firm + last-cycle rating strong |       128 | 140 |              6.2962 |  0.0553 |
| matched_live | Firm balanced (reference)       |       128 | 140 |              6.3067 |  0.0555 |
| matched_live | Firm balanced + within-firm n   |       128 | 140 |              6.3043 |  0.0554 |
| matched_live | Respondent n, 30d               |       128 | 140 |              6.3378 |  0.0575 |
| oct31        | Equal polls, 30d                |       131 | 140 |              5.2146 |  0.0509 |
| oct31        | Equal polls, no decay           |       130 | 140 |              5.1378 |  0.0514 |
| oct31        | Firm + last-cycle rating mild   |       132 | 140 |              5.2273 |  0.0507 |
| oct31        | Firm + last-cycle rating strong |       132 | 140 |              5.2497 |  0.0509 |
| oct31        | Firm balanced (reference)       |       132 | 140 |              5.206  |  0.0504 |
| oct31        | Firm balanced + within-firm n   |       132 | 140 |              5.2095 |  0.0504 |
| oct31        | Respondent n, 30d               |       131 | 140 |              5.2356 |  0.0515 |

Five cycles and140 modeled contests per horizon. Correct counts pool contests; MAE and Brier average cycle means. Full2012–2024 cycle tables and the frozen-bias arm are in notebook09.

Equal polls and respondent-count weighting do not improve the full Gaussian consistently. Within-firm respondent weighting barely changes results. Last-cycle ratings slightly improve September MAE but worsen October MAE. Literal equal/no-decay weighting lowers margin MAE at both horizons, yet reduces correct calls from128 to126 in September and132 to130 in October. Accuracy and numerical margin error therefore give different answers; this does not establish a uniformly better rule.

## Current forecast with refitted historical bias

| variant                         |   point_D |   expected_D |   D_lo70 |   D_hi70 |   D control % |
|:--------------------------------|----------:|-------------:|---------:|---------:|--------------:|
| Firm balanced (reference)       |        51 |       50.321 |       49 |       52 |        45.513 |
| Equal polls, 30d                |        51 |       50.364 |       49 |       52 |        46.58  |
| Respondent n, 30d               |        51 |       50.391 |       49 |       52 |        47.33  |
| Firm balanced + within-firm n   |        51 |       50.309 |       49 |       52 |        45.24  |
| Firm + last-cycle rating mild   |        51 |       50.305 |       49 |       52 |        45.07  |
| Firm + last-cycle rating strong |        50 |       50.29  |       49 |       52 |        44.657 |
| Equal polls, no decay           |        50 |       50.042 |       48 |       52 |        37.823 |

The strong rating and no-decay cases change the point count from51 to50 because Texas crosses an extremely narrow zero-margin boundary: reference D+0.064 pp, strong rating R+0.010 pp, no decay R+0.016 pp. This is a near-tie, not a confident reversal. Respondent weighting raises expected D seats by about0.07 and control probability by about1.8 percentage points relative to the reference.

Current evidence contains 233 admitted samples from 76 firms; 0 samples have missing/invalid n filled under the documented earlier-cycle rule. 16 firms have eligible prior-cycle comparative rating evidence; 60 retain neutral weight1. The default matters because names/coverage are sparse across Senate cycles.

## Scope and checks

This is a **fixed-variance Gaussian sensitivity**, not full retuning under alternative sampling models. Historical bias is either held fixed or re-estimated, but priors, polling variance budgets and original decayed firm precision remain fixed. The entire posterior margin covariance is checked unchanged. Ratings use only the immediately preceding cycle; missing rating history does not exclude a firm. No current labels are used.

The notebook executed all six code cells. All14 package tests passed, including missing-n handling, relative respondent weights, firm balance, recency and previous-cycle-only rating tests. All224 case/variant/calibration controls pass, including reference reproduction and covariance preservation. See POLL_WEIGHT_EXPERIMENT.md for equations, leakage boundaries and limitations.
