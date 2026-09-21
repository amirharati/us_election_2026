# Combined Student residual experiment

This experiment keeps the established historical fits, feature coefficients, bias estimates, fixed 30-day poll decay and forecast inputs frozen. It jointly replaces national electoral surprise, independent state electoral surprises and the systematic polling residual with Student-t components. This is not a Student refit of the historical estimation pipeline. No Gaussian shock mixture is included.

For state i, theta_i = historical_prior_i + feature_mean + c + r + delta_i. Feature uncertainty c is Gaussian with the saved coefficient-induced variance. National r and local delta_i have independent inverse-gamma variance scales; the systematic polling residual vector has one shared inverse-gamma scale and the saved diagonal covariance. The latter introduces tail dependence without introducing a signed common polling-error factor. Polls observe theta_i + historical_bias_i + systematic_error_i + Gaussian noise. Bias-estimation uncertainty and aggregation/sampling noise stay Gaussian.

For each Student component, s ~ InvGamma(nu/2, (nu-2)/2), so E[s]=1 and its unconditional covariance matches the corresponding Gaussian covariance. Degrees of freedom are shared across these three component types, fixed at 3 or 5. Electoral variance multipliers are 1 or 2 (SD multiplier 1 or sqrt(2)); feature uncertainty and polling-error variance are not inflated. Gaussian controls use both multipliers. Families: no features and shared momentum plus approval.

## Evaluation and numerical checks

- [x] Freeze and verify sources, old notebooks and working designation.
- [x] Check blocked conditional sampler against exact Gaussian conditioning and no-poll Student prior.
- [x] Run six candidates per family for 2012–2024 at matched September and October31 horizons, plus current 2026.
- [x] Use eight chains, initially 2000 warmup and 4000 retained draws per chain; extend if diagnostics fail. Rank/folded split R-hat <1.01 and bulk/tail ESS >=400 for margins, national components, error components, latent log scales and seat count. Constant parameters excluded.
- [x] Repeat representative historical/current Student fits with independent seeds and inspect Monte Carlo differences.
- [x] Select using only previous three available validation cycles, separately by chamber CRPS and state WIS; early Gaussian variance1 fallback.
- [x] Compare state MAE, calls, Brier, interval coverage/WIS and chamber CRPS, seat totals/intervals. Report 2016–2024 prominently and all older available test cycles.
- [x] Save a new executed notebook, immutable result artifacts and an audit; preserve the current working model.

Conditional moments and win probabilities use Rao–Blackwell averaging across sampled scales; state intervals and chamber distributions use joint posterior draws. Reported seat intervals are discrete quantiles. Diagnostics follow the [Stan reference manual](https://mc-stan.org/docs/reference-manual/analysis.html). Historical features and variances remain empirical-Bayes inputs with the uncertainty already present in the source model; this experiment does not add uncertainty about every historical hyperparameter. The 2026 data snapshot remains September17; no refresh. Repeated use of these historical holdouts makes this an exploratory comparison, not a new independent validation set.


## 5. Findings

The combined Student model does **not** give a general improvement. With momentum+approval, Oct31 MAE changes from5.344pp (Gaussian) to5.357pp (df5) or5.376pp (df3), while correct calls fall from133/140 to131/140. More strikingly, nominal70% state coverage falls from72.1% to62.1% or55.0%. Heavy tails here coexist with a sharper posterior center.

Doubling electoral variance recovers133/140 late calls for both Student alternatives but still gives only64.3% (df5) or57.9% (df3)70% coverage. It does not consistently improve chamber CRPS. Gaussian×2 itself is a useful control: it broadens intervals without changing the distribution family.

For the current both-feature forecast, Gaussian gives51.218 expectedD seats, df5 gives51.256 and df3 gives51.151. All three have51D/49R point calls and49–53D70% intervals. The current last-three-cycle selectors both choose Gaussian×1. These values are frozen-snapshot forecasts, not election outcomes.

Retain the Gaussian working designation and the prior component-by-component Student sensitivities. This experiment completes the combined Student residual comparison. A Student historical refit and an ordinary/shock mixture remain separate possible extensions; neither is required to conclude that this combined version has not improved calibration. Repeated exploration on a small number of cycles limits confidence in fine rankings.

## Validation and limitations

12 targeted tests and 18 artifact checks passed; 180 fixed forecasts (120 Student), 6,896 fixed/selected state rows, five independent-seed repeats. All Student fits used eight chains ×4,000 retained draws after2,000 warmup per chain. Maximum R-hat1.0052, minimum bulkESS1,971 and tailESS3,285. Eight notebook code cells executed with captured outputs and a concurrent-edit guard; two figures inspected. All28 older notebooks, source manifests and working designation preserved. No data refresh or model promotion.

Independent-seed mean differences ≤0.066pp; probability differences ≤0.0017; expected-seat differences ≤0.0045 seats. Far-tail state endpoints are less precise: up to3.66pp difference for WV under current df3/variance×2 (70% endpoint differences ≤0.79pp). That variant’s discrete70% lower chamber endpoint was50 in the primary run versus49 in the repeat. This is documented numerical uncertainty, not a stable one-seat difference. Some extreme-state95% intervals under inflation exceed physical ±100pp; the inherited unbounded-margin approximation is preserved without clipping. Matched-variance current both-feature point calls and70% chamber intervals agree between seeds.

A redundant fraction prediction column inherited from source forecasts was normalized to prediction_pp/100 before publication; source-model posterior decomposition columns were removed. Neither issue affected the sampler or metrics, which use the new percentage-point predictions. Future script runs perform this normalization before storage.
