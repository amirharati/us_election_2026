# Model names in tables and charts

All displayed forecasts use polling evidence when available. These names describe methods; they do not rate the quality of other models.

| Display name | Meaning |
|---|---|
| Gaussian Bayesian | Reference Bayesian model with a Gaussian predictive distribution. |
| Matched Student-t (df5) | Bayesian alternative using the reference construction with heavier tails. |
| Older Gaussian | Earlier Gaussian construction, retained for comparison. |
| Student-t research helper | Student-t alternative using the earlier construction. |
| Empirical baseline | Poll averages combined with historical polling-error patterns, with empirical uncertainty estimates. |
| Four-model mixture | Predictive mixture of the four Bayesian alternatives. |
| Mixture: 20% shift toward baseline | Moves the mixture mean 20% toward the empirical baseline, retaining the centered mixture distribution. |
| Gaussian: 20% shift toward baseline | Applies that mean shift to the Gaussian reference instead. |

For example, if the mixture predicts D+10 and the baseline predicts D+5, a 20% shift gives D+9. This is not a 20% weight on newly added polls. Other percentages follow the same rule.

Raw saved identifiers remain unchanged for compatibility: `Non-Bayesian corrected`, `Mixture + polling 20%`, and `Corrected 20%` map to the clearer display names above. Label changes do not change calculations or fitted models. Existing dated reports remain historical snapshots.
