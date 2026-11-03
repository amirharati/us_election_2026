import unittest
import tempfile
from pathlib import Path
import numpy as np
import pandas as pd
import election_lab
from polymarket_model_alignment import build,publish


class AlignmentTests(unittest.TestCase):
    def fixture(self):
        markets=[];details=[];audit=[]
        for mid,state,pm,values,liq in [('1','TX',.7,{'a':.8,'b':.6},1000),('2','GA',.2,{'a':.3,'b':.7},1000),('3','NE',.1,{'a':.9},1000),('4','TX',.1,{'a':.95},999999)]:
            question=f'Winner {state} {mid}'
            markets.append(dict(market_id=mid,question=question,category='Senate race winners',liquidity=liq))
            for name,p in values.items():
                for side in ['Yes','No']:
                    details.append(dict(market_id=mid,question=question,category='Senate race winners',side=side,model=name,
                                        market_midpoint=pm if side=='Yes' else 1-pm,model_low=p if side=='Yes' else 1-p,model_high=p if side=='Yes' else 1-p,
                                        model_blocker='',spread=.02,liquidity=liq,accepting_orders=True,order_book=True,book_age_seconds=10,
                                        settlement_proxy=state=='GA',publisher_date=None,mapping_reason='test',url='https://example.test'))
                audit.append(dict(market_id=mid,model=name,state=state,model_low=p,reason='test'))
        status=dict(max_spread=.1,min_liquidity=0,max_book_age_seconds=60,catalog_status='checked online',retrieved_at='2026-09-25T00:00:00+00:00',forecast_cutoff='2026-09-25')
        return dict(catalog=dict(markets=markets),status=status),dict(settings=dict(models=['a','b']),details=pd.DataFrame(details),audit=pd.DataFrame(audit))

    def test_equal_state_weights_shared_contracts_and_common_coverage(self):
        r,s=self.fixture();x=build(r,s);o=x['overall'].set_index('model');a=x['available'].set_index('model')
        self.assertEqual(x['settings']['common_states'],2)
        self.assertEqual(len(x['comparisons']),5) # No duplicate No-side observations.
        self.assertAlmostEqual(o.loc['a','mean_abs_gap_pp'],10)
        self.assertAlmostEqual(o.loc['b','mean_abs_gap_pp'],30)
        self.assertAlmostEqual(a.loc['a','mean_abs_gap_pp'],100/3)
        self.assertEqual(x['anchors'].set_index('state').loc['TX','market_id'],'1') # Coverage wins over liquidity.
        state=x['states'].set_index('state')
        self.assertEqual(state.loc['GA','closest'],'a*');self.assertEqual(state.loc['GA','farthest'],'b*')
        self.assertEqual(state.loc['NE','closest'],'Insufficient coverage')
        self.assertEqual(set(state.loc['TX','closest'].split(', ')),{'a','b'})

    def test_stale_quotes_are_excluded_without_fabricated_rank(self):
        r,s=self.fixture();s['details']['book_age_seconds']=100
        x=build(r,s);self.assertTrue(x['comparisons'].empty)
        self.assertEqual(x['settings']['common_states'],0)
        self.assertTrue(x['overall'].mean_abs_gap_pp.isna().all())
        self.assertTrue(x['exclusions'].exclusion.str.contains('age').all())

    def test_alignment_uses_all_comparisons_not_only_opportunities(self):
        r,s=self.fixture();s['external']={'Publisher':{'races':{'WV':{}}}};s['summary']=pd.DataFrame({'initial_candidate':[False]})
        x=build(r,s);self.assertEqual(x['settings']['common_states'],2)
        self.assertEqual(x['settings']['unrepresented_states'],['WV'])
        s['details'].loc[s['details'].model.eq('b'),'model_blocker']='old model'
        x=build(r,s);self.assertEqual(x['settings']['common_states'],0)
        self.assertTrue(x['overall'].mean_abs_gap_pp.isna().all())

    def test_report_assets_include_nested_report_dependencies(self):
        r,s=self.fixture();x=build(r,s)
        with tempfile.TemporaryDirectory() as temp:
            lines=publish(x,Path(temp));body='\n'.join(lines)
            for name in ['model_market_alignment.md','model_market_alignment.png','alignment_comparisons.parquet','alignment_anchors.parquet','alignment_exclusions.parquet','alignment_settings.json']:
                self.assertTrue((Path(temp)/name).exists());self.assertIn(name,body)

if __name__=='__main__':unittest.main()
