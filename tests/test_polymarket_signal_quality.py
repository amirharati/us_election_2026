import sys
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from polymarket_signal_quality import path_metrics,analyze,publisher_native,target_threshold,target_study,available_model_study,available_table
from polymarket_signal_publishers import economist_original,ddhq_history
from polymarket_edge_strategy import forecast_streams,simulate_market

class SignalQualityTest(unittest.TestCase):
    def test_available_models_use_own_panels_without_common_subset_filter(self):
        row=dict(cycle=2024,state='AZ',market_id='1',model='GB',model_date=pd.Timestamp('2024-09-01',tz='UTC'),
            entry_time=pd.Timestamp('2024-09-02',tz='UTC'),side='D',price=.4,edge=.2,horizon=30,complete=True,
            sustained_rise=.05,persistence=3,noise_cents=2)
        targets=target_study(dict(detail=pd.DataFrame([row,dict(row,model='RTWH',sustained_rise=.3)]),
            native_detail=pd.DataFrame([dict(row,model='RTWH',state='TX',market_id='2',sustained_rise=.1)])))
        r=available_model_study(targets,{'GB'})['available_overall']
        q=r[r.target.eq('Edge')].set_index('model')
        self.assertEqual(set(q.index),{'GB','RTWH'})
        self.assertEqual(q.loc['RTWH','signals'],1);self.assertEqual(q.loc['RTWH','confirmed'],0)
        self.assertEqual(q.loc['GB','signals'],1)
        table=available_table(r).set_index('Model')
        self.assertTrue(pd.isna(table.loc['538','Edge hit (%)']))
        self.assertEqual(table.loc['GB','Scored / markets'],'1 / 1')

    def test_relative_targets_are_price_returns_with_absolute_floor(self):
        self.assertAlmostEqual(target_threshold(.1,.4,'5%'),.02)
        self.assertAlmostEqual(target_threshold(.5,.4,'5%'),.025)
        self.assertAlmostEqual(target_threshold(.5,.4,'10%'),.05)
        self.assertAlmostEqual(target_threshold(.5,.4,'50%'),.25)
        self.assertAlmostEqual(target_threshold(.5,.4,'Edge'),.4)

    def test_relative_targets_do_not_also_require_covering_edge(self):
        row=dict(cycle=2024,state='AZ',market_id='1',model='GB',model_date=pd.Timestamp('2024-09-01',tz='UTC'),
            entry_time=pd.Timestamp('2024-09-02',tz='UTC'),side='D',price=.4,edge=.2,horizon=30,complete=True,
            sustained_rise=.05,persistence=3,noise_cents=2)
        r=target_study(dict(detail=pd.DataFrame([row]),native_detail=pd.DataFrame([dict(row,complete=False)])))
        q=r['target_summary'].query('panel=="Shared dates"').set_index('target')
        self.assertEqual(q.loc['Edge','full_hits'],0);self.assertEqual(q.loc['5%','full_hits'],1)
        self.assertEqual(q.loc['10%','full_hits'],1);self.assertEqual(q.loc['20%','full_hits'],0)
        q=r['target_summary'].query('panel=="Publisher dates"').set_index('target')
        self.assertEqual(q.loc['10%','partial_confirmed'],1);self.assertEqual(q.loc['10%','scored'],0)
        self.assertTrue(pd.isna(q.loc['10%','hit_pct']));self.assertEqual(q.loc['50%','unknown'],1)

    def test_single_off_grid_publisher_snapshot_is_retained(self):
        mapping=pd.DataFrame([dict(cycle=2024,state='AZ',market_id='1')])
        pubs=pd.DataFrame([dict(cycle=2024,geography='AZ',model='RTWH',forecast_date='2024-09-08',p_dem=.15,source_url='test')])
        h=pd.DataFrame(dict(market_id='1',timestamp=pd.date_range('2024-09-09',periods=32,tz='UTC'),price_first=[.1]+[.16]*31))
        r=publisher_native(mapping,h,pubs);q=r['native_summary'].query('horizon==30').iloc[0]
        self.assertEqual(q.dates,1);self.assertEqual(q.confirmed,1);self.assertEqual(q.evidence,'Single-date evidence')

    def test_partial_window_witness_is_not_a_full_window_rate(self):
        mapping=pd.DataFrame([dict(cycle=2024,state='AZ',market_id='1')])
        pubs=pd.DataFrame([dict(cycle=2024,geography='AZ',model='RTWH',forecast_date='2024-10-30',p_dem=.15)])
        h=pd.DataFrame(dict(market_id='1',timestamp=pd.date_range('2024-10-31',periods=5,tz='UTC'),price_first=[.1,.16,.16,.16,.1]))
        r=publisher_native(mapping,h,pubs);q=r['native_summary'].query('horizon==30').iloc[0]
        self.assertEqual(q.confirmed,1);self.assertEqual(q.partial_confirmed,1);self.assertEqual(q.scored,0);self.assertTrue(pd.isna(q.hit_pct))
        h['price_first']=[.1,.16,.1,.1,.1]
        q=publisher_native(mapping,h,pubs)['native_summary'].query('horizon==30').iloc[0]
        self.assertEqual(q.confirmed,0);self.assertEqual(q.unknown,1)

    def path(self,values,persistence=3):
        t=pd.Timestamp('2024-09-01',tz='UTC')
        h=pd.DataFrame(dict(timestamp=pd.date_range(t+pd.Timedelta(days=1),periods=len(values)),price_first=values))
        return path_metrics(h,t,.1,'D',len(values),pd.Timestamp('2024-11-05',tz='UTC'),persistence)

    def test_spike_does_not_qualify(self):
        q=self.path([.1,.1,.9,.1,.1,.1,.1])
        self.assertTrue(q['complete']);self.assertAlmostEqual(q['sustained_rise'],0)

    def test_three_day_floor_not_peak(self):
        q=self.path([.08,.15,.18,.16,.1,.1,.1])
        self.assertAlmostEqual(q['sustained_rise'],.05)
        i=np.argmax(q['levels']);self.assertAlmostEqual(q['worsts'][i],-.02)

    def test_invalid_day_breaks_run(self):
        q=self.path([.2,.2,np.nan,.2,.2,.1,.1])
        self.assertAlmostEqual(q['sustained_rise'],0)

    def test_gaps_do_not_become_persistence(self):
        t=pd.Timestamp('2024-09-01',tz='UTC')
        h=pd.DataFrame(dict(timestamp=pd.to_datetime(['2024-09-02','2024-09-05','2024-09-08'],utc=True),price_first=[.2]*3))
        q=path_metrics(h,t,.1,'D',7,pd.Timestamp('2024-11-05',tz='UTC'))
        self.assertFalse(q['complete']);self.assertTrue(np.isnan(q['sustained_rise']))

    def test_horizon_after_election_not_scored(self):
        t=pd.Timestamp('2024-11-01',tz='UTC')
        h=pd.DataFrame(dict(timestamp=pd.date_range(t,periods=10),price_first=[.9]*10))
        q=path_metrics(h,t,.1,'D',7,pd.Timestamp('2024-11-05',tz='UTC'))
        self.assertFalse(q['complete']);self.assertEqual(q['reason'],'Horizon reaches election')

    def test_economist_correction_never_backdated(self):
        q=economist_original(pd.DataFrame(dict(date=['10/30/2022','10/31/2022'],old_dem_win_prob=[.6,.7],new_dem_win_prob=[.1,.2])),'AZ')
        self.assertEqual(q.p_dem.tolist(),[.6]);self.assertEqual(q.valid_until.iloc[0],pd.Timestamp('2022-10-31',tz='UTC'))

    def test_ddhq_orientation_and_prelaunch_exclusion(self):
        raw=dict(candidates=[{'party':'DEM'},{'party':'GOP'}],time_series=[
            {'time':'2024-08-20','prob':.2},{'time':'2024-08-27','prob':.3},{'time':'2024-08-27','prob':.3}])
        q=ddhq_history(raw,'AZ','website_files_harris')
        self.assertEqual(len(q),1);self.assertAlmostEqual(q.p_dem.iloc[0],.7)
        self.assertEqual(q.model.iloc[0],'DDHQ')

    def test_ddhq_conflicting_duplicates_rejected(self):
        raw=dict(candidates=[{'party':'DEM'},{'party':'GOP'}],time_series=[
            {'time':'2024-09-01','prob':.2},{'time':'2024-09-01','prob':.3}])
        with self.assertRaises(ValueError):ddhq_history(raw,'AZ','website_files_harris')

    def test_may_forecast_survives_year_boundary_filter(self):
        mapping=pd.DataFrame([dict(cycle=2024,state='AZ',market_id='1')])
        local=pd.DataFrame(columns=['cycle','geography','model_code','forecast_date','p_dem'])
        pubs=pd.DataFrame([dict(cycle=2024,geography='AZ',model='RTWH',forecast_date=d,p_dem=p) for d,p in [('2023-12-30',.7),('2024-05-28',.8)]])
        f=forecast_streams(mapping,local,pubs)
        h=pd.DataFrame(dict(timestamp=pd.to_datetime(['2024-06-01','2024-11-04'],utc=True),price_first=[.6,.6],price_source='test'))
        r=simulate_market(f,h,cycle=2024,state='AZ',market_id='1',model='RTWH')
        self.assertEqual(r[0]['entry_model_date'],pd.Timestamp('2024-05-28',tz='UTC'))

    def test_signal_uses_post_forecast_price_and_fixed_initial_edge(self):
        samples=pd.DataFrame([dict(cycle=2024,state='AZ',market_id='1')])
        local=pd.DataFrame([dict(cycle=2024,geography='AZ',model_code='GB',forecast_date='2024-09-01',p_dem=.15)])
        pubs=pd.DataFrame(columns=['cycle','geography','model','forecast_date','p_dem'])
        h=pd.DataFrame(dict(market_id='1',timestamp=pd.date_range('2024-09-01',periods=33,tz='UTC'),price_first=[.9,.1]+[.15]*31))
        times=pd.Series(pd.to_datetime(['2024-09-01','2024-09-02','2024-09-03'],utc=True))
        r=analyze(samples,h,local,pubs,({'1':times},{'1'}))
        q=r['detail'].query('side=="D" and horizon==7 and persistence==3 and noise_cents==2').iloc[0]
        self.assertEqual(q.entry_time,pd.Timestamp('2024-09-02',tz='UTC'));self.assertAlmostEqual(q.edge,.05);self.assertEqual(q.hit,1.)
        self.assertEqual(q.prior_transactions,1);self.assertEqual(q.activity_band,'1–9 transactions')

    def test_controls_face_signal_edge_not_smaller_noise_floor(self):
        samples=pd.DataFrame([dict(cycle=2024,state=s,market_id=s) for s in ['AA','BB','CC','DD']])
        local=pd.DataFrame([dict(cycle=2024,geography=s,model_code='GB',forecast_date='2024-09-01',p_dem=.15 if s=='AA' else .09) for s in samples.state])
        pubs=pd.DataFrame(columns=['cycle','geography','model','forecast_date','p_dem'])
        h=pd.concat([pd.DataFrame(dict(market_id=s,timestamp=pd.date_range('2024-09-02',periods=32,tz='UTC'),price_first=[.1]+[.15 if s=='AA' else .13]*31)) for s in samples.state])
        r=analyze(samples,h,local,pubs)
        q=r['detail'].query('state=="AA" and side=="D" and horizon==7 and persistence==3 and noise_cents==2').iloc[0]
        self.assertEqual(q.hit,1);self.assertEqual(q.baseline_controls,3);self.assertEqual(q.baseline_hit,0)

if __name__=='__main__':unittest.main()
