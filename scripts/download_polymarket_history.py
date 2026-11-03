"""Collect only 2022/2024 Senate election contracts and bounded daily prices.

Public, unauthenticated APIs. Raw responses and compact research tables are
Git-ignored local data. Empty history is a coverage gap, never a zero price.
"""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import argparse
import gzip
import hashlib
import json
import re
import time
import requests
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/results/research/polymarket_history'
CACHE = ROOT / 'cache/polymarket_history'
GAMMA = 'https://gamma-api.polymarket.com'
CLOB = 'https://clob.polymarket.com'
ELECTIONS = {2022: '2022-11-08', 2024: '2024-11-05'}
SEEDS = {2022: ['2022-us-senate-elections-will-a-dem-or-rep-win-this-state'],
         2024: ['which-party-will-control-the-us-senate-after-the-2024-election']}


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2, default=str, allow_nan=False) + '\n')
    tmp.replace(path)


class PublicAPI:
    def __init__(self, offline=False, refresh=False):
        self.offline, self.refresh = offline, refresh

    def get(self, url, params):
        key = hashlib.sha256(json.dumps([url, params], sort_keys=True).encode()).hexdigest()
        path = CACHE / 'responses' / (key + '.json.gz')
        if path.exists() and (self.offline or not self.refresh):
            with gzip.open(path, 'rt') as f:
                return json.load(f)['data']
        if self.offline:
            raise FileNotFoundError('Uncached historical request: ' + url + ' ' + str(params))
        for attempt in range(3):
            try:
                r = requests.get(url, params=params, timeout=25)
                r.raise_for_status()
                data = r.json()
                path.parent.mkdir(parents=True, exist_ok=True)
                tmp = path.with_suffix('.tmp')
                with gzip.open(tmp, 'wt') as f:
                    json.dump(dict(url=url, params=params, retrieved_at=datetime.now(timezone.utc).isoformat(), data=data), f)
                tmp.replace(path)
                return data
            except (requests.RequestException, ValueError):
                if attempt == 2:
                    raise
                time.sleep(0.5 * (attempt + 1))


def event_pages(api, year):
    """Do not assume requested page size: Gamma may cap it silently."""
    # Monthly discovery avoids Gamma's offset ceiling for a whole election year.
    boundaries = pd.date_range(f'{year}-01-01', f'{year+1}-02-01', freq='MS')
    for lower, upper in zip(boundaries[:-1], boundaries[1:]):
        offset, seen = 0, set()
        while True:
            batch = api.get(GAMMA + '/events', dict(closed='true', end_date_min=str(lower.date()),
                           end_date_max=str(upper.date()), limit=100, offset=offset))
            if not isinstance(batch, list):
                raise ValueError('Expected an event list')
            if not batch:
                break
            ids = {str(e['id']) for e in batch}
            if ids <= seen:
                raise ValueError('Pagination repeated a page; refusing a false complete inventory')
            seen |= ids
            yield from batch
            offset += len(batch)
            if offset > 2000:
                raise ValueError('Monthly discovery exceeds API offset limit; split this month further')


def classify(event, market, year):
    text = ' '.join(str(x or '') for x in [event.get('title'), market.get('question'), market.get('description')]).lower()
    question = str(market.get('question', '')).lower()
    if not re.search(r'\bsenate\b|\bsenator\b', text):
        return None
    if not re.search(r'\b' + str(year) + r'\b', text):
        return ('excluded', 'Election cycle is not explicit in the contract or event.')
    if re.search(r'primary|nomination|nominee', question):
        return ('excluded', 'Primary nomination contract.')
    if re.search(r'presiden|\bhouse\b|balance of power', question):
        return ('excluded', 'Combined or non-Senate election contract.')
    if re.search(r'pass |confirm|resign|retire|filibuster|bill|act by|appointed|sign.*statement', question):
        return ('excluded', 'Legislative or personnel event, not an election outcome.')
    if re.search(r'margin|percentage|%|\bpoints?\b', question):
        return ('margin', '')
    if re.search(r'\bseats?\b|how many', question):
        return ('seats', '')
    if re.search(r'control|majority', question):
        return ('control', '')
    if re.search(r'win|winner|elected', question):
        return ('winner', '')
    return ('excluded', 'Unrecognized Senate contract; retained for review.')


def array(value):
    return json.loads(value) if isinstance(value, str) else (value or [])


def catalog(api, years):
    rows, seen = [], set()
    for year in years:
        count = 0
        events = list(event_pages(api, year))
        for slug in SEEDS[year]:
            events.extend(api.get(GAMMA + '/events', {'slug': slug}))
        for e in events:
            for m in e.get('markets', []):
                key = str(m['id'])
                if key in seen:
                    continue
                result = classify(e, m, year)
                if result is None:
                    continue
                seen.add(key)
                category, reason = result
                outcomes, tokens = array(m.get('outcomes')), array(m.get('clobTokenIds'))
                terminal = array(m.get('outcomePrices'))
                # A terminal market quote is not silently treated as a verified payout.
                resolved = m.get('umaResolutionStatus') == 'resolved' and bool(m.get('closed'))
                payout = float(terminal[0]) if resolved and len(terminal) == 2 and all(float(v) in [0., 1.] for v in terminal) and sum(map(float, terminal)) == 1 else None
                end = pd.Timestamp('2022-12-06' if year == 2022 and 'runoff' in str(m.get('question','')).lower() else ELECTIONS[year], tz='UTC')
                if 'runoff' in (str(m.get('question', '')) + str(m.get('description', ''))).lower():
                    # Keep runoff-linked contracts but don't reuse a general-election model.
                    reason = reason or 'Runoff-linked settlement requires a separate forecast mapping.'
                created = pd.to_datetime(m.get('startDate') or e.get('startDate'), utc=True, errors='coerce')
                start = max(pd.Timestamp(f'{year}-01-01', tz='UTC'), created.floor('D')) if pd.notna(created) else pd.Timestamp(f'{year}-01-01', tz='UTC')
                rows.append(dict(cycle=year, market_id=key, event_id=str(e['id']), question=m.get('question', ''),
                    condition_id=m.get('conditionId',''), market_maker_address=m.get('marketMakerAddress',''),
                    legacy_amm=bool(m.get('fpmmLive')) and m.get('enableOrderBook') is not True,
                    enable_order_book=m.get('enableOrderBook') is True, volume=float(m.get('volumeNum') or 0),
                    category=category, exclusion_reason=reason, outcomes=json.dumps(outcomes),
                    token=str(tokens[0]) if len(tokens) == 2 and len(outcomes) == 2 else '',
                    outcome_first=outcomes[0] if outcomes else '', outcome_second=outcomes[1] if len(outcomes)>1 else '',
                    description=m.get('description', ''), url='https://polymarket.com/event/' + e.get('slug',''),
                    start=start.isoformat(), stop=end.isoformat(), resolution_status=m.get('umaResolutionStatus', ''),
                    payout_first=payout, terminal_quote_first=float(terminal[0]) if terminal else None,
                    settlement_source='API resolved binary payout' if payout is not None else 'Unverified; terminal quote is not a payout'))
                count += category != 'excluded'
        print(f'{year}: examined {len(events)} events; {count} relevant Senate contracts.', flush=True)
    return pd.DataFrame(rows)


def windows(start, stop, days=14):
    start, stop = pd.Timestamp(start), pd.Timestamp(stop)
    while start < stop:
        end = min(start + pd.Timedelta(days=days), stop)
        yield int(start.timestamp()), int(end.timestamp())
        start = end


def history(api, row):
    prices, errors, requests_count = {}, [], 0
    if row.category == 'excluded' or not row.token:
        return [], dict(market_id=row.market_id, cycle=row.cycle, status='excluded' if row.category=='excluded' else 'no_tokens', points=0, requests=0, errors='')
    if pd.Timestamp(row.start) >= pd.Timestamp(row.stop):
        return [], dict(market_id=row.market_id, cycle=row.cycle, status='opened_after_cutoff', points=0, requests=0,
                        errors='', reason='Market opened on or after the pre-election history cutoff; later prices are not eligible.')
    for start, end in windows(row.start, row.stop):
        requests_count += 1
        try:
            result = api.get(CLOB + '/prices-history', {'market': row.token, 'startTs': start, 'endTs': end, 'fidelity': 1440})
            if not isinstance(result.get('history'), list):
                raise ValueError('Invalid price history response')
            for p in result['history']:
                ts, value = int(p['t']), float(p['p'])
                if start <= ts < end and 0 <= value <= 1:
                    prices[ts] = value
        except Exception as exc:
            errors.append(f'{start}: {type(exc).__name__}: {exc}')
    points = [dict(cycle=row.cycle, market_id=row.market_id, timestamp=pd.Timestamp(ts, unit='s', tz='UTC'), price_first=p,
                   price_source='CLOB daily history; not an executable quote') for ts,p in sorted(prices.items())]
    status = 'partial' if errors else 'available' if points else 'empty_history'
    if status == 'empty_history' and getattr(row, 'legacy_amm', False):
        status = 'legacy_amm_history_required'
    reason = 'Legacy liquidity-pool market; the CLOB history endpoint does not supply its AMM trading history.' if status == 'legacy_amm_history_required' else ''
    return points, dict(market_id=row.market_id, cycle=row.cycle, status=status, points=len(points), requests=requests_count, errors='; '.join(errors), reason=reason)


def collect(years=(2022,2024), offline=False, refresh=False, workers=6):
    if not set(years) <= set(ELECTIONS):
        raise ValueError('Only the 2022 and 2024 Senate cycles are supported')
    api = PublicAPI(offline, refresh)
    markets = catalog(api, years)
    if markets.empty:
        raise ValueError('No Senate catalog returned')
    prices, statuses = [], []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for i,(p,s) in enumerate(pool.map(lambda row: history(api,row), markets.itertuples(index=False)),1):
            prices.extend(p); statuses.append(s)
            if i % 10 == 0:
                print(f'History checked: {i}/{len(markets)} contracts', flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    markets.to_parquet(OUT/'markets.parquet', index=False)
    pd.DataFrame(prices, columns=['cycle','market_id','timestamp','price_first','price_source']).to_parquet(OUT/'prices.parquet', index=False)
    pd.DataFrame(statuses).to_parquet(OUT/'coverage.parquet', index=False)
    meta = dict(collected_at=datetime.now(timezone.utc).isoformat(), cycles=list(years), frequency_minutes=1440,
                history_stop='00:00 UTC on general-election day, or Dec6 for explicit2022 runoff contracts; no election-night prices',
                inventory_method='All closed events ending within cycle January through next January, plus known legacy seeds; text-reviewed categories. Not a guarantee of every deleted or misdated market.',
                outcome='First named outcome; never assume token zero is Yes', raw_cache='cache/polymarket_history/responses',
                files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.parquet') if p.name in ['markets.parquet','prices.parquet','coverage.parquet']})
    write_json(OUT/'collection.json', meta)
    print(pd.DataFrame(statuses).groupby(['cycle','status']).size().to_string(), flush=True)
    return OUT


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles', nargs='+', type=int, default=[2022,2024])
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--refresh', action='store_true', help='Explicitly retry cached responses, including empty histories')
    parser.add_argument('--workers', type=int, default=6)
    args = parser.parse_args()
    collect(args.cycles, args.offline, args.refresh, args.workers)
