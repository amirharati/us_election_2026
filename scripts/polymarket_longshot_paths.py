"""Exploratory pre-resolution long-shot price paths; no executable-fill claims."""
import numpy as np
import pandas as pd

METHOD='''This exploratory test asks whether model-backed long shots later rose in price. It does not estimate election-win accuracy or prove executable profits. Entry cohorts use saved model check dates from June through October. A date-only forecast is used only after the following UTC midnight. Entry is the first daily price observation within 36 hours after that time. The side must cost 1–10 cents at entry; sub-cent outcomes are excluded. The fixed signal requires model value at least 2 cents above that entry proxy. All models are shown separately, alongside buying every eligible long shot. No final election outcome is used to select entries.

The preset exit target is twice the entry price. A target hit requires a strictly later daily observation at or above that level, before November 3 00:00 UTC. The simulated exit is credited at the target, not the hindsight peak. Otherwise use the final observed price before that deadline, no more than seven days old. Missing or drained-pool observations prevent claiming a complete path. Daily snapshots can miss intraday target touches; observed prices are not executable bids/asks or evidence of depth. Complemented Democratic-win prices proxy the Republican side; historical sell quotes are unavailable.

The summary reports observed target touches, whether two consecutive observations within two days both reached the target, price direction after 7/14/30 days, and equal-share gross exit-minus-entry. Forward comparisons use a price at or before each horizon no more than two days old; horizons after the deadline stay missing. Worst observed changes describe the full price path, not losses on an already closed position. A configurable round-trip cost sensitivity subtracts 0, 1 or 2 cents per share; these are assumptions, not reconstructed historical fees. Overlapping entry dates reuse the same markets, capital and future paths: rows are not independent trades or a deployable portfolio. Model probabilities value final resolution and do not estimate the probability or timing of a temporary price rise. Parameters are exploratory choices, not optimized or out-of-sample validated.'''


def trace_path(history,entry_time,entry_price,dem_side,deadline,target_multiple=2.,max_exit_age_days=7):
    h=history[(history.timestamp>entry_time)&(history.timestamp<deadline)].sort_values('timestamp').copy()
    h['price']=h.price_first if dem_side else 1-h.price_first
    valid=h[h.price.between(0,1)]
    target=entry_price*target_multiple
    hits=valid[valid.price.ge(target)]
    hit=hits.iloc[0] if len(hits) else None
    # Unknown intervals invalidate execution inference, even if a later point exists.
    first_bad=h[h.price.isna()|~h.price.between(0,1)]
    invalid_before_hit=not first_bad.empty and (hit is None or first_bad.timestamp.iloc[0]<hit.timestamp)
    last=h.iloc[-1] if len(h) else None
    deadline_ok=last is not None and pd.notna(last.price) and 0<=last.price<=1 and (deadline-last.timestamp)<=pd.Timedelta(days=max_exit_age_days)
    complete=not invalid_before_hit and (hit is not None or deadline_ok)
    exit_price=target if hit is not None else float(last.price) if deadline_ok else np.nan
    if not complete:exit_price=np.nan
    above=h.price.ge(target)
    confirmed=above & above.shift(1,fill_value=False) & h.timestamp.diff().le(pd.Timedelta(days=2))
    forward={}
    for days in [7,14,30]:
        end=entry_time+pd.Timedelta(days=days)
        q=h[h.timestamp.le(end)] if end<deadline else h.iloc[:0]
        last_forward=q.iloc[-1] if len(q) else None
        ok=last_forward is not None and pd.notna(last_forward.price) and end-last_forward.timestamp<=pd.Timedelta(days=2)
        forward[f'change_{days}d']=float(last_forward.price)-entry_price if ok else np.nan
    return dict(**forward,confirmed_double=bool(confirmed.any()),target_price=target,observed_double=bool(hit is not None),hit_time=hit.timestamp if hit is not None else pd.NaT,
        days_to_double=(hit.timestamp-entry_time).total_seconds()/86400 if hit is not None else np.nan,
        max_price=float(valid.price.max()) if len(valid) else np.nan,
        worst_change=min(0,float(valid.price.min())-entry_price) if len(valid) else np.nan,
        deadline_price=float(last.price) if deadline_ok else np.nan,
        deadline_up=bool(last.price>entry_price) if deadline_ok else None,
        exit_price=exit_price,exit_reason='Target proxy' if complete and hit is not None else 'Deadline proxy' if complete else 'Incomplete path',
        gross_change=exit_price-entry_price if complete else np.nan,
        observations=len(valid),complete=complete)


def analyze(samples,prices,min_price=.01,max_price=.10,min_edge=.02):
    rows=[];audit=[]
    prices=prices.copy();prices.timestamp=pd.to_datetime(prices.timestamp,utc=True)
    if prices.duplicated(['market_id','timestamp']).any():raise ValueError('Ambiguous duplicate historical price')
    for (year,state,date),g in samples.groupby(['cycle','state','check_date']):
        deadline=pd.Timestamp(f'{year}-11-03',tz='UTC');available=date+pd.Timedelta(days=1)
        if available>=deadline:continue
        if g.market_id.nunique()!=1 or g.model.duplicated().any():raise ValueError('Ambiguous market/model mapping')
        market_id=g.market_id.iloc[0]
        h=prices[prices.market_id.eq(market_id)].sort_values('timestamp')
        entry_candidates=h[h.timestamp.ge(available)&h.timestamp.le(available+pd.Timedelta(hours=36))&h.timestamp.lt(deadline)]
        if entry_candidates.empty:
            audit.append(dict(cycle=year,state=state,check_date=date,reason='No fresh post-forecast entry observation'));continue
        entry=entry_candidates.iloc[0]
        if pd.isna(entry.price_first):
            audit.append(dict(cycle=year,state=state,check_date=date,reason='Invalid pool/price at entry'));continue
        dem_side=entry.price_first<=.5
        price=float(entry.price_first if dem_side else 1-entry.price_first)
        if not min_price-1e-12<=price<=max_price+1e-12:
            audit.append(dict(cycle=year,state=state,check_date=date,reason='Outside 1–10 cent entry range'));continue
        # Common-model panel ensures signal comparisons see identical opportunities.
        expected=set(samples[samples.cycle.eq(year)].model.unique())
        if set(g.model)!=expected or g.model_probability.isna().any():
            audit.append(dict(cycle=year,state=state,check_date=date,reason='Not available for every compared model'));continue
        if (g.model_date>date).any():raise ValueError('Future model snapshot')
        result=trace_path(h,entry.timestamp,price,dem_side,deadline)
        common=dict(cycle=year,state=state,market_id=market_id,side='D' if dem_side else 'R',check_date=date,
            entry_time=entry.timestamp,entry_price=price,price_source=entry.price_source,**result)
        rows.append(dict(**common,model='All long shots',model_probability=np.nan,edge=np.nan,selected=True))
        for f in g.itertuples():
            probability=float(f.model_probability if dem_side else 1-f.model_probability)
            if not -1e-9<=probability<=1+1e-9:raise ValueError('Invalid model probability')
            probability=np.clip(probability,0,1);edge=probability-price
            rows.append(dict(**common,model=f.model,model_probability=probability,edge=edge,selected=edge>=min_edge-1e-12))
    detail=pd.DataFrame(rows)
    summary=[]
    for (year,model),g in detail.groupby(['cycle','model']):
        for label,sub in [('Selected',g[g.selected]),('Not selected',g[~g.selected])]:
            if model=='All long shots' and label=='Not selected':continue
            complete=sub[sub.complete]
            for cost in [0.,.01,.02]:
                summary.append(dict(cycle=year,model=model,signal=label,cost_cents=cost*100,cases=len(sub),markets=sub.market_id.nunique(),
                    complete=len(complete),double_pct=100*complete.observed_double.mean() if len(complete) else np.nan,
                    deadline_up_pct=100*complete.deadline_up.dropna().mean() if len(complete.deadline_up.dropna()) else np.nan,
                    mean_entry_cents=100*complete.entry_price.mean(),net_cents=100*(complete.gross_change.mean()-cost),
                    mean_worst_change_cents=100*complete.worst_change.mean(),
                    confirmed_double_pct=100*complete.confirmed_double.mean() if len(complete) else np.nan,
                    **{f'up_{days}d_pct':100*sub[f'change_{days}d'].dropna().gt(0).mean() for days in [7,14,30]},
                    **{f'n_{days}d':int(sub[f'change_{days}d'].notna().sum()) for days in [7,14,30]}))
    return dict(detail=detail,summary=pd.DataFrame(summary),audit=pd.DataFrame(audit))


def summary_table(rows):
    return rows[['model','cases','markets','complete','double_pct','net_cents']].rename(columns={
        'model':'Model','cases':'Signals','markets':'Markets','complete':'Scored','double_pct':'Doubled (%)','net_cents':'Net/share (¢)'})


def cases_table(rows):
    return pd.DataFrame({'State/side':rows.state+'/'+rows.side,'Signal date':rows.check_date.dt.strftime('%b %d'),
        'Entry (¢)':100*rows.entry_price,'Model (¢)':100*rows.model_probability,'Peak (¢)':100*rows.max_price,
        'Doubled':rows.observed_double.map({True:'Yes',False:'No'}),'Exit Δ (¢)':100*rows.gross_change})


def report(r):
    lines=['## Long-shot price rises before November 3','',METHOD,'']
    for (year,cost),q in r['summary'].query('signal=="Selected"').groupby(['cycle','cost_cents']):
        lines += [f'### {year} — round-trip assumption: {cost:g}¢ per share','',summary_table(q).to_markdown(index=False,floatfmt='.2f'),'']
    for (year,signal),q in r['summary'].query('cost_cents==0').groupby(['cycle','signal']):
        lines += [f'### {year} — {signal}: price direction and target persistence','',direction_table(q).to_markdown(index=False),'']
    for (year,model),q in r['detail'].query('selected and model!="All long shots"').groupby(['cycle','model']):
        lines += [f'### {year} — {model}: every selected case','',cases_table(q).to_markdown(index=False,floatfmt='.2f'),'']
    lines += ['Peak is a hindsight diagnostic, not the assumed sale price. Incomplete paths have blank exit changes. Case-level timestamps and source receipts remain in the research tables.','']
    return '\n'.join(lines)+'\n'


def build(samples,prices,out):
    result=analyze(samples,prices)
    for name,table in result.items():table.to_parquet(out/f'longshot_paths_{name}.parquet',index=False)
    return result


def direction_table(rows):
    q=rows.copy();result=pd.DataFrame({'Model':q.model})
    for days in [7,14,30]:
        result[f'Up after {days}d']=q.apply(lambda r:f"{r[f'up_{days}d_pct']:.0f}% ({r[f'n_{days}d']} cases)" if r[f'n_{days}d'] else 'Unavailable',axis=1)
    result['Double confirmed (%)']=q.confirmed_double_pct.round(1)
    return result


def charts(result,prices,destination):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    colors={'GB':'#3366aa','ST':'#dd8844','MX':'#24845d','M10':'#a14d97','538':'#887133','RTWH':'#7c68b1'}
    files=[]
    selected=result['detail'].query('selected and model!="All long shots"')
    for year,g in selected.groupby('cycle'):
        cases=list(g.groupby(['state','side','market_id']))
        fig,axes=plt.subplots((len(cases)+1)//2,2,figsize=(12,3*((len(cases)+1)//2)),squeeze=False)
        for ax,((state,side,market_id),q) in zip(axes.flat,cases):
            h=prices[prices.market_id.eq(market_id)&prices.timestamp.ge(q.entry_time.min())&prices.timestamp.lt(pd.Timestamp(f'{year}-11-03',tz='UTC'))]
            price=h.price_first if side=='D' else 1-h.price_first
            ax.plot(h.timestamp,100*price,color='black',lw=1,label='Observed price')
            for model,r in q.groupby('model'):
                ax.scatter(r.entry_time,100*r.entry_price,s=28,facecolors='none',edgecolors=colors[model],label=model)
            ax.set_title(f'{state}: {side} side');ax.set_ylabel('Cents per share');ax.grid(alpha=.25)
            ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3,maxticks=5));ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        handles={}
        for ax in axes.flat:
            hh,ll=ax.get_legend_handles_labels();handles.update(zip(ll,hh))
        for ax in list(axes.flat)[len(cases):]:ax.set_visible(False)
        fig.legend(handles.values(),handles.keys(),loc='upper center',bbox_to_anchor=(.5,.965),ncol=7,fontsize=8)
        fig.suptitle(f'{year}: long-shot paths — circles mark model signals, not fills')
        fig.tight_layout(rect=(0,0,1,.92))
        path=destination/f'longshot_price_paths_{year}.png';fig.savefig(path,dpi=130);plt.close(fig);files.append(path)
    return files
