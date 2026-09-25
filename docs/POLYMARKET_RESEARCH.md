# Polymarket Senate research

Notebook11 discovers public 2026 U.S. Senate election markets and screens conditional gaps against the last verified Senate forecast. It does not place orders or refresh election inputs. No credentials are needed.

## Sources and discovery

The [public Gamma catalog](https://docs.polymarket.com/market-data/discover-markets) groups contracts into events. We paginate active, non-closed events for Midterms, US Elections, Senate Midterms and Senate Elections; deduplicate IDs; retain relevant open markets; and record every page checksum, tag, retrieval time and filter. The retained catalog includes only Senate winners, margins, relative results, control, seats and Senate-only combinations. Other offices, county results, turnout, primaries, leadership and price/forecast derivatives are excluded. An event groups related contracts: each margin band is a separate contract, while Yes and No tokens are two sides of that contract and are not counted twice. Event and contract counts are not race counts. The same scope filter applies to old caches and offline snapshots. Tag omissions and platform changes can leave gaps. A completed tag scan is not proof of universal coverage.

The catalog caches for 15 minutes. Online reruns always request fresh [CLOB order books](https://docs.polymarket.com/market-data/prices-order-books) for active Senate contracts. Yes and No use their own token IDs and asks. Orders are never submitted: the only POST is the documented batch **read** `/books`. Gamma prices and total volume are not executable prices or guaranteed liquidity.

## Settlement comes before price comparison

- State-party winner contracts can exclude independents even when our model groups them with Democrats. Independent and multi-round races are retained with an explanation when the scalar forecast is incompatible. Named-candidate contracts need explicit identity mapping.
- [Senate control](https://polymarket.com/event/which-party-will-win-the-senate-in-2026) has majority, vice-presidential tie-break, caucus declaration and fallback rules. Our comparison assumes the model's fixed-seat roster and independent grouping. This remains conditional.
- Republican seat totals use the saved weighted mixture seat-count distribution, not a sum of independent state probabilities. The conversion R=100−D/Independent assumes no unmatched vacancies or caucus arrangements.
- Many winning-margin contracts measure the top two candidates as a share of all valid votes; some specify the first round. A D/R margin is comparable only under matching candidate and denominator assumptions. A final-result model cannot price a first-round contract automatically.
- State event probabilities use the full saved predictive distribution: analytic Gaussian CDF for GB and actual joint simulations for ST, MX and M10. Component draws are saved once, and mixtures reuse them with their saved weights and translations. No quantile bounds, interpolation, or Gaussian approximation of Student-t/mixture distributions is used. Simulation estimates retain Monte Carlo error.
- Senate-only joint-result contracts remain in the catalog until their settlement events have supported mappings. Marginal probabilities are never multiplied to invent combination probabilities.

## Price and fee calculation

The book is sorted by price explicitly; response order is not assumed. A hypothetical 100-share purchase walks all required asks. Incomplete depth, crossed books, unrecognized fees and minimum-size failures cannot qualify. Current [fee documentation](https://docs.polymarket.com/trading/fees) gives `shares × rate × price × (1−price)`. We read each market's enabled flag and rate, require the supported exponent, and account for fees at each fill level. Unknown schedules are not treated as zero. Fees are estimates from public metadata; rebates, funding costs, taxes and future exit fees are excluded.

Default research filters require at least 3 percentage points of modeled probability less purchase cost after fees, spread no wider than 10 cents, reported liquidity at least $2,000, and a forecast no more than 3 calendar days old. These are editable descriptive screens, not optimized investment rules. Catalog failures/offline mode cannot generate live shortlists. Book snapshots describe the moment retrieved; prices and depth can change immediately.

A positive model gap can reflect a model error, stale roster, wrong settlement interpretation or a genuinely different assessment. Review pending forecast-source/candidate changes before acting. Multiple listed contracts can be overlapping claims on the same state or chamber outcome; this is not a diversified portfolio or an arbitrage claim.

## Output locations

- Notebook: `notebooks/11_live_polymarket.ipynb`.
- Latest report: `outputs/reports/markets/polymarket/report.md`.
- Latest data bundle: `outputs/results/markets/polymarket/`.
- Daily report and linked snapshots: `outputs/reports/history/YYYY-MM-DD/polymarket/report.md`.
- Ignored cache: `cache/polymarket/` and `cache/runs/polymarket/`.

The report lists every discovered event and links the full contract inventory, settlement rules, all model mappings/exclusions, both-side comparisons, books, settings and forecast manifest hash. A saved catalog provides an offline clone fallback with its original retrieval date. Offline results never masquerade as fresh quotes.

## Initial selected-model scanner

Notebook11 also scans every catalog contract against the four selected model variants in the saved live run. `scanner_audit.parquet` records every contract/model mapping, including exclusions. `scanner_details.parquet` holds each comparable model and Yes/No side. `scanner_summary.parquet` is the complete screen. `scanner_initial.md` displays the entire initial candidate list as a readable Markdown table. Named-candidate, independent-party, first-round and joint-result mismatches still require explicit mapping; no probability is invented for them.

The separate stress scenario adds 2 cents per share above the base ask-depth cost including taker fees. A separate 2-percentage-point haircut stresses each model probability. Both are editable assumptions. This assumes holding to settlement; configure additional friction for funding, exit or other costs as needed. The spread is already reflected in buying at asks and is not charged a second time.

The primary debug list now includes a market only when at least one individual model's model probability exceeds the cost by the configured edge threshold and the quote passes eligibility checks. It then displays every selected model and both sides, including disagreement and unavailable mappings, together under that market. Markets are ordered alphabetically, not by model consensus. Green means the row remains positive after the haircut; red means even its expected profit is negative; amber means weaker or unresolved value; gray means unavailable pricing or failed quote checks. The internal low/high fields are equal for the new point estimates and remain for file compatibility.

The displayed model envelope is not a statistical confidence interval. Win probabilities summarize predictive outcome uncertainty; margin-contract probabilities count matching outcomes in full simulations. Neither measures confidence in model correctness. The per-model download includes available 95% margin intervals and poll counts. Pending forecast-source reviews are carried into every summary row. This is an initial research list, not a final investment recommendation or position-sizing system.

The notebook renders scanner tables without ellipsis truncation. Select a contract ID and Yes/No side to see every available named model. Entry price is the average ask before fees. Base budget includes estimated fees for the configured share count; extra friction is a separate stress assumption. Expected net profit is shares × (probability − cost per share); return divides that profit by the total budget. Bounds remain ranges, with no invented midpoint. The separate stressed profit applies the probability haircut. The grouped Markdown and HTML reports display every selected market and all its model rows; the full per-model data remains in Parquet.


## Consistent probabilities and model-free price checks

Every model comparison uses that model's own analytic event probability, full predictive simulations, or saved seat-count frequency. A 95% margin interval is an interval for the election margin, not a 95% interval for the probability of winning. Missing model seat distributions remain unpriced. No model receives another model's uncertainty. No Gaussian approximation is imposed on Student-t or mixture forecasts.

Per-model tables distinguish the market midpoint, the model probability, and the probability needed to break even at the actual depth-adjusted purchase base cost including estimated fees. The model probability is compared with the purchase cost. Yes and No use their own order books; No probabilities complement the model's Yes probability.

Notebook section6 separately tests equal-size Yes+No purchases on the same contract, across the entire Senate inventory, even when model pricing is unavailable. A pair normally pays $1. The check subtracts both ask-depth costs, both taker fees and friction on each leg. It requires distinct tokens, complete depth, active order books, an online catalog, book timestamps no older than120 seconds and no more than30 seconds apart. It records all failures in `price_checks.parquet`. Snapshot-positive results require simultaneous fill and settlement review; they are not guaranteed executable arbitrage. This does not test sell-side, cross-contract or cross-event arbitrage, nor assume party contracts or margin bins are exhaustive without verified rules. All checks are Python code and public API reads.


## Debug view: payoff risk and model outcome ranges

Notebook section5 and `scanner_initial.md` show individual model rows grouped by market. `scanner_grouped.html` preserves the row colors outside the notebook; `scanner_grouped.parquet` provides the full numeric rows. There is no added ensemble or voting score. Missing model mappings remain visible as gray rows. The four-model mixture is simply one model row.

For Q shares at total per-share cost c, the normal-resolution realized profit is Q(1-c) on a win or −Qc on a loss. The reward/loss ratio is (1-c)/c; expected net profit is Q(p-c), and expected return is (p-c)/c. The modeled loss probability is 1-p. The probability p is a point estimate; the haircut remains a separate sensitivity assumption. These formulas do not assume shares of the same contract have independent outcomes.

The table also shows each model's expected election margin and available95% predictive margin interval for a mapped race. These describe D/Independent-minus-R election margins, not profit intervals or confidence intervals for p. No margin estimate is added to expected profit as extra evidence. National/state covariance is already reflected in the saved chamber distribution where available. Portfolio risk and cross-market joint outcomes would require joint predictive samples and their dependence; the current view makes no such portfolio calculation.


## Compact reading mode

The notebook and HTML report display every qualifying market directly, with all model/Yes-No pairs clustered in one five-column table per market. There are no dropdowns, widgets or hidden market selectors. Model / side uses shared model codes plus Y (buy Yes) or N (buy No). Status, P (%), EV ($), and Stress ($) complete the five columns. A model legend appears once at the top. Text labels accompany the green, red, amber and gray row colors. A small two-row payoff table above each market shows shared entry costs, total budget, win/loss payoff and reward-to-loss ratio.

Tables use readable14px text and wrap within a760px maximum width without horizontal scroll containers. Full numeric detail, predictive margin ranges and exclusions remain available in the Parquet downloads. The view is generated by Python on every run; it requires no AI calls, JavaScript or live widget kernel. Markdown reports use the same compact grouped tables, with status codes instead of colors. Auxiliary inventories and audits start collapsed.


## Base costs and separate stress scenarios

Base budgets, entry break-even probabilities, EV ranges and win/loss payoffs now use observed ask-depth purchase costs plus estimated taker fees only. The configurable extra friction is not charged to the base result. Markets qualify for the debug list on their individual model base edge, so changing the extra friction does not change base probabilities, EV or membership.

The compact Stress column combines two transparent assumptions: the configured probability haircut (default2 percentage points) and extra cost (default2 cents/share). Its formula is Q × [max(0, model probability − haircut) − base cost/share − extra friction/share]. Raw scanner details also retain friction-only and probability-haircut-only results. GO means the combined stress result remains positive; WEAK means base EV is positive but does not survive the stress assumptions. Neither assumption is a calibrated confidence interval or a measured typical execution cost.

The model-free Yes/No pair check likewise saves the base depth-plus-fee calculation in price_checks.parquet and the separate extra-friction scenario in price_checks_stress.parquet. No model-probability haircut applies to model-free pair checks.

P is the model's probability that the selected side pays $1 under the exact mapped settlement condition. For a winner contract, it is the chance that party wins (or does not win for No). For a margin band [a,b), it is the probability that the election margin falls inside that interval; No covers its complement. The No probability is 1 minus the Yes probability. A contract on the market price/probability crossing a future threshold requires a trading-price-path model and remains outside this election-outcome scanner. P never means probability that the model is correct.


## Focused model set

The scanner now defaults to four models: Gaussian Bayesian (GB), matched Student-t with df5 (ST), the four-model mixture (MX), and the mixture shifted10% toward the empirical baseline (M10). Every selected model retains its own probabilities and uncertainty; the four rows are not combined into a new forecast. Other saved models remain available elsewhere and are not retrained or deleted. `polymarket_scanner.DEFAULT_MODELS` defines this scope; an explicit `models` argument can override it. Missing requested models cause a clear error rather than silent substitution. Each qualifying market displays eight rows: four models × Yes/No. These models share evidence and components, so agreement is not four independent confirmations.

## Independent updates and event formulas

1. Notebook04 updates the election forecast and saves full component simulations alongside the Gaussian parameters. This uses fixed historical fits.
2. Notebook11 has a separate `download_markets()` cell. It refreshes Polymarket data without loading or running the election models.
3. `analyze(RUN, snapshot=MARKET_SNAPSHOT)` and `scanner.scan(...)` evaluate a saved forecast against that snapshot without downloading data or running inference. Set `REFRESH_MARKETS = False` to reuse the saved snapshot during Run All. Original market timestamps are preserved; quotes older than120 seconds and catalogs older than15 minutes cannot produce live candidates.

The checked-in latest forecast includes the full draws, so cloning and scanning requires no one-time inference upgrade. For an older forecast missing draws, `python scripts/export_predictive_distributions.py` reconstructs the exact saved inputs and verifies unchanged predictions and seat estimates before publishing an enriched copy. It downloads nothing. Future notebook04 runs save draws automatically. Component files are compressed once; shifted mixtures do not duplicate their samples.

The formulas are programmed by contract type; market text supplies the state, party, thresholds, and recognized boundary convention. Each audit row records `event_formula`, `probability_kind`, and the simulation count where applicable. Formula definitions also appear in the notebook and generated report. Unsupported settlement rules remain unpriced. Joint samples are available, but complex combination/ranking contracts still require an explicit compatible settlement mapping.

For a Democratic margin band `[a,b)`, the event is `a <= M < b`, where M is D minus R margin. For a Republican band it is `-b < M <= -a`; this reflection preserves the rule that exact boundaries belong to the higher winning-margin bracket. No is the complement. For continuous predictive distributions, exact ties have zero probability; actual contract tie/replacement/unresolved-election rules remain settlement assumptions, not separate modeled risks.

ST winner probabilities now count its same posterior draws used for margin events. They may differ slightly from the variance-reduced winner estimate in the forecast summary. Gaussian winner/margin probabilities use its analytic CDF; Gaussian chamber/seat probabilities use its joint simulation frequency. MX and M10 use the same weighted component draws that generated their published forecast probabilities. No independent-state approximation is introduced.
