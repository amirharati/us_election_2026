# Git storage cleanup — September 25, 2026

Current Git-eligible files total **75.4 MiB**, down from the earlier **136.6 MiB** inventory (about 45% smaller). This measures the next complete file snapshot, not compressed push traffic or existing Git history.

- Saved models and compact historical/current data remain tracked.
- Full predictive draws remain in ignored local cache. Published live bundles retain probabilities, intervals, covariance matrices, seat frequencies and verified manifests.
- A clean export with no cache rebuilt full simulations offline and verified unchanged predictions/seat tables. Its subsequent six-model scan evaluated 2,970 model–contract pairs with network calls and repeated inference blocked.
- Latest forecast and market bundles now have one canonical report location. Old duplicate folders and two optional legacy audit CSV exports are untracked and ignored; local copies remain.
- Dated reports and their images remain tracked. No tracked HTML report embeds duplicate base64 PNGs.
- All 112 tests passed. Notebook 11 reran and saved successfully (13.07 seconds). Forecast reports were regenerated from the existing forecast, without refreshing inputs or retraining. Public manifests, notebook execution checksum and report links verified.
- No Git LFS, history rewrite, commit or push was performed. Existing commits still contain their original files.

See [storage policy and clone behavior](../../docs/GIT_STORAGE.md).

---

The earlier validation below describes the September 21 layout before later features were added.

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
