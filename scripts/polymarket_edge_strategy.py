"""Independent-model positive-EV entries and chronological value-based exits."""
import json
import numpy as np
import pandas as pd

DEADLINES={2022:'2022-11-08',2024:'2024-11-05'}
METHOD='''Each model trades independently on every reviewed state-win market for which it has a forecast. Other models' views or availability never determine its entries. Models can cover different markets, so totals are not a matched-universe ranking. Positions contain 100 shares, with at most one open side per market/model. Forecasts become available at 00:00 UTC after their recorded date; local forecasts update at the saved 12 cutoffs, and publishers use their available historical series. Between updates the most recent forecast is retained, with its date recorded. Prices and forecasts are processed chronologically. No election result is consulted to choose a trade.

Buy the side whose model probability exceeds its all-in purchase cost; the main rule uses strictly positive EV, not the previous two-cent threshold. Purchase cost is the observed price plus an assumed per-side execution allowance. Net sale proceeds are the observed price minus that allowance, floored at zero. These symmetric allowances proxy spread/slippage/fees, not historical executable bids/asks or actual fee schedules. The main assumption is 0.5 cents per side; zero and one cent per side are sensitivities. A missing/invalid price cannot create a trade. Exact zero/one quotes cannot open positions.

The main rule exits when net sale proceeds reach the latest model value of the held side. This can realize a loss after a model revision. A separate variant also exits at a 20% net gain over all-in entry cost. Decisions execute at the current observed price proxy, without using a later peak. A robustness variant requires the edge-exit condition on two consecutive usable observations no more than two days apart; it executes at the second price, not the first. There is no same-observation re-entry. A later observation may reopen either side, so all costs and turnover are retained.

Positions close at the last usable price before general-election day (Nov8,2022; Nov5,2024), no more than three days old. No new entries are permitted in the final 24 hours, which are reserved for exits. Unpriced final positions remain explicitly unscored. The entire simulation starts June1. Results compare the same entered lots with holding to that pre-election close and, when a binary contract payout is known, to settlement. These are matched-entry counterfactuals, not separately simulated buy-and-hold portfolios; repeated entries would overlap under holding.

Entry-price bands refer to the side purchased: <=10%, 10–30%, 30–70%, 70–90%, and >=90%. They are frozen when the trade opens. Totals assume funding every signal, with no capital constraint or interest; 100-share sizing means unequal dollars at risk across probability levels. Return on turnover is not a portfolio return. No fill/depth data, independent model selection, rare-event guarantee or pristine historical publication-vintage replay is claimed. One-day spikes may dominate price-proxy exits; inspect the confirmation sensitivity and state trades before drawing conclusions.'''


def probability_band(p):
    if p<=.1:return 'Long shot (<=10%)'
    if p<.3:return 'Underdog (10–30%)'
    if p<=.7:return 'Competitive (30–70%)'
    if p<.9:return 'Favorite (70–90%)'
    return 'High probability (>=90%)'


def forecast_streams(samples,local,publishers):
    mapping=samples[['cycle','state','market_id']].drop_duplicates()
    if mapping.duplicated(['cycle','state']).any():raise ValueError('Multiple state contracts')
    own=local.rename(columns={'geography':'state','model_code':'code'})
    own=own[['cycle','state','code','forecast_date','p_dem']].rename(columns={'code':'model','forecast_date':'model_date','p_dem':'probability'})
    ext=publishers.rename(columns={'geography':'state','forecast_date':'model_date','p_dem':'probability'})[['cycle','state','model','model_date','probability']]
    result=pd.concat([q for q in [own,ext] if not q.empty],ignore_index=True).merge(mapping,on=['cycle','state'],validate='many_to_one')
    result['model_date']=pd.to_datetime(result.model_date,utc=True)
    result['available_at']=result.model_date+pd.Timedelta(days=1)
    # Trading starts June 1 in simulate_market; retain earlier information here
    # so the initial signal uses the latest known forecast, including May.
    if result.duplicated(['cycle','market_id','model','available_at']).any():raise ValueError('Duplicate dated model forecast')
    if (~result.probability.between(-1e-9,1+1e-9)).any():raise ValueError('Invalid forecast probability')
    result['probability']=result.probability.clip(0,1)
    return result.sort_values(['cycle','market_id','model','available_at'])


def simulate_market(forecasts,prices,*,cycle,state,market_id,model,cost=.005,rule='Edge',shares=100,profit_target=.20,confirmations=1,payout=np.nan):
    if cost<0 or shares<=0 or confirmations not in (1,2) or rule not in ('Edge','Edge + profit'):raise ValueError('Invalid strategy parameters')
    deadline=pd.Timestamp(DEADLINES[cycle],tz='UTC');start=pd.Timestamp(f'{cycle}-06-01',tz='UTC')
    f=forecasts.sort_values('available_at').reset_index(drop=True)
    h=prices[(prices.timestamp>=start)&(prices.timestamp<deadline)].sort_values('timestamp')
    if h.timestamp.duplicated().any():raise ValueError('Duplicate price timestamp')
    valid=h[h.price_first.between(0,1)]
    last=valid.iloc[-1] if len(valid) else None
    terminal=last if last is not None and deadline-last.timestamp<=pd.Timedelta(days=3) else None
    position=None;trades=[];i=-1;streak=0;previous_condition_time=None

    def close(time,raw,reason,current):
        nonlocal position
        p=position
        sale=max(0.,raw-cost) if pd.notna(raw) else np.nan
        terminal_price=(float(terminal.price_first) if p['side']=='D' else 1-float(terminal.price_first)) if terminal is not None else np.nan
        terminal_sale=max(0.,terminal_price-cost) if pd.notna(terminal_price) else np.nan
        resolved=(float(payout) if p['side']=='D' else 1-float(payout)) if payout in (0,1) else np.nan
        trades.append(dict(**p,exit_time=time,exit_price=raw,net_sale=sale,exit_reason=reason,
            exit_model_date=current.model_date if current is not None else pd.NaT,
            exit_model_probability=(current.probability if p['side']=='D' else 1-current.probability) if current is not None else np.nan,
            pnl=shares*(sale-p['entry_cost']),hold_close_pnl=shares*(terminal_sale-p['entry_cost']),
            hold_settlement_pnl=shares*(resolved-p['entry_cost']),settlement_available=pd.notna(resolved),
            holding_days=(time-p['entry_time']).total_seconds()/86400 if pd.notna(time) else np.nan,
            complete=pd.notna(sale)))
        position=None

    for quote in h.itertuples(index=False):
        while i+1<len(f) and f.available_at.iloc[i+1]<=quote.timestamp:i+=1
        if i<0:continue
        current=f.iloc[i]
        if not np.isfinite(quote.price_first) or not 0<=quote.price_first<=1:
            streak=0;previous_condition_time=None;continue
        if position is not None:
            value=float(current.probability if position['side']=='D' else 1-current.probability)
            raw=float(quote.price_first if position['side']=='D' else 1-quote.price_first)
            net=max(0.,raw-cost)
            edge_gone=net>=value-1e-12
            target=rule=='Edge + profit' and net>=position['entry_cost']*(1+profit_target)
            if edge_gone:
                streak=streak+1 if previous_condition_time is not None and quote.timestamp-previous_condition_time<=pd.Timedelta(days=2) else 1
                previous_condition_time=quote.timestamp
            else:streak=0;previous_condition_time=None
            reason='Edge gone' if edge_gone and streak>=confirmations else 'Profit target' if target else None
            if reason:
                close(quote.timestamp,raw,reason,current);streak=0;previous_condition_time=None
            continue
        if quote.timestamp>=deadline-pd.Timedelta(days=1) or not 0<quote.price_first<1:continue
        choices=[('D',float(quote.price_first),float(current.probability)),('R',float(1-quote.price_first),float(1-current.probability))]
        side,raw,value=max(choices,key=lambda x:x[2]-x[1]-cost)
        entry_cost=raw+cost
        if value-entry_cost<=1e-9 or entry_cost>=1:continue
        position=dict(cycle=cycle,state=state,market_id=market_id,model=model,rule=rule,cost_cents=100*cost,
            confirmations=confirmations,shares=shares,side=side,band=probability_band(raw),entry_time=quote.timestamp,
            entry_price=raw,entry_cost=entry_cost,entry_model_probability=value,entry_edge=value-entry_cost,
            entry_model_date=current.model_date,entry_available_at=current.available_at,
            entry_model_age_days=(quote.timestamp-current.model_date).total_seconds()/86400,
            price_source=getattr(quote,'price_source','Unspecified'))
    if position is not None:
        if terminal is not None and terminal.timestamp>=position['entry_time']:
            known=f[f.available_at.le(terminal.timestamp)].iloc[-1]
            raw=float(terminal.price_first if position['side']=='D' else 1-terminal.price_first)
            close(terminal.timestamp,raw,'Pre-election close',known)
        else:close(pd.NaT,np.nan,'Unpriced final position',f.iloc[i] if i>=0 else None)
    return trades


def summarize(trades,keys):
    rows=[]
    for key,g in trades.groupby(keys,dropna=False):
        key=key if isinstance(key,tuple) else (key,)
        q=g[g.complete];hold=q[q.hold_settlement_pnl.notna()];marked=q[q.hold_close_pnl.notna()]
        rows.append(dict(zip(keys,key),trades=len(g),markets=g.market_id.nunique(),scored=len(q),
            deployed=float((g.shares*g.entry_cost).sum()),pnl=float(q.pnl.sum()) if len(q) else np.nan,
            hold_close_pnl=float(marked.hold_close_pnl.sum()) if len(marked) else np.nan,
            close_scored=len(marked),exit_pnl_close_paired=float(marked.pnl.sum()) if len(marked) else np.nan,
            hold_settlement_pnl=float(hold.hold_settlement_pnl.sum()) if len(hold) else np.nan,
            settlement_scored=len(hold),exit_pnl_settlement_paired=float(hold.pnl.sum()) if len(hold) else np.nan,
            profitable_pct=100*q.pnl.gt(0).mean(),edge_exits=int(q.exit_reason.eq('Edge gone').sum()),
            target_exits=int(q.exit_reason.eq('Profit target').sum()),mean_days=q.holding_days.mean()))
    return pd.DataFrame(rows)


def matched_coverage(trades,coverage):
    """Post-hoc same-state comparison; never changes a model's trade decisions."""
    panels=[];rows=[]
    for year,c in coverage.groupby('cycle'):
        c=c[c.forecasts.gt(0)&c.prices.gt(0)]
        counts=c.groupby('state').model.nunique();states=counts[counts.eq(c.model.nunique())].index
        panels.append(trades[trades.cycle.eq(year)&trades.state.isin(states)])
        rows.append(dict(cycle=year,states=len(states),models=c.model.nunique(),included=', '.join(states)))
    paired=pd.concat(panels,ignore_index=True)
    keys=['cycle','model','rule','cost_cents','confirmations']
    return summarize(paired,keys),pd.DataFrame(rows)


def build(samples,prices,local,publishers,markets,out):
    streams=forecast_streams(samples,local,publishers);rows=[];coverage=[]
    prices=prices.copy();prices.timestamp=pd.to_datetime(prices.timestamp,utc=True)
    payouts=markets.set_index('market_id').payout_first.to_dict()
    configs=[(rule,c,1) for rule in ['Edge','Edge + profit'] for c in [0.,.005,.01]]+[('Edge',.005,2)]
    for (year,state,market_id,model),f in streams.groupby(['cycle','state','market_id','model']):
        h=prices[prices.market_id.eq(market_id)]
        end=pd.Timestamp(DEADLINES[year],tz='UTC');start=pd.Timestamp(f'{year}-06-01',tz='UTC')
        f=f[f.available_at.lt(end)];h=h[h.timestamp.ge(start)&h.timestamp.lt(end)]
        coverage.append(dict(cycle=year,state=state,market_id=market_id,model=model,forecasts=len(f),prices=len(h)))
        for rule,c,confirmation in configs:
            rows.extend(simulate_market(f,h,cycle=year,state=state,market_id=market_id,model=model,
                cost=c,rule=rule,confirmations=confirmation,payout=payouts.get(market_id,np.nan)))
    trades=pd.DataFrame(rows)
    keys=['cycle','model','rule','cost_cents','confirmations']
    result=dict(trades=trades,summary=summarize(trades,keys),bands=summarize(trades,keys+['band']),
        states=summarize(trades,keys+['state']),coverage=pd.DataFrame(coverage))
    result['matched_summary'],result['matched_coverage']=matched_coverage(trades,result['coverage'])
    for name,table in result.items():table.to_parquet(out/f'edge_strategy_{name}.parquet',index=False)
    (out/'edge_strategy_config.json').write_text(json.dumps(dict(shares=100,main_rule='Edge',main_cost_per_side=.005,
        profit_target=.20,entry_threshold='strictly positive net EV',deadlines=DEADLINES,independent_models=True),indent=2)+'\n')
    return result


def summary_table(q):
    return q[['model','trades','markets','scored','pnl','hold_close_pnl']].rename(columns={
        'model':'Model','trades':'Trades','markets':'Markets','scored':'Scored','pnl':'Exit P&L ($)','hold_close_pnl':'Hold to close ($)'})


def trade_table(q):
    return pd.DataFrame({'Race/side':q.state+'/'+q.side,'Buy':q.entry_time.dt.strftime('%b %d'),
        'Sell':q.exit_time.dt.strftime('%b %d'),'Buy (¢)':100*q.entry_cost,'Sell (¢)':100*q.net_sale,
        'P&L ($)':q.pnl,'Exit':q.exit_reason})


def report(result):
    lines=['## Independent-model positive-EV strategy','',METHOD,'']
    for (year,rule,cost,confirm),q in result['summary'].groupby(['cycle','rule','cost_cents','confirmations']):
        lines += [f'### {year} — {rule}; {cost:g}¢ per side; {confirm} observation(s)','',summary_table(q).fillna('').to_markdown(index=False,floatfmt='.2f'),'']
    main='rule=="Edge" and cost_cents==0.5 and confirmations==1'
    lines += ['### Strategy model legend','',
        'GB: Gaussian Bayesian; ST: matched Student-t; OG: older Gaussian; OS: older Student-t research model; MX: four-model mixture; M10: mixture with a 10% polling mean shift; 538: FiveThirtyEight Deluxe (2022); RTWH: Race to the WH (2024). OG and OS are also mixture components, so these alternatives are not independent evidence.','']
    for year,q in result['matched_summary'].query(main).groupby('cycle'):
        cover=result['matched_coverage'].query('cycle==@year').iloc[0]
        lines += [f'### {year} — same {cover.states} states for every model','',
            'States: '+cover.included+'. Forecast update frequencies and chosen trades still differ. This is a reporting comparison, not a model-agreement entry filter.','',summary_table(q).fillna('').to_markdown(index=False,floatfmt='.2f'),'']
    for year,q in result['summary'].query(main).groupby('cycle'):
        lines += [f'### {year} — hold-to-settlement comparison','',
            'Only entries with known binary contract payouts enter this paired comparison. Missing settlements remain blank.','',
            q[['model','settlement_scored','exit_pnl_settlement_paired','hold_settlement_pnl']].fillna('').to_markdown(index=False,floatfmt='.2f'),'']
    for year,q in result['states'].query(main).groupby('cycle'):
        lines += [f'### {year} — state-level edge-exit P&L','',q.pivot(index='state',columns='model',values='pnl').fillna('').to_markdown(floatfmt='.2f'),'']
    for (year,model),q in result['bands'].query(main).groupby(['cycle','model']):
        lines += [f'### {year} — {model}: entry-price bands','',q[['band','trades','pnl','hold_close_pnl','hold_settlement_pnl','settlement_scored']].fillna('').to_markdown(index=False,floatfmt='.2f'),'']
    for (year,model),q in result['trades'].query(main).groupby(['cycle','model']):
        lines += [f'### {year} — {model}: every main-rule trade','',trade_table(q).fillna('').to_markdown(index=False,floatfmt='.2f'),'']
    return '\n'.join(lines)+'\n'


def charts(result,destination):
    import matplotlib.pyplot as plt
    files=[]
    main=result['summary'].query('rule=="Edge" and cost_cents==0.5 and confirmations==1')
    for year,q in main.groupby('cycle'):
        q=q.sort_values('model');x=np.arange(len(q));fig,ax=plt.subplots(figsize=(9,4))
        ax.bar(x-.18,q.pnl,.36,label='Edge exit / forced close',color='#397daa')
        ax.bar(x+.18,q.hold_close_pnl,.36,label='Same entries held to close',color='#bbaa77')
        ax.set_xticks(x,q.model);ax.set_ylabel('Price-proxy P&L ($)');ax.axhline(0,color='black',lw=.8);ax.grid(axis='y',alpha=.25);ax.set_axisbelow(True)
        ax.set_title(f'{year}: 100 shares per trade; 0.5¢ per side\nIndependent model coverage; no execution/depth or capital constraint')
        ax.legend(fontsize=9);fig.tight_layout();path=destination/f'edge_strategy_{year}.png';fig.savefig(path,dpi=140);plt.close(fig);files.append(path)
    return files
