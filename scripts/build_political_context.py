"""Build a complete day-dated party-control reference, independently of polls."""
import argparse
from bisect import bisect_right
from datetime import date,timedelta
import json
from pathlib import Path
from data_utils import LAB,Snapshot,csv_bytes,digest

CONFIG=LAB/'config/political_context_v1.json'

def state_on(config,when):
    d=date.fromisoformat(str(when))
    if not date.fromisoformat(config['coverage_start'])<=d<=date.fromisoformat(config['reviewed_through']):
        raise ValueError('Date outside source-reviewed coverage; update the reviewed configuration first')
    def find(rows):
        i=bisect_right([r[0] for r in rows],d.isoformat())-1
        if i<0:raise ValueError('Uncovered date')
        return i,rows[i]
    _,house=find(config['house_transitions']);_,senate=find(config['senate_transitions'])
    i,president=find(config['presidents']);party_start=president[0]
    while i>0 and config['presidents'][i-1][2]==president[2]:
        i-=1;party_start=config['presidents'][i][0]
    wh=president[2];note=''
    for exc in config['exceptions']:
        if exc['start']<=d.isoformat()<exc['end_exclusive']:note=exc['note']
    return {'date':d.isoformat(),'president':president[1],'wh_party':wh,'house_party':house[1],
            'senate_party':senate[1],'unified_government':int(wh==house[1]==senate[1]),
            'split_congress':int(house[1]!=senate[1]),'wh_matches_house':int(wh==house[1]),
            'wh_matches_senate':int(wh==senate[1]),'presidential_election_year':int(d.year%4==0),
            'midterm_election_year':int(d.year%4==2),'president_days_in_office':(d-date.fromisoformat(president[0])).days,
            'wh_party_days_in_power':(d-date.fromisoformat(party_start)).days,'control_definition_note':note}

def build(config_path=CONFIG,root=LAB/'data/political_context/prepared'):
    config=json.loads(config_path.read_text());src=LAB/config['source_directory']
    assert digest((src/'manifest.json').read_bytes())==config['source_manifest_sha256']
    manifest=json.loads((src/'manifest.json').read_text())
    for name,meta in manifest.items():
        if 'sha256' in meta:assert digest((src/name).read_bytes())==meta['sha256'],name
    start=date.fromisoformat(config['coverage_start']);end=date.fromisoformat(config['reviewed_through'])
    rows=[state_on(config,start+timedelta(days=i)) for i in range((end-start).days+1)]
    assert len({r['date'] for r in rows})==len(rows)
    # Compact intervals preserve changes of president/party/definition without fabricating future terms.
    intervals=[];previous=None
    for r in rows:
        key=tuple(r[k] for k in ['president','wh_party','house_party','senate_party','control_definition_note'])
        if key!=previous:
            if intervals:intervals[-1]['end_exclusive']=r['date']
            intervals.append({k:v for k,v in r.items() if k in ['president','wh_party','house_party','senate_party','unified_government','split_congress','control_definition_note']})
            intervals[-1].update(start=r['date'],end_exclusive=(end+timedelta(days=1)).isoformat());previous=key
    with Snapshot(root,'political_control_reference') as snap:
        snap.add('daily_context.csv',csv_bytes(list(rows[0]),rows))
        snap.add('control_intervals.csv',csv_bytes(list(intervals[0]),intervals))
        snap.add('config.json',config_path.read_bytes())
        snap.add('recipe.py',Path(__file__).read_bytes())
        snap.write_json('sources.json',manifest)
        return snap.finish({'days':len(rows),'intervals':len(intervals),'first':rows[0]['date'],'last':rows[-1]['date'],
                            'aligned_to_polls':False,'future_control_assumed':False})

if __name__=='__main__':build()
