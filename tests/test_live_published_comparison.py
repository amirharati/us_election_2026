from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
import pandas as pd
import requests
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab as lab
import live_published_comparison as pub


class PublishedComparisonTests(unittest.TestCase):
    def inputs(self):
        p=pd.DataFrame([dict(model='Bayesian',target_id='2026-OH-3-special',geography='OH',special=True,p_dem=.80),
                        dict(model='Bayesian',target_id='2026-NE-2',geography='NE',special=False,p_dem=.60)])
        s=pd.DataFrame([dict(model='Bayesian',p_D_control=.45,expected_D=50.3)])
        return p,s

    def snapshot(self, **row):
        return dict(published_date='2026-09-20',D_control_pct=60.,expected_D=51.,
                    rows=[dict(geography='OH',seat_class=3,p_dem=.40,independent_pct=0,rating=None,**row)])

    def test_gap_direction_and_special_contest(self):
        p,s=self.inputs();c=pub.compare(p,s,{'rttwh':self.snapshot()},'2026-09-21',set(),('Bayesian',),15,.75)
        self.assertEqual(c['chamber_gaps'].iloc[0]['Gap (pp)'],-15)
        row=c['mismatches'].iloc[0]
        self.assertEqual(row['Contest'],'OH (special)')
        self.assertAlmostEqual(row['Gap (pp)'],40)
        self.assertIn('different parties.',row['Reason'])

    def test_future_releases_excluded(self):
        p,s=self.inputs();snap=self.snapshot()
        c=pub.compare(p,s,{'rttwh':snap},'2026-09-19',set(),('Bayesian',),15,.75)
        self.assertTrue(c['all_states'].empty)

    def test_independent_probability_added_once_and_race_included(self):
        p,s=self.inputs();snap=self.snapshot()
        snap['rows'][0].update(geography='NE',seat_class=2,p_dem=0.,independent_pct=65.)
        c=pub.compare(p,s,{'rttwh':snap},'2026-09-21',{'NE'},('Bayesian',),15,.75)
        row=c['all_states'].iloc[0]
        self.assertEqual(row['Published D/Independent win %'],65.)
        self.assertAlmostEqual(row['Gap (pp)'],-5.)
        self.assertFalse(row['selected'])
        self.assertTrue(c['exclusions'].empty)
        # A source that already places the independent in D gives the same result.
        snap['rows'][0].update(p_dem=.65,independent_pct=0.)
        other=pub.compare(p,s,{'rttwh':snap},'2026-09-21',{'NE'},('Bayesian',),15,.75)
        pd.testing.assert_frame_equal(c['all_states'],other['all_states'])
        # Separate D and independent candidates both contribute to the D/Independent side.
        snap['rows'][0].update(p_dem=.25,independent_pct=40.)
        other=pub.compare(p,s,{'rttwh':snap},'2026-09-21',{'NE'},('Bayesian',),15,.75)
        pd.testing.assert_frame_equal(c['all_states'],other['all_states'])

    def test_independent_ratings_are_on_combined_side(self):
        p,s=self.inputs();snap=self.snapshot();snap.update(D_control_pct=None,expected_D=None)
        snap['rows'][0].update(geography='NE',seat_class=2,p_dem=None,rating='Lean Independent')
        c=pub.compare(p,s,{'inside':snap},'2026-09-21',{'NE'},('Bayesian',),15,.75)
        self.assertEqual(len(c['all_states']),1)
        self.assertTrue(c['mismatches'].empty)
        self.assertEqual(c['ratings'].iloc[0]['Publisher D/Independent favored'],1)


    def test_ratings_have_no_invented_probability(self):
        p,s=self.inputs();snap=self.snapshot();snap.update(D_control_pct=None,expected_D=None)
        snap['rows'][0].update(p_dem=None,rating='Toss-up')
        c=pub.compare(p,s,{'inside':snap},'2026-09-21',set(),('Bayesian',),15,.75)
        self.assertTrue(pd.isna(c['mismatches'].iloc[0]['Published D/Independent win %']))
        self.assertEqual(c['ratings'].iloc[0]['Matched races'],1)
        self.assertEqual(c['ratings'].iloc[0]['Publisher toss-ups'],1)

    def test_seat_class_and_duplicate_local_state_rejected(self):
        p,s=self.inputs();snap=self.snapshot();snap['rows'][0]['seat_class']=2
        self.assertTrue(pub.compare(p,s,{'inside':snap},'2026-09-21',set(),('Bayesian',),15,.75)['all_states'].empty)
        self.assertTrue(pub.compare(pd.concat([p,p]),s,{'rttwh':self.snapshot()},'2026-09-21',set(),('Bayesian',),15,.75)['all_states'].empty)

    def test_offline_never_downloads_and_failure_is_explicit(self):
        old=dict(retrieved_at='2026-09-01T00:00:00+00:00',published_date='2026-09-01')
        with patch.object(pub,'cached_snapshot',return_value=old),patch.object(pub,'download',side_effect=requests.Timeout('timeout')) as get:
            snap,status=pub.acquire('rttwh',offline=True);get.assert_not_called()
            self.assertEqual(status['Status'],'offline_cache')
            snap,status=pub.acquire('rttwh',force=True)
            self.assertIs(snap,old);self.assertEqual(status['Status'],'stale_cache_after_failure')
            self.assertIn('Timeout',status['Error'])

    def test_missing_cache_does_not_fabricate_forecast(self):
        with patch.object(pub,'cached_snapshot',return_value=None),patch.object(pub,'download',side_effect=ValueError('Schema changed')):
            snap,status=pub.acquire('inside')
            self.assertIsNone(snap);self.assertEqual(status['Status'],'unavailable')

    def test_schema_rejects_unknown_rating(self):
        d=dict(office='Senate',total=100,last_updated='2026-09-20',ratings=[dict(rating='Maybe D',election_year='2026')])
        with self.assertRaises(ValueError):pub.parse_inside(d)

    def test_cached_snapshot_checksum_and_clone_fallback(self):
        with tempfile.TemporaryDirectory() as temp,patch.object(lab,'ROOT',Path(temp)):
            path=Path(temp)/'cache/published_forecasts/rttwh.json';path.parent.mkdir(parents=True)
            path.write_text(json.dumps(dict(sha256='wrong',snapshot={'changed':True})))
            self.assertIsNone(pub.cached_snapshot('rttwh'))
            out=Path(temp)/'outputs/reports/forecast';out.mkdir(parents=True)
            (out/'published_sources.json').write_text(json.dumps({'rttwh':{'test':1}}))
            with patch.object(lab,'verify_run',return_value=out),patch.object(pub,'validate',side_effect=lambda s:s):
                self.assertEqual(pub.cached_snapshot('rttwh'),{'test':1})
