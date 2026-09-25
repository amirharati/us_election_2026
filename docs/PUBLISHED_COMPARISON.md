# Automatic comparison with published forecasts

Notebook 04, section 5c, and `python run.py live` / `python run.py report` generate this comparison in code. They use the [Race to the WH public forecast](https://www.racetothewh.com/senate/26) , the [Inside Elections public ratings feed](https://insideelections.com/ratings/senate/), and [Silver Bulletin’s public forecast commentary](https://www.natesilver.net/p/nate-silver-2026-midterm-election-polls-model). No forecast numbers or selection sentences are entered manually.

The default comparison models are Gaussian Bayesian and the four-model mixture. The overall table shows Democratic control probability and expected Democratic seats. A signed probability gap is **our forecast minus Race to the WH**, in percentage points. Expected seats are not the number of races with a favored Democratic winner. Inside Elections has a separate table counting favored parties and toss-ups over exactly the matched races; its ratings are not numeric Senate-control probabilities.

The state table selects:

- Numerical forecasts that favor different parties, or differ by at least 15 percentage points in D/Independent win probability.
- Ratings that favor the opposite party, or call a race a toss-up when our model gives one party at least 75% probability.

These thresholds are configurable in the notebook. Every reason is generated from the comparison row. The complete matched table is saved, including rows that do not qualify. Changing the selection does not change our forecast or train a model.

The adapters match states and, where published, Senate seat classes. A state must have exactly one local contest. This preserves Florida and Ohio special elections even though the ratings feed currently marks its special-election boolean as false. Independent contenders are included on the D/Independent side under the user-selected comparison assumption. We add the publisher’s separate D and independent win probabilities. If an independent is already listed in its D column, that probability is counted only once. The source snapshot retains the original columns. State tables label the combined side and mark races using this assumption. Independent-favored ratings also map to the D/Independent side. This assumption does not assert a candidate’s party affiliation or future caucus. Chamber figures retain each source's own convention. Different methods, input dates, candidate assumptions and independent-caucus conventions can all cause differences; this comparison does not diagnose their cause.

Every run displays publication dates separately from retrieval dates. Releases later than our forecast cutoff are excluded. These are the latest available publisher snapshots, not historical publisher forecasts reconstructed for old cutoffs. Source failures retain a verified cached snapshot with an explicit stale status. Missing sources stay unavailable. The six-hour cache, `FORCE`, `OFFLINE`, TTL and timeout controls also apply to publisher retrieval. External comparison failures do not change the fitted model or block the underlying forecast.

Original downloads are not added to Git. Small normalized snapshots, original-response hashes, source URLs, dates, settings, and full comparison tables are saved in each report bundle. The latest bundle also provides a verified offline fallback for a clone with no local cache. Dated reports freeze their linked snapshot and comparison table. The dated HTML report includes the same tables. Direct `save_report()` calls use saved external evidence offline unless the caller supplies a newly built comparison; the notebook and CLI explicitly refresh it.

Adding another publisher requires a schema-validated adapter. Paywalled tables and search snippets are not treated as live data feeds. Source layout changes produce an explicit failed-refresh status rather than guessed values.

## Silver Bulletin

Silver Bulletin Deluxe is included as a **public topline only**. The adapter checks the forecast landing page and discovers relevant articles through Silver’s public RSS feed. It extracts an explicitly stated Deluxe Democratic Senate-control probability from the publicly rendered article body. It does not read serialized subscriber content or bypass the paywall. Publication date, exact article URL, response hash and discovery hashes are retained. This is a rounded number from dated commentary, not access to the subscriber-only live dashboard.

State probabilities and expected seats remain missing when they are not publicly available. They are not inferred from control odds. An unrecognized or ambiguous sentence causes the parser to decline the value. A failed refresh uses a verified older snapshot with its original date and explicit status. If no snapshot is available, Silver is marked unavailable. Chamber differences now have a separate row for each local-model/publisher pair.

## Shareable images

Run All generates PNGs beside the original tables in the live notebook. It also saves them beside the latest report in `outputs/reports/forecast/`, with names beginning `share_`. Dated report folders freeze the same images. The HTML report links its adjacent PNG images. Download the report folder to view it locally.

Images cover chamber probabilities and seat ranges, state mixture margin plots showing the mean and central 68%/95% predictive intervals, with a separate aligned panel of average pairwise margin disagreement among the four mixture components, predictive interval plots, surprise probability bars, and published-forecast comparison plots. Numeric publisher comparisons connect our probability to theirs. Qualitative ratings accompany race labels without being converted into probabilities. These are charts, not table images. Model names, cutoff dates, publisher dates, cache status where relevant, and short interpretation notes travel with each image. The existing cutoff-history chart remains available as `control_history.png`. The original tables and complete supporting data are retained. `share_images.json` records the generated PNG checksums and source forecast manifest.

State intervals use weighted quantiles of the full mixture draws (16th/84th and 2.5th/97.5th percentiles), not averaged component endpoints or Gaussian SD approximations. The companion probability chart shows mixture win probabilities, with disagreement in margin percentage points beside it; margin intervals are not probability intervals. Older saved forecasts without 68% quantiles display the available 95% interval and a rerun note.

Mixture margin intervals are teal with at least3 admitted recent poll samples from at least2 firms, amber with some recent polling below either threshold, and gray with no recent polling. The default window is30 days through the forecast cutoff, inclusive. Notebook coverage settings control both chart colors and watchlists. Samples are deduplicated; colors describe evidence coverage, not confidence. The mean dot stays dark and the interval widths retain their predictive meaning.
