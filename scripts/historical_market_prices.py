"""Dated prediction-price inputs, with audited reconstruction of legacy pools."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from download_polymarket_history import ROOT, OUT, write_json

ARCHIVE=ROOT/'outputs/results/research/senate_archive'
RAW=ROOT/'cache/polymarket_history/senate_archive/selected'


def replay_pool(events):
    """Replay binary FPMM balances in chain order; price0 = reserve1 / total.

    Funding amounts are actual net outcome tokens added/removed. Buy cash enters
    both reserves net of fees; a sale removes returnAmount+fee from both reserves.
    A drained pool emits an unavailable price, never a fabricated 0 or 1.
    """
    reserve=[0,0];rows=[]
    for e in sorted(events,key=lambda e:tuple(map(int,e['id'].split('_')[1:]))):
        kind=e['kind'];before=list(reserve)
        if kind in ['add','remove']:
            sign=1 if kind=='add' else -1
            amount=e['amountsAdded'] if kind=='add' else e['amountsRemoved']
            if len(amount)!=2:raise ValueError('Not a binary pool')
            reserve=[v+sign*int(a) for v,a in zip(reserve,amount)]
        else:
            index=int(e['outcomeIndex']);shares=int(e['outcomeTokensAmount'])
            if index not in [0,1]:raise ValueError('Invalid outcome index')
            cash=int(e['tradeAmount']);fee=int(e['feeAmount'])
            if kind=='Buy':
                reserve=[v+cash-fee for v in reserve];reserve[index]-=shares
            elif kind=='Sell':
                reserve=[v-cash-fee for v in reserve];reserve[index]+=shares
            else:raise ValueError('Unknown pool event')
        if min(reserve)<0:raise ValueError('Negative reconstructed reserves at '+e['id'])
        if reserve==before:continue
        probability=reserve[1]/sum(reserve) if min(reserve)>0 else np.nan
        rows.append(dict(event_id=e['id'],timestamp=pd.Timestamp(int(e['timestamp']),unit='s',tz='UTC'),
                         price_first=probability))
    return rows,reserve


def reconstruct_pools():
    pools=pd.read_parquet(ARCHIVE/'legacy_pools.parquet')
    markets=pd.read_parquet(ARCHIVE/'markets.parquet')
    files=[*sorted((RAW/'fpmm_transaction').rglob('*.parquet')),
           RAW/'fpmm_funding_addition.parquet',RAW/'fpmm_funding_removal.parquet']
    if not all(p.exists() for p in files) or len(files)<3:
        raise FileNotFoundError('Run scripts/prepare_historical_markets.py to restore the legacy event cache.')
    grouped={str(a).lower():[] for a in pools.id}
    for path in files:
        frame=pd.read_parquet(path)
        for e in frame.to_dict('records'):
            if 'fpmm_id' in e:
                address=e['fpmm_id'].lower();e['kind']='add' if 'addition' in path.name else 'remove'
            else:address=e['market_id'].lower();e['kind']=e['type']
            grouped[address].append(e)
    mapped={str(m.market_maker_address).lower():m for m in markets.itertuples(index=False)}
    rows=[];audit=[]
    for p in pools.itertuples(index=False):
        m=mapped[p.id.lower()]
        events=grouped[p.id.lower()]
        if len({e['id'] for e in events})!=len(events):raise ValueError('Duplicate pool event')
        history,reserve=replay_pool(events)
        expected=list(map(int,p.outcomeTokenAmounts))
        if reserve!=expected:raise ValueError('Reconstructed balances disagree with snapshot: '+m.market_id)
        audit.append(dict(market_id=m.market_id,cycle=m.cycle,pool=p.id,events=len(events),
                          reserves_match=True,final_reserve_0=str(reserve[0]),final_reserve_1=str(reserve[1])))
        rows.extend(dict(cycle=m.cycle,market_id=m.market_id,**r,
            price_source='Reconstructed FPMM marginal probability, before fees') for r in history)
    prices=pd.DataFrame(rows)
    prices['day']=prices.timestamp.dt.floor('D')
    # Input is already in block/log order, including events sharing a timestamp.
    prices=prices.groupby(['market_id','day'],sort=False).tail(1).drop(columns='day')
    prices.to_parquet(ARCHIVE/'reconstructed_pool_prices.parquet',index=False)
    pd.DataFrame(audit).to_parquet(ARCHIVE/'pool_reconstruction_audit.parquet',index=False)
    write_json(ARCHIVE/'pool_reconstruction.json',dict(
        method='Binary constant-product reserves replay; p0=reserve1/(reserve0+reserve1); no fees or slippage.',
        snapshots_used_only_for_validation=True,
        sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        pools_verified=len(audit)))
    return prices


def prediction_prices():
    """Choose a documented source per market; keep event timestamps and blanks."""
    base=pd.read_parquet(OUT/'prices.parquet').copy()
    if not (ARCHIVE/'daily_observations.parquet').exists():
        raise FileNotFoundError('Run scripts/prepare_historical_markets.py to recover the Senate archive first.')
    pool=reconstruct_pools()
    trades=pd.read_parquet(ARCHIVE/'daily_observations.parquet')
    trades['price_first']=np.where(trades.outcome_index.eq(0),trades.price,1-trades.price)
    trades['price_source']='Last on-chain execution probability proxy; outcome 1 complemented when used'
    trades=trades.sort_values(['timestamp','block_number','log_index']).copy()
    trades['day']=trades.timestamp.dt.floor('D')
    trades=trades.groupby(['market_id','day'],sort=False).tail(1)
    columns=['cycle','market_id','timestamp','price_first','price_source']
    sources=[pool[columns]]
    chosen=set(pool.loc[pool.price_first.notna(),'market_id'])
    # Empty legacy pool objects attached to CLOB markets do not override prices.
    sources[0]=sources[0][sources[0].market_id.isin(chosen)]
    path=ARCHIVE/'archived_daily_prices.parquet'
    if path.exists():
        archived=pd.read_parquet(path)
        archived=archived[archived.outcome_index.eq(0)].rename(columns={'price':'price_first','source':'price_source'})
        archived=archived[~archived.market_id.isin(chosen)]
        sources.append(archived[columns]);chosen.update(archived.market_id)
    # Public daily chart prices are preferable to individual fills for this
    # descriptive comparison when the user's optional original archive is absent.
    for frame in [base,trades]:
        frame=frame[~frame.market_id.isin(chosen)]
        sources.append(frame[columns]);chosen.update(frame.market_id)
    result=pd.concat(sources,ignore_index=True).sort_values(['market_id','timestamp'])
    result.to_parquet(OUT/'prediction_prices.parquet',index=False)
    return result
