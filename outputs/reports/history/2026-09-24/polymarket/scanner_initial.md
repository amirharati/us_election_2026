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

## Will the Democratic Party candidate win the 2026 Florida Senate election by 0%-3%?
Contract 3343185; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       31.57 |        32.36 | +67.64 / −32.36  | 2.09×         |
| No     |       90.48 |        90.82 | +9.18 / −90.82   | 0.10×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    9.44 |   -22.92 |       -26.92 |
| GB / N         | NEG      |   90.56 |    -0.26 |        -4.26 |
| ST / Y         | NEG      |    7.97 |   -24.40 |       -28.40 |
| ST / N         | WEAK     |   92.03 |     1.22 |        -2.78 |
| MX / Y         | NEG      |    9.64 |   -22.72 |       -26.72 |
| MX / N         | NEG      |   90.36 |    -0.46 |        -4.46 |
| M10 / Y        | NEG      |    8.79 |   -23.57 |       -27.57 |
| M10 / N        | WEAK     |   91.21 |     0.39 |        -3.61 |

## Will the Democratic Party candidate win the 2026 Florida Senate election by 3% or more?
Contract 3343186; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        6.12 |         6.35 | +93.65 / −6.35   | 14.75×        |
| No     |       97.55 |        97.65 | +2.35 / −97.65   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    8.40 |     2.05 |        -1.95 |
| GB / N         | NEG      |   91.60 |    -6.05 |       -10.05 |
| ST / Y         | NEG      |    4.46 |    -1.89 |        -5.89 |
| ST / N         | NEG      |   95.54 |    -2.10 |        -6.10 |
| MX / Y         | WEAK     |   10.28 |     3.93 |        -0.07 |
| MX / N         | NEG      |   89.72 |    -7.93 |       -11.93 |
| M10 / Y        | WEAK     |    9.20 |     2.85 |        -1.15 |
| M10 / N        | NEG      |   90.80 |    -6.84 |       -10.84 |

## Will the Democratic Party candidate win the 2026 Iowa Senate election by 0%-3%?
Contract 3343531; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        31.6 |        32.43 | +67.57 / −32.43  | 2.08×         |
| No     |        81   |        81.62 | +18.38 / −81.62  | 0.23×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   15.89 |   -16.54 |       -20.54 |
| GB / N         | WEAK     |   84.11 |     2.49 |        -1.51 |
| ST / Y         | NEG      |   17.74 |   -14.69 |       -18.69 |
| ST / N         | WEAK     |   82.26 |     0.64 |        -3.36 |
| MX / Y         | NEG      |   16.84 |   -15.59 |       -19.59 |
| MX / N         | WEAK     |   83.16 |     1.54 |        -2.46 |
| M10 / Y        | NEG      |   16.41 |   -16.02 |       -20.02 |
| M10 / N        | WEAK     |   83.59 |     1.97 |        -2.03 |

## Will the Democratic Party candidate win the 2026 Iowa Senate election by 12% or more?
Contract 3343535; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        0.77 |         0.8  | +99.20 / −0.80   | 124.73×       |
| No     |       99.8  |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.73 |    -0.06 |        -2.80 |
| GB / N         | NEG      |   99.27 |    -0.54 |        -4.54 |
| ST / Y         | NEG      |    0.22 |    -0.58 |        -2.80 |
| ST / N         | NEG      |   99.78 |    -0.03 |        -4.03 |
| MX / Y         | WEAK     |    0.90 |     0.11 |        -2.80 |
| MX / N         | NEG      |   99.10 |    -0.71 |        -4.71 |
| M10 / Y        | WEAK     |    0.82 |     0.03 |        -2.80 |
| M10 / N        | NEG      |   99.18 |    -0.63 |        -4.63 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 0%-10%?
Contract 3343809; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         1   |         1.04 | +98.96 / −1.04   | 95.19×        |
| No     |        99.4 |        99.42 | +0.58 / −99.42   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.40 |    -0.64 |        -3.04 |
| GB / N         | WEAK     |   99.60 |     0.18 |        -3.82 |
| ST / Y         | NEG      |    0.39 |    -0.65 |        -3.04 |
| ST / N         | WEAK     |   99.61 |     0.19 |        -3.81 |
| MX / Y         | NEG      |    0.77 |    -0.26 |        -3.04 |
| MX / N         | NEG      |   99.23 |    -0.20 |        -4.20 |
| M10 / Y        | WEAK     |    1.14 |     0.10 |        -3.04 |
| M10 / N        | NEG      |   98.86 |    -0.57 |        -4.57 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 10%-15%?
Contract 3343810; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         2   |         2.08 | +97.92 / −2.08   | 47.11×        |
| No     |        98.7 |        98.75 | +1.25 / −98.75   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    3.15 |     1.07 |        -2.93 |
| GB / N         | NEG      |   96.85 |    -1.90 |        -5.90 |
| ST / Y         | WEAK     |    2.27 |     0.19 |        -3.81 |
| ST / N         | NEG      |   97.73 |    -1.02 |        -5.02 |
| MX / Y         | WEAK     |    3.93 |     1.85 |        -2.15 |
| MX / N         | NEG      |   96.07 |    -2.68 |        -6.68 |
| M10 / Y        | WEAK     |    5.13 |     3.05 |        -0.95 |
| M10 / N        | NEG      |   94.87 |    -3.88 |        -7.88 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 15%-20%?
Contract 3343811; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         2.8 |         2.91 | +97.09 / −2.91   | 33.38×        |
| No     |        98   |        98.08 | +1.92 / −98.08   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   13.33 |    10.43 |         6.43 |
| GB / N         | NEG      |   86.67 |   -11.41 |       -15.41 |
| ST / Y         | GO       |   10.25 |     7.34 |         3.34 |
| ST / N         | NEG      |   89.75 |    -8.33 |       -12.33 |
| MX / Y         | GO       |   13.89 |    10.98 |         6.98 |
| MX / N         | NEG      |   86.11 |   -11.96 |       -15.96 |
| M10 / Y        | GO       |   16.66 |    13.75 |         9.75 |
| M10 / N        | NEG      |   83.34 |   -14.74 |       -18.74 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 20%-25%?
Contract 3343812; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       15.14 |        15.66 | +84.34 / −15.66  | 5.39×         |
| No     |       91    |        91.33 | +8.67 / −91.33   | 0.09×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   28.64 |    12.99 |         8.99 |
| GB / N         | NEG      |   71.36 |   -19.97 |       -23.97 |
| ST / Y         | GO       |   29.53 |    13.87 |         9.87 |
| ST / N         | NEG      |   70.47 |   -20.86 |       -24.86 |
| MX / Y         | GO       |   28.81 |    13.16 |         9.16 |
| MX / N         | NEG      |   71.19 |   -20.14 |       -24.14 |
| M10 / Y        | GO       |   31.08 |    15.42 |        11.42 |
| M10 / N        | NEG      |   68.92 |   -22.41 |       -26.41 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 35%-40%?
Contract 3343815; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       22    |        22.69 | +77.31 / −22.69  | 3.41×         |
| No     |       81.18 |        81.79 | +18.21 / −81.79  | 0.22×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    4.94 |   -17.75 |       -21.75 |
| GB / N         | GO       |   95.06 |    13.27 |         9.27 |
| ST / Y         | NEG      |    3.04 |   -19.65 |       -23.65 |
| ST / N         | GO       |   96.96 |    15.17 |        11.17 |
| MX / Y         | NEG      |    4.14 |   -18.55 |       -22.55 |
| MX / N         | GO       |   95.86 |    14.07 |        10.07 |
| M10 / Y        | NEG      |    2.98 |   -19.70 |       -23.70 |
| M10 / N        | GO       |   97.02 |    15.23 |        11.23 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 40%-45%?
Contract 3343816; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       15.61 |        16.14 | +83.86 / −16.14  | 5.20×         |
| No     |       91    |        91.33 | +8.67 / −91.33   | 0.09×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.71 |   -15.43 |       -18.14 |
| GB / N         | GO       |   99.29 |     7.96 |         3.96 |
| ST / Y         | NEG      |    0.26 |   -15.88 |       -18.14 |
| ST / N         | GO       |   99.74 |     8.41 |         4.41 |
| MX / Y         | NEG      |    0.65 |   -15.49 |       -18.14 |
| MX / N         | GO       |   99.35 |     8.03 |         4.03 |
| M10 / Y        | NEG      |    0.43 |   -15.71 |       -18.14 |
| M10 / N        | GO       |   99.57 |     8.24 |         4.24 |

## Will the Democratic Party candidate win the 2026 Massachusetts Senate election by 45% or more?
Contract 3343817; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         6.6 |         6.85 | +93.15 / −6.85   | 13.61×        |
| No     |        96.8 |        96.92 | +3.08 / −96.92   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.05 |    -6.79 |        -8.85 |
| GB / N         | WEAK     |   99.95 |     3.02 |        -0.98 |
| ST / Y         | NEG      |    0.03 |    -6.82 |        -8.85 |
| ST / N         | WEAK     |   99.98 |     3.05 |        -0.95 |
| MX / Y         | NEG      |    0.06 |    -6.78 |        -8.85 |
| MX / N         | WEAK     |   99.94 |     3.01 |        -0.99 |
| M10 / Y        | NEG      |    0.04 |    -6.81 |        -8.85 |
| M10 / N        | WEAK     |   99.96 |     3.04 |        -0.96 |

## Will the Democratic Party candidate win the 2026 Michigan Senate election by 3%-6%?
Contract 3343888; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       23    |        23.71 | +76.29 / −23.71  | 3.22×         |
| No     |       81.34 |        81.95 | +18.05 / −81.95  | 0.22×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   19.81 |    -3.90 |        -7.90 |
| GB / N         | NEG      |   80.19 |    -1.76 |        -5.76 |
| ST / Y         | WEAK     |   24.93 |     1.22 |        -2.78 |
| ST / N         | NEG      |   75.08 |    -6.87 |       -10.87 |
| MX / Y         | NEG      |   21.00 |    -2.71 |        -6.71 |
| MX / N         | NEG      |   79.00 |    -2.95 |        -6.95 |
| M10 / Y        | NEG      |   21.06 |    -2.65 |        -6.65 |
| M10 / N        | NEG      |   78.94 |    -3.01 |        -7.01 |

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 12%-15%?
Contract 3343942; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        10.6 |        10.97 | +89.03 / −10.97  | 8.11×         |
| No     |        95.4 |        95.58 | +4.42 / −95.58   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   17.78 |     6.81 |         2.81 |
| GB / N         | NEG      |   82.22 |   -13.36 |       -17.36 |
| ST / Y         | GO       |   18.04 |     7.07 |         3.07 |
| ST / N         | NEG      |   81.96 |   -13.62 |       -17.62 |
| MX / Y         | WEAK     |   13.20 |     2.23 |        -1.77 |
| MX / N         | NEG      |   86.80 |    -8.77 |       -12.77 |
| M10 / Y        | WEAK     |   14.28 |     3.31 |        -0.69 |
| M10 / N        | NEG      |   85.72 |    -9.85 |       -13.85 |

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 18% or more?
Contract 3343944; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        6.48 |         6.72 | +93.28 / −6.72   | 13.87×        |
| No     |       98.02 |        98.1  | +1.90 / −98.10   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    8.89 |     2.16 |        -1.84 |
| GB / N         | NEG      |   91.11 |    -6.98 |       -10.98 |
| ST / Y         | NEG      |    5.26 |    -1.46 |        -5.46 |
| ST / N         | NEG      |   94.74 |    -3.36 |        -7.36 |
| MX / Y         | NEG      |    4.81 |    -1.91 |        -5.91 |
| MX / N         | NEG      |   95.19 |    -2.91 |        -6.91 |
| M10 / Y        | NEG      |    5.80 |    -0.92 |        -4.92 |
| M10 / N        | NEG      |   94.20 |    -3.90 |        -7.90 |

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 3%-6%?
Contract 3343939; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          23 |        23.71 | +76.29 / −23.71  | 3.22×         |
| No     |          79 |        79.66 | +20.34 / −79.66  | 0.26×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   12.51 |   -11.20 |       -15.20 |
| GB / N         | GO       |   87.49 |     7.83 |         3.83 |
| ST / Y         | NEG      |   13.14 |   -10.57 |       -14.57 |
| ST / N         | GO       |   86.86 |     7.20 |         3.20 |
| MX / Y         | NEG      |   15.92 |    -7.79 |       -11.79 |
| MX / N         | GO       |   84.08 |     4.41 |         0.41 |
| M10 / Y        | NEG      |   14.98 |    -8.72 |       -12.72 |
| M10 / N        | GO       |   85.02 |     5.35 |         1.35 |

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 6%-9%?
Contract 3343940; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       18.72 |        19.33 | +80.67 / −19.33  | 4.17×         |
| No     |       83.6  |        84.15 | +15.85 / −84.15  | 0.19×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   18.42 |    -0.91 |        -4.91 |
| GB / N         | NEG      |   81.58 |    -2.57 |        -6.57 |
| ST / Y         | WEAK     |   19.85 |     0.52 |        -3.48 |
| ST / N         | NEG      |   80.15 |    -4.00 |        -8.00 |
| MX / Y         | NEG      |   18.91 |    -0.42 |        -4.42 |
| MX / N         | NEG      |   81.09 |    -3.05 |        -7.05 |
| M10 / Y        | NEG      |   18.66 |    -0.66 |        -4.66 |
| M10 / N        | NEG      |   81.34 |    -2.81 |        -6.81 |

## Will the Democratic Party candidate win the 2026 New Hampshire Senate election by 9%-12%?
Contract 3343941; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          15 |        15.51 | +84.49 / −15.51  | 5.45×         |
| No     |          86 |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   20.71 |     5.20 |         1.20 |
| GB / N         | NEG      |   79.29 |    -7.19 |       -11.19 |
| ST / Y         | GO       |   22.49 |     6.98 |         2.98 |
| ST / N         | NEG      |   77.51 |    -8.97 |       -12.97 |
| MX / Y         | WEAK     |   17.91 |     2.40 |        -1.60 |
| MX / N         | NEG      |   82.09 |    -4.39 |        -8.39 |
| M10 / Y        | WEAK     |   18.40 |     2.89 |        -1.11 |
| M10 / N        | NEG      |   81.60 |    -4.89 |        -8.89 |

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 12%-15%?
Contract 3343971; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10.93 |        11.32 | +88.68 / −11.32  | 7.83×         |
| No     |       91.7  |        92    | +8.00 / −92.00   | 0.09×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   15.08 |     3.75 |        -0.25 |
| GB / N         | NEG      |   84.92 |    -7.08 |       -11.08 |
| ST / Y         | GO       |   17.54 |     6.22 |         2.22 |
| ST / N         | NEG      |   82.46 |    -9.55 |       -13.55 |
| MX / Y         | GO       |   15.76 |     4.44 |         0.44 |
| MX / N         | NEG      |   84.24 |    -7.76 |       -11.76 |
| M10 / Y        | GO       |   15.77 |     4.45 |         0.45 |
| M10 / N        | NEG      |   84.23 |    -7.77 |       -11.77 |

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 15%-18%?
Contract 3343972; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       16    |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |       86.04 |        86.52 | +13.48 / −86.52  | 0.16×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   15.55 |    -0.99 |        -4.99 |
| GB / N         | NEG      |   84.45 |    -2.08 |        -6.08 |
| ST / Y         | WEAK     |   18.29 |     1.76 |        -2.24 |
| ST / N         | NEG      |   81.71 |    -4.82 |        -8.82 |
| MX / Y         | NEG      |   16.26 |    -0.28 |        -4.28 |
| MX / N         | NEG      |   83.74 |    -2.78 |        -6.78 |
| M10 / Y        | NEG      |   16.26 |    -0.27 |        -4.27 |
| M10 / N        | NEG      |   83.74 |    -2.79 |        -6.79 |

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 6%-9%?
Contract 3343969; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        7.72 |         8    | +92.00 / −8.00   | 11.49×        |
| No     |       95.66 |        95.83 | +4.17 / −95.83   | 0.04×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    8.92 |     0.92 |        -3.08 |
| GB / N         | NEG      |   91.08 |    -4.75 |        -8.75 |
| ST / Y         | NEG      |    7.81 |    -0.19 |        -4.19 |
| ST / N         | NEG      |   92.19 |    -3.64 |        -7.64 |
| MX / Y         | WEAK     |    8.76 |     0.76 |        -3.24 |
| MX / N         | NEG      |   91.24 |    -4.59 |        -8.59 |
| M10 / Y        | WEAK     |    8.81 |     0.81 |        -3.19 |
| M10 / N        | NEG      |   91.19 |    -4.64 |        -8.64 |

## Will the Democratic Party candidate win the 2026 New Mexico Senate election by 9%-12%?
Contract 3343970; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        10.9 |        11.29 | +88.71 / −11.29  | 7.86×         |
| No     |        95.5 |        95.67 | +4.33 / −95.67   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   12.53 |     1.24 |        -2.76 |
| GB / N         | NEG      |   87.47 |    -8.20 |       -12.20 |
| ST / Y         | WEAK     |   12.87 |     1.58 |        -2.42 |
| ST / N         | NEG      |   87.13 |    -8.54 |       -12.54 |
| MX / Y         | WEAK     |   12.57 |     1.29 |        -2.71 |
| MX / N         | NEG      |   87.43 |    -8.25 |       -12.25 |
| M10 / Y        | WEAK     |   12.65 |     1.37 |        -2.63 |
| M10 / N        | NEG      |   87.35 |    -8.32 |       -12.32 |

## Will the Democratic Party candidate win the 2026 North Carolina Senate election by 12%-15%?
Contract 3344037; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        16.3 |        16.82 | +83.18 / −16.82  | 4.94×         |
| No     |        88.1 |        88.52 | +11.48 / −88.52  | 0.13×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    5.48 |   -11.35 |       -15.35 |
| GB / N         | GO       |   94.52 |     6.00 |         2.00 |
| ST / Y         | NEG      |    3.51 |   -13.31 |       -17.31 |
| ST / N         | GO       |   96.49 |     7.97 |         3.97 |
| MX / Y         | NEG      |    3.07 |   -13.75 |       -17.75 |
| MX / N         | GO       |   96.93 |     8.41 |         4.41 |
| M10 / Y        | NEG      |    3.16 |   -13.67 |       -17.67 |
| M10 / N        | GO       |   96.84 |     8.32 |         4.32 |

## Will the Democratic Party candidate win the 2026 North Carolina Senate election by 3%-6%?
Contract 3344034; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          16 |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |          87 |        87.45 | +12.55 / −87.45  | 0.14×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   23.31 |     6.78 |         2.78 |
| GB / N         | NEG      |   76.69 |   -10.77 |       -14.77 |
| ST / Y         | GO       |   28.39 |    11.85 |         7.85 |
| ST / N         | NEG      |   71.61 |   -15.84 |       -19.84 |
| MX / Y         | GO       |   28.04 |    11.50 |         7.50 |
| MX / N         | NEG      |   71.96 |   -15.49 |       -19.49 |
| M10 / Y        | GO       |   28.07 |    11.53 |         7.53 |
| M10 / N        | NEG      |   71.93 |   -15.52 |       -19.52 |

## Will the Democratic Party candidate win the 2026 North Carolina Senate election by 9%-12%?
Contract 3344036; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          16 |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |          87 |        87.45 | +12.55 / −87.45  | 0.14×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   12.51 |    -4.03 |        -8.03 |
| GB / N         | WEAK     |   87.49 |     0.04 |        -3.96 |
| ST / Y         | NEG      |   11.48 |    -5.06 |        -9.06 |
| ST / N         | WEAK     |   88.52 |     1.07 |        -2.93 |
| MX / Y         | NEG      |    9.48 |    -7.06 |       -11.06 |
| MX / N         | WEAK     |   90.52 |     3.07 |        -0.93 |
| M10 / Y        | NEG      |    9.59 |    -6.95 |       -10.95 |
| M10 / N        | WEAK     |   90.41 |     2.96 |        -1.04 |

## Will the Democratic Party candidate win the 2026 Ohio Senate election by 0%-3%?
Contract 3344047; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       19    |        19.62 | +80.38 / −19.62  | 4.10×         |
| No     |       83.61 |        84.16 | +15.84 / −84.16  | 0.19×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   20.19 |     0.58 |        -3.42 |
| GB / N         | NEG      |   79.81 |    -4.35 |        -8.35 |
| ST / Y         | GO       |   24.77 |     5.16 |         1.16 |
| ST / N         | NEG      |   75.23 |    -8.93 |       -12.93 |
| MX / Y         | WEAK     |   21.87 |     2.26 |        -1.74 |
| MX / N         | NEG      |   78.13 |    -6.03 |       -10.03 |
| M10 / Y        | WEAK     |   22.26 |     2.64 |        -1.36 |
| M10 / N        | NEG      |   77.74 |    -6.42 |       -10.42 |

## Will the Democratic Party candidate win the 2026 Ohio Senate election by 6%-9%?
Contract 3344049; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       23.29 |        24    | +76.00 / −24.00  | 3.17×         |
| No     |       82    |        82.59 | +17.41 / −82.59  | 0.21×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   14.93 |    -9.08 |       -13.08 |
| GB / N         | WEAK     |   85.07 |     2.48 |        -1.52 |
| ST / Y         | NEG      |   15.46 |    -8.55 |       -12.55 |
| ST / N         | WEAK     |   84.54 |     1.95 |        -2.05 |
| MX / Y         | NEG      |   14.17 |    -9.83 |       -13.83 |
| MX / N         | WEAK     |   85.83 |     3.24 |        -0.76 |
| M10 / Y        | NEG      |   12.90 |   -11.11 |       -15.11 |
| M10 / N        | GO       |   87.10 |     4.51 |         0.51 |

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 10%-15%?
Contract 3344099; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.63 |         2.72 | +97.28 / −2.72   | 35.78×        |
| No     |       99.3  |        99.33 | +0.67 / −99.33   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    5.05 |     2.33 |        -1.67 |
| GB / N         | NEG      |   94.95 |    -4.38 |        -8.38 |
| ST / Y         | WEAK     |    3.48 |     0.77 |        -3.23 |
| ST / N         | NEG      |   96.52 |    -2.81 |        -6.81 |
| MX / Y         | GO       |    7.38 |     4.66 |         0.66 |
| MX / N         | NEG      |   92.62 |    -6.71 |       -10.71 |
| M10 / Y        | GO       |    8.19 |     5.47 |         1.47 |
| M10 / N        | NEG      |   91.81 |    -7.51 |       -11.51 |

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 25%-30%?
Contract 3344102; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          23 |        23.71 | +76.29 / −23.71  | 3.22×         |
| No     |          78 |        78.69 | +21.31 / −78.69  | 0.27×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   23.61 |    -0.10 |        -4.10 |
| GB / N         | NEG      |   76.39 |    -2.30 |        -6.30 |
| ST / Y         | WEAK     |   26.78 |     3.07 |        -0.93 |
| ST / N         | NEG      |   73.22 |    -5.46 |        -9.46 |
| MX / Y         | NEG      |   20.54 |    -3.17 |        -7.17 |
| MX / N         | WEAK     |   79.46 |     0.78 |        -3.22 |
| M10 / Y        | NEG      |   20.35 |    -3.36 |        -7.36 |
| M10 / N        | WEAK     |   79.65 |     0.96 |        -3.04 |

## Will the Democratic Party candidate win the 2026 Rhode Island Senate election by 5%-10%?
Contract 3344098; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         0.5 |         0.52 | +99.48 / −0.52   | 191.34×       |
| No     |        99.6 |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    1.50 |     0.98 |        -2.52 |
| GB / N         | NEG      |   98.50 |    -1.11 |        -5.11 |
| ST / Y         | WEAK     |    1.26 |     0.74 |        -2.52 |
| ST / N         | NEG      |   98.74 |    -0.87 |        -4.87 |
| MX / Y         | WEAK     |    4.05 |     3.53 |        -0.47 |
| MX / N         | NEG      |   95.95 |    -3.66 |        -7.66 |
| M10 / Y        | WEAK     |    4.49 |     3.97 |        -0.03 |
| M10 / N        | NEG      |   95.51 |    -4.11 |        -8.11 |

## Will the Democratic Party candidate win the 2026 Texas Senate election by 3%-6%?
Contract 3344142; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       23.79 |        24.51 | +75.49 / −24.51  | 3.08×         |
| No     |       81    |        81.62 | +18.38 / −81.62  | 0.23×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   16.89 |    -7.63 |       -11.63 |
| GB / N         | WEAK     |   83.11 |     1.50 |        -2.50 |
| ST / Y         | NEG      |   17.25 |    -7.26 |       -11.26 |
| ST / N         | WEAK     |   82.75 |     1.13 |        -2.87 |
| MX / Y         | NEG      |   16.41 |    -8.10 |       -12.10 |
| MX / N         | WEAK     |   83.59 |     1.97 |        -2.03 |
| M10 / Y        | NEG      |   16.65 |    -7.87 |       -11.87 |
| M10 / N        | WEAK     |   83.35 |     1.74 |        -2.26 |

## Will the Democratic Party candidate win the 2026 Texas Senate election by 9%-12%?
Contract 3344144; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        4.94 |         5.13 | +94.87 / −5.13   | 18.50×        |
| No     |       95.2  |        95.38 | +4.62 / −95.38   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    2.91 |    -2.22 |        -6.22 |
| GB / N         | WEAK     |   97.09 |     1.71 |        -2.29 |
| ST / Y         | NEG      |    1.57 |    -3.55 |        -7.13 |
| ST / N         | WEAK     |   98.42 |     3.04 |        -0.96 |
| MX / Y         | NEG      |    2.30 |    -2.83 |        -6.83 |
| MX / N         | WEAK     |   97.70 |     2.32 |        -1.68 |
| M10 / Y        | NEG      |    2.38 |    -2.75 |        -6.75 |
| M10 / N        | WEAK     |   97.62 |     2.24 |        -1.76 |

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 0%-3%?
Contract 3344162; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         0.9 |         0.94 | +99.06 / −0.94   | 105.87×       |
| No     |        99.2 |        99.23 | +0.77 / −99.23   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    2.36 |     1.43 |        -2.57 |
| GB / N         | NEG      |   97.64 |    -1.59 |        -5.59 |
| ST / Y         | WEAK     |    1.62 |     0.69 |        -2.94 |
| ST / N         | NEG      |   98.38 |    -0.86 |        -4.86 |
| MX / Y         | WEAK     |    3.03 |     2.09 |        -1.91 |
| MX / N         | NEG      |   96.97 |    -2.26 |        -6.26 |
| M10 / Y        | WEAK     |    3.54 |     2.61 |        -1.39 |
| M10 / N        | NEG      |   96.46 |    -2.77 |        -6.77 |

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 12%-15%?
Contract 3344166; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10.17 |        10.53 | +89.47 / −10.53  | 8.49×         |
| No     |       93    |        93.26 | +6.74 / −93.26   | 0.07×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   14.42 |     3.89 |        -0.11 |
| GB / N         | NEG      |   85.58 |    -7.68 |       -11.68 |
| ST / Y         | GO       |   16.10 |     5.57 |         1.57 |
| ST / N         | NEG      |   83.90 |    -9.36 |       -13.36 |
| MX / Y         | WEAK     |   13.55 |     3.01 |        -0.99 |
| MX / N         | NEG      |   86.45 |    -6.81 |       -10.81 |
| M10 / Y        | WEAK     |   14.10 |     3.57 |        -0.43 |
| M10 / N        | NEG      |   85.90 |    -7.36 |       -11.36 |

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 18%-21%?
Contract 3344168; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       28.55 |        29.37 | +70.63 / −29.37  | 2.41×         |
| No     |       74.91 |        75.67 | +24.33 / −75.67  | 0.32×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   14.36 |   -15.00 |       -19.00 |
| GB / N         | GO       |   85.64 |     9.97 |         5.97 |
| ST / Y         | NEG      |   16.90 |   -12.46 |       -16.46 |
| ST / N         | GO       |   83.10 |     7.43 |         3.43 |
| MX / Y         | NEG      |   13.33 |   -16.04 |       -20.04 |
| MX / N         | GO       |   86.67 |    11.01 |         7.01 |
| M10 / Y        | NEG      |   12.48 |   -16.89 |       -20.89 |
| M10 / N        | GO       |   87.52 |    11.85 |         7.85 |

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 3%-6%?
Contract 3344163; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         1.2 |         1.25 | +98.75 / −1.25   | 79.17×        |
| No     |        99.1 |        99.14 | +0.86 / −99.14   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    4.66 |     3.41 |        -0.59 |
| GB / N         | NEG      |   95.34 |    -3.80 |        -7.80 |
| ST / Y         | WEAK     |    3.18 |     1.93 |        -2.07 |
| ST / N         | NEG      |   96.82 |    -2.31 |        -6.31 |
| MX / Y         | WEAK     |    5.00 |     3.75 |        -0.25 |
| MX / N         | NEG      |   95.00 |    -4.14 |        -8.14 |
| M10 / Y        | GO       |    5.76 |     4.51 |         0.51 |
| M10 / N        | NEG      |   94.24 |    -4.89 |        -8.89 |

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 6%-9%?
Contract 3344164; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        3.07 |         3.19 | +96.81 / −3.19   | 30.36×        |
| No     |       97.54 |        97.64 | +2.36 / −97.64   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |    7.90 |     4.71 |         0.71 |
| GB / N         | NEG      |   92.10 |    -5.54 |        -9.54 |
| ST / Y         | WEAK     |    6.47 |     3.28 |        -0.72 |
| ST / N         | NEG      |   93.53 |    -4.11 |        -8.11 |
| MX / Y         | GO       |    7.66 |     4.47 |         0.47 |
| MX / N         | NEG      |   92.34 |    -5.30 |        -9.30 |
| M10 / Y        | GO       |    8.51 |     5.32 |         1.32 |
| M10 / N        | NEG      |   91.49 |    -6.15 |       -10.15 |

## Will the Democratic Party candidate win the 2026 Virginia Senate election by 9%-12%?
Contract 3344165; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.01 |         9.34 | +90.66 / −9.34   | 9.71×         |
| No     |       96.63 |        96.76 | +3.24 / −96.76   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   11.52 |     2.18 |        -1.82 |
| GB / N         | NEG      |   88.48 |    -8.28 |       -12.28 |
| ST / Y         | WEAK     |   10.63 |     1.30 |        -2.70 |
| ST / N         | NEG      |   89.37 |    -7.40 |       -11.40 |
| MX / Y         | WEAK     |   10.88 |     1.54 |        -2.46 |
| MX / N         | NEG      |   89.12 |    -7.64 |       -11.64 |
| M10 / Y        | WEAK     |   11.87 |     2.53 |        -1.47 |
| M10 / N        | NEG      |   88.13 |    -8.63 |       -12.63 |

## Will the Democratic Party control the Senate after the 2026 Midterm elections?
Contract 562793; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          63 |        63.93 | +36.07 / −63.93  | 0.56×         |
| No     |          38 |        38.94 | +61.06 / −38.94  | 1.57×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   47.59 |   -16.34 |       -20.34 |
| GB / N         | GO       |   52.41 |    13.46 |         9.46 |
| ST / Y         | NEG      |   52.91 |   -11.02 |       -15.02 |
| ST / N         | GO       |   47.09 |     8.15 |         4.15 |
| MX / Y         | NEG      |   57.72 |    -6.22 |       -10.22 |
| MX / N         | WEAK     |   42.28 |     3.34 |        -0.66 |
| M10 / Y        | NEG      |   53.99 |    -9.95 |       -13.95 |
| M10 / N        | GO       |   46.01 |     7.07 |         3.07 |

## Will the Democrats win the Alabama Senate race in 2026?
Contract 630627; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        4.23 |         4.39 | +95.61 / −4.39   | 21.77×        |
| No     |       99.4  |        99.42 | +0.58 / −99.42   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.04 |    -4.35 |        -6.39 |
| GB / N         | WEAK     |   99.96 |     0.54 |        -3.46 |
| ST / Y         | NEG      |    0.13 |    -4.26 |        -6.39 |
| ST / N         | WEAK     |   99.87 |     0.44 |        -3.56 |
| MX / Y         | NEG      |    1.38 |    -3.02 |        -6.39 |
| MX / N         | NEG      |   98.62 |    -0.80 |        -4.80 |
| M10 / Y        | NEG      |    1.33 |    -3.07 |        -6.39 |
| M10 / N        | NEG      |   98.67 |    -0.75 |        -4.75 |

## Will the Democrats win the Arkansas Senate race in 2026?
Contract 630653; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        6.44 |         6.69 | +93.31 / −6.69   | 13.96×        |
| No     |       95.97 |        96.12 | +3.88 / −96.12   | 0.04×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.17 |    -6.52 |        -8.69 |
| GB / N         | WEAK     |   99.83 |     3.71 |        -0.29 |
| ST / Y         | NEG      |    0.88 |    -5.80 |        -8.69 |
| ST / N         | WEAK     |   99.12 |     2.99 |        -1.01 |
| MX / Y         | NEG      |    6.29 |    -0.40 |        -4.40 |
| MX / N         | NEG      |   93.71 |    -2.41 |        -6.41 |
| M10 / Y        | NEG      |    5.55 |    -1.14 |        -5.14 |
| M10 / N        | NEG      |   94.45 |    -1.67 |        -5.67 |

## Will the Democrats win the Florida Senate race in 2026?
Contract 631044; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           9 |         9.33 | +90.67 / −9.33   | 9.72×         |
| No     |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   17.85 |     8.52 |         4.52 |
| GB / N         | NEG      |   82.15 |   -10.14 |       -14.14 |
| ST / Y         | WEAK     |   12.42 |     3.09 |        -0.91 |
| ST / N         | NEG      |   87.58 |    -4.72 |        -8.72 |
| MX / Y         | GO       |   19.92 |    10.59 |         6.59 |
| MX / N         | NEG      |   80.08 |   -12.22 |       -16.22 |
| M10 / Y        | GO       |   17.99 |     8.66 |         4.66 |
| M10 / N        | NEG      |   82.01 |   -10.28 |       -14.28 |

## Will the Democrats win the Iowa Senate race in 2026?
Contract 630733; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          47 |        48    | +52.00 / −48.00  | 1.08×         |
| No     |          55 |        55.99 | +44.01 / −55.99  | 0.79×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   33.52 |   -14.48 |       -18.48 |
| GB / N         | GO       |   66.48 |    10.49 |         6.49 |
| ST / Y         | NEG      |   30.84 |   -17.15 |       -21.15 |
| ST / N         | GO       |   69.16 |    13.17 |         9.17 |
| MX / Y         | NEG      |   34.81 |   -13.18 |       -17.18 |
| MX / N         | GO       |   65.19 |     9.20 |         5.20 |
| M10 / Y        | NEG      |   33.43 |   -14.57 |       -18.57 |
| M10 / N        | GO       |   66.57 |    10.58 |         6.58 |

## Will the Democrats win the Kansas Senate race in 2026?
Contract 630746; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          31 |        31.86 | +68.14 / −31.86  | 2.14×         |
| No     |          70 |        70.84 | +29.16 / −70.84  | 0.41×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    6.41 |   -25.44 |       -29.44 |
| GB / N         | GO       |   93.59 |    22.75 |        18.75 |
| ST / Y         | NEG      |    6.48 |   -25.37 |       -29.37 |
| ST / N         | GO       |   93.52 |    22.68 |        18.68 |
| MX / Y         | NEG      |    7.76 |   -24.09 |       -28.09 |
| MX / N         | GO       |   92.24 |    21.40 |        17.40 |
| M10 / Y        | NEG      |    8.70 |   -23.15 |       -27.15 |
| M10 / N        | GO       |   91.30 |    20.46 |        16.46 |

## Will the Democrats win the Kentucky Senate race in 2026?
Contract 630759; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        4.32 |         4.48 | +95.52 / −4.48   | 21.31×        |
| No     |       98.3  |        98.37 | +1.63 / −98.37   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.36 |    -3.12 |        -6.48 |
| GB / N         | WEAK     |   98.64 |     0.27 |        -3.73 |
| ST / Y         | NEG      |    0.98 |    -3.50 |        -6.48 |
| ST / N         | WEAK     |   99.02 |     0.65 |        -3.35 |
| MX / Y         | NEG      |    3.28 |    -1.20 |        -5.20 |
| MX / N         | NEG      |   96.72 |    -1.65 |        -5.65 |
| M10 / Y        | NEG      |    2.55 |    -1.94 |        -5.94 |
| M10 / N        | NEG      |   97.45 |    -0.91 |        -4.91 |

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
| ST / Y         | WEAK     |   99.99 |     1.62 |        -2.38 |
| ST / N         | NEG      |    0.01 |    -2.58 |        -4.60 |
| MX / Y         | WEAK     |   99.99 |     1.62 |        -2.38 |
| MX / N         | NEG      |    0.01 |    -2.58 |        -4.60 |
| M10 / Y        | WEAK     |   99.98 |     1.61 |        -2.39 |
| M10 / N        | NEG      |    0.02 |    -2.58 |        -4.60 |

## Will the Democrats win the Michigan Senate race in 2026?
Contract 630805; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          72 |        72.81 | +27.19 / −72.81  | 0.37×         |
| No     |          29 |        29.82 | +70.18 / −29.82  | 2.35×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   80.83 |     8.03 |         4.03 |
| GB / N         | NEG      |   19.17 |   -10.66 |       -14.66 |
| ST / Y         | GO       |   86.12 |    13.31 |         9.31 |
| ST / N         | NEG      |   13.88 |   -15.94 |       -19.94 |
| MX / Y         | GO       |   81.42 |     8.62 |         4.62 |
| MX / N         | NEG      |   18.58 |   -11.25 |       -15.25 |
| M10 / Y        | GO       |   77.28 |     4.48 |         0.48 |
| M10 / N        | NEG      |   22.72 |    -7.11 |       -11.11 |

## Will the Democrats win the Minnesota Senate race in 2026?
Contract 630818; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          93 |        93.26 | +6.74 / −93.26   | 0.07×         |
| No     |           8 |         8.29 | +91.71 / −8.29   | 11.06×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   87.90 |    -5.36 |        -9.36 |
| GB / N         | WEAK     |   12.10 |     3.80 |        -0.20 |
| ST / Y         | NEG      |   91.06 |    -2.20 |        -6.20 |
| ST / N         | WEAK     |    8.94 |     0.65 |        -3.35 |
| MX / Y         | NEG      |   90.68 |    -2.58 |        -6.58 |
| MX / N         | WEAK     |    9.32 |     1.03 |        -2.97 |
| M10 / Y        | NEG      |   89.68 |    -3.58 |        -7.58 |
| M10 / N        | WEAK     |   10.32 |     2.02 |        -1.98 |

## Will the Democrats win the Mississippi Senate race in 2026?
Contract 631017; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           9 |         9.33 | +90.67 / −9.33   | 9.72×         |
| No     |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    2.40 |    -6.93 |       -10.93 |
| GB / N         | GO       |   97.60 |     5.31 |         1.31 |
| ST / Y         | NEG      |    2.11 |    -7.22 |       -11.22 |
| ST / N         | GO       |   97.89 |     5.59 |         1.59 |
| MX / Y         | NEG      |    5.43 |    -3.90 |        -7.90 |
| MX / N         | WEAK     |   94.57 |     2.28 |        -1.72 |
| M10 / Y        | NEG      |    6.61 |    -2.72 |        -6.72 |
| M10 / N        | WEAK     |   93.39 |     1.10 |        -2.90 |

## Will the Democrats win the New Hampshire Senate race in 2026?
Contract 630844; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          86 |        86.48 | +13.52 / −86.48  | 0.16×         |
| No     |          16 |        16.54 | +83.46 / −16.54  | 5.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   96.44 |     9.96 |         5.96 |
| GB / N         | NEG      |    3.56 |   -12.98 |       -16.98 |
| ST / Y         | GO       |   95.80 |     9.32 |         5.32 |
| ST / N         | NEG      |    4.20 |   -12.33 |       -16.33 |
| MX / Y         | WEAK     |   89.02 |     2.54 |        -1.46 |
| MX / N         | NEG      |   10.98 |    -5.56 |        -9.56 |
| M10 / Y        | WEAK     |   90.45 |     3.97 |        -0.03 |
| M10 / N        | NEG      |    9.55 |    -6.99 |       -10.99 |

## Will the Democrats win the New Mexico Senate race in 2026?
Contract 630870; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       97.95 |        98.04 | +1.96 / −98.04   | 0.02×         |
| No     |        3.26 |         3.39 | +96.61 / −3.39   | 28.51×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   98.01 |    -0.03 |        -4.03 |
| GB / N         | NEG      |    1.99 |    -1.39 |        -5.39 |
| ST / Y         | WEAK     |   99.04 |     1.00 |        -3.00 |
| ST / N         | NEG      |    0.96 |    -2.43 |        -5.39 |
| MX / Y         | WEAK     |   98.14 |     0.11 |        -3.89 |
| MX / N         | NEG      |    1.86 |    -1.53 |        -5.39 |
| M10 / Y        | WEAK     |   98.11 |     0.08 |        -3.92 |
| M10 / N        | NEG      |    1.89 |    -1.50 |        -5.39 |

## Will the Democrats win the North Carolina Senate race in 2026?
Contract 630883; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          95 |        95.19 | +4.81 / −95.19   | 0.05×         |
| No     |           6 |         6.23 | +93.77 / −6.23   | 15.06×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   82.76 |   -12.43 |       -16.43 |
| GB / N         | GO       |   17.24 |    11.02 |         7.02 |
| ST / Y         | NEG      |   88.79 |    -6.40 |       -10.40 |
| ST / N         | GO       |   11.21 |     4.98 |         0.98 |
| MX / Y         | NEG      |   84.52 |   -10.67 |       -14.67 |
| MX / N         | GO       |   15.48 |     9.26 |         5.26 |
| M10 / Y        | NEG      |   84.81 |   -10.38 |       -14.38 |
| M10 / N        | GO       |   15.19 |     8.97 |         4.97 |

## Will the Democrats win the Ohio Senate race in 2026?
Contract 631057; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          62 |        62.94 | +37.06 / −62.94  | 0.59×         |
| No     |          39 |        39.95 | +60.05 / −39.95  | 1.50×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   68.94 |     6.00 |         2.00 |
| GB / N         | NEG      |   31.06 |    -8.89 |       -12.89 |
| ST / Y         | GO       |   74.74 |    11.80 |         7.80 |
| ST / N         | NEG      |   25.26 |   -14.70 |       -18.70 |
| MX / Y         | GO       |   68.40 |     5.45 |         1.45 |
| MX / N         | NEG      |   31.60 |    -8.35 |       -12.35 |
| M10 / Y        | WEAK     |   64.78 |     1.84 |        -2.16 |
| M10 / N        | NEG      |   35.22 |    -4.73 |        -8.73 |

## Will the Democrats win the Oklahoma Senate race in 2026?
Contract 631030; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        3.82 |         3.96 | +96.04 / −3.96   | 24.23×        |
| No     |       97.54 |        97.64 | +2.36 / −97.64   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.05 |    -3.91 |        -5.96 |
| GB / N         | WEAK     |   99.95 |     2.31 |        -1.69 |
| ST / Y         | NEG      |    0.38 |    -3.58 |        -5.96 |
| ST / N         | WEAK     |   99.62 |     1.98 |        -2.02 |
| MX / Y         | NEG      |    1.35 |    -2.61 |        -5.96 |
| MX / N         | WEAK     |   98.65 |     1.01 |        -2.99 |
| M10 / Y        | NEG      |    1.46 |    -2.50 |        -5.96 |
| M10 / N        | WEAK     |   98.54 |     0.90 |        -3.10 |

## Will the Democrats win the Rhode Island Senate race in 2026?
Contract 630911; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       99.5  |        99.52 | +0.48 / −99.52   | 0.00×         |
| No     |        3.14 |         3.26 | +96.74 / −3.26   | 29.64×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.95 |     0.43 |        -3.57 |
| GB / N         | NEG      |    0.05 |    -3.21 |        -5.26 |
| ST / Y         | WEAK     |   99.79 |     0.27 |        -3.73 |
| ST / N         | NEG      |    0.21 |    -3.06 |        -5.26 |
| MX / Y         | NEG      |   98.43 |    -1.09 |        -5.09 |
| MX / N         | NEG      |    1.57 |    -1.69 |        -5.26 |
| M10 / Y        | NEG      |   98.16 |    -1.36 |        -5.36 |
| M10 / N        | NEG      |    1.84 |    -1.42 |        -5.26 |

## Will the Democrats win the South Carolina Senate race in 2026?
Contract 630924; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          14 |        14.48 | +85.52 / −14.48  | 5.91×         |
| No     |          87 |        87.45 | +12.55 / −87.45  | 0.14×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    3.34 |   -11.14 |       -15.14 |
| GB / N         | GO       |   96.66 |     9.21 |         5.21 |
| ST / Y         | NEG      |    2.54 |   -11.94 |       -15.94 |
| ST / N         | GO       |   97.46 |    10.00 |         6.00 |
| MX / Y         | NEG      |    6.37 |    -8.11 |       -12.11 |
| MX / N         | GO       |   93.63 |     6.18 |         2.18 |
| M10 / Y        | NEG      |    5.66 |    -8.82 |       -12.82 |
| M10 / N        | GO       |   94.34 |     6.89 |         2.89 |

## Will the Democrats win the Tennessee Senate race in 2026?
Contract 630950; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         3.8 |         3.95 | +96.05 / −3.95   | 24.34×        |
| No     |        97.3 |        97.41 | +2.59 / −97.41   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.49 |    -3.46 |        -5.95 |
| GB / N         | WEAK     |   99.51 |     2.11 |        -1.89 |
| ST / Y         | NEG      |    1.10 |    -2.84 |        -5.95 |
| ST / N         | WEAK     |   98.90 |     1.49 |        -2.51 |
| MX / Y         | NEG      |    2.75 |    -1.19 |        -5.19 |
| MX / N         | NEG      |   97.25 |    -0.16 |        -4.16 |
| M10 / Y        | NEG      |    2.84 |    -1.11 |        -5.11 |
| M10 / N        | NEG      |   97.16 |    -0.24 |        -4.24 |

## Will the Democrats win the Texas Senate race in 2026?
Contract 630963; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          62 |        62.94 | +37.06 / −62.94  | 0.59×         |
| No     |          40 |        40.96 | +59.04 / −40.96  | 1.44×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   52.51 |   -10.43 |       -14.43 |
| GB / N         | GO       |   47.49 |     6.53 |         2.53 |
| ST / Y         | NEG      |   53.69 |    -9.25 |       -13.25 |
| ST / N         | GO       |   46.31 |     5.35 |         1.35 |
| MX / Y         | NEG      |   51.19 |   -11.75 |       -15.75 |
| MX / N         | GO       |   48.81 |     7.85 |         3.85 |
| M10 / Y        | NEG      |   51.85 |   -11.09 |       -15.09 |
| M10 / N        | GO       |   48.15 |     7.19 |         3.19 |

## Will the Democrats win the Virginia Senate race in 2026?
Contract 630976; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       99.61 |        99.63 | +0.37 / −99.63   | 0.00×         |
| No     |        2.96 |         3.08 | +96.92 / −3.08   | 31.49×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   98.42 |    -1.21 |        -5.21 |
| GB / N         | NEG      |    1.58 |    -1.50 |        -5.08 |
| ST / Y         | NEG      |   98.14 |    -1.49 |        -5.49 |
| ST / N         | NEG      |    1.86 |    -1.22 |        -5.08 |
| MX / Y         | NEG      |   95.82 |    -3.81 |        -7.81 |
| MX / N         | WEAK     |    4.18 |     1.10 |        -2.90 |
| M10 / Y        | NEG      |   95.05 |    -4.58 |        -8.58 |
| M10 / N        | WEAK     |    4.95 |     1.87 |        -2.13 |

## Will the Republican Party candidate win the 2026 Alabama Senate election by 0%-5%?
Contract 3343107; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.17 |         9.49 | +90.51 / −9.49   | 9.54×         |
| No     |       97.3  |        97.41 | +2.59 / −97.41   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.44 |    -9.05 |       -11.49 |
| GB / N         | WEAK     |   99.56 |     2.16 |        -1.84 |
| ST / Y         | NEG      |    0.58 |    -8.91 |       -11.49 |
| ST / N         | WEAK     |   99.42 |     2.01 |        -1.99 |
| MX / Y         | NEG      |    2.77 |    -6.72 |       -10.72 |
| MX / N         | NEG      |   97.23 |    -0.18 |        -4.18 |
| M10 / Y        | NEG      |    2.70 |    -6.79 |       -10.79 |
| M10 / N        | NEG      |   97.30 |    -0.11 |        -4.11 |

## Will the Republican Party candidate win the 2026 Alabama Senate election by 10%-15%?
Contract 3343105; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       13.87 |        14.35 | +85.65 / −14.35  | 5.97×         |
| No     |       90.39 |        90.74 | +9.26 / −90.74   | 0.10×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   10.84 |    -3.51 |        -7.51 |
| GB / N         | NEG      |   89.16 |    -1.57 |        -5.57 |
| ST / Y         | NEG      |    8.34 |    -6.01 |       -10.01 |
| ST / N         | WEAK     |   91.66 |     0.93 |        -3.07 |
| MX / Y         | NEG      |   13.32 |    -1.03 |        -5.03 |
| MX / N         | NEG      |   86.68 |    -4.06 |        -8.06 |
| M10 / Y        | NEG      |   13.08 |    -1.26 |        -5.26 |
| M10 / N        | NEG      |   86.92 |    -3.82 |        -7.82 |

## Will the Republican Party candidate win the 2026 Alabama Senate election by 20%-25%?
Contract 3343103; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       20.85 |        21.51 | +78.49 / −21.51  | 3.65×         |
| No     |       81.3  |        81.91 | +18.09 / −81.91  | 0.22×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   29.53 |     8.03 |         4.03 |
| GB / N         | NEG      |   70.47 |   -11.44 |       -15.44 |
| ST / Y         | GO       |   34.18 |    12.67 |         8.67 |
| ST / N         | NEG      |   65.82 |   -16.09 |       -20.09 |
| MX / Y         | GO       |   25.68 |     4.17 |         0.17 |
| MX / N         | NEG      |   74.32 |    -7.58 |       -11.58 |
| M10 / Y        | GO       |   25.79 |     4.28 |         0.28 |
| M10 / N        | NEG      |   74.21 |    -7.70 |       -11.70 |

## Will the Republican Party candidate win the 2026 Arkansas Senate election by 10%-15%?
Contract 3343124; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       27.37 |        28.16 | +71.84 / −28.16  | 2.55×         |
| No     |       73.65 |        74.43 | +25.57 / −74.43  | 0.34×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   14.32 |   -13.84 |       -17.84 |
| GB / N         | GO       |   85.68 |    11.25 |         7.25 |
| ST / Y         | NEG      |   15.55 |   -12.61 |       -16.61 |
| ST / N         | GO       |   84.45 |    10.02 |         6.02 |
| MX / Y         | NEG      |   17.43 |   -10.74 |       -14.74 |
| MX / N         | GO       |   82.57 |     8.14 |         4.14 |
| M10 / Y        | NEG      |   16.71 |   -11.46 |       -15.46 |
| M10 / N        | GO       |   83.29 |     8.86 |         4.86 |

## Will the Republican Party candidate win the 2026 Arkansas Senate election by 20%-25%?
Contract 3343122; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          11 |        11.39 | +88.61 / −11.39  | 7.78×         |
| No     |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   26.79 |    15.40 |        11.40 |
| GB / N         | NEG      |   73.21 |   -19.08 |       -23.08 |
| ST / Y         | GO       |   28.38 |    16.99 |        12.99 |
| ST / N         | NEG      |   71.62 |   -20.67 |       -24.67 |
| MX / Y         | GO       |   19.32 |     7.93 |         3.93 |
| MX / N         | NEG      |   80.68 |   -11.62 |       -15.62 |
| M10 / Y        | GO       |   20.10 |     8.71 |         4.71 |
| M10 / N        | NEG      |   79.90 |   -12.39 |       -16.39 |

## Will the Republican Party candidate win the 2026 Florida Senate election by 12%-15%?
Contract 3343180; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        8.64 |         8.96 | +91.04 / −8.96   | 10.17×        |
| No     |       97.15 |        97.26 | +2.74 / −97.26   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    9.59 |     0.63 |        -3.37 |
| GB / N         | NEG      |   90.41 |    -6.85 |       -10.85 |
| ST / Y         | NEG      |    7.68 |    -1.28 |        -5.28 |
| ST / N         | NEG      |   92.32 |    -4.94 |        -8.94 |
| MX / Y         | NEG      |    8.56 |    -0.40 |        -4.40 |
| MX / N         | NEG      |   91.44 |    -5.82 |        -9.82 |
| M10 / Y        | WEAK     |    9.33 |     0.38 |        -3.62 |
| M10 / N        | NEG      |   90.67 |    -6.59 |       -10.59 |

## Will the Republican Party candidate win the 2026 Florida Senate election by 15%-18%?
Contract 3343179; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.61 |         2.71 | +97.29 / −2.71   | 35.90×        |
| No     |       98.5  |        98.56 | +1.44 / −98.56   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    5.19 |     2.48 |        -1.52 |
| GB / N         | NEG      |   94.81 |    -3.75 |        -7.75 |
| ST / Y         | WEAK     |    2.73 |     0.02 |        -3.98 |
| ST / N         | NEG      |   97.27 |    -1.29 |        -5.29 |
| MX / Y         | WEAK     |    4.53 |     1.82 |        -2.18 |
| MX / N         | NEG      |   95.47 |    -3.09 |        -7.09 |
| M10 / Y        | WEAK     |    5.00 |     2.29 |        -1.71 |
| M10 / N        | NEG      |   95.00 |    -3.56 |        -7.56 |

## Will the Republican Party candidate win the 2026 Florida Senate election by 21% or more?
Contract 3343177; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        0.99 |         1.03 | +98.97 / −1.03   | 95.98×        |
| No     |       99.8  |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    1.13 |     0.10 |        -3.03 |
| GB / N         | NEG      |   98.87 |    -0.94 |        -4.94 |
| ST / Y         | NEG      |    0.28 |    -0.75 |        -3.03 |
| ST / N         | NEG      |   99.72 |    -0.09 |        -4.09 |
| MX / Y         | WEAK     |    1.58 |     0.54 |        -3.03 |
| MX / N         | NEG      |   98.42 |    -1.38 |        -5.38 |
| M10 / Y        | WEAK     |    1.83 |     0.80 |        -3.03 |
| M10 / N        | NEG      |   98.17 |    -1.64 |        -5.64 |

## Will the Republican Party candidate win the 2026 Iowa Senate election by 0%-3%?
Contract 3343530; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        28   |        28.81 | +71.19 / −28.81  | 2.47×         |
| No     |        74.8 |        75.55 | +24.45 / −75.55  | 0.32×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   19.61 |    -9.20 |       -13.20 |
| GB / N         | GO       |   80.39 |     4.84 |         0.84 |
| ST / Y         | NEG      |   24.62 |    -4.19 |        -8.19 |
| ST / N         | NEG      |   75.38 |    -0.17 |        -4.17 |
| MX / Y         | NEG      |   21.00 |    -7.80 |       -11.80 |
| MX / N         | WEAK     |   79.00 |     3.44 |        -0.56 |
| M10 / Y        | NEG      |   20.91 |    -7.89 |       -11.89 |
| M10 / N        | WEAK     |   79.09 |     3.53 |        -0.47 |

## Will the Republican Party candidate win the 2026 Iowa Senate election by 12% or more?
Contract 3343526; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         4.9 |         5.09 | +94.91 / −5.09   | 18.66×        |
| No     |        99.2 |        99.23 | +0.77 / −99.23   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    5.59 |     0.50 |        -3.50 |
| GB / N         | NEG      |   94.41 |    -4.82 |        -8.82 |
| ST / Y         | NEG      |    2.54 |    -2.55 |        -6.55 |
| ST / N         | NEG      |   97.46 |    -1.77 |        -5.77 |
| MX / Y         | NEG      |    4.46 |    -0.63 |        -4.63 |
| MX / N         | NEG      |   95.54 |    -3.69 |        -7.69 |
| M10 / Y        | NEG      |    4.80 |    -0.28 |        -4.28 |
| M10 / N        | NEG      |   95.20 |    -4.04 |        -8.04 |

## Will the Republican Party candidate win the 2026 Iowa Senate election by 3%-6%?
Contract 3343529; 100 shares per position.

| Side   | Entry (¢)   | Budget ($)   | Win / lose ($)   | Reward/loss   |
|:-------|:------------|:-------------|:-----------------|:--------------|
| Yes    | 21.00       | 21.66        | +78.34 / −21.66  | 3.62×         |
| No     | —           | —            | Unavailable      | —             |

| Model / side   | Status   |   P (%) | EV ($)   | Stress ($)          |
|:---------------|:---------|--------:|:---------|:--------------------|
| GB / Y         | NEG      |   18.86 | -2.80    | -6.8013906132380955 |
| GB / N         | N/A      |   81.14 | —        | —                   |
| ST / Y         | WEAK     |   22.46 | 0.80     | -3.2042249999999965 |
| ST / N         | N/A      |   77.54 | —        | —                   |
| MX / Y         | NEG      |   19.62 | -2.04    | -6.042089583333333  |
| MX / N         | N/A      |   80.38 | —        | —                   |
| M10 / Y        | NEG      |   19.87 | -1.79    | -5.789589583333333  |
| M10 / N        | N/A      |   80.13 | —        | —                   |

## Will the Republican Party candidate win the 2026 Iowa Senate election by 6%-9%?
Contract 3343528; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       12.33 |        12.76 | +87.24 / −12.76  | 6.84×         |
| No     |       90    |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   14.15 |     1.39 |        -2.61 |
| GB / N         | NEG      |   85.85 |    -4.51 |        -8.51 |
| ST / Y         | WEAK     |   13.72 |     0.96 |        -3.04 |
| ST / N         | NEG      |   86.28 |    -4.08 |        -8.08 |
| MX / Y         | WEAK     |   13.30 |     0.54 |        -3.46 |
| MX / N         | NEG      |   86.70 |    -3.66 |        -7.66 |
| M10 / Y        | WEAK     |   13.81 |     1.06 |        -2.94 |
| M10 / N        | NEG      |   86.19 |    -4.17 |        -8.17 |

## Will the Republican Party candidate win the 2026 Iowa Senate election by 9%-12%?
Contract 3343527; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         3.8 |         3.95 | +96.05 / −3.95   | 24.34×        |
| No     |        97.7 |        97.79 | +2.21 / −97.79   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |    8.28 |     4.33 |         0.33 |
| GB / N         | NEG      |   91.72 |    -6.07 |       -10.07 |
| ST / Y         | WEAK     |    5.83 |     1.88 |        -2.12 |
| ST / N         | NEG      |   94.17 |    -3.61 |        -7.61 |
| MX / Y         | WEAK     |    6.81 |     2.86 |        -1.14 |
| MX / N         | NEG      |   93.19 |    -4.60 |        -8.60 |
| M10 / Y        | WEAK     |    7.17 |     3.22 |        -0.78 |
| M10 / N        | NEG      |   92.83 |    -4.96 |        -8.96 |

## Will the Republican Party candidate win the 2026 Kansas Senate election by 10%-15%?
Contract 3343544; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          10 |        10.36 | +89.64 / −10.36  | 8.65×         |
| No     |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   26.97 |    16.61 |        12.61 |
| GB / N         | NEG      |   73.03 |   -19.26 |       -23.26 |
| ST / Y         | GO       |   26.29 |    15.93 |        11.93 |
| ST / N         | NEG      |   73.71 |   -18.59 |       -22.59 |
| MX / Y         | GO       |   25.65 |    15.29 |        11.29 |
| MX / N         | NEG      |   74.35 |   -17.94 |       -21.94 |
| M10 / Y        | GO       |   24.22 |    13.86 |         9.86 |
| M10 / N        | NEG      |   75.78 |   -16.52 |       -20.52 |

## Will the Republican Party candidate win the 2026 Kansas Senate election by 15%-20%?
Contract 3343543; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           6 |         6.23 | +93.77 / −6.23   | 15.06×        |
| No     |          97 |        97.12 | +2.88 / −97.12   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    9.74 |     3.52 |        -0.48 |
| GB / N         | NEG      |   90.26 |    -6.86 |       -10.86 |
| ST / Y         | WEAK     |    6.37 |     0.14 |        -3.86 |
| ST / N         | NEG      |   93.63 |    -3.48 |        -7.48 |
| MX / Y         | WEAK     |    8.59 |     2.36 |        -1.64 |
| MX / N         | NEG      |   91.41 |    -5.70 |        -9.70 |
| M10 / Y        | WEAK     |    7.69 |     1.46 |        -2.54 |
| M10 / N        | NEG      |   92.31 |    -4.80 |        -8.80 |

## Will the Republican Party candidate win the 2026 Kansas Senate election by 20%-25%?
Contract 3343542; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.13 |         9.46 | +90.54 / −9.46   | 9.58×         |
| No     |       96.96 |        97.08 | +2.92 / −97.08   | 0.03×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.62 |    -7.83 |       -11.46 |
| GB / N         | WEAK     |   98.38 |     1.30 |        -2.70 |
| ST / Y         | NEG      |    0.61 |    -8.84 |       -11.46 |
| ST / N         | WEAK     |   99.39 |     2.31 |        -1.69 |
| MX / Y         | NEG      |    1.52 |    -7.94 |       -11.46 |
| MX / N         | WEAK     |   98.48 |     1.40 |        -2.60 |
| M10 / Y        | NEG      |    1.31 |    -8.14 |       -11.46 |
| M10 / N        | WEAK     |   98.69 |     1.61 |        -2.39 |

## Will the Republican Party candidate win the 2026 Kansas Senate election by 25%-30%?
Contract 3343541; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          11 |        11.39 | +88.61 / −11.39  | 7.78×         |
| No     |          95 |        95.19 | +4.81 / −95.19   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.12 |   -11.27 |       -13.39 |
| GB / N         | GO       |   99.88 |     4.69 |         0.69 |
| ST / Y         | NEG      |    0.04 |   -11.35 |       -13.39 |
| ST / N         | GO       |   99.96 |     4.77 |         0.77 |
| MX / Y         | NEG      |    0.14 |   -11.25 |       -13.39 |
| MX / N         | GO       |   99.86 |     4.67 |         0.67 |
| M10 / Y        | NEG      |    0.11 |   -11.28 |       -13.39 |
| M10 / N        | GO       |   99.89 |     4.70 |         0.70 |

## Will the Republican Party candidate win the 2026 Kansas Senate election by 30% or more?
Contract 3343540; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        1.4  |         1.46 | +98.54 / −1.46   | 67.72×        |
| No     |       99.72 |        99.73 | +0.27 / −99.73   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.00 |    -1.45 |        -3.46 |
| GB / N         | WEAK     |  100.00 |     0.26 |        -3.74 |
| ST / Y         | NEG      |    0.00 |    -1.46 |        -3.46 |
| ST / N         | WEAK     |  100.00 |     0.27 |        -3.73 |
| MX / Y         | NEG      |    0.01 |    -1.45 |        -3.46 |
| MX / N         | WEAK     |   99.99 |     0.26 |        -3.74 |
| M10 / Y        | NEG      |    0.01 |    -1.45 |        -3.46 |
| M10 / N        | WEAK     |   99.99 |     0.26 |        -3.74 |

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 15%-20%?
Contract 3343563; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          21 |        21.66 | +78.34 / −21.66  | 3.62×         |
| No     |          81 |        81.62 | +18.38 / −81.62  | 0.23×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   26.13 |     4.46 |         0.46 |
| GB / N         | NEG      |   73.87 |    -7.74 |       -11.74 |
| ST / Y         | GO       |   28.36 |     6.70 |         2.70 |
| ST / N         | NEG      |   71.64 |    -9.97 |       -13.97 |
| MX / Y         | WEAK     |   23.24 |     1.58 |        -2.42 |
| MX / N         | NEG      |   76.76 |    -4.86 |        -8.86 |
| M10 / Y        | WEAK     |   25.64 |     3.98 |        -0.02 |
| M10 / N        | NEG      |   74.36 |    -7.26 |       -11.26 |

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 20%-25%?
Contract 3343562; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       21.34 |        22.01 | +77.99 / −22.01  | 3.54×         |
| No     |       83.8  |        84.34 | +15.66 / −84.34  | 0.19×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   11.87 |   -10.14 |       -14.14 |
| GB / N         | WEAK     |   88.13 |     3.79 |        -0.21 |
| ST / Y         | NEG      |    8.71 |   -13.30 |       -17.30 |
| ST / N         | GO       |   91.29 |     6.94 |         2.94 |
| MX / Y         | NEG      |    9.02 |   -12.99 |       -16.99 |
| MX / N         | GO       |   90.98 |     6.63 |         2.63 |
| M10 / Y        | NEG      |   11.00 |   -11.01 |       -15.01 |
| M10 / N        | GO       |   89.00 |     4.66 |         0.66 |

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 25%-30%?
Contract 3343561; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       13.16 |        13.62 | +86.38 / −13.62  | 6.34×         |
| No     |       92.5  |        92.78 | +7.22 / −92.78   | 0.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    2.89 |   -10.72 |       -14.72 |
| GB / N         | GO       |   97.11 |     4.33 |         0.33 |
| ST / Y         | NEG      |    1.24 |   -12.38 |       -15.62 |
| ST / N         | GO       |   98.76 |     5.98 |         1.98 |
| MX / Y         | NEG      |    2.20 |   -11.41 |       -15.41 |
| MX / N         | GO       |   97.80 |     5.02 |         1.02 |
| M10 / Y        | NEG      |    2.92 |   -10.70 |       -14.70 |
| M10 / N        | GO       |   97.08 |     4.30 |         0.30 |

## Will the Republican Party candidate win the 2026 Kentucky Senate election by 30%-35%?
Contract 3343560; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       19.78 |        20.39 | +79.61 / −20.39  | 3.91×         |
| No     |       93.5  |        93.74 | +6.26 / −93.74   | 0.07×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.38 |   -20.01 |       -22.39 |
| GB / N         | GO       |   99.62 |     5.88 |         1.88 |
| ST / Y         | NEG      |    0.12 |   -20.26 |       -22.39 |
| ST / N         | GO       |   99.88 |     6.13 |         2.13 |
| MX / Y         | NEG      |    0.34 |   -20.05 |       -22.39 |
| MX / N         | GO       |   99.66 |     5.92 |         1.92 |
| M10 / Y        | NEG      |    0.50 |   -19.89 |       -22.39 |
| M10 / N        | GO       |   99.50 |     5.76 |         1.76 |

## Will the Republican Party candidate win the 2026 Michigan Senate election by 12% or more?
Contract 3343882; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.74 |        10.08 | +89.92 / −10.08  | 8.92×         |
| No     |       99.7  |        99.71 | +0.29 / −99.71   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.19 |    -9.89 |       -12.08 |
| GB / N         | WEAK     |   99.81 |     0.10 |        -3.90 |
| ST / Y         | NEG      |    0.08 |   -10.00 |       -12.08 |
| ST / N         | WEAK     |   99.92 |     0.20 |        -3.80 |
| MX / Y         | NEG      |    0.32 |    -9.77 |       -12.08 |
| MX / N         | NEG      |   99.68 |    -0.03 |        -4.03 |
| M10 / Y        | NEG      |    0.45 |    -9.64 |       -12.08 |
| M10 / N        | NEG      |   99.55 |    -0.16 |        -4.16 |

## Will the Republican Party candidate win the 2026 Michigan Senate election by 6%-9%?
Contract 3343884; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       32.75 |        33.53 | +66.47 / −33.53  | 1.98×         |
| No     |       95.06 |        95.24 | +4.76 / −95.24   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    2.14 |   -31.39 |       -35.39 |
| GB / N         | WEAK     |   97.86 |     2.61 |        -1.39 |
| ST / Y         | NEG      |    1.10 |   -32.43 |       -35.53 |
| ST / N         | WEAK     |   98.90 |     3.65 |        -0.35 |
| MX / Y         | NEG      |    2.12 |   -31.41 |       -35.41 |
| MX / N         | WEAK     |   97.88 |     2.63 |        -1.37 |
| M10 / Y        | NEG      |    2.77 |   -30.76 |       -34.76 |
| M10 / N        | WEAK     |   97.23 |     1.99 |        -2.01 |

## Will the Republican Party candidate win the 2026 Michigan Senate election by 9%-12%?
Contract 3343883; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       29.13 |        29.86 | +70.14 / −29.86  | 2.35×         |
| No     |       97.95 |        98.03 | +1.97 / −98.03   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.66 |   -29.20 |       -31.86 |
| GB / N         | WEAK     |   99.34 |     1.31 |        -2.69 |
| ST / Y         | NEG      |    0.27 |   -29.59 |       -31.86 |
| ST / N         | WEAK     |   99.73 |     1.70 |        -2.30 |
| MX / Y         | NEG      |    0.73 |   -29.12 |       -31.86 |
| MX / N         | WEAK     |   99.27 |     1.23 |        -2.77 |
| M10 / Y        | NEG      |    1.01 |   -28.84 |       -31.86 |
| M10 / N        | WEAK     |   98.99 |     0.96 |        -3.04 |

## Will the Republican Party candidate win the 2026 New Hampshire Senate election by 0%-3%?
Contract 3343937; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          14 |        14.48 | +85.52 / −14.48  | 5.91×         |
| No     |          90 |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    2.57 |   -11.91 |       -15.91 |
| GB / N         | GO       |   97.43 |     7.07 |         3.07 |
| ST / Y         | NEG      |    2.84 |   -11.64 |       -15.64 |
| ST / N         | GO       |   97.16 |     6.80 |         2.80 |
| MX / Y         | NEG      |    6.17 |    -8.31 |       -12.31 |
| MX / N         | WEAK     |   93.83 |     3.47 |        -0.53 |
| M10 / Y        | NEG      |    5.47 |    -9.01 |       -13.01 |
| M10 / N        | GO       |   94.53 |     4.17 |         0.17 |

## Will the Republican Party candidate win the 2026 New Mexico Senate election by 3% or more?
Contract 3343965; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.69 |         2.79 | +97.21 / −2.79   | 34.80×        |
| No     |       99.4  |        99.42 | +0.58 / −99.42   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.71 |    -2.08 |        -4.79 |
| GB / N         | NEG      |   99.29 |    -0.14 |        -4.14 |
| ST / Y         | NEG      |    0.31 |    -2.49 |        -4.79 |
| ST / N         | WEAK     |   99.69 |     0.27 |        -3.73 |
| MX / Y         | NEG      |    0.69 |    -2.11 |        -4.79 |
| MX / N         | NEG      |   99.31 |    -0.11 |        -4.11 |
| M10 / Y        | NEG      |    0.69 |    -2.10 |        -4.79 |
| M10 / N        | NEG      |   99.31 |    -0.12 |        -4.12 |

## Will the Republican Party candidate win the 2026 North Carolina Senate election by 0%-3%?
Contract 3344032; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         6.5 |         6.74 | +93.26 / −6.74   | 13.83×        |
| No     |        96   |        96.15 | +3.85 / −96.15   | 0.04×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   11.05 |     4.30 |         0.30 |
| GB / N         | NEG      |   88.95 |    -7.20 |       -11.20 |
| ST / Y         | WEAK     |    8.38 |     1.63 |        -2.37 |
| ST / N         | NEG      |   91.62 |    -4.53 |        -8.53 |
| MX / Y         | GO       |   11.02 |     4.28 |         0.28 |
| MX / N         | NEG      |   88.98 |    -7.18 |       -11.18 |
| M10 / Y        | GO       |   10.83 |     4.08 |         0.08 |
| M10 / N        | NEG      |   89.17 |    -6.98 |       -10.98 |

## Will the Republican Party candidate win the 2026 Ohio Senate election by 0%-3%?
Contract 3344046; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       19.4  |        20.02 | +79.98 / −20.02  | 3.99×         |
| No     |       83.17 |        83.73 | +16.27 / −83.73  | 0.19×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   15.67 |    -4.36 |        -8.36 |
| GB / N         | WEAK     |   84.33 |     0.60 |        -3.40 |
| ST / Y         | NEG      |   15.72 |    -4.31 |        -8.31 |
| ST / N         | WEAK     |   84.28 |     0.55 |        -3.45 |
| MX / Y         | NEG      |   16.66 |    -3.36 |        -7.36 |
| MX / N         | NEG      |   83.34 |    -0.39 |        -4.39 |
| M10 / Y        | NEG      |   17.93 |    -2.09 |        -6.09 |
| M10 / N        | NEG      |   82.07 |    -1.66 |        -5.66 |

## Will the Republican Party candidate win the 2026 Ohio Senate election by 9%-12%?
Contract 3344043; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        1.98 |         2.06 | +97.94 / −2.06   | 47.52×        |
| No     |       99.4  |        99.42 | +0.58 / −99.42   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.45 |    -0.61 |        -4.06 |
| GB / N         | NEG      |   98.55 |    -0.87 |        -4.87 |
| ST / Y         | NEG      |    0.48 |    -1.58 |        -4.06 |
| ST / N         | WEAK     |   99.52 |     0.10 |        -3.90 |
| MX / Y         | NEG      |    1.47 |    -0.59 |        -4.06 |
| MX / N         | NEG      |   98.53 |    -0.90 |        -4.90 |
| M10 / Y        | NEG      |    1.79 |    -0.27 |        -4.06 |
| M10 / N        | NEG      |   98.21 |    -1.21 |        -5.21 |

## Will the Republican Party candidate win the 2026 Oklahoma Senate election by 15%-20%?
Contract 3344070; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       26.73 |        27.46 | +72.54 / −27.46  | 2.64×         |
| No     |       87    |        87.45 | +12.55 / −87.45  | 0.14×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   11.31 |   -16.16 |       -20.16 |
| GB / N         | WEAK     |   88.69 |     1.24 |        -2.76 |
| ST / Y         | NEG      |    9.48 |   -17.98 |       -21.98 |
| ST / N         | WEAK     |   90.52 |     3.06 |        -0.94 |
| MX / Y         | NEG      |   10.67 |   -16.79 |       -20.79 |
| MX / N         | WEAK     |   89.33 |     1.87 |        -2.13 |
| M10 / Y        | NEG      |   11.42 |   -16.04 |       -20.04 |
| M10 / N        | WEAK     |   88.58 |     1.12 |        -2.88 |

## Will the Republican Party candidate win the 2026 Oklahoma Senate election by 35%-40%?
Contract 3344066; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10    |        10.36 | +89.64 / −10.36  | 8.65×         |
| No     |       93.93 |        94.16 | +5.84 / −94.16   | 0.06×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   12.28 |     1.92 |        -2.08 |
| GB / N         | NEG      |   87.72 |    -6.44 |       -10.44 |
| ST / Y         | NEG      |    9.56 |    -0.80 |        -4.80 |
| ST / N         | NEG      |   90.44 |    -3.72 |        -7.72 |
| MX / Y         | WEAK     |   10.91 |     0.55 |        -3.45 |
| MX / N         | NEG      |   89.09 |    -5.07 |        -9.07 |
| M10 / Y        | NEG      |   10.18 |    -0.18 |        -4.18 |
| M10 / N        | NEG      |   89.82 |    -4.34 |        -8.34 |

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 0%-5%?
Contract 3344126; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       30.4  |        31.25 | +68.75 / −31.25  | 2.20×         |
| No     |       73.41 |        74.19 | +25.81 / −74.19  | 0.35×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   12.67 |   -18.58 |       -22.58 |
| GB / N         | GO       |   87.33 |    13.14 |         9.14 |
| ST / Y         | NEG      |   10.76 |   -20.48 |       -24.48 |
| ST / N         | GO       |   89.24 |    15.04 |        11.04 |
| MX / Y         | NEG      |   15.51 |   -15.73 |       -19.73 |
| MX / N         | GO       |   84.49 |    10.29 |         6.29 |
| M10 / Y        | NEG      |   14.31 |   -16.94 |       -20.94 |
| M10 / N        | GO       |   85.69 |    11.50 |         7.50 |

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 10%-15%?
Contract 3344124; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       16.08 |        16.62 | +83.38 / −16.62  | 5.02×         |
| No     |       85    |        85.51 | +14.49 / −85.51  | 0.17×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   31.46 |    14.84 |        10.84 |
| GB / N         | NEG      |   68.54 |   -16.97 |       -20.97 |
| ST / Y         | GO       |   36.76 |    20.14 |        16.14 |
| ST / N         | NEG      |   63.24 |   -22.27 |       -26.27 |
| MX / Y         | GO       |   29.44 |    12.82 |         8.82 |
| MX / N         | NEG      |   70.56 |   -14.95 |       -18.95 |
| M10 / Y        | GO       |   30.26 |    13.64 |         9.64 |
| M10 / N        | NEG      |   69.74 |   -15.77 |       -19.77 |

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 15%-20%?
Contract 3344123; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       13.92 |        14.39 | +85.61 / −14.39  | 5.95×         |
| No     |       92    |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   18.31 |     3.92 |        -0.08 |
| GB / N         | NEG      |   81.69 |   -10.60 |       -14.60 |
| ST / Y         | WEAK     |   16.09 |     1.70 |        -2.30 |
| ST / N         | NEG      |   83.91 |    -8.39 |       -12.39 |
| MX / Y         | WEAK     |   14.57 |     0.18 |        -3.82 |
| MX / N         | NEG      |   85.43 |    -6.87 |       -10.87 |
| M10 / Y        | WEAK     |   15.88 |     1.48 |        -2.52 |
| M10 / N        | NEG      |   84.12 |    -8.17 |       -12.17 |

## Will the Republican Party candidate win the 2026 South Carolina Senate election by 30% or more?
Contract 3344120; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        9.84 |        10.19 | +89.81 / −10.19  | 8.81×         |
| No     |       99.5  |        99.52 | +0.48 / −99.52   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.07 |   -10.12 |       -12.19 |
| GB / N         | WEAK     |   99.93 |     0.41 |        -3.59 |
| ST / Y         | NEG      |    0.03 |   -10.16 |       -12.19 |
| ST / N         | WEAK     |   99.97 |     0.45 |        -3.55 |
| MX / Y         | NEG      |    0.09 |   -10.11 |       -12.19 |
| MX / N         | WEAK     |   99.91 |     0.39 |        -3.61 |
| M10 / Y        | NEG      |    0.10 |   -10.09 |       -12.19 |
| M10 / N        | WEAK     |   99.90 |     0.38 |        -3.62 |

## Will the Republican Party candidate win the 2026 Tennessee Senate election by 15%-20%?
Contract 3344154; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       16.71 |        17.27 | +82.73 / −17.27  | 4.79×         |
| No     |       86    |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   21.28 |     4.01 |         0.01 |
| GB / N         | NEG      |   78.72 |    -7.76 |       -11.76 |
| ST / Y         | GO       |   23.94 |     6.67 |         2.67 |
| ST / N         | NEG      |   76.06 |   -10.42 |       -14.42 |
| MX / Y         | WEAK     |   19.88 |     2.61 |        -1.39 |
| MX / N         | NEG      |   80.12 |    -6.36 |       -10.36 |
| M10 / Y        | WEAK     |   20.07 |     2.80 |        -1.20 |
| M10 / N        | NEG      |   79.93 |    -6.55 |       -10.55 |

## Will the Republican Party candidate win the 2026 Tennessee Senate election by 45% or more?
Contract 3344148; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       10.65 |        10.99 | +89.01 / −10.99  | 8.10×         |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.22 |   -10.77 |       -12.99 |
| GB / N         | WEAK     |   99.78 |     0.16 |        -3.84 |
| ST / Y         | NEG      |    0.63 |   -10.36 |       -12.99 |
| ST / N         | NEG      |   99.37 |    -0.25 |        -4.25 |
| MX / Y         | NEG      |    1.40 |    -9.60 |       -12.99 |
| MX / N         | NEG      |   98.60 |    -1.01 |        -5.01 |
| M10 / Y        | NEG      |    1.35 |    -9.64 |       -12.99 |
| M10 / N        | NEG      |   98.65 |    -0.97 |        -4.97 |

## Will the Republican Party candidate win the 2026 Texas Senate election by 12% or more?
Contract 3344136; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.14 |         2.22 | +97.78 / −2.22   | 44.06×        |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.58 |    -1.64 |        -4.22 |
| GB / N         | NEG      |   99.42 |    -0.20 |        -4.20 |
| ST / Y         | NEG      |    0.16 |    -2.06 |        -4.22 |
| ST / N         | WEAK     |   99.84 |     0.22 |        -3.78 |
| MX / Y         | NEG      |    0.57 |    -1.64 |        -4.22 |
| MX / N         | NEG      |   99.43 |    -0.19 |        -4.19 |
| M10 / Y        | NEG      |    0.55 |    -1.67 |        -4.22 |
| M10 / N        | NEG      |   99.45 |    -0.17 |        -4.17 |

## Will the Republican Party candidate win the 2026 Texas Senate election by 3%-6%?
Contract 3344139; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       11.44 |        11.85 | +88.15 / −11.85  | 7.44×         |
| No     |       89.9  |        90.26 | +9.74 / −90.26   | 0.11×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   15.09 |     3.24 |        -0.76 |
| GB / N         | NEG      |   84.91 |    -5.35 |        -9.35 |
| ST / Y         | WEAK     |   14.27 |     2.42 |        -1.58 |
| ST / N         | NEG      |   85.73 |    -4.53 |        -8.53 |
| MX / Y         | WEAK     |   15.41 |     3.56 |        -0.44 |
| MX / N         | NEG      |   84.59 |    -5.67 |        -9.67 |
| M10 / Y        | WEAK     |   15.13 |     3.29 |        -0.71 |
| M10 / N        | NEG      |   84.87 |    -5.40 |        -9.40 |

## Will the Republican Party candidate win the 2026 Texas Senate election by 6%-9%?
Contract 3344138; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        5.44 |         5.65 | +94.35 / −5.65   | 16.71×        |
| No     |       95.48 |        95.65 | +4.35 / −95.65   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    6.98 |     1.33 |        -2.67 |
| GB / N         | NEG      |   93.02 |    -2.63 |        -6.63 |
| ST / Y         | NEG      |    4.52 |    -1.12 |        -5.12 |
| ST / N         | NEG      |   95.47 |    -0.18 |        -4.18 |
| MX / Y         | WEAK     |    6.36 |     0.72 |        -3.28 |
| MX / N         | NEG      |   93.64 |    -2.02 |        -6.02 |
| M10 / Y        | WEAK     |    6.23 |     0.58 |        -3.42 |
| M10 / N        | NEG      |   93.77 |    -1.88 |        -5.88 |

## Will the Republican Party candidate win the 2026 Texas Senate election by 9%-12%?
Contract 3344137; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       11.53 |        11.91 | +88.09 / −11.91  | 7.39×         |
| No     |       98.3  |        98.37 | +1.63 / −98.37   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    2.23 |    -9.68 |       -13.68 |
| GB / N         | NEG      |   97.77 |    -0.60 |        -4.60 |
| ST / Y         | NEG      |    0.90 |   -11.01 |       -13.91 |
| ST / N         | WEAK     |   99.10 |     0.73 |        -3.27 |
| MX / Y         | NEG      |    2.03 |    -9.88 |       -13.88 |
| MX / N         | NEG      |   97.97 |    -0.40 |        -4.40 |
| M10 / Y        | NEG      |    1.96 |    -9.95 |       -13.91 |
| M10 / N        | NEG      |   98.04 |    -0.33 |        -4.33 |

## Will the Republican Party candidate win the 2026 Virginia Senate election by 3% or more?
Contract 3344160; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        0.72 |         0.75 | +99.25 / −0.75   | 132.96×       |
| No     |       99.8  |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.55 |    -0.19 |        -2.75 |
| GB / N         | NEG      |   99.45 |    -0.36 |        -4.36 |
| ST / Y         | WEAK     |    1.01 |     0.26 |        -2.75 |
| ST / N         | NEG      |   98.99 |    -0.81 |        -4.81 |
| MX / Y         | WEAK     |    2.35 |     1.60 |        -2.40 |
| MX / N         | NEG      |   97.65 |    -2.16 |        -6.16 |
| M10 / Y        | WEAK     |    2.81 |     2.06 |        -1.94 |
| M10 / N        | NEG      |   97.19 |    -2.62 |        -6.62 |

## Will the Republican Party control the Senate after the 2026 Midterm elections?
Contract 562794; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          38 |        38.94 | +61.06 / −38.94  | 1.57×         |
| No     |          63 |        63.93 | +36.07 / −63.93  | 0.56×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   52.41 |    13.46 |         9.46 |
| GB / N         | NEG      |   47.59 |   -16.34 |       -20.34 |
| ST / Y         | GO       |   47.09 |     8.15 |         4.15 |
| ST / N         | NEG      |   52.91 |   -11.02 |       -15.02 |
| MX / Y         | WEAK     |   42.28 |     3.34 |        -0.66 |
| MX / N         | NEG      |   57.72 |    -6.22 |       -10.22 |
| M10 / Y        | GO       |   46.01 |     7.07 |         3.07 |
| M10 / N        | NEG      |   53.99 |    -9.95 |       -13.95 |

## Will the Republican Party hold 47 or fewer Senate seats after the 2026 midterm elections?
Contract 943819; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          38 |        38.94 | +61.06 / −38.94  | 1.57×         |
| No     |          63 |        63.93 | +36.07 / −63.93  | 0.56×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    7.90 |   -31.04 |       -35.04 |
| GB / N         | GO       |   92.10 |    28.16 |        24.16 |
| ST / Y         | NEG      |    8.10 |   -30.85 |       -34.85 |
| ST / N         | GO       |   91.90 |    27.97 |        23.97 |
| MX / Y         | NEG      |   16.70 |   -22.25 |       -26.25 |
| MX / N         | GO       |   83.30 |    19.37 |        15.37 |
| M10 / Y        | NEG      |   15.00 |   -23.94 |       -27.94 |
| M10 / N        | GO       |   85.00 |    21.07 |        17.07 |

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
| Yes    |       16    |        16.54 | +83.46 / −16.54  | 5.05×         |
| No     |       85.19 |        85.7  | +14.30 / −85.70  | 0.17×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   15.21 |    -1.32 |        -5.32 |
| GB / N         | NEG      |   84.79 |    -0.91 |        -4.91 |
| ST / Y         | WEAK     |   17.19 |     0.65 |        -3.35 |
| ST / N         | NEG      |   82.81 |    -2.88 |        -6.88 |
| MX / Y         | WEAK     |   17.89 |     1.36 |        -2.64 |
| MX / N         | NEG      |   82.11 |    -3.59 |        -7.59 |
| M10 / Y        | NEG      |   16.51 |    -0.03 |        -4.03 |
| M10 / N        | NEG      |   83.49 |    -2.20 |        -6.20 |

## Will the Republican Party hold exactly 49 Senate seats after the 2026 midterm elections?
Contract 943821; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          14 |        14.48 | +85.52 / −14.48  | 5.91×         |
| No     |          87 |        87.45 | +12.55 / −87.45  | 0.14×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   24.48 |    10.00 |         6.00 |
| GB / N         | NEG      |   75.52 |   -11.93 |       -15.93 |
| ST / Y         | GO       |   27.62 |    13.14 |         9.14 |
| ST / N         | NEG      |   72.38 |   -15.08 |       -19.08 |
| MX / Y         | GO       |   23.13 |     8.65 |         4.65 |
| MX / N         | NEG      |   76.87 |   -10.58 |       -14.58 |
| M10 / Y        | GO       |   22.48 |     8.00 |         4.00 |
| M10 / N        | NEG      |   77.52 |    -9.93 |       -13.93 |

## Will the Republican Party hold exactly 50 Senate seats after the 2026 midterm elections?
Contract 943822; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          11 |        11.39 | +88.61 / −11.39  | 7.78×         |
| No     |          90 |        90.36 | +9.64 / −90.36   | 0.11×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   25.11 |    13.72 |         9.72 |
| GB / N         | NEG      |   74.89 |   -15.47 |       -19.47 |
| ST / Y         | GO       |   25.59 |    14.20 |        10.20 |
| ST / N         | NEG      |   74.41 |   -15.95 |       -19.95 |
| MX / Y         | GO       |   20.84 |     9.44 |         5.44 |
| MX / N         | NEG      |   79.16 |   -11.20 |       -15.20 |
| M10 / Y        | GO       |   21.50 |    10.11 |         6.11 |
| M10 / N        | NEG      |   78.50 |   -11.86 |       -15.86 |

## Will the Republican Party hold exactly 51 Senate seats after the 2026 midterm elections?
Contract 943823; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           9 |         9.33 | +90.67 / −9.33   | 9.72×         |
| No     |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   16.70 |     7.37 |         3.37 |
| GB / N         | NEG      |   83.30 |    -8.99 |       -12.99 |
| ST / Y         | GO       |   14.57 |     5.24 |         1.24 |
| ST / N         | NEG      |   85.43 |    -6.87 |       -10.87 |
| MX / Y         | WEAK     |   13.04 |     3.71 |        -0.29 |
| MX / N         | NEG      |   86.96 |    -5.33 |        -9.33 |
| M10 / Y        | GO       |   14.36 |     5.03 |         1.03 |
| M10 / N        | NEG      |   85.64 |    -6.65 |       -10.65 |

## Will the Republican Party hold exactly 52 Senate seats after the 2026 midterm elections?
Contract 943824; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         6   |         6.23 | +93.77 / −6.23   | 15.06×        |
| No     |        94.9 |        95.09 | +4.91 / −95.09   | 0.05×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |    7.50 |     1.27 |        -2.73 |
| GB / N         | NEG      |   92.50 |    -2.59 |        -6.59 |
| ST / Y         | NEG      |    5.30 |    -0.93 |        -4.93 |
| ST / N         | NEG      |   94.70 |    -0.39 |        -4.39 |
| MX / Y         | NEG      |    5.84 |    -0.38 |        -4.38 |
| MX / N         | NEG      |   94.16 |    -0.94 |        -4.94 |
| M10 / Y        | WEAK     |    6.81 |     0.58 |        -3.42 |
| M10 / N        | NEG      |   93.19 |    -1.90 |        -5.90 |

## Will the Republican Party hold exactly 53 Senate seats after the 2026 midterm elections?
Contract 943825; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        4.6  |         4.78 | +95.22 / −4.78   | 19.94×        |
| No     |       98.46 |        98.52 | +1.48 / −98.52   | 0.02×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    2.44 |    -2.34 |        -6.34 |
| GB / N         | NEG      |   97.56 |    -0.96 |        -4.96 |
| ST / Y         | NEG      |    1.34 |    -3.43 |        -6.78 |
| ST / N         | WEAK     |   98.66 |     0.14 |        -3.86 |
| MX / Y         | NEG      |    1.94 |    -2.84 |        -6.78 |
| MX / N         | NEG      |   98.06 |    -0.45 |        -4.45 |
| M10 / Y        | NEG      |    2.48 |    -2.30 |        -6.30 |
| M10 / N        | NEG      |   97.52 |    -1.00 |        -5.00 |

## Will the Republican Party hold exactly 54 Senate seats after the 2026 midterm elections?
Contract 943826; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         2.5 |         2.6  | +97.40 / −2.60   | 37.50×        |
| No     |        98.5 |        98.56 | +1.44 / −98.56   | 0.01×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.57 |    -2.03 |        -4.60 |
| GB / N         | WEAK     |   99.43 |     0.87 |        -3.13 |
| ST / Y         | NEG      |    0.26 |    -2.34 |        -4.60 |
| ST / N         | WEAK     |   99.74 |     1.18 |        -2.82 |
| MX / Y         | NEG      |    0.52 |    -2.08 |        -4.60 |
| MX / N         | WEAK     |   99.48 |     0.92 |        -3.08 |
| M10 / Y        | NEG      |    0.70 |    -1.90 |        -4.60 |
| M10 / N        | WEAK     |   99.30 |     0.74 |        -3.26 |

## Will the Republican Party hold exactly 55 Senate seats after the 2026 midterm elections?
Contract 943827; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         1   |         1.04 | +98.96 / −1.04   | 95.19×        |
| No     |        99.8 |        99.81 | +0.19 / −99.81   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.08 |    -0.96 |        -3.04 |
| GB / N         | WEAK     |   99.92 |     0.11 |        -3.89 |
| ST / Y         | NEG      |    0.03 |    -1.01 |        -3.04 |
| ST / N         | WEAK     |   99.98 |     0.17 |        -3.83 |
| MX / Y         | NEG      |    0.10 |    -0.94 |        -3.04 |
| MX / N         | WEAK     |   99.90 |     0.09 |        -3.91 |
| M10 / Y        | NEG      |    0.14 |    -0.90 |        -3.04 |
| M10 / N        | WEAK     |   99.86 |     0.05 |        -3.95 |

## Will the Republican Party hold exactly 56 Senate seats after the 2026 midterm elections?
Contract 943828; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |         0.3 |         0.31 | +99.69 / −0.31   | 319.55×       |
| No     |        99.9 |        99.9  | +0.10 / −99.90   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.01 |    -0.30 |        -2.31 |
| GB / N         | WEAK     |   99.99 |     0.09 |        -3.91 |
| ST / Y         | NEG      |    0.00 |    -0.31 |        -2.31 |
| ST / N         | WEAK     |  100.00 |     0.09 |        -3.91 |
| MX / Y         | NEG      |    0.02 |    -0.30 |        -2.31 |
| MX / N         | WEAK     |   99.98 |     0.08 |        -3.92 |
| M10 / Y        | NEG      |    0.02 |    -0.29 |        -2.31 |
| M10 / N        | WEAK     |   99.98 |     0.07 |        -3.93 |

## Will the Republicans win the Alabama Senate race in 2026?
Contract 630628; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       99.32 |        99.34 | +0.66 / −99.34   | 0.01×         |
| No     |        4.96 |         5.15 | +94.85 / −5.15   | 18.41×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.96 |     0.62 |        -3.38 |
| GB / N         | NEG      |    0.04 |    -5.11 |        -7.15 |
| ST / Y         | WEAK     |   99.87 |     0.52 |        -3.48 |
| ST / N         | NEG      |    0.13 |    -5.02 |        -7.15 |
| MX / Y         | NEG      |   98.62 |    -0.72 |        -4.72 |
| MX / N         | NEG      |    1.38 |    -3.77 |        -7.15 |
| M10 / Y        | NEG      |   98.67 |    -0.67 |        -4.67 |
| M10 / N        | NEG      |    1.33 |    -3.82 |        -7.15 |

## Will the Republicans win the Arkansas Senate race in 2026?
Contract 630654; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       95.72 |        95.88 | +4.12 / −95.88   | 0.04×         |
| No     |        5.85 |         6.07 | +93.93 / −6.07   | 15.47×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.83 |     3.95 |        -0.05 |
| GB / N         | NEG      |    0.17 |    -5.90 |        -8.07 |
| ST / Y         | WEAK     |   99.12 |     3.23 |        -0.77 |
| ST / N         | NEG      |    0.88 |    -5.19 |        -8.07 |
| MX / Y         | NEG      |   93.71 |    -2.17 |        -6.17 |
| MX / N         | WEAK     |    6.29 |     0.22 |        -3.78 |
| M10 / Y        | NEG      |   94.45 |    -1.43 |        -5.43 |
| M10 / N        | NEG      |    5.55 |    -0.53 |        -4.53 |

## Will the Republicans win the Florida Senate race in 2026?
Contract 631045; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          92 |        92.29 | +7.71 / −92.29   | 0.08×         |
| No     |           9 |         9.33 | +90.67 / −9.33   | 9.72×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   82.15 |   -10.14 |       -14.14 |
| GB / N         | GO       |   17.85 |     8.52 |         4.52 |
| ST / Y         | NEG      |   87.58 |    -4.72 |        -8.72 |
| ST / N         | WEAK     |   12.42 |     3.09 |        -0.91 |
| MX / Y         | NEG      |   80.08 |   -12.22 |       -16.22 |
| MX / N         | GO       |   19.92 |    10.59 |         6.59 |
| M10 / Y        | NEG      |   82.01 |   -10.28 |       -14.28 |
| M10 / N        | GO       |   17.99 |     8.66 |         4.66 |

## Will the Republicans win the Iowa Senate race in 2026?
Contract 630734; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          54 |        54.99 | +45.01 / −54.99  | 0.82×         |
| No     |          47 |        48    | +52.00 / −48.00  | 1.08×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   66.48 |    11.49 |         7.49 |
| GB / N         | NEG      |   33.52 |   -14.48 |       -18.48 |
| ST / Y         | GO       |   69.16 |    14.16 |        10.16 |
| ST / N         | NEG      |   30.84 |   -17.15 |       -21.15 |
| MX / Y         | GO       |   65.19 |    10.19 |         6.19 |
| MX / N         | NEG      |   34.81 |   -13.18 |       -17.18 |
| M10 / Y        | GO       |   66.57 |    11.58 |         7.58 |
| M10 / N        | NEG      |   33.43 |   -14.57 |       -18.57 |

## Will the Republicans win the Kansas Senate race in 2026?
Contract 630747; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          70 |        70.84 | +29.16 / −70.84  | 0.41×         |
| No     |          31 |        31.86 | +68.14 / −31.86  | 2.14×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   93.59 |    22.75 |        18.75 |
| GB / N         | NEG      |    6.41 |   -25.44 |       -29.44 |
| ST / Y         | GO       |   93.52 |    22.68 |        18.68 |
| ST / N         | NEG      |    6.48 |   -25.37 |       -29.37 |
| MX / Y         | GO       |   92.24 |    21.40 |        17.40 |
| MX / N         | NEG      |    7.76 |   -24.09 |       -28.09 |
| M10 / Y        | GO       |   91.30 |    20.46 |        16.46 |
| M10 / N        | NEG      |    8.70 |   -23.15 |       -27.15 |

## Will the Republicans win the Kentucky Senate race in 2026?
Contract 630760; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       96.47 |        96.61 | +3.39 / −96.61   | 0.04×         |
| No     |        4.84 |         5.03 | +94.97 / −5.03   | 18.89×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   98.64 |     2.03 |        -1.97 |
| GB / N         | NEG      |    1.36 |    -3.67 |        -7.03 |
| ST / Y         | WEAK     |   99.02 |     2.41 |        -1.59 |
| ST / N         | NEG      |    0.98 |    -4.05 |        -7.03 |
| MX / Y         | WEAK     |   96.72 |     0.11 |        -3.89 |
| MX / N         | NEG      |    3.28 |    -1.75 |        -5.75 |
| M10 / Y        | WEAK     |   97.45 |     0.85 |        -3.15 |
| M10 / N        | NEG      |    2.55 |    -2.48 |        -6.48 |

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
| ST / Y         | NEG      |    0.01 |    -2.69 |        -4.70 |
| ST / N         | WEAK     |   99.99 |     1.03 |        -2.97 |
| MX / Y         | NEG      |    0.01 |    -2.69 |        -4.70 |
| MX / N         | WEAK     |   99.99 |     1.03 |        -2.97 |
| M10 / Y        | NEG      |    0.02 |    -2.68 |        -4.70 |
| M10 / N        | WEAK     |   99.98 |     1.03 |        -2.97 |

## Will the Republicans win the Michigan Senate race in 2026?
Contract 630806; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          29 |        29.82 | +70.18 / −29.82  | 2.35×         |
| No     |          72 |        72.81 | +27.19 / −72.81  | 0.37×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   19.17 |   -10.66 |       -14.66 |
| GB / N         | GO       |   80.83 |     8.03 |         4.03 |
| ST / Y         | NEG      |   13.88 |   -15.94 |       -19.94 |
| ST / N         | GO       |   86.12 |    13.31 |         9.31 |
| MX / Y         | NEG      |   18.58 |   -11.25 |       -15.25 |
| MX / N         | GO       |   81.42 |     8.62 |         4.62 |
| M10 / Y        | NEG      |   22.72 |    -7.11 |       -11.11 |
| M10 / N        | GO       |   77.28 |     4.48 |         0.48 |

## Will the Republicans win the Minnesota Senate race in 2026?
Contract 630819; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           8 |         8.29 | +91.71 / −8.29   | 11.06×        |
| No     |          93 |        93.26 | +6.74 / −93.26   | 0.07×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   12.10 |     3.80 |        -0.20 |
| GB / N         | NEG      |   87.90 |    -5.36 |        -9.36 |
| ST / Y         | WEAK     |    8.94 |     0.65 |        -3.35 |
| ST / N         | NEG      |   91.06 |    -2.20 |        -6.20 |
| MX / Y         | WEAK     |    9.32 |     1.03 |        -2.97 |
| MX / N         | NEG      |   90.68 |    -2.58 |        -6.58 |
| M10 / Y        | WEAK     |   10.32 |     2.02 |        -1.98 |
| M10 / N        | NEG      |   89.68 |    -3.58 |        -7.58 |

## Will the Republicans win the Mississippi Senate race in 2026?
Contract 631018; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          93 |        93.26 | +6.74 / −93.26   | 0.07×         |
| No     |           9 |         9.33 | +90.67 / −9.33   | 9.72×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   97.60 |     4.34 |         0.34 |
| GB / N         | NEG      |    2.40 |    -6.93 |       -10.93 |
| ST / Y         | GO       |   97.89 |     4.63 |         0.63 |
| ST / N         | NEG      |    2.11 |    -7.22 |       -11.22 |
| MX / Y         | WEAK     |   94.57 |     1.31 |        -2.69 |
| MX / N         | NEG      |    5.43 |    -3.90 |        -7.90 |
| M10 / Y        | WEAK     |   93.39 |     0.13 |        -3.87 |
| M10 / N        | NEG      |    6.61 |    -2.72 |        -6.72 |

## Will the Republicans win the New Hampshire Senate race in 2026?
Contract 630845; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          15 |        15.51 | +84.49 / −15.51  | 5.45×         |
| No     |          86 |        86.48 | +13.52 / −86.48  | 0.16×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    3.56 |   -11.95 |       -15.95 |
| GB / N         | GO       |   96.44 |     9.96 |         5.96 |
| ST / Y         | NEG      |    4.20 |   -11.31 |       -15.31 |
| ST / N         | GO       |   95.80 |     9.32 |         5.32 |
| MX / Y         | NEG      |   10.98 |    -4.53 |        -8.53 |
| MX / N         | WEAK     |   89.02 |     2.54 |        -1.46 |
| M10 / Y        | NEG      |    9.55 |    -5.96 |        -9.96 |
| M10 / N        | WEAK     |   90.45 |     3.97 |        -0.03 |

## Will the Republicans win the North Carolina Senate race in 2026?
Contract 630884; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |           7 |         7.26 | +92.74 / −7.26   | 12.77×        |
| No     |          94 |        94.23 | +5.77 / −94.23   | 0.06×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   17.24 |     9.98 |         5.98 |
| GB / N         | NEG      |   82.76 |   -11.47 |       -15.47 |
| ST / Y         | WEAK     |   11.21 |     3.95 |        -0.05 |
| ST / N         | NEG      |   88.79 |    -5.43 |        -9.43 |
| MX / Y         | GO       |   15.48 |     8.22 |         4.22 |
| MX / N         | NEG      |   84.52 |    -9.71 |       -13.71 |
| M10 / Y        | GO       |   15.19 |     7.93 |         3.93 |
| M10 / N        | NEG      |   84.81 |    -9.42 |       -13.42 |

## Will the Republicans win the Ohio Senate race in 2026?
Contract 631058; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          40 |        40.96 | +59.04 / −40.96  | 1.44×         |
| No     |          61 |        61.95 | +38.05 / −61.95  | 0.61×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |   31.06 |    -9.90 |       -13.90 |
| GB / N         | GO       |   68.94 |     6.99 |         2.99 |
| ST / Y         | NEG      |   25.26 |   -15.70 |       -19.70 |
| ST / N         | GO       |   74.74 |    12.79 |         8.79 |
| MX / Y         | NEG      |   31.60 |    -9.36 |       -13.36 |
| MX / N         | GO       |   68.40 |     6.44 |         2.44 |
| M10 / Y        | NEG      |   35.22 |    -5.74 |        -9.74 |
| M10 / N        | WEAK     |   64.78 |     2.83 |        -1.17 |

## Will the Republicans win the Oklahoma Senate race in 2026?
Contract 631031; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |       97.65 |        97.74 | +2.26 / −97.74   | 0.02×         |
| No     |        3.7  |         3.84 | +96.16 / −3.84   | 25.02×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.95 |     2.21 |        -1.79 |
| GB / N         | NEG      |    0.05 |    -3.79 |        -5.84 |
| ST / Y         | WEAK     |   99.62 |     1.88 |        -2.12 |
| ST / N         | NEG      |    0.38 |    -3.46 |        -5.84 |
| MX / Y         | WEAK     |   98.65 |     0.91 |        -3.09 |
| MX / N         | NEG      |    1.35 |    -2.49 |        -5.84 |
| M10 / Y        | WEAK     |   98.54 |     0.80 |        -3.20 |
| M10 / N        | NEG      |    1.46 |    -2.38 |        -5.84 |

## Will the Republicans win the Rhode Island Senate race in 2026?
Contract 630912; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.56 |         2.66 | +97.34 / −2.66   | 36.58×        |
| No     |       99.6  |        99.62 | +0.38 / −99.62   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    0.05 |    -2.61 |        -4.66 |
| GB / N         | WEAK     |   99.95 |     0.33 |        -3.67 |
| ST / Y         | NEG      |    0.21 |    -2.45 |        -4.66 |
| ST / N         | WEAK     |   99.79 |     0.18 |        -3.82 |
| MX / Y         | NEG      |    1.57 |    -1.09 |        -4.66 |
| MX / N         | NEG      |   98.43 |    -1.19 |        -5.19 |
| M10 / Y        | NEG      |    1.84 |    -0.82 |        -4.66 |
| M10 / N        | NEG      |   98.16 |    -1.46 |        -5.46 |

## Will the Republicans win the South Carolina Senate race in 2026?
Contract 630925; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          87 |        87.45 | +12.55 / −87.45  | 0.14×         |
| No     |          14 |        14.48 | +85.52 / −14.48  | 5.91×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   96.66 |     9.21 |         5.21 |
| GB / N         | NEG      |    3.34 |   -11.14 |       -15.14 |
| ST / Y         | GO       |   97.46 |    10.00 |         6.00 |
| ST / N         | NEG      |    2.54 |   -11.94 |       -15.94 |
| MX / Y         | GO       |   93.63 |     6.18 |         2.18 |
| MX / N         | NEG      |    6.37 |    -8.11 |       -12.11 |
| M10 / Y        | GO       |   94.34 |     6.89 |         2.89 |
| M10 / N        | NEG      |    5.66 |    -8.82 |       -12.82 |

## Will the Republicans win the Tennessee Senate race in 2026?
Contract 630951; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        97.2 |        97.31 | +2.69 / −97.31   | 0.03×         |
| No     |         3.8 |         3.95 | +96.05 / −3.95   | 24.34×        |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | WEAK     |   99.51 |     2.20 |        -1.80 |
| GB / N         | NEG      |    0.49 |    -3.46 |        -5.95 |
| ST / Y         | WEAK     |   98.90 |     1.59 |        -2.41 |
| ST / N         | NEG      |    1.10 |    -2.84 |        -5.95 |
| MX / Y         | NEG      |   97.25 |    -0.06 |        -4.06 |
| MX / N         | NEG      |    2.75 |    -1.19 |        -5.19 |
| M10 / Y        | NEG      |   97.16 |    -0.15 |        -4.15 |
| M10 / N        | NEG      |    2.84 |    -1.11 |        -5.11 |

## Will the Republicans win the Texas Senate race in 2026?
Contract 630964; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |          40 |        40.96 | +59.04 / −40.96  | 1.44×         |
| No     |          61 |        61.95 | +38.05 / −61.95  | 0.61×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | GO       |   47.49 |     6.53 |         2.53 |
| GB / N         | NEG      |   52.51 |    -9.44 |       -13.44 |
| ST / Y         | GO       |   46.31 |     5.35 |         1.35 |
| ST / N         | NEG      |   53.69 |    -8.26 |       -12.26 |
| MX / Y         | GO       |   48.81 |     7.85 |         3.85 |
| MX / N         | NEG      |   51.19 |   -10.76 |       -14.76 |
| M10 / Y        | GO       |   48.15 |     7.19 |         3.19 |
| M10 / N        | NEG      |   51.85 |   -10.10 |       -14.10 |

## Will the Republicans win the Virginia Senate race in 2026?
Contract 630977; 100 shares per position.

| Side   |   Entry (¢) |   Budget ($) | Win / lose ($)   | Reward/loss   |
|:-------|------------:|-------------:|:-----------------|:--------------|
| Yes    |        2.91 |         3.03 | +96.97 / −3.03   | 32.03×        |
| No     |       99.7  |        99.71 | +0.29 / −99.71   | 0.00×         |

| Model / side   | Status   |   P (%) |   EV ($) |   Stress ($) |
|:---------------|:---------|--------:|---------:|-------------:|
| GB / Y         | NEG      |    1.58 |    -1.44 |        -5.03 |
| GB / N         | NEG      |   98.42 |    -1.30 |        -5.30 |
| ST / Y         | NEG      |    1.86 |    -1.17 |        -5.03 |
| ST / N         | NEG      |   98.14 |    -1.57 |        -5.57 |
| MX / Y         | WEAK     |    4.18 |     1.15 |        -2.85 |
| MX / N         | NEG      |   95.82 |    -3.89 |        -7.89 |
| M10 / Y        | WEAK     |    4.95 |     1.92 |        -2.08 |
| M10 / N        | NEG      |   95.05 |    -4.66 |        -8.66 |

