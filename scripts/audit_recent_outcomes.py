"""Offline official result reconstruction for census repairs and national labels.

Reads immutable FEC worksheet extractions / Alabama canvass. Never infer a ballot
identity or party from the closeness of a poll to the election result.
"""
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import json
import re
from data_utils import LAB

ROOT = LAB/'reports/source_audit/recent_outcomes'
PARTIES = ('DEM', 'REP', 'OTHER')


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def extract():
    """Read original workbooks; retain full sheet rows and 1-based row provenance."""
    import openpyxl
    metadata=[]
    for y in (2016, 2018, 2020, 2022):
        p=ROOT/f'fec{y}.xlsx' if y!=2022 else ROOT.parent/'national_2022_result/fec2022.xlsx'
        b=openpyxl.load_workbook(p,read_only=True,data_only=True)
        sheets={s:list(b[s].values) for s in b.sheetnames if any(t in s for t in ('Senate Results','House Results','House by Party','Party Labels'))}
        b.close();out=ROOT/f'fec{y}_values.json';out.write_text(json.dumps(sheets,indent=1,default=str)+'\n')
        metadata.append(dict(year=y,input=str(p.relative_to(LAB)),input_sha256=sha(p),output=out.name,output_sha256=sha(out),
                             method='openpyxl read_only=True data_only=True; complete sheets, original row order',sheets=list(sheets)))
    (ROOT/'extraction.json').write_text(json.dumps(metadata,indent=2)+'\n')


def verify():
    for r in json.loads((ROOT/'provenance.json').read_text()):
        if 'sha256' in r: assert sha(ROOT/r['file'])==r['sha256'],r['file']
    for r in json.loads((ROOT/'extraction.json').read_text()):
        assert sha(LAB/r['input'])==r['input_sha256']
        assert sha(ROOT/r['output'])==r['output_sha256']


def values(year, token):
    data=json.loads((ROOT/f'fec{year}_values.json').read_text())
    found=[(s,v) for s,v in data.items() if token in s]
    assert len(found)==1
    return found[0]


def party(label, year, state='', candidate=''):
    """General-election affiliation; transitions are not uniformly fusion labels."""
    p=label.strip().replace('*','')
    if p in {'D','DFL','DNL','D(UND)','D/R','D/PRO/WF/IP','D/IP/PRO/WF','D/WF','D/IP/WF','W(D)/D','N(D)/D'}:
        return 'DEM'
    if p=='D/IP':
        return 'OTHER' if (year,state,candidate.strip())==(2020,'CT','Merlen, Brian') else 'DEM'
    if p in {'R','GOP','R/TRP','R/IP','IP/R','R/CON','W(R)/R'}:return 'REP'
    return 'OTHER'


def combine(lines, control_exceptions=None):
    groups=defaultdict(list)
    for r in lines:
        name=re.sub(r'\s+',' ',r['candidate']).rstrip(' #').casefold()
        name=name.replace(' (opportunity to ballot)','')
        groups[(r['state'],r['district'],name)].append(r)
    candidates=[];checks=[]
    for key,rs in groups.items():
        majors={r['party'] for r in rs}-{'OTHER'}
        assert len(majors)<=1,(key,majors)
        assert len({r['source_party'] for r in rs})==len(rs),key
        votes=sum(r['votes'] or 0 for r in rs)
        controls={int(r['combined_control']) for r in rs if isinstance(r['combined_control'],(int,float))}
        if controls:
            allowed=(control_exceptions or {}).get(key)
            assert controls=={votes} or (len(controls)==1 and allowed==(votes,next(iter(controls)))),(key,controls,votes)
            checks.append(dict(state=key[0],district=key[1],candidate=key[2],votes=votes,control=next(iter(controls)),
                               status='matches' if controls=={votes} else 'source_control_conflict_retained_line_sum'))
        affiliation=next(iter(majors)) if majors else 'OTHER'
        for r in rs:r['candidate_party']=affiliation
        candidates.append(dict(state=key[0],district=key[1],candidate=rs[0]['candidate'].rstrip(' #'),
            party=affiliation,source_parties='|'.join(r['source_party'] for r in rs),votes=votes,
            missing_votes=any(r['votes'] is None for r in rs),source_rows='|'.join(str(r['source_row']) for r in rs)))
    return candidates,checks


def senate_stage(year,state,district,column,cycle,stage,election_date,special=False):
    sheet,rows=values(year,'Senate Results')
    selected=[(i,r) for i,r in enumerate(rows,1) if r[1]==state and str(r[3]).strip()==district]
    lines=[]
    for i,r in selected:
        if not (r[8] and r[10] and isinstance(r[column],(float,int))):continue
        votes=r[column];assert int(votes)==votes and votes>=0
        lines.append(dict(source_row=i,state=state,district=district,candidate=r[8].strip(),source_party=r[10].strip(),
            party=party(r[10],year,state,r[8]),votes=int(votes),combined_control=r[19] if column==15 else None))
    candidates,fusion=combine(lines)
    controls=[r[column] for i,r in selected if r[9] and str(r[9]).startswith('Total') and isinstance(r[column],(float,int))]
    total=sum(r['votes'] for r in candidates)
    assert controls==[total],(year,state,controls,total)
    # Mississippi's special ballot was nonpartisan. Keep N as ballot party and
    # retain identity-based comparisons as candidate pairs, not invented D/R totals.
    unique_pair=all(sum(r['party']==p for r in candidates)==1 for p in ('DEM','REP'))
    counts={p:sum(r['votes'] for r in candidates if r['party']==p) for p in PARTIES}
    ref=dict(outcome_id=f'{cycle}-{state}-{"special" if special else "regular"}-{stage}',cycle=cycle,
        geography=state,outcome_type='senate_contest_stage',stage=stage,special=str(special).lower(),election_date=election_date,
        total_votes=total,dem_share=counts['DEM']/total if unique_pair else '',rep_share=counts['REP']/total if unique_pair else '',
        dem_rep_margin=(counts['DEM']-counts['REP'])/total if unique_pair else '',
        status='audited_candidate_votes',review_reasons='' if unique_pair else 'not_unique_dem_rep_pair',
        reference_version='recent-outcomes-v1',source=f'fec{year}.xlsx',source_sheet=sheet,source_column=column+1,
        source_rows='|'.join(str(i) for i,r in selected if r[8] and isinstance(r[column],(int,float))))
    for r in candidates:r['outcome_id']=ref['outcome_id']
    return ref,candidates,lines,fusion


def alabama():
    text=(ROOT/'al2017.txt').read_text()
    parsed=[]
    for i,line in enumerate(text.splitlines(),1):
        m=re.match(r'^\s*(Total|[A-Za-z][A-Za-z ]*?)\s{2,}([\d,]+)\s+([\d,]+)\s+([\d,]+)(?:\s|$)',line)
        if m:
            parsed.append(dict(source_text_line=i,county=m[1].strip(),DEM=int(m[2].replace(',','')),REP=int(m[3].replace(',','')),OTHER=int(m[4].replace(',',''))))
    control=[r for r in parsed if r['county']=='Total'];counties=[r for r in parsed if r['county']!='Total']
    assert len(control)==1 and len(counties)==len({r['county'] for r in counties})==67
    counts={p:sum(r[p] for r in counties) for p in PARTIES}
    assert all(counts[p]==control[0][p] for p in PARTIES)
    total=sum(counts.values())
    ref=dict(outcome_id='2017-AL-special-gen',cycle=2017,geography='AL',outcome_type='senate_contest_stage',
        stage='gen',special='true',election_date='2017-12-12',total_votes=total,dem_share=counts['DEM']/total,
        rep_share=counts['REP']/total,dem_rep_margin=(counts['DEM']-counts['REP'])/total,status='audited_candidate_votes',
        review_reasons='odd_year_features_not_built',reference_version='recent-outcomes-v1',source='al2017.pdf',source_sheet='PDF pages 2–3; 67 county totals',source_column='',source_rows='')
    candidates=[dict(outcome_id=ref['outcome_id'],state='AL',district='special',candidate=n,party=p,source_parties=s,
                     votes=counts[p],missing_votes=False,source_rows='67 county sums') for n,p,s in [('Doug Jones','DEM','D'),('Roy Moore','REP','R'),('Unallocated write-in','OTHER','W')]]
    return ref,candidates,counties


def national(year):
    sheet,rows=values(year,'House Results');_,summary=values(year,'House by Party')
    lines=[]
    for i,r in enumerate(rows[1:],2):
        # NY05 2018 has an unnamed write-in line; do not drop it with a name filter.
        candidate=r[8] or ('Unallocated write-in' if r[10]=='W' and not r[9] else '')
        if not (candidate and r[10] and r[15] is not None):continue
        numeric=isinstance(r[15],(float,int))
        removed=(year,r[1],candidate.strip(),r[15])==(2020,'MT','Gibney, John','#')
        assert numeric or r[15]=='Unopposed' or removed,(year,i,r[15])
        if numeric:assert r[15]>=0 and int(r[15])==r[15]
        district=str(r[3]).strip()
        lines.append(dict(source_row=i,state=r[1],district=district,candidate=candidate.strip(),source_party=r[10].strip(),
            party=party(r[10],year,r[1],candidate),votes=int(r[15]) if numeric else None,
            runoff_votes=r[17] if isinstance(r[17],(float,int)) else 0,combined_control=r[19],
            disposition='removed_from_general_ballot' if removed else 'nonvoting_delegation' if r[1] in {'AS','DC','GU','MP','VI','PR'} else
                        'extra_unexpired_term' if 'UNEXPIRED' in district.upper() else 'included',
            exception='uncertified_NC09' if year==2018 and r[1]=='NC' and district.zfill(2)=='09' else
                      'missing_unopposed_votes' if not numeric else ''))
    candidates,fusion=combine(lines,{('NY','14','cummings, john c.'):(58410,58440)} if year==2020 else {})
    district_totals=Counter()
    for r in lines:district_totals[(r['state'],r['district'])]+=r['votes'] or 0
    district_checks=[]
    for i,r in enumerate(rows,1):
        if str(r[9]).startswith(('District Votes:','Total District Votes:')) and isinstance(r[15],(float,int)):
            key=(r[1],str(r[3]).strip())
            if key not in district_totals:
                possible=[k for k in district_totals if k[0]==r[1]]
                assert len(possible)==1,(year,i,key,possible)
                key=possible[0]
            actual=district_totals[key]
            assert actual==r[15] or (year,key,actual,r[15])==(2016,('KY','1 - UNEXPIRED TERM'),80813,290623),(year,key,actual,r[15])
            district_checks.append(dict(state=key[0],district=key[1],total=actual,source_total=r[15],
                difference=actual-r[15],source_row=i,status='matches' if actual==r[15] else 'excluded_special_subtotal_conflict'))
    # The FEC party recap sums general + runoff votes; our reference uses the
    # initial general ballot once. Preserve explicit recap classification differences.
    state_totals=defaultdict(Counter)
    for r in lines:state_totals[r['state']][r['party']]+=(r['votes'] or 0)+r['runoff_votes']
    recap=[]
    for r in summary:
        if r[0] not in state_totals:continue
        for p,v in zip(PARTIES,r[4:7]):
            expected=v if isinstance(v,(float,int)) else 0
            actual=state_totals[r[0]][p]
            recap.append(dict(state=r[0],party=p,source_total=expected,reconstructed=actual,difference=actual-expected))
    nonzero={(r['state'],r['party']):r['difference'] for r in recap if r['difference']}
    allowed={2016:{},2018:{('WA','REP'):148968,('WA','OTHER'):-148968},
             2020:{('MO','REP'):-1750,('MO','OTHER'):1750}}
    assert nonzero==allowed[year],(year,nonzero)
    assert len(recap)==3*len(state_totals)
    selected=[r for r in lines if r['disposition']=='included']
    assert len({r['state'] for r in selected})==50 and len({(r['state'],r['district']) for r in selected})==435
    counts={p:sum(r['votes'] or 0 for r in selected if r['candidate_party']==p) for p in PARTIES}
    total=sum(counts.values());missing=[r for r in selected if r['votes'] is None]
    exceptions=[r for r in selected if r['exception']]
    without_uncertified=[r for r in selected if r['exception']!='uncertified_NC09']
    count_alt={p:sum(r['votes'] or 0 for r in without_uncertified if r['candidate_party']==p) for p in PARTIES}
    ref=dict(outcome_id=f'{year}-US-house-popular-vote-source-only',cycle=year,geography='US',outcome_type='national_house_popular_vote',
        stage='general',special='false',election_date='',total_votes=total,dem_share=counts['DEM']/total,rep_share=counts['REP']/total,
        dem_rep_margin=(counts['DEM']-counts['REP'])/total,status='audited_reported_votes_with_exceptions',
        review_reasons='reported_candidate_votes_only'+('|missing_unopposed_counts' if missing else '')+
                       ('|uncertified_NC09_included|recap_GOP_classification_difference' if year==2018 else '')+
                       ('|recap_writein_classification_difference|NY14_combined_control_30_vote_conflict' if year==2020 else ''),
        reference_version='recent-outcomes-v1',source=f'fec{year}.xlsx',source_sheet=sheet,source_column=16,source_rows='',
        DEM=counts['DEM'],REP=counts['REP'],OTHER=counts['OTHER'],missing_contests=len({(r['state'],r['district']) for r in missing}),
        without_uncertified_margin=(count_alt['DEM']-count_alt['REP'])/sum(count_alt.values()))
    return dict(reference=ref,lines=lines,candidates=candidates,fusion=fusion,district_checks=district_checks,recap=recap,exceptions=exceptions)


def audit():
    verify();references=[];candidates=[];senate_lines=[];fusion=[]
    for args in [(2016,'LA','S',15,2016,'gen','2016-11-08',False),
                 (2016,'LA','S',17,2016,'runoff','2016-12-10',False),
                 (2018,'MS','S-UNEXPIRED TERM',15,2018,'gen','2018-11-06',True),
                 (2018,'MS','S-UNEXPIRED TERM',17,2018,'runoff','2018-11-27',True),
                 (2022,'CT','S',15,2022,'gen','2022-11-08',False)]:
        ref,cs,ls,fs=senate_stage(*args);references.append(ref);candidates.extend(cs)
        senate_lines.extend(dict(**r,outcome_id=ref['outcome_id']) for r in ls);fusion.extend(fs)
    ref,cs,counties=alabama();references.append(ref);candidates.extend(cs)
    nationals={y:national(y) for y in (2016,2018,2020)}
    references.extend(r['reference'] for r in nationals.values())
    return dict(references=references,senate_candidates=candidates,senate_lines=senate_lines,senate_fusion=fusion,
                alabama_counties=counties,national=nationals)


if __name__=='__main__':
    import sys
    if '--extract' in sys.argv:extract()
    r=audit();print(json.dumps(r['references'],indent=2))
