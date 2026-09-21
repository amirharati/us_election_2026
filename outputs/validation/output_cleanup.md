# Output cleanup validation — September 21, 2026

[All outputs](../README.md) · [Notebook execution details](notebooks.md) · [Latest Markdown forecast](../reports/forecast/report.md)

## What changed

- `.codex/` is ignored; its previously tracked session log is removed from the index and retained locally.
- `outputs/reports/` contains the latest Markdown forecasts/comparisons, plus forecast HTML and its chart.
- `outputs/results/` contains 12 complete latest result bundles, grouped into forecast, experiments, and training.
- `outputs/validation/` contains notebook status and these checks.
- Timestamped executions now go to ignored `cache/runs/`; logs go to ignored `cache/notebook_execution/`.
- Previous outputs are preserved locally in `cache/legacy_outputs/20260921T044037Z/`. They are removed from the current Git working tree, not destroyed.
- Notebook 02 now has its own blend-weight bundle and cannot replace notebook 01's frozen reproduction results.
- Every notebook ends with a direct link to its published Markdown report. CLI runs print published paths before the local archive path.
- Forecast reports carry their own copied metadata, keeping provenance correct if another live run is executed later.

## Size

Published outputs decreased from **45.0 MiB** to approximately **12.6 MiB**. The old layout tracked 1,220 output files; the latest-only layout has approximately 319. Current Git-eligible files total approximately **59.4 MiB**, excluding local caches and Git history.

## Checks

- All ten notebooks executed successfully, in order, with legacy raw-data reads blocked; saved notebook hashes match the execution record.
- All 34 numerical/workflow/publication tests passed; all Python modules compile and `git diff --check` passes.
- The release audit verifies package and notebook sources, compact data, 15 historical model selections, and frozen numerical comparisons.
- All 12 published result manifests verify. Markdown report links resolve, including charts and provenance.
- A clean physical copy containing only Git-eligible files, without `.codex/`, raw archives or an initial cache, passed the audit, loaded all latest bundles, regenerated Markdown/HTML reports, and completed offline live inference/publication.
- Active model assets remain unchanged. Latest output paths are replaced on each run; committed versions remain available in Git history.

## Source status

The live cutoff is September 21, 2026. FRED failed its source check and used verified saved evidence, explicitly marked stale. The other providers reused recent successful checks. The report records this distinction; rerunning does not imply every source supplied new observations.

Total notebook execution time: 348.28 seconds.
