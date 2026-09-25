# All model-market pairs grouped by market

Y = buy Yes; N = buy No. P = model probability that the selected side pays $1 under the contract condition; it is not confidence that the model is correct. EV = base expected net profit after purchase depth and estimated fees. Budget and win/loss payoffs use those base costs. Stress adds the extra friction scenario and applies the probability haircut to the model probability. GO (green) survives stress; WEAK (amber) is positive before stress only; UNC (amber) is unresolved; NEG (red) is negative in expectation; N/A (gray) is unavailable. P comes from the full predictive distribution. Simulation estimates have sampling error. All model rows are independent comparisons; there is no combined score.

Base: quoted ask depth plus estimated fees. Stress only: add 2¢ per share and reduce the selected-side probability by 2 percentage points (minimum zero).

## Model codes

| Code   | Model name                         |
|:-------|:-----------------------------------|
| GB     | Gaussian Bayesian                  |
| ST     | Matched Student-t (df5)            |
| MX     | Four-model mixture                 |
| M10    | Mixture: 10% shift toward baseline |

## Will the Democratic Party candidate win the 2026 Florida Senate election by 3% or more?
Contract 3343186; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        6.12 |         6.35 | +93.65 / −6.35   | 14.75×        |
| No     |       97.47 |        97.57 | +2.43 / −97.57   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    8.75 |     2.40 |        -1.60 |
| GB / N         | NEG      |   91.25 |    -6.31 |       -10.31 |
| ST / Y         | NEG      |    4.67 |    -1.67 |        -5.67 |
| ST / N         | NEG      |   95.33 |    -2.24 |        -6.24 |
| MX / Y         | WEAK     |    9.58 |     3.23 |        -0.77 |
| MX / N         | NEG      |   90.42 |    -7.15 |       -11.15 |
| M10 / Y        | WEAK     |    8.39 |     2.04 |        -1.96 |
| M10 / N        | NEG      |   91.61 |    -5.96 |        -9.96 |

## Will the Democratic Party candidate win the 2026 Iowa Senate election by 0%-3%?
Contract 3343531; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       26.39 |        27.15 | +72.85 / −27.15  | 2.68×         |
| No     |       81    |        81.62 | +18.38 / −81.62  | 0.23×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   16.65 |   -10.51 |       -14.51 |
| GB / N         | WEAK     |   83.35 |     1.74 |        -2.26 |
| ST / Y         | NEG      |   18.59 |    -8.56 |       -12.56 |
| ST / N         | NEG      |   81.41 |    -0.20 |        -4.20 |
| MX / Y         | NEG      |   17.54 |    -9.61 |       -13.61 |
| MX / N         | WEAK     |   82.46 |     0.85 |        -3.15 |
| M10 / Y        | NEG      |   17.04 |   -10.11 |       -14.11 |
| M10 / N        | WEAK     |   82.96 |     1.34 |        -2.66 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 0%-10%?
Contract 3343809; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         1   |         1.04 | +98.96 / −1.04   | 95.19×        |
| No     |        99.4 |        99.42 | +0.58 / −99.42   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.23 |    -0.81 |        -3.04 |
| GB / N         | WEAK     |   99.77 |     0.34 |        -3.66 |
| ST / Y         | NEG      |    0.28 |    -0.76 |        -3.04 |
| ST / N         | WEAK     |   99.72 |     0.29 |        -3.71 |
| MX / Y         | NEG      |    0.53 |    -0.51 |        -3.04 |
| MX / N         | WEAK     |   99.47 |     0.05 |        -3.95 |
| M10 / Y        | NEG      |    0.77 |    -0.27 |        -3.04 |
| M10 / N        | NEG      |   99.23 |    -0.19 |        -4.19 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 10%-15%?
Contract 3343810; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         2   |         2.08 | +97.92 / −2.08   | 47.11×        |
| No     |        98.7 |        98.75 | +1.25 / −98.75   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    2.20 |     0.12 |        -3.88 |
| GB / N         | NEG      |   97.80 |    -0.95 |        -4.95 |
| ST / Y         | NEG      |    1.72 |    -0.36 |        -4.08 |
| ST / N         | NEG      |   98.28 |    -0.47 |        -4.47 |
| MX / Y         | WEAK     |    2.98 |     0.90 |        -3.10 |
| MX / N         | NEG      |   97.02 |    -1.73 |        -5.73 |
| M10 / Y        | WEAK     |    4.05 |     1.97 |        -2.03 |
| M10 / N        | NEG      |   95.95 |    -2.80 |        -6.80 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 15%-20%?
Contract 3343811; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         2.8 |         2.91 | +97.09 / −2.91   | 33.38×        |
| No     |        98   |        98.08 | +1.92 / −98.08   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   10.84 |     7.93 |         3.93 |
| GB / N         | NEG      |   89.16 |    -8.92 |       -12.92 |
| ST / Y         | GO       |    8.29 |     5.38 |         1.38 |
| ST / N         | NEG      |   91.71 |    -6.37 |       -10.37 |
| MX / Y         | GO       |   11.75 |     8.84 |         4.84 |
| MX / N         | NEG      |   88.25 |    -9.83 |       -13.83 |
| M10 / Y        | GO       |   14.39 |    11.48 |         7.48 |
| M10 / N        | NEG      |   85.61 |   -12.47 |       -16.47 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 20%-25%?
Contract 3343812; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       15.87 |        16.4  | +83.60 / −16.40  | 5.10×         |
| No     |       89.66 |        90.03 | +9.97 / −90.03   | 0.11×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   26.64 |    10.24 |         6.24 |
| GB / N         | NEG      |   73.36 |   -16.67 |       -20.67 |
| ST / Y         | GO       |   26.03 |     9.63 |         5.63 |
| ST / N         | NEG      |   73.97 |   -16.06 |       -20.06 |
| MX / Y         | GO       |   27.23 |    10.83 |         6.83 |
| MX / N         | NEG      |   72.77 |   -17.26 |       -21.26 |
| M10 / Y        | GO       |   29.69 |    13.29 |         9.29 |
| M10 / N        | NEG      |   70.31 |   -19.72 |       -23.72 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 35%-40%?
Contract 3343815; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          19 |        19.62 | +80.38 / −19.62  | 4.10×         |
| No     |          83 |        83.56 | +16.44 / −83.56  | 0.20×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    6.19 |   -13.43 |       -17.43 |
| GB / N         | GO       |   93.81 |    10.25 |         6.25 |
| ST / Y         | NEG      |    4.22 |   -15.40 |       -19.40 |
| ST / N         | GO       |   95.78 |    12.22 |         8.22 |
| MX / Y         | NEG      |    5.08 |   -14.53 |       -18.53 |
| MX / N         | GO       |   94.92 |    11.35 |         7.35 |
| M10 / Y        | NEG      |    3.70 |   -15.91 |       -19.91 |
| M10 / N        | GO       |   96.30 |    12.73 |         8.73 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 40%-45%?
Contract 3343816; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       15.81 |        16.35 | +83.65 / −16.35  | 5.12×         |
| No     |       91    |        91.33 | +8.67 / −91.33   | 0.09×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.95 |   -15.40 |       -18.35 |
| GB / N         | GO       |   99.05 |     7.73 |         3.73 |
| ST / Y         | NEG      |    0.39 |   -15.95 |       -18.35 |
| ST / N         | GO       |   99.61 |     8.28 |         4.28 |
| MX / Y         | NEG      |    0.81 |   -15.54 |       -18.35 |
| MX / N         | GO       |   99.19 |     7.87 |         3.87 |
| M10 / Y        | NEG      |    0.55 |   -15.79 |       -18.35 |
| M10 / N        | GO       |   99.45 |     8.12 |         4.12 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 45% or more?
Contract 3343817; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         6.9 |         7.16 | +92.84 / −7.16   | 12.97×        |
| No     |        97   |        97.12 | +2.88 / −97.12   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.07 |    -7.08 |        -9.16 |
| GB / N         | WEAK     |   99.93 |     2.81 |        -1.19 |
| ST / Y         | NEG      |    0.03 |    -7.13 |        -9.16 |
| ST / N         | WEAK     |   99.98 |     2.86 |        -1.14 |
| MX / Y         | NEG      |    0.08 |    -7.08 |        -9.16 |
| MX / N         | WEAK     |   99.92 |     2.80 |        -1.20 |
| M10 / Y        | NEG      |    0.05 |    -7.11 |        -9.16 |
| M10 / N        | WEAK     |   99.95 |     2.84 |        -1.16 |

## Will the Democratic Party candidate win the 2026 Michigan Senate election by 3%-6%?
Contract 3343888; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          23 |        23.71 | +76.29 / −23.71  | 3.22×         |
| No     |          79 |        79.66 | +20.34 / −79.66  | 0.26×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   19.52 |    -4.19 |        -8.19 |
| GB / N         | WEAK     |   80.48 |     0.82 |        -3.18 |
| ST / Y         | NEG      |   23.67 |    -0.04 |        -4.04 |
| ST / N         | NEG      |   76.33 |    -3.33 |        -7.33 |
| MX / Y         | NEG      |   20.47 |    -3.24 |        -7.24 |
| MX / N         | NEG      |   79.53 |    -0.13 |        -4.13 |
| M10 / Y        | NEG      |   20.88 |    -2.83 |        -6.83 |
| M10 / N        | NEG      |   79.12 |    -0.54 |        -4.54 |

## Will the Democratic Party candidate win the 2026 Michigan Senate election by 6%-9%?
Contract 3343889; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        22   |        22.69 | +77.31 / −22.69  | 3.41×         |
| No     |        81.2 |        81.81 | +18.19 / −81.81  | 0.22×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   19.14 |    -3.54 |        -7.54 |
| GB / N         | NEG      |   80.86 |    -0.95 |        -4.95 |
| ST / Y         | WEAK     |   23.20 |     0.51 |        -3.49 |
| ST / N         | NEG      |   76.80 |    -5.01 |        -9.01 |
| MX / Y         | NEG      |   19.73 |    -2.96 |        -6.96 |
| MX / N         | NEG      |   80.27 |    -1.54 |        -5.54 |
| M10 / Y        | NEG      |   18.49 |    -4.20 |        -8.20 |
| M10 / N        | NEG      |   81.51 |    -0.30 |        -4.30 |

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 12%-15%?
Contract 3343942; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.01 |         9.34 | +90.66 / −9.34   | 9.71×         |
| No     |       95.12 |        95.31 | +4.69 / −95.31   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   19.73 |    10.39 |         6.39 |
| GB / N         | NEG      |   80.27 |   -15.04 |       -19.04 |
| ST / Y         | GO       |   20.99 |    11.65 |         7.65 |
| ST / N         | NEG      |   79.01 |   -16.29 |       -20.29 |
| MX / Y         | GO       |   15.58 |     6.24 |         2.24 |
| MX / N         | NEG      |   84.42 |   -10.89 |       -14.89 |
| M10 / Y        | GO       |   16.41 |     7.08 |         3.08 |
| M10 / N        | NEG      |   83.59 |   -11.72 |       -15.72 |

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 18% or more?
Contract 3343944; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        8.67 |         8.96 | +91.04 / −8.96   | 10.16×        |
| No     |       98.56 |        98.62 | +1.38 / −98.62   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   12.30 |     3.34 |        -0.66 |
| GB / N         | NEG      |   87.70 |   -10.92 |       -14.92 |
| ST / Y         | WEAK     |    9.24 |     0.28 |        -3.72 |
| ST / N         | NEG      |   90.76 |    -7.85 |       -11.85 |
| MX / Y         | NEG      |    7.28 |    -1.67 |        -5.67 |
| MX / N         | NEG      |   92.72 |    -5.90 |        -9.90 |
| M10 / Y        | NEG      |    8.68 |    -0.28 |        -4.28 |
| M10 / N        | NEG      |   91.32 |    -7.30 |       -11.30 |

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 3%-6%?
Contract 3343939; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       21    |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |       80.87 |        81.49 | +18.51 / −81.49  | 0.23×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    9.93 |   -11.73 |       -15.73 |
| GB / N         | GO       |   90.07 |     8.58 |         4.58 |
| ST / Y         | NEG      |    9.62 |   -12.04 |       -16.04 |
| ST / N         | GO       |   90.38 |     8.89 |         4.89 |
| MX / Y         | NEG      |   14.00 |    -7.66 |       -11.66 |
| MX / N         | GO       |   86.00 |     4.51 |         0.51 |
| M10 / Y        | NEG      |   13.04 |    -8.62 |       -12.62 |
| M10 / N        | GO       |   86.96 |     5.47 |         1.47 |

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 9%-12%?
Contract 3343941; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          15 |        15.51 | +84.49 / −15.51  | 5.45×         |
| No     |          86 |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   20.72 |     5.21 |         1.21 |
| GB / N         | NEG      |   79.28 |    -7.20 |       -11.20 |
| ST / Y         | GO       |   21.75 |     6.24 |         2.24 |
| ST / N         | NEG      |   78.25 |    -8.23 |       -12.23 |
| MX / Y         | WEAK     |   19.09 |     3.58 |        -0.42 |
| MX / N         | NEG      |   80.91 |    -5.57 |        -9.57 |
| M10 / Y        | WEAK     |   19.27 |     3.76 |        -0.24 |
| M10 / N        | NEG      |   80.73 |    -5.76 |        -9.76 |

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 12%-15%?
Contract 3343971; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10.39 |        10.77 | +89.23 / −10.77  | 8.29×         |
| No     |       91.7  |        92    | +8.00 / −92.00   | 0.09×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   14.90 |     4.14 |         0.14 |
| GB / N         | NEG      |   85.10 |    -6.91 |       -10.91 |
| ST / Y         | GO       |   16.71 |     5.94 |         1.94 |
| ST / N         | NEG      |   83.29 |    -8.71 |       -12.71 |
| MX / Y         | GO       |   15.45 |     4.69 |         0.69 |
| MX / N         | NEG      |   84.55 |    -7.46 |       -11.46 |
| M10 / Y        | GO       |   15.49 |     4.72 |         0.72 |
| M10 / N        | NEG      |   84.51 |    -7.49 |       -11.49 |

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 15%-18%?
Contract 3343972; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          16 |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |          86 |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   15.54 |    -1.00 |        -5.00 |
| GB / N         | NEG      |   84.46 |    -2.02 |        -6.02 |
| ST / Y         | WEAK     |   17.72 |     1.18 |        -2.82 |
| ST / N         | NEG      |   82.28 |    -4.20 |        -8.20 |
| MX / Y         | NEG      |   16.12 |    -0.41 |        -4.41 |
| MX / N         | NEG      |   83.88 |    -2.61 |        -6.61 |
| M10 / Y        | NEG      |   16.12 |    -0.41 |        -4.41 |
| M10 / N        | NEG      |   83.88 |    -2.61 |        -6.61 |

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 18%-21%?
Contract 3343973; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          25 |        25.75 | +74.25 / −25.75  | 2.88×         |
| No     |          77 |        77.71 | +22.29 / −77.71  | 0.29×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   13.91 |   -11.84 |       -15.84 |
| GB / N         | GO       |   86.09 |     8.39 |         4.39 |
| ST / Y         | NEG      |   15.55 |   -10.20 |       -14.20 |
| ST / N         | GO       |   84.45 |     6.74 |         2.74 |
| MX / Y         | NEG      |   14.29 |   -11.46 |       -15.46 |
| MX / N         | GO       |   85.71 |     8.01 |         4.01 |
| M10 / Y        | NEG      |   14.25 |   -11.50 |       -15.50 |
| M10 / N        | GO       |   85.75 |     8.05 |         4.05 |

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 6%-9%?
Contract 3343969; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        6.4  |         6.64 | +93.36 / −6.64   | 14.06×        |
| No     |       94.88 |        95.07 | +4.93 / −95.07   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    8.66 |     2.02 |        -1.98 |
| GB / N         | NEG      |   91.34 |    -3.74 |        -7.74 |
| ST / Y         | WEAK     |    7.88 |     1.24 |        -2.76 |
| ST / N         | NEG      |   92.12 |    -2.95 |        -6.95 |
| MX / Y         | WEAK     |    8.64 |     2.00 |        -2.00 |
| MX / N         | NEG      |   91.36 |    -3.71 |        -7.71 |
| M10 / Y        | WEAK     |    8.70 |     2.06 |        -1.94 |
| M10 / N        | NEG      |   91.30 |    -3.78 |        -7.78 |

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 9%-12%?
Contract 3343970; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        8.13 |         8.43 | +91.57 / −8.43   | 10.86×        |
| No     |       95.5  |        95.67 | +4.33 / −95.67   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   12.26 |     3.83 |        -0.17 |
| GB / N         | NEG      |   87.74 |    -7.94 |       -11.94 |
| ST / Y         | GO       |   12.71 |     4.28 |         0.28 |
| ST / N         | NEG      |   87.29 |    -8.38 |       -12.38 |
| MX / Y         | WEAK     |   12.36 |     3.93 |        -0.07 |
| MX / N         | NEG      |   87.64 |    -8.03 |       -12.03 |
| M10 / Y        | GO       |   12.43 |     4.00 |         0.00 |
| M10 / N        | NEG      |   87.57 |    -8.11 |       -12.11 |

## Will the Democratic Party candidate win the 2026 North Carolina Senate election by 12%-15%?
Contract 3344037; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       26.14 |        26.9  | +73.10 / −26.90  | 2.72×         |
| No     |       89.49 |        89.87 | +10.13 / −89.87  | 0.11×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    6.68 |   -20.22 |       -24.22 |
| GB / N         | WEAK     |   93.32 |     3.45 |        -0.55 |
| ST / Y         | NEG      |    4.72 |   -22.17 |       -26.17 |
| ST / N         | GO       |   95.28 |     5.41 |         1.41 |
| MX / Y         | NEG      |    4.05 |   -22.85 |       -26.85 |
| MX / N         | GO       |   95.95 |     6.09 |         2.09 |
| M10 / Y        | NEG      |    4.01 |   -22.89 |       -26.89 |
| M10 / N        | GO       |   95.99 |     6.12 |         2.12 |

## Will the Democratic Party candidate win the 2026 North Carolina Senate election by 3%-6%?
Contract 3344034; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       16    |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |       85.16 |        85.67 | +14.33 / −85.67  | 0.17×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   23.03 |     6.49 |         2.49 |
| GB / N         | NEG      |   76.97 |    -8.69 |       -12.69 |
| ST / Y         | GO       |   27.96 |    11.42 |         7.42 |
| ST / N         | NEG      |   72.04 |   -13.62 |       -17.62 |
| MX / Y         | GO       |   28.21 |    11.67 |         7.67 |
| MX / N         | NEG      |   71.79 |   -13.88 |       -17.88 |
| M10 / Y        | GO       |   28.19 |    11.66 |         7.66 |
| M10 / N        | NEG      |   71.81 |   -13.86 |       -17.86 |

## Will the Democratic Party candidate win the 2026 North Carolina Senate election by 9%-12%?
Contract 3344036; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       18.51 |        19.11 | +80.89 / −19.11  | 4.23×         |
| No     |       87.4  |        87.84 | +12.16 / −87.84  | 0.14×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   14.23 |    -4.89 |        -8.89 |
| GB / N         | NEG      |   85.77 |    -2.07 |        -6.07 |
| ST / Y         | NEG      |   13.50 |    -5.62 |        -9.62 |
| ST / N         | NEG      |   86.50 |    -1.34 |        -5.34 |
| MX / Y         | NEG      |   11.48 |    -7.64 |       -11.64 |
| MX / N         | WEAK     |   88.52 |     0.68 |        -3.32 |
| M10 / Y        | NEG      |   11.41 |    -7.71 |       -11.71 |
| M10 / N        | WEAK     |   88.59 |     0.75 |        -3.25 |

## Will the Democratic Party candidate win the 2026 Ohio Senate election by 0%-3%?
Contract 3344047; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          19 |        19.62 | +80.38 / −19.62  | 4.10×         |
| No     |          83 |        83.56 | +16.44 / −83.56  | 0.20×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   20.16 |     0.54 |        -3.46 |
| GB / N         | NEG      |   79.84 |    -3.72 |        -7.72 |
| ST / Y         | GO       |   24.12 |     4.50 |         0.50 |
| ST / N         | NEG      |   75.88 |    -7.68 |       -11.68 |
| MX / Y         | WEAK     |   21.96 |     2.34 |        -1.66 |
| MX / N         | NEG      |   78.04 |    -5.52 |        -9.52 |
| M10 / Y        | WEAK     |   22.35 |     2.73 |        -1.27 |
| M10 / N        | NEG      |   77.65 |    -5.91 |        -9.91 |

## Will the Democratic Party candidate win the 2026 Ohio Senate election by 3%-6%?
Contract 3344048; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          23 |        23.71 | +76.29 / −23.71  | 3.22×         |
| No     |          80 |        80.64 | +19.36 / −80.64  | 0.24×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   20.20 |    -3.50 |        -7.50 |
| GB / N         | NEG      |   79.80 |    -0.84 |        -4.84 |
| ST / Y         | WEAK     |   24.94 |     1.24 |        -2.76 |
| ST / N         | NEG      |   75.06 |    -5.58 |        -9.58 |
| MX / Y         | NEG      |   21.15 |    -2.56 |        -6.56 |
| MX / N         | NEG      |   78.85 |    -1.79 |        -5.79 |
| M10 / Y        | NEG      |   20.11 |    -3.60 |        -7.60 |
| M10 / N        | NEG      |   79.89 |    -0.75 |        -4.75 |

## Will the Democratic Party candidate win the 2026 Ohio Senate election by 6%-9%?
Contract 3344049; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          81 |        81.62 | +18.38 / −81.62  | 0.23×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   15.40 |    -6.26 |       -10.26 |
| GB / N         | WEAK     |   84.60 |     2.98 |        -1.02 |
| ST / Y         | NEG      |   16.19 |    -5.47 |        -9.47 |
| ST / N         | WEAK     |   83.81 |     2.19 |        -1.81 |
| MX / Y         | NEG      |   14.57 |    -7.09 |       -11.09 |
| MX / N         | WEAK     |   85.43 |     3.81 |        -0.19 |
| M10 / Y        | NEG      |   13.08 |    -8.58 |       -12.58 |
| M10 / N        | GO       |   86.92 |     5.30 |         1.30 |

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 0%-5%?
Contract 3344097; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.53 |         9.87 | +90.13 / −9.87   | 9.13×         |
| No     |       99.7  |        99.71 | +0.29 / −99.71   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.09 |    -9.78 |       -11.87 |
| GB / N         | WEAK     |   99.91 |     0.20 |        -3.80 |
| ST / Y         | NEG      |    0.11 |    -9.76 |       -11.87 |
| ST / N         | WEAK     |   99.89 |     0.18 |        -3.82 |
| MX / Y         | NEG      |    0.66 |    -9.21 |       -11.87 |
| MX / N         | NEG      |   99.34 |    -0.37 |        -4.37 |
| M10 / Y        | NEG      |    0.77 |    -9.10 |       -11.87 |
| M10 / N        | NEG      |   99.23 |    -0.48 |        -4.48 |

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 10%-15%?
Contract 3344099; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        1.51 |         1.57 | +98.43 / −1.57   | 62.75×        |
| No     |       99.3  |        99.33 | +0.67 / −99.33   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    4.53 |     2.96 |        -1.04 |
| GB / N         | NEG      |   95.47 |    -3.86 |        -7.86 |
| ST / Y         | WEAK     |    3.53 |     1.96 |        -2.04 |
| ST / N         | NEG      |   96.47 |    -2.86 |        -6.86 |
| MX / Y         | GO       |    7.72 |     6.15 |         2.15 |
| MX / N         | NEG      |   92.28 |    -7.05 |       -11.05 |
| M10 / Y        | GO       |    8.45 |     6.88 |         2.88 |
| M10 / N        | NEG      |   91.55 |    -7.77 |       -11.77 |

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 15%-20%?
Contract 3344100; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        8.86 |         9.18 | +90.82 / −9.18   | 9.89×         |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   14.27 |     5.09 |         1.09 |
| GB / N         | NEG      |   85.73 |   -13.89 |       -17.89 |
| ST / Y         | WEAK     |   11.22 |     2.04 |        -1.96 |
| ST / N         | NEG      |   88.78 |   -10.83 |       -14.83 |
| MX / Y         | GO       |   16.65 |     7.47 |         3.47 |
| MX / N         | NEG      |   83.35 |   -16.26 |       -20.26 |
| M10 / Y        | GO       |   17.63 |     8.45 |         4.45 |
| M10 / N        | NEG      |   82.37 |   -17.25 |       -21.25 |

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 20%-25%?
Contract 3344101; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        16.9 |        17.46 | +82.54 / −17.46  | 4.73×         |
| No     |        88.9 |        89.29 | +10.71 / −89.29  | 0.12×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   26.25 |     8.79 |         4.79 |
| GB / N         | NEG      |   73.75 |   -15.54 |       -19.54 |
| ST / Y         | GO       |   24.83 |     7.37 |         3.37 |
| ST / N         | NEG      |   75.17 |   -14.13 |       -18.13 |
| MX / Y         | GO       |   25.32 |     7.86 |         3.86 |
| MX / N         | NEG      |   74.68 |   -14.61 |       -18.61 |
| M10 / Y        | GO       |   25.88 |     8.42 |         4.42 |
| M10 / N        | NEG      |   74.12 |   -15.17 |       -19.17 |

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 25%-30%?
Contract 3344102; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          22 |        22.69 | +77.31 / −22.69  | 3.41×         |
| No     |          79 |        79.66 | +20.34 / −79.66  | 0.26×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   28.21 |     5.52 |         1.52 |
| GB / N         | NEG      |   71.79 |    -7.87 |       -11.87 |
| ST / Y         | GO       |   32.07 |     9.39 |         5.39 |
| ST / N         | NEG      |   67.92 |   -11.74 |       -15.74 |
| MX / Y         | WEAK     |   25.34 |     2.65 |        -1.35 |
| MX / N         | NEG      |   74.66 |    -5.00 |        -9.00 |
| M10 / Y        | WEAK     |   24.57 |     1.89 |        -2.11 |
| M10 / N        | NEG      |   75.43 |    -4.24 |        -8.24 |

## Will the Democratic Party candidate win the 2026 Texas Senate election by 3%-6%?
Contract 3344142; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       22.6  |        23.3  | +76.70 / −23.30  | 3.29×         |
| No     |       80.59 |        81.22 | +18.78 / −81.22  | 0.23×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   18.36 |    -4.94 |        -8.94 |
| GB / N         | WEAK     |   81.64 |     0.42 |        -3.58 |
| ST / Y         | NEG      |   19.16 |    -4.14 |        -8.14 |
| ST / N         | NEG      |   80.84 |    -0.38 |        -4.38 |
| MX / Y         | NEG      |   17.81 |    -5.49 |        -9.49 |
| MX / N         | WEAK     |   82.19 |     0.98 |        -3.02 |
| M10 / Y        | NEG      |   17.92 |    -5.38 |        -9.38 |
| M10 / N        | WEAK     |   82.08 |     0.86 |        -3.14 |

## Will the Democratic Party candidate win the 2026 Texas Senate election by 9%-12%?
Contract 3344144; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        4.95 |         5.14 | +94.86 / −5.14   | 18.46×        |
| No     |       95.2  |        95.38 | +4.62 / −95.38   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    3.57 |    -1.57 |        -5.57 |
| GB / N         | WEAK     |   96.43 |     1.05 |        -2.95 |
| ST / Y         | NEG      |    1.94 |    -3.20 |        -7.14 |
| ST / N         | WEAK     |   98.06 |     2.68 |        -1.32 |
| MX / Y         | NEG      |    2.78 |    -2.36 |        -6.36 |
| MX / N         | WEAK     |   97.22 |     1.84 |        -2.16 |
| M10 / Y        | NEG      |    2.82 |    -2.32 |        -6.32 |
| M10 / N        | WEAK     |   97.18 |     1.80 |        -2.20 |

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 0%-3%?
Contract 3344162; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         0.9 |         0.94 | +99.06 / −0.94   | 105.87×       |
| No     |        99.2 |        99.23 | +0.77 / −99.23   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    1.19 |     0.26 |        -2.94 |
| GB / N         | NEG      |   98.81 |    -0.42 |        -4.42 |
| ST / Y         | NEG      |    0.76 |    -0.18 |        -2.94 |
| ST / N         | WEAK     |   99.24 |     0.01 |        -3.99 |
| MX / Y         | WEAK     |    1.73 |     0.80 |        -2.94 |
| MX / N         | NEG      |   98.27 |    -0.96 |        -4.96 |
| M10 / Y        | WEAK     |    1.71 |     0.78 |        -2.94 |
| M10 / N        | NEG      |   98.29 |    -0.94 |        -4.94 |

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 12%-15%?
Contract 3344166; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10.19 |        10.55 | +89.45 / −10.55  | 8.47×         |
| No     |       93    |        93.26 | +6.74 / −93.26   | 0.07×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   14.02 |     3.46 |        -0.54 |
| GB / N         | NEG      |   85.98 |    -7.28 |       -11.28 |
| ST / Y         | GO       |   14.88 |     4.33 |         0.33 |
| ST / N         | NEG      |   85.12 |    -8.14 |       -12.14 |
| MX / Y         | WEAK     |   13.61 |     3.06 |        -0.94 |
| MX / N         | NEG      |   86.39 |    -6.87 |       -10.87 |
| M10 / Y        | WEAK     |   13.54 |     2.99 |        -1.01 |
| M10 / N        | NEG      |   86.46 |    -6.80 |       -10.80 |

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 18%-21%?
Contract 3344168; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       27.37 |        28.16 | +71.84 / −28.16  | 2.55×         |
| No     |       74.64 |        75.4  | +24.60 / −75.40  | 0.33×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   16.42 |   -11.75 |       -15.75 |
| GB / N         | GO       |   83.58 |     8.18 |         4.18 |
| ST / Y         | NEG      |   19.27 |    -8.89 |       -12.89 |
| ST / N         | GO       |   80.73 |     5.33 |         1.33 |
| MX / Y         | NEG      |   15.59 |   -12.58 |       -16.58 |
| MX / N         | GO       |   84.41 |     9.01 |         5.01 |
| M10 / Y        | NEG      |   15.65 |   -12.51 |       -16.51 |
| M10 / N        | GO       |   84.35 |     8.95 |         4.95 |

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 3%-6%?
Contract 3344163; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         1.2 |         1.25 | +98.75 / −1.25   | 79.17×        |
| No     |        99.1 |        99.14 | +0.86 / −99.14   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    2.89 |     1.64 |        -2.36 |
| GB / N         | NEG      |   97.11 |    -2.02 |        -6.02 |
| ST / Y         | WEAK     |    2.00 |     0.75 |        -3.25 |
| ST / N         | NEG      |   98.00 |    -1.13 |        -5.13 |
| MX / Y         | WEAK     |    3.39 |     2.15 |        -1.85 |
| MX / N         | NEG      |   96.61 |    -2.53 |        -6.53 |
| M10 / Y        | WEAK     |    3.33 |     2.08 |        -1.92 |
| M10 / N        | NEG      |   96.67 |    -2.46 |        -6.46 |

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 6%-9%?
Contract 3344164; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        4.8  |         4.98 | +95.02 / −4.98   | 19.07×        |
| No     |       97.54 |        97.64 | +2.36 / −97.64   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    5.85 |     0.86 |        -3.14 |
| GB / N         | NEG      |   94.15 |    -3.49 |        -7.49 |
| ST / Y         | NEG      |    4.16 |    -0.83 |        -4.83 |
| ST / N         | NEG      |   95.84 |    -1.80 |        -5.80 |
| MX / Y         | WEAK     |    5.98 |     1.00 |        -3.00 |
| MX / N         | NEG      |   94.02 |    -3.63 |        -7.63 |
| M10 / Y        | WEAK     |    5.88 |     0.90 |        -3.10 |
| M10 / N        | NEG      |   94.12 |    -3.52 |        -7.52 |

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 9%-12%?
Contract 3344165; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.21 |         9.55 | +90.45 / −9.55   | 9.48×         |
| No     |       96.36 |        96.5  | +3.50 / −96.50   | 0.04×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    9.90 |     0.35 |        -3.65 |
| GB / N         | NEG      |   90.10 |    -6.40 |       -10.40 |
| ST / Y         | NEG      |    8.57 |    -0.97 |        -4.97 |
| ST / N         | NEG      |   91.43 |    -5.07 |        -9.07 |
| MX / Y         | WEAK     |    9.60 |     0.05 |        -3.95 |
| MX / N         | NEG      |   90.40 |    -6.10 |       -10.10 |
| M10 / Y        | NEG      |    9.46 |    -0.08 |        -4.08 |
| M10 / N        | NEG      |   90.54 |    -5.97 |        -9.97 |

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

## Will the Democrats win the Alabama Senate race in 2026?
Contract 630627; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        3.64 |         3.78 | +96.22 / −3.78   | 25.45×        |
| No     |       99.5  |        99.52 | +0.48 / −99.52   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.06 |    -3.72 |        -5.78 |
| GB / N         | WEAK     |   99.94 |     0.42 |        -3.58 |
| ST / Y         | NEG      |    0.15 |    -3.63 |        -5.78 |
| ST / N         | WEAK     |   99.85 |     0.33 |        -3.67 |
| MX / Y         | NEG      |    1.54 |    -2.25 |        -5.78 |
| MX / N         | NEG      |   98.46 |    -1.06 |        -5.06 |
| M10 / Y        | NEG      |    1.46 |    -2.32 |        -5.78 |
| M10 / N        | NEG      |   98.54 |    -0.98 |        -4.98 |

## Will the Democrats win the Arkansas Senate race in 2026?
Contract 630653; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        6.1  |         6.33 | +93.67 / −6.33   | 14.80×        |
| No     |       95.95 |        96.1  | +3.90 / −96.10   | 0.04×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.24 |    -6.09 |        -8.33 |
| GB / N         | WEAK     |   99.76 |     3.66 |        -0.34 |
| ST / Y         | NEG      |    0.79 |    -5.54 |        -8.33 |
| ST / N         | WEAK     |   99.21 |     3.11 |        -0.89 |
| MX / Y         | WEAK     |    6.64 |     0.31 |        -3.69 |
| MX / N         | NEG      |   93.36 |    -2.74 |        -6.74 |
| M10 / Y        | NEG      |    5.78 |    -0.55 |        -4.55 |
| M10 / N        | NEG      |   94.22 |    -1.88 |        -5.88 |

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

## Will the Democrats win the Iowa Senate race in 2026?
Contract 630733; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       45    |        45.99 | +54.01 / −45.99  | 1.17×         |
| No     |       56.95 |        57.93 | +42.07 / −57.93  | 0.73×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   36.18 |    -9.81 |       -13.81 |
| GB / N         | GO       |   63.82 |     5.89 |         1.89 |
| ST / Y         | NEG      |   33.44 |   -12.55 |       -16.55 |
| ST / N         | GO       |   66.56 |     8.63 |         4.63 |
| MX / Y         | NEG      |   36.92 |    -9.07 |       -13.07 |
| MX / N         | GO       |   63.08 |     5.15 |         1.15 |
| M10 / Y        | NEG      |   35.32 |   -10.67 |       -14.67 |
| M10 / N        | GO       |   64.68 |     6.75 |         2.75 |

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

## Will the Democrats win the Kentucky Senate race in 2026?
Contract 630759; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        4.39 |         4.56 | +95.44 / −4.56   | 20.92×        |
| No     |       97.38 |        97.48 | +2.52 / −97.48   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.88 |    -2.68 |        -6.56 |
| GB / N         | WEAK     |   98.12 |     0.64 |        -3.36 |
| ST / Y         | NEG      |    1.42 |    -3.14 |        -6.56 |
| ST / N         | WEAK     |   98.58 |     1.10 |        -2.90 |
| MX / Y         | NEG      |    3.90 |    -0.67 |        -4.67 |
| MX / N         | NEG      |   96.10 |    -1.38 |        -5.38 |
| M10 / Y        | NEG      |    2.96 |    -1.60 |        -5.60 |
| M10 / N        | NEG      |   97.04 |    -0.44 |        -4.44 |

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

## Will the Democrats win the New Mexico Senate race in 2026?
Contract 630870; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       97.97 |        98.05 | +1.95 / −98.05   | 0.02×         |
| No     |        3.27 |         3.4  | +96.60 / −3.40   | 28.44×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   98.10 |     0.05 |        -3.95 |
| GB / N         | NEG      |    1.90 |    -1.50 |        -5.40 |
| ST / Y         | WEAK     |   99.07 |     1.01 |        -2.99 |
| ST / N         | NEG      |    0.93 |    -2.46 |        -5.40 |
| MX / Y         | WEAK     |   98.19 |     0.14 |        -3.86 |
| MX / N         | NEG      |    1.81 |    -1.59 |        -5.40 |
| M10 / Y        | WEAK     |   98.15 |     0.10 |        -3.90 |
| M10 / N        | NEG      |    1.85 |    -1.55 |        -5.40 |

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

## Will the Republican Party candidate win the 2026 Alabama Senate election by 0%-5%?
Contract 3343107; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       16.93 |        17.45 | +82.55 / −17.45  | 4.73×         |
| No     |       97.3  |        97.41 | +2.59 / −97.41   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.61 |   -16.84 |       -19.45 |
| GB / N         | WEAK     |   99.39 |     1.99 |        -2.01 |
| ST / Y         | NEG      |    0.68 |   -16.78 |       -19.45 |
| ST / N         | WEAK     |   99.33 |     1.92 |        -2.08 |
| MX / Y         | NEG      |    3.00 |   -14.45 |       -18.45 |
| MX / N         | NEG      |   97.00 |    -0.41 |        -4.41 |
| M10 / Y        | NEG      |    2.90 |   -14.56 |       -18.56 |
| M10 / N        | NEG      |   97.10 |    -0.30 |        -4.30 |

## Will the Republican Party candidate win the 2026 Alabama Senate election by 20%-25%?
Contract 3343103; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        21   |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |        80.1 |        80.74 | +19.26 / −80.74  | 0.24×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   29.12 |     7.45 |         3.45 |
| GB / N         | NEG      |   70.88 |    -9.85 |       -13.85 |
| ST / Y         | GO       |   34.48 |    12.81 |         8.81 |
| ST / N         | NEG      |   65.53 |   -15.21 |       -19.21 |
| MX / Y         | WEAK     |   25.53 |     3.87 |        -0.13 |
| MX / N         | NEG      |   74.47 |    -6.27 |       -10.27 |
| M10 / Y        | GO       |   25.73 |     4.07 |         0.07 |
| M10 / N        | NEG      |   74.27 |    -6.47 |       -10.47 |

## Will the Republican Party candidate win the 2026 Alabama Senate election by 35% or more?
Contract 3343100; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       23.93 |        24.65 | +75.35 / −24.65  | 3.06×         |
| No     |       98.92 |        98.96 | +1.04 / −98.96   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.84 |   -22.81 |       -26.65 |
| GB / N         | NEG      |   98.16 |    -0.80 |        -4.80 |
| ST / Y         | NEG      |    1.01 |   -23.63 |       -26.65 |
| ST / N         | WEAK     |   98.99 |     0.03 |        -3.97 |
| MX / Y         | NEG      |    2.52 |   -22.13 |       -26.13 |
| MX / N         | NEG      |   97.48 |    -1.48 |        -5.48 |
| M10 / Y        | NEG      |    2.67 |   -21.98 |       -25.98 |
| M10 / N        | NEG      |   97.33 |    -1.63 |        -5.63 |

## Will the Republican Party candidate win the 2026 Alabama Senate election by 5%-10%?
Contract 3343106; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       16    |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |       89.34 |        89.72 | +10.28 / −89.72  | 0.11×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    3.67 |   -12.87 |       -16.87 |
| GB / N         | GO       |   96.33 |     6.61 |         2.61 |
| ST / Y         | NEG      |    2.84 |   -13.70 |       -17.70 |
| ST / N         | GO       |   97.16 |     7.44 |         3.44 |
| MX / Y         | NEG      |    7.20 |    -9.33 |       -13.33 |
| MX / N         | WEAK     |   92.80 |     3.07 |        -0.93 |
| M10 / Y        | NEG      |    6.97 |    -9.57 |       -13.57 |
| M10 / N        | WEAK     |   93.03 |     3.31 |        -0.69 |

## Will the Republican Party candidate win the 2026 Arkansas Senate election by 10%-15%?
Contract 3343124; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       28.31 |        29.12 | +70.88 / −29.12  | 2.43×         |
| No     |       73.8  |        74.57 | +25.43 / −74.57  | 0.34×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   16.18 |   -12.94 |       -16.94 |
| GB / N         | GO       |   83.82 |     9.25 |         5.25 |
| ST / Y         | NEG      |   16.19 |   -12.93 |       -16.93 |
| ST / N         | GO       |   83.81 |     9.23 |         5.23 |
| MX / Y         | NEG      |   17.99 |   -11.13 |       -15.13 |
| MX / N         | GO       |   82.01 |     7.44 |         3.44 |
| M10 / Y        | NEG      |   17.22 |   -11.90 |       -15.90 |
| M10 / N        | GO       |   82.78 |     8.21 |         4.21 |

## Will the Republican Party candidate win the 2026 Arkansas Senate election by 20%-25%?
Contract 3343122; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          11 |        11.39 | +88.61 / −11.39  | 7.78×         |
| No     |          91 |        91.33 | +8.67 / −91.33   | 0.09×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   25.96 |    14.57 |        10.57 |
| GB / N         | NEG      |   74.04 |   -17.28 |       -21.28 |
| ST / Y         | GO       |   28.23 |    16.83 |        12.83 |
| ST / N         | NEG      |   71.78 |   -19.55 |       -23.55 |
| MX / Y         | GO       |   18.79 |     7.40 |         3.40 |
| MX / N         | NEG      |   81.21 |   -10.12 |       -14.12 |
| M10 / Y        | GO       |   19.87 |     8.48 |         4.48 |
| M10 / N        | NEG      |   80.13 |   -11.20 |       -15.20 |

## Will the Republican Party candidate win the 2026 Arkansas Senate election by 25%-30%?
Contract 3343121; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        7    |         7.26 | +92.74 / −7.26   | 12.77×        |
| No     |       95.95 |        96.11 | +3.89 / −96.11   | 0.04×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   16.05 |     8.79 |         4.79 |
| GB / N         | NEG      |   83.95 |   -12.15 |       -16.15 |
| ST / Y         | GO       |   13.43 |     6.16 |         2.16 |
| ST / N         | NEG      |   86.58 |    -9.53 |       -13.53 |
| MX / Y         | WEAK     |   10.14 |     2.87 |        -1.13 |
| MX / N         | NEG      |   89.86 |    -6.24 |       -10.24 |
| M10 / Y        | GO       |   11.52 |     4.26 |         0.26 |
| M10 / N        | NEG      |   88.48 |    -7.63 |       -11.63 |

## Will the Republican Party candidate win the 2026 Arkansas Senate election by 35%-40%?
Contract 3343119; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.46 |         9.81 | +90.19 / −9.81   | 9.20×         |
| No     |       96.52 |        96.65 | +3.35 / −96.65   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.46 |    -8.35 |       -11.81 |
| GB / N         | WEAK     |   98.54 |     1.89 |        -2.11 |
| ST / Y         | NEG      |    0.56 |    -9.25 |       -11.81 |
| ST / N         | WEAK     |   99.44 |     2.79 |        -1.21 |
| MX / Y         | NEG      |    1.04 |    -8.77 |       -11.81 |
| MX / N         | WEAK     |   98.96 |     2.31 |        -1.69 |
| M10 / Y        | NEG      |    1.25 |    -8.56 |       -11.81 |
| M10 / N        | WEAK     |   98.75 |     2.10 |        -1.90 |

## Will the Republican Party candidate win the 2026 Florida Senate election by 12%-15%?
Contract 3343180; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        8.64 |         8.96 | +91.04 / −8.96   | 10.17×        |
| No     |       97.15 |        97.26 | +2.74 / −97.26   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    9.31 |     0.36 |        -3.64 |
| GB / N         | NEG      |   90.69 |    -6.57 |       -10.57 |
| ST / Y         | NEG      |    7.39 |    -1.57 |        -5.57 |
| ST / N         | NEG      |   92.61 |    -4.65 |        -8.65 |
| MX / Y         | NEG      |    8.79 |    -0.17 |        -4.17 |
| MX / N         | NEG      |   91.21 |    -6.05 |       -10.05 |
| M10 / Y        | WEAK     |    9.60 |     0.64 |        -3.36 |
| M10 / N        | NEG      |   90.40 |    -6.86 |       -10.86 |

## Will the Republican Party candidate win the 2026 Florida Senate election by 15%-18%?
Contract 3343179; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        3.34 |         3.46 | +96.54 / −3.46   | 27.87×        |
| No     |       98.45 |        98.51 | +1.49 / −98.51   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    4.97 |     1.51 |        -2.49 |
| GB / N         | NEG      |   95.03 |    -3.48 |        -7.48 |
| ST / Y         | NEG      |    2.97 |    -0.49 |        -4.49 |
| ST / N         | NEG      |   97.03 |    -1.48 |        -5.48 |
| MX / Y         | WEAK     |    4.68 |     1.22 |        -2.78 |
| MX / N         | NEG      |   95.32 |    -3.20 |        -7.20 |
| M10 / Y        | WEAK     |    5.31 |     1.85 |        -2.15 |
| M10 / N        | NEG      |   94.69 |    -3.82 |        -7.82 |

## Will the Republican Party candidate win the 2026 Iowa Senate election by 0%-3%?
Contract 3343530; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        27.6 |        28.4  | +71.60 / −28.40  | 2.52×         |
| No     |        75   |        75.75 | +24.25 / −75.75  | 0.32×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   19.82 |    -8.57 |       -12.57 |
| GB / N         | GO       |   80.18 |     4.43 |         0.43 |
| ST / Y         | NEG      |   24.07 |    -4.33 |        -8.33 |
| ST / N         | WEAK     |   75.93 |     0.18 |        -3.82 |
| MX / Y         | NEG      |   20.92 |    -7.48 |       -11.48 |
| MX / N         | WEAK     |   79.08 |     3.33 |        -0.67 |
| M10 / Y        | NEG      |   20.77 |    -7.63 |       -11.63 |
| M10 / N        | WEAK     |   79.23 |     3.48 |        -0.52 |

## Will the Republican Party candidate win the 2026 Iowa Senate election by 3%-6%?
Contract 3343529; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          80 |        80.64 | +19.36 / −80.64  | 0.24×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   18.40 |    -3.26 |        -7.26 |
| GB / N         | WEAK     |   81.60 |     0.96 |        -3.04 |
| ST / Y         | NEG      |   21.49 |    -0.17 |        -4.17 |
| ST / N         | NEG      |   78.51 |    -2.13 |        -6.13 |
| MX / Y         | NEG      |   19.11 |    -2.56 |        -6.56 |
| MX / N         | WEAK     |   80.89 |     0.25 |        -3.75 |
| M10 / Y        | NEG      |   19.57 |    -2.09 |        -6.09 |
| M10 / N        | NEG      |   80.43 |    -0.21 |        -4.21 |

## Will the Republican Party candidate win the 2026 Iowa Senate election by 6%-9%?
Contract 3343528; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          12 |        12.42 | +87.58 / −12.42  | 7.05×         |
| No     |          90 |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   13.31 |     0.88 |        -3.12 |
| GB / N         | NEG      |   86.69 |    -3.67 |        -7.67 |
| ST / Y         | WEAK     |   13.24 |     0.82 |        -3.18 |
| ST / N         | NEG      |   86.76 |    -3.60 |        -7.60 |
| MX / Y         | WEAK     |   12.81 |     0.38 |        -3.62 |
| MX / N         | NEG      |   87.19 |    -3.17 |        -7.17 |
| M10 / Y        | WEAK     |   13.32 |     0.90 |        -3.10 |
| M10 / N        | NEG      |   86.68 |    -3.68 |        -7.68 |

## Will the Republican Party candidate win the 2026 Kansas Senate election by 10%-15%?
Contract 3343544; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          10 |        10.36 | +89.64 / −10.36  | 8.65×         |
| No     |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   22.83 |    12.47 |         8.47 |
| GB / N         | NEG      |   77.17 |   -15.13 |       -19.13 |
| ST / Y         | GO       |   22.34 |    11.98 |         7.98 |
| ST / N         | NEG      |   77.66 |   -14.64 |       -18.64 |
| MX / Y         | GO       |   21.50 |    11.14 |         7.14 |
| MX / N         | NEG      |   78.50 |   -13.80 |       -17.80 |
| M10 / Y        | GO       |   20.08 |     9.72 |         5.72 |
| M10 / N        | NEG      |   79.92 |   -12.37 |       -16.37 |

## Will the Republican Party candidate win the 2026 Kansas Senate election by 15%-20%?
Contract 3343543; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           6 |         6.23 | +93.77 / −6.23   | 15.06×        |
| No     |          97 |        97.12 | +2.88 / −97.12   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    6.74 |     0.52 |        -3.48 |
| GB / N         | NEG      |   93.26 |    -3.86 |        -7.86 |
| ST / Y         | NEG      |    4.42 |    -1.81 |        -5.81 |
| ST / N         | NEG      |   95.58 |    -1.54 |        -5.54 |
| MX / Y         | NEG      |    5.86 |    -0.36 |        -4.36 |
| MX / N         | NEG      |   94.14 |    -2.98 |        -6.98 |
| M10 / Y        | NEG      |    5.18 |    -1.04 |        -5.04 |
| M10 / N        | NEG      |   94.82 |    -2.30 |        -6.30 |

## Will the Republican Party candidate win the 2026 Kansas Senate election by 20%-25%?
Contract 3343542; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        8.85 |         9.17 | +90.83 / −9.17   | 9.90×         |
| No     |       96.99 |        97.11 | +2.89 / −97.11   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.90 |    -8.27 |       -11.17 |
| GB / N         | WEAK     |   99.10 |     1.99 |        -2.01 |
| ST / Y         | NEG      |    0.37 |    -8.80 |       -11.17 |
| ST / N         | WEAK     |   99.63 |     2.52 |        -1.48 |
| MX / Y         | NEG      |    0.89 |    -8.29 |       -11.17 |
| MX / N         | WEAK     |   99.11 |     2.00 |        -2.00 |
| M10 / Y        | NEG      |    0.75 |    -8.42 |       -11.17 |
| M10 / N        | WEAK     |   99.25 |     2.14 |        -1.86 |

## Will the Republican Party candidate win the 2026 Kansas Senate election by 25%-30%?
Contract 3343541; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          11 |        11.39 | +88.61 / −11.39  | 7.78×         |
| No     |          95 |        95.19 | +4.81 / −95.19   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.05 |   -11.34 |       -13.39 |
| GB / N         | GO       |   99.95 |     4.76 |         0.76 |
| ST / Y         | NEG      |    0.02 |   -11.37 |       -13.39 |
| ST / N         | GO       |   99.98 |     4.79 |         0.79 |
| MX / Y         | NEG      |    0.07 |   -11.33 |       -13.39 |
| MX / N         | GO       |   99.93 |     4.74 |         0.74 |
| M10 / Y        | NEG      |    0.05 |   -11.34 |       -13.39 |
| M10 / N        | GO       |   99.95 |     4.76 |         0.76 |

## Will the Republican Party candidate win the 2026 Kansas Senate election by 30% or more?
Contract 3343540; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        3.63 |         3.77 | +96.23 / −3.77   | 25.55×        |
| No     |       99.35 |        99.37 | +0.63 / −99.37   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.00 |    -3.76 |        -5.77 |
| GB / N         | WEAK     |  100.00 |     0.62 |        -3.38 |
| ST / Y         | NEG      |    0.00 |    -3.76 |        -5.77 |
| ST / N         | WEAK     |  100.00 |     0.62 |        -3.38 |
| MX / Y         | NEG      |    0.00 |    -3.76 |        -5.77 |
| MX / N         | WEAK     |  100.00 |     0.62 |        -3.38 |
| M10 / Y        | NEG      |    0.00 |    -3.76 |        -5.77 |
| M10 / N        | WEAK     |  100.00 |     0.62 |        -3.38 |

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 10%-15%?
Contract 3343564; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          22 |        22.69 | +77.31 / −22.69  | 3.41×         |
| No     |          82 |        82.59 | +17.41 / −82.59  | 0.21×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   31.41 |     8.73 |         4.73 |
| GB / N         | NEG      |   68.59 |   -14.00 |       -18.00 |
| ST / Y         | GO       |   37.26 |    14.57 |        10.57 |
| ST / N         | NEG      |   62.74 |   -19.85 |       -23.85 |
| MX / Y         | GO       |   31.05 |     8.36 |         4.36 |
| MX / N         | NEG      |   68.95 |   -13.64 |       -17.64 |
| M10 / Y        | GO       |   30.91 |     8.23 |         4.23 |
| M10 / N        | NEG      |   69.09 |   -13.50 |       -17.50 |

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 15%-20%?
Contract 3343563; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          80 |        80.64 | +19.36 / −80.64  | 0.24×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   23.98 |     2.32 |        -1.68 |
| GB / N         | NEG      |   76.02 |    -4.62 |        -8.62 |
| ST / Y         | WEAK     |   24.88 |     3.22 |        -0.78 |
| ST / N         | NEG      |   75.12 |    -5.52 |        -9.52 |
| MX / Y         | NEG      |   20.99 |    -0.67 |        -4.67 |
| MX / N         | NEG      |   79.01 |    -1.63 |        -5.63 |
| M10 / Y        | WEAK     |   23.80 |     2.14 |        -1.86 |
| M10 / N        | NEG      |   76.20 |    -4.44 |        -8.44 |

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 20%-25%?
Contract 3343562; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          83 |        83.56 | +16.44 / −83.56  | 0.20×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    9.83 |   -11.83 |       -15.83 |
| GB / N         | GO       |   90.17 |     6.60 |         2.60 |
| ST / Y         | NEG      |    7.13 |   -14.53 |       -18.53 |
| ST / N         | GO       |   92.87 |     9.30 |         5.30 |
| MX / Y         | NEG      |    7.77 |   -13.90 |       -17.90 |
| MX / N         | GO       |   92.23 |     8.67 |         4.67 |
| M10 / Y        | NEG      |    9.63 |   -12.03 |       -16.03 |
| M10 / N        | GO       |   90.37 |     6.80 |         2.80 |

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 25%-30%?
Contract 3343561; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        12.2 |        12.63 | +87.37 / −12.63  | 6.92×         |
| No     |        91   |        91.33 | +8.67 / −91.33   | 0.09×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    2.16 |   -10.47 |       -14.47 |
| GB / N         | GO       |   97.84 |     6.51 |         2.51 |
| ST / Y         | NEG      |    1.08 |   -11.54 |       -14.63 |
| ST / N         | GO       |   98.92 |     7.59 |         3.59 |
| MX / Y         | NEG      |    1.81 |   -10.82 |       -14.63 |
| MX / N         | GO       |   98.19 |     6.86 |         2.86 |
| M10 / Y        | NEG      |    2.47 |   -10.16 |       -14.16 |
| M10 / N        | GO       |   97.53 |     6.20 |         2.20 |

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 30%-35%?
Contract 3343560; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       14.74 |        15.23 | +84.77 / −15.23  | 5.57×         |
| No     |       93.3  |        93.55 | +6.45 / −93.55   | 0.07×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.25 |   -14.98 |       -17.23 |
| GB / N         | GO       |   99.75 |     6.20 |         2.20 |
| ST / Y         | NEG      |    0.11 |   -15.12 |       -17.23 |
| ST / N         | GO       |   99.89 |     6.34 |         2.34 |
| MX / Y         | NEG      |    0.28 |   -14.95 |       -17.23 |
| MX / N         | GO       |   99.72 |     6.17 |         2.17 |
| M10 / Y        | NEG      |    0.40 |   -14.84 |       -17.23 |
| M10 / N        | GO       |   99.60 |     6.05 |         2.05 |

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 35%-40%?
Contract 3343559; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         7.6 |         7.88 | +92.12 / −7.88   | 11.69×        |
| No     |        93.8 |        94.03 | +5.97 / −94.03   | 0.06×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.02 |    -7.87 |        -9.88 |
| GB / N         | GO       |   99.98 |     5.95 |         1.95 |
| ST / Y         | NEG      |    0.01 |    -7.87 |        -9.88 |
| ST / N         | GO       |   99.99 |     5.95 |         1.95 |
| MX / Y         | NEG      |    0.03 |    -7.85 |        -9.88 |
| MX / N         | GO       |   99.97 |     5.94 |         1.94 |
| M10 / Y        | NEG      |    0.05 |    -7.83 |        -9.88 |
| M10 / N        | GO       |   99.95 |     5.91 |         1.91 |

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 40%-45%?
Contract 3343558; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10.39 |        10.76 | +89.24 / −10.76  | 8.29×         |
| No     |       93    |        93.26 | +6.74 / −93.26   | 0.07×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.00 |   -10.76 |       -12.76 |
| GB / N         | GO       |  100.00 |     6.74 |         2.74 |
| ST / Y         | NEG      |    0.01 |   -10.76 |       -12.76 |
| ST / N         | GO       |   99.99 |     6.73 |         2.73 |
| MX / Y         | NEG      |    0.00 |   -10.76 |       -12.76 |
| MX / N         | GO       |  100.00 |     6.74 |         2.74 |
| M10 / Y        | NEG      |    0.00 |   -10.76 |       -12.76 |
| M10 / N        | GO       |  100.00 |     6.74 |         2.74 |

## Will the Republican Party candidate win the 2026 Louisiana Senate election by 15%-20%?
Contract 3343574; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       27.19 |        27.98 | +72.02 / −27.98  | 2.57×         |
| No     |       81.8  |        82.39 | +17.61 / −82.39  | 0.21×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   15.11 |   -12.88 |       -16.88 |
| GB / N         | WEAK     |   84.89 |     2.50 |        -1.50 |
| ST / Y         | NEG      |   13.58 |   -14.41 |       -18.41 |
| ST / N         | GO       |   86.42 |     4.03 |         0.03 |
| MX / Y         | NEG      |   11.59 |   -16.40 |       -20.40 |
| MX / N         | GO       |   88.41 |     6.02 |         2.02 |
| M10 / Y        | NEG      |   11.35 |   -16.64 |       -20.64 |
| M10 / N        | GO       |   88.65 |     6.26 |         2.26 |

## Will the Republican Party candidate win the 2026 Louisiana Senate election by 20%-25%?
Contract 3343573; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          13 |        13.45 | +86.55 / −13.45  | 6.43×         |
| No     |          90 |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    4.06 |    -9.39 |       -13.39 |
| GB / N         | GO       |   95.94 |     5.58 |         1.58 |
| ST / Y         | NEG      |    2.27 |   -11.18 |       -15.18 |
| ST / N         | GO       |   97.72 |     7.36 |         3.36 |
| MX / Y         | NEG      |    2.84 |   -10.61 |       -14.61 |
| MX / N         | GO       |   97.16 |     6.80 |         2.80 |
| M10 / Y        | NEG      |    2.76 |   -10.69 |       -14.69 |
| M10 / N        | GO       |   97.24 |     6.88 |         2.88 |

## Will the Republican Party candidate win the 2026 Louisiana Senate election by 30%-35%?
Contract 3343571; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       14.86 |        15.34 | +84.66 / −15.34  | 5.52×         |
| No     |       96.47 |        96.61 | +3.39 / −96.61   | 0.04×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.04 |   -15.30 |       -17.34 |
| GB / N         | WEAK     |   99.96 |     3.35 |        -0.65 |
| ST / Y         | NEG      |    0.01 |   -15.33 |       -17.34 |
| ST / N         | WEAK     |   99.99 |     3.38 |        -0.62 |
| MX / Y         | NEG      |    0.05 |   -15.29 |       -17.34 |
| MX / N         | WEAK     |   99.95 |     3.34 |        -0.66 |
| M10 / Y        | NEG      |    0.05 |   -15.29 |       -17.34 |
| M10 / N        | WEAK     |   99.95 |     3.34 |        -0.66 |

## Will the Republican Party candidate win the 2026 Michigan Senate election by 12% or more?
Contract 3343882; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        11.8 |        12.21 | +87.79 / −12.21  | 7.19×         |
| No     |        99.7 |        99.71 | +0.29 / −99.71   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.14 |   -12.07 |       -14.21 |
| GB / N         | WEAK     |   99.86 |     0.15 |        -3.85 |
| ST / Y         | NEG      |    0.09 |   -12.12 |       -14.21 |
| ST / N         | WEAK     |   99.91 |     0.19 |        -3.81 |
| MX / Y         | NEG      |    0.29 |   -11.92 |       -14.21 |
| MX / N         | WEAK     |   99.71 |     0.00 |        -4.00 |
| M10 / Y        | NEG      |    0.39 |   -11.82 |       -14.21 |
| M10 / N        | NEG      |   99.61 |    -0.11 |        -4.11 |

## Will the Republican Party candidate win the 2026 Michigan Senate election by 6%-9%?
Contract 3343884; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       17.98 |        18.54 | +81.46 / −18.54  | 4.39×         |
| No     |       95.06 |        95.24 | +4.76 / −95.24   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.73 |   -16.82 |       -20.54 |
| GB / N         | WEAK     |   98.27 |     3.03 |        -0.97 |
| ST / Y         | NEG      |    0.97 |   -17.57 |       -20.54 |
| ST / N         | WEAK     |   99.02 |     3.78 |        -0.22 |
| MX / Y         | NEG      |    1.89 |   -16.66 |       -20.54 |
| MX / N         | WEAK     |   98.11 |     2.87 |        -1.13 |
| M10 / Y        | NEG      |    2.50 |   -16.05 |       -20.05 |
| M10 / N        | WEAK     |   97.50 |     2.26 |        -1.74 |

## Will the Republican Party candidate win the 2026 Michigan Senate election by 9%-12%?
Contract 3343883; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       19.45 |        20.04 | +79.96 / −20.04  | 3.99×         |
| No     |       97.95 |        98.03 | +1.97 / −98.03   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.50 |   -19.54 |       -22.04 |
| GB / N         | WEAK     |   99.50 |     1.46 |        -2.54 |
| ST / Y         | NEG      |    0.24 |   -19.80 |       -22.04 |
| ST / N         | WEAK     |   99.76 |     1.72 |        -2.28 |
| MX / Y         | NEG      |    0.65 |   -19.40 |       -22.04 |
| MX / N         | WEAK     |   99.36 |     1.32 |        -2.68 |
| M10 / Y        | NEG      |    0.92 |   -19.13 |       -22.04 |
| M10 / N        | WEAK     |   99.08 |     1.05 |        -2.95 |

## Will the Republican Party candidate win the 2026 New Hampshire Senate election by 0%-3%?
Contract 3343937; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       12.6  |        13.04 | +86.96 / −13.04  | 6.67×         |
| No     |       93.86 |        94.09 | +5.91 / −94.09   | 0.06×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.57 |   -11.47 |       -15.04 |
| GB / N         | GO       |   98.43 |     4.34 |         0.34 |
| ST / Y         | NEG      |    1.72 |   -11.32 |       -15.04 |
| ST / N         | GO       |   98.28 |     4.19 |         0.19 |
| MX / Y         | NEG      |    4.40 |    -8.64 |       -12.64 |
| MX / N         | WEAK     |   95.60 |     1.51 |        -2.49 |
| M10 / Y        | NEG      |    3.79 |    -9.25 |       -13.25 |
| M10 / N        | WEAK     |   96.21 |     2.12 |        -1.88 |

## Will the Republican Party candidate win the 2026 New Hampshire Senate election by 3%-6%?
Contract 3343936; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       29.83 |        30.59 | +69.41 / −30.59  | 2.27×         |
| No     |       99.3  |        99.33 | +0.67 / −99.33   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.41 |   -30.18 |       -32.59 |
| GB / N         | WEAK     |   99.59 |     0.26 |        -3.74 |
| ST / Y         | NEG      |    0.53 |   -30.06 |       -32.59 |
| ST / N         | WEAK     |   99.47 |     0.14 |        -3.86 |
| MX / Y         | NEG      |    1.86 |   -28.72 |       -32.59 |
| MX / N         | NEG      |   98.14 |    -1.19 |        -5.19 |
| M10 / Y        | NEG      |    1.57 |   -29.02 |       -32.59 |
| M10 / N        | NEG      |   98.43 |    -0.90 |        -4.90 |

## Will the Republican Party candidate win the 2026 New Hampshire Senate election by 6% or more?
Contract 3343935; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       20.65 |        21.16 | +78.84 / −21.16  | 3.72×         |
| No     |       99.9  |        99.9  | +0.10 / −99.90   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.10 |   -21.07 |       -23.16 |
| GB / N         | WEAK     |   99.90 |     0.00 |        -4.00 |
| ST / Y         | NEG      |    0.18 |   -20.99 |       -23.16 |
| ST / N         | NEG      |   99.83 |    -0.08 |        -4.08 |
| MX / Y         | NEG      |    0.97 |   -20.20 |       -23.16 |
| MX / N         | NEG      |   99.03 |    -0.87 |        -4.87 |
| M10 / Y        | NEG      |    0.77 |   -20.40 |       -23.16 |
| M10 / N        | NEG      |   99.23 |    -0.67 |        -4.67 |

## Will the Republican Party candidate win the 2026 New Mexico Senate election by 3% or more?
Contract 3343965; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        6.96 |         7.22 | +92.78 / −7.22   | 12.85×        |
| No     |       99.4  |        99.42 | +0.58 / −99.42   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.68 |    -6.54 |        -9.22 |
| GB / N         | NEG      |   99.32 |    -0.10 |        -4.10 |
| ST / Y         | NEG      |    0.30 |    -6.92 |        -9.22 |
| ST / N         | WEAK     |   99.70 |     0.27 |        -3.73 |
| MX / Y         | NEG      |    0.67 |    -6.55 |        -9.22 |
| MX / N         | NEG      |   99.33 |    -0.09 |        -4.09 |
| M10 / Y        | NEG      |    0.68 |    -6.54 |        -9.22 |
| M10 / N        | NEG      |   99.32 |    -0.10 |        -4.10 |

## Will the Republican Party candidate win the 2026 North Carolina Senate election by 0%-3%?
Contract 3344032; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        7.85 |         8.13 | +91.87 / −8.13   | 11.30×        |
| No     |       96    |        96.15 | +3.85 / −96.15   | 0.04×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    9.43 |     1.30 |        -2.70 |
| GB / N         | NEG      |   90.57 |    -5.58 |        -9.58 |
| ST / Y         | NEG      |    7.11 |    -1.02 |        -5.02 |
| ST / N         | NEG      |   92.89 |    -3.26 |        -7.26 |
| MX / Y         | WEAK     |    8.65 |     0.52 |        -3.48 |
| MX / N         | NEG      |   91.35 |    -4.80 |        -8.80 |
| M10 / Y        | WEAK     |    8.70 |     0.57 |        -3.43 |
| M10 / N        | NEG      |   91.30 |    -4.85 |        -8.85 |

## Will the Republican Party candidate win the 2026 Ohio Senate election by 0%-3%?
Contract 3344046; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          19 |        19.62 | +80.38 / −19.62  | 4.10×         |
| No     |          83 |        83.56 | +16.44 / −83.56  | 0.20×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   15.29 |    -4.33 |        -8.33 |
| GB / N         | WEAK     |   84.71 |     1.15 |        -2.85 |
| ST / Y         | NEG      |   15.56 |    -4.06 |        -8.06 |
| ST / N         | WEAK     |   84.44 |     0.88 |        -3.12 |
| MX / Y         | NEG      |   16.38 |    -3.23 |        -7.23 |
| MX / N         | WEAK     |   83.62 |     0.05 |        -3.95 |
| M10 / Y        | NEG      |   17.88 |    -1.74 |        -5.74 |
| M10 / N        | NEG      |   82.12 |    -1.44 |        -5.44 |

## Will the Republican Party candidate win the 2026 Ohio Senate election by 12% or more?
Contract 3344042; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        7.47 |         7.73 | +92.27 / −7.73   | 11.94×        |
| No     |       99.8  |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.40 |    -7.33 |        -9.73 |
| GB / N         | NEG      |   99.60 |    -0.21 |        -4.21 |
| ST / Y         | NEG      |    0.17 |    -7.56 |        -9.73 |
| ST / N         | WEAK     |   99.83 |     0.02 |        -3.98 |
| MX / Y         | NEG      |    0.53 |    -7.20 |        -9.73 |
| MX / N         | NEG      |   99.47 |    -0.33 |        -4.33 |
| M10 / Y        | NEG      |    0.68 |    -7.05 |        -9.73 |
| M10 / N        | NEG      |   99.32 |    -0.49 |        -4.49 |

## Will the Republican Party candidate win the 2026 Ohio Senate election by 3%-6%?
Contract 3344045; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10.35 |        10.72 | +89.28 / −10.72  | 8.33×         |
| No     |       91.4  |        91.71 | +8.29 / −91.71   | 0.09×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    8.82 |    -1.90 |        -5.90 |
| GB / N         | NEG      |   91.18 |    -0.53 |        -4.53 |
| ST / Y         | NEG      |    6.52 |    -4.21 |        -8.21 |
| ST / N         | WEAK     |   93.48 |     1.77 |        -2.23 |
| MX / Y         | NEG      |    8.73 |    -1.99 |        -5.99 |
| MX / N         | NEG      |   91.27 |    -0.44 |        -4.44 |
| M10 / Y        | NEG      |   10.08 |    -0.64 |        -4.64 |
| M10 / N        | NEG      |   89.92 |    -1.79 |        -5.79 |

## Will the Republican Party candidate win the 2026 Ohio Senate election by 6%-9%?
Contract 3344044; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.49 |         9.82 | +90.18 / −9.82   | 9.18×         |
| No     |       97.2  |        97.31 | +2.69 / −97.31   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    3.87 |    -5.95 |        -9.95 |
| GB / N         | NEG      |   96.13 |    -1.17 |        -5.17 |
| ST / Y         | NEG      |    2.07 |    -7.75 |       -11.75 |
| ST / N         | WEAK     |   97.93 |     0.63 |        -3.37 |
| MX / Y         | NEG      |    3.77 |    -6.05 |       -10.05 |
| MX / N         | NEG      |   96.23 |    -1.08 |        -5.08 |
| M10 / Y        | NEG      |    4.57 |    -5.25 |        -9.25 |
| M10 / N        | NEG      |   95.43 |    -1.88 |        -5.88 |

## Will the Republican Party candidate win the 2026 Oklahoma Senate election by 15%-20%?
Contract 3344070; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       22.26 |        22.95 | +77.05 / −22.95  | 3.36×         |
| No     |       87    |        87.45 | +12.55 / −87.45  | 0.14×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   13.24 |    -9.71 |       -13.71 |
| GB / N         | NEG      |   86.76 |    -0.69 |        -4.69 |
| ST / Y         | NEG      |   11.28 |   -11.67 |       -15.67 |
| ST / N         | WEAK     |   88.72 |     1.27 |        -2.73 |
| MX / Y         | NEG      |   13.55 |    -9.40 |       -13.40 |
| MX / N         | NEG      |   86.45 |    -1.00 |        -5.00 |
| M10 / Y        | NEG      |   11.99 |   -10.96 |       -14.96 |
| M10 / N        | WEAK     |   88.01 |     0.56 |        -3.44 |

## Will the Republican Party candidate win the 2026 Oklahoma Senate election by 30%-35%?
Contract 3344067; 100 shares per position.

| Side   | Entry (¢)   | Budget ($)   | Win / lose ($)   | Reward/loss   |
|:-------|:------------|:-------------|:-----------------|:--------------|
| Yes    | 15.00       | 15.51        | +84.49 / −15.51  | 5.45×         |
| No     | —           | —            | Unavailable      | —             |

| Model / side   | Status   |   P (%) | EV ($)   | Stress ($)          |
|:---------------|:---------|--------:|:---------|:--------------------|
| GB / Y         | WEAK     |   18.84 | 3.33     | -0.6663586198582621 |
| GB / N         | N/A      |   81.16 | —        | —                   |
| ST / Y         | WEAK     |   18.41 | 2.90     | -1.1037499999999978 |
| ST / N         | N/A      |   81.59 | —        | —                   |
| MX / Y         | WEAK     |   17.85 | 2.34     | -1.660677083333331  |
| MX / N         | N/A      |   82.15 | —        | —                   |
| M10 / Y        | GO       |   19.57 | 4.06     | 0.05510416666666962 |
| M10 / N        | N/A      |   80.43 | —        | —                   |

## Will the Republican Party candidate win the 2026 Oklahoma Senate election by 35%-40%?
Contract 3344066; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10    |        10.36 | +89.64 / −10.36  | 8.65×         |
| No     |       93.93 |        94.16 | +5.84 / −94.16   | 0.06×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    7.34 |    -3.02 |        -7.02 |
| GB / N         | NEG      |   92.66 |    -1.50 |        -5.50 |
| ST / Y         | NEG      |    4.98 |    -5.38 |        -9.38 |
| ST / N         | WEAK     |   95.03 |     0.87 |        -3.13 |
| MX / Y         | NEG      |    7.23 |    -3.13 |        -7.13 |
| MX / N         | NEG      |   92.77 |    -1.39 |        -5.39 |
| M10 / Y        | NEG      |    8.31 |    -2.05 |        -6.05 |
| M10 / N        | NEG      |   91.69 |    -2.46 |        -6.46 |

## Will the Republican Party candidate win the 2026 Oklahoma Senate election by 40%-45%?
Contract 3344065; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       14.42 |        14.91 | +85.09 / −14.91  | 5.71×         |
| No     |       97.66 |        97.75 | +2.25 / −97.75   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.68 |   -13.23 |       -16.91 |
| GB / N         | WEAK     |   98.32 |     0.57 |        -3.43 |
| ST / Y         | NEG      |    0.81 |   -14.10 |       -16.91 |
| ST / N         | WEAK     |   99.19 |     1.44 |        -2.56 |
| MX / Y         | NEG      |    2.08 |   -12.83 |       -16.83 |
| MX / N         | WEAK     |   97.92 |     0.17 |        -3.83 |
| M10 / Y        | NEG      |    2.54 |   -12.37 |       -16.37 |
| M10 / N        | NEG      |   97.46 |    -0.29 |        -4.29 |

## Will the Republican Party candidate win the 2026 Oklahoma Senate election by 45% or more?
Contract 3344064; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10.91 |        11.29 | +88.71 / −11.29  | 7.86×         |
| No     |       99.5  |        99.52 | +0.48 / −99.52   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.24 |   -11.04 |       -13.29 |
| GB / N         | WEAK     |   99.76 |     0.24 |        -3.76 |
| ST / Y         | NEG      |    0.16 |   -11.13 |       -13.29 |
| ST / N         | WEAK     |   99.84 |     0.32 |        -3.68 |
| MX / Y         | NEG      |    0.55 |   -10.73 |       -13.29 |
| MX / N         | NEG      |   99.45 |    -0.07 |        -4.07 |
| M10 / Y        | NEG      |    0.70 |   -10.59 |       -13.29 |
| M10 / N        | NEG      |   99.30 |    -0.22 |        -4.22 |

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 0%-5%?
Contract 3344126; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          29 |        29.82 | +70.18 / −29.82  | 2.35×         |
| No     |          74 |        74.77 | +25.23 / −74.77  | 0.34×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   15.48 |   -14.35 |       -18.35 |
| GB / N         | GO       |   84.52 |     9.75 |         5.75 |
| ST / Y         | NEG      |   13.98 |   -15.84 |       -19.84 |
| ST / N         | GO       |   86.02 |    11.25 |         7.25 |
| MX / Y         | NEG      |   18.14 |   -11.68 |       -15.68 |
| MX / N         | GO       |   81.86 |     7.09 |         3.09 |
| M10 / Y        | NEG      |   16.88 |   -12.94 |       -16.94 |
| M10 / N        | GO       |   83.12 |     8.35 |         4.35 |

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 10%-15%?
Contract 3344124; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          16 |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |          85 |        85.51 | +14.49 / −85.51  | 0.17×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   29.89 |    13.35 |         9.35 |
| GB / N         | NEG      |   70.11 |   -15.40 |       -19.40 |
| ST / Y         | GO       |   34.44 |    17.90 |        13.90 |
| ST / N         | NEG      |   65.56 |   -19.95 |       -23.95 |
| MX / Y         | GO       |   27.45 |    10.92 |         6.92 |
| MX / N         | NEG      |   72.55 |   -12.96 |       -16.96 |
| M10 / Y        | GO       |   28.49 |    11.95 |         7.95 |
| M10 / N        | NEG      |   71.51 |   -14.00 |       -18.00 |

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 15%-20%?
Contract 3344123; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       11.24 |        11.64 | +88.36 / −11.64  | 7.59×         |
| No     |       92    |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   15.33 |     3.69 |        -0.31 |
| GB / N         | NEG      |   84.67 |    -7.62 |       -11.62 |
| ST / Y         | WEAK     |   13.14 |     1.50 |        -2.50 |
| ST / N         | NEG      |   86.86 |    -5.44 |        -9.44 |
| MX / Y         | WEAK     |   12.02 |     0.38 |        -3.62 |
| MX / N         | NEG      |   87.98 |    -4.31 |        -8.31 |
| M10 / Y        | WEAK     |   13.25 |     1.61 |        -2.39 |
| M10 / N        | NEG      |   86.75 |    -5.55 |        -9.55 |

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 20%-25%?
Contract 3344122; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        6.22 |         6.45 | +93.55 / −6.45   | 14.50×        |
| No     |       97.46 |        97.56 | +2.44 / −97.56   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    4.04 |    -2.42 |        -6.42 |
| GB / N         | NEG      |   95.96 |    -1.60 |        -5.60 |
| ST / Y         | NEG      |    2.08 |    -4.37 |        -8.37 |
| ST / N         | WEAK     |   97.92 |     0.36 |        -3.64 |
| MX / Y         | NEG      |    2.92 |    -3.53 |        -7.53 |
| MX / N         | NEG      |   97.08 |    -0.48 |        -4.48 |
| M10 / Y        | NEG      |    3.35 |    -3.10 |        -7.10 |
| M10 / N        | NEG      |   96.65 |    -0.91 |        -4.91 |

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 30% or more?
Contract 3344120; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        7.25 |         7.51 | +92.49 / −7.51   | 12.31×        |
| No     |       99.5  |        99.52 | +0.48 / −99.52   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.04 |    -7.48 |        -9.51 |
| GB / N         | WEAK     |   99.96 |     0.44 |        -3.56 |
| ST / Y         | NEG      |    0.02 |    -7.50 |        -9.51 |
| ST / N         | WEAK     |   99.98 |     0.46 |        -3.54 |
| MX / Y         | NEG      |    0.06 |    -7.46 |        -9.51 |
| MX / N         | WEAK     |   99.94 |     0.42 |        -3.58 |
| M10 / Y        | NEG      |    0.08 |    -7.44 |        -9.51 |
| M10 / N        | WEAK     |   99.92 |     0.40 |        -3.60 |

## Will the Republican Party candidate win the 2026 Tennessee Senate election by 10%-15%?
Contract 3344155; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        17.4 |        17.97 | +82.03 / −17.97  | 4.56×         |
| No     |        85   |        85.51 | +14.49 / −85.51  | 0.17×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    9.71 |    -8.26 |       -12.26 |
| GB / N         | GO       |   90.29 |     4.78 |         0.78 |
| ST / Y         | NEG      |    7.53 |   -10.45 |       -14.45 |
| ST / N         | GO       |   92.47 |     6.96 |         2.96 |
| MX / Y         | NEG      |    8.99 |    -8.99 |       -12.99 |
| MX / N         | GO       |   91.01 |     5.50 |         1.50 |
| M10 / Y        | NEG      |    6.53 |   -11.45 |       -15.45 |
| M10 / N        | GO       |   93.47 |     7.96 |         3.96 |

## Will the Republican Party candidate win the 2026 Tennessee Senate election by 15%-20%?
Contract 3344154; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       15.63 |        16.16 | +83.84 / −16.16  | 5.19×         |
| No     |       86    |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   22.61 |     6.45 |         2.45 |
| GB / N         | NEG      |   77.39 |    -9.09 |       -13.09 |
| ST / Y         | GO       |   24.98 |     8.82 |         4.82 |
| ST / N         | NEG      |   75.02 |   -11.46 |       -15.46 |
| MX / Y         | GO       |   22.08 |     5.92 |         1.92 |
| MX / N         | NEG      |   77.92 |    -8.56 |       -12.56 |
| M10 / Y        | WEAK     |   18.37 |     2.21 |        -1.79 |
| M10 / N        | NEG      |   81.63 |    -4.85 |        -8.85 |

## Will the Republican Party candidate win the 2026 Tennessee Senate election by 25%-30%?
Contract 3344152; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       18.27 |        18.87 | +81.13 / −18.87  | 4.30×         |
| No     |       86.82 |        87.27 | +12.73 / −87.27  | 0.15×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   22.59 |     3.72 |        -0.28 |
| GB / N         | NEG      |   77.41 |    -9.86 |       -13.86 |
| ST / Y         | WEAK     |   21.72 |     2.85 |        -1.15 |
| ST / N         | NEG      |   78.28 |    -8.99 |       -12.99 |
| MX / Y         | WEAK     |   22.44 |     3.57 |        -0.43 |
| MX / N         | NEG      |   77.56 |    -9.71 |       -13.71 |
| M10 / Y        | GO       |   25.69 |     6.82 |         2.82 |
| M10 / N        | NEG      |   74.31 |   -12.96 |       -16.96 |

## Will the Republican Party candidate win the 2026 Tennessee Senate election by 30%-35%?
Contract 3344151; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        12.3 |        12.73 | +87.27 / −12.73  | 6.86×         |
| No     |        93   |        93.26 | +6.74 / −93.26   | 0.07×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    9.69 |    -3.04 |        -7.04 |
| GB / N         | NEG      |   90.31 |    -2.95 |        -6.95 |
| ST / Y         | NEG      |    7.12 |    -5.61 |        -9.61 |
| ST / N         | NEG      |   92.88 |    -0.38 |        -4.38 |
| MX / Y         | NEG      |   10.01 |    -2.72 |        -6.72 |
| MX / N         | NEG      |   89.99 |    -3.28 |        -7.28 |
| M10 / Y        | WEAK     |   12.95 |     0.22 |        -3.78 |
| M10 / N        | NEG      |   87.05 |    -6.21 |       -10.21 |

## Will the Republican Party candidate win the 2026 Tennessee Senate election by 45% or more?
Contract 3344148; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        6.03 |         6.25 | +93.75 / −6.25   | 15.00×        |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.03 |    -6.22 |        -8.25 |
| GB / N         | WEAK     |   99.97 |     0.36 |        -3.64 |
| ST / Y         | NEG      |    0.03 |    -6.22 |        -8.25 |
| ST / N         | WEAK     |   99.97 |     0.35 |        -3.65 |
| MX / Y         | NEG      |    0.11 |    -6.14 |        -8.25 |
| MX / N         | WEAK     |   99.89 |     0.27 |        -3.73 |
| M10 / Y        | NEG      |    0.21 |    -6.04 |        -8.25 |
| M10 / N        | WEAK     |   99.79 |     0.17 |        -3.83 |

## Will the Republican Party candidate win the 2026 Texas Senate election by 0%-3%?
Contract 3344140; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          83 |        83.56 | +16.44 / −83.56  | 0.20×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   21.67 |     0.00 |        -4.00 |
| GB / N         | NEG      |   78.33 |    -5.23 |        -9.23 |
| ST / Y         | WEAK     |   25.15 |     3.49 |        -0.51 |
| ST / N         | NEG      |   74.85 |    -8.72 |       -12.72 |
| MX / Y         | WEAK     |   23.65 |     1.98 |        -2.02 |
| MX / N         | NEG      |   76.35 |    -7.21 |       -11.21 |
| M10 / Y        | WEAK     |   23.52 |     1.86 |        -2.14 |
| M10 / N        | NEG      |   76.48 |    -7.09 |       -11.09 |

## Will the Republican Party candidate win the 2026 Texas Senate election by 12% or more?
Contract 3344136; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        3.86 |         4.01 | +95.99 / −4.01   | 23.97×        |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.42 |    -3.58 |        -6.01 |
| GB / N         | NEG      |   99.58 |    -0.04 |        -4.04 |
| ST / Y         | NEG      |    0.17 |    -3.83 |        -6.01 |
| ST / N         | WEAK     |   99.83 |     0.21 |        -3.79 |
| MX / Y         | NEG      |    0.46 |    -3.55 |        -6.01 |
| MX / N         | NEG      |   99.54 |    -0.07 |        -4.07 |
| M10 / Y        | NEG      |    0.45 |    -3.56 |        -6.01 |
| M10 / N        | NEG      |   99.55 |    -0.07 |        -4.07 |

## Will the Republican Party candidate win the 2026 Texas Senate election by 3%-6%?
Contract 3344139; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        11.5 |        11.91 | +88.09 / −11.91  | 7.40×         |
| No     |        89.2 |        89.59 | +10.41 / −89.59  | 0.12×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   13.56 |     1.65 |        -2.35 |
| GB / N         | NEG      |   86.44 |    -3.14 |        -7.14 |
| ST / Y         | WEAK     |   12.10 |     0.20 |        -3.80 |
| ST / N         | NEG      |   87.90 |    -1.69 |        -5.69 |
| MX / Y         | WEAK     |   13.83 |     1.92 |        -2.08 |
| MX / N         | NEG      |   86.17 |    -3.41 |        -7.41 |
| M10 / Y        | WEAK     |   13.69 |     1.78 |        -2.22 |
| M10 / N        | NEG      |   86.31 |    -3.28 |        -7.28 |

## Will the Republican Party candidate win the 2026 Texas Senate election by 6%-9%?
Contract 3344138; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        5.44 |         5.65 | +94.35 / −5.65   | 16.71×        |
| No     |       95.5  |        95.67 | +4.33 / −95.67   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    5.87 |     0.23 |        -3.77 |
| GB / N         | NEG      |   94.13 |    -1.54 |        -5.54 |
| ST / Y         | NEG      |    3.89 |    -1.76 |        -5.76 |
| ST / N         | WEAK     |   96.11 |     0.44 |        -3.56 |
| MX / Y         | NEG      |    5.55 |    -0.10 |        -4.10 |
| MX / N         | NEG      |   94.45 |    -1.22 |        -5.22 |
| M10 / Y        | NEG      |    5.47 |    -0.17 |        -4.17 |
| M10 / N        | NEG      |   94.53 |    -1.14 |        -5.14 |

## Will the Republican Party candidate win the 2026 Texas Senate election by 9%-12%?
Contract 3344137; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        8.01 |         8.3  | +91.70 / −8.30   | 11.05×        |
| No     |       98.3  |        98.37 | +1.63 / −98.37   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.76 |    -6.54 |       -10.30 |
| GB / N         | NEG      |   98.24 |    -0.13 |        -4.13 |
| ST / Y         | NEG      |    0.80 |    -7.50 |       -10.30 |
| ST / N         | WEAK     |   99.20 |     0.84 |        -3.16 |
| MX / Y         | NEG      |    1.61 |    -6.69 |       -10.30 |
| MX / N         | WEAK     |   98.39 |     0.03 |        -3.97 |
| M10 / Y        | NEG      |    1.57 |    -6.72 |       -10.30 |
| M10 / N        | WEAK     |   98.43 |     0.06 |        -3.94 |

## Will the Republican Party candidate win the 2026 Virginia Senate election by 0%-3%?
Contract 3344161; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        1.52 |         1.58 | +98.42 / −1.58   | 62.15×        |
| No     |       99.61 |        99.63 | +0.37 / −99.63   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.41 |    -1.17 |        -3.58 |
| GB / N         | NEG      |   99.59 |    -0.04 |        -4.04 |
| ST / Y         | NEG      |    0.33 |    -1.26 |        -3.58 |
| ST / N         | WEAK     |   99.67 |     0.05 |        -3.95 |
| MX / Y         | NEG      |    0.82 |    -0.76 |        -3.58 |
| MX / N         | NEG      |   99.18 |    -0.45 |        -4.45 |
| M10 / Y        | NEG      |    0.80 |    -0.78 |        -3.58 |
| M10 / N        | NEG      |   99.20 |    -0.43 |        -4.43 |

## Will the Republican Party candidate win the 2026 Virginia Senate election by 3% or more?
Contract 3344160; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         0.7 |         0.73 | +99.27 / −0.73   | 136.40×       |
| No     |        99.8 |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.15 |    -0.57 |        -2.73 |
| GB / N         | WEAK     |   99.85 |     0.04 |        -3.96 |
| ST / Y         | NEG      |    0.26 |    -0.47 |        -2.73 |
| ST / N         | NEG      |   99.74 |    -0.07 |        -4.07 |
| MX / Y         | NEG      |    0.69 |    -0.03 |        -2.73 |
| MX / N         | NEG      |   99.31 |    -0.50 |        -4.50 |
| M10 / Y        | NEG      |    0.68 |    -0.05 |        -2.73 |
| M10 / N        | NEG      |   99.32 |    -0.49 |        -4.49 |

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

## Will the Republican Party hold 47 or fewer Senate seats after the 2026 midterm elections?
Contract 943819; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          37 |        37.93 | +62.07 / −37.93  | 1.64×         |
| No     |          64 |        64.92 | +35.08 / −64.92  | 0.54×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   14.50 |   -23.43 |       -27.43 |
| GB / N         | GO       |   85.50 |    20.58 |        16.58 |
| ST / Y         | NEG      |   14.57 |   -23.36 |       -27.36 |
| ST / N         | GO       |   85.43 |    20.51 |        16.51 |
| MX / Y         | NEG      |   25.03 |   -12.90 |       -16.90 |
| MX / N         | GO       |   74.97 |    10.04 |         6.04 |
| M10 / Y        | NEG      |   22.32 |   -15.61 |       -19.61 |
| M10 / N        | GO       |   77.68 |    12.76 |         8.76 |

## Will the Republican Party hold 57 or more Senate seats after the 2026 midterm elections?
Contract 943829; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         0.7 |         0.73 | +99.27 / −0.73   | 136.40×       |
| No     |        99.6 |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.00 |    -0.73 |        -2.73 |
| GB / N         | WEAK     |  100.00 |     0.38 |        -3.62 |
| ST / Y         | NEG      |    0.00 |    -0.73 |        -2.73 |
| ST / N         | WEAK     |  100.00 |     0.38 |        -3.62 |
| MX / Y         | NEG      |    0.00 |    -0.73 |        -2.73 |
| MX / N         | WEAK     |  100.00 |     0.38 |        -3.62 |
| M10 / Y        | NEG      |    0.00 |    -0.73 |        -2.73 |
| M10 / N        | WEAK     |  100.00 |     0.38 |        -3.62 |

## Will the Republican Party hold exactly 48 Senate seats after the 2026 midterm elections?
Contract 943820; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          16 |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |          86 |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   20.04 |     3.50 |        -0.50 |
| GB / N         | NEG      |   79.96 |    -6.52 |       -10.52 |
| ST / Y         | GO       |   21.82 |     5.29 |         1.29 |
| ST / N         | NEG      |   78.17 |    -8.31 |       -12.31 |
| MX / Y         | GO       |   21.01 |     4.48 |         0.48 |
| MX / N         | NEG      |   78.99 |    -7.50 |       -11.50 |
| M10 / Y        | WEAK     |   19.82 |     3.28 |        -0.72 |
| M10 / N        | NEG      |   80.18 |    -6.30 |       -10.30 |

## Will the Republican Party hold exactly 49 Senate seats after the 2026 midterm elections?
Contract 943821; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          14 |        14.48 | +85.52 / −14.48  | 5.91×         |
| No     |          87 |        87.45 | +12.55 / −87.45  | 0.14×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   25.63 |    11.15 |         7.15 |
| GB / N         | NEG      |   74.37 |   -13.09 |       -17.09 |
| ST / Y         | GO       |   27.11 |    12.62 |         8.62 |
| ST / N         | NEG      |   72.89 |   -14.56 |       -18.56 |
| MX / Y         | GO       |   22.78 |     8.29 |         4.29 |
| MX / N         | NEG      |   77.22 |   -10.23 |       -14.23 |
| M10 / Y        | GO       |   22.81 |     8.33 |         4.33 |
| M10 / N        | NEG      |   77.19 |   -10.26 |       -14.26 |

## Will the Republican Party hold exactly 50 Senate seats after the 2026 midterm elections?
Contract 943822; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          11 |        11.39 | +88.61 / −11.39  | 7.78×         |
| No     |          90 |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   21.60 |    10.21 |         6.21 |
| GB / N         | NEG      |   78.40 |   -11.96 |       -15.96 |
| ST / Y         | GO       |   21.65 |    10.26 |         6.26 |
| ST / N         | NEG      |   78.35 |   -12.01 |       -16.01 |
| MX / Y         | GO       |   17.56 |     6.17 |         2.17 |
| MX / N         | NEG      |   82.44 |    -7.92 |       -11.92 |
| M10 / Y        | GO       |   18.69 |     7.30 |         3.30 |
| M10 / N        | NEG      |   81.31 |    -9.05 |       -13.05 |

## Will the Republican Party hold exactly 51 Senate seats after the 2026 midterm elections?
Contract 943823; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           9 |         9.33 | +90.67 / −9.33   | 9.72×         |
| No     |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   12.21 |     2.88 |        -1.12 |
| GB / N         | NEG      |   87.79 |    -4.50 |        -8.50 |
| ST / Y         | WEAK     |   10.49 |     1.16 |        -2.84 |
| ST / N         | NEG      |   89.51 |    -2.78 |        -6.78 |
| MX / Y         | NEG      |    9.10 |    -0.22 |        -4.22 |
| MX / N         | NEG      |   90.90 |    -1.40 |        -5.40 |
| M10 / Y        | WEAK     |   10.55 |     1.22 |        -2.78 |
| M10 / N        | NEG      |   89.45 |    -2.85 |        -6.85 |

## Will the Republican Party hold exactly 52 Senate seats after the 2026 midterm elections?
Contract 943824; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         6.1 |         6.33 | +93.67 / −6.33   | 14.80×        |
| No     |        94.9 |        95.09 | +4.91 / −95.09   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    4.51 |    -1.82 |        -5.82 |
| GB / N         | WEAK     |   95.49 |     0.39 |        -3.61 |
| ST / Y         | NEG      |    3.46 |    -2.87 |        -6.87 |
| ST / N         | WEAK     |   96.54 |     1.44 |        -2.56 |
| MX / Y         | NEG      |    3.32 |    -3.01 |        -7.01 |
| MX / N         | WEAK     |   96.68 |     1.59 |        -2.41 |
| M10 / Y        | NEG      |    4.16 |    -2.17 |        -6.17 |
| M10 / N        | WEAK     |   95.84 |     0.74 |        -3.26 |

## Will the Republican Party hold exactly 53 Senate seats after the 2026 midterm elections?
Contract 943825; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        5.12 |         5.31 | +94.69 / −5.31   | 17.83×        |
| No     |       98.09 |        98.16 | +1.84 / −98.16   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.22 |    -4.09 |        -7.31 |
| GB / N         | WEAK     |   98.78 |     0.62 |        -3.38 |
| ST / Y         | NEG      |    0.75 |    -4.56 |        -7.31 |
| ST / N         | WEAK     |   99.25 |     1.09 |        -2.91 |
| MX / Y         | NEG      |    0.94 |    -4.37 |        -7.31 |
| MX / N         | WEAK     |   99.06 |     0.90 |        -3.10 |
| M10 / Y        | NEG      |    1.31 |    -4.00 |        -7.31 |
| M10 / N        | WEAK     |   98.69 |     0.53 |        -3.47 |

## Will the Republican Party hold exactly 54 Senate seats after the 2026 midterm elections?
Contract 943826; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         2.5 |         2.6  | +97.40 / −2.60   | 37.50×        |
| No     |        98.5 |        98.56 | +1.44 / −98.56   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.27 |    -2.33 |        -4.60 |
| GB / N         | WEAK     |   99.73 |     1.17 |        -2.83 |
| ST / Y         | NEG      |    0.13 |    -2.47 |        -4.60 |
| ST / N         | WEAK     |   99.87 |     1.31 |        -2.69 |
| MX / Y         | NEG      |    0.23 |    -2.37 |        -4.60 |
| MX / N         | WEAK     |   99.77 |     1.22 |        -2.78 |
| M10 / Y        | NEG      |    0.29 |    -2.31 |        -4.60 |
| M10 / N        | WEAK     |   99.71 |     1.15 |        -2.85 |

## Will the Republican Party hold exactly 55 Senate seats after the 2026 midterm elections?
Contract 943827; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         1   |         1.04 | +98.96 / −1.04   | 95.19×        |
| No     |        99.8 |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.02 |    -1.02 |        -3.04 |
| GB / N         | WEAK     |   99.98 |     0.17 |        -3.83 |
| ST / Y         | NEG      |    0.03 |    -1.01 |        -3.04 |
| ST / N         | WEAK     |   99.98 |     0.17 |        -3.83 |
| MX / Y         | NEG      |    0.03 |    -1.01 |        -3.04 |
| MX / N         | WEAK     |   99.97 |     0.17 |        -3.83 |
| M10 / Y        | NEG      |    0.05 |    -0.99 |        -3.04 |
| M10 / N        | WEAK     |   99.95 |     0.14 |        -3.86 |

## Will the Republican Party hold exactly 56 Senate seats after the 2026 midterm elections?
Contract 943828; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         0.3 |         0.31 | +99.69 / −0.31   | 319.55×       |
| No     |        99.9 |        99.9  | +0.10 / −99.90   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.00 |    -0.31 |        -2.31 |
| GB / N         | WEAK     |  100.00 |     0.10 |        -3.90 |
| ST / Y         | NEG      |    0.00 |    -0.31 |        -2.31 |
| ST / N         | WEAK     |  100.00 |     0.10 |        -3.90 |
| MX / Y         | NEG      |    0.00 |    -0.31 |        -2.31 |
| MX / N         | WEAK     |  100.00 |     0.09 |        -3.91 |
| M10 / Y        | NEG      |    0.00 |    -0.31 |        -2.31 |
| M10 / N        | WEAK     |  100.00 |     0.09 |        -3.91 |

## Will the Republicans win the Alabama Senate race in 2026?
Contract 630628; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        99.2 |        99.24 | +0.76 / −99.24   | 0.01×         |
| No     |         4.6 |         4.77 | +95.23 / −4.77   | 19.96×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.94 |     0.70 |        -3.30 |
| GB / N         | NEG      |    0.06 |    -4.71 |        -6.77 |
| ST / Y         | WEAK     |   99.85 |     0.61 |        -3.39 |
| ST / N         | NEG      |    0.15 |    -4.62 |        -6.77 |
| MX / Y         | NEG      |   98.46 |    -0.77 |        -4.77 |
| MX / N         | NEG      |    1.54 |    -3.24 |        -6.77 |
| M10 / Y        | NEG      |   98.54 |    -0.70 |        -4.70 |
| M10 / N        | NEG      |    1.46 |    -3.31 |        -6.77 |

## Will the Republicans win the Arkansas Senate race in 2026?
Contract 630654; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       96.27 |        96.41 | +3.59 / −96.41   | 0.04×         |
| No     |        5.9  |         6.12 | +93.88 / −6.12   | 15.33×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.76 |     3.35 |        -0.65 |
| GB / N         | NEG      |    0.24 |    -5.88 |        -8.12 |
| ST / Y         | WEAK     |   99.21 |     2.80 |        -1.20 |
| ST / N         | NEG      |    0.79 |    -5.33 |        -8.12 |
| MX / Y         | NEG      |   93.36 |    -3.05 |        -7.05 |
| MX / N         | WEAK     |    6.64 |     0.51 |        -3.49 |
| M10 / Y        | NEG      |   94.22 |    -2.19 |        -6.19 |
| M10 / N        | NEG      |    5.78 |    -0.35 |        -4.35 |

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

## Will the Republicans win the New Hampshire Senate race in 2026?
Contract 630845; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       16    |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |       85.42 |        85.92 | +14.08 / −85.92  | 0.16×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    2.07 |   -14.46 |       -18.46 |
| GB / N         | GO       |   97.93 |    12.01 |         8.01 |
| ST / Y         | NEG      |    2.42 |   -14.12 |       -18.12 |
| ST / N         | GO       |   97.58 |    11.66 |         7.66 |
| MX / Y         | NEG      |    7.23 |    -9.31 |       -13.31 |
| MX / N         | GO       |   92.77 |     6.85 |         2.85 |
| M10 / Y        | NEG      |    6.12 |   -10.42 |       -14.42 |
| M10 / N        | GO       |   93.88 |     7.96 |         3.96 |

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

## Will the Republicans win the Tennessee Senate race in 2026?
Contract 630951; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       97.2  |        97.31 | +2.69 / −97.31   | 0.03×         |
| No     |        3.96 |         4.12 | +95.88 / −4.12   | 23.30×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.97 |     2.66 |        -1.34 |
| GB / N         | NEG      |    0.03 |    -4.09 |        -6.12 |
| ST / Y         | WEAK     |   99.98 |     2.67 |        -1.33 |
| ST / N         | NEG      |    0.02 |    -4.09 |        -6.12 |
| MX / Y         | WEAK     |   99.92 |     2.61 |        -1.39 |
| MX / N         | NEG      |    0.08 |    -4.04 |        -6.12 |
| M10 / Y        | WEAK     |   99.95 |     2.64 |        -1.36 |
| M10 / N        | NEG      |    0.05 |    -4.07 |        -6.12 |

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

