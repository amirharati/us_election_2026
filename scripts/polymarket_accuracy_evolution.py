"""Paired accuracy over time, with fixed cohorts and explicit long-shot events."""
import numpy as np
import pandas as pd

METHOD = '''The main trend holds both states and models fixed from September 5 through November 3. A state must have every model, a valid market price and a known nonconflicting result at every check date. All models score the same events with equal state weights. This reduces coverage but prevents changing membership from masquerading as improving accuracy.

Competitive means Polymarket gave Democrats 30–70% on September 5. Long-shot races had a side at 10% or less on that date; that same side is followed afterward. These fixed groups can change competitiveness later. A separate hindsight group contains races whose final D-minus-R margin was within five points; it must not be used to select historical trades. The dynamic long-shot table instead selects the <=10% side anew at each date and shows its expected and actual wins, with counts. Dynamic membership changes and dates reuse outcomes; they are not independent calibration trials.

Brier is squared probability error against the observed winner; lower is better. Long-shot Brier equals the corresponding favorite's Brier, so it does not by itself measure rare-event skill. Expected upset counts provide complementary context. No trading returns are computed. Missing historical folds, publication vintages and the seven-day market/six-day publisher age limits still apply.'''


def analyze(samples, start='09-05'):
    panels=[];coverage=[];dynamic=[]
    for year,g in samples.groupby('cycle'):
        g=g[g.check_date.ge(pd.Timestamp(f'{year}-{start}',tz='UTC'))].copy()
        # Weighted simulation sums can exceed one by a few trillionths.
        for col in ['market_probability','model_probability']:
            outside=g[col].notna() & ~g[col].between(-1e-9,1+1e-9)
            if outside.any():raise ValueError('Invalid probability: '+col)
            g[col]=g[col].clip(0,1)
        if g.duplicated(['state','check_date','model']).any():raise ValueError('Duplicate comparison row')
        names=sorted(g.model.unique());dates=sorted(g.check_date.unique())
        valid=g[g.final_winner.isin(['D','R']) & ~g.status.str.contains('disagree',na=False) &
            g.market_probability.between(0,1)&g.model_probability.between(0,1)].copy()
        for _,q in valid.groupby(['state','check_date']):
            if q.market_probability.nunique()!=1 or q.final_winner.nunique()!=1:raise ValueError('Inconsistent shared event')
        counts=valid.groupby('state').size();states=counts[counts.eq(len(names)*len(dates))].index
        coverage.append(dict(cycle=year,states=len(states),models=len(names),dates=len(dates),included=', '.join(states),
            excluded=', '.join(sorted(set(g.state)-set(states)))))
        fixed=valid[valid.state.isin(states)].copy()
        anchor=fixed[fixed.check_date.eq(dates[0])].drop_duplicates('state').set_index('state').market_probability
        fixed['anchor_probability']=fixed.state.map(anchor)
        fixed['probability']=fixed.model_probability
        market=fixed.drop_duplicates(['state','check_date']).copy();market['model']='Market';market['probability']=market.market_probability
        fixed=pd.concat([fixed,market],ignore_index=True)
        fixed['outcome']=fixed.final_winner.eq('D').astype(float)
        fixed['brier']=(fixed.probability-fixed.outcome)**2
        panels.append(fixed)
        # A fair same-date panel, without requiring availability at other dates.
        ct=valid.groupby(['state','check_date']).model.nunique()
        keys=ct[ct.eq(len(names))].index
        paired=valid.set_index(['state','check_date']).loc[keys].reset_index()
        market=paired.drop_duplicates(['state','check_date']).assign(model='Market')
        market['model_probability']=market.market_probability
        paired=pd.concat([paired,market],ignore_index=True)
        paired=paired[paired.market_probability.le(.1)|paired.market_probability.ge(.9)].copy()
        dem=paired.market_probability.le(.1)
        paired['longshot_probability']=np.where(dem,paired.model_probability,1-paired.model_probability)
        paired['longshot_win']=np.where(dem,paired.final_winner.eq('D'),paired.final_winner.eq('R')).astype(int)
        for (date,model),q in paired.groupby(['check_date','model']):
            dynamic.append(dict(cycle=year,check_date=date,model=model,races=len(q),expected_wins=q.longshot_probability.sum(),actual_wins=q.longshot_win.sum(),
                brier=((q.longshot_probability-q.longshot_win)**2).mean()))
    panel=pd.concat(panels,ignore_index=True)
    metrics=[]
    groups={'All fixed states':pd.Series(True,index=panel.index),
        'Competitive on Sep 5':panel.anchor_probability.between(.3,.7),
        'Long shot on Sep 5':panel.anchor_probability.le(.1)|panel.anchor_probability.ge(.9),
        'Final margin <=5 pp (hindsight)':panel.final_margin_pp.abs().le(5)}
    for name,mask in groups.items():
        q=panel[mask]
        r=q.groupby(['cycle','check_date','model'],as_index=False).agg(races=('state','nunique'),brier=('brier','mean'))
        r['cohort']=name;metrics.append(r)
    return dict(panel=panel,metrics=pd.concat(metrics,ignore_index=True),coverage=pd.DataFrame(coverage),longshots=pd.DataFrame(dynamic))


def score_table(rows):
    t=rows.pivot(index='check_date',columns='model',values='brier')
    t=t[[c for c in ['Market','GB','ST','MX','M10','538','RTWH'] if c in t]]
    t.index=t.index.strftime('%b %d');t.index.name='Date'
    return t.reset_index()


def report(result):
    lines=['## Accuracy over time: fixed states, competitive races and long shots','',METHOD,'']
    for row in result['coverage'].itertuples():
        lines += [f'**{row.cycle}: {row.states} states, {row.models} models, {row.dates} dates.** Included: {row.included}. Excluded from this fixed panel: {row.excluded}.','']
    for (year,cohort),q in result['metrics'].groupby(['cycle','cohort']):
        lines += [f'### {year} — {cohort} ({q.races.iloc[0]} races)','',score_table(q).to_markdown(index=False,floatfmt='.4f'),'']
    lines += ['### Long shots selected at each date','', 'Expected wins sum each model’s probabilities for the same market-defined underdogs. Actual wins reuse the same eventual outcomes across dates. Empty cohorts are omitted, not scored as zero.','']
    for (year,date),q in result['longshots'].groupby(['cycle','check_date']):
        lines += [f'**{year} — {date:%b %d}**','',q[['model','races','expected_wins','actual_wins','brier']].to_markdown(index=False,floatfmt='.3f'),'']
    for (year,state),q in result['panel'].groupby(['cycle','state']):
        lines += [f'### {year} — {state}: Brier by date (final: {q.final_winner.iloc[0]})','',score_table(q).to_markdown(index=False,floatfmt='.4f'),'']
    return '\n'.join(lines)+'\n'


def charts(result,destination):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    colors={'Market':'black','GB':'#3366aa','ST':'#dd8844','MX':'#24845d','M10':'#a14d97','538':'#887133','RTWH':'#7c68b1'}
    paths=[]
    for year,g in result['metrics'].groupby('cycle'):
        fig,axes=plt.subplots(2,2,figsize=(12,8))
        groups=['All fixed states','Competitive on Sep 5','Long shot on Sep 5','Final margin <=5 pp (hindsight)']
        for ax,cohort in zip(axes.flat,groups):
            q=g[g.cohort.eq(cohort)]
            count=int(q.races.iloc[0]) if len(q) else 0
            ax.set_title(f'{cohort}\n{count} '+('race' if count==1 else 'races'))
            if q.empty:ax.text(.5,.5,'No eligible races',transform=ax.transAxes,ha='center')
            for model,r in q.groupby('model'):
                ax.plot(r.check_date,r.brier,'.--' if model=='Market' else '.-',label=model,color=colors[model],lw=2 if model=='Market' else 1.3)
            ax.set_xticks([pd.Timestamp(f'{year}-{d}',tz='UTC') for d in ['09-05','09-20','10-01','10-15','11-03']])
            ax.grid(alpha=.3);ax.set_ylabel('Brier score (lower is better)');ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'));ax.tick_params(axis='x',rotation=25)
        handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='upper center',ncol=6,bbox_to_anchor=(.5,.965))
        fig.suptitle(f'{year}: accuracy with fixed races across dates');fig.tight_layout(rect=(0,0,1,.92))
        path=destination/f'accuracy_evolution_{year}.png';fig.savefig(path,dpi=140);plt.close(fig);paths.append(path)
    return paths


def build(samples,out,destination):
    result=analyze(samples)
    for name,table in result.items():table.to_parquet(out/f'accuracy_evolution_{name}.parquet',index=False)
    return result,charts(result,destination)
