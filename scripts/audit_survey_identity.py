"""Identity/dependence audit, separate from values, outcomes and model predictors.

Fingerprint matches are review candidates, never proof of duplicated respondents.
Only source-backed publisher aliases are applied; rating families are sensitivity keys.
"""
from collections import Counter,defaultdict
from itertools import combinations
from datetime import date
from pathlib import Path
import json
from data_utils import LAB,latest,digest,csv_bytes
from prepare_data import read

FACTS=LAB/'config/survey_identity_v1.json'

def label(s):return ' '.join(s.casefold().split())
def sponsor_key(ids,names):
    # Vendor IDs are semicolon-separated sets. Unknown is not an independent series.
    return 'ids:'+ ';'.join(sorted(set(x.strip() for x in ids.split(';') if x.strip()))) if ids.strip() else 'names:'+label(names) if names.strip() else 'unspecified'

def overlap(a,b):
    if not all(r.get(k) for r in (a,b) for k in ('poll_start','poll_end')):return None
    return max(0,(min(date.fromisoformat(a['poll_end']),date.fromisoformat(b['poll_end']))-
                  max(date.fromisoformat(a['poll_start']),date.fromisoformat(b['poll_start']))).days+1)

def fingerprint(r):
    # Deliberately stringent, still not sufficient to delete independent polls.
    fields=('cycle','dataset','geography','outcome_id','poll_start','poll_end','population','sample_size','dem_share','rep_share')
    if not all(r.get(k) for k in fields if k!='outcome_id'):return None
    return (r['canonical_firm'],)+tuple(r[k] for k in fields)

def audit(observations=None,paths=None):
    reviewed_path,_=latest(LAB/'data/reviewed')
    meta=json.loads((reviewed_path/'provenance.json').read_text())
    paths=paths or {k:LAB/'data'/k/'snapshots'/v for k,v in meta['snapshots'].items()}
    if observations is None:observations=read(reviewed_path/'tables/observations.csv')
    source_dir=LAB/'reports/source_audit/survey_identity'
    for proof in json.loads((source_dir/'provenance.json').read_text()):
        assert proof.get('sha256') and digest((source_dir/proof['file']).read_bytes())==proof['sha256']
    facts=json.loads(FACTS.read_text());aliases={label(n):a['canonical'] for a in facts['aliases'] for n in a['names']}
    raw={d:read(paths['historical']/f'tables/538_archive_{d}.csv') for d in ('senate','generic_ballot')}
    current_nyt=read(paths['2026']/'tables/senate_general_answers.csv')
    current_generic=read(paths['2026']/'raw/silver_bulletin_generic.csv')
    identity=[];conflicts=[]
    for r in observations:
        if int(r['cycle'])<2016:continue
        x=dict(r);x.update(canonical_firm=aliases.get(label(r['pollster']),label(r['pollster'])) or 'unknown:'+r['observation_id'],
                         publisher_id='',rating_id='',rating_name='',sponsor_ids='',sponsor_names='',series_key='',identity_basis='label_only')
        if r['source'] in ('538_archive','nyt'):
            source_rows=raw[r['dataset']] if r['source']=='538_archive' else current_nyt
            rows=[source_rows[int(i)-2] for i in r['source_rows'].split('|')]
            assert all((z['poll_id'],z['question_id'],z['race_id'])==(r['source_poll_id'],r['source_question_id'],r['source_race_id']) for z in rows)
            fields=['pollster_id','pollster_rating_id','pollster_rating_name','sponsor_ids','sponsors','tracking']
            for k in fields:
                if len({z[k] for z in rows})>1:conflicts.append(dict(observation_id=r['observation_id'],field=k,values='|'.join(sorted({z[k] for z in rows}))))
            z=rows[0];x.update(publisher_id=z['pollster_id'],rating_id=z['pollster_rating_id'],rating_name=z['pollster_rating_name'],
                sponsor_ids=z['sponsor_ids'],sponsor_names=z['sponsors'],identity_basis='archive_rows_verified' if r['source']=='538_archive' else 'current_rows_verified')
        if r['source']=='silver_bulletin':
            z=current_generic[int(r['source_rows'])-2]
            assert (z['poll_id'],z['question_id'])==(r['source_poll_id'],r['source_question_id'])
            x.update(sponsor_names=z['sponsors'],identity_basis='current_rows_verified')
        x['series_key']=x['canonical_firm']+'|'+sponsor_key(x['sponsor_ids'],x['sponsor_names'])
        x['rating_family_key']='rating:'+x['rating_id'] if x['rating_id'] else 'firm:'+x['canonical_firm']
        # Only the confirmed tracker series, not Morning Consult/Politico's RV surveys.
        x['rolling_method_evidence']=('MC2022_3day' if r['cycle']=='2022' and r['dataset']=='generic_ballot'
            and label(r['pollster'])=='morning consult' and r['population']=='lv' and
            r['source_url'].rstrip('/')=='https://morningconsult.com/2022-midterm-elections-tracker' else '')
        x['canonical_sample_group_id']=r['sample_group_id']
        x['sample_identity_status']='source_id_only'
        for link in facts.get('sample_links',[]):
            if r['sample_group_id'] in link['members']:
                x['canonical_sample_group_id']=link['canonical']
                x['sample_identity_status']=link['status']
        for pending in facts.get('pending_duplicates',[]):
            if r['sample_group_id'] in pending['members']:
                x['sample_identity_status']=pending['status']
        identity.append(x)
    for link in facts.get('sample_links',[]):
        linked=[r for r in identity if r['sample_group_id'] in link['members']]
        assert {r['sample_group_id'] for r in linked}==set(link['members']), 'Sample-link source changed: review before reuse'
        assert len({fingerprint(r) for r in linked})==1 and fingerprint(linked[0]) is not None
        assert len({(r['source_url'],r['source_race_id'],r['publisher_id'],r['reported_answer_sum']) for r in linked})==1
    active=[r for r in identity if r['selection_status']!='superseded_by_full_archive']
    families=defaultdict(list);ids=defaultdict(set);names=defaultdict(set)
    for r in identity:
        if r['publisher_id']:ids[(r['source'],r['publisher_id'])].add(r['pollster']);names[(r['source'],r['pollster'])].add(r['publisher_id'])
        if r['rating_id'] and r['source']=='538_archive':families[r['rating_id']].append(r)
    family_rows=[dict(rating_id=k,rating_name=rs[0]['rating_name'],publisher_ids='|'.join(sorted({r['publisher_id'] for r in rs})),
        names=' | '.join(sorted({r['pollster'] for r in rs})),canonical_firms=len({r['canonical_firm'] for r in rs}),
        versions=len(rs),disposition='sensitivity_only_not_identity_proof') for k,rs in families.items() if len({r['publisher_id'] for r in rs})>1]
    # Validate source-overlap disposition without assuming equal shares between versions.
    by_sample=defaultdict(list)
    for r in identity:by_sample[r['sample_group_id']].append(r)
    supersession=[];bundles=[]
    for sample,rs in by_sample.items():
        for r in rs:
            if r['selection_status']=='superseded_by_full_archive':
                match=[s for s in rs if s['source']=='538_archive' and s['dataset']==r['dataset']]
                assert match, r['observation_id']
                supersession.append(dict(observation_id=r['observation_id'],sample_group_id=sample,archive_versions=len(match),status='excluded_before_selection'))
        alive=[r for r in rs if r['selection_status']!='superseded_by_full_archive']
        if len(alive)>1:bundles.append(dict(sample_group_id=sample,versions=len(alive),questions=len({(r['dataset'],r['source_question_id']) for r in alive}),
            geographies='|'.join(sorted({r['geography'] for r in alive})),outcomes='|'.join(sorted({r['outcome_id'] for r in alive})),
            populations='|'.join(sorted({r['population'] for r in alive})),datasets='|'.join(sorted({r['dataset'] for r in alive})),
            disposition='select_within_contest_keep_shared_id_across_targets'))
    prints=defaultdict(list)
    for r in active:
        key=fingerprint(r)
        if key:prints[key].append(r)
    duplicates=[]
    for rs in prints.values():
        for a,b in combinations(rs,2):
            if a['sample_group_id']==b['sample_group_id']:continue
            duplicates.append(dict(left=a['observation_id'],right=b['observation_id'],cycle=a['cycle'],geography=a['geography'],
                outcome_id=a['outcome_id'],firm=a['canonical_firm'],left_poll=a['source_poll_id'],right_poll=b['source_poll_id'],
                canonical_same_sample=a['canonical_sample_group_id']==b['canonical_sample_group_id'],same_url=bool(a['source_url'] and a['source_url']==b['source_url']),url=a['source_url'],status='same_reported_survey_canonical_link' if a['canonical_sample_group_id']==b['canonical_sample_group_id'] else 'unverified_fingerprint_match_no_auto_drop'))
    summary=dict(recent_versions=len(identity),active_versions=len(active),archive_identity_rows=sum(r['identity_basis']=='archive_rows_verified' for r in identity),
        current_identity_rows=sum(r['identity_basis']=='current_rows_verified' for r in identity),
        publisher_id_name_conflicts=sum(len(v)>1 for v in ids.values()),name_id_conflicts=sum(len(v)>1 for v in names.values()),
        metadata_conflicts=len(conflicts),rating_families_with_multiple_publishers=len(family_rows),
        superseded_versions_checked=len(supersession),multi_version_samples=len(bundles),different_id_fingerprint_pairs=len(duplicates))
    return dict(identity=identity,families=family_rows,supersession=supersession,bundles=bundles,duplicates=duplicates,conflicts=conflicts,summary=summary,
                provenance=dict(version=facts['version'],reviewed_snapshot=reviewed_path.name,input_snapshots={k:p.name for k,p in paths.items()},
                    source_provenance_sha256=digest((source_dir/'provenance.json').read_bytes()),
                    input_manifest_sha256={k:digest((p/'manifest.json').read_bytes()) for k,p in paths.items()},
                    config_sha256=digest(FACTS.read_bytes()),script_sha256=digest(Path(__file__).read_bytes())))

def sensitivity(rows):
    """Fixed membership: only group weighting or date-overlap sensitivity changes."""
    def mean(rs):return sum(float(r['dem_rep_margin']) for r in rs)/len(rs)*100
    result=[]
    for name,key in [('equal_label','pollster'),('equal_canonical','canonical_firm'),('equal_rating_family','rating_family_key'),('equal_firm_sponsor','series_key')]:
        g=defaultdict(list)
        for r in rows:g[label(r[key])].append(r)
        result.append(dict(method=name,polls=len(rows),groups=len(g),mean_pp=sum(mean(rs) for rs in g.values())/len(g)))
    kept=[]
    for r in sorted(rows,key=lambda r:(r['poll_end'],r['poll_start'],r['observation_id']),reverse=True):
        if not any(r['series_key']==s['series_key'] and (overlap(r,s) or 0)>0 for s in kept):kept.append(r)
    result.append(dict(method='latest_nonoverlap_per_series_sensitivity',polls=len(kept),groups=len({r['series_key'] for r in kept}),mean_pp=mean(kept)))
    return result,kept

def write(result,out=None):
    out=out or LAB/'reports/data_review';out.mkdir(parents=True,exist_ok=True)
    for key in ('identity','families','supersession','bundles','duplicates','conflicts'):
        rows=result[key]
        # Empty tables still receive a header; no stale result from an earlier run.
        fields=list(dict.fromkeys(k for r in rows for k in r)) or ['status']
        (out/f'survey_identity_{key}.csv').write_bytes(csv_bytes(fields,rows))
    (out/'survey_identity_summary.json').write_text(json.dumps(dict(**result['summary'],provenance=result['provenance']),indent=2)+'\n')

if __name__=='__main__':
    r=audit();write(r);print(json.dumps(r['summary'],indent=2))
