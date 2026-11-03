# 2026 Senate forecast — 2026-11-02

[All outputs](../../README.md) · [HTML report](report.html) · [Supporting tables](./)

## At a glance

- **D/Independent control: 73.9%** under the reference Gaussian model.
- **Expected D/Independent seats: 51.5**; central 70% range: **50–53**.
- Predicted winners by mean margin: **51 D/IND / 49 R**.
- Trained through **2024**. Live evidence updates predictions; trained parameters are fixed.

Margins are D/Independent minus Republican percentage points. Positive margins favor the D/Independent side. D control requires 51 seats; R control includes a 50–50 chamber under the retained vice-presidential tie-break assumption.

## Poll coverage and candidate affiliations

[All-state polling audit](poll_audit.md). Independents retain their IND affiliation. For multiple D/IND candidates, the strongest individual candidate is used, never their summed votes. Independent chamber alignment is an explicit modeling assumption.

## Data freshness

| Source         | Status                  | Last successful check            |
|:---------------|:------------------------|:---------------------------------|
| polls          | Checked online this run | 2026-11-03T00:58:11.957699+00:00 |
| fred           | Checked online this run | 2026-11-03T00:58:11.846385+00:00 |
| michigan       | Checked online this run | 2026-11-03T00:58:14.731052+00:00 |
| ucsb           | Checked online this run | 2026-11-03T00:58:10.598109+00:00 |
| french         | Checked online this run | 2026-11-03T00:58:11.338020+00:00 |
| cboe           | Checked online this run | 2026-11-03T00:58:12.133717+00:00 |
| gpr            | Checked online this run | 2026-11-03T00:58:13.188666+00:00 |
| epu            | Checked online this run | 2026-11-03T00:58:13.825743+00:00 |
| infectious_emv | Checked online this run | 2026-11-03T00:58:13.098934+00:00 |

Political context is reviewed through **2026-09-17**. It is carried forward as an explicit assumption.

The forecast cutoff does not mean every source has observations through that date. Missing evidence is not replaced with a zero.

## Chamber forecast across models

| Model                               |   Expected D seats |   D control % |   R control % |   D seats: 70% low |   D seats: 70% high |
|:------------------------------------|-------------------:|--------------:|--------------:|-------------------:|--------------------:|
| Gaussian Bayesian                   |              51.47 |         73.93 |         26.07 |                 50 |                  53 |
| Gaussian: 10% shift toward baseline |              51.37 |         71.20 |         28.80 |                 50 |                  53 |
| Gaussian: 20% shift toward baseline |              51.26 |         68.37 |         31.63 |                 50 |                  53 |
| Gaussian: 40% shift toward baseline |              51.06 |         62.78 |         37.22 |                 49 |                  53 |
| Gaussian: 50% shift toward baseline |              50.96 |         60.30 |         39.70 |                 49 |                  53 |
| Empirical baseline                  |              50.47 |         49.33 |         50.67 |                 48 |                  53 |
| Older Gaussian                      |              52.47 |         85.09 |         14.91 |                 51 |                  54 |
| Student-t research helper           |              52.44 |         87.09 |         12.91 |                 51 |                  54 |
| Matched Student-t (df5)             |              51.59 |         77.79 |         22.21 |                 50 |                  53 |
| Four-model mixture                  |              51.99 |         80.97 |         19.03 |                 50 |                  54 |
| Mixture: 5% shift toward baseline   |              51.92 |         79.63 |         20.37 |                 50 |                  54 |
| Mixture: 10% shift toward baseline  |              51.84 |         78.25 |         21.75 |                 50 |                  54 |
| Mixture: 20% shift toward baseline  |              51.69 |         75.37 |         24.63 |                 50 |                  53 |
| Mixture: 30% shift toward baseline  |              51.55 |         72.28 |         27.72 |                 50 |                  53 |
| Mixture: 40% shift toward baseline  |              51.40 |         69.05 |         30.95 |                 50 |                  53 |
| Mixture: 50% shift toward baseline  |              51.25 |         65.78 |         34.22 |                 49 |                  53 |

All forecasts shown here use polling evidence when available. The empirical baseline uses poll averages and historical polling-error patterns. A 20% shift moves the predicted margin one-fifth of the way toward that baseline while retaining the original model’s uncertainty distribution. It does not mean the other models omit polls or need correction. Mixtures and mean shifts are comparisons, not automatically selected replacements for the reference model.

## State forecasts — reference model

| Contest      |   D/IND−R margin |   D/IND win % |   95% low |   95% high |
|:-------------|-----------------:|--------------:|----------:|-----------:|
| AK           |            -2.04 |         36.39 |    -13.52 |       9.44 |
| AL           |           -19.69 |          0.03 |    -31.04 |      -8.35 |
| AR           |           -20.63 |          0.18 |    -34.49 |      -6.77 |
| CO           |            19.71 |         99.93 |      7.70 |      31.73 |
| DE           |            26.75 |         99.96 |     11.26 |      42.25 |
| FL (special) |            -6.15 |         17.16 |    -18.87 |       6.57 |
| GA           |             7.34 |         89.69 |     -4.04 |      18.72 |
| IA           |            -2.29 |         34.96 |    -13.90 |       9.32 |
| ID           |           -17.86 |          0.05 |    -28.44 |      -7.27 |
| IL           |            19.87 |         99.88 |      7.01 |      32.74 |
| KS           |            -5.00 |         17.70 |    -15.57 |       5.57 |
| KY           |           -12.56 |          2.57 |    -25.19 |       0.07 |
| LA           |            -8.64 |          8.05 |    -20.71 |       3.44 |
| MA           |            28.76 |        100.00 |     17.78 |      39.73 |
| ME           |             8.94 |         93.94 |     -2.36 |      20.24 |
| MI           |             6.56 |         86.59 |     -5.05 |      18.16 |
| MN           |             9.05 |         92.22 |     -3.44 |      21.55 |
| MS           |            -9.05 |          5.24 |    -19.98 |       1.89 |
| MT           |            -8.82 |         10.13 |    -22.38 |       4.75 |
| NC           |             7.44 |         93.10 |     -2.39 |      17.27 |
| NE           |            -7.64 |         14.60 |    -21.86 |       6.57 |
| NH           |            12.15 |         98.54 |      1.23 |      23.08 |
| NJ           |            19.54 |         99.84 |      6.58 |      32.50 |
| NM           |            18.39 |         99.75 |      5.56 |      31.21 |
| OH (special) |             3.19 |         71.55 |     -7.79 |      14.18 |
| OK           |           -25.81 |          0.02 |    -39.96 |     -11.66 |
| OR           |            24.98 |         99.95 |     10.05 |      39.91 |
| RI           |            29.47 |        100.00 |     17.94 |      41.00 |
| SC           |            -7.97 |          8.63 |    -19.42 |       3.48 |
| SD           |           -27.33 |          0.06 |    -43.77 |     -10.89 |
| TN           |           -21.58 |          0.09 |    -35.08 |      -8.08 |
| TX           |             1.25 |         60.23 |     -8.21 |      10.71 |
| VA           |            18.34 |         99.39 |      4.00 |      32.69 |
| WV           |           -30.49 |          6.85 |    -70.68 |       9.69 |
| WY           |           -41.50 |          0.00 |    -56.56 |     -26.44 |

## Recently polled races with broad uncertainty

| Contest    | Latest poll   |   Recent samples |   Recent firms | Stronger coverage   |   95% interval width (pp) |
|:-----------|:--------------|-----------------:|---------------:|:--------------------|--------------------------:|
| SD         | 2026-10-26    |                6 |              5 | True                |                     32.88 |
| NE         | 2026-11-01    |               11 |              8 | True                |                     28.43 |
| AR         | 2026-10-28    |                3 |              2 | True                |                     27.72 |
| MT         | 2026-10-23    |                5 |              4 | True                |                     27.12 |
| IL         | 2026-11-02    |                3 |              2 | True                |                     25.73 |
| NM         | 2026-11-02    |                2 |              2 | False               |                     25.65 |
| FL special | 2026-11-02    |               19 |             15 | True                |                     25.44 |

Watchlist settings: recent_days=30, min_width_pp=25.0, min_samples=3, min_firms=2.

## Races to watch — room for a different outcome

Reference-model winner, margin, 95% interval and other-winner probability describe the likely outcome and its alternatives. Disagreement is the mean absolute pairwise difference in core-model margins. Predictive SD is the square root of the mean within-model variance, not variance between model means. Blends/mixtures are excluded; the core models share evidence and are not independent votes. Within each polling group, select the top 3 races on each of disagreement, predictive SD, reference-model other-winner probability, and historical mean absolute error (at least two past races); take their union and order by other-winner probability. Ties are broken by contest name. This is a review screen, not a calibrated probability of surprising the public. History uses the last three completed state races in September backtests before the current cycle; it can include other Senate seats and special elections. These are reconstructed forecasts, not issued forecasts. Past errors are context and do not alter current probabilities.

Coverage: at least 3 independent eligible samples from 2 firms in the past 30 days.

Available core models: Gaussian Bayesian, Matched Student-t (df5), Older Gaussian, Student-t research helper, Empirical baseline.

### Adequately polled races

| Race   | Likely winner   |   D−R margin | 95% range (pp)   |   Other winner % |   Disagreement (pp) |   Predictive SD (pp) | Recent polls / firms   | Past state surprises                                                                                                   | Why watch                                                                                                                                                                           |
|:-------|:----------------|-------------:|:-----------------|-----------------:|--------------------:|---------------------:|:-----------------------|:-----------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TX     | D               |         1.30 | -8.2 to 10.7     |            39.80 |                0.30 |                 6.90 | 31 / 23                | The largest miss was 5.1 pp in 2018. 0 of 3 results fell outside the 95% range. It missed the winner in 0 of 3 races.  | Other-winner probability ranks #1 in this group.                                                                                                                                    |
| AK     | R               |        -2.00 | -13.5 to 9.4     |            36.40 |                1.10 |                 7.80 | 6 / 4                  | No comparable history is available.                                                                                    | Other-winner probability ranks #2 in this group.                                                                                                                                    |
| IA     | R               |        -2.30 | -13.9 to 9.3     |            35.00 |                1.30 |                 7.60 | 15 / 13                | The largest miss was 10.4 pp in 2016. 0 of 3 results fell outside the 95% range. It missed the winner in 0 of 3 races. | Other-winner probability ranks #3 in this group.                                                                                                                                    |
| NE     | R               |        -7.60 | -21.9 to 6.6     |            14.60 |                2.70 |                 8.60 | 11 / 8                 | The largest miss was 22.2 pp in 2020. 0 of 3 results fell outside the 95% range. It missed the winner in 0 of 3 races. | Predictive uncertainty ranks #3 in this group. Past margin error ranks #2 in this group.                                                                                            |
| ME     | D               |         8.90 | -2.4 to 20.2     |             6.10 |                4.30 |                 7.80 | 14 / 13                | No comparable history is available.                                                                                    | Model disagreement ranks #3 in this group. Models disagree on the winner.                                                                                                           |
| AR     | R               |       -20.60 | -34.5 to -6.8    |             0.20 |                6.80 |                 9.50 | 3 / 2                  | The largest miss was 16.7 pp in 2022. 2 of 3 results fell outside the 95% range. It missed the winner in 0 of 3 races. | Model disagreement ranks #2 in this group. Predictive uncertainty ranks #2 in this group. Past margin error ranks #3 in this group. 2 of 3 past results fell outside the 95% range. |
| SD     | R               |       -27.30 | -43.8 to -10.9   |             0.10 |               10.10 |                11.20 | 6 / 5                  | The largest miss was 32.0 pp in 2016. 1 of 3 results fell outside the 95% range. It missed the winner in 0 of 3 races. | Model disagreement ranks #1 in this group. Predictive uncertainty ranks #1 in this group. Past margin error ranks #1 in this group. 1 of 3 past results fell outside the 95% range. |

### Thinly polled or no recent polls

| Race   | Likely winner   |   D−R margin | 95% range (pp)   | Other winner %   |   Disagreement (pp) |   Predictive SD (pp) | Recent polls / firms   | Past state surprises                                                                                                   | Why watch                                                                                                                                                                                                                                                                |
|:-------|:----------------|-------------:|:-----------------|:-----------------|--------------------:|---------------------:|:-----------------------|:-----------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| LA     | R               |        -8.60 | -20.7 to 3.4     | 8.1              |                2.20 |                 8.20 | 1 / 1                  | No comparable history is available.                                                                                    | Other-winner probability ranks #1 in this group. Recent polling is limited.                                                                                                                                                                                              |
| WV     | R               |       -30.50 | -70.7 to 9.7     | 6.8              |               10.10 |                31.10 | 0 / 0                  | The largest miss was 47.9 pp in 2020. 1 of 3 results fell outside the 95% range. It missed the winner in 1 of 3 races. | Model disagreement ranks #1 in this group. Predictive uncertainty ranks #1 in this group. Other-winner probability ranks #2 in this group. Past margin error ranks #1 in this group. There are no recent eligible polls. 1 of 3 past results fell outside the 95% range. |
| MS     | R               |        -9.00 | -20.0 to 1.9     | 5.2              |                3.60 |                 7.70 | 1 / 1                  | The largest miss was 9.1 pp in 2024. 0 of 3 results fell outside the 95% range. It missed the winner in 0 of 3 races.  | Other-winner probability ranks #3 in this group. Recent polling is limited.                                                                                                                                                                                              |
| TN     | R               |       -21.60 | -35.1 to -8.1    | 0.1              |                6.10 |                 8.70 | 0 / 0                  | The largest miss was 13.8 pp in 2020. 0 of 3 results fell outside the 95% range. It missed the winner in 0 of 3 races. | Model disagreement ranks #3 in this group. Past margin error ranks #2 in this group. There are no recent eligible polls.                                                                                                                                                 |
| OR     | D               |        25.00 | 10.0 to 39.9     | 0.1              |                7.00 |                 9.60 | 0 / 0                  | The largest miss was 9.7 pp in 2020. 0 of 3 results fell outside the 95% range. It missed the winner in 0 of 3 races.  | Model disagreement ranks #2 in this group. There are no recent eligible polls.                                                                                                                                                                                           |
| DE     | D               |        26.80 | 11.3 to 42.2     | <0.1             |                5.10 |                 9.90 | 0 / 0                  | The largest miss was 7.9 pp in 2020. 0 of 3 results fell outside the 95% range. It missed the winner in 0 of 3 races.  | Predictive uncertainty ranks #3 in this group. Past margin error ranks #3 in this group. There are no recent eligible polls.                                                                                                                                             |
| WY     | R               |       -41.50 | -56.6 to -26.4   | <0.1             |                0.50 |                10.10 | 0 / 0                  | The largest miss was 13.0 pp in 2018. 0 of 3 results fell outside the 95% range. It missed the winner in 0 of 3 races. | Predictive uncertainty ranks #2 in this group. There are no recent eligible polls.                                                                                                                                                                                       |

[All races and numerical scores](./surprise_all.parquet) · [Watchlist settings and provenance](./surprise_parameters.json)

## Control probability over cutoff dates

**This is a retrospective reconstruction, not a record of forecasts issued on those dates.** The current roster, revised historical features and September-calibrated model are reused at earlier cutoffs.

![Control probabilities across cutoff dates](control_history.png)

### Recent reference-model cutoffs

| Cutoff     |   D control % |   R control % |   Expected D seats |   D seats: 70% low |   D seats: 70% high |
|:-----------|--------------:|--------------:|-------------------:|-------------------:|--------------------:|
| 2026-10-31 |         71.82 |         28.18 |              51.39 |                 50 |                  53 |
| 2026-11-01 |         72.19 |         27.81 |              51.41 |                 50 |                  53 |
| 2026-11-02 |         73.93 |         26.07 |              51.47 |                 50 |                  53 |

History mode: **dated**; regular spacing: **30 days**. Small differences can include Monte Carlo variation. All models and cutoff rows are in the HTML and supporting Parquet tables.

## Comparison with published forecasts

This section is generated from publisher feeds on each live rerun. It compares the Gaussian Bayesian reference and the four-model mixture with published forecasts. A numerical mismatch means opposite favored winners or a D/Independent win probability gap of at least 15 percentage points. For ratings, a mismatch means opposite favored parties, or a publisher toss-up when our model gives one party at least 75% probability. Ratings are never converted into probabilities. These are differences of opinion, not evidence that either forecast is wrong. Sources can use different data dates and methods. Chamber totals retain each publisher’s own independent-caucus convention. Independent candidates count on the D/Independent side in state comparisons. Published D and independent win probabilities are added once; independents already in a publisher’s D column are not added again. This is our comparison assumption, not a claim about their party affiliation or future caucus. Silver supplies only a dated, rounded public Deluxe topline; its detailed subscriber forecasts are unavailable. Publisher releases after our cutoff are excluded. A successful download does not mean the forecast was updated today.

### Source dates and availability

| Source                 | URL                                                            | Status                    | Published   | Retrieved                        | Error                                                                                                                | Coverage                                                                                                                                     |   Days before our cutoff |
|:-----------------------|:---------------------------------------------------------------|:--------------------------|:------------|:---------------------------------|:---------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|-------------------------:|
| Silver Bulletin Deluxe | https://www.natesilver.net/p/expert-ratings-are-ignoring-signs | stale_cache_after_failure | 2026-09-20  | 2026-10-06T01:44:28.847019+00:00 | ValueError: No unambiguous Deluxe Senate-control probability in public text; detailed tables require a subscription. | Rounded Deluxe Senate-control probability from public text. State probabilities and expected seats are subscriber-only and unavailable here. |                       43 |
| Race to the WH         | https://www.racetothewh.com/senate/26                          | checked_online            | 2026-11-02  | 2026-11-03T00:58:34.417755+00:00 |                                                                                                                      | State and chamber forecasts                                                                                                                  |                        0 |
| Inside Elections       | https://insideelections.com/ratings/senate/                    | checked_online            | 2026-10-29  | 2026-11-03T00:58:35.398593+00:00 |                                                                                                                      | Public race ratings                                                                                                                          |                        4 |

### Senate control and expected seats

| Forecast               | Date       |   D control % | Expected D seats   | Coverage                                                                                                                                     |
|:-----------------------|:-----------|--------------:|:-------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|
| Gaussian Bayesian      | 2026-11-02 |         73.93 | 51.47256779754116  | Our model                                                                                                                                    |
| Four-model mixture     | 2026-11-02 |         80.97 | 51.98953177086481  | Our model                                                                                                                                    |
| Silver Bulletin Deluxe | 2026-09-20 |         65.00 | —                  | Rounded Deluxe Senate-control probability from public text. State probabilities and expected seats are subscriber-only and unavailable here. |
| Race to the WH         | 2026-11-02 |         80.30 | 53.2               | Published forecast.                                                                                                                          |

### Chamber differences: ours minus publisher

| Model              | Publisher              | Published   |   Our D control % |   Published D control % |   Gap (pp) | Expected-seat gap   | Comparison                                 |
|:-------------------|:-----------------------|:------------|------------------:|------------------------:|-----------:|:--------------------|:-------------------------------------------|
| Gaussian Bayesian  | Silver Bulletin Deluxe | 2026-09-20  |             73.93 |                   65.00 |       8.93 | —                   | The models favor the same Senate majority. |
| Four-model mixture | Silver Bulletin Deluxe | 2026-09-20  |             80.97 |                   65.00 |      15.97 | —                   | The models favor the same Senate majority. |
| Gaussian Bayesian  | Race to the WH         | 2026-11-02  |             73.93 |                   80.30 |      -6.37 | -1.7274322024588429 | The models favor the same Senate majority. |
| Four-model mixture | Race to the WH         | 2026-11-02  |             80.97 |                   80.30 |       0.67 | -1.210468229135195  | The models favor the same Senate majority. |

### Inside Elections: favored-party counts in matched races

| Model              |   Matched races |   Our D/Independent favored |   Our R favored |   Publisher D/Independent favored |   Publisher R favored |   Publisher toss-ups |
|:-------------------|----------------:|----------------------------:|----------------:|----------------------------------:|----------------------:|---------------------:|
| Gaussian Bayesian  |              35 |                          17 |              18 |                                16 |                    15 |                    4 |
| Four-model mixture |              35 |                          17 |              18 |                                16 |                    15 |                    4 |

### State mismatches

| Source           | Published   | Model              | Contest   |   Our D/Independent win % | Published D/Independent win %   | Published rating   | Gap (pp)            | Side definition   | Reason                                                                                         |
|:-----------------|:------------|:-------------------|:----------|--------------------------:|:--------------------------------|:-------------------|:--------------------|:------------------|:-----------------------------------------------------------------------------------------------|
| Inside Elections | 2026-10-29  | Four-model mixture | KS        |                     23.14 | —                               | Toss-up            | —                   | D versus R.       | The publisher rates this a toss-up. Our model gives R 76.9%.                                   |
| Inside Elections | 2026-10-29  | Four-model mixture | ME        |                     87.56 | —                               | Toss-up            | —                   | D versus R.       | The publisher rates this a toss-up. Our model gives D 87.6%.                                   |
| Inside Elections | 2026-10-29  | Gaussian Bayesian  | KS        |                     17.70 | —                               | Toss-up            | —                   | D versus R.       | The publisher rates this a toss-up. Our model gives R 82.3%.                                   |
| Inside Elections | 2026-10-29  | Gaussian Bayesian  | ME        |                     93.94 | —                               | Toss-up            | —                   | D versus R.       | The publisher rates this a toss-up. Our model gives D 93.9%.                                   |
| Race to the WH   | 2026-11-02  | Four-model mixture | KS        |                     23.14 | 58.4                            | —                  | -35.25703124999329  | D versus R.       | The forecasts favor different parties. Our D/Independent win probability is 35.3 points lower. |
| Race to the WH   | 2026-11-02  | Four-model mixture | IA        |                     34.80 | 65.6                            | —                  | -30.79932291668568  | D versus R.       | The forecasts favor different parties. Our D/Independent win probability is 30.8 points lower. |
| Race to the WH   | 2026-11-02  | Four-model mixture | SC        |                     15.02 | 40.1                            | —                  | -25.078437499998586 | D versus R.       | Our D/Independent win probability is 25.1 points lower.                                        |
| Race to the WH   | 2026-11-02  | Four-model mixture | TX        |                     59.04 | 81.6                            | —                  | -22.563124999973905 | D versus R.       | Our D/Independent win probability is 22.6 points lower.                                        |
| Race to the WH   | 2026-11-02  | Four-model mixture | AK        |                     42.17 | 61.6                            | —                  | -19.434687500025554 | D versus R.       | The forecasts favor different parties. Our D/Independent win probability is 19.4 points lower. |
| Race to the WH   | 2026-11-02  | Four-model mixture | WV        |                     19.83 | 0.5                             | —                  | 19.33437500000756   | D versus R.       | Our D/Independent win probability is 19.3 points higher.                                       |
| Race to the WH   | 2026-11-02  | Four-model mixture | ME        |                     87.56 | 72.3                            | —                  | 15.255416666823074  | D versus R.       | Our D/Independent win probability is 15.3 points higher.                                       |
| Race to the WH   | 2026-11-02  | Gaussian Bayesian  | KS        |                     17.70 | 58.4                            | —                  | -40.70200701184501  | D versus R.       | The forecasts favor different parties. Our D/Independent win probability is 40.7 points lower. |
| Race to the WH   | 2026-11-02  | Gaussian Bayesian  | SC        |                      8.63 | 40.1                            | —                  | -31.470182066182854 | D versus R.       | Our D/Independent win probability is 31.5 points lower.                                        |
| Race to the WH   | 2026-11-02  | Gaussian Bayesian  | IA        |                     34.96 | 65.6                            | —                  | -30.643427097347864 | D versus R.       | The forecasts favor different parties. Our D/Independent win probability is 30.6 points lower. |
| Race to the WH   | 2026-11-02  | Gaussian Bayesian  | AK        |                     36.39 | 61.6                            | —                  | -25.213661130668207 | D versus R.       | The forecasts favor different parties. Our D/Independent win probability is 25.2 points lower. |
| Race to the WH   | 2026-11-02  | Gaussian Bayesian  | ME        |                     93.94 | 72.3                            | —                  | 21.64070325442584   | D versus R.       | Our D/Independent win probability is 21.6 points higher.                                       |
| Race to the WH   | 2026-11-02  | Gaussian Bayesian  | TX        |                     60.23 | 81.6                            | —                  | -21.368143351643752 | D versus R.       | Our D/Independent win probability is 21.4 points lower.                                        |

### Excluded comparisons

No rows qualify or the source is unavailable. Check source status above.

[All matched state comparisons](./published_all_states.parquet) · [Publisher snapshots and provenance](./published_sources.json) · [Comparison settings](./published_parameters.json)

## Shareable images

The tables above remain available. These PNGs are generated from the same saved results on every run.

![chamber](share_chamber.png)

![compare inside elections four model mixture](share_compare_inside_elections_four_model_mixture.png)

![compare inside elections gaussian bayesian](share_compare_inside_elections_gaussian_bayesian.png)

![compare race to the wh four model mixture](share_compare_race_to_the_wh_four_model_mixture.png)

![compare race to the wh gaussian bayesian](share_compare_race_to_the_wh_gaussian_bayesian.png)

![published chamber](share_published_chamber.png)

![state margins](share_state_margins.png)

![state probabilities](share_state_probabilities.png)

![uncertainty](share_uncertainty.png)

![watch polled](share_watch_polled.png)

![watch thin](share_watch_thin.png)

[Image manifest](./share_images.json)

## Provenance and interpretation

- [Forecast settings, input hash and source receipts](./forecast_metadata.json)
- [Complete state predictions](./predictions.parquet)
- [Chamber results](./seats.parquet)

The model retains its candidate, caucus, election-rule, historical-vintage and small-sample limitations. Probabilities are model estimates. An unchanged fitted checkpoint can produce different forecasts when polls, feature observations or the cutoff change.
