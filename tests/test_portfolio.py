"""Structural tests for mixing dependent forecasts and translating their means."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import numpy as np
import election_lab
from model_portfolio import mixture_moments,make_mixture
import pandas as pd

class PortfolioTests(unittest.TestCase):
    def test_total_covariance_includes_model_disagreement(self):
        m,c=mixture_moments([[0,0],[2,4]],[np.eye(2),np.eye(2)],[.5,.5])
        np.testing.assert_allclose(m,[1,2])
        np.testing.assert_allclose(c,[[2,2],[2,5]])

    def test_joint_components_and_unequal_draw_counts(self):
        # Each component always has exactly one winner. Independent statewise
        # selection would spuriously allow zero or two winners.
        components={}
        for name,values,n in [('a',[2,-2],3),('b',[-2,2],7)]:
            components[name]=dict(predictions=pd.DataFrame({'target_id':['a','b'],'margin_pp':values}),
                                  covariance=np.zeros((2,2)),draws=np.tile(values,(n,1)))
        mixture=make_mixture(components,{'component_weights':{'a':.25,'b':.75}})
        np.testing.assert_allclose(mixture['weights']@(mixture['samples']>0),[.25,.75])
        self.assertTrue(((mixture['samples']>0).sum(axis=1)==1).all())
        shift=np.array([1.,-.2])
        centered=mixture['samples']-mixture['mean']
        np.testing.assert_allclose(mixture['samples']+shift-(mixture['mean']+shift),centered)

if __name__=='__main__':unittest.main()
