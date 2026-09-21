"""Distribution and linear-algebra controls for the signed-factor Student sampler."""
from pathlib import Path
import sys,unittest
import numpy as np
from scipy.stats import norm,t
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab as lab
from matched_student import sample,control


class MatchedStudentTests(unittest.TestCase):
    def test_signed_gaussian_control_with_missing_poll(self):
        args=(np.array([1.,-2.,4.]),np.array([9.,4.,6.]),2.,1.,np.array([1.2,-.8,.4]),np.array([0,2]),np.array([3.,1.]),np.array([4.,3.]),np.array([1.,2.]))
        (m,C),K=control(args)
        out=sample(*args,nu=0,seed=41,warmup=0,draws=64,chains=2,check=False)
        np.testing.assert_allclose(out['mean'],m,atol=1e-11)
        np.testing.assert_allclose(out['covariance'],C,atol=1e-11)
        np.testing.assert_allclose(out['p_dem'],norm.cdf(m/np.sqrt(np.diag(C))),atol=1e-12)
        self.assertGreater(K[0,2],K[0,1])

    def test_unobserved_scalar_matches_known_student_distribution(self):
        # With no polls or shared factors, the exact prior is a scaled univariate t.
        args=(np.array([2.]),np.array([4.]),0.,0.,np.array([0.]),np.array([],dtype=int),np.array([]),np.array([]),np.array([]))
        out=sample(*args,nu=5,seed=93,warmup=100,draws=4000,chains=4,check=False)
        exact=t.cdf(2/(2*np.sqrt(3/5)),df=5)
        self.assertAlmostEqual(out['mean'][0],2.,places=12)
        self.assertLess(abs(out['p_dem'][0]-exact),.006)
        self.assertLess(abs(out['covariance'][0,0]-4),.25)
        quantile=2+2*np.sqrt(3/5)*t.ppf([.15,.85],df=5)
        np.testing.assert_allclose(np.quantile(out['samples'][:,0],[.15,.85]),quantile,atol=.1)

    def test_scalar_observed_posterior_against_quadrature(self):
        # Independent numerical integration over prior/poll gamma precisions.
        from scipy.special import roots_genlaguerre,gamma
        def integrate(order):
            x,w=roots_genlaguerre(order,1.5);w=w/gamma(2.5)
            lv=4*1.5/x[:,None];rv=3*1.5/x[None,:]+1
            total=lv+rv;cm=-2+lv/total*7;cv=lv*rv/total
            weight=w[:,None]*w[None,:]*norm.pdf(7,scale=np.sqrt(total));weight/=weight.sum()
            mean=np.sum(weight*cm)
            return np.array([mean,np.sum(weight*(cv+cm*cm))-mean*mean,np.sum(weight*norm.cdf(cm/np.sqrt(cv)))])
        expected=integrate(128)
        np.testing.assert_allclose(integrate(96),expected,atol=.003)
        args=(np.array([-2.]),np.array([4.]),0.,0.,np.array([0.]),np.array([0]),np.array([5.]),np.array([3.]),np.array([1.]))
        out=sample(*args,nu=5,seed=231,warmup=2000,draws=4000,chains=8,check=True)
        self.assertLess(abs(out['mean'][0]-expected[0]),.08)
        self.assertLess(abs(out['covariance'][0,0]-expected[1]),.20)
        self.assertLess(abs(out['p_dem'][0]-expected[2]),.01)

    def test_infinite_variance_setting_rejected(self):
        args=(np.array([0.]),np.array([1.]),0.,0.,np.array([0.]),np.array([],dtype=int),np.array([]),np.array([]),np.array([]))
        with self.assertRaises(ValueError):sample(*args,nu=2)

if __name__=='__main__':unittest.main()
