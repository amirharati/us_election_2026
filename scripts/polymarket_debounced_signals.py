"""One entry per persistent model/outcome signal; retrospective path diagnostics."""
from datetime import datetime
import json
import hashlib
import numpy as np
import pandas as pd
from download_polymarket_history import ROOT, OUT
from polymarket_backtest import mapping
from polymarket_edge_strategy import DEADLINES, probability_band
from polymarket_signal_quality import MODEL_LABELS, activity_history

METHOD='''One setup per model and state race, not per forecast day. Use one fixed representative regular-winner contract per state/cycle: Democratic-first if available, then lowest numeric market ID; selection never uses future price performance. Other compatible contracts are audited, not counted again. This groups equivalent party exposure rather than claiming cross-contract arbitrage.

Check daily at 00:00 UTC, starting September 2 (September 1 forecasts become available then), strictly before election-day midnight. Use the latest already-available forecast, at most 72 hours after its labelled forecast date, and the latest price strictly before the decision, at most 36 hours old. Retain original source dates: a carried publisher forecast is not a new forecast. Superseded publisher versions cannot be used. Apply identical timing rules to all models.

Enter when the selected side's probability-minus-price edge exceeds 2 cents. Keep one active setup until its edge is nonpositive on two consecutive valid daily checks with distinct price observations. Missing/stale forecasts or quotes break reset confirmation but do not close or rearm a setup. Opposite-side entry must wait until a later daily check after reset. Hitting a price target does not rearm the signal. Close the observation window at confirmed reset or the pre-election cutoff; never optimize its length from future prices.

For each nonoverlapping setup, report the raw maximum observed rise and the maximum rise sustained across three consecutive UTC calendar days (at least 36-hour span and gaps no greater than 36 hours), plus fresh endpoint change and worst observed change. Maxima are hindsight diagnostics, not achievable sale prices or realized profits. Return percentages divide price change by starting share price; edge coverage divides it by initial model edge. Primary mean/median maxima use fully observed windows only (at least three possible subsequent days, 80% daily coverage, and a valid endpoint within 36 hours). Partial-path witnessed hits remain separate; absent evidence is unknown, not failure. Targets are 5/10/20/50% of entry price with a 2-cent floor, or the larger of initial edge and 2 cents. Daily path files save adjacent-day changes without filling missing days. Prices are research proxies, not executable quotes; no fees, order fills or position sizing are assumed. Different model coverage remains relevant; repeated races across models are not independent evidence.'''


def canonical_markets(markets):
    candidates=[];audit=[]
    for m in markets.itertuples(index=False):
        state,party,reason=mapping(m)
        audit.append(dict(cycle=m.cycle,state=state,market_id=m.market_id,reason=reason or 'Compatible alternative contract'))
        if not reason:candidates.append(dict(cycle=m.cycle,state=state,market_id=m.market_id,first_party=party))
    q=pd.DataFrame(candidates)
    q['priority']=q.first_party.ne('D').astype(int);q['number']=pd.to_numeric(q.market_id)
    q=q.sort_values(['cycle','state','priority','number']).drop_duplicates(['cycle','state'])
    audit=pd.DataFrame(audit);audit.loc[audit.market_id.isin(q.market_id),'reason']='Fixed representative contract'
    return q.drop(columns=['priority','number']),audit


def debounce(checks,deadline,entry_edge=.02):
    """State machine uses only current/past checks. Unknown never rearms."""
    active=None;negative=0;previous_day=None;previous_quote=None;episodes=[];daily=[]
    for r in checks.itertuples(index=False):
        valid=pd.notna(r.probability) and pd.notna(r.price)
        action='Unknown' if not valid else 'No entry'
        edge=np.nan
        if not valid:
            negative=0;previous_day=None;previous_quote=None
        elif active is None:
            signed=r.probability-r.price
            if abs(signed)>entry_edge+1e-12:
                side='D' if signed>0 else 'R'
                active=dict(start=r.decision,entry_quote_time=r.quote_time,model_date=r.model_date,
                    side=side,price=r.price if side=='D' else 1-r.price,
                    probability=r.probability if side=='D' else 1-r.probability,edge=abs(signed))
                action='Enter';edge=abs(signed)
        else:
            signed=r.probability-r.price;edge=signed if active['side']=='D' else -signed
            action='Continue'
            if edge<=0:
                consecutive=previous_day is not None and r.decision-previous_day==pd.Timedelta(days=1) and r.quote_time!=previous_quote
                negative=negative+1 if consecutive else 1
                previous_day=r.decision;previous_quote=r.quote_time
                if negative>=2:
                    episodes.append(dict(**active,end=r.decision,end_reason='Confirmed edge reset'))
                    active=None;negative=0;previous_day=None;previous_quote=None;action='Reset'
            else:negative=0;previous_day=None;previous_quote=None
        daily.append(dict(decision=r.decision,action=action,active=active is not None,edge=edge,
            probability=r.probability,price=r.price,quote_time=r.quote_time,model_date=r.model_date))
    if active is not None:episodes.append(dict(**active,end=deadline,end_reason='Election cutoff'))
    return episodes,pd.DataFrame(daily)


def episode_path(history,episode):
    start,end,price=episode['start'],episode['end'],episode['price']
    h=history[(history.timestamp>=start)&(history.timestamp<end)].copy()
    h=h.groupby(h.timestamp.dt.floor('D'),sort=False).tail(1).sort_values('timestamp')
    h['value']=h.price_first if episode['side']=='D' else 1-h.price_first
    h['change']=h.value-price
    valid=h.value.between(0,1)
    h['daily_change']=h.value.diff().where(h.timestamp.dt.floor('D').diff().eq(pd.Timedelta(days=1)) & valid & valid.shift(fill_value=False))
    h['daily_return']=h.daily_change/h.value.shift().replace(0,np.nan)
    levels=[];stamps=[]
    for i in range(2,len(h)):
        w=h.iloc[i-2:i+1]
        if not w.value.between(0,1).all():continue
        if not w.timestamp.dt.floor('D').diff().iloc[1:].eq(pd.Timedelta(days=1)).all():continue
        if w.timestamp.diff().iloc[1:].max()>pd.Timedelta(hours=36):continue
        if w.timestamp.iloc[-1]-w.timestamp.iloc[0]<pd.Timedelta(hours=36):continue
        levels.append(float(w.value.min()-price));stamps.append(w.timestamp.iloc[-1])
    expected=len(pd.date_range(start.floor('D'),end.floor('D')-pd.Timedelta(days=1),freq='D'))
    endpoint=h.iloc[-1] if len(h) else None
    fresh=endpoint is not None and bool(valid.iloc[-1]) and end-endpoint.timestamp<=pd.Timedelta(hours=36)
    complete=bool(expected>=3 and valid.sum()>=max(3,np.ceil(.8*expected)) and fresh)
    raw=float(h.loc[valid,'change'].max()) if valid.any() else np.nan
    sustained=max(levels) if levels else np.nan
    stats=dict(complete=complete,observed_days=int(valid.sum()),expected_days=expected,
        coverage_reason='Complete' if complete else 'Too short' if expected<3 else 'Sparse or stale',
        max_rise=raw,max_sustained_rise=sustained,max_return=raw/price,max_sustained_return=sustained/price,
        sustained_edge_coverage=sustained/episode['edge'],
        endpoint_change=float(endpoint.value-price) if fresh else np.nan,
        worst_change=float(h.loc[valid,'change'].min()) if valid.any() else np.nan)
    for label,ratio in [('5',.05),('10',.10),('20',.20),('50',.50),('edge',None)]:
        threshold=max(.02,episode['edge'] if ratio is None else price*ratio)
        hits=[i for i,v in enumerate(levels) if v>=threshold-1e-12]
        stats['hit_'+label]=bool(hits)
        stats['days_to_'+label]=(stamps[hits[0]]-start).total_seconds()/86400 if hits else np.nan
    return stats,h


def summarize(episodes,keys):
    rows=[]
    for key,g in episodes.groupby(keys,dropna=False):
        key=key if isinstance(key,tuple) else (key,);full=g[g.complete]
        observed=g[g.max_sustained_rise.notna()]
        median=lambda s: s.dropna().median() if s.notna().any() else np.nan
        row=dict(zip(keys,key),setups=len(g),states=g.state.nunique(),complete=len(full),
            observed_sustained_paths=len(observed),observed_mean_sustained_cents=100*observed.max_sustained_rise.mean(),
            observed_median_sustained_cents=100*median(observed.max_sustained_rise),
            partial_hits=int((~g.complete & g.hit_10).sum()),unknown=int((~g.complete & ~g.hit_10).sum()),
            mean_sustained_cents=100*full.max_sustained_rise.mean(),median_sustained_cents=100*median(full.max_sustained_rise),
            median_sustained_return_pct=100*median(full.max_sustained_return),
            median_edge_coverage=median(full.sustained_edge_coverage),mean_endpoint_cents=100*full.endpoint_change.mean(),
            mean_raw_max_cents=100*full.max_rise.mean(),mean_worst_cents=100*full.worst_change.mean())
        for target in ['5','10','20','50','edge']:row['hit_'+target+'_pct']=100*full['hit_'+target].mean()
        rows.append(row)
    return pd.DataFrame(rows)


def analyze(forecasts,markets,prices,expiry=None,activity=None):
    representatives,audit=canonical_markets(markets);rows=[];daily=[];paths=[]
    forecasts=forecasts[forecasts.status.eq('available')&forecasts.race_kind.eq('regular')]
    activities,known=activity if activity is not None else ({},set())
    expiry=expiry or {}
    for m in representatives.itertuples(index=False):
        h=prices[prices.market_id.eq(m.market_id)].sort_values('timestamp').copy()
        if m.first_party=='R':h.price_first=1-h.price_first
        deadline=pd.Timestamp(DEADLINES[m.cycle],tz='UTC')
        dates=pd.date_range(pd.Timestamp(f'{m.cycle}-09-02',tz='UTC'),deadline-pd.Timedelta(days=1))
        fs=forecasts[forecasts.cycle.eq(m.cycle)&forecasts.geography.eq(m.state)]
        for model,f in fs.groupby('model'):
            checks=[];f=f.sort_values('available_after_utc')
            for date in dates:
                available=f[f.available_after_utc.le(date)&f.forecast_date.ge(date-pd.Timedelta(days=3))]
                quotes=h[h.timestamp.lt(date)&h.timestamp.ge(date-pd.Timedelta(hours=36))]
                quote=quotes.iloc[-1] if len(quotes) else None
                forecast=available.iloc[-1] if len(available) else None
                expiration=expiry.get((m.cycle,model,m.state),pd.NaT)
                probability=float(forecast.p_dem) if forecast is not None and (pd.isna(expiration) or date<expiration) else np.nan
                price=float(quote.price_first) if quote is not None and 0<quote.price_first<1 else np.nan
                checks.append(dict(decision=date,probability=probability,price=price,
                    quote_time=quote.timestamp if quote is not None else pd.NaT,
                    model_date=forecast.forecast_date if forecast is not None else pd.NaT))
            episodes,decisions=debounce(pd.DataFrame(checks),deadline)
            common=dict(cycle=m.cycle,state=m.state,model=model,market_id=m.market_id)
            daily.append(decisions.assign(**common))
            for e in episodes:
                stats,path=episode_path(h,e);episode_id=len(rows)+1
                days=(deadline-e['start']).total_seconds()/86400
                events=activities.get(m.market_id,pd.Series([],dtype='datetime64[ns, UTC]'))
                count=int((events.ge(e['start']-pd.Timedelta(days=7))&events.lt(e['start'])).sum()) if m.market_id in known else np.nan
                rows.append(dict(**common,episode_id=episode_id,**e,**stats,
                    probability_band=probability_band(e['price']),time_band='≤7 days' if days<=7 else '7–14 days' if days<=14 else '14–30 days' if days<=30 else '>30 days',
                    activity_band='Unknown' if pd.isna(count) else '0' if count==0 else '1–9' if count<10 else '10–99' if count<100 else '100+'))
                paths.append(path.assign(**common,episode_id=episode_id))
    episodes=pd.DataFrame(rows)
    result=dict(episodes=episodes,decisions=pd.concat(daily,ignore_index=True),paths=pd.concat(paths,ignore_index=True),mapping=audit)
    for name,extra in [('overall',[]),('states',['state']),('probabilities',['probability_band']),('time',['time_band']),('activity',['activity_band'])]:
        result[name]=summarize(episodes,['cycle',*extra,'model'])
    return result


def display_tables(q):
    return [q[['model','setups','states','complete','partial_hits','unknown']].rename(columns={'model':'Model','setups':'Setups','states':'States','complete':'Full paths','partial_hits':'Partial hits (10%)','unknown':'Unknown (10%)'}),
        q[['model','observed_sustained_paths','observed_mean_sustained_cents','observed_median_sustained_cents']].rename(columns={
            'model':'Model','observed_sustained_paths':'Observed 3-day paths','observed_mean_sustained_cents':'Observed mean max (¢)','observed_median_sustained_cents':'Observed median max (¢)'}),
        q[['model','mean_sustained_cents','median_sustained_cents','mean_endpoint_cents','median_edge_coverage']].rename(columns={'model':'Model','mean_sustained_cents':'Mean max sustained (¢)','median_sustained_cents':'Median max sustained (¢)','mean_endpoint_cents':'Mean endpoint (¢)','median_edge_coverage':'Median edge covered (×)'}),
        q[['model','hit_5_pct','hit_10_pct','hit_20_pct','hit_50_pct','hit_edge_pct']].rename(columns={'model':'Model','hit_5_pct':'5% target','hit_10_pct':'10% target','hit_20_pct':'20% target','hit_50_pct':'50% target','hit_edge_pct':'Edge target'})]


def build():
    names=['daily_forecasts','markets','prediction_prices','signal_publisher_history']
    files={n:OUT/(n+'.parquet') for n in names};f,m,p,pubs=[pd.read_parquet(v) for v in files.values()]
    pubs['valid_until']=pd.to_datetime(pubs.valid_until,utc=True)
    expiry=pubs[pubs.valid_until.notna()].groupby(['cycle','model','geography']).valid_until.min().to_dict()
    result=analyze(f,m,p,expiry,activity_history())
    for name,frame in result.items():frame.to_parquet(OUT/('debounced_win_'+name+'.parquet'),index=False)
    (OUT/'debounced_win_manifest.json').write_text(json.dumps(dict(method=METHOD,entry_edge=.02,reset_checks=2,forecast_age_hours=72,
        quote_age_hours=36,inputs={n:hashlib.sha256(v.read_bytes()).hexdigest() for n,v in files.items()}),indent=2)+'\n')
    lines=['# Debounced state-winner setups','',METHOD,'','## Model names','',pd.DataFrame(MODEL_LABELS.items(),columns=['Code','Model']).to_markdown(index=False),'',
        'The Observed table includes every setup with a qualifying three-day sequence, even if the rest of its path is incomplete. Its maximum is a lower bound on the unobserved full-path maximum, not a complete-path estimate. Other return summaries and percentage target rates use full paths. Partial witnessed hits are counted separately. Negative maximum sustained rises are retained: no qualifying three-day period beat the entry price. These figures are hindsight diagnostics, not trade returns.','']
    for cycle,q in result['overall'].groupby('cycle'):
        lines += [f'## {cycle}: one setup until confirmed reset','']
        for t in display_tables(q):lines += [t.round(2).fillna('—').to_markdown(index=False),'']
        lines += ['Additional path diagnostics:','',q[['model','mean_raw_max_cents','mean_worst_cents','median_sustained_return_pct']].round(2).to_markdown(index=False),'']
    for name,band in [('states','state'),('probabilities','probability_band'),('time','time_band'),('activity','activity_band')]:
        for (cycle,label),q in result[name].groupby(['cycle',band]):
            lines += [f'### {cycle}: {name} — {label}','']
            for t in display_tables(q):lines += [t.round(2).fillna('—').to_markdown(index=False),'']
    report=ROOT/'outputs/reports/research/polymarket_history/debounced_win_signals.md';report.write_text('\n'.join(lines))
    dated=ROOT/'outputs/reports/history'/datetime.now().date().isoformat()/'polymarket_history';dated.mkdir(parents=True,exist_ok=True);(dated/report.name).write_bytes(report.read_bytes())
    result['report']=report
    print(result['overall'].round(3).to_string(index=False),flush=True)
    return result


if __name__=='__main__':build()
