import unittest
from unittest.mock import patch, Mock
from pathlib import Path
import tempfile
import numpy as np
import pandas as pd
import election_lab
import live_polymarket as poly
from polymarket_scanner import scan, model_table, table, selected_predictions, DEFAULT_MODELS
from polymarket_debug_view import build as debug_build, html as debug_html, compact_table, grouped_table, MODEL_CODES

class ScannerTests(unittest.TestCase):
    def test_models_use_own_probabilities_and_friction_and_no_complement(self):
        with tempfile.TemporaryDirectory() as tmp:
            context=dict(run=Path(tmp),pred=pd.DataFrame([dict(model=n,geography='TX',p_dem=p) for n,p in [('a',.8),('b',.4)]]))
            market=dict(market_id='1',question='Test',category='Senate race winners',url='link',yes_token='y',no_token='n',fees_enabled=False,fee_rate=0,fee_exponent=1,accepting_orders=True,order_book=True,liquidity=9999)
            books={t:dict(asks=[dict(price='.5',size='100')],bids=[dict(price='.49',size='100')]) for t in ['y','n']}
            research=dict(catalog={'markets':[market],'rules':{}},books=books,status=dict(shares=10,catalog_status='checked online',forecast_age_days=1,max_forecast_age_days=3,max_spread=.1,min_liquidity=2000,forecast_source_review='pending review'))
            def mapping(row,rules,ctx):
                p=ctx['mix'].loc['TX'].p_dem
                return dict(model_low=p,model_high=p,state='TX',mapping='Conditional comparison',reason='test')
            with patch.object(poly,'model_context',return_value=context),patch.object(poly,'configuration',return_value={'component_weights':{'a':.5,'b':.5}}),patch.object(poly,'assess_market',side_effect=mapping):
                r=scan(research,Path(tmp),models=['a','b'],friction_cents=2,probability_haircut_pp=3)
                d=r['details'].set_index(['model','side'])
                self.assertAlmostEqual(d.loc[('a','Yes'),'stressed_edge_pp'],25)
                self.assertAlmostEqual(d.loc[('a','No'),'model_low'],.2)
                self.assertAlmostEqual(d.loc[('b','Yes'),'model_low'],.4)
                self.assertEqual(len(r['audit']),2)
                grouped=debug_build(r)
                self.assertEqual(len(grouped),4)
                gr=grouped.set_index(['model','side'])
                self.assertEqual(gr.loc[('a','Yes'),'status'],'Positive after stress')
                self.assertEqual(gr.loc[('a','No'),'status'],'Negative expected profit')
                self.assertAlmostEqual(gr.loc[('a','Yes'),'loss_amount'],5.0)
                self.assertAlmostEqual(gr.loc[('a','Yes'),'win_profit'],5.0)
                self.assertAlmostEqual(gr.loc[('a','Yes'),'reward_to_risk'],1.0)
                self.assertAlmostEqual(gr.loc[('a','Yes'),'loss_probability_low'],.2)
                self.assertIn('#fbe3e3',debug_html(grouped))
                self.assertEqual(len(compact_table(grouped).columns),5)
                self.assertEqual(len(set(MODEL_CODES.values())),len(MODEL_CODES))
                shown_pairs=grouped_table(grouped)
                self.assertEqual(len(shown_pairs.columns),5)
                self.assertEqual(shown_pairs['Model / side'].tolist(),['a / Y','a / N','b / Y','b / N'])
                h=debug_html(grouped)
                self.assertNotIn('<select',h)
                self.assertNotIn('<script',h)
                self.assertNotIn('overflow-x:auto',h)
                self.assertIn('a / Y',h);self.assertIn('a / N',h)
                missing={**r,'details':r['details'][r['details'].model.ne('b')]}
                self.assertEqual(debug_build(missing).query("model == 'b'").status.unique().tolist(),['Unavailable'])
                flagged=grouped.copy();flagged['settlement_proxy']=True
                self.assertTrue(compact_table(flagged)['Status'].str.endswith('*').all())
                self.assertIn('#fff2cc',debug_html(flagged))
                self.assertIn('a, b:',debug_html(flagged))
                shown=model_table(r,'1','Yes').set_index('Model')
                self.assertAlmostEqual(shown.loc['a','Entry price (¢/share)'],50)
                self.assertAlmostEqual(shown.loc['a','Total budget for 10 shares ($)'],5.0)
                self.assertEqual(shown.loc['a','Expected net profit ($)'],'3.00')
                self.assertAlmostEqual(shown.loc['a','Stressed expected net profit ($)'],2.5)
                self.assertEqual(shown.loc['a','Expected return on budget (%)'],'60.00')
                self.assertIn('Lowest stressed profit model',table(r))
                self.assertAlmostEqual(shown.loc['a','Market midpoint (%)'],49.5)
                self.assertAlmostEqual(shown.loc['a','Purchase break-even probability (%)'],50)
                self.assertEqual(shown.loc['a','Model versus purchase cost'],'Model lower bound exceeds cost')
                self.assertEqual(shown.loc['b','Model versus purchase cost'],'Model upper bound is below cost')
                self.assertTrue(r['summary'].initial_candidate.all())
                self.assertTrue(r['summary'].core_models_positive.eq(1).all())
                high_friction=scan(research,Path(tmp),models=['a','b'],friction_cents=90)
                pd.testing.assert_series_equal(r['details'].edge_low_pp,high_friction['details'].edge_low_pp)
                self.assertTrue(high_friction['summary'].initial_candidate.any())
                self.assertTrue(high_friction['details'].stressed_edge_pp.lt(0).all())
                self.assertFalse(debug_build(high_friction).empty)
                self.assertAlmostEqual(d.loc[('a','Yes'),'friction_only_edge_low_pp'],28)
                self.assertAlmostEqual(d.loc[('a','Yes'),'probability_only_edge_low_pp'],27)
                research['status']['catalog_status']='offline snapshot'
                self.assertFalse(scan(research,Path(tmp),models=['a','b'])['summary'].initial_candidate.any())
    def test_available_winners_are_exposed_with_explicit_settlement_conditions(self):
        dist=Mock();dist.margin_probability.return_value=dict(probability=.88,probability_kind='Full simulations')
        def estimate(state,question,policy):
            ctx=dict(mix=pd.DataFrame({'geography':[state]}).set_index('geography'),review={state:policy},distributions=dist)
            return poly.assess_market(dict(event=question,question=question,category='Senate race winners',rules_id='r'),{'r':'Final election, including any runoffs.'},ctx)
        two=[dict(name='Jon Ossoff',party='DEM'),dict(name='Mike Collins',party='REP')]
        ga=estimate('GA','Will the Democrats win the Georgia Senate race in 2026?',dict(rule='majority_runoff',scalar_seat_mapping_ready=False,candidates=two))
        self.assertEqual(ga['model_low'],.88);self.assertTrue(ga['settlement_proxy']);self.assertIn('Runoff',ga['reason'])
        ak=estimate('AK','Will the Democrats win the Alaska Senate race in 2026?',dict(rule='rcv',candidates=two))
        self.assertEqual(ak['model_low'],.88);self.assertIn('Ranked-choice',ak['reason'])
        co=estimate('CO','Will the Democrats win the Colorado Senate race in 2026?',dict(rule='plurality',candidates=[]))
        self.assertEqual(co['model_low'],.88);self.assertIn('unreviewed',co['reason'])
        ne=dict(rule='plurality',candidates=[dict(name='Dan Osborn',party='IND'),dict(name='Pete Ricketts',party='REP')])
        self.assertEqual(estimate('NE','Will Dan Osborn win the Nebraska Senate race in 2026?',ne)['model_low'],.88)
        self.assertIsNone(estimate('NE','Will the Democrats win the Nebraska Senate race in 2026?',ne)['model_low'])
        mt=dict(rule='plurality',candidates=[dict(name='Bodnar',party='IND'),dict(name='Bankhead',party='DEM'),dict(name='Alme',party='REP')])
        self.assertAlmostEqual(estimate('MT','Will the Republicans win the Montana Senate race in 2026?',mt)['model_low'],.12)
        self.assertIsNone(estimate('MT','Will an Independent win the Montana Senate race in 2026?',mt)['model_low'])
        self.assertIsNone(estimate('MT','Will the Democrats win the Montana Senate race in 2026?',mt)['model_low'])

    def test_negative_or_nonfinite_assumptions_rejected(self):
        for value in [-1,np.nan,np.inf]:
            with self.assertRaises(ValueError):scan({},Path('.'),friction_cents=value)
    def test_control_uses_selected_model(self):
        context=dict(mix=pd.DataFrame(),review={},model_name='Other',seats=pd.DataFrame([dict(model='Four-model mixture',cycle=2026,p_D_control=.8),dict(model='Other',cycle=2026,p_D_control=.3)]))
        row=dict(event='Which party will win the Senate?',question='Democratic Party',category='Senate control',rules_id='r')
        self.assertEqual(poly.assess_market(row,{'r':''},context)['model_low'],.3)

    def test_default_scanner_selects_only_four_requested_models(self):
        self.assertEqual(DEFAULT_MODELS,('Bayesian','Matched Student-t (df5)','Four-model mixture','Mixture + polling 10%'))
        pred=pd.DataFrame({'model':[*DEFAULT_MODELS,'Older Gaussian','Mixture + polling 20%'],'geography':['TX']*6})
        selected,names=selected_predictions(pred)
        self.assertEqual(set(selected.model),set(DEFAULT_MODELS))
        self.assertEqual(names,list(DEFAULT_MODELS))
        self.assertEqual(len(pred),6)
        with self.assertRaisesRegex(ValueError,'missing'):selected_predictions(pred,['Missing model'])
        with self.assertRaisesRegex(ValueError,'distinct'):selected_predictions(pred,[])
