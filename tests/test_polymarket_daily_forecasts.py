import unittest
import pandas as pd
from polymarket_daily_forecasts import assemble, dates

class DailyForecastTests(unittest.TestCase):
    def test_dates_exclude_election_day(self):
        self.assertEqual(len(dates(2022)),68)
        self.assertEqual(len(dates(2024)),65)
        self.assertEqual(str(dates(2024)[-1].date()),'2024-11-04')

    def frames(self):
        local=pd.DataFrame([dict(cycle=2022,forecast_date='2022-09-01',geography='PA',model='Gaussian',
            model_code='GB',target_id='2022-PA-regular-gen',p_dem=.6,provenance='test',actual=1)])
        pub=pd.DataFrame([dict(cycle=2022,forecast_date='2022-09-02',geography='PA',model='538',
            p_dem=.7,source_url='test',source_sha256='test',provenance='test',valid_until=None)])
        return local,pub

    def test_missing_is_not_carried_and_outcome_is_not_saved(self):
        local,pub=self.frames();q=assemble(local,pub)
        self.assertNotIn('actual',q)
        available=q[q.status.eq('available')]
        self.assertEqual(len(available),2)
        self.assertTrue((available.available_after_utc-available.forecast_date==pd.Timedelta(days=1)).all())
        self.assertTrue(q.query('model=="538"').iloc[0].p_dem!=q.query('model=="538"').iloc[0].p_dem)
        pub['valid_until']='2022-09-02'
        self.assertEqual(len(assemble(local,pub).query('status=="available"')),1)

    def test_duplicate_or_invalid_forecasts_fail(self):
        local,pub=self.frames()
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            assemble(local,pd.concat([pub,pub]))
        pub['p_dem']=1.1
        with self.assertRaisesRegex(ValueError,'invalid probability'):
            assemble(local,pub)
        pub['p_dem']=1+2e-16
        q=assemble(local,pub)
        self.assertTrue(q.loc[q.status.eq('available'),'p_dem'].between(0,1).all())

    def test_regular_and_special_are_separate(self):
        local,pub=self.frames()
        regular=pub.copy();regular['special']=False
        special=pub.copy();special['special']=True;special['p_dem']=.2
        q=assemble(local,pd.concat([regular,special]))
        available=q.query('model=="538" and status=="available"')
        self.assertEqual(set(available.race_kind),{'regular','special'})
        self.assertEqual(len(available),2)
