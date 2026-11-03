"""Recover Senate-only on-chain history from the public Envio snapshot.

Original selected event rows stay in ignored cache. Local daily observations
and a market-by-market coverage audit are separate from the backtest inputs.
No AI, credentials, trading, or model training is involved.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse
import gzip
import hashlib
import json
import re
import subprocess
import time

import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import requests

from download_polymarket_history import PublicAPI, GAMMA, OUT as HISTORY, array, write_json

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'cache/polymarket_history/senate_archive'
OUT = ROOT / 'outputs/results/research/senate_archive'
REPO = 'moose-code/polymarket-onchain-v1'
HF = 'https://huggingface.co'
SOURCE = HF + '/datasets/' + REPO
USDC = '0x2791bca1f2de4661ed88a30c99a7a9449aa84174'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def get_json(url):
    for attempt in range(4):
        try:
            r = requests.get(url, timeout=45)
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            if attempt == 3:
                raise
            time.sleep(attempt + 1)


def fetch(revision, name, size=None, offline=False):
    path = CACHE / 'downloads' / name
    if path.exists() and (size is None or path.stat().st_size == size):
        return path
    if offline:
        raise FileNotFoundError('Archive partition is not cached: '+name)
    path.parent.mkdir(parents=True, exist_ok=True)
    url = SOURCE + '/resolve/' + revision + '/' + name
    tmp = path.with_suffix('.part')
    for attempt in range(4):
        try:
            with requests.get(url, stream=True, timeout=(20, 60)) as r:
                r.raise_for_status()
                with tmp.open('wb') as f:
                    for block in r.iter_content(1024 * 1024):
                        f.write(block)
            if size is not None and tmp.stat().st_size != size:
                raise ValueError('Incomplete download: ' + name)
            tmp.replace(path)
            return path
        except (requests.RequestException, ValueError):
            if attempt == 3:
                raise
            time.sleep(attempt + 1)


def scope(row):
    """Collection is broader than model mapping; primary data stays separate."""
    if row.category != 'excluded':
        return row.category
    q, desc = row.question.lower(), row.description.lower()
    if str(row.market_id) == '247671':
        return 'runoff_occurrence'
    if ('primary' in q or 'nomination' in q) and ('senate' in q or
            ('senate' in desc and 'utah republican primary' in q)):
        return 'primary'
    return 'excluded'


def scan_remote(host):
    """Read-only discovery against the user's optional archived Gamma batches."""
    folder=ROOT/'cache/polymarket_history/full_scan'
    folder.mkdir(parents=True,exist_ok=True)
    code='''import os,json,re,sys
root='/mnt/shared/market_data/polymarket/data/market_data'
scanned=0
with os.scandir(root) as files:
 for f in files:
  if not f.name.endswith('.jsonl'):continue
  with open(f.path) as lines:
   for line in lines:
    scanned+=1
    if not re.search(r'senat',line,re.I):continue
    m=json.loads(line)
    text=' '.join(str(m.get(x) or '') for x in ['question','description'])
    if re.search(r'\\bsenat(?:e|or)\\b',text,re.I) and re.search(r'2022|2024',text):
     print(json.dumps(m),flush=True)
print(json.dumps(dict(scanned=scanned)),file=sys.stderr)
'''
    dest=folder/'remote_senate_candidates.jsonl'
    tmp=dest.with_suffix('.tmp')
    with tmp.open('w') as f:
        done=subprocess.run(['ssh','-o','BatchMode=yes',host,'python3 -'],input=code,
                            text=True,stdout=f,stderr=subprocess.PIPE,check=True)
    tmp.replace(dest)
    write_json(folder/'remote_scan.json',dict(host=host,stderr=done.stderr,
        candidate_records=sum(1 for _ in dest.open()),sha256=sha(dest),
        checked_at=pd.Timestamp.now(tz='UTC').isoformat()))


def inventory(offline=False):
    base = pd.read_parquet(HISTORY / 'markets.parquet')
    base['archive_category'] = [scope(r) for r in base.itertuples(index=False)]
    api = PublicAPI(offline=offline)
    # The full metadata scan is an independent discovery cross-check.
    remote = ROOT / 'cache/polymarket_history/full_scan/remote_senate_candidates.jsonl'
    candidates = [json.loads(s) for s in remote.read_text().splitlines()] if remote.exists() else []
    by_id = {str(m['id']): m for m in candidates}
    # Review of the independent archive scan found these missing primary races.
    for mid in ['244921', '244922', '244923']:
        if mid not in set(base.market_id):
            m = by_id.get(mid) or api.get(GAMMA + '/markets/' + mid, {})
            by_id[mid] = m
            labels = array(m.get('outcomes'))
            base.loc[len(base)] = dict(cycle=2022, market_id=mid, event_id='',
                question=m['question'], description=m.get('description',''),
                category='excluded', archive_category='primary',
                exclusion_reason='Primary retained for collection; not a general-election forecast.',
                condition_id=m.get('conditionId',''), market_maker_address=m.get('marketMakerAddress',''),
                outcomes=json.dumps(labels), outcome_first=labels[0], outcome_second=labels[1],
                url='https://polymarket.com/event/'+m.get('slug',''))
    extra = []
    for mid, m in by_id.items():
        if mid not in set(base.market_id):
            q=m.get('question','').lower()
            reason=('House/Senate combined contract.' if 'house' in q else
                    'Leadership, appointment or cabinet event; not a Senate election contract.')
            extra.append(dict(market_id=mid, question=m.get('question', ''), reason=reason))
    pd.DataFrame(extra, columns=['market_id','question','reason']).to_parquet(OUT/'discovery_extra.parquet', index=False)
    raw, rows = [], []
    for r in base[base.archive_category.ne('excluded')].itertuples(index=False):
        m = by_id.get(r.market_id) or api.get(GAMMA + '/markets/' + r.market_id, {})
        outcomes, tokens = array(m.get('outcomes')), array(m.get('clobTokenIds'))
        if len(outcomes) != len(tokens):
            raise ValueError('Outcome/token count mismatch: ' + r.market_id)
        raw.append(m)
        item = r._asdict()
        item.update(tokens=json.dumps(tokens), outcomes=json.dumps(outcomes),
                    volume=float(m.get('volumeNum') or m.get('volume') or 0),
                    market_maker_address=m.get('marketMakerAddress') or r.market_maker_address,
                    condition_id=m.get('conditionId') or r.condition_id,
                    created_at=m.get('createdAt'), closed_at=m.get('closedTime'),
                    end_date=m.get('endDate'), metadata_source='Gamma / archived Gamma metadata')
        rows.append(item)
    write_json(CACHE/'metadata.json', raw)
    base.to_parquet(OUT/'scope_audit.parquet', index=False)
    markets = pd.DataFrame(rows)
    markets.to_parquet(OUT/'markets.parquet', index=False)
    return markets


def collect_remote_prices(host, markets, offline=False):
    """Copy only the requested original price files; never write on the server."""
    rows=[dict(market_id=r.market_id,cycle=r.cycle,outcomes=array(r.outcomes)) for r in markets.itertuples(index=False)]
    code='import json\nROWS=json.loads('+repr(json.dumps(rows))+')\n'+'''
import sys,gzip,re,hashlib
from pathlib import Path
root=Path('/mnt/shared/market_data/polymarket/data/price_history')
with gzip.GzipFile(fileobj=sys.stdout.buffer,mode='wb') as stream:
 for n,m in enumerate(ROWS):
  for i,label in enumerate(m['outcomes']):
   name='price_history_'+m['market_id']+'_'+re.sub(r'[^\\w\\-]','_',label)+'.json'
   p=root/name
   raw=p.read_bytes() if p.exists() else None
   record=dict(cycle=m['cycle'],market_id=m['market_id'],outcome_index=i,outcome=label,
      filename=name,status='found' if raw is not None else 'missing_file',
      source_sha256=hashlib.sha256(raw).hexdigest() if raw is not None else None,
      history=json.loads(raw).get('history',[]) if raw is not None else [])
   stream.write((json.dumps(record,separators=(',',':'))+'\\n').encode())
  if (n+1)%20==0:print('Price archive:',n+1,'markets read',file=sys.stderr,flush=True)
'''
    dest=CACHE/'remote_price_history.jsonl.gz'
    receipt=CACHE/'remote_prices.json'
    if receipt.exists() and json.loads(receipt.read_text()).get('requested_market_ids')!=sorted(markets.market_id):
        tag=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()[:16]
        dest=CACHE/('remote_price_history_'+tag+'.jsonl.gz')
    if not dest.exists():
        if offline:
            raise FileNotFoundError('Original remote price archive is not cached')
        tmp=dest.with_suffix('.tmp')
        with tmp.open('wb') as out:
            subprocess.run(['ssh','-o','BatchMode=yes',host,'python3 -'],input=code.encode(),stdout=out,check=True)
        tmp.replace(dest)
    coverage,daily=[],[]
    with gzip.open(dest,'rt') as f:
        for line in f:
            row=json.loads(line);h=row.pop('history');days={}
            for p in h:
                ts=int(p['t']);value=float(p['p'])
                if not 0<=value<=1:
                    raise ValueError('Invalid archived price')
                day=ts//86400
                if day not in days or ts>days[day][0]:days[day]=(ts,value)
            coverage.append(dict(**row,points=len(h),first=min((int(p['t']) for p in h),default=None),
                last=max((int(p['t']) for p in h),default=None)))
            for ts,value in days.values():
                daily.append(dict(cycle=row['cycle'],market_id=row['market_id'],outcome_index=row['outcome_index'],
                    outcome=row['outcome'],timestamp=pd.Timestamp(ts,unit='s',tz='UTC'),price=value,
                    source='Original archived CLOB price-history observation; not an executable quote'))
    pd.DataFrame(coverage).to_parquet(OUT/'archived_price_coverage.parquet',index=False)
    pd.DataFrame(daily).to_parquet(OUT/'archived_daily_prices.parquet',index=False)
    if {r['market_id'] for r in coverage} != set(markets.market_id):
        raise ValueError('Cached remote price files do not match the requested inventory')
    write_json(CACHE/'remote_prices.json',dict(host=host,file=str(dest.relative_to(ROOT)),sha256=sha(dest),bytes=dest.stat().st_size,
        requested_market_ids=sorted(markets.market_id),outcome_files=len(coverage),
        price_points=sum(r['points'] for r in coverage)))
    print('Original archived price observations:',sum(r['points'] for r in coverage),flush=True)


def select_events(table, entity, addresses, tokens):
    if entity == 'order_filled':
        mask = pc.or_(pc.is_in(table['makerAssetId'], value_set=pa.array(tokens)),
                      pc.is_in(table['takerAssetId'], value_set=pa.array(tokens)))
    else:
        col = ('fpmm_id' if entity.startswith('fpmm_funding_') else
               'market_id' if entity=='fpmm_transaction' else 'id')
        if col not in table.column_names:
            raise ValueError('Missing expected pool-address field: '+col)
        mask = pc.is_in(pc.utf8_lower(table[col]), value_set=pa.array(addresses))
    return table.filter(mask)


def extract(revision, item, addresses, tokens, fingerprint, offline=False):
    name = item['path']
    entity = name.split('/')[0].removesuffix('.parquet')
    selected = CACHE/'selected'/name
    receipt = selected.with_suffix('.json')
    if receipt.exists() and selected.exists():
        old = json.loads(receipt.read_text())
        funding_ok = not entity.startswith('fpmm_funding_') or old.get('address_field')=='fpmm_id'
        if funding_ok and old['revision'] == revision and old['inventory_hash'] == fingerprint and old['selected_sha256'] == sha(selected):
            if item.get('lfs',{}).get('oid') and item['lfs']['oid']!=old['source_sha256']:
                raise ValueError('Cached source checksum mismatch: '+name)
            return old
    original = fetch(revision, name, item['size'], offline=offline)
    selected.parent.mkdir(parents=True, exist_ok=True)
    tmp = selected.with_suffix('.tmp')
    writer, count, scanned = None, 0, 0
    try:
        for batch in pq.ParquetFile(original).iter_batches(batch_size=100000):
            table = pa.Table.from_batches([batch])
            keep = select_events(table, entity, addresses, tokens)
            if writer is None:
                writer = pq.ParquetWriter(tmp, keep.schema, compression='zstd')
            writer.write_table(keep)
            scanned += len(table)
            count += len(keep)
    finally:
        if writer:
            writer.close()
    tmp.replace(selected)
    source_sha=sha(original)
    if item.get('lfs',{}).get('oid') and item['lfs']['oid'] != source_sha:
        raise ValueError('Source checksum mismatch: '+name)
    result = dict(path=name, revision=revision, inventory_hash=fingerprint,
                  address_field='fpmm_id' if entity.startswith('fpmm_funding_') else None,
                  source_bytes=item['size'], source_sha256=source_sha,
                  source_url=SOURCE+'/resolve/'+revision+'/'+name,
                  scanned_rows=scanned, selected_rows=count, selected_sha256=sha(selected),
                  selected_bytes=selected.stat().st_size)
    write_json(receipt, result)
    # Selected rows are the exact original records. Unrelated bulk partitions
    # need not occupy the user's disk after successful validation and extraction.
    original.unlink()
    print(f'{name}: {count:,} Senate rows / {scanned:,} scanned', flush=True)
    return result


def fpmm_prices(frame):
    """Average execution prices; no claim of marginal pool price or bid/ask."""
    cash = frame.tradeAmount.map(int)
    fee = frame.feeAmount.map(int)
    shares = frame.outcomeTokensAmount.map(int)
    if (shares <= 0).any() or (~frame.type.isin(['Buy', 'Sell'])).any():
        raise ValueError('Invalid FPMM amount or side')
    gross = cash.where(frame.type.eq('Buy'), cash + fee)
    net = (cash - fee).where(frame.type.eq('Buy'), cash)
    return pd.DataFrame({'execution_price': cash / shares,
                         'price_before_fee': (cash - fee).where(frame.type.eq('Buy'), cash + fee) / shares,
                         'fee_per_share': fee / shares,
                         'cash_gross': gross, 'cash_net': net})


def observations(markets):
    address_map = {str(r.market_maker_address).lower(): r for r in markets.itertuples(index=False) if r.market_maker_address}
    token_map = {str(t): (r, i, array(r.outcomes)[i]) for r in markets.itertuples(index=False) for i,t in enumerate(array(r.tokens))}
    pools_path = CACHE/'selected/fixed_product_market_maker.parquet'
    pools = pd.read_parquet(pools_path)
    pools.to_parquet(OUT/'legacy_pools.parquet', index=False)
    pool_map = {r.id.lower():r for r in pools.itertuples(index=False)}
    chunks, exclusions = [], []
    for p in sorted((CACHE/'selected/fpmm_transaction').rglob('*.parquet')):
        d = pd.read_parquet(p)
        if d.empty:
            continue
        d['pool'] = d.market_id.str.lower()
        zero=d.outcomeTokensAmount.map(int).eq(0)
        for row in d[zero].itertuples(index=False):
            if int(row.tradeAmount)!=0 or int(row.feeAmount)!=0:
                raise ValueError('Cash transfer without outcome shares')
            exclusions.append(dict(source='FPMM',market_id=address_map[row.pool].market_id,
                event_id=row.id,reason='Zero-amount event retained in raw data; no execution price.'))
        d=d[~zero].copy()
        if d.empty:
            continue
        calc = fpmm_prices(d)
        for address, g in d.groupby('pool'):
            market = address_map[address]
            pool = pool_map[address]
            # Only these validated binary USDC pools are converted to prices.
            if pool.collateralToken.lower() != USDC or int(pool.outcomeSlotCount) != 2 or list(pool.conditions) != [market.condition_id]:
                raise ValueError('Unreviewed pool metadata: '+market.market_id)
            idx = g.outcomeIndex.astype(int)
            if not idx.isin([0,1]).all():
                raise ValueError('Unexpected outcome index')
            c = calc.loc[g.index]
            chunks.append(pd.DataFrame(dict(cycle=market.cycle,market_id=market.market_id,
                event_id=g.id,timestamp=pd.to_datetime(g.timestamp.astype('int64'),unit='s',utc=True),
                outcome_index=idx,outcome=idx.map(dict(enumerate(array(market.outcomes)))),
                price=c.price_before_fee.astype(float),execution_price=c.execution_price.astype(float),
                fee_per_share=c.fee_per_share.astype(float),side=g.type,
                source='FPMM average execution; fee removed; not a quote')))
    for p in sorted((CACHE/'selected/order_filled').rglob('*.parquet')):
        d = pd.read_parquet(p)
        if d.empty:
            continue
        noncash=d.makerAssetId.ne('0') & d.takerAssetId.ne('0')
        for row in d[noncash].itertuples(index=False):
            for mid in {token_map[t][0].market_id for t in [row.makerAssetId,row.takerAssetId] if t in token_map}:
                exclusions.append(dict(source='CLOB',market_id=mid,event_id=row.id,
                    reason='Token/token fill retained in raw data; no simple collateral price.'))
        # A fill may involve two outcome assets. Keep original rows regardless,
        # but only collateral-vs-token events have this simple price formula.
        for asset_col, other_col, qty_col, cash_col in [
            ('makerAssetId','takerAssetId','makerAmountFilled','takerAmountFilled'),
            ('takerAssetId','makerAssetId','takerAmountFilled','makerAmountFilled')]:
            ok = d[other_col].eq('0') & d[asset_col].isin(token_map)
            for token, g in d[ok].groupby(asset_col):
                market, index, label = token_map[token]
                qty = g[qty_col].map(int)
                if (qty <= 0).any():
                    raise ValueError('Zero-sized exchange fill')
                price = g[cash_col].map(int) / qty
                chunks.append(pd.DataFrame(dict(cycle=market.cycle,market_id=market.market_id,
                    event_id=g.id,timestamp=pd.to_datetime(g.timestamp.astype('int64'),unit='s',utc=True),
                    outcome_index=index,outcome=label,price=price.astype(float),
                    execution_price=price.astype(float),fee_per_share=float('nan'),
                    side='maker sells' if asset_col=='makerAssetId' else 'maker buys',
                    source='CLOB on-chain fill; fee separate in raw event; not a quote')))
    pd.DataFrame(exclusions,columns=['source','market_id','event_id','reason']).to_parquet(OUT/'normalization_audit.parquet',index=False)
    result = pd.concat(chunks,ignore_index=True)
    if result.duplicated(['event_id','market_id','outcome_index']).any():
        raise ValueError('Duplicate event/outcome across archive partitions')
    if not result.price.between(0,1).all():
        raise ValueError('Derived prices outside [0,1]')
    parts = result.event_id.str.split('_',expand=True)
    result['block_number'],result['log_index'] = parts[1].astype('int64'),parts[2].astype('int64')
    result = result.sort_values(['timestamp','block_number','log_index','outcome_index'])
    result.to_parquet(CACHE/'observations.parquet', index=False,compression='zstd')
    result['date'] = result.timestamp.dt.floor('D')
    keys = ['cycle','market_id','outcome_index','outcome','date']
    last = result.groupby(keys,sort=False).tail(1).copy()
    sizes = result.groupby(keys).size().rename('observations').reset_index()
    daily = last.merge(sizes,on=keys,validate='one_to_one')
    daily.to_parquet(OUT/'daily_observations.parquet',index=False)
    return result, daily, pools


def report(markets, obs, daily, pools, receipts, revision):
    normalization=pd.read_parquet(OUT/'normalization_audit.parquet')
    pool_checks=pools[['id','tradesQuantity','liquidityAddQuantity','liquidityRemoveQuantity']].copy()
    for entity,column in [('fpmm_funding_addition','liquidityAddQuantity'),('fpmm_funding_removal','liquidityRemoveQuantity')]:
        events=pd.read_parquet(CACHE/'selected'/(entity+'.parquet'))
        counts=events.groupby(events.fpmm_id.str.lower()).size()
        pool_checks[entity+'_observed']=pool_checks.id.str.lower().map(counts).fillna(0).astype(int)
        pool_checks[entity+'_matches']=pool_checks[entity+'_observed'].eq(pool_checks[column].astype(int))
    pool_checks.to_parquet(OUT/'liquidity_audit.parquet',index=False)
    rows=[]
    for m in markets.itertuples(index=False):
        g=obs[obs.market_id.eq(m.market_id)]
        cutoff=pd.Timestamp(f'{m.cycle}-11-'+('08' if m.cycle==2022 else '05'),tz='UTC')
        pre=g[g.timestamp.lt(cutoff)]
        pool=pools[pools.id.str.lower().eq(str(m.market_maker_address).lower())]
        expected=int(pool.tradesQuantity.iloc[0]) if len(pool)==1 else None
        omitted=normalization[normalization.market_id.eq(m.market_id)]
        actual=len(g[g.source.str.startswith('FPMM')])+len(omitted[omitted.source.eq('FPMM')])
        rows.append(dict(cycle=m.cycle,market_id=m.market_id,question=m.question,category=m.archive_category,
            outcomes=len(array(m.outcomes)),observed_outcomes=g.outcome_index.nunique(),
            observations=len(g),pre_general_election=len(pre),first=g.timestamp.min(),last=g.timestamp.max(),
            status='available' if len(g) else ('no_recorded_trades_zero_volume' if m.volume==0 else 'no_matching_events'),
            retained_unpriced_events=len(omitted),
            legacy_expected_trades=expected,legacy_observed_trades=actual,
            legacy_count_matches=(expected==actual) if expected is not None else None))
    coverage=pd.DataFrame(rows)
    coverage.to_parquet(OUT/'coverage.parquet',index=False)
    summary=coverage.groupby(['cycle','category']).agg(markets=('market_id','size'),
        with_events=('observations',lambda s:int(s.gt(0).sum())),observations=('observations','sum'),
        pre_election=('pre_general_election','sum')).reset_index()
    summary.to_parquet(OUT/'summary.parquet',index=False)
    meta=dict(collected_at=pd.Timestamp.now(tz='UTC').isoformat(),source=SOURCE,revision=revision,
        license='CC-BY-4.0; attribution: Envio (envio.dev)',
        scope='2022/2024 Senate general, control, margins, seats, runoff occurrence and Senate primaries; no House/presidential combinations.',
        time_scope='All available FPMM partitions; CLOB exchange events from inception through December 2024.',
        raw_cache=str(CACHE.relative_to(ROOT)),selected_raw_rows=sum(r['selected_rows'] for r in receipts),
        scanned_rows=sum(r['scanned_rows'] for r in receipts),source_bytes=sum(r['source_bytes'] for r in receipts),
        selected_raw_bytes=sum(r['selected_bytes'] for r in receipts),partitions=receipts,
        caveats=['Third-party blockchain index; not guaranteed exhaustive for deleted or misdated markets.',
                 'Archive state rows are retrospective; never use them as dated forecast features.',
                 'Average executed prices are not historical bid/ask quotes or marginal pool probabilities.',
                 'Raw exchange fills can contain matching-engine counterpart events; do not sum their volume as independent trades.',
                 'Daily files keep the last observed event and its actual timestamp; missing days stay missing.',
                 'Zero-amount and token/token events remain in the raw extract; normalization_audit explains why they have no derived price.',
                 'Primary and runoff contracts require separate forecast mappings. No new backtest or strategy claim.'],
        files={p.name:sha(p) for p in OUT.glob('*.parquet')})
    remote_receipt=CACHE/'remote_prices.json'
    if remote_receipt.exists():
        meta['original_price_archive']=json.loads(remote_receipt.read_text())
    remote_scan=ROOT/'cache/polymarket_history/full_scan/remote_scan.json'
    if remote_scan.exists():
        meta['independent_metadata_scan']=json.loads(remote_scan.read_text())
    write_json(OUT/'collection.json',meta)
    text='# Historical Senate archive coverage\n\n'
    text+=f'Generated {meta["collected_at"]}. Source: [Envio on-chain archive]({SOURCE}), snapshot `{revision}`. CC-BY-4.0; attribution: Envio.\n\n'
    text+=summary.to_markdown(index=False)+'\n\n'
    text+='Full Senate-only event rows are saved in `cache/polymarket_history/senate_archive/selected/`. '
    text+='Compact daily observations and coverage are saved in `outputs/results/research/senate_archive/`. '
    text+='Raw original fields, both outcomes, fees, block/log identities and available post-election events are retained. '
    text+='Post-election events are not eligible for pre-election prediction tests.\n\n'
    text+='## Interpretation and limits\n\n'+'\n'.join('- '+v for v in meta['caveats'])+'\n\n'
    text+='FPMM prices remove fees from buy payments and add fees back to sell receipts, then divide by outcome shares. '
    text+='This is the average price for that transaction. Separate fields preserve actual cash-per-share and fee-per-share. '
    text+='CLOB prices divide the collateral amount by the outcome-token amount; raw fee fields are retained.\n\n'
    legacy=coverage.dropna(subset=['legacy_count_matches'])
    text+=f'Legacy event-count audit: {int(legacy.legacy_count_matches.sum())} of {len(legacy)} pool totals match the source snapshot.\n\n'
    liquidity_ok=pool_checks[['fpmm_funding_addition_matches','fpmm_funding_removal_matches']].all(axis=1)
    text+=f'Liquidity-event audit: additions and removals both match for {int(liquidity_ok.sum())} of {len(pool_checks)} pools.\n\n'
    for cycle,g in coverage.groupby('cycle'):
        text+=f'## {cycle}: every market\n\n'+g[['market_id','question','observations','pre_general_election','status']].to_markdown(index=False)+'\n\n'
    price_coverage=OUT/'archived_price_coverage.parquet'
    if price_coverage.exists():
        ap=pd.read_parquet(price_coverage)
        text+='\n## Original archived price files\n\n'
        text+='These are independently saved CLOB price-history observations from the original downloader. '
        text+='Empty files are reported as empty; they are not evidence of no trading. Full histories stay in the ignored cache.\n\n'
        text+=ap.groupby('cycle').agg(outcome_files=('market_id','size'),
            nonempty=('points',lambda s:int(s.gt(0).sum())),points=('points','sum')).reset_index().to_markdown(index=False)+'\n'
    for folder in [ROOT/'outputs/reports/research/senate_archive',ROOT/'outputs/reports/history'/str(pd.Timestamp.now().date())/'senate_archive']:
        folder.mkdir(parents=True,exist_ok=True);(folder/'report.md').write_text(text)
    print(summary.to_string(index=False),flush=True)
    print('Missing:',coverage.loc[coverage.observations.eq(0),['market_id','question']].to_dict('records'),flush=True)


def collect(workers=3, offline=False):
    CACHE.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    markets=inventory(offline=offline)
    closure=pd.to_datetime(markets.closed_at,utc=True,errors='coerce',format='mixed')
    if closure.isna().any() or (closure>=pd.Timestamp('2025-01-01',tz='UTC')).any():
        raise ValueError('A market closes outside the reviewed archive period; extend partition coverage before proceeding.')
    addresses=sorted({str(x).lower() for x in markets.market_maker_address if x})
    tokens=sorted({str(t) for x in markets.tokens for t in array(x)})
    fingerprint=hashlib.sha256(json.dumps([addresses,tokens]).encode()).hexdigest()
    pin=CACHE/'snapshot.json'
    recipe=json.loads((ROOT/'config/polymarket_archive.json').read_text())
    if recipe['dataset']!=REPO:
        raise ValueError('Unexpected archive dataset in configuration')
    revision=recipe['revision']
    if pin.exists():
        if json.loads(pin.read_text())['revision']!=revision:
            raise ValueError('Cached snapshot differs from config/polymarket_archive.json; use a separate cache for a new snapshot.')
    else:
        write_json(pin,dict(revision=revision,source=SOURCE))
    listing=[]
    for entity in ['fpmm_transaction','order_filled']:
        listing_file=CACHE/(entity+'_listing.json')
        if listing_file.exists():
            items=json.loads(listing_file.read_text())
        else:
            if offline:
                raise FileNotFoundError('Archive listing is not cached: '+entity)
            items=get_json(HF+'/api/datasets/'+REPO+'/tree/'+revision+'/'+entity+'?recursive=true&limit=1000')
            write_json(listing_file,items)
        for item in items:
            if item.get('type')!='file':continue
            if entity=='order_filled' and int(re.search(r'year=(\d+)',item['path'])[1])>2024:continue
            listing.append(item)
    root_listing=CACHE/'root_listing.json'
    if root_listing.exists():
        root_items=json.loads(root_listing.read_text())
    else:
        if offline:
            raise FileNotFoundError('Archive root listing is not cached')
        root_items=get_json(HF+'/api/datasets/'+REPO+'/tree/'+revision)
        write_json(root_listing,root_items)
    listing.extend(x for x in root_items if x['path'] in ['fixed_product_market_maker.parquet','fpmm_funding_addition.parquet','fpmm_funding_removal.parquet'])
    print(f'{len(markets)} markets; {len(listing)} files; {sum(x["size"] for x in listing)/1e9:.2f} GB scanned, only Senate rows retained.',flush=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        receipts=list(pool.map(lambda item:extract(revision,item,addresses,tokens,fingerprint,offline=offline),listing))
    write_json(CACHE/'receipts.json',receipts)
    obs,daily,pools=observations(markets)
    remote_receipt=CACHE/'remote_prices.json'
    if remote_receipt.exists() and not all((OUT/name).exists() for name in ['archived_daily_prices.parquet','archived_price_coverage.parquet']):
        collect_remote_prices(json.loads(remote_receipt.read_text())['host'],markets,offline=True)
    report(markets,obs,daily,pools,receipts,revision)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--offline',action='store_true',help='Rebuild only from verified local receipts and cached source responses.')
    parser.add_argument('--scan-remote',help='Optional SSH host with the original Polymarket metadata archive (read-only).')
    parser.add_argument('--remote-prices',help='Optional SSH host for the original Senate price-history files.')
    args=parser.parse_args()
    if args.offline and (args.scan_remote or args.remote_prices):
        parser.error('--offline cannot be combined with remote downloads')
    if args.scan_remote:
        scan_remote(args.scan_remote)
    collect(args.workers,offline=args.offline)
    if args.remote_prices:
        collect_remote_prices(args.remote_prices,pd.read_parquet(OUT/'markets.parquet'))
        obs=pd.read_parquet(CACHE/'observations.parquet')
        report(pd.read_parquet(OUT/'markets.parquet'),obs,pd.read_parquet(OUT/'daily_observations.parquet'),
            pd.read_parquet(OUT/'legacy_pools.parquet'),json.loads((CACHE/'receipts.json').read_text()),
            json.loads((CACHE/'snapshot.json').read_text())['revision'])
