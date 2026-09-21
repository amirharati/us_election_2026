"""Compact input integrity, current revisions, and independence from raw history."""
from pathlib import Path
from datetime import date
import json
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab as lab
from compact_data import CompactDataset, HOME, poll_update, prepare
from alignment_features import FeatureStore
import release_refresh as refresh


class CompactTests(unittest.TestCase):
    def test_monthly_materialization_preserves_feature_values(self):
        data=CompactDataset(HOME/'current')
        records=pd.read_parquet(data.snapshot/'feature_records.parquet')
        political=json.loads((data.snapshot/'political.json').read_text())
        rebuilt=FeatureStore.from_records(records,political,data.policy['as_of'])
        saved=data.feature_store()
        for cutoff in ['2026-01-01','2026-06-30',data.policy['as_of']]:
            for a,b in zip(rebuilt.at(cutoff),saved.at(cutoff)):
                pd.testing.assert_series_equal(pd.Series(a),pd.Series(b))

    def test_corrupt_compact_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'inputs';shutil.copytree(HOME/'frozen',out)
            with (out/'tables/labels.parquet').open('ab') as f:f.write(b'corrupt')
            with self.assertRaisesRegex(ValueError,'checksum'):CompactDataset(out)

    def test_poll_removal_replaces_current_feed_and_retains_history(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);out=root/'inputs';shutil.copytree(HOME/'current',out)
            raw=root/'raw';(raw/'tables').mkdir(parents=True);(raw/'raw').mkdir();(raw/'config').mkdir()
            shutil.copyfile(out/'feeds/contests_2026.csv',raw/'config/contests_2026.csv')
            senate=pd.read_parquet(out/'feeds/senate.parquet')
            removed=senate.poll_id.iloc[0]
            senate=senate[senate.poll_id.ne(removed)]
            senate.to_csv(raw/'tables/senate_general_answers.csv',index=False)
            pd.read_parquet(out/'feeds/generic_ballot.parquet').to_csv(raw/'raw/silver_bulletin_generic.csv',index=False)
            before=pd.read_parquet(out/'tables/polls.parquet')
            when=date.fromisoformat(json.loads((out/'policy.json').read_text())['as_of'])
            changes=poll_update(out,dict(manifest_sha256='a'*64,raw_snapshot=str(raw)),when)
            after=pd.read_parquet(out/'tables/polls.parquet')
            self.assertIn(removed,changes['senate']['removed_poll_ids'])
            self.assertFalse(after.loc[after.cycle.eq(2026)&after.dataset.eq('senate'),'source_poll_id'].astype(str).eq(removed).any())
            pd.testing.assert_frame_equal(before[before.cycle.lt(2026)].reset_index(drop=True),after[after.cycle.lt(2026)].reset_index(drop=True))

    def test_feature_revision_replaces_current_series_without_changing_history(self):
        from compact_data import feature_update
        from alignment_features import sha
        with tempfile.TemporaryDirectory(dir=lab.ROOT/'cache') as temp:
            root=Path(temp);out=root/'inputs';shutil.copytree(HOME/'current',out)
            raw=root/'raw_bundle';(raw/'raw').mkdir(parents=True)
            source=raw/'raw/vix_daily.csv'
            source.write_text('DATE,OPEN,HIGH,LOW,CLOSE\n2026-07-01,20,22,18,21\n2026-08-01,30,32,28,31\n')
            (raw/'manifest.json').write_text(json.dumps(dict(retrieved_at='2026-09-20T12:00:00+00:00',
                files={'raw/vix_daily.csv':dict(sha256=sha(source))})))
            before=pd.read_parquet(out/'feature_records.parquet')
            feature_update(out,[dict(source='cboe',manifest_sha256='f'*64,raw_snapshot=str(raw))])
            after=pd.read_parquet(out/'feature_records.parquet')
            changed=after[after.source.eq('cboe')&after.scope.eq('current')]
            self.assertEqual(changed._value.tolist(),[21.,31.])
            pd.testing.assert_frame_equal(before[before.scope.eq('historical')].reset_index(drop=True),
                                          after[after.scope.eq('historical')].reset_index(drop=True))

    def test_failed_inference_does_not_promote_current_inputs(self):
        before=lab.sha(HOME/'current/manifest.json')
        pointer=lab.ROOT/'cache/runs/live/latest.json';old=pointer.read_bytes() if pointer.exists() else None
        with patch.object(lab,'live_forecast',side_effect=RuntimeError('test inference failure')):
            with self.assertRaisesRegex(RuntimeError,'test inference failure'):
                refresh.refresh_live(offline=True,include_student=False)
        self.assertEqual(before,lab.sha(HOME/'current/manifest.json'))
        self.assertEqual(old,pointer.read_bytes() if pointer.exists() else None)

    def test_fixed_history_is_present_without_raw_archives(self):
        data=CompactDataset(lab.FROZEN)
        labels=data.load_table('labels')
        self.assertTrue(labels.loc[labels.cycle.lt(2026),'dem_rep_margin'].notna().any())
        self.assertTrue(lab.FROZEN.is_relative_to(HOME))
        self.assertFalse(any(k.startswith('data/') and not k.startswith('data/compact/')
                             for k in json.loads((lab.ROOT/'PACKAGE_MANIFEST.json').read_text())))


if __name__=='__main__':unittest.main()
