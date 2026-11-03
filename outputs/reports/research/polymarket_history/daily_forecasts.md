# Daily historical Senate forecast dataset

2022: September 1–November 7 (68 days). 2024: September 1–November 4 (65 days).

One row per cycle, date, state, race kind (regular/special) and model. Missing rows are explicit; publisher forecasts are never forward-filled. No market-price, positive-edge or future-path filter selects these rows. No outcome labels are included. This is a reusable forecast dataset, not a trading result.

Local coverage follows the existing supported historical race roster; it is not all Senate contests. Publisher state series are retained separately and are not silently mapped onto special or independent-candidate contracts.

Retrospective reconstruction from saved chronological folds. Model design was developed later; feature publication vintages are not fully reconstructed. This is not a pristine prospective test. Local calibration remains the frozen September 17 calibration. Publisher histories are retrospective archives, not independently verified original daily publication vintages.

|   cycle | model   |   days |   states |   available |   missing |
|--------:|:--------|-------:|---------:|------------:|----------:|
|    2022 | 538     |     68 |       31 |        2176 |         0 |
|    2022 | 538C    |     68 |       31 |        2176 |         0 |
|    2022 | 538L    |     68 |       31 |        2176 |         0 |
|    2022 | DDHQ    |      0 |        0 |           0 |      2176 |
|    2022 | DDHQ0   |      0 |        0 |           0 |      2176 |
|    2022 | ECON    |     40 |        4 |         160 |      2016 |
|    2022 | GB      |     68 |       26 |        1768 |       408 |
|    2022 | M10     |     68 |       26 |        1768 |       408 |
|    2022 | MX      |     68 |       26 |        1768 |       408 |
|    2022 | OG      |     68 |       26 |        1768 |       408 |
|    2022 | OS      |     68 |       26 |        1768 |       408 |
|    2022 | RTWH    |      0 |        0 |           0 |      2176 |
|    2022 | ST      |     68 |       26 |        1768 |       408 |
|    2024 | 538     |      0 |        0 |           0 |      1950 |
|    2024 | 538C    |      0 |        0 |           0 |      1950 |
|    2024 | 538L    |      0 |        0 |           0 |      1950 |
|    2024 | DDHQ    |     61 |       30 |        1830 |       120 |
|    2024 | DDHQ0   |      0 |        0 |           0 |      1950 |
|    2024 | ECON    |      0 |        0 |           0 |      1950 |
|    2024 | GB      |     65 |       28 |        1820 |       130 |
|    2024 | M10     |     65 |       28 |        1820 |       130 |
|    2024 | MX      |     65 |       28 |        1820 |       130 |
|    2024 | OG      |     65 |       28 |        1820 |       130 |
|    2024 | OS      |     65 |       28 |        1820 |       130 |
|    2024 | RTWH    |     13 |       29 |         377 |      1573 |
|    2024 | ST      |     65 |       28 |        1820 |       130 |

Data: `outputs/results/research/polymarket_history/daily_forecasts.parquet` (Git-ignored). Source receipts and the checksum manifest live beside it. Rebuild with `.venv/bin/python scripts/polymarket_daily_forecasts.py`; add `--download-publishers` to retrieve missing publisher archives. Daily inference caches resume interrupted runs. Existing 12-date analysis tables are unchanged.
