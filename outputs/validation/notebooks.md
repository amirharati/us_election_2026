# Notebook execution

Executed in order with legacy raw-data reads blocked. Successful notebooks are saved in place; logs and failed attempts stay in the ignored local cache.

| Notebook | Status | Seconds |
|---|---|---:|
| [01_models_and_results.ipynb](../../notebooks/01_models_and_results.ipynb) | passed | 6.83 |
| [02_blend_weights.ipynb](../../notebooks/02_blend_weights.ipynb) | passed | 5.36 |
| [03_training_and_assumptions.ipynb](../../notebooks/03_training_and_assumptions.ipynb) | passed | 32.01 |
| [04_live_forecast.ipynb](../../notebooks/04_live_forecast.ipynb) | passed | 139.89 |
| [05_wave_and_poll_error_scenarios.ipynb](../../notebooks/05_wave_and_poll_error_scenarios.ipynb) | passed | 5.51 |
| [06_matched_student_comparison.ipynb](../../notebooks/06_matched_student_comparison.ipynb) | passed | 26.06 |
| [07_older_model_alternatives.ipynb](../../notebooks/07_older_model_alternatives.ipynb) | passed | 56.67 |
| [08_all_model_mixture.ipynb](../../notebooks/08_all_model_mixture.ipynb) | passed | 56.12 |
| [09_poll_weight_experiments.ipynb](../../notebooks/09_poll_weight_experiments.ipynb) | passed | 16.75 |
| [10_model_disagreements.ipynb](../../notebooks/10_model_disagreements.ipynb) | passed | 3.08 |

After execution, report navigation was corrected for GitHub using notebook-relative Markdown links. Model cells and numerical results were retained; notebooks were not rerun for this link-only edit. Original execution hashes and current file hashes are recorded in `notebooks.json`.

Notebooks 07/08 now publish separate reviews. Their publication steps were run against the verified saved portfolio; the complete notebooks were not rerun for that change.

Live notebook section 5b and its report cell were executed against the saved September 21 forecast, adding the surprise watchlists and retaining matching cutoff history. Other notebook outputs were retained; this was not a full rerun.

The corrected section 5b cell was also verified as the first cell in a fresh kernel launched from notebooks/, then the full report was regenerated from saved inputs.
