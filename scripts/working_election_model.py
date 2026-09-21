"""Load the explicitly designated working model from verified saved forecasts.

This does not fit, refresh data, or silently change model selection.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import simple_bayesian_polling as provenance


def load(lab):
    lab=Path(lab).resolve()
    metadata=json.loads((lab/'WORKING_MODEL.json').read_text())
    source=(lab/metadata['source_artifact']).resolve()
    if not source.is_relative_to(lab/'reports'):
        raise ValueError('Working forecast source must be inside lab reports')
    if provenance.verify(source)!=metadata['source_manifest_sha256']:
        raise ValueError('Working forecast manifest does not match designation')
    model=metadata['model_id']
    tables={name:pd.read_parquet(source/(name+'.parquet')) for name in
            ['predictions','seats','folds','summary','chamber_summary']}
    for name,table in tables.items():
        tables[name]=table[table.model.eq(model)].copy()
        if tables[name].empty:raise ValueError('Missing designated model in '+name)
    p,f,seats=tables['predictions'],tables['folds'],tables['seats']
    if not f.U_variance.eq(0).all() or not f.K_multiplier.eq(metadata['K_multiplier']).all():
        raise ValueError('Saved forecasts do not match designated settings')
    if p.duplicated(['scenario','target_id']).any():raise ValueError('Duplicate working forecasts')
    current=p[p.cycle.eq(metadata['current_cycle'])]
    if current.empty or current.actual.notna().any():raise ValueError('Invalid current forecast labels')
    for row in f.itertuples():
        q=p[p.scenario.eq(row.scenario)&p.cycle.eq(row.cycle)]
        ss=seats[seats.scenario.eq(row.scenario)&seats.cycle.eq(row.cycle)].iloc[0]
        if not np.isclose(ss.expected_D_exact,ss.fixed_D+q.p_dem.sum()):
            raise ValueError('Working chamber accounting mismatch')
    return metadata,source,tables
