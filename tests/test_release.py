"""Meaningful numerical and cache failure tests; no network required."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import tempfile
import json
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab as lab
from mean_only_blend_weights import blend_mean
from mean_only_polling_blend import translate_draws
import release_refresh as refresh


class ReleaseTests(unittest.TestCase):
    def test_weight_and_covariance(self):
        mu=np.array([-2.,4.]);other=np.array([3.,-1.]);cov=np.array([[9.,-1.],[-1.,4.]])
        draws=np.random.default_rng(3).multivariate_normal(mu,cov,1000)
        new=blend_mean(mu,other,.2);np.testing.assert_allclose(new,[-1.,3.])
        shifted=translate_draws(draws,mu,new)
        np.testing.assert_allclose(np.cov(shifted,rowvar=False),np.cov(draws,rowvar=False),atol=1e-12)

    def test_gasoline_cache_is_not_lost(self):
        p=refresh.cache_path('fred')
        from compact_data import CompactDataset
        store=CompactDataset(p).feature_store()
        self.assertFalse(store.monthly['gasoline'].empty)

    def test_failed_acquisition_is_explicit_stale_cache(self):
        with patch.object(refresh,'download_polls',side_effect=RuntimeError('offline')):
            r=refresh.acquire('polls',force=True,timeout=.1)
        self.assertEqual(r['acquisition_status'],'stale_cache_after_failure')
        self.assertEqual(r['failure_type'],'RuntimeError')
        self.assertTrue(Path(r['snapshot']).exists())

    def test_offline_does_not_download(self):
        with patch.object(refresh,'download_polls',side_effect=AssertionError('Unexpected network')):
            r=refresh.acquire('polls',offline=True)
        self.assertEqual(r['acquisition_status'],'offline_cache')

    def test_student_zero_df_gaussian_control(self):
        from combined_student_model import sample
        mu=np.array([1.,-2.]);L=np.array([9.,4.]);A=2.;FV=1.;obs=np.array([0]);y=np.array([3.]);P=np.array([4.]);F=np.array([1.])
        m,c,_=lab.gaussian.normal_update(mu,np.diag(L)+(A+FV),obs,y,np.diag(P+F))
        s=sample(mu,L,A,FV,obs,y,P,F,0,seed=31,warmup=30,draws=80,chains=2,check=False)
        np.testing.assert_allclose(s['mean'],m,atol=1e-12)
        np.testing.assert_allclose(s['covariance'],c,atol=1e-12)


if __name__=='__main__':unittest.main()
