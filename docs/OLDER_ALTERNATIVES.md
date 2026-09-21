# Older Gaussian / Student-t alternatives

Notebook07 compares the older pair with the final Gaussian reference. Both use the same held-out cycle, contest roster, available polls and feature cutoff. The older fit is retained from the earlier research architecture, not refitted with future labels.

| Model | Prior construction and relationships | Distribution |
|---|---|---|
| Bayesian (reference) | Repaired decay4 centers and selected variance penalties; national momentum/approval; common national and signed state factor | Gaussian |
| Matched Student-t (df5) | Same centers, budgets, features and signed loadings as reference | Variance-standardized Student scale mixtures; see MATCHED_STUDENT.md |
| Older Gaussian | Earlier decay4 centers and variance calibration; national features and common national factor; no signed state factor | Gaussian |
| Student-t research helper | Same earlier architecture as Older Gaussian | Earlier componentwise df5 Student sampler |

The older/newer comparison changes more than a distribution. Compare the matched pairs to isolate the tail experiment. Gaussian calibration is held fixed when introducing tails; the Student models are not separately retuned for this release.

Older models can favor Democrats through different centers **and** broader uncertainty in Republican states. Expected seats and win probabilities need not follow the sign of changes in point margins. A Student tail is symmetric before conditioning; conditioning on polls can change posterior centers in either direction.

Historical forecasts train and select parameters using earlier cycles. The September horizon remains the research September17 cutoff, while current inference uses the live timestamp. The final Gaussian is a designated reference with favorable historical margin performance, not uniformly the most accurate winner classifier. Repeated use of the validation years to explore architectures limits claims of generalization.

Implementation: `scripts/release_alternatives.py`. Live inference replaces polls and available feature values, retaining historical normalizers, fits and calibration. Unknown2026 labels remain missing. Notebook07 records sampler diagnostics and source manifests.
