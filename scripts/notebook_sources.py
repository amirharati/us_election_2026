"""Preserve notebook revisions and explicitly restore or accept managed sources."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import os
import tempfile
import nbformat

ROOT = Path(__file__).resolve().parents[1]


def sources(notebook):
    return [dict(cell_type=c.cell_type, source=c.source) for c in notebook.cells]


def source_path(path):
    return path.parent / 'sources' / (path.stem + '.json')


def snapshot(path, data, phase):
    directory = path.parent.parent / 'cache/notebook_history' / path.stem
    directory.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    target = directory / f'{stamp}-{phase}.ipynb'
    target.write_bytes(data)
    return target


def atomic_write(path, data):
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.'+path.name)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
        os.replace(name, path)
    finally:
        if os.path.exists(name): os.unlink(name)


def check_source(path, notebook):
    canonical = source_path(path)
    if canonical.exists() and sources(notebook) != json.loads(canonical.read_text()):
        raise ValueError(f'Notebook source differs from its recovery source: {path.name}. '
                         f'Save/review editor changes first. Use scripts/notebook_sources.py '
                         f'--restore {path.name[:2]} to recover, or --accept-current {path.name[:2]} '
                         'only if these source edits are intentional.')


def save_execution(path, notebook, original):
    data = nbformat.writes(notebook).encode()
    recovery = snapshot(path, data, 'executed')
    if not path.exists() or path.read_bytes() != original:
        raise RuntimeError(f'Notebook changed during execution; disk edits preserved. Executed copy: {recovery}')
    atomic_write(path, data)
    return recovery


def manage(path, restore=False):
    original = path.read_bytes()
    notebook = nbformat.reads(original.decode(), as_version=4)
    backup = snapshot(path, original, 'before-restore' if restore else 'accepted')
    canonical = source_path(path)
    if restore:
        cells = json.loads(canonical.read_text())
        notebook.cells = [nbformat.v4.new_code_cell(c['source']) if c['cell_type']=='code'
                          else nbformat.v4.new_markdown_cell(c['source']) for c in cells]
        atomic_write(path, nbformat.writes(notebook).encode())
    else:
        canonical.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(canonical, (json.dumps(sources(notebook), indent=2)+'\n').encode())
    return backup


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--restore', metavar='NUMBER')
    group.add_argument('--accept-current', metavar='NUMBER')
    args = parser.parse_args()
    number = int(args.restore or args.accept_current)
    matches = list((ROOT/'notebooks').glob(f'{number:02d}_*.ipynb'))
    if len(matches) != 1: parser.error('Expected exactly one matching notebook')
    print('Preserved previous copy:', manage(matches[0], restore=args.restore is not None))
