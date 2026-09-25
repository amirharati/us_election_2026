"""Initial multi-model research screen; correlated model variants are not votes."""
import numpy as np
import pandas as pd
from model_labels import model_label

METHOD = ('This is an initial research list. Each model uses its own full predictive distribution and saved joint seat distribution. '
          'Gaussian state probabilities use the analytic CDF; Student-t and mixture probabilities use full saved simulations. Simulation estimates retain Monte Carlo error. '
          'Model agreement is a sensitivity check, not independent evidence. Base costs use ask depth and estimated taker fees. Extra friction is a separate scenario; '
          'the probability haircut is a separate stress assumption. No extra half-spread is charged because asks already include the spread. '
          'All findings remain conditional on settlement mapping and the recorded forecast-source review. Unpriced contracts remain in the coverage audit.')


DEFAULT_MODELS=('Bayesian','Matched Student-t (df5)','Four-model mixture','Mixture + polling 10%')


def selected_predictions(pred, models=None):
    names=list(DEFAULT_MODELS if models is None else models)
    if not names or len(names)!=len(set(names)):raise ValueError('Select distinct model names')
    missing=set(names)-set(pred.model)
    if missing:raise ValueError('Requested saved models are missing: '+', '.join(sorted(missing)))
    return pred[pred.model.isin(names)].copy(),names


def scan(research, run, friction_cents=2., probability_haircut_pp=2., min_edge_pp=0., models=None):
    import live_polymarket as poly
    if not all(np.isfinite(x) and x>=0 for x in [friction_cents,probability_haircut_pp,min_edge_pp]):
        raise ValueError('Scanner assumptions must be finite and nonnegative')
    if probability_haircut_pp>100:raise ValueError('Probability haircut exceeds 100')
    context=poly.model_context(run);context['pred'],selected_models=selected_predictions(context['pred'],models)
    expected=research['status'].get('forecast_manifest_sha256')
    if expected and expected!=poly.lab.sha(context['run']/'manifest.json'):
        raise ValueError('Forecast changed since snapshot evaluation. Rerun analyze with the same market snapshot and the new forecast before scanning.')
    core=set(poly.configuration()['component_weights'])
    frequencies={}
    if (context['run']/'main_joint.npz').exists():
        with np.load(context['run']/'main_joint.npz') as a:
            f=a['seat_count_frequency'].astype(float)
            if f.sum()>0:frequencies['Bayesian']=f/f.sum()
    for path in (context['run']/'model_forecasts').glob('*.npz'):
        with np.load(path) as a:
            f=a['seat_count_frequency'].astype(float)
            if f.sum()>0:frequencies[str(a['model'])]=f/f.sum()
    details=[];audits=[]
    # Every catalog contract is considered for every saved model, even if unmappable.
    for name,pred in context['pred'].groupby('model'):
        ctx={**context,'mix':pred.set_index('geography'),'freq':frequencies.get(name),'model_name':name}
        if ctx['mix'].index.duplicated().any():raise ValueError('Ambiguous model geography')
        for row in research['catalog']['markets']:
            mapped=poly.assess_market(row,research['catalog']['rules'],ctx)
            audits.append(dict(market_id=row['market_id'],question=row['question'],model=name,**mapped))
            if mapped['model_low'] is None:continue
            for side in ['Yes','No']:
                lo,hi=mapped['model_low'],mapped['model_high']
                if side=='No':lo,hi=1-hi,1-lo
                token=row[side.lower()+'_token']
                quote=poly.fill_book(research['books'][token],row,research['status']['shares']) if token in research['books'] else dict(quote_status='book unavailable',avg_cost=None,spread=None)
                cost=quote['avg_cost'];effective=cost
                stress_cost=cost+friction_cents/100 if cost is not None else None
                stressed=max(0.,lo-probability_haircut_pp/100)
                ref=ctx['mix'].loc[mapped['state']] if mapped['state'] in ctx['mix'].index else {}
                details.append(dict(market_id=row['market_id'],question=row['question'],category=row['category'],side=side,url=row['url'],model=name,model_label=model_label(name),core_model=name in core,
                    model_low=lo,model_high=hi,stressed_low=stressed,avg_cost=cost,effective_cost=effective,stress_cost=stress_cost,
                    market_midpoint=(quote['best_bid']+quote['best_ask'])/2 if quote.get('best_bid') is not None and quote.get('best_ask') is not None else None,
                    probability_kind=mapped.get('probability_kind','Model probability'),
                    event_formula=mapped.get('event_formula') if side=='Yes' else '1 - ('+str(mapped.get('event_formula','P(Yes)'))+')',
                    simulation_draws=mapped.get('simulation_draws'),book_age_seconds=poly.book_age_seconds(quote),
                    entry_price=cost-quote['fee_cost'] if cost is not None else None,fee_per_share=quote.get('fee_cost'),
                    edge_low_pp=100*(lo-effective) if effective is not None else None,edge_high_pp=100*(hi-effective) if effective is not None else None,
                    stressed_edge_pp=100*(stressed-stress_cost) if stress_cost is not None else None,
                    friction_only_edge_low_pp=100*(lo-stress_cost) if stress_cost is not None else None,
                    probability_only_edge_low_pp=100*(stressed-effective) if effective is not None else None,
                    quote_status=quote['quote_status'],spread=quote.get('spread'),accepting_orders=row['accepting_orders'],order_book=row['order_book'],liquidity=row['liquidity'],
                    forecast_mean_margin_pp=next((poly.number(ref.get(k)) for k in ['margin_pp','prediction_pp'] if poly.number(ref.get(k)) is not None),None),
                    margin_lo95_pp=poly.number(ref.get('lo95_pp')),margin_hi95_pp=poly.number(ref.get('hi95_pp')),poll_samples=poly.number(ref.get('sample_count',ref.get('n_samples'))),
                    mapping_reason=mapped['reason']))
    detail=pd.DataFrame(details);summary=[];status=research['status']
    for (_,side),g in detail.groupby(['market_id','side']) if not detail.empty else []:
        first=g.iloc[0];cg=g[g.core_model];blocked=[]
        if status['catalog_status'] not in ['checked online','recent catalog cache']:blocked.append('Catalog is offline or stale.')
        if 'max_catalog_age_seconds' in status and not 0<=status['catalog_age_seconds']<=status['max_catalog_age_seconds']:blocked.append('Catalog age exceeds the configured limit.')
        if 'max_book_age_seconds' in status and (pd.isna(first.book_age_seconds) or not 0<=first.book_age_seconds<=status['max_book_age_seconds']):blocked.append('Order book is stale or its timestamp is unavailable.')
        if first.quote_status!='quoted':blocked.append(first.quote_status+'.')
        if not first.accepting_orders or not first.order_book:blocked.append('Contract is not accepting book orders.')
        if not 0<=status['forecast_age_days']<=status['max_forecast_age_days']:blocked.append('Forecast age exceeds the configured limit.')
        if pd.isna(first.spread) or first.spread>status['max_spread']:blocked.append('The spread is wide or missing.')
        if pd.isna(first.liquidity) or first.liquidity<status['min_liquidity']:blocked.append('Reported liquidity is below the configured limit.')
        robust=g.stressed_edge_pp.gt(min_edge_pp);possible=g.edge_high_pp.gt(min_edge_pp)
        tier=('Positive stressed edge in at least one selected model' if robust.any()
              else 'Possible edge; probability bounds overlap cost' if possible.any() else 'No positive modeled edge')
        included=bool(possible.any() and not blocked)
        summary.append(dict(market_id=first.market_id,question=first.question,side=side,category=first.category,url=first.url,
            initial_candidate=included,tier=tier,models_priced=len(g),models_positive=int(robust.sum()),core_models_priced=len(cg),core_models_positive=int(cg.stressed_edge_pp.gt(min_edge_pp).sum()),
            cost_cents=100*first.effective_cost if pd.notna(first.effective_cost) else None,
            entry_price=first.entry_price,fee_per_share=first.fee_per_share,
            best_model=model_label(g.loc[g.stressed_edge_pp.idxmax(),'model']) if g.stressed_edge_pp.notna().any() else None,
            worst_model=model_label(g.loc[g.stressed_edge_pp.idxmin(),'model']) if g.stressed_edge_pp.notna().any() else None,
            positive_models=', '.join(g.loc[robust,'model_label']) or 'None',
            expected_profit_low_per_share=g.edge_low_pp.min()/100,expected_profit_high_per_share=g.edge_high_pp.max()/100,
            probability_low_pct=100*g.model_low.min(),probability_high_pct=100*g.model_high.max(),
            worst_stressed_edge_pp=g.stressed_edge_pp.min(),best_stressed_edge_pp=g.stressed_edge_pp.max(),best_possible_edge_pp=g.edge_high_pp.max(),
            core_worst_stressed_edge_pp=cg.stressed_edge_pp.min(),
            reason=('At least one model permits a positive edge after base costs. '+tier+'.') if included else (' '.join(blocked) or 'No model permits a positive edge after base costs.'),
            blockers=' '.join(blocked),settlement_review=first.mapping_reason,forecast_source_review=status['forecast_source_review']))
    summary=pd.DataFrame(summary)
    if not summary.empty:summary=summary.sort_values(['question','side'],kind='stable')
    return dict(details=detail,summary=summary,audit=pd.DataFrame(audits),settings=dict(shares=research['status']['shares'],friction_cents=friction_cents,probability_haircut_pp=probability_haircut_pp,min_edge_pp=min_edge_pp,models=selected_models,core_models=sorted(core)),method=METHOD)


READING_GUIDE = (
    'Each model uses its own predictive distribution. State event probabilities use an analytic Gaussian CDF or full model simulations. Chamber probabilities use joint seat frequencies. A 95% margin interval is not a confidence interval for a win probability. '
    'Market midpoint is a descriptive price-based probability, not the purchase price or an objective probability. The purchase break-even probability includes depth and fees. '
    'Entry price is the average ask price for the configured number of shares, before fees. '
    'Base budget includes entry price and estimated taker fees. Extra friction is only included in the stress scenario. '
    'One share pays $1 if the selected Yes or No outcome wins and $0 otherwise. '
    'Expected net profit equals shares × (model probability − total cost per share). '
    'A range uses probability bounds; it is not a guaranteed profit or a confidence interval. '
    'Stress uses a probability floored at zero after subtracting the configured haircut from the lower bound, and adds the extra friction to costs. '
    'A losing position loses its total budget. Model variants share evidence, so their agreement is not independent confirmation.'
)


def _range(lo,hi):
    if pd.isna(lo) or pd.isna(hi):return 'Unavailable'
    return f'{lo:.2f}' if abs(lo-hi)<1e-9 else f'{lo:.2f} to {hi:.2f}'


def table(scanner,limit=30):
    q=scanner['summary']
    if q.empty:return pd.DataFrame({'Status':['No model-comparable contracts.']})
    q=q[q.initial_candidate].head(limit).copy()
    if q.empty:return pd.DataFrame({'Status':['No contracts pass the initial screen.']})
    shares=scanner['settings']['shares']
    return pd.DataFrame({
        'Contract ID':q.market_id,'Contract':q.question,'Buy side':q.side,
        'Entry price (¢/share)':100*q.entry_price,
        f'Total budget for {shares:g} shares ($)':q.cost_cents*shares/100,
        'Expected net profit across models ($)':[_range(r.expected_profit_low_per_share*shares,r.expected_profit_high_per_share*shares) for r in q.itertuples()],
        'Lowest stressed profit model':q.worst_model,'Highest stressed profit model':q.best_model,
        'Initial selection reason':q.tier})


def model_table(scanner,market_id=None,side=None):
    """Every available model for one explicitly selected contract side."""
    q=scanner['summary']
    if market_id is None:
        q=q[q.initial_candidate] if not q.empty else q
        if q.empty:return pd.DataFrame({'Status':['No initial candidate selected.']})
        market_id=q.iloc[0].market_id;side=q.iloc[0].side
    d=scanner['details'];d=d[d.market_id.eq(str(market_id)) & d.side.eq(side)].copy()
    if d.empty:return pd.DataFrame({'Status':['No model comparison for this contract side.']})
    shares=scanner['settings']['shares']
    return pd.DataFrame({'Model':d.model_label,'Core model':d.core_model.map({True:'Yes',False:'No'}),
        'Probability method':d.probability_kind,
        'Market midpoint (%)':100*d.market_midpoint,
        'Purchase break-even probability (%)':100*d.effective_cost,
        'Model minus midpoint (pp)':[_range(100*(r.model_low-r.market_midpoint),100*(r.model_high-r.market_midpoint)) if pd.notna(r.market_midpoint) else 'Unavailable' for r in d.itertuples()],
        'Model versus purchase cost':[('Unavailable' if pd.isna(r.effective_cost) else 'Model lower bound exceeds cost' if r.model_low>r.effective_cost else 'Model upper bound is below cost' if r.model_high<r.effective_cost else 'Bounds overlap cost; value is unresolved') for r in d.itertuples()],
        'Selected-side probability (%)':[_range(100*r.model_low,100*r.model_high) for r in d.itertuples()],
        'Entry price (¢/share)':100*d.entry_price,'Taker fee (¢/share)':100*d.fee_per_share,
        'Stress-only extra friction (¢/share)':scanner['settings']['friction_cents'],
        f'Total budget for {shares:g} shares ($)':shares*d.effective_cost,
        'Expected net profit ($)':[_range(shares*r.edge_low_pp/100,shares*r.edge_high_pp/100) for r in d.itertuples()],
        'Stressed expected net profit ($)':shares*d.stressed_edge_pp/100,
        'Expected return on budget (%)':[_range(100*r.edge_low_pp/(100*r.effective_cost),100*r.edge_high_pp/(100*r.effective_cost)) if pd.notna(r.effective_cost) and r.effective_cost>0 else 'Unavailable' for r in d.itertuples()]})


def display_full(frame):
    """Render full names, columns and rows without pandas ellipsis truncation."""
    from IPython.display import display, HTML
    display(HTML('<div style="overflow-x:auto">'+frame.to_html(index=False,escape=True,na_rep='Unavailable',float_format=lambda x:f'{x:.2f}')+'</div>'))


def publish(scanner,directory):
    import matplotlib.pyplot as plt
    import textwrap
    from pathlib import Path
    import election_lab as lab
    directory=Path(directory)
    for key in ['details','summary','audit']:scanner[key].to_parquet(directory/f'scanner_{key}.parquet',index=False)
    lab.write_json(directory/'scanner_settings.json',scanner['settings'])
    from polymarket_debug_view import publish as publish_grouped
    return publish_grouped(scanner,directory)
