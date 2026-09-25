# Current model disagreement review

Data cutoff: September20,2026. Review: `cache/legacy_outputs/20260921T044037Z/model_disagreement/20260921T003945.240960Z`.
Poll-weight experiments are excluded. Scope is the four Bayesian models, corrected-polling helper, retained Gaussian mean shifts, four-model mixture and mixture mean shifts. The16 retained forecasts share data and are not independent votes. Notebook10 contains every state, ranked spreads, interval plots and covariance/seat-tail summaries.

## Main findings

**Model architecture and the corrected-polling helper matter more than Gaussian-versus-Student tails for central margins.** Mean absolute state-margin difference is2.16 pp between final/older Gaussian,5.78 pp between final Gaussian/corrected polling, and only0.24 pp within either Gaussian/Student pair. These are across-state prediction differences, not errors against unknown2026 results.

### Chamber

| model                     |   point_D |   expected_D |   D_control_pct |   D_lo70 |   D_hi70 |
|:--------------------------|----------:|-------------:|----------------:|---------:|---------:|
| Gaussian Bayesian                  |        51 |       50.321 |          45.513 |       49 |       52 |
| Matched Student-t (df5)   |        51 |       50.477 |          50.069 |       49 |       52 |
| Older Gaussian            |        50 |       51.091 |          61.997 |       49 |       53 |
| Student-t research helper |        50 |       51.116 |          63.019 |       49 |       53 |
| Empirical baseline    |        48 |       48.373 |          16.354 |       46 |       51 |
| Four-model mixture        |        50 |       50.748 |          55.149 |       49 |       53 |
| Mixture: 20% shift toward baseline     |        50 |       50.42  |          47.403 |       49 |       52 |

Point seats count positive mean margins; expected seats sum probabilities; D control requires51. Bayesian/mixture chamber probabilities use joint forecasts. The non-Bayesian helper assumes independent states, so its control probability is not an identical uncertainty framework. All totals include continuing seats under the documented caucus/seat-ledger convention.

### Key states: D−R margin in pp / D win probability

| geography   | Gaussian Bayesian      | Matched Student-t (df5)   | Older Gaussian   | Student-t research helper   | Empirical baseline   |
|:------------|:--------------|:--------------------------|:-----------------|:----------------------------|:-------------------------|
| MI          | +4.99 / 79.9% | +4.90 / 85.0%             | +4.73 / 74.9%    | +4.72 / 80.6%               | -3.86 / 37.9%            |
| ME          | +8.19 / 92.0% | +7.96 / 94.0%             | +5.20 / 76.2%    | +5.35 / 82.4%               | -0.04 / 49.9%            |
| OH          | +2.77 / 68.7% | +2.90 / 74.2%             | +2.12 / 63.1%    | +2.21 / 67.6%               | -2.74 / 41.3%            |
| NH          | +9.95 / 95.4% | +9.38 / 94.1%             | +4.64 / 74.1%    | +4.90 / 79.3%               | +11.36 / 81.7%           |
| AK          | -3.09 / 30.0% | -2.86 / 27.5%             | -0.76 / 45.9%    | -0.86 / 44.3%               | -2.17 / 43.1%            |
| TX          | +0.06 / 50.5% | +0.13 / 51.1%             | -0.42 / 46.8%    | -0.33 / 46.8%               | +0.49 / 51.6%            |
| WV          | -32.46 / 5.7% | -32.40 / 4.8%             | -19.26 / 33.0%   | -18.99 / 30.0%              | -11.71 / 17.5%           |
| NE          | -24.08 / 3.5% | -23.91 / 3.4%             | -21.17 / 22.5%   | -20.90 / 19.1%              | -20.73 / 4.9%            |
| SD          | -34.05 / 0.0% | -33.88 / 0.3%             | -28.00 / 14.0%   | -27.73 / 11.2%              | -27.08 / 1.5%            |
| NC          | +4.75 / 82.6% | +4.94 / 88.7%             | +3.47 / 79.5%    | +3.88 / 86.4%               | +4.79 / 64.9%            |

- **Michigan, Maine and Ohio:** the corrected-polling helper is much more Republican than the Bayesian models. Michigan is final Gaussian D+4.99 versus helper R+3.86; Maine D+8.19 versus roughly tied; Ohio D+2.77 versus R+2.74. They differ in historical correction and prior/shrinkage mechanisms; this is not disagreement about the current raw polling source.
- **New Hampshire and Alaska:** architecture matters even among Bayesian models. NH is D+9.95/95.4% final Gaussian versus D+4.64/74.1% older Gaussian. AK is R+3.09/30.0% D versus R+0.76/45.9% D.
- **Texas:** all core models remain near a tie. Their mean margins span only R+0.42 to D+0.49; D probabilities range46.8–51.6%. Different point calls here are not strong substantive disagreement.
- **West Virginia, Nebraska and South Dakota:** the older models assign appreciably larger upset chances. These have no admitted polling in the current model; historical center and uncertainty construction deserve attention.

### Where uncertainty differs most

| geography   | model                     |   margin_pp |   D_probability_pct |   lo70_pp |   hi70_pp |   lo95_pp |   hi95_pp |
|:------------|:--------------------------|------------:|--------------------:|----------:|----------:|----------:|----------:|
| NE          | Gaussian Bayesian                  |      -24.08 |                3.51 |    -37.86 |    -10.3  |    -50.14 |      1.98 |
| SD          | Gaussian Bayesian                  |      -34.05 |                0.02 |    -43.98 |    -24.11 |    -52.83 |    -15.26 |
| WV          | Gaussian Bayesian                  |      -32.46 |                5.68 |    -53.73 |    -11.2  |    -72.67 |      7.74 |
| NE          | Older Gaussian            |      -21.17 |               22.52 |    -50.24 |      7.9  |    -76.15 |     33.81 |
| SD          | Older Gaussian            |      -28    |               13.98 |    -54.85 |     -1.16 |    -78.77 |     22.76 |
| WV          | Older Gaussian            |      -19.26 |               33.03 |    -64.71 |     26.19 |   -105.22 |     66.7  |
| NE          | Student-t research helper |      -20.9  |               19.07 |    -46.25 |      4.32 |    -77.38 |     35.51 |
| SD          | Student-t research helper |      -27.73 |               11.25 |    -51.01 |     -4.99 |    -78.94 |     23.7  |
| WV          | Student-t research helper |      -18.99 |               30.03 |    -58.37 |     20.36 |   -106.5  |     68.18 |
| NE          | Matched Student-t (df5)   |      -23.91 |                3.39 |    -35.79 |    -11.94 |    -50.06 |      2.48 |
| SD          | Matched Student-t (df5)   |      -33.88 |                0.29 |    -42.58 |    -25.25 |    -53.2  |    -14.86 |
| WV          | Matched Student-t (df5)   |      -32.4  |                4.77 |    -50.74 |    -13.81 |    -73.02 |      8.31 |

Older versus final Gaussian increases the expected D total by0.77 seats. **0.61 seats, about80% of that increase, comes from contests with no admitted polls.** This is an arithmetic decomposition, not a controlled causal isolation of variance: centers, feature fits and state relationships also differ. WV alone adds0.274 expected D seats, NE0.190 and SD0.140, offset by decreases elsewhere.

The old WV central95% interval extends below−100 pp. That is a limitation of the unbounded, extremely broad margin approximation, not a physically possible vote margin. The final model is narrower there, but still uncertain. Lack of admitted polls is different from claiming no source ever published a poll.

The corrected-polling helper uses one pooled SD≈12.54 pp, giving a70% width≈26.00 pp and95% width≈49.17 pp in every state. Its uncertainty is not state-adaptive. For example NC has nearly identical final-Gaussian/helper means (+4.75/+4.79), but D probabilities82.6%/64.9% because the helper is much broader.

### What changes with Student tails?

Final matched Student changes mean margins by0.24 pp on average, while central70% widths shrink by2.19 pp on average. Michigan's mean moves slightly from+4.99 to+4.90, but P(D) rises79.9→85.0%. NC rises82.6→88.7%; already Republican-favored states can instead become more Republican in probability. There is no built-in partisan direction.

Matched prior variances plus heavier far tails can mean narrower central intervals. Posterior inference can also change variances after observing polls. A Student posterior is not obtained by merely widening Gaussian error bars. Historical interval calibration remains relevant: final Gaussian versus matched Student70% coverage was78.6% versus66.4% in September and73.6% versus62.1% in October over2016–2024.

### Joint tails and mixtures

| model                     |   seat_sd |   p_D_at_least_55 |   p_D_45_or_fewer |   p_tie50 |   mean_state_correlation |
|:--------------------------|----------:|------------------:|------------------:|----------:|-------------------------:|
| Gaussian Bayesian                  |    1.5521 |            0.0022 |            0.001  |    0.2512 |                   0.0286 |
| Older Gaussian            |    2.0454 |            0.0447 |            0.0032 |    0.1654 |                   0.0178 |
| Student-t research helper |    1.896  |            0.0364 |            0.0014 |    0.1758 |                   0.0172 |
| Matched Student-t (df5)   |    1.4316 |            0.002  |            0.0004 |    0.2608 |                   0.0265 |
| Four-model mixture        |    1.7858 |            0.0213 |            0.0015 |    0.2133 |                   0.0198 |
| Mixture: 20% shift toward baseline     |    1.8287 |            0.0152 |            0.0035 |    0.2232 |                   0.0198 |

The probability of at least55 D seats is about0.22% final Gaussian,0.20% matched Student,4.47% older Gaussian and3.64% older Student. Thus the broader older **architecture**, more than the Student label by itself, drives this particular chamber-upset scenario. These are finite Monte Carlo estimates, especially noisy for very rare events. Mean correlations alone do not determine seat tails; marginal means, scales and dependence all matter.

The four-model mixture gives50.75 expected D seats and55.1% control; a20% mean-only shift toward corrected polling gives50.42 and47.4%. That translation preserves mixture margin covariance and interval widths, but can change winner correlations and seat variance. The model spread is a sensitivity range, not a confidence interval.

## Interval export correction and validation

This review found that the Gaussian rescoring helper refreshed70% intervals but could retain inherited50/80% intervals,95% widths and WIS after a mean/scale change. `rescore` now regenerates all50/70/80/95% intervals and derived scores, retaining missing uncertainty as missing. Student outputs keep their sampled quantiles.

A new live inference run on **identical saved data** was checked against the previous run: every model's margins, win probabilities,70% intervals and chamber table are unchanged. No model assumption, prior or poll was altered. Old runs remain immutable. The current comparison recomputes widths from endpoints and uses the corrected export. Historical portfolio scores displayed here were already computed with complete interval scoring; previous70%-only summaries are unchanged.

All16 tests passed, including two regressions for stale interval fields and missing uncertainty. Notebook10 executed all six code cells. Current outcomes remain unknown; historical comparisons used chronological fitting but reused evaluation years during model development. Nothing is promoted automatically.
