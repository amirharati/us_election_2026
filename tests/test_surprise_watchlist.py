"""Ranking semantics, zero-poll inclusion and historical leakage checks."""
from pathlib import Path
import sys
import unittest
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab
from live_surprise_watchlist import summarize, historical_context


class SurpriseWatchlistTests(unittest.TestCase):
    def fixtures(self):
        rows=[]
        for state, means in [('A',[-10,0,10]),('B',[20,21,22]),('C',[-2,3,6])]:
            for model, mean, sd in zip(['Bayesian','Older Gaussian','Non-Bayesian corrected'],means,[1,2,3]):
                rows.append(dict(target_id=state,geography=state,special=False,model=model,
                    prediction_pp=mean,posterior_sd_pp=sd,p_dem=.1 if mean<0 else .9,
                    lo95_pp=mean-2*sd,hi95_pp=mean+2*sd))
        p=pd.DataFrame(rows)
        coverage=pd.DataFrame(dict(target_id=['A','B','C'],recent_samples=[5,0,1],recent_firms=[3,0,1],
                                   latest_poll=['2026-09-20',None,'2026-09-19'],stronger_coverage=[True,False,False]))
        h=pd.DataFrame([dict(target_id=f'{year}-A',geography='A',cycle=year,scenario='matched_live',
            prediction_pp=0,actual=actual,lo95_pp=-5,hi95_pp=5,historical_horizon_comparable=True)
            for year,actual in [(2018,.1),(2020,.02),(2022,-.08),(2024,.01),(2026,.99)]])
        return p,coverage,h

    def test_pairwise_disagreement_is_distinct_from_within_model_variance(self):
        p,c,h=self.fixtures()
        # A redundant blend must not influence either statistic.
        blend=p.iloc[[0]].assign(model='Corrected 20%',prediction_pp=1000,posterior_sd_pp=1000)
        result=summarize(pd.concat([p,blend]),c,h,2026,top_n=1)
        row=result['all'].set_index('contest').loc['A']
        self.assertAlmostEqual(row.disagreement_pp,40/3)
        self.assertAlmostEqual(row.predictive_variance_pp2,14/3)
        self.assertAlmostEqual(row.predictive_sd_pp,np.sqrt(14/3))
        self.assertEqual(row.model_count,3)
        self.assertAlmostEqual(row.other_winner_pct,10)
        self.assertTrue(row.winner_split)

    def test_zero_poll_races_retained_and_groups_are_separate(self):
        p,c,h=self.fixtures();r=summarize(p,c,h,2026,top_n=3)
        self.assertEqual(set(r['all'].contest),{'A','B','C'})
        self.assertEqual(set(r['polled'].contest),{'A'})
        self.assertEqual(set(r['thin'].contest),{'B','C'})
        row=r['thin'].set_index('contest').loc['B']
        self.assertIn('There are no recent eligible polls.',row.selection_reason)
        self.assertTrue(pd.isna(row.historical_n))

    def test_history_excludes_current_cycle_and_uses_last_three(self):
        _,_,h=self.fixtures();row=historical_context(h,2026).iloc[0]
        self.assertEqual(row.historical_n,3)
        self.assertEqual(row.historical_cycles,'2020, 2022, 2024')
        self.assertAlmostEqual(row.worst_error_pp,8)
        self.assertEqual(row.worst_error_cycle,2022)
        self.assertEqual(row.interval_misses,1)
        # A different horizon must not double count or leak into September history.
        extra=h.assign(scenario='oct31',actual=1.)
        pd.testing.assert_frame_equal(historical_context(h,2026),historical_context(pd.concat([h,extra]),2026))

    def test_single_model_has_unknown_disagreement_not_false_agreement(self):
        p,c,h=self.fixtures();r=summarize(p[p.model.eq('Bayesian')],c,h,2026)
        self.assertTrue(r['all'].disagreement_pp.isna().all())
        self.assertTrue(r['all'].model_count.eq(1).all())
        self.assertTrue(r['all'].predictive_sd_pp.eq(1).all())

if __name__=='__main__': unittest.main()
