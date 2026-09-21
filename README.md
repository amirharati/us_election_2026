# US Senate 2026 — standalone final-model lab

Clone or copy the Git-tracked files in this folder to another computer. No parent
repository, raw historical archive, private account, or original absolute path is required.
The frozen experiment works offline. Live updates require public-source access.

The main model is the final research Gaussian `repaired_both__selected`.
The bias-corrected non-Bayesian model, research Student-t model and mean-only
blends are retained as helpers. This package explicitly designates its main
model; it does not change the older research folder's registry.

## Learning the models

Start with the [step-by-step model and inference guide](docs/MODEL_WALKTHROUGH.md).
It covers every released model, how historical parameters are learned, exact
Gaussian inference, Student sampling, a worked two-state example, and a map to
the code. The concise [model specification](docs/MODEL.md) records calibration
choices; the notebooks show the experiments and results.

## Install and run

Use Python 3.11 in a fresh environment, from this folder:

```sh
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py reproduce
python run.py audit
jupyter lab
```

On Windows activate with `.venv\Scripts\activate`. For reproducible numerical
threading, set `OPENBLAS_NUM_THREADS=1` before launching Python if needed.

## Ten short notebooks

| Notebook | Purpose | Downloads? |
|---|---|---|
| [01 Models and frozen results](notebooks/01_models_and_results.ipynb) | Recompute Gaussian/non-Bayesian forecasts and blends; compare history/current states and seats | No |
| [02 Blend weights](notebooks/02_blend_weights.ipynb) | Fixed 5/10/20/30/40/50% corrected-polling grid, separate September/October evaluation | No |
| [03 Training and assumptions](notebooks/03_training_and_assumptions.ipynb) | Refit prior variance, feature weights, signed factor and polling variance; inspect chronological choices; rerun Student sampler | No |
| [04 Live forecast](notebooks/04_live_forecast.ipynb) | Check downloads/cache, prepare data, compute forecasts, uncertainty watchlist, cutoff history and saved HTML report | Yes, cache aware |
| [05 Waves and polling error](notebooks/05_wave_and_poll_error_scenarios.ipynb) | Bayesian/20%/50% blends, 2D wave/error heatmaps, shared and independent random stress | No; latest saved live run |
| [06 Matched Student-t](notebooks/06_matched_student_comparison.ipynb) | Same final Gaussian priors/relationships, heavier tails; paired history and current comparison | No; latest saved live run |
| [07 Older alternatives](notebooks/07_older_model_alternatives.ipynb) | Earlier Gaussian/Student pair, historical and current comparisons | No; latest saved live run |
| [08 All-model mixture](notebooks/08_all_model_mixture.ipynb) | Fixed four-model joint mixture and 5–50% polling mean shifts | No; latest saved live run |
| [09 Poll weighting](notebooks/09_poll_weight_experiments.ipynb) | Equal polls, participant weights, firm balance and previous-cycle ratings | No; latest saved live run |
| [10 Model disagreements](notebooks/10_model_disagreements.ipynb) | Current margins, probabilities, intervals and chamber tails across retained models | No; saved forecasts |

Each notebook has a small parameter cell, explains the units and assumptions,
and calls readable functions rather than embedding hundreds of modeling lines.
Run All is supported. Saved outputs include the validation run performed during
packaging; future live results can differ.

## Command-line equivalents

```sh
python run.py reproduce
python run.py weights
python run.py scenarios
python run.py matched-student
python run.py portfolio
python run.py poll-weights
python run.py train --scenario matched_live --year 2026
python run.py student --scenario matched_live --year 2026
python run.py live
python run.py live --force
python run.py live --offline
python run.py live --strict
python run.py live --no-student
python -m unittest discover -s tests -v
```

`live` checks source caches every run (default successful-check TTL: six hours).
Changed current feeds update compact normalized inputs and produce new forecasts.
Historical training inputs remain fixed; raw downloads stay in ignored `cache/`. `--force` bypasses the TTL.
Failed sources use verified cached snapshots with explicit stale status;
`--strict` instead fails. Failed preparation leaves the last good forecast intact.
Both Student models and the four-model mixture can be omitted with `--no-student`. Run full live before the portfolio notebooks.

Raw historical acquisition is separate:

```sh
python run.py download-history
python scripts/download_historical.py --help
python scripts/download_features_historical.py --help
python scripts/download_features_current.py --help
```

Compact reviewed historical inputs are bundled, so acquiring raw history again is
unnecessary for reproduction or daily live runs. Newly downloaded historical labels do **not** silently replace
reviewed training labels; see [data preparation](docs/DATA.md).

## What is included

- `election_lab.py`, `run.py`: supported standalone API and commands.
- `scripts/`: numerical, acquisition, cleanup, alignment and audit helpers copied
  from research, plus portable orchestration. Older experiment `build()` entry
  points inside these helpers may reference research runs: use the supported API
  above, not those legacy experiment builders.
- `assets/`: training histories, fitted parameters, earlier-cycle selection
  surfaces, frozen reference results and exact forecast arrays.
- `data/compact/`: self-contained frozen/current model inputs, normalized feature
  history, poll metadata, and source receipts. Other data trees are optional local
  archives excluded from Git. Public source data remain subject to source terms.
- `config/`: dated candidate, survey, election-rule, feature and acceptance policy.
- `outputs/`: latest readable reports, supporting result bundles, and validation.
  Start with [outputs/README.md](outputs/README.md). Timestamped runs stay in ignored cache.
- `cache/`: ignored raw downloads, source checks, temporary preparation, and local
  exact-input replay copies.
- `tests/`, `PACKAGE_MANIFEST.json`: numerical and reproducibility checks.

## How to read the results

Margins are **Democratic minus Republican percentage points**. Positive favors
Democrats. Point seats count positive predicted means; expected seats sum win
probabilities plus continuing seats. Control probability comes from the full
joint simulation for Bayesian/blended/Student models. D requires 51 seats under
the retained chamber convention. The non-Bayesian helper's own seat probability
uses an explicitly labeled independence approximation.

Frozen research inputs are dated **September 17, 2026**. Live outputs show their own
as-of date and source freshness; downloading today does not mean every source
contains observations through today. Mean-only blending retains its base distribution covariance. The four-model mixture also includes between-model disagreement. No blend is silently promoted or selected
from the current election's unknown outcome.

Read [MODEL.md](docs/MODEL.md) for equations and assumptions,
[DATA.md](docs/DATA.md) for cleanup/source policy, and
[REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) for training, selection and limitations.

See [release validation](docs/VALIDATION.md) for executed checks and the saved live-data status.

For definitions of the wave/error axes and random stress, see [SCENARIOS.md](docs/SCENARIOS.md).

The [matched Student specification](docs/MATCHED_STUDENT.md) separates the new distribution-only experiment from the earlier fat-tail helper.

See [matched Student results](docs/MATCHED_STUDENT_RESULTS.md) for accuracy, margins, interval calibration and current seats.

See [older alternatives](docs/OLDER_ALTERNATIVES.md) and [ensemble equations / validation limits](docs/ENSEMBLE.md). The Gaussian is our reference, not a claim of universal superiority. Historical comparisons use chronological CV, with architecture exploration on the same evaluation years.

See [portfolio results](docs/PORTFOLIO_RESULTS.md) for the executed historical and live comparison.

### Saved live reports and cutoff history

Notebook 04 publishes [the Markdown forecast](outputs/reports/forecast/report.md)
and [the self-contained HTML report](outputs/reports/forecast/report.html).
Both have stable paths and are replaced on each successful run. They include
current models, state/chamber tables, the uncertainty watchlist and both-party
control history. Supporting data live in `outputs/results/forecast/`; comparison
reports live in `outputs/reports/experiments/`. See [all outputs](outputs/README.md).
Timestamped runs and previous outputs remain only in ignored `cache/`.

The default history runs from January1,2026 every30days plus the last3calendar days, including the current cutoff. Change `HISTORY_EVERY_DAYS` in the notebook for a finer grid. Each cutoff reuses fixed trained models and reruns inference with screened polls and dated feature references. Verified caches are keyed by actual inputs and model code/assets; the latest endpoint uses the exact current live forecast. Student models retain their sampler/convergence checks.

This is a **retrospective current-roster reconstruction**, not archived issued forecasts: revised feature history, unknown poll release dates, current candidate screening, and September-calibrated model parameters limit early-year interpretation. Features use reference periods, not vintage publication dates. Optional `HISTORY_FEATURE_MODE='fixed_latest'` holds today's features fixed for a polling-only sensitivity. Both-party control follows the existing D>=51 / R<=50 D-seat convention. See [live report methodology](docs/LIVE_REPORT_AND_HISTORY.md).

## Compact Git package

See [Git storage and model updates](docs/GIT_STORAGE.md) for the compact input
layout, current-only refresh, source-audit boundary, and model promotion behavior.
Run all ten notebooks with `python scripts/run_notebooks.py`; this also checks
that none depends on the ignored legacy data trees.

Dated reports are kept in `outputs/reports/history/YYYY-MM-DD/<report-type>/report.md`,
using the UTC execution date (the forecast cutoff is shown inside). Same-day reruns
replace that day’s report; other dates remain. Linked charts, tables and provenance
are copied with the report, while full execution archives remain ignored. Notebook
report generation and CLI report-producing tasks use this same publication path.
Run `python run.py report` to generate a dated forecast report from the saved forecast
without downloading data or fitting models. `python run.py live` also generates a report.

Notebooks 07 and 08 share verified portfolio calculations but publish separate reports:
`outputs/reports/experiments/older_alternatives.md` and
`outputs/reports/experiments/all_model_mixture.md`, with separate dated archives.
