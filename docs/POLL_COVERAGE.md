# Current Senate polling coverage

Notebook 04 rebuilds the forecast and its [all-state polling audit](../outputs/reports/forecast/poll_audit.md) automatically. Each dated report retains the audit, review qualifications and source receipts.

Current-election margins represent **D/Independent versus Republican**. Source answers and canonical identities keep actual affiliations. Independents are not relabeled Democrats. Assigning independent winners to the D/Independent chamber side remains an explicit modeling assumption, not a verified caucus commitment.

## Candidate identities and replacements

`config/candidate_review_2026.json` records reviewed candidate IDs, exact source names, and sourced aliases. For example, Louisiana's James/Jamie Davis IDs refer to the same person. Original source IDs and names remain in the answer table alongside canonical identities. There is no fuzzy name matching and no transfer of votes between different people. Polls involving replaced, withdrawn or defeated contenders remain stored with an exclusion reason.

The reviewed principal contenders must be present. Montana requires Bankhead (DEM), Bodnar (IND) and Alme (REP) in the same question; hypothetical removal scenarios do not enter its main forecast. Idaho requires Achilles (IND) and Risch (REP); omission of Fleming (IND) is retained as an explicit **partial-ballot qualification**, not described as a complete candidate-level forecast. Additional independent responses do not invalidate an otherwise reviewed matchup. Within a survey and population, the fuller eligible ballot is preferred over a reduced ballot.

For multiple D/IND candidates, the scalar margin is **the strongest individual's support minus Republican support**, never combined votes. This remains an approximation: it does not model a joint distribution over every candidate. Ranked-choice and runoff limitations remain separate from polling inclusion.

## Reviewed supplements and question metadata

`config/supplemental_polls_2026.json` stores small, source-linked public polling records missing from the upstream feed. The code applies them on every refresh without AI calls. It saves source URLs, release/checksum evidence, raw upstream rows, reviewed rows and the review configuration inside each sealed compact input snapshot. If the same firm's overlapping sample arrives upstream, the supplement yields to it; explicitly reviewed possible-overlap cases are conservatively linked to one sample.

The September25 review added Idaho ATR, Virginia TPSI May/June, and an additional South Carolina Impact release. South Carolina's two overlapping August releases share a sample identity, so they do not create two independent sample contributions. Idaho's missing July Change Research sample size is repaired from the original release while preserving the blank upstream field.

Explicit question reviews distinguish initial, informed, conditional and ambiguous results. An informed headline does not mean every question in that release is informed: Idaho's June Bullfinch initial ballot remains usable. Source changes to reviewed answer values invalidate the review instead of silently reusing it.

Known publication/archive dates constrain cutoff replays. For the June Virginia supplement, exact fieldwork dates were unavailable; June16 publication is recorded as a conservative upper-bound date and flagged. Virginia sample sizes use the original crosstab's unweighted counts (May703, June663), with its differing headline weighted counts documented in the ledger. These qualifications remain visible in the audit.

## Audit scope

Every source question remains available, including exclusions. Model sample counts collapse repeated question/population versions and the reviewed overlap group. Older polls remain usable with age weighting; the14-day ingestion summary and30-day watchlist windows do not delete them. The audit checks every Senate state for missing dispositions, invalid margins/sample sizes, rejected scenarios entering inference and observations after the cutoff.

Historical training data and fitted parameters are unchanged. Legacy current-forecast machine fields `dem_share`, `dem_rep_margin`, and `p_dem` use the D/Independent convention. Literal Democratic-party prediction-market contracts must still respect actual candidate affiliations; an independent win is not automatically a Democratic-party contract win.

The source inventory is not guaranteed to contain every public poll. A state without rows is reported as no source polling, not evidence that no poll exists anywhere. New unreviewed contenders remain visible for review.
