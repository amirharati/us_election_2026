# Release validation — September 20, 2026

The package was tested with CPython 3.11.7 and the numerical package versions in
`requirements.txt`. The required Excel/PDF parsers were also installed and used.
A completely fresh installation on a second operating system was not tested.

## Output hierarchy revalidation — September 21

All ten notebooks were rerun and saved after reorganizing output publication;
34 tests pass. Markdown reports, complete latest result bundles, and execution
status now have stable paths under `outputs/`. Start with the
[output index](../outputs/README.md) and [cleanup validation](../outputs/validation/output_cleanup.md).
Previous dated runs are preserved locally under ignored `cache/legacy_outputs/`.

## Compact-package revalidation

All ten notebooks and 31 tests passed after the compact-ingestion migration.
Legacy data reads were prohibited in every notebook. A clean Git-eligible copy
passed its audit and offline forecast without raw archives or existing caches.
See the [migration validation report](../reports/compact_migration.md) for sizes,
forecast parity, timings, and the live-source freshness qualification.

## Original package checks

- All four notebooks executed successfully; saved outputs are included. Each has
  five or six code cells. The blend figure was visually inspected.
- All 15 frozen Gaussian forecasts reproduced their saved means, full covariance
  matrices and joint seat-count frequencies. Non-Bayesian corrections reproduced
  their historical reference values.
- The 2026 training reproduction reconstructed chronological prior residuals,
  feature normalization, covariance, feature coefficients, signed loadings and
  polling-variance budgets. Earlier-cycle selection checks passed for all 15 folds.
- Five numerical/workflow tests passed: mean-blend orientation and covariance,
  Gaussian control for the Student sampler, gasoline cache retention, explicit
  stale-source handling, and no-network offline acquisition.
- The actual Student sampler was rerun for the frozen fit and live evidence.
  Latest live maximum R-hat was 1.00227, minimum bulk ESS 5,615.9 and minimum
  tail ESS 10,893.1, within the stated convergence thresholds.
- Online acquisition, poll screening, native feature preparation, dated alignment
  and fresh model inference completed. Current outputs contain 35 contests per
  model, missing current labels, valid probabilities and a 100-seat chamber.
- A physical copy under `/private/tmp/election_standalone_verification` reproduced
  frozen forecasts and performed cached live inference while a Python audit hook
  prohibited file access to the original repository. The input loader and all
  chronological/reference checks passed there. No symlinks were used.
- `PACKAGE_MANIFEST.json` protects immutable release files; notebook cell sources
  have their own checksum index. Each generated output run has an independent
  checksum manifest. Mutable outputs and cache pointers can change on later runs.

## Saved live-data status

The included live run has a September 20 cutoff, with Senate poll field dates
through September 18. Acquisition found 17 added polls and two revised polls
relative to the frozen raw snapshot. These raw counts precede eligibility and
sample-version screening.

FRED failed its online refresh and used the verified local cache, including the
reviewed gasoline addition. The other active checks succeeded or reused a recent
successful check. Political control is carried forward from its September 17
review, explicitly flagged in forecast metadata. The current model checkpoint
remains trained through 2024 with its frozen historical calibration.

This means the live path works, but does not imply every source is current to the
forecast date. Read the source-status table in notebook 04 on each run.

## Retained qualifications

The Student helper retains its research architecture, which differs from the
final Gaussian main model. Mean-only blends preserve Gaussian Bayesian margin covariance;
the non-Bayesian helper's own seat probabilities use an independence approximation.
Blend weights remain sensitivity experiments, with no automatically selected
winner or validated time-dependent schedule. See the full model and data guides
for candidate proxies, historical coverage, revised vintages and other limits.


## Scenario extension

Notebook 05 adds a 0–10 pp additional Democratic-wave axis and −5 to +5 pp
polls-minus-truth axis, plus shared/independent Gaussian error stress at SD 1–3 pp.
It compares the packaged main with 20% and 50% corrected-polling blends.
All 471 model/scenario rows and 16,485 state rows were generated. Zero-stress
baselines match saved live results; covariance/likelihood response and monotonic
wave checks pass. The six-cell notebook executed and its heatmap was inspected.
See SCENARIOS.md for the additive-stress interpretation and source cutoff.


## Matched Student extension

Notebook 06 executes the final-model-matched df5 experiment. All 16 cases
(14 historical folds, frozen2026 and saved live2026) pass the Gaussian recovery
and prior-moment checks; maximum R-hat is 1.00538 and minimum ESS is 2742.4.
Nine tests pass, including known scalar-t prior checks and independent gamma
quadrature for an observed scalar posterior. The six-cell notebook ran and the
coverage/probability figure was inspected. Results remain mixed; the Gaussian
main designation is unchanged. See MATCHED_STUDENT_RESULTS.md.

The matched comparison also passed a forced rerun of all 16 cases from a physical
copy under an unrelated directory, with original-repository file access blocked.
The copied cache verified, and fresh predictions and seat tables matched exactly.

Standalone portfolio verification: a physical copied folder recomputed all15 frozen cases and reproduced predictions, seats, cycle scores and summary tables exactly, with access to the original repository blocked. Latest live rows were manifest-verified.
