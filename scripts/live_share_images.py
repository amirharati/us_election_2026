"""Deterministic shareable PNGs from live tables. No AI, screenshots or table replacement."""
from pathlib import Path
import json
import textwrap

import matplotlib.pyplot as plt
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
    fig.text(.02,.015,'Source: local live forecast. D control requires 51 seats. Model alternatives are not independent forecasts.',fontsize=9,color=MUTED)
    fig.tight_layout(rect=[0,.04,1,.93]);return [finish(fig,directory,'share_chamber')]


def state_images(tables,models,directory,cutoff):
    paths=[]
    for key,title in [('margins','D/Independent minus R margin (pp)'),('probabilities','D/Independent win probability (%)')]:
        frame=tables[key][[m for m in models if m in tables[key].columns]].copy()
        frame=frame.loc[frame.mean(axis=1).sort_values().index]
        fig,ax=plt.subplots(figsize=(12,12));y=np.arange(len(frame))
        ax.hlines(y,frame.min(axis=1),frame.max(axis=1),color='#bcc7d2',lw=3,label='Range across displayed models')
        for m in frame:
            if m not in ['Bayesian','Four-model mixture']:ax.scatter(frame[m],y,color='#8e9ba8',s=12,zorder=2)
        for m,color,marker in [('Bayesian',BLUE,'o'),('Four-model mixture','#d58b25','D')]:
            if m in frame:ax.scatter(frame[m],y,color=color,marker=marker,s=36,label=model_label(m),zorder=3)
        ax.axvline(0 if key=='margins' else 50,color=MUTED,ls='--',lw=1)
        if key=='probabilities':ax.set_xlim(-2,102)
        style_axis(ax,frame.index);ax.set_xlabel(title);ax.legend(loc='upper center',bbox_to_anchor=(.5,1.10),ncol=3,fontsize=9)
        chart_caption(fig,f'2026 Senate · state forecasts and model spread\nCutoff {cutoff}',
            'Each dot is a model forecast. Connecting lines show model disagreement, not prediction intervals. Independents count with D/Independent.')
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
    paths+=state_images(tables,MODELS,out,cutoff)
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
