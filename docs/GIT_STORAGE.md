# Compact inputs, Git storage, and model updates

The supported commands and all eleven notebooks use ordinary Git files under
`data/compact/` and `assets/`. Raw provider archives and old preparation trees
are excluded by `.gitignore`; no Git LFS or external file-storage service is
required. Existing local archives have not been deleted.

## What is kept

- `assets/`: trained Gaussian/polling/Student parameters, earlier-cycle selection
  surfaces, compact training histories, reference predictions, and simulations.
- `data/compact/frozen/`: immutable extracted historical/frozen model inputs.
- `data/compact/current/`: the latest validated input bundle, replaced after a
  successful live forecast. It contains historical labels/poll metadata, current
  polls, normalized model feature observations, materialized monthly features,
  political context, source receipts, and checksums.
- `outputs/reports/`: latest Markdown reports and the latest forecast HTML and adjacent PNG images.
- `outputs/results/`: one complete latest bundle per forecast, experiment or training
  task, including tables, compact covariance/seat arrays, metadata and manifests. Full live predictive draws stay in ignored cache; forecast-report and market bundles have one canonical copy under `outputs/reports/`. These support rerunning
  downstream notebooks from a clone without retaining all timestamped runs.
- `outputs/validation/`: latest notebook status and cleanup validation.
- `reports/`: source-audit and historical migration documentation.

Start with [the output index](../outputs/README.md). Old timestamped outputs have
been moved to ignored `cache/legacy_outputs/`; new executions stay in ignored
`cache/runs/`. Published latest bundles are replaced, so output folders do not
accumulate full execution bundles. `.codex/` is also ignored and its existing log is untracked.

The two compact bundles preserve historical information and unknown values;
compression does not truncate history or round observations. Feature records
retain only model-consumed series and metadata required for revisions and dated
alignment. Monthly materializations avoid repeating raw feature digestion for
cutoff replays. The original feature and poll-screening calculations are reused.

## Live updates

`python run.py live` checks the current public providers. Downloads and temporary
normalization files live in ignored `cache/`. A provider's changed current feed
replaces that provider's current normalized partition, while its historical
partition remains fixed. Poll feeds are reconciled as a whole, including revised,
removed, and superseded polls. An unchanged row's observation date is retained.
Candidate/race mappings and source schema changes remain explicit review gates.
Some providers publish full files, so a download can still contain historical
rows; those large files are not retained in Git.

The candidate compact bundle is verified and used for inference before replacing
`data/compact/current/`. A failure leaves the previous current bundle and live
forecast pointer intact. Strict mode rejects failed source checks; ordinary mode
uses verified compact evidence with an explicit stale status. Offline mode needs
no raw archives. Six-hour successful-check caching remains available.

A small exact copy of each successful run's inputs is kept in ignored
`cache/run_inputs/` for local replay. A fresh checkout can replay the latest run
using the committed current bundle when its hash matches. Older reports remain
readable, but replaying an older input vintage requires its local cached inputs
or checking out the corresponding Git revision. Ordinary Git history records
committed current-input changes; daily raw archive copies are unnecessary.

## Training and audit

Live and cutoff runs update forecasts with fixed historical calibration; they
never overwrite `assets/`. `run.py train` reproduces the bundled historical fit,
checks it against the saved fit, and writes `outputs/results/training/training/fit.npz`.
It does not promote a replacement model, and that partial fit file is not a
complete drop-in checkpoint. Student commands resample posterior distributions.
A future training-data or model update requires explicit validation/promotion.

`run.py audit` verifies immutable release files, the compact current bundle's
own manifest, historical selections, and frozen numerical comparisons. The
package manifest freezes `data/compact/frozen/`; mutable current inputs use their
own manifest. It no longer requires raw-source files to exist.

The original raw-to-reviewed research scripts remain available for a separate
source audit or re-extraction. They may require optional ignored source archives;
they are not the supported daily runtime. Compact extraction records source
manifest hashes for provenance, but those hashes do not substitute for the raw
files when independently auditing source parsing.

Run all notebooks with:

```sh
python scripts/run_notebooks.py
```

The runner uses the active Python environment, executes cells in order, saves
successful notebooks in place, and writes a status report under
`outputs/validation/`. It blocks access to all legacy `data/` directories
outside `data/compact/`, so accidental raw-data dependencies fail visibly.

Dated reports are kept in `outputs/reports/history/YYYY-MM-DD/<report-type>/report.md`,
using the UTC execution date (the forecast cutoff is shown inside). Same-day reruns
replace that day’s report; other dates remain. Linked charts, tables and provenance
are copied with the report, while full execution archives remain ignored. Notebook
report generation and CLI report-producing tasks use this same publication path.
Run `python run.py report` to generate a dated forecast report from the saved forecast
without downloading data or fitting models. `python run.py live` also generates a report.


## Compact Git publication

Full predictive draw matrices are generated artifacts, not trained model parameters. Git keeps the saved fits in `assets/`, historical/current inputs in `data/compact/`, and compact latest forecast tables, covariance matrices and seat-count frequencies. Publication omits only the `samples` arrays from the live NPZ copies and reseals their manifests. Full execution artifacts remain unchanged under ignored `cache/runs/`.

Notebook 11 has a separate **Prepare local simulations when needed** cell. On a fresh clone it regenerates missing draws from the exact committed input bundle and saved settings, without downloads or historical retraining. It verifies unchanged prediction and seat tables before using the result. Subsequent scans reuse these local draws. Market downloads and external-forecast refreshes remain independent. If the precise input bundle is unavailable, the bootstrap fails rather than silently using newer evidence; rerun notebook 04 explicitly in that case.

Latest forecast reports, linked tables and images have one complete canonical bundle at `outputs/reports/forecast/`. Latest market research is at `outputs/reports/markets/polymarket/`. Duplicate older paths under `outputs/results/forecast/live_reports/` and `outputs/results/markets/` are ignored. Daily Markdown reports and linked images/data remain tracked, one copy per day. HTML uses adjacent PNG images instead of embedding another copy of every image.

The two optional legacy row-level CSV exports under `reports/data_review/` are ignored; their small summary JSONs and extracted compact inputs remain. Existing local copies are not deleted. `scripts/compact_git_outputs.py` migrates older published copies to this layout without touching immutable cached runs. Git LFS and external storage are not required.

These changes reduce future tracked snapshots and growth. Existing commits still contain their original files. No history rewrite or force-push is performed.
