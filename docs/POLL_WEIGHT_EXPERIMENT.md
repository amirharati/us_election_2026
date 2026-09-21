# Poll-weight sensitivity experiment

Notebook09 and `python run.py poll-weights` compare seven rules on the final Gaussian: equal polls with 30-day decay, respondent-count weights with the same decay, the current equal-firm rule, participant weights within equally balanced firms, mild/strong last-cycle firm ratings, and a literal equal-poll/no-decay average. The existing final/live models are unchanged. No sources are downloaded; run notebook04 first for newer inputs.

## Fixed design and scope

One poll is one admitted underlying sample after the existing candidate, date, basis and population screening. The same samples enter every variant. This experiment does not change LV/RV selection or use outside pollster ratings.

Historical inference uses frozen final-model priors and calibration checkpoints for 2012–2024 at September17 and October31, plus frozen2026 and the latest saved live2026 snapshot. The current-cycle cutoff and source dates are saved in run metadata. Four Bayesian alternatives are retained elsewhere, but this experiment tests only the main Gaussian to isolate the averaging question.

For sample i in firm f, define d_i=2^(-age_i/30), N_f=number of admitted samples from f in that contest, and n_i=participant count. Normalize each rule's sample weights to sum to one per contest:

| Rule | Unnormalized sample weight |
|---|---|
| Firm balanced (reference) | d_i / N_f |
| Equal polls,30d | d_i |
| Respondent n,30d | d_i n_i |
| Firm balanced + within-firm n | d_i n_i / sum_(j in f) n_j |
| Firm + last-cycle rating | (d_i / N_f) multiplier_f |
| Equal polls,no decay | 1 |

Respondent counts are deliberately uncapped here. Missing, nonfinite or nonpositive n uses the median positive reported n from **earlier cycles at that horizon**, falling back to1,000 when absent. Raw reported n, imputation flag and n used are all saved. The no-decay variant includes all admitted samples from the two-year cycle up to cutoff, so it changes timing as well as averaging.

## Last-cycle rating, default1

For target year Y, use only Y−2 Senate outcomes and samples available at the same historical forecast horizon. In each prior-cycle contest, restrict rating evidence to the final30 days before that horizon cutoff. Form one recency-weighted average per firm/contest, then compute its absolute margin error relative to the final result.

Subtract the median firm error within that contest. This reduces the reward for simply polling easy contests. A contest needs at least two firms for this relative comparison. Each firm/contest contributes equally; repeated samples cannot create extra rating observations. Unknown firm identity and firms without qualifying previous-cycle evidence get the neutral multiplier1.

For firm f, let E_f be mean excess error in pp and k_f its number of eligible prior-cycle contests:

    reliability_f = k_f / (k_f + 3)
    multiplier_f = clip(exp(-strength * reliability_f * E_f / 3), 0.5, 2)
    strength = 0.5 (mild) or 1.0 (strong).

Better-than-peer accuracy gives a multiplier above1; worse gives below1. This is a continuous rating rather than a hard top-N cutoff. The scale3 pp, shrinkage3 contests and caps are fixed sensitivity choices, not optimized on the displayed test results. It remains a noisy proxy: candidate/state mix, field timing and presidential-versus-midterm changes can alter its relevance. It does not isolate intrinsic pollster quality.

For 2026 the rating outcomes are2024; for the2024 historical forecast they are2022. A firm's current-cycle outcome is never used to score itself. If Y−2 has no eligible evidence, the factor remains1 rather than silently reaching farther back.

## Two historical-bias arms

1. **Frozen bias:** change only current-cycle polling averages, retaining that fold's original historical bias estimate.
2. **Refit bias:** reconstruct each earlier cycle's polling average under the same rule, with its own past-only ratings and n fallback. Re-estimate the historical Gaussian polling-bias posterior from those errors, with the same original training dates, relevance weights, diagonal polling variance budget and bias prior.

The reference rule must reproduce original aggregates and forecasts in both arms. Refit bias does not mean full variance/hyperparameter re-estimation.

We retain original firm_mass, hence the 16/firm_mass freshness variance, for every variant. We also retain the original systematic polling variance, observation availability, prior mean/covariance and their tuning choices. Bias posterior covariance stays the same because its precision inputs are unchanged; this is checked numerically. Therefore the **whole posterior margin covariance is unchanged** in this experiment. Respondent-count units or repeated samples cannot accidentally increase confidence merely by enlarging the sum of weights.

This is a controlled sensitivity of means and bias calibration, not a fully redesigned sample-size-aware likelihood. It can reveal useful directions but cannot establish that participant counts have no information about precision. A future variance/refitting experiment should use its own chronological tuning and checks.

## Outputs and interpretation

`outputs/results/experiments/poll_weights/` includes:

- `predictions.parquet`, `seats.parquet`: all variants, both arms and historical/live cases.
- `cycle_scores.parquet`, `summary.parquet`: cycle-level and all/recent historical accuracy, MAE, Brier, coverage, widths and WIS.
- `raw_polls.parquet`, `raw_summary.parquet`: raw polling averages and observed-race diagnostics.
- `sample_weights.parquet`: normalized sample weights, firm multipliers, reported/imputed n and dates.
- `ratings.parquet`: previous-cycle evidence and rating reliability.
- `bias_estimates.parquet`: all fitted/frozen state polling-bias estimates.
- `checks.parquet`, `run.json`, `manifest.json`: chronology, baseline reproduction, covariance controls and provenance.

Recent Gaussian summaries cover140 modeled contests over2016–2024 at each horizon. MAE/Brier average cycle means; winner counts/coverage pool contests. Raw-poll summaries cover only polled races,102 in September and125 in October, and pool their absolute errors. Those raw and full-model MAEs have different denominators/weighting and are not a direct skill comparison.

Point seats count positive mean margins, expected seats sum win probabilities, and control requires51 D seats under the saved ledger convention. Joint Gaussian draws use matched random numbers across variants. Margin covariance can remain fixed while winner/seat uncertainty changes after means shift. Historical unmodeled contested seats retain the documented fixed-completion assumptions.

Chronological fitting does not undo repeated architecture exploration on the same historical cycles. No variant is selected/promoted automatically; the notebook is a separate research experiment. Completed runs are cached by source, training and live-manifest hashes and remain portable inside the standalone folder.

See [saved results](POLL_WEIGHT_RESULTS.md) for the executed comparison.
