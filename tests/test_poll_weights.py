"""Behavioral checks for sample weighting and past-only pollster ratings."""
from pathlib import Path
import sys,unittest
import pandas as pd
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab
from poll_weight_experiment import aggregate,last_cycle_ratings,rating_multiplier,REFERENCE

class WeightTests(unittest.TestCase):
    def waves(self):
        return pd.DataFrame(dict(target_id=['x']*3,sample_key=['1','2','3'],firm=['a','a','b'],margin=[.1,.1,-.1],age_days=[0,0,0],reported_n=[100,100,800],publication_unknown=[False]*3))

    def test_firm_balance_n_and_missing_n(self):
        t=pd.DataFrame({'target_id':['x']});w=self.waves();empty=pd.DataFrame()
        expected={REFERENCE:0.,'Equal polls, 30d':10/3,'Respondent n, 30d':-6.,'Firm balanced + within-firm n':0.}
        for rule,mean in expected.items():
            a,ledger=aggregate(t,w,rule,empty,500.)
            self.assertAlmostEqual(a.q_pp.iloc[0],mean);self.assertAlmostEqual(a.firm_mass.iloc[0],2.)
            self.assertAlmostEqual(ledger.normalized_weight.sum(),1.)
        w.loc[2,'reported_n']=np.nan
        a,ledger=aggregate(t,w,'Respondent n, 30d',empty,200.)
        self.assertAlmostEqual(a.q_pp.iloc[0],0.);self.assertEqual(ledger.imputed_n.sum(),1)

    def test_only_previous_cycle_ranks_and_default_one(self):
        targets=pd.DataFrame(dict(target_id=['old','prev','now'],cycle=[2022,2024,2026],actual=[-.9,0.,.9]))
        w=pd.concat([self.waves().assign(target_id=t) for t in targets.target_id],ignore_index=True)
        # Make firm a accurate in the previous cycle, b less accurate.
        w.loc[w.target_id.eq('prev')&w.firm.eq('a'),'margin']=0.
        r=last_cycle_ratings(targets,w,2026)
        self.assertTrue(r.source_cycle.eq(2024).all())
        changed=targets.copy();changed.loc[changed.cycle.ne(2024),'actual']=-.123
        pd.testing.assert_frame_equal(r,last_cycle_ratings(changed,w,2026))
        factors=rating_multiplier(r,1.)
        self.assertGreater(factors['a'],1);self.assertLess(factors['b'],1)
        self.assertEqual(factors.get('unseen',1.),1.)
        self.assertTrue(all(.5<=v<=2 for v in factors.values()))

    def test_recency_and_literal_equal(self):
        t=pd.DataFrame({'target_id':['x']});w=self.waves().iloc[[0,2]].copy();w.loc[w.firm.eq('a'),'age_days']=30
        fresh,_=aggregate(t,w,'Equal polls, 30d',pd.DataFrame(),500.)
        equal,_=aggregate(t,w,'Equal polls, no decay',pd.DataFrame(),500.)
        self.assertAlmostEqual(fresh.q_pp.iloc[0],-10/3);self.assertAlmostEqual(equal.q_pp.iloc[0],0.)

if __name__=='__main__':unittest.main()
