"""Sustained favorable price paths after model signals; no exit/fill simulation."""
import json
import numpy as np
import pandas as pd
from download_polymarket_history import ROOT, OUT, CACHE
from polymarket_edge_strategy import DEADLINES, probability_band

METHOD='''Each model is evaluated separately at the same twelve historical check dates. Local forecasts must match the check date. Publisher forecasts must be dated on or before it and at most six days old; superseded versions are excluded. A forecast is usable after its dated day ends (UTC). The reference price is the first valid daily observation within the following 36 hours. No final result or future model update selects a signal. Both sides are retained as controls; a positive edge is initial model probability minus initial side price, without fees or an assumed trade.

We follow prices for 7, 14 and 30 days, strictly before the election. A sustained level is the lowest of three consecutive daily observations, spanning at least 36 hours, with no gap above 36 hours and no invalid observation between them. The largest such level is a hindsight path diagnostic, not a chosen exit. A qualifying move exceeds the larger of the initial positive edge and a 2-cent noise floor. Sensitivities use 1/2/3 cents and 2/3/5 consecutive observations. Days after the election are never substituted for a missing horizon. Primary hit rates use only full windows with at least 80% of expected daily observations and a valid endpoint within 36 hours. Incomplete windows remain visible and are not scored as failures.

Tables show case-weighted results and equal-market averages; dates within a race overlap and are not independent evidence. Hit rates alone do not rank calibration: large edges set harder targets. Compare sustained rises, endpoint changes, and edge bands as well. The paired-model table holds market and check date fixed, allowing each model its own signal side. A matched descriptive baseline uses other markets with nonpositive edge for the same model, cycle, horizon, check-date month and 5-percentage-point starting-price bin. Each control is tested against the signal's exact target; at least three control observations from two other markets are required. Missing matches stay missing. This comparison is descriptive, not a causal or held-out test.

Activity bands use distinct on-chain transaction hashes (CLOB) or distinct trade-event identifiers (legacy pools) during the seven days strictly before the reference time. This is a past-trading-activity proxy, not order-book depth or executable liquidity. Total lifetime market volume is never used. Unknown archive coverage stays Unknown. Neither persistent daily prices nor archive fills prove tradable size; this analysis reports potential setups, not earned profits.'''


def path_metrics(history,entry_time,entry_price,side,horizon,deadline,persistence=3,allow_partial=False):
    end=entry_time+pd.Timedelta(days=horizon)
    base=dict(complete=False,reason='Horizon reaches election',sustained_rise=np.nan,endpoint_change=np.nan,
              worst_change=np.nan,observations=0,levels=[],times=[],worsts=[])
    truncated=end>=deadline
    if truncated and not allow_partial:return base
    if truncated:end=deadline-pd.Timedelta(nanoseconds=1)
    q=history[(history.timestamp>entry_time)&(history.timestamp<=end)].sort_values('timestamp').copy()
    q['value']=q.price_first if side=='D' else 1-q.price_first
    # At most one actual observation per UTC day; never forward-fill inactivity.
    q=q.groupby(q.timestamp.dt.floor('D'),sort=False).tail(1).reset_index(drop=True)
    valid=q.value.between(0,1)
    count=int(valid.sum());endpoint=q.iloc[-1] if len(q) else None
    complete=(not truncated and count>=int(np.ceil(.8*horizon)) and endpoint is not None and bool(valid.iloc[-1])
              and end-endpoint.timestamp<=pd.Timedelta(hours=36))
    levels=[];times=[];worsts=[]
    values=q.value.to_numpy(dtype=float)
    stamps=q.timestamp.astype('int64').to_numpy()
    valid_values=(values>=0)&(values<=1)
    prior_min=np.minimum.accumulate(np.where(valid_values,values,np.inf))
    for i in range(persistence-1,len(q)):
        start=i-persistence+1
        if not valid_values[start:i+1].all():continue
        if np.diff(stamps[start:i+1]).max()>pd.Timedelta(hours=36).value:continue
        if stamps[i]-stamps[start]<pd.Timedelta(hours=18*(persistence-1)).value:continue
        levels.append(float(values[start:i+1].min()-entry_price));times.append(q.timestamp.iloc[i])
        worsts.append(min(0,float(prior_min[i]-entry_price)))
    return dict(complete=complete,reason='Complete' if complete else 'Horizon reaches election' if truncated else 'Sparse or stale path',
        sustained_rise=max(levels) if levels else np.nan,
        endpoint_change=float(endpoint.value-entry_price) if complete else np.nan,
        worst_change=min(0,float(q.loc[valid,'value'].min()-entry_price)) if count else np.nan,
        observations=count,levels=levels,times=times,worsts=worsts)


def activity_history():
    path=CACHE/'senate_archive/observations.parquet'
    if not path.exists():return {},set()
    q=pd.read_parquet(path,columns=['market_id','event_id','timestamp'])
    # Event IDs contain a block/log index, not a transaction hash. Resolve CLOB
    # hashes from raw records to avoid counting counterpart fill events twice.
    hashes=[]
    for raw in sorted((CACHE/'senate_archive/selected/order_filled').rglob('*.parquet')):
        hashes.append(pd.read_parquet(raw,columns=['id','transactionHash']))
    lookup=pd.concat(hashes,ignore_index=True).drop_duplicates('id').set_index('id').transactionHash if hashes else pd.Series(dtype=str)
    q['transaction']=q.event_id.map(lookup).fillna(q.event_id)
    q=q.drop_duplicates(['market_id','transaction'])
    groups={mid:g.timestamp.sort_values() for mid,g in q.groupby('market_id')}
    coverage_path=ROOT/'outputs/results/research/senate_archive/coverage.parquet'
    known=set(groups)
    if coverage_path.exists():
        c=pd.read_parquet(coverage_path)
        known.update(c.loc[c.status.eq('no_recorded_trades_zero_volume'),'market_id'])
    return groups,known


def summarize(detail,keys):
    rows=[]
    for key,g in detail.groupby(keys,dropna=False):
        key=key if isinstance(key,tuple) else (key,)
        s=g[g.edge.gt(1e-9)];q=s[s.complete]
        bymarket=q.groupby('market_id').hit.mean()
        matched=q[q.baseline_hit.notna()]
        rows.append(dict(zip(keys,key),signals=len(s),markets=s.market_id.nunique(),scored=len(q),scored_markets=q.market_id.nunique(),
            hit_pct=100*q.hit.mean(),equal_market_hit_pct=100*bymarket.mean(),
            rise_cents=100*q.sustained_rise.mean(),edge_cents=100*q.edge.mean(),
            endpoint_cents=100*q.endpoint_change.mean(),worst_cents=100*q.worst_change.mean(),
            days_to_hit=q.days_to_hit.mean(),worst_before_hit_cents=100*q.worst_before_hit.mean(),
            median_edge_covered=q.covered_edge.median(),
            matched=len(matched),baseline_pct=100*matched.baseline_hit.mean(),
            matched_hit_pct=100*matched.hit.mean(),lift_pp=100*(matched.hit-matched.baseline_hit).mean()))
    return pd.DataFrame(rows)


def analyze(samples,prices,local,publishers,activity=None):
    dates=local[['cycle','forecast_date']].drop_duplicates().copy()
    dates.forecast_date=pd.to_datetime(dates.forecast_date,utc=True)
    mapping=samples[['cycle','state','market_id']].drop_duplicates()
    if mapping.duplicated(['cycle','state']).any():raise ValueError('Ambiguous state market')
    local=local[['cycle','geography','model_code','forecast_date','p_dem']].rename(columns={'model_code':'model','geography':'state'}).copy()
    publishers=publishers.rename(columns={'geography':'state'}).copy()
    for q in [local,publishers]:q['forecast_date']=pd.to_datetime(q.forecast_date,utc=True)
    if 'valid_until' not in publishers:publishers['valid_until']=pd.NaT
    publishers['valid_until']=pd.to_datetime(publishers.valid_until,utc=True)
    prices=prices.copy();prices['timestamp']=pd.to_datetime(prices.timestamp,utc=True)
    if prices.duplicated(['market_id','timestamp']).any():raise ValueError('Duplicate price observation')
    activities,known=activity if activity is not None else ({},set())
    rows=[];audit=[]
    for m in mapping.itertuples(index=False):
        h=prices[prices.market_id.eq(m.market_id)].sort_values('timestamp')
        deadline=pd.Timestamp(DEADLINES[m.cycle],tz='UTC')
        for date in dates.loc[dates.cycle.eq(m.cycle),'forecast_date'].sort_values():
            available=date+pd.Timedelta(days=1)
            forecasts=local[local.cycle.eq(m.cycle)&local.state.eq(m.state)&local.forecast_date.eq(date)]
            ext=publishers[publishers.cycle.eq(m.cycle)&publishers.state.eq(m.state)&publishers.forecast_date.le(date)
                &publishers.forecast_date.ge(date-pd.Timedelta(days=6))]
            ext=ext.sort_values('forecast_date').groupby('model',sort=False).tail(1)
            forecasts=pd.concat([v for v in [forecasts,ext] if len(v)],ignore_index=True) if len(forecasts)+len(ext) else forecasts.copy()
            if 'valid_until' not in forecasts:forecasts['valid_until']=pd.NaT
            forecasts['valid_until']=pd.to_datetime(forecasts.valid_until,utc=True)
            quotes=h[h.timestamp.ge(available)&h.timestamp.le(available+pd.Timedelta(hours=36))&h.timestamp.lt(deadline)]
            if quotes.empty or not 0<quotes.iloc[0].price_first<1:
                audit.append(dict(cycle=m.cycle,state=m.state,check_date=date,reason='No valid fresh entry observation'));continue
            entry=quotes.iloc[0]
            fs=forecasts[forecasts.valid_until.isna()|forecasts.valid_until.gt(entry.timestamp)]
            expected=set(local.loc[local.cycle.eq(m.cycle),'model'])|set(publishers.loc[publishers.cycle.eq(m.cycle),'model'])
            for missing in expected-set(fs.model):audit.append(dict(cycle=m.cycle,state=m.state,check_date=date,model=missing,reason='No fresh unsuperseded forecast'))
            if fs.model.duplicated().any():raise ValueError('Duplicate model forecast')
            events=activities.get(m.market_id,pd.Series([],dtype='datetime64[ns, UTC]'))
            count=int((events.ge(entry.timestamp-pd.Timedelta(days=7))&events.lt(entry.timestamp)).sum()) if m.market_id in known else np.nan
            band='Unknown' if pd.isna(count) else '0 transactions' if count==0 else '1–9 transactions' if count<10 else '10–99 transactions' if count<100 else '100+ transactions'
            for side in ['D','R']:
                price=float(entry.price_first if side=='D' else 1-entry.price_first)
                for horizon in [7,14,30]:
                    for persistence in [2,3,5]:
                        path=path_metrics(h,entry.timestamp,price,side,horizon,deadline,persistence)
                        levels=np.array(path.pop('levels'));times=path.pop('times');worsts=path.pop('worsts')
                        for f in fs.itertuples(index=False):
                            p=float(f.p_dem if side=='D' else 1-f.p_dem)
                            if not -1e-9<=p<=1+1e-9:raise ValueError('Invalid forecast probability')
                            p=float(np.clip(p,0,1));edge=p-price
                            for floor in [.01,.02,.03]:
                                threshold=max(edge,floor);hits=np.flatnonzero(levels>=threshold-1e-12)
                                first=int(hits[0]) if len(hits) else None
                                rows.append(dict(cycle=m.cycle,state=m.state,market_id=m.market_id,check_date=date,model=f.model,
                                    model_date=f.forecast_date,model_age_days=(entry.timestamp-f.forecast_date).total_seconds()/86400,
                                    entry_time=entry.timestamp,side=side,price=price,probability=p,edge=edge,
                                    probability_band=probability_band(price),price_bin=int(np.floor(price*20)),month=date.month,
                                    edge_band='Nonpositive' if edge<=1e-9 else '<2¢' if edge<.02 else '2–5¢' if edge<.05 else '5–10¢' if edge<.1 else '10¢+',
                                    prior_transactions=count,activity_band=band,horizon=horizon,persistence=persistence,noise_cents=100*floor,
                                    threshold=threshold,hit=float(first is not None) if path['complete'] else np.nan,
                                    days_to_hit=(times[first]-entry.timestamp).total_seconds()/86400 if first is not None else np.nan,
                                    worst_before_hit=worsts[first] if first is not None else np.nan,
                                    covered_edge=path['sustained_rise']/edge if edge>1e-9 else np.nan,
                                    **path))
    detail=pd.DataFrame(rows);detail['baseline_hit']=np.nan;detail['baseline_controls']=0
    # Compute matched controls only for primary settings, preserving each signal's
    # own target rather than making control successes easier to achieve.
    primary=detail[detail.persistence.eq(3)&detail.noise_cents.eq(2)]
    for _,g in primary[primary.complete].groupby(['cycle','model','horizon','month','price_bin']):
        controls=g[g.edge.le(1e-9)]
        for i,r in g[g.edge.gt(1e-9)].iterrows():
            c=controls[controls.market_id.ne(r.market_id)]
            if len(c)>=3 and c.market_id.nunique()>=2:
                detail.at[i,'baseline_hit']=float(c.sustained_rise.ge(r.threshold-1e-12).mean())
                detail.at[i,'baseline_controls']=len(c)
    primary=detail[detail.persistence.eq(3)&detail.noise_cents.eq(2)]
    result=dict(detail=detail,audit=pd.DataFrame(audit),summary=summarize(primary,['cycle','model','horizon']),
        probabilities=summarize(primary,['cycle','horizon','probability_band','model']),
        activities=summarize(primary,['cycle','horizon','activity_band','model']),
        edges=summarize(primary,['cycle','horizon','edge_band','model']),
        states=summarize(primary,['cycle','horizon','state','model']),
        sensitivity=summarize(detail,['cycle','horizon','persistence','noise_cents','model']))
    pairs=[]
    selected=primary[primary.edge.gt(1e-9)&primary.complete]
    for (year,horizon),g in selected.groupby(['cycle','horizon']):
        models=sorted(g.model.unique())
        for i,a in enumerate(models):
            for b in models[i+1:]:
                keys=['market_id','check_date']
                q=g[g.model.eq(a)].merge(g[g.model.eq(b)],on=keys,suffixes=('_a','_b'),validate='one_to_one')
                if q.empty:continue
                pairs.append(dict(cycle=year,horizon=horizon,model_a=a,model_b=b,cases=len(q),markets=q.market_id.nunique(),
                    hit_a=100*q.hit_a.mean(),hit_b=100*q.hit_b.mean(),rise_a=100*q.sustained_rise_a.mean(),rise_b=100*q.sustained_rise_b.mean(),
                    same_side_pct=100*q.side_a.eq(q.side_b).mean()))
    result['paired']=pd.DataFrame(pairs)
    return result


def summary_table(q):
    return q[['model','signals','scored','scored_markets','hit_pct','rise_cents','endpoint_cents']].rename(columns={
        'model':'Model','signals':'Signals','scored':'Scored','scored_markets':'Scored markets','hit_pct':'Target (%)',
        'rise_cents':'Sustained rise (¢)','endpoint_cents':'End Δ (¢)'})


def report(result):
    lines=['## Sustained price moves after model signals','',METHOD,'',
        'GB: Gaussian Bayesian; ST: matched Student-t; OG: older Gaussian; OS: older Student-t; MX: four-model mixture; M10: mixture shifted 10% toward polling; 538: Deluxe; 538C: Classic; 538L: Lite; RTWH: Race to the WH; ECON: Economist original 2022 model (September 7 to October 30); DDHQ0: original 2024 DDHQ; DDHQ: revised 2024 DDHQ (August 27 onward).',
        '', 'A fixed 2-cent floor is unreachable when the starting price exceeds 98 cents. Those observations remain in their high-probability band; low hit rates there are partly mechanical. Scored 2022 coverage is sparse and cannot establish a reliable model ranking.', '']
    status_path=OUT/'signal_publisher_status.parquet'
    if status_path.exists():
        status=pd.read_parquet(status_path)
        status['publisher']=status.model.str.replace(r' (?:[A-Z]{2})$','',regex=True)
        status=status.groupby(['cycle','publisher','status'],as_index=False).agg(rows=('rows','sum'))
        lines += ['### Publisher retrieval coverage','',status.to_markdown(index=False),'']
    lines += [available_report(result)]
    lines += ['### Supplemental evidence: publishers on their actual forecast dates','',NATIVE_METHOD,'']
    for (year,horizon),q in result['native_summary'].groupby(['cycle','horizon']):
        lines += [f'#### {year}: {horizon} days after each publisher snapshot','',native_table(q).to_markdown(index=False),'']
    lines += ['Confirmed setups may include incomplete windows; they are not the numerator of the full-window percentage. Exact dates, probabilities, source URLs and unscored paths are saved in `signal_quality_native_detail.parquet`.','']
    lines += [target_report(result)]
    for (year,horizon),q in result['summary'].groupby(['cycle','horizon']):
        lines += [f'### {year}: {horizon}-day sustained moves','',summary_table(q).to_markdown(index=False,floatfmt='.2f'),'']
        d=q[['model','equal_market_hit_pct','matched','matched_hit_pct','baseline_pct','lift_pp']]
        lines += ['Equal-market target rates and matched nonpositive-edge baseline (percentage points; blank means insufficient matches):','',d.to_markdown(index=False,floatfmt='.2f'),'']
        lines += ['Time and adverse movement for qualifying paths; median fraction of initial edge covered across scored paths:','',q[['model','days_to_hit','worst_before_hit_cents','median_edge_covered']].to_markdown(index=False,floatfmt='.2f'),'']
    for label,key,group in [('Starting probability','probabilities','probability_band'),('Prior seven-day trading activity','activities','activity_band'),('Initial edge','edges','edge_band'),('State','states','state')]:
        for (year,band),q in result[key].query('horizon==30').groupby(['cycle',group]):
            if q.signals.sum()==0:continue
            lines += [f'### {year}: {label} — {band} (30 days)','',summary_table(q).to_markdown(index=False,floatfmt='.2f'),'']
    lines+=['### Matched model comparisons: same market and check date (30 days)','',result['paired'].query('horizon==30').drop(columns='horizon').to_markdown(index=False,floatfmt='.2f'),'']
    lines+=['### Persistence and noise sensitivity (30 days)','',result['sensitivity'].query('horizon==30')[['cycle','model','persistence','noise_cents','scored','hit_pct']].to_markdown(index=False,floatfmt='.2f'),'']
    return '\n'.join(lines).replace('nan','—')+'\n'


def charts(result,destination):
    import matplotlib.pyplot as plt
    files=[]
    for year,q in result['summary'].groupby('cycle'):
        fig,axes=plt.subplots(1,2,figsize=(12,4.8))
        for model,g in q.groupby('model'):
            axes[0].plot(g.horizon,g.hit_pct,marker='o',label=model)
            axes[1].plot(g.horizon,g.rise_cents,marker='o',label=model)
        for ax in axes:ax.set_xticks([7,14,30]);ax.set_xlabel('Forward days');ax.grid(alpha=.3)
        axes[0].set_ylabel('Signals reaching sustained target (%)');axes[1].set_ylabel('Mean largest sustained rise (¢)')
        axes[1].axhline(0,color='gray',lw=.7);axes[0].legend(ncol=3,fontsize=8)
        fig.suptitle(f'{year}: potential setups, not trading returns\n3 daily observations; target ≥ initial edge and ≥2¢; coverage varies')
        fig.tight_layout();path=destination/f'signal_quality_{year}.png';fig.savefig(path,dpi=140);plt.close(fig);files.append(path)
    for key,group,label in [('probabilities','probability_band','Starting probability'),('activities','activity_band','Past seven-day activity')]:
        for year,q in result[key].query('horizon==30').groupby('cycle'):
            values=q.pivot(index='model',columns=group,values='hit_pct')
            order=[probability_band(x) for x in [.05,.2,.5,.8,.95]] if key=='probabilities' else ['0 transactions','1–9 transactions','10–99 transactions','100+ transactions','Unknown']
            values=values.reindex(columns=[x for x in order if x in values.columns])
            counts=q.pivot(index='model',columns=group,values='scored').reindex_like(values)
            fig,ax=plt.subplots(figsize=(10, max(4,len(values)*.4)))
            im=ax.imshow(np.ma.masked_invalid(values.to_numpy()),vmin=0,vmax=100,cmap='YlGnBu',aspect='auto')
            ax.set_xticks(range(len(values.columns)),values.columns,rotation=15,ha='right',fontsize=8)
            ax.set_yticks(range(len(values)),values.index)
            for i in range(len(values)):
                for j in range(len(values.columns)):
                    value=values.iloc[i,j];n=counts.iloc[i,j]
                    ax.text(j,i,f'{value:.0f}% (n={n:.0f})' if pd.notna(value) else 'No scored paths',ha='center',va='center',fontsize=8,color='white' if pd.notna(value) and value>50 else 'black')
            ax.set_xticks(np.arange(-.5,len(values.columns),1),minor=True);ax.set_yticks(np.arange(-.5,len(values),1),minor=True)
            ax.grid(which='minor',color='white',linewidth=2);ax.tick_params(which='minor',bottom=False,left=False)
            ax.set_title(f'{year}: {label} — sustained target reached within 30 days\n3 daily observations; ≥ initial edge and ≥2¢; n = overlapping cases')
            fig.colorbar(im,ax=ax,label='Target reached (%)');fig.tight_layout()
            path=destination/f'signal_quality_{key}_{year}.png';fig.savefig(path,dpi=140);plt.close(fig);files.append(path)
    for (panel,year),q in result['target_summary'].query('horizon==30').groupby(['panel','cycle']):
        values=q.pivot(index='model',columns='target',values='hit_pct').reindex(columns=list(RETURN_TARGETS))
        counts=q.pivot(index='model',columns='target',values='scored').reindex_like(values)
        fig,ax=plt.subplots(figsize=(9,max(4,len(values)*.42)))
        im=ax.imshow(np.ma.masked_invalid(values.to_numpy()),vmin=0,vmax=100,cmap='YlGnBu',aspect='auto')
        ax.set_xticks(range(len(values.columns)),values.columns);ax.set_yticks(range(len(values)),values.index)
        for i in range(len(values)):
            for j in range(len(values.columns)):
                value=values.iloc[i,j]
                ax.text(j,i,f'{value:.1f}% (n={counts.iloc[i,j]:.0f})' if pd.notna(value) else 'Not scored',ha='center',va='center',fontsize=8,color='white' if pd.notna(value) and value>50 else 'black')
        ax.set_xticks(np.arange(-.5,len(values.columns),1),minor=True);ax.set_yticks(np.arange(-.5,len(values),1),minor=True)
        ax.grid(which='minor',color='white',linewidth=2);ax.tick_params(which='minor',bottom=False,left=False)
        ax.set_title(f'{year}: {panel} — sustained targets within 30 days\nRelative price increases; 2¢ minimum; 3 daily observations; complete windows only')
        fig.colorbar(im,ax=ax,label='Target reached (%)');fig.tight_layout()
        path=destination/f'signal_quality_targets_{panel.lower().replace(" ","_")}_{year}.png';fig.savefig(path,dpi=140);plt.close(fig);files.append(path)
    return files


NATIVE_METHOD='''Supplemental publisher evidence uses every recovered dated snapshot during the June-to-election research season, even a single snapshot. Each forecast is evaluated only on its own date, using the first market observation within 36 hours after that date ends. No interpolation, stale carry-forward, minimum sample count, or requirement that another model exists is applied. Known publication/version restrictions still apply. The target remains the larger of the initial edge and 2 cents, sustained across three daily observations. This is a different observation set from the shared-date comparison and must not be used as a head-to-head ranking.

Confirmed setups count actually observed sustained moves, including those inside incomplete or election-truncated windows. An incomplete path without such a move is Unknown, not a failure. Target rates use only complete windows. Forecast-date counts, markets, and sample-size labels stay visible; daily updates and overlapping paths are related observations, not independent opportunities or profits.'''


def publisher_native(samples,prices,publishers,activity=None):
    mapping=samples[['cycle','state','market_id']].drop_duplicates()
    if mapping.duplicated(['cycle','state']).any():raise ValueError('Ambiguous native market mapping')
    pubs=publishers.rename(columns={'geography':'state'}).merge(mapping,on=['cycle','state'],validate='many_to_one').copy()
    pubs['forecast_date']=pd.to_datetime(pubs.forecast_date,utc=True)
    if 'valid_until' not in pubs:pubs['valid_until']=pd.NaT
    pubs['valid_until']=pd.to_datetime(pubs.valid_until,utc=True)
    if pubs.duplicated(['cycle','state','model','forecast_date']).any():raise ValueError('Duplicate native forecast')
    prices=prices.copy();prices.timestamp=pd.to_datetime(prices.timestamp,utc=True)
    rows=[];audit=[];memo={}
    activities,known=activity if activity is not None else ({},set())
    for mid,forecasts in pubs.groupby('market_id'):
        h=prices[prices.market_id.eq(mid)].sort_values('timestamp')
        if h.timestamp.duplicated().any():raise ValueError('Duplicate native price')
        for f in forecasts.itertuples(index=False):
            date=f.forecast_date;available=date+pd.Timedelta(days=1)
            deadline=pd.Timestamp(DEADLINES[f.cycle],tz='UTC')
            if date<pd.Timestamp(f'{f.cycle}-06-01',tz='UTC') or available>=deadline:continue
            common=dict(cycle=f.cycle,state=f.state,market_id=mid,model=f.model,model_date=date)
            quotes=h[h.timestamp.ge(available)&h.timestamp.le(available+pd.Timedelta(hours=36))&h.timestamp.lt(deadline)]
            if quotes.empty or not 0<quotes.iloc[0].price_first<1:
                audit.append(dict(**common,reason='No valid fresh entry observation'));continue
            entry=quotes.iloc[0]
            if pd.notna(f.valid_until) and entry.timestamp>=f.valid_until:
                audit.append(dict(**common,reason='Superseded forecast'));continue
            if not np.isfinite(f.p_dem) or not -1e-9<=f.p_dem<=1+1e-9:raise ValueError('Invalid native probability')
            p=float(np.clip(f.p_dem,0,1));edge=p-float(entry.price_first)
            if abs(edge)<=1e-9:
                audit.append(dict(**common,reason='No positive edge'));continue
            side='D' if edge>0 else 'R';edge=abs(edge)
            price=float(entry.price_first if side=='D' else 1-entry.price_first)
            probability=p if side=='D' else 1-p;target=max(edge,.02)
            events=activities.get(mid,pd.Series([],dtype='datetime64[ns, UTC]'))
            count=int((events.ge(entry.timestamp-pd.Timedelta(days=7))&events.lt(entry.timestamp)).sum()) if mid in known else np.nan
            activity_band='Unknown' if pd.isna(count) else '0 transactions' if count==0 else '1–9 transactions' if count<10 else '10–99 transactions' if count<100 else '100+ transactions'
            for horizon in [7,14,30]:
                key=(mid,entry.timestamp,side,horizon)
                if key not in memo:memo[key]=path_metrics(h,entry.timestamp,price,side,horizon,deadline,allow_partial=True)
                path=memo[key];hits=np.flatnonzero(np.asarray(path['levels'])>=target-1e-12)
                confirmed=bool(len(hits));first=int(hits[0]) if confirmed else None
                rows.append(dict(**common,entry_time=entry.timestamp,side=side,price=price,probability=probability,
                    edge=edge,horizon=horizon,threshold=target,complete=path['complete'],confirmed=confirmed,
                    prior_transactions=count,activity_band=activity_band,
                    outcome='Confirmed setup' if confirmed else 'No setup in complete window' if path['complete'] else 'Unknown: incomplete window',
                    reason=path['reason'],sustained_rise=path['sustained_rise'],observations=path['observations'],
                    days_to_hit=(path['times'][first]-entry.timestamp).total_seconds()/86400 if confirmed else np.nan,
                    source_url=getattr(f,'source_url',''),provenance=getattr(f,'provenance','')))
    detail=pd.DataFrame(rows);summary=[]
    for (year,model,horizon),g in detail.groupby(['cycle','model','horizon']):
        complete=g[g.complete];unknown=g[~g.complete & ~g.confirmed]
        dates=g.model_date.nunique();markets=g.market_id.nunique()
        summary.append(dict(cycle=year,model=model,horizon=horizon,signals=len(g),dates=dates,markets=markets,
            confirmed=int(g.confirmed.sum()),partial_confirmed=int((g.confirmed&~g.complete).sum()),
            unknown=len(unknown),scored=len(complete),hit_pct=100*complete.confirmed.mean(),
            evidence='Single-date evidence' if dates==1 else 'Limited dates/markets' if dates<5 or markets<3 else 'Overlapping observations'))
    return dict(native_detail=detail,native_summary=pd.DataFrame(summary),native_audit=pd.DataFrame(audit))


def native_table(q):
    return pd.DataFrame({'Model':q.model,'Dates':q.dates,'Markets':q.markets,
        'Setups / signals':q.confirmed.astype(str)+' / '+q.signals.astype(str),
        'Unknown':q.unknown,'Full-window target':q.apply(lambda r:f'{r.hit_pct:.1f}% (n={r.scored})' if r.scored else 'Not scored',axis=1),
        'Evidence':q.evidence})


def build(samples,prices,local,out):
    path=out/'signal_publisher_history.parquet'
    if not path.exists():
        from polymarket_signal_publishers import collect_extended
        collect_extended(offline=True)
    activity=activity_history()
    result=analyze(samples,prices,local,pd.read_parquet(path),activity)
    result.update(publisher_native(samples,prices,pd.read_parquet(path),activity))
    result.update(target_study(result))
    result.update(available_model_study(result,set(local.model_code)))
    for name,table in result.items():table.to_parquet(out/f'signal_quality_{name}.parquet',index=False)
    (out/'signal_quality_config.json').write_text(json.dumps(dict(method=METHOD,horizons=[7,14,30],noise_cents=[1,2,3],persistence=[2,3,5],max_publisher_age_days=6,return_targets=RETURN_TARGETS,target_method=TARGET_METHOD),indent=2)+'\n')
    return result


RETURN_TARGETS={'Edge':None,'5%':.05,'10%':.10,'20%':.20,'50%':.50}
TARGET_METHOD='''Percentage targets mean relative increases from the initial market price, not percentage-point increases in probability. Required rise = max(starting price × target percentage, 2 cents). Signals still require positive model edge, but percentage targets do not require the price to cover the whole edge. The original Edge target = max(initial model edge, 2 cents) remains alongside them. Every target must persist across three consecutive daily observations. No sale or executable return is assumed. At 10 cents, both 5% and 10% require a 2-cent rise; at 50 cents, they require 2.5 and 5 cents. Targets above the $1 payoff ceiling remain visible and count as unattainable, not silently excluded.

Targets are compared on identical signal observations within each panel and horizon. Full-window percentages use only complete windows; witnessed setups in partial publisher paths are reported separately. Shared check dates and publisher snapshot dates are different panels, not directly comparable model rankings. Repeated snapshots and overlapping windows are not independent samples. Previously reported matched-control lift applies only to the original Edge target, not these new percentage targets.'''


def target_threshold(price,edge,target):
    return max(edge if RETURN_TARGETS[target] is None else price*RETURN_TARGETS[target],.02)


def target_study(result):
    shared=result['detail'].query('persistence==3 and noise_cents==2 and edge>1e-9').copy()
    native=result['native_detail'].copy()
    for q in [shared,native]:
        if 'probability_band' not in q:q['probability_band']=q.price.map(probability_band)
        if 'activity_band' not in q:q['activity_band']='Not classified in native panel'
    frames=[]
    for panel,source in [('Shared dates',shared),('Publisher dates',native)]:
        for name,fraction in RETURN_TARGETS.items():
            q=source[['cycle','state','market_id','model','model_date','entry_time','side','price','edge','horizon','complete','sustained_rise','probability_band','activity_band']].copy()
            q['panel']=panel;q['target']=name
            q['threshold']=np.maximum(q.edge if fraction is None else q.price*fraction,.02)
            q['attainable']=q.price+q.threshold<=1+1e-12
            q['confirmed']=q.sustained_rise.ge(q.threshold-1e-12)
            frames.append(q)
    detail=pd.concat(frames,ignore_index=True)
    def aggregate(keys):
        rows=[]
        for key,g in detail.groupby(keys,dropna=False):
            complete=g[g.complete];hits=complete[complete.confirmed]
            rows.append(dict(zip(keys,key),signals=len(g),dates=g.model_date.nunique(),markets=g.market_id.nunique(),
                confirmed=int(g.confirmed.sum()),confirmed_markets=g.loc[g.confirmed,'market_id'].nunique(),
                partial_confirmed=int((g.confirmed & ~g.complete).sum()),unknown=int((~g.complete & ~g.confirmed).sum()),
                scored=len(complete),scored_markets=complete.market_id.nunique(),full_hits=len(hits),
                hit_pct=100*complete.confirmed.mean(),unattainable=int((~g.attainable).sum()),
                equal_market_hit_pct=100*complete.groupby('market_id').confirmed.mean().mean()))
        return pd.DataFrame(rows)
    keys=['panel','cycle','horizon','model','target']
    return dict(target_detail=detail,target_summary=aggregate(keys),
        target_probabilities=aggregate(keys+['probability_band']),target_activities=aggregate(keys+['activity_band']),
        target_states=aggregate(keys+['state']))


def target_table(rows,counts=False):
    values=rows.assign(value=rows.confirmed if counts else rows.hit_pct).pivot(index='model',columns='target',values='value').reindex(columns=list(RETURN_TARGETS))
    base=rows[rows.target.eq('Edge')].set_index('model').reindex(values.index)
    values.columns=[str(x)+(' setups' if counts else ' hit (%)') for x in values.columns]
    values.insert(0,'Signals / markets' if counts else 'Scored / markets',
        (base.signals if counts else base.scored).astype(str)+' / '+(base.markets if counts else base.scored_markets).astype(str))
    return values.reset_index().rename(columns={'model':'Model'})


def target_report(result):
    lines=['### Several sustained price-rise targets','',TARGET_METHOD,'']
    for (panel,year,horizon),q in result['target_summary'].groupby(['panel','cycle','horizon']):
        lines += [f'#### {year}: {panel}, {horizon} days — complete-window rates','',target_table(q).to_markdown(index=False,floatfmt='.1f'),'']
        if panel=='Publisher dates':
            lines += ['Confirmed setups, including witnessed moves in incomplete paths (overlapping observations):','',target_table(q,counts=True).to_markdown(index=False),'']
    for (panel,year,band),q in result['target_probabilities'].query('horizon==30').groupby(['panel','cycle','probability_band']):
        lines += [f'#### {year}: {panel}, {band}, 30 days','',target_table(q).to_markdown(index=False,floatfmt='.1f'),'']
    return '\n'.join(lines).replace('nan','—')+'\n'


MODEL_LABELS={'GB':'Gaussian Bayesian','ST':'Matched Student-t','OG':'Older Gaussian','OS':'Older Student-t',
    'MX':'Four-model mixture','M10':'Mixture with 10% polling mean shift','538':'538 Deluxe','538C':'538 Classic',
    '538L':'538 Lite','ECON':'Economist original','RTWH':'Race to the WH','DDHQ0':'DDHQ original','DDHQ':'DDHQ revised'}
AVAILABLE_METHOD='''Each model uses its own available observations. Our six local models use their twelve reconstructed forecast dates; publishers use every recovered dated snapshot. Publisher shared-date rows are excluded here to avoid double-counting. No common-state, common-date or minimum-sample filter is imposed. Missing models are displayed explicitly. These tables are descriptive comparisons, not a matched-sample ranking: different dates, markets and signal sides can explain differences.

All signals have positive model edge. Columns show sustained Edge, 5%, 10%, 20% and 50% targets, with a 2-cent minimum and three consecutive observed days. Percentages use complete windows only; the coverage table and witnessed-setup tables also retain incomplete paths. N / markets means complete forecast observations / distinct markets contributing to that row. Overlapping dates are not independent trades. A blank rate is unscored, not zero. Subsets use the purchased side's initial probability, strictly prior seven-day trading activity, and initial edge; none uses the final election outcome. Activity is not executable liquidity. Targets above $1 remain in the denominator.'''


def available_model_study(result,local_codes):
    d=result['target_detail']
    selected=d[(d.panel.eq('Shared dates')&d.model.isin(local_codes)) | (d.panel.eq('Publisher dates')&~d.model.isin(local_codes))].copy()
    selected['source_panel']=selected.panel
    selected['edge_band']=pd.cut(selected.edge,[-np.inf,.02,.05,.10,np.inf],right=False,labels=['<2¢','2–5¢','5–10¢','10¢+']).astype(str)
    if selected.duplicated(['cycle','model','market_id','entry_time','model_date','horizon','target']).any():raise ValueError('Duplicate observation in available-model comparison')
    tables={}
    for name,extra in [('overall',[]),('probabilities',['probability_band']),('activities',['activity_band']),('edges',['edge_band']),('states',['state'])]:
        keys=['cycle','horizon','model','target']+extra;rows=[]
        for key,g in selected.groupby(keys,dropna=False):
            complete=g[g.complete]
            rows.append(dict(zip(keys,key),signals=len(g),dates=g.model_date.nunique(),markets=g.market_id.nunique(),
                scored=len(complete),scored_markets=complete.market_id.nunique(),full_hits=int(complete.confirmed.sum()),
                hit_pct=100*complete.confirmed.mean(),confirmed=int(g.confirmed.sum()),
                partial_confirmed=int((g.confirmed&~g.complete).sum()),unknown=int((~g.confirmed&~g.complete).sum()),
                unattainable=int((~g.attainable).sum()),equal_market_hit_pct=100*complete.groupby('market_id').confirmed.mean().mean(),
                first_date=g.model_date.min(),last_date=g.model_date.max()))
        tables['available_'+name]=pd.DataFrame(rows)
    return tables


def available_table(rows,counts=False):
    q=target_table(rows,counts=counts).set_index('Model')
    return q.reindex(list(MODEL_LABELS)).reset_index()


def available_coverage(rows):
    q=rows[rows.target.eq('Edge')].set_index('model').reindex(list(MODEL_LABELS))
    def span(r):
        return r.first_date.strftime('%b %d')+'–'+r.last_date.strftime('%b %d') if pd.notna(r.first_date) else 'Unavailable'
    return pd.DataFrame({'Model':q.index,'Forecast dates':q.apply(span,axis=1).values,
        'Dates':q.dates.values,'Signals':q.signals.values,'Markets':q.markets.values,
        'Complete paths':q.scored.values,'Partial paths':(q.signals-q.scored).values})


def available_report(result):
    lines=['## All models on their own available observations','',AVAILABLE_METHOD,'',
        pd.DataFrame(MODEL_LABELS.items(),columns=['Code','Model']).to_markdown(index=False),'']
    for (year,horizon),q in result['available_overall'].groupby(['cycle','horizon']):
        lines += [f'### {year}: {horizon}-day targets, every model','',available_table(q).to_markdown(index=False,floatfmt='.1f'),'']
        if horizon==30:
            lines += ['Coverage (observations overlap):','',available_coverage(q).to_markdown(index=False,floatfmt='.0f'),'']
            lines += ['Observed sustained setups, including witnesses in incomplete paths:','',available_table(q,counts=True).to_markdown(index=False,floatfmt='.0f'),'']
    for key,group,title in [('probabilities','probability_band','Starting probability'),('activities','activity_band','Past trading activity'),('edges','edge_band','Initial edge'),('states','state','State')]:
        for (year,band),q in result['available_'+key].query('horizon==30').groupby(['cycle',group]):
            if not q.signals.sum():continue
            lines += [f'### {year}: {title} — {band} (30 days)','',available_table(q).to_markdown(index=False,floatfmt='.1f'),'']
    return '\n'.join(lines).replace('nan','—')+'\n'
