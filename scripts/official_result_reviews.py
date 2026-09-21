"""Explicit official-result replacements; source evidence and all deltas retained."""
from collections import Counter
import json
from data_utils import LAB, digest

CONFIG = LAB/'config/official_result_reviews_v1.json'


def apply_reviews(tables, config=None):
    from build_accepted_data import disposition
    config = config or json.loads(CONFIG.read_text())
    outcomes = {r['outcome_id']: r for r in tables['outcomes']}
    errors = {r['observation_id']: r for r in tables['errors']}
    dispositions = {r['observation_id']: r for r in tables['dispositions']}
    audit = []
    for spec in config['results']:
        path = LAB/spec['source_path']
        if digest(path.read_bytes()) != spec['source_sha256']:
            raise ValueError('Changed official evidence')
        oid = spec['outcome_id']; target = outcomes[oid]
        if target['review_reasons'] != spec['expected_old_reason']:
            raise ValueError('Unexpected result restriction; review again: '+oid)
        if int(target['cycle']) != spec['cycle'] or target['geography'] != spec['state']:
            raise ValueError('Official result identity mismatch')
        if str(target['special']).lower() != 'false' or target['stage'] != 'gen':
            raise ValueError('Special/stage requires separate admission')
        total = spec['total_votes']
        if total <= 0 or sum(spec[k] for k in ['dem_votes','rep_votes','other_votes']) != total:
            raise ValueError('Official vote accounting failed')
        before = dict(target)
        margin = (spec['dem_votes']-spec['rep_votes'])/total
        target.update(dem_share=str(spec['dem_votes']/total), rep_share=str(spec['rep_votes']/total),
                      dem_rep_margin=str(margin), diagnostic_eligible='True', review_reasons='',
                      status='official_result_verified', reference_version=config['version'],
                      election_date=spec['election_date'], total_votes=str(total),
                      source=spec['source_url'], source_sheet=spec['source_section'],
                      DEM=str(spec['dem_votes']), REP=str(spec['rep_votes']), OTHER=str(spec['other_votes']))
        changed = 0
        for obs in tables['observations']:
            if obs['outcome_id'] != oid: continue
            err = errors[obs['observation_id']]
            err.update(reference_margin=str(margin), reference_version=config['version'])
            if obs['dem_rep_margin'] != '':
                err.update(poll_error=str(float(obs['dem_rep_margin'])-margin), status='reference_available')
            status, reason = disposition(obs, target, err)
            row = dispositions[obs['observation_id']]
            changed += row['status'] != status
            row.update(status=status, reason=reason)
        for r in tables['result_restrictions']:
            if r['outcome_id'] == oid:
                r.update(result_status=target['status'], reasons='', handling='resolved_official_result_review')
        audit.append(dict(outcome_id=oid, old_margin=float(before['dem_rep_margin']), new_margin=margin,
                          delta_pp=100*(margin-float(before['dem_rep_margin'])), old_status=before['status'],
                          old_reason=before['review_reasons'], new_status=target['status'],
                          disposition_changes=changed, **{k:spec[k] for k in ['source_url','source_path','source_sha256','reviewed_at']}))
    for row in tables['coverage']:
        rs=[r for r in tables['dispositions'] if all(str(r[k])==str(row[k]) for k in ['cycle','dataset','geography','outcome_id'])]
        counts=Counter(r['status'] for r in rs)
        for k in ['usable_retrospective','provisional','excluded','restricted','quarantined','current_screened','candidate_vector_only']:
            row[k]=counts[k]
    for row in tables['outcome_coverage']:
        target=outcomes[row['outcome_id']]
        row.update(diagnostic_eligible=target['diagnostic_eligible'], result_status=target['status'],
                   usable_versions=sum(r['status'] in ['usable_retrospective','provisional'] for r in tables['dispositions'] if r['outcome_id']==row['outcome_id']))
    tables['official_result_review_audit']=audit
    tables['config']['official_result_reviews']=config
    for relative in ['config/official_result_reviews_v1.json']+[r['source_path'] for r in config['results']]:
        tables['config']['files'][relative]=digest((LAB/relative).read_bytes())
    return tables
