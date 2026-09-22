# Results — start here

Latest reports and supporting results are below. Dated reports are retained in Git: one copy per UTC execution date and report type; same-day reruns replace that day’s copy. Forecast cutoffs are recorded inside each report.

## Forecast

- [Read the forecast](reports/forecast/report.md) — Markdown summary, state forecasts, source status and cutoff history.
- [Open the browser report](reports/forecast/report.html) — self-contained HTML (download/open locally).
- [Shareable PNG images](reports/forecast/report.md#shareable-images) — generated alongside the tables and retained in dated reports.

## Comparisons and training

- [All-model mixture review](reports/experiments/all_model_mixture.md)
- [Blend-weight comparison](reports/experiments/blend_weights.md)
- [Matched Student-t comparison](reports/experiments/matched_student.md)
- [Matched Student-t review](reports/experiments/matched_student_review.md)
- [Where the models disagree](reports/experiments/model_disagreement.md)
- [Older model alternatives](reports/experiments/older_alternatives.md)
- [Poll-weight experiments](reports/experiments/poll_weights.md)
- [All-model comparison and mixtures](reports/experiments/portfolio.md)
- [Frozen model reproduction](reports/experiments/reproduction.md)
- [Wave and polling-error scenarios](reports/experiments/scenarios.md)
- [Historical training reproduction](reports/training/training.md)

## Dated reports

- [2026-09-22 — Forecast report](reports/history/2026-09-22/live_reports/report.md)
- [2026-09-21 — Historical training reproduction](reports/history/2026-09-21/training/report.md)
- [2026-09-21 — Wave and polling-error scenarios](reports/history/2026-09-21/scenarios/report.md)
- [2026-09-21 — Frozen model reproduction](reports/history/2026-09-21/reproduction/report.md)
- [2026-09-21 — All-model comparison and mixtures](reports/history/2026-09-21/portfolio/report.md)
- [2026-09-21 — Poll-weight experiments](reports/history/2026-09-21/poll_weights/report.md)
- [2026-09-21 — Older model alternatives](reports/history/2026-09-21/older_alternatives/report.md)
- [2026-09-21 — Where the models disagree](reports/history/2026-09-21/model_disagreement/report.md)
- [2026-09-21 — Matched Student-t review](reports/history/2026-09-21/matched_student_review/report.md)
- [2026-09-21 — Matched Student-t comparison](reports/history/2026-09-21/matched_student/report.md)
- [2026-09-21 — Forecast report](reports/history/2026-09-21/live_reports/report.md)
- [2026-09-21 — Blend-weight comparison](reports/history/2026-09-21/blend_weights/report.md)
- [2026-09-21 — All-model mixture review](reports/history/2026-09-21/all_model_mixture/report.md)

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
