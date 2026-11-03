import sys
from pathlib import Path
import unittest
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from polymarket_longshot_paths import trace_path,analyze

class LongshotPathTest(unittest.TestCase):
    def prices(self,values):
        return pd.DataFrame([dict(market_id='1',timestamp=pd.Timestamp(t,tz='UTC'),price_first=p,price_source='Test') for t,p in values])

    def test_target_not_peak_and_strict_future_before_deadline(self):
        h=self.prices([('2024-09-05',.8),('2024-09-06',.05),('2024-09-07',.15),('2024-09-08',.11),('2024-11-03',.9)])
        r=trace_path(h,pd.Timestamp('2024-09-06',tz='UTC'),.05,True,pd.Timestamp('2024-11-03',tz='UTC'))
        self.assertEqual(r['exit_price'],.10);self.assertEqual(r['max_price'],.15)
        self.assertTrue(r['observed_double']);self.assertTrue(r['confirmed_double'])
        self.assertEqual(r['days_to_double'],1)

    def test_timeout_loss_and_stale_deadline(self):
        h=self.prices([('2024-09-07',.06),('2024-11-02',.02)])
        r=trace_path(h,pd.Timestamp('2024-09-06',tz='UTC'),.05,True,pd.Timestamp('2024-11-03',tz='UTC'))
        self.assertAlmostEqual(r['gross_change'],-.03);self.assertFalse(r['observed_double'])
        r=trace_path(h.iloc[:1],pd.Timestamp('2024-09-06',tz='UTC'),.05,True,pd.Timestamp('2024-11-03',tz='UTC'))
        self.assertFalse(r['complete']);self.assertTrue(pd.isna(r['gross_change']))

    def test_complement_and_isolated_spike(self):
        h=self.prices([('2024-09-07',.8),('2024-09-08',.99),('2024-11-02',.99)])
        r=trace_path(h,pd.Timestamp('2024-09-06',tz='UTC'),.05,False,pd.Timestamp('2024-11-03',tz='UTC'))
        self.assertTrue(r['observed_double']);self.assertFalse(r['confirmed_double'])
        self.assertAlmostEqual(r['exit_price'],.10)

    def test_invalid_pool_prevents_claimed_exit(self):
        h=self.prices([('2024-09-07',float('nan')),('2024-09-08',.15)])
        r=trace_path(h,pd.Timestamp('2024-09-06',tz='UTC'),.05,True,pd.Timestamp('2024-11-03',tz='UTC'))
        self.assertFalse(r['complete']);self.assertTrue(pd.isna(r['exit_price']))

    def test_signal_uses_fresh_entry_and_no_outcome_selection(self):
        samples=pd.DataFrame([dict(cycle=2024,state='AA',market_id='1',model=m,check_date=pd.Timestamp('2024-09-05',tz='UTC'),model_date=pd.Timestamp('2024-09-05',tz='UTC'),model_probability=p) for m,p in [('GB',.09),('ST',.03)]])
        h=self.prices([('2024-09-05',.01),('2024-09-06',.05),('2024-09-07',.10),('2024-11-02',.02)])
        r=analyze(samples,h);q=r['detail'].set_index('model')
        self.assertEqual(q.loc['GB','entry_price'],.05);self.assertTrue(q.loc['GB','selected']);self.assertFalse(q.loc['ST','selected'])
        row=r['summary'].query('model=="GB" and signal=="Selected" and cost_cents==1').iloc[0]
        self.assertAlmostEqual(row.net_cents,4)
        samples.loc[0,'model_date']=pd.Timestamp('2024-09-07',tz='UTC')
        with self.assertRaises(ValueError):analyze(samples,h)

    def test_forward_horizon_does_not_use_later_price(self):
        h=self.prices([('2024-09-12',.04),('2024-09-14',.15),('2024-11-02',.02)])
        r=trace_path(h,pd.Timestamp('2024-09-06',tz='UTC'),.05,True,pd.Timestamp('2024-11-03',tz='UTC'))
        self.assertAlmostEqual(r['change_7d'],-.01)
