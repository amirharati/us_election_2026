"""Historical Senate forecast/price alignment and explicit-signal P&L research.

No strategy is selected here. P&L uses historical price proxies, not fills.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import argparse
import sys
import numpy as np
import pandas as pd
from download_polymarket_history import ROOT, OUT, write_json
# CLI and prepare-script entry points must also resolve the repository module.
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from compare_current_forecasts import NAMES

MODELS = {'Bayesian':'GB', 'Matched Student-t (df5)':'ST',
          'Four-model mixture':'MX', 'Mixture + polling 10%':'M10'}
REPORT = ROOT/'outputs/reports/research/polymarket_history'
PROVENANCE = ('Retrospective reconstruction from saved chronological folds. Model design was developed later; '
              'feature publication vintages are not fully reconstructed. This is not a pristine prospective test.')


def load_forecasts():
    source = ROOT/'outputs/results/experiments/portfolio/predictions.parquet'
    if not source.exists():
        raise FileNotFoundError('Run notebook 08 to create the saved historical portfolio predictions first.')
    q = pd.read_parquet(source)
    q = q[q.cycle.isin([2022,2024]) & q.model.isin(MODELS)].copy()
    q['model_code'] = q.model.map(MODELS)
    q['forecast_date'] = pd.to_datetime(q.as_of, utc=True)
    # No within-day publication time is known: trade only after the cutoff day ends.
    q['available_at'] = q.forecast_date + pd.Timedelta(days=1)
    q['provenance'] = PROVENANCE
    columns = ['cycle','scenario','geography','target_id','model','model_code','forecast_date','available_at','p_dem','actual','provenance']
    q = q[columns]
    if q.duplicated(['scenario','cycle','target_id','model']).any():
        raise ValueError('Duplicate historical forecasts')
    publisher_path=OUT/'publisher_history.parquet'
    if publisher_path.exists():
        publisher=pd.read_parquet(publisher_path)
        publisher['forecast_date']=pd.to_datetime(publisher.forecast_date,utc=True)
        extra=[]
        for f in q[q.model_code.eq('GB')].itertuples(index=False):
            eligible=publisher[publisher.cycle.eq(f.cycle)&publisher.geography.eq(f.geography)&
                publisher.forecast_date.le(f.forecast_date)&publisher.forecast_date.ge(f.forecast_date-pd.Timedelta(days=6))]
            for model,g in eligible.groupby('model'):
                last=g.sort_values('forecast_date').iloc[-1]
                extra.append(dict(cycle=f.cycle,scenario=f.scenario,geography=f.geography,target_id=f.target_id,
                    model=model,model_code=model,forecast_date=last.forecast_date,
                    available_at=f.available_at,p_dem=float(last.p_dem),actual=f.actual,provenance=last.provenance))
        if extra:q=pd.concat([q,pd.DataFrame(extra)],ignore_index=True)
    q.to_parquet(OUT/'forecasts.parquet', index=False)
    return q, dict(path=str(source.relative_to(ROOT)), sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  publisher_sha256=hashlib.sha256(publisher_path.read_bytes()).hexdigest() if publisher_path.exists() else None)


def mapping(row):
    """Conservative exact party-winner mapping; every other contract remains audited."""
    if row.category != 'winner':
        return '', '', 'Needs a historical joint/seat/margin distribution adapter.'
    text = row.question.lower()
    states = [code for code,name in NAMES.items() if re.search(r'\b'+re.escape(name.lower())+r'\b',text)]
    if len(states) != 1:
        return '', '', 'No unique state in the question.'
    state = states[0]
    if re.search(r'runoff|special|first.round|ranked.choice', text+' '+row.description.lower()):
        return state, '', 'Election stage or special contest requires explicit review.'
    # These party contracts do not mean that the modeled independent is a Democrat.
    if (int(row.cycle),state) in {(2022,'UT'),(2024,'ME'),(2024,'VT'),(2024,'NE')}:
        return state, '', 'Independent/party settlement requires candidate-specific historical mapping.'
    first = row.outcome_first.lower()
    second = row.outcome_second.lower()
    if first in ['democrat','democrats','democratic'] and second in ['republican','republicans']:
        return state, 'D', ''
    if first in ['republican','republicans'] and second in ['democrat','democrats','democratic']:
        return state, 'R', ''
    if {first,second} == {'yes','no'}:
        dem = bool(re.search(r'\bdemocrat(?:s|ic)?\b',text))
        rep = bool(re.search(r'\brepublican(?:s)?\b',text))
        if dem != rep:
            party = 'D' if dem else 'R'
            if first == 'no': party = 'R' if party == 'D' else 'D'
            return state, party, ''
    return state, '', 'Candidate or other outcome needs an explicit party/candidate adapter.'


def align(markets, prices, forecasts, coverage, max_quote_age_hours=36):
    """First price after a forecast becomes available; never backdate a forecast."""
    pairs, audits = [], []
    statuses = coverage.set_index('market_id').status.to_dict()
    for m in markets.itertuples(index=False):
        state, party, reason = mapping(m)
        q = forecasts[forecasts.cycle.eq(m.cycle) & forecasts.geography.eq(state)]
        if m.category == 'excluded': reason = m.exclusion_reason
        if not reason and q.empty: reason = 'No saved historical forecast for this contest.'
        if not reason and statuses.get(m.market_id) != 'available': reason = 'History is missing or incomplete; excluded from scoring.'
        audits.append(dict(cycle=m.cycle,market_id=m.market_id,question=m.question,category=m.category,
                           state=state,model_mapping='mapped' if not reason else 'unmapped',reason=reason))
        if reason: continue
        h = prices[prices.market_id.eq(m.market_id)].sort_values('timestamp')
        for f in q.itertuples(index=False):
            candidates = h[h.timestamp.ge(f.available_at) & h.timestamp.le(f.available_at+pd.Timedelta(hours=max_quote_age_hours))]
            if candidates.empty:
                audits.append(dict(cycle=m.cycle,market_id=m.market_id,question=m.question,category=m.category,state=state,
                                   model_mapping='no_matched_price',reason=f'{f.scenario}: no price within {max_quote_age_hours} hours after forecast availability.'))
                continue
            quote = candidates.iloc[0]
            p = float(f.p_dem if party == 'D' else 1-f.p_dem)
            model_outcome = float(f.actual > 0) if pd.notna(f.actual) and f.actual != 0 else np.nan
            if party == 'R' and pd.notna(model_outcome): model_outcome = 1-model_outcome
            payout = m.payout_first
            settlement_ok = pd.notna(payout) and pd.notna(model_outcome) and payout == model_outcome
            pairs.append(dict(cycle=m.cycle,scenario=f.scenario,market_id=m.market_id,state=state,target_id=f.target_id,
                 question=m.question,model=f.model,model_code=f.model_code,forecast_date=f.forecast_date,
                 available_at=f.available_at,entry_time=quote.timestamp,price_first=float(quote.price_first),
                 probability_first=p,outcome_first=m.outcome_first,outcome_second=m.outcome_second,
                 payout_first=payout,settlement_verified=settlement_ok,
                 settlement_note='API resolution agrees with model election label' if settlement_ok else 'Missing resolution or disagreement; not eligible for scoring or P&L',
                 edge_pp=100*(p-quote.price_first),provenance=f.provenance))
    columns=['cycle','scenario','market_id','state','target_id','question','model','model_code','forecast_date','available_at','entry_time','price_first','probability_first','outcome_first','outcome_second','payout_first','settlement_verified','settlement_note','edge_pp','provenance']
    return pd.DataFrame(pairs,columns=columns), pd.DataFrame(audits)


def scores(pairs):
    columns=['cycle','scenario','model','races','model_brier','market_brier','model_log_loss','market_log_loss','mean_gap_pp']
    if pairs.empty: return pd.DataFrame(columns=columns)
    q=pairs[pairs.settlement_verified].copy()
    if q.empty: return pd.DataFrame(columns=columns)
    # One deterministic contract per contest; complementary D/R markets are not extra races.
    q['sort_id']=pd.to_numeric(q.market_id)
    q=q.sort_values('sort_id').drop_duplicates(['cycle','scenario','model','target_id'])
    shared=[]
    for _,g in q.groupby(['cycle','scenario']):
        total=g.model_code.nunique()
        ids=g.groupby('target_id').model_code.nunique()
        shared.append(g[g.target_id.isin(ids[ids.eq(total)].index)])
    q=pd.concat(shared,ignore_index=True)
    rows=[]
    for (year,scenario,model),g in q.groupby(['cycle','scenario','model_code']):
        p=np.clip(g.probability_first.to_numpy(float),1e-12,1-1e-12)
        market=np.clip(g.price_first.to_numpy(float),1e-12,1-1e-12);y=g.payout_first.to_numpy(float)
        rows.append(dict(cycle=year,scenario=scenario,model=model,races=len(g),model_brier=float(np.mean((p-y)**2)),
                    market_brier=float(np.mean((market-y)**2)),model_log_loss=float(np.mean(-y*np.log(p)-(1-y)*np.log1p(-p))),
                    market_log_loss=float(np.mean(-y*np.log(market)-(1-y)*np.log1p(-market))),mean_gap_pp=float(np.mean(abs(p-market))*100)))
    return pd.DataFrame(rows,columns=columns)


def evaluate_signals(pairs, signals, friction_cents=0.):
    """Evaluate user-supplied positions. No automatic strategy or sizing.

    signals columns: cycle, scenario, market_id, model_code, side (first/second),
    shares. Price history is a proxy; friction is a chosen per-share assumption.
    No capital reuse, liquidation, executable depth, or real-fill claim is made.
    """
    keys=['cycle','scenario','market_id','model_code']
    if not np.isfinite(friction_cents) or friction_cents<0: raise ValueError('Invalid friction')
    if signals.duplicated(keys+['side']).any(): raise ValueError('Duplicate positions')
    if not signals.side.isin(['first','second']).all(): raise ValueError('Side must be first or second')
    if not (np.isfinite(signals.shares)&signals.shares.gt(0)).all(): raise ValueError('Shares must be positive and finite')
    q=signals.merge(pairs,on=keys,validate='many_to_one',how='left',indicator=True)
    if not q._merge.eq('both').all() or not q.settlement_verified.fillna(False).all():
        raise ValueError('Signal lacks a matched forecast/price or verified settlement')
    second=q.side.eq('second')
    q['entry_proxy']=np.where(second,1-q.price_first,q.price_first)
    q['probability']=np.where(second,1-q.probability_first,q.probability_first)
    q['payout']=np.where(second,1-q.payout_first,q.payout_first)
    q['cost']=q.shares*(q.entry_proxy+friction_cents/100)
    q['expected_profit']=q.shares*q.probability-q.cost
    q['realized_profit']=q.shares*q.payout-q.cost
    q['return_on_cost']=q.realized_profit/q.cost.replace(0,np.nan)
    q['execution_assumption']='Historical price proxy; second outcome uses complement; friction is assumed, not historical fees.'
    return q.drop(columns='_merge')


def markdown(frame):
    return frame.to_markdown(index=False, floatfmt='.4f') if not frame.empty else 'No eligible observations.'


def chart_coverage(status, destination):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    relevant=status[status.status.ne('excluded')]
    table=relevant.pivot(index='cycle',columns='status',values='contracts').fillna(0)
    fig,ax=plt.subplots(figsize=(7,3.5))
    palette={'available':'#287d64','empty_history':'#c98b30','partial':'#be4d4d','no_tokens':'#888888','legacy_amm_history_required':'#c98b30','opened_after_cutoff':'#888888'}
    table.plot.bar(stacked=True,ax=ax,color=[palette.get(x,'#888888') for x in table.columns])
    ax.set(ylabel='Senate contracts',xlabel='Election cycle',title='Historical price coverage')
    ax.tick_params(axis='x',rotation=0);ax.set_axisbelow(True);ax.grid(axis='y',alpha=.25)
    handles,labels=ax.get_legend_handles_labels()
    labels=[{'available':'Prices available','legacy_amm_history_required':'Legacy AMM source needed','opened_after_cutoff':'Opened after election cutoff','empty_history':'No history returned'}.get(x,x) for x in labels]
    ax.legend(handles,labels,title='History status',fontsize=8);fig.tight_layout();fig.savefig(destination,dpi=150);plt.close(fig)


def build():
    """Historical prediction and exploratory price-path analysis; downloads and inference cache are separate."""
    from historical_model_forecasts import build_forecasts
    from historical_market_prices import prediction_prices
    from polymarket_history_samples import build_samples,report_section,overall_samples,proximity,prediction_charts
    collection=json.loads((OUT/'collection.json').read_text())
    for name,checksum in collection['files'].items():
        if hashlib.sha256((OUT/name).read_bytes()).hexdigest()!=checksum:raise ValueError('Collection checksum mismatch: '+name)
    markets=pd.read_parquet(OUT/'markets.parquet')
    prices=prediction_prices()
    forecasts=build_forecasts()
    samples,availability=build_samples()
    summary=overall_samples(samples);near=proximity(samples)
    near.to_parquet(OUT/'state_proximity.parquet',index=False)
    audit=[]
    for m in markets.itertuples(index=False):
        state,party,reason=mapping(m)
        audit.append(dict(cycle=m.cycle,market_id=m.market_id,state=state,reason=reason,model_mapping='unmapped' if reason else 'mapped'))
    audit=pd.DataFrame(audit);audit.to_parquet(OUT/'mapping_audit.parquet',index=False)
    status=prices.groupby(['cycle','price_source'],as_index=False).agg(contracts=('market_id','nunique'),points=('price_first','count'))
    REPORT.mkdir(parents=True,exist_ok=True)
    charts=prediction_charts(samples,summary,REPORT)
    from polymarket_accuracy_evolution import build as build_evolution, report as evolution_report
    evolution,evolution_charts=build_evolution(samples,OUT,REPORT)
    charts.extend(evolution_charts)
    from polymarket_longshot_paths import build as build_paths, report as path_report, charts as path_charts
    longshot_paths=build_paths(samples,prices,OUT)
    charts.extend(path_charts(longshot_paths,prices,REPORT))
    from polymarket_edge_strategy import build as build_edge, report as edge_report, charts as edge_charts
    edge_strategy=build_edge(samples,prices,forecasts,pd.read_parquet(OUT/'publisher_history.parquet'),markets,OUT)
    charts.extend(edge_charts(edge_strategy,REPORT))
    from polymarket_signal_quality import build as build_signals, report as signal_report, charts as signal_charts
    signals=build_signals(samples,prices,forecasts,OUT)
    from polymarket_signal_quality import available_report
    comparison_text='# All-model Senate signal comparison: 2022 and 2024\n\n'+available_report(signals)
    (REPORT/'all_models.md').write_text(comparison_text)
    charts.extend(signal_charts(signals,REPORT))
    text='# Historical Senate prediction comparison: 2022 and 2024\n\n'
    text+='This analysis compares win probabilities with election outcomes and measures distance from the market. It also includes an exploratory long-shot exit-price proxy test, which does not establish executable profits.\n\n'
    text+='## Method and limitations\n\n'+PROVENANCE+'\n\n'
    text+='Our four models are rerun at each cutoff, with the same frozen September 17 calibration and fits trained only on earlier cycles. Polls after each cutoff and known later releases are excluded. Unknown release dates use field-end dates. Features use latest-vintage reference periods, so this is not a publication-vintage replay. Calibration at much earlier or later dates is not separately validated. M10 shifts the mixture mean 10% toward the polling estimate; it does not add ten probability points.\n\n'
    text+='2022 prices are reconstructed marginal probabilities from the original liquidity-pool trades and funding events. All 42 final pool balances match the archive. 2024 uses original archived daily prices where available, then public CLOB history, then last-trade proxies. These are prediction proxies, not executable quotes. Latest observations must precede cutoff-day end and be no more than seven days old. Publisher snapshots must be on or before the check date and no more than six days old.\n\n'
    text+='## Price sources\n\n'+markdown(status)+'\n\n'
    text+='GB: Gaussian Bayesian; ST: matched Student-t; OG: older Gaussian; OS: older Student-t (OG/OS are standalone strategy comparisons and mixture components); MX: four-model mixture; M10: mixture with 10% polling mean shift; 538: FiveThirtyEight Deluxe (2022); RTWH: Race to the WH (2024).\n\n'
    for path in charts:text+=f'![{path.stem}]({path.name})\n\n'
    text+=signal_report(signals)
    text+=edge_report(edge_strategy)
    text+=path_report(longshot_paths)
    text+=evolution_report(evolution)
    text+=report_section(samples)
    reasons=audit[audit.reason.ne('')].groupby(['cycle','reason'],as_index=False).agg(contracts=('market_id','nunique'))
    text+='## Unmapped contracts\n\n'+markdown(reasons)+'\n\n'
    text+='State winner probabilities are compared here. Chamber control, seat counts, margins, special/runoff and independent-party contracts need separate reviewed mappings. Overall means accuracy across covered states, not the probability of Senate control. Missing observations stay blank. Repeated dates reuse the same election outcomes and are not independent tests.\n\n'
    text+='## Files\n\nSee [the notebook](../../../../notebooks/12_historical_polymarket_backtest.ipynb) and [methodology](../../../../docs/POLYMARKET_BACKTEST.md). Raw data, inference caches and research tables remain Git-ignored. Reports and charts are saved here and under `outputs/reports/history/YYYY-MM-DD/polymarket_history`.\n'
    (REPORT/'report.md').write_text(text)
    dated=ROOT/'outputs/reports/history'/datetime.now().date().isoformat()/'polymarket_history';dated.mkdir(parents=True,exist_ok=True)
    for path in charts:(dated/path.name).write_bytes(path.read_bytes())
    (dated/'report.md').write_text(text.replace('../../../../notebooks/','../../../../../notebooks/').replace('../../../../docs/','../../../../../docs/'))
    (dated/'all_models.md').write_text(comparison_text)
    write_json(OUT/'research.json',dict(built_at=datetime.now(timezone.utc).isoformat(),strategy_selected=True,strategy='Independent-model positive-EV research baseline; no live orders',
        price_alignment='Last observation before cutoff-day end; maximum age7days',provenance=PROVENANCE))
    return dict(markets=markets,prices=prices,coverage=status,forecasts=forecasts,audit=audit,scores=summary,
        signals=signals,edge_strategy=edge_strategy,longshot_paths=longshot_paths,evolution=evolution,date_samples=samples,date_availability=availability,state_proximity=near,charts=charts,report=REPORT/'report.md')


if __name__=='__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    result=build();print(result['coverage'].to_string(index=False));print(result['scores'].to_string(index=False));print(result['report'])
