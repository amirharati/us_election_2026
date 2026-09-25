"""Deterministic current-poll supplements and exact candidate identity review.

Raw upstream rows are never overwritten. Reviews and supplements are sealed with
compact inputs; refreshes need no AI calls. Candidate replacements are not aliases.
"""
import json
from pathlib import Path
import re
from datetime import date


def canonical_candidate(answer, spec):
    cid=answer['candidate_id']
    for candidate in spec['candidates']:
        if cid and cid in [candidate['candidate_id'],*candidate.get('source_ids',[])]:
            return candidate
    # Explicitly listed exact names allow source UUID changes, never fuzzy matches.
    for candidate in spec['candidates']:
        if (answer['candidate_name'] in candidate.get('source_names',[])
                and answer['party'] in candidate.get('source_parties',[candidate['party']])):
            return candidate
    return None


def reviewed_feed(upstream, supplements, as_of):
    from prepare_data import day
    rows=[dict(r) for r in upstream];receipts=[]
    columns=list(upstream[0])
    norm=lambda x: re.sub(r'[^a-z0-9]','',str(x).lower()).removeprefix('the')
    for poll in supplements['polls']:
        metadata=poll['metadata']
        # Same firm/state and overlapping field period identifies a possible upstream
        # copy. Prefer upstream and record the decision, never count two samples.
        matches=[r for r in upstream if r['state']==metadata['state']
                 and norm(r['pollster']) in {norm(x) for x in [metadata['pollster'],*poll.get('pollster_aliases',[])]}
                 and day(r['start_date'])<=day(metadata['end_date'])
                 and day(r['end_date'])>=day(metadata['start_date'])]
        matches=[r for r in matches if r['poll_id'] not in poll.get('retain_alongside_upstream_poll_ids',[])]
        status='upstream_sample_present' if matches else 'supplement_added'
        receipts.append(dict(poll_id=metadata['poll_id'],state=metadata['state'],status=status,
                             publication_date=metadata['created_at'],source_url=metadata['url'],
                             source_sha256=poll['source_sha256'],notes=poll['review_notes']))
        if matches:continue
        for question in poll['questions']:
            for answer in question['answers']:
                row={c:'' for c in columns}
                row.update(cycle='2026',office_type='U.S. Senate',stage='general',election_date='2026-11-03',
                           ranked_choice_final='FALSE',ranked_choice_reallocated='FALSE')
                row.update(metadata)
                row.update(question_id=question['question_id'],**question.get('metadata',{}))
                row.update(answer)
                row['answer']=row['candidate_name']
                rows.append(row)
    return rows,receipts
