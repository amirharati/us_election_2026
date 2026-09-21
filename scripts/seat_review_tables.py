"""Readable views of frozen review artifacts; never fit or select a model."""
from pathlib import Path
import pandas as pd
import numpy as np
from compare_current_forecasts import refresh_manifest

MODEL_NAMES={'prior':'Historical prior','polling':'Polling','bias':'Polling + state bias','bias__blend_all__last10':'Bias + selected peer blend'}
def margin(v):return '—' if pd.isna(v) else f"{'D' if v>=0 else 'R'} +{abs(v):.2f}"
def seats(d,r):return f'{int(d)} D / {int(r)} R'
def historical_summary(totals):
    q=totals[(totals.model=='bias')&(totals.cycle<2026)];rows=[]
    for y,g in q.groupby('cycle'):
        e=g[g.scenario=='matched_live'].iloc[0];o=g[g.scenario=='oct31'].iloc[0]
        rows.append(dict(Cycle=y,**{'Sep17 predicted total*':seats(e.completion_D,e.completion_R),
            'Oct31 predicted total*':seats(o.completion_D,o.completion_R),'Actual total':seats(o.actual_D,o.actual_R),
            'Scored races':f'{int(o.modeled_contests)}/{int(o.contested)}',
            'Earlier calls correct':f'{int(e.modeled_correct)}/{int(e.modeled_contests)}','Earlier MAE (pp)':round(e.modeled_mae_pp,2),
            'Oct31 calls correct':f'{int(o.modeled_correct)}/{int(o.modeled_contests)}',
            'Oct31 MAE (pp)':round(o.modeled_mae_pp,2),'Completion assumptions':int(o.unmodeled_contests)}))
    return pd.DataFrame(rows)

def model_summary(totals):
    rows=[]
    for (model,scenario),g in totals[totals.cycle<2026].groupby(['model','scenario']):
        n=int(g.modeled_contests.sum());c=int(g.modeled_correct.sum())
        rows.append(dict(Model=MODEL_NAMES[model],Horizon=scenario,**{'Correct calls':f'{c}/{n}','Accuracy (%)':round(100*c/n,2),'Mean cycle MAE (pp)':round(g.modeled_mae_pp.mean(),3)}))
    return pd.DataFrame(rows)

def state_history(history,year):
    q=history[(history.model=='bias')&(history.cycle==year)]
    a=q[q.scenario=='matched_live'].set_index('seat_id');b=q[q.scenario=='oct31'].set_index('seat_id');rows=[]
    for seat,r in b.sort_values(['state','seat_class']).iterrows():
        e=a.loc[seat];label=r.state+(' (special)' if r.special else '')
        rows.append(dict(State=label,**{'Sep17 predicted margin':margin(e.prediction_pp),'Oct31 predicted margin':margin(r.prediction_pp),
            'Actual margin':margin(r.actual_margin_pp),
            'Sep17 predicted winner':e.model_caucus if e.model_called else '—',
            'Oct31 predicted winner':r.model_caucus if r.model_called else '—',
            'Actual winner bloc':r.actual_caucus,
            'Oct31 correct?':('Yes' if r.model_caucus==r.actual_caucus else 'No') if r.model_called else 'Not modeled',
            'Completion assumption':'—' if r.model_called else 'Keep '+r.caucus,
            'Exclusion reason':str(r.historical_exclusion_reason) if not r.model_called and pd.notna(r.historical_exclusion_reason) else ('No admitted target' if not r.model_called else '—')}))
    return pd.DataFrame(rows)

def quote(bid,ask):return '—' if pd.isna(bid) else f'{bid:.1f}–{ask:.1f}%'
def current_table(comp):
    rows=[]
    for r in comp.sort_values('state').itertuples():
        notes=[]
        if r.n_samples==0:notes.append('no polls; prior fallback')
        if r.within_1pp:notes.append('within 1 pp')
        if r.material_rule_flag:notes.append('rule/independent flag')
        if r.call_disagreement:notes.append('different favored party')
        prob='—' if pd.isna(r.race_D_probability) else f'{r.race_D_probability:.1f}%'
        ip='—' if pd.isna(r.race_I_probability) else f'{r.race_I_probability:.1f}%'
        rows.append(dict(State=r.state,**{'Our margin (D−R pp)':margin(r.prediction_pp),'Our call*':r.model_caucus,
            'Actual result':'Pending','Poll samples':int(r.n_samples),'RaceToWH margin':r.race_display_margin,'RaceToWH D win':prob,'RaceToWH IND win':ip,
            'Kalshi D bid–ask':quote(r.kalshi_D_bid_pct,r.kalshi_D_ask_pct),
            'Kalshi IND bid–ask':quote(r.kalshi_I_bid_pct,r.kalshi_I_ask_pct),'Notes':'; '.join(notes)}))
    return pd.DataFrame(rows)

def write_report(lab,out):
    lab,out=Path(lab).resolve(),Path(out).resolve()
    totals=pd.read_parquet(out/'seat_totals.parquet');history=pd.read_parquet(out/'historical_states.parquet')
    comp=pd.read_parquet(out/'current_comparison.parquet');top=pd.read_parquet(out/'external_topline.parquet')
    intro='''# Senate model and seat review — September 18, 2026

The reference remains **polling + decayed state polling-bias correction** (`bias`): current-cycle polling with existing firm/recency weights and prior regularization; state error calibration uses the last five calendar cycles with an eight-year half-life, with shrinkage chosen using the previous cycle. No-poll states retain their historical prior. This is the strongest simple late-cycle winner-call reference among our exploratory comparisons, not a uniquely established best model. We have examined these historical outcomes repeatedly; they are not untouched validation data.

We have also tested pure priors, feature regressions and scores, state coefficients, trees/forests, momentum/approval corrections, fusion, polling-age decay and peer-state borrowing. Features occasionally help, particularly polling plus momentum at the late horizon, but do not consistently improve the bias reference. The latest peer blend improves average margin error and one earlier winner call, ties October calls, and selects **no borrowing for 2026**. No refitting or new model selection was performed for this review.

## How to read the numbers

- Positive margin means Democratic vote share minus Republican vote share; displays use D +x or R +x, in **percentage points**, not win probabilities. MAE is mean absolute margin error. The all-years MAE below averages cycle MAEs; accuracy pools modeled contests.
- Historical predictions were generated chronologically with earlier-cycle training/tuning. `matched_live` uses September 17 in each cycle (the same calendar date as the live snapshot); `oct31` is October 31. Current inputs stop September 17, 2026. Public comparisons were captured September 18.
- D seat totals include **Democratic-caucusing independents**. We count all 100 seats: continuing seats plus contested seats. The actual outcome is the following January 31 membership, including Georgia's January 2021 runoffs.
- A state can have a regular and a special race for different seats. Same-seat special/regular ballots (California) and later runoff stages are not additional seats.
- Historical models cover only 26–29 admitted contests per cycle. For a complete illustrative tally, unmodeled races explicitly retain their **pre-election incumbent caucus**. These assumptions are NOT model predictions and are NOT included in model accuracy. Actual winners never fill missing forecasts. A dash is missing, not a zero margin.
- The 2026 total is conditional on converting scalar D−R signs to seats. Independent candidates, Alaska/Maine ranked choice and Georgia runoff rules still need ballot/caucus resolution. These are **point-call tallies**, not expected seats, a calibrated seat distribution or Senate-control probabilities.

## Recent model comparison

'''
    parts=[intro,model_summary(totals).to_markdown(index=False),'\n\n## Full chamber totals by historical cycle\n\n',historical_summary(totals).to_markdown(index=False),
        '\n\n*Totals include the explicitly labeled incumbent-completion assumptions. In 2020 these assumptions retain Republican control of the excluded Arizona special and both Georgia seats; the real contests all elected Democrats. The 48–52 tally is therefore not a clean evaluation of a complete model. Correct-call and MAE columns score admitted model predictions only. Full ledgers also expose assigned seats before completion and the possible range over unmodeled seats; those are coverage bounds, not uncertainty intervals.\n\n']
    for y in [2016,2018,2020,2022,2024]:
        parts += [f'## {y}: every contested seat\n\n',state_history(history,y).to_markdown(index=False),'\n\n']
    parts += ['''## Current 2026: all contested seats

Our conditional tally is **50 D / 50 R**: 34 D / 31 R continuing seats, plus 16 D / 19 R calls among 35 contests. Of these, 21 have admitted polls and 14 use prior fallback. Maine (D +0.026 pp), Texas (D +0.670 pp) and Alaska (D +1.104 pp) are fragile sign-based calls. A 50–50 chamber would have Republican control through the current vice president; our point tally does not estimate the probability of that outcome.

All current seat mappings retain the snapshot's `seat_forecast_ready=False`; this review does not certify the candidate/rule layer. ID/MT/NE/SD have material independent-candidate issues; RaceToWH's non-Republican margins there are not comparable with our scalar D−R margins. Source party-column labels for Achilles and Bengs are recorded but normalized to independent, using our reviewed candidate policy. All other published margins are shown as reported, without claiming harmonized vote-share denominators.

''',current_table(comp).to_markdown(index=False),'\n\n## Published forecasts and markets — current cycle only\n\n',top[['source','D_seats','R_seats','seat_measure','D_control_pct','D_bid_pct','D_ask_pct','as_of']].to_markdown(index=False),'''

The **three RaceToWH call disagreements are Iowa, Michigan and Ohio**: our model favors R; RaceToWH favors D. RaceToWH's own individual favored-party calls would produce 53 D / 47 R with the same continuing-seat count, whereas its published **expected** seat count is 52.3 D / 47.7 R. These are different summaries. Kalshi favors D in Michigan and Ohio but R in Iowa. Markets have no matched state quotes here for 14 contests; blanks remain missing.

- [Race to the WH Senate forecast](https://www.racetothewh.com/senate/26): September 18, 1:25 PM ET update; 68.7% Democratic control and 52.3 expected D seats. The public embedded chart's live-data JSON is frozen with timestamps and hashes.
- [Silver Bulletin FLIPR / Deluxe](https://www.natesilver.net/p/nate-silver-2026-midterm-election-polls-model): September 18 public introduction gives 59% Democratic Senate control. Detailed state and seat estimates were not publicly accessible, so they remain missing. No subscriber-only content was bypassed.
- [Kalshi control contract](https://api.elections.kalshi.com/trade-api/v2/events/CONTROLS-2026?with_nested_markets=true): Democratic bid 59%, ask 60% at capture; midpoint 59.5%. State markets are frozen for 21 states. Contract geography uses title checked against resolution rules: `SENATELA-26` is **Kentucky**, while `KXSENATELA-26NOV` is Louisiana. Some candidate display names are stale/inconsistent; the market is a party/contract proposition, not a cleaned ballot roster. The South Carolina Republican display label is “Darline Graham”; we retain the label but do not treat it as a different candidate forecast.
- [Polymarket Senate control](https://polymarket.com/event/which-party-will-win-the-senate-in-2026): Democratic bid 59%, ask 60%; midpoint 59.5%. Separate party contracts need not sum to 100%; we do not silently normalize them.

Market quotes are prices interpreted as implied probabilities, not another poll or an independent ground-truth label. All public forecasts can share polling inputs. Our margin signs provide no comparable control probability yet. This one-day-asynchronous snapshot is a comparison, not a calibration or accuracy test against 2026 outcomes.

## Sources, checks and next work

Historical seat rosters use the public [congress-legislators term and dated affiliation archive](https://github.com/unitedstates/congress-legislators), checked against [official Senate party-division history](https://www.senate.gov/history/partydiv.htm). Initial Congress composition is used, not later within-Congress special-election changes. The frozen 2026 roster comes from the lab's reviewed official Senate snapshot.

- [x] Use one frozen reference model for all historical cycles and current forecasts.
- [x] Show state-by-state calls, margins, actual outcomes and missing historical coverage.
- [x] Reconcile exactly 100 unique seats per scenario, including continuing seats and specials.
- [x] Verify historical final caucus totals (48, 47, 50, 51, 47 D for 2016–2024).
- [x] Preserve forecasts when outcomes change; outcomes never complete predictions.
- [x] Keep dated party/caucus changes, external party labels and contract geography explicit.
- [x] Freeze sources, timestamps, hashes, public state quotes and reproducible parsing code.
- [ ] Resolve full 2026 ballot/independent/RCV/runoff treatment before calling the seat forecast certified.
- [ ] Complete excluded historical contests with a validated model if full-chamber model accuracy is required.
- [ ] Fit and validate marginal and correlated uncertainty before publishing winner/control probabilities or expected seat counts.

Notebook: **BASELINE_MODELS.ipynb, Sections 94–98**. Scripts: `senate_seat_review.py`, `compare_current_forecasts.py`, `seat_review_tables.py`. Replaying the notebook review uses the frozen report and checks all artifact/input hashes; it does not refetch a future forecast into this historical comparison. A new public capture requires a new dated source directory.

''',f'Artifacts: `{out.relative_to(lab)}`. `full_seat_ledger.parquet` contains every seat for every included cycle/horizon/model; `historical_states.parquet` and `current_comparison.parquet` contain the contested-seat details.\n']
    text=''.join(parts);(lab/'SENATE_SEAT_REVIEW.md').write_text(text);(out/'SENATE_SEAT_REVIEW.md').write_text(text)
    (out/'seat_review_tables.py').write_bytes(Path(__file__).read_bytes());refresh_manifest(out)
    print('Wrote report:',lab/'SENATE_SEAT_REVIEW.md')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--review-dir',type=Path,required=True);a=p.parse_args()
    write_report(Path(__file__).resolve().parents[1],a.review_dir)
