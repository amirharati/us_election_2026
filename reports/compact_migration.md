# Compact Git package validation — 2026-09-20

The supported CLI, ingestion, model loaders, audit, report/cutoff paths, and all ten notebooks were reviewed and exercised. Inherited research scripts were retained and compiled; they are optional raw-source audit/experiment tools, not the daily runtime.

## Result

- Git-eligible package: approximately 91.8 MiB, including existing and rerun reports.
- Self-contained frozen/current data: 23.97 MiB, down from approximately 762 MiB of previously required bundled data.
- Trained model assets and compact training histories: 6.57 MiB; active fitted parameters unchanged.
- Raw archives, legacy preparation trees, downloaded source files, and intermediate inference runs are ignored. No large-file storage service is required and no existing raw files were deleted.
- Live refresh replaces current evidence, including poll removals/revisions and changed feature partitions. Historical labels/calibration remain fixed. Candidate/schema gates, checksum checks, explicit stale fallback, and failed-inference rollback are retained.

## Verification

- 31 unit/workflow tests passed, including compact integrity, feature materialization parity, feature revisions, poll removal, historical retention, and failure rollback.
- All Python modules compiled successfully.
- Frozen/current extracted forecast inputs matched the legacy pipeline. The four core live models matched the pre-migration run exactly for margins, win probabilities, and 70%/95% interval endpoints (maximum difference 0).
- A physical copy containing only Git-eligible files passed the release audit and an offline forecast with no raw data directories and no initial cache. Exact latest-run inputs resolved from the committed compact current bundle.
- All ten notebooks executed in order and were saved in place. A kernel audit hook prohibited all legacy data reads outside data/compact/. Student sampling and cutoff history remained enabled.
- Immutable release hashes and notebook source hashes are verified by run.py audit; current compact data has its own mutable-bundle manifest.

| Notebook | Status | Seconds |
|---|---|---:|
| 01_models_and_results.ipynb | Passed | 18.51 |
| 02_blend_weights.ipynb | Passed | 5.23 |
| 03_training_and_assumptions.ipynb | Passed | 23.08 |
| 04_live_forecast.ipynb | Passed | 133.29 |
| 05_wave_and_poll_error_scenarios.ipynb | Passed | 5.29 |
| 06_matched_student_comparison.ipynb | Passed | 22.17 |
| 07_older_model_alternatives.ipynb | Passed | 59.58 |
| 08_all_model_mixture.ipynb | Passed | 54.86 |
| 09_poll_weight_experiments.ipynb | Passed | 15.56 |
| 10_model_disagreements.ipynb | Passed | 2.48 |

Total notebook execution time: 340.05 seconds.

## Live-source status and limits

The live cutoff is 2026-09-20. FRED failed its source check (RuntimeError), so the report explicitly uses verified stale compact FRED evidence. Other providers reused recent successful source checks. This run is not a claim of nine newly downloaded feeds. Fresh feature parsing/revision replacement was exercised separately by a synthetic provider-feed regression test.
Political context remains explicitly carried forward from its dated review. Independent raw-source parsing audits require optional original archives; normal forecasting and model reproduction do not. Older input vintages need the local replay cache or their Git revision; saved reports remain readable.

[Latest complete forecast report](../outputs/live_reports/20260921T035014.722114Z/report.html)

[Notebook execution record](../outputs/notebook_execution/results.json)

[Storage and model lifecycle](../docs/GIT_STORAGE.md)
