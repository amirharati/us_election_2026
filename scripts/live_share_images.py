"""Deterministic shareable PNGs from live tables. No AI, screenshots or table replacement."""
from pathlib import Path
import json
import textwrap

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

from model_labels import model_label

MODELS=['Bayesian','Matched Student-t (df5)','Older Gaussian','Student-t research helper',
        'Non-Bayesian corrected','Four-model mixture','Mixture + polling 20%']
INK='#172b4d';MUTED='#526477';BLUE='#2367a3';BG='#f4f7fb'


def status_label(value):
    return {'checked_online':'checked online','fresh_check_cache':'recent check reused',
            'offline_cache':'saved offline snapshot','stale_cache_after_failure':'STALE after source failure',
            'unavailable':'unavailable','unavailable_offline':'unavailable offline'}.get(value,value.replace('_',' '))


def probability_label(value):
    return '<1' if value<1 else '>99' if value>99 else f'{value:.0f}'


def finish(fig, directory, name):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    path=directory/(name+'.png')
    fig.savefig(path,dpi=160,facecolor='white',bbox_inches='tight',pad_inches=.2)
    plt.close(fig)
    return path


def style_axis(ax, labels):
    ax.set(yticks=np.arange(len(labels)), yticklabels=labels, ylim=(len(labels)-.4,-.6))
    ax.grid(axis='x',alpha=.15)
    ax.grid(axis='y',color='#b7c3cf',linewidth=.65,alpha=.65)
    for row in range(0,len(labels),2):
        ax.axhspan(row-.5,row+.5,color=BG,zorder=-2)
    ax.set_axisbelow(True)
    ax.spines[['top','right']].set_visible(False)
    if not len(labels):ax.text(.5,.5,'No races meet these selection rules.',transform=ax.transAxes,ha='center')


def chart_caption(fig,title,footer):
    fig.suptitle(title,fontsize=16,weight='bold',color=INK)
    fig.text(.02,.015,'\n'.join(textwrap.wrap(footer,140)),fontsize=9,color=MUTED)
    fig.tight_layout(rect=[0,.09,1,.89])


def chamber_images(seats,directory,cutoff):
    q=seats.set_index('model').reindex([m for m in MODELS if m in seats.model.values])
    fig,axes=plt.subplots(1,2,figsize=(13,5.2),gridspec_kw={'width_ratios':[1.25,1]})
    y=np.arange(len(q));labels=[model_label(m) for m in q.index]
    axes[0].barh(y,100*q.p_D_control,color=[BLUE if v>=.5 else '#b95550' for v in q.p_D_control],height=.6)
    for i,v in enumerate(100*q.p_D_control):axes[0].text(min(v+1.3,96),i,f'{v:.1f}%',va='center',fontsize=10)
    axes[0].set(yticks=y,yticklabels=labels,xlim=(0,103),xlabel='D / Independent control probability (%)')
    axes[0].axvline(50,color=MUTED,ls='--',lw=1)
    axes[1].hlines(y,q.D_lo70,q.D_hi70,color=BLUE,lw=4,alpha=.6)
    axes[1].scatter(q.expected_D,y,color=INK,zorder=3)
    for i,v in enumerate(q.expected_D):axes[1].annotate(f'{v:.1f}',(v,i),xytext=(0,-16),textcoords='offset points',ha='center',fontsize=9)
    axes[1].set(yticks=y,yticklabels=[],xlabel='Expected D / Independent seats · central 70% range')
    axes[1].axvline(51,color=MUTED,ls='--',lw=1)
    for ax in axes:ax.set_ylim(len(q),-.6);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True);ax.spines[['top','right']].set_visible(False)
    fig.suptitle(f'2026 Senate · chamber forecast · cutoff {cutoff}',fontsize=17,weight='bold',color=INK)
    fig.text(.02,.015,'All models use polls when available. A baseline shift changes the mean, not the uncertainty distribution. D control requires 51 seats.',fontsize=9,color=MUTED)
    fig.tight_layout(rect=[0,.04,1,.93]);return [finish(fig,directory,'share_chamber')]


def state_chart_data(tables):
    """Align actual mixture quantiles with its four component means by state."""
    from model_portfolio import configuration
    config=configuration();names=list(config['component_weights'])
    predictions=tables['predictions']
    mixture=predictions[predictions.model.eq(config['mixture_label'])].set_index('State')
    if mixture.empty:return mixture
    q=mixture.sort_values('margin_pp').copy()
    means=tables['margins'].reindex(q.index)[names].to_numpy(dtype=float)
    if not np.isfinite(means).all():raise ValueError('Missing four-model component margins')
    pairs=np.triu_indices(len(names),1)
    q['disagreement_pp']=np.abs(means[:,:,None]-means[:,None,:])[:,pairs[0],pairs[1]].mean(axis=1)
    return q


COVERAGE_COLORS={'adequate':'#16857b','thin':'#c28b18','none':'#7a8592'}


def interval_coverage(q,coverage):
    """Use unique admitted samples from the forecast's own cutoff and audit."""
    rows=coverage['all_contests'].query("model == 'Four-model mixture'")
    if rows.target_id.duplicated().any():raise ValueError('Duplicate polling coverage for a race')
    rows=rows.set_index('target_id').reindex(q.target_id)
    if rows[['recent_samples','recent_firms']].isna().any().any():
        raise ValueError('Missing polling coverage; missing is not zero polls')
    settings=coverage['parameters']
    adequate=(rows.recent_samples.ge(settings['min_samples']) & rows.recent_firms.ge(settings['min_firms']))
    groups=np.where(rows.recent_samples.eq(0),'none',np.where(adequate,'adequate','thin'))
    return [COVERAGE_COLORS[g] for g in groups]


def state_images(tables,models,directory,cutoff,coverage=None):
    q=state_chart_data(tables)
    if q.empty:return []  # The four-model mixture requires all four fitted components.
    paths=[];y=np.arange(len(q))
    if coverage is not None and str(coverage['as_of'])!=str(cutoff):
        raise ValueError('Polling coverage and chart cutoff differ')
    colors=interval_coverage(q,coverage) if coverage is not None else BLUE
    has68=all(c in q and q[c].notna().all() for c in ['lo68_pp','hi68_pp'])
    for key in ['margins','probabilities']:
        fig,axes=plt.subplots(1,2,figsize=(14,13),gridspec_kw={'width_ratios':[3,1]},sharey=True)
        ax,disagreement=axes
        if key=='margins':
            ax.hlines(y,q.lo95_pp,q.hi95_pp,color=colors,lw=2,label='Central 95% predictive interval',zorder=2)
            if has68:ax.hlines(y,q.lo68_pp,q.hi68_pp,color=colors,lw=6,label='Central 68% predictive interval',zorder=3)
            ax.scatter(q.margin_pp,y,color=INK,s=30,label='Mixture mean',zorder=4)
            ax.axvline(0,color=MUTED,ls='--',lw=1)
            ax.set_xlabel('D/Independent minus R vote margin (percentage points)')
            ax.set_title('Four-model mixture: possible election outcomes',fontsize=12,pad=90)
            handles=[Line2D([],[],color=INK,lw=2,label='Central 95% interval')]
            if has68:handles.append(Line2D([],[],color=INK,lw=6,label='Central 68% interval'))
            handles.append(Line2D([],[],color=INK,marker='o',ls='',label='Mixture mean'))
            if coverage is not None:
                settings=coverage['parameters']
                labels={'adequate':f"Adequate: ≥{settings['min_samples']} samples and ≥{settings['min_firms']} firms",
                        'thin':'Few samples or limited firm diversity','none':'No recent polls'}
                handles += [Line2D([],[],color=color,lw=5,label=labels[group]) for group,color in COVERAGE_COLORS.items()]
                legend_title=f"Polling coverage in the previous {settings['recent_days']} days"
            else:legend_title='Polling coverage unavailable'
            ax.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,1.015),fontsize=9,ncol=2,title=legend_title,title_fontsize=10)
            note='Color shows polling coverage, not confidence. Interval width reflects the full mixture, including within-model uncertainty and model differences.'
            if not has68:note+=' This older saved run has no 68% quantiles; rerun the live forecast to add them.'
        else:
            ax.scatter(100*q.p_dem,y,color=BLUE,s=35,zorder=3)
            ax.axvline(50,color=MUTED,ls='--',lw=1)
            ax.set(xlim=(-2,102),xlabel='D/Independent win probability (%)')
            ax.set_title('Four-model mixture: chance of winning',fontsize=12,pad=20)
            note='Dots show mixture win probabilities. Vote-margin predictive intervals belong in the companion margin chart.'
        disagreement.barh(y,q.disagreement_pp,height=.5,color='#8757a3',zorder=2)
        disagreement.set(xlim=(0,None),xlabel='Average pairwise margin gap (pp)')
        disagreement.set_title('Component disagreement',fontsize=12,pad=20)
        for axis in axes:style_axis(axis,q.index)
        disagreement.tick_params(axis='y',labelleft=False)
        title='predictive intervals' if key=='margins' else 'win probabilities'
        chart_caption(fig,f'2026 Senate · four-model mixture {title}\nCutoff {cutoff}',
            note+' Right panel averages the six absolute margin gaps among the four components; it is context, not extra uncertainty to add.')
        paths.append(finish(fig,directory,'share_state_'+key))
    return paths


def uncertainty_images(frame,directory,cutoff):
    q=frame.sort_values('width95_pp',ascending=False);y=np.arange(len(q))
    fig,ax=plt.subplots(figsize=(12,max(4.8,.45*len(q)+2)))
    ax.hlines(y,q.lo95_pp,q.hi95_pp,color=BLUE,lw=4,alpha=.5)
    ax.scatter(q.prediction_pp,y,color=INK,zorder=3)
    ax.axvline(0,color=MUTED,ls='--');ax.set_xlabel('D/Independent minus R margin (pp) · dot: prediction · line: 95% interval')
    style_axis(ax,[f'{r.contest} · {r.recent_samples:g} polls / {r.recent_firms:g} firms' for r in q.itertuples()])
    chart_caption(fig,f'Wide uncertainty despite recent polling\nGaussian Bayesian · cutoff {cutoff}',
        'R leads to the left of zero; D/Independent leads to the right. Intervals describe predictive uncertainty. Wide intervals do not imply a likely upset.')
    return [finish(fig,directory,'share_uncertainty')]


def watch_images(frame,key,directory,cutoff):
    q=frame.sort_values('other_winner_pct',ascending=False);y=np.arange(len(q))
    fig,axes=plt.subplots(1,3,figsize=(15,max(5,.5*len(q)+2)),gridspec_kw={'width_ratios':[1.5,1,1.25]})
    axes[0].hlines(y,q.lo95_pp,q.hi95_pp,color=BLUE,lw=4,alpha=.4)
    axes[0].scatter(q.margin_pp,y,color=INK,zorder=3);axes[0].axvline(0,color=MUTED,ls='--')
    axes[0].set_xlabel('D/Independent minus R margin (pp)');axes[0].set_title('Prediction and 95% interval',fontsize=11)
    axes[1].barh(y,q.other_winner_pct,color='#bd7c32',height=.5)
    axes[1].set(xlim=(0,50),xlabel='Probability (%)',title='Chance the other side wins')
    axes[2].scatter(q.disagreement_pp,y,color=BLUE,label='Model disagreement',s=45)
    axes[2].scatter(q.predictive_sd_pp,y,color='#8757a3',marker='D',label='Predictive SD',s=35)
    axes[2].set(xlim=(0,None),xlabel='Percentage points',title='Two sources of uncertainty')
    axes[2].legend(loc='upper center',bbox_to_anchor=(.5,-.15),fontsize=9)
    for i,ax in enumerate(axes):style_axis(ax,q.contest if i==0 else ['']*len(q))
    group='adequately polled' if key=='polled' else 'thinly polled / no recent polls'
    chart_caption(fig,f'Surprise watchlist · {group}\nCutoff {cutoff}',
        'Gaussian Bayesian supplies intervals and other-winner probabilities. Disagreement is the average pairwise model gap. Selection reasons and historical errors remain in the table.')
    return [finish(fig,directory,'share_watch_'+key)]


def published_images(comparison,directory,cutoff):
    overall=comparison['overall'];q=overall[overall['D control %'].notna()]
    fig,ax=plt.subplots(figsize=(12,4.5));y=np.arange(len(q))
    labels=[f'{r["Forecast"]}\n{r["Date"]}' for _,r in q.iterrows()]
    ax.barh(y,q['D control %'],height=.55,color=[BLUE if x.startswith(('Gaussian','Four-model')) else '#64848a' for x in q.Forecast])
    for i,v in enumerate(q['D control %']):ax.text(v+1,i,f'{v:.1f}%',va='center',fontsize=12)
    ax.set(yticks=y,yticklabels=labels,xlim=(0,100),xlabel='D / Independent Senate-control probability (%)')
    ax.invert_yaxis();ax.axvline(50,color=MUTED,ls='--',lw=1);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True);ax.spines[['top','right']].set_visible(False)
    fig.suptitle(f'Senate control · our models and published forecasts\nOur cutoff: {cutoff}',fontsize=17,weight='bold',color=INK)
    statuses='; '.join(f'{r.Source}: {status_label(r.Status)}' for r in comparison['status'].itertuples())
    footer='Silver is a rounded public Deluxe topline; dates can differ. Inside Elections publishes ratings, not a control probability. '+statuses
    fig.text(.02,.015,'\n'.join(textwrap.wrap(footer,135)),fontsize=8.5,color=MUTED)
    fig.tight_layout(rect=[0,.16,1,.87]);paths=[finish(fig,directory,'share_published_chamber')]
    for (source,model),group in comparison['mismatches'].groupby(['Source','Model'],sort=False):
        slug='_'.join((source+' '+model).lower().replace('-',' ').split())
        q=group.sort_values('Our D/Independent win %');y=np.arange(len(q))
        probability=q['Published D/Independent win %'].notna().any()
        fig,ax=plt.subplots(figsize=(12,max(4.8,.43*len(q)+2.5)))
        ours=q['Our D/Independent win %']
        if probability:
            theirs=q['Published D/Independent win %']
            ax.hlines(y,np.minimum(ours,theirs),np.maximum(ours,theirs),color='#bcc7d2',lw=3)
            ax.scatter(theirs,y,color='#bd7c32',marker='D',s=50,label=source,zorder=3)
            labels=q.Contest
        else:
            ax.hlines(y,50,ours,color='#bcc7d2',lw=3)
            labels=[f'{r["Contest"]} · {r["Published rating"]}' for _,r in q.iterrows()]
        ax.scatter(ours,y,color=BLUE,s=55,label=model,zorder=3)
        ax.set(xlim=(-2,102),xlabel='D / Independent win probability (%)')
        ax.axvline(50,color=MUTED,ls='--',lw=1);style_axis(ax,labels)
        ax.legend(loc='upper center',bbox_to_anchor=(.5,1.17),ncol=2,fontsize=9)
        status=comparison['status'].loc[comparison['status'].Source.eq(source),'Status'].iloc[0]
        note=('Connecting lines show the probability gap.' if probability else
              'Publisher ratings appear beside race names. Ratings are qualitative; only our model supplies numeric probabilities.')
        chart_caption(fig,f'{source} vs {model} · selected disagreements\nOur cutoff {cutoff} · publisher {group.Published.iloc[0]}',
            note+' Independents count with D/Independent. Source: '+status_label(status)+'.')
        paths.append(finish(fig,directory,'share_compare_'+slug))
    return paths


def build_share_images(out,run,watchlist,surprise,published):
    import election_lab as lab
    meta=json.loads((run/'run.json').read_text());cutoff=meta['as_of'];tables=lab.display_tables(run)
    paths=chamber_images(tables['seats'],out,cutoff)
    paths+=state_images(tables,MODELS,out,cutoff,coverage=watchlist)
    paths+=uncertainty_images(watchlist['broad'].query("model == 'Bayesian'"),out,cutoff)
    for key in ['polled','thin']:paths+=watch_images(surprise[key],key,out,cutoff)
    paths+=published_images(published,out,cutoff)
    manifest=dict(cutoff=cutoff,live_manifest_sha256=lab.sha(run/'manifest.json'),
                  files=[dict(name=p.name,sha256=lab.sha(p)) for p in paths])
    lab.write_json(out/'share_images.json',manifest)
    return paths


def display_images(paths):
    from IPython.display import Image, display
    for path in paths:display(Image(filename=str(path),width=1100))
