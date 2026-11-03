"""Download/rebuild the 2022/2024 Senate research inputs, then regenerate reports.

Run from any directory. Data stays Git-ignored. No AI calls or retraining.
The optional original price archive requires the user's SSH host; the public
trade archive and ordinary daily price collection do not require that host.
"""
import argparse
from download_polymarket_history import collect as market_history
from download_backtest_forecasts import collect as publisher_history
from download_senate_archive import collect as trade_archive, collect_remote_prices, OUT
from polymarket_backtest import build


def prepare(offline=False, remote_prices=None):
    if offline and remote_prices:
        raise ValueError('Offline rebuild cannot download remote prices')
    market_history(offline=offline)
    publishers=publisher_history(offline=offline)
    if not {'RTWH','538'}.issubset(set(publishers.model.unique())):
        raise RuntimeError('Publisher download incomplete; inspect publisher_status.parquet and rerun.')
    trade_archive(offline=offline)
    if remote_prices:
        import pandas as pd
        collect_remote_prices(remote_prices,pd.read_parquet(OUT/'markets.parquet'))
        trade_archive(offline=True)  # Update the report with the optional source.
    # Extended publisher retrieval uses reviewed market mappings from the base
    # analysis, then the second cached build includes every collected series.
    build()
    from polymarket_signal_publishers import collect_extended
    collect_extended(offline=offline)
    build()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline',action='store_true',help='Rebuild from existing caches without network calls.')
    parser.add_argument('--remote-prices',help='Optional SSH host (e.g. idea) for the original saved price histories.')
    args=parser.parse_args()
    prepare(offline=args.offline,remote_prices=args.remote_prices)
