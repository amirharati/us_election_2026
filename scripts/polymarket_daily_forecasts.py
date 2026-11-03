"""Build a reusable daily Senate forecast panel, independently of signal scoring."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from historical_model_forecasts import infer, fingerprint, CACHE, PROVENANCE
from download_polymarket_history import OUT, ROOT
from polymarket_signal_quality import MODEL_LABELS

ELECTIONS={2022:'2022-11-08',2024:'2024-11-05'}
LOCAL={'GB','ST','OG','OS','MX','M10'}
KEY=['cycle','forecast_date','geography','race_kind','model']


def dates(cycle):
    return pd.date_range(f'{cycle}-09-01',pd.Timestamp(ELECTIONS[cycle])-pd.Timedelta(days=1),tz='UTC')


def local_forecasts(force=False):
    key=fingerprint();rows=[]
    for cycle in ELECTIONS:
        for day in dates(cycle):
            cutoff=day.strftime('%Y-%m-%d');destination=CACHE/cutoff
            receipt=destination/'receipt.json'
            if not force and receipt.exists() and json.loads(receipt.read_text()).get('fingerprint')==key:
                frame=pd.read_parquet(destination/'predictions.parquet')
            else:
                print('Daily inference:',cutoff,flush=True)
                frame=infer(cutoff,destination)
                receipt.write_text(json.dumps(dict(fingerprint=key,cutoff=cutoff,trained_before=cycle,
                    calibration_horizon='Frozen September 17 folds reused at every date',provenance=PROVENANCE),indent=2)+'\n')
            rows.append(frame)
    return pd.concat(rows,ignore_index=True),key


def assemble(local,publishers):
    """Explicit missing rows; no forward fill and no join to markets or outcomes."""
    l=local.rename(columns={'model':'model_name','model_code':'model'}).copy()
    l['source_type']='local_reconstruction';l['source_url']='';l['source_sha256']=''
    p=publishers.copy();p['source_type']='publisher_archive'
    p['model_name']=p.model.map(MODEL_LABELS)
    p['target_id']=None
    for frame in [l,p]:
        special=frame.get('special',pd.Series(False,index=frame.index)).astype('boolean').fillna(False)
        frame['race_kind']=special.map({True:'special',False:'regular'})
    p['forecast_date']=pd.to_datetime(p.forecast_date,utc=True)
    if 'valid_until' in p:
        expiry=pd.to_datetime(p.valid_until,utc=True)
        p=p[expiry.isna() | p.forecast_date.lt(expiry)].copy()
    keep=['cycle','forecast_date','geography','race_kind','model','model_name','target_id','p_dem',
          'source_type','source_url','source_sha256','provenance']
    optional=['prediction_pp','posterior_sd_pp','lo95_pp','hi95_pp','sample_count','firm_count']
    present=pd.concat([l[keep+[c for c in optional if c in l]],p[keep]],ignore_index=True)
    present['forecast_date']=pd.to_datetime(present.forecast_date,utc=True).dt.normalize()
    present=present[present.apply(lambda r: r.forecast_date in dates(int(r.cycle)),axis=1)].copy()
    if present.duplicated(KEY).any():
        raise ValueError('Duplicate state/model/day: resolve contest identity or publisher revisions first')
    if present.p_dem.isna().any() or not present.p_dem.between(-1e-9,1+1e-9).all():
        raise ValueError('Available forecast has invalid probability')
    # Weighted mixture arithmetic can exceed 1 by floating-point roundoff.
    present['p_dem']=present.p_dem.clip(0,1)
    grids=[]
    for cycle in ELECTIONS:
        contests=present.loc[present.cycle.eq(cycle),['geography','race_kind']].drop_duplicates()
        grid=pd.MultiIndex.from_product([[cycle],dates(cycle),list(MODEL_LABELS)],names=['cycle','forecast_date','model']).to_frame(index=False)
        grid=grid.merge(contests,how='cross')
        grids.append(grid)
    result=pd.concat(grids,ignore_index=True).merge(present,on=KEY,how='left',validate='one_to_one')
    result['status']=result.p_dem.notna().map({True:'available',False:'missing'})
    result['missing_reason']=''
    missing=result.p_dem.isna()
    result.loc[missing & result.model.isin(LOCAL),'missing_reason']='Outside supported local historical race roster'
    result.loc[missing & ~result.model.isin(LOCAL),'missing_reason']='No recovered valid publisher snapshot for this day and state'
    result['model_name']=result.model.map(MODEL_LABELS)
    result['source_type']=result.model.isin(LOCAL).map({True:'local_reconstruction',False:'publisher_archive'})
    # Exact publication times are not known. A date-stamped forecast is usable
    # conservatively only after its entire labelled day has ended.
    result['available_after_utc']=result.forecast_date+pd.Timedelta(days=1)
    result.loc[missing,'available_after_utc']=pd.NaT
    result['election_date']=pd.to_datetime(result.cycle.map(ELECTIONS),utc=True)
    result['days_to_election']=(result.election_date-result.forecast_date).dt.days
    return result.sort_values(KEY).reset_index(drop=True)


def build(download=False,offline=False,force=False):
    publisher_path=OUT/'signal_publisher_history.parquet'
    if download or not publisher_path.exists():
        from polymarket_signal_publishers import collect_extended
        collect_extended(offline=offline)
    local,key=local_forecasts(force=force)
    table=assemble(local,pd.read_parquet(publisher_path))
    destination=OUT/'daily_forecasts.parquet';table.to_parquet(destination,index=False)
    coverage=[]
    for (cycle,model),g in table.groupby(['cycle','model']):
        a=g[g.status.eq('available')]
        coverage.append(dict(cycle=cycle,model=model,days=a.forecast_date.nunique(),states=a.geography.nunique(),
                             available=len(a),missing=len(g)-len(a)))
    coverage=pd.DataFrame(coverage)
    manifest=dict(built_at=datetime.now(timezone.utc).isoformat(),file=str(destination.relative_to(ROOT)),
        sha256=hashlib.sha256(destination.read_bytes()).hexdigest(),local_fingerprint=key,
        publisher_sha256=hashlib.sha256(publisher_path.read_bytes()).hexdigest(),
        windows={str(y):[str(dates(y)[0].date()),str(dates(y)[-1].date())] for y in ELECTIONS},
        rows=len(table),available=int(table.p_dem.notna().sum()),no_forward_fill=True,
        timing='Date-stamped forecasts usable after day end UTC; exact publication time unknown.',
        local_provenance=PROVENANCE,coverage=coverage.to_dict('records'))
    (OUT/'daily_forecasts_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    report='# Daily historical Senate forecast dataset\n\n'
    report+='2022: September 1–November 7 (68 days). 2024: September 1–November 4 (65 days).\n\n'
    report+='One row per cycle, date, state, race kind (regular/special) and model. Missing rows are explicit; publisher forecasts are never forward-filled. No market-price, positive-edge or future-path filter selects these rows. No outcome labels are included. This is a reusable forecast dataset, not a trading result.\n\n'
    report+='Local coverage follows the existing supported historical race roster; it is not all Senate contests. Publisher state series are retained separately and are not silently mapped onto special or independent-candidate contracts.\n\n'
    report+=PROVENANCE+' Local calibration remains the frozen September 17 calibration. Publisher histories are retrospective archives, not independently verified original daily publication vintages.\n\n'
    report+=coverage.to_markdown(index=False)+'\n\n'
    report+='Data: `outputs/results/research/polymarket_history/daily_forecasts.parquet` (Git-ignored). Source receipts and the checksum manifest live beside it. Rebuild with `.venv/bin/python scripts/polymarket_daily_forecasts.py`; add `--download-publishers` to retrieve missing publisher archives. Daily inference caches resume interrupted runs. Existing 12-date analysis tables are unchanged.\n'
    latest=ROOT/'outputs/reports/research/polymarket_history/daily_forecasts.md';latest.write_text(report)
    dated=ROOT/'outputs/reports/history'/datetime.now().date().isoformat()/'polymarket_history';dated.mkdir(parents=True,exist_ok=True)
    (dated/'daily_forecasts.md').write_text(report)
    print(coverage.to_string(index=False));print(destination,flush=True)
    return table


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download-publishers',action='store_true')
    parser.add_argument('--offline',action='store_true')
    parser.add_argument('--force',action='store_true')
    args=parser.parse_args();build(args.download_publishers,args.offline,args.force)
