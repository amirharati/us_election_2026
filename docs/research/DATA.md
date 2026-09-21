# Data sources and contracts

> **September 16 update:** the full 2018–2024 polling archives have been recovered and normalized. See [DATA_GAPS.md](DATA_GAPS.md) for revised coverage, source overlap handling, preparation steps and remaining gaps. Older counts below describe the original September 14 snapshot.

## Historical downloader

`scripts/download_historical.py` collects:

| Source | Contents | Use |
|---|---|---|
| [FiveThirtyEight pollster-ratings archive](https://github.com/fivethirtyeight/data/tree/master/pollster-ratings) | Individual historical polls with linked actual margins; raw file preserved across offices; Senate/general and generic-ballot extracts | Error calibration |
| [MIT Election Data and Science Lab Senate results](https://doi.org/10.7910/DVN/PEJ5QU) | Statewide Senate returns, 1976–2024 in the release checked September 14 | Results including unpolled races; prior training |
| [MIT Election Data and Science Lab presidential results](https://doi.org/10.7910/DVN/42MVDX) | State presidential returns, 1976–2024 in the checked release | Lagged state partisan lean |

FiveThirtyEight attribution: CC BY 4.0. MIT datasets declare CC0 1.0 in their
Dataverse metadata; preserve scholarly attribution nonetheless. The downloader
resolves the latest released dataset, records its version/file ID and keeps
metadata, codebooks and source lists alongside raw bytes. It checks for all-state
coverage and results through at least 2024, rather than trusting dated catalog titles.

The checked historical polling archive has 5,006 Senate general-election records
from 1998 through 2022 (including some odd-year specials), at median-field-date
horizons from 1 to 61 days. It does **not** supply 2024 Senate polls. Result
availability through 2024 does not make a 2024 poll-based backtest available.
Use 2020/2022 as held-out candidates and earlier training/validation cycles;
2024 polling can be a later source addition. Audit actual horizon coverage first.

Result files are preserved and converted to readable CSV, **not automatically
collapsed to one row per contest**. The source codebook warns that candidates
may have multiple party lines, and uncontested races may have placeholder vote
totals of 1. Stages, voting modes, special elections, two seats in one state,
runoffs and independent candidates require deliberate reconciliation. Some
codebooks retain older year ranges in their prose; the metadata/data determine
coverage. Do not sum repeated totalvotes or mix mode totals with their components.

Presidential results must include DC when constructing national vote totals, but
DC is not a Senate prediction target. State partisan lean for a historical
forecast uses a **previous** presidential election, never the same year's result.

## 2026 downloader

Primary source: [New York Times public Senate CSV](https://www.nytimes.com/newsgraphics/polls/senate.csv).
The [NYT polling tracker](https://www.nytimes.com/section/polls) declares the data
CC BY 4.0; attribute The New York Times. The export is multi-pollster data, not
just Times/Siena surveys. It contains candidate/answer rows, not one row per poll.

`scripts/download_2026.py` preserves the full raw export and produces a broad
2026 Senate general-election extraction. Other cycles and primaries are excluded
from this extract but retained in raw data. General/runoff stage variants are
accepted; if new stage labels appear they must be reviewed in summary counts.
Candidate names, IDs, poll/question IDs, populations, source URLs, dates,
partisan/internal and ranked-choice fields remain intact.

The snapshot coverage report has one row per configured contest, including
zero-poll contests. Counts mean **source coverage before nominee and population
review**, not usable sample size. General-election polls can test alternative
nominees or subpopulations; empty hypothetical flags do not establish validity.
Do not convert "Don't know" into a candidate, double-count questionnaires, or
silently interpret two-candidate questions as complete multi-candidate ballots.

Optional source with `--include-generic-ballot`: Silver Bulletin's public CSV,
linked from its [generic-ballot dashboard](https://www.natesilver.net/p/generic-ballot-average-2026-nate-silver-bulletin-congress-polls).
This is a separate file and is not used by the first model automatically. Preserve
attribution; a redistribution license was not separately established. For our
own model use raw dem/rep figures, not the publisher's adjusted values or influence
weights as if they were new independent evidence. The flag must be supplied on
each refresh that should include this input; omitted files are not silently
carried forward and presented as freshly downloaded.

## Snapshot semantics and integrity

- `manifest.json` records per-file SHA-256, byte count, source URL and retrieval
  timestamp; Dataverse records additionally include version and license metadata.
- Raw files are preserved byte for byte. Derived CSVs and summary/config files
  are hashed too. A failed refresh does not replace `latest.json`.
- Each new bundle is immutable; a JSON pointer is updated with an atomic rename.
  The lock prevents simultaneous writers to one output directory.
- `changes.json` compares grouped **whole poll IDs** in the current general
  extract: all questions/answers and duplicate multiplicities are preserved when
  detecting revisions. Added/removed IDs can reflect source ID changes or filter
  eligibility changes, not necessarily newly conducted/withdrawn surveys.
- Full-source byte changes, metadata revisions or config changes can create a
  snapshot even if the general-election poll-change counts are zero.
- Retrieval time, poll field dates and first publication time are different.
  Re-running today cannot recover the source as it appeared last month.
- No API key or subscription is required. New schema omissions, malformed/empty
  tables, invalid current percentages/dates and unexpected current states fail
  explicitly instead of becoming plausible-looking empty datasets.

## 2026 manifest provenance

[270toWin's 2026 Senate map](https://www.270towin.com/2026-senate-election/),
checked 2026-09-14: 33 class-II seats and class-III specials in FL/OH; 22 currently
R-held and 13 D-held. The versioned config is a manually checked ballot inventory,
not a live candidate feed. Recheck new special elections, continuing-seat changes
and nominees before forecasts. The script rejects unexpected states; two contests
in one state would require source race-ID mapping instead of state-only coverage.

## External checks, not independent observations

[Race to the WH](https://www.racetothewh.com/senate/26polls),
[RealClearPolling](https://www.realclearpolling.com/latest-polls/senate), and
[270toWin](https://www.270towin.com/polls/latest-2026-senate-election-polls/)
are useful checks for missing polls and state estimates. Their averages overlap
in underlying polls. Never combine them with component polls as independent data.
FiftyPlusOne has structured paid downloads; DDHQ, VoteHub and Silver Bulletin
also publish averages. No paid access or complex scraper is needed for this lab.

## Before fitting

The initial implementation of the steps below now lives in
[PREPARATION.md](PREPARATION.md), with executable transformations, reason-coded
audit tables and [run results](PREPARATION_REPORT.md). Outstanding source
disagreements and election-rule exceptions are preserved for review.

1. Reconcile full historical result contests and verify coverage against the
   election schedule, including specials and runoffs; availability of an archive
   is not proof every relevant contest is correctly represented.
2. Join polls to those contests with dates/candidate identities/seat distinctions.
3. Audit current nominee matchups, independent candidates, survey overlap,
   demographic subgroups and likely/registered-voter preference.
4. Construct lagged features, election-type/party metadata and forecast cutoffs.
5. Choose explicit winner/caucus rules and historical evaluation splits.

Raw download tables are acquisition/inventory. Prepared baseline eligibility is
a separate, conservative decision; it does not certify a full seat forecast.
