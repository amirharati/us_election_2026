import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd
import election_lab
import polymarket_external as ex
import live_polymarket as poly
from polymarket_scanner import scan
from polymarket_debug_view import build, html

NOW=datetime(2026,9,25,tzinfo=timezone.utc)


def page(data):
    return '<script>self.__next_f.push('+json.dumps([1,json.dumps(data)])+')</script>'


def snap():
    return dict(model=ex.RT,published_date='2026-09-24',refresh_status='checked online',control=.7,seat_bins=None,source_url='https://publisher.test',races={
        'NE':dict(candidates=[dict(name='Osborn',party='DEM',p=.3),dict(name='Ricketts',party='REP',p=.7)],published_date='2026-09-24',source_url='https://publisher.test/ne',market_weight=None)})


def market(q,cat='Senate race winners'):
    return dict(question=q,event='Nebraska Senate election',category=cat,rules_id='r')


REVIEW={'NE':{'candidates':[dict(name='Dan Osborn',party='IND'),dict(name='Pete Ricketts',party='REP')]}}


class ExternalTests(unittest.TestCase):
    def assess(self,q,s=None,cat='Senate race winners',rule='Final winner'):
        return ex.assess(market(q,cat),{'r':rule},s or snap(),REVIEW,now=NOW)

    def test_independent_is_not_democrat_and_absence_is_not_zero(self):
        self.assertIsNone(self.assess('Will the Democrats win the Nebraska Senate race in 2026?')['model_low'])
        self.assertEqual(self.assess('Will an independent win the Nebraska Senate race in 2026?')['model_low'],.3)
        self.assertEqual(self.assess('Will Dan Osborn win the Nebraska Senate race in 2026?')['model_low'],.3)
        self.assertEqual(self.assess('Will the Republicans win the Nebraska Senate race in 2026?')['model_low'],.7)
        self.assertIsNone(self.assess('Will Ann Other win the Nebraska Senate race in 2026?')['model_low'])

    def test_candidate_replacement_and_first_round_rejected(self):
        s=snap();s['races']['NE']['candidates'][0]['name']='Old Candidate'
        self.assertIn('roster',self.assess('Will the Republicans win the Nebraska Senate race in 2026?',s)['reason'])
        self.assertIn('final-election',self.assess('Will the Republicans win the Nebraska Senate race in 2026?',rule='First round')['reason'])

    def test_dates_failures_and_missing_distributions(self):
        q='Will the Republicans win the Nebraska Senate race in 2026?'
        for date in ['2026-09-01','2026-09-26']:
            s=snap();s['races']['NE']['published_date']=date
            self.assertIsNone(self.assess(q,s)['model_low'])
        s=snap();s['refresh_status']='stale after failure'
        self.assertIsNone(self.assess(q,s)['model_low'])
        self.assertIn('no full margin',self.assess('margin',cat='Senate margins / relative results')['reason'])
        self.assertIn('no seat-count',self.assess('seats',cat='Senate seat counts')['reason'])

    def test_histogram_not_expected_seats_prices_exact_and_threshold(self):
        s=snap();s.update(model=ex.DD,seat_bins=[dict(D=51,R=49,count=70),dict(D=50,R=50,count=30)],simulation_draws=100)
        for q,p in [('exactly 49',.7),('49 or fewer',.7),('50 or more',.3)]:
            r=self.assess(f'Will the Republican Party hold {q} Senate seats after the 2026 midterm elections?',s,'Senate seat counts')
            self.assertEqual(r['model_low'],p)
            self.assertEqual(r['simulation_draws'],100)
            self.assertIn('market inputs',r['reason'])
        r=self.assess('Will the Republican Party control the Senate after the 2026 Midterm elections?',s,'Senate control')
        self.assertAlmostEqual(r['model_low'],.3)

    def test_ddhq_parser_validates_histogram_and_party_semantics(self):
        data={'overviews':[{'forecast':{'year':2026,'updatedAt':'2026-09-25 12:00','parties':[dict(shortAbbrev='D',partyId=1,winProbability=.7),dict(shortAbbrev='R',partyId=2,winProbability=.3)]}}],
              'simulations':[dict(count=7,parties=[dict(partyId=1,seats=51),dict(partyId=2,seats=49)]),dict(count=3,parties=[dict(partyId=1,seats=50),dict(partyId=2,seats=50)])]}
        d=ex.parse_ddhq_national(page(data));self.assertEqual(d['simulation_draws'],10);self.assertAlmostEqual(d['expected_D'],50.7)
        data['simulations'][0]['count']=1
        with self.assertRaisesRegex(ValueError,'disagrees'):ex.parse_ddhq_national(page(data))

    def test_display_aliases_and_party_aggregate_not_candidate(self):
        policy={'candidates':[dict(name='James Risch',party='REP'),dict(name='Ben Ray Luján',party='DEM')]}
        rows,_=ex.normalized_candidates({'candidates':[dict(name='Jim Risch',party='REP',p=.9),dict(name='Ben Ray Lujan',party='DEM',p=.1)]},policy)
        self.assertEqual(rows[0]['name'],'James Risch')
        _,notes=ex.normalized_candidates({'candidates':[dict(name='Jim Risch',party='REP',p=.9)]},policy)
        self.assertIn('Ben Ray Luján',' '.join(notes))
        s=snap();s['races']['NE']['candidates'][1].update(name='',members=['Pete Ricketts','Another Republican'])
        self.assertEqual(self.assess('Will the Republicans win the Nebraska Senate race in 2026?',s)['model_low'],.7)
        self.assertIsNone(self.assess('Will Pete Ricketts win the Nebraska Senate race in 2026?',s)['model_low'])
        self.assertEqual(self.assess('Will Dan Osborn win the Nebraska Senate race in 2026?',s)['model_low'],.3)

    def test_snapshot_checksum(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'snapshot.json';d={'a':1};p.write_text(json.dumps(dict(payload=d,sha256=ex.digest(d))))
            self.assertEqual(ex.read_snapshot(p),d)
            p.write_text(json.dumps(dict(payload={'a':2},sha256=ex.digest(d))))
            with self.assertRaisesRegex(ValueError,'checksum'):ex.read_snapshot(p)

    def test_external_uses_same_cost_stress_and_side_complement(self):
        with tempfile.TemporaryDirectory() as temp:
            context=dict(run=Path(temp),review=REVIEW,pred=pd.DataFrame([dict(model='local',geography='NE',p_dem=.4)]))
            row={**market('Will an independent win the Nebraska Senate race in 2026?'), 'market_id':'1','url':'https://market.test','yes_token':'y','no_token':'n','fees_enabled':False,'fee_rate':0,'fee_exponent':1,'accepting_orders':True,'order_book':True,'liquidity':9999}
            books={t:dict(asks=[dict(price='.2',size='100')],bids=[dict(price='.19',size='100')]) for t in ['y','n']}
            research=dict(catalog=dict(markets=[row],rules={'r':'Final winner'}),books=books,status=dict(shares=10,catalog_status='checked online',forecast_age_days=1,max_forecast_age_days=3,max_spread=.1,min_liquidity=2000,forecast_source_review='reviewed'))
            s=snap();s['published_date']=datetime.now(timezone.utc).date().isoformat();s['races']['NE']['published_date']=s['published_date']
            with patch.object(poly,'model_context',return_value=context),patch.object(poly,'configuration',return_value={'component_weights':{'local':1}}),patch.object(poly,'assess_market',return_value=dict(model_low=.4,model_high=.4,state='NE',mapping='test',reason='local')):
                result=scan(research,Path(temp),models=['local'],external={ex.RT:s},friction_cents=2,probability_haircut_pp=3)
                d=result['details'].set_index(['model','side'])
                self.assertAlmostEqual(d.loc[(ex.RT,'Yes'),'effective_cost'],.2)
                self.assertAlmostEqual(d.loc[(ex.RT,'Yes'),'edge_low_pp'],10)
                self.assertAlmostEqual(d.loc[(ex.RT,'Yes'),'stressed_edge_pp'],5)
                self.assertAlmostEqual(d.loc[(ex.RT,'No'),'model_low'],.7)
                self.assertTrue(pd.isna(d.loc[(ex.RT,'Yes'),'margin_lo95_pp']))
                rendered=html(build(result));self.assertIn('RTWH / Y',rendered);self.assertIn('retains IND',rendered)
                research['status']['forecast_age_days']=20
                result=scan(research,Path(temp),models=['local'],external={ex.RT:s})
                grouped=build(result)
                self.assertTrue(grouped[grouped.model.eq('local')].status.eq('Unavailable').all())
                self.assertFalse(grouped[grouped.model.eq(ex.RT)].status.eq('Unavailable').any())

if __name__=='__main__':unittest.main()
