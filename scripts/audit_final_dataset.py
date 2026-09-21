"""Audit the latest/pinned bundle and export metadata, schema and missingness evidence."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from audit_refresh_2026 import verified
from data_utils import LAB
from alignment_features import sha
from load_final_dataset import open_dataset


def audit(snapshot=None):
    dataset=open_dataset(snapshot)
    for source in dataset.provenance['manifests']:verified(Path(source))
    run=dataset.provenance.get('run', {})
    if run.get('receipt'):
        if sha(LAB/run['receipt']) != run['receipt_sha256']:
            raise ValueError('Refresh receipt checksum mismatch')
    tables={}
    for name, expected_count in dataset.summary['counts'].items():
        frame=dataset.load_table(name)
        if len(frame) != expected_count:raise ValueError(f'Incorrect summary count: {name}')
        tables[name]=dict(rows=len(frame), columns={
            col:dict(dtype=str(frame[col].dtype), missing=int(frame[col].isna().sum())) for col in frame})
    if dataset.summary['as_of'] != dataset.policy['as_of']:
        raise ValueError('Summary/policy cutoff mismatch')
    ledger=dataset.load_table('feature_ledger')
    current=ledger[ledger.context_id.eq(dataset.policy['as_of'])]
    if len(current) != dataset.policy['selected_national_features']:
        raise ValueError('Incomplete current feature coverage')
    coverage=dataset.load_table('contest_coverage').merge(
        dataset.load_table('labels')[['target_id','cycle']], on='target_id', validate='one_to_one')
    return dict(
        audit_version=1, audited_at=datetime.now(timezone.utc).isoformat(),
        status='passed_with_documented_restrictions', dataset=dataset.metadata(),
        checks=dataset.checks, source_files_checksum_verified=True,
        summary_counts_verified=True, tables=tables,
        current_feature_count=len(current),
        current_populated_features=int(current.value_reference.notna().sum()),
        current_features=json.loads(current.drop(columns=['input_monthly_ids']).to_json(orient='records', date_format='iso')),
        current_contest_coverage=coverage[coverage.cycle.eq(2026)].status.value_counts().to_dict(),
        caveats=[
            'Reference data includes revised history; historical publication/vintage evidence is incomplete.',
            'Observed feature view alone does not certify poll publication or a strict historical backtest.',
            'Stored poll versions are not independent samples; selection/weighting remains a model decision.',
            'Political-control values beyond the reviewed-through date remain missing.',
            'Candidate/ballot/seat-rule restrictions remain; this is not a certified seat forecast.',
        ], political_review_through=dataset.summary['current_political_review_through'],
    )


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path)
    parser.add_argument('--output', type=Path)
    args=parser.parse_args();report=audit(args.snapshot)
    output=args.output or LAB/'data/final_audits'/f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')}.json"
    encoded=json.dumps(report, indent=2, allow_nan=False)+'\n'
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x') as f:f.write(encoded)
    print(json.dumps(dict(report=str(output), status=report['status'],
                         snapshot_id=report['dataset']['snapshot_id'],
                         current_populated_features=report['current_populated_features']), indent=2))
