import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from historical_market_prices import replay_pool

class PoolReplayTest(unittest.TestCase):
    def test_chain_order_net_fees_and_drained_pool(self):
        events=[dict(id='137_1_0',kind='add',timestamp=1,amountsAdded=['100','100']),
            dict(id='137_2_0',kind='Buy',timestamp=2,tradeAmount='12',feeAmount='2',outcomeIndex=0,outcomeTokensAmount='20'),
            dict(id='137_3_0',kind='Sell',timestamp=3,tradeAmount='8',feeAmount='2',outcomeIndex=0,outcomeTokensAmount='20'),
            dict(id='137_4_0',kind='remove',timestamp=4,amountsRemoved=['100','100'])]
        rows,reserve=replay_pool(list(reversed(events)))
        self.assertEqual(reserve,[0,0]);self.assertEqual(rows[0]['price_first'],.5)
        self.assertEqual(rows[1]['price_first'],.55);self.assertEqual(rows[2]['price_first'],.5)
        self.assertTrue(np.isnan(rows[-1]['price_first']))

    def test_missing_funding_fails(self):
        with self.assertRaises(ValueError):replay_pool([dict(id='137_1_0',kind='remove',timestamp=1,amountsRemoved=['1','1'])])

    def test_zero_event_does_not_refresh_price(self):
        rows,_=replay_pool([dict(id='137_1_0',kind='add',timestamp=1,amountsAdded=['100','100']),dict(id='137_2_0',kind='add',timestamp=2,amountsAdded=['0','0'])])
        self.assertEqual(len(rows),1)
