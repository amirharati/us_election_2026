"""Public publisher snapshots and exact-event comparisons; no fitted distributions."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import unicodedata

import pandas as pd
import requests
from bs4 import BeautifulSoup
import election_lab as lab
from compare_current_forecasts import ABBR
from data_utils import atomic_json

RT = 'Race to the WH'
DD = 'DDHQ'
URLS = {RT: 'https://www.racetothewh.com/senate/26', DD: 'https://votes.decisiondeskhq.com/forecast/2026/senate'}
# Publisher display-name aliases; these never join different people.
DISPLAY_ALIASES = {
    'James Risch': ['Jim Risch'],  # https://www.risch.senate.gov/about/about-jim/
    'Ed Markey': ['Edward Markey'],  # DDHQ Massachusetts named candidate page
    'Ben Ray Luján': ['Ray Luján'],  # RTWH label; https://www.lujan.senate.gov/about/
    'N’Kiyla Jasmine Thomas': ["N'Kiyla Thomas"],  # DDHQ Oklahoma named candidate page
}


def name_key(name):
    return ''.join(c for c in unicodedata.normalize('NFKD',name.replace('’',"'")) if not unicodedata.combining(c)).casefold()


FEED = 'https://live-data.jifo.co/6911ecb8-c744-4464-a182-70568e288364'
METHOD = ('RTWH and DDHQ are separate published forecasts, not new mixture components. '
          'They use the same ask depth, fees and sensitivity stresses as our models. '
          'Their displayed probabilities are point estimates, not confidence bounds; no state margin distribution is invented. '
          'DDHQ uses market inputs where disclosed, so its agreement with prices is not independent evidence. '
          'Publisher dates are independent of our forecast cutoff. Failed refreshes and forecasts older than the age limit are unpriced. '
          'Independent candidates stay separate from Democrats. Chamber comparisons remain conditional on publisher caucus conventions. '
          'Silver public commentary and Inside Elections ratings remain in notebook 04; they are not numerical state models here.')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def flight(html):
    parts=[]
    for s in BeautifulSoup(html, 'html.parser').find_all('script'):
        t=s.string or ''
        if t.startswith('self.__next_f.push('):
            v=json.loads(t[len('self.__next_f.push('):-1])
            if len(v)>1 and isinstance(v[1], str):parts.append(v[1])
    return ''.join(parts)


def field(text, key, predicate):
    values={}
    for m in re.finditer('"'+re.escape(key)+'":', text):
        try:v,_=json.JSONDecoder().raw_decode(text[m.end():].lstrip())
        except ValueError:continue
        if predicate(v):values[digest(v)]=v
    if len(values)!=1:raise ValueError('Missing or ambiguous publisher field: '+key)
    return next(iter(values.values()))


def probability(value):
    p=float(value)
    if not 0<=p<=1:raise ValueError('Invalid publisher probability')
    return p


def parse_rttwh(data):
    from live_published_comparison import parse_rttwh as validate
    checked=validate(data)
    sheets=dict(zip(data['sheetNames'],data['data']));races={}
    for row in sheets['Win'][1:]:
        if row[0] not in ABBR:continue
        candidates=[]
        for party,cell in zip(['DEM','REP','IND'],row[1:4]):
            if not cell:continue
            name,p=cell.rsplit(':',1)
            candidates.append(dict(name=name.strip(),party=party,p=probability(float(p.strip().rstrip('%'))/100),source_party=party))
        races[ABBR[row[0]]]=dict(candidates=candidates,published_date=checked['published_date'],source_url=URLS[RT],market_weight=None)
    if len(races)!=35:raise ValueError('Expected 35 unique Senate races')
    return dict(model=RT,published_date=checked['published_date'],control=checked['D_control_pct']/100,
                expected_D=checked['expected_D'],races=races,seat_bins=None,source_url=URLS[RT])


def parse_ddhq_national(html):
    text=flight(html)
    over=field(text,'overviews',lambda v:isinstance(v,list) and len(v)==1 and isinstance(v[0],dict) and 'forecast' in v[0])[0]['forecast']
    if over.get('year')!=2026:raise ValueError('Wrong forecast year')
    parties={p['shortAbbrev']:p for p in over['parties']}
    if not {'D','R'}<=parties.keys():raise ValueError('Missing chamber parties')
    p=probability(parties['D']['winProbability'])
    bins=field(text,'simulations',lambda v:isinstance(v,list) and bool(v) and isinstance(v[0],dict) and 'count' in v[0])
    cleaned=[]
    for b in bins:
        counts={x['partyId']:x['seats'] for x in b['parties']}
        d,r=counts[parties['D']['partyId']],counts[parties['R']['partyId']]
        if d+r!=100 or any(int(x)!=x or x<0 for x in [d,r,b['count']]):raise ValueError('Invalid seat histogram')
        cleaned.append(dict(D=int(d),R=int(r),count=int(b['count'])))
    total=sum(x['count'] for x in cleaned)
    if total<=0 or len({x['D'] for x in cleaned})!=len(cleaned):raise ValueError('Invalid histogram mass or duplicate bins')
    if abs(sum(x['count'] for x in cleaned if x['D']>=51)/total-p)>.011:raise ValueError('Seat histogram disagrees with control topline')
    return dict(model=DD,published_date=over['updatedAt'][:10],control=p,races={},seat_bins=cleaned,
                simulation_draws=total,source_url=URLS[DD],expected_D=sum(x['D']*x['count'] for x in cleaned)/total)


def parse_ddhq_race(html,url):
    d=field(flight(html),'forecast',lambda v:isinstance(v,dict) and 'raceId' in v and 'parties' in v)
    candidates=[]
    for p in d['parties']:
        # A party aggregate with multiple named contenders cannot be assigned to one person.
        names=[' '.join([c['firstName'],c['lastName']]).strip() for c in p['candidates']]
        candidates.append(dict(name=names[0] if len(names)==1 else '',party={'D':'DEM','R':'REP','I':'IND'}.get(p['shortAbbrev'],p['shortAbbrev']),
                               p=probability(p['winProbability']),source_party=p['shortAbbrev'],members=names))
    if abs(sum(c['p'] for c in candidates)-1)>.025:raise ValueError('Race probabilities do not sum to one within publisher rounding')
    return dict(candidates=candidates,published_date=d['updatedAt'][:10],source_url=url,market_weight=d.get('composition',{}).get('markets'))


def fetch(model, timeout=30):
    receipts=[]
    def get(url):
        r=requests.get(url,timeout=timeout);r.raise_for_status()
        receipts.append(dict(url=url,sha256=hashlib.sha256(r.content).hexdigest()))
        return r.text
    if model==RT:payload=parse_rttwh(json.loads(get(FEED)))
    else:
        html=get(URLS[DD]);payload=parse_ddhq_national(html)
        links=set(re.findall(r'href="(/races/2026-11-03/[^" ]+/forecast)"',html))
        wanted={}
        for name,state in ABBR.items():
            matches=[u for u in links if u.startswith('/races/2026-11-03/'+name.lower().replace(' ','-')+'-us-senate-')]
            if len(matches)>1:raise ValueError('Ambiguous Senate seat '+state)
            if matches:wanted[state]='https://votes.decisiondeskhq.com'+matches[0]
        if len(wanted)!=35:raise ValueError('Expected 35 DDHQ race links')
        def race(item):
            state,url=item
            try:return state,parse_ddhq_race(get(url),url)
            except Exception as e:return state,dict(error=str(e),source_url=url)
        with ThreadPoolExecutor(max_workers=6) as pool:payload['races']=dict(pool.map(race,wanted.items()))
    payload['schema_version']=1
    payload['receipts']=sorted(receipts,key=lambda x:x['url']);payload['retrieved_at']=datetime.now(timezone.utc).isoformat()
    return payload


def read_snapshot(path):
    d=json.loads(Path(path).read_text())
    if digest(d['payload'])!=d['sha256']:raise ValueError('External snapshot checksum mismatch')
    return d['payload']


def load(offline=False, force=False, ttl_hours=6, timeout=30):
    """Downloads are independent of model inference and market quote refreshes."""
    cache=lab.ROOT/'cache/polymarket_external';cache.mkdir(parents=True,exist_ok=True)
    fallback=lab.ROOT/'outputs/reports/markets/polymarket/external_forecasts.json'
    old_bundle=read_snapshot(fallback) if fallback.exists() else {}
    result={};now=datetime.now(timezone.utc)
    for model in [RT,DD]:
        path=cache/('rttwh.json' if model==RT else 'ddhq.json')
        old=read_snapshot(path) if path.exists() else old_bundle.get(model)
        age=(now-datetime.fromisoformat(old['retrieved_at'])).total_seconds()/3600 if old and old.get('retrieved_at') else float('inf')
        if offline:
            value=dict(old or {},refresh_status='offline snapshot' if old else 'unavailable')
        elif old and old.get('schema_version')==1 and not force and 0<=age<=ttl_hours and old.get('refresh_status')!='stale after failure':
            value=dict(old,refresh_status='recent publisher cache')
        else:
            try:
                value=dict(fetch(model,timeout),refresh_status='checked online')
                atomic_json(path,dict(payload=value,sha256=digest(value)))
            except Exception as e:value=dict(old or {},refresh_status='stale after failure',refresh_error=str(e))
        result[model]=value
    return result


def normalized_candidates(race, policy):
    """Exact full names or unique publisher surname abbreviations, scoped to state."""
    known=policy.get('candidates',[]);out=[];notes=[]
    for c in race['candidates']:
        name=c['name'];matches=[]
        if not name and len(c.get('members',[]))>1:
            out.append(c)
            notes.append('Publisher party aggregate covers multiple candidates and is not assigned to an individual.')
            continue
        for k in known:
            names=k.get('source_names',[k['name']])+[k['name']]+DISPLAY_ALIASES.get(k['name'],[])
            if any(name_key(name)==name_key(n) or (' ' not in name and name_key(name)==name_key(n.split()[-1])) for n in names):matches.append(k)
        if known and len(matches)!=1:raise ValueError('Publisher candidate does not match reviewed current roster: '+name)
        actual=matches[0]['party'] if matches else c['party']
        if actual!=c['party']:
            # Some published D columns include named independents. Never turn them into Democrats.
            if actual=='IND' and c['party'] in ['DEM','IND']:notes.append(name+' retains IND despite publisher column.')
            else:raise ValueError('Publisher party conflicts with reviewed candidate: '+name)
        out.append({**c,'party':actual,'name':matches[0]['name'] if matches else name})
    represented={name_key(c['name']) for c in out if c['name']}
    represented.update(name_key(n) for c in out for n in c.get('members',[]))
    missing=[k['name'] for k in known if name_key(k['name']) not in represented]
    if missing:notes.append('Publisher omits separate probabilities for reviewed contenders: '+', '.join(missing)+'.')
    return out,notes


def assess(row,rules,snapshot,review,now=None,max_age_days=3):
    now=now or datetime.now(timezone.utc)
    result=dict(model_low=None,model_high=None,probability_kind='Unavailable public forecast',mapping='Not priced',reason='No public distribution for this market type',state=None,
                publisher_date=snapshot.get('published_date'),publisher_url=snapshot.get('source_url'),market_weight=None)
    def unavailable(reason):return {**result,'reason':reason}
    def fresh(date):
        age=(now.date()-datetime.fromisoformat(date).date()).days
        return 0<=age<=max_age_days
    if snapshot.get('refresh_status') not in ['checked online','recent publisher cache','offline snapshot']:return unavailable('Publisher unavailable or refresh failed; cached data is not used to signal an opportunity.')
    cat=row['category'];q=row['question'];rule=rules[row['rules_id']]
    p=None;formula=None;notes=[];kind='Published point probability; confidence bounds unavailable'
    if cat=='Senate race winners':
        states={abbr for name,abbr in ABBR.items() if re.search(r'\b'+re.escape(name)+r'\b',row['event']+' '+q,re.I)}
        if len(states)!=1:return unavailable('Multiple or unknown states; no public joint-state distribution.')
        state=next(iter(states));result['state']=state
        race=snapshot.get('races',{}).get(state,{})
        if not race or race.get('error'):return unavailable('Publisher race unavailable: '+race.get('error','no record'))
        result.update(publisher_date=race['published_date'],publisher_url=race['source_url'],market_weight=race.get('market_weight'))
        if any(x in (row['event']+' '+q+' '+rule).lower() for x in ['first round','county']):return unavailable('Contract is not a statewide final-election winner.')
        try:candidates,notes=normalized_candidates(race,review.get(state,{}))
        except ValueError as e:return unavailable(str(e))
        party='DEM' if 'Democrats win' in q else 'REP' if 'Republicans win' in q else 'IND' if re.search(r'an independent win',q,re.I) else None
        if party:chosen=[c for c in candidates if c['party']==party]
        else:
            m=re.fullmatch(r'Will (.+) win the .+ Senate race in 2026\?',q)
            chosen=[c for c in candidates if m and name_key(c['name'])==name_key(m[1])]
        if not chosen:return unavailable('Requested party/candidate has no published probability; absence is not treated as zero.')
        if not party and len(chosen)!=1:return unavailable('Candidate probability is ambiguous.')
        p=sum(c['p'] for c in chosen);formula='Published P('+ (party or chosen[0]['name']) +' wins)'
        notes.append('Final-election publisher probability; current candidate and contract rules must agree.')
    elif cat=='Senate control':
        if 'Democratic Party' in q:p=snapshot.get('control');formula='Published P(D controls Senate)'
        elif 'Republican Party' in q:
            if snapshot.get('control') is not None:p=1-snapshot['control']
            formula='1 - published P(D controls Senate)'
        notes.append('Conditional on publisher caucus accounting, complete chamber and GOP tie-break convention; independents are not reclassified as Democrats in state contracts.')
    elif cat=='Senate seat counts':
        bins=snapshot.get('seat_bins')
        if not bins:return unavailable('Publisher supplies no seat-count distribution; expected seats cannot price this contract.')
        m=re.fullmatch(r'Will the (Republican|Democratic) Party hold (?:exactly )?(\d+)( or fewer| or more)? Senate seats after the 2026 midterm elections\?',q)
        if not m:return unavailable('Unrecognized exact-seat or seat-threshold contract.')
        party='R' if m[1]=='Republican' else 'D';n=int(m[2]);op=m[3] or ''
        mask=lambda b:b[party]<=n if 'fewer' in op else b[party]>=n if 'more' in op else b[party]==n
        p=sum(b['count'] for b in bins if mask(b))/sum(b['count'] for b in bins)
        formula=f'Sum published histogram: {party} seats '+ ('<=' if 'fewer' in op else '>=' if 'more' in op else '=')+f' {n}'
        kind='Published seat histogram; simulation error remains; no model-confidence interval'
        notes.append('Conditional on publisher caucus/seat accounting matching settlement; no joint state simulations are available.')
    else:return unavailable('Publisher has no full margin or joint-state distribution for this contract; no Gaussian approximation is substituted.')
    if not result['publisher_date'] or not fresh(result['publisher_date']):return unavailable('Publisher forecast is future-dated or older than the configured age limit.')
    if p is None:return unavailable('Requested publisher probability is unavailable.')
    p=probability(p)
    if snapshot.get('model')==DD:
        weight=result['market_weight'];notes.append(f'DDHQ uses {100*weight:g}% market inputs for this race.' if weight is not None else 'DDHQ incorporates market inputs; this is not independent corroboration of market prices.')
    notes.append('Published rounding is retained; equal endpoints represent one estimate, not certainty.')
    return {**result,'model_low':p,'model_high':p,'probability_kind':kind,'mapping':'Conditional public comparison','reason':' '.join(notes),'event_formula':formula,
            'simulation_draws':snapshot.get('simulation_draws') if cat=='Senate seat counts' else None}


def status_table(snapshots):
    return pd.DataFrame([{'Model': 'RTWH' if name==RT else 'DDHQ','Published':s.get('published_date','Unavailable'),
                          'Refresh':s.get('refresh_status','unavailable'),'Race records':sum(not r.get('error') for r in s.get('races',{}).values()),
                          'Note':s.get('refresh_error','State winners/control; no margin distribution.' if name==RT else 'Seat histogram available. Includes market inputs.')} for name,s in snapshots.items()])
