"""Daily independent-model winner signals and sustained moves before election."""
from datetime import datetime
import hashlib
import json
import numpy as np
import pandas as pd
from download_polymarket_history import ROOT, OUT
from polymarket_backtest import mapping
from polymarket_signal_quality import path_metrics, activity_history, MODEL_LABELS
from polymarket_edge_strategy import DEADLINES, probability_band

METHOD='''Use the saved September-to-election daily forecast table, separately for each model. Only reviewed regular state-winner contracts are eligible; missing publisher days are not filled. Each forecast becomes usable after its labelled day ends UTC. The first valid price within 36 hours is the reference, strictly before election-day 00:00 UTC. Both outcome orientations are mapped explicitly. A positive probability-minus-price edge selects the side; this is before fees, not executable positive EV.

Follow every signal until election-day 00:00 UTC, without requiring a 30-day window. Targets are 5%, 10%, 20%, 50% of starting price (each at least 2 cents), plus the larger of initial edge and 2 cents. A hit must persist across three consecutive observed UTC days spanning at least 36 hours, with gaps no greater than 36 hours. No inactive days are filled. A fully observed remaining window requires at least three possible daily observations, at least 80% daily coverage and a valid last price within 36 hours of cutoff. Missing/too-short paths are unknown, not failures. Confirmed hits in incomplete windows are retained separately. Rates use full windows only; confirmed/all-signals is a lower bound when paths are missing.

Longer remaining windows offer more time to hit. Report time-to-election bands, initial prices, initial edges, prior seven-day activity and state subsets. Repeated daily signals and multiple contracts for one race are correlated; counts are not independent trades. Consecutive same-side daily signals are grouped as episodes for context, not used to assume an entry/exit strategy. Market prices may be reconstructed pool probabilities or last-trade proxies, not executable quotes. These are retrospective potential setups, not earned profits. Frozen local calibration and incomplete publication-vintage reconstruction still apply.'''
TARGETS={'5%':.05,'10%':.10,'20%':.20,'50%':.50,'Edge':None}


def remaining_path(history,entry_time,price,side,deadline):
    days=(deadline-entry_time).total_seconds()/86400
    path=path_metrics(history,entry_time,price,side,int(np.ceil(days))+1,deadline,allow_partial=True)
    future=history[(history.timestamp>entry_time)&(history.timestamp<deadline)].copy()
    future=future.groupby(future.timestamp.dt.floor('D'),sort=False).tail(1)
    expected=len(pd.date_range(entry_time.floor('D')+pd.Timedelta(days=1),deadline-pd.Timedelta(days=1),freq='D'))
    valid=future.price_first.between(0,1)
    enough=expected>=3 and days>=1.5
    complete=bool(enough and int(valid.sum())>=max(3,int(np.ceil(.8*expected))) and len(future)
        and valid.iloc[-1] and deadline-future.timestamp.iloc[-1]<=pd.Timedelta(hours=36))
    path.update(complete=complete,expected_days=expected,remaining_days=days,
        reason='Complete remaining window' if complete else 'Too little time for persistence' if not enough else 'Sparse or stale path')
    return path


def summarize(detail,keys):
    rows=[]
    for key,g in detail.groupby(keys,dropna=False):
        key=key if isinstance(key,tuple) else (key,)
        full=g[g.complete]
        rows.append(dict(zip(keys,key),signals=len(g),markets=g.market_id.nunique(),states=g.state.nunique(),
            dates=g.model_date.nunique(),episodes=g.episode_id.nunique(),complete=len(full),
            confirmed=int(g.confirmed.sum()),partial_hits=int((g.confirmed & ~g.complete).sum()),
            unknown=int((~g.complete & ~g.confirmed).sum()),too_short=int(g.reason.eq('Too little time for persistence').sum()),
            hit_pct=100*full.confirmed.mean(),lower_bound_pct=100*g.confirmed.mean(),
            equal_state_pct=100*full.groupby('state').confirmed.mean().mean(),
            days_to_hit=g.loc[g.confirmed,'days_to_hit'].median()))
    return pd.DataFrame(rows)


def analyze(forecasts,markets,prices,activity=None):
    forecasts=forecasts[forecasts.status.eq('available') & forecasts.race_kind.eq('regular')].copy()
    histories={mid:g.sort_values('timestamp') for mid,g in prices.groupby('market_id')}
    activities,known=activity if activity is not None else ({},set())
    details=[];audit=[];market_audit=[];memo={}
    for m in markets.itertuples(index=False):
        state,first_party,reason=mapping(m)
        market_audit.append(dict(cycle=m.cycle,market_id=m.market_id,state=state,reason=reason or 'Eligible winner contract'))
        if reason:continue
        fs=forecasts[forecasts.cycle.eq(m.cycle)&forecasts.geography.eq(state)]
        h=histories.get(m.market_id,pd.DataFrame(columns=prices.columns)).copy()
        if first_party=='R':h['price_first']=1-h.price_first
        deadline=pd.Timestamp(DEADLINES[m.cycle],tz='UTC')
        for f in fs.itertuples(index=False):
            common=dict(cycle=m.cycle,state=state,market_id=m.market_id,model=f.model,model_date=f.forecast_date)
            quotes=h[h.timestamp.ge(f.available_after_utc)&h.timestamp.le(f.available_after_utc+pd.Timedelta(hours=36))&h.timestamp.lt(deadline)]
            quotes=quotes[quotes.price_first.gt(0)&quotes.price_first.lt(1)]
            if quotes.empty:
                audit.append(dict(**common,reason='No fresh valid pre-election price'));continue
            entry=quotes.iloc[0];edge=float(f.p_dem-entry.price_first)
            if abs(edge)<=1e-9:
                audit.append(dict(**common,reason='No positive edge'));continue
            side='D' if edge>0 else 'R';price=float(entry.price_first if side=='D' else 1-entry.price_first)
            key=(m.market_id,entry.timestamp,side)
            if key not in memo:memo[key]=remaining_path(h,entry.timestamp,price,side,deadline)
            path=memo[key];edge=abs(edge)
            events=activities.get(m.market_id,pd.Series([],dtype='datetime64[ns, UTC]'))
            count=int((events.ge(entry.timestamp-pd.Timedelta(days=7))&events.lt(entry.timestamp)).sum()) if m.market_id in known else np.nan
            days=path['remaining_days']
            for target,ratio in TARGETS.items():
                threshold=max(.02,edge if ratio is None else price*ratio)
                hits=np.flatnonzero(np.asarray(path['levels'])>=threshold-1e-12)
                first=int(hits[0]) if len(hits) else None
                details.append(dict(**common,target=target,entry_time=entry.timestamp,side=side,price=price,
                    probability=float(f.p_dem if side=='D' else 1-f.p_dem),edge=edge,threshold=threshold,
                    attainable=price+threshold<=1+1e-12,confirmed=first is not None,complete=path['complete'],reason=path['reason'],
                    days_to_hit=(path['times'][first]-entry.timestamp).total_seconds()/86400 if first is not None else np.nan,
                    sustained_rise=path['sustained_rise'],observations=path['observations'],expected_days=path['expected_days'],
                    remaining_days=days,time_band='≤3 days' if days<=3 else '3–7 days' if days<=7 else '7–14 days' if days<=14 else '14–30 days' if days<=30 else '>30 days',
                    probability_band=probability_band(price),edge_band='<2¢' if edge<.02 else '2–5¢' if edge<.05 else '5–10¢' if edge<.1 else '10¢+',
                    prior_transactions=count,activity_band='Unknown' if pd.isna(count) else '0' if count==0 else '1–9' if count<10 else '10–99' if count<100 else '100+',
                    price_source=getattr(entry,'price_source','Unknown')))
            audit.append(dict(**common,reason='Positive-edge signal'))
    detail=pd.DataFrame(details)
    if detail.empty:raise ValueError('No daily winner signals')
    signals=detail[detail.target.eq('10%')].sort_values(['cycle','model','market_id','model_date']).copy()
    group=signals.groupby(['cycle','model','market_id'])
    new=signals.side.ne(group.side.shift()) | signals.model_date.sub(group.model_date.shift()).ne(pd.Timedelta(days=1))
    signals['episode_id']=new.cumsum()
    detail=detail.merge(signals[['cycle','model','market_id','model_date','episode_id']],on=['cycle','model','market_id','model_date'],validate='many_to_one')
    result=dict(detail=detail,audit=pd.DataFrame(audit),market_audit=pd.DataFrame(market_audit))
    for name,extra in [('overall',[]),('time',['time_band']),('probabilities',['probability_band']),('activity',['activity_band']),('edges',['edge_band']),('states',['state'])]:
        result[name]=summarize(detail,['cycle',*extra,'model','target'])
    pairs=[]
    for cycle,g in detail[detail.target.eq('10%') & detail.complete].groupby('cycle'):
        models=sorted(g.model.unique())
        for i,a in enumerate(models):
            for b in models[i+1:]:
                q=g[g.model.eq(a)].merge(g[g.model.eq(b)],on=['market_id','model_date'],suffixes=('_a','_b'),validate='one_to_one')
                if len(q):pairs.append(dict(cycle=cycle,model_a=a,model_b=b,observations=len(q),markets=q.market_id.nunique(),hit_a=100*q.confirmed_a.mean(),hit_b=100*q.confirmed_b.mean()))
    result['paired']=pd.DataFrame(pairs)
    return result


def rates(rows):
    base=rows[rows.target.eq('10%')].set_index('model')
    out=pd.DataFrame(index=list(MODEL_LABELS));out.index.name='Model'
    for col,label in [('signals','Signals'),('markets','Markets'),('complete','Full paths'),('unknown','Unknown')]:out[label]=base[col]
    for target in ['5%','10%','20%','50%']:out[target]=rows[rows.target.eq(target)].set_index('model').hit_pct
    return out.reset_index().round(1)


def build():
    inputs={name:OUT/(name+'.parquet') for name in ['daily_forecasts','markets','prediction_prices']}
    forecasts,markets,prices=[pd.read_parquet(p) for p in inputs.values()]
    prices['timestamp']=pd.to_datetime(prices.timestamp,utc=True)
    result=analyze(forecasts,markets,prices,activity_history())
    for name,frame in result.items():frame.to_parquet(OUT/('daily_win_signals_'+name+'.parquet'),index=False)
    receipt=dict(built_at=datetime.now().isoformat(),inputs={name:hashlib.sha256(p.read_bytes()).hexdigest() for name,p in inputs.items()},method=METHOD)
    (OUT/'daily_win_signals_manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
    lines=['# Daily state-winner signal study','',METHOD,'','## Models','',pd.DataFrame(MODEL_LABELS.items(),columns=['Code','Model']).to_markdown(index=False),'']
    for cycle,q in result['overall'].groupby('cycle'):
        lines += [f'## {cycle}: all available daily signals','',rates(q).fillna('—').to_markdown(index=False),'',
            'Rates above use full remaining windows only. Confirmed hits below include incomplete-path witnesses; unknown cases are not failures.','',
            q[q.target.eq('10%')][['model','signals','dates','states','episodes','confirmed','partial_hits','unknown','too_short','lower_bound_pct','equal_state_pct','days_to_hit']].round(2).to_markdown(index=False),'']
    for name,band in [('time','time_band'),('probabilities','probability_band'),('activity','activity_band'),('edges','edge_band'),('states','state')]:
        lines += [f'## Results by {name}','']
        for (cycle,label),q in result[name].groupby(['cycle',band]):lines += [f'### {cycle}: {label}','',rates(q).fillna('—').to_markdown(index=False),'']
    lines += ['## Paired model comparisons: same market and forecast date, 10% target','',result['paired'].round(2).to_markdown(index=False),'',
        '## Forecast-to-market exclusions','',result['audit'].groupby(['cycle','model','reason']).size().rename('observations').reset_index().to_markdown(index=False),'',
        '## Market mapping audit','',result['market_audit'].groupby(['cycle','reason']).size().rename('markets').reset_index().to_markdown(index=False),'']
    report=ROOT/'outputs/reports/research/polymarket_history/daily_win_signals.md';report.write_text('\n'.join(lines).replace('nan','—'))
    dated=ROOT/'outputs/reports/history'/datetime.now().date().isoformat()/'polymarket_history';dated.mkdir(parents=True,exist_ok=True)
    (dated/report.name).write_bytes(report.read_bytes())
    result['report']=report
    print(result['overall'].query('target=="10%"')[['cycle','model','signals','complete','confirmed','partial_hits','unknown','hit_pct']].round(2).to_string(index=False),flush=True)
    return result


if __name__=='__main__':build()
