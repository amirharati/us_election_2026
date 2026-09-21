# Model decisions and assumptions

Agreed in discussion on 2026-09-14. This specifies the intended small lab;
implementation and empirical tuning come after data review.

## Target, training population and missing data

Predict the **joint distribution of election-day Senate outcomes**, then the
distribution of total seats and caucus control. Use historical Senate contests
across all 50 states to learn shared parameters and partially pooled state
effects. In 2026 infer only the 35 contested seats, including FL/OH specials;
add the 65 continuing seats directly. A historical training record is a contest
in a cycle, with seat/special-election and stage distinctions, not merely a state.

No election means no prediction target. An election without polls is still a
target. The same model must handle zero, few and many polls: omit missing
observations from the likelihood; update a state prior with available evidence;
borrow information through shared parameters and national factors. Do not use
zero or a previous election result as a fake current poll. More polls reduce
poll-specific uncertainty but do not eliminate shared polling error or future
movement. No-poll predictions retain substantial state-specific uncertainty.

Include historical results from unpolled races when learning priors. A
poll-only training sample overrepresents the contests that attract polling.
Historical data informs (1) priors for margins, (2) error calibration, and
(3) hyperparameter selection on separate validation cycles. These are distinct
uses within one model, not permission to count old observations twice.

## Inputs and scope

Core observations: Senate general-election polls. Core prior input: **lagged**
state presidential results, expressed as state margin minus national margin,
plus partially pooled state effects. Past Senate results train this relationship;
the usefulness of the previous same-seat margin can be checked later. A result
from the election being forecast must never enter its own prior.

Include an explicit presidential-year/midterm indicator in the mean and allow
shrunken differences in national/state error scales. Do not fit unrelated models
for the two election types. If modeling a penalty for the president's party,
include party orientation and its interaction with midterm status. Do not assign
a fixed penalty or assume midterms have higher variance before validation.
Odd-year specials and January runoffs need explicit cycle mapping; blindly
using calendar year modulo four is wrong for a runoff of a prior-cycle election.

National generic-ballot polls are an **optional extension**, collected separately.
An uncertain latent national climate G can enter state mean predictions. G is
not the arithmetic average of state Senate margins, and is not itself a seat.
Distinguish its uncertainty from residual national polling bias. Do not add the
same national uncertainty twice. Other offices' individual polls, regional
factors, elaborate pollster ratings and demographic models are out of the core
lab scope. Pollster effects are a later extension if basic calibration requires them.

## Proposed small generative model

For cycle t and state/contest s, let M_st be the election-day Democratic minus
Republican margin in percentage points for an ordinary D/R contest. Start with
a fundamentals prior, conditional on shared coefficients and state effects:

    M_st ~ Normal(x_st beta + a_s, tau_prior^2)
    a_s  ~ Normal(0, tau_state_effect^2)

x includes lagged partisan lean, election type and the specified party interaction;
G is added only in the optional extension. Partial pooling is essential because
there are few elections per state. Candidate/independent exceptions below are
handled before using this scalar margin representation.

For polls in a recent window around a forecast cutoff h days before election:

    y_sti = M_st + B_t(h) + U_st(h) + epsilon_sti

B is shared across the election; U is shared by polls in one state race;
epsilon is poll-specific noise. The combined polling-to-result discrepancy
includes later movement as well as measurement error. Means/biases and scales
are learned from earlier cycles, with shrinkage. Do not assume a consistent
partisan bias or estimate each cycle's shock from its held-out results.

Sample sizes inform epsilon, but nominal sampling error alone is insufficient:
account for an estimated noise floor and avoid treating correlated samples,
multiple questionnaire versions or repeated tracking windows as independent.
A reported margin of error for one candidate's share is not automatically the
standard error of a D-minus-R margin. Unavailable sample sizes need a documented
conservative noise convention, not dropped races or infinite weight.

At first use a simple, historically validated recency window; do not treat an
entire campaign's polls as observations of a constant level. Calibrate errors
at comparable forecast horizons and allow greater uncertainty farther from
election day. Window/noise choices are shared between distribution variants.

## Covariance and Gaussian versus Student-t

The state-error vector E_t = B_t 1 + U_t has a structured covariance:

    Sigma_t(h) = tau_N,c(h)^2 1 1' + diag(tau_s,c(h)^2)

c is election type. State scales should initially be shared or strongly pooled,
not independently estimated from a handful of elections. This one-factor
structure produces positive cross-state correlation. It is a simplifying
assumption; freely estimating a full 35x35 matrix is not justified by our small
number of cycles. The forecast posterior also contains uncertainty in M, state
effects and coefficients; Sigma is not all of posterior uncertainty.

Compare the **same mean/prior/features/noise treatment** with two residual laws:

    Gaussian:  E_t ~ MVN(bias_t, Sigma_t)
    Student-t: E_t ~ MVT_nu(bias_t, ((nu-2)/nu) Sigma_t), nu > 2

The factor rescales the t shape matrix so both residual laws have covariance
Sigma. Default candidate nu=5, with a small predefined validation grid later.
No claim that equal numeric Gaussian SD and t scale imply equal variance.

An equivalent t construction is Z_t ~ MVN(0, Sigma_t), Q_t ~ chi-square(nu),
E_t = bias_t + sqrt((nu-2)/Q_t) Z_t. One Q per whole election creates joint
high-variance episodes. This is **not** independent univariate t draws for each
state, nor the same model as independent t national and state components.
These alternatives have different tail dependence; keep one definition fixed
for the first comparison. Given polls and a Gaussian prior/noise, the resulting
posterior is not generally exactly a multivariate t. The earlier conversational
Normal-versus-t predictive formula was schematic; inference must follow this
generative model, not assume a conjugate t posterior.

Learn scales using training data and tune on validation cycles. An equal-covariance
sensitivity comparison isolates tail shape; an independently calibrated comparison
tests practical predictive performance. Label these two experiments separately.
Heavy tails need not always widen every central interval or increase a particular
party's control probability.

## Shock motivation and limits

The user cited COVID and war around 2020/2022 as **external-shock analogies** for
2026. This is motivation for sensitivity analysis, not a claim those years had
proven heavy-tailed polling errors. Political turbulence, bias, higher variance,
nonstationarity and heavy tails are different possibilities. Keep both quiet and
surprising cycles; do not cherry-pick years that favor a t model. Election-wide
tail parameters remain weakly identified with relatively few independent cycles.

## Clarified role of extraordinary events: uncertainty and tails

September 17, 2026: the user's main hypothesis is that an extraordinary-event
regime makes **unusually large forecast errors more likely**, without necessarily
pushing expected vote margins in a consistent partisan direction. The OR flag and
its four-year memory are candidate conditioning inputs for the **residual/error
distribution**, not merely another mean predictor. The raw vote-margin correlations
in feature notebook Section13 do not test this hypothesis; they remain data checks.

Keep two possibilities distinct:

1. **Scale change:** event periods have a larger residual covariance/variance, even
   under Gaussian errors. This alone can increase absolute tail exceedances.
2. **Tail-shape change:** event periods have more extreme residuals relative to
   their typical scale, for example lower Student-t degrees of freedom.

When modeling starts, compare a constant-uncertainty baseline, event-dependent
scale, and a parsimonious event-dependent-tail candidate with shared mean/selection
rules. A Student-t candidate can use nu(z) with nu>2 and the covariance-matching
factor already specified above; changing nu without that factor also changes
variance and would confound the equal-covariance tail comparison. The proposed
heavier event regime is a hypothesis to assess, not an imposed empirical finding.
Do not initially fit unrelated distributions or many tail parameters per event
category. Strong regularization/fixed sensitivity scenarios may be more defensible
than learning separate tail parameters from a handful of election cycles.

The national event condition should govern a **shared cycle-level shock/scale**
within the joint state model. Repeating its flag over states/polls does not produce
independent evidence about an event regime or justify independent per-state shocks.
WH-party orientation is relevant to directional mean and asymmetric-tail effects.
The user clarified that event effects need not be symmetric: a shock may shift the
expected margin, change the scale/tail weight, and make one-sided extreme errors
more likely. Four-year carry may cross administrations; it does not by itself assign
blame or impose a penalty for the current president's party.

The Gaussian and ordinary Student-t distributions above remain **symmetric baseline
models**, not a requirement that the real event-conditioned distribution be symmetric.
Moving the mean does not introduce skewness about that mean. If justified later,
compare a small asymmetric extension, such as an asymmetric shared-national-shock
mixture or skewed-t specification, against those baselines. Keep mean, scale, tail
weight and skewness conceptually distinct; do not fit many unconstrained event-regime
parameters from the small cycle sample. A party-relative direction may be encoded
with WH-party interactions without assuming in advance that every shock hurts the
incumbent. The user's hypothesis allows direct and distributional effects together;
no asymmetric distribution or parameterization has yet been selected.

Later diagnostics should use residuals from fixed/earlier-cycle-trained forecasts
at comparable horizons: signed bias, absolute error, calibrated interval coverage
and standardized extreme-error frequency. A larger average absolute error alone
does not establish heavier tails. Evaluate by whole cycles and preserve previously
explored-outcome restrictions. Predictors must be available at the forecast cutoff;
no future shock labels may enter an earlier forecast.

Current information is limited: the broad OR proxy is1 in12 of14 national-outcome
cycles, and the zero labels include2008 under its particular threshold/cutoff.
This makes regime contrasts weakly identified and reiterates that the numeric proxy
is not a comprehensive crisis label. Do not tune event definitions using forecast
errors to manufacture a tail result. Missing event flags remain unknown until the
model's missing-feature treatment is specified. No tail parameters/model have been
fit or chosen by this clarification.

## Seat mapping and election exceptions

Simulate one joint vector per election, determine winners, then add continuing
seats. Report expected seats, median/intervals, the full seat distribution and
control probability, with separate party and caucus totals.

The 2026 baseline is 31 continuing R, 32 continuing D, two continuing independents
currently caucusing with D. Do not silently label a new independent winner as D.
Independent caucus choices require explicit assumptions/sensitivity scenarios.
Audit multi-candidate, ranked-choice and runoff rules; a positive D/R margin is
not a universal winner rule. The dated leading-contender review supports a
matchup screen but is not a certified complete ballot. Full-chamber forecasts wait for these exceptions
to be resolved; do not silently drop the affected contests.

## Evaluation and anti-leakage rules

Update after the notebook's multi-cycle data review: the user requested explicit
2020/2022 poll-average versus outcome comparisons, followed by 2024 after archive recovery. Section 11 also compares every national House cycle from 1998–2024 across window choices. Those cycles have now been
explored and must not be called untouched test data. Any later evaluation on
them is retrospective; freeze the modeling protocol before scoring and report
the exploration. Reserve genuinely uninspected data for a fresh test if available.

- Hold out entire later election cycles; use rolling-origin training/validation.
  Hyperparameters, priors, features and poll selection must respect each cutoff.
- Evaluate margins with predictive log scores/interval coverage; winners with
  Brier/log scores; seat totals with predictive intervals and proper scores.
  Report presidential and midterm performance separately.
- Test naturally unpolled races and controlled masking/downsampling of polls.
  Masking alone does not reproduce the selection mechanism of unpolled races.
- Historical ratings computed after an election leak information; do not use
  retrospective pollster grades in a supposedly contemporaneous backtest.
- Field dates are not release dates. Record their availability and label a
  field-date-only historical backtest as approximate. Today's revised historical
  archives cannot reconstruct exactly what was published at past cutoffs.
- Check how many independent races/cycles remain at each horizon, not just poll
  rows. Source-linked final results must not be used to select nominees with
  hindsight without acknowledging the selection bias.

## Implementation order

Data acquisition and a conservative preparation pipeline are implemented. Read
[PREPARATION.md](PREPARATION.md) and its audit report before fitting. The initial
split tables retain the original training-through-2016 / validation-2018 / test-2020–2022 labels for provenance, but those later outcomes (and 2024) have now been explored. They are not untouched tests. Use the expanded normalized archives described in [DATA_GAPS.md](DATA_GAPS.md), replace the legacy-only window inputs, and agree on a new evaluation protocol before fitting. Resolve remaining contest/ballot exceptions before seat
simulation. Then
build the transparent Gaussian baseline and Student-t variant. No MCMC, fitting,
forecast UI or production refresh service is part of the present task.

## Recent-history priority (September 16 update)

Use [policy v1](ANALYSIS_POLICY.md) for the next diagnostics: primary reporting on
2016–2024, older eligible cycles retained in earlier-cycle training for priors/tuning
and separate sensitivities. No temporal decay selected yet. New national labels use
the audited first-choice references for 2022/2024; old exploratory tables keep their
recorded versions. Next compare firm-count weights across cycles before fitting.

Cross-cycle weighting follow-up: Section 25 finds a recent national equal-firm MAE
improvement but negligible/mixed Senate effects. No exponent is adopted. Return to
[the data-quality checklist](DATA_QUALITY_CHECKLIST.md), starting with a recent contest
and exclusion census, before interpreting this as a full Senate calibration sample.

## Preparation acceptance and next discussion

Section 31 assembles reviewed history, refreshed current polls, canonical survey identity and basis/availability metadata in a frozen accepted bundle. [Acceptance](PREPARATION_ACCEPTANCE.md) is for diagnostic and feature-analysis use with explicit restrictions, not complete seat-model readiness. The official 100-seat ledger reconciles to 65 continuing plus 35 contested; RCV/runoff/candidate/caucus handling remains a forecast gate. [Feature discussion](FEATURE_DISCUSSION.md) comes next, before fitting or freezing the revised retrospective protocol. Incumbency/open-seat status and lagged same-seat performance are discussion candidates, not adopted features.


## Implemented first baselines — September 17, 2026

[BASELINE_MODELS.ipynb](BASELINE_MODELS.ipynb) now implements the user's simpler
preliminary comparison before the correlated/heavy-tail model above. Separate
current-cycle poll EWMA and additive ridge residual models share an explicit
historical-outcome starting point; no current poll/economic-feature blending,
interactions, residual covariance or uncertainty model is fitted yet. Tune on the
immediately preceding cycle only; fit feature candidates on still-earlier cycles,
then refit the selected model on all older labels. Training-only missingness and
normalization rules are applied per fit. Older outcomes remain in priors/training.

[Method, saved run and results](BASELINE_RESULTS.md) document grids, source/sample
filters, historical/presidential fallbacks, weak national tuning sample size and
retrospective-data limitations. A previous state result can be another seat or
candidate; large no-poll fallback errors are now visible diagnostics. The feature
model is deliberately additive; WH × economic conditions is deferred. Current
outputs are point margins, not calibrated winner/seat probabilities.


## Contextual ridge extension — September 17, 2026

[Notebook Sections 10–14](BASELINE_MODELS.ipynb) add a controlled comparison of
additive levels, WH-sign × level interactions, and interactions plus changes since
election-year January 1 and previous-year October 31. Changes are computed before
training-only imputation/scaling; interactions use training-standardized values.
The small common alpha grid is .1/1/10/100, tuned on Y−2 only with earlier inner
training, then refit on all older outcomes. No predetermined coefficient signs.

Separate October31 historical evaluation from a matched-live calendar that caps
current data at its actual cutoff. There is no 2026 October31 prediction before
that date. The existing closed-reference-month and historical-vintage limitations
remain explicit. Source snapshots are unchanged; dated endpoints are run artifacts.
[Results and verification](CONTEXTUAL_BASELINE_RESULTS.md) show mixed performance:
context improves some Senate comparisons but richer national/change models are
unstable. Retain all variants as diagnostics; no winner was selected by matching
2026 polls. Residual uncertainty, correlation and seat aggregation remain pending.


## Explicit rolling CV report

[Notebook Sections 15–17](BASELINE_MODELS.ipynb) now expose the existing chronological
outer folds and last-cycle inner holdout, with a fixed minimum of six distinct
inner training cycles before Y−2. Refit on all older labels after tuning, then score
Y. Earlier default/warm-up forecasts are diagnostic only; 2026 has no scored outcome.
National qualifying tests begin2012; Senate tests begin2002 within the existing
evaluation range. All three calendar protocols and target coverage remain separate.
[Per-cycle results and audit](CYCLE_CV_RESULTS.md) preserve unchanged predictions;
this is not shuffled or multi-fold inner hyperparameter CV.


## Winner classification diagnostics

Notebook Sections 21–24 convert existing out-of-time margin predictions into
D/R calls for the prior, polling and every regression variant. No refit or
classification-specific tuning. Exact-zero predictions are uncalled; actual ties
and unknown outcomes are excluded. All-target, common-polled and no-poll scopes
are kept separate. Per-cycle counts, confusion matrices and final-|margin|≤5pp
descriptive subsets accompany margin errors. National calls concern the House
popular vote, not control; current calls are unscored and retain election-rule
restrictions. See [results and definitions](WINNER_CLASSIFICATION.md).


## Historical competitiveness screen

Notebook Sections25–27 evaluate unchanged CV forecasts on a state subset selected
using only Y−6,Y−4,Y−2 admitted Senate outcomes. Require two distinct cycles and
at least one absolute margin≤10pp; 5pp is a sensitivity. Missing history remains
unknown, and national House vote-leader scores remain separate. All earlier
training data and tuning are unchanged. See [method and results](COMPETITIVE_STATE_EVALUATION.md).


## Current primary outcome scope: Senate at both levels

User confirmed state-by-state and national-level Senate analysis. Primary views
are state/contest forecasts plus equal-contest mean Senate margins for each cycle;
see [scope and definitions](SENATE_PRIMARY_RESULTS.md), notebook Sections28–30.
House national analysis is auxiliary only. Aggregate the same Senate targets for
every model and observed result, with coverage and state errors alongside the
mean. This is not vote-weighted popular vote or control, not an independent new
training sample, and not a new national regression fit. Existing flagged prior
fallbacks and candidate/rule exclusions remain explicit.


## Fixed four-input summarizer (preparation only)

Notebook Sections32–35 now summarize economic conditions, economic momentum,
presidential approval and one unsigned disruption OR flag. Economic/approval
inputs use WH-party orientation; ingredient weights are fixed, and only
normalization statistics are estimated from earlier cycles. Raw NaNs and
component provenance remain explicit. No new regression is fitted. See
[the recipe, coverage and next experiment](FIXED_FEATURE_SCORES.md).


## Executed four-score correction

Notebook Sections36–39 now fit a Senate prior correction using the fixed v2
economic conditions, momentum, approval and disruption scores. Inner validation
is Y−2; normalization and median imputation are fitted within each fold, followed
by refitting on all earlier outcomes. Equal-cycle residual fitting uses at most
five parameters. Recent margin error improves slightly over prior, but winner
accuracy declines; polling remains stronger. [Results and audit](FOUR_SCORE_MODEL_RESULTS.md).

## Standardized and single-factor comparisons

Notebook Sections41–44 retain the original model and add five variants: all four
scores standardized, plus conditions-only, momentum-only, approval-only and
disruption-only corrections. After training-cycle median filling, selected
nonconstant scores are centered and scaled to population variance one within
each inner/final training fold, including variable binary disruption. Raw scores
and equivalent raw coefficients remain available. The cycle-balanced residual
target is unchanged; alpha is selected independently for each variant on Y−2.
The combined model has at most five electoral parameters; single-factor models
have at most two and fall back to intercept-only when their factor is constant.
Recent tests show little change from scaling and no feature-model winner-accuracy
gain over prior. No new model is automatically promoted based on these explored
test cycles. [Methods, results and verification](STANDARDIZED_SCORE_MODEL_RESULTS.md).

## State-specific coefficients with partial pooling

Notebook Sections45–48 extend the shared four-score correction to jointly fitted
state intercept/slope deviations. The same national inputs and training-cycle
scales apply across states; deviations shrink toward shared coefficients. The
objective preserves equal total loss weight per cycle and adds separate penalties
for shared slopes and state deviations. Each model tunes both penalties on Y−2,
then refits all older outcomes. A state-intercept-only control distinguishes
persistent state bias from different feature responses. Unseen states use the
shared correction. Both nominal parameter counts and conditional effective degrees
of freedom are retained; this is no longer a five-parameter model. See
[method, state histories and results](STATE_SCORE_MODEL_RESULTS.md).

## Polling-error regressions

Notebook Sections49–52 change the regression offset from the historical state
prior to its chronological polling forecast. Rebuild historical polling forecasts
using only their own previous-cycle tuning; only polled contests train/receive a
correction. No-poll targets keep the existing prior fallback. Twelve existing
regression variants retain their feature recipes and train-only preprocessing,
with Y−2 polled-contest MAE for penalty selection. Six polled inner cycles are
required, so fitted CV begins later than the prior-correction experiments. Show
with-polls results first and identical-target all-state/competitive views alongside.
No automatic selection across variants from outer-test results. See
[methods, rolling coverage and results](POLL_ERROR_MODEL_RESULTS.md).

## Direct state regression and recency controls

Notebook Sections53–56 compare direct final-margin regression with prior/polling
residual targets using the same partially pooled state architecture and four inputs.
Equal weights, 8-year and 16-year half-lives retain older history; cycle weights
have mean one and also govern training-only preprocessing. A separate strategy
selects half-life and penalties on Y−2. Date-range and identical-polled-history
prior controls help separate older training data from coverage and offset changes.
All comparisons use common eligible outer cycles, while direct/all-history prior
fits retain earlier outcomes. Direct predictions contain no prior/polling offset;
unseen states receive flagged shared predictions without learned state lean.
See [method, effective training support and results](RECENCY_DIRECT_MODEL_RESULTS.md).

Sections 57–59 apply the existing historical competitive-state screen to these same forecasts. Training and tuning remain unchanged; compare both horizons, 10/5-point thresholds, state results and unknown-history coverage. [Focused results](COMPETITIVE_RECENCY_RESULTS.md).

## Momentum-only architecture and historical decay

Baseline notebook Sections61–64 hold the fixed economic momentum score and chronological polling baseline constant while comparing shared intercept/slope with partially pooled state intercept/slopes. Equal/8-year/16-year cycle weights and a Y−2-selected strategy govern both preprocessing and regression loss; no-poll fallbacks stay unchanged. See [methods, validation and results](MOMENTUM_RECENCY_RESULTS.md).

## Historical state polling-bias calibration

Notebook Sections65–68 estimate actual-minus-polling errors using all history or the previous3/5calendar cycles, with equal/8-year/16-year weights. Local state-cycle means shrink toward a shared cycle-balanced error; shrinkage and optional window/decay selection useY−2. No economic inputs; no-poll forecasts unchanged. Shared controls and reused momentum forecasts distinguish calibration benefits. [Method and results](STATE_POLL_BIAS_RESULTS.md).

## State bias plus residual momentum

Notebook Sections 69–72 combine the last-five-cycle/8-year state-bias recipe (and a past-selected bias control) with shared economic momentum learned on remaining errors. Every historical first-layer forecast is reconstructed from earlier information; in-sample first-layer residuals are not used. A constant-only residual control separates further calibration from momentum value. All stage tuning uses Y−2. [Method, limitations and results](BIAS_MOMENTUM_RESULTS.md).

### Forecast fusion experiment

See [MODEL_FUSION_RESULTS.md](MODEL_FUSION_RESULTS.md), baseline Sections73–76: shared ridge combines seven chronological forecasts, plus compact prior/latest variants. Standardize only within training, cycle-balance loss, tune onY−2 and refit all past meta-cycles; first eligible test2020. Applies to no-poll contests too. Lower margin MAE does not establish improved competitive winner accuracy; retain bias-only reference.

### Parallel tree and forest experiment

Baseline Sections 77–80 compare tree/forest × scores/raw × direct/prior correction, using state identity, cycle-balanced training and whole-cycle forest bootstraps. Raw predictors retain unsigned and WH-signed forms; tune depth on Y−2, refit all earlier cycles, preserve current October cutoff. Held-out group removals diagnose importance; they do not select a reduced model on the outer labels. See [TREE_FEATURE_RESULTS.md](TREE_FEATURE_RESULTS.md). No fusion or production-model replacement.

### Small momentum/approval comparison

Baseline Sections81–84 compare shared momentum, overall approval level, both and constant-only corrections to prior/polling/prequential state-bias polling, with fixed8-year history decay andY−2ridge tuning. An optional selector can choose no correction usingY−2 alone. Approval does not consistently improve the strongest bias reference;2026bias selector choosesnone. No-poll polling/bias forecasts stay unchanged. See [MOMENTUM_APPROVAL_RESULTS.md](MOMENTUM_APPROVAL_RESULTS.md).

### Within-cycle polling recency

Baseline Sections 85–88 compare 7/14/30/60/90-day and no poll-age decay at fixed forecast cutoffs. Hold the original prior fraction fixed for the main comparison, and separately allow decayed evidence mass to change that fraction. Rebuild historical forecasts and state-bias calibration per rule; select optional half-lives using Y−2 polled MAE. No-poll forecasts remain unchanged. Faster decay helps some plain-polling calls but can hurt calibrated calls; no automatic replacement. See [POLL_AGE_DECAY_RESULTS.md](POLL_AGE_DECAY_RESULTS.md).

### Cross-state borrowing for sparse polls

Sections 89–93 predict each state's deviation from its prior using other states' observable poll-minus-prior signals. One-donor/all-donor ridge models use train-only associations, missing-value handling and recency weights; the target state's own polls are excluded. These estimates can apply without own polls. Coverage-aware blends with polling/bias use Y−2 tuning and a no-borrowing option; identical blends using only a historical state adjustment isolate donor value. Error-only corrections are tested separately. Pairwise margin/shift/error correlations and state reliability are descriptive; no pairwise covariance inversion or joint uncertainty forecast is claimed. See [STATE_PEER_RESULTS.md](STATE_PEER_RESULTS.md).

### Full-seat review, September 18, 2026

Sections 94–98 retain the fixed bias reference and replay forecasts; no new fit or model promotion. Historical September horizons use September 17 in each cycle (confirmed against saved calendars), not an exact common number of days to Election Day. A 100-seat roster adds continuing seats to contested calls. Excluded historical contests are explicitly completed by retaining their pre-cutoff incumbent caucus; these assumptions are never counted as modeled/scored forecasts. Dated party-affiliation segments determine the contemporaneous caucus. Following-January membership supplies outcomes only; specials/runoffs for the same seat are deduplicated. The conditional 2026 D−R sign tally is 50 D / 50 R, not calibrated expected seats or control odds; candidate/independent/RCV/runoff restrictions remain. Public probabilities and market quotes stay separate from margins. See [SENATE_SEAT_REVIEW.md](SENATE_SEAT_REVIEW.md).

### Extra factors in the full-seat comparison

Sections102–104 reuse the previously trained shared momentum/approval residual stacks. The bias reference itself has no economic/approval inputs; adding features is a separate regression on remaining chronological forecast errors. Fixed momentum/approval/both arms, constant-only and past-selected extra layers accompany the existing polling/bias models. Calibration and regularization are distinct: current state-bias shrinkage is zero, while feature slopes are strongly ridge-shrunk. Current fixed two-score contributions are approximately−1.420pp intercept,+0.105momentum,+0.198approval; the net−1.117 shifts three fragile calls (AK/ME/TX) and gives conditional47D/53R. The past selector chooses no extra layer and retains50D/50R. This review does not promote either recipe. See [FEATURE_STACK_SEAT_REVIEW.md](FEATURE_STACK_SEAT_REVIEW.md).

### Methodology review, Section105

The shared factor layer targets remaining forecast error, not the outcome itself. Its weighted fit on246state rows equals a14-row regression of cycle-mean residuals because national inputs are repeated and cycle weight is divided among states; this equivalence was independently verified. An unpenalized second intercept, shifting state coverage and one-cycle validation merit separate controls. [COMBINATION_METHODOLOGY_REVIEW.md](COMBINATION_METHODOLOGY_REVIEW.md) records proposed zero/shrunk-intercept diagnostics and a small constrained blend of corrected polling with existing fundamentals/prior forecasts. These are proposals, not implemented model changes; prior broad fusion's mixed results remain relevant.


### Intercept and constrained-blend experiment, Sections106–109

The Section105 proposals are now implemented as separate diagnostics. Keep the state-bias reference fixed. Compare zero/strongly-shrunk second intercepts using the same momentum/approval residual design; tune slope alpha onY−2, retain original-alpha controls. Strong shrinkage penalizes the intercept by10times totalcycleweight, reducing it to1/11of the old intercept at fixedalpha. Centered features make the zero-intercept anchor the training-average context.

The separate fundamentals constituent is historical state prior plus shared momentum/approval outcome correction. Combine it with corrected polling using fixed50/50, fixed90/10, or a previous-cycle selected convexweight from0/.25/.5/.75/1. The90/10 sensitivity does not modify that search grid. Validation constituents are themselves past-only forecasts; no held-out/current outcomes select their own parameters. The same8-year historical decay and training-only transforms remain. No-poll blends use fundamentals; fallback-only control isolates that change from blending on polled states.

Recent2016–2024 September/October correct calls: bias125/132, zero/shrunk124/129,50/50blend124/127,90/10blend124/130,selectedblend126/132.90/10lowers SeptemberMAE7.364→7.266pp but worsensOctober5.230→5.360. Every selected historicalOctoberweight is100%polling; all-state differences then come only from no-poll fallback. Currentconditional totals: bias/interceptcontrols50D/50R,50/50blend49/51,90/10andselectedblend48/52. The small90/10margin changes flip near-tiedAK/TX; seat-sign changes are discontinuous, so smoother margins do not guarantee stable seat counts. No model promotion or uncertainty claim. See [results](COMBINATION_DIAGNOSTICS_RESULTS.md).


### Separate state priors from national feature adjustments

[SEPARATED_FEATURE_RESULTS.md](SEPARATED_FEATURE_RESULTS.md), baseline Sections110–112, replaces the feature-only interpretation of the earlier complete-forecast blend. Components are explicit: historical state prior P, corrected polling C, intercept a, momentum contribution and approval contribution. New predictions are C +10%/50%of the two feature contributions; no state prior or extra intercept enters this new layer. Compare existing outcome-trained slopes as a transfer sensitivity with residual-trained zero-intercept slopes as the target-aligned correction; no new slope tuning. No-poll fallbacks unchanged. Both use historical training-only normalization and party-aware scores. Old full-forecast blends remain labeled historical controls.

Current all four new variants retain50D/50R; AK/TX no longer flipR. The10%residual correction adds+0.103ppD, preserving recent125/138September and132/138October calls, with small mixedMAE changes. No claim of a new superior model. Three new notebook cells evaluated in-process; earlier221cells/outputs preserved.


### Three standalone forecasts and literal combinations (Sections113–116)

[THREE_MODEL_RESULTS.md](THREE_MODEL_RESULTS.md) compares M1 corrected polling, M2 historical prior, and M3 direct outcome regression on economic momentum/approval, plus literal50/25/25,90/5/5and past-learned convex combinations. M3has partially pooled state intercepts/slopes and no supplied prior/poll offset; state history still trains its coefficients. The learned mixture uses minimum2/last3prequential cycles, a231-rule5ppsimplex grid and equal-cycleMAE. It starts2016; current weights95/0/5, all testedOctoberweights100/0/0. No-poll M1fallback retained, M3shared fallback for states without admitted training outcomes.

RecentSep/Oct correct outof138: M1 125/132,M2 120/120,M3 110/113,50/25/25 122/127,90/5/5 124/130,learned123/132. CurrentconditionalDseats50/47/56/49/49/50respectively; no modelpromotion. Historical per-cycle accuracy/MAE, state predictions with actuals, complete chamber scenarios and component-removal sensitivities saved. Four new cells checked in-process; previous227cells/outputs preserved.


### Surprise prediction with polling/prior fusion (Sections118–121)

[SURPRISE_FUSION_RESULTS.md](SURPRISE_FUSION_RESULTS.md) restores the feature target to actual minus historical corrected polling, using shared momentum/approval slopes without an extra intercept/state baseline. No-poll surprise labels/estimates remain missing; those states retain their prior. Final forecast is `(1−a)*corrected_polling + a*prior + b*surprise`, clipped tovalidmargins. Fixed50/25/25means a=1/3,b=.25;90/5/5means a=1/19,b=.05, explicitly normalizing baseline weights rather than averaging a delta as a full forecast. Learned a/b use441pairs with minimum2/last3past prequential cycles and equal-cycle polledMAE; previous-cycle ridge tuning remains.

CurrentS=+1.032ppD; learned a=0,b=.85adds+.877ppDandkeeps50D/50R. RecentSep/Oct learned124/130correct versus correctedpolling125/132; October2020surprise sign is a notable held-out failure. Same-baseline/no-surprise controls isolate Sfromprior mixing; no promotion. Four new cells checked in-process; prior236cells/outputs preserved; report contains all historical state actuals and surprise labels.


### Shared versus state-specific surprise coefficients (Sections 122–124)

[STATE_SURPRISE_RESULTS.md](STATE_SURPRISE_RESULTS.md) compares shared economic/approval surprise slopes with partially pooled state slopes. Both predict actual minus chronological corrected polling, without an intercept or state baseline. Previous-cycle validation jointly selects shared and state penalties, including the infinite state penalty that returns to shared coefficients. Final fusion weights remain global; fixed recipes, separately learned recipes and a control holding shared final weights fixed distinguish coefficient changes from downstream selection effects.

Ten of fifteen fits select the shared limit, including 2026. Current surprise is identical: +1.032 pp D. Different historical forecast paths produce separately selected surprise multipliers of 0.85 (shared) and 0.05 (state-capable), with zero prior share; both give conditional 50 D / 50 R. Locking the shared final weights makes current forecasts identical. Recent 2016–2024 learned-fusion calls are 124/130 (September/October) for shared versus 124/128 for state-capable, out of 138; corrected polling remains 125/132. No consistent benefit or model promotion.

Five tests pass. Fifteen final and fifteen selected inner fits were independently reconstructed, 4,851 fusion losses recalculated, and 6,679 forecasts / 235 complete chamber scenarios audited. Three added notebook cells were evaluated in-process; prior 244 cells and outputs and both review notebooks are unchanged. This does not claim a full notebook kernel rerun. Existing ballot, coverage and joint-uncertainty limitations remain.


### Simple shared direct regression (Sections 125–126)

[SHARED_DIRECT_RESULTS.md](SHARED_DIRECT_RESULTS.md) completes direct/shared, direct/state, surprise/shared and surprise/state cases. The new linear ridge model has one shared intercept and two shared economic/approval slopes, no state identity or prior/poll offset. Training uses all older admitted Senate outcomes, equal cycle mass before eight-year decay, training-only normalization/fills and Y−2 alpha selection. National-only inputs imply the same direct margin for every state; this is a diagnostic control, not national popular vote.

Recent 2016–2024 correct calls: direct shared 70/138 at both horizons versus direct state 110/138 September and 113/138 October. Current shared forecast R+0.33 everywhere decomposes into R+1.33 intercept plus about 1.00 pp Democratic feature contribution. All four cases and corrected-polling/prior references have paired state actuals, per-cycle metrics and conditional chamber totals. Existing forecasts and mixing weights are unchanged; no model promotion.

Two tests pass; all 15 final and 60 inner fits checked against augmented least squares. Two added notebook cells evaluated in-process; prior 250 cells and both review notebooks preserved. Source hashes, 2,135 retained reference predictions, 2,562 total forecasts and 90 full chamber scenarios audited.


### First Bayesian Gaussian model

Open [BAYESIAN_GAUSSIAN.ipynb](BAYESIAN_GAUSSIAN.ipynb). Its original Sections 1–8 retain their outputs and five figures; Sections 9–12 add the correction comparison described below. [BAYESIAN_GAUSSIAN_RESULTS.md](BAYESIAN_GAUSSIAN_RESULTS.md) gives the first specification and results. The first model uses lagged state priors, unblended polling, partially pooled state biases, one learned movement factor and a separate polling-error factor. Those first sections exclude economic/approval features; event effects remain future work.

All older eligible outcomes train stable state loadings/biases; older versus last-ten-year noise scales differ, crossed with midterm/presidential cycles. Missing races are not zero-filled. This pools covariance information without estimating an unrestricted matrix or treating many state rows as independent national contexts. The covariance-off comparison preserves marginal prior variances and common polling error, using the same historical posterior; it is a forecast sensitivity, not a separately fitted model.

Four-chain Bayesian fits cover 2012–2024 at both horizons and frozen September17,2026. Learned covariance reduces recent MAE from7.82→7.64pp in September and6.11→5.70pp in October; correct calls123→124and129→129of138. Corrected polling remains a stronger point reference (125/132calls). Gaussian95%interval coverage is only90.6%/87.7%: predictive calibration is not accepted. Masked-poll gains are mixed, helping2024but slightly hurting2020.

Current conditional covariance result:48.17expectedD/51.83R, nominal95%Dseat interval44–53,49Dindividual majority-probability calls. D≥51probability14.0%,exactly50probability12.0%; these are conditional scalar/ballot/caucus scenarios, not certified control probabilities. Rule uncertainty is not modeled, and undercoverage limits interpretation.

Six tests and implementation audits pass:15fits×4chains,854forecasts,30chamber distributions,224masked forecasts; maxRhat1.00984,minbulkESS453,mintailESS765. Minimum full forecast importanceESS433; some masked cases~201remain noisy. All earlier notebooks are unchanged. Entire new notebook analysis replayed in-process, with actual model fitting completed separately through its build function. Default rerun verifies/reuses pinned artifacts; set REFIT_MODEL=True to fit again. It does not download newer polls. Validated run metadata lives at reports/bayesian/latest.json; status explicitly distinguishes implementation checks from unaccepted predictive calibration.

### Joint Bayesian feature surprise and bias controls (Sections 9–12)

The approved extension keeps latent final margins, lagged priors and movement covariance unchanged, and models polling error as:

```
raw_poll_st = final_margin_st + persistent_bias_s
              - beta_momentum * x_momentum_t - beta_approval * x_approval_t
              + common_poll_error_t + race_poll_error_st + aggregation_noise_st
```

The two shared coefficients have independent Normal(0, 2²) priors in pp per training-score SD. Positive beta·x is a Democratic actual-minus-poll surprise. There is no extra intercept or state feature slope. This is a polling-surprise model, not a direct fundamentals forecast. The old correction to prior-weighted polling is displayed as a reference, never added into this likelihood.

Both party-aware scores retain the existing fixed recipes, including January 1 and previous October 31 economic changes. Ingredient statistics, missing-score medians and final standardization are learned from one row per older polled cycle, equally weighted. Only momentum and approval enter the likelihood; broader score utility metadata does not imply four modeled coefficients. All older eligible errors train it, with the existing older/recent and midterm/presidential variance groups. Neither current inputs nor held-out outcomes fit preprocessing.

Given observed historical final outcomes, the movement and polling parameter posteriors factorize. Independently combine saved movement draws with a new four-chain polling fit; sample shared coefficients jointly with common cycle errors through a collapsed Gaussian update. Reused movement samples retain their original ESS. Forecast-date polls update the combined posterior through marginal-likelihood importance weights. No-poll states receive no direct feature observation; indirect covariance/parameter updates remain possible.

Controls: (1) original covariance on/off, retained exactly; (2) suppress persistent bias at forecast time, same scales; (3) separately refit with persistent bias zero, retaining random common polling error; (4) jointly fit bias plus features; (5) suppress features at forecast time, keeping joint fitted bias/scales. The forecast-only controls are sensitivities, not independently fitted models. Error scales may change under refitting, so these controls answer different questions.

Recent 2016–2024 results are mixed. Original / no-bias refit / joint-feature September calls: 124 / 126 / 125 of 138; October: 129 / 129 / 129. MAE: 7.643 / 7.597 / 7.673 pp and 5.697 / 5.901 / 5.712 pp, respectively. MAE and Brier average cycles equally; interval coverage pools contest forecasts. The feature model has 92.0% / 87.7% coverage for nominal 95% intervals; current coefficient intervals include zero. No promotion or predictive-calibration acceptance.

Current frozen September 17, 2026 primary covariance-on variants all call 49 D / 51 R; expected D seats 48.17 / 48.55 / 48.79. Current feature surprise is about +1.16 pp D before posterior weighting. Seat distributions remain conditional on existing ballot/caucus assumptions. Six additional tests and artifact audits pass; all earlier notebook outputs are preserved. See [BAYESIAN_CORRECTIONS_RESULTS.md](BAYESIAN_CORRECTIONS_RESULTS.md) and `reports/bayesian_corrections/latest.json`. Next: scale/calibration sensitivity, then Student-t with the same mean/input structure, followed by a separate disruption-scale experiment.

### Completed scale and Student-t comparison (Sections 13–16)

Keep the original mean equations `theta = prior + loading*F + eta` and `poll = theta + bias + B + R + aggregation_noise`. Three Gaussian forecast sensitivities multiply movement SD, polling SD (including aggregation), or both by 1.5, retaining the historical posterior but recalculating forecast-poll weights. These do not constitute historical prior/scale refits.

The Student-t experiment replaces F, eta, B and R with independent t components conditional on shared loadings and variance parameters. Fixed nu=5; component scale squared is `(nu-2)/nu * V`, so V remains its marginal variance and retains the Gaussian model's prior. F has variance one. Bias/loading priors and aggregation noise remain Gaussian. This is a structured t factor model, not an unrestricted multivariate-t distribution. It excludes the extra economic/approval corrections for a matched mean comparison and does not condition tails on disruption flags.

Represent each component using `w ~ Gamma(nu/2, rate=nu/2)` and conditional variance `V*(nu-2)/(nu*w)`. Gibbs refits all historical parameters and latent precisions; new-cycle precision draws are integrated jointly with forecast polling. Outcomes score forecasts but never enter current inference. Four-chain convergence gates pass; independent forecast integrations change no calls. Six tests include exact recovery of the Gaussian sampler when mixture scales are one, predictive covariance checks, and synthetic outlier robustness.

All seven comparison models share 427 target/horizon records. Main evaluation is 2016–2024 (138 per horizon); 2012–2024 provides an older-inclusive check. Compare fixed non-Bayesian corrected polling and its momentum extension without selecting between them on each test outcome. Use mean-margin sign for shared point accuracy, equal-cycle MAE, and separate Bayesian probability accuracy/Brier/coverage. Non-Bayesian probability fields stay missing.

Student-t is mixed: earlier calls 125 vs Gaussian 124, October 128 vs 129; MAE 7.600 vs 7.643 pp and 5.789 vs 5.697 pp. Corrected polling leads October (132/138, 5.230 pp); its momentum extension leads earlier (126/138, 7.205 pp). Student-t 95% coverage is 89.9%/86.2%; wider Gaussian scales improve 95% coverage but overcover central intervals. No promotion or predictive-calibration acceptance. These results do not establish which mean/scale assumption is wrong or rule out other t specifications.

Implementation audit and saved outputs: [BAYESIAN_TAILS_RESULTS.md](BAYESIAN_TAILS_RESULTS.md), `reports/bayesian_tails/latest.json`. Notebook prior 24 cells/outputs preserved, four appended cells executed in-process. Further mean/bias/recency, historical prior-scale and disruption-scale changes are not included; review this comparison before expanding the model.

## Transparent polling-update restart (September 19, 2026)

The separate [SIMPLE_BAYESIAN_POLLING_MODEL.md](SIMPLE_BAYESIAN_POLLING_MODEL.md) supersedes neither earlier artifacts nor their results. It specifies a new small first model requested after reviewing the complexity of learned state loadings. Final margins have a history-centered Gaussian prior with exchangeable covariance; polls are noisy measurements with regularized state bias, a persistent error floor and shared polling error. Three global grid settings and Gaussian bias variables are integrated analytically. There is no regression W or economic/approval feature term yet.

[SIMPLE_BAYESIAN_POLLING.ipynb](SIMPLE_BAYESIAN_POLLING.ipynb) independently rebuilds the approved poll samples at each exact saved cutoff, reproduces old counts/raw means, runs15 historical/current folds, contrasts linked and local controls with frozen benchmarks, and displays arrival replay, no-poll stress tests, historical actuals and full-chamber distributions. Generalized Bayesian historical relevance weights and fixed poll aggregation are explicit assumptions. Full execution and numerical/provenance audits pass. Predictive superiority is not established; corrected polling retains lower recent point error. Next review: small-grid resolution, boundary mass and fixed-scale sensitivity before feature expansion.

For the transparent polling restart, maintain [CURRENT_BAYESIAN_MODEL.md](CURRENT_BAYESIAN_MODEL.md) as the living model/assumption record. Its initial revision documents existing behavior only; no new sigma/rho prior, feature model or interstate relationship has been implemented by creating that document.


### Bayesian Revision 2 — learned state uncertainty and relationships

[BAYESIAN_REVISION2.ipynb](BAYESIAN_REVISION2.ipynb) is a separate, fully executed experiment. It retains the historical mean and poll aggregation, learns heterogeneous signed outcome and polling-error covariances with missing-data-aware, regularized Gaussian EM, and integrates persistent state-bias uncertainty. Earlier-cycle validation selects regularization. Covariance estimates remain fixed during forecasting (empirical Bayes). See [the living specification](CURRENT_BAYESIAN_MODEL.md), [exact estimator](BAYESIAN_REVISION2_ESTIMATOR.md) and [results](BAYESIAN_REVISION2_RESULTS.md).

For 2016–2024, linked MAE changes from 7.877 to 7.498 pp at September 17 and 6.038 to 5.600 pp at October 31. Correct calls change from 125 to 124 and remain 129 of 138, respectively. Corrected polling still leads October with 5.230 pp MAE and 132 correct calls. No model promotion. Frozen September 17, 2026: point total 51 D / 49 R, expected 49.55 D, central 95% range 45–54 D, conditional on the fitted covariances and existing ballot/caucus assumptions.

Eleven numerical tests and provenance/chronology/convergence audits pass. The full notebook, including fitting, executed in-process: 14 code cells, 7 figures, 15 forecast folds and 118 cached component fits. All earlier notebooks/artifacts were preserved. `reports/bayesian_revision2/latest.json` identifies the verified output; `REBUILD=True` rebuilds from frozen inputs without downloading. Next review: systematic prior-mean errors, existing calibration exclusions for AK/GA/LA/ME, weak pair support and covariance-estimation uncertainty.


### Prior Revision 3 — historical center and tunable strength

[BAYESIAN_PRIOR_REVISION3.ipynb](BAYESIAN_PRIOR_REVISION3.ipynb) compares current, latest-result and decay-weighted priors, each with fixed versus shared tuned prior strength. Historical errors/covariance are rebuilt for each recipe. A past-only selected variance multiplier a scales the full prior covariance; penalty strength is 1/a. Mean half-life and strength validation are nested chronologically. [Design](BAYESIAN_PRIOR_REVISION3.md), [results](BAYESIAN_PRIOR_REVISION3_RESULTS.md), and [living model specification](CURRENT_BAYESIAN_MODEL.md) explain the details.

Recent 2016–2024 prior-only MAE improves 9.765→8.230 pp with decay. October posterior MAE: current 5.600, latest fixed 5.277, decay fixed 5.400 pp; winner calls 129/131/129 of 138. Shared strength tuning does not consistently help, and several tuned variants have worse coverage. Current decay model selects four-year mean half-life and a=1: 49 D / 51 R point calls, expected 48.95 D, 95% range 45–53 D, on frozen September 17 inputs. No automatic promotion.

All 19 relevant numerical tests and 23 artifact checks pass. Fifteen forecast folds, 195 component fits (90 reused/105 new), 2,562 new forecasts, 90 draw files; all 13 notebook analysis cells executed in-process with 5 saved figures. Model fitting completed separately using the same build function. `REBUILD=True` refits; default verifies/reuses `reports/bayesian_prior_revision3/latest.json`. Earlier notebooks and artifacts remain unchanged. Remaining issues: prior mean bias, sparse admission/relationship support, selection uncertainty and Gaussian mass beyond valid margin bounds.


### State-specific prior penalties — Revision 4

[BAYESIAN_STATE_PENALTY.ipynb](BAYESIAN_STATE_PENALTY.ipynb) adds state prior-variance multipliers shrunk toward the shared value learned from the last three earlier cycles. Local evidence has a four-year half-life and two-result shrinkage; no recent outcome means exact shared fallback. Covariance scales as D C D, preserving correlations. Three new variants retain the exact current/latest/decay means and all fitted Revision 3 components. [Design](BAYESIAN_STATE_PENALTY.md), [results](BAYESIAN_STATE_PENALTY_RESULTS.md), and [living specification](CURRENT_BAYESIAN_MODEL.md).

For 2016–2024, decay/state October MAE is 5.193 pp and 130/138 calls versus decay/shared 5.415 and 129/138; competitive calls 46/52 versus 45/52. September changes are modest. Nominal 95% intervals cover 92.03% of October outcomes, so no promotion. Frozen September 17, 2026 decay/state forecast: 48 D / 52 R point total, expected 48.50 D, 95% range 45–52 D; Michigan crosses zero by only 0.02 pp.

Eight new tests and 23 artifact checks pass; 12 analysis cells executed with 4 figures, 15 folds, 1,281 new forecasts, 2,250 state profiles and 45 draw files. No new covariance fits or downloads; prior notebooks preserved. Default verifies/reuses `reports/bayesian_state_penalty/latest.json`; REBUILD=True reruns state tuning/forecasts from pinned components. Calibration, bounds, sparse history and omitted covariance/penalty uncertainty remain documented limitations.


### Prior Revision 5 — input review, faster mean and shrunk mean correction

[BAYESIAN_PRIOR_REVISION5.ipynb](BAYESIAN_PRIOR_REVISION5.ipynb) adds a two-year mean half-life candidate and a separate Gaussian shared/state correction to actual-minus-prior error, including correction uncertainty in the refitted prior covariance. Polling bias remains unchanged. Fixed/shared/state strengths are retuned chronologically. [Design](BAYESIAN_PRIOR_REVISION5.md), [results](BAYESIAN_PRIOR_REVISION5_RESULTS.md), [living specification](CURRENT_BAYESIAN_MODEL.md).

Historical validation still chooses four years everywhere; only 2026 selects two, so historical faster-family forecasts are unchanged. Mean correction has mixed results: recent state-strength MAE 6.900→6.856 September but 5.193→5.278 October, with 127/130 winner calls unchanged. Prior-only MAE worsens 8.230→8.312. No promotion; Revision 4 stays the benchmark. New current variants call 49 D / 51 R, with corrected/state expected 48.83 D and 95% range 45–53 D on frozen September 17 inputs.

Targeted review records existing unofficial-source exclusions for WV 2018 and SD 2020 with official-source follow-ups; matched dataset admissions are unchanged. Eight new tests and 29 audits pass; 15 folds, 179 component fits (67 new), 2,562 new predictions, 90 draws, 12 executed analysis cells and 4 figures. Earlier notebooks are preserved. Default verifies/reuses `reports/bayesian_prior_revision5/latest.json`; REBUILD=True repeats fitting/selection without downloading polls. Next: verified admission updates and seat/incumbency context before more prior tuning.


## Official-result repair and current references

## Review decision after official-result repair

The preferred references remain **bias-corrected polling for late-cycle point forecasts** and **Revision4's decay prior with state-shrunk strength for Bayesian probabilities and joint seats**. Neither dominates every metric; no new model family is promoted.

Recent2016–2024, same140 contests per horizon:

| Model | September correct | September MAE pp | October correct | October MAE pp |
|---|---:|---:|---:|---:|
| Tuned polling |124/140|8.106|128/140|6.071|
| Polling + historical bias |127/140|7.472|133/140|5.220|
| Bias + shared momentum |127/140|7.296|129/140|5.367|
| Bayesian decay/state |129/140|6.980|131/140|5.250|
| Bayesian mean correction/state |128/140|6.944|132/140|5.287|
| Bayesian latest/shared |125/140|6.732|132/140|5.675|

Bayesian decay/state has the lowest recent Brier score among rerun Bayesian variants at both horizons (0.0639/0.0471). Its95% coverage is92.14% at both horizons, so probability calibration needs work. Latest/shared wins earlier MAE but loses calls. The mean correction remains mixed. Adding momentum to bias correction lowers earlier MAE without extra correct calls and worsens late performance. The unchanged historical fast-grid forecasts match decay because both select4years;2026fast selects2years.

The Bayesian advantage is partly in no-poll cases: September MAE8.87 versus11.13pp for the bias model's history fallback. Among polled September contests, bias+momentum MAE5.06 beats Bayesian decay/state5.99; both correctly call92/102. Thus all-state results must not be interpreted as uniform superiority in well-polled races. The competitive screen now has54 competitive,68 noncompetitive and18 unknown-history cases; unknown cases are not silently classed as safe.

For October2024, both main references correctly call26/28, but bias MAE3.10 is much better than Bayesian decay/state5.86. The Bayesian model's lower MAE in2016–2022 does not erase that weakness. On the original138 recent contests alone, the data repair changes October bias MAE5.230→5.206 and calls132→131; Bayesian decay/state MAE5.193→5.235 and calls130→129. Both models correctly call the two added contests, giving the140-case totals above. Predictions before2018 are unchanged within9.1e−8pp.

**2026, frozen September17 inputs:** both main references give49D/51R by point calls. Bayesian expected seats48.48D/51.52R;70% D interval47–50 and95%45–52. Michigan is D+0.018pp with50.12% D probability: a sign flip near exactly50%, not a confident gain. Full chamber counts retain continuing-seat and explicit incumbent-caucus completion rules for unmodeled contests. Point models have no invented probability intervals.

This review refits36 existing contenders with repaired data, including15 prior/strength Bayesian variants,2 link ablations, raw polling and18 prior/poll/bias/feature references. Earlier complex Gaussian/Student-t/tree/fusion experiments remain archived, not falsely labeled as repaired-data reruns. Historical experimentation has already used these test cycles, so the ranking remains exploratory.

See [executed review notebook](OFFICIAL_REPAIR_MODEL_REVIEW.ipynb) and [reproduction contract](OFFICIAL_REPAIR_MODEL_REVIEW.md).


## Prior calibration and sensitivity

[Executed notebook](PRIOR_CALIBRATION_SENSITIVITY.ipynb), [full results](PRIOR_CALIBRATION_SENSITIVITY_RESULTS.md), [design](PRIOR_CALIBRATION_SENSITIVITY.md). Prior95%intervals cover98–99%of recent outcomes, versus92%after polls. Four-year covariance history improves earlierMAE/latecalls; less state pooling improves lateMAE but worsens coverage. Joint mean/strength tuning does not help. Keep the current reference and two named challengers; move next to polling-error/update calibration, preserving sparse-history and covariance-uncertainty limitations. No new polling/data acquisition or automatic model promotion.


## Frozen-prior polling update review

[Executed notebook](POLLING_UPDATE_REVIEW.ipynb), [results](POLLING_UPDATE_REVIEW_RESULTS.md), [contract](POLLING_UPDATE_REVIEW.md). All three prior recipes are fixed. Doubling total likelihood variance improves coverage but slightly worsens margin accuracy; chronological scale selection does not consistently help. No promotion. The exact state decomposition and descriptive prior/poll error dependence make common errors/effective evidence the next focused direction, ahead of election-day drift, parameter uncertainty/heavy tails and feature surprises. Reference current forecast remains49D/51R by calls, expected48.48D,70% D range47–50 on frozen September17 inputs.


## Recent polling bias and reliability penalty

[Executed notebook](RECENT_POLL_BIAS.ipynb), [results](RECENT_POLL_BIAS_RESULTS.md), [contract](RECENT_POLL_BIAS.md). Exact election priors remain fixed while recent Gaussian zero/shared/state bias estimates replace the old bias mean and uncertainty. Five-cycle history,4/8year decay and shared likelihood multiplier1/2/4 are tested chronologically. Recent-zero8 yields tiny margin-score gains; shared4 plus selected penalty improves late calls131→134/140 but worsens lateMAE5.250→5.304pp and probability score. Two extra calls are2016, one2020. No automatic promotion. Reference current49Dpoint/48.481expected/70%47–50D remains, using frozenSep17 inputs. Covariance recentering and effective common polling errors remain separate follow-ups.


## Joint polling bias and residual scale

[Executed notebook](JOINT_POLL_ERROR.ipynb), [results](JOINT_POLL_ERROR_RESULTS.md), [contract](JOINT_POLL_ERROR.md). Estimate one residual-only covariance multiplier while integrating bias, keeping exact election priors/correlation patterns and whole-likelihood lambda1. All90fitted scales are below1; no boundary hits. State4 margin MAE improves slightly but95%coverage falls, and all six reference-prior recipes worsen recent marginal NLL at both horizons. No promotion. This identifies a training-fit/predictive-calibration gap; effective common polling errors, horizon drift and parameter uncertainty remain next directions. Reference current49Dpoint/48.481expected/70%47–50D remains on frozenSep17 inputs.


## Structured polling-error sensitivity

[Executed notebook](STRUCTURED_POLL_ERROR.ipynb), [results](STRUCTURED_POLL_ERROR_RESULTS.md), [design](STRUCTURED_POLL_ERROR.md). Freeze exact election priors, historical bias and baseline residual covariance. Test added common cycle error, same-firm cross-state fresh-noise links (unchanged marginal variance), and poll-age/time-to-election discrepancy. Last-three-earlier-cycle joint Gaussian score selects components, with zero allowed and first tuned test in 2018. Fixed common SD 2pp improves recent state MAE and probability scores at both horizons; October calls rise 131 to 133/140. Expected chamber-seat MAE worsens 1.288 to 1.479, so retain it as a challenger. Firm links are small and extra time variance lacks clear benefit; the baseline already includes historical common/time errors. These are optional predictive terms, not separately identified physical effects. No promotion or refresh. Living specification revision 11 documents equations and assumptions.


## National error, scale uncertainty and wave scenarios

[Notebook](NATIONAL_TAILS_WAVES.ipynb), [results](NATIONAL_TAILS_WAVES_RESULTS.md), [design](NATIONAL_TAILS_WAVES.md). Tune extra national polling-error SD0/2/4/6 using earlier-cycle joint density. Compare Gaussian, inverse-gamma common-scale mixtures nu4/10/30 and covariance-matched t5 sensitivity, with the same historical prior/correlation shape. All families preserve means at fixed national SD. Matched-t improves joint density but weakens central coverage; uncertain common scale is overconfident. National selection is mixed and worsens late chamber error. Keep reference and fixed Gaussian common2 challenger. Separate editable national-error and blue/red-wave controls in Section8; delta shifts final modeled margins without assigning a scenario probability. Current reference−2/0/+2pp gives47.13/48.48/49.90expectedD. Full covariance uncertainty remains open; no promotion/refresh.


## Fitted Student-t systematic polling error

[Notebook](STUDENT_POLLING_LIKELIHOOD.ipynb), [results](STUDENT_POLLING_LIKELIHOOD_RESULTS.md), [design](STUDENT_POLLING_LIKELIHOOD.md). Fit a Student-t systematic-error likelihood by integrating one shared inverse-gamma scale, keeping Gaussian historical prior and bias/fresh noise fixed. This changes posterior means, unlike the prior matched-t predictive sensitivity. Fixednu5 atg0/g2 plusnu10/30 and chronological selectors. Modest MAE/Brier/joint-density gains trade against coverage and close winner calls; atg2 latecalls133→131 and95%coverage92.1→90.0%,MAE5.218→5.162pp. No promotion. Current selectednu5/g2 gives48Dpoint/48.446expected/70%47–50D; reference remains49point/48.481expected. Next is review and inclusion decision, not automatic expansion.


## Refined df and prior/non-Bayesian influence

[Notebook](DF_PRIOR_REVIEW.ipynb), [df results](DF_PRIOR_REVIEW_RESULTS.md), [explanatory review](PRIOR_INFLUENCE_RESULTS.md). Refine df2.5–30 plus Gaussian using previous3cycles;2026selectsdf4/g2 butdf3–5scores are nearly tied. Exact matched-state bridge separates averaging, bias, own-prior and other-state contributions. NBpolling currently selects zero prior weight in polled states. NC/TX prior contrasts materially favorR, but MI's own prior favorsD and other-state information pullsR; NBbias there is more Republican. K2/K4 weaken Bayesian prior precision and make2026moreD while worsening several historical accuracy scores and improving coverage. No global over-weighting conclusion or promotion. CurrentrefinedStudent48Dpoint/48.544expected/70%47–50; reference unchanged. No external forecast refresh was performed.


## Coverage, prior strength and cross-state diagnostics

[Executed notebook](COVERAGE_BALANCE.ipynb), [results](COVERAGE_BALANCE_RESULTS.md), [contract](COVERAGE_BALANCE.md). WIS penalizes width and misses, selecting K1/K2/K4 using last3 earlier out-of-sample cycles. Full-period state WIS favors original strength, but2020/22/24 validation narrowly selectsK2 for2026 in both Gaussian and Student families. StudentK2 gives50Dpoint/49.382expected/70%47–52. Chamber CRPS improves with weaker priors, illustrating that marginal-state and total-seat objectives differ. Michigan refit using only its own current polls givesD+3.10 atK2 versusD+0.56 with all states. Fixed covariance-removal diagnostics clarify movement versus error attribution, with mixed historical benefits. No promotion or data refresh; previous notebooks remain intact.


## Simple explicit national electoral movement and polling error

[Notebook](SIMPLE_NATIONAL_MODEL.ipynb), [results](SIMPLE_NATIONAL_MODEL_RESULTS.md), [design](SIMPLE_NATIONAL_MODEL.md). Two fitted shared variances replace the old movement/error covariance shapes while preserving state marginal budgets. Gaussian N/U with fixed+1 loadings and independent local movement, coherent historical bias refit; no new slopes, pairwise movement matrix or tail parameter. Chronological WIS selectsK1. Recent all-state MAE6.630/5.040pp improves, but competitive WIS and late chamber scores do not uniformly improve. Current realN D+.967 versus inferred polling overstatementD+4.723 yieldsMI R+.229 and47.760expectedD seats. No promotion or input refresh; retain previous reference and full diagnostics.


## Working designation: no shared polling-error factor

User-approved working candidate is`no_U_K1`; see [working notebook](WORKING_MODEL.ipynb), [designation](WORKING_MODEL.md) and `WORKING_MODEL.json`. Retain historical bias, local polling error and real national movement. Shared-error alternatives remain sensitivities; earlier experimental model selection records are unchanged. No fresh fitting or data download. Next is a bounded review of N withU=0/K1 fixed, including missing-state polling checks and chamber-focused validation.


## National-factor strength and information-transfer review

[Notebook](NATIONAL_FACTOR_REVIEW.ipynb) and [design/findings](NATIONAL_FACTOR_REVIEW.md) complete the bounded review with U=0/K1 fixed. Stronger common variance modestly helps chamber scores but has mixed state and hidden-poll results. Past-only chamber selection helps September and slightly worsens October. Keep the current no_U_K1 designation; doubled national variance remains a sensitivity. Current input to N is state polling minus historical bias minus historical prior, with uncertainty weights; no independent national polling or features added.


## Poll timing and matched Student experiment

[Notebook](POLL_TIMING_STUDENT.ipynb), [design/findings](POLL_TIMING_STUDENT.md). Refit each half-life's historical polling calibration while freezing no-U electoral priors/national structure. Current past-cycle selection is90days/Gaussian, but it does not consistently outperform fixed30days across historical horizons. Matched df5/10 gives mixed performance and reduced late interval coverage. Keep the pinned30day Gaussian candidate. Next distinct timing question would be forecast-to-election movement uncertainty, not yet implemented.


## Coverage-adaptive poll decay

[Notebook](ADAPTIVE_POLL_DECAY.ipynb), [design/findings](ADAPTIVE_POLL_DECAY.md). Half-life depends on distinct recent firms with sharedk1/3/6; historical calibration repeated under the same rule. Adaptive forecasts modestly improve state-margin and chamber CRPS versus fixed30 but do not improve all seat-error/coverage metrics. Tuningk adds little. Current selectedk6 gives50.091expectedD/51Dpoint/70%48–52. Working30dayGaussian remains pinned.


## National feature-prior experiment

[Notebook](NATIONAL_FEATURE_PRIOR.ipynb), [design/findings](NATIONAL_FEATURE_PRIOR.md). One or two shared, shrunk feature coefficients inform the national prior before polling, with coefficient uncertainty propagated. Prior scale is chosen on the last three earlier held-out cycles. Approval-only is strongest for recent state accuracy; both features are strongest for chamber CRPS. Current both-feature forecast is 51.218 expected Democratic seats, 51 Democratic point calls and a central 70% range of 49–53. This remains an experimental comparison; the working model is unchanged.


## Feature priors with Student polling error

[Notebook](NATIONAL_FEATURE_STUDENT.ipynb), [findings](NATIONAL_FEATURE_STUDENT.md). The feature benefit persists, but df5/10 does not improve chamber CRPS or expected-seat MAE over matched Gaussian feature models. Late interval coverage generally falls. Current both-feature Student forecasts give about 51.3–51.4 expected D seats and a 49–53 central70% range; a near-zero Texas flip produces 52D point calls. The past-only selector chooses Gaussian for every current feature recipe. No promotion.


## Student national electoral surprises

[Notebook](ELECTORAL_SURPRISE_STUDENT.ipynb), [findings](ELECTORAL_SURPRISE_STUDENT.md). Only national electoral residual variance receives an inverse-gamma scale; Gaussian local movement/polling/feature uncertainty remain fixed. Variance-matched df10/5/3 mostly changes predictions slightly. Both-feature t3 improves late state MAE5.344→5.331pp and seatMAE0.972→0.967 but does not resolve2020/2022 coverage misses. Current selected df3 gives51.180 expectedD versusGaussian51.218, identical51Dpoint and49–53 central70%range. Working designation unchanged.


## Final bounded comparisons

[Notebook](FINAL_BASELINE_EXPERIMENTS.ipynb), [findings](FINAL_BASELINE_EXPERIMENTS.md). Local Student selection improves chamber metrics but loses late state calls/coverage. Event multiplier selects no inflation for both-feature model; all recent years flagged, preventing event-specific inference. Additional horizon variance adds little. Gaussian features+adaptive3 modestly improves margin MAE/chamberCRPS but not all seat-error/coverage metrics. Current bothadaptive51.151 expectedD, point51D49R,70%49–53; local-selectedt5 51.023 expectedD with same point/range. Working designation unchanged.


## Combined Student residual comparison

[Notebook](COMBINED_STUDENT_MODEL.ipynb), [results](COMBINED_STUDENT_MODEL_RESULTS.md). Joint Student national/local electoral and systematic polling residuals do not generally improve the Gaussian comparison. With both features, late matched-variance df5/3 coverage70 falls to62.1%/55.0% versusGaussian72.1%, and calls131/140 versus133/140. Inflation recovers calls but not overall calibration. Current Gaussian/df5/df3 matched-variance all51D49R point,49–53D70% interval; expectedD51.218/51.256/51.151. Both current feature-family selectors chooseGaussian1. Working designation unchanged; historical empirical-Bayes calibration remains frozen.


## Revision 26 — variance stability and published-model comparison

[Executed notebook](VARIANCE_AND_PUBLISHED_REVIEW.ipynb), [design](VARIANCE_STABILITY_REVIEW.md), [results/checklist](VARIANCE_AND_PUBLISHED_RESULTS.md). Gaussian no-feature and momentum+approval recipes remain fixed. Delete each of the newest three shared residual cycles from electoral/polling covariance estimation, refitting the original regularized estimator and preserving remaining weights, prior centers and selected penalties. Recompute affected Gaussian updates coherently. This is a residual-block influence check, not a variance posterior or a new full-pipeline CV. Baseline forecasts/covariances reproduce exactly.

Current no-feature expected D seats range 50.119–50.532 across deletion alternatives (base50.130); both-feature 51.227–51.461 (base51.218). Most point forecasts stay51D; omitting2022 polling residuals flips near-zeroTexas in two feature variants to52D. Do not optimize by choosing the favorable omission. Combined Student stays a side model.

Exact common-contest benchmarks use archived FiveThirtyEight2018/2020/2022 forecasts, Race to the WH2024 retrospective probability history and a limited Economist2022 correction check. Our late calls compare well, but FiveThirtyEight wins on2020/2022 Brier and2022 margin error; our80% intervals under-cover in those cycles. Dates, independent/special exclusions, missing metrics and post-selection limitations are explicit. Full-chamber totals are contextual because our ledger fixes some excluded outcomes. State-level and common-contest aggregates are the primary comparison.

19 targeted tests and26 artifact checks pass;300 forecasts,90 covariance refits,8620 stability rows,2208 matched benchmark rows,20 publisher/date comparisons. Seven notebook code cells executed, two figures inspected;29 previous notebooks/source artifacts/working designation preserved. Conditional Texas/wave/2024-error/price scenarios are documented but not run. No data refresh or promotion.


## Revision27 — current public comparison and conditional scenarios

[Executed notebook](CURRENT_COMPARISON_AND_SCENARIOS.ipynb), [definitions](CURRENT_COMPARISON_AND_SCENARIOS.md), [results/checklist](CURRENT_COMPARISON_AND_SCENARIOS_RESULTS.md). CurrentRace to the WH/DDHQ35state forecasts andSilver public control topline are archived. IndependentID/MT/NE/SD comparisons are flagged, not reclassified asDemocratic. Our feature model has47.8%Texas/35.1%Iowa versus74.6%/53.1%Race to the WH; Michigan75.2%vs78.8%. WestVirginia33.1%D versusabout1%externally exposes very wide no-poll uncertainty (posteriorSD43.86pp) despite meanR+19.23. This deserves a prior/variance review before treating its chamber contribution as reliable.

Both frozenGaussian families run48scenarios: Texas sign/exactmargin conditioning; uniform wave shifts and conditioning the existing national factor; matchedSeptember/October2024bias replay net of current correction, half/full strength andstate-pattern fallback; proportionateCPI/gas shocks with frozen normalizers/coefficients. No new covariance loading layer or duplicate poll/error update. Feature-model expectedD51.218 baseline,51.817givenTexasD,50.669givenTexasR,52.705uniformD+2,51.869knownnational+2,48.024/49.395September/October2024error,51.237severeprices. Texas effects on other states are modest. Prices have little effect conditional on fixed approval/polls because the fitted momentum coefficient isnearzero. The analyses retain current ballot/caucus assumptions and are not causal estimates.

11tests,66numerical checks and14artifact audits pass;1680state rows,200,000joint draws per scenario;9notebook code cells/2inspected figures. All30prior notebooks andsource/designation hashes preserved. Remaining substantive review: no-poll prior/variance outliers andindependent/caucus conventions. No data refresh or model promotion.


## Revision 28 — smoothed polling trends and sparse-state variance diagnosis

[Executed notebook](POLL_TREND_AND_SPARSE_REVIEW.ipynb), [design](POLL_TREND_AND_SPARSE_REVIEW.md), [results and checklist](POLL_TREND_AND_SPARSE_REVIEW_RESULTS.md). Matched-firm/metadata recent-versus-previous 30-day slopes, median pooling, J/(J+3) shrinkage and capped recent-level/half/full projection were compared with zero trend. Every variant refits past-only polling calibration; prior means, electoral covariance and feature fits remain fixed. Selection uses last-three-earlier-cycle chamber CRPS, separately by family/horizon.

For the feature family in 2016–2024, selected trend changes September calls 129→130/140 and MAE 6.809→6.829pp; October calls 133→131 and MAE 5.344→5.334. Late chamber CRPS improves 0.6662→0.6322, but there is no overall win. Current feature-family selector uses full trend: expected D 51.218→51.264, Texas 47.8%→52.1%, point calls 51→52 D, unchanged 49–53 central 70% interval. Only AK/IA/NC/TX have matched current trend support. No-feature selector retains baseline.

Sparse review reconstructs WV's prior misses, raw SD 32.57pp and variance multiplier 1.811 selected with only two recent local validation cycles. Its weighted residual mean is −21.86pp, centered SD 25.13pp: a lagging prior contributes substantially to the second moment used as uncertainty. With no polls, only 0.19% of variance is removed; posterior SD remains 43.86pp and Democratic probability 33.1%. NE/SD are additional high-variance independent proxies; LA has no admitted historical residuals and uses shared fallback. Diagnosis points to reviewing prior means and centered residual variance together, not a blanket sparse-state cap. No repair or promotion yet.

15 tests, 19 main audits and 1,368 sparse reconstruction checks pass; 150 forecasts, 60 calibration fits and 4,310 forecast rows. Nine notebook code cells executed, three figures inspected; all 31 older notebooks, source inputs and working designation preserved. Frozen September 17 data. Candidate-match limitations, small validation samples, repeated exploration and chamber proxy conventions remain explicit.


## Revision 29 — prior-center repair and conditional state influence

[Executed notebook](PRIOR_CENTER_REPAIR.ipynb), [design](PRIOR_CENTER_REPAIR.md), [results/checklist](PRIOR_CENTER_REPAIR_RESULTS.md). Five chronological center recipes (decay4/latest/same-seat and rolling prior-error corrections) with κ8 covariance refits, fixed/shared/state variance calibration and both Gaussian families. Polling remains fixed. Correction estimates use earlier errors; variance fits use out-of-time corrected-prior errors. Shared/state penalties use earlier-cycle WIS, and national/feature parameters are refitted with original earlier-selected feature τ.

Corrected decay + state penalties improves feature-model recent MAE 6.809→6.315 earlier and 5.344→5.222 late, WIS 4.053→3.827 / 3.101→3.055; calls fall by one at each horizon. The wider rolling selector worsens MAE; no promotion. Same-seat is useful diagnostically but not a general late improvement. Current corrected feature forecast: WV prior R+37.99, posterior R+31.90/SD20.55/D6.02% versus baseline R+19.23/SD43.86/D33.05%. Expected D seats 50.419, point51D/49R, 70%49–52. Original baseline remains pinned. Part of the change comes from stronger covariance shrinkage and different variance calibration; the unchanged decay4 control is retained.

Conditioning on a Texas D win in the original feature baseline shifts national movement +0.258pp and adds 0.077 expected D seats elsewhere; SC D shifts +0.362pp and adds 0.114 elsewhere. SC is rarer (12.0% versus47.8%) but local uncertainty dilutes its signal. Repaired model SC is3.36% and adds0.203 other seats. D/R mixtures recover baseline moments/probabilities; no duplicate poll/wave update.

13 tests, 13 main audits, 10 review audits and 28 conditional checks pass; 510 forecasts/14,654 rows,40 covariance fits. Eight notebook code cells/three inspected figures;32 earlier notebooks preserved. Louisiana fallback is traced to upstream explicit state-rule admission restrictions, not missing real elections. Historical admission and independent/caucus review remain open; empirical-Bayes and repeated-selection limits remain. No refresh or promotion.


## Revision30 — one signed state factor alongside national movement

[Executed notebook](SIGNED_STATE_FACTOR.ipynb), [design](SIGNED_STATE_FACTOR.md), [results/checklist](SIGNED_STATE_FACTOR_RESULTS.md). Added one centered, bounded, ridge-regularized loading per supported state and a standard-Normal signed factor. Existing national/feature/prior/polling parameters stay fixed; independent local variance is reduced by the new factor's variance contribution, preserving every marginal prior variance. Historical likelihood integrates latent national movement. λ0/.1/.25/.5 selected by last3past-cycle WIS, zero fallback; original/repaired and no-feature/both-feature controls.

Repaired-feature selected MAE6.315→6.307 earlier and5.222→5.206 late, calls128/132 unchanged, tiny WIS/chamberCRPS gains and slightly worse lateBrier. Original feature MAE/WIS slightly worse. Current repaired selectedλ.5 gives50.426expectedD (control50.419),51Dpoint,70%49–52. Signed links appear: IA–NH+.077, OH–IA+.067, IA–OR−.048. TX loading≈+.020pp; conditioningTexasD+10 still gives only+.537pp national/+0.149other expected seats. Paired coherent/opposing TX/OH surprises update N/Z differently, as intended.

Repaired-factor direction is sensitive to omitting2020 (cosine.416; maximumcurrent probability shift2.59pp); omitting2022/24 barely changes it. One pattern is not a causal issue label or a general state-similarity network. Keep as experimental sensitivity; no promotion or national-variance retuning.16tests/24artifact checks;60main+12deletionfits,300forecasts/8,620rows,18scenarios with100kdraws.8executed cells/3inspected figures;33older notebooks and source/designation preserved. FrozenSeptember17 data and upstream admission/caucus limits remain.
