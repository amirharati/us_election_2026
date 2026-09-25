from pathlib import Path
import json,tempfile,unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
import election_lab as lab
from predictive_distributions import PredictiveDistributions
import live_polymarket as poly


class PredictiveTests(unittest.TestCase):
    def distribution(self):
        d=PredictiveDistributions.__new__(PredictiveDistributions)
        d.arrays={'Bayesian':dict(mean=np.array([0.]),covariance=np.array([[1.]]),geographies=['TX'],samples=np.array([[-2.],[0.],[2.]])),
                  'Matched Student-t (df5)':dict(geographies=['TX'],samples=np.array([[-4.],[0.],[1.],[3.]]))}
        d.config={'component_weights':{'Bayesian':.25,'Matched Student-t (df5)':.75}}
        d.pred=pd.DataFrame([dict(model=m,geography='TX',margin_pp=x) for m,x in [('Four-model mixture',0),('Mixture + polling 10%',2)]])
        return d

    def test_analytic_gaussian_bands_and_tails(self):
        d=self.distribution()
        p=lambda a,b:d.margin_probability('Bayesian','TX',a,b)['probability']
        self.assertAlmostEqual(p(-1,1),.6826894921370859)
        self.assertGreater(p(10,11),0)
        self.assertEqual(p(-np.inf,np.inf),1)
        self.assertAlmostEqual(sum(p(a,b) for a,b in zip([-np.inf,-1,0,1],[-1,0,1,np.inf])),1)

    def test_actual_draws_weighting_shift_and_endpoints(self):
        d=self.distribution();st='Matched Student-t (df5)'
        p=lambda m,a,b,**kw:d.margin_probability(m,'TX',a,b,**kw)['probability']
        self.assertEqual(p(st,0,1),.25)
        self.assertEqual(p(st,0,1,lower_closed=False,upper_closed=True),.25)
        self.assertEqual(p(st,0,np.inf,lower_closed=False),.5)
        self.assertAlmostEqual(p('Four-model mixture',0,1),.25/3+.75/4)
        self.assertAlmostEqual(p('Mixture + polling 10%',2,3),p('Four-model mixture',0,1))
        for m in [st,'Four-model mixture','Mixture + polling 10%']:
            self.assertAlmostEqual(sum(p(m,a,b) for a,b in zip([-np.inf,0,1,2], [0,1,2,np.inf])),1)
        del d.arrays[st]['samples']
        with self.assertRaisesRegex(ValueError,'missing'):p(st,0,1)

    def test_market_formula_and_reflected_republican_band(self):
        d=self.distribution()
        context=dict(distributions=d,model_name='Matched Student-t (df5)',mix=pd.DataFrame([{'geography':'TX'}]).set_index('geography'),
            review={'TX':dict(scalar_seat_mapping_ready=True,candidates=[{'party':'DEM'},{'party':'REP'}])})
        row=dict(event='Texas Senate margin',question='Will the Republican Party candidate win by 0%-4%?',category='Senate margins / relative results',rules_id='r')
        rules={'r':'margin between top two candidates; boundary goes to higher margin bracket'}
        result=poly.assess_market(row,rules,context)
        self.assertEqual(result['model_low'],.25) # -4 excluded; zero included.
        self.assertEqual(result['model_low'],result['model_high'])
        self.assertEqual(result['event_formula'],'P(-4 < M <= -0)')
        self.assertIsNone(poly.assess_market(row,{'r':'Unrecognized rules'},context)['model_low'])

    def test_download_has_no_model_dependency_and_snapshot_keeps_time(self):
        catalog=dict(markets=[dict(accepting_orders=True,order_book=True,yes_token='y',no_token='n')],retrieved_at='2026-09-24T00:00:00+00:00')
        with tempfile.TemporaryDirectory() as tmp,patch.object(poly,'CACHE',Path(tmp)),patch.object(poly,'model_context',side_effect=AssertionError('model called')),patch.object(poly,'discover',return_value=(catalog,'checked online')),patch.object(poly,'fetch_books',return_value=({'y':{}},{'status':'checked online'})):
            snapshot=poly.download_markets()
            with patch.object(poly,'request',side_effect=AssertionError('network called')):
                self.assertEqual(snapshot,poly.load_market_snapshot())
            path=Path(tmp)/'market_snapshot.json.gz'
            import gzip
            env=json.loads(gzip.decompress(path.read_bytes()));env['payload']['retrieved_at']='changed'
            path.write_bytes(gzip.compress(json.dumps(env).encode()))
            with self.assertRaisesRegex(ValueError,'checksum'):poly.load_market_snapshot()

    def test_saved_live_draws_match_mixture_probabilities(self):
        run=lab.latest_run('live');d=PredictiveDistributions(run)
        for model in ['Four-model mixture','Mixture + polling 10%']:
            rows=d.pred[d.pred.model.eq(model)]
            for row in rows.itertuples():
                result=d.margin_probability(model,row.geography,0,np.inf,lower_closed=False)
                self.assertAlmostEqual(result['probability'],row.p_dem,places=10)

    def test_saved_snapshot_evaluation_never_downloads_or_runs_models(self):
        from polymarket_scanner import scan
        run=lab.latest_run('live');snapshot=poly.load_market_snapshot()
        with patch.object(poly,'download_markets',side_effect=AssertionError('download called')),patch.object(lab,'live_forecast',side_effect=AssertionError('inference called')):
            research=poly.analyze(run,snapshot=snapshot)
            research['status']['catalog_age_seconds']=10000
            result=scan(research,run)
            self.assertFalse(result['summary'].initial_candidate.any())
            self.assertTrue(result['details'].model_low.eq(result['details'].model_high).all())
            research['status']['forecast_manifest_sha256']='wrong'
            with self.assertRaisesRegex(ValueError,'Forecast changed'):scan(research,run)
