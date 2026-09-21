# Final uncertainty review — results

Executed on frozen September 17, 2026 inputs. No new polling, model selection, weight search or promotion. The reference here is `repaired_both__selected`; the 50/50 mean-only polling blend inherits its covariance. The older formally designated `no_U_K1` is preserved and explicitly distinguished in the model contract.

## Main findings

1. **Missing-poll behavior is conservative, not overconfident in this test.** Hiding historical current-cycle polls worsens accuracy while widening intervals. One recently available firm recovers much of the accuracy. Masking is not random natural missingness, and this does not prove every no-poll prior is well centered.
2. **The disruption flag is not an adequate indicator of known extraordinary events.** All five recent cycles are flagged. Across 1998–2024, only 2008 and 2014 are unflagged; 2008's financial crisis is missed at these cutoffs by the strict monthly-threshold/completed-month construction. No causal or crisis-specific fat-tail conclusion is supported by this flag.
3. **Shared forecast misses and isolated large misses both occur.** In 2020 and 2024, roughly85–89% of admitted states miss in the same direction. September2022 has two standardized errors beyond3SD (Vermont and South Dakota); both winner calls are correct. These are errors relative to our forecasts, not proof of a wave relative to the preceding election, or proof of an event cause. A biased mean or too-small shared covariance can also explain coherent misses.
4. **Where more information helps depends on the model.** At the fixed effective-error benchmark, Bayesian ranking starts Alaska/Ohio/Iowa/Texas; the mean-only blend starts Colorado/West Virginia/Alaska/Iowa. The latter two unpolled-state priorities expose prior/fallback sensitivity. Close ranking differences are not precise distinctions.
5. **Four candidate-proxy cases remain unresolved.** Idaho, Montana, Nebraska and South Dakota lack validated local independent-candidate distributions. Allocation bounds quantify their effect; they are not estimates of those candidates' election chances.

## Fixed current forecasts

Expected seats use exact marginals; control and ranges use the original30,000 paired joint draws. D needs51, R controls a50–50 tie under the saved ledger convention. These numbers retain the stated candidate-proxy assumptions.

| scenario     |   cycle | model           |   point_D |   expected_D |   actual_D |   p_D_at_least_51 |   D_lo70 |   D_hi70 |   expected_seat_absolute_error |   seat_crps | coverage70   |   unmodeled_contested |
|:-------------|--------:|:----------------|----------:|-------------:|-----------:|------------------:|---------:|---------:|-------------------------------:|------------:|:-------------|----------------------:|
| matched_live |    2026 | Gaussian Bayesian        |        51 |      50.4262 |        nan |            0.4827 |       49 |       52 |                            nan |         nan |              |                     0 |
| matched_live |    2026 | Mean-only blend |        52 |      50.7967 |        nan |            0.574  |       49 |       53 |                            nan |         nan |              |                     0 |

## Historical reference comparison, 2016–2024

140 contests per horizon. Error metrics average cycles equally; counts/correct calls pool contests. `matched_live` is September17; `oct31` is October31. Positive margin means D−R; Brier and MAE are lower-is-better. Widths are percentage points. The mean-only blend does not beat Bayesian alone on these scores.

| scenario     | model           |   mae_pp |   brier |   coverage70 |   width70_pp |   coverage95 |   width95_pp |   n |   cycles |   correct |
|:-------------|:----------------|---------:|--------:|-------------:|-------------:|-------------:|-------------:|----:|---------:|----------:|
| matched_live | Gaussian Bayesian        |   6.3067 |  0.0555 |       0.7821 |      19.8764 |       0.9395 |      37.5876 | 140 |        5 |       128 |
| matched_live | Mean-only blend |   6.9263 |  0.0628 |       0.7463 |      19.8764 |       0.9472 |      37.5876 | 140 |        5 |       126 |
| oct31        | Gaussian Bayesian        |   5.206  |  0.0504 |       0.7317 |      15.7997 |       0.9419 |      29.8782 | 140 |        5 |       132 |
| oct31        | Mean-only blend |   5.5174 |  0.0526 |       0.7105 |      15.7997 |       0.9342 |      29.8782 | 140 |        5 |       130 |

## Masking historical state polls

Same originally polled targets in all three rows per model/horizon:102 earlier and125 late contests over2016–2024. Each masking case removes or thins one state at a time, retains other states, and redoes the Bayesian update from its prior. Prior/historical parameter fits are fixed. The plain component uses its original historical-prior fallback when masked, never its hidden polled forecast. One firm means all eligible samples from the most recently available firm; selection uses receipt/field dates and a fixed alphabetical tie rule, not outcomes. Existing unknown-publication-date proxies are retained. National features are momentum/approval, with no hidden state-poll dependency.

| scenario     | model           | mask     |   mae_pp |   brier |   coverage70 |   width70_pp |   coverage95 |   width95_pp |   n |   cycles |   correct |
|:-------------|:----------------|:---------|---------:|--------:|-------------:|-------------:|-------------:|-------------:|----:|---------:|----------:|
| matched_live | Gaussian Bayesian        | full     |   5.3271 |  0.0716 |       0.7716 |      14.5101 |       0.94   |      27.4396 | 102 |        5 |        93 |
| matched_live | Gaussian Bayesian        | no_polls |   6.9765 |  0.1021 |       0.9011 |      30.7503 |       0.9813 |      58.1509 | 102 |        5 |        89 |
| matched_live | Gaussian Bayesian        | one_firm |   5.5723 |  0.0762 |       0.7649 |      15.4202 |       0.95   |      29.1607 | 102 |        5 |        92 |
| matched_live | Mean-only blend | full     |   5.6085 |  0.0764 |       0.7344 |      14.5101 |       0.95   |      27.4396 | 102 |        5 |        90 |
| matched_live | Mean-only blend | no_polls |   7.3665 |  0.109  |       0.8639 |      30.7503 |       0.9913 |      58.1509 | 102 |        5 |        89 |
| matched_live | Mean-only blend | one_firm |   5.9973 |  0.0795 |       0.6876 |      15.4202 |       0.9513 |      29.1607 | 102 |        5 |        90 |
| oct31        | Gaussian Bayesian        | full     |   5.2399 |  0.0563 |       0.6883 |      13.1044 |       0.9311 |      24.7812 | 125 |        5 |       117 |
| oct31        | Gaussian Bayesian        | no_polls |   7.9208 |  0.0955 |       0.9094 |      36.8107 |       0.9909 |      69.6115 | 125 |        5 |       107 |
| oct31        | Gaussian Bayesian        | one_firm |   5.4378 |  0.0627 |       0.7169 |      14.8421 |       0.9659 |      28.0673 | 125 |        5 |       113 |
| oct31        | Mean-only blend | full     |   5.4322 |  0.0574 |       0.6747 |      13.1044 |       0.922  |      24.7812 | 125 |        5 |       115 |
| oct31        | Mean-only blend | no_polls |   8.4608 |  0.1034 |       0.889  |      36.8107 |       1      |      69.6115 | 125 |        5 |       109 |
| oct31        | Mean-only blend | one_firm |   5.728  |  0.0649 |       0.6775 |      14.8421 |       0.9568 |      28.0673 | 125 |        5 |       113 |

Naturally unpolled contests are a separate, small population (38 earlier/15 late). Their results must not be interpreted as a randomized masking experiment.

| scenario     | model           |   mae_pp |   brier |   coverage70 |   width70_pp |   coverage95 |   width95_pp |   n |   cycles |   correct |
|:-------------|:----------------|---------:|--------:|-------------:|-------------:|-------------:|-------------:|----:|---------:|----------:|
| matched_live | Gaussian Bayesian        |   8.3923 |  0.0219 |       0.7283 |      30.5222 |       0.9653 |      57.7194 |  38 |        5 |        35 |
| matched_live | Mean-only blend |   9.2672 |  0.0305 |       0.755  |      30.5222 |       0.9653 |      57.7194 |  38 |        5 |        36 |
| oct31        | Gaussian Bayesian        |   6.2029 |  0.0073 |       1      |      35.1439 |       1      |      66.4594 |  15 |        5 |        15 |
| oct31        | Mean-only blend |   7.1883 |  0.0147 |       0.8    |      35.1439 |       1      |      66.4594 |  15 |        5 |        15 |

## Event support and source limitation

The OR flag uses elevated health-news/VIX/GPR proxies above a past120-month95th percentile, requiring60 prior values, with January(cycle−4) through the last closed month. This is the existing inclusive calendar-year convention, not a strict48-month interval. Unknown components remain unknown unless another component is1. Historical reference vintages are not certified as available in real time.

| scenario     |   cycle |   health_disruption_4y |   financial_disruption_4y |   security_disruption_4y |   extraordinary_event_any_4y |   vix_3m |   gpr_3m |   admitted_contests |   polled_contests |   actual_outcomes | event_status   |   known_components | vintage_status                                                             | window_definition                                                                      |
|:-------------|--------:|-----------------------:|--------------------------:|-------------------------:|-----------------------------:|---------:|---------:|--------------------:|------------------:|------------------:|:---------------|-------------------:|:---------------------------------------------------------------------------|:---------------------------------------------------------------------------------------|
| matched_live |    1998 |                      1 |                         1 |                        0 |                            1 |   24.394 |   60.026 |                  31 |                10 |                31 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2000 |                      1 |                         1 |                        0 |                            1 |   19.841 |   40.729 |                  31 |                21 |                31 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2002 |                      1 |                         1 |                        1 |                            1 |   31.021 |   95.536 |                  24 |                12 |                24 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2004 |                      1 |                         1 |                        1 |                            1 |   15.843 |  122.535 |                  30 |                17 |                30 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2006 |                      1 |                         1 |                        1 |                            1 |   15.199 |   98.853 |                  30 |                16 |                30 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2008 |                      0 |                         0 |                        0 |                            0 |   22.376 |   74.908 |                  28 |                16 |                28 | unflagged      |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2010 |                      1 |                         1 |                        0 |                            1 |   26.743 |   78.814 |                  27 |                19 |                27 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2012 |                      1 |                         1 |                        0 |                            1 |   18.129 |   65.992 |                  31 |                19 |                31 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2014 |                      0 |                         0 |                        0 |                            0 |   12.443 |   94.321 |                  27 |                15 |                27 | unflagged      |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2016 |                      1 |                         0 |                        1 |                            1 |   14.444 |   81.434 |                  29 |                13 |                29 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2018 |                      1 |                         0 |                        1 |                            1 |   13.124 |   73.28  |                  30 |                28 |                30 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2020 |                      1 |                         1 |                        1 |                            1 |   26.95  |   60.702 |                  27 |                18 |                27 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2022 |                      1 |                         1 |                        1 |                            1 |   25.133 |  105.733 |                  26 |                20 |                26 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2024 |                      1 |                         1 |                        1 |                            1 |   15.451 |   87.973 |                  28 |                23 |                28 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| matched_live |    2026 |                      0 |                         1 |                        1 |                            1 |   16.742 |  146.762 |                  35 |                21 |                 0 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    1998 |                      1 |                         1 |                        0 |                            1 |   29.908 |   57.359 |                  31 |                27 |                31 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    2000 |                      1 |                         1 |                        0 |                            1 |   19.223 |   38.949 |                  31 |                28 |                31 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    2002 |                      1 |                         1 |                        1 |                            1 |   35.196 |   96.775 |                  24 |                22 |                24 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    2004 |                      1 |                         1 |                        1 |                            1 |   15.422 |  125.12  |                  30 |                24 |                30 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    2006 |                      1 |                         1 |                        1 |                            1 |   13.621 |  104.245 |                  30 |                22 |                30 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    2008 |                      0 |                         0 |                        0 |                            0 |   25.085 |   77.381 |                  28 |                28 |                28 | unflagged      |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    2010 |                      1 |                         1 |                        0 |                            1 |   24.276 |   67.979 |                  27 |                25 |                27 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    2012 |                      1 |                         1 |                        0 |                            1 |   16.18  |   65.847 |                  31 |                23 |                31 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    2014 |                      0 |                         0 |                        0 |                            0 |   13.085 |  101.587 |                  27 |                24 |                27 | unflagged      |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    2016 |                      1 |                         0 |                        1 |                            1 |   13.259 |   88.038 |                  29 |                24 |                29 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    2018 |                      1 |                         0 |                        1 |                            1 |   12.868 |   64.791 |                  30 |                28 |                30 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    2020 |                      1 |                         1 |                        1 |                            1 |   25.793 |   58.926 |                  27 |                24 |                27 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    2022 |                      1 |                         1 |                        1 |                            1 |   24.836 |  110.028 |                  26 |                22 |                26 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |
| oct31        |    2024 |                      1 |                         1 |                        1 |                            1 |   17.117 |   90.949 |                  28 |                27 |                28 | flagged        |                  3 | Reference-vintage proxies; historical real-time availability not certified | January of cycle-4 through last closed month; fixed rolling95th-percentile proxy flags |

In2008, September VIX monthly mean30.24 was below its33.76 threshold. October mean61.18 exceeded32.77, but October is not a completed reference month at the October31 forecast cutoff. The stored2008 flag therefore remains0. This is a definition/timing limitation, not proof that2008 was an ordinary election environment. Existing event flags were not changed after seeing errors.


## Cycle-level surprise patterns

Errors are actual minus forecast. Negative signed errors mean outcomes were more Republican than our forecast. Standardization uses the original forecast SD. Simulation reference bands use the same joint covariance and admitted states for each cycle. They are exploratory diagnostics, not multiple-testing-adjusted significance results.

|                        |   fraction_abs_z_gt2 |   fraction_abs_z_gt3 |   mean_error_pp |   median_abs_z |   same_direction_fraction |
|:-----------------------|---------------------:|---------------------:|----------------:|---------------:|--------------------------:|
| ('matched_live', 2016) |               0.0345 |               0      |         -4.0894 |         0.3507 |                    0.7241 |
| ('matched_live', 2018) |               0      |               0      |         -0.6824 |         0.4073 |                    0.5333 |
| ('matched_live', 2020) |               0.037  |               0      |         -7.0541 |         0.6739 |                    0.8519 |
| ('matched_live', 2022) |               0.1923 |               0.0769 |         -2.9042 |         0.4793 |                    0.6923 |
| ('matched_live', 2024) |               0      |               0      |         -3.5602 |         0.6949 |                    0.8929 |
| ('oct31', 2016)        |               0.1379 |               0      |         -4.4569 |         0.8377 |                    0.7931 |
| ('oct31', 2018)        |               0      |               0      |          0.6171 |         0.4127 |                    0.5667 |
| ('oct31', 2020)        |               0.037  |               0      |         -6.0652 |         0.9082 |                    0.8889 |
| ('oct31', 2022)        |               0.1154 |               0      |         -1.8949 |         0.7703 |                    0.6154 |
| ('oct31', 2024)        |               0      |               0      |         -3.6382 |         0.5724 |                    0.8929 |

VIX has a positive descriptive association with typical standardized error, particularly at October31; geopolitical risk has no consistent direction across models/horizons. Only5 recent or7 full backtest cycles support these correlations. Omission ranges show instability. They do not establish a causal event effect or justify new feature weights.

|   first_cycle | scenario     | model    | proxy   | outcome                 |   omitted_cycle |   n |   pearson_r |   omit_one_min |   omit_one_max |
|--------------:|:-------------|:---------|:--------|:------------------------|----------------:|----:|------------:|---------------:|---------------:|
|          2012 | matched_live | Gaussian Bayesian | vix_3m  | median_abs_z            |             nan |   7 |      0.3264 |         0.0249 |         0.5276 |
|          2012 | matched_live | Gaussian Bayesian | vix_3m  | same_direction_fraction |             nan |   7 |      0.4347 |         0.1545 |         0.7342 |
|          2012 | matched_live | Gaussian Bayesian | gpr_3m  | median_abs_z            |             nan |   7 |     -0.1926 |        -0.346  |         0.0923 |
|          2012 | matched_live | Gaussian Bayesian | gpr_3m  | same_direction_fraction |             nan |   7 |     -0.0634 |        -0.2608 |         0.3058 |
|          2012 | oct31        | Gaussian Bayesian | vix_3m  | median_abs_z            |             nan |   7 |      0.6366 |         0.3988 |         0.9331 |
|          2012 | oct31        | Gaussian Bayesian | vix_3m  | same_direction_fraction |             nan |   7 |      0.1887 |        -0.1874 |         0.6577 |
|          2012 | oct31        | Gaussian Bayesian | gpr_3m  | median_abs_z            |             nan |   7 |      0.1128 |        -0.165  |         0.6462 |
|          2012 | oct31        | Gaussian Bayesian | gpr_3m  | same_direction_fraction |             nan |   7 |     -0.1928 |        -0.6614 |         0.1428 |

Older raw-poll error comparisons are saved separately in `raw_poll_error_cycles.parquet`; they are not additional model-backtest folds.


## Candidate/caucus sensitivity

The100-seat ledger and35 current physical contests reconcile; candidate identity and caucus interpretation are different checks. The exception table uses already captured public source evidence, not a fresh candidate certification. None of these four proxies supplies a validated candidate-specific probability. The bounds below remove the model allocation for the named seat(s), set them to D or R, and leave the other simulated races unchanged. This is neither conditioning on a surprising win nor assuming a national wave. Extreme all-four allocations are logical bounds, not plausible-scenario probabilities. Expected seats here are Monte Carlo means and can differ slightly from exact marginal sums.

| state   | candidates                                    | source_url                                                                                         | updated                   | comparison_note                                                                                     | distribution_status                                                            |
|:--------|:----------------------------------------------|:---------------------------------------------------------------------------------------------------|:--------------------------|:----------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------|
| ID      | {"R": ["Jim Risch"], "I": ["Todd Achilles"]}  | https://votes.decisiondeskhq.com/races/2026-11-03/idaho-us-senate-general-election/forecast        | 2026-09-18 14:40:49.01501 | Independent/ballot proxy: D-vs-R model output is not a literal Democratic candidate win probability | No validated local candidate-specific distribution; use allocation bounds only |
| MT      | {"R": ["Kurt Alme"], "I": ["Seth Bodnar"]}    | https://votes.decisiondeskhq.com/races/2026-11-03/montana-us-senate-general-election/forecast      | 2026-09-18 14:40:49.01501 | Independent/ballot proxy: D-vs-R model output is not a literal Democratic candidate win probability | No validated local candidate-specific distribution; use allocation bounds only |
| NE      | {"R": ["Pete Ricketts"], "I": ["Dan Osborn"]} | https://votes.decisiondeskhq.com/races/2026-11-03/nebraska-us-senate-general-election/forecast     | 2026-09-18 14:40:49.01501 | Independent/ballot proxy: D-vs-R model output is not a literal Democratic candidate win probability | No validated local candidate-specific distribution; use allocation bounds only |
| SD      | {"R": ["Mike Rounds"], "I": ["Brian Bengs"]}  | https://votes.decisiondeskhq.com/races/2026-11-03/south-dakota-us-senate-general-election/forecast | 2026-09-18 14:40:49.01501 | Independent/ballot proxy: D-vs-R model output is not a literal Democratic candidate win probability | No validated local candidate-specific distribution; use allocation bounds only |

| model           | affected_states   |   allocated_D |   expected_D |   p_D_control |   D_lo70 |   D_hi70 |   baseline_expected_D |   baseline_p_D_control | interpretation                                                           |
|:----------------|:------------------|--------------:|-------------:|--------------:|---------:|---------:|----------------------:|-----------------------:|:-------------------------------------------------------------------------|
| Gaussian Bayesian        | ID                |             0 |      50.4151 |        0.4827 |       49 |       52 |               50.4153 |                 0.4827 | Allocation-only bound; other races held fixed, not conditioning on a win |
| Gaussian Bayesian        | ID                |             1 |      51.4151 |        0.7345 |       50 |       53 |               50.4153 |                 0.4827 | Allocation-only bound; other races held fixed, not conditioning on a win |
| Gaussian Bayesian        | MT                |             0 |      50.4114 |        0.4818 |       49 |       52 |               50.4153 |                 0.4827 | Allocation-only bound; other races held fixed, not conditioning on a win |
| Gaussian Bayesian        | MT                |             1 |      51.4114 |        0.7339 |       50 |       53 |               50.4153 |                 0.4827 | Allocation-only bound; other races held fixed, not conditioning on a win |
| Gaussian Bayesian        | NE                |             0 |      50.3805 |        0.4743 |       49 |       52 |               50.4153 |                 0.4827 | Allocation-only bound; other races held fixed, not conditioning on a win |
| Gaussian Bayesian        | NE                |             1 |      51.3805 |        0.7293 |       50 |       53 |               50.4153 |                 0.4827 | Allocation-only bound; other races held fixed, not conditioning on a win |
| Gaussian Bayesian        | SD                |             0 |      50.415  |        0.4827 |       49 |       52 |               50.4153 |                 0.4827 | Allocation-only bound; other races held fixed, not conditioning on a win |
| Gaussian Bayesian        | SD                |             1 |      51.415  |        0.7345 |       50 |       53 |               50.4153 |                 0.4827 | Allocation-only bound; other races held fixed, not conditioning on a win |
| Gaussian Bayesian        | ID,MT,NE,SD       |             0 |      50.3761 |        0.4733 |       49 |       52 |               50.4153 |                 0.4827 | Allocation-only bound; other races held fixed, not conditioning on a win |
| Gaussian Bayesian        | ID,MT,NE,SD       |             4 |      54.3761 |        0.9936 |       53 |       56 |               50.4153 |                 0.4827 | Allocation-only bound; other races held fixed, not conditioning on a win |
| Mean-only blend | ID                |             0 |      50.7954 |        0.574  |       49 |       53 |               50.7955 |                 0.574  | Allocation-only bound; other races held fixed, not conditioning on a win |
| Mean-only blend | ID                |             1 |      51.7954 |        0.7745 |       50 |       54 |               50.7955 |                 0.574  | Allocation-only bound; other races held fixed, not conditioning on a win |
| Mean-only blend | MT                |             0 |      50.7938 |        0.5739 |       49 |       53 |               50.7955 |                 0.574  | Allocation-only bound; other races held fixed, not conditioning on a win |
| Mean-only blend | MT                |             1 |      51.7938 |        0.7743 |       50 |       54 |               50.7955 |                 0.574  | Allocation-only bound; other races held fixed, not conditioning on a win |
| Mean-only blend | NE                |             0 |      50.7507 |        0.5653 |       49 |       53 |               50.7955 |                 0.574  | Allocation-only bound; other races held fixed, not conditioning on a win |
| Mean-only blend | NE                |             1 |      51.7507 |        0.7691 |       50 |       54 |               50.7955 |                 0.574  | Allocation-only bound; other races held fixed, not conditioning on a win |
| Mean-only blend | SD                |             0 |      50.7947 |        0.574  |       49 |       53 |               50.7955 |                 0.574  | Allocation-only bound; other races held fixed, not conditioning on a win |
| Mean-only blend | SD                |             1 |      51.7947 |        0.7745 |       50 |       54 |               50.7955 |                 0.574  | Allocation-only bound; other races held fixed, not conditioning on a win |
| Mean-only blend | ID,MT,NE,SD       |             0 |      50.7482 |        0.5651 |       49 |       53 |               50.7955 |                 0.574  | Allocation-only bound; other races held fixed, not conditioning on a win |
| Mean-only blend | ID,MT,NE,SD       |             4 |      54.7482 |        0.99   |       53 |       57 |               50.7955 |                 0.574  | Allocation-only bound; other races held fixed, not conditioning on a win |

Historical full-chamber totals retain explicit fixed completion for2–9 unmodeled contests per cycle. State accuracy excludes those contests. The completion counts and conditional chamber CRPS/seat errors are saved in `historical_completion.parquet` and `chamber_scores.parquet`.


## Value of more information

This is an auxiliary noisy observation of the final margin with independent measurement noise. It is **not** a literal new-poll likelihood: shared future polling errors and future vote drift are not explicitly modeled here. The effective SD floor is8.887pp, anchored to the median current systematic/bias uncertainty plus one fresh firm; the second quality doubles it to17.774pp. Perfect-final-margin information is the ideal limiting benchmark, numerically integrated, not something a poll can provide.

We average over both favorable and unfavorable observations. The primary criterion is expected reduction in binary Senate-control entropy; secondary is reduction in seat-count variance. A1% entropy reduction does not mean a1-point change in Democratic control odds. On average, expected seats/control odds recover the starting forecast.

| model           | state   |   rank | polled   | structural_proxy   |   p_dem |   information_bits |   control_entropy_reduction_pct |   seat_variance_reduction |
|:----------------|:--------|-------:|:---------|:-------------------|--------:|-------------------:|--------------------------------:|--------------------------:|
| Gaussian Bayesian        | AK      |      1 | True     | False              |  0.3881 |             0.015  |                          1.5039 |                    0.0842 |
| Gaussian Bayesian        | OH      |      2 | True     | False              |  0.6905 |             0.0131 |                          1.3117 |                    0.0707 |
| Gaussian Bayesian        | IA      |      3 | True     | False              |  0.2993 |             0.0125 |                          1.2545 |                    0.072  |
| Gaussian Bayesian        | TX      |      4 | True     | False              |  0.5147 |             0.012  |                          1.2039 |                    0.0704 |
| Gaussian Bayesian        | FL      |      5 | True     | False              |  0.1781 |             0.0089 |                          0.8916 |                    0.0583 |
| Gaussian Bayesian        | MI      |      6 | True     | False              |  0.8022 |             0.0085 |                          0.854  |                    0.0504 |
| Gaussian Bayesian        | GA      |      7 | True     | False              |  0.8295 |             0.0083 |                          0.8282 |                    0.0487 |
| Gaussian Bayesian        | CO      |      8 | False    | False              |  0.9279 |             0.0072 |                          0.7233 |                    0.0548 |
| Gaussian Bayesian        | NC      |      9 | True     | False              |  0.8353 |             0.0065 |                          0.6467 |                    0.0386 |
| Gaussian Bayesian        | WV      |     10 | False    | False              |  0.0573 |             0.0064 |                          0.6392 |                    0.048  |
| Mean-only blend | CO      |      1 | False    | False              |  0.8362 |             0.0145 |                          1.4721 |                    0.0928 |
| Mean-only blend | WV      |      2 | False    | False              |  0.1413 |             0.0119 |                          1.2117 |                    0.08   |
| Mean-only blend | AK      |      3 | True     | False              |  0.5896 |             0.0111 |                          1.1234 |                    0.0798 |
| Mean-only blend | IA      |      4 | True     | False              |  0.388  |             0.0106 |                          1.0811 |                    0.074  |
| Mean-only blend | OH      |      5 | True     | False              |  0.7388 |             0.0097 |                          0.9899 |                    0.0544 |
| Mean-only blend | FL      |      6 | True     | False              |  0.2169 |             0.0091 |                          0.9294 |                    0.063  |
| Mean-only blend | MI      |      7 | True     | False              |  0.7388 |             0.0089 |                          0.8998 |                    0.0636 |
| Mean-only blend | TX      |      8 | True     | False              |  0.6089 |             0.0085 |                          0.8619 |                    0.0615 |
| Mean-only blend | NH      |      9 | True     | False              |  0.8394 |             0.0072 |                          0.7266 |                    0.0571 |
| Mean-only blend | MN      |     10 | True     | False              |  0.8007 |             0.0069 |                          0.706  |                    0.0581 |

All35 states, three information qualities, two model means;8,192 scrambled quasi-Monte Carlo conditional draws and48 quadrature nodes. Top-five union repeated with independent16,384 draws and64 nodes. Maximum mean-recovery error=0.000081 seats; maximum control-recovery error=0.375 percentage points. Tiny negative information estimates near zero are numerical error and retained rather than hidden. Rankings are model-dependent; small adjacent differences are not decision-grade.


## Closeout

The bounded review is complete. Keep the Bayesian reference, bias-corrected polling point benchmark, mean-only blend sensitivity and existing Student sensitivities explicitly named. No model is promoted. Remaining substantive limits are candidate/proxy interpretation, the event flag's meaning and timing, sparse state priors, historical feature vintages and repeated exploration of a small number of cycles.

The existing `refresh_2026.py` can acquire/prepare/align a new dataset. The recent model experiment scripts pin old artifacts; rerunning them does not automatically consume that refreshed dataset. A versioned orchestration step through the selected modeling dependencies is still needed before calling this an end-to-end live forecast refresh. This review performs no download or refresh.
