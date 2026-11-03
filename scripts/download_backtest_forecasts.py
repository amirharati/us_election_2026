"""Optional archived publisher inputs for the 2022/2024 Senate backtest.

Downloads are independent of market downloads and local model execution.
Failures remain visible and never turn into invented model probabilities.
"""
import argparse
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
import pandas as pd
import requests
from download_polymarket_history import ROOT, OUT, CACHE, PublicAPI, write_json
from compare_current_forecasts import NAMES

RTWH='https://live-data.jifo.co/a5b574eb-6085-4eff-90d6-6cf9a2aa0fee'
FTE='https://web.archive.org/web/20250306125236id_/https://projects.fivethirtyeight.com/2022-general-election-forecast-data/senate_state_toplines_2022.csv'


def collect(offline=False):
    from published_forecast_review import rttwh_history, normalize_538
    root=CACHE/'publishers';root.mkdir(parents=True,exist_ok=True)
    rows=[];status=[]
    for name,year,url,filename in [('RTWH',2024,RTWH,'rtwh_2024.json'),('538',2022,FTE,'538_2022.csv')]:
        path=root/filename
        try:
            if not path.exists():
                if offline: raise FileNotFoundError('Publisher is not cached')
                response=requests.get(url,timeout=30);response.raise_for_status()
                # Parse before publishing the cache entry; HTML errors are never cached as data.
                if name=='RTWH':response.json()
                elif 'forecastdate' not in response.text[:3000]:raise ValueError('Response is not a forecast CSV')
                path.write_bytes(response.content)
            if name=='RTWH':
                q=rttwh_history(path,{v:k for k,v in NAMES.items()});q['model']='RTWH'
            else:
                q=normalize_538(pd.read_csv(path),year)
                # Deluxe is the single benchmark; other variants are not extra independent models.
                q=q[q.model.str.lower().str.contains('deluxe')].copy();q['model']='538'
            if q.empty:raise ValueError('No supported Senate forecasts were parsed')
            q['source_url']=url;q['source_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
            q['provenance']='Publisher retrospective history; original daily publication snapshots are not independently verified.'
            rows.append(q)
            status.append(dict(model=name,cycle=year,status='available',rows=len(q),first=str(q.forecast_date.min().date()),last=str(q.forecast_date.max().date()),url=url,error=''))
        except Exception as exc:
            status.append(dict(model=name,cycle=year,status='unavailable',rows=0,first='',last='',url=url,error=f'{type(exc).__name__}: {exc}'))
    OUT.mkdir(parents=True,exist_ok=True)
    columns=['cycle','forecast_date','geography','seat_class','special','model','p_dem','source_url','source_sha256','provenance']
    q=pd.concat(rows,ignore_index=True) if rows else pd.DataFrame(columns=columns)
    q[columns].to_parquet(OUT/'publisher_history.parquet',index=False)
    pd.DataFrame(status).to_parquet(OUT/'publisher_status.parquet',index=False)
    print(pd.DataFrame(status).to_string(index=False))
    return q


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--offline',action='store_true')
    collect(parser.parse_args().offline)
