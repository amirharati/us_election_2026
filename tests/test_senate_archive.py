import sys
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import pandas as pd
import pyarrow as pa

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from download_senate_archive import fpmm_prices, select_events, scope, fetch


class ArchiveTests(unittest.TestCase):
    def test_offline_missing_partition_never_requests_network(self):
        with patch('download_senate_archive.requests.get') as get:
            with self.assertRaises(FileNotFoundError):
                fetch('test-revision','nonexistent-test-partition.parquet',offline=True)
            get.assert_not_called()

    def test_fee_direction(self):
        d=pd.DataFrame(dict(type=['Buy','Sell'],tradeAmount=['51','49'],
                            feeAmount=['1','1'],outcomeTokensAmount=['100','100']))
        prices=fpmm_prices(d)
        self.assertEqual(prices.execution_price.tolist(),[.51,.49])
        self.assertEqual(prices.price_before_fee.tolist(),[.5,.5])
        self.assertEqual(prices.fee_per_share.tolist(),[.01,.01])

    def test_zero_shares_rejected(self):
        with self.assertRaises(ValueError):
            fpmm_prices(pd.DataFrame(dict(type=['Buy'],tradeAmount=['1'],
                        feeAmount=['0'],outcomeTokensAmount=['0'])))

    def test_both_exchange_legs_and_unrelated_tokens(self):
        d=pa.table({'makerAssetId':['123','0','999'], 'takerAssetId':['0','123','0']})
        kept=select_events(d,'order_filled',[],['123'])
        self.assertEqual(kept.num_rows,2)

    def test_amm_address_case(self):
        d=pa.table({'market_id':['0xAbC','0xDEF']})
        self.assertEqual(select_events(d,'fpmm_transaction',['0xabc'],[]).num_rows,1)

    def test_funding_uses_pool_address_not_event_id(self):
        d=pa.table({'id':['137_123_4','137_125_2'],'fpmm_id':['0xAbC','0xDEF']})
        self.assertEqual(select_events(d,'fpmm_funding_addition',['0xabc'],[]).num_rows,1)
        with self.assertRaises(ValueError):
            select_events(pa.table({'id':['0xabc']}),'fpmm_funding_addition',['0xabc'],[])

    def test_scope_primary_and_runoff_are_separate(self):
        r=SimpleNamespace(category='excluded',question='Will X win the Senate primary?',
                          description='',market_id='1')
        self.assertEqual(scope(r),'primary')
        r.question='Will a major challenger win the presidential nomination?'
        r.description='A Senator might run.'
        self.assertEqual(scope(r),'excluded')
        r.market_id='247671'
        self.assertEqual(scope(r),'runoff_occurrence')


if __name__=='__main__':
    unittest.main()
