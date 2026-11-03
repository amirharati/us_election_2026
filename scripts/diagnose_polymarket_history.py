"""Explain historical price gaps using fresh public API probes (no API keys)."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import argparse
import json
import pandas as pd
import requests
from download_polymarket_history import OUT, CACHE, write_json


def probe(row):
    record=dict(cycle=int(row.cycle),market_id=row.market_id,question=row.question,checked_at=datetime.now(timezone.utc).isoformat())
    try:
        r=requests.get('https://gamma-api.polymarket.com/markets/'+row.market_id,timeout=20);r.raise_for_status();raw=r.json()
        record.update(fpmm=bool(raw.get('fpmmLive')),orderbook=raw.get('enableOrderBook') is True,
                      amm_address=raw.get('marketMakerAddress',''),volume=float(raw.get('volumeNum') or 0))
        r=requests.get('https://clob.polymarket.com/markets/'+raw['conditionId'],timeout=20)
        record['clob_status']=r.status_code
        # Diagnostic whole-life availability probe, not an input to the pre-election dataset.
        r=requests.get('https://data-api.polymarket.com/v2/prices-history',params={
            'token_id':row.token,'interval':'max','bucket_seconds':43200},timeout=20)
        record['v2_status']=r.status_code;r.raise_for_status();data=r.json()
        points=data.get('data',[])
        record.update(v2_points=len(points),v2_first_timestamp=points[0]['timestamp'] if points else None,
                      v2_has_more=data.get('pagination',{}).get('has_more'))
        if pd.Timestamp(row.start)>=pd.Timestamp(row.stop):
            record['diagnosis']='Opened after pre-election cutoff; any later prices are outside the backtest.'
        elif record['fpmm'] and record['clob_status']==404:
            record['diagnosis']='Legacy AMM contract absent from CLOB. Recover AMM history from an archive or on-chain events.'
        else:record['diagnosis']='Unresolved source gap; investigate without treating missing prices as zero.'
    except Exception as exc:record['error']=f'{type(exc).__name__}: {exc}'
    return record


def diagnose(refresh=False):
    markets=pd.read_parquet(OUT/'markets.parquet');coverage=pd.read_parquet(OUT/'coverage.parquet')
    q=markets.merge(coverage[['market_id','status']],on='market_id',validate='one_to_one')
    q=q[q.status.isin(['empty_history','legacy_amm_history_required','opened_after_cutoff','partial'])]
    receipt=CACHE/'diagnosis_receipt.json'
    if receipt.exists() and not refresh:
        saved=json.loads(receipt.read_text());rows=saved['rows']
        if set(r['market_id'] for r in rows)!=set(q.market_id):raise ValueError('Gap inventory changed; rerun with --refresh')
    else:
        with ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(probe,q.itertuples(index=False)))
        write_json(receipt,dict(checked_at=datetime.now(timezone.utc).isoformat(),rows=rows))
    result=pd.DataFrame(rows);result.to_parquet(OUT/'history_diagnosis.parquet',index=False)
    print(result[['cycle','market_id','clob_status','v2_points','diagnosis']].to_string(index=False))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--refresh',action='store_true')
    diagnose(parser.parse_args().refresh)
