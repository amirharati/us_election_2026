# Data acquisition, preparation and live updates

The supported runtime now uses self-contained `data/compact/frozen/` and
`data/compact/current/`; raw acquisition and the full research preparation
lineage below are optional audit workflows. See [compact ingestion and storage](GIT_STORAGE.md).

## Reproduction snapshot versus live snapshot

The frozen reproduction uses audited inputs as of September 17, 2026, including
the later review of historical official results. It never follows a live pointer.
Live runs use newly acquired/cached sources and today's cutoff, writing a new
versioned dataset and forecast. No 2026 labels are present in either path.

The package includes raw/provider provenance, the official-result review evidence,
acceptance policies, selected native feature tables, final aligned tables and
training views. Large optional source archives unused by these final models were
omitted. Their original download adapters remain available. Native table values
were not changed when constructing the smaller package; source manifests and the
subset operation are recorded.

## Sources used by the supported live workflow

| Input | Provider / original source | Refresh policy |
|---|---|---|
| Current Senate polls | New York Times public Senate CSV | Check each live run, successful-check cache 6h |
| Generic ballot auxiliary archive | Silver Bulletin published sheet | Acquired with polls; not a separate Senate outcome |
| CPI, gasoline CPI, income, unemployment, GDP, financial series | FRED distributions of BLS/BEA/Fed series | Check/cache; preserve earlier verified values on failure |
| Consumer sentiment and finances | University of Michigan | Discover current publisher spreadsheets |
| Presidential approval, including party groups when available | American Presidency Project, UCSB | Current table plus retained historical presidents |
| Market returns | Kenneth French library | Daily/monthly provider archives |
| Market stress | CBOE VIX history | Provider daily data |
| Geopolitical risk | Caldara/Iacoviello GPR | Provider workbooks |
| Economic policy uncertainty | PolicyUncertainty.com | Monthly/daily/categorical provider data |
| Infectious-disease news stress | PolicyUncertainty.com infectious EMV | Provider index |
| COVID policy | Oxford OxCGRT | Completed historical archive, no invented 2026 feed |
| Historical polls/results | FiveThirtyEight/ABC archive, MIT Election Lab Dataverse, reviewed official results | Frozen reviewed training set; separate acquisition command |
| Political control | Reviewed House/Senate/presidency sources | Dated local policy, not inferred from polling |

Exact URLs, retrieval timestamps, hashes and available source-license annotations
are stored alongside the raw snapshots and in `scripts/feature_sources.py` and
`scripts/download_historical.py`. Public availability does not give this package
authority to relicense provider data. Keep source attribution and check the
provider's terms before redistributing data externally. The package contains no
API keys or paid-source access credentials; optional adapters requiring access
remain opt-in.

## Cleanup contract

1. **Download immutably.** Validate required fields, numeric ranges, dates and
   source schema. Record added, removed and revised poll IDs. Preserve the prior
   snapshot on errors; identical content reuses the existing snapshot.
2. **Normalize answers and elections.** Keep candidate answers, parties and
   denominators; compute D-minus-R without silently assigning independents to D
   or converting to two-party shares. Preserve missing sample sizes.
3. **Review identity and eligibility.** Resolve pollster/sample identifiers,
   superseded records and known duplicates. Match dated leading-contender policy;
   unfamiliar/former contenders remain quarantined rather than being automatically
   admitted. Keep an audit trail for all exclusions.
4. **Resolve target labels separately.** Reviewed official outcomes are not poll
   predictors. Historical excluded contests and fixed completion assumptions are
   visible. Current targets have missing outcomes. The national auxiliary House
   series is not treated as a Senate national popular-vote target.
5. **Deduplicate sample versions.** Prefer full sample and the explicit population
   ordering. Average tied accepted versions. Filter field/release dates before the
   cutoff, and admit only the two-calendar-year polling cycle.
6. **Prepare features natively.** Keep source dates, reference-period boundaries,
   units, explicit missing values and provenance. Percentages are converted using
   documented source units; index growth is proportional. Missing is not zero.
7. **Align dated contexts.** Use the last eligible completed reference period,
   required lag/delta endpoints and staleness limits. Store reference-date and
   strict observed-by-cutoff views separately. Feature imputation happens only
   inside training-fitted model transformations.
8. **Verify joins and counts.** No many-to-many poll expansion, duplicate target
   keys, future outcome leakage or dropped current unpolled states. Reconcile
   exactly 100 seats. Source and output manifests protect each step.

The live source audit can show many source polls but fewer modeled samples:
candidate restrictions, duplicated versions, release dates, current-cycle windows
and independent-candidate cases account for the difference.

## Date semantics and political carry-forward

`as_of` is the evidence cutoff, not a claim that all inputs were observed that day.
Every live run records download/check status, latest source dates, dataset hash
and the numerical model checkpoint. Model fits remain trained through 2024.

The party-control source was reviewed through September 17. For live dates after
that review, this 2026 package explicitly carries its last known party-control
configuration forward when making current feature scores. The forecast metadata
sets `political_context_carried_forward=true` and retains the actual review date.
This is a scenario assumption, not a fresh verification. Update
`config/political_context_v1.json` with new evidence if officeholding/control
changes. Aligned source tables themselves still mark out-of-review context as
missing; carry-forward occurs only in the live modeling context.

Current candidate/caucus proxies for ID/MT/NE/SD and other election-rule flags
remain research assumptions. A new contest roster raises an error rather than
reusing an incompatible state vector. A new unknown candidate is quarantined;
the cache does not silently update the human-reviewed candidate policy.

## Cache/failure behavior

- Default TTL is six hours since a **successful source check**, with matching
  manifest hash. Cache age is inspected every notebook run.
- `--force` checks all active sources again. `--offline` never accesses the network.
- On a source failure, use a verified cache and record `stale_cache_after_failure`.
  Failure does not advance the successful-check timestamp. `--strict` rejects it.
- Preparation cache keys include source hashes, cutoff and preparation code.
  The complete validated source snapshot is rebuilt when evidence changes.
- Forecasts are recomputed from the selected dataset. A failed run records its
  failure and does not replace the previous successful forecast pointer.
- A lock prevents concurrent refresh writers. After an interrupted process,
  confirm no refresh remains running before removing `cache/.live.lock`.

During packaging the online test downloaded Senate polls through September 18:
17 added polls and 2 revised polls relative to the frozen raw snapshot. Eight
active source checks succeeded or were unchanged; FRED failed and used its
verified cache, including the reviewed gasoline addition. This is recorded in
the saved live run; it is not described as a fully fresh economics dataset.

## Historical rebuild and updates

`python run.py download-history` acquires raw history independently. Publisher
revisions do not automatically overwrite reviewed historical labels or trained
checkpoints. For scientific reproduction use the bundled reviewed snapshots.
For a new historical-data edition, run the supplied preparation/audit modules,
review changed results/candidate mappings, rebuild training views, and publish a
new explicit model version. This 2026 release is not an automatic 2028 pipeline.

The supporting cached preparation script can regenerate accepted/feature/aligned
data from the included raw sources without the parent lab. Main numerical
training can be rerun from the included audited state-cycle histories and
training blocks. Original arbitrary research-grid builders are retained as code
context but are not the supported standalone interface.
