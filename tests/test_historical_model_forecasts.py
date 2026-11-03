import sys
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
import election_lab as lab
from historical_model_forecasts import prepare

class HistoricalInferenceTest(unittest.TestCase):
    def test_cutoff_screening_and_earlier_training(self):
        q,fit,fold,cal,targets,waves,audit,actual,ledger=prepare('2022-09-05')
        eligible=audit[audit.cycle.eq(2022)&audit.baseline_status.eq('eligible')]
        self.assertTrue(eligible.field_end.le(pd.Timestamp('2022-09-05')).all())
        self.assertTrue(eligible.release.dropna().le(pd.Timestamp('2022-09-05')).all())
        self.assertLess(fit['years'].max(),2022)
        self.assertTrue(q.actual.isna().all());self.assertTrue(targets.actual.isna().all())
        self.assertEqual(set(q.as_of),{'2022-09-05'})
        self.assertEqual(set(cal.loc[cal.cycle.eq(2022),'context_id']),{'2022-09-05'})

    def test_original_cutoff_reproduces_and_new_date_changes_evidence(self):
        q,fit,fold,*_=prepare('2022-09-17')
        p,_,_=lab.signed.predict(q,fit,lab.load_poll('matched_live',2022),fit['loading'],fold.lambda_value)
        saved=pd.read_parquet(lab.ASSETS/'main/predictions.parquet').query('scenario=="matched_live" and cycle==2022').sort_values('target_id')
        np.testing.assert_allclose(p.prediction_pp,saved.prediction_pp,atol=1e-10)
        earlier,*_=prepare('2022-06-01')
        self.assertLess(earlier.sample_count.sum(),q.sample_count.sum())

    def test_november_features_are_not_clamped_to_october(self):
        q,fit,fold,cal,*_=prepare('2024-11-03')
        self.assertEqual(set(cal.loc[cal.cycle.eq(2024),'context_id']),{'2024-11-03'})
        self.assertTrue(q.as_of.eq('2024-11-03').all())
