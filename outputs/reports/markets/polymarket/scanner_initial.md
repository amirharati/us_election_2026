# All model-market pairs grouped by market

Y = buy Yes; N = buy No. P = model probability that the selected side pays $1 under the contract condition; it is not confidence that the model is correct. EV = base expected net profit after purchase depth and estimated fees. Budget and win/loss payoffs use those base costs. Stress adds the extra friction scenario and applies the probability haircut to the model probability. GO (green) survives stress; WEAK (amber) is positive before stress only; UNC (amber) is unresolved; NEG (red) is negative in expectation; N/A (gray) is unavailable. Local P comes from the full predictive distribution. External P is a published point estimate or seat-histogram probability; equal endpoints are not a confidence interval. Simulation estimates have sampling error. All model rows are independent comparisons; there is no combined score.

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

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | N/A      | —       | —        | —                  |
| GB / N         | N/A      | —       | —        | —                  |
| ST / Y         | N/A      | —       | —        | —                  |
| ST / N         | N/A      | —       | —        | —                  |
| MX / Y         | N/A      | —       | —        | —                  |
| MX / N         | N/A      | —       | —        | —                  |
| M10 / Y        | N/A      | —       | —        | —                  |
| M10 / N        | N/A      | —       | —        | —                  |
| RTWH / Y       | GO       | 12.90   | 7.92     | 3.9172200000000004 |
| RTWH / N       | NEG      | 87.10   | -9.05    | -13.0536           |
| DDHQ / Y       | NEG      | 3.00    | -1.98    | -5.98278           |
| DDHQ / N       | WEAK     | 97.00   | 0.85     | -3.153600000000001 |

RTWH (2026-09-25): Bengs retains IND despite publisher column. Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will Dan Sullivan win the Alaska Senate race in 2026?
Contract 634974; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          29 |        29.82 | +70.18 / −29.82  | 2.35×         |
| No     |          72 |        72.81 | +27.19 / −72.81  | 0.37×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | N/A      | —       | —        | —                  |
| GB / N         | N/A      | —       | —        | —                  |
| ST / Y         | N/A      | —       | —        | —                  |
| ST / N         | N/A      | —       | —        | —                  |
| MX / Y         | N/A      | —       | —        | —                  |
| MX / N         | N/A      | —       | —        | —                  |
| M10 / Y        | N/A      | —       | —        | —                  |
| M10 / N        | N/A      | —       | —        | —                  |
| RTWH / Y       | GO       | 43.40   | 13.58    | 9.576400000000001  |
| RTWH / N       | NEG      | 56.60   | -16.21   | -20.20639999999999 |
| DDHQ / Y       | N/A      | —       | —        | —                  |
| DDHQ / N       | N/A      | —       | —        | —                  |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Requested party/candidate has no published probability; absence is not treated as zero.

## Will Mary Peltola win the Alaska Senate race in 2026?
Contract 634976; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          73 |        73.79 | +26.21 / −73.79  | 0.36×         |
| No     |          28 |        28.81 | +71.19 / −28.81  | 2.47×         |

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
| RTWH / Y       | NEG      | 56.60   | -17.19   | -21.18839999999999  |
| RTWH / N       | GO       | 43.40   | 14.59    | 10.593599999999986  |
| DDHQ / Y       | NEG      | 61.00   | -12.79   | -16.788400000000003 |
| DDHQ / N       | GO       | 39.00   | 10.19    | 6.193599999999993   |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Publisher party aggregate covers multiple candidates and is not assigned to an individual. Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will Todd Achilles win the Idaho Senate race in 2026?
Contract 630707; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.39 |         9.73 | +90.27 / −9.73   | 9.28×         |
| No     |       96.49 |        96.63 | +3.37 / −96.63   | 0.03×         |

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
| RTWH / Y       | NEG      | 4.20    | -5.53    | -9.530330000000001  |
| RTWH / N       | NEG      | 95.80   | -0.83    | -4.82547000000001   |
| DDHQ / Y       | NEG      | 3.00    | -6.73    | -10.730330000000002 |
| DDHQ / N       | WEAK     | 97.00   | 0.37     | -3.6254700000000084 |

RTWH (2026-09-25): Achilles retains IND despite publisher column. Publisher omits separate probabilities for reviewed contenders: Natalie Fleming. Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Publisher omits separate probabilities for reviewed contenders: Natalie Fleming. Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will an Independent win the Montana Senate race in 2026?
Contract 630833; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10.4  |        10.77 | +89.23 / −10.77  | 8.28×         |
| No     |       90.71 |        91.05 | +8.95 / −91.05   | 0.10×         |

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
| RTWH / Y       | GO       | 22.10   | 11.33    | 7.3272600000000025  |
| RTWH / N       | NEG      | 77.90   | -13.15   | -17.149369999999998 |
| DDHQ / Y       | NEG      | 10.00   | -0.77    | -4.772739999999999  |
| DDHQ / N       | NEG      | 90.00   | -1.05    | -5.049369999999998  |

RTWH (2026-09-25): Publisher omits separate probabilities for reviewed contenders: Alani Bankhead. Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Publisher omits separate probabilities for reviewed contenders: Alani Bankhead. Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will an independent win the Nebraska Senate race in 2026?
Contract 634893; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          31 |        31.86 | +68.14 / −31.86  | 2.14×         |
| No     |          70 |        70.84 | +29.16 / −70.84  | 0.41×         |

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
| RTWH / Y       | GO       | 36.00   | 4.14     | 0.14439999999999453 |
| RTWH / N       | NEG      | 64.00   | -6.84    | -10.840000000000005 |
| DDHQ / Y       | NEG      | 17.00   | -14.86   | -18.8556            |
| DDHQ / N       | GO       | 83.00   | 12.16    | 8.15999999999999    |

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
| Yes    |       20.64 |        21.29 | +78.71 / −21.29  | 3.70×         |
| No     |       81    |        81.62 | +18.38 / −81.62  | 0.23×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 16.65   | -4.65    | -8.648853140444718  |
| GB / N         | WEAK     | 83.35   | 1.74     | -2.2610868595552835 |
| ST / Y         | NEG      | 18.59   | -2.71    | -6.706839999999997  |
| ST / N         | NEG      | 81.41   | -0.20    | -4.2031000000000045 |
| MX / Y         | NEG      | 17.54   | -3.76    | -7.758194166666666  |
| MX / N         | WEAK     | 82.46   | 0.85     | -3.151745833333342  |
| M10 / Y        | NEG      | 17.04   | -4.25    | -8.251006666666665  |
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
| Yes    |       10.51 |        10.88 | +89.12 / −10.88  | 8.19×         |
| No     |       96.82 |        96.95 | +3.05 / −96.95   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.88    | -10.00   | -12.88482           |
| GB / N         | WEAK     | 99.12   | 2.17     | -1.828283046147483  |
| ST / Y         | NEG      | 0.34    | -10.54   | -12.88482           |
| ST / N         | WEAK     | 99.66   | 2.71     | -1.2859350000000047 |
| MX / Y         | NEG      | 1.02    | -9.87    | -12.88482           |
| MX / N         | WEAK     | 98.98   | 2.04     | -1.9626537499999985 |
| M10 / Y        | NEG      | 0.92    | -9.96    | -12.88482           |
| M10 / N        | WEAK     | 99.08   | 2.13     | -1.8670287499999996 |
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

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 15%-20%?
Contract 3343811; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         2.8 |         2.91 | +97.09 / −2.91   | 33.38×        |
| No     |        98   |        98.08 | +1.92 / −98.08   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 10.84   | 7.93     | 3.9303172022441144  |
| GB / N         | NEG      | 89.16   | -8.92    | -12.917577202244113 |
| ST / Y         | GO       | 8.29    | 5.38     | 1.3786399999999999  |
| ST / N         | NEG      | 91.71   | -6.37    | -10.365899999999995 |
| MX / Y         | GO       | 11.75   | 8.84     | 4.839056666666665   |
| MX / N         | NEG      | 88.25   | -9.83    | -13.82631666666666  |
| M10 / Y        | GO       | 14.39   | 11.48    | 7.480879583333333   |
| M10 / N        | NEG      | 85.61   | -12.47   | -16.46813958333333  |
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
| No     |       89.49 |        89.87 | +10.13 / −89.87  | 0.11×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 26.64   | 12.16    | 8.160535398573735   |
| GB / N         | NEG      | 73.36   | -16.51   | -20.51280539857373  |
| ST / Y         | GO       | 26.03   | 11.55    | 7.549649999999999   |
| ST / N         | NEG      | 73.97   | -15.90   | -19.901919999999983 |
| MX / Y         | GO       | 27.23   | 12.75    | 8.749806249999997   |
| MX / N         | NEG      | 72.77   | -17.10   | -21.102076249999993 |
| M10 / Y        | GO       | 29.69   | 15.21    | 11.211368749999998  |
| M10 / N        | NEG      | 70.31   | -19.56   | -23.563638749999992 |
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
| Yes    |          19 |        19.62 | +80.38 / −19.62  | 4.10×         |
| No     |          83 |        83.56 | +16.44 / −83.56  | 0.20×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 6.19    | -13.43   | -17.42945779486262  |
| GB / N         | GO       | 93.81   | 10.25    | 6.249457794862611   |
| ST / Y         | NEG      | 4.22    | -15.40   | -19.39685           |
| ST / N         | GO       | 95.78   | 12.22    | 8.216849999999987   |
| MX / Y         | NEG      | 5.08    | -14.53   | -18.534766666666666 |
| MX / N         | GO       | 94.92   | 11.35    | 7.354766666666657   |
| M10 / Y        | NEG      | 3.70    | -15.91   | -19.91158958333333  |
| M10 / N        | GO       | 96.30   | 12.73    | 8.73158958333332    |
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
| Yes    |       15.21 |        15.73 | +84.27 / −15.73  | 5.36×         |
| No     |       90.5  |        90.84 | +9.16 / −90.84   | 0.10×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.95    | -14.78   | -17.729139999999997 |
| GB / N         | GO       | 99.05   | 8.21     | 4.210072629596418   |
| ST / Y         | NEG      | 0.39    | -15.34   | -17.729139999999997 |
| ST / N         | GO       | 99.61   | 8.76     | 4.7626100000000005  |
| MX / Y         | NEG      | 0.81    | -14.92   | -17.729139999999997 |
| MX / N         | GO       | 99.19   | 8.35     | 4.350839166666676   |
| M10 / Y        | NEG      | 0.55    | -15.18   | -17.729139999999997 |
| M10 / N        | GO       | 99.45   | 8.60     | 4.604589166666672   |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

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

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 12%-15%?
Contract 3343942; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.14 |         9.47 | +90.53 / −9.47   | 9.56×         |
| No     |       95.2  |        95.38 | +4.62 / −95.38   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 19.73   | 10.26    | 6.261135063107474   |
| GB / N         | NEG      | 80.27   | -15.11   | -19.11292506310747  |
| ST / Y         | GO       | 20.99   | 11.52    | 7.518470000000001   |
| ST / N         | NEG      | 79.01   | -16.37   | -20.370259999999995 |
| MX / Y         | GO       | 15.58   | 6.11     | 2.111178333333334   |
| MX / N         | NEG      | 84.42   | -10.96   | -14.962968333333327 |
| M10 / Y        | GO       | 16.41   | 6.94     | 2.9432095833333323  |
| M10 / N        | NEG      | 83.59   | -11.79   | -15.794999583333327 |
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
| Yes    |        8.08 |         8.37 | +91.63 / −8.37   | 10.95×        |
| No     |       98.56 |        98.62 | +1.38 / −98.62   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)           |
|:---------------|:---------|:--------|:---------|:---------------------|
| GB / Y         | WEAK     | 12.30   | 3.93     | -0.06961267025738654 |
| GB / N         | NEG      | 87.70   | -10.92   | -14.916167329742613  |
| ST / Y         | WEAK     | 9.24    | 0.87     | -3.1310300000000013  |
| ST / N         | NEG      | 90.76   | -7.85    | -11.854749999999992  |
| MX / Y         | NEG      | 7.28    | -1.08    | -5.083946666666668   |
| MX / N         | NEG      | 92.72   | -5.90    | -9.901833333333322   |
| M10 / Y        | WEAK     | 8.68    | 0.31     | -3.687175833333333   |
| M10 / N        | NEG      | 91.32   | -7.30    | -11.29860416666666   |
| RTWH / Y       | N/A      | —       | —        | —                    |
| RTWH / N       | N/A      | —       | —        | —                    |
| DDHQ / Y       | N/A      | —       | —        | —                    |
| DDHQ / N       | N/A      | —       | —        | —                    |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 3%-6%?
Contract 3343939; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       21    |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |       80.27 |        80.9  | +19.10 / −80.90  | 0.24×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 9.93    | -11.73   | -15.731893958934224 |
| GB / N         | GO       | 90.07   | 9.17     | 5.166833958934214   |
| ST / Y         | NEG      | 9.62    | -12.04   | -16.041725          |
| ST / N         | GO       | 90.38   | 9.48     | 5.476664999999992   |
| MX / Y         | NEG      | 14.00   | -7.66    | -11.65917291666667  |
| MX / N         | GO       | 86.00   | 5.09     | 1.0941129166666563  |
| M10 / Y        | NEG      | 13.04   | -8.62    | -12.618704166666667 |
| M10 / N        | GO       | 86.96   | 6.05     | 2.0536441666666683  |
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

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 12%-15%?
Contract 3343971; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.97 |        10.33 | +89.67 / −10.33  | 8.68×         |
| No     |       91.66 |        91.97 | +8.03 / −91.97   | 0.09×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 14.90   | 4.57     | 0.5695556415712372  |
| GB / N         | NEG      | 85.10   | -6.87    | -10.86653564157124  |
| ST / Y         | GO       | 16.71   | 6.38     | 2.375049999999998   |
| ST / N         | NEG      | 83.29   | -8.67    | -12.672030000000001 |
| MX / Y         | GO       | 15.45   | 5.12     | 1.1205187499999991  |
| MX / N         | NEG      | 84.55   | -7.42    | -11.41749875        |
| M10 / Y        | GO       | 15.49   | 5.15     | 1.154737499999997   |
| M10 / N        | NEG      | 84.51   | -7.45    | -11.451717500000003 |
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
| No     |          86 |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 15.54   | -1.00    | -4.999703544712824  |
| GB / N         | NEG      | 84.46   | -2.02    | -6.019496455287188  |
| ST / Y         | WEAK     | 17.72   | 1.18     | -2.8219750000000015 |
| ST / N         | NEG      | 82.28   | -4.20    | -8.197225000000008  |
| MX / Y         | NEG      | 16.12   | -0.41    | -4.4132250000000015 |
| MX / N         | NEG      | 83.88   | -2.61    | -6.605975000000008  |
| M10 / Y        | NEG      | 16.12   | -0.41    | -4.413433333333333  |
| M10 / N        | NEG      | 83.88   | -2.61    | -6.605766666666679  |
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
| Yes    |          25 |        25.75 | +74.25 / −25.75  | 2.88×         |
| No     |          77 |        77.71 | +22.29 / −77.71  | 0.29×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 13.91   | -11.84   | -15.844614129253237 |
| GB / N         | GO       | 86.09   | 8.39     | 4.386214129253229   |
| ST / Y         | NEG      | 15.55   | -10.20   | -14.203125000000002 |
| ST / N         | GO       | 84.45   | 6.74     | 2.7447249999999923  |
| MX / Y         | NEG      | 14.29   | -11.46   | -15.464375000000002 |
| MX / N         | GO       | 85.71   | 8.01     | 4.005974999999995   |
| M10 / Y        | NEG      | 14.25   | -11.50   | -15.50385416666667  |
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
| Yes    |        7.55 |         7.83 | +92.17 / −7.83   | 11.77×        |
| No     |       94.88 |        95.07 | +4.93 / −95.07   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 8.66    | 0.83     | -3.166339207354754  |
| GB / N         | NEG      | 91.34   | -3.74    | -7.736380792645248  |
| ST / Y         | WEAK     | 7.88    | 0.05     | -3.9541100000000013 |
| ST / N         | NEG      | 92.12   | -2.95    | -6.9486099999999995 |
| MX / Y         | WEAK     | 8.64    | 0.81     | -3.1925995833333345 |
| MX / N         | NEG      | 91.36   | -3.71    | -7.7101204166666655 |
| M10 / Y        | WEAK     | 8.70    | 0.87     | -3.1259329166666667 |
| M10 / N        | NEG      | 91.30   | -3.78    | -7.7767870833333355 |
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
| Yes    |        8.12 |         8.41 | +91.59 / −8.41   | 10.89×        |
| No     |       95.5  |        95.67 | +4.33 / −95.67   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)            |
|:---------------|:---------|:--------|:---------|:----------------------|
| GB / Y         | WEAK     | 12.26   | 3.85     | -0.1486509037467318   |
| GB / N         | NEG      | 87.74   | -7.94    | -11.935859096253266   |
| ST / Y         | GO       | 12.71   | 4.30     | 0.2998899999999985    |
| ST / N         | NEG      | 87.29   | -8.38    | -12.384399999999996   |
| MX / Y         | WEAK     | 12.36   | 3.94     | -0.055370416666668254 |
| MX / N         | NEG      | 87.64   | -8.03    | -12.029139583333336   |
| M10 / Y        | GO       | 12.43   | 4.02     | 0.021296250000001075  |
| M10 / N        | NEG      | 87.57   | -8.11    | -12.105806250000006   |
| RTWH / Y       | N/A      | —       | —        | —                     |
| RTWH / N       | N/A      | —       | —        | —                     |
| DDHQ / Y       | N/A      | —       | —        | —                     |
| DDHQ / N       | N/A      | —       | —        | —                     |

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

## Will the Democratic Party candidate win the 2026 North Carolina Senate election by 3%-6%?
Contract 3344034; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        16   |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |        85.4 |        85.9  | +14.10 / −85.90  | 0.16×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 23.03   | 6.49     | 2.4906914225439336  |
| GB / N         | NEG      | 76.97   | -8.93    | -12.926931422543941 |
| ST / Y         | GO       | 27.96   | 11.42    | 7.418649999999996   |
| ST / N         | NEG      | 72.04   | -13.85   | -17.85489           |
| MX / Y         | GO       | 28.21   | 11.67    | 7.672191666666664   |
| MX / N         | NEG      | 71.79   | -14.11   | -18.108431666666668 |
| M10 / Y        | GO       | 28.19   | 11.66    | 7.655837499999999   |
| M10 / N        | NEG      | 71.81   | -14.09   | -18.092077500000016 |
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
| Yes    |       18.71 |        19.32 | +80.68 / −19.32  | 4.18×         |
| No     |       87    |        87.45 | +12.55 / −87.45  | 0.14×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 14.23   | -5.09    | -9.090674274735967  |
| GB / N         | NEG      | 85.77   | -1.68    | -5.680245725264033  |
| ST / Y         | NEG      | 13.50   | -5.82    | -9.821645           |
| ST / N         | NEG      | 86.50   | -0.95    | -4.949274999999997  |
| MX / Y         | NEG      | 11.48   | -7.84    | -11.841592916666666 |
| MX / N         | WEAK     | 88.52   | 1.07     | -2.9293270833333325 |
| M10 / Y        | NEG      | 11.41   | -7.91    | -11.91055125        |
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
| No     |          80 |        80.64 | +19.36 / −80.64  | 0.24×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 20.20   | -3.50    | -7.5041260243810335 |
| GB / N         | NEG      | 79.80   | -0.84    | -4.844273975618973  |
| ST / Y         | WEAK     | 24.94   | 1.24     | -2.764650000000002  |
| ST / N         | NEG      | 75.06   | -5.58    | -9.583750000000002  |
| MX / Y         | NEG      | 21.15   | -2.56    | -6.560795833333335  |
| MX / N         | NEG      | 78.85   | -1.79    | -5.7876041666666715 |
| M10 / Y        | NEG      | 20.11   | -3.60    | -7.5958479166666715 |
| M10 / N        | NEG      | 79.89   | -0.75    | -4.752552083333339  |
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
| Yes    |        9.53 |         9.87 | +90.13 / −9.87   | 9.13×         |
| No     |       99.7  |        99.71 | +0.29 / −99.71   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.09    | -9.78    | -11.87254           |
| GB / N         | WEAK     | 99.91   | 0.20     | -3.8023471132106694 |
| ST / Y         | NEG      | 0.11    | -9.76    | -11.87254           |
| ST / N         | WEAK     | 99.89   | 0.18     | -3.8244600000000073 |
| MX / Y         | NEG      | 0.66    | -9.21    | -11.87254           |
| MX / N         | NEG      | 99.34   | -0.37    | -4.374616250000008  |
| M10 / Y        | NEG      | 0.77    | -9.10    | -11.87254           |
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
| Yes    |        1.51 |         1.57 | +98.43 / −1.57   | 62.75×        |
| No     |       99.3  |        99.33 | +0.67 / −99.33   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 4.53    | 2.96     | -1.036650191994189  |
| GB / N         | NEG      | 95.47   | -3.86    | -7.8598998080058    |
| ST / Y         | WEAK     | 3.53    | 1.96     | -2.0375             |
| ST / N         | NEG      | 96.47   | -2.86    | -6.859049999999989  |
| MX / Y         | GO       | 7.72    | 6.15     | 2.149427083333333   |
| MX / N         | NEG      | 92.28   | -7.05    | -11.045977083333325 |
| M10 / Y        | GO       | 8.45    | 6.88     | 2.878177083333333   |
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
| Yes    |        8.85 |         9.17 | +90.83 / −9.17   | 9.90×         |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 14.27   | 5.10     | 1.1009649412902376  |
| GB / N         | NEG      | 85.73   | -13.89   | -17.88934494129022  |
| ST / Y         | WEAK     | 11.22   | 2.04     | -1.9568150000000006 |
| ST / N         | NEG      | 88.78   | -10.83   | -14.83156499999998  |
| MX / Y         | GO       | 16.65   | 7.48     | 3.475476666666668   |
| MX / N         | NEG      | 83.35   | -16.26   | -20.26385666666666  |
| M10 / Y        | GO       | 17.63   | 8.46     | 4.457247500000003   |
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
| Yes    |        16.9 |        17.46 | +82.54 / −17.46  | 4.73×         |
| No     |        88.9 |        89.29 | +10.71 / −89.29  | 0.12×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 26.25   | 8.79     | 4.78686705392817    |
| GB / N         | NEG      | 73.75   | -15.54   | -19.543347053928183 |
| ST / Y         | GO       | 24.83   | 7.37     | 3.3726150000000015  |
| ST / N         | NEG      | 75.17   | -14.13   | -18.129095000000017 |
| MX / Y         | GO       | 25.32   | 7.86     | 3.8571462500000013  |
| MX / N         | NEG      | 74.68   | -14.61   | -18.613626250000014 |
| M10 / Y        | GO       | 25.88   | 8.42     | 4.415687916666664   |
| M10 / N        | NEG      | 74.12   | -15.17   | -19.172167916666684 |
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
| Yes    |       21.6  |        22.28 | +77.72 / −22.28  | 3.49×         |
| No     |       80.39 |        81.02 | +18.98 / −81.02  | 0.23×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 18.36   | -3.92    | -7.917472316586167  |
| GB / N         | WEAK     | 81.64   | 0.62     | -3.3819976834138403 |
| ST / Y         | NEG      | 19.16   | -3.12    | -7.116874999999996  |
| ST / N         | NEG      | 80.84   | -0.18    | -4.182595000000012  |
| MX / Y         | NEG      | 17.81   | -4.47    | -8.470052083333329  |
| MX / N         | WEAK     | 82.19   | 1.17     | -2.8294179166666766 |
| M10 / Y        | NEG      | 17.92   | -4.35    | -8.35479166666666   |
| M10 / N        | WEAK     | 82.08   | 1.06     | -2.9446783333333504 |
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
| Yes    |        9.11 |         9.45 | +90.55 / −9.45   | 9.59×         |
| No     |       93    |        93.26 | +6.74 / −93.26   | 0.07×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 14.02   | 4.57     | 0.570707812225224   |
| GB / N         | NEG      | 85.98   | -7.28    | -11.276257812225232 |
| ST / Y         | GO       | 14.88   | 5.44     | 1.439225000000001   |
| ST / N         | NEG      | 85.12   | -8.14    | -12.144774999999996 |
| MX / Y         | GO       | 13.61   | 4.17     | 0.16594374999999995 |
| MX / N         | NEG      | 86.39   | -6.87    | -10.871493750000006 |
| M10 / Y        | GO       | 13.54   | 4.10     | 0.09787083333333557 |
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
| Yes    |       26.8  |        27.58 | +72.42 / −27.58  | 2.63×         |
| No     |       74.58 |        75.34 | +24.66 / −75.34  | 0.33×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 16.42   | -11.17   | -15.168153620365196 |
| GB / N         | GO       | 83.58   | 8.24     | 4.242283620365184   |
| ST / Y         | NEG      | 19.27   | -8.32    | -12.31595           |
| ST / N         | GO       | 80.73   | 5.39     | 1.3900799999999935  |
| MX / Y         | NEG      | 15.59   | -12.00   | -15.999439583333332 |
| MX / N         | GO       | 84.41   | 9.07     | 5.073569583333326   |
| M10 / Y        | NEG      | 15.65   | -11.93   | -15.932929166666668 |
| M10 / N        | GO       | 84.35   | 9.01     | 5.007059166666661   |
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
| Yes    |        4.78 |         4.96 | +95.04 / −4.96   | 19.15×        |
| No     |       97.54 |        97.64 | +2.36 / −97.64   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 5.85    | 0.88     | -3.1155619335149947 |
| GB / N         | NEG      | 94.15   | -3.49    | -7.487328066484988  |
| ST / Y         | NEG      | 4.16    | -0.81    | -4.80585            |
| ST / N         | NEG      | 95.84   | -1.80    | -5.797039999999976  |
| MX / Y         | WEAK     | 5.98    | 1.02     | -2.977308333333334  |
| MX / N         | NEG      | 94.02   | -3.63    | -7.625581666666648  |
| M10 / Y        | WEAK     | 5.88    | 0.92     | -3.078402083333334  |
| M10 / N        | NEG      | 94.12   | -3.52    | -7.5244879166666445 |
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
| Yes    |        7.65 |         7.93 | +92.07 / −7.93   | 11.61×        |
| No     |       96    |        96.15 | +3.85 / −96.15   | 0.04×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | WEAK     | 9.90    | 1.97     | -2.029690332438118 |
| GB / N         | NEG      | 90.10   | -6.05    | -10.05381966756188 |
| ST / Y         | WEAK     | 8.57    | 0.64     | -3.358035000000001 |
| ST / N         | NEG      | 91.43   | -4.73    | -8.725474999999994 |
| MX / Y         | WEAK     | 9.60    | 1.67     | -2.334545416666668 |
| MX / N         | NEG      | 90.40   | -5.75    | -9.748964583333331 |
| M10 / Y        | WEAK     | 9.46    | 1.53     | -2.466993333333334 |
| M10 / N        | NEG      | 90.54   | -5.62    | -9.616516666666664 |
| RTWH / Y       | N/A      | —       | —        | —                  |
| RTWH / N       | N/A      | —       | —        | —                  |
| DDHQ / Y       | N/A      | —       | —        | —                  |
| DDHQ / N       | N/A      | —       | —        | —                  |

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
| Yes    |        3.94 |         4.1  | +95.90 / −4.10   | 23.41×        |
| No     |       99.53 |        99.55 | +0.45 / −99.55   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.06 |    -4.04 |        -6.10 |
| GB / N         | WEAK     |   99.94 |     0.39 |        -3.61 |
| ST / Y         | NEG      |    0.15 |    -3.94 |        -6.10 |
| ST / N         | WEAK     |   99.85 |     0.30 |        -3.70 |
| MX / Y         | NEG      |    1.54 |    -2.56 |        -6.10 |
| MX / N         | NEG      |   98.46 |    -1.09 |        -5.09 |
| M10 / Y        | NEG      |    1.46 |    -2.63 |        -6.10 |
| M10 / N        | NEG      |   98.54 |    -1.01 |        -5.01 |
| RTWH / Y       | NEG      |    1.10 |    -3.00 |        -6.10 |
| RTWH / N       | NEG      |   98.90 |    -0.65 |        -4.65 |
| DDHQ / Y       | WEAK     |    5.00 |     0.90 |        -3.10 |
| DDHQ / N       | NEG      |   95.00 |    -4.55 |        -8.55 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Arkansas Senate race in 2026?
Contract 630653; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        6.12 |         6.35 | +93.65 / −6.35   | 14.74×        |
| No     |       95.4  |        95.58 | +4.42 / −95.58   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.24 |    -6.11 |        -8.35 |
| GB / N         | GO       |   99.76 |     4.18 |         0.18 |
| ST / Y         | NEG      |    0.79 |    -5.57 |        -8.35 |
| ST / N         | WEAK     |   99.21 |     3.64 |        -0.36 |
| MX / Y         | WEAK     |    6.64 |     0.28 |        -3.72 |
| MX / N         | NEG      |   93.36 |    -2.21 |        -6.21 |
| M10 / Y        | NEG      |    5.78 |    -0.58 |        -4.58 |
| M10 / N        | NEG      |   94.22 |    -1.35 |        -5.35 |
| RTWH / Y       | NEG      |    2.00 |    -4.35 |        -8.35 |
| RTWH / N       | WEAK     |   98.00 |     2.42 |        -1.58 |
| DDHQ / Y       | NEG      |    4.00 |    -2.35 |        -6.35 |
| DDHQ / N       | WEAK     |   96.00 |     0.42 |        -3.58 |

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
| RTWH / Y       | NEG      | 94.40   | -0.79    | -4.789999999999994  |
| RTWH / N       | NEG      | 5.60    | -0.63    | -4.625600000000006  |
| DDHQ / Y       | NEG      | 87.00   | -8.19    | -12.190000000000003 |
| DDHQ / N       | GO       | 13.00   | 6.77     | 2.7744000000000004  |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Illinois Senate race in 2026?
Contract 630720; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       98.77 |        98.82 | +1.18 / −98.82   | 0.01×         |
| No     |        2.7  |         2.81 | +97.19 / −2.81   | 34.65×        |

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
| RTWH / Y       | NEG      | 97.50   | -1.32    | -5.3185799999999945 |
| RTWH / N       | NEG      | 2.50    | -0.31    | -4.3050799999999985 |
| DDHQ / Y       | NEG      | 96.00   | -2.82    | -6.818579999999996  |
| DDHQ / N       | WEAK     | 4.00    | 1.19     | -2.805079999999997  |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Iowa Senate race in 2026?
Contract 630733; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          45 |        45.99 | +54.01 / −45.99  | 1.17×         |
| No     |          56 |        56.99 | +43.01 / −56.99  | 0.75×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   36.18 |    -9.81 |       -13.81 |
| GB / N         | GO       |   63.82 |     6.84 |         2.84 |
| ST / Y         | NEG      |   33.44 |   -12.55 |       -16.55 |
| ST / N         | GO       |   66.56 |     9.58 |         5.58 |
| MX / Y         | NEG      |   36.92 |    -9.07 |       -13.07 |
| MX / N         | GO       |   63.08 |     6.09 |         2.09 |
| M10 / Y        | NEG      |   35.32 |   -10.67 |       -14.67 |
| M10 / N        | GO       |   64.68 |     7.70 |         3.70 |
| RTWH / Y       | GO       |   58.90 |    12.91 |         8.91 |
| RTWH / N       | NEG      |   41.10 |   -15.89 |       -19.89 |
| DDHQ / Y       | WEAK     |   49.00 |     3.01 |        -0.99 |
| DDHQ / N       | NEG      |   51.00 |    -5.99 |        -9.99 |

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
| Yes    |        4.4  |         4.57 | +95.43 / −4.57   | 20.87×        |
| No     |       96.95 |        97.07 | +2.93 / −97.07   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.88 |    -2.69 |        -6.57 |
| GB / N         | WEAK     |   98.12 |     1.05 |        -2.95 |
| ST / Y         | NEG      |    1.42 |    -3.15 |        -6.57 |
| ST / N         | WEAK     |   98.58 |     1.51 |        -2.49 |
| MX / Y         | NEG      |    3.90 |    -0.68 |        -4.68 |
| MX / N         | NEG      |   96.10 |    -0.96 |        -4.96 |
| M10 / Y        | NEG      |    2.96 |    -1.61 |        -5.61 |
| M10 / N        | NEG      |   97.04 |    -0.03 |        -4.03 |
| RTWH / Y       | NEG      |    2.10 |    -2.47 |        -6.47 |
| RTWH / N       | WEAK     |   97.90 |     0.83 |        -3.17 |
| DDHQ / Y       | WEAK     |    5.00 |     0.43 |        -3.57 |
| DDHQ / N       | NEG      |   95.00 |    -2.07 |        -6.07 |

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
| RTWH / Y       | NEG      | 62.20   | -7.66    | -11.6556            |
| RTWH / N       | GO       | 37.80   | 4.93     | 0.9296000000000026  |
| DDHQ / Y       | NEG      | 54.00   | -15.86   | -19.855599999999995 |
| DDHQ / N       | GO       | 46.00   | 13.13    | 9.129599999999998   |

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

## Will the Democrats win the New Mexico Senate race in 2026?
Contract 630870; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       97.97 |        98.05 | +1.95 / −98.05   | 0.02×         |
| No     |        3.28 |         3.41 | +96.59 / −3.41   | 28.36×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   98.10 |     0.05 |        -3.95 |
| GB / N         | NEG      |    1.90 |    -1.51 |        -5.41 |
| ST / Y         | WEAK     |   99.07 |     1.01 |        -2.99 |
| ST / N         | NEG      |    0.93 |    -2.47 |        -5.41 |
| MX / Y         | WEAK     |   98.19 |     0.14 |        -3.86 |
| MX / N         | NEG      |    1.81 |    -1.60 |        -5.41 |
| M10 / Y        | WEAK     |   98.15 |     0.10 |        -3.90 |
| M10 / N        | NEG      |    1.85 |    -1.56 |        -5.41 |
| RTWH / Y       | WEAK     |   99.30 |     1.25 |        -2.75 |
| RTWH / N       | NEG      |    0.70 |    -2.71 |        -5.41 |
| DDHQ / Y       | NEG      |   96.00 |    -2.05 |        -6.05 |
| DDHQ / N       | WEAK     |    4.00 |     0.59 |        -3.41 |

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
| No     |         3.3 |         3.43 | +96.57 / −3.43   | 28.16×        |

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
| RTWH / Y       | NEG      | 97.90   | -0.47    | -4.466839999999994  |
| RTWH / N       | NEG      | 2.10    | -1.33    | -5.32977000000001   |
| DDHQ / Y       | WEAK     | 99.00   | 0.63     | -3.3668400000000043 |
| DDHQ / N       | NEG      | 1.00    | -2.43    | -5.429770000000001  |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Democrats win the Rhode Island Senate race in 2026?
Contract 630911; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       99.5  |        99.52 | +0.48 / −99.52   | 0.00×         |
| No     |        3.94 |         4.09 | +95.91 / −4.09   | 23.44×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.99 |     0.47 |        -3.53 |
| GB / N         | NEG      |    0.01 |    -4.09 |        -6.09 |
| ST / Y         | WEAK     |   99.99 |     0.47 |        -3.53 |
| ST / N         | NEG      |    0.01 |    -4.08 |        -6.09 |
| MX / Y         | WEAK     |   99.85 |     0.33 |        -3.67 |
| MX / N         | NEG      |    0.15 |    -3.95 |        -6.09 |
| M10 / Y        | WEAK     |   99.82 |     0.30 |        -3.70 |
| M10 / N        | NEG      |    0.18 |    -3.91 |        -6.09 |
| RTWH / Y       | NEG      |   98.90 |    -0.62 |        -4.62 |
| RTWH / N       | NEG      |    1.10 |    -2.99 |        -6.09 |
| DDHQ / Y       | NEG      |   99.00 |    -0.52 |        -4.52 |
| DDHQ / N       | NEG      |    1.00 |    -3.09 |        -6.09 |

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
| Yes    |         3.4 |         3.53 | +96.47 / −3.53   | 27.32×        |
| No     |        97.3 |        97.41 | +2.59 / −97.41   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.03 |    -3.50 |        -5.53 |
| GB / N         | WEAK     |   99.97 |     2.57 |        -1.43 |
| ST / Y         | NEG      |    0.02 |    -3.51 |        -5.53 |
| ST / N         | WEAK     |   99.98 |     2.57 |        -1.43 |
| MX / Y         | NEG      |    0.08 |    -3.45 |        -5.53 |
| MX / N         | WEAK     |   99.92 |     2.52 |        -1.48 |
| M10 / Y        | NEG      |    0.05 |    -3.48 |        -5.53 |
| M10 / N        | WEAK     |   99.95 |     2.55 |        -1.45 |
| RTWH / Y       | NEG      |    1.00 |    -2.53 |        -5.53 |
| RTWH / N       | WEAK     |   99.00 |     1.59 |        -2.41 |
| DDHQ / Y       | NEG      |    3.00 |    -0.53 |        -4.53 |
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
| Yes    |         2.9 |         3.01 | +96.99 / −3.01   | 32.19×        |
| No     |        97.8 |        97.89 | +2.11 / −97.89   | 0.02×         |

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
| RTWH / Y       | NEG      | 1.20    | -1.81    | -5.01264            |
| RTWH / N       | WEAK     | 98.80   | 0.91     | -3.0860600000000016 |
| DDHQ / Y       | NEG      | 1.00    | -2.01    | -5.01264            |
| DDHQ / N       | WEAK     | 99.00   | 1.11     | -2.886060000000002  |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party candidate win the 2026 Alabama Senate election by 0%-5%?
Contract 3343107; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.13 |         9.45 | +90.55 / −9.45   | 9.58×         |
| No     |       97.3  |        97.41 | +2.59 / −97.41   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.61    | -8.84    | -11.45324           |
| GB / N         | WEAK     | 99.39   | 1.99     | -2.014552592690899  |
| ST / Y         | NEG      | 0.68    | -8.78    | -11.45324           |
| ST / N         | WEAK     | 99.33   | 1.92     | -2.0800800000000064 |
| MX / Y         | NEG      | 3.00    | -6.45    | -10.449906666666669 |
| MX / N         | NEG      | 97.00   | -0.41    | -4.408413333333339  |
| M10 / Y        | NEG      | 2.90    | -6.56    | -10.556365000000001 |
| M10 / N        | NEG      | 97.10   | -0.30    | -4.301955000000001  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Alabama Senate election by 10%-15%?
Contract 3343105; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       17.28 |        17.85 | +82.15 / −17.85  | 4.60×         |
| No     |       89    |        89.39 | +10.61 / −89.39  | 0.12×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 12.70   | -5.15    | -9.148857683235569  |
| GB / N         | NEG      | 87.30   | -2.10    | -6.095852316764427  |
| ST / Y         | NEG      | 10.22   | -7.63    | -11.62811           |
| ST / N         | WEAK     | 89.78   | 0.38     | -3.6165999999999925 |
| MX / Y         | NEG      | 14.48   | -3.38    | -7.377693333333333  |
| MX / N         | NEG      | 85.52   | -3.87    | -7.867016666666659  |
| M10 / Y        | NEG      | 14.11   | -3.74    | -7.7419120833333315 |
| M10 / N        | NEG      | 85.89   | -3.50    | -7.502797916666659  |
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
| Yes    |        20.9 |        21.56 | +78.44 / −21.56  | 3.64×         |
| No     |        80.1 |        80.74 | +19.26 / −80.74  | 0.24×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)            |
|:---------------|:---------|:--------|:---------|:----------------------|
| GB / Y         | GO       | 29.12   | 7.55     | 3.553812752421756     |
| GB / N         | NEG      | 70.88   | -9.85    | -13.852692752421769   |
| ST / Y         | GO       | 34.48   | 12.91    | 8.91372               |
| ST / N         | NEG      | 65.53   | -15.21   | -19.212600000000013   |
| MX / Y         | WEAK     | 25.53   | 3.97     | -0.029092499999994192 |
| MX / N         | NEG      | 74.47   | -6.27    | -10.269787500000016   |
| M10 / Y        | GO       | 25.73   | 4.17     | 0.17335541666667065   |
| M10 / N        | NEG      | 74.27   | -6.47    | -10.472235416666685   |
| RTWH / Y       | N/A      | —       | —        | —                     |
| RTWH / N       | N/A      | —       | —        | —                     |
| DDHQ / Y       | N/A      | —       | —        | —                     |
| DDHQ / N       | N/A      | —       | —        | —                     |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Alabama Senate election by 35% or more?
Contract 3343100; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       13.42 |        13.88 | +86.12 / −13.88  | 6.20×         |
| No     |       98.92 |        98.96 | +1.04 / −98.96   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.84    | -12.04   | -15.881959999999998 |
| GB / N         | NEG      | 98.16   | -0.80    | -4.801002412164235  |
| ST / Y         | NEG      | 1.01    | -12.87   | -15.881959999999998 |
| ST / N         | WEAK     | 98.99   | 0.03     | -3.973020000000005  |
| MX / Y         | NEG      | 2.52    | -11.36   | -15.363001666666667 |
| MX / N         | NEG      | 97.48   | -1.48    | -5.479478333333332  |
| M10 / Y        | NEG      | 2.67    | -11.21   | -15.21336625        |
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
| Yes    |       26.66 |        27.44 | +72.56 / −27.44  | 2.64×         |
| No     |       73.8  |        74.57 | +25.43 / −74.57  | 0.34×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 16.18   | -11.27   | -15.26745899498048  |
| GB / N         | GO       | 83.82   | 9.25     | 5.250318994980474   |
| ST / Y         | NEG      | 16.19   | -11.25   | -15.249970000000005 |
| ST / N         | GO       | 83.81   | 9.23     | 5.232829999999989   |
| MX / Y         | NEG      | 17.99   | -9.46    | -13.456792916666673 |
| MX / N         | GO       | 82.01   | 7.44     | 3.439652916666658   |
| M10 / Y        | NEG      | 17.22   | -10.23   | -14.225595000000006 |
| M10 / N        | GO       | 82.78   | 8.21     | 4.208455            |
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

## Will the Republican Party candidate win the 2026 Arkansas Senate election by 35%-40%?
Contract 3343119; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        7.74 |         8.02 | +91.98 / −8.02   | 11.46×        |
| No     |       96.4  |        96.54 | +3.46 / −96.54   | 0.04×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.46    | -6.57    | -10.02381           |
| GB / N         | WEAK     | 98.54   | 2.00     | -1.9963005587320337 |
| ST / Y         | NEG      | 0.56    | -7.47    | -10.02381           |
| ST / N         | WEAK     | 99.44   | 2.91     | -1.0949700000000062 |
| MX / Y         | NEG      | 1.04    | -6.99    | -10.02381           |
| MX / N         | WEAK     | 98.96   | 2.42     | -1.5758033333333368 |
| M10 / Y        | NEG      | 1.25    | -6.78    | -10.02381           |
| M10 / N        | WEAK     | 98.75   | 2.22     | -1.7844491666666684 |
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
| Yes    |       14.12 |        14.61 | +85.39 / −14.61  | 5.85×         |
| No     |       89.31 |        89.69 | +10.31 / −89.69  | 0.11×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)           |
|:---------------|:---------|:--------|:---------|:---------------------|
| GB / Y         | NEG      | 6.23    | -8.38    | -12.375507075936149  |
| GB / N         | GO       | 93.77   | 4.08     | 0.07907707593612923  |
| ST / Y         | NEG      | 6.44    | -8.16    | -12.161260000000002  |
| ST / N         | WEAK     | 93.56   | 3.86     | -0.13517000000001778 |
| MX / Y         | NEG      | 12.47   | -2.14    | -6.135218333333336   |
| MX / N         | NEG      | 87.53   | -2.16    | -6.161211666666677   |
| M10 / Y        | NEG      | 11.49   | -3.12    | -7.11876             |
| M10 / N        | NEG      | 88.51   | -1.18    | -5.1776700000000115  |
| RTWH / Y       | N/A      | —       | —        | —                    |
| RTWH / N       | N/A      | —       | —        | —                    |
| DDHQ / Y       | N/A      | —       | —        | —                    |
| DDHQ / N       | N/A      | —       | —        | —                    |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Florida Senate election by 0%-3%?
Contract 3343184; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       21.2  |        21.87 | +78.13 / −21.87  | 3.57×         |
| No     |       80.32 |        80.95 | +19.05 / −80.95  | 0.24×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 14.55   | -7.32    | -11.321225629165234 |
| GB / N         | GO       | 85.45   | 4.50     | 0.49839562916521585 |
| ST / Y         | NEG      | 15.98   | -5.88    | -9.883884999999998  |
| ST / N         | WEAK     | 84.02   | 3.06     | -0.9389450000000243 |
| MX / Y         | NEG      | 14.41   | -7.46    | -11.4579475         |
| MX / N         | GO       | 85.59   | 4.64     | 0.635117499999982   |
| M10 / Y        | NEG      | 13.61   | -8.26    | -12.255864166666665 |
| M10 / N        | GO       | 86.39   | 5.43     | 1.4330341666666468  |
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
| Yes    |        8.56 |         8.87 | +91.13 / −8.87   | 10.27×        |
| No     |       96.31 |        96.45 | +3.55 / −96.45   | 0.04×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 9.31    | 0.44     | -3.560349861488217  |
| GB / N         | NEG      | 90.69   | -5.76    | -9.761070138511773  |
| ST / Y         | NEG      | 7.39    | -1.48    | -5.482375000000002  |
| ST / N         | NEG      | 92.61   | -3.84    | -7.839044999999988  |
| MX / Y         | NEG      | 8.79    | -0.08    | -4.0847708333333355 |
| MX / N         | NEG      | 91.21   | -5.24    | -9.236649166666645  |
| M10 / Y        | WEAK     | 9.60    | 0.73     | -3.2748750000000033 |
| M10 / N        | NEG      | 90.40   | -6.05    | -10.046544999999984 |
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
| Yes    |        3.14 |         3.26 | +96.74 / −3.26   | 29.70×        |
| No     |       98.45 |        98.51 | +1.49 / −98.51   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 4.97    | 1.72     | -2.284985306782922  |
| GB / N         | NEG      | 95.03   | -3.48    | -7.483824693217079  |
| ST / Y         | NEG      | 2.97    | -0.28    | -4.284935000000001  |
| ST / N         | NEG      | 97.03   | -1.48    | -5.483875000000005  |
| MX / Y         | WEAK     | 4.68    | 1.43     | -2.5728516666666668 |
| MX / N         | NEG      | 95.32   | -3.20    | -7.195958333333341  |
| M10 / Y        | WEAK     | 5.31    | 2.05     | -1.9456641666666676 |
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
| Yes    |         4.1 |         4.26 | +95.74 / −4.26   | 22.49×        |
| No     |        99.2 |        99.23 | +0.77 / −99.23   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | WEAK     | 4.79    | 0.54     | -3.464010421168612 |
| GB / N         | NEG      | 95.21   | -4.03    | -8.025009578831387 |
| ST / Y         | NEG      | 2.37    | -1.89    | -5.88853           |
| ST / N         | NEG      | 97.63   | -1.60    | -5.600489999999992 |
| MX / Y         | NEG      | 3.96    | -0.30    | -4.296811250000002 |
| MX / N         | NEG      | 96.04   | -3.19    | -7.192208749999995 |
| M10 / Y        | WEAK     | 4.31    | 0.05     | -3.948113333333335 |
| M10 / N        | NEG      | 95.69   | -3.54    | -7.540906666666658 |
| RTWH / Y       | N/A      | —       | —        | —                  |
| RTWH / N       | N/A      | —       | —        | —                  |
| DDHQ / Y       | N/A      | —       | —        | —                  |
| DDHQ / N       | N/A      | —       | —        | —                  |

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
| Yes    |       12.13 |        12.55 | +87.45 / −12.55  | 6.97×         |
| No     |       90    |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 13.31   | 0.75     | -3.246309761911513  |
| GB / N         | NEG      | 86.69   | -3.67    | -7.6666902380884805 |
| ST / Y         | WEAK     | 13.24   | 0.69     | -3.3092499999999982 |
| ST / N         | NEG      | 86.76   | -3.60    | -7.603749999999998  |
| MX / Y         | WEAK     | 12.81   | 0.25     | -3.7475312499999984 |
| MX / N         | NEG      | 87.19   | -3.17    | -7.165468750000005  |
| M10 / Y        | WEAK     | 13.32   | 0.77     | -3.228312500000001  |
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
| No     |       92.19 |        92.48 | +7.52 / −92.48   | 0.08×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 22.83   | 12.47    | 8.4723771908735     |
| GB / N         | NEG      | 77.17   | -15.31   | -19.3138871908735   |
| ST / Y         | GO       | 22.34   | 11.98    | 7.983750000000002   |
| ST / N         | NEG      | 77.66   | -14.83   | -18.82526           |
| MX / Y         | GO       | 21.50   | 11.14    | 7.143958333333335   |
| MX / N         | NEG      | 78.50   | -13.99   | -17.985468333333344 |
| M10 / Y        | GO       | 20.08   | 9.72     | 5.71578125          |
| M10 / N        | NEG      | 79.92   | -12.56   | -16.557291250000006 |
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
| Yes    |        8.65 |         8.96 | +91.04 / −8.96   | 10.16×        |
| No     |       96.99 |        97.11 | +2.89 / −97.11   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.90    | -8.06    | -10.964310000000003 |
| GB / N         | WEAK     | 99.10   | 1.99     | -2.012713824121104  |
| ST / Y         | NEG      | 0.37    | -8.60    | -10.964310000000003 |
| ST / N         | WEAK     | 99.63   | 2.52     | -1.4782100000000131 |
| MX / Y         | NEG      | 0.89    | -8.08    | -10.964310000000003 |
| MX / N         | WEAK     | 99.11   | 2.00     | -1.9956579166666821 |
| M10 / Y        | NEG      | 0.75    | -8.21    | -10.964310000000003 |
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

## Will the Republican Party candidate win the 2026 Kansas Senate election by 30% or more?
Contract 3343540; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        3.53 |         3.67 | +96.33 / −3.67   | 26.24×        |
| No     |       99.52 |        99.54 | +0.46 / −99.54   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.00    | -3.67    | -5.670680000000002  |
| GB / N         | WEAK     | 100.00  | 0.46     | -3.544342181719884  |
| ST / Y         | NEG      | 0.00    | -3.67    | -5.670680000000002  |
| ST / N         | WEAK     | 100.00  | 0.45     | -3.5459750000000123 |
| MX / Y         | NEG      | 0.00    | -3.67    | -5.670680000000002  |
| MX / N         | WEAK     | 100.00  | 0.45     | -3.5452979166666783 |
| M10 / Y        | NEG      | 0.00    | -3.67    | -5.670680000000002  |
| M10 / N        | WEAK     | 100.00  | 0.46     | -3.544516666666675  |
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
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          82 |        82.59 | +17.41 / −82.59  | 0.21×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | GO       | 31.41   | 9.75     | 5.750891351664948   |
| GB / N         | NEG      | 68.59   | -14.00   | -18.00489135166494  |
| ST / Y         | GO       | 37.26   | 15.60    | 11.595774999999998  |
| ST / N         | NEG      | 62.74   | -19.85   | -23.849775000000008 |
| MX / Y         | GO       | 31.05   | 9.38     | 5.382389583333333   |
| MX / N         | NEG      | 68.95   | -13.64   | -17.636389583333333 |
| M10 / Y        | GO       | 30.91   | 9.25     | 5.248014583333335   |
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
| Yes    |        12.6 |        13.04 | +86.96 / −13.04  | 6.67×         |
| No     |        91   |        91.33 | +8.67 / −91.33   | 0.09×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 2.16    | -10.88   | -14.880503765393918 |
| GB / N         | GO       | 97.84   | 6.51     | 2.512503765393903   |
| ST / Y         | NEG      | 1.08    | -11.96   | -15.040400000000002 |
| ST / N         | GO       | 98.92   | 7.59     | 3.5880249999999836  |
| MX / Y         | NEG      | 1.81    | -11.23   | -15.040400000000002 |
| MX / N         | GO       | 98.19   | 6.86     | 2.8619312499999823  |
| M10 / Y        | NEG      | 2.47    | -10.57   | -14.572066666666666 |
| M10 / N        | GO       | 97.53   | 6.20     | 2.2040666666666486  |
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

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 35%-40%?
Contract 3343559; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        7.6  |         7.88 | +92.12 / −7.88   | 11.69×        |
| No     |       93.76 |        93.99 | +6.01 / −93.99   | 0.06×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | NEG      | 0.02    | -7.87    | -9.880899999999999 |
| GB / N         | GO       | 99.98   | 5.99     | 1.9901296059564921 |
| ST / Y         | NEG      | 0.01    | -7.87    | -9.880899999999999 |
| ST / N         | GO       | 99.99   | 5.99     | 1.993480000000003  |
| MX / Y         | NEG      | 0.03    | -7.85    | -9.880899999999999 |
| MX / N         | GO       | 99.97   | 5.97     | 1.9741050000000038 |
| M10 / Y        | NEG      | 0.05    | -7.83    | -9.880899999999999 |
| M10 / N        | GO       | 99.95   | 5.95     | 1.9534800000000074 |
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
| Yes    |       10.59 |        10.97 | +89.03 / −10.97  | 8.12×         |
| No     |       93    |        93.26 | +6.74 / −93.26   | 0.07×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | NEG      | 0.00    | -10.97   | -12.96864          |
| GB / N         | GO       | 100.00  | 6.74     | 2.7390741754790726 |
| ST / Y         | NEG      | 0.01    | -10.96   | -12.96864          |
| ST / N         | GO       | 99.99   | 6.73     | 2.733350000000001  |
| MX / Y         | NEG      | 0.00    | -10.97   | -12.96864          |
| MX / N         | GO       | 100.00  | 6.74     | 2.7364229166666587 |
| M10 / Y        | NEG      | 0.00    | -10.97   | -12.96864          |
| M10 / N        | GO       | 100.00  | 6.74     | 2.7364229166666587 |
| RTWH / Y       | N/A      | —       | —        | —                  |
| RTWH / N       | N/A      | —       | —        | —                  |
| DDHQ / Y       | N/A      | —       | —        | —                  |
| DDHQ / N       | N/A      | —       | —        | —                  |

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

## Will the Republican Party candidate win the 2026 Louisiana Senate election by 30%-35%?
Contract 3343571; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.61 |         9.95 | +90.05 / −9.95   | 9.05×         |
| No     |       96.47 |        96.61 | +3.39 / −96.61   | 0.04×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.04    | -9.91    | -11.95099           |
| GB / N         | WEAK     | 99.96   | 3.35     | -0.6495432294449266 |
| ST / Y         | NEG      | 0.01    | -9.94    | -11.95099           |
| ST / N         | WEAK     | 99.99   | 3.38     | -0.6208500000000061 |
| MX / Y         | NEG      | 0.05    | -9.90    | -11.95099           |
| MX / N         | WEAK     | 99.95   | 3.34     | -0.6616312500000054 |
| M10 / Y        | NEG      | 0.05    | -9.90    | -11.95099           |
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

## Will the Republican Party candidate win the 2026 Michigan Senate election by 6%-9%?
Contract 3343884; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       14.98 |        15.48 | +84.52 / −15.48  | 5.46×         |
| No     |       95.06 |        95.24 | +4.76 / −95.24   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)           |
|:---------------|:---------|:--------|:---------|:---------------------|
| GB / Y         | NEG      | 1.73    | -13.75   | -17.47923            |
| GB / N         | WEAK     | 98.27   | 3.03     | -0.9702383920397684  |
| ST / Y         | NEG      | 0.97    | -14.50   | -17.47923            |
| ST / N         | WEAK     | 99.02   | 3.78     | -0.21876000000000673 |
| MX / Y         | NEG      | 1.89    | -13.59   | -17.47923            |
| MX / N         | WEAK     | 98.11   | 2.87     | -1.1321974999999984  |
| M10 / Y        | NEG      | 2.50    | -12.98   | -16.98188625         |
| M10 / N        | WEAK     | 97.50   | 2.26     | -1.741103750000006   |
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
| Yes    |       11.63 |        12.03 | +87.97 / −12.03  | 7.31×         |
| No     |       97.95 |        98.03 | +1.97 / −98.03   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.50    | -11.53   | -14.032269999999999 |
| GB / N         | WEAK     | 99.50   | 1.46     | -2.5359847961896387 |
| ST / Y         | NEG      | 0.24    | -11.79   | -14.032269999999999 |
| ST / N         | WEAK     | 99.76   | 1.72     | -2.2763600000000106 |
| MX / Y         | NEG      | 0.65    | -11.39   | -14.032269999999999 |
| MX / N         | WEAK     | 99.36   | 1.32     | -2.677610000000008  |
| M10 / Y        | NEG      | 0.92    | -11.11   | -14.032269999999999 |
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
| Yes    |       14.64 |        15.14 | +84.86 / −15.14  | 5.61×         |
| No     |       90.73 |        91.07 | +8.93 / −91.07   | 0.10×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.57    | -13.57   | -17.13978           |
| GB / N         | GO       | 98.43   | 7.37     | 3.365980986404382   |
| ST / Y         | NEG      | 1.72    | -13.42   | -17.13978           |
| ST / N         | GO       | 98.28   | 7.22     | 3.2176849999999924  |
| MX / Y         | NEG      | 4.40    | -10.74   | -14.743738333333331 |
| MX / N         | GO       | 95.60   | 4.54     | 0.5372683333333184  |
| M10 / Y        | NEG      | 3.79    | -11.35   | -15.353946666666666 |
| M10 / N        | GO       | 96.21   | 5.15     | 1.147476666666658   |
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
| Yes    |       25.36 |        26.06 | +73.94 / −26.06  | 2.84×         |
| No     |       99.48 |        99.5  | +0.50 / −99.50   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.41    | -25.65   | -28.059440000000006 |
| GB / N         | WEAK     | 99.59   | 0.09     | -3.910956561711909  |
| ST / Y         | NEG      | 0.53    | -25.53   | -28.059440000000006 |
| ST / N         | NEG      | 99.47   | -0.03    | -4.031899999999999  |
| MX / Y         | NEG      | 1.86    | -24.19   | -28.059440000000006 |
| MX / N         | NEG      | 98.14   | -1.37    | -5.3655979166666645 |
| M10 / Y        | NEG      | 1.57    | -24.49   | -28.059440000000006 |
| M10 / N        | NEG      | 98.43   | -1.07    | -5.068827083333327  |
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
| Yes    |       17.94 |        18.42 | +81.58 / −18.42  | 4.43×         |
| No     |       99.9  |        99.9  | +0.10 / −99.90   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | NEG      | 0.10    | -18.33   | -20.4234           |
| GB / N         | WEAK     | 99.90   | 0.00     | -3.999027712691716 |
| ST / Y         | NEG      | 0.18    | -18.25   | -20.4234           |
| ST / N         | NEG      | 99.83   | -0.08    | -4.079000000000022 |
| MX / Y         | NEG      | 0.97    | -17.45   | -20.4234           |
| MX / N         | NEG      | 99.03   | -0.87    | -4.873166666666684 |
| M10 / Y        | NEG      | 0.77    | -17.66   | -20.4234           |
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
| Yes    |        6.62 |         6.86 | +93.14 / −6.86   | 13.57×        |
| No     |       99.4  |        99.42 | +0.58 / −99.42   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.68    | -6.19    | -8.86381            |
| GB / N         | NEG      | 99.32   | -0.10    | -4.101424594971103  |
| ST / Y         | NEG      | 0.30    | -6.56    | -8.86381            |
| ST / N         | WEAK     | 99.70   | 0.27     | -3.726985000000016  |
| MX / Y         | NEG      | 0.67    | -6.20    | -8.86381            |
| MX / N         | NEG      | 99.33   | -0.09    | -4.0896412500000086 |
| M10 / Y        | NEG      | 0.68    | -6.19    | -8.86381            |
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
| Yes    |        7.48 |         7.76 | +92.24 / −7.76   | 11.89×        |
| No     |       96    |        96.15 | +3.85 / −96.15   | 0.04×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 9.43    | 1.67     | -2.325980676277348  |
| GB / N         | NEG      | 90.57   | -5.58    | -9.584589323722648  |
| ST / Y         | NEG      | 7.11    | -0.65    | -4.647595           |
| ST / N         | NEG      | 92.89   | -3.26    | -7.262974999999994  |
| MX / Y         | WEAK     | 8.65    | 0.89     | -3.1116054166666656 |
| MX / N         | NEG      | 91.35   | -4.80    | -8.798964583333335  |
| M10 / Y        | WEAK     | 8.70    | 0.94     | -3.058272083333334  |
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
| Yes    |        7.39 |         7.65 | +92.35 / −7.65   | 12.08×        |
| No     |       99.8  |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.40    | -7.25    | -9.645649999999998  |
| GB / N         | NEG      | 99.60   | -0.21    | -4.2073421895840735 |
| ST / Y         | NEG      | 0.17    | -7.48    | -9.645649999999998  |
| ST / N         | WEAK     | 99.83   | 0.02     | -3.976729999999995  |
| MX / Y         | NEG      | 0.53    | -7.12    | -9.645649999999998  |
| MX / N         | NEG      | 99.47   | -0.33    | -4.3330320833333325 |
| M10 / Y        | NEG      | 0.68    | -6.97    | -9.645649999999998  |
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
| Yes    |       10.41 |        10.78 | +89.22 / −10.78  | 8.27×         |
| No     |       91.46 |        91.77 | +8.23 / −91.77   | 0.09×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 8.82    | -1.97    | -5.966234538015495  |
| GB / N         | NEG      | 91.18   | -0.59    | -4.5890454619845205 |
| ST / Y         | NEG      | 6.52    | -4.27    | -8.267335000000003  |
| ST / N         | WEAK     | 93.48   | 1.71     | -2.2879450000000134 |
| MX / Y         | NEG      | 8.73    | -2.06    | -6.056293333333334  |
| MX / N         | NEG      | 91.27   | -0.50    | -4.498986666666682  |
| M10 / Y        | NEG      | 10.08   | -0.70    | -4.703949583333335  |
| M10 / N        | NEG      | 89.92   | -1.85    | -5.851330416666679  |
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
| Yes    |        9.35 |         9.68 | +90.32 / −9.68   | 9.33×         |
| No     |       97.2  |        97.31 | +2.69 / −97.31   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 3.87    | -5.82    | -9.815305681132337  |
| GB / N         | NEG      | 96.13   | -1.17    | -5.174384318867675  |
| ST / Y         | NEG      | 2.07    | -7.62    | -11.615205000000001 |
| ST / N         | WEAK     | 97.93   | 0.63     | -3.374485000000016  |
| MX / Y         | NEG      | 3.77    | -5.91    | -9.913850833333333  |
| MX / N         | NEG      | 96.23   | -1.08    | -5.075839166666674  |
| M10 / Y        | NEG      | 4.57    | -5.11    | -9.11004875         |
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
| Yes    |       17.51 |        18.09 | +81.91 / −18.09  | 4.53×         |
| No     |       87    |        87.45 | +12.55 / −87.45  | 0.14×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 13.24   | -4.85    | -8.847566343916458  |
| GB / N         | NEG      | 86.76   | -0.69    | -4.692313656083547  |
| ST / Y         | NEG      | 11.28   | -6.81    | -10.812480000000003 |
| ST / N         | WEAK     | 88.72   | 1.27     | -2.7274000000000016 |
| MX / Y         | NEG      | 13.55   | -4.54    | -8.540136250000002  |
| MX / N         | NEG      | 86.45   | -1.00    | -4.999743749999997  |
| M10 / Y        | NEG      | 11.99   | -6.10    | -10.095188333333336 |
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
| No     |        88.2 |        88.61 | +11.39 / −88.61  | 0.13×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 18.84   | 3.33     | -0.6663586198582621 |
| GB / N         | NEG      | 81.16   | -7.46    | -11.457631380141741 |
| ST / Y         | WEAK     | 18.41   | 2.90     | -1.1037499999999978 |
| ST / N         | NEG      | 81.59   | -7.02    | -11.020240000000003 |
| MX / Y         | WEAK     | 17.85   | 2.34     | -1.660677083333331  |
| MX / N         | NEG      | 82.15   | -6.46    | -10.463312916666666 |
| M10 / Y        | GO       | 19.57   | 4.06     | 0.05510416666666962 |
| M10 / N        | NEG      | 80.43   | -8.18    | -12.17909416666667  |
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
| No     |       93.93 |        94.16 | +5.84 / −94.16   | 0.06×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 7.34    | -3.02    | -7.016327838535908  |
| GB / N         | NEG      | 92.66   | -1.50    | -5.499872161464103  |
| ST / Y         | NEG      | 4.98    | -5.38    | -9.385              |
| ST / N         | WEAK     | 95.03   | 0.87     | -3.1312000000000006 |
| MX / Y         | NEG      | 7.23    | -3.13    | -7.129375000000001  |
| MX / N         | NEG      | 92.77   | -1.39    | -5.386825000000005  |
| M10 / Y        | NEG      | 8.31    | -2.05    | -6.051770833333333  |
| M10 / N        | NEG      | 91.69   | -2.46    | -6.464429166666674  |
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
| Yes    |       10.43 |        10.8  | +89.20 / −10.80  | 8.26×         |
| No     |       97.66 |        97.75 | +2.25 / −97.75   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.68    | -9.11    | -12.7964            |
| GB / N         | WEAK     | 98.32   | 0.57     | -3.4318948234330793 |
| ST / Y         | NEG      | 0.81    | -9.98    | -12.7964            |
| ST / N         | WEAK     | 99.19   | 1.44     | -2.5623000000000062 |
| MX / Y         | NEG      | 2.08    | -8.72    | -12.716504166666667 |
| MX / N         | WEAK     | 97.92   | 0.17     | -3.829695833333335  |
| M10 / Y        | NEG      | 2.54    | -8.26    | -12.260045833333333 |
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
| Yes    |        5.97 |         6.19 | +93.81 / −6.19   | 15.15×        |
| No     |       99.3  |        99.33 | +0.67 / −99.33   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.24    | -5.95    | -8.19171            |
| GB / N         | WEAK     | 99.76   | 0.43     | -3.572493910512276  |
| ST / Y         | NEG      | 0.16    | -6.04    | -8.19171            |
| ST / N         | WEAK     | 99.84   | 0.52     | -3.484049999999994  |
| MX / Y         | NEG      | 0.55    | -5.64    | -8.19171            |
| MX / N         | WEAK     | 99.45   | 0.12     | -3.8821229166666638 |
| M10 / Y        | NEG      | 0.70    | -5.49    | -8.19171            |
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
| No     |          74 |        74.77 | +25.23 / −74.77  | 0.34×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 15.48   | -14.35   | -18.346082935097296 |
| GB / N         | GO       | 84.52   | 9.75     | 5.752882935097303   |
| ST / Y         | NEG      | 13.98   | -15.84   | -19.842349999999996 |
| ST / N         | GO       | 86.02   | 11.25    | 7.249150000000004   |
| MX / Y         | NEG      | 18.14   | -11.68   | -15.683756249999995 |
| MX / N         | GO       | 81.86   | 7.09     | 3.0905562500000094  |
| M10 / Y        | NEG      | 16.88   | -12.94   | -16.941933333333328 |
| M10 / N        | GO       | 83.12   | 8.35     | 4.348733333333343   |
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
| Yes    |       11.24 |        11.64 | +88.36 / −11.64  | 7.59×         |
| No     |       91.4  |        91.71 | +8.29 / −91.71   | 0.09×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)           |
|:---------------|:---------|:--------|:---------|:---------------------|
| GB / Y         | WEAK     | 15.33   | 3.69     | -0.31230713051806636 |
| GB / N         | NEG      | 84.67   | -7.04    | -11.041012869481936  |
| ST / Y         | WEAK     | 13.14   | 1.50     | -2.4952499999999973  |
| ST / N         | NEG      | 86.86   | -4.86    | -8.858070000000007   |
| MX / Y         | WEAK     | 12.02   | 0.38     | -3.621187499999999   |
| MX / N         | NEG      | 87.98   | -3.73    | -7.732132500000011   |
| M10 / Y        | WEAK     | 13.25   | 1.61     | -2.3857708333333325  |
| M10 / N        | NEG      | 86.75   | -4.97    | -8.967549166666677   |
| RTWH / Y       | N/A      | —       | —        | —                    |
| RTWH / N       | N/A      | —       | —        | —                    |
| DDHQ / Y       | N/A      | —       | —        | —                    |
| DDHQ / N       | N/A      | —       | —        | —                    |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 20%-25%?
Contract 3344122; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        5.54 |         5.75 | +94.25 / −5.75   | 16.39×        |
| No     |       97.46 |        97.56 | +2.44 / −97.56   | 0.03×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 4.04    | -1.71    | -5.713594989445572  |
| GB / N         | NEG      | 95.96   | -1.60    | -5.596005010554439  |
| ST / Y         | NEG      | 2.08    | -3.66    | -7.664735           |
| ST / N         | WEAK     | 97.92   | 0.36     | -3.644865000000019  |
| MX / Y         | NEG      | 2.92    | -2.83    | -6.8297870833333345 |
| MX / N         | NEG      | 97.08   | -0.48    | -4.479812916666681  |
| M10 / Y        | NEG      | 3.35    | -2.40    | -6.400932916666667  |
| M10 / N        | NEG      | 96.65   | -0.91    | -4.908667083333351  |
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
| Yes    |        6.29 |         6.53 | +93.47 / −6.53   | 14.32×        |
| No     |       99.5  |        99.52 | +0.48 / −99.52   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.04    | -6.49    | -8.526150000000001  |
| GB / N         | WEAK     | 99.96   | 0.44     | -3.558586705563871  |
| ST / Y         | NEG      | 0.02    | -6.51    | -8.526150000000001  |
| ST / N         | WEAK     | 99.98   | 0.46     | -3.535524999999995  |
| MX / Y         | NEG      | 0.06    | -6.47    | -8.526150000000001  |
| MX / N         | WEAK     | 99.94   | 0.42     | -3.577347916666662  |
| M10 / Y        | NEG      | 0.08    | -6.45    | -8.526150000000001  |
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
| No     |          85 |        85.51 | +14.49 / −85.51  | 0.17×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 9.71    | -7.85    | -11.853309677381798 |
| GB / N         | GO       | 90.29   | 4.78     | 0.7789096773817894  |
| ST / Y         | NEG      | 7.53    | -10.04   | -14.036274999999998 |
| ST / N         | GO       | 92.47   | 6.96     | 2.9618749999999916  |
| MX / Y         | NEG      | 8.99    | -8.58    | -12.576899999999998 |
| MX / N         | GO       | 91.01   | 5.50     | 1.5024999999999844  |
| M10 / Y        | NEG      | 6.53    | -11.04   | -15.039087499999999 |
| M10 / N        | GO       | 93.47   | 7.96     | 3.964687499999986   |
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

## Will the Republican Party candidate win the 2026 Tennessee Senate election by 30%-35%?
Contract 3344151; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          10 |        10.36 | +89.64 / −10.36  | 8.65×         |
| No     |          93 |        93.26 | +6.74 / −93.26   | 0.07×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 9.69    | -0.67    | -4.667964655606395  |
| GB / N         | NEG      | 90.31   | -2.95    | -6.952435344393604  |
| ST / Y         | NEG      | 7.12    | -3.24    | -7.241250000000001  |
| ST / N         | NEG      | 92.88   | -0.38    | -4.379149999999998  |
| MX / Y         | NEG      | 10.01   | -0.35    | -4.345364583333334  |
| MX / N         | NEG      | 89.99   | -3.28    | -7.275035416666675  |
| M10 / Y        | WEAK     | 12.95   | 2.59     | -1.411770833333334  |
| M10 / N        | NEG      | 87.05   | -6.21    | -10.208629166666672 |
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
| Yes    |        11.4 |        11.78 | +88.22 / −11.78  | 7.49×         |
| No     |        99.6 |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.03    | -11.75   | -13.780979999999998 |
| GB / N         | WEAK     | 99.97   | 0.36     | -3.6426365741092814 |
| ST / Y         | NEG      | 0.03    | -11.75   | -13.780979999999998 |
| ST / N         | WEAK     | 99.97   | 0.35     | -3.647189999999989  |
| MX / Y         | NEG      | 0.11    | -11.67   | -13.780979999999998 |
| MX / N         | WEAK     | 99.89   | 0.27     | -3.727971249999984  |
| M10 / Y        | NEG      | 0.21    | -11.57   | -13.780979999999998 |
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
| No     |          83 |        83.56 | +16.44 / −83.56  | 0.20×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 21.67   | 0.00     | -3.9977917929015727 |
| GB / N         | NEG      | 78.33   | -5.23    | -9.230208207098434  |
| ST / Y         | WEAK     | 25.15   | 3.49     | -0.5104749999999991 |
| ST / N         | NEG      | 74.85   | -8.72    | -12.717525000000007 |
| MX / Y         | WEAK     | 23.65   | 1.98     | -2.0156833333333317 |
| MX / N         | NEG      | 76.35   | -7.21    | -11.212316666666677 |
| M10 / Y        | WEAK     | 23.52   | 1.86     | -2.1409958333333314 |
| M10 / N        | NEG      | 76.48   | -7.09    | -11.08700416666668  |
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
| Yes    |        3.86 |         4.01 | +95.99 / −4.01   | 23.97×        |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.42    | -3.58    | -6.0053100000000015 |
| GB / N         | NEG      | 99.58   | -0.04    | -4.038532506731595  |
| ST / Y         | NEG      | 0.17    | -3.83    | -6.0053100000000015 |
| ST / N         | WEAK     | 99.83   | 0.21     | -3.7878149999999833 |
| MX / Y         | NEG      | 0.46    | -3.55    | -6.0053100000000015 |
| MX / N         | NEG      | 99.54   | -0.07    | -4.072294166666646  |
| M10 / Y        | NEG      | 0.45    | -3.56    | -6.0053100000000015 |
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
| Yes    |        11.5 |        11.91 | +88.09 / −11.91  | 7.40×         |
| No     |        89.2 |        89.59 | +10.41 / −89.59  | 0.12×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | WEAK     | 13.56   | 1.65     | -2.349034773076268  |
| GB / N         | NEG      | 86.44   | -3.14    | -7.143405226923738  |
| ST / Y         | WEAK     | 12.10   | 0.20     | -3.803975           |
| ST / N         | NEG      | 87.90   | -1.69    | -5.6884650000000105 |
| MX / Y         | WEAK     | 13.83   | 1.92     | -2.07944375         |
| MX / N         | NEG      | 86.17   | -3.41    | -7.4129962500000035 |
| M10 / Y        | WEAK     | 13.69   | 1.78     | -2.2163708333333325 |
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
| Yes    |        5.73 |         5.94 | +94.06 / −5.94   | 15.84×        |
| No     |       98.3  |        98.37 | +1.63 / −98.37   | 0.02×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 1.76    | -4.18    | -7.937960000000001  |
| GB / N         | NEG      | 98.24   | -0.13    | -4.126846062794343  |
| ST / Y         | NEG      | 0.80    | -5.14    | -7.937960000000001  |
| ST / N         | WEAK     | 99.20   | 0.84     | -3.1637150000000003 |
| MX / Y         | NEG      | 1.61    | -4.33    | -7.937960000000001  |
| MX / N         | WEAK     | 98.39   | 0.03     | -3.9746524999999973 |
| M10 / Y        | NEG      | 1.57    | -4.36    | -7.937960000000001  |
| M10 / N        | WEAK     | 98.43   | 0.06     | -3.9417358333333374 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | N/A      | —       | —        | —                   |
| DDHQ / N       | N/A      | —       | —        | —                   |

RTWH (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.
DDHQ (2026-09-25): Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.

## Will the Republican Party candidate win the 2026 Virginia Senate election by 0%-3%?
Contract 3344161; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        1.4  |         1.46 | +98.54 / −1.46   | 67.72×        |
| No     |       99.61 |        99.63 | +0.37 / −99.63   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.41    | -1.04    | -3.4552200000000006 |
| GB / N         | NEG      | 99.59   | -0.04    | -4.0365993278346775 |
| ST / Y         | NEG      | 0.33    | -1.13    | -3.4552200000000006 |
| ST / N         | WEAK     | 99.67   | 0.05     | -3.9505399999999913 |
| MX / Y         | NEG      | 0.82    | -0.63    | -3.4552200000000006 |
| MX / N         | NEG      | 99.18   | -0.45    | -4.450175416666657  |
| M10 / Y        | NEG      | 0.80    | -0.65    | -3.4552200000000006 |
| M10 / N        | NEG      | 99.20   | -0.43    | -4.42741499999999   |
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

## Will the Republican Party hold exactly 54 Senate seats after the 2026 midterm elections?
Contract 943826; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         2.5 |         2.6  | +97.40 / −2.60   | 37.50×        |
| No     |        98.5 |        98.56 | +1.44 / −98.56   | 0.01×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.27    | -2.33    | -4.5975             |
| GB / N         | WEAK     | 99.73   | 1.17     | -2.8290999999999955 |
| ST / Y         | NEG      | 0.13    | -2.47    | -4.5975             |
| ST / N         | WEAK     | 99.87   | 1.31     | -2.6872249999999926 |
| MX / Y         | NEG      | 0.23    | -2.37    | -4.5975             |
| MX / N         | WEAK     | 99.77   | 1.22     | -2.7843604166666425 |
| M10 / Y        | NEG      | 0.29    | -2.31    | -4.5975             |
| M10 / N        | WEAK     | 99.71   | 1.15     | -2.849047916666636  |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | WEAK     | 4.72    | 2.12     | -1.8754000000000004 |
| DDHQ / N       | NEG      | 95.28   | -3.28    | -7.281199999999988  |

RTWH (2026-09-25): Publisher supplies no seat-count distribution; expected seats cannot price this contract.
DDHQ (2026-09-25): Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available. DDHQ incorporates market inputs; this is not independent corroboration of market prices. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republican Party hold exactly 55 Senate seats after the 2026 midterm elections?
Contract 943827; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         1   |         1.04 | +98.96 / −1.04   | 95.19×        |
| No     |        99.8 |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)          |
|:---------------|:---------|:--------|:---------|:--------------------|
| GB / Y         | NEG      | 0.02    | -1.02    | -3.0396000000000005 |
| GB / N         | WEAK     | 99.98   | 0.17     | -3.827979999999998  |
| ST / Y         | NEG      | 0.03    | -1.01    | -3.0396000000000005 |
| ST / N         | WEAK     | 99.98   | 0.17     | -3.8329799999999974 |
| MX / Y         | NEG      | 0.03    | -1.01    | -3.0396000000000005 |
| MX / N         | WEAK     | 99.97   | 0.17     | -3.8348029166666686 |
| M10 / Y        | NEG      | 0.05    | -0.99    | -3.0396000000000005 |
| M10 / N        | WEAK     | 99.95   | 0.14     | -3.8551154166666657 |
| RTWH / Y       | N/A      | —       | —        | —                   |
| RTWH / N       | N/A      | —       | —        | —                   |
| DDHQ / Y       | WEAK     | 3.32    | 2.28     | -1.7234000000000003 |
| DDHQ / N       | NEG      | 96.68   | -3.12    | -7.124180000000003  |

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
| No     |        4.93 |         5.12 | +94.88 / −5.12   | 18.53×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.94 |     0.73 |        -3.27 |
| GB / N         | NEG      |    0.06 |    -5.06 |        -7.12 |
| ST / Y         | WEAK     |   99.85 |     0.63 |        -3.37 |
| ST / N         | NEG      |    0.15 |    -4.97 |        -7.12 |
| MX / Y         | NEG      |   98.46 |    -0.75 |        -4.75 |
| MX / N         | NEG      |    1.54 |    -3.58 |        -7.12 |
| M10 / Y        | NEG      |   98.54 |    -0.68 |        -4.68 |
| M10 / N        | NEG      |    1.46 |    -3.66 |        -7.12 |
| RTWH / Y       | NEG      |   98.90 |    -0.31 |        -4.31 |
| RTWH / N       | NEG      |    1.10 |    -4.02 |        -7.12 |
| DDHQ / Y       | NEG      |   95.00 |    -4.21 |        -8.21 |
| DDHQ / N       | NEG      |    5.00 |    -0.12 |        -4.12 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Arkansas Senate race in 2026?
Contract 630654; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       95.77 |        95.93 | +4.07 / −95.93   | 0.04×         |
| No     |        5.9  |         6.12 | +93.88 / −6.12   | 15.33×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.76 |     3.83 |        -0.17 |
| GB / N         | NEG      |    0.24 |    -5.88 |        -8.12 |
| ST / Y         | WEAK     |   99.21 |     3.28 |        -0.72 |
| ST / N         | NEG      |    0.79 |    -5.33 |        -8.12 |
| MX / Y         | NEG      |   93.36 |    -2.57 |        -6.57 |
| MX / N         | WEAK     |    6.64 |     0.51 |        -3.49 |
| M10 / Y        | NEG      |   94.22 |    -1.71 |        -5.71 |
| M10 / N        | NEG      |    5.78 |    -0.35 |        -4.35 |
| RTWH / Y       | WEAK     |   98.00 |     2.07 |        -1.93 |
| RTWH / N       | NEG      |    2.00 |    -4.12 |        -8.12 |
| DDHQ / Y       | WEAK     |   96.00 |     0.07 |        -3.93 |
| DDHQ / N       | NEG      |    4.00 |    -2.12 |        -6.12 |

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
| Yes    |        5.8  |         6.02 | +93.98 / −6.02   | 15.62×        |
| No     |       94.96 |        95.15 | +4.85 / −95.15   | 0.05×         |

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | N/A      | —       | —        | —                  |
| GB / N         | N/A      | —       | —        | —                  |
| ST / Y         | N/A      | —       | —        | —                  |
| ST / N         | N/A      | —       | —        | —                  |
| MX / Y         | N/A      | —       | —        | —                  |
| MX / N         | N/A      | —       | —        | —                  |
| M10 / Y        | N/A      | —       | —        | —                  |
| M10 / N        | N/A      | —       | —        | —                  |
| RTWH / Y       | NEG      | 5.60    | -0.42    | -4.418540000000001 |
| RTWH / N       | NEG      | 94.40   | -0.75    | -4.747440000000013 |
| DDHQ / Y       | GO       | 13.00   | 6.98     | 2.9814599999999998 |
| DDHQ / N       | NEG      | 87.00   | -8.15    | -12.14744000000001 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Idaho Senate race in 2026?
Contract 630706; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       92.68 |        92.95 | +7.05 / −92.95   | 0.08×         |
| No     |        9    |         9.33 | +90.67 / −9.33   | 9.72×         |

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
| RTWH / Y       | WEAK     | 95.80   | 2.85     | -1.1513500000000176 |
| RTWH / N       | NEG      | 4.20    | -5.13    | -9.127599999999997  |
| DDHQ / Y       | GO       | 97.00   | 4.05     | 0.04864999999998343 |
| DDHQ / N       | NEG      | 3.00    | -6.33    | -10.327599999999997 |

RTWH (2026-09-25): Achilles retains IND despite publisher column. Publisher omits separate probabilities for reviewed contenders: Natalie Fleming. Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Publisher omits separate probabilities for reviewed contenders: Natalie Fleming. Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Illinois Senate race in 2026?
Contract 630721; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.67 |         2.78 | +97.22 / −2.78   | 34.98×        |
| No     |       98.66 |        98.71 | +1.29 / −98.71   | 0.01×         |

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
| RTWH / Y       | NEG      | 2.50    | -0.28    | -4.279129999999999  |
| RTWH / N       | NEG      | 97.50   | -1.21    | -5.209489999999983  |
| DDHQ / Y       | WEAK     | 4.00    | 1.22     | -2.7791299999999994 |
| DDHQ / N       | NEG      | 96.00   | -2.71    | -6.709489999999985  |

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

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)           |
|:---------------|:---------|:--------|:---------|:---------------------|
| GB / Y         | N/A      | —       | —        | —                    |
| GB / N         | N/A      | —       | —        | —                    |
| ST / Y         | N/A      | —       | —        | —                    |
| ST / N         | N/A      | —       | —        | —                    |
| MX / Y         | N/A      | —       | —        | —                    |
| MX / N         | N/A      | —       | —        | —                    |
| M10 / Y        | N/A      | —       | —        | —                    |
| M10 / N        | N/A      | —       | —        | —                    |
| RTWH / Y       | WEAK     | 37.80   | 3.92     | -0.08440000000000669 |
| RTWH / N       | NEG      | 62.20   | -6.67    | -10.67039999999999   |
| DDHQ / Y       | GO       | 46.00   | 12.12    | 8.1156               |
| DDHQ / N       | NEG      | 54.00   | -14.87   | -18.870399999999997  |

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

| Model / side   | Status   | P (%)   | EV ($)   | Stress ($)         |
|:---------------|:---------|:--------|:---------|:-------------------|
| GB / Y         | N/A      | —       | —        | —                  |
| GB / N         | N/A      | —       | —        | —                  |
| ST / Y         | N/A      | —       | —        | —                  |
| ST / N         | N/A      | —       | —        | —                  |
| MX / Y         | N/A      | —       | —        | —                  |
| MX / N         | N/A      | —       | —        | —                  |
| M10 / Y        | N/A      | —       | —        | —                  |
| M10 / N        | N/A      | —       | —        | —                  |
| RTWH / Y       | NEG      | 77.90   | -13.43   | -17.42760000000001 |
| RTWH / N       | GO       | 22.10   | 10.71    | 6.708399999999997  |
| DDHQ / Y       | NEG      | 90.00   | -1.33    | -5.32760000000001  |
| DDHQ / N       | NEG      | 10.00   | -1.39    | -5.391600000000003 |

RTWH (2026-09-25): Publisher omits separate probabilities for reviewed contenders: Alani Bankhead. Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Publisher omits separate probabilities for reviewed contenders: Alani Bankhead. Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Nebraska Senate race in 2026?
Contract 634892; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          70 |        70.84 | +29.16 / −70.84  | 0.41×         |
| No     |          31 |        31.86 | +68.14 / −31.86  | 2.14×         |

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
| RTWH / Y       | NEG      | 64.00   | -6.84    | -10.840000000000005 |
| RTWH / N       | GO       | 36.00   | 4.14     | 0.14439999999999453 |
| DDHQ / Y       | GO       | 83.00   | 12.16    | 8.15999999999999    |
| DDHQ / N       | NEG      | 17.00   | -14.86   | -18.8556            |

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
| RTWH / Y       | NEG      | 2.90    | -0.85    | -4.852970000000001  |
| RTWH / N       | NEG      | 97.10   | -2.15    | -6.152340000000012  |
| DDHQ / Y       | WEAK     | 4.00    | 0.25     | -3.7529699999999995 |
| DDHQ / N       | NEG      | 96.00   | -3.25    | -7.252340000000013  |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the New Mexico Senate race in 2026?
Contract 630871; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        3.3  |         3.43 | +96.57 / −3.43   | 28.17×        |
| No     |       99.17 |        99.21 | +0.79 / −99.21   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.90 |    -1.53 |        -5.43 |
| GB / N         | NEG      |   98.10 |    -1.10 |        -5.10 |
| ST / Y         | NEG      |    0.93 |    -2.49 |        -5.43 |
| ST / N         | NEG      |   99.07 |    -0.14 |        -4.14 |
| MX / Y         | NEG      |    1.81 |    -1.62 |        -5.43 |
| MX / N         | NEG      |   98.19 |    -1.01 |        -5.01 |
| M10 / Y        | NEG      |    1.85 |    -1.58 |        -5.43 |
| M10 / N        | NEG      |   98.15 |    -1.05 |        -5.05 |
| RTWH / Y       | NEG      |    0.70 |    -2.73 |        -5.43 |
| RTWH / N       | WEAK     |   99.30 |     0.09 |        -3.91 |
| DDHQ / Y       | WEAK     |    4.00 |     0.57 |        -3.43 |
| DDHQ / N       | NEG      |   96.00 |    -3.21 |        -7.21 |

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
| RTWH / Y       | NEG      | 2.10    | -0.39    | -4.393700000000001  |
| RTWH / N       | NEG      | 97.90   | -0.37    | -4.370700000000005  |
| DDHQ / Y       | NEG      | 1.00    | -1.49    | -4.4937000000000005 |
| DDHQ / N       | WEAK     | 99.00   | 0.73     | -3.2707000000000037 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Rhode Island Senate race in 2026?
Contract 630912; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.19 |         2.28 | +97.72 / −2.28   | 42.89×        |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.01 |    -2.27 |        -4.28 |
| GB / N         | WEAK     |   99.99 |     0.38 |        -3.62 |
| ST / Y         | NEG      |    0.01 |    -2.27 |        -4.28 |
| ST / N         | WEAK     |   99.99 |     0.37 |        -3.63 |
| MX / Y         | NEG      |    0.15 |    -2.13 |        -4.28 |
| MX / N         | WEAK     |   99.85 |     0.24 |        -3.76 |
| M10 / Y        | NEG      |    0.18 |    -2.10 |        -4.28 |
| M10 / N        | WEAK     |   99.82 |     0.20 |        -3.80 |
| RTWH / Y       | NEG      |    1.10 |    -1.18 |        -4.28 |
| RTWH / N       | NEG      |   98.90 |    -0.72 |        -4.72 |
| DDHQ / Y       | NEG      |    1.00 |    -1.28 |        -4.28 |
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
| No     |        6.57 |         6.81 | +93.19 / −6.81   | 13.68×        |

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
| RTWH / Y       | NEG      | 87.10   | -7.42    | -11.41500000000001  |
| RTWH / N       | GO       | 12.90   | 6.09     | 2.0872599999999992  |
| DDHQ / Y       | WEAK     | 97.00   | 2.48     | -1.5150000000000108 |
| DDHQ / N       | NEG      | 3.00    | -3.81    | -7.812739999999999  |

RTWH (2026-09-25): Bengs retains IND despite publisher column. Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Tennessee Senate race in 2026?
Contract 630951; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        97.2 |        97.31 | +2.69 / −97.31   | 0.03×         |
| No     |         3.9 |         4.05 | +95.95 / −4.05   | 23.69×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.97 |     2.66 |        -1.34 |
| GB / N         | NEG      |    0.03 |    -4.02 |        -6.05 |
| ST / Y         | WEAK     |   99.98 |     2.67 |        -1.33 |
| ST / N         | NEG      |    0.02 |    -4.03 |        -6.05 |
| MX / Y         | WEAK     |   99.92 |     2.61 |        -1.39 |
| MX / N         | NEG      |    0.08 |    -3.97 |        -6.05 |
| M10 / Y        | WEAK     |   99.95 |     2.64 |        -1.36 |
| M10 / N        | NEG      |    0.05 |    -4.00 |        -6.05 |
| RTWH / Y       | WEAK     |   99.00 |     1.69 |        -2.31 |
| RTWH / N       | NEG      |    1.00 |    -3.05 |        -6.05 |
| DDHQ / Y       | NEG      |   97.00 |    -0.31 |        -4.31 |
| DDHQ / N       | NEG      |    3.00 |    -1.05 |        -5.05 |

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
| Yes    |        2.91 |         3.03 | +96.97 / −3.03   | 32.03×        |
| No     |       99.7  |        99.71 | +0.29 / −99.71   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.57 |    -2.46 |        -5.03 |
| GB / N         | NEG      |   99.43 |    -0.28 |        -4.28 |
| ST / Y         | NEG      |    0.59 |    -2.44 |        -5.03 |
| ST / N         | NEG      |   99.41 |    -0.30 |        -4.30 |
| MX / Y         | NEG      |    1.52 |    -1.51 |        -5.03 |
| MX / N         | NEG      |   98.48 |    -1.23 |        -5.23 |
| M10 / Y        | NEG      |    1.48 |    -1.55 |        -5.03 |
| M10 / N        | NEG      |   98.52 |    -1.19 |        -5.19 |
| RTWH / Y       | NEG      |    1.90 |    -1.13 |        -5.03 |
| RTWH / N       | NEG      |   98.10 |    -1.61 |        -5.61 |
| DDHQ / Y       | WEAK     |    4.00 |     0.97 |        -3.03 |
| DDHQ / N       | NEG      |   96.00 |    -3.71 |        -7.71 |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

## Will the Republicans win the Wyoming Senate race in 2026?
Contract 631003; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        97   |        97.12 | +2.88 / −97.12   | 0.03×         |
| No     |         3.1 |         3.22 | +96.78 / −3.22   | 30.05×        |

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
| RTWH / Y       | WEAK     | 98.80   | 1.68     | -2.3164000000000073 |
| RTWH / N       | NEG      | 1.20    | -2.02    | -5.22016            |
| DDHQ / Y       | WEAK     | 99.00   | 1.88     | -2.116400000000007  |
| DDHQ / N       | NEG      | 1.00    | -2.22    | -5.22016            |

RTWH (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. Published rounding is retained; equal endpoints represent one estimate, not certainty.
DDHQ (2026-09-25): Final-election publisher probability; current candidate and contract rules must agree. DDHQ uses 25% market inputs for this race. Published rounding is retained; equal endpoints represent one estimate, not certainty.

