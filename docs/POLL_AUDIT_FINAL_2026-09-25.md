# Final all-state input audit — 2026-09-25

Forecast run: `20260925T165454.221722Z`. Cutoff: **2026-09-25**. Trained model parameters remain fixed.

## Result

All **35 Senate states** were checked. All **647 source question versions**, including reviewed supplements, reconcile to the retained audit records. Every question has a model disposition. No flagged conditional/informed/reduced alternative is admitted; valid margins, positive sample sizes and publication/fieldwork cutoff checks pass. The previous coverage review's confirmed gaps are addressed below. These checks validate the stored inventory; they do not prove that every public poll is available in our sources.

| Check                                                      | Passed   |
|:-----------------------------------------------------------|:---------|
| Every source question has a forecast disposition           | True     |
| All admitted questions have valid margins and sample sizes | True     |
| No rejected ballot/scenario enters the forecast            | True     |
| No admitted fieldwork or known release is after cutoff     | True     |

## Resolved findings

- **Louisiana:** James Davis is a sourced alias for Jamie Davis. Both polls enter. Raw candidate IDs/names are preserved alongside canonical identities. Aliases do not transfer polls between different people.
- **Montana:** Bankhead (DEM), Bodnar (IND) and Alme (REP) must all appear. Ten full-core-field samples enter, including three recent firms. Head-to-head removal scenarios remain stored but do not enter the main forecast.
- **Idaho:** The missing September ATR survey enters once, using its fuller three-candidate ballot. July Change Research's missing sample size is repaired from its primary release (1,213 LV). Bullfinch's initial June ballot is retained; its informed headline is not used to reject initial results. The August reduced two-way version is not averaged with its fuller ballot.
- **Virginia:** Both TPSI surveys enter using original LV crosstab shares and unweighted sample counts. The current Republican nominee has an explicit canonical identity, and Mark Moran remains IND.
- **South Carolina:** The recovered August 22 primary memo is retained with its verified public availability date. It overlaps the existing August 24 release; both are conservatively linked to one sample, preventing an extra independent observation.
- **Across states:** Fuller eligible ballots take precedence over reduced versions within a survey/population. Current contender IDs and explicitly reviewed exact names/aliases are accepted; replaced or withdrawn people remain distinct. Known publication/archive availability bounds are now enforced in cutoff replays as well as initial ingestion.

## All states

Recent means the preceding 30 days. Model samples collapse question/population versions and conservative overlap groups. Excluded counts refer to question versions, not whole surveys. Older eligible polls still contribute.

| State   |   Model samples |   Recent samples |   Questions |   Excluded |
|:--------|----------------:|-----------------:|------------:|-----------:|
| AK      |              14 |                3 |          28 |         14 |
| AL      |               1 |                0 |           1 |          0 |
| AR      |               4 |                0 |           4 |          0 |
| CO      |               0 |                0 |           0 |          0 |
| DE      |               0 |                0 |           0 |          0 |
| FL      |               9 |                5 |          25 |         16 |
| GA      |              15 |                4 |          50 |         34 |
| IA      |              19 |                9 |          33 |         13 |
| ID      |               6 |                1 |          12 |          6 |
| IL      |               0 |                0 |           0 |          0 |
| KS      |               6 |                3 |          15 |          9 |
| KY      |               2 |                1 |           6 |          4 |
| LA      |               2 |                1 |           2 |          0 |
| MA      |              10 |                1 |          19 |          9 |
| ME      |              12 |                7 |          61 |         49 |
| MI      |              35 |               11 |          82 |         47 |
| MN      |               8 |                4 |          16 |          8 |
| MS      |               2 |                0 |           5 |          3 |
| MT      |              10 |                3 |          28 |         18 |
| NC      |              34 |                8 |          48 |         12 |
| NE      |               7 |                3 |          10 |          3 |
| NH      |              19 |                4 |          45 |         26 |
| NJ      |               0 |                0 |           0 |          0 |
| NM      |               1 |                1 |           1 |          0 |
| OH      |              22 |                5 |          26 |          4 |
| OK      |               1 |                0 |           2 |          1 |
| OR      |               0 |                0 |           0 |          0 |
| RI      |               4 |                1 |           4 |          0 |
| SC      |               3 |                2 |          18 |         15 |
| SD      |               7 |                1 |          11 |          4 |
| TN      |               1 |                1 |           2 |          1 |
| TX      |              39 |               12 |          90 |         51 |
| VA      |               2 |                0 |           3 |          1 |
| WV      |               0 |                0 |           0 |          0 |
| WY      |               0 |                0 |           0 |          0 |

## Explicit remaining qualifications

1. **Idaho partial ballots:** some surveys, including ATR, omit Natalie Fleming. They retain a partial-ballot flag and are not described as complete candidate-level distributions. The scalar model uses the strongest D/IND individual's margin, not summed votes. Pollster inclusion does not establish accuracy.
2. **Virginia dates and sample sizes:** the June release lacks exact fieldwork dates, so publication June 16 is an explicit conservative field-end upper bound. Crosstab unweighted samples are May 703 and June 663; the differing headline weighted totals are documented. May's inconsistent year in one prose heading is resolved to 2026 using the workbook and dated release.
3. **South Carolina independence:** distinct reported sample sizes and dates are documented, but respondent independence is unproven. One sample contribution is retained conservatively.
4. **No source questions:** CO, DE, IL, NJ, OR, WV and WY have no rows in the downloaded source, rather than hidden local exclusions. Their first incoming matchups will still need reviewed candidate identities. Absence of a verified external survey is not proof no survey exists.
5. **Election rules:** ranked-choice/runoff and multicandidate win probabilities remain approximations of the existing scalar forecast. This work corrects evidence ingestion; it does not introduce a joint candidate-level model.

## Reproducibility

The automatic audit is in [notebook 04](../notebooks/04_live_forecast.ipynb) and the [latest forecast audit](../outputs/reports/forecast/poll_audit.md), with a copy beside the [dated forecast](../outputs/reports/history/2026-09-25/live_reports/forecast-2026-09-25.md). Source receipts and review qualifications regenerate without AI. Compact snapshots seal the candidate review, supplemental records, unmodified upstream feed and reviewed feed.

Reviewed records: [candidate and question review](../config/candidate_review_2026.json), [supplemental source ledger](../config/supplemental_polls_2026.json). Primary-source URLs and document checksums are recorded there. See [polling policy](POLL_COVERAGE.md) for the selection rules.
