# All model-market pairs grouped by market

Y = buy Yes; N = buy No. P = model probability that the selected side pays $1 under the contract condition; it is not confidence that the model is correct. EV = base expected net profit after purchase depth and estimated fees. Budget and win/loss payoffs use those base costs. Stress adds the extra friction scenario and applies the probability haircut to the model probability. GO (green) survives stress; WEAK (amber) is positive before stress only; UNC (amber) is unresolved; NEG (red) is negative in expectation; N/A (gray) is unavailable. A status marked * uses a conditional settlement proxy: its P, EV and stress depend on the stated runoff, ranked-choice or candidate assumptions. Color follows the assessment even with a star; the star separately flags the settlement assumption. Local P comes from the full predictive distribution. External P is a published point estimate or seat-histogram probability; equal endpoints are not a confidence interval. Simulation estimates have sampling error. All model rows are independent comparisons; there is no combined score.

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
| Yes    |       11.09 |        11.48 | +88.52 / −11.48  | 7.71×         |
| No     |       90.93 |        91.26 | +8.74 / −91.26   | 0.10×         |

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
| RTWH / Y       | NEG      | 4.20    | -7.28    | -11.284399999999998 |
| RTWH / N       | GO       | 95.80   | 4.54     | 0.5407599999999846  |
| DDHQ / Y       | NEG      | 3.00    | -8.48    | -12.484399999999999 |
| DDHQ / N       | GO       | 97.00   | 5.74     | 1.7407599999999857  |

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
| Yes    |       23.51 |        24.22 | +75.78 / −24.22  | 3.13×         |
| No     |       81    |        81.62 | +18.38 / −81.62  | 0.23×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 16.65   | -7.57    | -11.572223140444718 |
| GB / N         | WEAK     | 83.35   | 1.74     | -2.2610868595552835 |
| ST / Y         | NEG      | 18.59   | -5.63    | -9.630209999999998  |
| ST / N         | NEG      | 81.41   | -0.20    | -4.2031000000000045 |
| MX / Y         | NEG      | 17.54   | -6.68    | -10.681564166666668 |
| MX / N         | WEAK     | 82.46   | 0.85     | -3.151745833333342  |
| M10 / Y        | NEG      | 17.04   | -7.17    | -11.174376666666666 |
| M10 / N        | WEAK     | 82.96   | 1.34     | -2.6589333333333354 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 0%-10%?
Contract 3343809; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         1   |         1.04 | +98.96 / −1.04   | 95.19×        |
| No     |        99.4 |        99.42 | +0.58 / −99.42   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.23    | -0.81    | -3.0396000000000005 |
| GB / N         | WEAK     | 99.77   | 0.34     | -3.6564655114206928 |
| ST / Y         | NEG      | 0.28    | -0.76    | -3.0396000000000005 |
| ST / N         | WEAK     | 99.72   | 0.29     | -3.7051100000000114 |
| MX / Y         | NEG      | 0.53    | -0.51    | -3.0396000000000005 |
| MX / N         | WEAK     | 99.47   | 0.05     | -3.9531308333333404 |
| M10 / Y        | NEG      | 0.77    | -0.27    | -3.0396000000000005 |
| M10 / N        | NEG      | 99.23   | -0.19    | -4.19125583333334   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 10%-15%?
Contract 3343810; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         2   |         2.08 | +97.92 / −2.08   | 47.11×        |
| No     |        98.7 |        98.75 | +1.25 / −98.75   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 2.20    | 0.12     | -3.8792953803983723 |
| GB / N         | NEG      | 97.80   | -0.95    | -4.950424619601634  |
| ST / Y         | NEG      | 1.72    | -0.36    | -4.0784             |
| ST / N         | NEG      | 98.28   | -0.47    | -4.473194999999997  |
| MX / Y         | WEAK     | 2.98    | 0.90     | -3.0950145833333336 |
| MX / N         | NEG      | 97.02   | -1.73    | -5.734705416666664  |
| M10 / Y        | WEAK     | 4.05    | 1.97     | -2.0302750000000005 |
| M10 / N        | NEG      | 95.95   | -2.80    | -6.799445000000004  |
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
| Yes    |       14    |        14.48 | +85.52 / −14.48  | 5.91×         |
| No     |       89.28 |        89.67 | +10.33 / −89.67  | 0.12×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 26.64   | 12.16    | 8.160535398573735   |
| GB / N         | NEG      | 73.36   | -16.31   | -20.30863539857376  |
| ST / Y         | GO       | 26.03   | 11.55    | 7.549649999999999   |
| ST / N         | NEG      | 73.97   | -15.70   | -19.697750000000013 |
| MX / Y         | GO       | 27.23   | 12.75    | 8.749806249999997   |
| MX / N         | NEG      | 72.77   | -16.90   | -20.89790625000002  |
| M10 / Y        | GO       | 29.69   | 15.21    | 11.211368749999998  |
| M10 / N        | NEG      | 70.31   | -19.36   | -23.359468750000023 |
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

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 45% or more?
Contract 3343817; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         6.9 |         7.16 | +92.84 / −7.16   | 12.97×        |
| No     |        97   |        97.12 | +2.88 / −97.12   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.07    | -7.08    | -9.15692            |
| GB / N         | WEAK     | 99.93   | 2.81     | -1.1908811582839296 |
| ST / Y         | NEG      | 0.03    | -7.13    | -9.15692            |
| ST / N         | WEAK     | 99.98   | 2.86     | -1.1414000000000035 |
| MX / Y         | NEG      | 0.08    | -7.08    | -9.15692            |
| MX / N         | WEAK     | 99.92   | 2.80     | -1.195879166666669  |
| M10 / Y        | NEG      | 0.05    | -7.11    | -9.15692            |
| M10 / N        | WEAK     | 99.95   | 2.84     | -1.1647854166666693 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Michigan Senate election by 3%-6%?
Contract 3343888; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          22 |        22.69 | +77.31 / −22.69  | 3.41×         |
| No     |          79 |        79.66 | +20.34 / −79.66  | 0.26×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 19.52   | -3.17    | -7.167897716121683  |
| GB / N         | WEAK     | 80.48   | 0.82     | -3.1821022838783186 |
| ST / Y         | WEAK     | 23.67   | 0.98     | -3.020774999999995  |
| ST / N         | NEG      | 76.33   | -3.33    | -7.329225000000005  |
| MX / Y         | NEG      | 20.47   | -2.22    | -6.217962499999996  |
| MX / N         | NEG      | 79.53   | -0.13    | -4.132037500000008  |
| M10 / Y        | NEG      | 20.88   | -1.81    | -5.810254166666665  |
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
| No     |          79 |        79.66 | +20.34 / −79.66  | 0.26×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 19.14   | -3.54    | -7.5441279221754725 |
| GB / N         | WEAK     | 80.86   | 1.19     | -2.805872077824534  |
| ST / Y         | WEAK     | 23.20   | 0.51     | -3.4863999999999953 |
| ST / N         | NEG      | 76.80   | -2.86    | -6.8636000000000035 |
| MX / Y         | NEG      | 19.73   | -2.96    | -6.95567083333333   |
| MX / N         | WEAK     | 80.27   | 0.61     | -3.394329166666677  |
| M10 / Y        | NEG      | 18.49   | -4.20    | -8.197389583333328  |
| M10 / N        | WEAK     | 81.51   | 1.85     | -2.152610416666667  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Michigan Senate election by 9%-12%?
Contract 3343890; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       14.58 |        15.08 | +84.92 / −15.08  | 5.63×         |
| No     |       94.75 |        94.95 | +5.05 / −94.95   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 14.62   | -0.47    | -4.46603840469243   |
| GB / N         | NEG      | 85.38   | -9.57    | -13.569541595307566 |
| ST / Y         | WEAK     | 15.29   | 0.21     | -3.7890299999999986 |
| ST / N         | NEG      | 84.71   | -10.25   | -14.246549999999992 |
| MX / Y         | NEG      | 14.30   | -0.78    | -4.783509166666668  |
| MX / N         | NEG      | 85.70   | -9.25    | -13.25207083333333  |
| M10 / Y        | NEG      | 12.30   | -2.79    | -6.7862695833333335 |
| M10 / N        | NEG      | 87.70   | -7.25    | -11.249310416666658 |
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
| Yes    |        9.2  |         9.54 | +90.46 / −9.54   | 9.49×         |
| No     |       95.12 |        95.31 | +4.69 / −95.31   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 19.73   | 10.19    | 6.194655063107477   |
| GB / N         | NEG      | 80.27   | -15.04   | -19.035795063107475 |
| ST / Y         | GO       | 20.99   | 11.45    | 7.451990000000003   |
| ST / N         | NEG      | 79.01   | -16.29   | -20.293130000000005 |
| MX / Y         | GO       | 15.58   | 6.04     | 2.0446983333333364  |
| MX / N         | NEG      | 84.42   | -10.89   | -14.885838333333334 |
| M10 / Y        | GO       | 16.41   | 6.88     | 2.8767295833333346  |
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
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          80 |        80.64 | +19.36 / −80.64  | 0.24×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 9.93    | -11.73   | -15.731893958934224 |
| GB / N         | GO       | 90.07   | 9.43     | 5.428293958934216   |
| ST / Y         | NEG      | 9.62    | -12.04   | -16.041725          |
| ST / N         | GO       | 90.38   | 9.74     | 5.738124999999994   |
| MX / Y         | NEG      | 14.00   | -7.66    | -11.65917291666667  |
| MX / N         | GO       | 86.00   | 5.36     | 1.3555729166666586  |
| M10 / Y        | NEG      | 13.04   | -8.62    | -12.618704166666667 |
| M10 / N        | GO       | 86.96   | 6.32     | 2.3151041666666705  |
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
| Yes    |          13 |        13.45 | +86.55 / −13.45  | 6.43×         |
| No     |          88 |        88.42 | +11.58 / −88.42  | 0.13×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 20.72   | 7.27     | 3.2652287263198825  |
| GB / N         | NEG      | 79.28   | -9.14    | -13.140028726319885 |
| ST / Y         | GO       | 21.75   | 8.29     | 4.294475            |
| ST / N         | NEG      | 78.25   | -10.17   | -14.169275000000003 |
| MX / Y         | GO       | 19.09   | 5.63     | 1.6345270833333343  |
| MX / N         | NEG      | 80.91   | -7.51    | -11.509327083333332 |
| M10 / Y        | GO       | 19.27   | 5.82     | 1.8214020833333344  |
| M10 / N        | NEG      | 80.73   | -7.70    | -11.69620208333334  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 12%-15%?
Contract 3343971; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.15 |         9.49 | +90.51 / −9.49   | 9.54×         |
| No     |       91.6  |        91.91 | +8.09 / −91.91   | 0.09×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 14.90   | 5.41     | 1.4132656415712388  |
| GB / N         | NEG      | 85.10   | -6.81    | -10.808535641571247 |
| ST / Y         | GO       | 16.71   | 7.22     | 3.2187599999999996  |
| ST / N         | NEG      | 83.29   | -8.61    | -12.614030000000009 |
| MX / Y         | GO       | 15.45   | 5.96     | 1.9642287500000009  |
| MX / N         | NEG      | 84.55   | -7.36    | -11.359498750000007 |
| M10 / Y        | GO       | 15.49   | 6.00     | 1.9984474999999988  |
| M10 / N        | NEG      | 84.51   | -7.39    | -11.393717500000012 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

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

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 6%-9%?
Contract 3343969; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        7.8  |         8.09 | +91.91 / −8.09   | 11.36×        |
| No     |       94.36 |        94.57 | +5.43 / −94.57   | 0.06×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 8.66    | 0.58     | -3.4248892073547537 |
| GB / N         | NEG      | 91.34   | -3.24    | -7.235450792645237  |
| ST / Y         | NEG      | 7.88    | -0.21    | -4.21266            |
| ST / N         | NEG      | 92.12   | -2.45    | -6.4476799999999885 |
| MX / Y         | WEAK     | 8.64    | 0.55     | -3.451149583333334  |
| MX / N         | NEG      | 91.36   | -3.21    | -7.209190416666655  |
| M10 / Y        | WEAK     | 8.70    | 0.62     | -3.384482916666666  |
| M10 / N        | NEG      | 91.30   | -3.28    | -7.275857083333326  |
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
| Yes    |        7.84 |         8.13 | +91.87 / −8.13   | 11.30×        |
| No     |       95.5  |        95.67 | +4.33 / −95.67   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 12.26   | 4.14     | 0.13606909625326763 |
| GB / N         | NEG      | 87.74   | -7.94    | -11.935859096253266 |
| ST / Y         | GO       | 12.71   | 4.58     | 0.5846099999999979  |
| ST / N         | NEG      | 87.29   | -8.38    | -12.384399999999996 |
| MX / Y         | GO       | 12.36   | 4.23     | 0.22934958333333116 |
| MX / N         | NEG      | 87.64   | -8.03    | -12.029139583333336 |
| M10 / Y        | GO       | 12.43   | 4.31     | 0.3060162500000005  |
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
| Yes    |       13.76 |        14.23 | +85.77 / −14.23  | 6.03×         |
| No     |       87.4  |        87.84 | +12.16 / −87.84  | 0.14×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 6.68    | -7.55    | -11.554835590328128 |
| GB / N         | GO       | 93.32   | 5.48     | 1.480565590328109   |
| ST / Y         | NEG      | 4.72    | -9.51    | -13.50877           |
| ST / N         | GO       | 95.28   | 7.43     | 3.4344999999999843  |
| MX / Y         | NEG      | 4.05    | -10.19   | -14.187624166666664 |
| MX / N         | GO       | 95.95   | 8.11     | 4.1133541666666495  |
| M10 / Y        | NEG      | 4.01    | -10.22   | -14.221374166666667 |
| M10 / N        | GO       | 95.99   | 8.15     | 4.147104166666649   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 North Carolina Senate election by 15%-18%?
Contract 3344038; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10    |        10.36 | +89.64 / −10.36  | 8.65×         |
| No     |       93.92 |        94.14 | +5.86 / −94.14   | 0.06×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 2.22    | -8.14    | -12.137241775557827 |
| GB / N         | WEAK     | 97.78   | 3.63     | -0.3673182244421813 |
| ST / Y         | NEG      | 1.33    | -9.03    | -12.36              |
| ST / N         | GO       | 98.67   | 4.52     | 0.5241900000000022  |
| MX / Y         | NEG      | 1.08    | -9.28    | -12.36              |
| MX / N         | GO       | 98.92   | 4.78     | 0.7771066666666604  |
| M10 / Y        | NEG      | 1.07    | -9.29    | -12.36              |
| M10 / N        | GO       | 98.93   | 4.79     | 0.7892420833333302  |
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
| Yes    |        9.99 |        10.35 | +89.65 / −10.35  | 8.66×         |
| No     |       94.26 |        94.48 | +5.52 / −94.48   | 0.06×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.62    | -9.73    | -12.354440000000002 |
| GB / N         | GO       | 99.38   | 4.90     | 0.8987927245220351  |
| ST / Y         | NEG      | 0.29    | -10.07   | -12.354440000000002 |
| ST / N         | GO       | 99.71   | 5.23     | 1.234410000000019   |
| MX / Y         | NEG      | 0.26    | -10.10   | -12.354440000000002 |
| MX / N         | GO       | 99.74   | 5.27     | 1.2664933333333517  |
| M10 / Y        | NEG      | 0.25    | -10.10   | -12.354440000000002 |
| M10 / N        | GO       | 99.75   | 5.27     | 1.2688891666666868  |
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
| Yes    |       16.57 |        17.12 | +82.88 / −17.12  | 4.84×         |
| No     |       87    |        87.45 | +12.55 / −87.45  | 0.14×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 14.23   | -2.90    | -6.895124274735966  |
| GB / N         | NEG      | 85.77   | -1.68    | -5.680245725264033  |
| ST / Y         | NEG      | 13.50   | -3.63    | -7.626094999999998  |
| ST / N         | NEG      | 86.50   | -0.95    | -4.949274999999997  |
| MX / Y         | NEG      | 11.48   | -5.65    | -9.646042916666666  |
| MX / N         | WEAK     | 88.52   | 1.07     | -2.9293270833333325 |
| M10 / Y        | NEG      | 11.41   | -5.72    | -9.715001249999998  |
| M10 / N        | WEAK     | 88.59   | 1.14     | -2.8603687499999975 |
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
| Yes    |          19 |        19.62 | +80.38 / −19.62  | 4.10×         |
| No     |          83 |        83.56 | +16.44 / −83.56  | 0.20×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 20.16   | 0.54     | -3.4601456718344634 |
| GB / N         | NEG      | 79.84   | -3.72    | -7.7198543281655425 |
| ST / Y         | GO       | 24.12   | 4.50     | 0.5031500000000022  |
| ST / N         | NEG      | 75.88   | -7.68    | -11.683150000000007 |
| MX / Y         | WEAK     | 21.96   | 2.34     | -1.660079166666664  |
| MX / N         | NEG      | 78.04   | -5.52    | -9.51992083333334   |
| M10 / Y        | WEAK     | 22.35   | 2.73     | -1.26549583333333   |
| M10 / N        | NEG      | 77.65   | -5.91    | -9.914504166666681  |
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
| Yes    |       13.87 |        14.33 | +85.67 / −14.33  | 5.98×         |
| No     |       99.7  |        99.71 | +0.29 / −99.71   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.09    | -14.24   | -16.328870000000002 |
| GB / N         | WEAK     | 99.91   | 0.20     | -3.8023471132106694 |
| ST / Y         | NEG      | 0.11    | -14.22   | -16.328870000000002 |
| ST / N         | WEAK     | 99.89   | 0.18     | -3.8244600000000073 |
| MX / Y         | NEG      | 0.66    | -13.67   | -16.328870000000002 |
| MX / N         | NEG      | 99.34   | -0.37    | -4.374616250000008  |
| M10 / Y        | NEG      | 0.77    | -13.56   | -16.328870000000002 |
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
| Yes    |        1.45 |         1.5  | +98.50 / −1.50   | 65.58×        |
| No     |       99.3  |        99.33 | +0.67 / −99.33   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 4.53    | 3.03     | -0.969880191994189  |
| GB / N         | NEG      | 95.47   | -3.86    | -7.8598998080058    |
| ST / Y         | WEAK     | 3.53    | 2.03     | -1.97073            |
| ST / N         | NEG      | 96.47   | -2.86    | -6.859049999999989  |
| MX / Y         | GO       | 7.72    | 6.22     | 2.216197083333333   |
| MX / N         | NEG      | 92.28   | -7.05    | -11.045977083333325 |
| M10 / Y        | GO       | 8.45    | 6.94     | 2.9449470833333335  |
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
| Yes    |       11.32 |        11.7  | +88.30 / −11.70  | 7.55×         |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 14.27   | 2.57     | -1.4263650587097623 |
| GB / N         | NEG      | 85.73   | -13.89   | -17.88934494129022  |
| ST / Y         | NEG      | 11.22   | -0.48    | -4.484145000000001  |
| ST / N         | NEG      | 88.78   | -10.83   | -14.83156499999998  |
| MX / Y         | GO       | 16.65   | 4.95     | 0.9481466666666688  |
| MX / N         | NEG      | 83.35   | -16.26   | -20.26385666666666  |
| M10 / Y        | GO       | 17.63   | 5.93     | 1.9299175000000028  |
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
| Yes    |       15.9  |        16.43 | +83.57 / −16.43  | 5.08×         |
| No     |       87.73 |        88.16 | +11.84 / −88.16  | 0.13×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 26.25   | 9.81     | 5.8137470539281715  |
| GB / N         | NEG      | 73.75   | -14.41   | -18.40660705392816  |
| ST / Y         | GO       | 24.83   | 8.40     | 4.3994950000000035  |
| ST / N         | NEG      | 75.17   | -12.99   | -16.992354999999993 |
| MX / Y         | GO       | 25.32   | 8.88     | 4.884026250000003   |
| MX / N         | NEG      | 74.68   | -13.48   | -17.47688624999999  |
| M10 / Y        | GO       | 25.88   | 9.44     | 5.442567916666666   |
| M10 / N        | NEG      | 74.12   | -14.04   | -18.035427916666656 |
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

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 0%-3%?
Contract 3344162; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         0.9 |         0.94 | +99.06 / −0.94   | 105.87×       |
| No     |        99.2 |        99.23 | +0.77 / −99.23   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 1.19    | 0.26     | -2.9356799999999996 |
| GB / N         | NEG      | 98.81   | -0.42    | -4.423105329589405  |
| ST / Y         | NEG      | 0.76    | -0.18    | -2.9356799999999996 |
| ST / N         | WEAK     | 99.24   | 0.01     | -3.987989999999997  |
| MX / Y         | WEAK     | 1.73    | 0.80     | -2.9356799999999996 |
| MX / N         | NEG      | 98.27   | -0.96    | -4.96278166666666   |
| M10 / Y        | WEAK     | 1.71    | 0.78     | -2.9356799999999996 |
| M10 / N        | NEG      | 98.29   | -0.94    | -4.943302499999991  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 12%-15%?
Contract 3344166; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        8.49 |         8.8  | +91.20 / −8.80   | 10.36×        |
| No     |       93    |        93.26 | +6.74 / −93.26   | 0.07×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 14.02   | 5.22     | 1.2162178122252232  |
| GB / N         | NEG      | 85.98   | -7.28    | -11.276257812225232 |
| ST / Y         | GO       | 14.88   | 6.08     | 2.0847350000000002  |
| ST / N         | NEG      | 85.12   | -8.14    | -12.144774999999996 |
| MX / Y         | GO       | 13.61   | 4.81     | 0.811453749999999   |
| MX / N         | NEG      | 86.39   | -6.87    | -10.871493750000006 |
| M10 / Y        | GO       | 13.54   | 4.74     | 0.7433808333333347  |
| M10 / N        | NEG      | 86.46   | -6.80    | -10.803420833333343 |
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
| Yes    |        26.7 |        27.48 | +72.52 / −27.48  | 2.64×         |
| No     |        74   |        74.77 | +25.23 / −74.77  | 0.34×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 16.42   | -11.07   | -15.066293620365197 |
| GB / N         | GO       | 83.58   | 8.81     | 4.813853620365194   |
| ST / Y         | NEG      | 19.27   | -8.21    | -12.214090000000004 |
| ST / N         | GO       | 80.73   | 5.96     | 1.9616500000000037  |
| MX / Y         | NEG      | 15.59   | -11.90   | -15.897579583333336 |
| MX / N         | GO       | 84.41   | 9.65     | 5.645139583333336   |
| M10 / Y        | NEG      | 15.65   | -11.83   | -15.83106916666667  |
| M10 / N        | GO       | 84.35   | 9.58     | 5.57862916666667    |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 21% or more?
Contract 3344169; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          46 |        46.99 | +53.01 / −46.99  | 1.13×         |
| No     |          57 |        57.98 | +42.02 / −57.98  | 0.72×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 32.59   | -14.41   | -18.40510568559921  |
| GB / N         | GO       | 67.41   | 9.43     | 5.431105685599203   |
| ST / Y         | NEG      | 30.11   | -16.88   | -20.884225000000004 |
| ST / N         | GO       | 69.89   | 11.91    | 7.910225000000004   |
| MX / Y         | NEG      | 32.50   | -14.50   | -18.495943750000006 |
| MX / N         | GO       | 67.50   | 9.52     | 5.521943749999991   |
| M10 / Y        | NEG      | 32.92   | -14.07   | -18.073183333333336 |
| M10 / N        | GO       | 67.08   | 9.10     | 5.099183333333324   |
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

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 6%-9%?
Contract 3344164; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        3.09 |         3.21 | +96.79 / −3.21   | 30.14×        |
| No     |       97.54 |        97.64 | +2.36 / −97.64   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 5.85    | 2.64     | -1.3642619335149946 |
| GB / N         | NEG      | 94.15   | -3.49    | -7.487328066484988  |
| ST / Y         | WEAK     | 4.16    | 0.95     | -3.05455            |
| ST / N         | NEG      | 95.84   | -1.80    | -5.797039999999976  |
| MX / Y         | WEAK     | 5.98    | 2.77     | -1.2260083333333338 |
| MX / N         | NEG      | 94.02   | -3.63    | -7.625581666666648  |
| M10 / Y        | WEAK     | 5.88    | 2.67     | -1.327102083333334  |
| M10 / N        | NEG      | 94.12   | -3.52    | -7.5244879166666445 |
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
| Yes    |        3.72 |         3.86 | +96.14 / −3.86   | 24.90×        |
| No     |       99.57 |        99.59 | +0.41 / −99.59   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.06 |    -3.80 |        -5.86 |
| GB / N         | WEAK     |   99.94 |     0.35 |        -3.65 |
| ST / Y         | NEG      |    0.15 |    -3.71 |        -5.86 |
| ST / N         | WEAK     |   99.85 |     0.26 |        -3.74 |
| MX / Y         | NEG      |    1.54 |    -2.32 |        -5.86 |
| MX / N         | NEG      |   98.46 |    -1.12 |        -5.12 |
| M10 / Y        | NEG      |    1.46 |    -2.40 |        -5.86 |
| M10 / N        | NEG      |   98.54 |    -1.05 |        -5.05 |
| RTWH / Y       | NEG      |    1.10 |    -2.76 |        -5.86 |
| RTWH / N       | NEG      |   98.90 |    -0.69 |        -4.69 |
| DDHQ / Y       | WEAK     |    5.00 |     1.14 |        -2.86 |
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
| Yes    |        99.7 |        99.71 | +0.29 / −99.71   | 0.00×         |
| No     |         1.9 |         1.97 | +98.03 / −1.97   | 49.64×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK*    |   99.95 |     0.24 |        -3.76 |
| GB / N         | NEG*     |    0.05 |    -1.93 |        -3.97 |
| ST / Y         | NEG*     |   99.62 |    -0.09 |        -4.09 |
| ST / N         | NEG*     |    0.38 |    -1.60 |        -3.97 |
| MX / Y         | NEG*     |   99.57 |    -0.14 |        -4.14 |
| MX / N         | NEG*     |    0.43 |    -1.54 |        -3.97 |
| M10 / Y        | NEG*     |   99.46 |    -0.25 |        -4.25 |
| M10 / N        | NEG*     |    0.54 |    -1.43 |        -3.97 |
| RTWH / Y       | NEG      |   98.00 |    -1.71 |        -5.71 |
| RTWH / N       | WEAK     |    2.00 |     0.03 |        -3.97 |
| DDHQ / Y       | NEG      |   99.00 |    -0.71 |        -4.71 |
| DDHQ / N       | NEG      |    1.00 |    -0.97 |        -3.97 |

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
| Yes    |        4.41 |         4.58 | +95.42 / −4.58   | 20.83×        |
| No     |       97.17 |        97.28 | +2.72 / −97.28   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.88 |    -2.70 |        -6.58 |
| GB / N         | WEAK     |   98.12 |     0.83 |        -3.17 |
| ST / Y         | NEG      |    1.42 |    -3.16 |        -6.58 |
| ST / N         | WEAK     |   98.58 |     1.29 |        -2.71 |
| MX / Y         | NEG      |    3.90 |    -0.68 |        -4.68 |
| MX / N         | NEG      |   96.10 |    -1.18 |        -5.18 |
| M10 / Y        | NEG      |    2.96 |    -1.62 |        -5.62 |
| M10 / N        | NEG      |   97.04 |    -0.24 |        -4.24 |
| RTWH / Y       | NEG      |    2.10 |    -2.48 |        -6.48 |
| RTWH / N       | WEAK     |   97.90 |     0.62 |        -3.38 |
| DDHQ / Y       | WEAK     |    5.00 |     0.42 |        -3.58 |
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
| Yes    |          68 |        68.87 | +31.13 / −68.87  | 0.45×         |
| No     |          33 |        33.88 | +66.12 / −33.88  | 1.95×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO*      |   92.55 |    23.68 |        19.68 |
| GB / N         | NEG*     |    7.45 |   -26.44 |       -30.44 |
| ST / Y         | GO*      |   93.63 |    24.76 |        20.76 |
| ST / N         | NEG*     |    6.37 |   -27.52 |       -31.52 |
| MX / Y         | GO*      |   85.54 |    16.67 |        12.67 |
| MX / N         | NEG*     |   14.46 |   -19.43 |       -23.43 |
| M10 / Y        | GO*      |   82.94 |    14.07 |        10.07 |
| M10 / N        | NEG*     |   17.06 |   -16.83 |       -20.83 |
| RTWH / Y       | NEG      |   62.20 |    -6.67 |       -10.67 |
| RTWH / N       | WEAK     |   37.80 |     3.92 |        -0.08 |
| DDHQ / Y       | NEG      |   54.00 |   -14.87 |       -18.87 |
| DDHQ / N       | GO       |   46.00 |    12.12 |         8.12 |

GB, ST, MX, M10: Ranked-choice transfers are not separately modeled; the modeled margin is used as a proxy for the eventual winner.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Massachusetts Senate race in 2026?
Contract 630790; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       98.28 |        98.34 | +1.66 / −98.34   | 0.02×         |
| No     |        2.5  |         2.6  | +97.40 / −2.60   | 37.50×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |  100.00 |     1.66 |        -2.34 |
| GB / N         | NEG      |    0.00 |    -2.60 |        -4.60 |
| ST / Y         | WEAK     |  100.00 |     1.65 |        -2.35 |
| ST / N         | NEG      |    0.00 |    -2.59 |        -4.60 |
| MX / Y         | WEAK     |   99.99 |     1.65 |        -2.35 |
| MX / N         | NEG      |    0.01 |    -2.59 |        -4.60 |
| M10 / Y        | WEAK     |   99.99 |     1.65 |        -2.35 |
| M10 / N        | NEG      |    0.01 |    -2.59 |        -4.60 |
| RTWH / Y       | WEAK     |   99.60 |     1.26 |        -2.74 |
| RTWH / N       | NEG      |    0.40 |    -2.20 |        -4.60 |
| DDHQ / Y       | WEAK     |   99.00 |     0.66 |        -3.34 |
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
| No     |        2.86 |         2.97 | +97.03 / −2.97   | 32.62×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   99.43 |    -0.20 |        -4.20 |
| GB / N         | NEG      |    0.57 |    -2.41 |        -4.97 |
| ST / Y         | NEG      |   99.41 |    -0.22 |        -4.22 |
| ST / N         | NEG      |    0.59 |    -2.39 |        -4.97 |
| MX / Y         | NEG      |   98.48 |    -1.15 |        -5.15 |
| MX / N         | NEG      |    1.52 |    -1.46 |        -4.97 |
| M10 / Y        | NEG      |   98.52 |    -1.11 |        -5.11 |
| M10 / N        | NEG      |    1.48 |    -1.49 |        -4.97 |
| RTWH / Y       | NEG      |   98.10 |    -1.53 |        -5.53 |
| RTWH / N       | NEG      |    1.90 |    -1.07 |        -4.97 |
| DDHQ / Y       | NEG      |   96.00 |    -3.63 |        -7.63 |
| DDHQ / N       | WEAK     |    4.00 |     1.03 |        -2.97 |

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
| Yes    |          13 |        13.45 | +86.55 / −13.45  | 6.43×         |
| No     |          88 |        88.42 | +11.58 / −88.42  | 0.13×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 12.70   | -0.75    | -4.748147683235569  |
| GB / N         | NEG      | 87.30   | -1.13    | -5.126652316764434  |
| ST / Y         | NEG      | 10.22   | -3.23    | -7.2274             |
| ST / N         | WEAK     | 89.78   | 1.35     | -2.6473999999999993 |
| MX / Y         | WEAK     | 14.48   | 1.02     | -2.9769833333333344 |
| MX / N         | NEG      | 85.52   | -2.90    | -6.897816666666667  |
| M10 / Y        | WEAK     | 14.11   | 0.66     | -3.3412020833333314 |
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

## Will the Republican Party candidate win the 2026 Alabama Senate election by 25%-30%?
Contract 3343102; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        18.2 |        18.8  | +81.20 / −18.80  | 4.32×         |
| No     |        84   |        84.54 | +15.46 / −84.54  | 0.18×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 19.30   | 0.50     | -3.4969262743435676 |
| GB / N         | NEG      | 80.70   | -3.84    | -7.8361137256564355 |
| ST / Y         | WEAK     | 19.33   | 0.53     | -3.467314999999998  |
| ST / N         | NEG      | 80.67   | -3.87    | -7.865725000000001  |
| MX / Y         | NEG      | 15.84   | -2.95    | -6.951950416666666  |
| MX / N         | NEG      | 84.16   | -0.38    | -4.381089583333331  |
| M10 / Y        | NEG      | 16.34   | -2.45    | -6.45471083333333   |
| M10 / N        | NEG      | 83.66   | -0.88    | -4.878329166666672  |
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
| No     |       86.94 |        87.39 | +12.61 / −87.39  | 0.14×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 3.67    | -11.84   | -15.840217679996963 |
| GB / N         | GO       | 96.33   | 8.94     | 4.94032767999697    |
| ST / Y         | NEG      | 2.84    | -12.67   | -16.6725            |
| ST / N         | GO       | 97.16   | 9.77     | 5.772609999999999   |
| MX / Y         | NEG      | 7.20    | -8.31    | -12.306614583333333 |
| MX / N         | GO       | 92.80   | 5.41     | 1.4067245833333408  |
| M10 / Y        | NEG      | 6.97    | -8.54    | -12.543125          |
| M10 / N        | GO       | 93.03   | 5.64     | 1.6432350000000095  |
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
| No     |        73.6 |        74.38 | +25.62 / −74.38  | 0.34×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 16.18   | -11.10   | -15.102838994980475 |
| GB / N         | GO       | 83.82   | 9.45     | 5.446518994980476   |
| ST / Y         | NEG      | 16.19   | -11.09   | -15.08535           |
| ST / N         | GO       | 83.81   | 9.43     | 5.42902999999999    |
| MX / Y         | NEG      | 17.99   | -9.29    | -13.292172916666665 |
| MX / N         | GO       | 82.01   | 7.64     | 3.6358529166666598  |
| M10 / Y        | NEG      | 17.22   | -10.06   | -14.060975000000001 |
| M10 / N        | GO       | 82.78   | 8.40     | 4.404655000000002   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Arkansas Senate election by 15%-20%?
Contract 3343123; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          28 |        28.81 | +71.19 / −28.81  | 2.47×         |
| No     |          73 |        73.79 | +26.21 / −73.79  | 0.36×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 26.03   | -2.78    | -6.780271689315534  |
| GB / N         | WEAK     | 73.97   | 0.19     | -3.8145283106844725 |
| ST / Y         | WEAK     | 28.82   | 0.02     | -3.9814000000000065 |
| ST / N         | NEG      | 71.17   | -2.61    | -6.613400000000002  |
| MX / Y         | NEG      | 21.87   | -6.94    | -10.936608333333337 |
| MX / N         | GO       | 78.13   | 4.34     | 0.34180833333332655 |
| M10 / Y        | NEG      | 21.51   | -7.30    | -11.297910416666673 |
| M10 / N        | GO       | 78.49   | 4.70     | 0.7031104166666635  |
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
| Yes    |          11 |        11.39 | +88.61 / −11.39  | 7.78×         |
| No     |          91 |        91.33 | +8.67 / −91.33   | 0.09×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 25.96   | 14.57    | 10.565290760275026  |
| GB / N         | NEG      | 74.04   | -17.28   | -21.284490760275045 |
| ST / Y         | GO       | 28.23   | 16.83    | 12.833399999999997  |
| ST / N         | NEG      | 71.78   | -19.55   | -23.552600000000012 |
| MX / Y         | GO       | 18.79   | 7.40     | 3.397722916666668   |
| MX / N         | NEG      | 81.21   | -10.12   | -14.116922916666674 |
| M10 / Y        | GO       | 19.87   | 8.48     | 4.4772541666666665  |
| M10 / N        | NEG      | 80.13   | -11.20   | -15.196454166666673 |
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
| No     |        81.3 |        81.91 | +18.09 / −81.91  | 0.22×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 14.55   | -7.12    | -11.116565629165231 |
| GB / N         | WEAK     | 85.45   | 3.54     | -0.455154370834765  |
| ST / Y         | NEG      | 15.98   | -5.68    | -9.679224999999997  |
| ST / N         | WEAK     | 84.02   | 2.11     | -1.8924950000000051 |
| MX / Y         | NEG      | 14.41   | -7.25    | -11.253287499999999 |
| MX / N         | WEAK     | 85.59   | 3.68     | -0.3184324999999988 |
| M10 / Y        | NEG      | 13.61   | -8.05    | -12.051204166666665 |
| M10 / N        | GO       | 86.39   | 4.48     | 0.47948416666666605 |
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
| Yes    |        8.6  |         8.91 | +91.09 / −8.91   | 10.22×        |
| No     |       93.16 |        93.42 | +6.58 / −93.42   | 0.07×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 9.31    | 0.40     | -3.6017698614882145 |
| GB / N         | NEG      | 90.69   | -2.73    | -6.729680138511807  |
| ST / Y         | NEG      | 7.39    | -1.52    | -5.523795           |
| ST / N         | NEG      | 92.61   | -0.81    | -4.807655000000022  |
| MX / Y         | NEG      | 8.79    | -0.13    | -4.126190833333333  |
| MX / N         | NEG      | 91.21   | -2.21    | -6.205259166666676  |
| M10 / Y        | WEAK     | 9.60    | 0.68     | -3.316295000000001  |
| M10 / N        | NEG      | 90.40   | -3.02    | -7.015155000000018  |
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
| Yes    |        3.25 |         3.37 | +96.63 / −3.37   | 28.64×        |
| No     |       98.5  |        98.56 | +1.44 / −98.56   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 4.97    | 1.60     | -2.4022253067829227 |
| GB / N         | NEG      | 95.03   | -3.53    | -7.530924693217067  |
| ST / Y         | NEG      | 2.97    | -0.40    | -4.4021750000000015 |
| ST / N         | NEG      | 97.03   | -1.53    | -5.530974999999994  |
| MX / Y         | WEAK     | 4.68    | 1.31     | -2.690091666666667  |
| MX / N         | NEG      | 95.32   | -3.24    | -7.24305833333333   |
| M10 / Y        | WEAK     | 5.31    | 1.94     | -2.062904166666668  |
| M10 / N        | NEG      | 94.69   | -3.87    | -7.870245833333323  |
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
| Yes    |          12 |        12.42 | +87.58 / −12.42  | 7.05×         |
| No     |          90 |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 13.31   | 0.88     | -3.1157097619115124 |
| GB / N         | NEG      | 86.69   | -3.67    | -7.6666902380884805 |
| ST / Y         | WEAK     | 13.24   | 0.82     | -3.178649999999998  |
| ST / N         | NEG      | 86.76   | -3.60    | -7.603749999999998  |
| MX / Y         | WEAK     | 12.81   | 0.38     | -3.6169312499999986 |
| MX / N         | NEG      | 87.19   | -3.17    | -7.165468750000005  |
| M10 / Y        | WEAK     | 13.32   | 0.90     | -3.0977125000000014 |
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
| Yes    |        3.74 |         3.88 | +96.12 / −3.88   | 24.75×        |
| No     |       97.7  |        97.79 | +2.21 / −97.79   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)           |
|:---------------|:---------|:--------|:---------|:---------------------|
| GB / Y         | WEAK     | 7.50    | 3.62     | -0.38383448117687846 |
| GB / N         | NEG      | 92.50   | -5.29    | -9.28892551882312    |
| ST / Y         | WEAK     | 5.39    | 1.51     | -2.4891300000000003  |
| ST / N         | NEG      | 94.61   | -3.18    | -7.183629999999996   |
| MX / Y         | WEAK     | 6.29    | 2.41     | -1.5937654166666677  |
| MX / N         | NEG      | 93.71   | -4.08    | -8.078994583333332   |
| M10 / Y        | WEAK     | 6.71    | 2.83     | -1.1723070833333336  |
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
| No     |       94.39 |        94.6  | +5.40 / −94.60   | 0.06×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 22.83   | 12.47    | 8.4723771908735     |
| GB / N         | NEG      | 77.17   | -17.43   | -21.430337190873505 |
| ST / Y         | GO       | 22.34   | 11.98    | 7.983750000000002   |
| ST / N         | NEG      | 77.66   | -16.94   | -20.941710000000004 |
| MX / Y         | GO       | 21.50   | 11.14    | 7.143958333333335   |
| MX / N         | NEG      | 78.50   | -16.10   | -20.101918333333344 |
| M10 / Y        | GO       | 20.08   | 9.72     | 5.71578125          |
| M10 / N        | NEG      | 79.92   | -14.67   | -18.67374125000001  |
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
| Yes    |        9.78 |        10.13 | +89.87 / −10.13  | 8.88×         |
| No     |       96.99 |        97.11 | +2.89 / −97.11   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.90    | -9.22    | -12.12621           |
| GB / N         | WEAK     | 99.10   | 1.99     | -2.012713824121104  |
| ST / Y         | NEG      | 0.37    | -9.76    | -12.12621           |
| ST / N         | WEAK     | 99.63   | 2.52     | -1.4782100000000131 |
| MX / Y         | NEG      | 0.89    | -9.24    | -12.12621           |
| MX / N         | WEAK     | 99.11   | 2.00     | -1.9956579166666821 |
| M10 / Y        | NEG      | 0.75    | -9.37    | -12.12621           |
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
| Yes    |       11    |        11.39 | +88.61 / −11.39  | 7.78×         |
| No     |       94.84 |        95.04 | +4.96 / −95.04   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | NEG      | 0.05    | -11.34   | -13.3916           |
| GB / N         | GO       | 99.95   | 4.91     | 0.9097466825398803 |
| ST / Y         | NEG      | 0.02    | -11.37   | -13.3916           |
| ST / N         | GO       | 99.98   | 4.94     | 0.9424249999999913 |
| MX / Y         | NEG      | 0.07    | -11.33   | -13.3916           |
| MX / N         | GO       | 99.93   | 4.90     | 0.8986749999999932 |
| M10 / Y        | NEG      | 0.05    | -11.34   | -13.3916           |
| M10 / N        | GO       | 99.95   | 4.91     | 0.9101854166666645 |
| RTWH / Y       | N/A      | —       | —        | —                  |
| RTWH / N       | N/A      | —       | —        | —                  |
| DDHQ / Y       | N/A      | —       | —        | —                  |
| DDHQ / N       | N/A      | —       | —        | —                  |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Kansas Senate election by 30% or more?
Contract 3343540; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        5.32 |         5.52 | +94.48 / −5.52   | 17.12×        |
| No     |       99.62 |        99.64 | +0.36 / −99.64   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.00    | -5.52    | -7.518849999999999  |
| GB / N         | WEAK     | 100.00  | 0.36     | -3.64038218171987   |
| ST / Y         | NEG      | 0.00    | -5.52    | -7.518849999999999  |
| ST / N         | WEAK     | 100.00  | 0.36     | -3.6420149999999984 |
| MX / Y         | NEG      | 0.00    | -5.52    | -7.518849999999999  |
| MX / N         | WEAK     | 100.00  | 0.36     | -3.641337916666665  |
| M10 / Y        | NEG      | 0.00    | -5.52    | -7.518849999999999  |
| M10 / N        | WEAK     | 100.00  | 0.36     | -3.640556666666661  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

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

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 25%-30%?
Contract 3343561; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          12 |        12.42 | +87.58 / −12.42  | 7.05×         |
| No     |          90 |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 2.16    | -10.26   | -14.262503765393918 |
| GB / N         | GO       | 97.84   | 7.48     | 3.480103765393916   |
| ST / Y         | NEG      | 1.08    | -11.34   | -14.4224            |
| ST / N         | GO       | 98.92   | 8.56     | 4.5556249999999965  |
| MX / Y         | NEG      | 1.81    | -10.61   | -14.4224            |
| MX / N         | GO       | 98.19   | 7.83     | 3.8295312499999956  |
| M10 / Y        | NEG      | 2.47    | -9.95    | -13.954066666666666 |
| M10 / N        | GO       | 97.53   | 7.17     | 3.1716666666666615  |
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
| Yes    |        11   |        11.39 | +88.61 / −11.39  | 7.78×         |
| No     |        93.4 |        93.65 | +6.35 / −93.65   | 0.07×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | NEG      | 0.25    | -11.14   | -13.3916           |
| GB / N         | GO       | 99.75   | 6.10     | 2.09997300432625   |
| ST / Y         | NEG      | 0.11    | -11.28   | -13.3916           |
| ST / N         | GO       | 99.89   | 6.24     | 2.2410199999999825 |
| MX / Y         | NEG      | 0.28    | -11.11   | -13.3916           |
| MX / N         | GO       | 99.72   | 6.07     | 2.0749783333333216 |
| M10 / Y        | NEG      | 0.40    | -11.00   | -13.3916           |
| M10 / N        | GO       | 99.60   | 5.96     | 1.9582595833333216 |
| RTWH / Y       | N/A      | —       | —        | —                  |
| RTWH / N       | N/A      | —       | —        | —                  |
| DDHQ / Y       | N/A      | —       | —        | —                  |
| DDHQ / N       | N/A      | —       | —        | —                  |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 35%-40%?
Contract 3343559; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         7.6 |         7.88 | +92.12 / −7.88   | 11.69×        |
| No     |        93.6 |        93.84 | +6.16 / −93.84   | 0.07×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | NEG      | 0.02    | -7.87    | -9.880899999999999 |
| GB / N         | GO       | 99.98   | 6.14     | 2.144529605956469  |
| ST / Y         | NEG      | 0.01    | -7.87    | -9.880899999999999 |
| ST / N         | GO       | 99.99   | 6.15     | 2.14787999999998   |
| MX / Y         | NEG      | 0.03    | -7.85    | -9.880899999999999 |
| MX / N         | GO       | 99.97   | 6.13     | 2.1285049999999806 |
| M10 / Y        | NEG      | 0.05    | -7.83    | -9.880899999999999 |
| M10 / N        | GO       | 99.95   | 6.11     | 2.107879999999984  |
| RTWH / Y       | N/A      | —       | —        | —                  |
| RTWH / N       | N/A      | —       | —        | —                  |
| DDHQ / Y       | N/A      | —       | —        | —                  |
| DDHQ / N       | N/A      | —       | —        | —                  |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 40%-45%?
Contract 3343558; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10.19 |        10.56 | +89.44 / −10.56  | 8.47×         |
| No     |       94.14 |        94.36 | +5.64 / −94.36   | 0.06×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.00    | -10.56   | -12.555999999999997 |
| GB / N         | GO       | 100.00  | 5.64     | 1.6396541754790772  |
| ST / Y         | NEG      | 0.01    | -10.55   | -12.555999999999997 |
| ST / N         | GO       | 99.99   | 5.63     | 1.6339300000000057  |
| MX / Y         | NEG      | 0.00    | -10.55   | -12.555999999999997 |
| MX / N         | GO       | 100.00  | 5.64     | 1.637002916666663   |
| M10 / Y        | NEG      | 0.00    | -10.55   | -12.555999999999997 |
| M10 / N        | GO       | 100.00  | 5.64     | 1.637002916666663   |
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
| Yes    |          12 |        12.42 | +87.58 / −12.42  | 7.05×         |
| No     |          90 |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 15.89   | 3.46     | -0.5369260168352985 |
| GB / N         | NEG      | 84.11   | -6.25    | -10.245473983164697 |
| ST / Y         | WEAK     | 14.19   | 1.77     | -2.2317749999999985 |
| ST / N         | NEG      | 85.81   | -4.55    | -8.550625           |
| MX / Y         | GO       | 19.12   | 6.69     | 2.6940583333333383  |
| MX / N         | NEG      | 80.88   | -9.48    | -13.47645833333333  |
| M10 / Y        | GO       | 19.38   | 6.96     | 2.956870833333336   |
| M10 / N        | NEG      | 80.62   | -9.74    | -13.739270833333329 |
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
| Yes    |          23 |        23.71 | +76.29 / −23.71  | 3.22×         |
| No     |          80 |        80.64 | +19.36 / −80.64  | 0.24×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 15.11   | -8.60    | -12.599539182068328 |
| GB / N         | GO       | 84.89   | 4.25     | 0.2511391820683162  |
| ST / Y         | NEG      | 13.58   | -10.13   | -14.133400000000002 |
| ST / N         | GO       | 86.42   | 5.78     | 1.7849999999999921  |
| MX / Y         | NEG      | 11.59   | -12.12   | -16.118452083333334 |
| MX / N         | GO       | 88.41   | 7.77     | 3.770052083333331   |
| M10 / Y        | NEG      | 11.35   | -12.36   | -16.35850416666667  |
| M10 / N        | GO       | 88.65   | 8.01     | 4.010104166666661   |
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
| Yes    |        12.4 |        12.83 | +87.17 / −12.83  | 6.79×         |
| No     |        90   |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 4.06    | -8.78    | -12.775499857489448 |
| GB / N         | GO       | 95.94   | 5.58     | 1.5810998574894541  |
| ST / Y         | NEG      | 2.27    | -10.56   | -14.559399999999997 |
| ST / N         | GO       | 97.72   | 7.36     | 3.364999999999996   |
| MX / Y         | NEG      | 2.84    | -9.99    | -13.989764583333331 |
| MX / N         | GO       | 97.16   | 6.80     | 2.795364583333337   |
| M10 / Y        | NEG      | 2.76    | -10.07   | -14.070024999999998 |
| M10 / N        | GO       | 97.24   | 6.88     | 2.875625000000004   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Louisiana Senate election by 25%-30%?
Contract 3343572; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        4.9  |         5.08 | +94.92 / −5.08   | 18.68×        |
| No     |       99.48 |        99.5  | +0.50 / −99.50   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.57    | -4.51    | -7.0810200000000005 |
| GB / N         | NEG      | 99.43   | -0.07    | -4.071820880038701  |
| ST / Y         | NEG      | 0.21    | -4.87    | -7.0810200000000005 |
| ST / N         | WEAK     | 99.79   | 0.29     | -3.710329999999995  |
| MX / Y         | NEG      | 0.46    | -4.62    | -7.0810200000000005 |
| MX / N         | WEAK     | 99.54   | 0.03     | -3.96746541666666   |
| M10 / Y        | NEG      | 0.45    | -4.64    | -7.0810200000000005 |
| M10 / N        | WEAK     | 99.55   | 0.05     | -3.949392499999993  |
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
| Yes    |        6.87 |         7.12 | +92.88 / −7.12   | 13.04×        |
| No     |       96.47 |        96.61 | +3.39 / −96.61   | 0.04×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.04    | -7.08    | -9.12099            |
| GB / N         | WEAK     | 99.96   | 3.35     | -0.6495432294449266 |
| ST / Y         | NEG      | 0.01    | -7.11    | -9.12099            |
| ST / N         | WEAK     | 99.99   | 3.38     | -0.6208500000000061 |
| MX / Y         | NEG      | 0.05    | -7.07    | -9.12099            |
| MX / N         | WEAK     | 99.95   | 3.34     | -0.6616312500000054 |
| M10 / Y        | NEG      | 0.05    | -7.07    | -9.12099            |
| M10 / N        | WEAK     | 99.95   | 3.34     | -0.6607979166666667 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Louisiana Senate election by 35% or more?
Contract 3343570; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9    |         9.33 | +90.67 / −9.33   | 9.72×         |
| No     |       94.22 |        94.44 | +5.56 / −94.44   | 0.06×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | NEG      | 0.00    | -9.33    | -11.3276           |
| GB / N         | GO       | 100.00  | 5.56     | 1.560655779237141  |
| ST / Y         | NEG      | 0.00    | -9.32    | -11.3276           |
| ST / N         | GO       | 100.00  | 5.56     | 1.559104999999994  |
| MX / Y         | NEG      | 0.01    | -9.32    | -11.3276           |
| MX / N         | GO       | 99.99   | 5.55     | 1.5539487500000004 |
| M10 / Y        | NEG      | 0.01    | -9.32    | -11.3276           |
| M10 / N        | GO       | 99.99   | 5.55     | 1.5539487500000004 |
| RTWH / Y       | N/A      | —       | —        | —                  |
| RTWH / N       | N/A      | —       | —        | —                  |
| DDHQ / Y       | N/A      | —       | —        | —                  |
| DDHQ / N       | N/A      | —       | —        | —                  |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Louisiana Senate election by 5%-10%?
Contract 3343576; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        20   |        20.64 | +79.36 / −20.64  | 3.84×         |
| No     |        82.6 |        83.17 | +16.83 / −83.17  | 0.20×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 29.86   | 9.22     | 5.224615972357083   |
| GB / N         | NEG      | 70.14   | -13.04   | -17.039415972357077 |
| ST / Y         | GO       | 32.12   | 11.48    | 7.481874999999999   |
| ST / N         | NEG      | 67.88   | -15.30   | -19.296674999999997 |
| MX / Y         | GO       | 29.45   | 8.81     | 4.806458333333335   |
| MX / N         | NEG      | 70.55   | -12.62   | -16.621258333333333 |
| M10 / Y        | GO       | 29.52   | 8.88     | 4.881614583333333   |
| M10 / N        | NEG      | 70.48   | -12.70   | -16.69641458333333  |
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
| Yes    |        7.31 |         7.57 | +92.43 / −7.57   | 12.20×        |
| No     |       99.7  |        99.71 | +0.29 / −99.71   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.14    | -7.44    | -9.574660000000002  |
| GB / N         | WEAK     | 99.86   | 0.15     | -3.8494331671657394 |
| ST / Y         | NEG      | 0.09    | -7.48    | -9.574660000000002  |
| ST / N         | WEAK     | 99.91   | 0.19     | -3.8057100000000066 |
| MX / Y         | NEG      | 0.29    | -7.29    | -9.574660000000002  |
| MX / N         | WEAK     | 99.71   | 0.00     | -3.9982620833333375 |
| M10 / Y        | NEG      | 0.39    | -7.18    | -9.574660000000002  |
| M10 / N        | NEG      | 99.61   | -0.11    | -4.106126666666665  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Michigan Senate election by 3%-6%?
Contract 3343885; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       12.44 |        12.88 | +87.12 / −12.88  | 6.77×         |
| No     |       93.26 |        93.51 | +6.49 / −93.51   | 0.07×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)           |
|:---------------|:---------|:--------|:---------|:---------------------|
| GB / Y         | NEG      | 4.61    | -8.27    | -12.266576231994168  |
| GB / N         | WEAK     | 95.39   | 1.88     | -2.1195837680058394  |
| ST / Y         | NEG      | 2.98    | -9.89    | -13.894290000000002  |
| ST / N         | WEAK     | 97.02   | 3.51     | -0.49187000000000536 |
| MX / Y         | NEG      | 4.59    | -8.29    | -12.288821250000002  |
| MX / N         | WEAK     | 95.41   | 1.90     | -2.0973387499999996  |
| M10 / Y        | NEG      | 5.81    | -7.07    | -11.066060833333333  |
| M10 / N        | WEAK     | 94.19   | 0.68     | -3.320099166666668   |
| RTWH / Y       | N/A      | —       | —        | —                    |
| RTWH / N       | N/A      | —       | —        | —                    |
| DDHQ / Y       | N/A      | —       | —        | —                    |
| DDHQ / N       | N/A      | —       | —        | —                    |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Michigan Senate election by 6%-9%?
Contract 3343884; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       35.04 |        35.74 | +64.26 / −35.74  | 1.80×         |
| No     |       95.02 |        95.2  | +4.80 / −95.20   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)           |
|:---------------|:---------|:--------|:---------|:---------------------|
| GB / Y         | NEG      | 1.73    | -34.01   | -37.73683            |
| GB / N         | WEAK     | 98.27   | 3.07     | -0.9309383920397707  |
| ST / Y         | NEG      | 0.97    | -34.76   | -37.73683            |
| ST / N         | WEAK     | 99.02   | 3.82     | -0.17946000000000908 |
| MX / Y         | NEG      | 1.89    | -33.85   | -37.73683            |
| MX / N         | WEAK     | 98.11   | 2.91     | -1.0928975000000007  |
| M10 / Y        | NEG      | 2.50    | -33.24   | -37.23948625         |
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
| Yes    |       16.29 |        16.81 | +83.19 / −16.81  | 4.95×         |
| No     |       97.95 |        98.03 | +1.97 / −98.03   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.50    | -16.30   | -18.807629999999996 |
| GB / N         | WEAK     | 99.50   | 1.46     | -2.5359847961896387 |
| ST / Y         | NEG      | 0.24    | -16.56   | -18.807629999999996 |
| ST / N         | WEAK     | 99.76   | 1.72     | -2.2763600000000106 |
| MX / Y         | NEG      | 0.65    | -16.16   | -18.807629999999996 |
| MX / N         | WEAK     | 99.36   | 1.32     | -2.677610000000008  |
| M10 / Y        | NEG      | 0.92    | -15.89   | -18.807629999999996 |
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
| Yes    |       12.44 |        12.88 | +87.12 / −12.88  | 6.77×         |
| No     |       89    |        89.39 | +10.61 / −89.39  | 0.12×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.57    | -11.31   | -14.875599999999999 |
| GB / N         | GO       | 98.43   | 9.04     | 5.041070986404394   |
| ST / Y         | NEG      | 1.72    | -11.16   | -14.875599999999999 |
| ST / N         | GO       | 98.28   | 8.89     | 4.892775000000005   |
| MX / Y         | NEG      | 4.40    | -8.48    | -12.479558333333335 |
| MX / N         | GO       | 95.60   | 6.21     | 2.2123583333333308  |
| M10 / Y        | NEG      | 3.79    | -9.09    | -13.089766666666668 |
| M10 / N        | GO       | 96.21   | 6.82     | 2.8225666666666704  |
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
| Yes    |       25.72 |        26.43 | +73.57 / −26.43  | 2.78×         |
| No     |       99.3  |        99.33 | +0.67 / −99.33   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.41    | -26.02   | -28.43132           |
| GB / N         | WEAK     | 99.59   | 0.26     | -3.7381065617119074 |
| ST / Y         | NEG      | 0.53    | -25.90   | -28.43132           |
| ST / N         | WEAK     | 99.47   | 0.14     | -3.8590499999999976 |
| MX / Y         | NEG      | 1.86    | -24.57   | -28.43132           |
| MX / N         | NEG      | 98.14   | -1.19    | -5.192747916666662  |
| M10 / Y        | NEG      | 1.57    | -24.86   | -28.43132           |
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
| Yes    |       17.93 |        18.42 | +81.58 / −18.42  | 4.43×         |
| No     |       99.9  |        99.9  | +0.10 / −99.90   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | NEG      | 0.10    | -18.32   | -20.41908          |
| GB / N         | WEAK     | 99.90   | 0.00     | -3.999027712691716 |
| ST / Y         | NEG      | 0.18    | -18.24   | -20.41908          |
| ST / N         | NEG      | 99.83   | -0.08    | -4.079000000000022 |
| MX / Y         | NEG      | 0.97    | -17.45   | -20.41908          |
| MX / N         | NEG      | 99.03   | -0.87    | -4.873166666666684 |
| M10 / Y        | NEG      | 0.77    | -17.65   | -20.41908          |
| M10 / N        | NEG      | 99.23   | -0.67    | -4.670718750000013 |
| RTWH / Y       | N/A      | —       | —        | —                  |
| RTWH / N       | N/A      | —       | —        | —                  |
| DDHQ / Y       | N/A      | —       | —        | —                  |
| DDHQ / N       | N/A      | —       | —        | —                  |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 New Mexico Senate election by 3% or more?
Contract 3343965; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         2.6 |         2.7  | +97.30 / −2.70   | 36.02×        |
| No     |        99.4 |        99.42 | +0.58 / −99.42   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.68    | -2.02    | -4.7013             |
| GB / N         | NEG      | 99.32   | -0.10    | -4.101424594971103  |
| ST / Y         | NEG      | 0.30    | -2.40    | -4.7013             |
| ST / N         | WEAK     | 99.70   | 0.27     | -3.726985000000016  |
| MX / Y         | NEG      | 0.67    | -2.04    | -4.7013             |
| MX / N         | NEG      | 99.33   | -0.09    | -4.0896412500000086 |
| M10 / Y        | NEG      | 0.68    | -2.02    | -4.7013             |
| M10 / N        | NEG      | 99.32   | -0.10    | -4.101151666666681  |
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

## Will the Republican Party candidate win the 2026 Ohio Senate election by 12% or more?
Contract 3344042; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.45 |         2.54 | +97.46 / −2.54   | 38.44×        |
| No     |       99.8  |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.40    | -2.14    | -4.5357400000000005 |
| GB / N         | NEG      | 99.60   | -0.21    | -4.2073421895840735 |
| ST / Y         | NEG      | 0.17    | -2.37    | -4.5357400000000005 |
| ST / N         | WEAK     | 99.83   | 0.02     | -3.976729999999995  |
| MX / Y         | NEG      | 0.53    | -2.01    | -4.5357400000000005 |
| MX / N         | NEG      | 99.47   | -0.33    | -4.3330320833333325 |
| M10 / Y        | NEG      | 0.68    | -1.86    | -4.5357400000000005 |
| M10 / N        | NEG      | 99.32   | -0.49    | -4.488240416666667  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Ohio Senate election by 3%-6%?
Contract 3344045; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10.35 |        10.72 | +89.28 / −10.72  | 8.33×         |
| No     |       91.4  |        91.71 | +8.29 / −91.71   | 0.09×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 8.82    | -1.90    | -5.904334538015493  |
| GB / N         | NEG      | 91.18   | -0.53    | -4.531045461984517  |
| ST / Y         | NEG      | 6.52    | -4.21    | -8.205434999999998  |
| ST / N         | WEAK     | 93.48   | 1.77     | -2.229945000000011  |
| MX / Y         | NEG      | 8.73    | -1.99    | -5.994393333333331  |
| MX / N         | NEG      | 91.27   | -0.44    | -4.44098666666668   |
| M10 / Y        | NEG      | 10.08   | -0.64    | -4.642049583333331  |
| M10 / N        | NEG      | 89.92   | -1.79    | -5.7933304166666755 |
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
| Yes    |        9.08 |         9.4  | +90.60 / −9.40   | 9.64×         |
| No     |       97.2  |        97.31 | +2.69 / −97.31   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 3.87    | -5.53    | -9.534815681132338  |
| GB / N         | NEG      | 96.13   | -1.17    | -5.174384318867675  |
| ST / Y         | NEG      | 2.07    | -7.33    | -11.334715000000003 |
| ST / N         | WEAK     | 97.93   | 0.63     | -3.374485000000016  |
| MX / Y         | NEG      | 3.77    | -5.63    | -9.633360833333334  |
| MX / N         | NEG      | 96.23   | -1.08    | -5.075839166666674  |
| M10 / Y        | NEG      | 4.57    | -4.83    | -8.829558750000002  |
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
| Yes    |          16 |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |          86 |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 13.24   | -3.30    | -7.2976863439164585 |
| GB / N         | WEAK     | 86.76   | 0.28     | -3.7215136560835527 |
| ST / Y         | NEG      | 11.28   | -5.26    | -9.2626             |
| ST / N         | WEAK     | 88.72   | 2.24     | -1.7566000000000082 |
| MX / Y         | NEG      | 13.55   | -2.99    | -6.99025625         |
| MX / N         | NEG      | 86.45   | -0.03    | -4.0289437500000025 |
| M10 / Y        | NEG      | 11.99   | -4.55    | -8.545308333333336  |
| M10 / N        | WEAK     | 88.01   | 1.53     | -2.473891666666672  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Oklahoma Senate election by 25%-30%?
Contract 3344068; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          31 |        31.86 | +68.14 / −31.86  | 2.14×         |
| No     |          70 |        70.84 | +29.16 / −70.84  | 0.41×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 28.45   | -3.40    | -7.402257756775632  |
| GB / N         | WEAK     | 71.55   | 0.71     | -3.2933422432243846 |
| ST / Y         | WEAK     | 33.38   | 1.52     | -2.4774750000000068 |
| ST / N         | NEG      | 66.62   | -4.22    | -8.218124999999999  |
| MX / Y         | NEG      | 27.55   | -4.30    | -8.302839583333338  |
| MX / N         | WEAK     | 72.45   | 1.61     | -2.3927604166666727 |
| M10 / Y        | NEG      | 28.10   | -3.75    | -7.754662500000004  |
| M10 / N        | WEAK     | 71.90   | 1.06     | -2.9409375000000066 |
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
| No     |        86.2 |        86.67 | +13.33 / −86.67  | 0.15×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 18.84   | 3.33     | -0.6663586198582621 |
| GB / N         | NEG      | 81.16   | -5.52    | -9.518431380141745  |
| ST / Y         | WEAK     | 18.41   | 2.90     | -1.1037499999999978 |
| ST / N         | NEG      | 81.59   | -5.08    | -9.081040000000007  |
| MX / Y         | WEAK     | 17.85   | 2.34     | -1.660677083333331  |
| MX / N         | NEG      | 82.15   | -4.52    | -8.52411291666667   |
| M10 / Y        | GO       | 19.57   | 4.06     | 0.05510416666666962 |
| M10 / N        | NEG      | 80.43   | -6.24    | -10.239894166666675 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Oklahoma Senate election by 35%-40%?
Contract 3344066; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10    |        10.36 | +89.64 / −10.36  | 8.65×         |
| No     |       92.65 |        92.93 | +7.07 / −92.93   | 0.08×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 7.34    | -3.02    | -7.016327838535908  |
| GB / N         | NEG      | 92.66   | -0.27    | -4.269522161464112  |
| ST / Y         | NEG      | 4.98    | -5.38    | -9.385              |
| ST / N         | WEAK     | 95.03   | 2.10     | -1.9008500000000095 |
| MX / Y         | NEG      | 7.23    | -3.13    | -7.129375000000001  |
| MX / N         | NEG      | 92.77   | -0.16    | -4.156475000000015  |
| M10 / Y        | NEG      | 8.31    | -2.05    | -6.051770833333333  |
| M10 / N        | NEG      | 91.69   | -1.23    | -5.2340791666666835 |
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
| Yes    |        5.64 |         5.85 | +94.15 / −5.85   | 16.09×        |
| No     |       97.66 |        97.75 | +2.25 / −97.75   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.68    | -4.17    | -7.853000000000001  |
| GB / N         | WEAK     | 98.32   | 0.57     | -3.4318948234330793 |
| ST / Y         | NEG      | 0.81    | -5.04    | -7.853000000000001  |
| ST / N         | WEAK     | 99.19   | 1.44     | -2.5623000000000062 |
| MX / Y         | NEG      | 2.08    | -3.77    | -7.773104166666666  |
| MX / N         | WEAK     | 97.92   | 0.17     | -3.829695833333335  |
| M10 / Y        | NEG      | 2.54    | -3.32    | -7.316645833333333  |
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
| Yes    |        3.78 |         3.93 | +96.07 / −3.93   | 24.46×        |
| No     |       99.5  |        99.52 | +0.48 / −99.52   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.24    | -3.68    | -5.928180000000001  |
| GB / N         | WEAK     | 99.76   | 0.24     | -3.7645939105122816 |
| ST / Y         | NEG      | 0.16    | -3.77    | -5.928180000000001  |
| ST / N         | WEAK     | 99.84   | 0.32     | -3.6761500000000003 |
| MX / Y         | NEG      | 0.55    | -3.37    | -5.928180000000001  |
| MX / N         | NEG      | 99.45   | -0.07    | -4.07422291666667   |
| M10 / Y        | NEG      | 0.70    | -3.23    | -5.928180000000001  |
| M10 / N        | NEG      | 99.30   | -0.22    | -4.217295833333335  |
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
| Yes    |          16 |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |          85 |        85.51 | +14.49 / −85.51  | 0.17×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 29.89   | 13.35    | 9.353264716252843   |
| GB / N         | NEG      | 70.11   | -15.40   | -19.40086471625285  |
| ST / Y         | GO       | 34.44   | 17.90    | 13.899899999999995  |
| ST / N         | NEG      | 65.56   | -19.95   | -23.947500000000012 |
| MX / Y         | GO       | 27.45   | 10.92    | 6.915837499999997   |
| MX / N         | NEG      | 72.55   | -12.96   | -16.963437500000012 |
| M10 / Y        | GO       | 28.49   | 11.95    | 7.951774999999997   |
| M10 / N        | NEG      | 71.51   | -14.00   | -17.999375000000008 |
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
| Yes    |        5.9  |         6.12 | +93.88 / −6.12   | 15.35×        |
| No     |       97.46 |        97.56 | +2.44 / −97.56   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | NEG      | 4.04    | -2.08    | -6.082084989445572 |
| GB / N         | NEG      | 95.96   | -1.60    | -5.596005010554439 |
| ST / Y         | NEG      | 2.08    | -4.03    | -8.033225          |
| ST / N         | WEAK     | 97.92   | 0.36     | -3.644865000000019 |
| MX / Y         | NEG      | 2.92    | -3.20    | -7.198277083333334 |
| MX / N         | NEG      | 97.08   | -0.48    | -4.479812916666681 |
| M10 / Y        | NEG      | 3.35    | -2.77    | -6.769422916666667 |
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
| Yes    |        5.28 |         5.48 | +94.52 / −5.48   | 17.25×        |
| No     |       99.47 |        99.49 | +0.51 / −99.49   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.54    | -4.94    | -7.479430000000001  |
| GB / N         | NEG      | 99.46   | -0.03    | -4.032113348139577  |
| ST / Y         | NEG      | 0.26    | -5.22    | -7.479430000000001  |
| ST / N         | WEAK     | 99.74   | 0.25     | -3.7476349999999936 |
| MX / Y         | NEG      | 0.44    | -5.04    | -7.479430000000001  |
| MX / N         | WEAK     | 99.56   | 0.07     | -3.929978749999996  |
| M10 / Y        | NEG      | 0.51    | -4.97    | -7.479430000000001  |
| M10 / N        | WEAK     | 99.49   | 0.00     | -3.997635           |
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
| Yes    |         5.7 |         5.92 | +94.08 / −5.92   | 15.90×        |
| No     |        99.5 |        99.52 | +0.48 / −99.52   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.04    | -5.88    | -7.9183             |
| GB / N         | WEAK     | 99.96   | 0.44     | -3.558586705563871  |
| ST / Y         | NEG      | 0.02    | -5.90    | -7.9183             |
| ST / N         | WEAK     | 99.98   | 0.46     | -3.535524999999995  |
| MX / Y         | NEG      | 0.06    | -5.86    | -7.9183             |
| MX / N         | WEAK     | 99.94   | 0.42     | -3.577347916666662  |
| M10 / Y        | NEG      | 0.08    | -5.84    | -7.9183             |
| M10 / N        | WEAK     | 99.92   | 0.40     | -3.5969312500000017 |
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
| Yes    |          15 |        15.51 | +84.49 / −15.51  | 5.45×         |
| No     |          86 |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 22.61   | 7.10     | 3.1015456279348954  |
| GB / N         | NEG      | 77.39   | -9.09    | -13.093145627934899 |
| ST / Y         | GO       | 24.98   | 9.47     | 5.471250000000002   |
| ST / N         | NEG      | 75.02   | -11.46   | -15.462850000000008 |
| MX / Y         | GO       | 22.08   | 6.57     | 2.565156250000003   |
| MX / N         | NEG      | 77.92   | -8.56    | -12.556756250000012 |
| M10 / Y        | WEAK     | 18.37   | 2.86     | -1.1425520833333314 |
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
| Yes    |        6.03 |         6.25 | +93.75 / −6.25   | 15.00×        |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.03    | -6.22    | -8.250960000000001  |
| GB / N         | WEAK     | 99.97   | 0.36     | -3.6426365741092814 |
| ST / Y         | NEG      | 0.03    | -6.22    | -8.250960000000001  |
| ST / N         | WEAK     | 99.97   | 0.35     | -3.647189999999989  |
| MX / Y         | NEG      | 0.11    | -6.14    | -8.250960000000001  |
| MX / N         | WEAK     | 99.89   | 0.27     | -3.727971249999984  |
| M10 / Y        | NEG      | 0.21    | -6.04    | -8.250960000000001  |
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
| Yes    |       11.38 |        11.78 | +88.22 / −11.78  | 7.49×         |
| No     |       89    |        89.39 | +10.61 / −89.39  | 0.12×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 13.56   | 1.77     | -2.225324773076269  |
| GB / N         | NEG      | 86.44   | -2.95    | -6.949665226923729  |
| ST / Y         | WEAK     | 12.10   | 0.32     | -3.6802650000000003 |
| ST / N         | NEG      | 87.90   | -1.49    | -5.494725000000001  |
| MX / Y         | WEAK     | 13.83   | 2.04     | -1.955733750000001  |
| MX / N         | NEG      | 86.17   | -3.22    | -7.2192562499999955 |
| M10 / Y        | WEAK     | 13.69   | 1.91     | -2.0926608333333334 |
| M10 / N        | NEG      | 86.31   | -3.08    | -7.082329166666669  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Texas Senate election by 6%-9%?
Contract 3344138; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        5.44 |         5.65 | +94.35 / −5.65   | 16.71×        |
| No     |       95.48 |        95.65 | +4.35 / −95.65   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 5.87    | 0.23     | -3.7731804110406095 |
| GB / N         | NEG      | 94.13   | -1.52    | -5.523529588959386  |
| ST / Y         | NEG      | 3.89    | -1.76    | -5.758259999999998  |
| ST / N         | WEAK     | 96.11   | 0.46     | -3.538449999999993  |
| MX / Y         | NEG      | 5.55    | -0.10    | -4.098884999999999  |
| MX / N         | NEG      | 94.45   | -1.20    | -5.197824999999989  |
| M10 / Y        | NEG      | 5.47    | -0.17    | -4.173884999999999  |
| M10 / N        | NEG      | 94.53   | -1.12    | -5.122824999999997  |
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
| Yes    |        9.84 |        10.17 | +89.83 / −10.17  | 8.83×         |
| No     |       98.3  |        98.37 | +1.63 / −98.37   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.76    | -8.41    | -12.1748            |
| GB / N         | NEG      | 98.24   | -0.13    | -4.126846062794343  |
| ST / Y         | NEG      | 0.80    | -9.38    | -12.1748            |
| ST / N         | WEAK     | 99.20   | 0.84     | -3.1637150000000003 |
| MX / Y         | NEG      | 1.61    | -8.57    | -12.1748            |
| MX / N         | WEAK     | 98.39   | 0.03     | -3.9746524999999973 |
| M10 / Y        | NEG      | 1.57    | -8.60    | -12.1748            |
| M10 / N        | WEAK     | 98.43   | 0.06     | -3.9417358333333374 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Virginia Senate election by 3% or more?
Contract 3344160; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        0.72 |         0.75 | +99.25 / −0.75   | 132.96×       |
| No     |       99.8  |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.15    | -0.59    | -2.74648            |
| GB / N         | WEAK     | 99.85   | 0.04     | -3.9620026260141827 |
| ST / Y         | NEG      | 0.26    | -0.48    | -2.74648            |
| ST / N         | NEG      | 99.74   | -0.07    | -4.070479999999998  |
| MX / Y         | NEG      | 0.69    | -0.05    | -2.74648            |
| MX / N         | NEG      | 99.31   | -0.50    | -4.502407083333337  |
| M10 / Y        | NEG      | 0.68    | -0.07    | -2.74648            |
| M10 / N        | NEG      | 99.32   | -0.49    | -4.486209166666666  |
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
| Yes    |         0.9 |         0.94 | +99.06 / −0.94   | 105.87×       |
| No     |        99.5 |        99.52 | +0.48 / −99.52   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.00    | -0.94    | -2.9356799999999996 |
| GB / N         | WEAK     | 100.00  | 0.48     | -3.519899999999998  |
| ST / Y         | NEG      | 0.00    | -0.94    | -2.9356799999999996 |
| ST / N         | WEAK     | 100.00  | 0.48     | -3.519899999999998  |
| MX / Y         | NEG      | 0.00    | -0.94    | -2.9356799999999996 |
| MX / N         | WEAK     | 100.00  | 0.48     | -3.519899999999998  |
| M10 / Y        | NEG      | 0.00    | -0.94    | -2.9356799999999996 |
| M10 / N        | WEAK     | 100.00  | 0.48     | -3.519899999999998  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | WEAK     | 3.09    | 2.15     | -1.8498800000000002 |
| DDHQ / N       | NEG      | 96.91   | -2.61    | -6.605700000000002  |

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

## Will the Republican Party hold exactly 54 Senate seats after the 2026 midterm elections?
Contract 943826; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.51 |         2.61 | +97.39 / −2.61   | 37.31×        |
| No     |       98.46 |        98.52 | +1.48 / −98.52   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | NEG      | 0.27    | -2.34    | -4.60999           |
| GB / N         | WEAK     | 99.73   | 1.21     | -2.790649999999994 |
| ST / Y         | NEG      | 0.13    | -2.48    | -4.60999           |
| ST / N         | WEAK     | 99.87   | 1.35     | -2.648774999999992 |
| MX / Y         | NEG      | 0.23    | -2.38    | -4.60999           |
| MX / N         | WEAK     | 99.77   | 1.25     | -2.745910416666641 |
| M10 / Y        | NEG      | 0.29    | -2.32    | -4.60999           |
| M10 / N        | WEAK     | 99.71   | 1.19     | -2.810597916666635 |
| RTWH / Y       | N/A      | —       | —        | —                  |
| RTWH / N       | N/A      | —       | —        | —                  |
| DDHQ / Y       | WEAK     | 4.72    | 2.11     | -1.88789           |
| DDHQ / N       | NEG      | 95.28   | -3.24    | -7.242749999999988 |

RTWH (2026-09-25): Publisher supplies no seat-count distribution; expected seats cannot price this contract.
DDHQ (2026-09-25): Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party hold exactly 55 Senate seats after the 2026 midterm elections?
Contract 943827; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         0.9 |         0.94 | +99.06 / −0.94   | 105.87×       |
| No     |        99.8 |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.02    | -0.92    | -2.9356799999999996 |
| GB / N         | WEAK     | 99.98   | 0.17     | -3.827979999999998  |
| ST / Y         | NEG      | 0.03    | -0.91    | -2.9356799999999996 |
| ST / N         | WEAK     | 99.98   | 0.17     | -3.8329799999999974 |
| MX / Y         | NEG      | 0.03    | -0.91    | -2.9356799999999996 |
| MX / N         | WEAK     | 99.97   | 0.17     | -3.8348029166666686 |
| M10 / Y        | NEG      | 0.05    | -0.89    | -2.9356799999999996 |
| M10 / N        | WEAK     | 99.95   | 0.14     | -3.8551154166666657 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | WEAK     | 3.32    | 2.38     | -1.6194800000000003 |
| DDHQ / N       | NEG      | 96.68   | -3.12    | -7.124180000000003  |

RTWH (2026-09-25): Publisher supplies no seat-count distribution; expected seats cannot price this contract.
DDHQ (2026-09-25): Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party hold exactly 56 Senate seats after the 2026 midterm elections?
Contract 943828; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        0.3  |         0.31 | +99.69 / −0.31   | 319.55×       |
| No     |       99.89 |        99.89 | +0.11 / −99.89   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | NEG      | 0.00    | -0.31    | -2.31196           |
| GB / N         | WEAK     | 100.00  | 0.11     | -3.894390000000003 |
| ST / Y         | NEG      | 0.00    | -0.31    | -2.31196           |
| ST / N         | WEAK     | 100.00  | 0.11     | -3.894390000000003 |
| MX / Y         | NEG      | 0.00    | -0.31    | -2.31196           |
| MX / N         | WEAK     | 100.00  | 0.10     | -3.896056666666669 |
| M10 / Y        | NEG      | 0.00    | -0.31    | -2.31196           |
| M10 / N        | WEAK     | 100.00  | 0.10     | -3.89850458333334  |
| RTWH / Y       | N/A      | —       | —        | —                  |
| RTWH / N       | N/A      | —       | —        | —                  |
| DDHQ / Y       | WEAK     | 2.22    | 1.91     | -2.09476           |
| DDHQ / N       | NEG      | 97.78   | -2.11    | -6.11159           |

RTWH (2026-09-25): Publisher supplies no seat-count distribution; expected seats cannot price this contract.
DDHQ (2026-09-25): Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Alabama Senate race in 2026?
Contract 630628; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       98.56 |        98.62 | +1.38 / −98.62   | 0.01×         |
| No     |        4.96 |         5.15 | +94.85 / −5.15   | 18.41×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.94 |     1.32 |        -2.68 |
| GB / N         | NEG      |    0.06 |    -5.09 |        -7.15 |
| ST / Y         | WEAK     |   99.85 |     1.23 |        -2.77 |
| ST / N         | NEG      |    0.15 |    -5.00 |        -7.15 |
| MX / Y         | NEG      |   98.46 |    -0.15 |        -4.15 |
| MX / N         | NEG      |    1.54 |    -3.62 |        -7.15 |
| M10 / Y        | NEG      |   98.54 |    -0.08 |        -4.08 |
| M10 / N        | NEG      |    1.46 |    -3.69 |        -7.15 |
| RTWH / Y       | WEAK     |   98.90 |     0.28 |        -3.72 |
| RTWH / N       | NEG      |    1.10 |    -4.05 |        -7.15 |
| DDHQ / Y       | NEG      |   95.00 |    -3.62 |        -7.62 |
| DDHQ / N       | NEG      |    5.00 |    -0.15 |        -4.15 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Arkansas Senate race in 2026?
Contract 630654; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        95.5 |        95.68 | +4.32 / −95.68   | 0.05×         |
| No     |         5.9 |         6.12 | +93.88 / −6.12   | 15.33×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   99.76 |     4.08 |         0.08 |
| GB / N         | NEG      |    0.24 |    -5.88 |        -8.12 |
| ST / Y         | WEAK     |   99.21 |     3.54 |        -0.46 |
| ST / N         | NEG      |    0.79 |    -5.33 |        -8.12 |
| MX / Y         | NEG      |   93.36 |    -2.31 |        -6.31 |
| MX / N         | WEAK     |    6.64 |     0.51 |        -3.49 |
| M10 / Y        | NEG      |   94.22 |    -1.45 |        -5.45 |
| M10 / N        | NEG      |    5.78 |    -0.35 |        -4.35 |
| RTWH / Y       | WEAK     |   98.00 |     2.32 |        -1.68 |
| RTWH / N       | NEG      |    2.00 |    -4.12 |        -8.12 |
| DDHQ / Y       | WEAK     |   96.00 |     0.32 |        -3.68 |
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
| Yes    |        2    |         2.08 | +97.92 / −2.08   | 47.11×        |
| No     |       99.43 |        99.46 | +0.54 / −99.46   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG*     |    0.05 |    -2.03 |        -4.08 |
| GB / N         | WEAK*    |   99.95 |     0.49 |        -3.51 |
| ST / Y         | NEG*     |    0.38 |    -1.70 |        -4.08 |
| ST / N         | WEAK*    |   99.62 |     0.17 |        -3.83 |
| MX / Y         | NEG*     |    0.43 |    -1.65 |        -4.08 |
| MX / N         | WEAK*    |   99.57 |     0.11 |        -3.89 |
| M10 / Y        | NEG*     |    0.54 |    -1.54 |        -4.08 |
| M10 / N        | WEAK*    |   99.46 |     0.00 |        -4.00 |
| RTWH / Y       | NEG      |    2.00 |    -0.08 |        -4.08 |
| RTWH / N       | NEG      |   98.00 |    -1.46 |        -5.46 |
| DDHQ / Y       | NEG      |    1.00 |    -1.08 |        -4.08 |
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
| Yes    |        5.7  |         5.92 | +94.08 / −5.92   | 15.91×        |
| No     |       94.96 |        95.15 | +4.85 / −95.15   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO*      |   12.68 |     6.77 |         2.77 |
| GB / N         | NEG*     |   87.32 |    -7.83 |       -11.83 |
| ST / Y         | WEAK*    |    8.14 |     2.22 |        -1.78 |
| ST / N         | NEG*     |   91.86 |    -3.28 |        -7.28 |
| MX / Y         | GO*      |   11.43 |     5.51 |         1.51 |
| MX / N         | NEG*     |   88.57 |    -6.57 |       -10.57 |
| M10 / Y        | GO*      |   12.09 |     6.18 |         2.18 |
| M10 / N        | NEG*     |   87.91 |    -7.24 |       -11.24 |
| RTWH / Y       | NEG      |    5.60 |    -0.32 |        -4.32 |
| RTWH / N       | NEG      |   94.40 |    -0.75 |        -4.75 |
| DDHQ / Y       | GO       |   13.00 |     7.08 |         3.09 |
| DDHQ / N       | NEG      |   87.00 |    -8.15 |       -12.15 |

GB, ST, MX, M10: Runoff transfers and turnout are not separately modeled; the modeled margin is used as a proxy for the eventual winner.
RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Idaho Senate race in 2026?
Contract 630706; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        91.1 |        91.42 | +8.58 / −91.42   | 0.09×         |
| No     |        10.6 |        10.98 | +89.02 / −10.98  | 8.11×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO*      |   99.95 |     8.52 |         4.52 |
| GB / N         | NEG*     |    0.05 |   -10.93 |       -12.98 |
| ST / Y         | GO*      |   99.68 |     8.26 |         4.26 |
| ST / N         | NEG*     |    0.32 |   -10.66 |       -12.98 |
| MX / Y         | GO*      |   99.76 |     8.33 |         4.33 |
| MX / N         | NEG*     |    0.24 |   -10.74 |       -12.98 |
| M10 / Y        | GO*      |   99.61 |     8.19 |         4.19 |
| M10 / N        | NEG*     |    0.39 |   -10.59 |       -12.98 |
| RTWH / Y       | GO       |   95.80 |     4.38 |         0.38 |
| RTWH / N       | NEG      |    4.20 |    -6.78 |       -10.78 |
| DDHQ / Y       | GO       |   97.00 |     5.58 |         1.58 |
| DDHQ / N       | NEG      |    3.00 |    -7.98 |       -11.98 |

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
| Yes    |          34 |        34.9  | +65.10 / −34.90  | 1.87×         |
| No     |          67 |        67.88 | +32.12 / −67.88  | 0.47×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG*     |    7.45 |   -27.45 |       -31.45 |
| GB / N         | GO*      |   92.55 |    24.67 |        20.67 |
| ST / Y         | NEG*     |    6.37 |   -28.53 |       -32.53 |
| ST / N         | GO*      |   93.63 |    25.75 |        21.75 |
| MX / Y         | NEG*     |   14.46 |   -20.44 |       -24.44 |
| MX / N         | GO*      |   85.54 |    17.66 |        13.66 |
| M10 / Y        | NEG*     |   17.06 |   -17.84 |       -21.84 |
| M10 / N        | GO*      |   82.94 |    15.06 |        11.06 |
| RTWH / Y       | WEAK     |   37.80 |     2.90 |        -1.10 |
| RTWH / N       | NEG      |   62.20 |    -5.68 |        -9.68 |
| DDHQ / Y       | GO       |   46.00 |    11.10 |         7.10 |
| DDHQ / N       | NEG      |   54.00 |   -13.88 |       -17.88 |

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
| Yes    |       15    |        15.51 | +84.49 / −15.51  | 5.45×         |
| No     |       86.13 |        86.61 | +13.39 / −86.61  | 0.15×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    2.07 |   -13.44 |       -17.44 |
| GB / N         | GO       |   97.93 |    11.32 |         7.32 |
| ST / Y         | NEG      |    2.42 |   -13.09 |       -17.09 |
| ST / N         | GO       |   97.58 |    10.97 |         6.97 |
| MX / Y         | NEG      |    7.23 |    -8.28 |       -12.28 |
| MX / N         | GO       |   92.77 |     6.16 |         2.16 |
| M10 / Y        | NEG      |    6.12 |    -9.39 |       -13.39 |
| M10 / N        | GO       |   93.88 |     7.27 |         3.27 |
| RTWH / Y       | NEG      |   13.80 |    -1.71 |        -5.71 |
| RTWH / N       | NEG      |   86.20 |    -0.41 |        -4.41 |
| DDHQ / Y       | WEAK     |   19.00 |     3.49 |        -0.51 |
| DDHQ / N       | NEG      |   81.00 |    -5.61 |        -9.61 |

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
| Yes    |        3.2  |         3.32 | +96.68 / −3.32   | 29.09×        |
| No     |       99.17 |        99.2  | +0.80 / −99.20   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.90 |    -1.43 |        -5.32 |
| GB / N         | NEG      |   98.10 |    -1.10 |        -5.10 |
| ST / Y         | NEG      |    0.93 |    -2.39 |        -5.32 |
| ST / N         | NEG      |   99.07 |    -0.13 |        -4.13 |
| MX / Y         | NEG      |    1.81 |    -1.52 |        -5.32 |
| MX / N         | NEG      |   98.19 |    -1.01 |        -5.01 |
| M10 / Y        | NEG      |    1.85 |    -1.48 |        -5.32 |
| M10 / N        | NEG      |   98.15 |    -1.05 |        -5.05 |
| RTWH / Y       | NEG      |    0.70 |    -2.62 |        -5.32 |
| RTWH / N       | WEAK     |   99.30 |     0.10 |        -3.90 |
| DDHQ / Y       | WEAK     |    4.00 |     0.68 |        -3.32 |
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
| Yes    |       98.13 |        98.21 | +1.79 / −98.21   | 0.02×         |
| No     |        2.7  |         2.81 | +97.19 / −2.81   | 34.65×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.99 |     1.79 |        -2.21 |
| GB / N         | NEG      |    0.01 |    -2.80 |        -4.81 |
| ST / Y         | WEAK     |   99.99 |     1.78 |        -2.22 |
| ST / N         | NEG      |    0.01 |    -2.80 |        -4.81 |
| MX / Y         | WEAK     |   99.94 |     1.73 |        -2.27 |
| MX / N         | NEG      |    0.06 |    -2.75 |        -4.81 |
| M10 / Y        | WEAK     |   99.96 |     1.75 |        -2.25 |
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
| Yes    |         1.8 |         1.87 | +98.13 / −1.87   | 52.56×        |
| No     |        99.6 |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.01 |    -1.86 |        -3.87 |
| GB / N         | WEAK     |   99.99 |     0.38 |        -3.62 |
| ST / Y         | NEG      |    0.01 |    -1.86 |        -3.87 |
| ST / N         | WEAK     |   99.99 |     0.37 |        -3.63 |
| MX / Y         | NEG      |    0.15 |    -1.72 |        -3.87 |
| MX / N         | WEAK     |   99.85 |     0.24 |        -3.76 |
| M10 / Y        | NEG      |    0.18 |    -1.68 |        -3.87 |
| M10 / N        | WEAK     |   99.82 |     0.20 |        -3.80 |
| RTWH / Y       | NEG      |    1.10 |    -0.77 |        -3.87 |
| RTWH / N       | NEG      |   98.90 |    -0.72 |        -4.72 |
| DDHQ / Y       | NEG      |    1.00 |    -0.87 |        -3.87 |
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
| No     |        6.35 |         6.58 | +93.42 / −6.58   | 14.19×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO*      |   99.94 |     5.42 |         1.42 |
| GB / N         | NEG*     |    0.06 |    -6.52 |        -8.58 |
| ST / Y         | GO*      |   99.18 |     4.66 |         0.66 |
| ST / N         | NEG*     |    0.82 |    -5.76 |        -8.58 |
| MX / Y         | NEG*     |   91.88 |    -2.64 |        -6.64 |
| MX / N         | WEAK*    |    8.12 |     1.54 |        -2.46 |
| M10 / Y        | NEG*     |   92.85 |    -1.66 |        -5.66 |
| M10 / N        | WEAK*    |    7.15 |     0.57 |        -3.43 |
| RTWH / Y       | NEG      |   87.10 |    -7.42 |       -11.42 |
| RTWH / N       | GO       |   12.90 |     6.32 |         2.32 |
| DDHQ / Y       | WEAK     |   97.00 |     2.48 |        -1.52 |
| DDHQ / N       | NEG      |    3.00 |    -3.58 |        -7.58 |

GB, ST, MX, M10: The strongest D/Independent-versus-R margin approximates the winning side; third-candidate outcomes are not jointly modeled. Independents remain IND.
RTWH (2026-09-25): Bengs retains IND despite publisher column. Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Tennessee Senate race in 2026?
Contract 630951; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        97.2 |        97.31 | +2.69 / −97.31   | 0.03×         |
| No     |         3.7 |         3.84 | +96.16 / −3.84   | 25.02×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.97 |     2.66 |        -1.34 |
| GB / N         | NEG      |    0.03 |    -3.82 |        -5.84 |
| ST / Y         | WEAK     |   99.98 |     2.67 |        -1.33 |
| ST / N         | NEG      |    0.02 |    -3.82 |        -5.84 |
| MX / Y         | WEAK     |   99.92 |     2.61 |        -1.39 |
| MX / N         | NEG      |    0.08 |    -3.76 |        -5.84 |
| M10 / Y        | WEAK     |   99.95 |     2.64 |        -1.36 |
| M10 / N        | NEG      |    0.05 |    -3.80 |        -5.84 |
| RTWH / Y       | WEAK     |   99.00 |     1.69 |        -2.31 |
| RTWH / N       | NEG      |    1.00 |    -2.84 |        -5.84 |
| DDHQ / Y       | NEG      |   97.00 |    -0.31 |        -4.31 |
| DDHQ / N       | NEG      |    3.00 |    -0.84 |        -4.84 |

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
| Yes    |         2.9 |         3.01 | +96.99 / −3.01   | 32.19×        |
| No     |        99.7 |        99.71 | +0.29 / −99.71   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.57 |    -2.45 |        -5.01 |
| GB / N         | NEG      |   99.43 |    -0.28 |        -4.28 |
| ST / Y         | NEG      |    0.59 |    -2.43 |        -5.01 |
| ST / N         | NEG      |   99.41 |    -0.30 |        -4.30 |
| MX / Y         | NEG      |    1.52 |    -1.49 |        -5.01 |
| MX / N         | NEG      |   98.48 |    -1.23 |        -5.23 |
| M10 / Y        | NEG      |    1.48 |    -1.53 |        -5.01 |
| M10 / N        | NEG      |   98.52 |    -1.19 |        -5.19 |
| RTWH / Y       | NEG      |    1.90 |    -1.11 |        -5.01 |
| RTWH / N       | NEG      |   98.10 |    -1.61 |        -5.61 |
| DDHQ / Y       | WEAK     |    4.00 |     0.99 |        -3.01 |
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

