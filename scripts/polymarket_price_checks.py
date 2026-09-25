"""Model-free same-contract Yes/No purchase checks. No orders are submitted."""
import math
import pandas as pd

METHOD = ('This check buys equal quantities of Yes and No on the same binary contract. '
          'Their combined settlement payout is $1 per pair under normal settlement. '
          'A snapshot mismatch exists only when ask-depth costs, taker fees and friction on BOTH legs total less than $1. '
          'This does not use an election model. It is not an executable guarantee: both legs must fill, quotes can change, and settlement/platform risk remains. '
          'Other relationships, such as winner versus margin bands or seat totals versus control, are not tested without verified matching settlement rules.')


def scan_pairs(research,friction_cents=2.,max_book_age_seconds=120.,max_book_skew_seconds=30.):
    import live_polymarket as poly
    if not all(math.isfinite(x) and x>=0 for x in [friction_cents,max_book_age_seconds,max_book_skew_seconds]):
        raise ValueError('Price-check settings must be finite and nonnegative')
    shares=research['status']['shares'];now=pd.Timestamp.now(tz='UTC');rows=[]
    for r in research['catalog']['markets']:
        blocked=[];quotes=[];times=[]
        if research['status']['catalog_status'] not in ['checked online','recent catalog cache']:blocked.append('Catalog is offline or stale.')
        if not r['accepting_orders'] or not r['order_book']:blocked.append('Contract is not accepting book orders.')
        if not r['yes_token'] or not r['no_token'] or r['yes_token']==r['no_token']:blocked.append('Distinct Yes and No tokens are required.')
        for side in ['yes','no']:
            book=research['books'].get(r[side+'_token'])
            quote=poly.fill_book(book,r,shares) if book else dict(quote_status='book unavailable',avg_cost=None)
            quotes.append(quote)
            if quote['quote_status']!='quoted':blocked.append(side.title()+': '+quote['quote_status']+'.')
            try:
                stamp=pd.to_datetime(float(book['timestamp']),unit='ms',utc=True)
                age=(now-stamp).total_seconds()
                if not math.isfinite(age) or not 0<=age<=max_book_age_seconds:blocked.append(side.title()+': book timestamp is stale or in the future.')
                times.append(stamp)
            except (TypeError,KeyError,ValueError,OverflowError):blocked.append(side.title()+': missing or invalid book timestamp.')
        if len(times)==2 and abs((times[0]-times[1]).total_seconds())>max_book_skew_seconds:blocked.append('Book timestamps are too far apart.')
        cost=sum(q['avg_cost'] for q in quotes)+2*friction_cents/100 if all(q['avg_cost'] is not None for q in quotes) else None
        profit=shares*(1-cost) if cost is not None else None
        candidate=not blocked and profit is not None and profit>1e-8
        rows.append(dict(market_id=r['market_id'],question=r['question'],url=r['url'],shares_each_side=shares,
            yes_cost_with_fees=quotes[0]['avg_cost'],no_cost_with_fees=quotes[1]['avg_cost'],friction_per_pair=2*friction_cents/100,
            total_cost=shares*cost if cost is not None else None,combined_payout=shares,snapshot_profit=profit,
            candidate=candidate,status='Snapshot mismatch; verify both fills' if candidate else 'Blocked' if blocked else 'No positive mismatch after costs',
            reason=' '.join(blocked) or ('Combined purchase cost is below the normal settlement payout.' if candidate else 'Combined purchase cost is at least the normal settlement payout.')))
    return pd.DataFrame(rows)


def table(frame,limit=20):
    if frame.empty:return pd.DataFrame({'Status':['No contracts found.']})
    q=frame.sort_values(['candidate','snapshot_profit'],ascending=False,na_position='last').head(limit)
    return q[['question','shares_each_side','total_cost','combined_payout','snapshot_profit','status','reason']].rename(columns={
        'question':'Contract','shares_each_side':'Shares on each side','total_cost':'Cost of both sides ($)',
        'combined_payout':'Normal combined payout ($)','snapshot_profit':'Snapshot payoff less cost ($)','status':'Status','reason':'Explanation'})
