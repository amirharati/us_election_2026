"""Changing a helper's scale must invalidate all inherited Gaussian summaries."""
from pathlib import Path
import sys,unittest
import numpy as np
import pandas as pd
from scipy.stats import norm
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab
from mean_only_polling_blend import rescore

class IntervalRefreshTests(unittest.TestCase):
    def test_scale_and_shift_replace_all_stale_intervals(self):
        p=pd.DataFrame(dict(margin_pp=[3.],sigma_pp=[12.],actual_pp=[4.],median_pp=[-8.],wis_pp=[999.]))
        for level in [50,70,80,95]:p[f'lo{level}_pp']=-1.;p[f'hi{level}_pp']=1.;p[f'width{level}_pp']=2.
        q=rescore(p)
        for level in [50,70,80,95]:
            half=norm.ppf((1+level/100)/2)*12
            self.assertAlmostEqual(q[f'lo{level}_pp'].iloc[0],3-half)
            self.assertAlmostEqual(q[f'hi{level}_pp'].iloc[0],3+half)
            self.assertAlmostEqual(q[f'width{level}_pp'].iloc[0],2*half)
        self.assertAlmostEqual(q.p_dem.iloc[0],norm.cdf(.25))
        self.assertLess(q.wis_pp.iloc[0],20.)
        shifted=rescore(q.assign(margin_pp=8.))
        for level in [50,70,80,95]:
            self.assertAlmostEqual(shifted[f'lo{level}_pp'].iloc[0]-q[f'lo{level}_pp'].iloc[0],5.)
            self.assertAlmostEqual(shifted[f'width{level}_pp'].iloc[0],q[f'width{level}_pp'].iloc[0])

    def test_unavailable_uncertainty_is_not_a_coverage_failure(self):
        p=rescore(pd.DataFrame(dict(margin_pp=[1.],sigma_pp=[np.nan],actual_pp=[2.])))
        self.assertEqual(p.correct.iloc[0],1.)
        self.assertTrue(p.brier.isna().all())
        for level in [50,70,80,95]:self.assertTrue(p[f'coverage{level}'].isna().all())

if __name__=='__main__':unittest.main()
