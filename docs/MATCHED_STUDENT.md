# Student-t experiment matched to the final Gaussian

Run notebook `06_matched_student_comparison.ipynb` or:

```sh
python run.py matched-student
```

This is a research comparison. The main Gaussian designation and earlier Student
helper are unchanged. No downloads occur: frozen historical evidence and the
latest verified saved live forecast are used. Run notebook 04 first for newer
current evidence. Completed comparisons are cached by source/code hashes;
`--force` reruns the sampler.

## What is fixed

Both versions use `repaired_both__selected`: repaired historical centers,
Gaussian-trained feature coefficients and their uncertainty, state variance
budgets, signed loadings and selected strength, historical polling bias, current
poll aggregates and their freshness, and all chronological hyperparameter choices.
The experiment does not retune any of these under Student errors or select degrees
of freedom from historical scores. The sole candidate has df=5 and variance
multiplier=1. Historical results are paired on identical targets and labels.

## Generative model

For each currently eligible state/contest s:

`theta_s = center_s + x' E[beta] + C + N + h_s Z + epsilon_s`.

- `C ~ Normal(0, FV)`, `FV = x' Cov(beta) x`: retained feature-fit uncertainty.
- `N`: national residual, variance A.
- `Z`: signed-pattern residual, variance 1; fixed `h = sqrt(lambda)*loading`.
- `epsilon_s`: independent local residual, variance `L_s = V_s - A - h_s²`.

Each of N, Z and epsilon has its own zero-mean, variance-standardized Student-t
(df=5) scale mixture. If a component's original Gaussian variance is v, use
`Normal(0, v*S)`, with `S ~ InvGamma(df/2, (df-2)/2)` in shape/scale convention.
E[S]=1, so its variance remains v. An ordinary unit-scale t5 would instead have
variance 5/3: that unintended variance inflation is explicitly avoided here.
A zero signed loading makes that component irrelevant for the state.

For observed states:

`q_s - historical_bias_s = theta_s + eta_s + xi_s`.

`eta | S_poll ~ Normal(0, S_poll*diag(P))` has one shared inverse-gamma scale;
`xi ~ Normal(0, diag(F))` retains bias-estimation uncertainty and freshness noise.
F includes `16/firm_mass`. The common polling scale permits larger error magnitudes
in a noisy cycle without imposing a shared partisan error sign. All component
scales are mutually independent a priori. Missing polls create no likelihood row.

Before conditioning on current polls, the mean and full covariance exactly match
the final Gaussian:

`mu = center + x' E[beta]`

`K = diag(L) + (A+FV)*11' + h*h'`.

The covariance relationships and linear loadings are fixed, but tail dependence
changes. This is a componentwise heavy-tail model, not a single multivariate-t
scale inflating every state together. The resulting marginal posterior is not
generally a simple univariate t distribution.

## Inference

Blocked Gibbs sampling integrates the state-local residuals when drawing the two
shared factors `(C+N, Z)`. It then samples local results, splits the national
residual from Gaussian feature uncertainty, draws polling residuals, and updates
the inverse-gamma scales. Conditional means, second moments and win probabilities
are averaged analytically (Rao–Blackwellization); quantiles and chamber totals use
joint draws. This recomputes the posterior, rather than widening old intervals.

Eight chains start with 2,000 warmup and 4,000 retained draws per chain. Runs extend
if necessary until maximum rank/split R-hat is below 1.01 and minimum bulk/tail ESS
is at least 400. A failed convergence gate raises an error and does not create a
completed cached comparison. Sampler settings and diagnostics are saved per fold.

## Controls and evaluation

For every fold, setting all scale variables to one reproduces the final Gaussian
prior covariance, posterior mean, posterior covariance and marginal probabilities.
A separate scalar, unobserved-state test compares the sampler with the known t5
CDF, variance and quantiles. Signed-factor/no-poll Gaussian tests exercise opposite
loadings and partial observations. Finite-variance settings require df>2.

The comparison includes 2012–2024 at the matched September and October 31 horizons,
frozen2026, and the latest saved live2026. Primary recent summaries use2016–2024.
Metrics include margin MAE, winner accuracy, Brier score, interval coverage/width,
weighted interval score and chamber CRPS. Current outcomes remain unknown.
Classification uses the sign of the predicted mean for continuity with earlier
work; Student P(D)>0.5 classification is also retained separately in predictions.

Historical parameters and selections precede their forecast cycles, but the
architecture has been explored on this historical record. These are research
hindcasts, not an untouched final holdout or proof that one distribution is best.
Historical economic vintages, candidate proxies and other release limitations
remain unchanged. Student tails do not inherently favor either party.

## Files and reproducibility

`outputs/matched_student/` contains predictions, seat distributions, all-fold
Gaussian controls, convergence diagnostics, source hashes and immutable manifests.
Forecast NPZ files retain prior/posterior moments, trace summaries and seat counts.
The comparison notebook writes its tables/plot to a separate
`outputs/matched_student_review/` run so its display files cannot invalidate the
sampler cache. The earlier fat-tail helper remains a separate architecture.
