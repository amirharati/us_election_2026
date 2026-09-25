from pathlib import Path
import sys,unittest,tempfile,json
from unittest.mock import patch
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import election_lab
from live_polymarket import (margin_band,fill_book,normalize,category,assess_market,comparison_table)

class PolymarketTests(unittest.TestCase):
    def test_margin_band_parsing(self):
        self.assertEqual(margin_band('Will the Republican Party candidate win by 3%-6%?'),(-6,-3))
        self.assertEqual(margin_band('Will the Democratic Party candidate win by 12% or more?'),(12,np.inf))
        self.assertIsNone(margin_band('Will X win?'))

    def test_depth_uses_real_asks_and_charges_fees(self):
        book=dict(bids=[dict(price='.2',size='100'),dict(price='.4',size='50')],asks=[dict(price='.6',size='80'),dict(price='.5',size='20')],min_order_size='5')
        row=dict(fees_enabled=True,fee_rate=.04,fee_exponent=1)
        q=fill_book(book,row,100)
        self.assertEqual(q['best_bid'],.4);self.assertEqual(q['best_ask'],.5)
        self.assertAlmostEqual(q['avg_cost'],.58+.00968)
        self.assertEqual(fill_book(book,row,101)['quote_status'],'insufficient displayed ask depth')
        self.assertEqual(fill_book(book,{**row,'fee_rate':None},100)['quote_status'],'unknown fee schedule')
        self.assertEqual(fill_book(book,row,2)['quote_status'],'below minimum order size')
        self.assertEqual(fill_book({**book,'bids':[dict(price='.7',size='10')]},row,10)['quote_status'],'crossed book')

    def test_normalize_aligns_yes_no_tokens_and_ignores_placeholders(self):
        market=dict(id='m',active=True,closed=False,question='Will Democrats win?',slug='d',outcomes='["No","Yes"]',clobTokenIds='["no-token","yes-token"]',outcomePrices='["0.4","0.6"]',description='Rules')
        event=dict(id='e',title='Texas Senate Election Winner',slug='tx',tags=[],markets=[market,{**market,'id':'placeholder','active':False}])
        rows,rules=normalize([event]);self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['yes_token'],'yes-token');self.assertEqual(rows[0]['indicative_yes'],.6)
        self.assertEqual(category('Texas State Senate Winner 2026?'),'State legislatures')
        self.assertEqual(category('Texas Senate odds hit 80%?'),'Market-price / forecast derivatives')

    def test_first_round_and_independent_rules_are_not_silently_priced(self):
        row=dict(event='Alaska Senate Election Margin of Victory (First Round)',question='Will the Democratic Party win by 0%-3%?',category='Senate margins / relative results',rules_id='r')
        context=dict(distributions=None,mix=pd.DataFrame({'geography':['AK'],'p_dem':[.8]}).set_index('geography'),review={'AK':{'scalar_seat_mapping_ready':False,'candidates':[]}})
        self.assertIn('First-round',assess_market(row,{'r':'first round'},context)['reason'])
        row.update(event='Alaska Senate Election Winner',category='Senate race winners',question='Will Unknown Candidate win the Alaska Senate race in 2026?')
        self.assertIsNone(assess_market(row,{'r':'final election'},context)['model_low'])

    def test_empty_shortlist_is_displayable(self):
        q=pd.DataFrame([dict(screen='Not shortlisted')]);self.assertIn('Status',comparison_table(dict(comparisons=q)))

    def test_catalog_failure_is_stale_and_pagination_cap_is_not_complete(self):
        import live_polymarket as poly
        with tempfile.TemporaryDirectory() as temp,patch.object(poly,'CACHE',Path(temp)),patch.object(poly,'RESULT',Path(temp)/'none'):
            payload=dict(retrieved_at='2020-01-01T00:00:00+00:00',markets=[],rules={})
            (Path(temp)/'catalog.json').write_text(json.dumps(dict(payload=payload,sha256=poly.digest(payload))))
            with patch.object(poly,'request',side_effect=RuntimeError('network unavailable')):
                saved,status=poly.discover(force=True)
            self.assertEqual(saved,poly.restrict_catalog(payload));self.assertTrue(status.startswith('STALE'))
            (Path(temp)/'catalog.json').unlink()
            with patch.object(poly,'request',return_value=[dict(id=str(i)) for i in range(100)]):
                with self.assertRaisesRegex(RuntimeError,'pagination cap'):
                    poly.discover(force=True,max_pages=1)
            self.assertFalse((Path(temp)/'catalog.json').exists())

    def test_offline_books_are_never_presented_as_live(self):
        from live_polymarket import fetch_books
        books,status=fetch_books(['token'],offline=True)
        self.assertEqual(books,{})
        self.assertIn('offline',status['status'])

    def test_senate_scope_applies_to_legacy_offline_cache(self):
        import live_polymarket as poly
        keep=['Texas Senate Election Winner','Texas Senate Election Margin of Victory','Which party will win the Senate in 2026?', 'Republican Senate seats in 2026', 'Senate Three-Way Combo: Texas, Michigan, Maine']
        reject=['House Election Winner 2026','Senate and House combo','Texas State Senate Election Winner','Texas Senate Primary Winner','Senate turnout margin','Senate odds hit 80%?', 'Senate Election Winner 2028', 'Senate or Governor Election Winner', 'Senate majority leader']
        for title in keep:self.assertTrue(poly.relevant({'title':title}),title)
        for title in reject:self.assertFalse(poly.relevant({'title':title}),title)
        rows=[dict(event=t,market_id=str(i),rules_id=str(i)) for i,t in enumerate(keep+reject)]
        payload=dict(retrieved_at='2020-01-01T00:00:00+00:00',markets=rows,rules={r['rules_id']:'rule' for r in rows})
        with tempfile.TemporaryDirectory() as temp,patch.object(poly,'CACHE',Path(temp)),patch.object(poly,'RESULT',Path(temp)/'none'):
            (Path(temp)/'catalog.json').write_text(json.dumps(dict(payload=payload,sha256=poly.digest(payload))))
            saved,status=poly.discover(offline=True)
        self.assertEqual([r['event'] for r in saved['markets']],keep)
        self.assertEqual(len(saved['rules']),len(keep))
        self.assertEqual(saved['scope'],poly.SCOPE)
        self.assertEqual(status,'offline snapshot')
