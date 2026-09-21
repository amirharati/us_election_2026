"""Versioned result/join repair layer; original normalized snapshots stay intact.

Run after normalization. Consumers must use this bundle's outcomes and poll joins
 together. Historical error labels are written separately from observations.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
import csv
import json
from data_utils import LAB, Snapshot, latest, digest, csv_bytes
from prepare_data import read, surname
from analysis_policy import apply_references
from audit_recent_outcomes import audit, ROOT
from audit_contest_coverage import expected_contests, FACTS

VERSION='recent-outcomes-v1'
RACE_MAP={(2022,'8921'):'2022-CA-regular-gen',(2022,'9480'):'2022-CA-special-gen',
          (2024,'9506'):'2024-CA-regular-gen',(2024,'10013'):'2024-CA-special-gen'}


def correct_ca2022(row):
    """Original Research Co. tables page 2: 63/37 decided; archive contains 53/37."""
    if (row['cycle'],row['geography'],row['source_poll_id'])!=('2022','CA','81582'):return False
    expected={'165129':('9480',423),'165130':('8921',428)}
    assert row['source_question_id'] in expected
    race,n=expected[row['source_question_id']]
    assert row['source_race_id']==race and float(row['dem_share'])==.53 and float(row['rep_share'])==.37
    assert float(row['sample_size'])==450
    row.update(dem_share='0.63',dem_rep_margin='0.26',non_dem_rep_share='0.0',
               estimate_basis='decided',survey_sample_size='450',estimate_sample_size=str(n),
               estimate_source='reports/source_audit/estimate_basis/oh_tables.pdf#page=2')
    if row['reported_answer_sum']!='':row['reported_answer_sum']='1.0'
    return True


def pair_match(answers,candidates):
    """Return a unique candidate reference pair; party on a ballot stays separate."""
    pair=[]
    for party in ('DEM','REP'):
        aa=[a for a in answers if a['party']==party and str(a.get('exact_duplicate','')).lower()!='true']
        if len(aa)!=1:return None
        matched=[c for c in candidates if surname(c['candidate'])==surname(aa[0]['candidate_name'])]
        if len(matched)!=1:return None
        pair.append(matched[0])
    if pair[0]['candidate']==pair[1]['candidate']:return None
    return pair


def validate_ca_evidence(paths,observations):
    evidence=ROOT.parent/'estimate_basis'
    entry=next(r for r in json.loads((evidence/'provenance.json').read_text()) if r['file']=='oh_tables.pdf')
    assert digest((evidence/entry['file']).read_bytes())==entry['sha256']
    legacy=read(paths['historical']/'tables/senate_polls.csv')
    for race,token in [('8921','2022_Sen-G_CA'),('9480','2022_Sen-GS_CA')]:
        rs=[r for r in legacy if r['cycle']=='2022' and r['location']=='CA' and r['race_id']==race]
        assert rs and {r['race'] for r in rs}=={token}
    # Original Research Co. page 1: special full sample 61/35, regular 60/37.
    # These establish vendor race IDs, without consulting either election result.
    for race,qid,d,r in [('10013','216192',.61,.35),('9506','216193',.60,.37)]:
        aa=[a for a in observations if a['source']=='538_archive' and a['source_poll_id']=='89320' and a['source_question_id']==qid]
        assert len(aa)==1
        a=aa[0];assert (a['cycle'],a['geography'],a['source_race_id'])==('2024','CA',race)
        assert abs(float(a['dem_share'])-d)<1e-10 and abs(float(a['rep_share'])-r)<1e-10


def build(paths=None):
    paths=paths or {k:latest(LAB/'data'/k)[0] for k in ('historical','prepared','normalized','2026')}
    original=read(paths['normalized']/'tables/election_outcomes.csv')
    source_obs=read(paths['normalized']/'tables/poll_observations.csv')
    source_candidates=read(paths['prepared']/'tables/historical_candidates.csv')
    answers=read(paths['normalized']/'tables/poll_answers.csv')
    normalized_provenance=json.loads((paths['normalized']/'provenance.json').read_text())
    assert all(paths[k].name==v for k,v in normalized_provenance['snapshots'].items()),'Mixed input snapshots'
    result=audit();base,prior_versions=apply_references(original,paths['historical'])
    refs={r['outcome_id']:r for r in result['references']}
    by_id={r['outcome_id']:r for r in base}
    replacements=[]
    for oid,r in refs.items():
        old=by_id.get(oid)
        replacements.append(dict(outcome_id=oid,action='replace' if old else 'add',
            original_status=old['status'] if old else '',old_margin=old['dem_rep_margin'] if old else '',
            reviewed_margin=r['dem_rep_margin'],total_votes=r['total_votes'],source=r['source'],
            reasons=r['review_reasons']))
        by_id[oid]=deepcopy(r)
    outcomes=[]
    for oid,r in by_id.items():
        x=dict(r)
        x['reference_version']=r.get('reference_version','analysis-policy-v1' if oid in {v['outcome_id'] for v in prior_versions} else 'normalized:'+paths['normalized'].name)
        x['diagnostic_eligible']=r['status']=='reconciled_baseline' or oid=='2022-CT-regular-gen' or r['outcome_type']=='national_house_popular_vote'
        outcomes.append(x)
    by_id={r['outcome_id']:r for r in outcomes}
    candidates=[]
    replaced_senate={r['outcome_id'] for r in result['references'] if r['outcome_type']=='senate_contest_stage'}
    for r in source_candidates:
        if r['contest_id'] in replaced_senate:continue
        candidates.append(dict(outcome_id=r['contest_id'],candidate=r['candidate'],votes=float(r['votes']),
            party={'DEMOCRAT':'DEM','REPUBLICAN':'REP'}.get(r['party'],'OTHER'),source_parties=r['party'],
            reference_version='prepared:'+paths['prepared'].name,source_rows=r['source_rows']))
    candidates.extend(dict(**r,reference_version=VERSION) for r in result['senate_candidates'])
    cc=defaultdict(list);aa=defaultdict(list)
    for r in candidates:cc[r['outcome_id']].append(r)
    for r in answers:aa[r['observation_id']].append(r)
    validate_ca_evidence(paths,source_obs)
    observations=[];joins=[];errors=[];corrections=[];reviewed_answers=deepcopy(answers)
    for source in source_obs:
        r=deepcopy(source);oid=r['outcome_id'];y=int(r['cycle']);state=r['geography']
        r.update(original_dem_share=source['dem_share'],original_rep_share=source['rep_share'],
                 estimate_basis='',survey_sample_size='',estimate_sample_size='',estimate_source='')
        if correct_ca2022(r):
            corrections.append(dict(observation_id=r['observation_id'],source_poll_id=r['source_poll_id'],
                source_question_id=r['source_question_id'],original_dem_share=source['dem_share'],reviewed_dem_share=r['dem_share'],
                rep_share=r['rep_share'],reported_n=r['sample_size'],estimate_n=r['estimate_sample_size'],
                basis='decided',source=r['estimate_source'],reason='archive_transcription_differs_from_original_table'))
            for a in reviewed_answers:
                if a['observation_id']==r['observation_id'] and a['party']=='DEM':
                    assert float(a['support_share'])==.53
                    a['support_share']='0.63'
        target=None;basis='';attempt=False
        if r['dataset']=='senate':
            if state=='CA' and y in (2022,2024):
                target=RACE_MAP.get((y,r['source_race_id']));basis='source_race_id_with_ballot_evidence';attempt=True
            elif (y,state) in {(2017,'AL'),(2022,'CT'),(2016,'LA')}:
                matches=[x for x in refs.values() if x['cycle']==y and x['geography']==state and x['election_date']==r['election_date']]
                target=matches[0]['outcome_id'] if len(matches)==1 else None;basis='official_date_and_candidate_identity';attempt=True
            elif (y,state)==(2018,'MS') and (r['source_seat_name']=='Class II' or r['source_race_id']=='6209' or oid=='2018-MS-special-gen'):
                matches=[x for x in refs.values() if x['cycle']==y and x['geography']==state and x['election_date']==r['election_date']]
                target=matches[0]['outcome_id'] if len(matches)==1 else None;basis='official_special_election_stage';attempt=True
            elif (y,state,r['source_stage'],r['election_date'])==(2022,'GA','runoff','2022-12-06'):
                target='2022-GA-regular-gen_runoff';basis='runoff_stage_alias';attempt=True
            elif (y,state)==(2020,'LA') and not r['election_date'] and r['source_stage']=='runoff':
                basis='unheld_runoff_no_observed_election_date';attempt=True
        if attempt:
            pair=pair_match(aa[r['observation_id']],cc[target]) if target else None
            if pair:
                r['outcome_id']=target;r['matchup_status']='matched_candidate_identity'
                join_status='matched_pair'
            elif target:
                r['outcome_id']=target;r['matchup_status']='contest_stage_only_candidate_review'
                join_status='stage_assigned_pair_unresolved'
            else:
                r['outcome_id']='';r['matchup_status']='unresolved_ballot_or_date'
                join_status='restricted_unheld_runoff' if basis.startswith('unheld') else 'unresolved'
            r['scalar_seat_mapping_ready']=str(bool(pair and by_id[target]['diagnostic_eligible'] and not r['quality_flags']))
            joins.append(dict(observation_id=r['observation_id'],cycle=y,state=state,source_race_id=r['source_race_id'],
                original_outcome_id=source['outcome_id'],reviewed_outcome_id=r['outcome_id'],
                original_matchup_status=source['matchup_status'],reviewed_matchup_status=r['matchup_status'],
                status=join_status,evidence=basis,source_poll_id=r['source_poll_id'],sample_group_id=r['sample_group_id'],
                selection_status=r['selection_status']))
        r['original_outcome_id']=source['outcome_id'];r['original_matchup_status']=source['matchup_status']
        r['join_reference_version']=VERSION if attempt else 'normalized:'+paths['normalized'].name
        observations.append(r)
        target=by_id.get(r['outcome_id']);reference='';label='';status=''
        if y==2026:status='future_outcome_unavailable'
        elif not target:status='missing_outcome'
        elif r['dataset']=='generic_ballot':
            reference=target['dem_rep_margin'];label='national_house_D_minus_R';status='reference_available'
        elif r['matchup_status'] not in ('matched','matched_candidate_identity'):status='unresolved_candidate_pair'
        else:
            pair=pair_match(aa[r['observation_id']],cc[r['outcome_id']])
            if pair:
                # Use the entire candidate-vote denominator, never a two-party rescale.
                total=float(target.get('total_votes') or sum(c['votes'] for c in cc[r['outcome_id']]))
                reference=(float(pair[0]['votes'])-float(pair[1]['votes']))/total
                label=pair[0]['candidate']+' minus '+pair[1]['candidate'];status='reference_available'
            else:status='unresolved_candidate_pair'
        error=float(r['dem_rep_margin'])-float(reference) if reference!='' and r['dem_rep_margin']!='' else ''
        errors.append(dict(observation_id=r['observation_id'],cycle=y,geography=state,outcome_id=r['outcome_id'],
            reference_version=target['reference_version'] if target else '',reference_label=label,
            reference_margin=reference,poll_error=error,status=status,
            use='retrospective_only_not_predictor',selection_status=r['selection_status']))
    assert len(observations)==len(source_obs) and all(r['poll_error']=='' for r in errors if r['cycle']==2026)
    # Only the four explicitly source-corrected versions can change vote shares.
    allowed={'outcome_id','matchup_status','scalar_seat_mapping_ready'}
    corrected={r['observation_id'] for r in corrections}
    assert len(corrected)==4
    for a,b in zip(source_obs,observations):
        exceptions=allowed | ({'dem_share','dem_rep_margin','non_dem_rep_share','reported_answer_sum'} if a['observation_id'] in corrected else set())
        assert all(a[k]==b[k] for k in a if k not in exceptions)
    assert len(outcomes)==len(original)+4
    # Inventory every remaining recent restricted result and its numerical exposure.
    restrictions=[]
    for r in outcomes:
        y=int(r['cycle'])
        if r['outcome_type']!='senate_contest_stage' or not 2016<=y<=2024 or r['diagnostic_eligible']:continue
        ps=[x for x in observations if x['outcome_id']==r['outcome_id'] and x['selection_status']!='superseded_by_full_archive']
        initial_multiple=(r['outcome_id'] in {'2016-LA-regular-gen','2018-MS-special-gen','2020-GA-special-gen','2020-LA-regular-gen','2022-LA-regular-gen'})
        action=('candidate_vector_and_rule_required' if initial_multiple else
                'candidate_affiliation_and_caucus_review' if any(c['party']=='OTHER' and c['votes']>sum(d['votes'] for d in cc[r['outcome_id']])*.2 for c in cc[r['outcome_id']]) else
                'retain_explicit_result_or_rule_restriction')
        restrictions.append(dict(outcome_id=r['outcome_id'],cycle=y,state=r['geography'],stage=r['stage'],special=r['special'],
            result_status=r['status'],reasons=r['review_reasons'],handling=action,active_joined_questions=len(ps),
            within_days_1_to_15=sum(x['days_to_election']!='' and 1<=float(x['days_to_election'])<=15 for x in ps)))
    # Reconcile expected stages after repairs without relying on old stage-name ambiguity.
    expected=expected_contests(json.loads(FACTS.read_text()));coverage=[]
    for c in expected:
        for stage,dt in [('gen',c['initial_date']),('runoff',c['runoff_date'])]:
            if not dt:continue
            matches=[r for r in outcomes if r['outcome_type']=='senate_contest_stage' and int(r['cycle'])==c['cycle']
                and r['geography']==c['state'] and r['special']==str(c['special']).lower()
                and (r['stage']==stage or stage=='runoff' and r['stage']=='gen runoff')]
            status='not_due' if c['cycle']==2026 else 'present' if len(matches)==1 else 'missing' if not matches else 'ambiguous'
            coverage.append(dict(contest_id=c['contest_id'],cycle=c['cycle'],state=c['state'],stage=stage,election_date=dt,
                                 outcome_id='|'.join(r['outcome_id'] for r in matches),status=status))
    assert all(r['status'] in ('present','not_due') for r in coverage),[r for r in coverage if r['status'] not in ('present','not_due')]
    return dict(outcomes=outcomes,observations=observations,answers=reviewed_answers,candidates=candidates,errors=errors,joins=joins,corrections=corrections,
        replacements=replacements,restrictions=restrictions,coverage=coverage,audit=result,paths=paths,
        state_features=read(paths['normalized']/'tables/state_features.csv'),current_contests=read(paths['normalized']/'tables/current_contests.csv'))


def write_csv(bundle,name,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    if fields:bundle.add('tables/'+name+'.csv',csv_bytes(fields,rows),rows=len(rows))


def publish(result):
    paths=result['paths'];a=result['audit']
    with Snapshot(LAB/'data/reviewed','reviewed_polling_results') as bundle:
        for key in ('outcomes','observations','answers','candidates','errors','joins','corrections','replacements','restrictions','coverage','state_features','current_contests'):
            write_csv(bundle,key,result[key])
        for key in ('senate_lines','senate_fusion','alabama_counties'):write_csv(bundle,key,a[key])
        for year,n in a['national'].items():
            for key in ('lines','fusion','district_checks','recap','exceptions'):write_csv(bundle,f'national_{year}_{key}',n[key])
        provenance=dict(version=VERSION,snapshots={k:p.name for k,p in paths.items()},
            manifest_sha256={k:digest((p/'manifest.json').read_bytes()) for k,p in paths.items()},
            as_of=json.loads((paths['normalized']/'provenance.json').read_text())['as_of'],
            source_audit_sha256={str(p.relative_to(LAB)):digest(p.read_bytes()) for p in
                [ROOT/'provenance.json',ROOT/'extraction.json',ROOT/'researchco_ca2024.pdf',FACTS,
                 Path(__file__),LAB/'scripts/audit_recent_outcomes.py',
                 ROOT.parent/'estimate_basis/oh_tables.pdf',ROOT.parent/'estimate_basis/provenance.json']},
            restrictions='Diagnostic eligibility preserves prior rule exclusions; CT2022 label added. All current2026 errors blank. No caucus assignment inferred from ballot-party label.')
        bundle.write_json('provenance.json',provenance)
        summary=dict(version=VERSION,observations=len(result['observations']),outcomes=len(result['outcomes']),
            reference_additions=sum(r['action']=='add' for r in result['replacements']),reference_replacements=sum(r['action']=='replace' for r in result['replacements']),
            join_statuses=dict(Counter(r['status'] for r in result['joins'])),expected_stage_statuses=dict(Counter(r['status'] for r in result['coverage'])),
            restricted_recent_result_stages=len(result['restrictions']))
        summary['source_corrected_poll_versions']=len(result['corrections'])
        bundle.write_json('summary.json',summary)
        return bundle.finish(summary)


if __name__=='__main__':publish(build())
