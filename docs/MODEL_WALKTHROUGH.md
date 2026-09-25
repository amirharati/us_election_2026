# Learning guide: construction and inference for every released model

This guide describes the implemented models, not a proposed redesign. Start here, then use [MODEL.md](MODEL.md) for calibration details, [DATA.md](DATA.md) for data preparation, and the implementation map at the end. All paths are relative to the standalone folder; no parent repository is needed.

## 1. What is being predicted?

For forecast cycle t, θ_s is the final Democratic-minus-Republican margin in Senate contest s, measured in **percentage points** (pp). A margin of +3 means a three-point Democratic advantage. It is not a probability. Recorded candidate-share denominators are retained; we do not silently renormalize to two-party shares.

The output is a joint distribution for the vector θ of current contests. In 2026 there are 35 modeled contests and 65 continuing seats. A national movement is a **latent shared cause of state changes**, not an additional national popular-vote target or a directly observed generic-ballot likelihood.

Historical storage covers all states, but a state without a Senate contest in a cycle contributes no invented result. We select observed state-cycle entries when fitting and current eligible contests when forecasting. Special elections and caucus assignments follow the documented admission/seat ledger. A fully general two-contest-per-state joint model is not implemented.

## 2. Model family map

| Display label | Historical center / relationships | Distribution and inference |
|---|---|---|
| Gaussian Bayesian | Repaired historical centers, national momentum/approval, common movement plus signed state pattern | Exact joint Gaussian conditioning |
| Matched Student-t (df5) | Same final centers, fitted coefficients, variance budgets, loadings and calibration | Componentwise Student scales; Gibbs sampling |
| Older Gaussian | Earlier historical centers/calibration, national momentum/approval and common movement; no signed pattern | Exact joint Gaussian conditioning |
| Student-t research helper | Same older architecture as Older Gaussian | Earlier componentwise Student scales; Gibbs sampling |
| Empirical baseline | Polling average plus historical state polling-error correction; no economic regression term | Point estimate, with separate empirical residual calibration |
| Corrected / Plain percentage blends | Translate the final Gaussian toward the specified corrected/raw polling helper | Gaussian covariance retained |
| Four-model mixture | Fixed 25% weight on each of the four Bayesian distributions | Mixture of whole joint state vectors |
| Mixture + polling percentage | Translate that mixture toward the corrected polling point estimate | Entire centered mixture retained |

The older pair is not a controlled comparison with the final pair: centers and covariance construction changed. Compare Student with its corresponding Gaussian to isolate our tail experiment. The final Gaussian is the designated reference, not a universally superior model.

## 3. Inputs, units and the order of operations

There are three distinct operations:

1. **Prepare data:** identify contests/parties/samples, screen polls, build dated features, retain missingness and provenance.
2. **Fit from earlier cycles:** construct historical centers, estimate residual budgets and polling bias, learn feature coefficients/loadings, and choose permitted hyperparameters using earlier validation cycles.
3. **Infer this cycle:** condition the retained model on available current polling and current feature scores. In a live refresh the historical fits stay frozen, while polls and feature values can change.

Core notation:

| Symbol | Meaning | Units / size |
|---|---|---|
| c_s | Historical result-based center | pp, one per state |
| q_s | Current screened polling aggregate, if present | pp |
| M_s | Decayed pollster mass | dimensionless |
| d_s | Historical poll-minus-result bias estimate | pp |
| B_s | Uncertainty in that bias estimate | pp² |
| x_t | Standardized national momentum/approval scores | usually length 2 |
| β | Shared feature coefficients | pp per standardized score |
| V_s | Historical electoral residual variance budget | pp² |
| A | Common national residual variance | pp² |
| h_s | Signed-pattern loading, √λ times learned loading | pp |
| P_s | Systematic polling residual variance | pp² |
| F_s | Extra observation variance, B_s + 16/M_s | pp² |

Variance is the square of a standard deviation. An SD of 4 pp is a variance of 16 pp²; those are not interchangeable hyperparameters.

### Polls become one observation per polled contest

Candidate rows and question versions first become screened estimates for underlying samples. The selection policy handles LV/RV/adults, decided-only alternatives, duplicate samples and candidate matchups before modeling; see DATA.md.

For the Bayesian models, sample i receives weight

    a_i = 2^(-age_days_i / 30) / number_of_samples_from_its_firm_in_this_contest
    M_s = sum_i a_i
    q_s = sum_i a_i * margin_i / M_s.

This balances firms and discounts old samples. Reported respondent counts remain available for auditing, but the final Bayesian likelihood is **not** a binomial model of every respondent, and its freshness variance is not simply 1 / total respondents. It uses learned historical polling-error variance plus 16/M_s. Many polls from one firm do not become many independent firms.

If no admissible poll exists, q_s is missing and that contest has **no likelihood row**. Its forecast still comes from history, features and shared factors. Each refresh reconstructs the aggregate from the whole snapshot and conditions once; it does not reuse yesterday's posterior and feed yesterday's polls in again.

## 4. Construct historical centers and uncertainty separately

The final center starts from same-state earlier Senate results, weighted with a four-year half-life. It then adds a shrunk estimate of earlier errors of that chronological center:

    base_s,t = weighted mean of earlier same-state results
    error_s,u = actual_s,u - base_s,u       (base at u used only years before u)
    repair_s,t = sum_u w_u error_s,u / (sum_u w_u + 2)
    c_s,t = base_s,t + repair_s,t.

The older pair retains the earlier, unrepaired center/calibration. A recorded fallback handles missing usable same-state history. This is not an unconstrained state intercept fitted to the held-out outcome.

Electoral variance is learned from **errors relative to chronological centers**, not from whether a state usually votes for one party. A state can almost always vote Republican but still have variable margins. A tightly predicted winner and a tightly predicted numerical margin are different properties.

Training-cycle weights have an eight-year half-life and a 0.5 multiplier for the other cycle type (presidential versus midterm). This is a weighted/power likelihood. Penalized EM estimates residual covariance with missing entries and measurement noise, shrinking toward a pooled diagonal target. Its update has the form

    C_new = [sum_t w_t E(e_t e_t' | observed entries) + κ T] / [sum_t w_t + κ].

T is the pooled shrinkage target. Conditional second moments account for missing entries; missing election labels are not written into the dataset as known outcomes. In the final model, the resulting **diagonal budgets**, with selected state variance multipliers, feed the factor construction below. We do not install an unrestricted estimated 50×50 correlation matrix as the final prior.

Shared/local variance multipliers use earlier validation cycles and shrink local choices toward a shared choice. Unsupported signed loadings are zero. These safeguards matter because there are few observed elections per state. See MODEL.md for grids and regularization constants.

## 5. Learn national feature coefficients: what is W?

In this model the regression W is a short shared vector β, not 50 separate five-feature regressions. The final active inputs are **economic momentum** and **presidential approval**, oriented by White House party. Other collected features remain in the dataset but are not automatically active in this forecast.

Momentum combines sentiment, employment and cost-pressure blocks with fixed weights. Cost pressure includes inflation, price-index and gasoline changes. Changes use both January 1 and the previous October 31 anchors relative to the available cutoff. Rising costs have a negative governing-party orientation; White House signing translates that orientation into D-minus-R terms. It does **not** constrain the learned coefficient to be positive.

Ingredient scaling/clipping and fixed score weights are in `config/fixed_feature_scores_v2.json`. Score construction preserves missing required ingredients. The regression design then fills missing composite scores using the training weighted median, standardizes using training weighted mean/SD, and drops constant/all-missing training terms. Future observations/outcomes do not set normalizers. This distinction explains why prepared data can preserve NaNs while model input is finite.

For historical cycle t, define observed state residual vector r_t = actual_t − c_t and design matrix D_t whose every row is x_t'. Conditional on a common variance A,

    r_t | β ~ Normal(D_t β, Σ_t)
    Σ_t = diag(V_s − A + measurement_noise_s,t) + A 11'
    β ~ Normal(0, τ² I).

With cycle weights w_t, the Gaussian coefficient posterior is

    Vβ = [τ^-2 I + sum_t w_t D_t' Σ_t^-1 D_t]^-1
    mβ = Vβ sum_t w_t D_t' Σ_t^-1 r_t.

Only observed states enter each cycle block. National features are shared across states, so 35 races do not supply 35 independent economic histories. The common covariance limits how much repeated state rows tell us about national movement. At τ=0 the coefficients are fixed to zero rather than evaluating τ^-2 numerically.

A is fitted by profiling the integrated evidence over a bounded scalar interval. τ is selected from 0/1/3/6 on earlier cycles' chamber CRPS. The signed pattern is fitted **after** this feature/common fit and its strength selected separately; this is staged empirical Bayes, not joint sampling of every fitted quantity.

At the forecast's feature vector x,

    f = x' mβ                    (national feature mean, pp)
    FV = x' Vβ x                 (uncertainty about that mean, pp²).

Both enter inference. Live updates do not refit historical β, but current polls can update the implied latent shared movement through conditioning. A negative economic score need not imply a mechanically forced partisan shift: orientation and learned response are separate.

## 6. Final Gaussian: generative model and exact inference

Write independent prior components

    C ~ Normal(0, FV)             feature-coefficient uncertainty
    N ~ Normal(0, A)              residual common national movement
    Z ~ Normal(0, 1)              signed interstate pattern
    ε_s ~ Normal(0, L_s)          local election surprise
    L_s = V_s − A − h_s²
    θ_s = c_s + f + C + N + h_s Z + ε_s.

C and N can be combined into one Gaussian factor for computation. The loadings h may have opposite signs. They are learned from earlier residuals with regularization, a zero-sum constraint and magnitude limits; their allocation is subtracted from L so the state budget is not counted twice.

The prior vector is

    μ = c + f 1
    K = diag(L) + (A+FV) 11' + h h'.

For distinct states s,r, covariance is A+FV+h_s h_r. Opposite loading signs can reduce or reverse the association if strong enough. This is still only one common factor and one signed pattern: it cannot represent every possible political relationship.

Historical polling bias is defined as **poll minus result**. For example, d_s=+2 means polls historically overstated the Democratic margin by two points; we subtract it. Its Gaussian prior has SD 3 pp, and its posterior estimation uncertainty B is retained.

Let H select observed contests. The likelihood is

    y = q − d
    y | θ ~ Normal(Hθ, R)
    R = diag(P_s + B_s + 16/M_s) over observed states.

The released final specification has no signed common polling-error offset: the polling residual and bias covariance here are diagonal. State dependence is in the electoral prior. This assumption does not say national polling misses are impossible; it limits how they are represented.

Conditioning gives

    G = K H' (H K H' + R)^-1
    m = μ + G (y − Hμ)
    Cpost = K − G H K.

The code uses Cholesky solves rather than explicit matrix inversion. G is a matrix of sensitivities: element G_s,r tells how one extra point in observed contest r shifts state s's posterior mean, with fitted inputs held fixed. The **surprise relative to the prior**, not simply whether a poll is pro-D, drives the update. Several observed states must be considered jointly because their information overlaps.

With fixed K and R, the Gaussian posterior covariance depends on observation availability/precision, not the numerical polling margins. Student inference differs on this point because observed surprises can change inferred scales.

### Worked two-state example (illustrative, not real election data)

Suppose

    μ = [-2, 1] pp
    K = [[16, 6], [6, 25]] pp²
    only state A is polled: corrected y_A = +2 pp, R_A = 9 pp².

The surprise is +4 pp. The gain is [16,6]/(16+9) = [0.64,0.24]. Therefore

    m = [-2,1] + [0.64,0.24]*4 = [0.56,1.96] pp
    Cpost = [[5.76,2.16],[2.16,23.56]] pp².

State A mixes its prior and its poll. Unpolled B moves +0.96 pp because it is positively associated with A. A negative cross-covariance would reverse B's update. With zero cross-covariance, B would not move.

A's posterior SD is 2.4 pp, so P(D wins A)=Φ(0.56/2.4)≈59.2%. Its central 70% interval is approximately [−1.93,+3.05] pp. These numbers distinguish the predicted margin, uncertainty and win probability.

Run this from the standalone folder to reproduce the illustrative example:

```python
import numpy as np
from scipy.stats import norm
from election_lab import gaussian

mean, covariance, _ = gaussian.normal_update(
    np.array([-2., 1.]), np.array([[16., 6.], [6., 25.]]),
    np.array([0]), np.array([2.]), np.array([[9.]])
)
print(mean, covariance)
print("State A P(D):", norm.cdf(mean[0] / np.sqrt(covariance[0, 0])))
```

## 7. Older Gaussian: same conditioning, different construction

For the older pair, use its historical centers, feature fit and variance budgets; set the signed factor to zero:

    θ_s = c_old,s + f_old + C_old + N_old + ε_old,s
    K_old = diag(V_old − A_old) + (A_old+FV_old) 11'.

Use the same current polling evidence and the same Gaussian conditioning formula. Older and final models therefore share the mathematical update rule, but their prior means, variances, feature calibration and state relationships differ. A wider distribution in a safe Republican state can increase its D win probability even when its mean remains Republican. That helps explain why older models may have higher expected D seats without more positive-mean state calls.

## 8. Student versions: what changes and why inference needs sampling

A heavy-tailed residual is implemented through a random variance multiplier. For a Gaussian component whose variance was v, use

    S ~ InvGamma(ν/2, (ν−2)/2)     shape/scale convention
    e | S ~ Normal(0, v S),       ν=5.

The inverse-gamma density is proportional to S^(-a-1) exp(-b/S). E[S]=1, hence Var(e)=v. Equivalently, e has a Student-t distribution with scale sqrt(v*(ν−2)/ν). Using scale sqrt(v) in an ordinary t5 would inflate variance by 5/3 and would not be the intended controlled experiment.

For the **matched final Student**, give N, Z and each local ε_s their own scales. Keep C Gaussian. For the **older Student**, use the older architecture and omit Z. Both retain their corresponding Gaussian fitted centers/budgets/feature calibration; no Student-specific retuning is performed in this comparison.

Polling uses a separate scale shared across the polled contests:

    η | S_poll ~ Normal(0, S_poll diag(P))
    ξ ~ Normal(0, diag(F))
    y = Hθ + η + ξ.

Bias-estimation and freshness uncertainty stay Gaussian in ξ. Sharing a positive variance scale makes simultaneous large absolute polling misses more plausible, but does not impose that their partisan signs match. A national electoral factor, in contrast, produces a common directional shift. These are different dependence mechanisms.

At fixed scales, all components are Gaussian. Integrating the scales creates heavy tails. The sum of these components, and the posterior after polls, is **not generally a single multivariate Student distribution**. We cannot replace NormalCDF with a t CDF using the old posterior mean/SD and call that inference.

### Gibbs inference, one iteration

The sampler alternates exact conditional draws:

1. Given scales, integrate local residuals and draw shared factors (C+N,Z). This is a two-dimensional Gaussian conditional; the older model has just the common factor.
2. Draw state-local residuals conditional on those factors and the polls, giving one complete joint θ draw. Unpolled states retain their conditional local prior.
3. Split C+N into its Gaussian feature uncertainty and scaled national residual. Draw η conditional on y−Hθ and its extra Gaussian noise ξ.
4. Update scales from the residual draws. For a scalar component e of base variance v,

       S | e ~ InvGamma((ν+1)/2, ((ν−2)+e²/v)/2).

   For the shared polling scale with k observations,

       S_poll | η ~ InvGamma((ν+k)/2, ((ν−2)+sum_j η_j²/P_j)/2).

   Unobserved local scales can be drawn directly from their prior with the local residual integrated out. Zero/absent components are skipped.
5. Repeat after warmup; save joint margins and scale/factor diagnostics. Average conditional Gaussian means, second moments and win probabilities to reduce Monte Carlo noise (Rao–Blackwellization). Obtain intervals and chamber outcomes from the joint draws.

Eight chains start at 2,000 warmup and 4,000 retained draws each. They extend until max rank/split R-hat <1.01 and minimum bulk/tail ESS ≥400; failure prevents a completed result. This checks sampling, not whether the scientific model is correct. Fixing every scale at one recovers the corresponding Gaussian and is an implementation control.

A large residual can increase a polling scale and weaken that observation, or increase an electoral scale and permit a larger true movement. The posterior weighs those explanations jointly. Heavy tails neither guarantee wider central intervals at matched variance nor guarantee a shift toward either party.

## 9. Empirical baseline polling

This helper starts with a polling average whose half-life/prior-strength choices are tuned on the preceding cycle. For the 2026 checkpoint these are 30 days and zero prior strength. It then learns **result minus poll**, the opposite sign convention from d above:

    u_s,t = actual_s,t − polling_baseline_s,t
    correction_s = reliability_s * local_mean_s + (1−reliability_s) * shared_mean
    reliability_s = history_mass_s / (history_mass_s + shrinkage)
    helper_s = polling_baseline_s + correction_s.

It uses the last five calendar cycles with eight-year decay; the shared mean balances cycles. Shrinkage is selected on the preceding cycle, fitting only older outcomes for that selection. Unpolled contests retain their historical fallback instead of receiving this polling correction. The result is clipped to the allowed margin range.

Its own uncertainty is a pooled Gaussian approximation based on earlier out-of-sample prediction errors, requiring at least three calibration cycles. It is not a Bayesian posterior over its coefficients. Missing early uncertainty stays missing. Its own chamber distribution assumes independent states; that assumption is not imported into a mean-only blend.

The Plain helper omits this historical error correction. It is a useful polling reference, but no-poll fallback and aggregation/timing rules still matter: “plain” does not mean every candidate row gets equal weight.

## 10. Mixtures, translations and seats

For the four Bayesian predictive distributions, choose **one model for the whole state vector** with fixed weight 1/4. The joint distribution is p_mix(θ)=sum_k w_k p_k(θ). Its moments satisfy

    m_mix = sum_k w_k m_k
    C_mix = sum_k w_k [C_k + (m_k−m_mix)(m_k−m_mix)'].

The second term captures model disagreement. Mixing independently by state would change dependence; averaging corresponding model draws would generally reduce variance. Neither is our implementation. These are fixed forecast-combination weights, not posterior model probabilities estimated from evidence.

To blend with helper point vector h at weight α, translate each complete base draw:

    δ = α(h−m_base)
    θ_blend = θ_base + δ.

The mean becomes (1−α)m_base+αh. Centered draws, covariance and margin interval widths are unchanged. For a Gaussian base, Gaussian covariance is preserved; for the four-model base, **mixture covariance** is preserved. Changing winner thresholds can still change correlations/variance of binary wins and total seats. This is an empirical translation, not a second independent polling likelihood.

For each joint draw, count D wins plus continuing/fixed D seats. Expected seats equal fixed_D+sum_s P(θ_s>0); control is the fraction of full chamber draws with at least 51 D seats under the retained caucus/vice-presidential convention. Point seats count positive predicted mean margins. With asymmetric posteriors, positive mean and P(D)>50% need not always agree. Historical unmodeled races have documented fixed-completion assumptions, so chamber scores do not establish full forecast coverage of every contest.

## 11. What is learned, fixed or uncertain?

| Quantity | Treatment |
|---|---|
| Current θ, common movement and signed realization | Inferred jointly from prior and polls |
| Feature β | Gaussian posterior from earlier-cycle training, integrated via f and FV |
| Persistent polling bias | Historical Gaussian posterior; its mean and uncertainty enter the likelihood |
| Centers, variance budgets, A, signed loadings | Historical estimates, held fixed for current inference |
| Decay recipes, selection grids, regularization policy | Explicit design choices / earlier-cycle selection, not fully integrated random variables |
| Student scales | Inferred in each forecast; df fixed at 5 here |
| Four-model weights | Fixed 25% each, not fitted |
| Mean-shift weights | Fixed sensitivity grid, not learned from 2026 outcomes |

This is a partially Bayesian, empirical-Bayes workflow. It does not put a prior over every estimated hyperparameter or integrate uncertainty in architecture selection. Counting only the two feature coefficients understates the model's total complexity; counting 50 states times every feature overstates its regression complexity. There are derived state centers, regularized state budgets/biases/loadings, shared coefficients and latent current margins with different roles.

## 12. Validation, limitations and a learning route

Each historical target cycle is forecast using earlier outcomes. Hyperparameter choices use still-earlier validation forecasts. This is rolling-origin temporal validation, not random state-row CV. Repeated architecture experiments reused these years, so the resulting model comparison is exploratory, not an untouched final test set. Live 2026 has no labels and is never included in historical scores.

Historical economics often use revised rather than real-time data; some old poll release dates are unknown. Candidate proxies and election rules have documented restrictions. Gaussian/Student margins are unbounded mathematical approximations, although vote margins are bounded. Sparse states lean more heavily on assumptions. These limitations remain after good numerical convergence and clean-data audits.

Suggested learning sequence:

1. Reproduce the two-state example above; set cross-covariance to zero/negative and remove the poll.
2. Inspect notebook03 to connect saved historical fits to centers, budgets and β.
3. Compare final Gaussian with matched Student in notebook06. Verify means/covariance before polling match, then inspect posterior changes and central intervals.
4. Compare the older pair in notebook07; distinguish architecture changes from tail changes.
5. Use notebook08 to distinguish a predictive mixture from a covariance-preserving translation.
6. Use notebook04 for a cached live update; inspect source dates separately from the forecast timestamp.

### Implementation map

| Topic | File / function |
|---|---|
| Supported CLI and live orchestration | `run.py`; `election_lab.py:live_forecast`, `refit_main` |
| Poll aggregation / Gaussian conditioning | `scripts/simple_bayesian_polling.py:aggregate`, `normal_update` |
| Center repair / variance selection | `scripts/prior_center_repair.py:histories`, `choose_scales` |
| Missing-data covariance fitting | `scripts/bayesian_revision2.py:blocks`, `fit_covariance` |
| Historical fixed-common polling fit | `scripts/simple_national_model.py:fixed_common` |
| Scores and normalization | `scripts/feature_scores.py`; `scripts/recency_state_baselines.py:WeightedScoreDesign` |
| Shared regression and older Gaussian | `scripts/national_feature_prior.py:regression_at_a`, `fit_feature`, `predict` |
| Final signed factor | `scripts/signed_state_factor.py:learn_loading`, `predict` |
| Matched Student | `scripts/matched_student.py:inputs`, `chain`, `sample`, `control` |
| Older Student | `scripts/combined_student_model.py:inputs`, `chain`, `student_predict` |
| Paired alternative orchestration | `scripts/release_alternatives.py:older_pair`, `matched_tail` |
| Corrected polling | `scripts/state_poll_bias.py:fit_bias` |
| Mixture and mean shifts | `scripts/model_portfolio.py:make_mixture`, `distribution_rows`, `weighted_seats` |

Use supported `run.py` commands or notebook functions. Some inherited research modules retain old experiment builders; the standalone API supplies portable inputs instead of relying on those builders' old research paths.

The separate [poll-weight experiment](POLL_WEIGHT_EXPERIMENT.md) and notebook09 compare alternative averaging rules without changing these reference models.
