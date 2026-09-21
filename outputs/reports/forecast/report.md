# 2026 Senate forecast — 2026-09-21

[All outputs](../../README.md) · [HTML report](report.html) · [Supporting tables](../../results/forecast/live_reports/)

## At a glance

- **Democratic control: 45.5%** under the reference Gaussian model.
- **Expected Democratic seats: 50.3**; central 70% range: **49–52**.
- Predicted winners by mean margin: **51 D / 49 R**.
- Trained through **2024**. Live evidence updates predictions; trained parameters are fixed.

Margins are Democratic minus Republican percentage points. Positive margins favor Democrats. D control requires 51 seats; R control includes a 50–50 chamber under the retained vice-presidential tie-break assumption.

## Data freshness

| Source         | Status                                          | Last successful check            |
|:---------------|:------------------------------------------------|:---------------------------------|
| polls          | Recent successful check reused                  | 2026-09-21T01:30:21.133335+00:00 |
| fred           | STALE: source check failed; saved evidence used | Not recorded                     |
| michigan       | Recent successful check reused                  | 2026-09-21T01:30:21.672682+00:00 |
| ucsb           | Recent successful check reused                  | 2026-09-21T01:30:19.881029+00:00 |
| french         | Recent successful check reused                  | 2026-09-21T01:30:20.378348+00:00 |
| cboe           | Recent successful check reused                  | 2026-09-21T01:30:20.682464+00:00 |
| gpr            | Recent successful check reused                  | 2026-09-21T01:30:23.335887+00:00 |
| epu            | Recent successful check reused                  | 2026-09-21T01:30:22.308967+00:00 |
| infectious_emv | Recent successful check reused                  | 2026-09-21T01:30:22.306390+00:00 |

Political context is reviewed through **2026-09-17**. It is carried forward as an explicit assumption.

The forecast cutoff does not mean every source has observations through that date. Missing evidence is not replaced with a zero.

## Chamber forecast across models

| Model                     |   Expected D seats |   D control % |   R control % |   D seats: 70% low |   D seats: 70% high |
|:--------------------------|-------------------:|--------------:|--------------:|-------------------:|--------------------:|
| Bayesian                  |              50.32 |         45.52 |         54.48 |                 49 |                  52 |
| Corrected 10%             |              50.18 |         41.81 |         58.19 |                 49 |                  52 |
| Corrected 20%             |              50.03 |         38.29 |         61.71 |                 48 |                  52 |
| Corrected 40%             |              49.71 |         31.99 |         68.01 |                 48 |                  51 |
| Corrected 50%             |              49.54 |         28.95 |         71.05 |                 48 |                  51 |
| Non-Bayesian corrected    |              48.37 |         16.35 |         83.65 |                 46 |                  51 |
| Older Gaussian            |              51.09 |         62.00 |         38.00 |                 49 |                  53 |
| Student-t research helper |              51.12 |         63.01 |         36.99 |                 49 |                  53 |
| Matched Student-t (df5)   |              50.48 |         50.03 |         49.97 |                 49 |                  52 |
| Four-model mixture        |              50.75 |         55.14 |         44.86 |                 49 |                  53 |
| Mixture + polling 5%      |              50.67 |         53.24 |         46.76 |                 49 |                  52 |
| Mixture + polling 10%     |              50.59 |         51.31 |         48.69 |                 49 |                  52 |
| Mixture + polling 20%     |              50.42 |         47.38 |         52.62 |                 49 |                  52 |
| Mixture + polling 30%     |              50.24 |         43.56 |         56.44 |                 48 |                  52 |
| Mixture + polling 40%     |              50.06 |         39.82 |         60.18 |                 48 |                  52 |
| Mixture + polling 50%     |              49.87 |         35.95 |         64.05 |                 48 |                  52 |

Mixtures and polling blends are comparisons, not automatically selected replacements for the reference model.

## State forecasts — reference model

| Contest      |   D−R margin |   D win % |   95% low |   95% high |
|:-------------|-------------:|----------:|----------:|-----------:|
| AK           |        -3.10 |     30.01 |    -14.67 |       8.48 |
| AL           |       -22.02 |      0.04 |    -34.85 |      -9.18 |
| AR           |       -20.80 |      0.17 |    -34.69 |      -6.90 |
| CO           |        17.44 |     92.75 |     -6.02 |      40.89 |
| DE           |        24.95 |     99.92 |      9.41 |      40.49 |
| FL (special) |        -5.48 |     20.29 |    -18.39 |       7.43 |
| GA           |         5.22 |     80.84 |     -6.51 |      16.94 |
| IA           |        -3.27 |     29.18 |    -14.95 |       8.41 |
| ID           |       -25.97 |      0.02 |    -40.47 |     -11.48 |
| IL           |        22.02 |     99.60 |      5.76 |      38.28 |
| KS           |        -8.39 |      6.37 |    -19.17 |       2.39 |
| KY           |       -13.60 |      1.37 |    -25.67 |      -1.52 |
| LA           |       -15.98 |      2.71 |    -32.26 |       0.29 |
| MA           |        25.62 |    100.00 |     14.09 |      37.15 |
| ME           |         8.19 |     92.00 |     -3.23 |      19.61 |
| MI           |         4.99 |     79.94 |     -6.67 |      16.65 |
| MN           |         8.39 |     87.90 |     -5.66 |      22.43 |
| MS           |       -11.64 |      2.38 |    -23.15 |      -0.13 |
| MT           |       -18.69 |      0.37 |    -32.34 |      -5.03 |
| NC           |         4.75 |     82.58 |     -5.18 |      14.67 |
| NE           |       -24.08 |      3.51 |    -50.14 |       1.98 |
| NH           |         9.98 |     95.41 |     -1.62 |      21.57 |
| NJ           |        17.72 |     99.62 |      4.70 |      30.74 |
| NM           |        15.59 |     98.11 |      0.88 |      30.31 |
| OH (special) |         2.77 |     68.66 |     -8.40 |      13.95 |
| OK           |       -27.86 |      0.05 |    -44.46 |     -11.27 |
| OR           |        23.07 |     99.87 |      8.08 |      38.05 |
| RI           |        27.17 |     99.95 |     10.99 |      43.36 |
| SC           |       -10.92 |      3.32 |    -22.58 |       0.74 |
| SD           |       -34.05 |      0.02 |    -52.84 |     -15.26 |
| TN           |       -21.44 |      0.48 |    -37.68 |      -5.20 |
| TX           |         0.06 |     50.51 |     -9.51 |       9.64 |
| VA           |        16.45 |     98.41 |      1.43 |      31.46 |
| WV           |       -32.47 |      5.68 |    -72.67 |       7.74 |
| WY           |       -43.33 |      0.00 |    -58.44 |     -28.22 |

## Recently polled races with broad uncertainty

| Contest    | Latest poll   |   Recent samples |   Recent firms | Stronger coverage   |   95% interval width (pp) |
|:-----------|:--------------|-----------------:|---------------:|:--------------------|--------------------------:|
| NM         | 2026-08-28    |                1 |              1 | False               |                     29.42 |
| MN         | 2026-09-10    |                1 |              1 | False               |                     28.10 |
| MT         | 2026-09-15    |                3 |              3 | True                |                     27.31 |
| FL special | 2026-09-17    |                3 |              3 | True                |                     25.82 |

Watchlist settings: recent_days=30, min_width_pp=25, min_samples=3, min_firms=2.

## Control probability over cutoff dates

**This is a retrospective reconstruction, not a record of forecasts issued on those dates.** The current roster, revised historical features and September-calibrated model are reused at earlier cutoffs.

![Control probabilities across cutoff dates](control_history.png)

### Recent reference-model cutoffs

| Cutoff     |   D control % |   R control % |   Expected D seats |   D seats: 70% low |   D seats: 70% high |
|:-----------|--------------:|--------------:|-------------------:|-------------------:|--------------------:|
| 2026-09-19 |         45.54 |         54.46 |              50.32 |                 49 |                  52 |
| 2026-09-20 |         45.51 |         54.49 |              50.32 |                 49 |                  52 |
| 2026-09-21 |         45.52 |         54.48 |              50.32 |                 49 |                  52 |

History mode: **dated**; regular spacing: **30 days**. Small differences can include Monte Carlo variation. All models and cutoff rows are in the HTML and supporting Parquet tables.

## Provenance and interpretation

- [Forecast settings, input hash and source receipts](../../results/forecast/live_reports/forecast_metadata.json)
- [Complete state predictions](../../results/forecast/live_reports/predictions.parquet)
- [Chamber results](../../results/forecast/live_reports/seats.parquet)

The model retains its candidate, caucus, election-rule, historical-vintage and small-sample limitations. Probabilities are model estimates. An unchanged fitted checkpoint can produce different forecasts when polls, feature observations or the cutoff change.
