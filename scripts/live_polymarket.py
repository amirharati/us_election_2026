"""Read-only public Polymarket discovery and conditional forecast-gap research.

No wallet, credentials, orders, or inference refresh. Price snapshots are not offers.
"""
from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, json, math, re, time
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import election_lab as lab
from compare_current_forecasts import ABBR
from model_portfolio import configuration

GAMMA='https://gamma-api.polymarket.com'
CLOB='https://clob.polymarket.com'
TAGS={'midterms':'102289','US elections':'1101','Senate midterms':'104093','Senate elections':'100199'}
SOURCES={'discovery':'https://docs.polymarket.com/market-data/discover-markets',
         'books':'https://docs.polymarket.com/market-data/prices-order-books',
         'fees':'https://docs.polymarket.com/trading/fees'}
CACHE=lab.ROOT/'cache/polymarket'
RESULT=lab.ROOT/'outputs/reports/markets/polymarket'


def utcnow():return datetime.now(timezone.utc).isoformat()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,allow_nan=False).encode()).hexdigest()
def array(value):return json.loads(value) if isinstance(value,str) else value or []
def number(value):
    try:
        n=float(value)
        return n if math.isfinite(n) else None
    except (TypeError,ValueError):return None


def request(path,params=None,body=None):
    # POST /books is a documented batch READ, never an order endpoint.
    for attempt in range(3):
        try:
            r=requests.get(path,params=params,timeout=35) if body is None else requests.post(path,json=body,timeout=35)
            r.raise_for_status();return r.json()
        except requests.RequestException:
            if attempt==2:raise
            time.sleep(1+attempt)


SCOPE='senate-election-outcomes-v1'
COVERAGE='All pages of the listed discovery tags were scanned. Only 2026 U.S. Senate winners, margins/relative results, control, seat totals and Senate-only combinations are retained. Tag omissions or unrecognized titles can leave gaps; this is not guaranteed platform-wide coverage.'


def relevant(event):
    title=event.get('title','').lower()
    if 'senate' not in title or re.search(r'\b20\d{2}\b',title) and any(y!='2026' for y in re.findall(r'\b20\d{2}\b',title)):return False
    if re.search(r'house|governor|gubernatorial|trifecta|state senate|turnout|particip|county|primary|nominee|nomination|odds|favored|favorite|bulletin|leader',title):return False
    return category(title) in {'Senate race winners','Senate margins / relative results','Senate control','Senate seat counts','Senate-only combinations'}


def restrict_catalog(payload):
    """Apply current scope to legacy caches too, including offline/failure fallbacks."""
    rows=[{**r,'category':category(r['event'])} for r in payload['markets'] if relevant({'title':r['event']})]
    used={r['rules_id'] for r in rows}
    return {**payload,'markets':rows,'rules':{k:v for k,v in payload['rules'].items() if k in used},'scope':SCOPE,'coverage_note':COVERAGE}


def category(title):
    t=title.lower()
    if 'primary' in t or 'nominee' in t or 'nomination' in t:return 'Primaries / nominations'
    if re.search(r'odds|favored|favorite|bulletin|flip democrats',t):return 'Market-price / forecast derivatives'
    if 'county' in t:return 'County results'
    if 'state senate' in t or 'state house' in t:return 'State legislatures'
    if 'turnout' in t:return 'Turnout'
    if 'margin' in t or 'within ' in t or 'closest' in t or 'best tossup' in t:
        return 'Senate margins / relative results' if 'senate' in t else 'Other margins / vote shares'
    if 'combo' in t or 'balance of power' in t or 'trifecta' in t or 'core four' in t or 'senate and house' in t:return 'Senate-only combinations' if 'senate' in t and not re.search(r'house|governor|trifecta',t) else 'Combined outcomes'
    if 'senate seats' in t:return 'Senate seat counts'
    if 'win the senate' in t:return 'Senate control'
    if 'senate election winner' in t:return 'Senate race winners'
    if 'house seats' in t:return 'House seat counts'
    if 'win the house' in t:return 'House control'
    if 'house election winner' in t:return 'House district winners'
    if 'governor' in t or 'gubernatorial' in t:return 'Governors'
    return 'Other midterm-related'


def normalize(events):
    rows=[];rules={}
    for e in events:
        if not relevant(e):continue
        for m in e.get('markets',[]):
            if not m.get('active') or m.get('closed') or m.get('archived'):continue
            description=m.get('description','');rule_id=hashlib.sha256(description.encode()).hexdigest();rules[rule_id]=description
            outcomes=array(m.get('outcomes'));tokens=array(m.get('clobTokenIds'));prices=array(m.get('outcomePrices'))
            if len(outcomes)!=len(tokens):tokens=[None]*len(outcomes)
            by_outcome={str(o).lower():dict(token=t,price=number(prices[i]) if i<len(prices) else None) for i,(o,t) in enumerate(zip(outcomes,tokens))}
            fee=m.get('feeSchedule') or {}
            rows.append(dict(event_id=str(e['id']),event=e['title'],category=category(e['title']),event_slug=e['slug'],market_id=str(m['id']),
                question=m.get('question',''),outcome=m.get('groupItemTitle',''),slug=m['slug'],
                url=f"https://polymarket.com/event/{e['slug']}/{m['slug']}",rules_id=rule_id,
                end_date=m.get('endDate'),updated_at=m.get('updatedAt'),accepting_orders=bool(m.get('acceptingOrders')),
                order_book=bool(m.get('enableOrderBook')),liquidity=number(m.get('liquidityNum')),volume=number(m.get('volumeNum')),volume24h=number(m.get('volume24hr')),
                yes_token=by_outcome.get('yes',{}).get('token'),no_token=by_outcome.get('no',{}).get('token'),
                indicative_yes=by_outcome.get('yes',{}).get('price'),gamma_bid=number(m.get('bestBid')),gamma_ask=number(m.get('bestAsk')),
                fees_enabled=m.get('feesEnabled'),fee_rate=number(fee.get('rate')),fee_exponent=number(fee.get('exponent')),neg_risk=bool(m.get('negRisk'))))
    if not rows:return [],rules
    frame=pd.DataFrame(rows).drop_duplicates('market_id')
    return frame.astype(object).where(frame.notna(),None).to_dict('records'),rules


def discover(offline=False,force=False,ttl_minutes=15,max_pages=100):
    CACHE.mkdir(parents=True,exist_ok=True)
    cached=CACHE/'catalog.json';fallback=RESULT/'catalog.json.gz'
    old=None;current_scope=False
    for p in [cached,fallback]:
        if p.exists():
            candidate=json.loads(gzip.decompress(p.read_bytes())) if p.suffix=='.gz' else json.loads(p.read_text())
            if digest(candidate['payload'])!=candidate['sha256']:raise ValueError('Polymarket catalog checksum mismatch')
            current_scope=candidate['payload'].get('scope')==SCOPE
            old=restrict_catalog(candidate['payload']);break
    if offline:
        if old is None:raise RuntimeError('No saved Polymarket catalog; run online once')
        return old,'offline snapshot'
    if old and current_scope and not force and (datetime.now(timezone.utc)-datetime.fromisoformat(old['retrieved_at'])).total_seconds()<ttl_minutes*60:
        return old,'recent catalog cache'
    try:
        events={};pages=[]
        for name,tag in TAGS.items():
            total=0
            for page in range(max_pages):
                params=dict(tag_id=tag,closed='false',active='true',limit=100,offset=page*100,order='id',ascending='true')
                batch=request(GAMMA+'/events',params)
                if not isinstance(batch,list):raise ValueError('Unexpected catalog schema')
                pages.append(dict(tag=name,offset=page*100,count=len(batch),sha256=digest(batch)))
                for event in batch:events[str(event['id'])]=event
                total+=len(batch)
                if len(batch)<100:break
            else:raise RuntimeError('Catalog pagination cap reached; cannot call discovery complete')
        rows,rules=normalize(events.values())
        payload=dict(retrieved_at=utcnow(),tag_scope=TAGS,pages=pages,events_scanned=len(events),markets=rows,rules=rules,
                     discovery_complete=True,scope=SCOPE,coverage_note=COVERAGE)
        lab.write_json(cached,dict(payload=payload,sha256=digest(payload)))
        return payload,'checked online'
    except Exception as exc:
        if old is None:raise
        return old,'STALE catalog after failure: '+str(exc)


def margin_band(question):
    m=re.search(r'by (\d+(?:\.\d+)?)%-(\d+(?:\.\d+)?)%',question)
    if m:lo,hi=map(float,m.groups())
    else:
        m=re.search(r'by (\d+(?:\.\d+)?)% or more',question)
        if not m:return None
        lo,hi=float(m[1]),np.inf
    if 'Democratic Party' in question:return lo,hi
    if 'Republican Party' in question:return -hi,-lo
    return None


def model_context(run):
    run=lab.verify_run(Path(run));meta=json.loads((run/'run.json').read_text())
    pred=pd.read_parquet(run/'predictions.parquet');pred=pred[pred.cycle.eq(2026)]
    seats=pd.read_parquet(run/'seats.parquet');mix=pred[pred.model.eq('Four-model mixture')].set_index('geography')
    if mix.index.duplicated().any():raise ValueError('Ambiguous state/seat mapping')
    review=json.loads((lab.ROOT/'config/candidate_review_2026.json').read_text())['contests']
    freq=None
    for p in (run/'model_forecasts').glob('*.npz'):
        with np.load(p) as a:
            if str(a['model'])=='Four-model mixture':freq=a['seat_count_frequency'].astype(float)
    if freq is not None:freq=freq/freq.sum()
    from predictive_distributions import PredictiveDistributions
    return dict(run=run,meta=meta,pred=pred,mix=mix,seats=seats,review=review,freq=freq,distributions=PredictiveDistributions(run))


def assess_market(row,rules,context):
    title=row['event'];question=row['question'];rule=rules[row['rules_id']]
    result=dict(model_low=None,model_high=None,probability_kind='unavailable',mapping='Not priced',reason='Outside supported Senate outcome mapping',state=None)
    mix=context['mix'];review=context['review'];cat=row['category']
    # Named party contracts are not automatically independent-candidate contracts.
    if cat=='Senate race winners' or cat=='Senate margins / relative results':
        states=[abbr for name,abbr in ABBR.items() if re.search(r'\b'+re.escape(name)+r'\b',title+' '+question,re.I)]
        if len(set(states))!=1:return {**result,'reason':'Multiple states or unrecognized geography; joint/relative outcome requires a separate model'}
        state=states[0];result['state']=state
        if state not in mix.index:return {**result,'reason':'No forecast for this state/seat'}
        ref=mix.loc[state];policy=review.get(state,{})
        parties={c.get('party') for c in policy.get('candidates',[])}
        if 'first round' in (title+' '+rule).lower():return {**result,'reason':'First-round contract is not the final-election forecast'}
        if not policy.get('scalar_seat_mapping_ready') or not {'DEM','REP'}.issubset(parties) or any(p not in {'DEM','REP'} for p in parties):
            return {**result,'reason':'Independent candidate or multi-round rules differ from D/Independent-versus-R forecast'}
        if 'county' in title.lower():return {**result,'reason':'County contract is not a statewide forecast'}
        model=context.get('model_name','Four-model mixture')
        if cat=='Senate race winners':
            if 'Democrats win' in question:republican=False
            elif 'Republicans win' in question:republican=True
            else:return {**result,'reason':'Named candidate contract needs explicit candidate mapping'}
            event=context['distributions'].margin_probability(model,state,0,np.inf,lower_closed=False)
            p=1-event['probability'] if republican else event['probability']
            return {**result,**event,'model_low':p,'model_high':p,'probability':p,'event_formula':'1 - P(M > 0)' if republican else 'P(M > 0)','mapping':'Conditional comparison',
                    'reason':'Assumes modeled D/R contenders exhaust the winning outcomes; party replacements and third-party wins require review'}
        band=margin_band(question)
        if band is None:return {**result,'reason':'Margin/ranking contract is not a recognized party-specific margin band'}
        if 'top two candidates' not in rule.lower() or 'higher margin bracket' not in rule.lower():return {**result,'reason':'Unrecognized margin settlement definition or boundary rule'}
        republican='Republican Party' in question
        event=context['distributions'].margin_probability(model,state,*band,lower_closed=not republican,upper_closed=republican)
        p=event['probability'];lo,hi=band
        formula=f'P({lo:g} < M <= {hi:g})' if republican else f'P({lo:g} <= M < {hi:g})'
        return {**result,**event,'model_low':p,'model_high':p,'event_formula':formula,
                'mapping':'Conditional comparison','reason':'Assumes D/R are the top two and forecast margin uses the same vote denominator; full predictive distribution is used'}
    if cat=='Senate control':
        selected=context['seats'];selected=selected[selected.model.eq(context.get('model_name','Four-model mixture')) & selected.cycle.eq(2026)]
        if len(selected)!=1:return {**result,'reason':'Missing or ambiguous model chamber forecast'}
        main=selected.iloc[0]
        if 'Democratic Party' in question:p=float(main.p_D_control)
        elif 'Republican Party' in question:p=1-float(main.p_D_control)
        else:return {**result,'reason':'Other-party control is not modeled'}
        return {**result,'model_low':p,'model_high':p,'event_formula':'P(D seats >= 51)' if 'Democratic Party' in question else 'P(D seats <= 50)','probability_kind':'Saved joint chamber simulations','mapping':'Conditional comparison',
                'reason':'Assumes modeled independent winners caucus with Democrats, the existing fixed-seat roster, and GOP 50-seat tie-break; contract waits for caucus declarations'}
    if cat=='Senate seat counts' and context['freq'] is not None:
        m=re.search(r'hold (?:exactly )?(\d+)( or fewer| or more)? Senate seats',question)
        if not m or 'Republican Party' not in question:return result
        rseats=100-np.arange(len(context['freq']));n=int(m[1]);op=m[2] or ''
        mask=rseats<=n if 'fewer' in op else rseats>=n if 'more' in op else rseats==n
        p=float(context['freq'][mask].sum())
        return {**result,'model_low':p,'model_high':p,'event_formula':f'P(R seats {"<=" if "fewer" in op else ">=" if "more" in op else "="} {n})','probability_kind':'Saved model seat-count distribution','mapping':'Conditional comparison',
                'reason':'Assumes R seats equal 100 minus modeled D/Independent seats; caucus choices and vacancies may differ from contract'}
    return result


def fee_per_share(price,row):
    if row['fees_enabled'] is False:return 0.
    if row['fees_enabled'] is not True or number(row['fee_rate']) is None or row['fee_exponent']!=1:
        return None
    return row['fee_rate']*price*(1-price)


def fill_book(book,row,shares):
    bids=[(float(x['price']),float(x['size'])) for x in book.get('bids',[]) if float(x['size'])>0]
    asks=sorted((float(x['price']),float(x['size'])) for x in book.get('asks',[]) if float(x['size'])>0)
    if any(not(0<p<1) or not math.isfinite(n) for p,n in bids+asks):raise ValueError('Invalid book levels')
    bid=max((p for p,n in bids),default=None);ask=min((p for p,n in asks),default=None)
    result=dict(best_bid=bid,best_ask=ask,spread=ask-bid if bid is not None and ask is not None else None,
                filled=0.,avg_cost=None,fee_cost=None,min_order_size=number(book.get('min_order_size')),book_time=book.get('timestamp'),book_hash=book.get('hash'))
    if bid is not None and ask is not None and bid>ask:return {**result,'quote_status':'crossed book'}
    if result['min_order_size'] is not None and shares<result['min_order_size']:return {**result,'quote_status':'below minimum order size'}
    remaining=shares;cost=0.;fees=0.
    for price,size in asks:
        take=min(remaining,size);fee=fee_per_share(price,row)
        if fee is None:return {**result,'quote_status':'unknown fee schedule'}
        cost+=take*price;fees+=round(take*fee,5);remaining-=take
        if remaining<=1e-9:break
    result.update(filled=shares-remaining)
    if remaining>1e-9:return {**result,'quote_status':'insufficient displayed ask depth'}
    return {**result,'quote_status':'quoted','avg_cost':(cost+fees)/shares,'fee_cost':fees/shares}


def fetch_books(tokens,offline=False):
    if offline:return {},{'status':'offline; no live order books','errors':[],'retrieved_at':utcnow()}
    books={};errors=[]
    for offset in range(0,len(tokens),100):
        batch=tokens[offset:offset+100]
        try:
            response=request(CLOB+'/books',body=[dict(token_id=t) for t in batch])
            if not isinstance(response,list):raise ValueError('Unexpected books response')
            for book in response:
                if 'asset_id' in book:books[book['asset_id']]=book
        except Exception as exc:errors.append(dict(batch=offset,error=str(exc)))
    return books,dict(status='checked online' if not errors else 'partial failure',errors=errors,retrieved_at=utcnow(),tokens_requested=len(tokens),books_returned=len(books))


def download_markets(offline=False,force=False):
    """Refresh only public market data; no forecast loading or model execution."""
    catalog,catalog_status=discover(offline,force)
    tokens=sorted({r[k] for r in catalog['markets'] if r['accepting_orders'] and r['order_book'] for k in ['yes_token','no_token'] if r[k]})
    books,book_status=fetch_books(tokens,offline)
    snapshot=dict(catalog=catalog,catalog_status=catalog_status,books=books,book_status=book_status,retrieved_at=utcnow())
    if not offline:
        CACHE.mkdir(parents=True,exist_ok=True)
        path=CACHE/'market_snapshot.json.gz';temporary=path.with_suffix('.tmp')
        temporary.write_bytes(gzip.compress(json.dumps(dict(payload=snapshot,sha256=digest(snapshot)),sort_keys=True).encode(),mtime=0))
        temporary.replace(path)
    return snapshot


def load_market_snapshot(path=None):
    """Reuse a saved download unchanged, including its original timestamps."""
    path=Path(path) if path else CACHE/'market_snapshot.json.gz'
    if path.exists():
        envelope=json.loads(gzip.decompress(path.read_bytes()));snapshot=envelope['payload']
        if digest(snapshot)!=envelope['sha256']:raise ValueError('Market snapshot checksum mismatch')
        return snapshot
    if path!=CACHE/'market_snapshot.json.gz':raise FileNotFoundError(path)
    lab.verify_run(RESULT)
    status=json.loads((RESULT/'status.json').read_text())
    return dict(catalog=json.loads(gzip.decompress((RESULT/'catalog.json.gz').read_bytes()))['payload'],
        books=json.loads(gzip.decompress((RESULT/'order_books.json.gz').read_bytes())),catalog_status=status['catalog_status'],
        book_status=status['book_status'],retrieved_at=status['retrieved_at'])


def book_age_seconds(quote):
    stamp=number(quote.get('book_time'))
    return None if stamp is None else time.time()-stamp/1000


def analyze(run,offline=False,force=False,shares=100,min_edge_pp=3,max_spread=.10,min_liquidity=2000,max_forecast_age_days=3,snapshot=None):
    if shares<=0:raise ValueError('Shares must be positive')
    snapshot=download_markets(offline,force) if snapshot is None else snapshot
    catalog=snapshot['catalog'];catalog_status=snapshot['catalog_status'];context=model_context(run)
    rows=[]
    for row in catalog['markets']:rows.append({**row,**assess_market(row,catalog['rules'],context)})
    candidates=[r for r in rows if r['model_low'] is not None and r['accepting_orders'] and r['order_book']]
    books=snapshot['books'];book_status=snapshot['book_status']
    catalog_age=(pd.Timestamp.now(tz='UTC')-pd.Timestamp(catalog['retrieved_at'])).total_seconds()
    age=(pd.Timestamp.now(tz='UTC').normalize()-pd.Timestamp(context['meta']['as_of'],tz='UTC')).days
    validation=lab.ROOT/'outputs/validation/notebooks.json'
    source_review='No review status recorded here; inspect forecast provenance.'
    if validation.exists():
        live_status=next((r for r in json.loads(validation.read_text()) if r.get('notebook')=='04_live_forecast.ipynb'),{})
        mode=live_status.get('execution_mode','')
        if 'blocked' in mode or 'review' in mode:source_review=mode
    out=[]
    for r in candidates:
        for side in ['Yes','No']:
            token=r[side.lower()+'_token'];lo,hi=r['model_low'],r['model_high']
            if side=='No':lo,hi=1-hi,1-lo
            quote=fill_book(books[token],r,shares) if token in books else dict(quote_status='book unavailable',avg_cost=None,spread=None)
            cost=quote['avg_cost'];edge=100*(lo-cost) if cost is not None else None
            blockers=[]
            if catalog_status.startswith('STALE') or offline:blockers.append('catalog not live')
            if not 0<=catalog_age<=900:blockers.append('catalog age outside limit')
            quote_age=book_age_seconds(quote)
            if quote_age is None or not 0<=quote_age<=120:blockers.append('order book stale or timestamp unavailable')
            if quote['quote_status']!='quoted':blockers.append(quote['quote_status'])
            if quote.get('spread') is None or quote['spread']>max_spread:blockers.append('wide/missing spread')
            if (r['liquidity'] or 0)<min_liquidity:blockers.append('low reported liquidity')
            if age>max_forecast_age_days or age<0:blockers.append('forecast age outside limit')
            if edge is None or edge<min_edge_pp:blockers.append('conservative model gap below threshold')
            out.append({**r,**quote,'side':side,'prob_low':lo,'prob_high':hi,'net_edge_low_pp':edge,
                        'net_edge_high_pp':100*(hi-cost) if cost is not None else None,'screen':'Review candidate' if not blockers else 'Not shortlisted',
                        'screen_reason':'; '.join(blockers) or 'Positive modeled gap after displayed depth and taker fees; verify settlement assumptions and forecast inputs'})
    frame=pd.DataFrame(rows);comparisons=pd.DataFrame(out)
    if not comparisons.empty:comparisons=comparisons.sort_values('net_edge_low_pp',ascending=False,na_position='last')
    return dict(catalog=catalog,inventory=frame,comparisons=comparisons,books=books,
                status=dict(retrieved_at=snapshot['retrieved_at'],evaluated_at=utcnow(),catalog_status=catalog_status,book_status=book_status,catalog_age_seconds=catalog_age,max_catalog_age_seconds=900,max_book_age_seconds=120,forecast_cutoff=context['meta']['as_of'],forecast_age_days=age,
                            forecast_manifest_sha256=lab.sha(Path(run)/'manifest.json'),forecast_source_review=source_review,shares=shares,min_edge_pp=min_edge_pp,max_spread=max_spread,min_liquidity=min_liquidity,max_forecast_age_days=max_forecast_age_days,
                            priced_markets=len(candidates),scope='Research only; model-conditioned expected-value gaps are not arbitrage or guaranteed returns. No orders or account access.',
                            limitations='Forecast may retain unresolved source/roster reviews. No candidate-by-candidate third-party or first-round model. Joint draws are saved, but combination/ranking settlement mappings remain unsupported. Simulation estimates have Monte Carlo error and are not confidence in model accuracy. Prices can move before execution. Repeated contracts share risk.'))


def inventory_summary(result):
    q=result['inventory'];return q.groupby('category').agg(events=('event_id','nunique'),contracts=('market_id','nunique'),reported_liquidity=('liquidity','sum')).reset_index().sort_values('contracts',ascending=False)


def comparison_table(result,only_shortlist=True,limit=25):
    q=result['comparisons']
    if q.empty:return pd.DataFrame({'Status':['No compatible model comparisons or quotes available']})
    if only_shortlist:q=q[q.screen.eq('Review candidate')]
    q=q.head(limit).copy()
    if q.empty:return pd.DataFrame({'Status':['No contracts pass the configured live-quote and modeled-gap filters']})
    q['Model probability %']=q.apply(lambda r:f'{100*r.prob_low:.1f}' if r.prob_low==r.prob_high else f'{100*r.prob_low:.1f}–{100*r.prob_high:.1f}',axis=1)
    q['Cost incl. fees (¢)']=100*q.avg_cost
    return q[['question','side','Model probability %','Cost incl. fees (¢)','net_edge_low_pp','spread','probability_kind','reason','screen','url']].rename(columns={'question':'Contract','side':'Outcome','net_edge_low_pp':'Minimum modeled gap (pp)','spread':'Bid–ask spread ($)','reason':'Settlement assumption'})


def figures(result,directory):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True);paths=[]
    q=inventory_summary(result).sort_values('contracts')
    fig,ax=plt.subplots(figsize=(12,7));ax.barh(q.category,q.contracts,color='#2367a3');ax.set_xlabel('Active contracts found');ax.grid(axis='x',alpha=.2)
    ax.set_title('2026 U.S. Senate · discovered Polymarket inventory');fig.tight_layout();p=directory/'inventory.png';fig.savefig(p,dpi=140);plt.close(fig);paths.append(p)
    q=result['comparisons']
    if not q.empty:
        q=q[q.avg_cost.notna()].head(15).iloc[::-1]
        if len(q):
            fig,ax=plt.subplots(figsize=(13,max(5,.45*len(q)+2)));y=np.arange(len(q))
            ax.hlines(y,100*q.prob_low,100*q.prob_high,color='#16857b',lw=5,label='Mixture probability from full simulations')
            ax.scatter(100*q.prob_low,y,color='#16857b');ax.scatter(100*q.avg_cost,y,color='#c28b18',marker='x',label='Displayed ask-depth cost including fees')
            labels=[r.question+' — '+r.side for r in q.itertuples()]
            import textwrap
            ax.set(yticks=y,yticklabels=['\n'.join(textwrap.wrap(x,65)) for x in labels],xlabel='Cents per $1 payout / model probability (%)',xlim=(0,100))
            ax.grid(alpha=.2);ax.legend(loc='upper center',bbox_to_anchor=(.5,1.15),fontsize=8)
            fig.suptitle('Conditional research gaps · verify settlement and model assumptions',fontsize=14)
            fig.tight_layout(rect=[0,0,1,.94]);p=directory/'research_gaps.png';fig.savefig(p,dpi=140);plt.close(fig);paths.append(p)
    return paths


def save(result):
    from output_publication import replace_directory,archive_report,write_index
    out=lab.new_run('polymarket');meta=result['status']
    result['inventory'].to_parquet(out/'inventory.parquet',index=False)
    result['comparisons'].to_parquet(out/'comparisons.parquet',index=False)
    events=result['inventory'][['event_id','event','category','event_slug']].drop_duplicates('event_id')
    events.to_parquet(out/'events.parquet',index=False)
    (out/'catalog.json.gz').write_bytes(gzip.compress(json.dumps(dict(payload=result['catalog'],sha256=digest(result['catalog'])),sort_keys=True).encode(),mtime=0))
    (out/'order_books.json.gz').write_bytes(gzip.compress(json.dumps(result['books'],sort_keys=True).encode(),mtime=0));lab.write_json(out/'status.json',meta)
    pictures=figures(result,out)
    lines=['# Polymarket Senate market research','',f"Snapshot: **{meta['retrieved_at']}**. Forecast cutoff: **{meta['forecast_cutoff']}** ({meta['forecast_age_days']} days old).",
           '',f"Catalog: {meta['catalog_status']}. Order books: {meta['book_status']['status']}.",'',
           result['catalog']['coverage_note'],'',meta['scope'],'',meta['limitations'],'',
           'Forecast source review: '+meta['forecast_source_review'],'',
           '## Catalog coverage','',f"**{len(events)} event groups; {result['inventory'].market_id.nunique()} active contracts.** An event groups related contracts. Each margin band is a separate contract. Yes and No are two sides of one contract and are not counted twice. These counts are not numbers of races.",'',inventory_summary(result).to_markdown(index=False,floatfmt='.2f'),'',
           '## Conditional review candidates','',f"Illustrative depth: {meta['shares']} shares per contract. Threshold: at least {meta['min_edge_pp']}pp modeled gap after taker fees, spread ≤{meta['max_spread']}, reported liquidity ≥${meta['min_liquidity']}. These are independent contract screens, not a portfolio or instructions to trade.",'',
           comparison_table(result).fillna('—').to_markdown(index=False,floatfmt='.3f'),'',
           '## How to interpret margins and missing comparisons','',
           'Margin probabilities use full saved predictive simulations. Gaussian model state events use an analytic CDF. Simulation estimates have Monte Carlo error. Top-two candidate, vote denominator, first-round, third-party and caucus rules must match before treating a gap as comparable. House, governor, turnout, county, primary and price-target contracts are excluded. Senate-only combinations remain inventoried but unpriced until their joint settlement conditions have a supported mapping. Do not multiply marginal state probabilities for correlated combination markets.','',
           '## Downloads','', '[Full event inventory](events.parquet) · [All contracts](inventory.parquet) · [All comparisons and exclusion reasons](comparisons.parquet) · [Source metadata and rules](catalog.json.gz) · [Order-book snapshot](order_books.json.gz) · [Run settings](status.json)','',
           '## All discovered events','']
    for category_name,group in events.groupby('category'):
        lines += ['### '+category_name,'']
        lines += [f"- [{r.event}](https://polymarket.com/event/{r.event_slug})" for r in group.sort_values('event').itertuples()]
        lines+=['']
    if 'scanner' in result:
        from polymarket_scanner import publish
        lines+=publish(result['scanner'],out)
    if 'price_checks' in result:
        from polymarket_price_checks import METHOD as PAIR_METHOD, table as pair_table
        result['price_checks'].to_parquet(out/'price_checks.parquet',index=False)
        if 'price_checks_stress' in result:
            result['price_checks_stress'].to_parquet(out/'price_checks_stress.parquet',index=False)
            lines += [f"Extra-friction pair scenario: {int(result['price_checks_stress'].candidate.sum())} snapshot candidates.",'', '[Extra-friction pair checks](price_checks_stress.parquet)','']
        lines += ['## Model-free Yes/No price checks','',PAIR_METHOD,'',f"Snapshot candidates: {int(result['price_checks'].candidate.sum())}.",'',pair_table(result['price_checks']).fillna('Unavailable').to_markdown(index=False,floatfmt='.2f'),'', '[All same-contract price checks](price_checks.parquet)','']
    lines+=['## Figures','']
    for p in pictures:lines += [f'![{p.stem}]({p.name})','']
    from predictive_distributions import FORMULAS
    lines+=['## Probability formulas','',FORMULAS,'']
    lines+=['## Sources','']+[f'- [{k}]({v})' for k,v in SOURCES.items()]
    (out/'report.md').write_text('\n'.join(lines)+'\n')
    lab.finish(out,dict(kind='polymarket',as_of=meta['forecast_cutoff'],market_retrieved_at=meta['retrieved_at']),publish=False)
    replace_directory(out,RESULT)
    archive_report(lab.ROOT,out,lab.ROOT/'outputs/reports/markets/polymarket/report.md')
    write_index(lab.ROOT)
    return out
