# Results — start here

Only the latest published results live here. Each rerun replaces the corresponding report and result bundle; Git history preserves committed versions.

## Forecast

- [Read the forecast](reports/forecast/report.md) — Markdown summary, state forecasts, source status and cutoff history.
- [Open the browser report](reports/forecast/report.html) — self-contained HTML (download/open locally).

## Comparisons and training

- [Blend-weight comparison](reports/experiments/blend_weights.md)
- [Matched Student-t comparison](reports/experiments/matched_student.md)
- [Matched Student-t review](reports/experiments/matched_student_review.md)
- [Where the models disagree](reports/experiments/model_disagreement.md)
- [Poll-weight experiments](reports/experiments/poll_weights.md)
- [All-model comparison and mixtures](reports/experiments/portfolio.md)
- [Frozen model reproduction](reports/experiments/reproduction.md)
- [Wave and polling-error scenarios](reports/experiments/scenarios.md)
- [Historical training reproduction](reports/training/training.md)

## Validation

- [Notebook execution status](validation/notebooks.md)
- [Storage and rerun validation](validation/output_cleanup.md)

## Supporting files

- `results/forecast/`: latest forecast tables, joint arrays and cutoff history.
- `results/experiments/`: latest tables and diagnostics for each comparison.
- `results/training/`: latest explicit training/sampler reruns. The active model remains in `../assets/`.
- Every result bundle includes `run.json` and `manifest.json`; keep bundles complete.

Timestamped executions, intermediate forecasts, logs and older migrated outputs are local-only under `../cache/`. They are ignored by Git. Source-audit and migration documentation remain under `../reports/`.

Rerun all notebooks: `python scripts/run_notebooks.py` from the project root.
