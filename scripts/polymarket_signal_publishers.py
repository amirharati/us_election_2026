"""Reproducible additional publisher inputs for signal research, never AI calls."""
import argparse
import hashlib
import json
from pathlib import Path
import pandas as pd
import requests
from download_backtest_forecasts import collect, FTE, RTWH
from download_polymarket_history import CACHE, OUT
from published_forecast_review import normalize_538
from compare_current_forecasts import NAMES

ECON='https://raw.githubusercontent.com/TheEconomist/us-midterms-2022-change-data/main/'
PROBES={
    'RTWH 2022 trend':'https://live-data.jifo.co/8d4e07e5-5025-4774-8dea-23c88d3c79b1',
    '538 2024 archive':'https://web.archive.org/web/20241106000000id_/https://projects.fivethirtyeight.com/2024-election-forecast/senate_state_toplines_2024.csv',
}

def ddhq_history(data,state,version):
    # Official titles.089382fb.js plots prob as GOP and 1-prob as DEM.
    parties={c['party'] for c in data['candidates']}
    if parties!={'DEM','GOP'}:raise ValueError('No reviewed two-party candidate mapping')
    q=pd.DataFrame(data['time_series']).rename(columns={'time':'forecast_date'})
    q['forecast_date']=pd.to_datetime(q.forecast_date)
    q=q.drop_duplicates()
    if q.forecast_date.duplicated().any():raise ValueError('Conflicting DDHQ daily probabilities')
    if not q.prob.between(0,1).all():raise ValueError('Invalid DDHQ probability')
    q['p_dem']=1-q.prob;q['cycle']=2024;q['geography']=state
    q['model']='DDHQ' if version=='website_files_harris' else 'DDHQ0'
    if version=='website_files_harris':
        # Exclude reconstructed days before the public relaunch (Aug27).
        q=q[q.forecast_date.ge('2024-08-27')].copy();q['valid_until']=pd.NaT
    else:q['valid_until']=pd.Timestamp('2024-07-21',tz='UTC')
    return q

def economist_original(frame,state):
    q=pd.DataFrame(dict(forecast_date=pd.to_datetime(frame.date,format='%m/%d/%Y'),p_dem=frame.old_dem_win_prob))
    # Correction published Oct31; never backdate the corrected history. Stop the
    # old version when superseded; unavailable later snapshots remain missing.
    # Conservatively begin with the publisher's Sep7 launch announcement.
    q=q[q.forecast_date.ge('2022-09-07') & q.forecast_date.lt('2022-10-31') & q.p_dem.notna()].copy()
    q['cycle']=2022;q['geography']=state;q['model']='ECON'
    q['valid_until']=pd.Timestamp('2022-10-31',tz='UTC')
    return q


def collect_extended(offline=False):
    base=collect(offline=offline);root=CACHE/'publishers'
    # 538 launched June30. Earlier dated rows are retrospective prelaunch data.
    base=base[~base.model.eq('538') | base.forecast_date.ge('2022-06-30')].copy()
    rows=[base];status=pd.read_parquet(OUT/'publisher_status.parquet').to_dict('records')
    q=normalize_538(pd.read_csv(root/'538_2022.csv'),2022)
    for variant,code in [('classic','538C'),('lite','538L')]:
        v=q[q.model.str.lower().str.contains(variant) & q.forecast_date.ge('2022-06-30')].copy()
        if len(v):
            v['model']=code;v['source_url']=FTE;v['source_sha256']=hashlib.sha256((root/'538_2022.csv').read_bytes()).hexdigest()
            v['provenance']='Archived publisher retrospective history; variant of 538, not independent evidence.'
            rows.append(v);status.append(dict(model=code,cycle=2022,status='available',rows=len(v),first=str(v.forecast_date.min().date()),last=str(v.forecast_date.max().date()),url=FTE,error=''))
    for state in ['AZ','GA','NV','PA']:
        url=ECON+'data/'+state.lower()+'_senate_old_v_new.csv';path=root/('econ_'+state+'.csv')
        try:
            if not path.exists():
                if offline:raise FileNotFoundError('Not cached')
                r=requests.get(url,timeout=25);r.raise_for_status();pd.read_csv(__import__('io').StringIO(r.text))['old_dem_win_prob'];path.write_bytes(r.content)
            v=economist_original(pd.read_csv(path),state);v['source_url']=url;v['source_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
            v['provenance']='Publisher original model history, before Oct31 correction. Corrected retrospective probabilities excluded; daily publication vintage not independently verified.'
            rows.append(v);status.append(dict(model='ECON '+state,cycle=2022,status='available',rows=len(v),first=str(v.forecast_date.min().date()),last=str(v.forecast_date.max().date()),url=url,error=''))
        except Exception as e:status.append(dict(model='ECON '+state,cycle=2022,status='unavailable',rows=0,url=url,error=str(e)))
    # Include the local historical roster too: forecast collection must not
    # depend on whether we have a reviewed Polymarket contract for a state.
    mapping=pd.read_parquet(OUT/'date_samples.parquet')
    states=set(mapping.loc[mapping.cycle.eq(2024),'state'])
    local_path=OUT/'dated_forecasts.parquet'
    if local_path.exists():
        local=pd.read_parquet(local_path)
        states.update(local.loc[local.cycle.eq(2024),'geography'])
    for state in sorted(states):
        for version in ['website_files','website_files_harris']:
            url='https://data.ddhq.io/election_center/forecasting/'+version+'/race_outputs/senate-'+NAMES[state].lower().replace(' ','-')+'.json'
            path=root/('ddhq_'+version+'_'+state+'.json')
            try:
                if not path.exists():
                    if offline:raise FileNotFoundError('Not cached')
                    r=requests.get(url,timeout=20);r.raise_for_status();ddhq_history(r.json(),state,version);path.write_bytes(r.content)
                v=ddhq_history(json.loads(path.read_text()),state,version)
                v['source_url']=url;v['source_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
                v['provenance']='Publisher retrospective daily series; original publication vintages not independently verified. GOP prob converted to D. Revised series begins Aug27; original version expires July21.'
                rows.append(v);status.append(dict(model=v.model.iloc[0]+' '+state,cycle=2024,status='available',rows=len(v),first=str(v.forecast_date.min().date()),last=str(v.forecast_date.max().date()),url=url,error=''))
            except Exception as e:status.append(dict(model=('DDHQ' if version.endswith('harris') else 'DDHQ0')+' '+state,cycle=2024,status='unavailable',rows=0,url=url,error=str(e)))
    receipt=root/'additional_probes.json'
    if not offline:
        probes=[]
        for name,url in PROBES.items():
            try:
                r=requests.get(url,timeout=15)
                probes.append(dict(model=name,url=url,http_status=r.status_code,final_url=r.url,
                    status='Not integrated: no validated dated state series',bytes=len(r.content)))
                if r.ok:(root/(name.replace(' ','_')+'_probe.txt')).write_bytes(r.content)
            except Exception as e:probes.append(dict(model=name,url=url,status='Retrieval failed',error=str(e)))
        receipt.write_text(json.dumps(probes,indent=2)+'\n')
    if receipt.exists():
        for r in json.loads(receipt.read_text()):
            if r['model'] not in PROBES:continue
            status.append(dict(model=r['model'],cycle=2022 if '2022' in r['model'] else 2024,status=r['status'],rows=0,url=r['url'],error=r.get('error',f"HTTP {r.get('http_status')}; inspect saved response before integrating")))
    result=pd.concat(rows,ignore_index=True)
    columns=['cycle','forecast_date','geography','seat_class','special','model','p_dem','source_url','source_sha256','provenance','valid_until']
    if 'valid_until' not in result:result['valid_until']=pd.NaT
    result[columns].to_parquet(OUT/'signal_publisher_history.parquet',index=False)
    pd.DataFrame(status).to_parquet(OUT/'signal_publisher_status.parquet',index=False)
    print(pd.DataFrame(status)[['model','cycle','status','rows']].to_string(index=False))
    return result[columns]

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--offline',action='store_true');collect_extended(p.parse_args().offline)
