"""Assemble pinned reviewed history, current refresh and audited metadata.

Offline, immutable, with one source-version-qualified observation ID per row.
Acceptance concerns provenance/accounting and diagnostic use; seat forecasting is
separately gated by complete candidate vectors, election rules and caucus choices.
"""
import argparse
from collections import Counter, defaultdict
from datetime import date,timedelta
import json
from pathlib import Path

from data_utils import LAB,Snapshot,csv_bytes,digest
from prepare_data import read,number
from audit_refresh_2026 import verified
from audit_survey_identity import label,sponsor_key

CONFIG=LAB/'config/preparation_acceptance_v1.json'
IDENTITY_FIELDS=('canonical_firm','publisher_id','rating_id','rating_name','sponsor_ids','sponsor_names',
    'series_key','identity_basis','rating_family_key','rolling_method_evidence','canonical_sample_group_id','sample_identity_status')
PREDICTORS=('observation_id','source','dataset','cycle','geography','geography_type','source_poll_id','source_question_id',
    'sample_group_id','canonical_sample_group_id','poll_start','poll_end','poll_date','date_basis','source_available_date',
    'election_date','days_to_election','pollster','population','sample_size','methodology','partisan',
    'dem_share','rep_share','dem_rep_margin','non_dem_rep_share','reported_answer_sum','response_coverage')


def check(condition,message):
    if not condition:raise ValueError(message)


def qualified(origin,version,old_id):
    return f'{origin}/{version}/{old_id}'


def unique(rows,key):
    result={r[key]:r for r in rows}
    check(len(result)==len(rows),f'Duplicate {key}')
    return result


def load_inputs(config_path=CONFIG):
    config=json.loads(config_path.read_text());paths={}
    for kind,entry in config['snapshots'].items():
        path=LAB/entry['path'];verified(path)
        check(digest((path/'manifest.json').read_bytes())==entry['sha256'],f'Changed {kind} manifest')
        paths[kind]=path
    for path,sha in config['files'].items():
        check(digest((LAB/path).read_bytes())==sha,f'Changed pinned dependency: {path}')
    return config,paths


def default_identity(o,aliases):
    firm=aliases.get(label(o['pollster']),label(o['pollster'])) or 'unknown:'+o['observation_id']
    return dict(canonical_firm=firm,publisher_id='',rating_id='',rating_name='',sponsor_ids='',sponsor_names='',
        series_key=firm+'|unspecified',identity_basis='label_only_older_archive',rating_family_key='firm:'+firm,
        rolling_method_evidence='',canonical_sample_group_id=o['sample_group_id'],sample_identity_status='source_id_only')


def current_identity(o,raw,aliases,facts):
    x=default_identity(o,aliases)
    rs=[raw[o['dataset']][int(i)-2] for i in o['source_rows'].split('|')]
    check(all((r['poll_id'],r['question_id'])==(o['source_poll_id'],o['source_question_id']) for r in rs),'Current identity source mismatch')
    if o['dataset']=='senate':
        check(all(r['race_id']==o['source_race_id'] for r in rs),'Current race ID mismatch')
        fields={'publisher_id':'pollster_id','rating_id':'pollster_rating_id','rating_name':'pollster_rating_name',
                'sponsor_ids':'sponsor_ids','sponsor_names':'sponsors'}
        for dest,src in fields.items():
            values={r[src] for r in rs};check(len(values)==1,'Current identity metadata conflict');x[dest]=next(iter(values))
    else:x['sponsor_names']=rs[0]['sponsors']
    x.update(identity_basis='current_source_rows_verified',series_key=x['canonical_firm']+'|'+sponsor_key(x['sponsor_ids'],x['sponsor_names']),
        rating_family_key='rating:'+x['rating_id'] if x['rating_id'] else 'firm:'+x['canonical_firm'])
    for link in facts['sample_links']:
        if o['sample_group_id'] in link['members']:
            x.update(canonical_sample_group_id=link['canonical'],sample_identity_status=link['status'])
    for pending in facts['pending_duplicates']:
        if o['sample_group_id'] in pending['members']:x['sample_identity_status']=pending['status']
    return x


def default_metadata(o,fields):
    x={k:'' for k in fields}
    for k in ('observation_id','source','dataset','cycle','geography','source_poll_id','source_question_id','population','selection_status'):
        x[k]=o[k]
    x.update(reported_n=o['sample_size'],reported_n_basis='unknown',estimate_basis='unknown',basis_review_status='not_reviewed',
        source_quality_flags=o['quality_flags'],question_construct='unknown',availability_status='not_reviewed',
        archive_created_date=o['source_available_date'],metadata_version='acceptance-v1_unknown_current')
    return x


def disposition(o,target,error):
    if o['selection_status']=='superseded_by_full_archive':return 'excluded','superseded_by_full_archive'
    if o['cycle']=='2026':
        if o['dataset']=='senate':
            if o['matchup_status']!='accepted':return 'quarantined',o['quality_flags'] or 'unreviewed_matchup'
            if o['dem_rep_margin']=='':return 'candidate_vector_only','independent_or_no_unique_DR_pair'
            return 'current_screened',o['selection_status']
        flags=set(filter(None,o['quality_flags'].split('|')))-{'missing_or_invalid_sample_size'}
        if flags:return 'quarantined','|'.join(sorted(flags))
        return 'current_screened','national_question_requires_window_selection'
    if not o['election_date'] or o['days_to_election']=='':return 'restricted','missing_election_date'
    if o['dem_rep_margin']=='' or o['dem_share']=='' or o['rep_share']=='':return 'restricted','no_unique_DR_margin'
    if float(o['dem_share'])+float(o['rep_share'])>1+1e-9:return 'restricted','party_sum_above_one'
    if float(o['days_to_election'])<0:return 'restricted','after_election'
    tolerated={'missing_or_invalid_sample_size','historical_population_and_publication_date_unavailable'}
    if set(filter(None,o['quality_flags'].split('|')))-tolerated:return 'restricted','source_quality_review'
    if not target or not error.get('poll_error'):return 'restricted','missing_or_unresolved_reference'
    if o['dataset']=='senate':
        if o['matchup_status'] not in ('matched','matched_candidate_identity'):return 'restricted','unresolved_candidate_pair'
        if target['diagnostic_eligible']!='True':return 'restricted','result_or_election_rule_restriction'
    if target['status']=='source_reported_not_independently_reconciled':return 'provisional','older_source_only_result'
    return 'usable_retrospective','publication_vintage_not_fully_verified'


def seat_ledger(roster,contests,chamber):
    expected={(r['state'],r['seat_class']):r for r in contests}
    check(len(expected)==35,'Expected 35 distinct contested seats')
    check(len(roster)==100 and len({(r['state'],r['seat_class']) for r in roster})==100,'100 unique seats required')
    check(set(Counter(r['state'] for r in roster).values())=={2},'Two seats per state required')
    check(set(expected)<={(r['state'],r['seat_class']) for r in roster},'Contest missing from roster')
    result=[]
    for r in roster:
        c=expected.get((r['state'],r['seat_class']))
        if c:check(r['party']==c['current_party'],'Roster and contest party disagree')
        caucus=r['party']
        if r['party']=='IND':
            check(r['state'] in {'ME','VT'} and r['seat_class']=='1','Unreviewed continuing independent')
            caucus='DEM'
        result.append(dict(seat_id=r['state']+'-class'+r['seat_class'],**r,
            contest_id=c['contest_id'] if c else '',status='contested' if c else 'continuing',
            continuing_party='' if c else r['party'],continuing_caucus='' if c else caucus,
            affiliation_as_of='2026-09-16',caucus_condition='current affiliation held fixed; new independent winners unresolved'))
    continuing=Counter(r['continuing_party'] for r in result if r['status']=='continuing')
    check(dict(continuing)==chamber['continuing_seats_by_party'],'Continuing-party control differs')
    return result


def build(config_path=CONFIG):
    config,paths=load_inputs(config_path)
    reviewed,refresh=paths['reviewed'],paths['refresh']
    rmeta=json.loads((reviewed/'provenance.json').read_text())
    for k,sha in rmeta['manifest_sha256'].items():
        check(digest((paths[k]/'manifest.json').read_bytes())==sha,'Reviewed lineage mismatch')
    fmeta=json.loads((refresh/'provenance.json').read_text())
    check(digest((paths['current_raw']/'manifest.json').read_bytes())==fmeta['new_manifest_sha256'],'Refresh lineage mismatch')
    original=read(reviewed/'tables/observations.csv');fresh=read(refresh/'tables/observations.csv')
    outcomes=read(reviewed/'tables/outcomes.csv');targets=unique(outcomes,'outcome_id')
    labels=unique(read(reviewed/'tables/errors.csv'),'observation_id')
    basis=unique(read(LAB/config['basis_file']),'observation_id')
    identities=unique(read(LAB/config['identity_file']),'observation_id')
    check(set(basis)=={r['observation_id'] for r in original},'Incomplete baseline metadata')
    original_by_id=unique(original,'observation_id')
    for oid,b in basis.items():
        o=original_by_id[oid]
        check(all(b[k]==o[k] for k in ('source','cycle','source_poll_id','source_question_id','population')),'Stale basis annotation identity')
        check(number(b['reported_n'])==number(o['sample_size']),'Metadata changed reported N')
    facts=json.loads((LAB/'config/survey_identity_v1.json').read_text())
    aliases={label(n):a['canonical'] for a in facts['aliases'] for n in a['names']}
    raw={'senate':read(paths['current_raw']/'tables/senate_general_answers.csv'),
         'generic_ballot':read(paths['current_raw']/'raw/silver_bulletin_generic.csv')}
    observations=[];metadata=[];identity_rows=[];errors=[];lineage=[];dispositions=[]
    idmap={};sources=[]
    for origin,version,rows in [('reviewed',reviewed.name,[r for r in original if r['cycle']!='2026']),
                                ('refresh',refresh.name,fresh)]:
        for old in rows:
            oid=qualified(origin,version,old['observation_id']);idmap[(origin,old['observation_id'])]=oid
            x=dict(old);x.pop('poll_error_vs_result',None)
            x.update(observation_id=oid,origin_bundle=origin,origin_snapshot=version,origin_observation_id=old['observation_id'])
            if origin=='reviewed':
                b=dict(basis[old['observation_id']]);i=identities.get(old['observation_id'])
                identity={k:i[k] for k in IDENTITY_FIELDS} if i else default_identity(old,aliases)
                if i:check(all(i[k]==old[k] for k in ('cycle','source_poll_id','source_question_id','dem_share','rep_share','sample_size')),'Stale identity overlay')
                err=dict(labels[old['observation_id']])
            else:
                check(old['cycle']=='2026' and not old['outcome_id'] and not old['poll_error_vs_result'],'Current future label present')
                b=default_metadata(old,list(next(iter(basis.values()))))
                identity=current_identity(old,raw,aliases,facts)
                err=dict(observation_id=oid,cycle='2026',geography=old['geography'],outcome_id='',reference_version='',
                    reference_label='',reference_margin='',poll_error='',status='future_outcome_unavailable',
                    use='retrospective_only_not_predictor',selection_status=old['selection_status'])
            b['observation_id']=oid;identity['observation_id']=oid;err['observation_id']=oid
            x['canonical_sample_group_id']=identity['canonical_sample_group_id']
            status,reason=disposition(x,targets.get(x['outcome_id']),err)
            observations.append(x);metadata.append(b);identity_rows.append(identity);errors.append(err)
            dispositions.append(dict(observation_id=oid,cycle=x['cycle'],geography=x['geography'],dataset=x['dataset'],
                source=x['source'],outcome_id=x['outcome_id'],status=status,reason=reason))
            lineage.append(dict(observation_id=oid,origin=origin,snapshot=version,old_observation_id=old['observation_id'],
                source=x['source'],source_poll_id=x['source_poll_id'],source_question_id=x['source_question_id'],source_rows=x['source_rows']))
    for o in observations:
        if o.get('superseded_by'):
            o['origin_superseded_by']=o['superseded_by']
            o['superseded_by']='|'.join(idmap[(o['origin_bundle'],key)] for key in o['superseded_by'].split('|'))
    answers=[]
    for origin,path in [('reviewed',reviewed/'tables/answers.csv'),('refresh',refresh/'tables/normalized_answers.csv')]:
        for a in read(path):
            key=(origin,a['observation_id'])
            if key not in idmap:continue # obsolete current answers replaced as a whole, not appended
            answers.append({**a,'observation_id':idmap[key]})
    questions=read(refresh/'tables/questions.csv');candidate_review=json.loads((refresh/'config/candidate_review_2026.json').read_text())
    contests=read(paths['current_raw']/'config/contests_2026.csv')
    chamber=json.loads((paths['current_raw']/'config/chamber_2026.json').read_text())
    seats=seat_ledger(read(LAB/config['roster_file']),contests,chamber)
    rules=config['rule_reviews'];current_contests=[]
    for c in contests:
        spec=candidate_review['contests'][c['state']];qs=[q for q in questions if q['state']==c['state']]
        notes=['complete_ballot_not_certified']
        if not spec['candidates'] or any(not a['candidate_id'] for a in spec['candidates']):notes.append('candidate_source_mapping_incomplete')
        if spec['rule']=='rcv':notes.append('ranked_choice_transfers_required')
        if spec['rule']=='majority_runoff':notes.append('runoff_stage_model_required')
        if any(a['party']=='IND' for a in spec['candidates']):notes.append('independent_caucus_scenarios_required')
        if any('unreviewed_or_former_contender' in q['reasons'] for q in qs):notes.append('quarantined_alternative_candidates')
        current_contests.append(dict(**c,election_rule=spec['rule'],rule_source=rules.get(c['state'],{}).get('source',''),
            rule_review_status='official_exception_rule_checked' if c['state'] in rules else 'existing_plurality_configuration_not_individually_reaudited',
            conditional_runoff_date='2026-12-01' if c['state']=='GA' else '',
            candidate_screen_date=candidate_review['review_date'],leading_candidate_count=len(spec['candidates']),
            source_questions=len(qs),accepted_questions=sum(q['accepted_matchup']=='True' for q in qs),
            selected_questions=sum(q['selection']=='selected' for q in qs),
            polling_status='source_present' if qs else 'no_source_polls',
            seat_forecast_ready=False,seat_mapping_restrictions='|'.join(notes)))
    features=read(reviewed/'tables/state_features.csv')
    for f in features:
        check(int(f['prior_presidential_year'])<int(f['cycle']),'Feature leaks target election')
        f['legacy_split']=f.pop('split');f['evaluation_status']='forecast' if f['cycle']=='2026' else 'previously_explored_retrospective'
    groups=defaultdict(list)
    for d in dispositions:groups[(d['cycle'],d['dataset'],d['geography'],d['outcome_id'])].append(d)
    coverage=[]
    for key,rs in sorted(groups.items()):
        counts=Counter(r['status'] for r in rs)
        coverage.append(dict(cycle=key[0],dataset=key[1],geography=key[2],outcome_id=key[3],stored_versions=len(rs),
            **{k:counts[k] for k in ['usable_retrospective','provisional','excluded','restricted','quarantined','current_screened','candidate_vector_only']}))
    # Left join outcomes: all result-only races remain targets, never fabricated polls.
    outcome_coverage=[]
    for t in outcomes:
        rs=[d for d in dispositions if d['outcome_id']==t['outcome_id']]
        outcome_coverage.append(dict(outcome_id=t['outcome_id'],cycle=t['cycle'],geography=t['geography'],
            outcome_type=t['outcome_type'],diagnostic_eligible=t['diagnostic_eligible'],result_status=t['status'],
            stored_versions=len(rs),usable_versions=sum(r['status'] in ('usable_retrospective','provisional') for r in rs),
            coverage_status='no_joined_poll' if not rs else 'polls_present'))
    # Explicit unknowns on odd-year specials and states with no race.
    fmap={(r['cycle'],r['state']):r for r in features};states=sorted({r['state'] for r in seats})
    calendar=[]
    cycles=sorted({int(r['cycle']) for r in observations}|{int(r['cycle']) for r in outcomes})
    for cycle in cycles:
        for state in states:
            ts=[r for r in outcomes if r['cycle']==str(cycle) and r['geography']==state and r['outcome_type']=='senate_contest_stage']
            cs=[r for r in current_contests if cycle==2026 and r['state']==state]
            calendar.append(dict(cycle=cycle,state=state,result_stages=len(ts),scheduled_current_contests=len(cs),
                has_election=bool(ts or cs),feature_status='lagged_features_present' if (str(cycle),state) in fmap else 'not_prepared_for_cycle'))
    corrections=read(reviewed/'tables/corrections.csv')
    for r in corrections:
        r['origin_observation_id']=r['observation_id'];r['observation_id']=idmap[('reviewed',r['observation_id'])]
    result = dict(observations=observations,answers=answers,outcomes=outcomes,errors=errors,metadata=metadata,identity=identity_rows,
        lineage=lineage,dispositions=dispositions,coverage=coverage,outcome_coverage=outcome_coverage,current_contests=current_contests,
        seat_ledger=seats,state_features=features,state_calendar=calendar,
        predictors=[{k:o.get(k,'') for k in PREDICTORS} for o in observations],
        result_restrictions=read(reviewed/'tables/restrictions.csv'),corrections=corrections,historical_candidates=read(reviewed/'tables/candidates.csv'),
        current_candidate_screen=[dict(state=state,**a,review_date=candidate_review['review_date'],status=spec['status']) for state,spec in candidate_review['contests'].items() for a in spec['candidates']],
        question_dispositions=questions,config=config,paths=paths)
    from official_result_reviews import apply_reviews
    return apply_reviews(result)


def publish(result,output=None,config_path=CONFIG):
    output=output or LAB/'data/accepted'
    from verify_accepted_data import verify_tables
    checks=verify_tables(result)
    refresh_summary=json.loads((result['paths']['refresh']/'summary.json').read_text())
    summary=dict(version='preparation-acceptance-v1',as_of=refresh_summary['as_of'],status='accepted_for_diagnostics_with_restrictions',
        seat_forecast_ready=False,counts={k:len(v) for k,v in result.items() if isinstance(v,list)},
        observation_dispositions=dict(Counter(r['status'] for r in result['dispositions'])),
        basis_reviewed=sum(r['basis_review_status']!='not_reviewed' for r in result['metadata']),
        publication_reviewed=sum(r['availability_status']!='not_reviewed' for r in result['metadata']),
        current_selected_questions=sum(r['selection']=='selected' for r in result['question_dispositions']),
        no_source_poll_states=[r['state'] for r in result['current_contests'] if r['polling_status']=='no_source_polls'],checks=checks)
    with Snapshot(output,'accepted_election_data') as bundle:
        for key,rs in result.items():
            if isinstance(rs,list) and rs:
                fields=list(dict.fromkeys(k for r in rs for k in r));bundle.add('tables/'+key+'.csv',csv_bytes(fields,rs),rows=len(rs))
        for path in result['config']['files']:
            bundle.add('inputs/'+path,(LAB/path).read_bytes())
        bundle.write_json('config.json',result['config'])
        bundle.write_json('summary.json',summary)
        bundle.write_json('provenance.json',dict(version=summary['version'],snapshots=result['config']['snapshots'],
            source_config_sha256=digest(Path(config_path).read_bytes()),
            scripts={n:digest((LAB/'scripts'/n).read_bytes()) for n in ['build_accepted_data.py','official_result_reviews.py','verify_accepted_data.py','data_utils.py','prepare_data.py','audit_refresh_2026.py','audit_survey_identity.py']},
            semantics='Historical labels and errors are separate from predictor allowlist. All stored versions retained except obsolete current snapshot replaced wholesale. '
            'No effective N, publication vintage, complete ballot or independent caucus is inferred. New candidate mapping remains gated.'))
        return bundle.finish(summary)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path)
    p.add_argument('--config',type=Path,default=CONFIG)
    a=p.parse_args();publish(build(a.config),a.output_dir,a.config)

if __name__=='__main__':main()
