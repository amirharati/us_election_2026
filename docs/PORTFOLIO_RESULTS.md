# Portfolio comparison results

Saved comparison: `cache/legacy_outputs/20260921T044037Z/portfolio/20260920T212316.436489Z`. Live source: `cache/legacy_outputs/20260921T044037Z/live/20260920T212126.170629Z`.
As of 2026-09-20. Gaussian remains reference; mixture and shifts are exploratory.

## Recent historical folds,2016–2024

| scenario     | model                     |   correct |   n |   MAE pp |   brier |   70% coverage % |
|:-------------|:--------------------------|----------:|----:|---------:|--------:|-----------------:|
| matched_live | Gaussian Bayesian                  |       128 | 140 |   6.3067 |  0.0555 |          78.5714 |
| matched_live | Four-model mixture        |       129 | 140 |   6.5119 |  0.0561 |          75      |
| matched_live | Matched Student-t (df5)   |       129 | 140 |   6.3443 |  0.0548 |          66.4286 |
| matched_live | Mixture: 20% shift toward baseline     |       129 | 140 |   6.5124 |  0.0566 |          75.7143 |
| matched_live | Older Gaussian            |       129 | 140 |   6.8085 |  0.0591 |          79.2857 |
| matched_live | Student-t research helper |       129 | 140 |   6.8011 |  0.0579 |          66.4286 |
| oct31        | Gaussian Bayesian                  |       132 | 140 |   5.206  |  0.0504 |          73.5714 |
| oct31        | Four-model mixture        |       132 | 140 |   5.2748 |  0.0495 |          67.1429 |
| oct31        | Matched Student-t (df5)   |       132 | 140 |   5.2242 |  0.0495 |          62.1429 |
| oct31        | Mixture: 20% shift toward baseline     |       133 | 140 |   5.0972 |  0.0473 |          71.4286 |
| oct31        | Older Gaussian            |       133 | 140 |   5.3436 |  0.0501 |          72.1429 |
| oct31        | Student-t research helper |       131 | 140 |   5.3574 |  0.049  |          62.1429 |

Both horizons contain140 race predictions over five cycles. MAE/Brier average per-cycle scores equally. Correct counts and coverage pool races. This is earlier-cycle chronological validation, but architecture exploration reused the validation years. The20% shift was fixed for display; it was not optimized on these results.

The ensemble adds one September correct call but worsens MAE relative to the Gaussian. At October31, the20% mean shift adds one correct call and reduces MAE/Brier. This horizon dependence supports keeping alternatives rather than declaring a universal winner.

## Live chamber totals

| model                     |   point_D |   expected_D |   D_lo70 |   D_hi70 |   D control % |
|:--------------------------|----------:|-------------:|---------:|---------:|--------------:|
| Gaussian Bayesian                  |        51 |       50.321 |       49 |       52 |        45.513 |
| Older Gaussian            |        50 |       51.091 |       49 |       53 |        61.997 |
| Student-t research helper |        50 |       51.116 |       49 |       53 |        63.019 |
| Matched Student-t (df5)   |        51 |       50.477 |       49 |       52 |        50.069 |
| Four-model mixture        |        50 |       50.748 |       49 |       53 |        55.149 |
| Mixture: 20% shift toward baseline     |        50 |       50.42  |       49 |       52 |        47.403 |

Point D seats count positive mean margins; R point seats are100 minus D. Expected seats sum probabilities. D control requires51. Every prediction includes continuing seats. The20% mixture shift preserves mixture covariance and interval widths, while moving means toward the more Republican corrected-polling helper. Hence its control probability decreases; this is not a covariance change.

## Validation

- 11 numerical/acquisition tests passed, including total covariance and whole-vector mixture checks.
- Notebooks04,07,08 execute end to end; all eight saved notebooks contain no error outputs.
- 105 frozen mixture/translation cases pass centered-draw and interval-width invariance checks.
- Both Student samplers: max Rhat=1.005375; minimum bulk ESS=2742.4; minimum tail ESS=4775.3.
- No 2026 labels used. Early missing non-Bayesian interval calibration remains missing rather than counted as a coverage failure.
- Live freshness mode: `online_with_cache`; stale sources: `['fred']`. Political review through 2026-09-17 is explicitly carried forward, not newly verified.

See ENSEMBLE.md for equations, fixed weighting, uncertainty accounting and historical chamber-completion limitations. Complete state/cycle tables and immutable manifests are in the notebooks and output directory.

Standalone portfolio verification: a physical copied folder recomputed all15 frozen cases and reproduced predictions, seats, cycle scores and summary tables exactly, with access to the original repository blocked. Latest live rows were manifest-verified.
