"""Build separate observation metadata and retrospective error tables, offline.

Preserve immutable normalized snapshots. Never put realized errors in predictors.
Unknown survey/estimate bases remain unknown; annotations need explicit evidence.
"""
import argparse
from datetime import date
import json
from pathlib import Path

from data_utils import LAB, Snapshot, latest, digest
from prepare_data import read, write_table


def numeric(value):
    try:
        v = float(value)
        return v if __import__('math').isfinite(v) else None
    except (ValueError, TypeError):
        return None


def key(o):
    return tuple(str(o[k]) for k in ('source','dataset','cycle','geography','source_poll_id','source_question_id'))


def enrich(observations, outcomes, annotations, as_of):
    lookup = {}
    for a in annotations:
        k = key(a)
        if k in lookup: raise ValueError(f'Duplicate annotation: {k}')
        if not a.get('evidence'): raise ValueError(f'Annotation lacks evidence: {k}')
        lookup[k] = a
    targets = {r['outcome_id']: r for r in outcomes}
    if len(targets) != len(outcomes): raise ValueError('Duplicate outcome IDs')
    metadata, errors, used = [], [], set()
    for o in observations:
        row = dict(observation_id=o['observation_id'], source=o['source'], dataset=o['dataset'],
                   cycle=o['cycle'], geography=o['geography'], source_poll_id=o['source_poll_id'],
                   source_question_id=o['source_question_id'], population=o['population'],
                   reported_n=numeric(o['sample_size']), reported_n_basis='unknown',
                   estimate_basis='unknown', survey_n=None, estimate_n=None,
                   basis_review_status='not_reviewed', basis_evidence='', basis_notes='',
                   selection_status=o['selection_status'], source_quality_flags=o['quality_flags'])
        if key(o) in lookup:
            a = lookup[key(o)]; used.add(key(o))
            for f, expected in a['expected'].items():
                v = numeric(o.get(f))
                if v is None or abs(v-float(expected)) > 1e-9:
                    raise ValueError(f'Stale annotation {key(o)}: {f} changed')
            row.update({f:a[f] for f in ('reported_n_basis','estimate_basis','survey_n','estimate_n','basis_review_status')})
            row.update(basis_evidence=a['evidence'], basis_notes=a['notes'])
        metadata.append(row)
        target = targets.get(o['outcome_id'])
        margin = numeric(o['dem_rep_margin'])
        label = numeric(target['dem_rep_margin']) if target else None
        # Retain one diagnostic row per observation, with explicit reasons for blanks.
        if not o.get('election_date') or date.fromisoformat(o['election_date']) >= as_of:
            status = 'not_yet_observed'
        elif o['selection_status'] in ('superseded_by_full_archive','excluded','alternative_question_same_poll'):
            status = 'excluded_or_superseded_observation'
        elif o['matchup_status'] not in ('matched','matched_candidate_identity','generic_party_question','accepted'):
            status = 'unresolved_matchup'
        elif margin is None:
            status = 'missing_poll_margin'
        elif not target or label is None:
            status = 'missing_outcome'
        elif target['status'] == 'review_required':
            status = 'outcome_requires_review'
        else:
            status = 'computed_provisional_outcome' if target['status']=='source_reported_not_independently_reconciled' else 'computed'
        computable = status.startswith('computed')
        errors.append(dict(observation_id=o['observation_id'], cycle=o['cycle'], geography=o['geography'],
            dataset=o['dataset'], source_poll_id=o['source_poll_id'], sample_group_id=o['sample_group_id'],
            outcome_id=o['outcome_id'], election_date=o['election_date'], poll_date=o['poll_date'],
            days_to_election=o['days_to_election'], poll_margin_pp=100*margin if margin is not None else None,
            outcome_margin_pp=100*label if computable else None,
            poll_error_pp=100*(margin-label) if computable else None,
            absolute_poll_error_pp=abs(100*(margin-label)) if computable else None,
            error_status=status, outcome_status=target['status'] if target else '',
            selection_status=o['selection_status'], matchup_status=o['matchup_status'],
            diagnostic_only=True))
    unused = set(lookup)-used
    if unused: raise ValueError(f'Annotations no longer match source observations: {sorted(unused)}')
    return metadata, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--normalized-dir', type=Path, default=LAB/'data/normalized')
    parser.add_argument('--output-dir', type=Path, default=LAB/'data/audit')
    parser.add_argument('--annotations', type=Path, default=LAB/'config/estimate_basis_annotations.json')
    parser.add_argument('--as-of', type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    source, manifest = latest(args.normalized_dir)
    annotations = json.loads(args.annotations.read_text())
    metadata, errors = enrich(read(source/'tables/poll_observations.csv'),
                             read(source/'tables/election_outcomes.csv'), annotations, args.as_of)
    from collections import Counter
    summary = dict(normalized_snapshot=source.name, as_of=str(args.as_of), observations=len(metadata),
                   basis_reviewed=sum(r['basis_review_status']!='not_reviewed' for r in metadata),
                   error_status=dict(Counter(r['error_status'] for r in errors)),
                   diagnostic_only=True, raw_reported_n_preserved=True)
    with Snapshot(args.output_dir,'audit') as bundle:
        write_table(bundle,'poll_observation_metadata',metadata)
        write_table(bundle,'poll_outcome_errors',errors)
        bundle.write_json('summary.json',summary)
        bundle.write_json('provenance.json',dict(normalized_snapshot=source.name,
            normalized_manifest_sha256=digest((source/'manifest.json').read_bytes()),
            annotations_sha256=digest(args.annotations.read_bytes()),
            script_sha256=digest(Path(__file__).read_bytes()), as_of=str(args.as_of),
            units='Shares in input are fractions; diagnostic margins/errors are percentage points.',
            label_availability='Retrospective final results, not reconstructed publication-time vintages.',
            restrictions='Do not use outcome/error fields as forecasting predictors; source-reported outcomes remain provisional.'))
        bundle.finish(summary)
    print(json.dumps(summary,indent=2))

if __name__ == '__main__': main()
