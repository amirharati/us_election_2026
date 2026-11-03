"""Descriptive model alignment to winner-market midpoints, not forecast accuracy."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from polymarket_debug_view import MODEL_CODES, small_html, CSS

METHOD = ('Winner contracts only; no margin, seat-total or control markets. Market probability is the Yes best-bid/ask midpoint, '
          'before fees; it is not an executable purchase price or ground truth. All mapped winner contracts are considered, not just profitable trades. '
          'Each state uses one shared contract: maximize model coverage, then reported liquidity, then narrower spread, then contract ID. '
          'This avoids counting Yes/No and alternative winner contracts as independent observations. '
          'The headline ranking uses only states covered by every selected model, with equal weight per state. '
          'Mean absolute gap is the average absolute probability difference in percentage points; lower means closer. '
          'The available-coverage table is descriptive and uses different state sets. State rankings show ties and exclude missing models. '
          'Conditional settlement estimates remain included and flagged; unavailable probabilities are not imputed. '
          'DDHQ includes market inputs, so closeness is not independent validation or evidence of better forecasting.')


def build(research, scanner):
    models=scanner['settings']['models'];status=research['status']
    audit=scanner['audit'];details=scanner['details']
    columns=['market_id','question','category','liquidity']
    catalog=pd.DataFrame(research['catalog']['markets'])[columns].copy()
    catalog['market_id']=catalog.market_id.astype(str)
    d=details[details.category.eq('Senate race winners') & details.side.eq('Yes')].copy()
    d['market_id']=d.market_id.astype(str)
    d=d.merge(audit[['market_id','model','state']].assign(market_id=lambda x:x.market_id.astype(str)),on=['market_id','model'],validate='one_to_one')
    exclusions=[]
    def reason(r):
        if r.model_blocker:return r.model_blocker
        if pd.isna(r.state):return 'No unique state mapping.'
        if pd.isna(r.market_midpoint) or not 0<=r.market_midpoint<=1:return 'Missing or invalid two-sided midpoint.'
        if pd.isna(r.spread) or not 0<=r.spread<=status['max_spread']:return 'Wide, crossed or missing spread.'
        if pd.isna(r.liquidity) or r.liquidity<status['min_liquidity']:return 'Liquidity below configured minimum.'
        if not r.accepting_orders or not r.order_book:return 'Contract is not accepting book orders.'
        if pd.isna(r.model_low) or pd.isna(r.model_high) or not np.isclose(r.model_low,r.model_high):return 'No single model probability.'
        if 'max_book_age_seconds' in status and (pd.isna(r.book_age_seconds) or not 0<=r.book_age_seconds<=status['max_book_age_seconds']):return 'Quote exceeds configured age limit.'
        if status['catalog_status'] not in ['checked online','recent catalog cache']:return 'Catalog is offline or stale.'
        if 'max_catalog_age_seconds' in status and not 0<=status['catalog_age_seconds']<=status['max_catalog_age_seconds']:return 'Catalog exceeds configured age limit.'
        return ''
    if not d.empty:
        d['exclusion']=d.apply(reason,axis=1)
        exclusions=d[d.exclusion.ne('')][['market_id','model','state','exclusion']].to_dict('records')
        d=d[d.exclusion.eq('')].copy()
    rows=[];anchors=[]
    for state,group in d.groupby('state',sort=True):
        candidates=group.groupby('market_id').agg(models=('model','nunique'),liquidity=('liquidity','first'),spread=('spread','first')).reset_index()
        chosen=candidates.sort_values(['models','liquidity','spread','market_id'],ascending=[False,False,True,True],kind='stable').iloc[0]
        part=group[group.market_id.eq(chosen.market_id)].copy()
        if part.model.duplicated().any():raise ValueError('Duplicate model/contract comparison')
        if part.market_midpoint.max()-part.market_midpoint.min()>1e-10:raise ValueError('Models compared to different quotes')
        first=part.iloc[0]
        anchors.append(dict(state=state,market_id=first.market_id,question=first.question,url=first.url,
                            market_probability=float(first.market_midpoint),models_available=len(part),common=len(part)==len(models)))
        for r in part.itertuples():
            rows.append(dict(state=state,market_id=r.market_id,question=r.question,model=r.model,
                             probability=r.model_low,market_probability=r.market_midpoint,
                             signed_gap_pp=100*(r.model_low-r.market_midpoint),abs_gap_pp=100*abs(r.model_low-r.market_midpoint),
                             settlement_proxy=bool(r.settlement_proxy),publisher_date=r.publisher_date,
                             source_note=r.mapping_reason,common=len(part)==len(models)))
    comparisons=pd.DataFrame(rows,columns=['state','market_id','question','model','probability','market_probability','signed_gap_pp','abs_gap_pp','settlement_proxy','publisher_date','source_note','common'])
    anchors=pd.DataFrame(anchors,columns=['state','market_id','question','url','market_probability','models_available','common'])
    overall=[];available=[];states=[]
    for name in models:
        for shared,target in [(True,overall),(False,available)]:
            part=comparisons[comparisons.model.eq(name)]
            if shared:part=part[part.common.eq(True)]
            target.append(dict(model=name,states=len(part),mean_abs_gap_pp=part.abs_gap_pp.mean(),mean_signed_gap_pp=part.signed_gap_pp.mean(),conditional=int(part.settlement_proxy.sum())))
    for state,part in comparisons.groupby('state',sort=True):
        closest=part.abs_gap_pp.min();farthest=part.abs_gap_pp.max()
        codes=lambda mask:', '.join(MODEL_CODES.get(r.model,r.model)+('*' if r.settlement_proxy else '') for r in part.loc[mask].itertuples())
        states.append(dict(state=state,models=len(part),closest=codes(np.isclose(part.abs_gap_pp,closest)) if len(part)>1 else 'Insufficient coverage',
                           closest_gap_pp=closest,farthest=codes(np.isclose(part.abs_gap_pp,farthest)) if len(part)>1 else 'Insufficient coverage',farthest_gap_pp=farthest,
                           common=bool(part.common.iloc[0])))
    for r in audit[audit.market_id.astype(str).isin(catalog[catalog.category.eq('Senate race winners')].market_id)&audit.model_low.isna()].itertuples():
        exclusions.append(dict(market_id=str(r.market_id),model=r.model,state=r.state,exclusion=r.reason))
    universe=set(audit.state.dropna())|{state for source in scanner.get('external',{}).values() for state in source.get('races',{})}
    missing_states=sorted(universe-set(anchors.state))
    for state in missing_states:
        if state not in set(audit.state.dropna()):
            exclusions.append(dict(market_id=None,model=None,state=state,exclusion='No mapped active winner contract in the downloaded catalog.'))
    return dict(overall=pd.DataFrame(overall).sort_values('mean_abs_gap_pp',na_position='last',kind='stable'),
                available=pd.DataFrame(available).sort_values('mean_abs_gap_pp',na_position='last',kind='stable'),
                states=pd.DataFrame(states,columns=['state','models','closest','closest_gap_pp','farthest','farthest_gap_pp','common']),
                comparisons=comparisons,anchors=anchors,exclusions=pd.DataFrame(exclusions,columns=['market_id','model','state','exclusion']),
                settings=dict(models=models,common_states=int(anchors.common.sum()),states_with_quotes=len(anchors),market_retrieved_at=status['retrieved_at'],
                              forecast_cutoff=status['forecast_cutoff'],unrepresented_states=missing_states,max_spread=status['max_spread'],min_liquidity=status['min_liquidity']),method=METHOD)


def overall_table(frame):
    return pd.DataFrame({'Model':[MODEL_CODES.get(m,m) for m in frame.model],'States':frame.states,
                         'Mean gap (pp)':frame.mean_abs_gap_pp,'Signed gap (pp)':frame.mean_signed_gap_pp,'Conditional':frame.conditional})


def state_table(result):
    s=result['states']
    return pd.DataFrame({'State':[r.state+(' †' if not r.common else '') for r in s.itertuples()],
                         'Closest':s.closest,'Gap (pp)':s.closest_gap_pp,'Farthest':s.farthest,'Far gap (pp)':s.farthest_gap_pp})


def detail_table(result,state):
    d=result['comparisons'];d=d[d.state.eq(state)].copy()
    return pd.DataFrame({'Model':[MODEL_CODES.get(r.model,r.model)+('*' if r.settlement_proxy else '') for r in d.itertuples()],
                         'Model (%)':100*d.probability,'Market (%)':100*d.market_probability,'Gap (pp)':d.signed_gap_pp})


def figure(result):
    import matplotlib.pyplot as plt
    import matplotlib.colors as colors
    d=result['comparisons'];models=result['settings']['models']
    if d.empty:return None
    mat=d.pivot(index='state',columns='model',values='abs_gap_pp').reindex(columns=models)
    fig,(left,right)=plt.subplots(1,2,figsize=(12,max(5,len(mat)*.28)),gridspec_kw={'width_ratios':[1,1.8]})
    common=result['overall'].dropna(subset=['mean_abs_gap_pp']).iloc[::-1]
    left.barh([MODEL_CODES.get(m,m) for m in common.model],common.mean_abs_gap_pp,color='#4278a8')
    left.set_xlabel('Mean absolute gap (percentage points)');left.set_title(f"Overall: same {result['settings']['common_states']} states")
    left.grid(axis='x',alpha=.25);left.set_axisbelow(True)
    cmap=plt.get_cmap('YlOrRd').copy();cmap.set_bad('#dddddd')
    im=right.imshow(mat.to_numpy(float),aspect='auto',cmap=cmap,vmin=0,vmax=max(1,float(mat.max().max())))
    right.set_xticks(range(len(models)),[MODEL_CODES.get(m,m) for m in models]);right.set_yticks(range(len(mat)),mat.index)
    right.set_xticks(np.arange(-.5,len(models),1),minor=True);right.set_yticks(np.arange(-.5,len(mat),1),minor=True)
    right.grid(which='minor',color='white',linewidth=.8);right.tick_params(which='minor',bottom=False,left=False)
    for i,state in enumerate(mat.index):
        for j,model in enumerate(models):
            value=mat.loc[state,model]
            if pd.notna(value):right.text(j,i,f'{value:.1f}',ha='center',va='center',fontsize=8,color='white' if value>im.norm.vmax*.6 else 'black')
    right.set_title('State gaps; lighter = closer; gray = missing')
    fig.colorbar(im,ax=right,label='Absolute gap (pp)',fraction=.035,pad=.03)
    fig.suptitle('Model distance from Polymarket winner probabilities',fontsize=13)
    fig.text(.02,.012,'Same contract within each state. Conditional estimates included. DDHQ uses market inputs. Closeness is not accuracy.',fontsize=9)
    fig.text(.02,.032,'Market snapshot: '+result['settings']['market_retrieved_at']+' | Local forecast cutoff: '+result['settings']['forecast_cutoff'],fontsize=9)
    fig.tight_layout(rect=(0,.06,1,.96));return fig


def display(result):
    from IPython.display import display as show,HTML
    print(METHOD)
    if result['settings']['unrepresented_states']:print('No eligible comparison in this snapshot: '+', '.join(result['settings']['unrepresented_states'])+'. See the saved exclusions.')
    show(HTML(CSS+'<div class="scan"><h3>Overall: common states only</h3>'+small_html(overall_table(result['overall']))+
              '<h3>Available coverage (different state sets)</h3>'+small_html(overall_table(result['available']))+
              '<h3>Closest and farthest by state</h3><p>† Some models are missing. * marks a conditional estimate. Missing models are excluded from that state ranking. Gaps are percentage points.</p>'+small_html(state_table(result))+'</div>'))


def publish(result,directory):
    import matplotlib.pyplot as plt
    directory=Path(directory)
    for key in ['overall','available','states','comparisons','anchors','exclusions']:result[key].to_parquet(directory/f'alignment_{key}.parquet',index=False)
    (directory/'alignment_settings.json').write_text(json.dumps(result['settings'],indent=2)+'\n')
    f=figure(result)
    if f is not None:f.savefig(directory/'model_market_alignment.png',dpi=150,bbox_inches='tight');plt.close(f)
    lines=['# Model alignment to Polymarket winner probabilities','',METHOD,'',
           'Snapshot: '+result['settings']['market_retrieved_at']+'. Our forecast cutoff: '+result['settings']['forecast_cutoff']+'.','',
           '## Overall: identical state coverage','',overall_table(result['overall']).to_markdown(index=False,floatfmt='.2f'),'',
           '## All available coverage (different state sets)','',overall_table(result['available']).to_markdown(index=False,floatfmt='.2f'),'',
           '## Per-state ranking','', '† Some models are missing; they are excluded from that state ranking. * marks a conditional estimate.','',state_table(result).to_markdown(index=False,floatfmt='.2f'),'']
    if result['settings']['unrepresented_states']:lines+=['No eligible comparison in this snapshot: '+', '.join(result['settings']['unrepresented_states'])+'. See the saved exclusions.','']
    if f is not None:lines+=['![Overall and state probability distances](model_market_alignment.png)','']
    for anchor in result['anchors'].itertuples():
        lines += ['## '+anchor.state,'',f'[{anchor.question}]({anchor.url}) — contract {anchor.market_id}.','',detail_table(result,anchor.state).to_markdown(index=False,floatfmt='.2f'),'',
                  '* marks a conditional settlement estimate. Model minus market is signed; closer means a smaller absolute gap.','']
    lines+=['[All comparisons](alignment_comparisons.parquet) · [Selected state contracts](alignment_anchors.parquet) · [Exclusions](alignment_exclusions.parquet) · [Settings](alignment_settings.json)','']
    (directory/'model_market_alignment.md').write_text('\n'.join(lines))
    return ['## Which models are closest to Polymarket?','',METHOD,'',overall_table(result['overall']).to_markdown(index=False,floatfmt='.2f'),'',
            '[Per-state rankings, probabilities and coverage](model_market_alignment.md) · [All comparisons](alignment_comparisons.parquet) · [State contracts](alignment_anchors.parquet) · [Exclusions](alignment_exclusions.parquet) · [Settings](alignment_settings.json) · [Common coverage](alignment_overall.parquet) · [Available coverage](alignment_available.parquet) · [State summaries](alignment_states.parquet)','',
            *(['![Model distance from market probabilities](model_market_alignment.png)',''] if f is not None else [])]
