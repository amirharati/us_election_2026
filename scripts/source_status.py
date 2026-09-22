"""Readable source receipts without displaying missing error fields as NaN."""
import pandas as pd


def format_source_status(sources):
    rows=[]
    for source in sources:
        dates=source.get('poll_latest_dates') or {}
        rows.append(dict(source=source['source'],
            acquisition_status=source.get('acquisition_status') or 'None',
            checked_at=source.get('checked_at') or 'None',
            poll_latest_dates='; '.join(f'{k}: {v}' for k,v in dates.items()) or 'None',
            failure_type=source.get('failure_type') or 'None',
            failure_detail=source.get('failure_detail') or ''))
    return pd.DataFrame(rows).fillna('')
