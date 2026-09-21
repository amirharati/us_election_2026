"""Offline first-choice 2024 House reference; preserve original mixed-round snapshot.

Use --extract once with openpyxl after retrieving the Maine workbook. Routine
notebook reruns use the hash-bound JSON extraction and the standard library.
"""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from data_utils import LAB, latest
from prepare_data import read

AUDIT = LAB / 'reports/source_audit/national_2024_rounds'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract():
    import openpyxl
    path = AUDIT / 'maine_first_choices.xlsx'
    book = openpyxl.load_workbook(path, read_only=True, data_only=True)
    assert book.sheetnames == ['Sheet1']
    rows = list(book['Sheet1'].values)
    book.close()
    target = AUDIT / 'maine_workbook_values.json'
    target.write_text(json.dumps(rows, indent=1) + '\n')
    (AUDIT / 'extraction.json').write_text(json.dumps(dict(input=path.name,
        input_sha256=sha(path), output=target.name, output_sha256=sha(target),
        sheet='Sheet1', method='openpyxl read_only=True, data_only=True; full rows including blanks',
        openpyxl_version=openpyxl.__version__), indent=2)+'\n')


def reconcile_maine(rows):
    assert rows[0] == ['DIST','CTY','MUNICIPALITY','Golden, Jared Forrest','Theriault, Austin','Others','BLANK','TBC']
    assert rows[2][3:5] == ['Democratic','Republican']
    ledger, counties, checks = [], defaultdict(Counter), []
    fields = ('DEM','REP','OTHER','blank','ballots')
    for number,row in enumerate(rows[3:],4):
        if row[2] in (None,''): continue
        county = (row[1] or '').strip() or 'UOCAVA'
        values = row[3:8]
        assert all(isinstance(v,(int,float)) and v >= 0 and int(v)==v for v in values), (number,values)
        counts = dict(zip(fields,map(int,values)))
        assert sum(values[:4]) == values[4], (number,'ballot accounting')
        if row[2] == 'Statewide Totals':
            checks.append(dict(scope='state',source_row=number,**counts));continue
        if row[2] == 'Totals':
            checks.append(dict(scope=county,source_row=number,**counts));continue
        assert row[0] == 2
        ledger.append(dict(source_row=number,county=county,municipality=row[2],**counts))
        counties[county].update(counts)
    assert len({(r['county'],r['municipality']) for r in ledger}) == len(ledger)
    total = Counter()
    for c in counties.values(): total.update(c)
    for check in checks:
        observed = total if check['scope']=='state' else counties[check['scope']]
        assert all(observed[f]==check[f] for f in fields),check
    assert len([c for c in checks if c['scope']=='state'])==1
    assert {c['scope'] for c in checks if c['scope']!='state'} == set(counties)-{'UOCAVA'}
    return ledger, checks, dict(total)


def replace_district(candidates, counts):
    old = [r for r in candidates if r['state']=='ME' and int(r['district'])==2]
    assert {(r['party'],int(r['votes'])) for r in old} == {('DEM',197151),('REP',194445)}
    retained = [dict(r) for r in candidates if not (r['state']=='ME' and int(r['district'])==2)]
    for party,name in [('DEM','Golden, Jared Forrest'),('REP','Theriault, Austin'),('OTHER','Unallocated: Others')]:
        retained.append(dict(state='ME',district='2',candidate=name,party=party,votes=counts[party],
                             source_rows='Maine Sheet1 municipal rows; statewide control D425:F425'))
    assert len({(r['state'],r['district']) for r in retained}) == 435
    assert sorted(f"{r['state']}-{r['district']}" for r in retained if r['votes'] in ('',None)) == ['FL-20','OK-3']
    return old, retained


def totals(candidates):
    result = Counter()
    for c in candidates: result[c['party']] += int(c['votes']) if c['votes'] not in ('',None) else 0
    denominator = sum(result.values())
    return dict(**result,total_votes=denominator,dem_share=result['DEM']/denominator,
                rep_share=result['REP']/denominator,dem_rep_margin=(result['DEM']-result['REP'])/denominator,
                margin_pp=100*(result['DEM']-result['REP'])/denominator)


def audit(historical=None):
    historical = Path(historical) if historical else latest(LAB/'data/historical')[0]
    for p in json.loads((AUDIT/'provenance.json').read_text()):
        assert sha(AUDIT/p['file']) == p['sha256']
    meta=json.loads((AUDIT/'extraction.json').read_text())
    assert sha(AUDIT/meta['input']) == meta['input_sha256']
    assert sha(AUDIT/meta['output']) == meta['output_sha256']
    ledger,checks,counts=reconcile_maine(json.loads((AUDIT/meta['output']).read_text()))
    assert counts==dict(DEM=196388,REP=194130,OTHER=421,blank=11997,ballots=402936)
    # Visually transcribed from the one-page certified RCV PDF, with source hash.
    certified=json.loads((AUDIT/'certified_facts.json').read_text())
    assert sha(AUDIT/certified['file'])==certified['sha256']
    assert certified['DEM']+certified['REP']==certified['continuing']
    assert certified['continuing']+certified['exhausted']==counts['ballots']
    candidates=read(historical/'tables/house_2024_candidates.csv')
    reference=json.loads((historical/'house_2024_reference.json').read_text())
    before=totals(candidates)
    assert before['total_votes']==reference['total_candidate_votes']
    assert abs(before['dem_rep_margin']-reference['dem_rep_margin'])<1e-12
    old,replaced=replace_district(candidates,counts)
    after=totals(replaced)
    assert after['total_votes']-before['total_votes']==sum(counts[p] for p in ('DEM','REP','OTHER'))-certified['continuing']
    return dict(historical_snapshot=historical.name,municipal_ledger=ledger,controls=checks,
                first_choice_counts=counts,certified_rcv=certified,replaced_rows=old,candidates=replaced,
                original=before,benchmark=after,change_margin_pp=after['margin_pp']-before['margin_pp'])


if __name__=='__main__':
    import sys
    if '--extract' in sys.argv: extract()
    result=audit()
    print(json.dumps({k:result[k] for k in ('historical_snapshot','first_choice_counts','original','benchmark','change_margin_pp')},indent=2))
