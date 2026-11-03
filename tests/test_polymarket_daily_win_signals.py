import unittest
import pandas as pd
from polymarket_daily_win_signals import remaining_path, analyze

class DailyWinnerTests(unittest.TestCase):
    def test_late_window_can_be_complete_without_thirty_days(self):
        stamps=pd.date_range('2022-11-03','2022-11-07',tz='UTC')
        h=pd.DataFrame({'timestamp':stamps,'price_first':[.2,.3,.3,.3,.3]})
        p=remaining_path(h,stamps[0],.2,'D',pd.Timestamp('2022-11-08',tz='UTC'))
        self.assertTrue(p['complete']);self.assertAlmostEqual(p['sustained_rise'],.1)
        short=remaining_path(h,stamps[-2],.3,'D',pd.Timestamp('2022-11-08',tz='UTC'))
        self.assertFalse(short['complete']);self.assertEqual(short['reason'],'Too little time for persistence')

    def test_spike_and_election_day_do_not_qualify(self):
        stamps=pd.date_range('2022-11-03','2022-11-09',tz='UTC')
        h=pd.DataFrame({'timestamp':stamps,'price_first':[.2,.3,.2,.2,.3,.9,.9]})
        p=remaining_path(h,stamps[0],.2,'D',pd.Timestamp('2022-11-08',tz='UTC'))
        self.assertEqual(p['sustained_rise'],0)

    def test_mapping_no_lookahead_and_partial_hits(self):
        f=pd.DataFrame([dict(cycle=2022,forecast_date=pd.Timestamp('2022-09-01',tz='UTC'),
            available_after_utc=pd.Timestamp('2022-09-02',tz='UTC'),geography='PA',race_kind='regular',model='GB',p_dem=.8,status='available')])
        markets=pd.DataFrame([dict(cycle=2022,market_id='a',category='winner',question='Will Republicans win Pennsylvania Senate?',description='',outcome_first='Yes',outcome_second='No')])
        prices=pd.DataFrame({'market_id':['a']*5,'timestamp':pd.date_range('2022-09-01',periods=5,tz='UTC'),
            'price_first':[.99,.8,.7,.7,.7]})
        r=analyze(f,markets,prices)['detail'].query('target=="10%"').iloc[0]
        self.assertEqual(r.side,'D');self.assertAlmostEqual(r.price,.2)
        self.assertEqual(r.entry_time,pd.Timestamp('2022-09-02',tz='UTC'))
        self.assertTrue(r.confirmed);self.assertFalse(r.complete)
        self.assertEqual(r.observations,3)
