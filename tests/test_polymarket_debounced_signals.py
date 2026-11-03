import unittest
import numpy as np
import pandas as pd
from polymarket_debounced_signals import debounce,episode_path,canonical_markets,analyze

class DebounceTests(unittest.TestCase):
    def checks(self,edges):
        dates=pd.date_range('2022-09-02',periods=len(edges),tz='UTC')
        return pd.DataFrame(dict(decision=dates,probability=[.5+x for x in edges],price=.5,
            quote_time=dates-pd.Timedelta(hours=1),model_date=dates-pd.Timedelta(days=1)))

    def test_repeat_and_brief_flip_are_one_setup(self):
        e,d=debounce(self.checks([.08,.07,-.01,.03,.04]),pd.Timestamp('2022-11-08',tz='UTC'))
        self.assertEqual(len(e),1);self.assertEqual((d.action=='Enter').sum(),1)

    def test_reset_then_new_entry_and_no_overlap(self):
        e,d=debounce(self.checks([.08,.03,-.01,-.02,.04]),pd.Timestamp('2022-11-08',tz='UTC'))
        self.assertEqual(len(e),2)
        self.assertEqual(e[0]['end'],pd.Timestamp('2022-09-05',tz='UTC'))
        self.assertGreater(e[1]['start'],e[0]['end'])
        self.assertEqual(d.action.tolist(),['Enter','Continue','Continue','Reset','Enter'])

    def test_missing_and_reused_quote_do_not_confirm_reset(self):
        e,d=debounce(self.checks([.08,-.01,np.nan,-.01,.04]),pd.Timestamp('2022-11-08',tz='UTC'))
        self.assertEqual(len(e),1);self.assertNotIn('Reset',d.action.tolist())
        q=self.checks([.08,-.01,-.02]);q.loc[2,'quote_time']=q.loc[1,'quote_time']
        e,d=debounce(q,pd.Timestamp('2022-11-08',tz='UTC'))
        self.assertNotIn('Reset',d.action.tolist())

    def test_strict_entry_threshold(self):
        e,d=debounce(self.checks([.019,.02,.021]),pd.Timestamp('2022-11-08',tz='UTC'))
        self.assertEqual(e[0]['start'],pd.Timestamp('2022-09-04',tz='UTC'))

    def test_path_stops_at_reset_and_rejects_spike(self):
        h=pd.DataFrame(dict(timestamp=pd.date_range('2022-09-02',periods=7,tz='UTC')+pd.Timedelta(hours=12),
                            price_first=[.3,.3,.3,.9,.2,.99,.99]))
        e=dict(start=pd.Timestamp('2022-09-02',tz='UTC'),end=pd.Timestamp('2022-09-07',tz='UTC'),price=.2,side='D',edge=.1)
        stats,path=episode_path(h,e)
        self.assertAlmostEqual(stats['max_sustained_rise'],.1)
        self.assertAlmostEqual(stats['max_rise'],.7)
        self.assertAlmostEqual(stats['endpoint_change'],0)
        self.assertEqual(len(path),5);self.assertTrue(stats['complete'])
        self.assertTrue(stats['hit_edge'])
        h=h.drop(index=1)
        stats,_=episode_path(h,e)
        self.assertFalse(stats['hit_edge'])

    def test_equivalent_contracts_grouped_without_future_data(self):
        m=pd.DataFrame([dict(cycle=2022,market_id=str(i),category='winner',question=f'Will {party} win Pennsylvania Senate?',description='',outcome_first='Yes',outcome_second='No') for i,party in [(3,'Republicans'),(5,'Democrats'),(7,'Democrats')]])
        reps,audit=canonical_markets(m)
        self.assertEqual(reps.market_id.tolist(),['5'])
        self.assertEqual(len(audit),3)

    def test_forecast_freshness_and_no_future_quotes(self):
        m=pd.DataFrame([dict(cycle=2022,market_id='1',category='winner',question='Will Democrats win Pennsylvania Senate?',description='',outcome_first='Yes',outcome_second='No')])
        f=pd.DataFrame([dict(cycle=2022,geography='PA',race_kind='regular',status='available',model='GB',p_dem=.8,
            forecast_date=pd.Timestamp('2022-09-01',tz='UTC'),available_after_utc=pd.Timestamp('2022-09-02',tz='UTC'))])
        p=pd.DataFrame(dict(market_id='1',timestamp=pd.date_range('2022-09-01',periods=7,tz='UTC')+pd.Timedelta(hours=12),price_first=.5))
        r=analyze(f,m,p)
        d=r['decisions']
        self.assertEqual(d.iloc[0].price,.5)
        self.assertLess(d.iloc[0].quote_time,d.iloc[0].decision)
        self.assertTrue(d.loc[d.decision.ge('2022-09-05'),'probability'].isna().all())
        self.assertEqual(len(r['episodes']),1)
