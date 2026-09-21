#!/usr/bin/env python3
"""Refresh 2026 polls/features and rebuild the verified final aligned dataset.

Use --download-only for acquisition alone. Frozen notebook inputs are never changed.
"""
import argparse
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
from types import SimpleNamespace

from data_utils import LAB, atomic_json, digest, utc_now
from download_2026 import run as download_polls
from feature_download import run_source
from feature_sources import SOURCES

DEFAULT_SOURCES = tuple(n for n, spec in SOURCES.items()
                        if spec['access'] == 'public' and n != 'bea')


def verified_receipt(path):
    path = Path(path).resolve()
    raw = (path / 'manifest.json').read_bytes()
    manifest = json.loads(raw)
    for name, info in manifest['files'].items():
        artifact = (path / name).resolve()
        if not artifact.is_relative_to(path) or digest(artifact.read_bytes()) != info['sha256']:
            raise ValueError(f'Invalid artifact or checksum: {name}')
    summary = json.loads((path / 'summary.json').read_text())
    freshness = {name: {k: info[k] for k in
                 ['first_source_date', 'last_source_date', 'selected_rows', 'freshness'] if k in info}
                 for name, info in summary.get('artifacts', {}).items()}
    return dict(snapshot=str(path), manifest_sha256=digest(raw),
                verified_files=len(manifest['files']), freshness=freshness,
                poll_latest_dates={k: summary[k] for k in
                    ['latest_poll_end', 'generic_latest_poll_end'] if k in summary})


def refresh(data_dir, sources=DEFAULT_SOURCES, timeout=45):
    """Continue independent sources after failures; never promote a partial receipt."""
    sources = list(dict.fromkeys(sources))
    if not sources or any(s not in DEFAULT_SOURCES for s in sources) or timeout <= 0:
        raise ValueError('Choose public sources and a positive timeout')
    data_dir = Path(data_dir).resolve()
    root = data_dir / 'refresh_2026'
    root.mkdir(parents=True, exist_ok=True)
    lock = root / '.refresh.lock'
    lock.mkdir()  # Refuse concurrent orchestration; do not remove another run's lock.
    try:
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
        reports = root / 'runs'
        reports.mkdir(exist_ok=True)
        report_path = reports / (stamp + '.json')
        report = dict(started_at=utc_now(), year=2026, sources=sources, results=[],
                      status='running', acquisition_only=True, aligned=False,
                      preparation_rebuilt=False, model_ready=False)
        atomic_json(report_path, report)
        args = SimpleNamespace(output_dir=data_dir / 'features', mode='current', year=2026,
                               start_year=1976, refresh=False, timeout=timeout, series=None,
                               vintage=None, document_url=[], input_file=[])
        for name in ['polls', *sources]:
            print(f'Refreshing {name}', flush=True)
            try:
                if name == 'polls':
                    path = download_polls(data_dir / '2026', include_generic=True, timeout=timeout)
                    result = dict(source=name, status='saved_or_unchanged', **verified_receipt(path))
                else:
                    result = run_source(name, args)
                    if result['status'] in {'saved_or_unchanged', 'cached'}:
                        result.update(verified_receipt(result['snapshot']))
                    elif result['status'] != 'historical_only':
                        raise ValueError(f"Unexpected acquisition status: {result['status']}")
            except Exception as exc:
                message = str(exc)
                if os.environ.get('FRED_API_KEY'):
                    message = message.replace(os.environ['FRED_API_KEY'], 'REDACTED')
                result = dict(source=name, status='failed', reason=message)
                print(f'Failed: {name}: {message}', flush=True)
            report['results'].append(result)
            atomic_json(report_path, report)
        failed = any(r['status'] == 'failed' for r in report['results'])
        report.update(finished_at=utc_now(), status='partial_failure' if failed else 'acquisition_complete')
        atomic_json(report_path, report)
        if not failed:
            atomic_json(root / 'latest_successful.json', dict(report=str(report_path.relative_to(root)),
                        report_sha256=digest(report_path.read_bytes()), sources=sources,
                        scope='requested acquisition sources only; not prepared/aligned data'))
        print(f"{report['status']}: {report_path}", flush=True)
        return report_path, report
    finally:
        lock.rmdir()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=LAB / 'data')
    parser.add_argument('--sources', nargs='+', choices=DEFAULT_SOURCES, default=list(DEFAULT_SOURCES))
    parser.add_argument('--timeout', type=float, default=45)
    parser.add_argument('--dry-run', action='store_true', help='Show the plan without network or file changes')
    parser.add_argument('--download-only', action='store_true', help='Stop after acquisition; do not rebuild the final dataset')
    parser.add_argument('--from-receipt', type=Path, help='Rebuild from an exact successful acquisition receipt without re-downloading')
    parser.add_argument('--as-of', type=date.fromisoformat, default=date.today())
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    if args.as_of > date.today():
        parser.error('--as-of cannot be in the future')
    if not args.download_only and not args.data_dir.resolve().is_relative_to(LAB):
        parser.error('Final dataset output must be inside this lab; use --download-only for external raw collections')
    if args.dry_run:
        print(json.dumps(dict(year=2026, polls=['Senate', 'national generic ballot'],
              features=args.sources, data_dir=str(args.data_dir.resolve()),
              acquisition_only=args.download_only, rebuild_preparation=not args.download_only,
              build_final_dataset=not args.download_only, from_receipt=str(args.from_receipt) if args.from_receipt else None,
              as_of=str(args.as_of), pinned_notebooks_unchanged=True), indent=2))
        return 0
    try:
        if args.from_receipt:
            receipt_path=args.from_receipt
            report=json.loads(receipt_path.read_text())
        else:
            receipt_path, report = refresh(args.data_dir, args.sources, args.timeout)
        if report['status'] != 'acquisition_complete':
            return 1
        if not args.download_only:
            # Import lazily: download-only/dry-run still use only the standard library.
            from final_pipeline import prepare
            from build_final_dataset import build_final
            print('Preparing and aligning the verified refresh receipt...',flush=True)
            inputs=prepare(receipt_path,args.as_of,args.data_dir)
            out=build_final(LAB/inputs['accepted'],LAB/inputs['features'],LAB/inputs['political'],
                            args.as_of,args.data_dir/'final',inputs)
            print(f'FINAL DATASET: {out}',flush=True)
        return 0
    except Exception as exc:
        parser.exit(1, f'Refresh could not complete: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
