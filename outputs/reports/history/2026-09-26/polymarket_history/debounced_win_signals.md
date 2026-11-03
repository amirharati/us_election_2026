# Debounced state-winner setups

One setup per model and state race, not per forecast day. Use one fixed representative regular-winner contract per state/cycle: Democratic-first if available, then lowest numeric market ID; selection never uses future price performance. Other compatible contracts are audited, not counted again. This groups equivalent party exposure rather than claiming cross-contract arbitrage.

Check daily at 00:00 UTC, starting September 2 (September 1 forecasts become available then), strictly before election-day midnight. Use the latest already-available forecast, at most 72 hours after its labelled forecast date, and the latest price strictly before the decision, at most 36 hours old. Retain original source dates: a carried publisher forecast is not a new forecast. Superseded publisher versions cannot be used. Apply identical timing rules to all models.

Enter when the selected side's probability-minus-price edge exceeds 2 cents. Keep one active setup until its edge is nonpositive on two consecutive valid daily checks with distinct price observations. Missing/stale forecasts or quotes break reset confirmation but do not close or rearm a setup. Opposite-side entry must wait until a later daily check after reset. Hitting a price target does not rearm the signal. Close the observation window at confirmed reset or the pre-election cutoff; never optimize its length from future prices.

For each nonoverlapping setup, report the raw maximum observed rise and the maximum rise sustained across three consecutive UTC calendar days (at least 36-hour span and gaps no greater than 36 hours), plus fresh endpoint change and worst observed change. Maxima are hindsight diagnostics, not achievable sale prices or realized profits. Return percentages divide price change by starting share price; edge coverage divides it by initial model edge. Primary mean/median maxima use fully observed windows only (at least three possible subsequent days, 80% daily coverage, and a valid endpoint within 36 hours). Partial-path witnessed hits remain separate; absent evidence is unknown, not failure. Targets are 5/10/20/50% of entry price with a 2-cent floor, or the larger of initial edge and 2 cents. Daily path files save adjacent-day changes without filling missing days. Prices are research proxies, not executable quotes; no fees, order fills or position sizing are assumed. Different model coverage remains relevant; repeated races across models are not independent evidence.

## Model names

| Code   | Model                               |
|:-------|:------------------------------------|
| GB     | Gaussian Bayesian                   |
| ST     | Matched Student-t                   |
| OG     | Older Gaussian                      |
| OS     | Older Student-t                     |
| MX     | Four-model mixture                  |
| M10    | Mixture with 10% polling mean shift |
| 538    | 538 Deluxe                          |
| 538C   | 538 Classic                         |
| 538L   | 538 Lite                            |
| ECON   | Economist original                  |
| RTWH   | Race to the WH                      |
| DDHQ0  | DDHQ original                       |
| DDHQ   | DDHQ revised                        |

The Observed table includes every setup with a qualifying three-day sequence, even if the rest of its path is incomplete. Its maximum is a lower bound on the unobserved full-path maximum, not a complete-path estimate. Other return summaries and percentage target rates use full paths. Partial witnessed hits are counted separately. Negative maximum sustained rises are retained: no qualifying three-day period beat the entry price. These figures are hindsight diagnostics, not trade returns.

## 2022: one setup until confirmed reset

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |       20 |       13 |            8 |                    1 |              11 |
| 538C    |       17 |       13 |            6 |                    1 |              10 |
| 538L    |       15 |       13 |            5 |                    1 |               9 |
| ECON    |        4 |        4 |            3 |                    0 |               1 |
| GB      |       13 |       11 |            2 |                    1 |              10 |
| M10     |       17 |       11 |            4 |                    0 |              13 |
| MX      |       18 |       11 |            6 |                    0 |              12 |
| OG      |       15 |       11 |            3 |                    2 |              10 |
| OS      |       15 |       11 |            5 |                    1 |               9 |
| ST      |       16 |       11 |            3 |                    0 |              13 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                     17 |                    1.54 |                      1.74 |
| 538C    |                     15 |                    3.18 |                      1.74 |
| 538L    |                     13 |                    2.35 |                      0.29 |
| ECON    |                      4 |                    0.36 |                      0.76 |
| GB      |                     11 |                    1.87 |                      0.29 |
| M10     |                     14 |                    0.85 |                      0.18 |
| MX      |                     15 |                    1.11 |                      0.07 |
| OG      |                     14 |                    2.54 |                      0.18 |
| OS      |                     15 |                    1.92 |                      0.87 |
| ST      |                     12 |                    1.19 |                      0.18 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| 538     |                     0.77 |                       0.29 |               -3.1  |                      0.04 |
| 538C    |                     4.13 |                       1.88 |               -7.69 |                      0.15 |
| 538L    |                     3.92 |                       1.88 |              -10.64 |                      0.11 |
| ECON    |                     4.24 |                       3.38 |              -18.2  |                      0.16 |
| GB      |                     0.13 |                       0.13 |              -12.13 |                      0.01 |
| M10     |                    -0.73 |                       0.13 |               -6.48 |                      0.01 |
| MX      |                     0.36 |                      -0.02 |               -1.84 |                     -0    |
| OG      |                     0.72 |                       0.29 |               -7.63 |                      0.02 |
| OS      |                     1.04 |                       0.29 |               -0.01 |                      0.05 |
| ST      |                     1.02 |                       0.29 |               -7.3  |                      0.02 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| 538     |       25    |         0    |         0    |         0    |          0    |
| 538C    |       50    |        33.33 |        16.67 |         0    |         16.67 |
| 538L    |       40    |        20    |        20    |         0    |         20    |
| ECON    |       66.67 |        33.33 |        33.33 |         0    |         33.33 |
| GB      |        0    |         0    |         0    |         0    |          0    |
| M10     |        0    |         0    |         0    |         0    |          0    |
| MX      |        0    |         0    |         0    |         0    |          0    |
| OG      |        0    |         0    |         0    |         0    |          0    |
| OS      |       20    |        20    |         0    |         0    |          0    |
| ST      |       33.33 |        33.33 |        33.33 |        33.33 |         33.33 |

Additional path diagnostics:

| model   |   mean_raw_max_cents |   mean_worst_cents |   median_sustained_return_pct |
|:--------|---------------------:|-------------------:|------------------------------:|
| 538     |                 4.51 |              -9.09 |                          0.34 |
| 538C    |                 5.91 |             -10.72 |                          2.75 |
| 538L    |                 4.86 |             -13.33 |                          2.75 |
| ECON    |                 7.31 |             -22.35 |                          5.03 |
| GB      |                 1.55 |             -15.88 |                          0.14 |
| M10     |                 3.17 |             -10.44 |                          0.14 |
| MX      |                 3.09 |              -6.61 |                         -0.05 |
| OG      |                 2.23 |             -10.89 |                          0.34 |
| OS      |                 5.46 |              -7.31 |                          0.39 |
| ST      |                 2.52 |             -10.03 |                          0.34 |

## 2024: one setup until confirmed reset

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |       38 |       25 |           35 |                    0 |               3 |
| GB      |       35 |       22 |           32 |                    0 |               3 |
| M10     |       31 |       23 |           30 |                    0 |               1 |
| MX      |       30 |       23 |           29 |                    0 |               1 |
| OG      |       34 |       23 |           32 |                    0 |               2 |
| OS      |       27 |       23 |           27 |                    0 |               0 |
| RTWH    |       24 |       22 |           24 |                    0 |               0 |
| ST      |       28 |       23 |           26 |                    0 |               2 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                     35 |                    3.59 |                      1.85 |
| GB      |                     32 |                    4.22 |                      0.9  |
| M10     |                     30 |                    2.81 |                      1.25 |
| MX      |                     29 |                    2.91 |                      1    |
| OG      |                     32 |                    4.04 |                      1.5  |
| OS      |                     27 |                    3.11 |                      1.5  |
| RTWH    |                     24 |                    1.64 |                      1    |
| ST      |                     26 |                    3.75 |                      1.62 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     3.59 |                       1.85 |                3.86 |                      0.55 |
| GB      |                     4.22 |                       0.9  |                4.46 |                      0.36 |
| M10     |                     2.81 |                       1.25 |                3.29 |                      0.32 |
| MX      |                     2.91 |                       1    |                2.73 |                      0.31 |
| OG      |                     4.04 |                       1.5  |                4.03 |                      0.41 |
| OS      |                     3.11 |                       1.5  |                2.09 |                      0.37 |
| RTWH    |                     1.64 |                       1    |               -0.99 |                      0.34 |
| ST      |                     3.75 |                       1.62 |                3.35 |                      0.51 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |       25.71 |        22.86 |        14.29 |         5.71 |         14.29 |
| GB      |       28.12 |        18.75 |        18.75 |         6.25 |         12.5  |
| M10     |       26.67 |        16.67 |        10    |         0    |         13.33 |
| MX      |       20.69 |        10.34 |        10.34 |         0    |         17.24 |
| OG      |       28.12 |        15.62 |        12.5  |         3.12 |         12.5  |
| OS      |       18.52 |        11.11 |         7.41 |         0    |          7.41 |
| RTWH    |       16.67 |         8.33 |         4.17 |         4.17 |          0    |
| ST      |       34.62 |        23.08 |        11.54 |         0    |          7.69 |

Additional path diagnostics:

| model   |   mean_raw_max_cents |   mean_worst_cents |   median_sustained_return_pct |
|:--------|---------------------:|-------------------:|------------------------------:|
| DDHQ    |                 5.55 |              -1.45 |                          2.88 |
| GB      |                 5.83 |              -1.83 |                          1.13 |
| M10     |                 4.82 |              -4.97 |                          1.93 |
| MX      |                 4.38 |              -5.69 |                          1.6  |
| OG      |                 5.29 |              -1.99 |                          2.76 |
| OS      |                 4.02 |              -6.34 |                          1.82 |
| RTWH    |                 3.24 |              -9.26 |                          1.86 |
| ST      |                 5.14 |              -5.9  |                          1.71 |

### 2022: states — AZ

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        1 |        1 |            1 |                    0 |               0 |
| 538C    |        1 |        1 |            1 |                    0 |               0 |
| 538L    |        1 |        1 |            1 |                    0 |               0 |
| ECON    |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      1 |                    3.47 |                      3.47 |
| 538C    |                      1 |                    3.47 |                      3.47 |
| 538L    |                      1 |                    3.47 |                      3.47 |
| ECON    |                      1 |                    3.38 |                      3.38 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| 538     |                     3.47 |                       3.47 |              -13.21 |                      0.44 |
| 538C    |                     3.47 |                       3.47 |              -13.21 |                      0.23 |
| 538L    |                     3.47 |                       3.47 |              -13.21 |                      0.17 |
| ECON    |                     3.38 |                       3.38 |              -13.29 |                      0.16 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| 538     |         100 |            0 |            0 |            0 |             0 |
| 538C    |         100 |            0 |            0 |            0 |             0 |
| 538L    |         100 |            0 |            0 |            0 |             0 |
| ECON    |         100 |            0 |            0 |            0 |             0 |

### 2022: states — CO

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        1 |        1 |            0 |                    0 |               1 |
| 538C    |        3 |        1 |            1 |                    0 |               2 |
| 538L    |        1 |        1 |            0 |                    0 |               1 |
| GB      |        1 |        1 |            0 |                    0 |               1 |
| M10     |        1 |        1 |            0 |                    0 |               1 |
| MX      |        1 |        1 |            0 |                    0 |               1 |
| OG      |        1 |        1 |            0 |                    0 |               1 |
| OS      |        1 |        1 |            0 |                    0 |               1 |
| ST      |        1 |        1 |            0 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      1 |                    7.19 |                      7.19 |
| 538C    |                      2 |                    7.7  |                      7.7  |
| 538L    |                      1 |                    7.19 |                      7.19 |
| GB      |                      1 |                    7.19 |                      7.19 |
| M10     |                      1 |                    7.19 |                      7.19 |
| MX      |                      1 |                    7.19 |                      7.19 |
| OG      |                      1 |                    7.19 |                      7.19 |
| OS      |                      1 |                    7.19 |                      7.19 |
| ST      |                      1 |                    7.19 |                      7.19 |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538     | —                        | —                          | —                   | —                         |
| 538C    | 9.52                     | 9.52                       | 9.96                | 0.76                      |
| 538L    | —                        | —                          | —                   | —                         |
| GB      | —                        | —                          | —                   | —                         |
| M10     | —                        | —                          | —                   | —                         |
| MX      | —                        | —                          | —                   | —                         |
| OG      | —                        | —                          | —                   | —                         |
| OS      | —                        | —                          | —                   | —                         |
| ST      | —                        | —                          | —                   | —                         |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538     | —           | —            | —            | —            | —             |
| 538C    | 100.0       | 100.0        | 0.0          | 0.0          | 0.0           |
| 538L    | —           | —            | —            | —            | —             |
| GB      | —           | —            | —            | —            | —             |
| M10     | —           | —            | —            | —            | —             |
| MX      | —           | —            | —            | —            | —             |
| OG      | —           | —            | —            | —            | —             |
| OS      | —           | —            | —            | —            | —             |
| ST      | —           | —            | —            | —            | —             |

### 2022: states — FL

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        2 |        1 |            0 |                    0 |               2 |
| 538C    |        1 |        1 |            0 |                    0 |               1 |
| 538L    |        1 |        1 |            0 |                    0 |               1 |
| GB      |        1 |        1 |            0 |                    0 |               1 |
| M10     |        1 |        1 |            0 |                    0 |               1 |
| MX      |        1 |        1 |            0 |                    0 |               1 |
| OG      |        1 |        1 |            0 |                    0 |               1 |
| OS      |        1 |        1 |            0 |                    0 |               1 |
| ST      |        1 |        1 |            0 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      1 |                   -8.31 |                     -8.31 |
| 538C    |                      1 |                   -0.15 |                     -0.15 |
| 538L    |                      1 |                   -0.15 |                     -0.15 |
| GB      |                      1 |                   -0.15 |                     -0.15 |
| M10     |                      1 |                   -0.15 |                     -0.15 |
| MX      |                      1 |                   -0.15 |                     -0.15 |
| OG      |                      1 |                   -0.15 |                     -0.15 |
| OS      |                      1 |                   -0.15 |                     -0.15 |
| ST      |                      1 |                   -0.15 |                     -0.15 |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538     | —                        | —                          | —                   | —                         |
| 538C    | —                        | —                          | —                   | —                         |
| 538L    | —                        | —                          | —                   | —                         |
| GB      | —                        | —                          | —                   | —                         |
| M10     | —                        | —                          | —                   | —                         |
| MX      | —                        | —                          | —                   | —                         |
| OG      | —                        | —                          | —                   | —                         |
| OS      | —                        | —                          | —                   | —                         |
| ST      | —                        | —                          | —                   | —                         |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538     | —           | —            | —            | —            | —             |
| 538C    | —           | —            | —            | —            | —             |
| 538L    | —           | —            | —            | —            | —             |
| GB      | —           | —            | —            | —            | —             |
| M10     | —           | —            | —            | —            | —             |
| MX      | —           | —            | —            | —            | —             |
| OG      | —           | —            | —            | —            | —             |
| OS      | —           | —            | —            | —            | —             |
| ST      | —           | —            | —            | —            | —             |

### 2022: states — GA

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        4 |        1 |            3 |                    1 |               0 |
| 538C    |        1 |        1 |            1 |                    0 |               0 |
| 538L    |        1 |        1 |            1 |                    0 |               0 |
| ECON    |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      4 |                    1.9  |                      1.84 |
| 538C    |                      1 |                   11.94 |                     11.94 |
| 538L    |                      1 |                   11.94 |                     11.94 |
| ECON    |                      1 |                   11.21 |                     11.21 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| 538     |                     0.67 |                       1.31 |                1.55 |                      0.25 |
| 538C    |                    11.94 |                      11.94 |              -15.86 |                      2.71 |
| 538L    |                    11.94 |                      11.94 |              -15.86 |                      1.07 |
| ECON    |                    11.21 |                      11.21 |              -16.59 |                      1.55 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| 538     |       33.33 |            0 |            0 |            0 |             0 |
| 538C    |      100    |          100 |          100 |            0 |           100 |
| 538L    |      100    |          100 |          100 |            0 |           100 |
| ECON    |      100    |          100 |          100 |            0 |           100 |

### 2022: states — IA

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        1 |        1 |            0 |                    0 |               1 |
| 538C    |        3 |        1 |            1 |                    0 |               2 |
| 538L    |        1 |        1 |            0 |                    0 |               1 |
| GB      |        1 |        1 |            0 |                    0 |               1 |
| M10     |        3 |        1 |            1 |                    0 |               2 |
| MX      |        3 |        1 |            1 |                    0 |               2 |
| OG      |        3 |        1 |            1 |                    0 |               2 |
| OS      |        1 |        1 |            0 |                    0 |               1 |
| ST      |        3 |        1 |            1 |                    0 |               2 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      1 |                    2.66 |                      2.66 |
| 538C    |                      2 |                   -1.01 |                     -1.01 |
| 538L    |                      1 |                   -0.05 |                     -0.05 |
| GB      |                      1 |                   -0.05 |                     -0.05 |
| M10     |                      2 |                    0.93 |                      0.93 |
| MX      |                      2 |                    0.93 |                      0.93 |
| OG      |                      2 |                    0.93 |                      0.93 |
| OS      |                      1 |                    2.28 |                      2.28 |
| ST      |                      2 |                    1.38 |                      1.38 |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538     | —                        | —                          | —                   | —                         |
| 538C    | -0.39                    | -0.39                      | -2.77               | -0.19                     |
| 538L    | —                        | —                          | —                   | —                         |
| GB      | —                        | —                          | —                   | —                         |
| M10     | 1.91                     | 1.91                       | 1.37                | 0.83                      |
| MX      | 1.91                     | 1.91                       | 1.37                | 0.79                      |
| OG      | 1.91                     | 1.91                       | 1.37                | 0.8                       |
| OS      | —                        | —                          | —                   | —                         |
| ST      | 2.81                     | 2.81                       | 2.35                | 1.07                      |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538     | —           | —            | —            | —            | —             |
| 538C    | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| 538L    | —           | —            | —            | —            | —             |
| GB      | —           | —            | —            | —            | —             |
| M10     | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| MX      | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| OG      | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| OS      | —           | —            | —            | —            | —             |
| ST      | 100.0       | 100.0        | 100.0        | 100.0        | 100.0         |

### 2022: states — NC

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        2 |        1 |            0 |                    0 |               2 |
| 538C    |        1 |        1 |            0 |                    1 |               0 |
| 538L    |        1 |        1 |            0 |                    1 |               0 |
| GB      |        3 |        1 |            0 |                    1 |               2 |
| M10     |        2 |        1 |            0 |                    0 |               2 |
| MX      |        2 |        1 |            0 |                    0 |               2 |
| OG      |        1 |        1 |            0 |                    1 |               0 |
| OS      |        1 |        1 |            0 |                    1 |               0 |
| ST      |        4 |        1 |            0 |                    0 |               4 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      1 |                    3.04 |                      3.04 |
| 538C    |                      1 |                    8.17 |                      8.17 |
| 538L    |                      1 |                    8.17 |                      8.17 |
| GB      |                      1 |                    3.04 |                      3.04 |
| M10     |                      2 |                    0.93 |                      0.93 |
| MX      |                      2 |                    0.93 |                      0.93 |
| OG      |                      1 |                   12.7  |                     12.7  |
| OS      |                      1 |                   12.7  |                     12.7  |
| ST      |                      1 |                   -6.02 |                     -6.02 |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538     | —                        | —                          | —                   | —                         |
| 538C    | —                        | —                          | —                   | —                         |
| 538L    | —                        | —                          | —                   | —                         |
| GB      | —                        | —                          | —                   | —                         |
| M10     | —                        | —                          | —                   | —                         |
| MX      | —                        | —                          | —                   | —                         |
| OG      | —                        | —                          | —                   | —                         |
| OS      | —                        | —                          | —                   | —                         |
| ST      | —                        | —                          | —                   | —                         |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538     | —           | —            | —            | —            | —             |
| 538C    | —           | —            | —            | —            | —             |
| 538L    | —           | —            | —            | —            | —             |
| GB      | —           | —            | —            | —            | —             |
| M10     | —           | —            | —            | —            | —             |
| MX      | —           | —            | —            | —            | —             |
| OG      | —           | —            | —            | —            | —             |
| OS      | —           | —            | —            | —            | —             |
| ST      | —           | —            | —            | —            | —             |

### 2022: states — NH

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        3 |        1 |            2 |                    0 |               1 |
| 538C    |        1 |        1 |            0 |                    0 |               1 |
| 538L    |        2 |        1 |            1 |                    0 |               1 |
| GB      |        1 |        1 |            0 |                    0 |               1 |
| M10     |        4 |        1 |            1 |                    0 |               3 |
| MX      |        5 |        1 |            3 |                    0 |               2 |
| OG      |        2 |        1 |            0 |                    1 |               1 |
| OS      |        5 |        1 |            3 |                    0 |               2 |
| ST      |        1 |        1 |            0 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      2 |                    2.94 |                      2.94 |
| 538C    |                      1 |                    6.21 |                      6.21 |
| 538L    |                      1 |                    2.03 |                      2.03 |
| GB      |                      1 |                    6.21 |                      6.21 |
| M10     |                      2 |                   -1.56 |                     -1.56 |
| MX      |                      3 |                    0.54 |                     -0.02 |
| OG      |                      2 |                    5.72 |                      5.72 |
| OS      |                      5 |                    0.5  |                      0.87 |
| ST      |                      1 |                    6.21 |                      6.21 |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538     | -0.34                    | -0.34                      | 4.03                | -0.05                     |
| 538C    | —                        | —                          | —                   | —                         |
| 538L    | —                        | —                          | 0.15                | —                         |
| GB      | —                        | —                          | —                   | —                         |
| M10     | -5.1                     | -5.1                       | -3.05               | -0.88                     |
| MX      | -0.18                    | -0.18                      | 3.96                | -0.02                     |
| OG      | —                        | —                          | —                   | —                         |
| OS      | 1.65                     | 0.87                       | 8.06                | 0.26                      |
| ST      | —                        | —                          | —                   | —                         |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538     | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| 538C    | —           | —            | —            | —            | —             |
| 538L    | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| GB      | —           | —            | —            | —            | —             |
| M10     | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| MX      | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| OG      | —           | —            | —            | —            | —             |
| OS      | 33.33       | 33.33        | 0.0          | 0.0          | 0.0           |
| ST      | —           | —            | —            | —            | —             |

### 2022: states — NV

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        1 |        1 |            0 |                    0 |               1 |
| 538C    |        1 |        1 |            0 |                    0 |               1 |
| 538L    |        1 |        1 |            0 |                    0 |               1 |
| ECON    |        1 |        1 |            0 |                    0 |               1 |
| GB      |        1 |        1 |            0 |                    0 |               1 |
| M10     |        1 |        1 |            0 |                    0 |               1 |
| MX      |        1 |        1 |            0 |                    0 |               1 |
| OG      |        1 |        1 |            0 |                    0 |               1 |
| OS      |        1 |        1 |            0 |                    0 |               1 |
| ST      |        1 |        1 |            0 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      1 |                    0.07 |                      0.07 |
| 538C    |                      1 |                    0.07 |                      0.07 |
| 538L    |                      1 |                    0.07 |                      0.07 |
| ECON    |                      1 |                  -11.29 |                    -11.29 |
| GB      |                      1 |                    0.07 |                      0.07 |
| M10     |                      1 |                    0.07 |                      0.07 |
| MX      |                      1 |                    0.07 |                      0.07 |
| OG      |                      1 |                    0.07 |                      0.07 |
| OS      |                      1 |                    0.07 |                      0.07 |
| ST      |                      1 |                    0.07 |                      0.07 |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538     | —                        | —                          | —                   | —                         |
| 538C    | —                        | —                          | —                   | —                         |
| 538L    | —                        | —                          | —                   | —                         |
| ECON    | —                        | —                          | —                   | —                         |
| GB      | —                        | —                          | —                   | —                         |
| M10     | —                        | —                          | —                   | —                         |
| MX      | —                        | —                          | —                   | —                         |
| OG      | —                        | —                          | —                   | —                         |
| OS      | —                        | —                          | —                   | —                         |
| ST      | —                        | —                          | —                   | —                         |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538     | —           | —            | —            | —            | —             |
| 538C    | —           | —            | —            | —            | —             |
| 538L    | —           | —            | —            | —            | —             |
| ECON    | —           | —            | —            | —            | —             |
| GB      | —           | —            | —            | —            | —             |
| M10     | —           | —            | —            | —            | —             |
| MX      | —           | —            | —            | —            | —             |
| OG      | —           | —            | —            | —            | —             |
| OS      | —           | —            | —            | —            | —             |
| ST      | —           | —            | —            | —            | —             |

### 2022: states — OH

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        1 |        1 |            0 |                    0 |               1 |
| 538C    |        1 |        1 |            0 |                    0 |               1 |
| 538L    |        1 |        1 |            0 |                    0 |               1 |
| GB      |        1 |        1 |            0 |                    0 |               1 |
| M10     |        1 |        1 |            0 |                    0 |               1 |
| MX      |        1 |        1 |            0 |                    0 |               1 |
| OG      |        1 |        1 |            0 |                    0 |               1 |
| OS      |        1 |        1 |            0 |                    0 |               1 |
| ST      |        1 |        1 |            0 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      1 |                    1.74 |                      1.74 |
| 538C    |                      1 |                    1.74 |                      1.74 |
| 538L    |                      1 |                    1.74 |                      1.74 |
| GB      |                      1 |                    1.74 |                      1.74 |
| M10     |                      1 |                    1.74 |                      1.74 |
| MX      |                      1 |                    1.74 |                      1.74 |
| OG      |                      1 |                    1.74 |                      1.74 |
| OS      |                      1 |                    1.74 |                      1.74 |
| ST      |                      1 |                    1.74 |                      1.74 |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538     | —                        | —                          | —                   | —                         |
| 538C    | —                        | —                          | —                   | —                         |
| 538L    | —                        | —                          | —                   | —                         |
| GB      | —                        | —                          | —                   | —                         |
| M10     | —                        | —                          | —                   | —                         |
| MX      | —                        | —                          | —                   | —                         |
| OG      | —                        | —                          | —                   | —                         |
| OS      | —                        | —                          | —                   | —                         |
| ST      | —                        | —                          | —                   | —                         |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538     | —           | —            | —            | —            | —             |
| 538C    | —           | —            | —            | —            | —             |
| 538L    | —           | —            | —            | —            | —             |
| GB      | —           | —            | —            | —            | —             |
| M10     | —           | —            | —            | —            | —             |
| MX      | —           | —            | —            | —            | —             |
| OG      | —           | —            | —            | —            | —             |
| OS      | —           | —            | —            | —            | —             |
| ST      | —           | —            | —            | —            | —             |

### 2022: states — PA

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        1 |        1 |            1 |                    0 |               0 |
| 538C    |        1 |        1 |            1 |                    0 |               0 |
| 538L    |        1 |        1 |            1 |                    0 |               0 |
| ECON    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      1 |                   -0.03 |                     -0.03 |
| 538C    |                      1 |                   -0.03 |                     -0.03 |
| 538L    |                      1 |                   -0.03 |                     -0.03 |
| ECON    |                      1 |                   -1.86 |                     -1.86 |
| GB      |                      1 |                   -0.03 |                     -0.03 |
| M10     |                      1 |                   -0.03 |                     -0.03 |
| MX      |                      1 |                   -0.03 |                     -0.03 |
| OG      |                      1 |                   -0.03 |                     -0.03 |
| OS      |                      1 |                   -0.03 |                     -0.03 |
| ST      |                      1 |                   -0.03 |                     -0.03 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| 538     |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| 538C    |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| 538L    |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| ECON    |                    -1.86 |                      -1.86 |              -24.72 |                     -0.09 |
| GB      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| M10     |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| MX      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| OG      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| OS      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| ST      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| 538     |           0 |            0 |            0 |            0 |             0 |
| 538C    |           0 |            0 |            0 |            0 |             0 |
| 538L    |           0 |            0 |            0 |            0 |             0 |
| ECON    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2022: states — VT

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        1 |        1 |            0 |                    0 |               1 |
| 538C    |        1 |        1 |            0 |                    0 |               1 |
| 538L    |        2 |        1 |            0 |                    0 |               2 |
| GB      |        1 |        1 |            0 |                    0 |               1 |
| M10     |        1 |        1 |            0 |                    0 |               1 |
| MX      |        1 |        1 |            0 |                    0 |               1 |
| OG      |        2 |        1 |            0 |                    0 |               2 |
| OS      |        1 |        1 |            0 |                    0 |               1 |
| ST      |        1 |        1 |            0 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      1 |                    4.03 |                      4.03 |
| 538C    |                      1 |                    4.03 |                      4.03 |
| 538L    |                      1 |                   -2.79 |                     -2.79 |
| GB      |                      1 |                    3.62 |                      3.62 |
| M10     |                      1 |                    3.62 |                      3.62 |
| MX      |                      1 |                    3.62 |                      3.62 |
| OG      |                      2 |                    0.94 |                      0.94 |
| OS      |                      1 |                    3.62 |                      3.62 |
| ST      |                      1 |                    3.62 |                      3.62 |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538     | —                        | —                          | —                   | —                         |
| 538C    | —                        | —                          | —                   | —                         |
| 538L    | —                        | —                          | —                   | —                         |
| GB      | —                        | —                          | —                   | —                         |
| M10     | —                        | —                          | —                   | —                         |
| MX      | —                        | —                          | —                   | —                         |
| OG      | —                        | —                          | —                   | —                         |
| OS      | —                        | —                          | —                   | —                         |
| ST      | —                        | —                          | —                   | —                         |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538     | —           | —            | —            | —            | —             |
| 538C    | —           | —            | —            | —            | —             |
| 538L    | —           | —            | —            | —            | —             |
| GB      | —           | —            | —            | —            | —             |
| M10     | —           | —            | —            | —            | —             |
| MX      | —           | —            | —            | —            | —             |
| OG      | —           | —            | —            | —            | —             |
| OS      | —           | —            | —            | —            | —             |
| ST      | —           | —            | —            | —            | —             |

### 2022: states — WA

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        1 |        1 |            1 |                    0 |               0 |
| 538C    |        1 |        1 |            1 |                    0 |               0 |
| 538L    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      1 |                    0.29 |                      0.29 |
| 538C    |                      1 |                    0.29 |                      0.29 |
| 538L    |                      1 |                    0.29 |                      0.29 |
| GB      |                      1 |                    0.29 |                      0.29 |
| M10     |                      1 |                    0.29 |                      0.29 |
| MX      |                      1 |                    0.29 |                      0.29 |
| OG      |                      1 |                    0.29 |                      0.29 |
| OS      |                      1 |                    0.29 |                      0.29 |
| ST      |                      1 |                    0.29 |                      0.29 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| 538     |                     0.29 |                       0.29 |                0.29 |                      0.04 |
| 538C    |                     0.29 |                       0.29 |                0.29 |                      0.06 |
| 538L    |                     0.29 |                       0.29 |                0.29 |                      0.05 |
| GB      |                     0.29 |                       0.29 |                0.29 |                      0.03 |
| M10     |                     0.29 |                       0.29 |                0.29 |                      0.03 |
| MX      |                     0.29 |                       0.29 |                0.29 |                      0.02 |
| OG      |                     0.29 |                       0.29 |                0.29 |                      0.02 |
| OS      |                     0.29 |                       0.29 |                0.29 |                      0.02 |
| ST      |                     0.29 |                       0.29 |                0.29 |                      0.02 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| 538     |           0 |            0 |            0 |            0 |             0 |
| 538C    |           0 |            0 |            0 |            0 |             0 |
| 538L    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2022: states — WI

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        1 |        1 |            0 |                    0 |               1 |
| 538C    |        1 |        1 |            0 |                    0 |               1 |
| 538L    |        1 |        1 |            0 |                    0 |               1 |
| GB      |        1 |        1 |            0 |                    0 |               1 |
| M10     |        1 |        1 |            0 |                    0 |               1 |
| MX      |        1 |        1 |            0 |                    0 |               1 |
| OG      |        1 |        1 |            0 |                    0 |               1 |
| OS      |        1 |        1 |            0 |                    0 |               1 |
| ST      |        1 |        1 |            0 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      1 |                   -1.38 |                     -1.38 |
| 538C    |                      1 |                   -1.38 |                     -1.38 |
| 538L    |                      1 |                   -1.38 |                     -1.38 |
| GB      |                      1 |                   -1.38 |                     -1.38 |
| M10     |                      1 |                   -1.38 |                     -1.38 |
| MX      |                      1 |                   -1.38 |                     -1.38 |
| OG      |                      1 |                   -1.38 |                     -1.38 |
| OS      |                      1 |                   -1.38 |                     -1.38 |
| ST      |                      1 |                   -1.38 |                     -1.38 |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538     | —                        | —                          | —                   | —                         |
| 538C    | —                        | —                          | —                   | —                         |
| 538L    | —                        | —                          | —                   | —                         |
| GB      | —                        | —                          | —                   | —                         |
| M10     | —                        | —                          | —                   | —                         |
| MX      | —                        | —                          | —                   | —                         |
| OG      | —                        | —                          | —                   | —                         |
| OS      | —                        | —                          | —                   | —                         |
| ST      | —                        | —                          | —                   | —                         |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538     | —           | —            | —            | —            | —             |
| 538C    | —           | —            | —            | —            | —             |
| 538L    | —           | —            | —            | —            | —             |
| GB      | —           | —            | —            | —            | —             |
| M10     | —           | —            | —            | —            | —             |
| MX      | —           | —            | —            | —            | —             |
| OG      | —           | —            | —            | —            | —             |
| OS      | —           | —            | —            | —            | —             |
| ST      | —           | —            | —            | —            | —             |

### 2024: states — AZ

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        2 |        1 |            2 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      2 |                       0 |                         0 |
| RTWH    |                      1 |                       6 |                         6 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                        0 |                          0 |                -2.5 |                      0.01 |
| RTWH    |                        6 |                          6 |                -6   |                      0.77 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| RTWH    |         100 |            0 |            0 |            0 |             0 |

### 2024: states — CA

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                    1.45 |                      1.45 |
| GB      |                      1 |                    0.9  |                      0.9  |
| M10     |                      1 |                    0.9  |                      0.9  |
| MX      |                      1 |                    0.9  |                      0.9  |
| OG      |                      1 |                    0.9  |                      0.9  |
| OS      |                      1 |                    0.9  |                      0.9  |
| RTWH    |                      1 |                    1    |                      1    |
| ST      |                      1 |                    0.9  |                      0.9  |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     1.45 |                       1.45 |                1.4  |                      0.44 |
| GB      |                     0.9  |                       0.9  |                0.85 |                      0.31 |
| M10     |                     0.9  |                       0.9  |                0.85 |                      0.31 |
| MX      |                     0.9  |                       0.9  |                0.85 |                      0.31 |
| OG      |                     0.9  |                       0.9  |                0.85 |                      0.31 |
| OS      |                     0.9  |                       0.9  |                0.85 |                      0.31 |
| RTWH    |                     1    |                       1    |                0.95 |                      0.38 |
| ST      |                     0.9  |                       0.9  |                0.85 |                      0.31 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — CT

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                    1.85 |                      1.85 |
| GB      |                      1 |                    0.9  |                      0.9  |
| M10     |                      1 |                    2.25 |                      2.25 |
| MX      |                      1 |                    2.25 |                      2.25 |
| OG      |                      1 |                    2.25 |                      2.25 |
| OS      |                      1 |                    2.25 |                      2.25 |
| ST      |                      1 |                    0.9  |                      0.9  |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     1.85 |                       1.85 |                1.9  |                      0.67 |
| GB      |                     0.9  |                       0.9  |                0.95 |                      0.41 |
| M10     |                     2.25 |                       2.25 |                2.3  |                      1.06 |
| MX      |                     2.25 |                       2.25 |                2.3  |                      1.08 |
| OG      |                     2.25 |                       2.25 |                2.3  |                      0.76 |
| OS      |                     2.25 |                       2.25 |                2.3  |                      0.87 |
| ST      |                     0.9  |                       0.9  |                0.95 |                      0.37 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |           100 |
| MX      |           0 |            0 |            0 |            0 |           100 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — DE

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                    1.5  |                      1.5  |
| GB      |                      1 |                    1.75 |                      1.75 |
| M10     |                      1 |                    1.75 |                      1.75 |
| MX      |                      1 |                    1.75 |                      1.75 |
| OG      |                      1 |                    1.75 |                      1.75 |
| OS      |                      1 |                    1.75 |                      1.75 |
| ST      |                      1 |                    1.75 |                      1.75 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     1.5  |                       1.5  |                0.35 |                      0.69 |
| GB      |                     1.75 |                       1.75 |                0.6  |                      0.55 |
| M10     |                     1.75 |                       1.75 |                0.6  |                      0.6  |
| MX      |                     1.75 |                       1.75 |                0.6  |                      0.59 |
| OG      |                     1.75 |                       1.75 |                0.6  |                      0.53 |
| OS      |                     1.75 |                       1.75 |                0.6  |                      0.61 |
| ST      |                     1.75 |                       1.75 |                0.6  |                      0.63 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — FL

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        2 |        1 |            2 |                    0 |               0 |
| M10     |        2 |        1 |            2 |                    0 |               0 |
| MX      |        2 |        1 |            2 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        2 |        1 |            2 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        2 |        1 |            2 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                    2.5  |                      2.5  |
| GB      |                      2 |                   -1    |                     -1    |
| M10     |                      2 |                    2.25 |                      2.25 |
| MX      |                      2 |                    0.5  |                      0.5  |
| OG      |                      1 |                    2.5  |                      2.5  |
| OS      |                      2 |                    2.25 |                      2.25 |
| RTWH    |                      1 |                    3    |                      3    |
| ST      |                      2 |                    3.25 |                      3.25 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     2.5  |                       2.5  |                -6.5 |                      0.19 |
| GB      |                    -1    |                      -1    |                -2   |                     -0.33 |
| M10     |                     2.25 |                       2.25 |                 2.5 |                      0.44 |
| MX      |                     0.5  |                       0.5  |                 1.5 |                      0.12 |
| OG      |                     2.5  |                       2.5  |                -6.5 |                      1.19 |
| OS      |                     2.25 |                       2.25 |                 2.5 |                      0.48 |
| RTWH    |                     3    |                       3    |                -6   |                      0.2  |
| ST      |                     3.25 |                       3.25 |                 4.5 |                      0.29 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |         100 |          100 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |         100 |          100 |            0 |            0 |           100 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |         100 |          100 |            0 |            0 |             0 |
| ST      |          50 |            0 |            0 |            0 |             0 |

### 2024: states — IN

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                    1.35 |                      1.35 |
| M10     |                      1 |                    0    |                      0    |
| MX      |                      1 |                    0    |                      0    |
| OG      |                      1 |                    0.55 |                      0.55 |
| OS      |                      1 |                    0    |                      0    |
| RTWH    |                      1 |                    1.45 |                      1.45 |
| ST      |                      1 |                    1.3  |                      1.3  |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     1.35 |                       1.35 |               -0.75 |                      0.67 |
| M10     |                     0    |                       0    |                0    |                      0    |
| MX      |                     0    |                       0    |               -0.2  |                      0    |
| OG      |                     0.55 |                       0.55 |                0.75 |                      0.04 |
| OS      |                     0    |                       0    |               -0.4  |                      0    |
| RTWH    |                     1.45 |                       1.45 |                1.65 |                      0.29 |
| ST      |                     1.3  |                       1.3  |               -0.8  |                      0.64 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — MA

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                    0.15 |                      0.15 |
| GB      |                      1 |                   -0.25 |                     -0.25 |
| M10     |                      1 |                    0.15 |                      0.15 |
| MX      |                      1 |                    0.15 |                      0.15 |
| OG      |                      1 |                    0.15 |                      0.15 |
| OS      |                      1 |                    0.15 |                      0.15 |
| RTWH    |                      1 |                    0.4  |                      0.4  |
| ST      |                      1 |                    0.15 |                      0.15 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     0.15 |                       0.15 |                0.45 |                      0.06 |
| GB      |                    -0.25 |                      -0.25 |                0.05 |                     -0.12 |
| M10     |                     0.15 |                       0.15 |                0.45 |                      0.06 |
| MX      |                     0.15 |                       0.15 |                0.45 |                      0.06 |
| OG      |                     0.15 |                       0.15 |                0.45 |                      0.07 |
| OS      |                     0.15 |                       0.15 |                0.45 |                      0.07 |
| RTWH    |                     0.4  |                       0.4  |                0.7  |                      0.18 |
| ST      |                     0.15 |                       0.15 |                0.45 |                      0.06 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — MD

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        2 |        1 |            2 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                     6   |                       6   |
| GB      |                      1 |                     6   |                       6   |
| M10     |                      1 |                     6   |                       6   |
| MX      |                      1 |                     6   |                       6   |
| OG      |                      1 |                     6   |                       6   |
| OS      |                      1 |                     6   |                       6   |
| RTWH    |                      2 |                     0.5 |                       0.5 |
| ST      |                      1 |                     6   |                       6   |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                      6   |                        6   |                7.5  |                      0.44 |
| GB      |                      6   |                        6   |                7.5  |                      0.42 |
| M10     |                      6   |                        6   |                7.5  |                      0.55 |
| MX      |                      6   |                        6   |                7.5  |                      0.48 |
| OG      |                      6   |                        6   |                7.5  |                      0.42 |
| OS      |                      6   |                        6   |                7.5  |                      0.55 |
| RTWH    |                      0.5 |                        0.5 |               -1.25 |                      0.2  |
| ST      |                      6   |                        6   |                7.5  |                      0.56 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |         100 |            0 |            0 |            0 |             0 |
| GB      |         100 |            0 |            0 |            0 |             0 |
| M10     |         100 |            0 |            0 |            0 |             0 |
| MX      |         100 |            0 |            0 |            0 |             0 |
| OG      |         100 |            0 |            0 |            0 |             0 |
| OS      |         100 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |         100 |            0 |            0 |            0 |             0 |

### 2024: states — MI

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        2 |        1 |            2 |                    0 |               0 |
| GB      |        3 |        1 |            2 |                    0 |               1 |
| M10     |        3 |        1 |            3 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        2 |        1 |            2 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      2 |                   -0.5  |                     -0.5  |
| GB      |                      2 |                    1.25 |                      1.25 |
| M10     |                      3 |                    1.5  |                      2    |
| MX      |                      1 |                    2.5  |                      2.5  |
| OG      |                      2 |                    3.25 |                      3.25 |
| OS      |                      1 |                    2.5  |                      2.5  |
| RTWH    |                      1 |                    1.5  |                      1.5  |
| ST      |                      1 |                    2.5  |                      2.5  |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                    -0.5  |                      -0.5  |               -0.75 |                     -1.16 |
| GB      |                     1.25 |                       1.25 |                7    |                      0.6  |
| M10     |                     1.5  |                       2    |                4.33 |                      0.83 |
| MX      |                     2.5  |                       2.5  |                1    |                      0.59 |
| OG      |                     3.25 |                       3.25 |                3.5  |                      0.79 |
| OS      |                     2.5  |                       2.5  |                1    |                      0.25 |
| RTWH    |                     1.5  |                       1.5  |                0    |                      0.38 |
| ST      |                     2.5  |                       2.5  |                1    |                      0.45 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |       50    |        50    |           50 |            0 |            50 |
| GB      |       50    |        50    |           50 |            0 |            50 |
| M10     |       33.33 |        33.33 |            0 |            0 |             0 |
| MX      |        0    |         0    |            0 |            0 |             0 |
| OG      |       50    |         0    |            0 |            0 |             0 |
| OS      |        0    |         0    |            0 |            0 |             0 |
| RTWH    |        0    |         0    |            0 |            0 |             0 |
| ST      |        0    |         0    |            0 |            0 |             0 |

### 2024: states — MN

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        2 |        1 |            2 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                    2    |                      2    |
| GB      |                      1 |                    0.05 |                      0.05 |
| M10     |                      1 |                    0.05 |                      0.05 |
| MX      |                      1 |                    0.05 |                      0.05 |
| OG      |                      1 |                    0.05 |                      0.05 |
| OS      |                      1 |                    1.5  |                      1.5  |
| RTWH    |                      2 |                    1.67 |                      1.67 |
| ST      |                      1 |                    1.5  |                      1.5  |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     2    |                       2    |                1.9  |                      0.96 |
| GB      |                     0.05 |                       0.05 |               -1.75 |                      0.01 |
| M10     |                     0.05 |                       0.05 |                0.1  |                      0.02 |
| MX      |                     0.05 |                       0.05 |                0.1  |                      0.02 |
| OG      |                     0.05 |                       0.05 |               -1.75 |                      0.01 |
| OS      |                     1.5  |                       1.5  |                1.5  |                      0.61 |
| RTWH    |                     1.67 |                       1.67 |                0.75 |                      0.48 |
| ST      |                     1.5  |                       1.5  |                1.5  |                      0.58 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — MO

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                    1.65 |                      1.65 |
| GB      |                      1 |                   -0.45 |                     -0.45 |
| M10     |                      1 |                   -0.45 |                     -0.45 |
| MX      |                      1 |                   -0.45 |                     -0.45 |
| OG      |                      1 |                   -0.45 |                     -0.45 |
| OS      |                      1 |                   -0.45 |                     -0.45 |
| RTWH    |                      1 |                    0.55 |                      0.55 |
| ST      |                      1 |                   -0.45 |                     -0.45 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     1.65 |                       1.65 |                2.35 |                      0.47 |
| GB      |                    -0.45 |                      -0.45 |                0.25 |                     -0.05 |
| M10     |                    -0.45 |                      -0.45 |                0.25 |                     -0.08 |
| MX      |                    -0.45 |                      -0.45 |                0.25 |                     -0.06 |
| OG      |                    -0.45 |                      -0.45 |                0.25 |                     -0.05 |
| OS      |                    -0.45 |                      -0.45 |                0.25 |                     -0.08 |
| RTWH    |                     0.55 |                       0.55 |                0.65 |                      0.26 |
| ST      |                    -0.45 |                      -0.45 |                0.25 |                     -0.08 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — MS

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                    2.35 |                      2.35 |
| GB      |                      1 |                    1.95 |                      1.95 |
| M10     |                      1 |                    2    |                      2    |
| MX      |                      1 |                    3.1  |                      3.1  |
| OG      |                      1 |                    2.5  |                      2.5  |
| OS      |                      1 |                    3.15 |                      3.15 |
| ST      |                      1 |                    2.15 |                      2.15 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     2.35 |                       2.35 |                2.85 |                      1    |
| GB      |                     1.95 |                       1.95 |                2.1  |                      0.96 |
| M10     |                     2    |                       2    |                2.1  |                      0.94 |
| MX      |                     3.1  |                       3.1  |                3.15 |                      1.54 |
| OG      |                     2.5  |                       2.5  |                2.55 |                      1.21 |
| OS      |                     3.15 |                       3.15 |                2.9  |                      1.5  |
| ST      |                     2.15 |                       2.15 |                2.2  |                      0.96 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |           100 |
| OG      |           0 |            0 |            0 |            0 |           100 |
| OS      |           0 |            0 |            0 |            0 |           100 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — MT

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        4 |        1 |            4 |                    0 |               0 |
| GB      |        5 |        1 |            5 |                    0 |               0 |
| M10     |        4 |        1 |            4 |                    0 |               0 |
| MX      |        4 |        1 |            4 |                    0 |               0 |
| OG      |        2 |        1 |            2 |                    0 |               0 |
| OS      |        4 |        1 |            4 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        3 |        1 |            2 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      4 |                    2.5  |                      1.25 |
| GB      |                      5 |                    0.9  |                      0.5  |
| M10     |                      4 |                    1.38 |                      0.5  |
| MX      |                      4 |                    0.75 |                      0.25 |
| OG      |                      2 |                    0    |                      0    |
| OS      |                      4 |                    0.5  |                      0.25 |
| RTWH    |                      1 |                    1    |                      1    |
| ST      |                      2 |                    9.25 |                      9.25 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     2.5  |                       1.25 |                3.37 |                      0.47 |
| GB      |                     0.9  |                       0.5  |                1.8  |                      0.1  |
| M10     |                     1.38 |                       0.5  |                5.5  |                      0.09 |
| MX      |                     0.75 |                       0.25 |                1.5  |                      0.05 |
| OG      |                     0    |                       0    |               -1.5  |                     -0.02 |
| OS      |                     0.5  |                       0.25 |                1.75 |                      0.06 |
| RTWH    |                     1    |                       1    |               -7.5  |                      0.06 |
| ST      |                     9.25 |                       9.25 |               11    |                      2.28 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |          25 |           25 |            0 |            0 |            50 |
| GB      |           0 |            0 |            0 |            0 |            20 |
| M10     |          25 |            0 |            0 |            0 |            25 |
| MX      |           0 |            0 |            0 |            0 |            25 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |         100 |          100 |            0 |            0 |            50 |

### 2024: states — ND

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                   -0.05 |                     -0.05 |
| GB      |                      1 |                   -0.05 |                     -0.05 |
| M10     |                      1 |                   -0.05 |                     -0.05 |
| MX      |                      1 |                   -0.05 |                     -0.05 |
| OG      |                      1 |                   -0.05 |                     -0.05 |
| OS      |                      1 |                   -0.05 |                     -0.05 |
| RTWH    |                      1 |                    0.7  |                      0.7  |
| ST      |                      1 |                   -0.05 |                     -0.05 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                    -0.05 |                      -0.05 |               -0.05 |                     -0.02 |
| GB      |                    -0.05 |                      -0.05 |               -0.05 |                     -0.02 |
| M10     |                    -0.05 |                      -0.05 |               -0.05 |                     -0.02 |
| MX      |                    -0.05 |                      -0.05 |               -0.05 |                     -0.02 |
| OG      |                    -0.05 |                      -0.05 |               -0.05 |                     -0.02 |
| OS      |                    -0.05 |                      -0.05 |               -0.05 |                     -0.02 |
| RTWH    |                     0.7  |                       0.7  |                1.35 |                      0.11 |
| ST      |                    -0.05 |                      -0.05 |               -0.05 |                     -0.02 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — NJ

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        2 |        1 |            1 |                    0 |               1 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                     4   |                       4   |
| GB      |                      1 |                     1.5 |                       1.5 |
| M10     |                      1 |                     1.5 |                       1.5 |
| MX      |                      1 |                     1.5 |                       1.5 |
| OG      |                      1 |                     1.5 |                       1.5 |
| OS      |                      1 |                     1.5 |                       1.5 |
| RTWH    |                      1 |                     2   |                       2   |
| ST      |                      1 |                     1.5 |                       1.5 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                      4   |                        4   |                 4   |                      0.65 |
| GB      |                      1.5 |                        1.5 |                 1.5 |                      0.42 |
| M10     |                      1.5 |                        1.5 |                 1.5 |                      0.3  |
| MX      |                      1.5 |                        1.5 |                 1.5 |                      0.3  |
| OG      |                      1.5 |                        1.5 |                 1.5 |                      0.25 |
| OS      |                      1.5 |                        1.5 |                 1.5 |                      0.26 |
| RTWH    |                      2   |                        2   |                 2   |                      0.57 |
| ST      |                      1.5 |                        1.5 |                 1.5 |                      0.32 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — NM

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        3 |        1 |            2 |                    0 |               1 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        3 |        1 |            2 |                    0 |               1 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                   47    |                     47    |
| GB      |                      2 |                   23.5  |                     23.5  |
| M10     |                      1 |                    1    |                      1    |
| MX      |                      1 |                    1    |                      1    |
| OG      |                      2 |                   23.25 |                     23.25 |
| OS      |                      1 |                    1    |                      1    |
| RTWH    |                      1 |                    1    |                      1    |
| ST      |                      1 |                    1    |                      1    |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                    47    |                      47    |               47.5  |                      1    |
| GB      |                    23.5  |                      23.5  |               23.75 |                      0.49 |
| M10     |                     1    |                       1    |                0.5  |                      0.34 |
| MX      |                     1    |                       1    |                0.5  |                      0.5  |
| OG      |                    23.25 |                      23.25 |               23.5  |                      0.49 |
| OS      |                     1    |                       1    |                0.5  |                      0.3  |
| RTWH    |                     1    |                       1    |                0.5  |                      0.43 |
| ST      |                     1    |                       1    |                0.5  |                      0.25 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |         100 |          100 |          100 |          100 |             0 |
| GB      |          50 |           50 |           50 |           50 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |          50 |           50 |           50 |           50 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — NV

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        3 |        1 |            2 |                    0 |               1 |
| GB      |        4 |        1 |            3 |                    0 |               1 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        2 |        1 |            2 |                    0 |               0 |
| OG      |        3 |        1 |            3 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      2 |                    0    |                      0    |
| GB      |                      3 |                    2.33 |                      3.5  |
| M10     |                      1 |                    9    |                      9    |
| MX      |                      2 |                    2.75 |                      2.75 |
| OG      |                      3 |                    0.83 |                      0.5  |
| OS      |                      1 |                    9    |                      9    |
| RTWH    |                      1 |                    6.5  |                      6.5  |
| ST      |                      1 |                    9    |                      9    |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     0    |                       0    |                2.75 |                      0.01 |
| GB      |                     2.33 |                       3.5  |                6.83 |                      0.7  |
| M10     |                     9    |                       9    |                3    |                      0.76 |
| MX      |                     2.75 |                       2.75 |                2    |                      0.33 |
| OG      |                     0.83 |                       0.5  |                3.67 |                      0.16 |
| OS      |                     9    |                       9    |                3    |                      0.71 |
| RTWH    |                     6.5  |                       6.5  |                0.5  |                      0.65 |
| ST      |                     9    |                       9    |                3    |                      0.74 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |        0    |         0    |         0    |            0 |             0 |
| GB      |       66.67 |        33.33 |        33.33 |            0 |             0 |
| M10     |      100    |       100    |         0    |            0 |             0 |
| MX      |       50    |         0    |         0    |            0 |             0 |
| OG      |       33.33 |         0    |         0    |            0 |             0 |
| OS      |      100    |       100    |         0    |            0 |             0 |
| RTWH    |      100    |         0    |         0    |            0 |             0 |
| ST      |      100    |       100    |         0    |            0 |             0 |

### 2024: states — NY

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                    2.1  |                      2.1  |
| GB      |                      1 |                    2.8  |                      2.8  |
| M10     |                      1 |                    2.8  |                      2.8  |
| MX      |                      1 |                    2.8  |                      2.8  |
| OG      |                      1 |                    2.8  |                      2.8  |
| OS      |                      1 |                    2.8  |                      2.8  |
| RTWH    |                      1 |                   -0.15 |                     -0.15 |
| ST      |                      1 |                    2.8  |                      2.8  |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     2.1  |                       2.1  |                1.55 |                      0.55 |
| GB      |                     2.8  |                       2.8  |                2.25 |                      0.61 |
| M10     |                     2.8  |                       2.8  |                2.25 |                      0.6  |
| MX      |                     2.8  |                       2.8  |                2.25 |                      0.6  |
| OG      |                     2.8  |                       2.8  |                2.25 |                      0.61 |
| OS      |                     2.8  |                       2.8  |                2.25 |                      0.59 |
| RTWH    |                    -0.15 |                      -0.15 |               -0.15 |                     -0.07 |
| ST      |                     2.8  |                       2.8  |                2.25 |                      0.59 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — OH

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                     1.5 |                       1.5 |
| GB      |                      1 |                    15   |                      15   |
| M10     |                      1 |                    15   |                      15   |
| MX      |                      1 |                    15   |                      15   |
| OG      |                      1 |                    15   |                      15   |
| OS      |                      1 |                    15   |                      15   |
| RTWH    |                      1 |                     1   |                       1   |
| ST      |                      1 |                    15   |                      15   |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                      1.5 |                        1.5 |                -2   |                      0.14 |
| GB      |                     15   |                       15   |                12.5 |                      1.93 |
| M10     |                     15   |                       15   |                12.5 |                      2.51 |
| MX      |                     15   |                       15   |                12.5 |                      2.55 |
| OG      |                     15   |                       15   |                12.5 |                      2.99 |
| OS      |                     15   |                       15   |                12.5 |                      3.47 |
| RTWH    |                      1   |                        1   |               -11   |                      0.07 |
| ST      |                     15   |                       15   |                12.5 |                      2.64 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |         100 |          100 |          100 |            0 |           100 |
| M10     |         100 |          100 |          100 |            0 |           100 |
| MX      |         100 |          100 |          100 |            0 |           100 |
| OG      |         100 |          100 |          100 |            0 |           100 |
| OS      |         100 |          100 |          100 |            0 |           100 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |         100 |          100 |          100 |            0 |           100 |

### 2024: states — PA

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        3 |        1 |            2 |                    0 |               1 |
| GB      |        2 |        1 |            2 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        3 |        1 |            3 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      2 |                     6   |                       6   |
| GB      |                      2 |                     0   |                       0   |
| M10     |                      1 |                     0.5 |                       0.5 |
| MX      |                      1 |                    -1   |                      -1   |
| OG      |                      3 |                     0.5 |                       1.5 |
| OS      |                      1 |                    -1   |                      -1   |
| RTWH    |                      1 |                     1.5 |                       1.5 |
| ST      |                      1 |                    -1   |                      -1   |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                      6   |                        6   |               11.5  |                      0.94 |
| GB      |                      0   |                        0   |               -1.75 |                      0.04 |
| M10     |                      0.5 |                        0.5 |               -7.5  |                      0.15 |
| MX      |                     -1   |                       -1   |               -9    |                     -0.43 |
| OG      |                      0.5 |                        1.5 |                0.67 |                      0.49 |
| OS      |                     -1   |                       -1   |               -9    |                     -0.22 |
| RTWH    |                      1.5 |                        1.5 |               -6.5  |                      0.6  |
| ST      |                     -1   |                       -1   |               -9    |                     -0.16 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |          50 |           50 |           50 |           50 |            50 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — RI

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                   23.45 |                     23.45 |
| GB      |                      1 |                   23.45 |                     23.45 |
| M10     |                      1 |                   23.45 |                     23.45 |
| MX      |                      1 |                   23.45 |                     23.45 |
| OG      |                      1 |                   23.45 |                     23.45 |
| OS      |                      1 |                   23.45 |                     23.45 |
| RTWH    |                      1 |                    0    |                      0    |
| ST      |                      1 |                   23.45 |                     23.45 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                    23.45 |                      23.45 |               23.9  |                      0.98 |
| GB      |                    23.45 |                      23.45 |               23.9  |                      0.94 |
| M10     |                    23.45 |                      23.45 |               23.9  |                      0.94 |
| MX      |                    23.45 |                      23.45 |               23.9  |                      0.94 |
| OG      |                    23.45 |                      23.45 |               23.9  |                      0.94 |
| OS      |                    23.45 |                      23.45 |               23.9  |                      0.94 |
| RTWH    |                     0    |                       0    |                2.95 |                      0    |
| ST      |                    23.45 |                      23.45 |               23.9  |                      0.94 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |         100 |          100 |          100 |            0 |             0 |
| GB      |         100 |          100 |          100 |            0 |             0 |
| M10     |         100 |          100 |          100 |            0 |             0 |
| MX      |         100 |          100 |          100 |            0 |             0 |
| OG      |         100 |          100 |          100 |            0 |             0 |
| OS      |         100 |          100 |          100 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |         100 |          100 |          100 |            0 |             0 |

### 2024: states — TX

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                     2.5 |                       2.5 |
| GB      |                      1 |                     5.5 |                       5.5 |
| M10     |                      1 |                     5.5 |                       5.5 |
| MX      |                      1 |                     5.5 |                       5.5 |
| OG      |                      1 |                     5.5 |                       5.5 |
| OS      |                      1 |                     5.5 |                       5.5 |
| RTWH    |                      1 |                     6.5 |                       6.5 |
| ST      |                      1 |                     5.5 |                       5.5 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                      2.5 |                        2.5 |                   1 |                      0.64 |
| GB      |                      5.5 |                        5.5 |                   0 |                      0.46 |
| M10     |                      5.5 |                        5.5 |                   0 |                      0.42 |
| MX      |                      5.5 |                        5.5 |                   0 |                      0.41 |
| OG      |                      5.5 |                        5.5 |                   0 |                      0.44 |
| OS      |                      5.5 |                        5.5 |                   0 |                      0.37 |
| RTWH    |                      6.5 |                        6.5 |                   5 |                      0.52 |
| ST      |                      5.5 |                        5.5 |                   0 |                      0.38 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |         100 |          100 |            0 |            0 |             0 |
| GB      |         100 |            0 |            0 |            0 |             0 |
| M10     |         100 |            0 |            0 |            0 |             0 |
| MX      |         100 |            0 |            0 |            0 |             0 |
| OG      |         100 |            0 |            0 |            0 |             0 |
| OS      |         100 |            0 |            0 |            0 |             0 |
| RTWH    |         100 |          100 |          100 |          100 |             0 |
| ST      |         100 |            0 |            0 |            0 |             0 |

### 2024: states — VA

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        2 |        1 |            2 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        2 |        1 |            2 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      2 |                   -0.25 |                     -0.25 |
| GB      |                      1 |                    0.5  |                      0.5  |
| M10     |                      1 |                    0.5  |                      0.5  |
| MX      |                      1 |                    1    |                      1    |
| OG      |                      2 |                   -0.75 |                     -0.75 |
| OS      |                      1 |                    1    |                      1    |
| RTWH    |                      1 |                    1    |                      1    |
| ST      |                      1 |                    0.5  |                      0.5  |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                    -0.25 |                      -0.25 |                0.25 |                     -0.22 |
| GB      |                     0.5  |                       0.5  |                1.5  |                      0.2  |
| M10     |                     0.5  |                       0.5  |                1.5  |                      0.18 |
| MX      |                     1    |                       1    |                1    |                      0.31 |
| OG      |                    -0.75 |                      -0.75 |                0    |                     -0.31 |
| OS      |                     1    |                       1    |                0.5  |                      0.4  |
| RTWH    |                     1    |                       1    |                0.5  |                      0.3  |
| ST      |                     0.5  |                       0.5  |                0    |                      0.16 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: states — WA

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      1 |                     1.9 |                       1.9 |
| RTWH    |                      1 |                     1.6 |                       1.6 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                      1.9 |                        1.9 |                 1.9 |                      0.7  |
| RTWH    |                      1.6 |                        1.6 |                 1.6 |                      0.49 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |

### 2024: states — WI

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        3 |        1 |            3 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        3 |        1 |            2 |                    0 |               1 |
| MX      |        3 |        1 |            2 |                    0 |               1 |
| OG      |        3 |        1 |            2 |                    0 |               1 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        3 |        1 |            2 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      3 |                    0.67 |                      3    |
| GB      |                      1 |                   16.5  |                     16.5  |
| M10     |                      2 |                   -1    |                     -1    |
| MX      |                      2 |                    4.75 |                      4.75 |
| OG      |                      2 |                    4.75 |                      4.75 |
| OS      |                      1 |                    1.5  |                      1.5  |
| RTWH    |                      1 |                   -1.5  |                     -1.5  |
| ST      |                      2 |                   -1    |                     -1    |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     0.67 |                       3    |                3.33 |                      0.66 |
| GB      |                    16.5  |                      16.5  |                7    |                      1.31 |
| M10     |                    -1    |                      -1    |                3.5  |                     -0.87 |
| MX      |                     4.75 |                       4.75 |                8.75 |                      0.84 |
| OG      |                     4.75 |                       4.75 |                9    |                      1.24 |
| OS      |                     1.5  |                       1.5  |               -7.5  |                      0.73 |
| RTWH    |                    -1.5  |                      -1.5  |               -4    |                     -0.5  |
| ST      |                    -1    |                      -1    |                3.5  |                     -1.24 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |       33.33 |        33.33 |        33.33 |            0 |         33.33 |
| GB      |      100    |       100    |       100    |          100 |        100    |
| M10     |       50    |        50    |        50    |            0 |         50    |
| MX      |       50    |        50    |        50    |            0 |         50    |
| OG      |       50    |        50    |        50    |            0 |         50    |
| OS      |        0    |         0    |         0    |            0 |          0    |
| RTWH    |        0    |         0    |         0    |            0 |          0    |
| ST      |       50    |        50    |        50    |            0 |          0    |

### 2022: probabilities — Competitive (30–70%)

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |       10 |        7 |            6 |                    1 |               3 |
| 538C    |        5 |        5 |            3 |                    0 |               2 |
| 538L    |        5 |        5 |            3 |                    0 |               2 |
| ECON    |        4 |        4 |            3 |                    0 |               1 |
| GB      |        5 |        4 |            1 |                    1 |               3 |
| M10     |        3 |        3 |            1 |                    0 |               2 |
| MX      |        4 |        4 |            2 |                    0 |               2 |
| OG      |        3 |        3 |            1 |                    0 |               2 |
| OS      |        4 |        4 |            2 |                    0 |               2 |
| ST      |        6 |        4 |            1 |                    0 |               5 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                     10 |                    1.24 |                      0.69 |
| 538C    |                      5 |                    2.81 |                      0.07 |
| 538L    |                      5 |                    2.81 |                      0.07 |
| ECON    |                      4 |                    0.36 |                      0.76 |
| GB      |                      4 |                    0.42 |                      0.02 |
| M10     |                      3 |                   -0.45 |                     -0.03 |
| MX      |                      4 |                   -0.42 |                     -0.19 |
| OG      |                      3 |                   -0.45 |                     -0.03 |
| OS      |                      4 |                   -0.27 |                      0.02 |
| ST      |                      4 |                   -1.84 |                     -0.71 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| 538     |                     0.85 |                       0.64 |               -5.18 |                      0.13 |
| 538C    |                     5.12 |                       3.47 |              -17.87 |                      0.23 |
| 538L    |                     5.12 |                       3.47 |              -17.87 |                      0.17 |
| ECON    |                     4.24 |                       3.38 |              -18.2  |                      0.16 |
| GB      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| M10     |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| MX      |                    -0.19 |                      -0.19 |              -11.25 |                     -0.02 |
| OG      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| OS      |                     0.11 |                       0.11 |              -10.95 |                      0.03 |
| ST      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| 538     |       33.33 |         0    |         0    |            0 |          0    |
| 538C    |       66.67 |        33.33 |        33.33 |            0 |         33.33 |
| 538L    |       66.67 |        33.33 |        33.33 |            0 |         33.33 |
| ECON    |       66.67 |        33.33 |        33.33 |            0 |         33.33 |
| GB      |        0    |         0    |         0    |            0 |          0    |
| M10     |        0    |         0    |         0    |            0 |          0    |
| MX      |        0    |         0    |         0    |            0 |          0    |
| OG      |        0    |         0    |         0    |            0 |          0    |
| OS      |        0    |         0    |         0    |            0 |          0    |
| ST      |        0    |         0    |         0    |            0 |          0    |

### 2022: probabilities — Favorite (70–90%)

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        4 |        3 |            2 |                    0 |               2 |
| 538C    |        4 |        3 |            2 |                    0 |               2 |
| 538L    |        3 |        3 |            1 |                    0 |               2 |
| GB      |        3 |        3 |            1 |                    0 |               2 |
| M10     |        6 |        4 |            2 |                    0 |               4 |
| MX      |        5 |        4 |            2 |                    0 |               3 |
| OG      |        3 |        3 |            1 |                    1 |               1 |
| OS      |        4 |        4 |            1 |                    1 |               2 |
| ST      |        3 |        3 |            1 |                    0 |               2 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      3 |                    4.56 |                      6.21 |
| 538C    |                      4 |                    5.47 |                      6.04 |
| 538L    |                      3 |                    3.17 |                      2.03 |
| GB      |                      3 |                    4.56 |                      6.21 |
| M10     |                      5 |                    1.8  |                      1.97 |
| MX      |                      4 |                    3.52 |                      3.3  |
| OG      |                      3 |                    6.73 |                      7.19 |
| OS      |                      4 |                    5.54 |                      4.58 |
| ST      |                      3 |                    4.56 |                      6.21 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| 538     |                     0.29 |                       0.29 |                3.15 |                      0.04 |
| 538C    |                     4.9  |                       4.9  |                5.13 |                      0.41 |
| 538L    |                     0.29 |                       0.29 |                0.29 |                      0.05 |
| GB      |                     0.29 |                       0.29 |                0.29 |                      0.03 |
| M10     |                    -2.41 |                      -2.41 |               -1.38 |                     -0.43 |
| MX      |                     0.29 |                       0.29 |                3.15 |                      0.02 |
| OG      |                     0.29 |                       0.29 |                0.29 |                      0.02 |
| OS      |                     0.29 |                       0.29 |                0.29 |                      0.02 |
| ST      |                     0.29 |                       0.29 |                0.29 |                      0.02 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| 538     |           0 |            0 |            0 |            0 |             0 |
| 538C    |          50 |           50 |            0 |            0 |             0 |
| 538L    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2022: probabilities — High probability (>=90%)

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        2 |        2 |            0 |                    0 |               2 |
| 538C    |        3 |        2 |            0 |                    0 |               3 |
| 538L    |        1 |        1 |            0 |                    0 |               1 |
| GB      |        1 |        1 |            0 |                    0 |               1 |
| M10     |        1 |        1 |            0 |                    0 |               1 |
| MX      |        1 |        1 |            0 |                    0 |               1 |
| OG      |        1 |        1 |            0 |                    0 |               1 |
| OS      |        2 |        2 |            0 |                    0 |               2 |
| ST      |        2 |        2 |            0 |                    0 |               2 |

| Model   |   Observed 3-day paths | Observed mean max (¢)   | Observed median max (¢)   |
|:--------|-----------------------:|:------------------------|:--------------------------|
| 538     |                      2 | 3.35                    | 3.35                      |
| 538C    |                      2 | 1.2                     | 1.2                       |
| 538L    |                      0 | —                       | —                         |
| GB      |                      1 | 3.62                    | 3.62                      |
| M10     |                      1 | 3.62                    | 3.62                      |
| MX      |                      1 | 3.62                    | 3.62                      |
| OG      |                      1 | 1.92                    | 1.92                      |
| OS      |                      2 | 2.95                    | 2.95                      |
| ST      |                      1 | 3.62                    | 3.62                      |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538     | —                        | —                          | —                   | —                         |
| 538C    | —                        | —                          | —                   | —                         |
| 538L    | —                        | —                          | —                   | —                         |
| GB      | —                        | —                          | —                   | —                         |
| M10     | —                        | —                          | —                   | —                         |
| MX      | —                        | —                          | —                   | —                         |
| OG      | —                        | —                          | —                   | —                         |
| OS      | —                        | —                          | —                   | —                         |
| ST      | —                        | —                          | —                   | —                         |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538     | —           | —            | —            | —            | —             |
| 538C    | —           | —            | —            | —            | —             |
| 538L    | —           | —            | —            | —            | —             |
| GB      | —           | —            | —            | —            | —             |
| M10     | —           | —            | —            | —            | —             |
| MX      | —           | —            | —            | —            | —             |
| OG      | —           | —            | —            | —            | —             |
| OS      | —           | —            | —            | —            | —             |
| ST      | —           | —            | —            | —            | —             |

### 2022: probabilities — Long shot (<=10%)

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538C    |        1 |        1 |            1 |                    0 |               0 |
| 538L    |        2 |        2 |            0 |                    0 |               2 |
| GB      |        1 |        1 |            0 |                    0 |               1 |
| M10     |        3 |        1 |            1 |                    0 |               2 |
| MX      |        3 |        1 |            1 |                    0 |               2 |
| OG      |        4 |        2 |            1 |                    0 |               3 |
| ST      |        2 |        1 |            1 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538C    |                      1 |                   -0.39 |                     -0.39 |
| 538L    |                      2 |                   -1.42 |                     -1.42 |
| GB      |                      1 |                   -0.05 |                     -0.05 |
| M10     |                      2 |                    0.93 |                      0.93 |
| MX      |                      2 |                    0.93 |                      0.93 |
| OG      |                      3 |                    0.61 |                     -0.04 |
| ST      |                      2 |                    1.38 |                      1.38 |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538C    | -0.39                    | -0.39                      | -2.77               | -0.19                     |
| 538L    | —                        | —                          | —                   | —                         |
| GB      | —                        | —                          | —                   | —                         |
| M10     | 1.91                     | 1.91                       | 1.37                | 0.83                      |
| MX      | 1.91                     | 1.91                       | 1.37                | 0.79                      |
| OG      | 1.91                     | 1.91                       | 1.37                | 0.8                       |
| ST      | 2.81                     | 2.81                       | 2.35                | 1.07                      |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538C    | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| 538L    | —           | —            | —            | —            | —             |
| GB      | —           | —            | —            | —            | —             |
| M10     | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| MX      | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| OG      | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| ST      | 100.0       | 100.0        | 100.0        | 100.0        | 100.0         |

### 2022: probabilities — Underdog (10–30%)

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        4 |        3 |            0 |                    0 |               4 |
| 538C    |        4 |        4 |            0 |                    1 |               3 |
| 538L    |        4 |        4 |            1 |                    1 |               2 |
| GB      |        3 |        3 |            0 |                    0 |               3 |
| M10     |        4 |        4 |            0 |                    0 |               4 |
| MX      |        5 |        4 |            1 |                    0 |               4 |
| OG      |        4 |        3 |            0 |                    1 |               3 |
| OS      |        5 |        3 |            2 |                    0 |               3 |
| ST      |        3 |        3 |            0 |                    0 |               3 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      2 |                   -3.29 |                     -3.29 |
| 538C    |                      3 |                    3.25 |                      1.74 |
| 538L    |                      3 |                    3.25 |                      1.74 |
| GB      |                      2 |                    0.79 |                      0.79 |
| M10     |                      3 |                   -0.39 |                     -0.15 |
| MX      |                      4 |                   -0.3  |                     -0.09 |
| OG      |                      4 |                    3.26 |                      0.79 |
| OS      |                      5 |                    0.38 |                      0.87 |
| ST      |                      2 |                    0.79 |                      0.79 |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538     | —                        | —                          | —                   | —                         |
| 538C    | —                        | —                          | —                   | —                         |
| 538L    | —                        | —                          | 0.15                | —                         |
| GB      | —                        | —                          | —                   | —                         |
| M10     | —                        | —                          | —                   | —                         |
| MX      | -0.02                    | -0.02                      | 3.81                | -0.01                     |
| OG      | —                        | —                          | —                   | —                         |
| OS      | 2.34                     | 2.34                       | 10.77               | 0.44                      |
| ST      | —                        | —                          | —                   | —                         |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538     | —           | —            | —            | —            | —             |
| 538C    | —           | —            | —            | —            | —             |
| 538L    | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| GB      | —           | —            | —            | —            | —             |
| M10     | —           | —            | —            | —            | —             |
| MX      | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| OG      | —           | —            | —            | —            | —             |
| OS      | 50.0        | 50.0         | 0.0          | 0.0          | 0.0           |
| ST      | —           | —            | —            | —            | —             |

### 2024: probabilities — Competitive (30–70%)

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        8 |        7 |            7 |                    0 |               1 |
| GB      |        3 |        3 |            3 |                    0 |               0 |
| M10     |        4 |        3 |            3 |                    0 |               1 |
| MX      |        3 |        3 |            3 |                    0 |               0 |
| OG      |        3 |        3 |            3 |                    0 |               0 |
| OS      |        2 |        2 |            2 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        4 |        3 |            3 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      7 |                    6.14 |                      2    |
| GB      |                      3 |                   20.83 |                     15    |
| M10     |                      3 |                    2.33 |                      0.5  |
| MX      |                      3 |                    6.17 |                      3    |
| OG      |                      3 |                   21.5  |                     15    |
| OS      |                      2 |                    7.75 |                      7.75 |
| RTWH    |                      1 |                    1    |                      1    |
| ST      |                      3 |                    5.17 |                      9    |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     6.14 |                       2    |                6.43 |                      0.66 |
| GB      |                    20.83 |                      15    |               22.83 |                      0.98 |
| M10     |                     2.33 |                       0.5  |                4    |                      0.06 |
| MX      |                     6.17 |                       3    |                7.5  |                      0.45 |
| OG      |                    21.5  |                      15    |               20.5  |                      0.98 |
| OS      |                     7.75 |                       7.75 |               10.5  |                      1.8  |
| RTWH    |                     1    |                       1    |              -11    |                      0.07 |
| ST      |                     5.17 |                       9    |                4.67 |                      0.86 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |       28.57 |        28.57 |        14.29 |        14.29 |         14.29 |
| GB      |       66.67 |        66.67 |        66.67 |        33.33 |         33.33 |
| M10     |       33.33 |        33.33 |        33.33 |         0    |         33.33 |
| MX      |       33.33 |        33.33 |        33.33 |         0    |         33.33 |
| OG      |       66.67 |        66.67 |        66.67 |        33.33 |         33.33 |
| OS      |       50    |        50    |        50    |         0    |         50    |
| RTWH    |        0    |         0    |         0    |         0    |          0    |
| ST      |       66.67 |        66.67 |        33.33 |         0    |         33.33 |

### 2024: probabilities — Favorite (70–90%)

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        5 |        5 |            5 |                    0 |               0 |
| GB      |       11 |        8 |           11 |                    0 |               0 |
| M10     |        9 |        8 |            9 |                    0 |               0 |
| MX      |        9 |        8 |            9 |                    0 |               0 |
| OG      |        9 |        6 |            9 |                    0 |               0 |
| OS      |        9 |        9 |            9 |                    0 |               0 |
| RTWH    |        5 |        5 |            5 |                    0 |               0 |
| ST      |        9 |        8 |            8 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      5 |                    6.19 |                       3   |
| GB      |                     11 |                    3.81 |                       2.5 |
| M10     |                      9 |                    6.16 |                       4.5 |
| MX      |                      9 |                    5.05 |                       3   |
| OG      |                      9 |                    4.83 |                       4   |
| OS      |                      9 |                    5.99 |                       4   |
| RTWH    |                      5 |                    2.8  |                       1.5 |
| ST      |                      8 |                    7.74 |                       6.5 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     6.19 |                        3   |                6.58 |                      0.44 |
| GB      |                     3.81 |                        2.5 |                4.9  |                      0.42 |
| M10     |                     6.16 |                        4.5 |                5.1  |                      0.69 |
| MX      |                     5.05 |                        3   |                3.82 |                      0.48 |
| OG      |                     4.83 |                        4   |                5.27 |                      0.58 |
| OS      |                     5.99 |                        4   |                3.1  |                      0.71 |
| RTWH    |                     2.8  |                        1.5 |               -3.2  |                      0.6  |
| ST      |                     7.74 |                        6.5 |                5.74 |                      0.65 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |       40    |        20    |        20    |            0 |         20    |
| GB      |       36.36 |         9.09 |         9.09 |            0 |          9.09 |
| M10     |       55.56 |        22.22 |        11.11 |            0 |         11.11 |
| MX      |       44.44 |        11.11 |        11.11 |            0 |         11.11 |
| OG      |       55.56 |        11.11 |        11.11 |            0 |          0    |
| OS      |       44.44 |        22.22 |        11.11 |            0 |          0    |
| RTWH    |       40    |         0    |         0    |            0 |          0    |
| ST      |       75    |        37.5  |        12.5  |            0 |         12.5  |

### 2024: probabilities — High probability (>=90%)

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |       11 |       11 |           11 |                    0 |               0 |
| GB      |        9 |        9 |            9 |                    0 |               0 |
| M10     |       10 |       10 |           10 |                    0 |               0 |
| MX      |       10 |       10 |           10 |                    0 |               0 |
| OG      |        8 |        8 |            8 |                    0 |               0 |
| OS      |       11 |       11 |           11 |                    0 |               0 |
| RTWH    |        9 |        9 |            9 |                    0 |               0 |
| ST      |       12 |       12 |           12 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                     11 |                    1.69 |                      1.85 |
| GB      |                      9 |                    1.11 |                      0.9  |
| M10     |                     10 |                    1.28 |                      1.25 |
| MX      |                     10 |                    1.44 |                      1.25 |
| OG      |                      8 |                    1.47 |                      1.62 |
| OS      |                     11 |                    1.45 |                      1.5  |
| RTWH    |                      9 |                    1.07 |                      1    |
| ST      |                     12 |                    1.2  |                      1.15 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     1.69 |                       1.85 |                1.41 |                      0.67 |
| GB      |                     1.11 |                       0.9  |                1.08 |                      0.41 |
| M10     |                     1.28 |                       1.25 |                1.2  |                      0.32 |
| MX      |                     1.44 |                       1.25 |                1.26 |                      0.4  |
| OG      |                     1.47 |                       1.62 |                1.31 |                      0.42 |
| OS      |                     1.45 |                       1.5  |                1.21 |                      0.4  |
| RTWH    |                     1.07 |                       1    |                1.13 |                      0.4  |
| ST      |                     1.2  |                       1.15 |                0.83 |                      0.35 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |          0    |
| GB      |           0 |            0 |            0 |            0 |          0    |
| M10     |           0 |            0 |            0 |            0 |         10    |
| MX      |           0 |            0 |            0 |            0 |         20    |
| OG      |           0 |            0 |            0 |            0 |         12.5  |
| OS      |           0 |            0 |            0 |            0 |          9.09 |
| RTWH    |           0 |            0 |            0 |            0 |          0    |
| ST      |           0 |            0 |            0 |            0 |          0    |

### 2024: probabilities — Long shot (<=10%)

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        3 |        2 |            3 |                    0 |               0 |
| GB      |        4 |        3 |            3 |                    0 |               1 |
| M10     |        3 |        3 |            3 |                    0 |               0 |
| MX      |        3 |        3 |            3 |                    0 |               0 |
| OG      |        7 |        5 |            6 |                    0 |               1 |
| OS      |        2 |        2 |            2 |                    0 |               0 |
| RTWH    |        5 |        5 |            5 |                    0 |               0 |
| ST      |        2 |        2 |            2 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      3 |                    0.38 |                      1    |
| GB      |                      3 |                   -0.13 |                      0    |
| M10     |                      3 |                   -0.13 |                      0    |
| MX      |                      3 |                   -0.13 |                      0    |
| OG      |                      6 |                   -0.22 |                      0    |
| OS      |                      2 |                   -0.23 |                     -0.23 |
| RTWH    |                      5 |                    0.86 |                      0.7  |
| ST      |                      2 |                   -0.48 |                     -0.48 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     0.38 |                       1    |                0.95 |                      0.1  |
| GB      |                    -0.13 |                       0    |               -0.5  |                      0    |
| M10     |                    -0.13 |                       0    |                0.12 |                      0    |
| MX      |                    -0.13 |                       0    |                0.05 |                      0    |
| OG      |                    -0.22 |                       0    |               -0.12 |                      0    |
| OS      |                    -0.23 |                      -0.23 |               -0.08 |                     -0.04 |
| RTWH    |                     0.86 |                       0.7  |                1.31 |                      0.26 |
| ST      |                    -0.48 |                      -0.48 |                0.62 |                     -0.16 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: probabilities — Underdog (10–30%)

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |       11 |        8 |            9 |                    0 |               2 |
| GB      |        8 |        5 |            6 |                    0 |               2 |
| M10     |        5 |        4 |            5 |                    0 |               0 |
| MX      |        5 |        3 |            4 |                    0 |               1 |
| OG      |        7 |        5 |            6 |                    0 |               1 |
| OS      |        3 |        2 |            3 |                    0 |               0 |
| RTWH    |        4 |        4 |            4 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      9 |                    3.56 |                      2.5  |
| GB      |                      6 |                    3.5  |                      1.5  |
| M10     |                      5 |                    1.9  |                      0.5  |
| MX      |                      4 |                    1.62 |                      0.25 |
| OG      |                      6 |                    1.83 |                      1.25 |
| OS      |                      3 |                   -0.33 |                      0    |
| RTWH    |                      4 |                    2.63 |                      2    |
| ST      |                      1 |                    6.5  |                      6.5  |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     3.56 |                       2.5  |                4.33 |                      0.43 |
| GB      |                     3.5  |                       1.5  |                2    |                      0.32 |
| M10     |                     1.9  |                       0.5  |                5.7  |                      0.19 |
| MX      |                     1.62 |                       0.25 |                2.37 |                      0.06 |
| OG      |                     1.83 |                       1.25 |                1.75 |                      0.32 |
| OS      |                    -0.33 |                       0    |               -1.83 |                      0    |
| RTWH    |                     2.63 |                       2    |               -3.38 |                      0.13 |
| ST      |                     6.5  |                       6.5  |               16    |                      0.93 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |       55.56 |        55.56 |        33.33 |        11.11 |         33.33 |
| GB      |       50    |        50    |        50    |        16.67 |         33.33 |
| M10     |       40    |        40    |        20    |         0    |         20    |
| MX      |       25    |        25    |        25    |         0    |         25    |
| OG      |       33.33 |        33.33 |        16.67 |         0    |         33.33 |
| OS      |        0    |         0    |         0    |         0    |          0    |
| RTWH    |       50    |        50    |        25    |        25    |          0    |
| ST      |      100    |       100    |       100    |         0    |          0    |

### 2022: time — 14–30 days

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        2 |        2 |            1 |                    0 |               1 |
| 538C    |        2 |        2 |            1 |                    0 |               1 |
| M10     |        2 |        2 |            1 |                    0 |               1 |
| MX      |        2 |        2 |            2 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      2 |                   -4.99 |                     -4.99 |
| 538C    |                      1 |                   -0.39 |                     -0.39 |
| M10     |                      1 |                    1.91 |                      1.91 |
| MX      |                      2 |                    0.95 |                      0.95 |
| OG      |                      1 |                    1.91 |                      1.91 |
| OS      |                      1 |                    3.81 |                      3.81 |
| ST      |                      1 |                    2.81 |                      2.81 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| 538     |                    -1.67 |                      -1.67 |              -11.3  |                     -0.23 |
| 538C    |                    -0.39 |                      -0.39 |               -2.77 |                     -0.19 |
| M10     |                     1.91 |                       1.91 |                1.37 |                      0.83 |
| MX      |                     0.95 |                       0.95 |                2.59 |                      0.39 |
| OG      |                     1.91 |                       1.91 |                1.37 |                      0.8  |
| OS      |                     3.81 |                       3.81 |               11.32 |                      0.62 |
| ST      |                     2.81 |                       2.81 |                2.35 |                      1.07 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| 538     |           0 |            0 |            0 |            0 |             0 |
| 538C    |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |         100 |          100 |            0 |            0 |             0 |
| ST      |         100 |          100 |          100 |          100 |           100 |

### 2022: time — 7–14 days

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        2 |        2 |            2 |                    0 |               0 |
| 538C    |        2 |        2 |            2 |                    0 |               0 |
| 538L    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        3 |        3 |            2 |                    0 |               1 |
| MX      |        3 |        3 |            2 |                    0 |               1 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        2 |        2 |            2 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      1 |                    0.29 |                      0.29 |
| 538C    |                      2 |                    4.9  |                      4.9  |
| 538L    |                      1 |                    0.29 |                      0.29 |
| GB      |                      1 |                    0.29 |                      0.29 |
| M10     |                      3 |                   -2.53 |                     -2.77 |
| MX      |                      2 |                   -1.24 |                     -1.24 |
| OG      |                      1 |                    0.29 |                      0.29 |
| OS      |                      2 |                    0.58 |                      0.58 |
| ST      |                      1 |                    0.29 |                      0.29 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| 538     |                     0.29 |                       0.29 |                3.15 |                      0.04 |
| 538C    |                     4.9  |                       4.9  |                5.13 |                      0.41 |
| 538L    |                     0.29 |                       0.29 |                0.29 |                      0.05 |
| GB      |                     0.29 |                       0.29 |                0.29 |                      0.03 |
| M10     |                    -2.41 |                      -2.41 |               -1.38 |                     -0.43 |
| MX      |                     0.29 |                       0.29 |                3.15 |                      0.02 |
| OG      |                     0.29 |                       0.29 |                0.29 |                      0.02 |
| OS      |                     0.58 |                       0.58 |                5.26 |                      0.14 |
| ST      |                     0.29 |                       0.29 |                0.29 |                      0.02 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| 538     |           0 |            0 |            0 |            0 |             0 |
| 538C    |          50 |           50 |            0 |            0 |             0 |
| 538L    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2022: time — >30 days

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |       15 |       12 |            4 |                    1 |              10 |
| 538C    |       13 |       12 |            3 |                    1 |               9 |
| 538L    |       14 |       12 |            4 |                    1 |               9 |
| ECON    |        4 |        4 |            3 |                    0 |               1 |
| GB      |       12 |       10 |            1 |                    1 |              10 |
| M10     |       11 |       10 |            1 |                    0 |              10 |
| MX      |       11 |       10 |            1 |                    0 |              10 |
| OG      |       12 |       10 |            1 |                    2 |               9 |
| OS      |       11 |       10 |            1 |                    1 |               9 |
| ST      |       14 |       10 |            1 |                    0 |              13 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                     13 |                    2.79 |                      2.66 |
| 538C    |                     12 |                    3.19 |                      2.6  |
| 538L    |                     12 |                    2.52 |                      0.9  |
| ECON    |                      4 |                    0.36 |                      0.76 |
| GB      |                     10 |                    2.03 |                      0.9  |
| M10     |                     10 |                    1.76 |                      0.9  |
| MX      |                     10 |                    1.76 |                      0.9  |
| OG      |                     12 |                    2.78 |                      0.02 |
| OS      |                     11 |                    2.15 |                      1.74 |
| ST      |                     10 |                    1.12 |                      0.02 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| 538     |                     1.78 |                       1.84 |               -5.45 |                      0.35 |
| 538C    |                     5.12 |                       3.47 |              -17.87 |                      0.23 |
| 538L    |                     5.12 |                       3.47 |              -13.37 |                      0.17 |
| ECON    |                     4.24 |                       3.38 |              -18.2  |                      0.16 |
| GB      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| M10     |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| MX      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| OG      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| OS      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| ST      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| 538     |       50    |         0    |         0    |            0 |          0    |
| 538C    |       66.67 |        33.33 |        33.33 |            0 |         33.33 |
| 538L    |       50    |        25    |        25    |            0 |         25    |
| ECON    |       66.67 |        33.33 |        33.33 |            0 |         33.33 |
| GB      |        0    |         0    |         0    |            0 |          0    |
| M10     |        0    |         0    |         0    |            0 |          0    |
| MX      |        0    |         0    |         0    |            0 |          0    |
| OG      |        0    |         0    |         0    |            0 |          0    |
| OS      |        0    |         0    |         0    |            0 |          0    |
| ST      |        0    |         0    |         0    |            0 |          0    |

### 2022: time — ≤7 days

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            0 |                    0 |               1 |
| MX      |        2 |        2 |            1 |                    0 |               1 |
| OG      |        1 |        1 |            0 |                    0 |               1 |
| OS      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths | Observed mean max (¢)   | Observed median max (¢)   |
|:--------|-----------------------:|:------------------------|:--------------------------|
| 538     |                      1 | -0.34                   | -0.34                     |
| M10     |                      0 | —                       | —                         |
| MX      |                      1 | -0.34                   | -0.34                     |
| OG      |                      0 | —                       | —                         |
| OS      |                      1 | 0.26                    | 0.26                      |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538     | -0.34                    | -0.34                      | 2.05                | -0.05                     |
| M10     | —                        | —                          | —                   | —                         |
| MX      | -0.34                    | -0.34                      | 2.05                | -0.04                     |
| OG      | —                        | —                          | —                   | —                         |
| OS      | 0.26                     | 0.26                       | 2.65                | 0.05                      |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538     | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| M10     | —           | —            | —            | —            | —             |
| MX      | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| OG      | —           | —            | —            | —            | —             |
| OS      | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |

### 2024: time — 14–30 days

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        6 |        6 |            5 |                    0 |               1 |
| GB      |        7 |        7 |            7 |                    0 |               0 |
| M10     |        6 |        6 |            5 |                    0 |               1 |
| MX      |        5 |        5 |            5 |                    0 |               0 |
| OG      |        6 |        6 |            6 |                    0 |               0 |
| OS      |        2 |        2 |            2 |                    0 |               0 |
| RTWH    |        5 |        5 |            5 |                    0 |               0 |
| ST      |        3 |        3 |            2 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      5 |                   15.69 |                      3    |
| GB      |                      7 |                    9.56 |                      0.5  |
| M10     |                      5 |                    5.29 |                      0.5  |
| MX      |                      5 |                    5.59 |                      1    |
| OG      |                      6 |                   12.41 |                      3.5  |
| OS      |                      2 |                   11.98 |                     11.98 |
| RTWH    |                      5 |                    0.33 |                      0.7  |
| ST      |                      2 |                   12.8  |                     12.8  |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                    15.69 |                       3    |               16.68 |                      0.98 |
| GB      |                     9.56 |                       0.5  |               10.86 |                      0.2  |
| M10     |                     5.29 |                       0.5  |                6.1  |                      0.19 |
| MX      |                     5.59 |                       1    |                4.88 |                      0.31 |
| OG      |                    12.41 |                       3.5  |               12.23 |                      0.63 |
| OS      |                    11.98 |                      11.98 |               11.45 |                      0.57 |
| RTWH    |                     0.33 |                       0.7  |               -0.07 |                      0.11 |
| ST      |                    12.8  |                      12.8  |               13.05 |                      0.95 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |       40    |        40    |        40    |        20    |            20 |
| GB      |       28.57 |        28.57 |        28.57 |        14.29 |             0 |
| M10     |       20    |        20    |        20    |         0    |             0 |
| MX      |       20    |        20    |        20    |         0    |             0 |
| OG      |       50    |        33.33 |        33.33 |        16.67 |             0 |
| OS      |       50    |        50    |        50    |         0    |             0 |
| RTWH    |        0    |         0    |         0    |         0    |             0 |
| ST      |       50    |        50    |        50    |         0    |             0 |

### 2024: time — 7–14 days

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        4 |        4 |            4 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      4 |                     0.5 |                      -0.5 |
| GB      |                      1 |                    -1.5 |                      -1.5 |
| OG      |                      1 |                    -3   |                      -3   |
| OS      |                      1 |                     0   |                       0   |
| ST      |                      1 |                    -0.5 |                      -0.5 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                      0.5 |                       -0.5 |                0.12 |                     -0.17 |
| GB      |                     -1.5 |                       -1.5 |                3.5  |                     -0.67 |
| OG      |                     -3   |                       -3   |                1    |                     -1.49 |
| OS      |                      0   |                        0   |                1    |                      0    |
| ST      |                     -0.5 |                       -0.5 |                1    |                     -0.24 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: time — >30 days

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |       22 |       21 |           22 |                    0 |               0 |
| GB      |       23 |       18 |           23 |                    0 |               0 |
| M10     |       22 |       19 |           22 |                    0 |               0 |
| MX      |       23 |       20 |           23 |                    0 |               0 |
| OG      |       23 |       21 |           23 |                    0 |               0 |
| OS      |       22 |       20 |           22 |                    0 |               0 |
| RTWH    |       19 |       19 |           19 |                    0 |               0 |
| ST      |       20 |       19 |           20 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                     22 |                    2.97 |                      1.87 |
| GB      |                     23 |                    3.03 |                      1.5  |
| M10     |                     22 |                    3    |                      1.87 |
| MX      |                     23 |                    2.46 |                      1.5  |
| OG      |                     23 |                    2.59 |                      1.5  |
| OS      |                     22 |                    2.66 |                      1.62 |
| RTWH    |                     19 |                    1.99 |                      1.45 |
| ST      |                     20 |                    3.97 |                      2.12 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     2.97 |                       1.87 |                3.25 |                      0.59 |
| GB      |                     3.03 |                       1.5  |                2.75 |                      0.42 |
| M10     |                     3    |                       1.87 |                3.35 |                      0.48 |
| MX      |                     2.46 |                       1.5  |                2.38 |                      0.41 |
| OG      |                     2.59 |                       1.5  |                2.4  |                      0.44 |
| OS      |                     2.66 |                       1.62 |                1.42 |                      0.38 |
| RTWH    |                     1.99 |                       1.45 |               -1.23 |                      0.38 |
| ST      |                     3.97 |                       2.12 |                3.38 |                      0.51 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |       31.82 |        27.27 |        13.64 |         4.55 |         18.18 |
| GB      |       30.43 |        17.39 |        17.39 |         4.35 |         17.39 |
| M10     |       31.82 |        18.18 |         9.09 |         0    |         18.18 |
| MX      |       21.74 |         8.7  |         8.7  |         0    |         21.74 |
| OG      |       26.09 |        13.04 |         8.7  |         0    |         17.39 |
| OS      |       18.18 |         9.09 |         4.55 |         0    |          9.09 |
| RTWH    |       21.05 |        10.53 |         5.26 |         5.26 |          0    |
| ST      |       40    |        25    |        10    |         0    |         10    |

### 2024: time — ≤7 days

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        6 |        6 |            4 |                    0 |               2 |
| GB      |        4 |        4 |            1 |                    0 |               3 |
| M10     |        3 |        3 |            3 |                    0 |               0 |
| MX      |        2 |        2 |            1 |                    0 |               1 |
| OG      |        4 |        4 |            2 |                    0 |               2 |
| OS      |        2 |        2 |            2 |                    0 |               0 |
| ST      |        4 |        4 |            3 |                    0 |               1 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      4 |                   -5.01 |                     -5    |
| GB      |                      1 |                   -0.05 |                     -0.05 |
| M10     |                      3 |                   -2.68 |                     -0.05 |
| MX      |                      1 |                   -0.05 |                     -0.05 |
| OG      |                      2 |                   -0.78 |                     -0.78 |
| OS      |                      2 |                    0.72 |                      0.72 |
| ST      |                      3 |                   -2.35 |                     -0.05 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                    -5.01 |                      -5    |               -5.01 |                     -0.87 |
| GB      |                    -0.05 |                      -0.05 |               -0.05 |                     -0.02 |
| M10     |                    -2.68 |                      -0.05 |               -1.85 |                     -0.02 |
| MX      |                    -0.05 |                      -0.05 |               -0.05 |                     -0.02 |
| OG      |                    -0.78 |                      -0.78 |               -0.28 |                     -0.32 |
| OS      |                     0.72 |                       0.72 |                0.72 |                      0.3  |
| ST      |                    -2.35 |                      -0.05 |               -2.52 |                     -0.02 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2022: activity — 0

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        1 |        1 |            1 |                    0 |               0 |
| 538C    |        1 |        1 |            1 |                    0 |               0 |
| 538L    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      1 |                    0.29 |                      0.29 |
| 538C    |                      1 |                    0.29 |                      0.29 |
| 538L    |                      1 |                    0.29 |                      0.29 |
| GB      |                      1 |                    0.29 |                      0.29 |
| M10     |                      1 |                    0.29 |                      0.29 |
| MX      |                      1 |                    0.29 |                      0.29 |
| OG      |                      1 |                    0.29 |                      0.29 |
| OS      |                      1 |                    0.29 |                      0.29 |
| ST      |                      1 |                    0.29 |                      0.29 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| 538     |                     0.29 |                       0.29 |                0.29 |                      0.04 |
| 538C    |                     0.29 |                       0.29 |                0.29 |                      0.06 |
| 538L    |                     0.29 |                       0.29 |                0.29 |                      0.05 |
| GB      |                     0.29 |                       0.29 |                0.29 |                      0.03 |
| M10     |                     0.29 |                       0.29 |                0.29 |                      0.03 |
| MX      |                     0.29 |                       0.29 |                0.29 |                      0.02 |
| OG      |                     0.29 |                       0.29 |                0.29 |                      0.02 |
| OS      |                     0.29 |                       0.29 |                0.29 |                      0.02 |
| ST      |                     0.29 |                       0.29 |                0.29 |                      0.02 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| 538     |           0 |            0 |            0 |            0 |             0 |
| 538C    |           0 |            0 |            0 |            0 |             0 |
| 538L    |           0 |            0 |            0 |            0 |             0 |
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2022: activity — 100+

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538C    |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538C    |                      1 |                    9.52 |                      9.52 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| 538C    |                     9.52 |                       9.52 |                9.96 |                      0.76 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| 538C    |         100 |          100 |            0 |            0 |             0 |

### 2022: activity — 10–99

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |       12 |        7 |            7 |                    1 |               4 |
| 538C    |       10 |        9 |            4 |                    1 |               5 |
| 538L    |        9 |        8 |            4 |                    1 |               4 |
| ECON    |        1 |        1 |            1 |                    0 |               0 |
| GB      |        7 |        5 |            1 |                    1 |               5 |
| M10     |       10 |        7 |            2 |                    0 |               8 |
| MX      |       11 |        7 |            4 |                    0 |               7 |
| OG      |        7 |        7 |            1 |                    2 |               4 |
| OS      |        9 |        6 |            4 |                    1 |               4 |
| ST      |        7 |        5 |            1 |                    0 |               6 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                     10 |                    1.41 |                      1.52 |
| 538C    |                      8 |                    2.92 |                      0.85 |
| 538L    |                      8 |                    3.22 |                      1.88 |
| ECON    |                      1 |                   11.21 |                     11.21 |
| GB      |                      5 |                    0.64 |                     -0.03 |
| M10     |                      7 |                    0.24 |                     -0.03 |
| MX      |                      8 |                    0.8  |                     -0.03 |
| OG      |                      6 |                    4.76 |                      0.85 |
| OS      |                      9 |                    2.2  |                      0.87 |
| ST      |                      4 |                    0.04 |                     -0.09 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| 538     |                     0.85 |                       0.64 |               -3.58 |                      0.13 |
| 538C    |                     3.74 |                       1.72 |              -14.1  |                      0.12 |
| 538L    |                     5.12 |                       3.47 |              -13.37 |                      0.17 |
| ECON    |                    11.21 |                      11.21 |              -16.59 |                      1.55 |
| GB      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| M10     |                    -2.57 |                      -2.57 |              -13.8  |                     -0.44 |
| MX      |                    -0.13 |                      -0.03 |               -3.17 |                     -0.01 |
| OG      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |
| OS      |                     1.23 |                       0.56 |               -0.09 |                      0.16 |
| ST      |                    -0.03 |                      -0.03 |              -24.55 |                     -0    |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| 538     |       28.57 |            0 |            0 |            0 |             0 |
| 538C    |       50    |           25 |           25 |            0 |            25 |
| 538L    |       50    |           25 |           25 |            0 |            25 |
| ECON    |      100    |          100 |          100 |            0 |           100 |
| GB      |        0    |            0 |            0 |            0 |             0 |
| M10     |        0    |            0 |            0 |            0 |             0 |
| MX      |        0    |            0 |            0 |            0 |             0 |
| OG      |        0    |            0 |            0 |            0 |             0 |
| OS      |       25    |           25 |            0 |            0 |             0 |
| ST      |        0    |            0 |            0 |            0 |             0 |

### 2022: activity — 1–9

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| 538     |        7 |        6 |            0 |                    0 |               7 |
| 538C    |        5 |        5 |            0 |                    0 |               5 |
| 538L    |        5 |        4 |            0 |                    0 |               5 |
| ECON    |        3 |        3 |            2 |                    0 |               1 |
| GB      |        5 |        5 |            0 |                    0 |               5 |
| M10     |        6 |        5 |            1 |                    0 |               5 |
| MX      |        6 |        5 |            1 |                    0 |               5 |
| OG      |        7 |        5 |            1 |                    0 |               6 |
| OS      |        5 |        5 |            0 |                    0 |               5 |
| ST      |        8 |        6 |            1 |                    0 |               7 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| 538     |                      6 |                    1.98 |                      3.35 |
| 538C    |                      5 |                    2.91 |                      4.03 |
| 538L    |                      4 |                    1.11 |                      0.01 |
| ECON    |                      3 |                   -3.26 |                     -1.86 |
| GB      |                      5 |                    3.41 |                      3.62 |
| M10     |                      6 |                    1.66 |                      0.99 |
| MX      |                      6 |                    1.66 |                      0.99 |
| OG      |                      7 |                    0.97 |                      0.07 |
| OS      |                      5 |                    1.75 |                      2.28 |
| ST      |                      7 |                    1.98 |                      2.81 |

| Model   | Mean max sustained (¢)   | Median max sustained (¢)   | Mean endpoint (¢)   | Median edge covered (×)   |
|:--------|:-------------------------|:---------------------------|:--------------------|:--------------------------|
| 538     | —                        | —                          | —                   | —                         |
| 538C    | —                        | —                          | —                   | —                         |
| 538L    | —                        | —                          | —                   | —                         |
| ECON    | 0.76                     | 0.76                       | -19.0               | 0.04                      |
| GB      | —                        | —                          | —                   | —                         |
| M10     | 1.91                     | 1.91                       | 1.37                | 0.83                      |
| MX      | 1.91                     | 1.91                       | 1.37                | 0.79                      |
| OG      | 1.91                     | 1.91                       | 1.37                | 0.8                       |
| OS      | —                        | —                          | —                   | —                         |
| ST      | 2.81                     | 2.81                       | 2.35                | 1.07                      |

| Model   | 5% target   | 10% target   | 20% target   | 50% target   | Edge target   |
|:--------|:------------|:-------------|:-------------|:-------------|:--------------|
| 538     | —           | —            | —            | —            | —             |
| 538C    | —           | —            | —            | —            | —             |
| 538L    | —           | —            | —            | —            | —             |
| ECON    | 50.0        | 0.0          | 0.0          | 0.0          | 0.0           |
| GB      | —           | —            | —            | —            | —             |
| M10     | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| MX      | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| OG      | 0.0         | 0.0          | 0.0          | 0.0          | 0.0           |
| OS      | —           | —            | —            | —            | —             |
| ST      | 100.0       | 100.0        | 100.0        | 100.0        | 100.0         |

### 2024: activity — 0

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| GB      |        1 |        1 |            1 |                    0 |               0 |
| M10     |        2 |        2 |            2 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| GB      |                      1 |                    1.5  |                      1.5  |
| M10     |                      2 |                    1.25 |                      1.25 |
| MX      |                      1 |                    1.5  |                      1.5  |
| OG      |                      1 |                    1.5  |                      1.5  |
| OS      |                      1 |                    1.5  |                      1.5  |
| RTWH    |                      1 |                    2    |                      2    |
| ST      |                      1 |                    1.5  |                      1.5  |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| GB      |                     1.5  |                       1.5  |                 1.5 |                      0.42 |
| M10     |                     1.25 |                       1.25 |                 1   |                      0.32 |
| MX      |                     1.5  |                       1.5  |                 1.5 |                      0.3  |
| OG      |                     1.5  |                       1.5  |                 1.5 |                      0.25 |
| OS      |                     1.5  |                       1.5  |                 1.5 |                      0.26 |
| RTWH    |                     2    |                       2    |                 2   |                      0.57 |
| ST      |                     1.5  |                       1.5  |                 1.5 |                      0.32 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| GB      |           0 |            0 |            0 |            0 |             0 |
| M10     |           0 |            0 |            0 |            0 |             0 |
| MX      |           0 |            0 |            0 |            0 |             0 |
| OG      |           0 |            0 |            0 |            0 |             0 |
| OS      |           0 |            0 |            0 |            0 |             0 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |           0 |            0 |            0 |            0 |             0 |

### 2024: activity — 100+

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        6 |        5 |            5 |                    0 |               1 |
| GB      |        4 |        3 |            2 |                    0 |               2 |
| M10     |        1 |        1 |            1 |                    0 |               0 |
| MX      |        1 |        1 |            1 |                    0 |               0 |
| OG      |        1 |        1 |            1 |                    0 |               0 |
| OS      |        1 |        1 |            1 |                    0 |               0 |
| RTWH    |        1 |        1 |            1 |                    0 |               0 |
| ST      |        1 |        1 |            1 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      5 |                   -1.2  |                     -0.5  |
| GB      |                      2 |                    6.75 |                      6.75 |
| M10     |                      1 |                   15    |                     15    |
| MX      |                      1 |                   15    |                     15    |
| OG      |                      1 |                   15    |                     15    |
| OS      |                      1 |                   15    |                     15    |
| RTWH    |                      1 |                    1.6  |                      1.6  |
| ST      |                      1 |                   15    |                     15    |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                    -1.2  |                      -0.5  |               -2.3  |                     -0.2  |
| GB      |                     6.75 |                       6.75 |                8    |                      0.63 |
| M10     |                    15    |                      15    |               12.5  |                      2.51 |
| MX      |                    15    |                      15    |               12.5  |                      2.55 |
| OG      |                    15    |                      15    |               12.5  |                      2.99 |
| OS      |                    15    |                      15    |               12.5  |                      3.47 |
| RTWH    |                     1.6  |                       1.6  |               -0.05 |                      0.4  |
| ST      |                    15    |                      15    |               12.5  |                      2.64 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |           0 |            0 |            0 |            0 |             0 |
| GB      |          50 |           50 |           50 |            0 |            50 |
| M10     |         100 |          100 |          100 |            0 |           100 |
| MX      |         100 |          100 |          100 |            0 |           100 |
| OG      |         100 |          100 |          100 |            0 |           100 |
| OS      |         100 |          100 |          100 |            0 |           100 |
| RTWH    |           0 |            0 |            0 |            0 |             0 |
| ST      |         100 |          100 |          100 |            0 |           100 |

### 2024: activity — 10–99

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |       26 |       20 |           24 |                    0 |               2 |
| GB      |       23 |       15 |           22 |                    0 |               1 |
| M10     |       23 |       15 |           22 |                    0 |               1 |
| MX      |       20 |       14 |           19 |                    0 |               1 |
| OG      |       24 |       16 |           22 |                    0 |               2 |
| OS      |       17 |       13 |           17 |                    0 |               0 |
| RTWH    |       19 |       18 |           19 |                    0 |               0 |
| ST      |       20 |       15 |           18 |                    0 |               2 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                     24 |                    3.83 |                      1.92 |
| GB      |                     22 |                    4.06 |                      0.7  |
| M10     |                     22 |                    1.79 |                      0.7  |
| MX      |                     19 |                    2.1  |                      1    |
| OG      |                     22 |                    3.83 |                      1.87 |
| OS      |                     17 |                    2.29 |                      1.5  |
| RTWH    |                     19 |                    1.69 |                      1    |
| ST      |                     18 |                    2.96 |                      1.83 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     3.83 |                       1.92 |                4.28 |                      0.55 |
| GB      |                     4.06 |                       0.7  |                4.1  |                      0.28 |
| M10     |                     1.79 |                       0.7  |                2.6  |                      0.25 |
| MX      |                     2.1  |                       1    |                2.73 |                      0.31 |
| OG      |                     3.83 |                       1.87 |                3.9  |                      0.43 |
| OS      |                     2.29 |                       1.5  |                1.41 |                      0.37 |
| RTWH    |                     1.69 |                       1    |               -1.49 |                      0.26 |
| ST      |                     2.96 |                       1.83 |                3.03 |                      0.51 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |       29.17 |        25    |        12.5  |         4.17 |         16.67 |
| GB      |       27.27 |        13.64 |        13.64 |         9.09 |         13.64 |
| M10     |       27.27 |        13.64 |         4.55 |         0    |         13.64 |
| MX      |       21.05 |         5.26 |         5.26 |         0    |         21.05 |
| OG      |       31.82 |        13.64 |         9.09 |         4.55 |         13.64 |
| OS      |       17.65 |         5.88 |         0    |         0    |          5.88 |
| RTWH    |       21.05 |        10.53 |         5.26 |         5.26 |          0    |
| ST      |       38.89 |        22.22 |         5.56 |         0    |          5.56 |

### 2024: activity — 1–9

| Model   |   Setups |   States |   Full paths |   Partial hits (10%) |   Unknown (10%) |
|:--------|---------:|---------:|-------------:|---------------------:|----------------:|
| DDHQ    |        6 |        6 |            6 |                    0 |               0 |
| GB      |        7 |        7 |            7 |                    0 |               0 |
| M10     |        5 |        5 |            5 |                    0 |               0 |
| MX      |        8 |        8 |            8 |                    0 |               0 |
| OG      |        8 |        8 |            8 |                    0 |               0 |
| OS      |        8 |        8 |            8 |                    0 |               0 |
| RTWH    |        3 |        3 |            3 |                    0 |               0 |
| ST      |        6 |        6 |            6 |                    0 |               0 |

| Model   |   Observed 3-day paths |   Observed mean max (¢) |   Observed median max (¢) |
|:--------|-----------------------:|------------------------:|--------------------------:|
| DDHQ    |                      6 |                    6.63 |                      2    |
| GB      |                      7 |                    4.4  |                      1.75 |
| M10     |                      5 |                    5.51 |                      1.75 |
| MX      |                      8 |                    3.51 |                      0.75 |
| OG      |                      8 |                    3.58 |                      0.53 |
| OS      |                      8 |                    3.57 |                      1    |
| RTWH    |                      3 |                    1.2  |                      1    |
| ST      |                      6 |                    4.59 |                      1.37 |

| Model   |   Mean max sustained (¢) |   Median max sustained (¢) |   Mean endpoint (¢) |   Median edge covered (×) |
|:--------|-------------------------:|---------------------------:|--------------------:|--------------------------:|
| DDHQ    |                     6.63 |                       2    |                7.35 |                      0.69 |
| GB      |                     4.4  |                       1.75 |                5.01 |                      0.55 |
| M10     |                     5.51 |                       1.75 |                5.4  |                      0.6  |
| MX      |                     3.51 |                       0.75 |                1.66 |                      0.33 |
| OG      |                     3.58 |                       0.53 |                3.66 |                      0.1  |
| OS      |                     3.57 |                       1    |                2.33 |                      0.35 |
| RTWH    |                     1.2  |                       1    |                0.87 |                      0.43 |
| ST      |                     4.59 |                       1.37 |                3.08 |                      0.42 |

| Model   |   5% target |   10% target |   20% target |   50% target |   Edge target |
|:--------|------------:|-------------:|-------------:|-------------:|--------------:|
| DDHQ    |       33.33 |        33.33 |        33.33 |        16.67 |         16.67 |
| GB      |       28.57 |        28.57 |        28.57 |         0    |          0    |
| M10     |       20    |        20    |        20    |         0    |          0    |
| MX      |       12.5  |        12.5  |        12.5  |         0    |          0    |
| OG      |       12.5  |        12.5  |        12.5  |         0    |          0    |
| OS      |       12.5  |        12.5  |        12.5  |         0    |          0    |
| RTWH    |        0    |         0    |         0    |         0    |          0    |
| ST      |       16.67 |        16.67 |        16.67 |         0    |          0    |
