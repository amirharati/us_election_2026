# All model-market pairs grouped by market

Y = buy Yes; N = buy No. P = model probability that the selected side pays $1 under the contract condition; it is not confidence that the model is correct. EV = base expected net profit after purchase depth and estimated fees. Budget and win/loss payoffs use those base costs. Stress adds the extra friction scenario and applies the probability haircut to the model probability. GO (green) survives stress; WEAK (amber) is positive before stress only; UNC (amber) is unresolved; NEG (red) is negative in expectation; N/A (gray) is unavailable. A status marked * uses a conditional settlement proxy: its P, EV and stress depend on the stated runoff, ranked-choice or candidate assumptions. These rows are amber even when the numerical edge is positive. Local P comes from the full predictive distribution. External P is a published point estimate or seat-histogram probability; equal endpoints are not a confidence interval. Simulation estimates have sampling error. All model rows are independent comparisons; there is no combined score.

Base: quoted ask depth plus estimated fees. Stress only: add 2¢ per share and reduce the selected-side probability by 2 percentage points (minimum zero).

## External forecast sources

RTWH and DDHQ are separate published forecasts, not new mixture components. They use the same ask depth, fees and sensitivity stresses as our models. Their displayed probabilities are point estimates, not confidence bounds; no state margin distribution is invented. DDHQ uses market inputs where disclosed, so its agreement with prices is not independent evidence. Publisher dates are independent of our forecast cutoff. Failed refreshes and forecasts older than the age limit are unpriced. Independent candidates stay separate from Democrats. Chamber comparisons remain conditional on publisher caucus conventions. Silver public commentary and Inside Elections ratings remain in notebook 04; they are not numerical state models here.

| Model   | Published   | Refresh                |   Race records | Note                                              |
|:--------|:------------|:-----------------------|---------------:|:--------------------------------------------------|
| RTWH    | 2026-09-25  | recent publisher cache |             35 | State winners/control; no margin distribution.    |
| DDHQ    | 2026-09-25  | recent publisher cache |             35 | Seat histogram available. Includes market inputs. |

[Normalized publisher snapshot and receipts](external_forecasts.json)

## Model codes

| Code   | Model name                         |
|:-------|:-----------------------------------|
| GB     | Gaussian Bayesian                  |
| ST     | Matched Student-t (df5)            |
| MX     | Four-model mixture                 |
| M10    | Mixture: 10% shift toward baseline |
| RTWH   | Race to the WH                     |
| DDHQ   | DDHQ                               |

## Will Brian Bengs win the South Dakota Senate race in 2026?
Contract 630939; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         4.8 |         4.98 | +95.02 / −4.98   | 19.07×        |
| No     |        96   |        96.15 | +3.85 / −96.15   | 0.04×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG*     |    0.06 |    -4.92 |        -6.98 |
| GB / N         | WEAK*    |   99.94 |     3.78 |        -0.22 |
| ST / Y         | NEG*     |    0.82 |    -4.16 |        -6.98 |
| ST / N         | WEAK*    |   99.18 |     3.02 |        -0.98 |
| MX / Y         | WEAK*    |    8.12 |     3.14 |        -0.86 |
| MX / N         | NEG*     |   91.88 |    -4.28 |        -8.28 |
| M10 / Y        | WEAK*    |    7.15 |     2.17 |        -1.83 |
| M10 / N        | NEG*     |   92.85 |    -3.30 |        -7.30 |
| RTWH / Y       | GO       |   12.90 |     7.92 |         3.92 |
| RTWH / N       | NEG      |   87.10 |    -9.05 |       -13.05 |
| DDHQ / Y       | NEG      |    3.00 |    -1.98 |        -5.98 |
| DDHQ / N       | WEAK     |   97.00 |     0.85 |        -3.15 |

GB, ST, MX, M10: The strongest D/Independent-versus-R margin approximates the winning side; third-candidate outcomes are not jointly modeled. Independents remain IND.
RTWH (2026-09-25): Bengs retains IND despite publisher column. Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will Dan Sullivan win the Alaska Senate race in 2026?
Contract 634974; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          29 |        29.82 | +70.18 / −29.82  | 2.35×         |
| No     |          72 |        72.81 | +27.19 / −72.81  | 0.37×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO*      | 66.12   | 36.30    | 32.29978904881732   |
| GB / N         | NEG*     | 33.88   | -38.93   | -42.92978904881731  |
| ST / Y         | GO*      | 69.44   | 39.62    | 35.617025000000005  |
| ST / N         | NEG*     | 30.56   | -42.25   | -46.247024999999994 |
| MX / Y         | GO*      | 60.04   | 30.22    | 26.216712499999993  |
| MX / N         | NEG*     | 39.96   | -32.85   | -36.84671249999999  |
| M10 / Y        | GO*      | 60.40   | 30.57    | 26.574577083333327  |
| M10 / N        | NEG*     | 39.60   | -33.20   | -37.20457708333333  |
| RTWH / Y       | GO       | 43.40   | 13.58    | 9.576400000000001   |
| RTWH / N       | NEG      | 56.60   | -16.21   | -20.20639999999999  |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

GB, ST, MX, M10: Ranked-choice transfers are not separately modeled; the modeled margin is used as a proxy for the eventual winner.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Requested party/candidate has no published probability; absence is not treated as zero.

## Will Mary Peltola win the Alaska Senate race in 2026?
Contract 634976; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          73 |        73.79 | +26.21 / −73.79  | 0.36×         |
| No     |          28 |        28.81 | +71.19 / −28.81  | 2.47×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG*     |   33.88 |   -39.91 |       -43.91 |
| GB / N         | GO*      |   66.12 |    37.32 |        33.32 |
| ST / Y         | NEG*     |   30.56 |   -43.23 |       -47.23 |
| ST / N         | GO*      |   69.44 |    40.63 |        36.63 |
| MX / Y         | NEG*     |   39.96 |   -33.83 |       -37.83 |
| MX / N         | GO*      |   60.04 |    31.23 |        27.23 |
| M10 / Y        | NEG*     |   39.60 |   -34.19 |       -38.19 |
| M10 / N        | GO*      |   60.40 |    31.59 |        27.59 |
| RTWH / Y       | NEG      |   56.60 |   -17.19 |       -21.19 |
| RTWH / N       | GO       |   43.40 |    14.59 |        10.59 |
| DDHQ / Y       | NEG      |   61.00 |   -12.79 |       -16.79 |
| DDHQ / N       | GO       |   39.00 |    10.19 |         6.19 |

GB, ST, MX, M10: Ranked-choice transfers are not separately modeled; the modeled margin is used as a proxy for the eventual winner.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Publisher party aggregate covers multiple candidates and is not assigned to an individual. Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will Todd Achilles win the Idaho Senate race in 2026?
Contract 630707; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.18 |         9.51 | +90.49 / −9.51   | 9.51×         |
| No     |       95.92 |        96.08 | +3.92 / −96.08   | 0.04×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | N/A      | —       | —        | —                   |
| GB / N         | N/A      | —       | —        | —                   |
| ST / Y         | N/A      | —       | —        | —                   |
| ST / N         | N/A      | —       | —        | —                   |
| MX / Y         | N/A      | —       | —        | —                   |
| MX / N         | N/A      | —       | —        | —                   |
| M10 / Y        | N/A      | —       | —        | —                   |
| M10 / N        | N/A      | —       | —        | —                   |
| RTWH / Y       | NEG      | 4.20    | -5.31    | -9.31349            |
| RTWH / N       | NEG      | 95.80   | -0.28    | -4.2765400000000175 |
| DDHQ / Y       | NEG      | 3.00    | -6.51    | -10.513490000000001 |
| DDHQ / N       | WEAK     | 97.00   | 0.92     | -3.0765400000000165 |

GB, ST, MX, M10: The model has no separate probability for this candidate among multiple contenders on the same modeled side.
RTWH (2026-09-25): Achilles retains IND despite publisher column. Publisher omits separate probabilities for reviewed contenders: Natalie Fleming. Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Publisher omits separate probabilities for reviewed contenders: Natalie Fleming. Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will an Independent win the Montana Senate race in 2026?
Contract 630833; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        10.1 |        10.46 | +89.54 / −10.46  | 8.56×         |
| No     |        90.6 |        90.94 | +9.06 / −90.94   | 0.10×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | N/A      | —       | —        | —                   |
| GB / N         | N/A      | —       | —        | —                   |
| ST / Y         | N/A      | —       | —        | —                   |
| ST / N         | N/A      | —       | —        | —                   |
| MX / Y         | N/A      | —       | —        | —                   |
| MX / N         | N/A      | —       | —        | —                   |
| M10 / Y        | N/A      | —       | —        | —                   |
| M10 / N        | N/A      | —       | —        | —                   |
| RTWH / Y       | GO       | 22.10   | 11.64    | 7.636799999999999   |
| RTWH / N       | NEG      | 77.90   | -13.04   | -17.040660000000006 |
| DDHQ / Y       | NEG      | 10.00   | -0.46    | -4.463200000000002  |
| DDHQ / N       | NEG      | 90.00   | -0.94    | -4.940660000000008  |

GB, ST, MX, M10: The model forecasts the strongest D/Independent side versus R; it cannot allocate that probability to this party separately.
RTWH (2026-09-25): Publisher omits separate probabilities for reviewed contenders: Alani Bankhead. Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Publisher omits separate probabilities for reviewed contenders: Alani Bankhead. Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will an independent win the Nebraska Senate race in 2026?
Contract 634893; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          31 |        31.86 | +68.14 / −31.86  | 2.14×         |
| No     |          70 |        70.84 | +29.16 / −70.84  | 0.41×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG*     |   16.93 |   -14.93 |       -18.93 |
| GB / N         | GO*      |   83.07 |    12.23 |         8.23 |
| ST / Y         | NEG*     |   19.31 |   -12.54 |       -16.54 |
| ST / N         | GO*      |   80.69 |     9.85 |         5.85 |
| MX / Y         | NEG*     |   29.66 |    -2.19 |        -6.19 |
| MX / N         | NEG*     |   70.34 |    -0.50 |        -4.50 |
| M10 / Y        | NEG*     |   29.78 |    -2.08 |        -6.08 |
| M10 / N        | NEG*     |   70.22 |    -0.62 |        -4.62 |
| RTWH / Y       | GO       |   36.00 |     4.14 |         0.14 |
| RTWH / N       | NEG      |   64.00 |    -6.84 |       -10.84 |
| DDHQ / Y       | NEG      |   17.00 |   -14.86 |       -18.86 |
| DDHQ / N       | GO       |   83.00 |    12.16 |         8.16 |

GB, ST, MX, M10: The strongest D/Independent-versus-R margin approximates the winning side; third-candidate outcomes are not jointly modeled. Independents remain IND.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democratic Party candidate win the 2026 Florida Senate election by 3% or more?
Contract 3343186; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        6.12 |         6.35 | +93.65 / −6.35   | 14.75×        |
| No     |       97.42 |        97.52 | +2.48 / −97.52   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 8.75    | 2.40     | -1.6033951884954365 |
| GB / N         | NEG      | 91.25   | -6.27    | -10.266884811504575 |
| ST / Y         | NEG      | 4.67    | -1.67    | -5.67475            |
| ST / N         | NEG      | 95.33   | -2.20    | -6.195530000000006  |
| MX / Y         | WEAK     | 9.58    | 3.23     | -0.7729791666666666 |
| MX / N         | NEG      | 90.42   | -7.10    | -11.097300833333344 |
| M10 / Y        | WEAK     | 8.39    | 2.04     | -1.962041666666667  |
| M10 / N        | NEG      | 91.61   | -5.91    | -9.90823833333334   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Iowa Senate election by 0%-3%?
Contract 3343531; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          20 |        20.64 | +79.36 / −20.64  | 3.84×         |
| No     |          81 |        81.62 | +18.38 / −81.62  | 0.23×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 16.65   | -3.99    | -7.9945131404447185 |
| GB / N         | WEAK     | 83.35   | 1.74     | -2.2610868595552835 |
| ST / Y         | NEG      | 18.59   | -2.05    | -6.052499999999997  |
| ST / N         | NEG      | 81.41   | -0.20    | -4.2031000000000045 |
| MX / Y         | NEG      | 17.54   | -3.10    | -7.1038541666666655 |
| MX / N         | WEAK     | 82.46   | 0.85     | -3.151745833333342  |
| M10 / Y        | NEG      | 17.04   | -3.60    | -7.596666666666667  |
| M10 / N        | WEAK     | 82.96   | 1.34     | -2.6589333333333354 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Iowa Senate election by 12% or more?
Contract 3343535; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        8.41 |         8.71 | +91.29 / −8.71   | 10.48×        |
| No     |       97.27 |        97.38 | +2.62 / −97.38   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.88    | -7.83    | -10.713720000000002 |
| GB / N         | WEAK     | 99.12   | 1.74     | -2.25959304614749   |
| ST / Y         | NEG      | 0.34    | -8.37    | -10.713720000000002 |
| ST / N         | WEAK     | 99.66   | 2.28     | -1.7172450000000117 |
| MX / Y         | NEG      | 1.02    | -7.70    | -10.713720000000002 |
| MX / N         | WEAK     | 98.98   | 1.61     | -2.3939637500000055 |
| M10 / Y        | NEG      | 0.92    | -7.79    | -10.713720000000002 |
| M10 / N        | WEAK     | 99.08   | 1.70     | -2.2983387500000063 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 20%-25%?
Contract 3343812; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       14.23 |        14.72 | +85.28 / −14.72  | 5.79×         |
| No     |       89    |        89.39 | +10.61 / −89.39  | 0.12×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 26.64   | 11.92    | 7.921425398573733   |
| GB / N         | NEG      | 73.36   | -16.03   | -20.03373539857374  |
| ST / Y         | GO       | 26.03   | 11.31    | 7.310539999999999   |
| ST / N         | NEG      | 73.97   | -15.42   | -19.42284999999999  |
| MX / Y         | GO       | 27.23   | 12.51    | 8.510696249999997   |
| MX / N         | NEG      | 72.77   | -16.62   | -20.623006249999992 |
| M10 / Y        | GO       | 29.69   | 14.97    | 10.972258750000002  |
| M10 / N        | NEG      | 70.31   | -19.08   | -23.084568750000003 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 35%-40%?
Contract 3343815; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          20 |        20.64 | +79.36 / −20.64  | 3.84×         |
| No     |          82 |        82.59 | +17.41 / −82.59  | 0.21×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 6.19    | -14.45   | -18.45385779486262  |
| GB / N         | GO       | 93.81   | 11.22    | 7.22345779486262    |
| ST / Y         | NEG      | 4.22    | -16.42   | -20.42125           |
| ST / N         | GO       | 95.78   | 13.19    | 9.190849999999994   |
| MX / Y         | NEG      | 5.08    | -15.56   | -19.559166666666666 |
| MX / N         | GO       | 94.92   | 12.33    | 8.328766666666665   |
| M10 / Y        | NEG      | 3.70    | -16.94   | -20.93598958333333  |
| M10 / N        | GO       | 96.30   | 13.71    | 9.70558958333333    |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 40%-45%?
Contract 3343816; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          13 |        13.45 | +86.55 / −13.45  | 6.43×         |
| No     |          88 |        88.42 | +11.58 / −88.42  | 0.13×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)        |
|:---------------|:---------|:--------|:---------|:------------------|
| GB / Y         | NEG      | 0.95    | -12.51   | -15.4524          |
| GB / N         | GO       | 99.05   | 10.63    | 6.631312629596408 |
| ST / Y         | NEG      | 0.39    | -13.06   | -15.4524          |
| ST / N         | GO       | 99.61   | 11.18    | 7.183849999999992 |
| MX / Y         | NEG      | 0.81    | -12.65   | -15.4524          |
| MX / N         | GO       | 99.19   | 10.77    | 6.772079166666668 |
| M10 / Y        | NEG      | 0.55    | -12.90   | -15.4524          |
| M10 / N        | GO       | 99.45   | 11.03    | 7.025829166666664 |
| RTWH / Y       | N/A      | —       | —        | —                 |
| RTWH / N       | N/A      | —       | —        | —                 |
| DDHQ / Y       | N/A      | —       | —        | —                 |
| DDHQ / N       | N/A      | —       | —        | —                 |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Michigan Senate election by 3%-6%?
Contract 3343888; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          23 |        23.71 | +76.29 / −23.71  | 3.22×         |
| No     |          79 |        79.66 | +20.34 / −79.66  | 0.26×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 19.52   | -4.19    | -8.189897716121688  |
| GB / N         | WEAK     | 80.48   | 0.82     | -3.1821022838783186 |
| ST / Y         | NEG      | 23.67   | -0.04    | -4.042775000000002  |
| ST / N         | NEG      | 76.33   | -3.33    | -7.329225000000005  |
| MX / Y         | NEG      | 20.47   | -3.24    | -7.2399625000000025 |
| MX / N         | NEG      | 79.53   | -0.13    | -4.132037500000008  |
| M10 / Y        | NEG      | 20.88   | -2.83    | -6.83225416666667   |
| M10 / N        | NEG      | 79.12   | -0.54    | -4.539745833333331  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Michigan Senate election by 6%-9%?
Contract 3343889; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          22 |        22.69 | +77.31 / −22.69  | 3.41×         |
| No     |          80 |        80.64 | +19.36 / −80.64  | 0.24×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 19.14   | -3.54    | -7.5441279221754725 |
| GB / N         | WEAK     | 80.86   | 0.22     | -3.7822720778245333 |
| ST / Y         | WEAK     | 23.20   | 0.51     | -3.4863999999999953 |
| ST / N         | NEG      | 76.80   | -3.84    | -7.8400000000000025 |
| MX / Y         | NEG      | 19.73   | -2.96    | -6.95567083333333   |
| MX / N         | NEG      | 80.27   | -0.37    | -4.370729166666676  |
| M10 / Y        | NEG      | 18.49   | -4.20    | -8.197389583333328  |
| M10 / N        | WEAK     | 81.51   | 0.87     | -3.129010416666666  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 12%-15%?
Contract 3343942; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.96 |        10.32 | +89.68 / −10.32  | 8.69×         |
| No     |       95.12 |        95.31 | +4.69 / −95.31   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 19.73   | 9.41     | 5.413775063107476   |
| GB / N         | NEG      | 80.27   | -15.04   | -19.035795063107475 |
| ST / Y         | GO       | 20.99   | 10.67    | 6.671110000000001   |
| ST / N         | NEG      | 79.01   | -16.29   | -20.293130000000005 |
| MX / Y         | GO       | 15.58   | 5.26     | 1.2638183333333344  |
| MX / N         | NEG      | 84.42   | -10.89   | -14.885838333333334 |
| M10 / Y        | GO       | 16.41   | 6.10     | 2.0958495833333326  |
| M10 / N        | NEG      | 83.59   | -11.72   | -15.717869583333332 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 18% or more?
Contract 3343944; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        5.59 |         5.8  | +94.20 / −5.80   | 16.23×        |
| No     |       98.56 |        98.62 | +1.38 / −98.62   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 12.30   | 6.50     | 2.495217329742615   |
| GB / N         | NEG      | 87.70   | -10.92   | -14.916167329742613 |
| ST / Y         | WEAK     | 9.24    | 3.43     | -0.5662             |
| ST / N         | NEG      | 90.76   | -7.85    | -11.854749999999992 |
| MX / Y         | WEAK     | 7.28    | 1.48     | -2.5191166666666667 |
| MX / N         | NEG      | 92.72   | -5.90    | -9.901833333333322  |
| M10 / Y        | WEAK     | 8.68    | 2.88     | -1.1223458333333312 |
| M10 / N        | NEG      | 91.32   | -7.30    | -11.29860416666666  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 3%-6%?
Contract 3343939; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       21    |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |       80.47 |        81.1  | +18.90 / −81.10  | 0.23×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 9.93    | -11.73   | -15.731893958934224 |
| GB / N         | GO       | 90.07   | 8.97     | 4.97171395893421    |
| ST / Y         | NEG      | 9.62    | -12.04   | -16.041725          |
| ST / N         | GO       | 90.38   | 9.28     | 5.281544999999987   |
| MX / Y         | NEG      | 14.00   | -7.66    | -11.65917291666667  |
| MX / N         | GO       | 86.00   | 4.90     | 0.8989929166666522  |
| M10 / Y        | NEG      | 13.04   | -8.62    | -12.618704166666667 |
| M10 / N        | GO       | 86.96   | 5.86     | 1.858524166666664   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 9%-12%?
Contract 3343941; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          15 |        15.51 | +84.49 / −15.51  | 5.45×         |
| No     |          86 |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)           |
|:---------------|:---------|:--------|:---------|:---------------------|
| GB / Y         | GO       | 20.72   | 5.21     | 1.2076287263198844   |
| GB / N         | NEG      | 79.28   | -7.20    | -11.19922872631989   |
| ST / Y         | GO       | 21.75   | 6.24     | 2.236875000000002    |
| ST / N         | NEG      | 78.25   | -8.23    | -12.228475000000005  |
| MX / Y         | WEAK     | 19.09   | 3.58     | -0.42307291666666413 |
| MX / N         | NEG      | 80.91   | -5.57    | -9.568527083333333   |
| M10 / Y        | WEAK     | 19.27   | 3.76     | -0.2361979166666639  |
| M10 / N        | NEG      | 80.73   | -5.76    | -9.755402083333342   |
| RTWH / Y       | N/A      | —       | —        | —                    |
| RTWH / N       | N/A      | —       | —        | —                    |
| DDHQ / Y       | N/A      | —       | —        | —                    |
| DDHQ / N       | N/A      | —       | —        | —                    |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 15%-18%?
Contract 3343972; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          16 |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |          85 |        85.51 | +14.49 / −85.51  | 0.17×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 15.54   | -1.00    | -4.999703544712824  |
| GB / N         | NEG      | 84.46   | -1.05    | -5.0478964552871926 |
| ST / Y         | WEAK     | 17.72   | 1.18     | -2.8219750000000015 |
| ST / N         | NEG      | 82.28   | -3.23    | -7.225625000000013  |
| MX / Y         | NEG      | 16.12   | -0.41    | -4.4132250000000015 |
| MX / N         | NEG      | 83.88   | -1.63    | -5.634375000000014  |
| M10 / Y        | NEG      | 16.12   | -0.41    | -4.413433333333333  |
| M10 / N        | NEG      | 83.88   | -1.63    | -5.634166666666684  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 18%-21%?
Contract 3343973; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          24 |        24.73 | +75.27 / −24.73  | 3.04×         |
| No     |          77 |        77.71 | +22.29 / −77.71  | 0.29×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 13.91   | -10.82   | -14.824214129253239 |
| GB / N         | GO       | 86.09   | 8.39     | 4.386214129253229   |
| ST / Y         | NEG      | 15.55   | -9.18    | -13.182725000000003 |
| ST / N         | GO       | 84.45   | 6.74     | 2.7447249999999923  |
| MX / Y         | NEG      | 14.29   | -10.44   | -14.443975000000002 |
| MX / N         | GO       | 85.71   | 8.01     | 4.005974999999995   |
| M10 / Y        | NEG      | 14.25   | -10.48   | -14.48345416666667  |
| M10 / N        | GO       | 85.75   | 8.05     | 4.045454166666662   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 9%-12%?
Contract 3343970; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         7   |         7.26 | +92.74 / −7.26   | 12.77×        |
| No     |        95.5 |        95.67 | +4.33 / −95.67   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 12.26   | 5.00     | 1.0035590962532677  |
| GB / N         | NEG      | 87.74   | -7.94    | -11.935859096253266 |
| ST / Y         | GO       | 12.71   | 5.45     | 1.4520999999999982  |
| ST / N         | NEG      | 87.29   | -8.38    | -12.384399999999996 |
| MX / Y         | GO       | 12.36   | 5.10     | 1.096839583333331   |
| MX / N         | NEG      | 87.64   | -8.03    | -12.029139583333336 |
| M10 / Y        | GO       | 12.43   | 5.17     | 1.1735062500000004  |
| M10 / N        | NEG      | 87.57   | -8.11    | -12.105806250000006 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 North Carolina Senate election by 0%-3%?
Contract 3344033; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          16 |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |          86 |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)           |
|:---------------|:---------|:--------|:---------|:---------------------|
| GB / Y         | WEAK     | 17.50   | 0.96     | -3.0380164851866844  |
| GB / N         | NEG      | 82.50   | -3.98    | -7.981183514813317   |
| ST / Y         | WEAK     | 18.07   | 1.54     | -2.462600000000001   |
| ST / N         | NEG      | 81.92   | -4.56    | -8.556600000000003   |
| MX / Y         | WEAK     | 20.36   | 3.82     | -0.18187083333333354 |
| MX / N         | NEG      | 79.64   | -6.84    | -10.837329166666676  |
| M10 / Y        | WEAK     | 20.46   | 3.92     | -0.07556874999999907 |
| M10 / N        | NEG      | 79.54   | -6.94    | -10.943631250000008  |
| RTWH / Y       | N/A      | —       | —        | —                    |
| RTWH / N       | N/A      | —       | —        | —                    |
| DDHQ / Y       | N/A      | —       | —        | —                    |
| DDHQ / N       | N/A      | —       | —        | —                    |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 North Carolina Senate election by 12%-15%?
Contract 3344037; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       14.91 |        15.42 | +84.58 / −15.42  | 5.49×         |
| No     |       87.4  |        87.84 | +12.16 / −87.84  | 0.14×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 6.68    | -8.74    | -12.737205590328129 |
| GB / N         | GO       | 93.32   | 5.48     | 1.480565590328109   |
| ST / Y         | NEG      | 4.72    | -10.69   | -14.691140000000003 |
| ST / N         | GO       | 95.28   | 7.43     | 3.4344999999999843  |
| MX / Y         | NEG      | 4.05    | -11.37   | -15.369994166666668 |
| MX / N         | GO       | 95.95   | 8.11     | 4.1133541666666495  |
| M10 / Y        | NEG      | 4.01    | -11.40   | -15.40374416666667  |
| M10 / N        | GO       | 95.99   | 8.15     | 4.147104166666649   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 North Carolina Senate election by 18% or more?
Contract 3344039; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       11.77 |        12.18 | +87.82 / −12.18  | 7.21×         |
| No     |       96.71 |        96.83 | +3.17 / −96.83   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.62    | -11.56   | -14.18417           |
| GB / N         | WEAK     | 99.38   | 2.55     | -1.4531172754779995 |
| ST / Y         | NEG      | 0.29    | -11.90   | -14.18417           |
| ST / N         | WEAK     | 99.71   | 2.88     | -1.1175000000000157 |
| MX / Y         | NEG      | 0.26    | -11.93   | -14.18417           |
| MX / N         | WEAK     | 99.74   | 2.91     | -1.0854166666666831 |
| M10 / Y        | NEG      | 0.25    | -11.93   | -14.18417           |
| M10 / N        | WEAK     | 99.75   | 2.92     | -1.083020833333348  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 North Carolina Senate election by 3%-6%?
Contract 3344034; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          16 |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |          85 |        85.51 | +14.49 / −85.51  | 0.17×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 23.03   | 6.49     | 2.4906914225439336  |
| GB / N         | NEG      | 76.97   | -8.54    | -12.538291422543946 |
| ST / Y         | GO       | 27.96   | 11.42    | 7.418649999999996   |
| ST / N         | NEG      | 72.04   | -13.47   | -17.466250000000006 |
| MX / Y         | GO       | 28.21   | 11.67    | 7.672191666666664   |
| MX / N         | NEG      | 71.79   | -13.72   | -17.719791666666673 |
| M10 / Y        | GO       | 28.19   | 11.66    | 7.655837499999999   |
| M10 / N        | NEG      | 71.81   | -13.70   | -17.703437500000017 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 North Carolina Senate election by 9%-12%?
Contract 3344036; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       17.74 |        18.32 | +81.68 / −18.32  | 4.46×         |
| No     |       87.4  |        87.84 | +12.16 / −87.84  | 0.14×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 14.23   | -4.10    | -8.095974274735969  |
| GB / N         | NEG      | 85.77   | -2.07    | -6.068245725264044  |
| ST / Y         | NEG      | 13.50   | -4.83    | -8.826945000000002  |
| ST / N         | NEG      | 86.50   | -1.34    | -5.337275000000008  |
| MX / Y         | NEG      | 11.48   | -6.85    | -10.846892916666668 |
| MX / N         | WEAK     | 88.52   | 0.68     | -3.3173270833333435 |
| M10 / Y        | NEG      | 11.41   | -6.92    | -10.915851250000001 |
| M10 / N        | WEAK     | 88.59   | 0.75     | -3.248368750000008  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Ohio Senate election by 0%-3%?
Contract 3344047; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       19    |        19.62 | +80.38 / −19.62  | 4.10×         |
| No     |       83.41 |        83.96 | +16.04 / −83.96  | 0.19×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 20.16   | 0.54     | -3.4601456718344634 |
| GB / N         | NEG      | 79.84   | -4.12    | -8.119544328165517  |
| ST / Y         | GO       | 24.12   | 4.50     | 0.5031500000000022  |
| ST / N         | NEG      | 75.88   | -8.08    | -12.082839999999983 |
| MX / Y         | WEAK     | 21.96   | 2.34     | -1.660079166666664  |
| MX / N         | NEG      | 78.04   | -5.92    | -9.919610833333314  |
| M10 / Y        | WEAK     | 22.35   | 2.73     | -1.26549583333333   |
| M10 / N        | NEG      | 77.65   | -6.31    | -10.314194166666658 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Ohio Senate election by 3%-6%?
Contract 3344048; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          23 |        23.71 | +76.29 / −23.71  | 3.22×         |
| No     |          79 |        79.66 | +20.34 / −79.66  | 0.26×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 20.20   | -3.50    | -7.5041260243810335 |
| GB / N         | WEAK     | 79.80   | 0.13     | -3.8678739756189744 |
| ST / Y         | WEAK     | 24.94   | 1.24     | -2.764650000000002  |
| ST / N         | NEG      | 75.06   | -4.61    | -8.607350000000002  |
| MX / Y         | NEG      | 21.15   | -2.56    | -6.560795833333335  |
| MX / N         | NEG      | 78.85   | -0.81    | -4.811204166666672  |
| M10 / Y        | NEG      | 20.11   | -3.60    | -7.5958479166666715 |
| M10 / N        | WEAK     | 79.89   | 0.22     | -3.7761520833333395 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Ohio Senate election by 6%-9%?
Contract 3344049; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          81 |        81.62 | +18.38 / −81.62  | 0.23×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 15.40   | -6.26    | -10.264097303510939 |
| GB / N         | WEAK     | 84.60   | 2.98     | -1.0151026964890675 |
| ST / Y         | NEG      | 16.19   | -5.47    | -9.469849999999996  |
| ST / N         | WEAK     | 83.81   | 2.19     | -1.8093500000000098 |
| MX / Y         | NEG      | 14.57   | -7.09    | -11.092089583333332 |
| MX / N         | WEAK     | 85.43   | 3.81     | -0.1871104166666693 |
| M10 / Y        | NEG      | 13.08   | -8.58    | -12.582089583333333 |
| M10 / N        | GO       | 86.92   | 5.30     | 1.3028895833333332  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 0%-5%?
Contract 3344097; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        8.91 |         9.23 | +90.77 / −9.23   | 9.84×         |
| No     |       99.7  |        99.71 | +0.29 / −99.71   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.09    | -9.14    | -11.227139999999999 |
| GB / N         | WEAK     | 99.91   | 0.20     | -3.8023471132106694 |
| ST / Y         | NEG      | 0.11    | -9.11    | -11.227139999999999 |
| ST / N         | WEAK     | 99.89   | 0.18     | -3.8244600000000073 |
| MX / Y         | NEG      | 0.66    | -8.56    | -11.227139999999999 |
| MX / N         | NEG      | 99.34   | -0.37    | -4.374616250000008  |
| M10 / Y        | NEG      | 0.77    | -8.46    | -11.227139999999999 |
| M10 / N        | NEG      | 99.23   | -0.48    | -4.481647500000008  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 10%-15%?
Contract 3344099; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        1.45 |         1.51 | +98.49 / −1.51   | 65.25×        |
| No     |       99.3  |        99.33 | +0.67 / −99.33   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 4.53    | 3.02     | -0.9773001919941894 |
| GB / N         | NEG      | 95.47   | -3.86    | -7.8598998080058    |
| ST / Y         | WEAK     | 3.53    | 2.02     | -1.9781500000000003 |
| ST / N         | NEG      | 96.47   | -2.86    | -6.859049999999989  |
| MX / Y         | GO       | 7.72    | 6.21     | 2.2087770833333327  |
| MX / N         | NEG      | 92.28   | -7.05    | -11.045977083333325 |
| M10 / Y        | GO       | 8.45    | 6.94     | 2.9375270833333333  |
| M10 / N        | NEG      | 91.55   | -7.77    | -11.774727083333325 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 15%-20%?
Contract 3344100; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10.89 |        11.26 | +88.74 / −11.26  | 7.88×         |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 14.27   | 3.01     | -0.990395058709763  |
| GB / N         | NEG      | 85.73   | -13.89   | -17.88934494129022  |
| ST / Y         | NEG      | 11.22   | -0.05    | -4.048175000000001  |
| ST / N         | NEG      | 88.78   | -10.83   | -14.83156499999998  |
| MX / Y         | GO       | 16.65   | 5.38     | 1.3841166666666682  |
| MX / N         | NEG      | 83.35   | -16.26   | -20.26385666666666  |
| M10 / Y        | GO       | 17.63   | 6.37     | 2.365887500000002   |
| M10 / N        | NEG      | 82.37   | -17.25   | -21.245627499999987 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 20%-25%?
Contract 3344101; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       15.93 |        16.46 | +83.54 / −16.46  | 5.07×         |
| No     |       87.93 |        88.35 | +11.65 / −88.35  | 0.13×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 26.25   | 9.79     | 5.78644705392817    |
| GB / N         | NEG      | 73.75   | -14.60   | -18.59983705392816  |
| ST / Y         | GO       | 24.83   | 8.37     | 4.372195000000001   |
| ST / N         | NEG      | 75.17   | -13.19   | -17.185584999999993 |
| MX / Y         | GO       | 25.32   | 8.86     | 4.856726250000001   |
| MX / N         | NEG      | 74.68   | -13.67   | -17.67011624999999  |
| M10 / Y        | GO       | 25.88   | 9.42     | 5.4152679166666635  |
| M10 / N        | NEG      | 74.12   | -14.23   | -18.228657916666656 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 25%-30%?
Contract 3344102; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          22 |        22.69 | +77.31 / −22.69  | 3.41×         |
| No     |          79 |        79.66 | +20.34 / −79.66  | 0.26×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 28.21   | 5.52     | 1.5239343496978197  |
| GB / N         | NEG      | 71.79   | -7.87    | -11.873934349697823 |
| ST / Y         | GO       | 32.07   | 9.39     | 5.388599999999999   |
| ST / N         | NEG      | 67.92   | -11.74   | -15.738600000000002 |
| MX / Y         | WEAK     | 25.34   | 2.65     | -1.346816666666664  |
| MX / N         | NEG      | 74.66   | -5.00    | -9.00318333333333   |
| M10 / Y        | WEAK     | 24.57   | 1.89     | -2.1129104166666606 |
| M10 / N        | NEG      | 75.43   | -4.24    | -8.237089583333345  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 5%-10%?
Contract 3344098; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         0.3 |         0.31 | +99.69 / −0.31   | 319.55×       |
| No     |        99.8 |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 0.84    | 0.53     | -2.31196            |
| GB / N         | NEG      | 99.16   | -0.65    | -4.64700341288874   |
| ST / Y         | WEAK     | 0.77    | 0.46     | -2.31196            |
| ST / N         | NEG      | 99.23   | -0.58    | -4.579854999999999  |
| MX / Y         | WEAK     | 2.65    | 2.34     | -1.6575329166666666 |
| MX / N         | NEG      | 97.35   | -2.46    | -6.462407083333333  |
| M10 / Y        | WEAK     | 2.98    | 2.67     | -1.3283662500000002 |
| M10 / N        | NEG      | 97.02   | -2.79    | -6.791573750000001  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Texas Senate election by 3%-6%?
Contract 3344142; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          80 |        80.64 | +19.36 / −80.64  | 0.24×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 18.36   | -3.30    | -7.304822316586169  |
| GB / N         | WEAK     | 81.64   | 1.00     | -2.998777683413833  |
| ST / Y         | NEG      | 19.16   | -2.50    | -6.504224999999996  |
| ST / N         | WEAK     | 80.84   | 0.20     | -3.7993750000000044 |
| MX / Y         | NEG      | 17.81   | -3.86    | -7.857402083333332  |
| MX / N         | WEAK     | 82.19   | 1.55     | -2.4461979166666703 |
| M10 / Y        | NEG      | 17.92   | -3.74    | -7.742141666666663  |
| M10 / N        | WEAK     | 82.08   | 1.44     | -2.561458333333344  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Texas Senate election by 9%-12%?
Contract 3344144; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        4.95 |         5.14 | +94.86 / −5.14   | 18.46×        |
| No     |       95.2  |        95.38 | +4.62 / −95.38   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 3.57    | -1.57    | -5.565827084375543  |
| GB / N         | WEAK     | 96.43   | 1.05     | -2.9547629156244426 |
| ST / Y         | NEG      | 1.94    | -3.20    | -7.137809999999998  |
| ST / N         | WEAK     | 98.06   | 2.68     | -1.3234049999999775 |
| MX / Y         | NEG      | 2.78    | -2.36    | -6.358018333333332  |
| MX / N         | WEAK     | 97.22   | 1.84     | -2.162571666666646  |
| M10 / Y        | NEG      | 2.82    | -2.32    | -6.318330833333332  |
| M10 / N        | WEAK     | 97.18   | 1.80     | -2.2022591666666536 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 18%-21%?
Contract 3344168; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       26.7  |        27.48 | +72.52 / −27.48  | 2.64×         |
| No     |       74.54 |        75.3  | +24.70 / −75.30  | 0.33×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 16.42   | -11.07   | -15.066293620365197 |
| GB / N         | GO       | 83.58   | 8.28     | 4.281493620365195   |
| ST / Y         | NEG      | 19.27   | -8.21    | -12.214090000000004 |
| ST / N         | GO       | 80.73   | 5.43     | 1.4292900000000055  |
| MX / Y         | NEG      | 15.59   | -11.90   | -15.897579583333336 |
| MX / N         | GO       | 84.41   | 9.11     | 5.112779583333338   |
| M10 / Y        | NEG      | 15.65   | -11.83   | -15.83106916666667  |
| M10 / N        | GO       | 84.35   | 9.05     | 5.046269166666672   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 3%-6%?
Contract 3344163; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         1.2 |         1.25 | +98.75 / −1.25   | 79.17×        |
| No     |        99.1 |        99.14 | +0.86 / −99.14   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 2.89    | 1.64     | -2.360927827463211  |
| GB / N         | NEG      | 97.11   | -2.02    | -6.022172172536788  |
| ST / Y         | WEAK     | 2.00    | 0.75     | -3.24742            |
| ST / N         | NEG      | 98.00   | -1.13    | -5.132554999999994  |
| MX / Y         | WEAK     | 3.39    | 2.15     | -1.8539304166666666 |
| MX / N         | NEG      | 96.61   | -2.53    | -6.529169583333328  |
| M10 / Y        | WEAK     | 3.33    | 2.08     | -1.9198679166666666 |
| M10 / N        | NEG      | 96.67   | -2.46    | -6.463232083333326  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 9%-12%?
Contract 3344165; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        7.88 |         8.17 | +91.83 / −8.17   | 11.24×        |
| No     |       95.64 |        95.8  | +4.20 / −95.80   | 0.04×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 9.90    | 1.73     | -2.267520332438118  |
| GB / N         | NEG      | 90.10   | -5.70    | -9.704029667561887  |
| ST / Y         | WEAK     | 8.57    | 0.40     | -3.5958650000000008 |
| ST / N         | NEG      | 91.43   | -4.38    | -8.375684999999999  |
| MX / Y         | WEAK     | 9.60    | 1.43     | -2.5723754166666684 |
| MX / N         | NEG      | 90.40   | -5.40    | -9.399174583333336  |
| M10 / Y        | WEAK     | 9.46    | 1.30     | -2.7048233333333336 |
| M10 / N        | NEG      | 90.54   | -5.27    | -9.266726666666669  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party control the Senate after the 2026 Midterm elections?
Contract 562793; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          63 |        63.93 | +36.07 / −63.93  | 0.56×         |
| No     |          38 |        38.94 | +61.06 / −38.94  | 1.57×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   60.17 |    -3.76 |        -7.76 |
| GB / N         | WEAK     |   39.83 |     0.88 |        -3.12 |
| ST / Y         | NEG      |   63.50 |    -0.43 |        -4.43 |
| ST / N         | NEG      |   36.50 |    -2.44 |        -6.44 |
| MX / Y         | GO       |   68.82 |     4.89 |         0.89 |
| MX / N         | NEG      |   31.18 |    -7.77 |       -11.77 |
| M10 / Y        | WEAK     |   64.95 |     1.02 |        -2.98 |
| M10 / N        | NEG      |   35.05 |    -3.89 |        -7.89 |
| RTWH / Y       | GO       |   70.50 |     6.57 |         2.57 |
| RTWH / N       | NEG      |   29.50 |    -9.44 |       -13.44 |
| DDHQ / Y       | NEG      |   54.00 |    -9.93 |       -13.93 |
| DDHQ / N       | GO       |   46.00 |     7.06 |         3.06 |

RTWH (2026-09-25): Conditional on publisher caucus accounting, complete chamber and GOP tie-break convention; independents are not reclassified as Democrats in state contracts. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Conditional on publisher caucus accounting, complete chamber and GOP tie-break convention; independents are not reclassified as Democrats in state contracts. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Alabama Senate race in 2026?
Contract 630627; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        3.86 |         4.01 | +95.99 / −4.01   | 23.95×        |
| No     |       99.57 |        99.59 | +0.41 / −99.59   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.06 |    -3.95 |        -6.01 |
| GB / N         | WEAK     |   99.94 |     0.35 |        -3.65 |
| ST / Y         | NEG      |    0.15 |    -3.86 |        -6.01 |
| ST / N         | WEAK     |   99.85 |     0.26 |        -3.74 |
| MX / Y         | NEG      |    1.54 |    -2.47 |        -6.01 |
| MX / N         | NEG      |   98.46 |    -1.12 |        -5.12 |
| M10 / Y        | NEG      |    1.46 |    -2.54 |        -6.01 |
| M10 / N        | NEG      |   98.54 |    -1.05 |        -5.05 |
| RTWH / Y       | NEG      |    1.10 |    -2.91 |        -6.01 |
| RTWH / N       | NEG      |   98.90 |    -0.69 |        -4.69 |
| DDHQ / Y       | WEAK     |    5.00 |     0.99 |        -3.01 |
| DDHQ / N       | NEG      |   95.00 |    -4.59 |        -8.59 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Arkansas Senate race in 2026?
Contract 630653; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        6.2  |         6.43 | +93.57 / −6.43   | 14.55×        |
| No     |       94.98 |        95.17 | +4.83 / −95.17   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.24 |    -6.19 |        -8.43 |
| GB / N         | GO       |   99.76 |     4.59 |         0.59 |
| ST / Y         | NEG      |    0.79 |    -5.65 |        -8.43 |
| ST / N         | GO       |   99.21 |     4.04 |         0.04 |
| MX / Y         | WEAK     |    6.64 |     0.20 |        -3.80 |
| MX / N         | NEG      |   93.36 |    -1.81 |        -5.81 |
| M10 / Y        | NEG      |    5.78 |    -0.66 |        -4.66 |
| M10 / N        | NEG      |   94.22 |    -0.95 |        -4.95 |
| RTWH / Y       | NEG      |    2.00 |    -4.43 |        -8.43 |
| RTWH / N       | WEAK     |   98.00 |     2.83 |        -1.17 |
| DDHQ / Y       | NEG      |    4.00 |    -2.43 |        -6.43 |
| DDHQ / N       | WEAK     |   96.00 |     0.83 |        -3.17 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Colorado Senate race in 2026?
Contract 630666; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       99.48 |        99.5  | +0.50 / −99.50   | 0.00×         |
| No     |        3.84 |         3.98 | +96.02 / −3.98   | 24.11×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG*     |   93.98 |    -5.52 |        -9.52 |
| GB / N         | WEAK*    |    6.02 |     2.04 |        -1.96 |
| ST / Y         | NEG*     |   94.99 |    -4.52 |        -8.52 |
| ST / N         | WEAK*    |    5.01 |     1.03 |        -2.97 |
| MX / Y         | NEG*     |   91.70 |    -7.81 |       -11.81 |
| MX / N         | GO*      |    8.30 |     4.32 |         0.32 |
| M10 / Y        | NEG*     |   90.37 |    -9.13 |       -13.13 |
| M10 / N        | GO*      |    9.63 |     5.65 |         1.65 |
| RTWH / Y       | NEG      |   98.50 |    -1.00 |        -5.00 |
| RTWH / N       | NEG      |    1.50 |    -2.48 |        -5.98 |
| DDHQ / Y       | NEG      |   97.00 |    -2.50 |        -6.50 |
| DDHQ / N       | NEG      |    3.00 |    -0.98 |        -4.98 |

GB, ST, MX, M10: Candidate roster is unreviewed; this assumes the modeled D/R sides match the party nominees.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Delaware Senate race in 2026?
Contract 630679; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       99.7  |        99.71 | +0.29 / −99.71   | 0.00×         |
| No     |        2.07 |         2.15 | +97.85 / −2.15   | 45.49×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK*    |   99.95 |     0.24 |        -3.76 |
| GB / N         | NEG*     |    0.05 |    -2.10 |        -4.15 |
| ST / Y         | NEG*     |   99.62 |    -0.09 |        -4.09 |
| ST / N         | NEG*     |    0.38 |    -1.78 |        -4.15 |
| MX / Y         | NEG*     |   99.57 |    -0.14 |        -4.14 |
| MX / N         | NEG*     |    0.43 |    -1.72 |        -4.15 |
| M10 / Y        | NEG*     |   99.46 |    -0.25 |        -4.25 |
| M10 / N        | NEG*     |    0.54 |    -1.61 |        -4.15 |
| RTWH / Y       | NEG      |   98.00 |    -1.71 |        -5.71 |
| RTWH / N       | NEG      |    2.00 |    -0.15 |        -4.15 |
| DDHQ / Y       | NEG      |   99.00 |    -0.71 |        -4.71 |
| DDHQ / N       | NEG      |    1.00 |    -1.15 |        -4.15 |

GB, ST, MX, M10: Candidate roster is unreviewed; this assumes the modeled D/R sides match the party nominees.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Florida Senate race in 2026?
Contract 631044; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           9 |         9.33 | +90.67 / −9.33   | 9.72×         |
| No     |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   18.45 |     9.13 |         5.13 |
| GB / N         | NEG      |   81.55 |   -10.75 |       -14.75 |
| ST / Y         | WEAK     |   13.03 |     3.71 |        -0.29 |
| ST / N         | NEG      |   86.97 |    -5.33 |        -9.33 |
| MX / Y         | GO       |   18.92 |     9.59 |         5.59 |
| MX / N         | NEG      |   81.08 |   -11.22 |       -15.22 |
| M10 / Y        | GO       |   16.86 |     7.53 |         3.53 |
| M10 / N        | NEG      |   83.14 |    -9.15 |       -13.15 |
| RTWH / Y       | GO       |   26.20 |    16.87 |        12.87 |
| RTWH / N       | NEG      |   73.80 |   -18.49 |       -22.49 |
| DDHQ / Y       | GO       |   22.00 |    12.67 |         8.67 |
| DDHQ / N       | NEG      |   78.00 |   -14.29 |       -18.29 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Georgia Senate race in 2026?
Contract 630692; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          95 |        95.19 | +4.81 / −95.19   | 0.05×         |
| No     |           6 |         6.23 | +93.77 / −6.23   | 15.06×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG*     |   87.32 |    -7.87 |       -11.87 |
| GB / N         | GO*      |   12.68 |     6.46 |         2.46 |
| ST / Y         | NEG*     |   91.86 |    -3.33 |        -7.33 |
| ST / N         | WEAK*    |    8.14 |     1.91 |        -2.09 |
| MX / Y         | NEG*     |   88.57 |    -6.62 |       -10.62 |
| MX / N         | GO*      |   11.43 |     5.20 |         1.20 |
| M10 / Y        | NEG*     |   87.91 |    -7.28 |       -11.28 |
| M10 / N        | GO*      |   12.09 |     5.87 |         1.87 |
| RTWH / Y       | NEG      |   94.40 |    -0.79 |        -4.79 |
| RTWH / N       | NEG      |    5.60 |    -0.63 |        -4.63 |
| DDHQ / Y       | NEG      |   87.00 |    -8.19 |       -12.19 |
| DDHQ / N       | GO       |   13.00 |     6.77 |         2.77 |

GB, ST, MX, M10: Runoff transfers and turnout are not separately modeled; the modeled margin is used as a proxy for the eventual winner.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Illinois Senate race in 2026?
Contract 630720; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       98.77 |        98.82 | +1.18 / −98.82   | 0.01×         |
| No     |        2.7  |         2.81 | +97.19 / −2.81   | 34.65×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK*    |   99.74 |     0.92 |        -3.08 |
| GB / N         | NEG*     |    0.26 |    -2.55 |        -4.81 |
| ST / Y         | WEAK*    |   99.28 |     0.47 |        -3.53 |
| ST / N         | NEG*     |    0.72 |    -2.09 |        -4.81 |
| MX / Y         | NEG*     |   98.18 |    -0.64 |        -4.64 |
| MX / N         | NEG*     |    1.82 |    -0.99 |        -4.81 |
| M10 / Y        | NEG*     |   97.97 |    -0.85 |        -4.85 |
| M10 / N        | NEG*     |    2.03 |    -0.77 |        -4.77 |
| RTWH / Y       | NEG      |   97.50 |    -1.32 |        -5.32 |
| RTWH / N       | NEG      |    2.50 |    -0.31 |        -4.31 |
| DDHQ / Y       | NEG      |   96.00 |    -2.82 |        -6.82 |
| DDHQ / N       | WEAK     |    4.00 |     1.19 |        -2.81 |

GB, ST, MX, M10: Candidate roster is unreviewed; this assumes the modeled D/R sides match the party nominees.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Iowa Senate race in 2026?
Contract 630733; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          45 |        45.99 | +54.01 / −45.99  | 1.17×         |
| No     |          57 |        57.98 | +42.02 / −57.98  | 0.72×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   36.18 |    -9.81 |       -13.81 |
| GB / N         | GO       |   63.82 |     5.84 |         1.84 |
| ST / Y         | NEG      |   33.44 |   -12.55 |       -16.55 |
| ST / N         | GO       |   66.56 |     8.58 |         4.58 |
| MX / Y         | NEG      |   36.92 |    -9.07 |       -13.07 |
| MX / N         | GO       |   63.08 |     5.10 |         1.10 |
| M10 / Y        | NEG      |   35.32 |   -10.67 |       -14.67 |
| M10 / N        | GO       |   64.68 |     6.70 |         2.70 |
| RTWH / Y       | GO       |   58.90 |    12.91 |         8.91 |
| RTWH / N       | NEG      |   41.10 |   -16.88 |       -20.88 |
| DDHQ / Y       | WEAK     |   49.00 |     3.01 |        -0.99 |
| DDHQ / N       | NEG      |   51.00 |    -6.98 |       -10.98 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Kansas Senate race in 2026?
Contract 630746; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          31 |        31.86 | +68.14 / −31.86  | 2.14×         |
| No     |          70 |        70.84 | +29.16 / −70.84  | 0.41×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    9.28 |   -22.57 |       -26.57 |
| GB / N         | GO       |   90.72 |    19.88 |        15.88 |
| ST / Y         | NEG      |    8.48 |   -23.37 |       -27.37 |
| ST / N         | GO       |   91.52 |    20.68 |        16.68 |
| MX / Y         | NEG      |   10.61 |   -21.25 |       -25.25 |
| MX / N         | GO       |   89.39 |    18.55 |        14.55 |
| M10 / Y        | NEG      |   11.87 |   -19.99 |       -23.99 |
| M10 / N        | GO       |   88.13 |    17.29 |        13.29 |
| RTWH / Y       | GO       |   36.80 |     4.94 |         0.94 |
| RTWH / N       | NEG      |   63.20 |    -7.64 |       -11.64 |
| DDHQ / Y       | NEG      |   23.00 |    -8.86 |       -12.86 |
| DDHQ / N       | GO       |   77.00 |     6.16 |         2.16 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Kentucky Senate race in 2026?
Contract 630759; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        4.22 |         4.38 | +95.62 / −4.38   | 21.82×        |
| No     |       97.17 |        97.28 | +2.72 / −97.28   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.88 |    -2.50 |        -6.38 |
| GB / N         | WEAK     |   98.12 |     0.83 |        -3.17 |
| ST / Y         | NEG      |    1.42 |    -2.96 |        -6.38 |
| ST / N         | WEAK     |   98.58 |     1.29 |        -2.71 |
| MX / Y         | NEG      |    3.90 |    -0.49 |        -4.49 |
| MX / N         | NEG      |   96.10 |    -1.18 |        -5.18 |
| M10 / Y        | NEG      |    2.96 |    -1.42 |        -5.42 |
| M10 / N        | NEG      |   97.04 |    -0.24 |        -4.24 |
| RTWH / Y       | NEG      |    2.10 |    -2.28 |        -6.28 |
| RTWH / N       | WEAK     |   97.90 |     0.62 |        -3.38 |
| DDHQ / Y       | WEAK     |    5.00 |     0.62 |        -3.38 |
| DDHQ / N       | NEG      |   95.00 |    -2.28 |        -6.28 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Louisiana Senate race in 2026?
Contract 634878; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           7 |         7.26 | +92.74 / −7.26   | 12.77×        |
| No     |          94 |        94.23 | +5.77 / −94.23   | 0.06×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    5.10 |    -2.16 |        -6.16 |
| GB / N         | WEAK     |   94.90 |     0.67 |        -3.33 |
| ST / Y         | NEG      |    4.26 |    -3.00 |        -7.00 |
| ST / N         | WEAK     |   95.74 |     1.52 |        -2.48 |
| MX / Y         | WEAK     |   10.53 |     3.27 |        -0.73 |
| MX / N         | NEG      |   89.47 |    -4.76 |        -8.76 |
| M10 / Y        | WEAK     |   10.76 |     3.50 |        -0.50 |
| M10 / N        | NEG      |   89.24 |    -4.98 |        -8.98 |
| RTWH / Y       | WEAK     |   10.80 |     3.54 |        -0.46 |
| RTWH / N       | NEG      |   89.20 |    -5.03 |        -9.03 |
| DDHQ / Y       | WEAK     |   11.00 |     3.74 |        -0.26 |
| DDHQ / N       | NEG      |   89.00 |    -5.23 |        -9.23 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Maine Senate race in 2026?
Contract 630772; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          69 |        69.86 | +30.14 / −69.86  | 0.43×         |
| No     |          32 |        32.87 | +67.13 / −32.87  | 2.04×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO*      |   92.55 |    22.70 |        18.70 |
| GB / N         | NEG*     |    7.45 |   -25.42 |       -29.42 |
| ST / Y         | GO*      |   93.63 |    23.78 |        19.78 |
| ST / N         | NEG*     |    6.37 |   -26.50 |       -30.50 |
| MX / Y         | GO*      |   85.54 |    15.69 |        11.69 |
| MX / N         | NEG*     |   14.46 |   -18.41 |       -22.41 |
| M10 / Y        | GO*      |   82.94 |    13.09 |         9.09 |
| M10 / N        | NEG*     |   17.06 |   -15.81 |       -19.81 |
| RTWH / Y       | NEG      |   62.20 |    -7.66 |       -11.66 |
| RTWH / N       | GO       |   37.80 |     4.93 |         0.93 |
| DDHQ / Y       | NEG      |   54.00 |   -15.86 |       -19.86 |
| DDHQ / N       | GO       |   46.00 |    13.13 |         9.13 |

GB, ST, MX, M10: Ranked-choice transfers are not separately modeled; the modeled margin is used as a proxy for the eventual winner.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Massachusetts Senate race in 2026?
Contract 630790; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        98.3 |        98.37 | +1.63 / −98.37   | 0.02×         |
| No     |         2.5 |         2.6  | +97.40 / −2.60   | 37.50×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |  100.00 |     1.63 |        -2.37 |
| GB / N         | NEG      |    0.00 |    -2.60 |        -4.60 |
| ST / Y         | WEAK     |  100.00 |     1.63 |        -2.37 |
| ST / N         | NEG      |    0.00 |    -2.59 |        -4.60 |
| MX / Y         | WEAK     |   99.99 |     1.62 |        -2.38 |
| MX / N         | NEG      |    0.01 |    -2.59 |        -4.60 |
| M10 / Y        | WEAK     |   99.99 |     1.62 |        -2.38 |
| M10 / N        | NEG      |    0.01 |    -2.59 |        -4.60 |
| RTWH / Y       | WEAK     |   99.60 |     1.23 |        -2.77 |
| RTWH / N       | NEG      |    0.40 |    -2.20 |        -4.60 |
| DDHQ / Y       | WEAK     |   99.00 |     0.63 |        -3.37 |
| DDHQ / N       | NEG      |    1.00 |    -1.60 |        -4.60 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Michigan Senate race in 2026?
Contract 630805; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          72 |        72.81 | +27.19 / −72.81  | 0.37×         |
| No     |          29 |        29.82 | +70.18 / −29.82  | 2.35×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   83.45 |    10.64 |         6.64 |
| GB / N         | NEG      |   16.55 |   -13.27 |       -17.27 |
| ST / Y         | GO       |   88.17 |    15.36 |        11.36 |
| ST / N         | NEG      |   11.83 |   -17.99 |       -21.99 |
| MX / Y         | GO       |   83.17 |    10.36 |         6.36 |
| MX / N         | NEG      |   16.83 |   -12.99 |       -16.99 |
| M10 / Y        | GO       |   79.07 |     6.27 |         2.27 |
| M10 / N        | NEG      |   20.93 |    -8.90 |       -12.90 |
| RTWH / Y       | GO       |   82.10 |     9.29 |         5.29 |
| RTWH / N       | NEG      |   17.90 |   -11.92 |       -15.92 |
| DDHQ / Y       | NEG      |   70.00 |    -2.81 |        -6.81 |
| DDHQ / N       | WEAK     |   30.00 |     0.18 |        -3.82 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Minnesota Senate race in 2026?
Contract 630818; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |
| No     |           9 |         9.33 | +90.67 / −9.33   | 9.72×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   84.80 |    -7.49 |       -11.49 |
| GB / N         | GO       |   15.20 |     5.87 |         1.87 |
| ST / Y         | NEG      |   86.87 |    -5.43 |        -9.43 |
| ST / N         | WEAK     |   13.13 |     3.80 |        -0.20 |
| MX / Y         | NEG      |   87.32 |    -4.97 |        -8.97 |
| MX / N         | WEAK     |   12.68 |     3.35 |        -0.65 |
| M10 / Y        | NEG      |   86.03 |    -6.26 |       -10.26 |
| M10 / N        | GO       |   13.97 |     4.64 |         0.64 |
| RTWH / Y       | NEG      |   84.80 |    -7.49 |       -11.49 |
| RTWH / N       | GO       |   15.20 |     5.87 |         1.87 |
| DDHQ / Y       | NEG      |   87.00 |    -5.29 |        -9.29 |
| DDHQ / N       | WEAK     |   13.00 |     3.67 |        -0.33 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Mississippi Senate race in 2026?
Contract 631017; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           9 |         9.33 | +90.67 / −9.33   | 9.72×         |
| No     |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    3.21 |    -6.12 |       -10.12 |
| GB / N         | GO       |   96.79 |     4.49 |         0.49 |
| ST / Y         | NEG      |    2.51 |    -6.82 |       -10.82 |
| ST / N         | GO       |   97.49 |     5.19 |         1.19 |
| MX / Y         | NEG      |    6.30 |    -3.03 |        -7.03 |
| MX / N         | WEAK     |   93.70 |     1.40 |        -2.60 |
| M10 / Y        | NEG      |    7.53 |    -1.80 |        -5.80 |
| M10 / N        | WEAK     |   92.47 |     0.18 |        -3.82 |
| RTWH / Y       | WEAK     |   13.10 |     3.77 |        -0.23 |
| RTWH / N       | NEG      |   86.90 |    -5.39 |        -9.39 |
| DDHQ / Y       | NEG      |    7.00 |    -2.33 |        -6.33 |
| DDHQ / N       | WEAK     |   93.00 |     0.71 |        -3.29 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the New Hampshire Senate race in 2026?
Contract 630844; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          86 |        86.48 | +13.52 / −86.48  | 0.16×         |
| No     |          15 |        15.51 | +84.49 / −15.51  | 5.45×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   97.93 |    11.45 |         7.45 |
| GB / N         | NEG      |    2.07 |   -13.44 |       -17.44 |
| ST / Y         | GO       |   97.58 |    11.10 |         7.10 |
| ST / N         | NEG      |    2.42 |   -13.09 |       -17.09 |
| MX / Y         | GO       |   92.77 |     6.29 |         2.29 |
| MX / N         | NEG      |    7.23 |    -8.28 |       -12.28 |
| M10 / Y        | GO       |   93.88 |     7.40 |         3.40 |
| M10 / N        | NEG      |    6.12 |    -9.39 |       -13.39 |
| RTWH / Y       | NEG      |   86.20 |    -0.28 |        -4.28 |
| RTWH / N       | NEG      |   13.80 |    -1.71 |        -5.71 |
| DDHQ / Y       | NEG      |   81.00 |    -5.48 |        -9.48 |
| DDHQ / N       | WEAK     |   19.00 |     3.49 |        -0.51 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the New Jersey Senate race in 2026?
Contract 630857; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       97.83 |        97.91 | +2.09 / −97.91   | 0.02×         |
| No     |        4.43 |         4.6  | +95.40 / −4.60   | 20.76×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK*    |   99.78 |     1.87 |        -2.13 |
| GB / N         | NEG*     |    0.22 |    -4.37 |        -6.60 |
| ST / Y         | WEAK*    |   99.24 |     1.33 |        -2.67 |
| ST / N         | NEG*     |    0.76 |    -3.84 |        -6.60 |
| MX / Y         | WEAK*    |   99.65 |     1.74 |        -2.26 |
| MX / N         | NEG*     |    0.35 |    -4.25 |        -6.60 |
| M10 / Y        | WEAK*    |   99.56 |     1.65 |        -2.35 |
| M10 / N        | NEG*     |    0.44 |    -4.16 |        -6.60 |
| RTWH / Y       | NEG      |   97.10 |    -0.81 |        -4.81 |
| RTWH / N       | NEG      |    2.90 |    -1.70 |        -5.70 |
| DDHQ / Y       | NEG      |   96.00 |    -1.91 |        -5.91 |
| DDHQ / N       | NEG      |    4.00 |    -0.60 |        -4.60 |

GB, ST, MX, M10: Candidate roster is unreviewed; this assumes the modeled D/R sides match the party nominees.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the New Mexico Senate race in 2026?
Contract 630870; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       97.96 |        98.04 | +1.96 / −98.04   | 0.02×         |
| No     |        3.3  |         3.43 | +96.57 / −3.43   | 28.17×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   98.10 |     0.06 |        -3.94 |
| GB / N         | NEG      |    1.90 |    -1.53 |        -5.43 |
| ST / Y         | WEAK     |   99.07 |     1.03 |        -2.97 |
| ST / N         | NEG      |    0.93 |    -2.49 |        -5.43 |
| MX / Y         | WEAK     |   98.19 |     0.15 |        -3.85 |
| MX / N         | NEG      |    1.81 |    -1.62 |        -5.43 |
| M10 / Y        | WEAK     |   98.15 |     0.12 |        -3.88 |
| M10 / N        | NEG      |    1.85 |    -1.58 |        -5.43 |
| RTWH / Y       | WEAK     |   99.30 |     1.26 |        -2.74 |
| RTWH / N       | NEG      |    0.70 |    -2.73 |        -5.43 |
| DDHQ / Y       | NEG      |   96.00 |    -2.04 |        -6.04 |
| DDHQ / N       | WEAK     |    4.00 |     0.57 |        -3.43 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the North Carolina Senate race in 2026?
Contract 630883; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          95 |        95.19 | +4.81 / −95.19   | 0.05×         |
| No     |           6 |         6.23 | +93.77 / −6.23   | 15.06×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   85.77 |    -9.42 |       -13.42 |
| GB / N         | GO       |   14.23 |     8.00 |         4.00 |
| ST / Y         | NEG      |   90.64 |    -4.55 |        -8.55 |
| ST / N         | WEAK     |    9.36 |     3.13 |        -0.87 |
| MX / Y         | NEG      |   88.11 |    -7.08 |       -11.08 |
| MX / N         | GO       |   11.89 |     5.66 |         1.66 |
| M10 / Y        | NEG      |   88.03 |    -7.16 |       -11.16 |
| M10 / N        | GO       |   11.97 |     5.74 |         1.74 |
| RTWH / Y       | NEG      |   89.80 |    -5.39 |        -9.39 |
| RTWH / N       | WEAK     |   10.20 |     3.97 |        -0.03 |
| DDHQ / Y       | NEG      |   81.00 |   -14.19 |       -18.19 |
| DDHQ / N       | GO       |   19.00 |    12.77 |         8.77 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Ohio Senate race in 2026?
Contract 631057; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          58 |        58.97 | +41.03 / −58.97  | 0.70×         |
| No     |          43 |        43.98 | +56.02 / −43.98  | 1.27×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   70.34 |    11.37 |         7.37 |
| GB / N         | NEG      |   29.66 |   -14.32 |       -18.32 |
| ST / Y         | GO       |   75.06 |    16.08 |        12.08 |
| ST / N         | NEG      |   24.94 |   -19.04 |       -23.04 |
| MX / Y         | GO       |   69.18 |    10.21 |         6.21 |
| MX / N         | NEG      |   30.82 |   -13.16 |       -17.16 |
| M10 / Y        | GO       |   65.03 |     6.05 |         2.05 |
| M10 / N        | NEG      |   34.97 |    -9.01 |       -13.01 |
| RTWH / Y       | GO       |   74.40 |    15.43 |        11.43 |
| RTWH / N       | NEG      |   25.60 |   -18.38 |       -22.38 |
| DDHQ / Y       | NEG      |   51.00 |    -7.97 |       -11.97 |
| DDHQ / N       | GO       |   49.00 |     5.02 |         1.02 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Oklahoma Senate race in 2026?
Contract 631030; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         2.4 |         2.49 | +97.51 / −2.49   | 39.10×        |
| No     |        98   |        98.08 | +1.92 / −98.08   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.01 |    -2.49 |        -4.49 |
| GB / N         | WEAK     |   99.99 |     1.92 |        -2.08 |
| ST / Y         | NEG      |    0.01 |    -2.48 |        -4.49 |
| ST / N         | WEAK     |   99.99 |     1.91 |        -2.09 |
| MX / Y         | NEG      |    0.06 |    -2.43 |        -4.49 |
| MX / N         | WEAK     |   99.94 |     1.86 |        -2.14 |
| M10 / Y        | NEG      |    0.04 |    -2.45 |        -4.49 |
| M10 / N        | WEAK     |   99.96 |     1.88 |        -2.12 |
| RTWH / Y       | NEG      |    0.80 |    -1.69 |        -4.49 |
| RTWH / N       | WEAK     |   99.20 |     1.12 |        -2.88 |
| DDHQ / Y       | NEG      |    1.00 |    -1.49 |        -4.49 |
| DDHQ / N       | WEAK     |   99.00 |     0.92 |        -3.08 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Oregon Senate race in 2026?
Contract 630898; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        98.3 |        98.37 | +1.63 / −98.37   | 0.02×         |
| No     |         3.2 |         3.32 | +96.68 / −3.32   | 29.09×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK*    |   99.93 |     1.56 |        -2.44 |
| GB / N         | NEG*     |    0.07 |    -3.25 |        -5.32 |
| ST / Y         | WEAK*    |   99.65 |     1.28 |        -2.72 |
| ST / N         | NEG*     |    0.35 |    -2.97 |        -5.32 |
| MX / Y         | WEAK*    |   99.33 |     0.97 |        -3.03 |
| MX / N         | NEG*     |    0.67 |    -2.66 |        -5.32 |
| M10 / Y        | WEAK*    |   99.08 |     0.71 |        -3.29 |
| M10 / N        | NEG*     |    0.92 |    -2.40 |        -5.32 |
| RTWH / Y       | NEG      |   97.90 |    -0.47 |        -4.47 |
| RTWH / N       | NEG      |    2.10 |    -1.22 |        -5.22 |
| DDHQ / Y       | WEAK     |   99.00 |     0.63 |        -3.37 |
| DDHQ / N       | NEG      |    1.00 |    -2.32 |        -5.32 |

GB, ST, MX, M10: Candidate roster is unreviewed; this assumes the modeled D/R sides match the party nominees.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Rhode Island Senate race in 2026?
Contract 630911; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       99.5  |        99.52 | +0.48 / −99.52   | 0.00×         |
| No     |        3.77 |         3.91 | +96.09 / −3.91   | 24.57×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.99 |     0.47 |        -3.53 |
| GB / N         | NEG      |    0.01 |    -3.91 |        -5.91 |
| ST / Y         | WEAK     |   99.99 |     0.47 |        -3.53 |
| ST / N         | NEG      |    0.01 |    -3.90 |        -5.91 |
| MX / Y         | WEAK     |   99.85 |     0.33 |        -3.67 |
| MX / N         | NEG      |    0.15 |    -3.76 |        -5.91 |
| M10 / Y        | WEAK     |   99.82 |     0.30 |        -3.70 |
| M10 / N        | NEG      |    0.18 |    -3.73 |        -5.91 |
| RTWH / Y       | NEG      |   98.90 |    -0.62 |        -4.62 |
| RTWH / N       | NEG      |    1.10 |    -2.81 |        -5.91 |
| DDHQ / Y       | NEG      |   99.00 |    -0.52 |        -4.52 |
| DDHQ / N       | NEG      |    1.00 |    -2.91 |        -5.91 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the South Carolina Senate race in 2026?
Contract 630924; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          14 |        14.48 | +85.52 / −14.48  | 5.91×         |
| No     |          87 |        87.45 | +12.55 / −87.45  | 0.14×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    4.70 |    -9.78 |       -13.78 |
| GB / N         | GO       |   95.30 |     7.85 |         3.85 |
| ST / Y         | NEG      |    3.78 |   -10.70 |       -14.70 |
| ST / N         | GO       |   96.22 |     8.77 |         4.77 |
| MX / Y         | NEG      |    8.21 |    -6.27 |       -10.27 |
| MX / N         | GO       |   91.79 |     4.33 |         0.33 |
| M10 / Y        | NEG      |    7.31 |    -7.17 |       -11.17 |
| M10 / N        | GO       |   92.69 |     5.24 |         1.24 |
| RTWH / Y       | GO       |   20.30 |     5.82 |         1.82 |
| RTWH / N       | NEG      |   79.70 |    -7.75 |       -11.75 |
| DDHQ / Y       | GO       |   27.00 |    12.52 |         8.52 |
| DDHQ / N       | NEG      |   73.00 |   -14.45 |       -18.45 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Tennessee Senate race in 2026?
Contract 630950; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         3.3 |         3.43 | +96.57 / −3.43   | 28.17×        |
| No     |        97.3 |        97.41 | +2.59 / −97.41   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.03 |    -3.40 |        -5.43 |
| GB / N         | WEAK     |   99.97 |     2.57 |        -1.43 |
| ST / Y         | NEG      |    0.02 |    -3.41 |        -5.43 |
| ST / N         | WEAK     |   99.98 |     2.57 |        -1.43 |
| MX / Y         | NEG      |    0.08 |    -3.35 |        -5.43 |
| MX / N         | WEAK     |   99.92 |     2.52 |        -1.48 |
| M10 / Y        | NEG      |    0.05 |    -3.38 |        -5.43 |
| M10 / N        | WEAK     |   99.95 |     2.55 |        -1.45 |
| RTWH / Y       | NEG      |    1.00 |    -2.43 |        -5.43 |
| RTWH / N       | WEAK     |   99.00 |     1.59 |        -2.41 |
| DDHQ / Y       | NEG      |    3.00 |    -0.43 |        -4.43 |
| DDHQ / N       | NEG      |   97.00 |    -0.41 |        -4.41 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Texas Senate race in 2026?
Contract 630963; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          62 |        62.94 | +37.06 / −62.94  | 0.59×         |
| No     |          39 |        39.95 | +60.05 / −39.95  | 1.50×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   56.72 |    -6.22 |       -10.22 |
| GB / N         | WEAK     |   43.28 |     3.33 |        -0.67 |
| ST / Y         | NEG      |   57.89 |    -5.05 |        -9.05 |
| ST / N         | WEAK     |   42.11 |     2.16 |        -1.84 |
| MX / Y         | NEG      |   54.91 |    -8.03 |       -12.03 |
| MX / N         | GO       |   45.09 |     5.14 |         1.14 |
| M10 / Y        | NEG      |   55.29 |    -7.65 |       -11.65 |
| M10 / N        | GO       |   44.71 |     4.76 |         0.76 |
| RTWH / Y       | GO       |   77.50 |    14.56 |        10.56 |
| RTWH / N       | NEG      |   22.50 |   -17.45 |       -21.45 |
| DDHQ / Y       | NEG      |   56.00 |    -6.94 |       -10.94 |
| DDHQ / N       | GO       |   44.00 |     4.05 |         0.05 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Virginia Senate race in 2026?
Contract 630976; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       99.61 |        99.63 | +0.37 / −99.63   | 0.00×         |
| No     |        2.87 |         2.98 | +97.02 / −2.98   | 32.54×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   99.43 |    -0.20 |        -4.20 |
| GB / N         | NEG      |    0.57 |    -2.42 |        -4.98 |
| ST / Y         | NEG      |   99.41 |    -0.22 |        -4.22 |
| ST / N         | NEG      |    0.59 |    -2.39 |        -4.98 |
| MX / Y         | NEG      |   98.48 |    -1.15 |        -5.15 |
| MX / N         | NEG      |    1.52 |    -1.46 |        -4.98 |
| M10 / Y        | NEG      |   98.52 |    -1.11 |        -5.11 |
| M10 / N        | NEG      |    1.48 |    -1.50 |        -4.98 |
| RTWH / Y       | NEG      |   98.10 |    -1.53 |        -5.53 |
| RTWH / N       | NEG      |    1.90 |    -1.08 |        -4.98 |
| DDHQ / Y       | NEG      |   96.00 |    -3.63 |        -7.63 |
| DDHQ / N       | WEAK     |    4.00 |     1.02 |        -2.98 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Wyoming Senate race in 2026?
Contract 631002; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         2.8 |         2.91 | +97.09 / −2.91   | 33.38×        |
| No     |        97.8 |        97.89 | +2.11 / −97.89   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG*     |    0.00 |    -2.91 |        -4.91 |
| GB / N         | WEAK*    |  100.00 |     2.11 |        -1.89 |
| ST / Y         | NEG*     |    0.03 |    -2.88 |        -4.91 |
| ST / N         | WEAK*    |   99.97 |     2.09 |        -1.91 |
| MX / Y         | NEG*     |    0.06 |    -2.84 |        -4.91 |
| MX / N         | WEAK*    |   99.94 |     2.05 |        -1.95 |
| M10 / Y        | NEG*     |    0.07 |    -2.84 |        -4.91 |
| M10 / N        | WEAK*    |   99.93 |     2.05 |        -1.95 |
| RTWH / Y       | NEG      |    1.20 |    -1.71 |        -4.91 |
| RTWH / N       | WEAK     |   98.80 |     0.91 |        -3.09 |
| DDHQ / Y       | NEG      |    1.00 |    -1.91 |        -4.91 |
| DDHQ / N       | WEAK     |   99.00 |     1.11 |        -2.89 |

GB, ST, MX, M10: Candidate roster is unreviewed; this assumes the modeled D/R sides match the party nominees.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party candidate win the 2026 Alabama Senate election by 10%-15%?
Contract 3343105; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          14 |        14.48 | +85.52 / −14.48  | 5.91×         |
| No     |          88 |        88.42 | +11.58 / −88.42  | 0.13×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 12.70   | -1.78    | -5.777347683235572  |
| GB / N         | NEG      | 87.30   | -1.13    | -5.126652316764434  |
| ST / Y         | NEG      | 10.22   | -4.26    | -8.256600000000002  |
| ST / N         | WEAK     | 89.78   | 1.35     | -2.6473999999999993 |
| MX / Y         | NEG      | 14.48   | -0.01    | -4.006183333333337  |
| MX / N         | NEG      | 85.52   | -2.90    | -6.897816666666667  |
| M10 / Y        | NEG      | 14.11   | -0.37    | -4.370402083333334  |
| M10 / N        | NEG      | 85.89   | -2.53    | -6.5335979166666664 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Alabama Senate election by 20%-25%?
Contract 3343103; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        20.8 |        21.46 | +78.54 / −21.46  | 3.66×         |
| No     |        80   |        80.64 | +19.36 / −80.64  | 0.24×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 29.12   | 7.66     | 3.6561527524217534  |
| GB / N         | NEG      | 70.88   | -9.76    | -13.75509275242176  |
| ST / Y         | GO       | 34.48   | 13.02    | 9.016059999999998   |
| ST / N         | NEG      | 65.53   | -15.12   | -19.115000000000006 |
| MX / Y         | GO       | 25.53   | 4.07     | 0.0732475000000038  |
| MX / N         | NEG      | 74.47   | -6.17    | -10.172187500000007 |
| M10 / Y        | GO       | 25.73   | 4.28     | 0.27569541666666864 |
| M10 / N        | NEG      | 74.27   | -6.37    | -10.37463541666668  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Alabama Senate election by 35% or more?
Contract 3343100; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       21.42 |        22.07 | +77.93 / −22.07  | 3.53×         |
| No     |       98.92 |        98.96 | +1.04 / −98.96   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.84    | -20.23   | -24.073619999999995 |
| GB / N         | NEG      | 98.16   | -0.80    | -4.801002412164235  |
| ST / Y         | NEG      | 1.01    | -21.06   | -24.073619999999995 |
| ST / N         | WEAK     | 98.99   | 0.03     | -3.973020000000005  |
| MX / Y         | NEG      | 2.52    | -19.55   | -23.554661666666664 |
| MX / N         | NEG      | 97.48   | -1.48    | -5.479478333333332  |
| M10 / Y        | NEG      | 2.67    | -19.41   | -23.405026250000002 |
| M10 / N        | NEG      | 97.33   | -1.63    | -5.629113750000004  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Alabama Senate election by 5%-10%?
Contract 3343106; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       15    |        15.51 | +84.49 / −15.51  | 5.45×         |
| No     |       89.74 |        90.11 | +9.89 / −90.11   | 0.11×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 3.67    | -11.84   | -15.840217679996963 |
| GB / N         | GO       | 96.33   | 6.22     | 2.219977679996954   |
| ST / Y         | NEG      | 2.84    | -12.67   | -16.6725            |
| ST / N         | GO       | 97.16   | 7.05     | 3.0522599999999844  |
| MX / Y         | NEG      | 7.20    | -8.31    | -12.306614583333333 |
| MX / N         | WEAK     | 92.80   | 2.69     | -1.3136254166666752 |
| M10 / Y        | NEG      | 6.97    | -8.54    | -12.543125          |
| M10 / N        | WEAK     | 93.03   | 2.92     | -1.0771150000000063 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Arkansas Senate election by 10%-15%?
Contract 3343124; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        26.5 |        27.28 | +72.72 / −27.28  | 2.67×         |
| No     |        73.7 |        74.48 | +25.52 / −74.48  | 0.34×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 16.18   | -11.10   | -15.102838994980475 |
| GB / N         | GO       | 83.82   | 9.35     | 5.348418994980475   |
| ST / Y         | NEG      | 16.19   | -11.09   | -15.08535           |
| ST / N         | GO       | 83.81   | 9.33     | 5.33092999999999    |
| MX / Y         | NEG      | 17.99   | -9.29    | -13.292172916666665 |
| MX / N         | GO       | 82.01   | 7.54     | 3.5377529166666593  |
| M10 / Y        | NEG      | 17.22   | -10.06   | -14.060975000000001 |
| M10 / N        | GO       | 82.78   | 8.31     | 4.306555000000001   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Arkansas Senate election by 20%-25%?
Contract 3343122; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       11    |        11.39 | +88.61 / −11.39  | 7.78×         |
| No     |       91.14 |        91.46 | +8.54 / −91.46   | 0.09×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 25.96   | 14.57    | 10.565290760275026  |
| GB / N         | NEG      | 74.04   | -17.42   | -21.41985076027503  |
| ST / Y         | GO       | 28.23   | 16.83    | 12.833399999999997  |
| ST / N         | NEG      | 71.78   | -19.69   | -23.687959999999997 |
| MX / Y         | GO       | 18.79   | 7.40     | 3.397722916666668   |
| MX / N         | NEG      | 81.21   | -10.25   | -14.252282916666658 |
| M10 / Y        | GO       | 19.87   | 8.48     | 4.4772541666666665  |
| M10 / N        | NEG      | 80.13   | -11.33   | -15.331814166666657 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Arkansas Senate election by 25%-30%?
Contract 3343121; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        7    |         7.26 | +92.74 / −7.26   | 12.77×        |
| No     |       95.75 |        95.91 | +4.09 / −95.91   | 0.04×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 16.05   | 8.79     | 4.787059341832207   |
| GB / N         | NEG      | 83.95   | -11.96   | -15.960159341832213 |
| ST / Y         | GO       | 13.43   | 6.16     | 2.1646              |
| ST / N         | NEG      | 86.58   | -9.34    | -13.337700000000009 |
| MX / Y         | WEAK     | 10.14   | 2.87     | -1.1252437500000003 |
| MX / N         | NEG      | 89.86   | -6.05    | -10.04785625000001  |
| M10 / Y        | GO       | 11.52   | 4.26     | 0.25975624999999836 |
| M10 / N        | NEG      | 88.48   | -7.43    | -11.432856250000011 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Arkansas Senate election by 35%-40%?
Contract 3343119; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.06 |         9.39 | +90.61 / −9.39   | 9.64×         |
| No     |       96.6  |        96.73 | +3.27 / −96.73   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.46    | -7.94    | -11.394219999999997 |
| GB / N         | WEAK     | 98.54   | 1.81     | -2.188860558732031  |
| ST / Y         | NEG      | 0.56    | -8.84    | -11.394219999999997 |
| ST / N         | WEAK     | 99.44   | 2.71     | -1.2875300000000032 |
| MX / Y         | NEG      | 1.04    | -8.36    | -11.394219999999997 |
| MX / N         | WEAK     | 98.96   | 2.23     | -1.768363333333334  |
| M10 / Y        | NEG      | 1.25    | -8.15    | -11.394219999999997 |
| M10 / N        | WEAK     | 98.75   | 2.02     | -1.9770091666666656 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Arkansas Senate election by 5%-10%?
Contract 3343125; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          13 |        13.45 | +86.55 / −13.45  | 6.43×         |
| No     |          88 |        88.42 | +11.58 / −88.42  | 0.13×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 6.23    | -7.22    | -11.222897075936146 |
| GB / N         | GO       | 93.77   | 5.35     | 1.348097075936139   |
| ST / Y         | NEG      | 6.44    | -7.01    | -11.00865           |
| ST / N         | GO       | 93.56   | 5.13     | 1.1338499999999918  |
| MX / Y         | NEG      | 12.47   | -0.98    | -4.982608333333334  |
| MX / N         | NEG      | 87.53   | -0.89    | -4.892191666666667  |
| M10 / Y        | NEG      | 11.49   | -1.97    | -5.966149999999999  |
| M10 / N        | WEAK     | 88.51   | 0.09     | -3.9086500000000024 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Florida Senate election by 0%-3%?
Contract 3343184; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        21   |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |        81.4 |        82.01 | +17.99 / −82.01  | 0.22×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 14.55   | -7.12    | -11.116565629165231 |
| GB / N         | WEAK     | 85.45   | 3.45     | -0.5546543708347618 |
| ST / Y         | NEG      | 15.98   | -5.68    | -9.679224999999997  |
| ST / N         | WEAK     | 84.02   | 2.01     | -1.991995000000002  |
| MX / Y         | NEG      | 14.41   | -7.25    | -11.253287499999999 |
| MX / N         | WEAK     | 85.59   | 3.58     | -0.4179324999999956 |
| M10 / Y        | NEG      | 13.61   | -8.05    | -12.051204166666665 |
| M10 / N        | GO       | 86.39   | 4.38     | 0.3799841666666693  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Florida Senate election by 12%-15%?
Contract 3343180; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        8.62 |         8.94 | +91.06 / −8.94   | 10.19×        |
| No     |       95.2  |        95.38 | +4.62 / −95.38   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 9.31    | 0.38     | -3.6224398614882136 |
| GB / N         | NEG      | 90.69   | -4.69    | -8.691340138511805  |
| ST / Y         | NEG      | 7.39    | -1.54    | -5.544464999999999  |
| ST / N         | NEG      | 92.61   | -2.77    | -6.769315000000019  |
| MX / Y         | NEG      | 8.79    | -0.15    | -4.146860833333332  |
| MX / N         | NEG      | 91.21   | -4.17    | -8.166919166666675  |
| M10 / Y        | WEAK     | 9.60    | 0.66     | -3.336965           |
| M10 / N        | NEG      | 90.40   | -4.98    | -8.976815000000016  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Florida Senate election by 15%-18%?
Contract 3343179; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.94 |         3.05 | +96.95 / −3.05   | 31.79×        |
| No     |       98.45 |        98.51 | +1.49 / −98.51   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 4.97    | 1.92     | -2.0774653067829214 |
| GB / N         | NEG      | 95.03   | -3.48    | -7.483824693217079  |
| ST / Y         | NEG      | 2.97    | -0.08    | -4.077415           |
| ST / N         | NEG      | 97.03   | -1.48    | -5.483875000000005  |
| MX / Y         | WEAK     | 4.68    | 1.63     | -2.365331666666666  |
| MX / N         | NEG      | 95.32   | -3.20    | -7.195958333333341  |
| M10 / Y        | WEAK     | 5.31    | 2.26     | -1.7381441666666673 |
| M10 / N        | NEG      | 94.69   | -3.82    | -7.823145833333333  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Iowa Senate election by 0%-3%?
Contract 3343530; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          27 |        27.79 | +72.21 / −27.79  | 2.60×         |
| No     |          75 |        75.75 | +24.25 / −75.75  | 0.32×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 19.82   | -7.96    | -11.96384078555484  |
| GB / N         | GO       | 80.18   | 4.43     | 0.42544078555483145 |
| ST / Y         | NEG      | 24.07   | -3.72    | -7.722775000000004  |
| ST / N         | WEAK     | 75.93   | 0.18     | -3.815625           |
| MX / Y         | NEG      | 20.92   | -6.87    | -10.872618750000004 |
| MX / N         | WEAK     | 79.08   | 3.33     | -0.6657812499999971 |
| M10 / Y        | NEG      | 20.77   | -7.02    | -11.021681250000004 |
| M10 / N        | WEAK     | 79.23   | 3.48     | -0.5167187500000003 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Iowa Senate election by 12% or more?
Contract 3343526; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        3.83 |         3.98 | +96.02 / −3.98   | 24.15×        |
| No     |       99.2  |        99.23 | +0.77 / −99.23   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 4.79    | 0.82     | -3.1833204211686104 |
| GB / N         | NEG      | 95.21   | -4.03    | -8.025009578831387  |
| ST / Y         | NEG      | 2.37    | -1.61    | -5.6078399999999995 |
| ST / N         | NEG      | 97.63   | -1.60    | -5.600489999999992  |
| MX / Y         | NEG      | 3.96    | -0.02    | -4.01612125         |
| MX / N         | NEG      | 96.04   | -3.19    | -7.192208749999995  |
| M10 / Y        | WEAK     | 4.31    | 0.33     | -3.6674233333333333 |
| M10 / N        | NEG      | 95.69   | -3.54    | -7.540906666666658  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Iowa Senate election by 3%-6%?
Contract 3343529; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          80 |        80.64 | +19.36 / −80.64  | 0.24×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 18.40   | -3.26    | -7.2645161272817    |
| GB / N         | WEAK     | 81.60   | 0.96     | -3.0390838727182956 |
| ST / Y         | NEG      | 21.49   | -0.17    | -4.172974999999998  |
| ST / N         | NEG      | 78.51   | -2.13    | -6.130625           |
| MX / Y         | NEG      | 19.11   | -2.56    | -6.557818749999999  |
| MX / N         | WEAK     | 80.89   | 0.25     | -3.745781250000002  |
| M10 / Y        | NEG      | 19.57   | -2.09    | -6.09177708333333   |
| M10 / N        | NEG      | 80.43   | -0.21    | -4.211822916666675  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Iowa Senate election by 6%-9%?
Contract 3343528; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       12.04 |        12.46 | +87.54 / −12.46  | 7.03×         |
| No     |       90    |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 13.31   | 0.85     | -3.153619761911512  |
| GB / N         | NEG      | 86.69   | -3.67    | -7.6666902380884805 |
| ST / Y         | WEAK     | 13.24   | 0.78     | -3.2165599999999976 |
| ST / N         | NEG      | 86.76   | -3.60    | -7.603749999999998  |
| MX / Y         | WEAK     | 12.81   | 0.35     | -3.6548412499999974 |
| MX / N         | NEG      | 87.19   | -3.17    | -7.165468750000005  |
| M10 / Y        | WEAK     | 13.32   | 0.86     | -3.1356225          |
| M10 / N        | NEG      | 86.68   | -3.68    | -7.684687499999998  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Iowa Senate election by 9%-12%?
Contract 3343527; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         3.8 |         3.95 | +96.05 / −3.95   | 24.34×        |
| No     |        97.7 |        97.79 | +2.21 / −97.79   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)           |
|:---------------|:---------|:--------|:---------|:---------------------|
| GB / Y         | WEAK     | 7.50    | 3.55     | -0.44717448117687764 |
| GB / N         | NEG      | 92.50   | -5.29    | -9.28892551882312    |
| ST / Y         | WEAK     | 5.39    | 1.45     | -2.5524699999999996  |
| ST / N         | NEG      | 94.61   | -3.18    | -7.183629999999996   |
| MX / Y         | WEAK     | 6.29    | 2.34     | -1.6571054166666668  |
| MX / N         | NEG      | 93.71   | -4.08    | -8.078994583333332   |
| M10 / Y        | WEAK     | 6.71    | 2.76     | -1.2356470833333328  |
| M10 / N        | NEG      | 93.29   | -4.50    | -8.500452916666667   |
| RTWH / Y       | N/A      | —       | —        | —                    |
| RTWH / N       | N/A      | —       | —        | —                    |
| DDHQ / Y       | N/A      | —       | —        | —                    |
| DDHQ / N       | N/A      | —       | —        | —                    |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Kansas Senate election by 10%-15%?
Contract 3343544; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10    |        10.36 | +89.64 / −10.36  | 8.65×         |
| No     |       92.19 |        92.48 | +7.52 / −92.48   | 0.08×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 22.83   | 12.47    | 8.4723771908735     |
| GB / N         | NEG      | 77.17   | -15.31   | -19.312637190873506 |
| ST / Y         | GO       | 22.34   | 11.98    | 7.983750000000002   |
| ST / N         | NEG      | 77.66   | -14.82   | -18.82401           |
| MX / Y         | GO       | 21.50   | 11.14    | 7.143958333333335   |
| MX / N         | NEG      | 78.50   | -13.98   | -17.984218333333345 |
| M10 / Y        | GO       | 20.08   | 9.72     | 5.71578125          |
| M10 / N        | NEG      | 79.92   | -12.56   | -16.556041250000007 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Kansas Senate election by 15%-20%?
Contract 3343543; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           6 |         6.23 | +93.77 / −6.23   | 15.06×        |
| No     |          97 |        97.12 | +2.88 / −97.12   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 6.74    | 0.52     | -3.484523788900436  |
| GB / N         | NEG      | 93.26   | -3.86    | -7.857476211099569  |
| ST / Y         | NEG      | 4.42    | -1.81    | -5.80685            |
| ST / N         | NEG      | 95.58   | -1.54    | -5.5351500000000105 |
| MX / Y         | NEG      | 5.86    | -0.36    | -4.363099999999999  |
| MX / N         | NEG      | 94.14   | -2.98    | -6.97890000000001   |
| M10 / Y        | NEG      | 5.18    | -1.04    | -5.0428395833333335 |
| M10 / N        | NEG      | 94.82   | -2.30    | -6.2991604166666715 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Kansas Senate election by 20%-25%?
Contract 3343542; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        8.84 |         9.16 | +90.84 / −9.16   | 9.91×         |
| No     |       96.99 |        97.11 | +2.89 / −97.11   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.90    | -8.26    | -11.162139999999999 |
| GB / N         | WEAK     | 99.10   | 1.99     | -2.012713824121104  |
| ST / Y         | NEG      | 0.37    | -8.79    | -11.162139999999999 |
| ST / N         | WEAK     | 99.63   | 2.52     | -1.4782100000000131 |
| MX / Y         | NEG      | 0.89    | -8.28    | -11.162139999999999 |
| MX / N         | WEAK     | 99.11   | 2.00     | -1.9956579166666821 |
| M10 / Y        | NEG      | 0.75    | -8.41    | -11.162139999999999 |
| M10 / N        | WEAK     | 99.25   | 2.14     | -1.8622725000000173 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Kansas Senate election by 25%-30%?
Contract 3343541; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          11 |        11.39 | +88.61 / −11.39  | 7.78×         |
| No     |          95 |        95.19 | +4.81 / −95.19   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | NEG      | 0.05    | -11.34   | -13.3916           |
| GB / N         | GO       | 99.95   | 4.76     | 0.7554466825398842 |
| ST / Y         | NEG      | 0.02    | -11.37   | -13.3916           |
| ST / N         | GO       | 99.98   | 4.79     | 0.7881249999999951 |
| MX / Y         | NEG      | 0.07    | -11.33   | -13.3916           |
| MX / N         | GO       | 99.93   | 4.74     | 0.7443749999999971 |
| M10 / Y        | NEG      | 0.05    | -11.34   | -13.3916           |
| M10 / N        | GO       | 99.95   | 4.76     | 0.7558854166666684 |
| RTWH / Y       | N/A      | —       | —        | —                  |
| RTWH / N       | N/A      | —       | —        | —                  |
| DDHQ / Y       | N/A      | —       | —        | —                  |
| DDHQ / N       | N/A      | —       | —        | —                  |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 10%-15%?
Contract 3343564; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          20 |        20.64 | +79.36 / −20.64  | 3.84×         |
| No     |          82 |        82.59 | +17.41 / −82.59  | 0.21×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 31.41   | 10.77    | 6.774491351664946   |
| GB / N         | NEG      | 68.59   | -14.00   | -18.00489135166494  |
| ST / Y         | GO       | 37.26   | 16.62    | 12.619375           |
| ST / N         | NEG      | 62.74   | -19.85   | -23.849775000000008 |
| MX / Y         | GO       | 31.05   | 10.41    | 6.405989583333333   |
| MX / N         | NEG      | 68.95   | -13.64   | -17.636389583333333 |
| M10 / Y        | GO       | 30.91   | 10.27    | 6.271614583333335   |
| M10 / N        | NEG      | 69.09   | -13.50   | -17.502014583333334 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 15%-20%?
Contract 3343563; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          80 |        80.64 | +19.36 / −80.64  | 0.24×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 23.98   | 2.32     | -1.6790022998784127 |
| GB / N         | NEG      | 76.02   | -4.62    | -8.624597700121583  |
| ST / Y         | WEAK     | 24.88   | 3.22     | -0.7792249999999973 |
| ST / N         | NEG      | 75.12   | -5.52    | -9.524375000000006  |
| MX / Y         | NEG      | 20.99   | -0.67    | -4.6711             |
| MX / N         | NEG      | 79.01   | -1.63    | -5.632499999999996  |
| M10 / Y        | WEAK     | 23.80   | 2.14     | -1.8597458333333288 |
| M10 / N        | NEG      | 76.20   | -4.44    | -8.443854166666675  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 20%-25%?
Contract 3343562; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          83 |        83.56 | +16.44 / −83.56  | 0.20×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 9.83    | -11.83   | -15.831589860167867 |
| GB / N         | GO       | 90.17   | 6.60     | 2.603589860167854   |
| ST / Y         | NEG      | 7.13    | -14.53   | -18.529225          |
| ST / N         | GO       | 92.87   | 9.30     | 5.301224999999987   |
| MX / Y         | NEG      | 7.77    | -13.90   | -17.89844375        |
| MX / N         | GO       | 92.23   | 8.67     | 4.670443749999986   |
| M10 / Y        | NEG      | 9.63    | -12.03   | -16.03235           |
| M10 / N        | GO       | 90.37   | 6.80     | 2.804349999999989   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 30%-35%?
Contract 3343560; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       11.28 |        11.68 | +88.32 / −11.68  | 7.56×         |
| No     |       93.6  |        93.84 | +6.16 / −93.84   | 0.07×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.25    | -11.43   | -13.680119999999999 |
| GB / N         | GO       | 99.75   | 5.91     | 1.9069330043262611  |
| ST / Y         | NEG      | 0.11    | -11.57   | -13.680119999999999 |
| ST / N         | GO       | 99.89   | 6.05     | 2.0479799999999937  |
| MX / Y         | NEG      | 0.28    | -11.40   | -13.680119999999999 |
| MX / N         | GO       | 99.72   | 5.88     | 1.8819383333333328  |
| M10 / Y        | NEG      | 0.40    | -11.28   | -13.680119999999999 |
| M10 / N        | GO       | 99.60   | 5.77     | 1.7652195833333328  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Louisiana Senate election by 0%-5%?
Contract 3343577; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        14.4 |        14.89 | +85.11 / −14.89  | 5.72×         |
| No     |        94.4 |        94.61 | +5.39 / −94.61   | 0.06×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 15.89   | 0.99     | -3.0060460168352954 |
| GB / N         | NEG      | 84.11   | -10.50   | -14.496833983164702 |
| ST / Y         | NEG      | 14.19   | -0.70    | -4.700894999999996  |
| ST / N         | NEG      | 85.81   | -8.80    | -12.801985000000007 |
| MX / Y         | GO       | 19.12   | 4.22     | 0.224938333333341   |
| MX / N         | NEG      | 80.88   | -13.73   | -17.727818333333335 |
| M10 / Y        | GO       | 19.38   | 4.49     | 0.48775083333333913 |
| M10 / N        | NEG      | 80.62   | -13.99   | -17.99063083333333  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Louisiana Senate election by 15%-20%?
Contract 3343574; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          24 |        24.73 | +75.27 / −24.73  | 3.04×         |
| No     |          81 |        81.62 | +18.38 / −81.62  | 0.23×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 15.11   | -9.62    | -13.620739182068327 |
| GB / N         | WEAK     | 84.89   | 3.28     | -0.7244608179316825 |
| ST / Y         | NEG      | 13.58   | -11.15   | -15.154600000000002 |
| ST / N         | GO       | 86.42   | 4.81     | 0.8093999999999935  |
| MX / Y         | NEG      | 11.59   | -13.14   | -17.139652083333335 |
| MX / N         | GO       | 88.41   | 6.79     | 2.794452083333332   |
| M10 / Y        | NEG      | 11.35   | -13.38   | -17.37970416666667  |
| M10 / N        | GO       | 88.65   | 7.03     | 3.034504166666663   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Louisiana Senate election by 20%-25%?
Contract 3343573; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       13.6  |        14.07 | +85.93 / −14.07  | 6.11×         |
| No     |       90.07 |        90.43 | +9.57 / −90.43   | 0.11×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 4.06    | -10.01   | -14.011019857489455 |
| GB / N         | GO       | 95.94   | 5.51     | 1.5138598574894524  |
| ST / Y         | NEG      | 2.27    | -11.79   | -15.794920000000001 |
| ST / N         | GO       | 97.72   | 7.30     | 3.297759999999994   |
| MX / Y         | NEG      | 2.84    | -11.23   | -15.225284583333334 |
| MX / N         | GO       | 97.16   | 6.73     | 2.7281245833333356  |
| M10 / Y        | NEG      | 2.76    | -11.31   | -15.305545          |
| M10 / N        | GO       | 97.24   | 6.81     | 2.8083850000000026  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Louisiana Senate election by 30%-35%?
Contract 3343571; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       13.49 |        13.93 | +86.07 / −13.93  | 6.18×         |
| No     |       96.47 |        96.61 | +3.39 / −96.61   | 0.04×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.04    | -13.89   | -15.933529999999998 |
| GB / N         | WEAK     | 99.96   | 3.35     | -0.6495432294449266 |
| ST / Y         | NEG      | 0.01    | -13.92   | -15.933529999999998 |
| ST / N         | WEAK     | 99.99   | 3.38     | -0.6208500000000061 |
| MX / Y         | NEG      | 0.05    | -13.88   | -15.933529999999998 |
| MX / N         | WEAK     | 99.95   | 3.34     | -0.6616312500000054 |
| M10 / Y        | NEG      | 0.05    | -13.88   | -15.933529999999998 |
| M10 / N        | WEAK     | 99.95   | 3.34     | -0.6607979166666667 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Louisiana Senate election by 5%-10%?
Contract 3343576; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          22 |        22.69 | +77.31 / −22.69  | 3.41×         |
| No     |          82 |        82.59 | +17.41 / −82.59  | 0.21×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 29.86   | 7.18     | 3.1782159723570844  |
| GB / N         | NEG      | 70.14   | -12.46   | -16.455015972357078 |
| ST / Y         | GO       | 32.12   | 9.44     | 5.435475            |
| ST / N         | NEG      | 67.88   | -14.71   | -18.712275          |
| MX / Y         | GO       | 29.45   | 6.76     | 2.7600583333333373  |
| MX / N         | NEG      | 70.55   | -12.04   | -16.03685833333334  |
| M10 / Y        | GO       | 29.52   | 6.84     | 2.835214583333334   |
| M10 / N        | NEG      | 70.48   | -12.11   | -16.112014583333334 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Michigan Senate election by 0%-3%?
Contract 3343886; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          17 |        17.56 | +82.44 / −17.56  | 4.69×         |
| No     |          84 |        84.54 | +15.46 / −84.54  | 0.18×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 9.58    | -7.99    | -11.986452029192371 |
| GB / N         | GO       | 90.42   | 5.88     | 1.8844520291923628  |
| ST / Y         | NEG      | 7.54    | -10.02   | -14.023774999999999 |
| ST / N         | GO       | 92.46   | 7.92     | 3.921774999999994   |
| MX / Y         | NEG      | 9.43    | -8.14    | -12.137472916666665 |
| MX / N         | GO       | 90.57   | 6.04     | 2.0354729166666585  |
| M10 / Y        | NEG      | 11.31   | -6.26    | -10.257316666666666 |
| M10 / N        | GO       | 88.69   | 4.16     | 0.15531666666666055 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Michigan Senate election by 12% or more?
Contract 3343882; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       11.58 |        11.99 | +88.01 / −11.99  | 7.34×         |
| No     |       99.7  |        99.71 | +0.29 / −99.71   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.14    | -11.85   | -13.98947           |
| GB / N         | WEAK     | 99.86   | 0.15     | -3.8494331671657394 |
| ST / Y         | NEG      | 0.09    | -11.90   | -13.98947           |
| ST / N         | WEAK     | 99.91   | 0.19     | -3.8057100000000066 |
| MX / Y         | NEG      | 0.29    | -11.70   | -13.98947           |
| MX / N         | WEAK     | 99.71   | 0.00     | -3.9982620833333375 |
| M10 / Y        | NEG      | 0.39    | -11.60   | -13.98947           |
| M10 / N        | NEG      | 99.61   | -0.11    | -4.106126666666665  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Michigan Senate election by 6%-9%?
Contract 3343884; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       30.56 |        31.37 | +68.63 / −31.37  | 2.19×         |
| No     |       95.02 |        95.2  | +4.80 / −95.20   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)           |
|:---------------|:---------|:--------|:---------|:---------------------|
| GB / Y         | NEG      | 1.73    | -29.65   | -33.372840000000004  |
| GB / N         | WEAK     | 98.27   | 3.07     | -0.9309383920397707  |
| ST / Y         | NEG      | 0.97    | -30.40   | -33.372840000000004  |
| ST / N         | WEAK     | 99.02   | 3.82     | -0.17946000000000908 |
| MX / Y         | NEG      | 1.89    | -29.48   | -33.372840000000004  |
| MX / N         | WEAK     | 98.11   | 2.91     | -1.0928975000000007  |
| M10 / Y        | NEG      | 2.50    | -28.88   | -32.875496250000005  |
| M10 / N        | WEAK     | 97.50   | 2.30     | -1.7018037500000083  |
| RTWH / Y       | N/A      | —       | —        | —                    |
| RTWH / N       | N/A      | —       | —        | —                    |
| DDHQ / Y       | N/A      | —       | —        | —                    |
| DDHQ / N       | N/A      | —       | —        | —                    |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Michigan Senate election by 9%-12%?
Contract 3343883; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       24.27 |        24.98 | +75.02 / −24.98  | 3.00×         |
| No     |       97.95 |        98.03 | +1.97 / −98.03   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.50    | -24.47   | -26.97835           |
| GB / N         | WEAK     | 99.50   | 1.46     | -2.5359847961896387 |
| ST / Y         | NEG      | 0.24    | -24.73   | -26.97835           |
| ST / N         | WEAK     | 99.76   | 1.72     | -2.2763600000000106 |
| MX / Y         | NEG      | 0.65    | -24.33   | -26.97835           |
| MX / N         | WEAK     | 99.36   | 1.32     | -2.677610000000008  |
| M10 / Y        | NEG      | 0.92    | -24.06   | -26.97835           |
| M10 / N        | WEAK     | 99.08   | 1.05     | -2.9507350000000154 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 New Hampshire Senate election by 0%-3%?
Contract 3343937; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       14.84 |        15.35 | +84.65 / −15.35  | 5.52×         |
| No     |       90    |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.57    | -13.78   | -17.34526           |
| GB / N         | GO       | 98.43   | 8.07     | 4.0726709864043915  |
| ST / Y         | NEG      | 1.72    | -13.63   | -17.34526           |
| ST / N         | GO       | 98.28   | 7.92     | 3.924375000000002   |
| MX / Y         | NEG      | 4.40    | -10.95   | -14.94921833333333  |
| MX / N         | GO       | 95.60   | 5.24     | 1.2439583333333282  |
| M10 / Y        | NEG      | 3.79    | -11.56   | -15.559426666666665 |
| M10 / N        | GO       | 96.21   | 5.85     | 1.854166666666668   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 New Hampshire Senate election by 3%-6%?
Contract 3343936; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       24.58 |        25.27 | +74.73 / −25.27  | 2.96×         |
| No     |       99.3  |        99.33 | +0.67 / −99.33   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.41    | -24.86   | -27.26727           |
| GB / N         | WEAK     | 99.59   | 0.26     | -3.7381065617119074 |
| ST / Y         | NEG      | 0.53    | -24.74   | -27.26727           |
| ST / N         | WEAK     | 99.47   | 0.14     | -3.8590499999999976 |
| MX / Y         | NEG      | 1.86    | -23.40   | -27.26727           |
| MX / N         | NEG      | 98.14   | -1.19    | -5.192747916666662  |
| M10 / Y        | NEG      | 1.57    | -23.70   | -27.26727           |
| M10 / N        | NEG      | 98.43   | -0.90    | -4.8959770833333245 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 New Hampshire Senate election by 6% or more?
Contract 3343935; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       17.92 |        18.41 | +81.59 / −18.41  | 4.43×         |
| No     |       99.8  |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.10    | -18.31   | -20.408430000000003 |
| GB / N         | WEAK     | 99.90   | 0.10     | -3.9030077126916973 |
| ST / Y         | NEG      | 0.18    | -18.23   | -20.408430000000003 |
| ST / N         | WEAK     | 99.83   | 0.02     | -3.982980000000003  |
| MX / Y         | NEG      | 0.97    | -17.44   | -20.408430000000003 |
| MX / N         | NEG      | 99.03   | -0.78    | -4.777146666666665  |
| M10 / Y        | NEG      | 0.77    | -17.64   | -20.408430000000003 |
| M10 / N        | NEG      | 99.23   | -0.57    | -4.574698749999994  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 North Carolina Senate election by 0%-3%?
Contract 3344032; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         6.5 |         6.74 | +93.26 / −6.74   | 13.83×        |
| No     |        96   |        96.15 | +3.85 / −96.15   | 0.04×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 9.43    | 2.69     | -1.3121106762773491 |
| GB / N         | NEG      | 90.57   | -5.58    | -9.584589323722648  |
| ST / Y         | WEAK     | 7.11    | 0.37     | -3.633725000000001  |
| ST / N         | NEG      | 92.89   | -3.26    | -7.262974999999994  |
| MX / Y         | WEAK     | 8.65    | 1.90     | -2.097735416666667  |
| MX / N         | NEG      | 91.35   | -4.80    | -8.798964583333335  |
| M10 / Y        | WEAK     | 8.70    | 1.96     | -2.0444020833333356 |
| M10 / N        | NEG      | 91.30   | -4.85    | -8.852297916666663  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Ohio Senate election by 0%-3%?
Contract 3344046; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          19 |        19.62 | +80.38 / −19.62  | 4.10×         |
| No     |          83 |        83.56 | +16.44 / −83.56  | 0.20×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 15.29   | -4.33    | -8.327464128137663  |
| GB / N         | WEAK     | 84.71   | 1.15     | -2.8525358718623384 |
| ST / Y         | NEG      | 15.56   | -4.06    | -8.056224999999998  |
| ST / N         | WEAK     | 84.44   | 0.88     | -3.1237750000000064 |
| MX / Y         | NEG      | 16.38   | -3.23    | -7.232474999999996  |
| MX / N         | WEAK     | 83.62   | 0.05     | -3.9475250000000073 |
| M10 / Y        | NEG      | 17.88   | -1.74    | -5.739714583333333  |
| M10 / N        | NEG      | 82.12   | -1.44    | -5.440285416666679  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Ohio Senate election by 6%-9%?
Contract 3344044; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.38 |         9.7  | +90.30 / −9.70   | 9.30×         |
| No     |       97.2  |        97.31 | +2.69 / −97.31   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 3.87    | -5.84    | -9.838985681132337  |
| GB / N         | NEG      | 96.13   | -1.17    | -5.174384318867675  |
| ST / Y         | NEG      | 2.07    | -7.64    | -11.638885000000002 |
| ST / N         | WEAK     | 97.93   | 0.63     | -3.374485000000016  |
| MX / Y         | NEG      | 3.77    | -5.94    | -9.937530833333334  |
| MX / N         | NEG      | 96.23   | -1.08    | -5.075839166666674  |
| M10 / Y        | NEG      | 4.57    | -5.13    | -9.133728750000001  |
| M10 / N        | NEG      | 95.43   | -1.88    | -5.879641250000011  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Oklahoma Senate election by 15%-20%?
Contract 3344070; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        16.8 |        17.36 | +82.64 / −17.36  | 4.76×         |
| No     |        87   |        87.45 | +12.55 / −87.45  | 0.14×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 13.24   | -4.12    | -8.119126343916456  |
| GB / N         | NEG      | 86.76   | -0.69    | -4.692313656083547  |
| ST / Y         | NEG      | 11.28   | -6.08    | -10.08404           |
| ST / N         | WEAK     | 88.72   | 1.27     | -2.7274000000000016 |
| MX / Y         | NEG      | 13.55   | -3.81    | -7.811696249999998  |
| MX / N         | NEG      | 86.45   | -1.00    | -4.999743749999997  |
| M10 / Y        | NEG      | 11.99   | -5.37    | -9.366748333333334  |
| M10 / N        | WEAK     | 88.01   | 0.56     | -3.4446916666666656 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Oklahoma Senate election by 30%-35%?
Contract 3344067; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        15   |        15.51 | +84.49 / −15.51  | 5.45×         |
| No     |        89.9 |        90.25 | +9.75 / −90.25   | 0.11×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 18.84   | 3.33     | -0.6663586198582621 |
| GB / N         | NEG      | 81.16   | -9.10    | -13.09807138014174  |
| ST / Y         | WEAK     | 18.41   | 2.90     | -1.1037499999999978 |
| ST / N         | NEG      | 81.59   | -8.66    | -12.660680000000003 |
| MX / Y         | WEAK     | 17.85   | 2.34     | -1.660677083333331  |
| MX / N         | NEG      | 82.15   | -8.10    | -12.103752916666668 |
| M10 / Y        | GO       | 19.57   | 4.06     | 0.05510416666666962 |
| M10 / N        | NEG      | 80.43   | -9.82    | -13.819534166666669 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Oklahoma Senate election by 40%-45%?
Contract 3344065; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       18.36 |        18.88 | +81.12 / −18.88  | 4.30×         |
| No     |       97.66 |        97.75 | +2.25 / −97.75   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.68    | -17.19   | -20.87708           |
| GB / N         | WEAK     | 98.32   | 0.57     | -3.4318948234330793 |
| ST / Y         | NEG      | 0.81    | -18.06   | -20.87708           |
| ST / N         | WEAK     | 99.19   | 1.44     | -2.5623000000000062 |
| MX / Y         | NEG      | 2.08    | -16.80   | -20.797184166666668 |
| MX / N         | WEAK     | 97.92   | 0.17     | -3.829695833333335  |
| M10 / Y        | NEG      | 2.54    | -16.34   | -20.34072583333333  |
| M10 / N        | NEG      | 97.46   | -0.29    | -4.286154166666667  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Oklahoma Senate election by 45% or more?
Contract 3344064; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        11.1 |        11.46 | +88.54 / −11.46  | 7.72×         |
| No     |        99.3 |        99.33 | +0.67 / −99.33   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.24    | -11.22   | -13.46299           |
| GB / N         | WEAK     | 99.76   | 0.43     | -3.572493910512276  |
| ST / Y         | NEG      | 0.16    | -11.31   | -13.46299           |
| ST / N         | WEAK     | 99.84   | 0.52     | -3.484049999999994  |
| MX / Y         | NEG      | 0.55    | -10.91   | -13.46299           |
| MX / N         | WEAK     | 99.45   | 0.12     | -3.8821229166666638 |
| M10 / Y        | NEG      | 0.70    | -10.77   | -13.46299           |
| M10 / N        | NEG      | 99.30   | -0.03    | -4.025195833333328  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 0%-5%?
Contract 3344126; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          29 |        29.82 | +70.18 / −29.82  | 2.35×         |
| No     |          73 |        73.79 | +26.21 / −73.79  | 0.36×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 15.48   | -14.35   | -18.346082935097296 |
| GB / N         | GO       | 84.52   | 10.73    | 6.734082935097296   |
| ST / Y         | NEG      | 13.98   | -15.84   | -19.842349999999996 |
| ST / N         | GO       | 86.02   | 12.23    | 8.230349999999998   |
| MX / Y         | NEG      | 18.14   | -11.68   | -15.683756249999995 |
| MX / N         | GO       | 81.86   | 8.07     | 4.071756250000003   |
| M10 / Y        | NEG      | 16.88   | -12.94   | -16.941933333333328 |
| M10 / N        | GO       | 83.12   | 9.33     | 5.3299333333333365  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 10%-15%?
Contract 3344124; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       16.54 |        17.09 | +82.91 / −17.09  | 4.85×         |
| No     |       85.4  |        85.9  | +14.10 / −85.90  | 0.16×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 29.89   | 12.80    | 8.798784716252841   |
| GB / N         | NEG      | 70.11   | -15.79   | -19.78950471625285  |
| ST / Y         | GO       | 34.44   | 17.35    | 13.345419999999995  |
| ST / N         | NEG      | 65.56   | -20.34   | -24.33614000000001  |
| MX / Y         | GO       | 27.45   | 10.36    | 6.361357499999994   |
| MX / N         | NEG      | 72.55   | -13.35   | -17.352077500000007 |
| M10 / Y        | GO       | 28.49   | 11.40    | 7.397294999999996   |
| M10 / N        | NEG      | 71.51   | -14.39   | -18.388015000000003 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 15%-20%?
Contract 3344123; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        10.8 |        11.19 | +88.81 / −11.19  | 7.94×         |
| No     |        92   |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 15.33   | 4.14     | 0.14141286948193277 |
| GB / N         | NEG      | 84.67   | -7.62    | -11.62109286948193  |
| ST / Y         | WEAK     | 13.14   | 1.96     | -2.0415299999999985 |
| ST / N         | NEG      | 86.86   | -5.44    | -9.43815            |
| MX / Y         | WEAK     | 12.02   | 0.83     | -3.1674674999999994 |
| MX / N         | NEG      | 87.98   | -4.31    | -8.312212500000005  |
| M10 / Y        | WEAK     | 13.25   | 2.07     | -1.9320508333333333 |
| M10 / N        | NEG      | 86.75   | -5.55    | -9.54762916666667   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 20%-25%?
Contract 3344122; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        5.81 |         6.02 | +93.98 / −6.02   | 15.60×        |
| No     |       97.46 |        97.56 | +2.44 / −97.56   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | NEG      | 4.04    | -1.99    | -5.988424989445572 |
| GB / N         | NEG      | 95.96   | -1.60    | -5.596005010554439 |
| ST / Y         | NEG      | 2.08    | -3.94    | -7.939565          |
| ST / N         | WEAK     | 97.92   | 0.36     | -3.644865000000019 |
| MX / Y         | NEG      | 2.92    | -3.10    | -7.104617083333334 |
| MX / N         | NEG      | 97.08   | -0.48    | -4.479812916666681 |
| M10 / Y        | NEG      | 3.35    | -2.68    | -6.675762916666667 |
| M10 / N        | NEG      | 96.65   | -0.91    | -4.908667083333351 |
| RTWH / Y       | N/A      | —       | —        | —                  |
| RTWH / N       | N/A      | —       | —        | —                  |
| DDHQ / Y       | N/A      | —       | —        | —                  |
| DDHQ / N       | N/A      | —       | —        | —                  |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 25%-30%?
Contract 3344121; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        5.19 |         5.39 | +94.61 / −5.39   | 17.57×        |
| No     |       99.3  |        99.33 | +0.67 / −99.33   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.54    | -4.84    | -7.38626            |
| GB / N         | WEAK     | 99.46   | 0.13     | -3.87165334813957   |
| ST / Y         | NEG      | 0.26    | -5.13    | -7.38626            |
| ST / N         | WEAK     | 99.74   | 0.41     | -3.5871749999999865 |
| MX / Y         | NEG      | 0.44    | -4.94    | -7.38626            |
| MX / N         | WEAK     | 99.56   | 0.23     | -3.7695187499999894 |
| M10 / Y        | NEG      | 0.51    | -4.88    | -7.38626            |
| M10 / N        | WEAK     | 99.49   | 0.16     | -3.837174999999993  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 30% or more?
Contract 3344120; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         6.6 |         6.84 | +93.16 / −6.84   | 13.62×        |
| No     |        99.5 |        99.52 | +0.48 / −99.52   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.04    | -6.80    | -8.83952            |
| GB / N         | WEAK     | 99.96   | 0.44     | -3.558586705563871  |
| ST / Y         | NEG      | 0.02    | -6.82    | -8.83952            |
| ST / N         | WEAK     | 99.98   | 0.46     | -3.535524999999995  |
| MX / Y         | NEG      | 0.06    | -6.78    | -8.83952            |
| MX / N         | WEAK     | 99.94   | 0.42     | -3.577347916666662  |
| M10 / Y        | NEG      | 0.08    | -6.76    | -8.83952            |
| M10 / N        | WEAK     | 99.92   | 0.40     | -3.5969312500000017 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Tennessee Senate election by 0%-10%?
Contract 3344156; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        8.43 |         8.73 | +91.27 / −8.73   | 10.45×        |
| No     |       97.58 |        97.67 | +2.33 / −97.67   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 2.70    | -6.03    | -10.034247339056023 |
| GB / N         | NEG      | 97.30   | -0.37    | -4.371882660943982  |
| ST / Y         | NEG      | 1.44    | -7.29    | -10.731929999999998 |
| ST / N         | WEAK     | 98.56   | 0.89     | -3.1117000000000066 |
| MX / Y         | NEG      | 2.79    | -5.95    | -9.946044583333332  |
| MX / N         | NEG      | 97.21   | -0.46    | -4.46008541666667   |
| M10 / Y        | NEG      | 1.77    | -6.96    | -10.731929999999998 |
| M10 / N        | WEAK     | 98.23   | 0.55     | -3.447325000000001  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Tennessee Senate election by 10%-15%?
Contract 3344155; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          17 |        17.56 | +82.44 / −17.56  | 4.69×         |
| No     |          84 |        84.54 | +15.46 / −84.54  | 0.18×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 9.71    | -7.85    | -11.853309677381798 |
| GB / N         | GO       | 90.29   | 5.75     | 1.751309677381796   |
| ST / Y         | NEG      | 7.53    | -10.04   | -14.036274999999998 |
| ST / N         | GO       | 92.47   | 7.93     | 3.934274999999998   |
| MX / Y         | NEG      | 8.99    | -8.58    | -12.576899999999998 |
| MX / N         | GO       | 91.01   | 6.47     | 2.474899999999991   |
| M10 / Y        | NEG      | 6.53    | -11.04   | -15.039087499999999 |
| M10 / N        | GO       | 93.47   | 8.94     | 4.9370874999999925  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Tennessee Senate election by 15%-20%?
Contract 3344154; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       15.13 |        15.65 | +84.35 / −15.65  | 5.39×         |
| No     |       86    |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 22.61   | 6.96     | 2.963025627934895   |
| GB / N         | NEG      | 77.39   | -9.09    | -13.093145627934899 |
| ST / Y         | GO       | 24.98   | 9.33     | 5.332730000000002   |
| ST / N         | NEG      | 75.02   | -11.46   | -15.462850000000008 |
| MX / Y         | GO       | 22.08   | 6.43     | 2.4266362500000027  |
| MX / N         | NEG      | 77.92   | -8.56    | -12.556756250000012 |
| M10 / Y        | WEAK     | 18.37   | 2.72     | -1.2810720833333318 |
| M10 / N        | NEG      | 81.63   | -4.85    | -8.849047916666674  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Tennessee Senate election by 25%-30%?
Contract 3344152; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          17 |        17.56 | +82.44 / −17.56  | 4.69×         |
| No     |          85 |        85.51 | +14.49 / −85.51  | 0.17×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 22.59   | 5.02     | 1.0249689722677897  |
| GB / N         | NEG      | 77.41   | -8.10    | -12.099368972267799 |
| ST / Y         | GO       | 21.72   | 4.15     | 0.1543500000000031  |
| ST / N         | NEG      | 78.28   | -7.23    | -11.228750000000009 |
| MX / Y         | GO       | 22.44   | 4.87     | 0.8749750000000028  |
| MX / N         | NEG      | 77.56   | -7.95    | -11.949375000000007 |
| M10 / Y        | GO       | 25.69   | 8.12     | 4.123099999999999   |
| M10 / N        | NEG      | 74.31   | -11.20   | -15.197500000000009 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Tennessee Senate election by 45% or more?
Contract 3344148; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        6.93 |         7.18 | +92.82 / −7.18   | 12.93×        |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.03    | -7.15    | -9.177349999999999  |
| GB / N         | WEAK     | 99.97   | 0.36     | -3.6426365741092814 |
| ST / Y         | NEG      | 0.03    | -7.15    | -9.177349999999999  |
| ST / N         | WEAK     | 99.97   | 0.35     | -3.647189999999989  |
| MX / Y         | NEG      | 0.11    | -7.07    | -9.177349999999999  |
| MX / N         | WEAK     | 99.89   | 0.27     | -3.727971249999984  |
| M10 / Y        | NEG      | 0.21    | -6.97    | -9.177349999999999  |
| M10 / N        | WEAK     | 99.79   | 0.17     | -3.8272941666666505 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Texas Senate election by 0%-3%?
Contract 3344140; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          82 |        82.59 | +17.41 / −82.59  | 0.21×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 21.67   | 0.00     | -3.9977917929015727 |
| GB / N         | NEG      | 78.33   | -4.26    | -8.256208207098425  |
| ST / Y         | WEAK     | 25.15   | 3.49     | -0.5104749999999991 |
| ST / N         | NEG      | 74.85   | -7.74    | -11.743524999999998 |
| MX / Y         | WEAK     | 23.65   | 1.98     | -2.0156833333333317 |
| MX / N         | NEG      | 76.35   | -6.24    | -10.23831666666667  |
| M10 / Y        | WEAK     | 23.52   | 1.86     | -2.1409958333333314 |
| M10 / N        | NEG      | 76.48   | -6.11    | -10.113004166666673 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Texas Senate election by 12% or more?
Contract 3344136; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        1.94 |         2.02 | +97.98 / −2.02   | 48.60×        |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.42    | -1.59    | -4.016109999999999  |
| GB / N         | NEG      | 99.58   | -0.04    | -4.038532506731595  |
| ST / Y         | NEG      | 0.17    | -1.84    | -4.016109999999999  |
| ST / N         | WEAK     | 99.83   | 0.21     | -3.7878149999999833 |
| MX / Y         | NEG      | 0.46    | -1.56    | -4.016109999999999  |
| MX / N         | NEG      | 99.54   | -0.07    | -4.072294166666646  |
| M10 / Y        | NEG      | 0.45    | -1.57    | -4.016109999999999  |
| M10 / N        | NEG      | 99.55   | -0.07    | -4.065783749999985  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Texas Senate election by 3%-6%?
Contract 3344139; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       11.46 |        11.87 | +88.13 / −11.87  | 7.43×         |
| No     |       89.2  |        89.59 | +10.41 / −89.59  | 0.12×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 13.56   | 1.69     | -2.30779477307627   |
| GB / N         | NEG      | 86.44   | -3.14    | -7.143405226923738  |
| ST / Y         | WEAK     | 12.10   | 0.24     | -3.762735000000002  |
| ST / N         | NEG      | 87.90   | -1.69    | -5.6884650000000105 |
| MX / Y         | WEAK     | 13.83   | 1.96     | -2.038203750000002  |
| MX / N         | NEG      | 86.17   | -3.41    | -7.4129962500000035 |
| M10 / Y        | WEAK     | 13.69   | 1.82     | -2.1751308333333346 |
| M10 / N        | NEG      | 86.31   | -3.28    | -7.276069166666677  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Texas Senate election by 9%-12%?
Contract 3344137; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         5.6 |         5.81 | +94.19 / −5.81   | 16.22×        |
| No     |        98.3 |        98.37 | +1.63 / −98.37   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.76    | -4.05    | -7.806040000000001  |
| GB / N         | NEG      | 98.24   | -0.13    | -4.126846062794343  |
| ST / Y         | NEG      | 0.80    | -5.01    | -7.806040000000001  |
| ST / N         | WEAK     | 99.20   | 0.84     | -3.1637150000000003 |
| MX / Y         | NEG      | 1.61    | -4.20    | -7.806040000000001  |
| MX / N         | WEAK     | 98.39   | 0.03     | -3.9746524999999973 |
| M10 / Y        | NEG      | 1.57    | -4.23    | -7.806040000000001  |
| M10 / N        | WEAK     | 98.43   | 0.06     | -3.9417358333333374 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party control the Senate after the 2026 Midterm elections?
Contract 562794; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          38 |        38.94 | +61.06 / −38.94  | 1.57×         |
| No     |          63 |        63.93 | +36.07 / −63.93  | 0.56×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   39.83 |     0.88 |        -3.12 |
| GB / N         | NEG      |   60.17 |    -3.76 |        -7.76 |
| ST / Y         | NEG      |   36.50 |    -2.44 |        -6.44 |
| ST / N         | NEG      |   63.50 |    -0.43 |        -4.43 |
| MX / Y         | NEG      |   31.18 |    -7.77 |       -11.77 |
| MX / N         | GO       |   68.82 |     4.89 |         0.89 |
| M10 / Y        | NEG      |   35.05 |    -3.89 |        -7.89 |
| M10 / N        | WEAK     |   64.95 |     1.02 |        -2.98 |
| RTWH / Y       | NEG      |   29.50 |    -9.44 |       -13.44 |
| RTWH / N       | GO       |   70.50 |     6.57 |         2.57 |
| DDHQ / Y       | GO       |   46.00 |     7.06 |         3.06 |
| DDHQ / N       | NEG      |   54.00 |    -9.93 |       -13.93 |

RTWH (2026-09-25): Conditional on publisher caucus accounting, complete chamber and GOP tie-break convention; independents are not reclassified as Democrats in state contracts. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Conditional on publisher caucus accounting, complete chamber and GOP tie-break convention; independents are not reclassified as Democrats in state contracts. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party hold 47 or fewer Senate seats after the 2026 midterm elections?
Contract 943819; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          37 |        37.93 | +62.07 / −37.93  | 1.64×         |
| No     |          64 |        64.92 | +35.08 / −64.92  | 0.54×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 14.50   | -23.43   | -27.429066666666667 |
| GB / N         | GO       | 85.50   | 20.58    | 16.57506666666666   |
| ST / Y         | NEG      | 14.57   | -23.36   | -27.363650000000007 |
| ST / N         | GO       | 85.43   | 20.51    | 16.509649999999997  |
| MX / Y         | NEG      | 25.03   | -12.90   | -16.89828541666886  |
| MX / N         | GO       | 74.97   | 10.04    | 6.04428541666886    |
| M10 / Y        | NEG      | 22.32   | -15.61   | -19.610472916669643 |
| M10 / N        | GO       | 77.68   | 12.76    | 8.756472916669633   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | NEG      | 34.67   | -3.26    | -7.261400000000001  |
| DDHQ / N       | WEAK     | 65.33   | 0.41     | -3.5926000000000125 |

RTWH (2026-09-25): Publisher supplies no seat-count distribution; expected seats cannot price this contract.
DDHQ (2026-09-25): Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party hold 57 or more Senate seats after the 2026 midterm elections?
Contract 943829; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         0.7 |         0.73 | +99.27 / −0.73   | 136.40×       |
| No     |        99.6 |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.00    | -0.73    | -2.7278000000000002 |
| GB / N         | WEAK     | 100.00  | 0.38     | -3.615939999999984  |
| ST / Y         | NEG      | 0.00    | -0.73    | -2.7278000000000002 |
| ST / N         | WEAK     | 100.00  | 0.38     | -3.615939999999984  |
| MX / Y         | NEG      | 0.00    | -0.73    | -2.7278000000000002 |
| MX / N         | WEAK     | 100.00  | 0.38     | -3.615939999999984  |
| M10 / Y        | NEG      | 0.00    | -0.73    | -2.7278000000000002 |
| M10 / N        | WEAK     | 100.00  | 0.38     | -3.615939999999984  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | WEAK     | 3.09    | 2.36     | -1.6420000000000003 |
| DDHQ / N       | NEG      | 96.91   | -2.70    | -6.701739999999989  |

RTWH (2026-09-25): Publisher supplies no seat-count distribution; expected seats cannot price this contract.
DDHQ (2026-09-25): Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party hold exactly 48 Senate seats after the 2026 midterm elections?
Contract 943820; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          16 |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |          86 |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)           |
|:---------------|:---------|:--------|:---------|:---------------------|
| GB / Y         | WEAK     | 20.04   | 3.50     | -0.5009333333333338  |
| GB / N         | NEG      | 79.96   | -6.52    | -10.518266666666678  |
| ST / Y         | GO       | 21.82   | 5.29     | 1.2873999999999994   |
| ST / N         | NEG      | 78.17   | -8.31    | -12.306600000000012  |
| MX / Y         | GO       | 21.01   | 4.48     | 0.47635833333578015  |
| MX / N         | NEG      | 78.99   | -7.50    | -11.495558333335786  |
| M10 / Y        | WEAK     | 19.82   | 3.28     | -0.7175999999967569  |
| M10 / N        | NEG      | 80.18   | -6.30    | -10.301600000003253  |
| RTWH / Y       | N/A      | —       | —        | —                    |
| RTWH / N       | N/A      | —       | —        | —                    |
| DDHQ / Y       | NEG      | 9.59    | -6.95    | -10.950200000000002  |
| DDHQ / N       | WEAK     | 90.41   | 3.93     | -0.06900000000000794 |

RTWH (2026-09-25): Publisher supplies no seat-count distribution; expected seats cannot price this contract.
DDHQ (2026-09-25): Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party hold exactly 49 Senate seats after the 2026 midterm elections?
Contract 943821; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          14 |        14.48 | +85.52 / −14.48  | 5.91×         |
| No     |          87 |        87.45 | +12.55 / −87.45  | 0.14×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 25.63   | 11.15    | 7.151733333333335   |
| GB / N         | NEG      | 74.37   | -13.09   | -17.08573333333333  |
| ST / Y         | GO       | 27.11   | 12.62    | 8.624649999999995   |
| ST / N         | NEG      | 72.89   | -14.56   | -18.55865           |
| MX / Y         | GO       | 22.78   | 8.29     | 4.294493750001075   |
| MX / N         | NEG      | 77.22   | -10.23   | -14.22849375000107  |
| M10 / Y        | GO       | 22.81   | 8.33     | 4.325587500001074   |
| M10 / N        | NEG      | 77.19   | -10.26   | -14.25958750000108  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | NEG      | 9.92    | -4.56    | -8.559100000000003  |
| DDHQ / N       | WEAK     | 90.08   | 2.63     | -1.3749000000000011 |

RTWH (2026-09-25): Publisher supplies no seat-count distribution; expected seats cannot price this contract.
DDHQ (2026-09-25): Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party hold exactly 50 Senate seats after the 2026 midterm elections?
Contract 943822; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          11 |        11.39 | +88.61 / −11.39  | 7.78×         |
| No     |          90 |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 21.60   | 10.21    | 6.205066666666666   |
| GB / N         | NEG      | 78.40   | -11.96   | -15.956666666666663 |
| ST / Y         | GO       | 21.65   | 10.26    | 6.255274999999999   |
| ST / N         | NEG      | 78.35   | -12.01   | -16.006874999999997 |
| MX / Y         | GO       | 17.56   | 6.17     | 2.1666291666667616  |
| MX / N         | NEG      | 82.44   | -7.92    | -11.91822916666676  |
| M10 / Y        | GO       | 18.69   | 7.30     | 3.296785416666834   |
| M10 / N        | NEG      | 81.31   | -9.05    | -13.04838541666683  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | NEG      | 9.69    | -1.70    | -5.703400000000001  |
| DDHQ / N       | NEG      | 90.31   | -0.05    | -4.048200000000001  |

RTWH (2026-09-25): Publisher supplies no seat-count distribution; expected seats cannot price this contract.
DDHQ (2026-09-25): Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party hold exactly 51 Senate seats after the 2026 midterm elections?
Contract 943823; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           9 |         9.33 | +90.67 / −9.33   | 9.72×         |
| No     |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 12.21   | 2.88     | -1.1209333333333336 |
| GB / N         | NEG      | 87.79   | -4.50    | -8.501066666666668  |
| ST / Y         | WEAK     | 10.49   | 1.16     | -2.840100000000001  |
| ST / N         | NEG      | 89.51   | -2.78    | -6.781900000000007  |
| MX / Y         | NEG      | 9.10    | -0.22    | -4.22260000000097   |
| MX / N         | NEG      | 90.90   | -1.40    | -5.399399999999033  |
| M10 / Y        | WEAK     | 10.55   | 1.22     | -2.7764020833345784 |
| M10 / N        | NEG      | 89.45   | -2.85    | -6.845597916665424  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | NEG      | 8.91    | -0.42    | -4.417900000000001  |
| DDHQ / N       | NEG      | 91.09   | -1.20    | -5.2041             |

RTWH (2026-09-25): Publisher supplies no seat-count distribution; expected seats cannot price this contract.
DDHQ (2026-09-25): Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party hold exactly 52 Senate seats after the 2026 midterm elections?
Contract 943824; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         6.1 |         6.33 | +93.67 / −6.33   | 14.80×        |
| No     |        94.9 |        95.09 | +4.91 / −95.09   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 4.51    | -1.82    | -5.815786666666667  |
| GB / N         | WEAK     | 95.49   | 0.39     | -3.6069333333333393 |
| ST / Y         | NEG      | 3.46    | -2.87    | -6.866619999999999  |
| ST / N         | WEAK     | 96.54   | 1.44     | -2.5561000000000056 |
| MX / Y         | NEG      | 3.32    | -3.01    | -7.0080262500003485 |
| MX / N         | WEAK     | 96.68   | 1.59     | -2.4146937499996524 |
| M10 / Y        | NEG      | 4.16    | -2.17    | -6.166463750000159  |
| M10 / N        | WEAK     | 95.84   | 0.74     | -3.256256249999845  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | WEAK     | 7.65    | 1.33     | -2.6744199999999996 |
| DDHQ / N       | NEG      | 92.35   | -2.75    | -6.7483000000000075 |

RTWH (2026-09-25): Publisher supplies no seat-count distribution; expected seats cannot price this contract.
DDHQ (2026-09-25): Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party hold exactly 53 Senate seats after the 2026 midterm elections?
Contract 943825; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        5.12 |         5.31 | +94.69 / −5.31   | 17.83×        |
| No     |       98.23 |        98.3  | +1.70 / −98.30   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.22    | -4.09    | -7.30957            |
| GB / N         | WEAK     | 98.78   | 0.48     | -3.5174200000000155 |
| ST / Y         | NEG      | 0.75    | -4.56    | -7.30957            |
| ST / N         | WEAK     | 99.25   | 0.95     | -3.0474200000000113 |
| MX / Y         | NEG      | 0.94    | -4.37    | -7.30957            |
| MX / N         | WEAK     | 99.06   | 0.76     | -3.2351804166665943 |
| M10 / Y        | NEG      | 1.31    | -4.00    | -7.30957            |
| M10 / N        | WEAK     | 98.69   | 0.40     | -3.6048679166666098 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | WEAK     | 6.23    | 0.92     | -3.0843700000000003 |
| DDHQ / N       | NEG      | 93.77   | -4.52    | -8.522620000000014  |

RTWH (2026-09-25): Publisher supplies no seat-count distribution; expected seats cannot price this contract.
DDHQ (2026-09-25): Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party hold exactly 56 Senate seats after the 2026 midterm elections?
Contract 943828; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         0.3 |         0.31 | +99.69 / −0.31   | 319.55×       |
| No     |        99.9 |        99.9  | +0.10 / −99.90   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.00    | -0.31    | -2.31196            |
| GB / N         | WEAK     | 100.00  | 0.10     | -3.9040000000000186 |
| ST / Y         | NEG      | 0.00    | -0.31    | -2.31196            |
| ST / N         | WEAK     | 100.00  | 0.10     | -3.9040000000000186 |
| MX / Y         | NEG      | 0.00    | -0.31    | -2.31196            |
| MX / N         | WEAK     | 100.00  | 0.09     | -3.9056666666666846 |
| M10 / Y        | NEG      | 0.00    | -0.31    | -2.31196            |
| M10 / N        | WEAK     | 100.00  | 0.09     | -3.9081145833333553 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | WEAK     | 2.22    | 1.91     | -2.09476            |
| DDHQ / N       | NEG      | 97.78   | -2.12    | -6.121200000000016  |

RTWH (2026-09-25): Publisher supplies no seat-count distribution; expected seats cannot price this contract.
DDHQ (2026-09-25): Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Alabama Senate race in 2026?
Contract 630628; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       99.18 |        99.21 | +0.79 / −99.21   | 0.01×         |
| No     |        4.8  |         4.98 | +95.02 / −4.98   | 19.08×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.94 |     0.73 |        -3.27 |
| GB / N         | NEG      |    0.06 |    -4.92 |        -6.98 |
| ST / Y         | WEAK     |   99.85 |     0.64 |        -3.36 |
| ST / N         | NEG      |    0.15 |    -4.83 |        -6.98 |
| MX / Y         | NEG      |   98.46 |    -0.75 |        -4.75 |
| MX / N         | NEG      |    1.54 |    -3.45 |        -6.98 |
| M10 / Y        | NEG      |   98.54 |    -0.67 |        -4.67 |
| M10 / N        | NEG      |    1.46 |    -3.52 |        -6.98 |
| RTWH / Y       | NEG      |   98.90 |    -0.31 |        -4.31 |
| RTWH / N       | NEG      |    1.10 |    -3.88 |        -6.98 |
| DDHQ / Y       | NEG      |   95.00 |    -4.21 |        -8.21 |
| DDHQ / N       | WEAK     |    5.00 |     0.02 |        -3.98 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Arkansas Senate race in 2026?
Contract 630654; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       95.31 |        95.49 | +4.51 / −95.49   | 0.05×         |
| No     |        5.9  |         6.12 | +93.88 / −6.12   | 15.33×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   99.76 |     4.27 |         0.27 |
| GB / N         | NEG      |    0.24 |    -5.88 |        -8.12 |
| ST / Y         | WEAK     |   99.21 |     3.72 |        -0.28 |
| ST / N         | NEG      |    0.79 |    -5.33 |        -8.12 |
| MX / Y         | NEG      |   93.36 |    -2.13 |        -6.13 |
| MX / N         | WEAK     |    6.64 |     0.51 |        -3.49 |
| M10 / Y        | NEG      |   94.22 |    -1.27 |        -5.27 |
| M10 / N        | NEG      |    5.78 |    -0.35 |        -4.35 |
| RTWH / Y       | WEAK     |   98.00 |     2.51 |        -1.49 |
| RTWH / N       | NEG      |    2.00 |    -4.12 |        -8.12 |
| DDHQ / Y       | WEAK     |   96.00 |     0.51 |        -3.49 |
| DDHQ / N       | NEG      |    4.00 |    -2.12 |        -6.12 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Colorado Senate race in 2026?
Contract 630667; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.94 |         3.06 | +96.94 / −3.06   | 31.70×        |
| No     |       99.62 |        99.63 | +0.37 / −99.63   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK*    |    6.02 |     2.96 |        -1.04 |
| GB / N         | NEG*     |   93.98 |    -5.65 |        -9.65 |
| ST / Y         | WEAK*    |    5.01 |     1.95 |        -2.05 |
| ST / N         | NEG*     |   94.99 |    -4.65 |        -8.65 |
| MX / Y         | GO*      |    8.30 |     5.25 |         1.25 |
| MX / N         | NEG*     |   91.70 |    -7.94 |       -11.94 |
| M10 / Y        | GO*      |    9.63 |     6.57 |         2.57 |
| M10 / N        | NEG*     |   90.37 |    -9.26 |       -13.26 |
| RTWH / Y       | NEG      |    1.50 |    -1.56 |        -5.06 |
| RTWH / N       | NEG      |   98.50 |    -1.13 |        -5.13 |
| DDHQ / Y       | NEG      |    3.00 |    -0.06 |        -4.06 |
| DDHQ / N       | NEG      |   97.00 |    -2.63 |        -6.63 |

GB, ST, MX, M10: Candidate roster is unreviewed; this assumes the modeled D/R sides match the party nominees.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Delaware Senate race in 2026?
Contract 630680; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.04 |         2.12 | +97.88 / −2.12   | 46.17×        |
| No     |       99.43 |        99.46 | +0.54 / −99.46   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG*     |    0.05 |    -2.07 |        -4.12 |
| GB / N         | WEAK*    |   99.95 |     0.49 |        -3.51 |
| ST / Y         | NEG*     |    0.38 |    -1.74 |        -4.12 |
| ST / N         | WEAK*    |   99.62 |     0.17 |        -3.83 |
| MX / Y         | NEG*     |    0.43 |    -1.69 |        -4.12 |
| MX / N         | WEAK*    |   99.57 |     0.11 |        -3.89 |
| M10 / Y        | NEG*     |    0.54 |    -1.58 |        -4.12 |
| M10 / N        | WEAK*    |   99.46 |     0.00 |        -4.00 |
| RTWH / Y       | NEG      |    2.00 |    -0.12 |        -4.12 |
| RTWH / N       | NEG      |   98.00 |    -1.46 |        -5.46 |
| DDHQ / Y       | NEG      |    1.00 |    -1.12 |        -4.12 |
| DDHQ / N       | NEG      |   99.00 |    -0.46 |        -4.46 |

GB, ST, MX, M10: Candidate roster is unreviewed; this assumes the modeled D/R sides match the party nominees.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Florida Senate race in 2026?
Contract 631045; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |
| No     |           9 |         9.33 | +90.67 / −9.33   | 9.72×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   81.55 |   -10.75 |       -14.75 |
| GB / N         | GO       |   18.45 |     9.13 |         5.13 |
| ST / Y         | NEG      |   86.97 |    -5.33 |        -9.33 |
| ST / N         | WEAK     |   13.03 |     3.71 |        -0.29 |
| MX / Y         | NEG      |   81.08 |   -11.22 |       -15.22 |
| MX / N         | GO       |   18.92 |     9.59 |         5.59 |
| M10 / Y        | NEG      |   83.14 |    -9.15 |       -13.15 |
| M10 / N        | GO       |   16.86 |     7.53 |         3.53 |
| RTWH / Y       | NEG      |   73.80 |   -18.49 |       -22.49 |
| RTWH / N       | GO       |   26.20 |    16.87 |        12.87 |
| DDHQ / Y       | NEG      |   78.00 |   -14.29 |       -18.29 |
| DDHQ / N       | GO       |   22.00 |    12.67 |         8.67 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Georgia Senate race in 2026?
Contract 630693; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        5.76 |         5.98 | +94.02 / −5.98   | 15.72×        |
| No     |       94.96 |        95.15 | +4.85 / −95.15   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO*      |   12.68 |     6.71 |         2.71 |
| GB / N         | NEG*     |   87.32 |    -7.83 |       -11.83 |
| ST / Y         | WEAK*    |    8.14 |     2.16 |        -1.84 |
| ST / N         | NEG*     |   91.86 |    -3.28 |        -7.28 |
| MX / Y         | GO*      |   11.43 |     5.45 |         1.45 |
| MX / N         | NEG*     |   88.57 |    -6.57 |       -10.57 |
| M10 / Y        | GO*      |   12.09 |     6.11 |         2.11 |
| M10 / N        | NEG*     |   87.91 |    -7.24 |       -11.24 |
| RTWH / Y       | NEG      |    5.60 |    -0.38 |        -4.38 |
| RTWH / N       | NEG      |   94.40 |    -0.75 |        -4.75 |
| DDHQ / Y       | GO       |   13.00 |     7.02 |         3.02 |
| DDHQ / N       | NEG      |   87.00 |    -8.15 |       -12.15 |

GB, ST, MX, M10: Runoff transfers and turnout are not separately modeled; the modeled margin is used as a proxy for the eventual winner.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Idaho Senate race in 2026?
Contract 630706; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       92.72 |        92.99 | +7.01 / −92.99   | 0.08×         |
| No     |        8.86 |         9.18 | +90.82 / −9.18   | 9.89×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO*      |   99.95 |     6.95 |         2.95 |
| GB / N         | NEG*     |    0.05 |    -9.13 |       -11.18 |
| ST / Y         | GO*      |   99.68 |     6.69 |         2.69 |
| ST / N         | NEG*     |    0.32 |    -8.86 |       -11.18 |
| MX / Y         | GO*      |   99.76 |     6.77 |         2.77 |
| MX / N         | NEG*     |    0.24 |    -8.94 |       -11.18 |
| M10 / Y        | GO*      |   99.61 |     6.62 |         2.62 |
| M10 / N        | NEG*     |    0.39 |    -8.79 |       -11.18 |
| RTWH / Y       | WEAK     |   95.80 |     2.81 |        -1.19 |
| RTWH / N       | NEG      |    4.20 |    -4.98 |        -8.98 |
| DDHQ / Y       | GO       |   97.00 |     4.01 |         0.01 |
| DDHQ / N       | NEG      |    3.00 |    -6.18 |       -10.18 |

GB, ST, MX, M10: The strongest D/Independent-versus-R margin approximates the winning side; third-candidate outcomes are not jointly modeled. Independents remain IND.
RTWH (2026-09-25): Achilles retains IND despite publisher column. Publisher omits separate probabilities for reviewed contenders: Natalie Fleming. Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Publisher omits separate probabilities for reviewed contenders: Natalie Fleming. Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Illinois Senate race in 2026?
Contract 630721; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.67 |         2.78 | +97.22 / −2.78   | 34.98×        |
| No     |       98.66 |        98.71 | +1.29 / −98.71   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG*     |    0.26 |    -2.52 |        -4.78 |
| GB / N         | WEAK*    |   99.74 |     1.03 |        -2.97 |
| ST / Y         | NEG*     |    0.72 |    -2.06 |        -4.78 |
| ST / N         | WEAK*    |   99.28 |     0.57 |        -3.43 |
| MX / Y         | NEG*     |    1.82 |    -0.96 |        -4.78 |
| MX / N         | NEG*     |   98.18 |    -0.53 |        -4.53 |
| M10 / Y        | NEG*     |    2.03 |    -0.75 |        -4.75 |
| M10 / N        | NEG*     |   97.97 |    -0.74 |        -4.74 |
| RTWH / Y       | NEG      |    2.50 |    -0.28 |        -4.28 |
| RTWH / N       | NEG      |   97.50 |    -1.21 |        -5.21 |
| DDHQ / Y       | WEAK     |    4.00 |     1.22 |        -2.78 |
| DDHQ / N       | NEG      |   96.00 |    -2.71 |        -6.71 |

GB, ST, MX, M10: Candidate roster is unreviewed; this assumes the modeled D/R sides match the party nominees.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Iowa Senate race in 2026?
Contract 630734; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          57 |        57.98 | +42.02 / −57.98  | 0.72×         |
| No     |          44 |        44.99 | +55.01 / −44.99  | 1.22×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   63.82 |     5.84 |         1.84 |
| GB / N         | NEG      |   36.18 |    -8.81 |       -12.81 |
| ST / Y         | GO       |   66.56 |     8.58 |         4.58 |
| ST / N         | NEG      |   33.44 |   -11.55 |       -15.55 |
| MX / Y         | GO       |   63.08 |     5.10 |         1.10 |
| MX / N         | NEG      |   36.92 |    -8.06 |       -12.06 |
| M10 / Y        | GO       |   64.68 |     6.70 |         2.70 |
| M10 / N        | NEG      |   35.32 |    -9.67 |       -13.67 |
| RTWH / Y       | NEG      |   41.10 |   -16.88 |       -20.88 |
| RTWH / N       | GO       |   58.90 |    13.91 |         9.91 |
| DDHQ / Y       | NEG      |   51.00 |    -6.98 |       -10.98 |
| DDHQ / N       | GO       |   49.00 |     4.01 |         0.01 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Kansas Senate race in 2026?
Contract 630747; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          70 |        70.84 | +29.16 / −70.84  | 0.41×         |
| No     |          31 |        31.86 | +68.14 / −31.86  | 2.14×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   90.72 |    19.88 |        15.88 |
| GB / N         | NEG      |    9.28 |   -22.57 |       -26.57 |
| ST / Y         | GO       |   91.52 |    20.68 |        16.68 |
| ST / N         | NEG      |    8.48 |   -23.37 |       -27.37 |
| MX / Y         | GO       |   89.39 |    18.55 |        14.55 |
| MX / N         | NEG      |   10.61 |   -21.25 |       -25.25 |
| M10 / Y        | GO       |   88.13 |    17.29 |        13.29 |
| M10 / N        | NEG      |   11.87 |   -19.99 |       -23.99 |
| RTWH / Y       | NEG      |   63.20 |    -7.64 |       -11.64 |
| RTWH / N       | GO       |   36.80 |     4.94 |         0.94 |
| DDHQ / Y       | GO       |   77.00 |     6.16 |         2.16 |
| DDHQ / N       | NEG      |   23.00 |    -8.86 |       -12.86 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Kentucky Senate race in 2026?
Contract 630760; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        96.5 |        96.64 | +3.36 / −96.64   | 0.03×         |
| No     |         4.7 |         4.88 | +95.12 / −4.88   | 19.50×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   98.12 |     1.48 |        -2.52 |
| GB / N         | NEG      |    1.88 |    -3.00 |        -6.88 |
| ST / Y         | WEAK     |   98.58 |     1.94 |        -2.06 |
| ST / N         | NEG      |    1.42 |    -3.46 |        -6.88 |
| MX / Y         | NEG      |   96.10 |    -0.53 |        -4.53 |
| MX / N         | NEG      |    3.90 |    -0.98 |        -4.98 |
| M10 / Y        | WEAK     |   97.04 |     0.41 |        -3.59 |
| M10 / N        | NEG      |    2.96 |    -1.92 |        -5.92 |
| RTWH / Y       | WEAK     |   97.90 |     1.26 |        -2.74 |
| RTWH / N       | NEG      |    2.10 |    -2.78 |        -6.78 |
| DDHQ / Y       | NEG      |   95.00 |    -1.64 |        -5.64 |
| DDHQ / N       | WEAK     |    5.00 |     0.12 |        -3.88 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Louisiana Senate race in 2026?
Contract 634879; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          94 |        94.23 | +5.77 / −94.23   | 0.06×         |
| No     |           7 |         7.26 | +92.74 / −7.26   | 12.77×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   94.90 |     0.67 |        -3.33 |
| GB / N         | NEG      |    5.10 |    -2.16 |        -6.16 |
| ST / Y         | WEAK     |   95.74 |     1.52 |        -2.48 |
| ST / N         | NEG      |    4.26 |    -3.00 |        -7.00 |
| MX / Y         | NEG      |   89.47 |    -4.76 |        -8.76 |
| MX / N         | WEAK     |   10.53 |     3.27 |        -0.73 |
| M10 / Y        | NEG      |   89.24 |    -4.98 |        -8.98 |
| M10 / N        | WEAK     |   10.76 |     3.50 |        -0.50 |
| RTWH / Y       | NEG      |   89.20 |    -5.03 |        -9.03 |
| RTWH / N       | WEAK     |   10.80 |     3.54 |        -0.46 |
| DDHQ / Y       | NEG      |   89.00 |    -5.23 |        -9.23 |
| DDHQ / N       | WEAK     |   11.00 |     3.74 |        -0.26 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Maine Senate race in 2026?
Contract 630773; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          33 |        33.88 | +66.12 / −33.88  | 1.95×         |
| No     |          68 |        68.87 | +31.13 / −68.87  | 0.45×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG*     |    7.45 |   -26.44 |       -30.44 |
| GB / N         | GO*      |   92.55 |    23.68 |        19.68 |
| ST / Y         | NEG*     |    6.37 |   -27.52 |       -31.52 |
| ST / N         | GO*      |   93.63 |    24.76 |        20.76 |
| MX / Y         | NEG*     |   14.46 |   -19.43 |       -23.43 |
| MX / N         | GO*      |   85.54 |    16.67 |        12.67 |
| M10 / Y        | NEG*     |   17.06 |   -16.83 |       -20.83 |
| M10 / N        | GO*      |   82.94 |    14.07 |        10.07 |
| RTWH / Y       | WEAK     |   37.80 |     3.92 |        -0.08 |
| RTWH / N       | NEG      |   62.20 |    -6.67 |       -10.67 |
| DDHQ / Y       | GO       |   46.00 |    12.12 |         8.12 |
| DDHQ / N       | NEG      |   54.00 |   -14.87 |       -18.87 |

GB, ST, MX, M10: Ranked-choice transfers are not separately modeled; the modeled margin is used as a proxy for the eventual winner.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Massachusetts Senate race in 2026?
Contract 630791; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.6  |         2.7  | +97.30 / −2.70   | 36.02×        |
| No     |       98.91 |        98.95 | +1.05 / −98.95   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.00 |    -2.70 |        -4.70 |
| GB / N         | WEAK     |  100.00 |     1.05 |        -2.95 |
| ST / Y         | NEG      |    0.00 |    -2.70 |        -4.70 |
| ST / N         | WEAK     |  100.00 |     1.04 |        -2.96 |
| MX / Y         | NEG      |    0.01 |    -2.69 |        -4.70 |
| MX / N         | WEAK     |   99.99 |     1.04 |        -2.96 |
| M10 / Y        | NEG      |    0.01 |    -2.69 |        -4.70 |
| M10 / N        | WEAK     |   99.99 |     1.04 |        -2.96 |
| RTWH / Y       | NEG      |    0.40 |    -2.30 |        -4.70 |
| RTWH / N       | WEAK     |   99.60 |     0.65 |        -3.35 |
| DDHQ / Y       | NEG      |    1.00 |    -1.70 |        -4.70 |
| DDHQ / N       | WEAK     |   99.00 |     0.05 |        -3.95 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Michigan Senate race in 2026?
Contract 630806; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          29 |        29.82 | +70.18 / −29.82  | 2.35×         |
| No     |          72 |        72.81 | +27.19 / −72.81  | 0.37×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   16.55 |   -13.27 |       -17.27 |
| GB / N         | GO       |   83.45 |    10.64 |         6.64 |
| ST / Y         | NEG      |   11.83 |   -17.99 |       -21.99 |
| ST / N         | GO       |   88.17 |    15.36 |        11.36 |
| MX / Y         | NEG      |   16.83 |   -12.99 |       -16.99 |
| MX / N         | GO       |   83.17 |    10.36 |         6.36 |
| M10 / Y        | NEG      |   20.93 |    -8.90 |       -12.90 |
| M10 / N        | GO       |   79.07 |     6.27 |         2.27 |
| RTWH / Y       | NEG      |   17.90 |   -11.92 |       -15.92 |
| RTWH / N       | GO       |   82.10 |     9.29 |         5.29 |
| DDHQ / Y       | WEAK     |   30.00 |     0.18 |        -3.82 |
| DDHQ / N       | NEG      |   70.00 |    -2.81 |        -6.81 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Minnesota Senate race in 2026?
Contract 630819; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           9 |         9.33 | +90.67 / −9.33   | 9.72×         |
| No     |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   15.20 |     5.87 |         1.87 |
| GB / N         | NEG      |   84.80 |    -7.49 |       -11.49 |
| ST / Y         | WEAK     |   13.13 |     3.80 |        -0.20 |
| ST / N         | NEG      |   86.87 |    -5.43 |        -9.43 |
| MX / Y         | WEAK     |   12.68 |     3.35 |        -0.65 |
| MX / N         | NEG      |   87.32 |    -4.97 |        -8.97 |
| M10 / Y        | GO       |   13.97 |     4.64 |         0.64 |
| M10 / N        | NEG      |   86.03 |    -6.26 |       -10.26 |
| RTWH / Y       | GO       |   15.20 |     5.87 |         1.87 |
| RTWH / N       | NEG      |   84.80 |    -7.49 |       -11.49 |
| DDHQ / Y       | WEAK     |   13.00 |     3.67 |        -0.33 |
| DDHQ / N       | NEG      |   87.00 |    -5.29 |        -9.29 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Mississippi Senate race in 2026?
Contract 631018; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          93 |        93.26 | +6.74 / −93.26   | 0.07×         |
| No     |           9 |         9.33 | +90.67 / −9.33   | 9.72×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   96.79 |     3.53 |        -0.47 |
| GB / N         | NEG      |    3.21 |    -6.12 |       -10.12 |
| ST / Y         | GO       |   97.49 |     4.23 |         0.23 |
| ST / N         | NEG      |    2.51 |    -6.82 |       -10.82 |
| MX / Y         | WEAK     |   93.70 |     0.44 |        -3.56 |
| MX / N         | NEG      |    6.30 |    -3.03 |        -7.03 |
| M10 / Y        | NEG      |   92.47 |    -0.79 |        -4.79 |
| M10 / N        | NEG      |    7.53 |    -1.80 |        -5.80 |
| RTWH / Y       | NEG      |   86.90 |    -6.36 |       -10.36 |
| RTWH / N       | WEAK     |   13.10 |     3.77 |        -0.23 |
| DDHQ / Y       | NEG      |   93.00 |    -0.26 |        -4.26 |
| DDHQ / N       | NEG      |    7.00 |    -2.33 |        -6.33 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Montana Senate race in 2026?
Contract 630832; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          91 |        91.33 | +8.67 / −91.33   | 0.09×         |
| No     |          11 |        11.39 | +88.61 / −11.39  | 7.78×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO*      |   97.05 |     5.72 |         1.72 |
| GB / N         | NEG*     |    2.95 |    -8.44 |       -12.44 |
| ST / Y         | GO*      |   98.18 |     6.85 |         2.85 |
| ST / N         | NEG*     |    1.82 |    -9.57 |       -13.39 |
| MX / Y         | GO*      |   97.96 |     6.63 |         2.63 |
| MX / N         | NEG*     |    2.04 |    -9.35 |       -13.35 |
| M10 / Y        | GO*      |   98.46 |     7.14 |         3.14 |
| M10 / N        | NEG*     |    1.54 |    -9.85 |       -13.39 |
| RTWH / Y       | NEG      |   77.90 |   -13.43 |       -17.43 |
| RTWH / N       | GO       |   22.10 |    10.71 |         6.71 |
| DDHQ / Y       | NEG      |   90.00 |    -1.33 |        -5.33 |
| DDHQ / N       | NEG      |   10.00 |    -1.39 |        -5.39 |

GB, ST, MX, M10: The strongest D/Independent-versus-R margin approximates the winning side; third-candidate outcomes are not jointly modeled. Independents remain IND.
RTWH (2026-09-25): Publisher omits separate probabilities for reviewed contenders: Alani Bankhead. Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Publisher omits separate probabilities for reviewed contenders: Alani Bankhead. Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Nebraska Senate race in 2026?
Contract 634892; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        70.5 |        71.33 | +28.67 / −71.33  | 0.40×         |
| No     |        31   |        31.86 | +68.14 / −31.86  | 2.14×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO*      |   83.07 |    11.74 |         7.74 |
| GB / N         | NEG*     |   16.93 |   -14.93 |       -18.93 |
| ST / Y         | GO*      |   80.69 |     9.36 |         5.36 |
| ST / N         | NEG*     |   19.31 |   -12.54 |       -16.54 |
| MX / Y         | NEG*     |   70.34 |    -1.00 |        -5.00 |
| MX / N         | NEG*     |   29.66 |    -2.19 |        -6.19 |
| M10 / Y        | NEG*     |   70.22 |    -1.11 |        -5.11 |
| M10 / N        | NEG*     |   29.78 |    -2.08 |        -6.08 |
| RTWH / Y       | NEG      |   64.00 |    -7.33 |       -11.33 |
| RTWH / N       | GO       |   36.00 |     4.14 |         0.14 |
| DDHQ / Y       | GO       |   83.00 |    11.67 |         7.67 |
| DDHQ / N       | NEG      |   17.00 |   -14.86 |       -18.86 |

GB, ST, MX, M10: The strongest D/Independent-versus-R margin approximates the winning side; third-candidate outcomes are not jointly modeled. Independents remain IND.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the New Hampshire Senate race in 2026?
Contract 630845; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          16 |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |          85 |        85.51 | +14.49 / −85.51  | 0.17×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    2.07 |   -14.46 |       -18.46 |
| GB / N         | GO       |   97.93 |    12.42 |         8.42 |
| ST / Y         | NEG      |    2.42 |   -14.12 |       -18.12 |
| ST / N         | GO       |   97.58 |    12.07 |         8.07 |
| MX / Y         | NEG      |    7.23 |    -9.31 |       -13.31 |
| MX / N         | GO       |   92.77 |     7.26 |         3.26 |
| M10 / Y        | NEG      |    6.12 |   -10.42 |       -14.42 |
| M10 / N        | GO       |   93.88 |     8.37 |         4.37 |
| RTWH / Y       | NEG      |   13.80 |    -2.74 |        -6.74 |
| RTWH / N       | WEAK     |   86.20 |     0.69 |        -3.31 |
| DDHQ / Y       | WEAK     |   19.00 |     2.46 |        -1.54 |
| DDHQ / N       | NEG      |   81.00 |    -4.51 |        -8.51 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the New Jersey Senate race in 2026?
Contract 630858; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        3.61 |         3.75 | +96.25 / −3.75   | 25.65×        |
| No     |       99.22 |        99.25 | +0.75 / −99.25   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG*     |    0.22 |    -3.53 |        -5.75 |
| GB / N         | WEAK*    |   99.78 |     0.53 |        -3.47 |
| ST / Y         | NEG*     |    0.76 |    -2.99 |        -5.75 |
| ST / N         | NEG*     |   99.24 |    -0.01 |        -4.01 |
| MX / Y         | NEG*     |    0.35 |    -3.40 |        -5.75 |
| MX / N         | WEAK*    |   99.65 |     0.40 |        -3.60 |
| M10 / Y        | NEG*     |    0.44 |    -3.31 |        -5.75 |
| M10 / N        | WEAK*    |   99.56 |     0.31 |        -3.69 |
| RTWH / Y       | NEG      |    2.90 |    -0.85 |        -4.85 |
| RTWH / N       | NEG      |   97.10 |    -2.15 |        -6.15 |
| DDHQ / Y       | WEAK     |    4.00 |     0.25 |        -3.75 |
| DDHQ / N       | NEG      |   96.00 |    -3.25 |        -7.25 |

GB, ST, MX, M10: Candidate roster is unreviewed; this assumes the modeled D/R sides match the party nominees.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the New Mexico Senate race in 2026?
Contract 630871; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        3.21 |         3.34 | +96.66 / −3.34   | 28.95×        |
| No     |       99.17 |        99.2  | +0.80 / −99.20   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.90 |    -1.44 |        -5.34 |
| GB / N         | NEG      |   98.10 |    -1.10 |        -5.10 |
| ST / Y         | NEG      |    0.93 |    -2.40 |        -5.34 |
| ST / N         | NEG      |   99.07 |    -0.13 |        -4.13 |
| MX / Y         | NEG      |    1.81 |    -1.53 |        -5.34 |
| MX / N         | NEG      |   98.19 |    -1.01 |        -5.01 |
| M10 / Y        | NEG      |    1.85 |    -1.49 |        -5.34 |
| M10 / N        | NEG      |   98.15 |    -1.05 |        -5.05 |
| RTWH / Y       | NEG      |    0.70 |    -2.64 |        -5.34 |
| RTWH / N       | WEAK     |   99.30 |     0.10 |        -3.90 |
| DDHQ / Y       | WEAK     |    4.00 |     0.66 |        -3.34 |
| DDHQ / N       | NEG      |   96.00 |    -3.20 |        -7.20 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the North Carolina Senate race in 2026?
Contract 630884; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           7 |         7.26 | +92.74 / −7.26   | 12.77×        |
| No     |          94 |        94.23 | +5.77 / −94.23   | 0.06×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   14.23 |     6.97 |         2.97 |
| GB / N         | NEG      |   85.77 |    -8.45 |       -12.45 |
| ST / Y         | WEAK     |    9.36 |     2.10 |        -1.90 |
| ST / N         | NEG      |   90.64 |    -3.58 |        -7.58 |
| MX / Y         | GO       |   11.89 |     4.63 |         0.63 |
| MX / N         | NEG      |   88.11 |    -6.12 |       -10.12 |
| M10 / Y        | GO       |   11.97 |     4.71 |         0.71 |
| M10 / N        | NEG      |   88.03 |    -6.19 |       -10.19 |
| RTWH / Y       | WEAK     |   10.20 |     2.94 |        -1.06 |
| RTWH / N       | NEG      |   89.80 |    -4.43 |        -8.43 |
| DDHQ / Y       | GO       |   19.00 |    11.74 |         7.74 |
| DDHQ / N       | NEG      |   81.00 |   -13.23 |       -17.23 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Ohio Senate race in 2026?
Contract 631058; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          41 |        41.97 | +58.03 / −41.97  | 1.38×         |
| No     |          60 |        60.96 | +39.04 / −60.96  | 0.64×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   29.66 |   -12.31 |       -16.31 |
| GB / N         | GO       |   70.34 |     9.38 |         5.38 |
| ST / Y         | NEG      |   24.94 |   -17.03 |       -21.03 |
| ST / N         | GO       |   75.06 |    14.10 |        10.10 |
| MX / Y         | NEG      |   30.82 |   -11.15 |       -15.15 |
| MX / N         | GO       |   69.18 |     8.22 |         4.22 |
| M10 / Y        | NEG      |   34.97 |    -7.00 |       -11.00 |
| M10 / N        | GO       |   65.03 |     4.07 |         0.07 |
| RTWH / Y       | NEG      |   25.60 |   -16.37 |       -20.37 |
| RTWH / N       | GO       |   74.40 |    13.44 |         9.44 |
| DDHQ / Y       | GO       |   49.00 |     7.03 |         3.03 |
| DDHQ / N       | NEG      |   51.00 |    -9.96 |       -13.96 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Oklahoma Senate race in 2026?
Contract 631031; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       98.14 |        98.21 | +1.79 / −98.21   | 0.02×         |
| No     |        2.7  |         2.81 | +97.19 / −2.81   | 34.65×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.99 |     1.78 |        -2.22 |
| GB / N         | NEG      |    0.01 |    -2.80 |        -4.81 |
| ST / Y         | WEAK     |   99.99 |     1.78 |        -2.22 |
| ST / N         | NEG      |    0.01 |    -2.80 |        -4.81 |
| MX / Y         | WEAK     |   99.94 |     1.73 |        -2.27 |
| MX / N         | NEG      |    0.06 |    -2.75 |        -4.81 |
| M10 / Y        | WEAK     |   99.96 |     1.74 |        -2.26 |
| M10 / N        | NEG      |    0.04 |    -2.76 |        -4.81 |
| RTWH / Y       | WEAK     |   99.20 |     0.99 |        -3.01 |
| RTWH / N       | NEG      |    0.80 |    -2.01 |        -4.81 |
| DDHQ / Y       | WEAK     |   99.00 |     0.79 |        -3.21 |
| DDHQ / N       | NEG      |    1.00 |    -1.81 |        -4.81 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Oregon Senate race in 2026?
Contract 630899; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         2.4 |         2.49 | +97.51 / −2.49   | 39.10×        |
| No     |        98.2 |        98.27 | +1.73 / −98.27   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG*     |    0.07 |    -2.42 |        -4.49 |
| GB / N         | WEAK*    |   99.93 |     1.65 |        -2.35 |
| ST / Y         | NEG*     |    0.35 |    -2.14 |        -4.49 |
| ST / N         | WEAK*    |   99.65 |     1.38 |        -2.62 |
| MX / Y         | NEG*     |    0.67 |    -1.83 |        -4.49 |
| MX / N         | WEAK*    |   99.33 |     1.06 |        -2.94 |
| M10 / Y        | NEG*     |    0.92 |    -1.57 |        -4.49 |
| M10 / N        | WEAK*    |   99.08 |     0.81 |        -3.19 |
| RTWH / Y       | NEG      |    2.10 |    -0.39 |        -4.39 |
| RTWH / N       | NEG      |   97.90 |    -0.37 |        -4.37 |
| DDHQ / Y       | NEG      |    1.00 |    -1.49 |        -4.49 |
| DDHQ / N       | WEAK     |   99.00 |     0.73 |        -3.27 |

GB, ST, MX, M10: Candidate roster is unreviewed; this assumes the modeled D/R sides match the party nominees.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Rhode Island Senate race in 2026?
Contract 630912; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.23 |         2.32 | +97.68 / −2.32   | 42.16×        |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.01 |    -2.31 |        -4.32 |
| GB / N         | WEAK     |   99.99 |     0.38 |        -3.62 |
| ST / Y         | NEG      |    0.01 |    -2.31 |        -4.32 |
| ST / N         | WEAK     |   99.99 |     0.37 |        -3.63 |
| MX / Y         | NEG      |    0.15 |    -2.17 |        -4.32 |
| MX / N         | WEAK     |   99.85 |     0.24 |        -3.76 |
| M10 / Y        | NEG      |    0.18 |    -2.13 |        -4.32 |
| M10 / N        | WEAK     |   99.82 |     0.20 |        -3.80 |
| RTWH / Y       | NEG      |    1.10 |    -1.22 |        -4.32 |
| RTWH / N       | NEG      |   98.90 |    -0.72 |        -4.72 |
| DDHQ / Y       | NEG      |    1.00 |    -1.32 |        -4.32 |
| DDHQ / N       | NEG      |   99.00 |    -0.62 |        -4.62 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the South Carolina Senate race in 2026?
Contract 630925; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          87 |        87.45 | +12.55 / −87.45  | 0.14×         |
| No     |          14 |        14.48 | +85.52 / −14.48  | 5.91×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   95.30 |     7.85 |         3.85 |
| GB / N         | NEG      |    4.70 |    -9.78 |       -13.78 |
| ST / Y         | GO       |   96.22 |     8.77 |         4.77 |
| ST / N         | NEG      |    3.78 |   -10.70 |       -14.70 |
| MX / Y         | GO       |   91.79 |     4.33 |         0.33 |
| MX / N         | NEG      |    8.21 |    -6.27 |       -10.27 |
| M10 / Y        | GO       |   92.69 |     5.24 |         1.24 |
| M10 / N        | NEG      |    7.31 |    -7.17 |       -11.17 |
| RTWH / Y       | NEG      |   79.70 |    -7.75 |       -11.75 |
| RTWH / N       | GO       |   20.30 |     5.82 |         1.82 |
| DDHQ / Y       | NEG      |   73.00 |   -14.45 |       -18.45 |
| DDHQ / N       | GO       |   27.00 |    12.52 |         8.52 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the South Dakota Senate race in 2026?
Contract 630938; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       94.3  |        94.52 | +5.48 / −94.52   | 0.06×         |
| No     |        6.37 |         6.6  | +93.40 / −6.60   | 14.14×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO*      |   99.94 |     5.42 |         1.42 |
| GB / N         | NEG*     |    0.06 |    -6.54 |        -8.60 |
| ST / Y         | GO*      |   99.18 |     4.66 |         0.66 |
| ST / N         | NEG*     |    0.82 |    -5.78 |        -8.60 |
| MX / Y         | NEG*     |   91.88 |    -2.64 |        -6.64 |
| MX / N         | WEAK*    |    8.12 |     1.52 |        -2.48 |
| M10 / Y        | NEG*     |   92.85 |    -1.66 |        -5.66 |
| M10 / N        | WEAK*    |    7.15 |     0.55 |        -3.45 |
| RTWH / Y       | NEG      |   87.10 |    -7.42 |       -11.42 |
| RTWH / N       | GO       |   12.90 |     6.30 |         2.30 |
| DDHQ / Y       | WEAK     |   97.00 |     2.48 |        -1.52 |
| DDHQ / N       | NEG      |    3.00 |    -3.60 |        -7.60 |

GB, ST, MX, M10: The strongest D/Independent-versus-R margin approximates the winning side; third-candidate outcomes are not jointly modeled. Independents remain IND.
RTWH (2026-09-25): Bengs retains IND despite publisher column. Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Tennessee Senate race in 2026?
Contract 630951; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        97.2 |        97.31 | +2.69 / −97.31   | 0.03×         |
| No     |         3.8 |         3.95 | +96.05 / −3.95   | 24.34×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.97 |     2.66 |        -1.34 |
| GB / N         | NEG      |    0.03 |    -3.92 |        -5.95 |
| ST / Y         | WEAK     |   99.98 |     2.67 |        -1.33 |
| ST / N         | NEG      |    0.02 |    -3.92 |        -5.95 |
| MX / Y         | WEAK     |   99.92 |     2.61 |        -1.39 |
| MX / N         | NEG      |    0.08 |    -3.87 |        -5.95 |
| M10 / Y        | WEAK     |   99.95 |     2.64 |        -1.36 |
| M10 / N        | NEG      |    0.05 |    -3.90 |        -5.95 |
| RTWH / Y       | WEAK     |   99.00 |     1.69 |        -2.31 |
| RTWH / N       | NEG      |    1.00 |    -2.95 |        -5.95 |
| DDHQ / Y       | NEG      |   97.00 |    -0.31 |        -4.31 |
| DDHQ / N       | NEG      |    3.00 |    -0.95 |        -4.95 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Texas Senate race in 2026?
Contract 630964; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          40 |        40.96 | +59.04 / −40.96  | 1.44×         |
| No     |          61 |        61.95 | +38.05 / −61.95  | 0.61×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   43.28 |     2.32 |        -1.68 |
| GB / N         | NEG      |   56.72 |    -5.23 |        -9.23 |
| ST / Y         | WEAK     |   42.11 |     1.15 |        -2.85 |
| ST / N         | NEG      |   57.89 |    -4.06 |        -8.06 |
| MX / Y         | GO       |   45.09 |     4.13 |         0.13 |
| MX / N         | NEG      |   54.91 |    -7.04 |       -11.04 |
| M10 / Y        | WEAK     |   44.71 |     3.75 |        -0.25 |
| M10 / N        | NEG      |   55.29 |    -6.66 |       -10.66 |
| RTWH / Y       | NEG      |   22.50 |   -18.46 |       -22.46 |
| RTWH / N       | GO       |   77.50 |    15.55 |        11.55 |
| DDHQ / Y       | WEAK     |   44.00 |     3.04 |        -0.96 |
| DDHQ / N       | NEG      |   56.00 |    -5.95 |        -9.95 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Virginia Senate race in 2026?
Contract 630977; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.71 |         2.82 | +97.18 / −2.82   | 34.46×        |
| No     |       99.7  |        99.71 | +0.29 / −99.71   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.57 |    -2.25 |        -4.82 |
| GB / N         | NEG      |   99.43 |    -0.28 |        -4.28 |
| ST / Y         | NEG      |    0.59 |    -2.23 |        -4.82 |
| ST / N         | NEG      |   99.41 |    -0.30 |        -4.30 |
| MX / Y         | NEG      |    1.52 |    -1.30 |        -4.82 |
| MX / N         | NEG      |   98.48 |    -1.23 |        -5.23 |
| M10 / Y        | NEG      |    1.48 |    -1.34 |        -4.82 |
| M10 / N        | NEG      |   98.52 |    -1.19 |        -5.19 |
| RTWH / Y       | NEG      |    1.90 |    -0.92 |        -4.82 |
| RTWH / N       | NEG      |   98.10 |    -1.61 |        -5.61 |
| DDHQ / Y       | WEAK     |    4.00 |     1.18 |        -2.82 |
| DDHQ / N       | NEG      |   96.00 |    -3.71 |        -7.71 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Wyoming Senate race in 2026?
Contract 631003; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        97   |        97.12 | +2.88 / −97.12   | 0.03×         |
| No     |         3.1 |         3.22 | +96.78 / −3.22   | 30.05×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK*    |  100.00 |     2.88 |        -1.12 |
| GB / N         | NEG*     |    0.00 |    -3.22 |        -5.22 |
| ST / Y         | WEAK*    |   99.97 |     2.86 |        -1.14 |
| ST / N         | NEG*     |    0.03 |    -3.19 |        -5.22 |
| MX / Y         | WEAK*    |   99.94 |     2.82 |        -1.18 |
| MX / N         | NEG*     |    0.06 |    -3.16 |        -5.22 |
| M10 / Y        | WEAK*    |   99.93 |     2.82 |        -1.18 |
| M10 / N        | NEG*     |    0.07 |    -3.15 |        -5.22 |
| RTWH / Y       | WEAK     |   98.80 |     1.68 |        -2.32 |
| RTWH / N       | NEG      |    1.20 |    -2.02 |        -5.22 |
| DDHQ / Y       | WEAK     |   99.00 |     1.88 |        -2.12 |
| DDHQ / N       | NEG      |    1.00 |    -2.22 |        -5.22 |

GB, ST, MX, M10: Candidate roster is unreviewed; this assumes the modeled D/R sides match the party nominees.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

