from pathlib import Path
import sys
import unittest
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from polymarket_history_samples import prepare_samples,sample_table


class DateSamplesTest(unittest.TestCase):
    def inputs(self):
        m=pd.DataFrame([dict(cycle=2024,market_id='1',question='Will Democrats win the Texas Senate election in 2024?',
            url='https://example.com',category='winner',description='General election.',outcome_first='Yes',outcome_second='No',payout_first=0.)])
        p=pd.DataFrame([dict(market_id='1',timestamp=pd.Timestamp(t,tz='UTC'),price_first=v) for t,v in
            [('2024-09-17 12:00',.1),('2024-09-18 00:00',.2),('2024-10-02 00:00',.3)]])
        f=pd.DataFrame([dict(cycle=2024,geography='TX',model_code='GB',forecast_date='2024-09-17',p_dem=.15,actual=-.08)])
        x=pd.DataFrame([dict(cycle=2024,geography='TX',model='RTWH',forecast_date=d,p_dem=v) for d,v in
            [('2024-09-15',.25),('2024-09-18',.99),('2024-09-30',.35)]])
        return m,p,f,x

    def test_dates_and_no_local_carry_forward(self):
        q,a=prepare_samples(*self.inputs(),dates=['09-17','10-01'])
        local=q[q.model.eq('GB')];self.assertEqual(len(local),1)
        self.assertEqual(local.market_probability.iloc[0],.1)
        published=q[q.model.eq('RTWH')]
        self.assertEqual(published.model_probability.tolist(),[.25,.35])
        self.assertTrue((q.model_date<=q.check_date).all())
        self.assertTrue((q.market_time.dropna()<q.loc[q.market_time.notna(),"check_date"]+pd.Timedelta(days=1)).all())
        self.assertTrue(a[~a.available].reason.str.len().gt(0).all())

    def test_missing_price_is_blank_with_known_result(self):
        m,p,f,x=self.inputs();p=p.iloc[:0]
        q,_=prepare_samples(m,p,f,x,dates=['09-17'])
        self.assertTrue(q.market_probability.isna().all())
        self.assertEqual(set(q.final_winner),{'R'})
        self.assertTrue(q.status.str.contains('No market price').all())
        self.assertEqual(len(sample_table(q[q.model.eq('GB')]).columns),6)

    def test_stale_publisher_not_reused(self):
        q,a=prepare_samples(*self.inputs(),dates=['10-15'])
        self.assertTrue(q.empty)
        self.assertFalse(a.available.any())

    def test_drained_pool_does_not_use_an_earlier_quote(self):
        m,p,f,x=self.inputs()
        p=pd.concat([p,p.iloc[:1].assign(timestamp=pd.Timestamp('2024-09-17 23:00',tz='UTC'),price_first=float('nan'))])
        q,_=prepare_samples(m,p,f,x,dates=['09-17'])
        self.assertTrue(q.market_probability.isna().all())

    def test_stale_market_is_not_reused(self):
        m,p,f,x=self.inputs()
        p=p.iloc[:1].assign(timestamp=pd.Timestamp('2024-09-01',tz='UTC'))
        q,_=prepare_samples(m,p,f,x,dates=['09-17'])
        self.assertTrue(q.market_probability.isna().all())

    def test_conflicting_results_fail(self):
        m,p,f,x=self.inputs();f=pd.concat([f,f.assign(model_code='ST',actual=.08)])
        with self.assertRaises(ValueError):prepare_samples(m,p,f,x)

    def test_settlement_conflict_is_visible(self):
        m,p,f,x=self.inputs();m['payout_first']=1.
        q,_=prepare_samples(m,p,f,x,dates=['09-17'])
        self.assertTrue(q.status.str.contains('disagree').all())


class OverallSamplesTest(unittest.TestCase):
    def test_common_states_and_missing_prices(self):
        from polymarket_history_samples import overall_samples
        date=pd.Timestamp('2024-09-17',tz='UTC')
        rows=[dict(cycle=2024,check_date=date,state=state,model=model,final_winner='R',status='Matched',model_probability=p,market_probability=m)
              for state,model,p,m in [('TX','GB',.2,.3),('TX','ST',.4,.3),('PA','GB',.8,.7)]]
        q=overall_samples(pd.DataFrame(rows))
        self.assertEqual(q.priced_states.tolist(),[1,1])
        self.assertAlmostEqual(q.model_brier.iloc[0],.04)
        self.assertAlmostEqual(q.market_brier.iloc[0],.09)
        for row in rows:row['market_probability']=float('nan')
        q=overall_samples(pd.DataFrame(rows));self.assertTrue(q.model_brier.isna().all());self.assertTrue(q.market_brier.isna().all())

    def test_control_result_uses_saved_outcomes_and_no_model_guess(self):
        from polymarket_history_samples import chamber_market_samples
        m=pd.DataFrame([dict(cycle=2024,market_id='1',category='control',outcome_first='Democrats')])
        p=pd.DataFrame([dict(market_id='1',timestamp=pd.Timestamp('2024-09-17 20:00',tz='UTC'),price_first=.2)])
        s=pd.DataFrame([dict(cycle=2024,actual_D=47)])
        q=chamber_market_samples(m,p,s,dates=['09-17'])
        self.assertEqual(q.final_control.iloc[0],'R');self.assertTrue(q.model_probability.isna().all())
        self.assertEqual(q.market_probability.iloc[0],.2)

if __name__=='__main__':unittest.main()

class ProximityTest(unittest.TestCase):
    def test_unknown_winners_are_not_scored_as_republican(self):
        from polymarket_history_samples import proximity
        q=pd.DataFrame([dict(cycle=2024,state='TX',check_date=pd.Timestamp('2024-09-05'),model='GB',market_probability=.3,model_probability=.2,status='Matched',final_winner='Unavailable')])
        self.assertTrue(proximity(q).empty)

    def test_overall_proximity_uses_same_states(self):
        from polymarket_history_samples import overall_proximity
        q=pd.DataFrame([dict(state=s,model=m,gap_pp=g,model_brier=.1) for s,m,g in [('TX','GB',10),('TX','ST',20),('PA','GB',99)]])
        r=overall_proximity(q)
        self.assertEqual(r.states.tolist(),[1,1]);self.assertEqual(r.gap_pp.tolist(),[10,20])
