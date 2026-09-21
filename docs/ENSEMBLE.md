# All-model mixture and mean-only polling adjustment

## Fixed alternatives

The four Bayesian distributions receive equal25% weights: final Gaussian, matched final df5 Student, older Gaussian, older df5 Student. They see the same election evidence. They are alternative interpretations, **not independent measurements**; no likelihoods are multiplied.

For joint state-margin vector Y, define

    p_mix(Y | data) = sum_k w_k p_k(Y | data), w_k = 0.25
    m = sum_k w_k m_k
    C = sum_k w_k [C_k + (m_k-m)(m_k-m)^T].

One component applies to the entire state vector. Implementation concatenates joint draws, weighting each draw by w_k / number_of_component_draws. This retains within-model state dependence, does not give longer chains greater model weight, and includes uncertainty from disagreements between models. It is not a Gaussian approximation, independent per-state mixture, or average of four draw vectors. The latter would shrink uncertainty improperly.

## Corrected polling helper

Let h be the non-Bayesian corrected-polling margin vector. At a fixed alpha,

    delta = alpha (h-m)
    Y_adjusted = Y_mix + delta
    E[Y_adjusted] = (1-alpha)m + alpha h
    Cov(Y_adjusted) = C.

We test alpha=5/10/20/30/40/50%. The20% example is for compact display, not an optimized choice or promoted main model. Each state receives its own translation; the full centered distribution, correlations, covariance and interval widths are unchanged. Helper uncertainty is not added. This preserves **mixture** uncertainty, which differs from the reference Gaussian's uncertainty. The earlier reference-Gaussian-only mean blends remain available in notebook02 and live saved outputs.

Mixture probabilities, quantiles and seat frequencies use weighted joint draws. Component probabilities may use analytic/Rao–Blackwell calculations; finite Monte Carlo differences are expected. For mixture rows, expected seats exactly equal continuing D seats plus the sum of simulated state win probabilities. Control requires51. The separate non-Bayesian helper's own chamber probabilities assume independent states and are labeled accordingly.

## Chronological validation and limits

Historical folds cover2012–2024 at September17 and October31; recent summaries focus on2016–2024. For target cycle t, training labels and hyperparameter selection use cycles before t. Normalization is historical, never estimated using held-out outcomes. This is rolling-origin temporal cross-validation, not random state folds. State observations within one cycle share national conditions and should not be treated as independent national-feature samples.

Architecture choices were explored repeatedly on these same historical years. Consequently the published comparison can have model-selection optimism even though fold fitting is chronological. It is not an untouched final holdout, and the Gaussian reference is not proven universally best. Mixture weights and the mean-shift grid are fixed sensitivities; neither is learned from the evaluation results. All2026 outcomes remain unknown.

MAE/Brier/WIS summaries average cycle metrics equally; classification accuracy and interval coverage pool contests. Missing early non-Bayesian probability calibration remains missing and `probability_n` reports its denominator. Historical chamber totals include documented fixed completion of some unmodeled contests; they are not a claim of fully forecast coverage. Frozen2026 and fresh live2026 have different evidence tags and are never pooled into historical scores.

## Reproduction

Run `python run.py live` (online, cached) then `python run.py portfolio`. An offline live recomputation is `python run.py live --offline`. Notebook07 shows older alternatives; notebook08 shows the mixture, all shift weights, state margins/probabilities and historical/current seats. Neither comparison notebook downloads data: it uses the latest saved live run. `--no-student` deliberately omits both Students and the four-model mixture; run full live before the portfolio.

`config/ensemble_v1.json` defines weights and labels. `scripts/model_portfolio.py` verifies contest alignment, joint control arithmetic, unchanged centered draws, and interval widths for every translation. Cached runs are keyed by source/config/training/live-manifest hashes. Every completed output has a manifest, provenance, diagnostics, historical score tables and saved forecast moments. Seeds and samplers regenerate joint draws; full draw matrices are not archived.
