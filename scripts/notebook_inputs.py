"""Resolve and checksum the notebook's pinned baseline; no moving latest pointers."""
import json
from data_utils import LAB,digest
from audit_refresh_2026 import verified

def baseline():
    config=json.loads((LAB/'config/notebook_baseline_v1.json').read_text())
    bundles={}
    for kind,info in config.items():
        path=LAB/'data'/kind/'snapshots'/info['snapshot']
        if digest((path/'manifest.json').read_bytes())!=info['manifest_sha256']:
            raise ValueError(f'Pinned {kind} manifest changed')
        bundles[kind]=(path,verified(path))
    return bundles
