import sys
from pathlib import Path
import unittest
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from polymarket_accuracy_evolution import analyze

class EvolutionTest(unittest.TestCase):
    def fixture(self):
        rows=[]
        for state,p,winner,margin in [('AA',.5,'D',1.),('BB',.95,'R',-8.)]:
            for date in ['09-05','09-20']:
                for model,probability in [('GB',.8),('ST',.7)]:
                    rows.append(dict(cycle=2024,state=state,model=model,check_date=pd.Timestamp('2024-'+date,tz='UTC'),
                        market_probability=p,model_probability=probability,final_winner=winner,final_margin_pp=margin,status='Matched'))
        return pd.DataFrame(rows)

    def test_fixed_cohort_same_events_and_complemented_underdog(self):
        r=analyze(self.fixture());self.assertEqual(r['coverage'].states.iloc[0],2)
        s=r['metrics'];q=s[(s.cohort=='Competitive on Sep 5')&(s.model=='GB')]
        self.assertTrue(q.races.eq(1).all());self.assertAlmostEqual(q.brier.iloc[0],.04)
        q=r['longshots'];self.assertTrue(q.actual_wins.eq(1).all())
        self.assertAlmostEqual(q[q.model=='GB'].expected_wins.iloc[0],.2)
        self.assertAlmostEqual(q[q.model=='Market'].expected_wins.iloc[0],.05)

    def test_missing_date_removes_state_from_whole_fixed_panel(self):
        q=self.fixture();q=q.drop(q[(q.state=='AA')&(q.model=='ST')].index[:1])
        r=analyze(q);self.assertEqual(set(r['panel'].state),{'BB'})
        self.assertEqual(r['coverage'].states.iloc[0],1)

    def test_unknown_outcome_not_scored_and_cohort_not_reassigned(self):
        q=self.fixture();q.loc[q.state=='BB','final_winner']='Unavailable'
        q.loc[(q.state=='AA') & (q.check_date.dt.day==20),'market_probability']=.99
        r=analyze(q)
        self.assertEqual(set(r['panel'].state),{'AA'})
        self.assertEqual(len(r['metrics'].query('cohort=="Competitive on Sep 5"')),6)
        self.assertEqual(len(r['metrics'].query('cohort=="Long shot on Sep 5"')),0)

    def test_duplicate_or_inconsistent_event_fails(self):
        q=self.fixture()
        with self.assertRaises(ValueError):analyze(pd.concat([q,q.iloc[:1]]))
        q.loc[0,'market_probability']=.6
        with self.assertRaises(ValueError):analyze(q)

    def test_numerical_boundary_tolerance_is_not_missing_coverage(self):
        q=self.fixture();q.loc[0,'model_probability']=1+3e-12
        r=analyze(q);self.assertEqual(r['coverage'].states.iloc[0],2)
        self.assertLessEqual(r['panel'].probability.max(),1)
        q.loc[0,'model_probability']=1.01
        with self.assertRaises(ValueError):analyze(q)
