"""Cached public acquisition -> audited preparation -> newly computed forecasts.

On network failure retain verified source caches, record their dates/status,
and never label them fresh. A failed preparation never replaces a good forecast.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timezone
from pathlib import Path
from types import SimpleNamespace
import json
import shutil
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import election_lab as release
from data_utils import latest, atomic_json
from refresh_2026 import verified_receipt
from feature_download import run_source
from download_2026 import run as download_polls

PROVIDERS=['fred','michigan','ucsb','french','cboe','gpr','epu','infectious_emv']


def preparation_key(as_of, results):
    """Invalidate preparation on evidence, cutoff, policy, or data-code changes."""
    modules=['prepare_features','data_utils','build_accepted_data','official_result_reviews',
             'audit_refresh_2026','audit_survey_identity','prepare_data','normalize_data',
             'build_final_dataset','alignment_features','disruption_features',
             'build_political_context','final_pipeline','verify_final_dataset','verify_accepted_data']
    key=dict(as_of=str(as_of),sources={r['source']:r['manifest_sha256'] for r in results},
             code={n:release.sha(ROOT/'scripts'/(n+'.py')) for n in modules},
             config={p.name:release.sha(p) for p in sorted((ROOT/'config').glob('*')) if p.is_file()})
    return __import__('hashlib').sha256(json.dumps(key,sort_keys=True).encode()).hexdigest()


def cache_path(name):
    """The verified compact bundle is sufficient even on a fresh Git checkout."""
    from compact_data import HOME
    return HOME/'current'


def acquire(name, force=False, offline=False, ttl_hours=6., timeout=20):
    from compact_data import CompactDataset
    before=cache_path(name);CompactDataset(before)
    saved=json.loads((before/'sources.json').read_text())[name]
    info={k:v for k,v in saved.items() if k not in ['acquisition_status','checked_at','failure_type','failure_detail','status']}
    stamp=ROOT/'cache/acquisition'/f'{name}.json'
    meta=json.loads(stamp.read_text()) if stamp.exists() else {}
    age=float('inf')
    if meta.get('checked_at'):
        age=(datetime.now(timezone.utc)-datetime.fromisoformat(meta['checked_at'])).total_seconds()/3600
    if offline or (not force and age<ttl_hours and meta.get('manifest_sha256')==info['manifest_sha256']):
        return dict(**info,source=name,status='saved_or_unchanged',snapshot=str(before),
                    acquisition_status='offline_cache' if offline else 'fresh_check_cache',checked_at=meta.get('checked_at'))
    try:
        print('Checking source:',name,flush=True)
        raw_root=ROOT/'cache/raw'
        if name=='polls':path=download_polls(raw_root/'polls',include_generic=True,timeout=timeout)
        else:
            args=SimpleNamespace(output_dir=raw_root/'features',mode='current',year=2026,start_year=1976,
                                 refresh=False,timeout=timeout,series=None,vintage=None,document_url=[],input_file=[])
            result=run_source(name,args);path=Path(result['snapshot'])
        new=verified_receipt(path);now=datetime.now(timezone.utc).isoformat()
        # Successful checks are recorded after the compact update is committed.
        return dict(**new,source=name,status='saved_or_unchanged',raw_snapshot=str(path),
                    acquisition_status='checked_online',checked_at=now)
    except Exception as exc:
        detail=str(exc)[:1000]
        print('Using verified compact inputs for',name,':',type(exc).__name__,detail,flush=True)
        return dict(**info,source=name,status='saved_or_unchanged',snapshot=str(before),
                    acquisition_status='stale_cache_after_failure',failure_type=type(exc).__name__,failure_detail=detail,checked_at=meta.get('checked_at'))


def portable_snapshot(path):
    path=Path(path);prov=json.loads((path/'provenance.json').read_text())
    for key in ['accepted_snapshot','prepared_feature_snapshot','political_snapshot']:
        prov[key]=str(Path(prov[key]).resolve().relative_to(ROOT))
    prov['manifests']={str(Path(k).resolve().relative_to(ROOT)):v for k,v in prov['manifests'].items()}
    release.write_json(path/'provenance.json',prov)
    manifest=json.loads((path/'manifest.json').read_text())
    manifest['files']['provenance.json'].update(sha256=release.sha(path/'provenance.json'),bytes=(path/'provenance.json').stat().st_size)
    release.write_json(path/'manifest.json',manifest)
    return path


def prepare_sources(receipt_path, as_of):
    from final_pipeline import prepare
    from build_final_dataset import build_final
    inputs=prepare(receipt_path,as_of,ROOT/'data')
    out=build_final(ROOT/inputs['accepted'],ROOT/inputs['features'],ROOT/inputs['political'],as_of,ROOT/'data/final',inputs)
    return portable_snapshot(out)


def refresh_live(force=False, offline=False, ttl_hours=6., timeout=20,
                 include_student=True, strict=False, as_of=None):
    """Refresh current compact evidence; keep historical labels/calibration fixed."""
    import tempfile
    from compact_data import HOME, prepare, CompactDataset
    if ttl_hours<0 or timeout<=0:raise ValueError('Nonnegative TTL and positive timeout required')
    as_of=date.today() if as_of is None else date.fromisoformat(str(as_of))
    if as_of.year!=2026 or as_of>date.today():raise ValueError('Use a nonfuture2026 cutoff')
    current=HOME/'current';CompactDataset(current)
    lock=ROOT/'cache/.live.lock';lock.parent.mkdir(parents=True,exist_ok=True);lock.mkdir()
    report_dir=release.new_run('refresh')
    try:
        with ThreadPoolExecutor(max_workers=4) as pool:
            results=list(pool.map(lambda n:acquire(n,force,offline,ttl_hours,timeout),['polls',*PROVIDERS]))
        stale=[r['source'] for r in results if r['acquisition_status']=='stale_cache_after_failure']
        if stale and strict:raise RuntimeError('Strict refresh failed for: '+', '.join(stale))
        freshness=dict(mode='offline' if offline else 'online_with_cache',checked_on=str(date.today()),stale_sources=stale,
            sources=[{k:v for k,v in r.items() if k not in ['snapshot','raw_snapshot']} for r in results])
        with tempfile.TemporaryDirectory(dir=ROOT/'cache',prefix='compact-update-') as tmp:
            candidate=prepare(current,results,as_of,Path(tmp)/'candidate')
            old_pointer=ROOT/'cache/runs/live/latest.json'
            previous=old_pointer.read_bytes() if old_pointer.exists() else None
            try:
                forecast=release.live_forecast(candidate,include_student=include_student,freshness=freshness)
                # Freeze this run's small inputs locally for cutoff replay. Git
                # retains only current/frozen compact inputs, never this cache.
                replay=ROOT/'cache/run_inputs'/release.sha(candidate/'manifest.json')
                replay.parent.mkdir(parents=True,exist_ok=True)
                if not replay.exists():shutil.copytree(candidate,replay)
                metadata=json.loads((forecast/'run.json').read_text())
                metadata['dataset']=str(replay.relative_to(ROOT))
                release.finish(forecast,metadata,publish=False)
                backup=Path(tmp)/'previous'
                current.rename(backup)
                try:
                    candidate.rename(current)
                    release.publish_run(forecast)
                except BaseException:
                    if current.exists():shutil.rmtree(current)
                    backup.rename(current);raise
            except BaseException:
                if previous is not None:old_pointer.write_bytes(previous)
                elif old_pointer.exists():old_pointer.unlink()
                raise
        for r in results:
            if r['acquisition_status']=='checked_online':
                release.write_json(ROOT/'cache/acquisition'/f"{r['source']}.json",
                    dict(checked_at=r['checked_at'],manifest_sha256=r['manifest_sha256']))
        release.finish(report_dir,dict(status='complete_with_stale_sources' if stale else 'complete',
            forecast=str(forecast.relative_to(ROOT)),freshness=freshness))
        return forecast
    except Exception as exc:
        release.write_json(report_dir/'failure.json',dict(status='failed',exception_type=type(exc).__name__,
            message=str(exc),previous_forecast_preserved=True))
        raise
    finally:lock.rmdir()
