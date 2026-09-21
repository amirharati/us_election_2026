# Model specification

For a step-by-step teaching reference, including coefficient fitting, a worked
two-state update and Student Gibbs inference, start with [MODEL_WALKTHROUGH.md](MODEL_WALKTHROUGH.md).

## Model identities and roles

| Role | Research identity | Definition |
|---|---|---|
| Main | `repaired_both__selected` | Gaussian state forecasts, repaired historical centers, national momentum/approval mean, common movement and one signed state factor |
| Point/probability helper | `bias` | Tuned polling aggregate plus decayed historical state polling error; own pooled residual uncertainty |
| Older Gaussian alternative | `both` | Earlier centers/calibration and common national factor, without the signed state pattern |
| Older fat-tail helper | `both__t5v1` | Actual research Student-t electoral and polling residual model, df 5 and variance multiplier 1 |
| Matched fat-tail helper | `final_gaussian_matched_componentwise_t5` | Final Gaussian centers, budgets and signed pattern retained; Student residual scales |
| Predictive ensemble | `Four-model mixture` | Fixed 25% mixture of the four complete joint Bayesian distributions |
| Ensemble mean shifts | `Mixture + polling` percentages | Translate mixture means toward corrected polling, preserving mixture covariance |
| Sensitivities | Corrected/Plain blend percentages | Translate main-model means toward the named helper; preserve main-model covariance |

The older Student helper predates the repaired centers and signed factor. It has its
original historical prior and national feature term. It is **not** the final main
architecture with one Gaussian-to-Student substitution. This distinction is
preserved because the matched final-model Student is a separate experiment;
see [MATCHED_STUDENT.md](MATCHED_STUDENT.md).

## Units, targets and observations

One admitted Senate contest per state/cycle is modeled. Internal Gaussian
margins and scales use percentage points (pp). Some historical tables store
fractions; conversions are explicit: `prediction_pp = 100 * prediction`.
Targets use the recorded D/R shares' denominator, not a silent two-party
renormalization. No 2026 outcome enters training, validation or scoring.

An election cycle is an even year. States absent from that year's Senate
election contribute no fabricated label. Historical general-election admission,
special-election mapping and physical-seat accounting are retained from the
audited data. Current forecasts cover 35 contests plus 65 continuing seats.

## Poll aggregation

Poll question/candidate rows first become one screened estimate per underlying
sample. Full-sample estimates take priority over decided-only/follow-up versions;
population preference is LV, RV, voters, adults, unknown. Tied acceptable versions
are averaged. Hypothetical matchups, superseded records, post-cutoff observations
and known late releases are excluded. Unknown historical publication dates are
explicitly retained as a limitation.

For the main model, sample weight is proportional to

`2^(-age_days/30) / number_of_samples_from_that_firm_in_the_contest`.

The weighted mean is `q_s`; total weight is `firm_mass_s`. Polls are rebuilt from
the complete snapshot on every update; a revised or repeated poll is not added
again to an old posterior. No-poll states remain in the state vector but have no
likelihood row. The freshness variance term is `16 / firm_mass_s`, in pp².

## Historical state prior mean

The main recipe is `decay4_centered`:

1. Average earlier admitted same-state Senate outcomes with a four-year half-life.
2. Estimate earlier errors of that chronological prior, also with four-year decay.
3. Add their weighted sum divided by total weight plus 2 (shrink toward zero).
4. Retain the documented fallback if no admitted same-state result exists.

Each historical row is constructed using only outcomes preceding that row's
cycle. The correction learns drift/miscalibration of the historical center;
it is separate from the polling-error correction below.

## Training relevance and marginal variance

Electoral residuals are final result minus chronological prior. Poll residuals
are poll aggregate minus final result. Training-cycle relevance uses an eight-year
half-life and weight 0.5 for the other cycle type (presidential versus midterm).
Missing state/cycle entries remain missing. Effective national evidence is a
small number of cycles, not hundreds of independent national-feature examples.

The historical covariance routine uses penalized EM with missing observations
and measurement noise. The final main recipe takes its **diagonal variance
budgets**, then constructs the explicit factor covariance below. Movement
regularization is kappa 8. Prior variance multipliers are drawn from
0.25/0.5/1/2/4; a shared choice and local choices use the last three earlier scored
cycles, with local multipliers shrunk toward the shared multiplier in log space.
The local reliability is weighted evidence mass divided by mass+2.

Polling variance regularization is retained per fold from earlier research
selection. Its diagonal budget receives an additional 4 pp². Historical polling
bias has a zero-centered Normal prior with SD 3 pp. The main final specification
sets the explicit common polling-error covariance to zero; uncertainty in local
bias estimates remains in the observation covariance.

## National features and their coefficients

The main model uses two fixed composite scores: **economic momentum** and
**presidential approval**, signed according to the White House party so that
their orientation is D-minus-R. Exact ingredients, directions, fixed ingredient
weights, clipping and missingness rules are in `config/fixed_feature_scores_v2.json`.

Levels and changes are dated to the forecast cutoff; changes include the
election-year January 1 and prior-year October 31 anchors. Inflation/gasoline use
proportional index changes where specified. Source selection uses completed
reference periods, never future months. Historical feature values are generally
latest revised, not a fully reconstructed real-time vintage.

Feature normalization is fitted only on training cycles. Ingredient values use
training-weighted centers/SDs and fixed score recipes. Composite missing values
use the training weighted median, then weighted mean/SD scaling. All-missing or
constant training terms are dropped. Normalizers are frozen for live 2026 updates.

Let `x` be the active standardized scores. Coefficients have a Normal prior
`beta ~ N(0, tau² I)`. Their conditional posterior is integrated analytically.
Tau is chosen from 0/1/3/6 using the last three earlier cycles' chamber CRPS.
For the packaged 2026 main fit tau=6; two active coefficients are used.
Neither coefficient signs nor the current forecast are forced toward a party.

## Main joint prior and likelihood

For contest s, write

`theta_s = historical_center_s + N + sqrt(lambda) * b_s * Z + epsilon_s`.

- `N ~ Normal(f, g)`, where `f = x' E[beta]` and
  `g = a + x' Cov(beta) x`.
- `Z ~ Normal(0,1)` is one additional signed pattern.
- `epsilon_s ~ Normal(0, V_s - a - lambda*b_s²)` independently.
- `a` is the fitted common national residual variance and `V_s` the calibrated
  state variance budget. All quantities here use pp or pp² consistently.

Thus

`mu = historical_center + f`

`K = diag(V - a - lambda*b²) + g*11' + lambda*b*b'`.

The common component can move all states together; the signed pattern permits
states to move in opposite directions. Loadings are fitted from earlier-cycle
residuals conditional on their feature means, with ridge 4, a zero-sum constraint,
standardized magnitude bound 0.95 and at least three observed state cycles.
Unsupported states get zero signed loading. Lambda is selected from 0/0.1/0.25/0.5
using the last three earlier cycles' mean weighted interval score. In 2026 it is 0.5.
Covariance is not an unrestricted empirical 50×50 correlation table.

Let H select currently polled contests, b_poll be the historical polling-bias
posterior mean and R include polling residual variance, bias uncertainty and
the freshness term. Then

`y = q - b_poll`, `y | theta ~ Normal(H theta, R)`.

The posterior is the exact Gaussian conditional:

`mu_post = mu + K H' (H K H' + R)^(-1) (y - H mu)`

`K_post = K - K H' (H K H' + R)^(-1) H K`.

The implementation uses Cholesky solves. Unpolled states can update through
cross-state covariance. Empirical-Bayes covariance, loading and selected
hyperparameter uncertainty are not fully integrated.

## Non-Bayesian helper

Current-cycle polling averages choose half-life 30/90 days and prior-strength 0/2
using the preceding cycle. A state error correction uses the last five calendar
cycles, eight-year decay anchored at Y−2, and local state means shrunk toward a
cycle-balanced shared error. Shrinkage0/1/3/10 is selected on Y−2 using older
training data. Polled cases receive the correction; unpolled cases retain the
historical fallback. The 2026 checkpoint selected shrinkage 0.

Its own forecast SD is the square root of the cycle-balanced historical squared
prediction errors, fitted only on earlier evaluated cycles (minimum three).
This is an approximate pooled Gaussian error model, not a Bayesian posterior.
Own chamber probabilities assume independent states and are labeled accordingly.

## Student-t helper

The research sampler uses df 5 variance-standardized inverse-gamma scale mixtures
for local electoral residuals, the common national electoral residual and polling
error. Feature-coefficient uncertainty remains Gaussian; historical calibration
is empirical Bayes. A shared polling scale allows a generally noisier polling
cycle without introducing a signed common polling-error offset.

The sampler uses eight chains, at least 2,000 warmup and 4,000 retained draws per
chain. Runs extend if needed until maximum split/rank R-hat<1.01 and minimum
bulk/tail ESS≥400. A zero-heavy-tail Gaussian control is tested analytically.
Historical saved output can be viewed quickly; the training notebook reruns the
actual sampler. Live forecasts rerun it unless explicitly skipped.

## Blends and seat totals

For a user-specified helper weight w:

`mu_blend = (1-w)*mu_post + w*mu_helper`

`draw_blend = draw_Bayesian + (mu_blend-mu_post)`.

Full Gaussian Bayesian **margin** covariance and interval widths remain unchanged.
Thresholding margins into winners can change seat-count variance and correlations.
This is an empirical forecast translation, not a posterior obtained by lowering
prior precision. It reduces prior pull on the mean only indirectly; helper
corrections/fallbacks also retain history.

The grid is a sensitivity experiment, not outcome-based current-cycle tuning.
September shows only tiny MAE gains at low weights; October improves through 50%
with diminishing gains. A time-varying schedule has not been validated.

State P(D)=NormalCDF(mean/SD) for Gaussian/blends; Student probabilities integrate
its conditional draws. Thirty thousand paired joint Gaussian simulations give
total seats and control probabilities. Totals include continuing seats.
Historical unmodeled contested seats retain explicit fixed-completion assumptions.
Candidate/caucus proxies, runoffs and ranked-choice limitations remain visible.

## Matched final-model Student experiment

The new [matched Student specification](MATCHED_STUDENT.md) and [results](MATCHED_STUDENT_RESULTS.md) hold this final Gaussian architecture fixed while changing residual distributions. It is separate from the older helper above and does not replace the main model.
