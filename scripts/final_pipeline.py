"""Rebuild prepared inputs and the final dataset from one explicit refresh receipt."""
import argparse
from datetime import date, datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys

from data_utils import LAB, atomic_json, digest, latest
from refresh_2026 import verified_receipt
from prepare_features import stable, sha_file

BASE_ACCEPTANCE=LAB/'config/preparation_acceptance_v1.json'
# Retain the approved gasoline addition even during a later partial-source refresh.
# The earlier feature-review notebook's frozen input config remains unchanged.
BASE_FEATURES=LAB/'config/feature_preparation_cost_v2.json'


def ref(path):
    p=Path(path).resolve()
    return str(p.relative_to(LAB)) if p.is_relative_to(LAB) else str(p)


def pin_feature_receipt(receipt, output):
    """Replace only explicitly refreshed current bundles; retain pinned historical/source alternatives."""
    baseline=json.loads(BASE_FEATURES.read_text())
    replacements={r['source']:Path(r['snapshot']) for r in receipt['results'] if r['source']!='polls' and r['status']=='saved_or_unchanged'}
    paths=[];replaced=set()
    for entry in baseline['bundles']:
        p=LAB/entry['path'];request=json.loads((p/'request.json').read_text())
        source=request['source']
        if request['mode']=='current' and source in replacements:
            p=replacements[source];replaced.add(source)
        paths.append(p)
    paths += [p for source,p in replacements.items() if source not in replaced]
    paths=list(dict.fromkeys(p.resolve() for p in paths));bundles=[];unique={}
    for p in paths:
        check=verified_receipt(p);manifest=json.loads((p/'manifest.json').read_text())
        request=json.loads((p/'request.json').read_text());source=request['source']
        bundles.append(dict(path=ref(p),manifest_sha256=check['manifest_sha256']))
        for name,info in sorted(manifest['files'].items()):
            if not name.startswith('raw/'):continue
            key=(source,Path(name).name,info['sha256'])
            origin=dict(path=ref(p/name),url=info.get('url',''),retrieved_at=info.get('retrieved_at',manifest.get('retrieved_at','')))
            if key not in unique:unique[key]=dict(id=stable(key)[:24],source=source,path=origin['path'],sha256=info['sha256'],origins=[])
            unique[key]['origins'].append(origin)
    config=dict(schema_version=1,bundles=bundles,artifacts=list(unique.values()))
    atomic_json(output,config)
    return config


def validate_receipt_cutoff(receipt, as_of):
    """Compare retrieval and cutoff on the same local calendar, not UTC dates.

    Live/CLI cutoffs use date.today(). New receipts pin an offset-aware local
    timestamp for portability; legacy receipts use this machine's local zone.
    Both timestamps must identify the same instant when a local copy is present.
    """
    retrieved = datetime.fromisoformat(receipt['finished_at'])
    if retrieved.tzinfo is None:
        retrieved = retrieved.replace(tzinfo=timezone.utc)  # Legacy UTC receipts.
    if receipt.get('finished_at_local'):
        local = datetime.fromisoformat(receipt['finished_at_local'])
        if local.tzinfo is None or local != retrieved:
            raise ValueError('Receipt local/UTC retrieval timestamps disagree')
    else:
        local = retrieved.astimezone()
    if local.date() > as_of:
        raise ValueError(f'Receipt retrieval date {local.date()} exceeds requested '
                         f'current cutoff {as_of} (receipt local calendar)')


def prepare(receipt_path,as_of,data_dir=LAB/'data'):
    receipt_path=Path(receipt_path).resolve();data_dir=Path(data_dir).resolve()
    if not data_dir.is_relative_to(LAB):raise ValueError('Final build data directory must be inside the lab; isolated raw downloads can use any directory')
    receipt=json.loads(receipt_path.read_text())
    if receipt['status']!='acquisition_complete':raise ValueError('Cannot align a failed or incomplete refresh receipt')
    validate_receipt_cutoff(receipt,as_of)
    for item in receipt['results']:
        if 'snapshot' in item:
            actual=verified_receipt(item['snapshot'])
            if actual['manifest_sha256']!=item['manifest_sha256']:raise ValueError('Receipt manifest mismatch')
    current=next(Path(r['snapshot']) for r in receipt['results'] if r['source']=='polls')
    if not current.is_relative_to(LAB):raise ValueError('Final-build poll snapshots must be inside the lab')
    work=data_dir/'final_work'/f'{receipt_path.stem}_{as_of}'
    work.mkdir(parents=True,exist_ok=True)
    config=json.loads(BASE_ACCEPTANCE.read_text())
    old=LAB/config['snapshots']['current_raw']['path']
    old_summary=json.loads((LAB/config['snapshots']['refresh']['path']/'summary.json').read_text())
    from audit_refresh_2026 import run
    refreshed=run(old,current,date.fromisoformat(old_summary['as_of']),as_of,data_dir/'final_inputs/current_polls')
    for key,path in [('refresh',refreshed),('current_raw',current)]:
        config['snapshots'][key]=dict(path=ref(path),sha256=sha_file(path/'manifest.json'))
    acceptance=work/'acceptance.json';atomic_json(acceptance,config)
    from build_accepted_data import build,publish
    from verify_accepted_data import verify
    accepted=publish(build(acceptance),data_dir/'final_inputs/accepted',acceptance)
    verify(accepted)
    feature_config=work/'feature_inputs.json';pin_feature_receipt(receipt,feature_config)
    output=data_dir/'final_inputs/features_prepared'
    result=subprocess.run([sys.executable,str(LAB/'scripts/prepare_features.py'),'--config',str(feature_config),'--output',str(output)],capture_output=True,text=True)
    (work/'feature_preparation.log').write_text(result.stdout+result.stderr)
    if result.returncode:raise RuntimeError('Feature preparation failed; see '+str(work/'feature_preparation.log'))
    prepared=latest(output)[0]
    from verify_prepared_features import verify as verify_features
    verify_features(output)
    from build_political_context import build as build_political
    political=build_political(root=data_dir/'final_inputs/political')
    result=dict(accepted=ref(accepted),features=ref(prepared),political=ref(political),as_of=str(as_of),
                receipt=ref(receipt_path),receipt_sha256=sha_file(receipt_path),work=ref(work),
                receipt_sources=receipt['sources'],full_public_collection=len(receipt['sources'])==20)
    atomic_json(work/'prepared_inputs.json',result)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--receipt',type=Path,required=True);p.add_argument('--as-of',type=date.fromisoformat,default=date.today())
    p.add_argument('--data-dir',type=Path,default=LAB/'data');p.add_argument('--prepare-only',action='store_true')
    p.add_argument('--reuse-prepared',type=Path,help='Exact prepared_inputs.json from a prior attempt; no downloads or new input selection')
    a=p.parse_args()
    if a.reuse_prepared:
        inputs=json.loads(a.reuse_prepared.read_text())
        if inputs['receipt_sha256']!=sha_file(a.receipt) or inputs['as_of']!=str(a.as_of):raise ValueError('Prepared input receipt/cutoff mismatch')
    else:inputs=prepare(a.receipt,a.as_of,a.data_dir)
    if not a.prepare_only:
        from build_final_dataset import build_final
        out=build_final(LAB/inputs['accepted'],LAB/inputs['features'],LAB/inputs['political'],a.as_of,
                        a.data_dir/'final',inputs)
        print(f'FINAL DATASET: {out}',flush=True)


if __name__=='__main__':main()
