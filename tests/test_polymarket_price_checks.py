import unittest
import pandas as pd
import election_lab
from polymarket_price_checks import scan_pairs

class PriceCheckTests(unittest.TestCase):
    def fixture(self):
        now=str(int(pd.Timestamp.now(tz='UTC').timestamp()*1000))
        books={side:dict(timestamp=now,bids=[dict(price='.4',size='100')],asks=[dict(price='.45',size='100')]) for side in ['y','n']}
        r=dict(market_id='1',question='Test',url='link',yes_token='y',no_token='n',accepting_orders=True,order_book=True,fees_enabled=False,fee_rate=0,fee_exponent=1)
        return dict(status=dict(shares=100,catalog_status='checked online'),catalog=dict(markets=[r]),books=books)
    def test_same_contract_payout_and_friction_on_both_legs(self):
        r=self.fixture();q=scan_pairs(r,friction_cents=2).iloc[0]
        self.assertTrue(q.candidate);self.assertAlmostEqual(q.total_cost,94);self.assertAlmostEqual(q.snapshot_profit,6)
        self.assertFalse(scan_pairs(r,friction_cents=6).iloc[0].candidate)
    def test_missing_depth_stale_and_duplicate_tokens_block(self):
        for change in ['depth','stale','tokens','offline','missing']:
            r=self.fixture()
            if change=='depth':r['books']['n']['asks'][0]['size']='99'
            if change=='stale':r['books']['n']['timestamp']='0'
            if change=='tokens':r['catalog']['markets'][0]['no_token']='y'
            if change=='offline':r['status']['catalog_status']='offline snapshot'
            if change=='missing':del r['books']['n']
            self.assertFalse(scan_pairs(r).iloc[0].candidate,change)
    def test_fees_can_remove_apparent_mismatch(self):
        r=self.fixture()
        for b in r['books'].values():b['asks'][0]['price']='.499'
        self.assertTrue(scan_pairs(r,friction_cents=0).iloc[0].candidate)
        r['catalog']['markets'][0].update(fees_enabled=True,fee_rate=.04)
        self.assertFalse(scan_pairs(r,friction_cents=0).iloc[0].candidate)
