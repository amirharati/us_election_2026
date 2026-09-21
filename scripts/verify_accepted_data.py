"""Independent acceptance checks on in-memory or reloaded exported tables.

Does not invoke builder selection/normalization logic. Checks joins, arithmetic,
accounting, future labels, fractional units and the predictor/label boundary.
"""
from collections import Counter,defaultdict
import argparse
import json
import math
from pathlib import Path
from data_utils import LAB,digest
from prepare_data import read
from audit_refresh_2026 import verified


def require(test,message):
    if not test:raise ValueError(message)


def num(x):
    if x is None or x=='':return None
    value=float(x);require(math.isfinite(value),'Nonfinite numeric value');return value


def verify_tables(t):
    obs=t['observations'];lookup={r['observation_id']:r for r in obs};ids=set(lookup)
    require(len(obs)==len(ids),'Duplicate observation IDs')
    for name in ['metadata','identity','errors','dispositions','lineage','predictors']:
        rows=t[name];require(len(rows)==len(ids) and {r['observation_id'] for r in rows}==ids,f'{name} incomplete or duplicate join')
    outcomes={r['outcome_id']:r for r in t['outcomes']}
    require(len(outcomes)==len(t['outcomes']),'Duplicate outcomes')
    errors={r['observation_id']:r for r in t['errors']};metas={r['observation_id']:r for r in t['metadata']}
    identity={r['observation_id']:r for r in t['identity']}
    basis_checks=0;margin_checks=0
    for o in obs:
        d,r,m=[num(o.get(k)) for k in ['dem_share','rep_share','dem_rep_margin']]
        require(all(x is None or 0<=x<=1 for x in [d,r]),'Shares outside fraction range')
        if d is not None and r is not None:
            require(m is not None and abs(m-(d-r))<1e-9,'D-R margin arithmetic mismatch');margin_checks+=1
        if m is not None:require(-1<=m<=1,'Margin outside fraction range')
        require(not o['outcome_id'] or o['outcome_id'] in outcomes,'Dangling outcome join')
        require(num(o['sample_size'])==num(metas[o['observation_id']]['reported_n']),'Reported N changed by metadata join')
        require(o['canonical_sample_group_id']==identity[o['observation_id']]['canonical_sample_group_id'],'Canonical sample join mismatch')
        for key in filter(None,o.get('superseded_by','').split('|')):require(key in ids,'Dangling supersession link')
        e=errors[o['observation_id']]
        if str(o['cycle'])=='2026':
            require(not o['outcome_id'] and num(e.get('poll_error')) is None and num(e.get('reference_margin')) is None,'Future outcome leakage')
        elif num(e.get('poll_error')) is not None:
            require(m is not None and num(e.get('reference_margin')) is not None,'Error without margin/reference')
            require(abs(num(e['poll_error'])-(m-num(e['reference_margin'])))<1e-9,'Error sign or units mismatch')
        if metas[o['observation_id']]['basis_review_status']!='not_reviewed':basis_checks+=1
    # Predictor export is an explicit interface, not all columns copied from analysis.
    forbidden={'outcome_id','poll_error','poll_error_vs_result','reference_margin','original_outcome_id',
        'reference_version','diagnostic_eligible','legacy_split','status','selection_status','scalar_seat_mapping_ready'}
    for r in t['predictors']:
        require(not forbidden.intersection(r),'Outcome/selection fields leaked into predictor interface')
        require(all(r[k]==lookup[r['observation_id']].get(k,'') for k in r),'Predictor value changed')
    vectors=defaultdict(list)
    for a in t['answers']:
        require(a['observation_id'] in ids,'Dangling answer join')
        s=num(a['support_share']);require(s is None or 0<=s<=1,'Candidate share outside fraction range')
        if str(a['exact_duplicate']).lower()!='true':vectors[a['observation_id']].append(a)
    answer_checks=0
    for oid,rows in vectors.items():
        for party,field in [('DEM','dem_share'),('REP','rep_share')]:
            aa=[a for a in rows if a['party']==party];value=num(lookup[oid].get(field))
            if len(aa)==1 and value is not None:
                require(abs(value-num(aa[0]['support_share']))<1e-9,'Answer and observation differ');answer_checks+=1
    for row in t['corrections']:
        require(row['observation_id'] in ids,'Dangling correction ID')
        require(abs(num(lookup[row['observation_id']]['dem_share'])-num(row['reviewed_dem_share']))<1e-9,'Reviewed correction lost')
    for r in t['state_features']:
        require(int(r['prior_presidential_year'])<int(r['cycle']),'Same-cycle prior leakage')
        require(abs(num(r['prior_state_lean'])-(num(r['prior_state_pres_margin'])-num(r['prior_national_pres_margin'])))<1e-9,'State lean arithmetic mismatch')
        require('split' not in r,'Legacy test split presented as fresh holdout')
    coverage=t['coverage']
    require(sum(int(r['stored_versions']) for r in coverage)==len(obs),'Coverage loses observations')
    for c in coverage:
        require(sum(int(c[k]) for k in ['usable_retrospective','provisional','excluded','restricted','quarantined','current_screened','candidate_vector_only'])==int(c['stored_versions']),'Disposition counts do not reconcile')
    require(len(t['outcome_coverage'])==len(outcomes) and {r['outcome_id'] for r in t['outcome_coverage']}==set(outcomes),'Unpolled outcomes disappeared')
    seats=t['seat_ledger'];require(len(seats)==100 and len({r['seat_id'] for r in seats})==100,'100 distinct seats required')
    require(Counter(r['status'] for r in seats)=={'continuing':65,'contested':35},'Contested plus continuing seat total wrong')
    require(len({r['state'] for r in seats})==50 and set(Counter(r['state'] for r in seats).values())=={2},'Two seats for every state required')
    cc=t['current_contests'];require(len(cc)==35 and {r['contest_id'] for r in cc}=={r['contest_id'] for r in seats if r['status']=='contested'},'Current contests and seats disagree')
    require(all(str(r['seat_forecast_ready']).lower()=='false' for r in cc),'Incomplete candidate roster marked ready')
    require(len({(str(r['cycle']),r['state']) for r in t['state_calendar']})==len(t['state_calendar']),'Duplicate state calendar rows')
    return dict(observation_ids=len(ids),one_to_one_overlay_tables=6,margin_arithmetic=margin_checks,
        answer_share_checks=answer_checks,reviewed_basis_versions=basis_checks,
        historical_error_arithmetic='passed',future_labels_blank='passed',predictor_boundary='passed',
        reported_n_preservation='passed',feature_lags='passed',coverage_accounting='passed',seat_accounting='100=65+35')


def verify(path):
    verified(path)
    tables={p.stem:read(p) for p in (path/'tables').glob('*.csv')}
    result=verify_tables(tables)
    config=json.loads((path/'config.json').read_text())
    if 'official_result_reviews' in config:
        labels={r['outcome_id']:r for r in tables['outcomes']}
        observations={r['observation_id']:r for r in tables['observations']}
        for spec in config['official_result_reviews']['results']:
            require(digest((LAB/spec['source_path']).read_bytes())==spec['source_sha256'],'Official evidence changed')
            r=labels[spec['outcome_id']];total=spec['total_votes']
            require(total==spec['dem_votes']+spec['rep_votes']+spec['other_votes'],'Official vote accounting')
            expected=(spec['dem_votes']-spec['rep_votes'])/total
            require(abs(float(r['dem_rep_margin'])-expected)<1e-12,'Official label mismatch')
            require(str(r['diagnostic_eligible']).lower()=='true' and not r['review_reasons'],'Official admission lost')
            for e in tables['errors']:
                if e['outcome_id']==spec['outcome_id']:
                    require(abs(float(e['reference_margin'])-expected)<1e-12,'Stale linked reference')
                    o=observations[e['observation_id']]
                    if o['dem_rep_margin']:
                        require(abs(float(e['poll_error'])-(float(o['dem_rep_margin'])-expected))<1e-12,'Stale linked poll error')
        result['official_result_reviews_verified']=len(config['official_result_reviews']['results'])
    for name,info in config['snapshots'].items():
        src=LAB/info['path'];verified(src)
        require(digest((src/'manifest.json').read_bytes())==info['sha256'],f'Input manifest changed: {name}')
    # Check source preservation independently of the builder and its disposition rules.
    origins={name:read(LAB/config['snapshots'][name]['path']/'tables/observations.csv') for name in ['reviewed','refresh']}
    lookup={(name,r['observation_id']):r for name,rs in origins.items() for r in rs}
    expected={(name,r['observation_id']) for name,rs in origins.items() for r in rs if name=='refresh' or r['cycle']!='2026'}
    require({(r['origin_bundle'],r['origin_observation_id']) for r in tables['observations']}==expected,'Current duplicated or historical records lost')
    for r in tables['observations']:
        source=lookup[(r['origin_bundle'],r['origin_observation_id'])]
        for field in ['source','source_rows','source_poll_id','source_question_id','cycle','geography','sample_size','dem_share','rep_share','dem_rep_margin','quality_flags','selection_status','outcome_id','election_date','poll_start','poll_end','poll_date','source_available_date','days_to_election']:
            require(r[field]==source[field],f'Unexpected source change: {r["observation_id"]} {field}')
    result['source_values_preserved']=len(tables['observations'])
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('snapshot',type=Path)
    a=p.parse_args();print(json.dumps(verify(a.snapshot),indent=2))
