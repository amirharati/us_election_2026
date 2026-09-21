"""Chronology and cache invalidation checks for retrospective cutoff reports."""
from pathlib import Path
import sys
import unittest
import numpy as np
import pandas as pd

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab as lab
from live_forecast_report import cutoff_schedule, _evidence_hash


class CutoffHistoryTests(unittest.TestCase):
    def test_schedule_includes_endpoint_and_recent_days_without_duplicates(self):
        dates=cutoff_schedule('2026-01-01','2026-01-10',every_days=3,last_days=3)
        self.assertEqual([d.day for d in dates],[1,4,7,8,9,10])
        self.assertEqual(len(cutoff_schedule('2026-01-01','2026-01-01')),1)
        with self.assertRaises(ValueError):cutoff_schedule('2026-01-01','2026-01-10',0)
        with self.assertRaises(ValueError):cutoff_schedule('2026-01-10','2026-01-01')

    def test_cache_tracks_evidence_and_models_not_row_order(self):
        frame=pd.DataFrame({'state':['A','B'],'value':[1.,2.]})
        evidence=dict(q=frame,targets=frame,cal=frame,feature_mode='dated',
            waves=pd.DataFrame({'target_id':['A','B'],'margin':[.1,.2],
                                'age_days':[2,5],'firm':['X','Y']}))
        key=_evidence_hash(evidence,'model-v1',True,[.2])
        shuffled={k:(v.iloc[::-1] if isinstance(v,pd.DataFrame) else v) for k,v in evidence.items()}
        self.assertEqual(key,_evidence_hash(shuffled,'model-v1',True,[.2]))
        self.assertNotEqual(key,_evidence_hash(evidence,'model-v2',True,[.2]))
        modified={**evidence,'waves':evidence['waves'].assign(age_days=[3,6])}
        self.assertNotEqual(key,_evidence_hash(modified,'model-v1',True,[.2]))

    def test_january_inputs_exclude_future_poll_dates_and_feature_periods(self):
        evidence=lab.prepare_live_evidence(lab.FROZEN,'2026-01-01')
        cutoff=pd.Timestamp('2026-01-01')
        waves=evidence['waves'];waves=waves[waves.target_id.isin(evidence['q'].target_id)]
        self.assertTrue(pd.to_datetime(waves.field_end).le(cutoff).all())
        audit=evidence['poll_audit'];admitted=audit[audit.cycle.eq(2026)&audit.baseline_status.eq('eligible')]
        self.assertTrue(pd.to_datetime(admitted.release).dropna().le(cutoff).all())
        ledger=evidence['feature_ledger'];current=ledger[ledger.context_id.eq('2026-01-01')]
        self.assertTrue(pd.to_datetime(current.reference_end).dropna().le(cutoff).all())
        self.assertTrue(evidence['fit']['years'].max()<2026)
        self.assertEqual(evidence['current_context'].context_id.iloc[0],'2026-01-01')


if __name__=='__main__':unittest.main()
