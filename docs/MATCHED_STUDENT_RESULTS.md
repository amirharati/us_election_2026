# Matched final Gaussian / Student-t results

Completed September 20, 2026. All prior centers, initial covariance, features,
loadings, historical poll corrections and tuning choices were held fixed.
Student electoral/polling residuals use df=5 with matched prior variance. No
Student-specific retuning or promotion was performed.

## Recent historical results: 2016–2024

Five cycles, 140 identical races at each horizon. MAE/Brier/WIS/width are averaged
within cycle then across cycles; accuracy/coverage pool contests. September
refers to the retained matched historical horizon, not refreshed historical data.

| scenario     | model                   |   races |   correct |   accuracy_pct |   absolute_error_pp |   brier |
|:-------------|:------------------------|--------:|----------:|---------------:|--------------------:|--------:|
| matched_live | Bayesian                |     140 |       128 |        91.4286 |              6.3067 |  0.0555 |
| matched_live | Matched Student-t (df5) |     140 |       129 |        92.1429 |              6.3443 |  0.0548 |
| oct31        | Bayesian                |     140 |       132 |        94.2857 |              5.206  |  0.0504 |
| oct31        | Matched Student-t (df5) |     140 |       132 |        94.2857 |              5.2242 |  0.0495 |

| scenario     | model                   |   width70_pp |   coverage70 |   width95_pp |   coverage95 |   wis_pp |
|:-------------|:------------------------|-------------:|-------------:|-------------:|-------------:|---------:|
| matched_live | Bayesian                |       19.876 |       78.571 |       37.588 |       94.286 |    3.822 |
| matched_live | Matched Student-t (df5) |       16.929 |       66.429 |       35.084 |       92.857 |    3.783 |
| oct31        | Bayesian                |       15.8   |       73.571 |       29.878 |       94.286 |    3.054 |
| oct31        | Matched Student-t (df5) |       13.287 |       62.143 |       26.851 |       92.143 |    3.049 |

Chamber metrics (lower is better):

| scenario     | model                   |   seat_crps |   expected_seat_error |
|:-------------|:------------------------|------------:|----------------------:|
| matched_live | Bayesian                |      0.7046 |                1.1331 |
| matched_live | Matched Student-t (df5) |      0.7686 |                1.2424 |
| oct31        | Bayesian                |      0.6633 |                0.9458 |
| oct31        | Matched Student-t (df5) |      0.6828 |                0.9729 |

The Student result has one additional correct September call and ties October.
Its margin MAE is slightly worse at both horizons, while Brier and WIS improve
slightly. Joint chamber CRPS and expected-seat error worsen. Central 70%
intervals are narrower and under-cover, especially in October (62.1% coverage).
95% coverage also falls modestly. These mixed results do not support automatic
replacement of the Gaussian main model.

Variance matching does not force central intervals to be equally wide. The t5
shape is more concentrated around its center with heavier extreme tails; current
observations also update its latent variance scales. This is why “fat tails” did
not automatically increase 70% coverage.

## Current saved live evidence

Same September 20 cutoff and source run for both models. Polls extend through
September 18; inherited FRED cache fallback and political-control carry-forward
remain explicit in the source metadata.

| model                   |   point_D |   point_R |   expected_D |   D control % | 70% D seats   |
|:------------------------|----------:|----------:|-------------:|--------------:|:--------------|
| Bayesian                |        51 |        49 |      50.3214 |       45.5133 | 49–52         |
| Matched Student-t (df5) |        51 |        49 |      50.4775 |       50.0687 | 49–52         |

Student raises expected D seats by about 0.16 and control probability by about
4.6 percentage points, to approximately a coin flip. Both call 51D/49R and have
a central 70% range of 49–52 Democratic seats. The simulated 50.1% is not a
meaningful distinction from 50%; sampling and model uncertainty remain.

## Validation and artifacts

- All 16 cases passed exact Gaussian-control and matched prior-covariance checks.
- Maximum R-hat: 1.005375; minimum bulk/tail ESS: 2742.4.
- Nine tests passed, including an independent quadrature check of a scalar observed Student posterior.
- Notebook 06 executed successfully; the comparison figure was inspected.
- Sampler run: `outputs/matched_student/20260920T205948.809875Z`.
- Tables and figure: `outputs/matched_student_review/20260920T210126.682933Z`.

All 2012–2024 per-cycle results, current state margins/probabilities and sampler
diagnostics are in notebook 06 and these versioned artifacts. Historical scores
are exploratory after repeated architecture comparisons, not untouched holdout
proof of superiority. The earlier Student helper remains a separate architecture.
