"""Release checks: portable sources, chronology, reproduction and missing labels."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import election_lab as lab


def audit():
    checks={}
    # Package hashes cover immutable sources/snapshots. Download check receipts,
    # preparation scratch files and notebook outputs change during ordinary use;
    # notebook code/markdown are verified separately below.
    path=lab.ROOT/'PACKAGE_MANIFEST.json'
    if path.exists():
        for rel,expected in json.loads(path.read_text()).items():
            p=(lab.ROOT/rel).resolve()
            if not p.is_relative_to(lab.ROOT) or lab.sha(p)!=expected:raise ValueError('Package checksum failed: '+rel)
        checks['package_files_verified']=True
    notebook_index=lab.ROOT/'NOTEBOOK_SOURCES.json'
    if notebook_index.exists():
        import hashlib
        for rel,expected in json.loads(notebook_index.read_text()).items():
            notebook=json.loads((lab.ROOT/rel).read_text())
            cells=[dict(cell_type=c['cell_type'],source=''.join(c['source'])) for c in notebook['cells']]
            actual=hashlib.sha256(json.dumps(cells,sort_keys=True).encode()).hexdigest()
            if actual!=expected:raise ValueError('Notebook source changed: '+rel)
        checks['notebook_sources_verified']=True
    from load_final_dataset import open_dataset
    data=open_dataset(lab.FROZEN)
    current=open_dataset(lab.ROOT/'data/compact/current')
    checks['compact_current_inputs_verified']=bool(current.checks)
    checks['portable_frozen_dataset_verified']=True
    folds=pd.read_parquet(lab.ASSETS/'main/folds.parquet')
    for r in folds.itertuples():
        fit=np.load(lab.ASSETS/'main'/r.fit_path)
        assert fit['years'].max()<r.cycle
        lab.verify_selection(r.scenario,int(r.cycle))
    checks['all_15_chronological_model_selections']=True
    root=lab.ROOT/'outputs/reproduction'
    if (root/'latest.json').exists():
        run=lab.latest_run('reproduction');p=pd.read_parquet(run/'predictions.parquet');s=pd.read_parquet(run/'seats.parquet')
        reference=pd.read_parquet(lab.ASSETS/'reference_blends/predictions.parquet')
        common=set(p.model)&set(reference.model)
        for name in common:
            a=p[p.model.eq(name)].merge(reference[reference.model.eq(name)],on=['scenario','cycle','target_id'],validate='one_to_one',suffixes=('','_ref'))
            assert len(a)==431
            for col in ['margin_pp','p_dem','width70_pp']:np.testing.assert_allclose(a[col],a[col+'_ref'],atol=1e-9,equal_nan=True)
        assert p[p.cycle.eq(2026)].actual_pp.isna().all()
        assert not p.duplicated(['scenario','cycle','target_id','model']).any()
        assert (s.point_D+s.point_R).eq(100).all()
        checks['frozen_research_comparisons_reproduced']=True
    return checks
