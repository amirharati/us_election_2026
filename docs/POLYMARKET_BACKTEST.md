# Historical Senate prediction comparison

[Notebook 12](../notebooks/12_historical_polymarket_backtest.ipynb) compares our models, published forecasts and Polymarket with the final election result. It measures forecast accuracy and distance from the market. It also includes an exploratory long-shot exit-price proxy study; it does not establish executable trading returns. [Latest report](../outputs/reports/research/polymarket_history/report.md); daily copies live under `outputs/reports/history/YYYY-MM-DD/polymarket_history/`.

## Reproduce the analysis

```sh
# First run: download public inputs, rebuild the archive, and run inference.
.venv/bin/python scripts/prepare_historical_markets.py
# Later runs: use downloaded data and cached dated inference.
.venv/bin/python scripts/polymarket_backtest.py
.venv/bin/python scripts/run_notebooks.py --start 12
```

Downloads and model inference are independent. The notebook has explicit public-market and publisher refresh switches. `prepare_historical_markets.py --offline` reconstructs from existing download caches. Optional original archived prices can be restored with `--remote-prices idea`; public trade and CLOB sources work without that private SSH host. No API key is required for public sources, and no AI calls are used.

`historical_model_forecasts.build_forecasts(force=True)` explicitly recomputes inference. Normal reruns reuse caches only when source-code, frozen model assets, configuration and compact-input fingerprints match. Updating market or publisher prices alone does not rerun local inference.

## Models and dated evidence

| Code | Model |
|---|---|
| GB | Gaussian Bayesian |
| ST | Matched Student-t |
| MX | Four-model predictive mixture |
| M10 | Mixture with its mean shifted 10% toward polling |
| 538 | FiveThirtyEight Deluxe, archived 2022 |
| RTWH | Race to the WH, archived 2024 |

M10 is not a ten-percentage-point probability shift. Our four models are freshly inferred for June 1, July 1, August 1, September 1, 5, 15, 17 and 20, October 1, 15 and 31, and November 3 in both cycles. Missing local forecasts are never interpolated or carried forward. The actual Student-t samplers and their convergence checks run for both Student-t components. The mixture uses the full component distributions.

Each run retains the frozen September 17 calibration and fits trained only on cycles before the target election. Keeping the fit fixed makes changes across dates reflect new evidence. Calibration at other horizons is not separately validated. The September 17 Gaussian reconstruction reproduces the original saved forecast. Outcomes for the target election are hidden during inference and restored afterward for evaluation.

Polls ending after the cutoff and known later releases are excluded. Missing release dates use field-end dates; many historical polls lack known release dates. Features use dated reference periods but latest-vintage revisions. These forecasts are retrospective reconstructions, not a pristine replay of publications available then. Model architecture was developed later, so this is not an untouched holdout.

Third parties use the latest available snapshot on or before each check date, at most six days old. Actual snapshot dates are shown. Published histories may also have been revised. No third-party model is reconstructed from invented parameters.

## Historical market probabilities

`historical_market_prices.py` replays 2022 binary constant-product pools in block/log order. Funding adds/removes actual outcome-token amounts. Buys add cash net of fees to both reserves and remove purchased shares; sells remove cash plus fees and add sold shares. The marginal first-outcome probability is `reserve_1 / (reserve_0 + reserve_1)`. All 42 final balances match the source snapshot exactly. Final balances validate the replay; they are not used as earlier probabilities. Drained pools emit missing values; zero-amount events do not refresh a quote.

2024 source priority is original archived daily price history, public CLOB daily history, then the last on-chain execution proxy. Sources are identified per state. An execution proxy can include slippage and need not equal a quoted probability. None of these are historical executable bid/ask quotes.

For each check date, take the last observation strictly before the following UTC midnight, no more than seven days old. Never take a future quote. The tables show actual market time and age. This age rule is a transparent comparison assumption; it may leave sparse markets blank. New invalid pool observations are not skipped to resurrect an earlier valid quote.

## Accuracy, agreement and scope

Brier score is the mean squared error between predicted probability and the observed binary winner; lower is better. Gap is the mean absolute model–market difference in percentage points; lower is closer. Proximity alone does not establish predictive skill or profitability.

Each date compares models on the same priced states. State proximity rankings use dates shared by all available models in that state; the overall proximity ranking uses states shared by every model and gives those states equal weight. Counts are shown. Coverage varies across dates, and repeated dates reuse the same outcomes. These are descriptive small-sample comparisons, not independent repeated elections.

Only reviewed general-election Democratic party-win contracts enter this view, with one deterministic contract per state. Explicit independent, candidate-only, special/runoff, margin, seat-count and chamber-control mappings stay in the audit. Independent winners are not silently relabeled Democrats. Overall accuracy means accuracy across states, not Senate-control probability. The Senate-control adapter needs joint assumptions, including the vice presidency in 2024.

Final election labels come from saved outcomes and are used only for scoring. Conflicts with available resolved market payouts are flagged and excluded from scoring. Recoverable/resolved-market selection can introduce survivorship bias.

## Local files and Git

All raw downloads, research tables and inference caches remain Git-ignored. The notebook, Markdown reports and charts are tracked.

- `outputs/results/research/polymarket_history/dated_forecasts.parquet`: four local models at every cutoff.
- `historical_inference/YYYY-MM-DD/`: cached predictions, poll audit, feature ledger, sampler diagnostics and source fingerprint.
- `prediction_prices.parquet`: documented historical price sources.
- `date_samples.parquet`, `date_sample_overall.parquet`, `state_proximity.parquet`: comparisons and scores.
- `date_sample_availability.parquet`, `mapping_audit.parquet`: missing-model and contract-mapping explanations.
- `outputs/results/research/senate_archive/pool_reconstruction_audit.parquet`: exact pool-balance reconciliation.

Older `forecasts.parquet`, `pairs.parquet` and `scores.parquet` may remain from the previous two-cutoff analysis. Notebook 12 uses the dated files above. The legacy explicit-signal utility remains available in code, but this notebook does not invoke it.

## Recovered on-chain archive for both cycles

Run `.venv/bin/python scripts/download_senate_archive.py` to collect the relevant original trade events from the public [Envio archive](https://huggingface.co/datasets/moose-code/polymarket-onchain-v1). No API key is required. The script pins the source revision, checks complete file downloads, matches exact pool addresses or outcome tokens, and resumes from checksummed Senate-only extracts. It scans all legacy FPMM partitions and CLOB partitions from inception through December 2024. Both named outcomes and post-election observations are retained. Senate primaries are labeled separately and do not enter the general-election comparison.

The optional `--scan-remote idea` performs a read-only scan of the original Gamma metadata archive on that SSH host. Discovery found three additional Missouri primary contracts and a previously excluded Georgia runoff-occurrence contract. House/presidential combinations, appointments and chamber-leadership contests remain excluded. Deleted or misdated markets may still escape discovery; the source snapshot and scope exclusions are explicit.

Add `--remote-prices idea` to copy the original Senate-only price histories from that host. The complete observations stay compressed in the ignored cache, while `archived_daily_prices.parquet` and `archived_price_coverage.parquet` preserve daily observations and per-outcome counts. This optional source is independent of the public on-chain download; the server is never modified.

- Original selected events and download receipts: `cache/polymarket_history/senate_archive/selected/` (ignored by Git).
- Full normalized event observations: `cache/polymarket_history/senate_archive/observations.parquet` (ignored by Git).
- Git-ignored market metadata, daily observations, summary and per-market audit: `outputs/results/research/senate_archive/`.
- [Latest archive coverage report](../outputs/reports/research/senate_archive/report.md), also regenerated under `outputs/reports/history/YYYY-MM-DD/senate_archive/`.

The all-market monthly source files are discarded after the exact Senate rows have been validated and saved. The manifest preserves their hashes and immutable URLs. Attribution: Envio, CC-BY-4.0.

For legacy transactions, cash per share preserves the actual buy payment or sell receipt. The fee-adjusted price subtracts fees on buys and adds fees back on sells before dividing by shares. It is an **average transaction price**, not the pool's marginal price or a historical bid/ask quote. Exchange records retain original fill fields; derived prices use collateral/token fills only. Matching-engine counterpart events must not be summed as independent trading volume. Daily tables retain each outcome's last observed event and its real UTC timestamp, without filling missing days.

Notebook 12 now uses the reviewed pool reconstruction and archived-price adapter described above. Full source coverage remains separate from the narrower set of supported model comparisons.

## Why the original price endpoint omits 2022

The September 25 audit checked all 18 relevant 2022 contracts. Gamma identifies all of them as legacy fixed-product liquidity-pool (AMM/FPMM) markets with market-maker addresses and positive trading volume. The CLOB market lookup returns404 for their condition IDs, and both CLOB history and the newer Data API's permanent12-hour history return no prices. These contracts traded, but the CLOB downloader has no legacy AMM-history adapter (the separate pool replay now supplies these prices). This is recorded as `legacy_amm_history_required`, not evidence that the markets never had prices.

The official Data API v2 documentation describes its permanent coarse price series as starting November18,2022, after the November8 general election. The legacy The Graph endpoint could not be reached; Goldsky's public FPMM endpoint explicitly returned `ENDPOINT_DEPRECATED`. Its replacement API requires a Goldsky key and documents activity, balances, positions and blocks, but does not advertise a legacy AMM price-history route. The separate Envio archive above supplies the original trades that these endpoint probes did not recover.

The seven other gaps were2024 Arizona margin contracts that opened November8, after the November5 election. Their later price history exists. They are correctly outside a pre-election test and now labeled `opened_after_cutoff`.

Run `scripts/diagnose_polymarket_history.py --refresh` to repeat market-level probes. Receipts stay in the ignored cache; `history_diagnosis.parquet` preserves compact evidence. Source definitions: [official Data API v2](https://data-api.polymarket.com/v2/docs), [official FPMM schema](https://github.com/Polymarket/polymarket-subgraph/blob/main/fpmm-subgraph/schema.graphql), and [replacement API specification](https://edge.goldsky.com/data/openapi.json).

## Rebuild after cloning

Use the project Python environment and run:

```sh
.venv/bin/python scripts/prepare_historical_markets.py
.venv/bin/python scripts/run_notebooks.py --start 12
```

The first command downloads daily market history, archived publisher forecasts and Senate-only on-chain events, then rebuilds the research tables and reports. It uses the saved local-model portfolio already in the repository; it does not train models or call AI. Public sources require no API key. The initial public archive scan transfers about 4 GB, filters to Senate records and removes unrelated partitions. The Envio snapshot revision is fixed in `config/polymarket_archive.json`. Gamma and publisher endpoints can change; their retrieved source hashes are recorded.

To rebuild generated tables from existing caches without network requests:

```sh
.venv/bin/python scripts/prepare_historical_markets.py --offline
```

The optional original 68.5-million-observation price archive comes from the user's `idea` server. To reproduce that additional source, use `--remote-prices idea` on the prepare command. It requires that SSH archive; it is not bundled in Git or guaranteed to match a fresh public API download. When already cached, offline preparation rebuilds its daily summaries too.

Both `outputs/results/research/polymarket_history/` and `outputs/results/research/senate_archive/` are ignored in full, along with `cache/`. Scripts, source configuration, reports and notebook outputs remain versioned.

## Accuracy evolution and long shots

Notebook 12 and both report locations now include `polymarket_accuracy_evolution.py` outputs. The main panel holds states and model availability fixed across all eight check dates from September 5 through November 3. It retains eight 2022 states and 26 2024 states; excluded states are listed. Earlier June-to-November charts remain coverage-varying comparisons, labeled accordingly.

Fixed cohorts use September 5 market probabilities: competitive races have P(D) between 30% and 70%, while long-shot races have either side at 10% or less. A separate final-margin-within-five-points cohort is explicitly hindsight-only. All models score the same events. State tables show Brier scores at each date; lower is better.

Dynamic long-shot tables apply the 10% threshold anew at each date on the shared same-date panel. They compare predicted upset counts (sum of each model's probabilities for the market-defined underdogs) with actual counts. Counts and membership vary across dates. No eligible cohort is treated as unavailable, not as zero error. No model-specific selection or winning-trade filter is used. Long-shot Brier equals favorite Brier, so rare-event calibration needs more evidence than a low average score. Repeated dates do not create independent elections. No profitability claim follows from these accuracy scores.

Generated `accuracy_evolution_*.parquet` files stay in the ignored historical research folder. Corresponding figures, notebook output and Markdown summaries are saved with the reports.

## Long-shot price paths before resolution

`polymarket_longshot_paths.py` is an exploratory test separate from election accuracy. It uses every existing check date before November 3, first observed entry prices within 36 hours after the forecast date ends, a 1–10 cent entry band, and a model value at least two cents higher than entry. All compared models must be available for the same opportunity. Final outcomes do not select entries. Republican sides use complementary first-outcome price proxies.

The preset exit rule takes profit at twice entry if a later daily observation reaches that target before November 3 00:00 UTC. The assumed sale price is the target, never the observed peak. Non-hits use the last pre-deadline observation no more than seven days old. Missing/invalid paths remain unscored, with counts. The summary compares every model's selections against all eligible long shots. It also shows nonselected cases' direction, and 7/14/30-day positive-move rates with sample counts. Short horizons exclude observations after the requested horizon and require a prior quote within two days.

Target persistence means two consecutive available observations at or above target, at most two days apart. This sensitivity exposes isolated spikes; it does not prove fills. Recorded prices can jump sharply in thin markets, and neither daily history nor market-implied probability supplies historical bid/ask depth. The plotted signals are not actual trades. Intraday opportunities can also be missed by daily sampling.

Cost assumptions are zero, one or two cents per share for the entire round trip. These are illustrative sensitivities, not estimated fees. Equal-share average changes do not account for capital reuse or form a portfolio return. Repeated entry dates overlap and refer to few unique markets. Parameters have not been optimized or validated out of sample. A model's settlement probability is not its forecast of a temporary price doubling.

[Polymarket's early-sale explanation](https://help.polymarket.com/en/articles/13364247-can-i-sell-early) describes selling at the prevailing bid or placing a limit order. That ability does not establish that an archived price was executable. All generated `longshot_paths_*.parquet` files remain Git-ignored; notebook tables, charts and dated Markdown reports are retained.

## Independent-model positive-EV strategy

`polymarket_edge_strategy.py` implements the simple baseline in notebook 12. Each model operates independently across every supported state-win contract it can forecast. It does not require another model to agree or have coverage. Both YES/D and NO/R sides are considered. Enter only when the model's probability exceeds purchase price plus assumed per-side execution cost. No extra two-cent edge threshold is imposed.

The base run uses 100 shares, 0.5 cents cost per side, and one open position per model/market. Zero and one cent per side are sensitivities. The simulation starts June 1. Forecasts are available the day after their date. Our model stream uses the saved 12 historical inference dates; publishers use their available historical daily/periodic series. The last known forecast persists until the next update. This is a discrete-update strategy, not daily model inference.

Exit when net sale proceeds reach the latest model valuation; this can be a loss when a forecast changes. The separate profit-target variant also closes at a 20% net gain. Confirmation sensitivity requires two consecutive edge-exit observations within two days and executes at the second observation. There is no re-entry on the same quote. Later entries are allowed and charged again.

No new positions open during the final 24 hours before the general election. Remaining positions are marked closed using the last usable pre-election price at most three days old. This terminal valuation is applied after chronological decisions; the identity of the last available quote is never used to filter earlier entries. Missing final prices stay unscored. Hold-to-close and known-payout hold-to-settlement comparisons use the same purchased lots. They are counterfactuals with potentially overlapping holdings, not capital-constrained buy-and-hold portfolios. Missing resolved payout metadata remains missing (not replaced with guessed settlement).

All price bands are based on the purchased side's entry price. Notebook/report summaries include per-model P&L, counts, state results, probability-band results, paired hold comparisons, execution-cost sensitivities, confirmation sensitivity and every main-rule trade. Source dates, model values, EV, turnover and all variant trades are in ignored `edge_strategy_*.parquet` files, with assumptions in `edge_strategy_config.json`.

Archived daily prices and complementary side prices remain proxies. Sudden jumps, depth, spread and fill uncertainty can materially affect exits. No model's historical P&L establishes future profit. Model coverage and forecast update frequency differ, and fixed shares imply unequal dollars at risk. Profit totals are not matched-universe rankings, account returns or statistically independent trials.

### Older models and third-party strategy comparisons

The independent-model strategy also includes **OG**, the older Gaussian architecture, and **OS**, the older Student-t research architecture. Both are rerun at the same 12 historical cutoffs with their frozen earlier-cycle fits and the same dated polling evidence. Their predictions were already used as mixture components; they are now retained as standalone historical inference outputs. ST continues to mean the matched Student-t model. The existing probability-accuracy and long-shot sections retain their four-model selection; the strategy section has its own complete eight-code legend including publishers.

Available publisher archives are FiveThirtyEight Deluxe for 2022 and Race to the WH for 2024. We do not have these same publishers for both cycles in this dataset. Full-coverage trading results retain each model's own available states and update frequency. A separate post-hoc same-state summary restricts results to states covered by every compared model:11in2022 and26in2024. This does not filter trade entries by model agreement, and it does not equalize publication schedules, position counts or dollars deployed. OG/OS and the mixture are related forecasts, not independent validations.

## Sustained signal quality (not execution)

Notebook 12 now places a signal-quality study before the older trading experiments.
Run `PYTHONPATH=.:scripts .venv/bin/python scripts/polymarket_signal_publishers.py`
to download additional publisher histories separately. Add `--offline` to rebuild
from cached responses. Normal notebook reruns reuse them; `DOWNLOAD_PUBLISHERS=True`
refreshes the collector. No AI calls are needed. Raw responses and research tables
stay under ignored cache/results directories; dated Markdown and PNG reports are
saved under `outputs/reports/history/YYYY-MM-DD/polymarket_history/`.

Each local model is evaluated independently at the same twelve check dates.
Publisher snapshots must be at most six days old. Entry is the first observation
within 36 hours after the check date ends. Signals have positive model probability
minus market price. No costs, sale timing, or realized profit are assumed.
The primary target is a rise of at least the initial edge and at least 2 cents,
lasting across three consecutive observed days (at least 36 hours). No gap can
exceed 36 hours. An isolated peak cannot qualify. Forward windows are 7, 14, and
30 days; full-window scoring requires 80% daily coverage and a fresh endpoint.
Post-election or incomplete windows are unscored, including sparse 2022 paths.
No forward-filling is used to manufacture persistence.

Reports include target rates, largest sustained rises, endpoint changes, time to
qualify, prior adverse moves, equal-market averages, initial-price/edge/activity
bands, state tables, pairwise matched market/date comparisons, and sensitivity to
1/2/3-cent floors and 2/3/5 observations. A nonpositive-edge baseline matches the
same model, cycle, horizon, month and 5-point starting-price bin, excludes the same
market, and applies the positive signal's exact target to its controls. At least
three controls from two other markets are required. Missing matches stay blank.
Repeated dates are correlated; no statistical significance or validated winner is
claimed. A larger model edge sets a harder target, so target rates alone cannot
rank models.

Activity counts CLOB transaction hashes (deduplicating counterpart events) or
legacy trade events during the preceding seven days. It is not order-book depth.
Final lifetime volume is never used to classify historical signals. Unknown
archive coverage is distinct from zero recorded activity.

Publisher coverage is explicit in `signal_publisher_status.parquet`:

- 538 Deluxe, Classic and Lite in 2022, after the June 30 launch documented in
  [the publisher's methodology](https://fivethirtyeight.com/methodology/how-fivethirtyeights-house-and-senate-models-work/).
- RTWH 2024 dated state history. Its 2022 trend feed currently returns 404; this
  does not establish that no other archive exists.
- Economist original 2022 probabilities for AZ, GA, NV and PA. Start conservatively
  September 7, the date of [the publisher's model announcement](https://shows.acast.com/theintelligencepodcast/episodes/americas-next-top-model-predicting-the-midterm-results).
  Stop before October 31. The [official change archive](https://github.com/TheEconomist/us-midterms-2022-change-data)
  includes corrected back-history; that version is never backdated into signals.
- DDHQ original 2024 (DDHQ0), through the July suspension, and revised 2024 (DDHQ),
  conservatively from August 27. The official state page's public JSON contains
  Republican win probability, converted to Democratic probability using the same
  `1 - prob` conversion as its chart. The original and revised versions remain
  separate; missing dates are not interpolated. Example source:
  [DDHQ Arizona](https://elections2024.thehill.com/forecast/2024/senate/arizona).
- A usable 538 2024 dated Senate series has not been recovered. The tested archive
  response and other retrieval attempts are recorded in the ignored cache.

All publisher series are retrospective archives, not independently verified daily
publication snapshots. Local inference is also retrospective with frozen fits and
latest-vintage limitations described above. The study detects sustained favorable
setups in historical price proxies; it does not establish executable profits.

### Sparse publisher snapshots

A supplemental native-date panel evaluates every recovered third-party snapshot on
its actual forecast date, independently of the twelve common check dates. There is
no minimum number of forecasts or markets. Single-date and limited-market samples
are labeled. It uses the same June-to-election research season, publication/version
restrictions, post-forecast entry timing, and 3-day/max(edge,2c) target.
An actually observed sustained target can be reported even if the full 7/14/30-day
window is incomplete or reaches election day. Such confirmed setups are separate
from full-window rates. Incomplete paths without a witnessed target are Unknown,
never failures. The matched comparison remains unchanged. Daily snapshots overlap
and cannot be counted as independent trading opportunities. Exact forecasts and
source URLs are preserved in `signal_quality_native_detail.parquet`; summaries
and exclusion audits are regenerated by the notebook without AI calls.

### Relative rise targets

The signal study also evaluates relative price increases of 5%, 10%, 20% and 50%,
each with a 2-cent minimum: `max(entry_price * return_fraction, .02)`.
Positive model edge remains the signal-selection rule. These targets do not also
require covering the whole edge. The original `max(edge, .02)` target remains
separately labeled Edge. Three observed daily values must sustain every target.
At a 10-cent entry the first three relative targets all require a 2-cent rise;
at a 50-cent entry, 5% requires 2.5 cents and 10% requires 5 cents. An unattainable
target above $1 is counted and not removed from the denominator.

Both shared-date and native publisher panels receive the same target grid, with
7/14/30-day summaries, initial-price bands, activity and state tables. Full-window
rates and observed partial-window setups remain separate. These are hypothetical
price rises, not executed returns. The preexisting matched-control lift applies
only to Edge; no new control-lift claim is made for the percentage targets.

### Combined available-model tables

The complete comparison in notebook 12 and `all_models.md` puts local and third-party
models in the same tables, without requiring common dates, markets or sample sizes.
Local rows use the twelve reconstructed cutoffs; publisher rows use native dates.
Publisher shared-date rows are excluded to avoid counting their signals twice.
Every model code stays visible, with unavailable rows blank. Overall tables cover
7, 14 and 30 days. Thirty-day subsets cover starting probability, strictly prior
trading activity, initial edge and state. Publisher activity is calculated on its
own snapshot's reference time, using the same historical activity definition as
local models. Coverage and witnessed-setup tables accompany the full-window rates.
The combined view is descriptive and not a matched-universe model ranking.
Reports are saved both in the research report folder and the dated report folder.

### Notebook recovery and editor saves

Notebook 12 has a separate source copy in `notebooks/sources/`. The execution
runner checks it before running, keeps timestamped copies in the ignored
`cache/notebook_history/`, and refuses to replace a notebook changed during
execution. Successful saves use an atomic file replacement.

Save your editor before running the external script. Reload the notebook from
disk afterward if the editor still shows an older version; saving that stale
buffer can overwrite the file even after the script finishes. The runner cannot
control external editor saves, but detects source differences on its next run.

To recover notebook 12, run
`.venv/bin/python scripts/notebook_sources.py --restore 12`, then rerun it with
`.venv/bin/python scripts/run_notebooks.py --start 12`. Restoration preserves the
current disk copy and clears outputs for regeneration. If you intentionally edit
its code or text, save and review those changes, then use `--accept-current 12`
instead of `--restore 12`. Release source checksums must also be updated for
intentional source changes. Recovery copies are local and are not uploaded to Git.

### Reusable daily forecasts (before signal analysis)

Run `.venv/bin/python scripts/polymarket_daily_forecasts.py --download-publishers`
to build `outputs/results/research/polymarket_history/daily_forecasts.parquet`.
This single, Git-ignored table covers September 1 through election eve:
68 dates in 2022 and 65 in 2024. Normal reruns omit `--download-publishers` and
reuse valid per-day inference caches; `--force` recomputes local forecasts.

Each row identifies cycle, forecast date, state, regular/special race, model and Democratic win
probability, plus source type, provenance and availability status. All six
local models run daily over their supported historical race roster. Publisher
rows use actual archived dates, never interpolation or carry-forward. Missing
model/state/day combinations remain explicit, including unavailable publisher
series. Publisher archive validity restrictions still apply. No final outcome,
market price, edge threshold or future-price coverage filter selects this table.

`available_after_utc` conservatively means after the labelled forecast day ends;
it does not assert a known publication timestamp. Dates before election day are
included, so an election-eve row becomes usable at election-day midnight UTC.
Any later trading study must enforce its own exact final pre-election cutoff.
Local forecasts remain retrospective reconstructions with frozen earlier-cycle
fits and September 17 calibration; feature publication vintages are incomplete.
Publisher archive dates do not independently establish original publication
vintages. State-level publisher rows do not resolve special-election or
independent-candidate contract definitions by themselves.

The checksum/coverage manifest is saved beside the table. A readable inventory
is saved as `daily_forecasts.md` in the latest and dated research report folders.
The existing twelve-date notebook signal results are not replaced by this
preparation step; a new signal design will consume the saved daily table later.

### Daily winner signal study

Run `.venv/bin/python scripts/polymarket_daily_win_signals.py` after building
the daily forecast table. Notebook 12 has a **Daily state-winner signals — current
study** section; its older twelve-date experiments remain explicitly labelled.
The new result lives in `daily_win_signals.md` in latest and dated report folders,
with ignored case-level tables under the research results directory.

Each compatible regular winner contract is oriented to Democratic win probability,
including Republican-first contracts. Models select their own positive-edge side.
Prices after forecast day end must arrive within36hours and before election-day
00:00UTC. Follow-up ends at that cutoff; no30day requirement applies. Three daily
observations spanning>=36hours, with gaps<=36hours, must sustain the target.
Full remaining paths need>=80percent daily coverage,>=3possible observations and
a fresh endpoint. Confirmed partial-path hits remain visible; missing or too-short
paths are not failures. Election-eve forecasts become available at the cutoff and
cannot initiate a pre-election signal. Fees and executable liquidity are not modeled.

Tables include coverage,5/10/20/50percent price-rise targets (minimum2c),the original
edge-sized target,states,starting-price/activity/edge/time-remaining subsets and
same-market/date paired comparisons. Episodes count consecutive same-side signal
dates within each model/contract; they do not simulate trades. Multiple contracts
and repeated dates for the same race are correlated. Full-path rates and lower-bound
confirmed/all-signal rates answer different questions. No model ranking should be
inferred without considering state/date coverage and time remaining.

### Debounced setups and hindsight path diagnostics

The primary section of notebook12 is now **Debounced winner setups — current
study**. Run `scripts/polymarket_debounced_signals.py` with the project Python to
regenerate it independently. The older daily-observation analysis remains
available and explicitly includes repeated signals.

One fixed reviewed winner contract represents each state/cycle: prefer D-first,
then lowest numeric marketID, without looking at subsequent prices or coverage.
At00:00UTC daily, use the latest prior quote no older than36hours and latest
already-available forecast no older than72hours from its labelled date. Preserve
publisher dates and reject superseded versions. Enter above2cedge; hold the same
setup until its edge is<=0 on two consecutive valid checks with distinct quote
observations. Unknown checks interrupt reset confirmation and never rearm a
setup. Re-entry can occur only on a later check after reset. This is one active
setup per model/race, including opposite-side signals; target hits do not rearm.

Measure paths from entry decision until confirmed reset or election-day00:00UTC.
Retain raw maximum, maximum sustained across3consecutive UTCdays, endpoint and
worst changes. Hindsight maxima do not represent executable returns. Full paths
need3possible days,80percentcoverage,andfreshendpoint. Summaries use full paths;
partial witnessed hits remain visible. Saved daily changes connect adjacent
observed dates without filling missing observations. Prices are pre-fee proxies;
there is no assumed realized trade,position size,or optimized exit.

Ignored `debounced_win_episodes.parquet`, `debounced_win_decisions.parquet`, and
`debounced_win_paths.parquet` contain setup records,state-machine decisions,and
daily price paths. Summary/subset tables and an input-checksum manifest are saved
beside them. `debounced_win_signals.md` is published in latest anddated folders.

Observed-max tables also retain partial windows with at least one qualifying
three-day sequence. They show the number of such paths and their observed maxima;
each observed maximum is a lower bound on the unknown full-path maximum. They
must not be confused with complete-path return summaries or hit-rate denominators.
