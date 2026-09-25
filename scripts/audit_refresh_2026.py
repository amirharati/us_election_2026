"""Offline acceptance of two immutable current-feed snapshots; never fits a model.

A refresh is accepted for storage/diagnostics with explicit quarantine. It does not
certify the dated candidate configuration or provide complete ballot/seat mapping.
"""
import argparse
from collections import Counter, defaultdict
from datetime import date
import json
from pathlib import Path

from data_utils import LAB, Snapshot, csv_bytes, digest, poll_changes, table
from prepare_data import current_questions, select_current
from normalize_data import current_senate, current_generic

AGGREGATOR_FIELDS = {'timestamp','modeldate','weight','influence','adjusted_dem',
                     'adjusted_rep','adjusted_net','date'}
SENATE = 'tables/senate_general_answers.csv'
GENERIC = 'raw/silver_bulletin_generic.csv'


def verified(path):
    manifest = json.loads((path/'manifest.json').read_text())
    for name, info in manifest['files'].items():
        if digest((path/name).read_bytes()) != info['sha256']:
            raise ValueError(f'Checksum mismatch: {path/name}')
    return manifest


def compare(old, new, ignored=()):
    # Preserve question multiplicity, irrespective of row order; never key by row index.
    a = [{k:v for k,v in r.items() if k not in ignored} for r in old]
    b = [{k:v for k,v in r.items() if k not in ignored} for r in new]
    result = poll_changes(a,b)
    result['revised_fields'] = []
    for pid in result['revised_poll_ids']:
        left = [r for r in a if r['poll_id']==pid]
        right = [r for r in b if r['poll_id']==pid]
        fields = sorted({k for r in left+right for k in r})
        changed = [k for k in fields if Counter(r.get(k) for r in left)!=Counter(r.get(k) for r in right)]
        result['revised_fields'].append(dict(poll_id=pid, fields='|'.join(changed),
            old_rows=len(left), new_rows=len(right),
            note='joint row associations changed' if not changed else ''))
    return result


def csv_form(rows):
    # Existing normalizer deliberately consumes the serialized preparation schema.
    return [{k:'' if v is None else str(v) for k,v in r.items()} for r in rows]


def scenario(rows, review, asof, window):
    questions, answers = current_questions(rows, review, asof)
    select_current(questions,asof,window)
    return questions, answers


def validate_race_ids(old, new, review):
    """Accept explicitly reviewed source identities, not unreviewed matchups."""
    known={(r['state'],r['race_id']) for r in old}
    added={(r['state'],r['race_id']) for r in new}-known
    allowed={(state,race) for state,spec in review['contests'].items() for race in spec.get('source_race_ids',[])}
    unknown=added-allowed
    if unknown:
        detail='; '.join(f'{state}: {race}' for state,race in sorted(unknown))
        raise ValueError('New source race IDs require review: '+detail+'; inspect config/candidate_review_2026.json. Previous forecast is preserved.')
    for r in new:
        if (r['state'],r['race_id']) in added:
            if (str(r.get('cycle')),r.get('office_type'),r.get('stage'),r.get('election_date'))!=('2026','U.S. Senate','general','2026-11-03'):
                raise ValueError('Reviewed source race has incompatible election metadata: '+r['state']+': '+r['race_id'])


def run(old_path, new_path, old_asof, asof, output, window=14):
    if asof < old_asof:
        raise ValueError('New cutoff precedes baseline cutoff')
    old_manifest, new_manifest = verified(old_path), verified(new_path)
    review_raw = (LAB/'config/candidate_review_2026.json').read_bytes()
    review = json.loads(review_raw)
    identity_raw = (LAB/'config/survey_identity_v1.json').read_bytes()
    identity = json.loads(identity_raw)
    rows = {}; changes = {}
    for label, name in [('senate',SENATE),('national',GENERIC)]:
        old_fields, a = table((old_path/name).read_bytes(), {'poll_id','question_id'})
        fields, b = table((new_path/name).read_bytes(), {'poll_id','question_id'})
        if fields != old_fields:
            raise ValueError(f'{label} schema changed: review before acceptance')
        rows[label] = (a,b)
        changes[label+'_raw'] = compare(a,b)
        if label=='national':
            changes['national_reported'] = compare(a,b,AGGREGATOR_FIELDS)
    _, contests = table((new_path/'config/contests_2026.csv').read_bytes(), {'contest_id','state'})
    if (new_path/'config/contests_2026.csv').read_bytes() != (old_path/'config/contests_2026.csv').read_bytes():
        raise ValueError('Contest manifest changed: explicit race review required')
    expected = {r['state'] for r in contests}
    if {r['state'] for r in rows['senate'][1]}-expected:
        raise ValueError('Unexpected Senate state')
    validate_race_ids(rows['senate'][0],rows['senate'][1],review)
    scenario_rows = []; scenarios = {}; question_sets = {}
    for name, raw, cutoff in [('old_data_old_cutoff',rows['senate'][0],old_asof),
                             ('old_data_new_cutoff',rows['senate'][0],asof),
                             ('new_data_new_cutoff',rows['senate'][1],asof)]:
        qs, ans = scenario(raw,review,cutoff,window)
        scenarios[name] = dict(questions=len(qs),accepted=sum(q['accepted_matchup'] for q in qs),
            selected=sum(q['selection']=='selected' for q in qs),
            selected_states=len({q['state'] for q in qs if q['selection']=='selected'}))
        question_sets[name] = qs
        for c in contests:
            pool = [q for q in qs if q['state']==c['state']]
            selected = [q for q in pool if q['selection']=='selected']
            ms = [q['dem_rep_margin'] for q in selected if q['dem_rep_margin'] is not None]
            scenario_rows.append(dict(scenario=name,as_of=str(cutoff),state=c['state'],
                source_questions=len(pool), accepted=sum(q['accepted_matchup'] for q in pool),
                selected=len(selected), dr_observations=len(ms),
                equal_poll_margin_pp=sum(ms)/len(ms) if ms else None,
                status='selected' if selected else 'no_selected_question' if pool else 'no_source_poll'))
    observations, normalized_answers = current_senate(csv_form(qs),csv_form(ans))
    national, national_answers = current_generic(rows['national'][1],asof)
    observations += national; normalized_answers += national_answers
    links = {member:x['canonical'] for x in identity['sample_links'] for member in x['members']}
    pending = {member for x in identity['pending_duplicates'] for member in x['members']}
    for o in observations:
        o['canonical_sample_group_id'] = links.get(o['sample_group_id'],o['sample_group_id'])
        o['identity_review_status'] = ('confirmed_sample_link' if o['sample_group_id'] in links else
            'possible_duplicate_retained' if o['sample_group_id'] in pending else 'no_documented_link')
        o['poll_error_vs_result'] = None
        assert not o['outcome_id'] and o['cycle']==2026
        for field in ['dem_share','rep_share']:
            assert o[field] is None or 0 <= o[field] <= 1
        assert o['dem_rep_margin'] is None or -1 <= o['dem_rep_margin'] <= 1
    additions = set(changes['senate_raw']['added_poll_ids'])
    new_questions = [q for q in qs if q['poll_id'] in additions]
    summary = dict(status='accepted_with_quarantine',model_ready=False,as_of=str(asof),
        old_as_of=str(old_asof),window_days=window,window_endpoints='inclusive',
        source_schema_unchanged=True,source_race_ids_unchanged=True,
        contests=len(contests),source_senate_polls=len({r['poll_id'] for r in rows['senate'][1]}),
        new_senate_questions=len(new_questions),new_questions_accepted=sum(q['accepted_matchup'] for q in new_questions),
        new_questions_quarantined=sum(not q['accepted_matchup'] for q in new_questions),
        national_rows=len(national),national_flagged_rows=sum(bool(o['quality_flags']) for o in national),
        no_source_poll_states=sorted(expected-{r['state'] for r in rows['senate'][1]}),
        scenarios=scenarios,candidate_review_date=review['review_date'],
        candidate_policy='unchanged dated leading-contender screen; incomplete ballot, unknown candidates quarantined',
        confirmed_link_rows=sum(o['identity_review_status']=='confirmed_sample_link' for o in observations),
        possible_duplicate_rows=sum(o['identity_review_status']=='possible_duplicate_retained' for o in observations),
        quarantine_reasons=dict(Counter(r for q in new_questions for r in q['reasons'].split('|') if r)))
    with Snapshot(output,'refresh_2026_acceptance') as snap:
        snap.add('config/candidate_review_2026.json',review_raw)
        snap.add('config/survey_identity_v1.json',identity_raw)
        for name, rs in [('questions',qs),('answers',ans),('observations',observations),
                         ('normalized_answers',normalized_answers),('new_questions',new_questions),
                         ('coverage_scenarios',scenario_rows),('new_national_rows',[r for r in rows['national'][1]
                         if r['poll_id'] in changes['national_raw']['added_poll_ids']])]:
            if rs:snap.add(f'tables/{name}.csv',csv_bytes(list(rs[0]),rs))
        snap.write_json('changes.json',changes)
        snap.write_json('summary.json',summary)
        snap.write_json('provenance.json',dict(old_snapshot=str(old_path.relative_to(LAB)),
            new_snapshot=str(new_path.relative_to(LAB)),old_manifest_sha256=digest((old_path/'manifest.json').read_bytes()),
            new_manifest_sha256=digest((new_path/'manifest.json').read_bytes()),
            scripts={n:digest((LAB/'scripts'/n).read_bytes()) for n in
                     ['audit_refresh_2026.py','prepare_data.py','normalize_data.py','data_utils.py']},
            ignored_only_in_reported_content_diff=sorted(AGGREGATOR_FIELDS),
            units='shares/margins fractions; coverage diagnostic mean in percentage points',
            limitations='Not a complete source census, certified ballot roster, publication vintage or seat-model dataset. '
            'All source rows retained, questionable rows flagged; no missing-poll zeros or future labels. '
            'Canonical links are separate; no unconfirmed duplicate automatically deleted.'))
        return snap.finish(summary)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--old',type=Path,required=True);p.add_argument('--new',type=Path,required=True)
    p.add_argument('--old-as-of',type=date.fromisoformat,required=True)
    p.add_argument('--as-of',type=date.fromisoformat,required=True)
    p.add_argument('--window-days',type=int,default=14)
    p.add_argument('--output-dir',type=Path,default=LAB/'data/refresh_2026')
    a=p.parse_args()
    if a.window_days<0:p.error('window-days must be nonnegative')
    run(a.old.resolve(),a.new.resolve(),a.old_as_of,a.as_of,a.output_dir,a.window_days)

if __name__=='__main__':main()
