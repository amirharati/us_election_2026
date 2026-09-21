"""Parse frozen public September 18 captures; keep margins and probabilities separate."""
from pathlib import Path
import json,re,hashlib
import numpy as np
import pandas as pd

STATE_NAMES='AL:Alabama|AK:Alaska|AZ:Arizona|AR:Arkansas|CA:California|CO:Colorado|CT:Connecticut|DE:Delaware|FL:Florida|GA:Georgia|HI:Hawaii|ID:Idaho|IL:Illinois|IN:Indiana|IA:Iowa|KS:Kansas|KY:Kentucky|LA:Louisiana|ME:Maine|MD:Maryland|MA:Massachusetts|MI:Michigan|MN:Minnesota|MS:Mississippi|MO:Missouri|MT:Montana|NE:Nebraska|NV:Nevada|NH:New Hampshire|NJ:New Jersey|NM:New Mexico|NY:New York|NC:North Carolina|ND:North Dakota|OH:Ohio|OK:Oklahoma|OR:Oregon|PA:Pennsylvania|RI:Rhode Island|SC:South Carolina|SD:South Dakota|TN:Tennessee|TX:Texas|UT:Utah|VT:Vermont|VA:Virginia|WA:Washington|WV:West Virginia|WI:Wisconsin|WY:Wyoming'
NAMES=dict(x.split(':') for x in STATE_NAMES.split('|'));ABBR={v:k for k,v in NAMES.items()}
RACE_URL='https://www.racetothewh.com/senate/26'
SILVER_URL='https://www.natesilver.net/p/nate-silver-2026-midterm-election-polls-model'
KALSHI_URL='https://api.elections.kalshi.com/trade-api/v2/events/CONTROLS-2026?with_nested_markets=true'
POLY_URL='https://polymarket.com/event/which-party-will-win-the-senate-in-2026'


def race_rows(payload):
    probabilities=[]
    for row in payload['data'][6][1:]:
        name=row[0]
        if name not in ABBR:continue # Explicit placeholder rows, not real contests.
        for party,value in zip(['D','R','I'],row[1:]):
            if not value:continue
            candidate,prob=value.rsplit(':',1);normalized=party
            if (name,candidate) in [('Idaho','Achilles'),('South Dakota','Bengs')]:normalized='I'
            probabilities.append(dict(state=ABBR[name],candidate=candidate,source_party_column=party,
                party=normalized,win_probability_pct=float(prob.strip().rstrip('%'))))
    probs=pd.DataFrame(probabilities);rows=[]
    for row in payload['data'][7][1:]:
        if row[0] not in ABBR:continue
        state=ABBR[row[0]];margin=next(v for v in row[1:] if v)
        leader,amount=re.match(r'([DRI]) \+([\d.]+)%',margin).groups()
        pp=float(amount)*(1 if leader=='D' else -1)
        p=probs[probs.state.eq(state)]
        vals={party:p.loc[p.party.eq(party),'win_probability_pct'].sum(min_count=1) for party in ['D','R','I']}
        rows.append(dict(state=state,race_leader=leader,race_display_margin=margin,
            race_margin_DR_pp=pp if state not in ['ID','MT','NE','SD'] else np.nan,
            race_margin_basis='major_candidates_not_DR' if state in ['ID','MT','NE','SD'] else 'published_DR_not_harmonized',
            race_D_probability=vals['D'],race_R_probability=vals['R'],race_I_probability=vals['I']))
    result=pd.DataFrame(rows)
    assert len(result)==35 and result.state.is_unique
    assert np.allclose(probs.groupby('state').win_probability_pct.sum(),100)
    return result,probs


def kalshi_rows(source):
    metadata={r['name']:r for r in json.loads((source/'comparison_download_manifest.json').read_text())}
    rows=[]
    for path in sorted(source.glob('kalshi_*.json')):
        payload=json.loads(path.read_text());event=payload.get('event',{})
        if not event.get('title','').endswith(' Senate winner?'):continue
        # Contract geography is read from title AND resolution rule. Ticker LA is Kentucky!
        state_name=event['title'].removesuffix(' Senate winner?');state=ABBR[state_name]
        for m in event['markets']:
            assert 'Senator of '+state_name+' ' in m['rules_primary']
            suffix=m['ticker'].split('-')[-1];party=suffix if suffix in ['D','R'] else 'I'
            bid=100*float(m['yes_bid_dollars']);ask=100*float(m['yes_ask_dollars'])
            assert 0<=bid<=ask<=100
            rows.append(dict(state=state,event_ticker=event['event_ticker'],ticker=m['ticker'],candidate_label=m['yes_sub_title'],
                party=party,bid_pct=bid,ask_pct=ask,mid_pct=(bid+ask)/2,rule=m['rules_primary'],
                captured_at=metadata[path.stem]['retrieved_at'],url=metadata[path.stem]['url']))
    result=pd.DataFrame(rows);assert not result.duplicated(['state','party']).any()
    return result


def build_comparison(source,out):
    source,out=Path(source),Path(out)
    rp=json.loads((source/'racetowh_live_6911ecb8-c744-4464-a182-70568e288364.json').read_text())
    race,probabilities=race_rows(rp);quotes=kalshi_rows(source)
    current=pd.read_parquet(out/'current_states.parquet').sort_values('state')
    comp=current.merge(race,on='state',validate='one_to_one')
    for party in ['D','R','I']:
        q=quotes[quotes.party.eq(party)][['state','bid_pct','ask_pct','mid_pct']].rename(columns={c:f'kalshi_{party}_{c}' for c in ['bid_pct','ask_pct','mid_pct']})
        comp=comp.merge(q,on='state',how='left',validate='one_to_one')
    comp['call_disagreement']=comp.model_caucus.ne(comp.race_leader)
    comp['our_model_as_of']='2026-09-17'
    comp['race_updated']=rp['data'][3][0][0]
    comp['kalshi_note']=comp.state.map({'KY':'Ticker SENATELA maps to Kentucky by title and contract rule.',
        'SC':'Candidate label Darline Graham is inconsistent; contract is Republican party, South Carolina.',
        'ID':'D contract label David Roth is stale; Achilles is independent.',
        'SD':'D contract label Beaudion is stale/withdrawn; Bengs is independent.',
        'NE':'Osborn independent probability is separate from D contract.'}).fillna('')
    km=json.loads((source/'kalshi_CONTROLS-2026.json').read_text())['event']['markets']
    kd=next(m for m in km if m['ticker'].endswith('-D'))
    poly=json.loads((source/'polymarket_control.txt').read_text())[0]
    pm=next(m for m in poly['markets'] if 'Democrat' in m['question'])
    # Public introduction is accessible; detailed Silver state/seat table is paywalled.
    from bs4 import BeautifulSoup
    silver_text=BeautifulSoup((source/'silver_public.txt').read_text(),'html.parser').get_text(' ',strip=True)
    assert re.search(r'59\s*(?:%|percent)',silver_text)
    sd=34+int(comp.model_caucus.eq('D').sum());sr=100-sd
    top=pd.DataFrame([
        dict(source='Our bias-corrected polling',D_seats=sd,R_seats=sr,seat_measure='conditional point calls',D_control_pct=np.nan,D_bid_pct=np.nan,D_ask_pct=np.nan,as_of='2026-09-17',url='local frozen model'),
        dict(source='Race to the WH',D_seats=float(rp['data'][1][1][1].split()[0]),R_seats=float(rp['data'][1][1][2].split()[0]),seat_measure='published expected seats',D_control_pct=float(rp['data'][0][1][1].split('%')[0]),as_of=rp['data'][3][0][0],url=RACE_URL),
        dict(source='Silver Bulletin Deluxe',D_seats=np.nan,R_seats=np.nan,seat_measure='not publicly accessible',D_control_pct=59.,as_of='2026-09-18 public introduction',url=SILVER_URL),
        dict(source='Kalshi Senate control',D_seats=np.nan,R_seats=np.nan,seat_measure='control contract only',D_control_pct=50*(float(kd['yes_bid_dollars'])+float(kd['yes_ask_dollars'])),D_bid_pct=100*float(kd['yes_bid_dollars']),D_ask_pct=100*float(kd['yes_ask_dollars']),as_of='2026-09-18T18:16:48Z capture',url=KALSHI_URL),
        dict(source='Polymarket Senate control',D_seats=np.nan,R_seats=np.nan,seat_measure='control contract only',D_control_pct=50*(pm['bestBid']+pm['bestAsk']),D_bid_pct=100*pm['bestBid'],D_ask_pct=100*pm['bestAsk'],as_of=poly['updatedAt'],url=POLY_URL),
    ])
    for name,df in dict(current_comparison=comp,external_topline=top,racetowh_candidate_probabilities=probabilities,kalshi_contract_quotes=quotes).items():df.to_parquet(out/(name+'.parquet'),index=False)
    (out/'external_sources.json').write_text(json.dumps(dict(source_directory=str(source.resolve()),files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.iterdir() if p.is_file()},
        race_update=rp['data'][3][0][0],race_refresh=rp['refreshed'],kalshi_geography_policy='event title checked against resolution rule, never ticker alone',
        probability_policy='retain quoted bid/ask and midpoint; no normalization of separate contracts; no conversion of our margins to probabilities',
        race_party_overrides={'ID/Achilles':'independent','SD/Bengs':'independent'},
        silver='59 percent from public Sep18 introduction; no detailed subscriber-only forecasts accessed',
        comparison_limitations='Our Sep17 inputs versus Sep18 sources; published margin definitions not harmonized; candidate/ballot and caucus restrictions remain.'),indent=2)+'\n')
    (out/'compare_current_forecasts.py').write_bytes(Path(__file__).read_bytes())
    refresh_manifest(out)
    print(top.to_string(index=False));print('Disagree:',comp.loc[comp.call_disagreement,'state'].tolist());print('Kalshi states:',quotes.state.nunique())
    return comp,top


def refresh_manifest(out):
    (out/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name!='manifest.json'},indent=2)+'\n')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path,required=True);p.add_argument('--review-dir',type=Path,required=True);a=p.parse_args()
    build_comparison(a.source_dir,a.review_dir)
