import sys
from pathlib import Path
import unittest
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from polymarket_edge_strategy import simulate_market,probability_band,forecast_streams

class EdgeStrategyTest(unittest.TestCase):
    def forecasts(self,values):
        return pd.DataFrame([dict(model_date=pd.Timestamp(t,tz='UTC'),available_at=pd.Timestamp(t,tz='UTC')+pd.Timedelta(days=1),probability=p) for t,p in values])
    def prices(self,values):
        return pd.DataFrame([dict(timestamp=pd.Timestamp(t,tz='UTC'),price_first=p,price_source='Test') for t,p in values])
    def run_case(self,f,h,**kw):
        return simulate_market(self.forecasts(f),self.prices(h),cycle=2024,state='AA',market_id='1',model='GB',**kw)

    def test_no_future_forecast_and_loss_exit_after_revision(self):
        r=self.run_case([('2024-09-05',.7),('2024-09-07',.3)], [('2024-09-05',.5),('2024-09-06',.5),('2024-09-07',.4),('2024-09-08',.4),('2024-11-04',.4)])
        self.assertEqual(len(r),1);t=r[0]
        self.assertEqual(t['entry_time'],pd.Timestamp('2024-09-06',tz='UTC'))
        self.assertEqual(t['exit_time'],pd.Timestamp('2024-09-08',tz='UTC'))
        self.assertEqual(t['exit_reason'],'Edge gone');self.assertAlmostEqual(t['pnl'],-11.)

    def test_no_overlap_no_same_observation_reentry_and_both_sides(self):
        r=self.run_case([('2024-09-05',.7)],[('2024-09-06',.5),('2024-09-07',.5),('2024-09-08',.8),('2024-09-09',.8),('2024-09-10',.65),('2024-11-04',.65)])
        self.assertEqual([t['side'] for t in r],['D','R'])
        self.assertEqual(r[1]['entry_time'],pd.Timestamp('2024-09-09',tz='UTC'))
        self.assertLess(r[0]['exit_time'],r[1]['entry_time'])

    def test_positive_midpoint_edge_is_not_positive_after_cost(self):
        r=self.run_case([('2024-09-05',.503)],[('2024-09-06',.5),('2024-11-04',.5)],cost=.005)
        self.assertEqual(r,[])

    def test_no_new_buys_final_day_and_no_hindsight_entry_filter(self):
        r=self.run_case([('2024-11-01',.8)],[('2024-11-02',.5)])
        self.assertEqual(len(r),1);self.assertEqual(r[0]['exit_reason'],'Pre-election close');self.assertAlmostEqual(r[0]['pnl'],-1.)
        r=self.run_case([('2024-11-03',.8)],[('2024-11-04',.5)])
        self.assertEqual(r,[])

    def test_confirmation_uses_second_observation_price(self):
        h=[('2024-09-06',.5),('2024-09-07',.9),('2024-09-08',.5),('2024-09-09',.72),('2024-09-10',.73),('2024-11-04',.73)]
        r=self.run_case([('2024-09-05',.7)],h,confirmations=2)
        self.assertEqual(r[0]['exit_time'],pd.Timestamp('2024-09-10',tz='UTC'));self.assertAlmostEqual(r[0]['net_sale'],.725)

    def test_profit_variant_and_settlement_do_not_change_entry(self):
        f=[('2024-09-05',.9)];h=[('2024-09-06',.5),('2024-09-07',.65),('2024-11-04',.65)]
        a=self.run_case(f,h,rule='Edge + profit',payout=1.)
        b=self.run_case(f,h,rule='Edge + profit',payout=0.)
        self.assertEqual(a[0]['exit_reason'],'Profit target');self.assertEqual(a[0]['pnl'],b[0]['pnl'])
        self.assertAlmostEqual(a[0]['hold_settlement_pnl']-b[0]['hold_settlement_pnl'],100.)

    def test_stale_close_remains_missing_not_zero(self):
        r=self.run_case([('2024-09-05',.8)],[('2024-09-06',.5)])
        self.assertFalse(r[0]['complete']);self.assertTrue(pd.isna(r[0]['pnl']))

    def test_probability_bands(self):
        self.assertIn('Long shot',probability_band(.10));self.assertIn('Competitive',probability_band(.3));self.assertIn('High probability',probability_band(.9))

    def test_model_availability_is_independent(self):
        mapping=pd.DataFrame([dict(cycle=2024,state='AA',market_id='1'),dict(cycle=2024,state='BB',market_id='2')])
        local=pd.DataFrame([dict(cycle=2024,geography=s,model_code=m,forecast_date='2024-09-05',p_dem=.7) for s,m in [('AA','GB'),('BB','ST')]])
        publishers=pd.DataFrame(columns=['cycle','geography','model','forecast_date','p_dem'])
        r=forecast_streams(mapping,local,publishers)
        self.assertEqual(set(zip(r.state,r.model)),{('AA','GB'),('BB','ST')})
        self.assertTrue((r.available_at>r.model_date).all())

    def test_no_future_peak_exit_or_hindsight_repricing(self):
        r=self.run_case([('2024-09-05',.7)],[('2024-09-06',.5),('2024-09-07',.72),('2024-09-08',.9),('2024-11-04',.9)])
        self.assertAlmostEqual(r[0]['net_sale'],.715)
        self.assertEqual(r[0]['exit_time'],pd.Timestamp('2024-09-07',tz='UTC'))

    def test_same_state_summary_does_not_change_independent_trades(self):
        from polymarket_edge_strategy import matched_coverage
        first=self.run_case([('2024-09-05',.7)],[('2024-09-06',.5),('2024-09-07',.8),('2024-11-04',.8)])[0]
        rows=[first,dict(first,model='OG',pnl=4.),dict(first,state='BB',market_id='2',pnl=99.)]
        trades=pd.DataFrame(rows)
        coverage=pd.DataFrame([dict(cycle=2024,state=s,model=m,forecasts=2,prices=5) for s,m in [('AA','GB'),('AA','OG'),('BB','GB')]])
        result,counts=matched_coverage(trades,coverage)
        self.assertEqual(counts.states.iloc[0],1)
        self.assertEqual(set(result.model),{'GB','OG'})
        self.assertEqual(result.set_index('model').loc['GB','pnl'],first['pnl'])
        self.assertEqual(len(trades),3)
