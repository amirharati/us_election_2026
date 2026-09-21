"""Small read-only interface to the final bundle and its complete pinned source catalog."""
import json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from data_utils import LAB
from alignment_features import sha


def resolve_snapshot(root=LAB/'data/final'):
    root=Path(root).resolve()
    p=(root/json.loads((root/'latest.json').read_text())['snapshot']).resolve()
    if not p.is_relative_to(root/'snapshots'):raise ValueError('Invalid final dataset pointer')
    return p


def load_table(name='poll_inputs_reference',snapshot=None):
    p=Path(snapshot) if snapshot is not None else resolve_snapshot()
    relative=f'tables/{name}.parquet';manifest=json.loads((p/'manifest.json').read_text())
    if relative not in manifest['files']:raise KeyError(name)
    if sha(p/relative)!=manifest['files'][relative]['sha256']:raise ValueError('Table checksum mismatch')
    return pd.read_parquet(p/relative)


def load_feature_source(name,snapshot=None):
    """Access optional native source tables; these are not automatically model predictors."""
    p=Path(snapshot) if snapshot is not None else resolve_snapshot()
    prov=json.loads((p/'provenance.json').read_text());source=LAB/Path(prov['prepared_feature_snapshot'])
    if sha(source/'manifest.json')!=prov['manifests'].get(prov['prepared_feature_snapshot'], prov['manifests'].get(str(source.resolve()))):raise ValueError('Feature manifest changed')
    relative=prov['feature_source_catalog'][name]['path'];manifest=json.loads((source/'manifest.json').read_text())
    if sha(source/relative)!=manifest['files'][relative]['sha256']:raise ValueError('Feature source checksum mismatch')
    return pd.read_csv(source/relative,low_memory=False)


class FinalDataset:
    """A verified snapshot pinned for the lifetime of one analysis/evaluation."""

    def __init__(self, snapshot):
        from verify_final_dataset import verify
        self.snapshot = Path(snapshot).resolve()
        self.manifest_sha256 = sha(self.snapshot/'manifest.json')
        self.checks = verify(self.snapshot)
        self._check_pin()
        self.manifest = json.loads((self.snapshot/'manifest.json').read_text())
        if self.manifest.get('kind') != 'final_aligned_election_dataset':
            raise ValueError('Not a final election dataset')
        self.policy = json.loads((self.snapshot/'policy.json').read_text())
        self.summary = json.loads((self.snapshot/'summary.json').read_text())
        self.provenance = json.loads((self.snapshot/'provenance.json').read_text())
        if self.policy['version'] != 'final-alignment-v1':
            raise ValueError('Unsupported alignment contract; review the new schema')

    def _check_pin(self):
        if sha(self.snapshot/'manifest.json') != self.manifest_sha256:
            raise ValueError('Pinned dataset manifest changed')

    def load_table(self, name):
        self._check_pin()
        return load_table(name, self.snapshot)

    def load_feature_source(self, name):
        self._check_pin()
        return load_feature_source(name, self.snapshot)

    def metadata(self):
        self._check_pin()
        return dict(
            snapshot=str(self.snapshot), snapshot_id=self.snapshot.name,
            manifest_sha256=self.manifest_sha256,
            manifest_schema_version=self.manifest['schema_version'],
            alignment_version=self.policy['version'], as_of=self.policy['as_of'],
            built_at=self.manifest['retrieved_at'],
            historical_horizon_days=self.policy['historical_horizon_days'],
            source_manifests=self.provenance['manifests'],
            refresh=self.provenance.get('run', {}),
            status=self.summary['status'],
            seat_forecast_ready=self.summary['seat_forecast_ready'],
            restrictions=self.policy['not_forecast_ready_reasons'],
            file_hashes={k:v['sha256'] for k,v in self.manifest['files'].items()},
        )

    def write_run_metadata(self, path, *, feature_view, tables, run_config):
        """Record inputs alongside later results; never overwrite another run record.

        run_config is caller-supplied model/features/splits/seed/code version etc.
        This records dataset provenance; it does not fit or evaluate a model.
        """
        if feature_view not in {'reference', 'observed'}:
            raise ValueError('Choose reference or observed explicitly')
        if not tables:
            raise ValueError('Record at least one input table')
        for name in tables:
            if f'tables/{name}.parquet' not in self.manifest['files']:
                raise KeyError(name)
            if name.endswith(('_reference', '_observed')) and not name.endswith('_'+feature_view):
                raise ValueError('Input table conflicts with recorded feature view')
        record=dict(record_version=1, recorded_at=datetime.now(timezone.utc).isoformat(),
                    dataset=self.metadata(), feature_view=feature_view,
                    tables=list(tables), run_config=run_config)
        encoded=json.dumps(record, indent=2, allow_nan=False)+'\n'
        path=Path(path);path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('x') as f:f.write(encoded)
        return path


def open_dataset(snapshot=None, *, root=LAB/'data/final'):
    """Resolve latest once (or use an explicit historical snapshot), then verify."""
    path = Path(snapshot) if snapshot is not None else resolve_snapshot(root)
    if json.loads((path/'manifest.json').read_text()).get('kind') == 'compact_model_inputs':
        from compact_data import CompactDataset
        return CompactDataset(path)
    return FinalDataset(path)


def open_run_dataset(path):
    """Replay a saved run's dataset without following today's latest pointer."""
    record=json.loads(Path(path).read_text())
    if record.get('record_version') != 1:raise ValueError('Unsupported run record')
    pin=record['dataset'];snapshot=Path(pin['snapshot'])
    if sha(snapshot/'manifest.json') != pin['manifest_sha256']:
        raise ValueError('Run dataset checksum mismatch')
    return open_dataset(snapshot)
