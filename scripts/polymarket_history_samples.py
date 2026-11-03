"""Readable model / market / result samples at explicit historical dates."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from download_polymarket_history import ROOT, OUT
from polymarket_backtest import MODELS, mapping

from historical_model_forecasts import DATES as SAMPLE_DATES
COLUMNS = ['cycle','state','market_id','question','url','check_date','model','model_date','market_time',
           'model_probability','market_probability','final_winner','final_margin_pp','status','result_source','price_source','market_age_days']


def prepare_samples(markets, prices, local, publishers, dates=SAMPLE_DATES, max_forecast_age_days=6, max_market_age_days=7):
    """Use exact-date local inference and latest earlier publisher snapshots.

    Market prices are the last observation before cutoff-day end, at most seven
    days old. No future quote, local forecast carry-forward or interpolation.
    """
    local=local[local.model_code.isin(MODELS.values())].copy()
    local['forecast_date']=pd.to_datetime(local.forecast_date,utc=True)
    publishers=publishers.copy()
    publishers['forecast_date']=pd.to_datetime(publishers.forecast_date,utc=True)
    prices=prices.copy();prices['timestamp']=pd.to_datetime(prices.timestamp,utc=True)
    candidates=[]
    for m in markets.itertuples(index=False):
        state,party,reason=mapping(m)
        if not reason and party=='D':candidates.append((m,state))
    # A consistent Democratic-win contract for every date/model in each state.
    candidates.sort(key=lambda item:int(item[0].market_id))
    seen=set();rows=[];availability=[]
    for m,state in candidates:
        if (m.cycle,state) in seen:continue
        seen.add((m.cycle,state))
        forecasts=local[local.cycle.eq(m.cycle)&local.geography.eq(state)]
        actuals=forecasts.actual.dropna().unique()
        if len(actuals)>1:raise ValueError('Historical election labels disagree across model rows')
        actual=actuals[0] if len(actuals)==1 else np.nan
        final=('D' if actual>0 else 'R' if actual<0 else 'Tie') if pd.notna(actual) else 'Unavailable'
        h=prices[prices.market_id.eq(m.market_id)].sort_values('timestamp')
        for month_day in dates:
            cutoff=pd.Timestamp(f'{m.cycle}-{month_day}',tz='UTC')
            available=cutoff+pd.Timedelta(days=1)
            matches=h[h.timestamp.lt(available)&h.timestamp.ge(available-pd.Timedelta(days=max_market_age_days))]
            quote=matches.iloc[-1] if len(matches) else None
            if quote is not None and pd.isna(quote.price_first):quote=None
            selected=[]
            for model in MODELS.values():
                q=forecasts[forecasts.model_code.eq(model)&forecasts.forecast_date.eq(cutoff)]
                if len(q)>1:raise ValueError('Multiple local forecasts at one cutoff')
                availability.append(dict(cycle=m.cycle,state=state,check_date=cutoff,model=model,available=not q.empty,
                                         reason='' if not q.empty else 'No exact-date local inference is available; not carried forward.'))
                if not q.empty:
                    f=q.iloc[0];selected.append((model,f.forecast_date,float(f.p_dem)))
            ext=publishers[publishers.cycle.eq(m.cycle)&publishers.geography.eq(state)&
                publishers.forecast_date.le(cutoff)&publishers.forecast_date.ge(cutoff-pd.Timedelta(days=max_forecast_age_days))]
            for model in publishers[publishers.cycle.eq(m.cycle)].model.unique():
                q=ext[ext.model.eq(model)].sort_values('forecast_date')
                availability.append(dict(cycle=m.cycle,state=state,check_date=cutoff,model=model,available=not q.empty,
                                         reason='' if not q.empty else 'No publisher snapshot within the allowed six-day age.'))
                if not q.empty:
                    f=q.iloc[-1];selected.append((model,f.forecast_date,float(f.p_dem)))
            for model,forecast_date,p in selected:
                status='Matched'
                if quote is None:status='No market price within the previous seven days'
                if pd.isna(actual):status+='; final election label unavailable'
                # Resolution information is evaluation-only, never an input to date selection.
                if pd.notna(m.payout_first) and pd.notna(actual) and m.payout_first!=float(actual>0):
                    status+='; settlement and election label disagree'
                rows.append(dict(cycle=m.cycle,state=state,market_id=m.market_id,question=m.question,url=m.url,
                    check_date=cutoff,model=model,model_date=forecast_date,
                    market_time=quote.timestamp if quote is not None else pd.NaT,
                    model_probability=p,market_probability=float(quote.price_first) if quote is not None else np.nan,
                    final_winner=final,final_margin_pp=float(actual*100) if pd.notna(actual) else np.nan,
                    price_source=quote.get('price_source','Unspecified') if quote is not None else '',
                    market_age_days=(available-quote.timestamp).total_seconds()/86400 if quote is not None else np.nan,
                    status=status,result_source='Saved election label; D-minus-R margin' if pd.notna(actual) else 'Unavailable'))
    return pd.DataFrame(rows,columns=COLUMNS),pd.DataFrame(availability)


def sample_table(rows):
    """Six narrow columns. Every probability means a Democratic win."""
    q=rows.sort_values('check_date')
    return pd.DataFrame({
        'Check date':q.check_date.dt.strftime('%b %d'),
        'Model date':q.model_date.dt.strftime('%b %d'),
        'Market time (UTC)':q.market_time.dt.strftime('%b %d %H:%M'),
        'Model (%)':100*q.model_probability,
        'Market (%)':100*q.market_probability,
        'Final winner':q.final_winner,
    })


def build_samples(dates=SAMPLE_DATES):
    samples,availability=prepare_samples(pd.read_parquet(OUT/'markets.parquet'),pd.read_parquet(OUT/'prediction_prices.parquet'),
        pd.read_parquet(OUT/'dated_forecasts.parquet'),
        pd.read_parquet(OUT/'publisher_history.parquet') if (OUT/'publisher_history.parquet').exists() else
        pd.DataFrame(columns=['cycle','geography','forecast_date','model','p_dem']),dates)
    samples.to_parquet(OUT/'date_samples.parquet',index=False)
    availability.to_parquet(OUT/'date_sample_availability.parquet',index=False)
    overall_samples(samples).to_parquet(OUT/'date_sample_overall.parquet',index=False)
    chamber_market_samples(pd.read_parquet(OUT/'markets.parquet'),pd.read_parquet(OUT/'prediction_prices.parquet'),pd.read_parquet(ROOT/'outputs/results/experiments/portfolio/seats.parquet'),dates).to_parquet(OUT/'date_sample_chamber.parquet',index=False)
    return samples,availability


def report_section(samples,states=None,cycle=None):
    lines=['## Accuracy and distance from the market','',
        'Lower Brier scores mean better probability predictions against the observed winner. Lower gap means closer to the market; it does not establish better accuracy. Each date uses the same priced states across its available models. Coverage can change across dates.','']
    overall=overall_samples(samples)
    for (year,date),q in overall.groupby(['cycle','check_date']):
        table=q[['model','priced_states','model_brier','market_brier','gap_pp']].rename(columns={'model':'Model','priced_states':'States','model_brier':'Brier','market_brier':'Market Brier','gap_pp':'Gap (pp)'})
        lines += [f'### {year} — {date:%b %d}','',table.fillna('').to_markdown(index=False,floatfmt='.3f'),'']
    near=proximity(samples)
    for year,q in near.groupby('cycle'):
        rank=overall_proximity(q)
        lines += [f'### {year} — overall proximity','',
            'Equal weight per state; within each state, only dates shared by all available models are used. Smaller gap means closer. These are descriptive rankings from a small historical sample.','',rank.to_markdown(index=False,floatfmt='.3f'),'']
    selected=samples if cycle is None else samples[samples.cycle.eq(cycle)]
    if states is not None:selected=selected[selected.state.isin(states)]
    for (year,state),rows in selected.groupby(['cycle','state']):
        lines += [f'### {year} — {state} (final winner: {rows.final_winner.iloc[0]})','',
            'All values are P(D wins), in percent. A blank means unavailable.','',state_comparison_table(rows).fillna('').to_markdown(index=False,floatfmt='.1f'),'']
        q=near[near.cycle.eq(year)&near.state.eq(state)].sort_values('gap_pp')
        lines += ['**Model proximity and accuracy across shared dates**','',q[['model','dates','gap_pp','model_brier','market_brier']].to_markdown(index=False,floatfmt='.3f'),'']
        timing=rows[['check_date','model','model_date','market_time','market_age_days','price_source']].copy()
        ext=timing[~timing.model.isin(['GB','ST','MX','M10'])]
        timing=timing.drop_duplicates('check_date').set_index('check_date')
        dates=ext.assign(model_date=ext.model_date.dt.strftime('%b %d')).pivot(index='check_date',columns='model',values='model_date')
        timing=pd.DataFrame({'Market UTC':timing.market_time.dt.strftime('%b %d %H:%M'),'Age (days)':timing.market_age_days})
        for col in dates:timing[col+' date']=dates[col]
        timing.index=timing.index.strftime('%b %d');timing.index.name='Check date'
        lines += ['**Observation dates**','',timing.reset_index().fillna('').to_markdown(index=False,floatfmt='.2f'),'']
        lines += ['Price source: '+'; '.join(sorted(set(rows.price_source)-{''}))+'.','']
    return '\n'.join(lines)+'\n'


def overall_samples(samples):
    """Equal-state, common-model panel at each date; score only priced results.

    Repeated dates remain separate. Missing prices never enter a score as zero.
    """
    rows=[]
    for (year,date),g in samples.groupby(['cycle','check_date']):
        if g.duplicated(['state','model']).any():raise ValueError('Duplicate state/model sample')
        names=sorted(g.model.unique())
        valid=g[g.final_winner.isin(['D','R']) & ~g.status.str.contains('disagree',na=False)]
        counts=valid.groupby('state').model.nunique()
        states=counts[counts.eq(len(names))].index
        common=valid[valid.state.isin(states)]
        priced=common[common.market_probability.notna()]
        counts=priced.groupby('state').model.nunique()
        priced=priced[priced.state.isin(counts[counts.eq(len(names))].index)]
        for name in names:
            q=priced[priced.model.eq(name)];y=q.final_winner.eq('D').astype(float)
            rows.append(dict(cycle=year,check_date=date,model=name,common_states=len(states),priced_states=len(q),
                model_brier=float(((q.model_probability-y)**2).mean()) if len(q) else np.nan,
                market_brier=float(((q.market_probability-y)**2).mean()) if len(q) else np.nan,
                gap_pp=float((100*abs(q.model_probability-q.market_probability)).mean()) if len(q) else np.nan))
    return pd.DataFrame(rows)


def overall_table(rows):
    q=rows.sort_values('check_date')
    return pd.DataFrame({'Date':q.check_date.dt.strftime('%b %d'),'States':q.common_states,
        'With prices':q.priced_states,'Model Brier':q.model_brier,'Market Brier':q.market_brier,'Gap (pp)':q.gap_pp})


def chamber_market_samples(markets,prices,seat_results,dates=SAMPLE_DATES):
    """Display known control contracts without pretending seat totals model the VP."""
    rows=[]
    for m in markets[markets.category.eq('control')].itertuples(index=False):
        if m.outcome_first.lower() not in ['democrat','democrats','democratic']:continue
        h=prices[prices.market_id.eq(m.market_id)].sort_values('timestamp')
        results=seat_results[seat_results.cycle.eq(m.cycle)].actual_D.dropna().unique()
        if len(results)>1:raise ValueError('Saved chamber outcomes disagree')
        actual=results[0] if len(results) else np.nan
        final='D' if actual>50 else 'R' if actual<50 else 'Unavailable'
        for month_day in dates:
            cutoff=pd.Timestamp(f'{m.cycle}-{month_day}',tz='UTC');available=cutoff+pd.Timedelta(days=1)
            q=h[h.timestamp.lt(available)&h.timestamp.ge(available-pd.Timedelta(days=7))]
            quote=q.iloc[-1] if len(q) else None
            rows.append(dict(cycle=m.cycle,check_date=cutoff,market_time=quote.timestamp if quote is not None else pd.NaT,
                market_probability=float(quote.price_first) if quote is not None else np.nan,
                model_probability=np.nan,final_control=final,
                result_source='Saved portfolio actual_D outcome; caucus seats, not party-only seats.',
                reason='A reviewed chamber-control adapter is not available;2024 also requires the vice-presidential joint outcome.'))
    return pd.DataFrame(rows)


def state_comparison_table(rows):
    """One compact table per state, with all models alongside the market."""
    q=rows.pivot(index='check_date',columns='model',values='model_probability')*100
    order=[m for m in ['GB','ST','MX','M10','538','RTWH'] if m in q]
    q=q[order]
    market=rows.groupby('check_date').market_probability.first()*100
    q.insert(0,'Market',market)
    q.index=q.index.strftime('%b %d');q.index.name='Date'
    return q.reset_index()


def proximity(samples):
    """Rank distance per state on dates shared by every available model there."""
    output=[]
    valid=samples[samples.market_probability.notna() & samples.final_winner.isin(['D','R']) & ~samples.status.str.contains('disagree')]
    for (year,state),g in valid.groupby(['cycle','state']):
        names=g.model.unique();counts=g.groupby('check_date').model.nunique()
        g=g[g.check_date.isin(counts[counts.eq(len(names))].index)]
        for model,q in g.groupby('model'):
            y=q.final_winner.eq('D').astype(float)
            output.append(dict(cycle=year,state=state,model=model,dates=len(q),gap_pp=100*abs(q.model_probability-q.market_probability).mean(),
                model_brier=((q.model_probability-y)**2).mean(),market_brier=((q.market_probability-y)**2).mean()))
    return pd.DataFrame(output)


def prediction_charts(samples,overall,destination):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    files=[]
    colors={'GB':'#3366aa','ST':'#dd8844','MX':'#24845d','M10':'#a14d97','538':'#887133','RTWH':'#7c68b1'}
    for year,g in overall.groupby('cycle'):
        fig,axes=plt.subplots(1,2,figsize=(11,3.8))
        for model,q in g.groupby('model'):
            for ax,col in zip(axes,['model_brier','gap_pp']):
                ax.plot(q.check_date,q[col],'.-',label=model,color=colors.get(model))
        q=g.drop_duplicates('check_date');axes[0].plot(q.check_date,q.market_brier,'k.--',label='Market')
        for ax,title in zip(axes,['Accuracy: lower Brier is better','Distance from market: lower is closer']):
            ax.set_title(title);ax.grid(alpha=.3);ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'));ax.tick_params(axis='x',rotation=35)
        axes[0].set_ylabel('Brier score');axes[1].set_ylabel('Mean absolute gap (percentage points)')
        axes[0].legend(ncol=3,fontsize=8);fig.suptitle(f'{year}: common states at each date (coverage varies)');fig.tight_layout()
        path=destination/f'prediction_comparison_{year}.png';fig.savefig(path,dpi=140);plt.close(fig);files.append(path)
    for year,g in samples.groupby('cycle'):
        states=sorted(g.state.unique());fig,axes=plt.subplots((len(states)+2)//3,3,figsize=(12,3*((len(states)+2)//3)),squeeze=False)
        for ax,state in zip(axes.flat,states):
            rows=g[g.state.eq(state)]
            for model,q in rows.groupby('model'):
                q=q.sort_values('check_date');ax.plot(q.check_date,100*q.model_probability,label=model,color=colors.get(model),lw=1.2)
            q=rows.drop_duplicates('check_date').sort_values('check_date');ax.plot(q.check_date,100*q.market_probability,'k.--',label='Market')
            ax.set_title(f'{state} — final: {rows.final_winner.iloc[0]}');ax.set_ylim(-3,103);ax.axhline(50,color='gray',lw=.7,ls=':');ax.grid(alpha=.25)
            ax.xaxis.set_major_locator(mdates.MonthLocator());ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'));ax.set_ylabel('P(D wins), %')
        for ax in list(axes.flat)[len(states):]:ax.set_visible(False)
        handles={}
        for ax in axes.flat:
            hh,ll=ax.get_legend_handles_labels();handles.update(zip(ll,hh))
        fig.legend(handles.values(),handles.keys(),loc='upper center',ncol=6,bbox_to_anchor=(.5,1.028),fontsize=9)
        fig.suptitle(f'{year}: model, market and final result',y=1.002);fig.tight_layout()
        path=destination/f'state_probabilities_{year}.png';fig.savefig(path,dpi=130,bbox_inches='tight');plt.close(fig);files.append(path)
    return files


def overall_proximity(rows):
    """Require the same states for every model in the cycle-level ranking."""
    names=rows.model.nunique()
    counts=rows.groupby('state').model.nunique()
    common=rows[rows.state.isin(counts[counts.eq(names)].index)]
    return common.groupby('model').agg(states=('state','nunique'),gap_pp=('gap_pp','mean'),brier=('model_brier','mean')).sort_values('gap_pp').reset_index()
