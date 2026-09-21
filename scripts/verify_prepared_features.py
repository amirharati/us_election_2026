"""Independent offline checks on a prepared feature snapshot; no downloads or joins."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
from datetime import date
from decimal import Decimal
import hashlib
import json
import math
from pathlib import Path
import sqlite3
import tempfile
from data_utils import LAB


def hash_file(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def verify(root):
    path=root/json.loads((root/'latest.json').read_text())['snapshot']
    if not path.resolve().is_relative_to(root.resolve()/'snapshots'):raise ValueError('Invalid pointer')
    manifest=json.loads((path/'manifest.json').read_text())
    for name,info in manifest['files'].items():
        p=path/name
        if p.stat().st_size!=info['bytes'] or hash_file(p)!=info['sha256']:raise ValueError(f'Output checksum: {name}')
    inputs=json.loads((path/'inputs.json').read_text());artifacts={a['id']:a for a in inputs['artifacts']}
    for a in artifacts.values():
        if hash_file(LAB/a['path'])!=a['sha256']:raise ValueError(f'Input checksum: {a["path"]}')
    catalog=json.loads((path/'catalog.json').read_text());counts=Counter();flags=Counter()
    with tempfile.TemporaryDirectory(prefix='verify-feature-') as temp:
        db=sqlite3.connect(Path(temp)/'ids.sqlite');db.execute('CREATE TABLE ids (id TEXT PRIMARY KEY)')
        for name,entry in catalog.items():
            n=0;first='';last='';source=name.split('/')[0]
            numeric={k for k,v in entry.get('source_columns',{}).items() if v['type']=='number'}
            with (path/entry['path']).open(newline='') as f:
                reader=csv.DictReader(f)
                expected=['record_id','logical_key','artifact_id','source_row',*entry['columns']]
                if reader.fieldnames!=expected:raise ValueError(f'Schema: {name}')
                for r in reader:
                    if None in r or any(v is None for v in r.values()):raise ValueError(f'CSV width: {name}')
                    n+=1;db.execute('INSERT INTO ids VALUES (?)',(r['record_id'],))
                    if artifacts[r['artifact_id']]['source']!=source:raise ValueError('Wrong provenance source')
                    if not r['source_row']:raise ValueError('Missing original row locator')
                    if r.get('available_at',''):raise ValueError('Unexpected inferred availability date')
                    for a,z in [('period_start','period_end'),('start_date','end_date'),('date_start','date_end')]:
                        if a in r:
                            lo,hi=date.fromisoformat(r[a]),date.fromisoformat(r[z])
                            if lo>hi:raise ValueError(f'Reversed interval: {name}')
                    for k in numeric|({'value'} if 'value' in r else set()):
                        if r[k] and not math.isfinite(float(r[k])):raise ValueError(f'Nonfinite: {name}/{k}')
                    if 'value_status' in r:
                        if (r['value_status']=='observed') != bool(r['value']):raise ValueError(f'Missingness: {name}')
                        if r['value']:
                            original=Decimal(r['source_value'].strip().rstrip('%').replace(',','').replace('−','-'))
                            if r.get('source_unit') in ('percent','percent_return') or source=='ucsb':original/=100
                            if abs(float(original)-float(r['value']))>1e-9*max(1,abs(float(original))):
                                raise ValueError(f'Unit conversion: {name}/{r["record_id"]}')
                    for flag in r.get('quality_flags','').split('|'):
                        if flag:flags[source+':'+flag]+=1
                    if source=='silver_bulletin' and r['subgroup'] in ('Strong','Weak') and (r['subgroup_type']!='intensity' or r['respondent_party']):
                        raise ValueError('Approval intensity mislabeled as party')
                    if source=='policy_agendas' and r['value'] and not 0<=float(r['value'])<=1:raise ValueError('MIP proportion scale')
                    if source=='michigan' and r['averaging_basis']=='three_month_moving_average' and not r['publisher_window_start']:
                        raise ValueError('Missing publisher averaging window')
                    d=r.get('date',r.get('period_end',r.get('end_date',r.get('date_end',''))))
                    if d:first=min(first or d,d);last=max(last,d)
            if (n,first,last)!=(entry['rows'],entry['first_date'],entry['last_date']):raise ValueError(f'Catalog mismatch: {name}')
            counts[source]+=n
        dup=path/'audit/duplicate_rows.jsonl'
        if dup.exists():
            for line in dup.open():
                r=json.loads(line)
                if not db.execute('SELECT 1 FROM ids WHERE id=?',(r['canonical_record_id'],)).fetchone():raise ValueError('Dangling duplicate')
        variants=path/'audit/overlapping_variants.jsonl';ngroups=0
        if variants.exists():
            for line in variants.open():
                r=json.loads(line);ngroups+=1
                for rid in r['record_ids']:
                    if not db.execute('SELECT 1 FROM ids WHERE id=?',(rid,)).fetchone():raise ValueError('Dangling variant')
        db.close()
    summary=json.loads((path/'summary.json').read_text())
    if sum(counts.values())!=summary['rows'] or ngroups!=summary['overlapping_variant_groups']:raise ValueError('Summary mismatch')
    return dict(snapshot=str(path.relative_to(LAB)),tables=len(catalog),rows=sum(counts.values()),source_rows=dict(counts),
                quality_flags=dict(flags),overlapping_variant_groups=ngroups,checks_passed=True,
                meaning='Structure, provenance, conversion and internal consistency checked; source flags/review restrictions remain.')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=LAB/'data/features_prepared')
    print(json.dumps(verify(ap.parse_args().root),indent=2))
