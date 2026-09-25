"""Inspect individual model/contract predictions without a model consensus score."""
from html import escape
import numpy as np
import pandas as pd
from model_labels import model_label

GUIDE = ('A market is included when at least one model has a positive expected profit after costs. '
         'Both Yes and No sides and every saved model are then shown, including disagreements and unavailable mappings. '
         'Markets are ordered by question, not by model votes. Green means profit survives the probability haircut. '
         'Red means expected profit is below zero. Amber means a weaker or unresolved result. '
         'Gray means pricing or quote requirements are not met. Text labels accompany the colors. '
         'Expected profit is not the realized payoff: a binary position either gains the stated win profit or loses the stated budget. '
         'All shares in one contract settle together; buying more shares does not diversify its outcome risk. '
         'Predictive margin intervals describe election outcomes, not confidence in model accuracy. '
         'The mixture appears as one named model. No new ensemble or consensus score is formed.')


def build(scanner):
    d=scanner['details'];s=scanner['summary'];a=scanner['audit'];shares=scanner['settings']['shares']
    if d.empty or s.empty:return pd.DataFrame()
    eligible={(str(r.market_id),r.side):r.blockers for r in s.itertuples()}
    selected=set(d.loc[d.apply(lambda r:not eligible.get((str(r.market_id),r.side),'Unavailable') and not r.get('model_blocker','') and pd.notna(r.edge_low_pp) and r.edge_low_pp>scanner['settings']['min_edge_pp'],axis=1),'market_id'])
    records=[]
    for market in sorted(selected,key=lambda mid:(str(s[s.market_id.eq(mid)].iloc[0].question),str(mid))):
        header=s[s.market_id.eq(market)].iloc[0]
        for side in ['Yes','No']:
            for model in scanner['settings']['models']:
                rows=d[d.market_id.eq(market)&d.side.eq(side)&d.model.eq(model)]
                audit=a[a.market_id.eq(market)&a.model.eq(model)]
                base=dict(market_id=market,question=header.question,url=header.url,side=side,model=model,model_label=model_label(model),shares=shares,friction_cents=scanner['settings']['friction_cents'],haircut_pp=scanner['settings']['probability_haircut_pp'])
                if rows.empty:
                    records.append({**base,'status':'Unavailable','reason':audit.iloc[0].reason if len(audit) else 'No saved comparison.',
                                    'publisher_date':audit.iloc[0].get('publisher_date') if len(audit) else None});continue
                r=rows.iloc[0];blocked=eligible.get((str(market),side),'Missing quote eligibility.') or r.get('model_blocker','')
                status=('Unavailable' if blocked or pd.isna(r.effective_cost) else 'Positive after stress' if r.stressed_edge_pp>scanner['settings']['min_edge_pp']
                        else 'Negative expected profit' if r.edge_high_pp<0 else 'Positive before stress only' if r.edge_low_pp>0 else 'Bounds overlap cost')
                cost=r.effective_cost
                records.append({**base,'status':status,'reason':blocked or r.mapping_reason,
                    'probability_low':r.model_low,'probability_high':r.model_high,'loss_probability_low':1-r.model_high,'loss_probability_high':1-r.model_low,
                    'entry_cents':100*r.entry_price,'cost':shares*cost,
                    'expected_profit_low':shares*r.edge_low_pp/100,'expected_profit_high':shares*r.edge_high_pp/100,
                    'stressed_profit':shares*r.stressed_edge_pp/100,'win_profit':shares*(1-cost),'loss_amount':shares*cost,
                    'reward_to_risk':(1-cost)/cost if pd.notna(cost) and cost>0 else None,
                    'return_low_pct':r.edge_low_pp/cost if pd.notna(cost) and cost>0 else None,'return_high_pct':r.edge_high_pp/cost if pd.notna(cost) and cost>0 else None,
                    'forecast_mean_margin_pp':r.get('forecast_mean_margin_pp'),'margin_lo95_pp':r.margin_lo95_pp,'margin_hi95_pp':r.margin_hi95_pp,
                    'settlement_proxy':bool(r.get('settlement_proxy',False)),'probability_kind':r.probability_kind,'publisher_date':r.get('publisher_date'),'publisher_url':r.get('publisher_url'),'market_weight':r.get('market_weight')})
    return pd.DataFrame(records)


def span(lo,hi,scale=1):
    if pd.isna(lo) or pd.isna(hi):return 'Unavailable'
    lo*=scale;hi*=scale
    return f'{lo:.2f}' if abs(lo-hi)<1e-9 else f'{lo:.2f} to {hi:.2f}'


def table(group):
    rows=[]
    for r in group.to_dict('records'):
        get=lambda k:r.get(k,np.nan)
        rows.append({'Model':r['model_label'],'Assessment':r['status'],
            'Probability of selected side (%)':span(get('probability_low'),get('probability_high'),100),
            'Entry (¢/share)':get('entry_cents'),'Total cost ($)':get('cost'),
            'Expected profit ($)':span(get('expected_profit_low'),get('expected_profit_high')),
            'Stressed profit ($)':get('stressed_profit'),'Expected return (%)':span(get('return_low_pct'),get('return_high_pct')),
            'Profit if win ($)':get('win_profit'),'Loss if lose ($)':get('loss_amount'),
            'Win profit / loss':get('reward_to_risk'),'Probability of loss (%)':span(get('loss_probability_low'),get('loss_probability_high'),100),
            'Mean D/Independent minus R margin (pp)':get('forecast_mean_margin_pp'),
            '95% predictive margin interval (pp)':span(get('margin_lo95_pp'),get('margin_hi95_pp')),
            'Probability method':get('probability_kind'),'Explanation':r['reason']})
    return pd.DataFrame(rows)


MODEL_CODES={'Race to the WH':'RTWH','DDHQ':'DDHQ','Bayesian':'GB','Matched Student-t (df5)':'ST','Older Gaussian':'OG','Student-t research helper':'OT','Non-Bayesian corrected':'EB','Four-model mixture':'MX',
             **{f'Corrected {x}%':f'G{x}' for x in [10,20,40,50]},**{f'Mixture + polling {x}%':f'M{x}' for x in [5,10,20,30,40,50]}}
STATUS_CODES={'Positive after stress':'GO','Positive before stress only':'WEAK','Bounds overlap cost':'UNC','Negative expected profit':'NEG','Unavailable':'N/A'}
COLORS={'GO':'#e0f2e7','NEG':'#fbe3e3','N/A':'#eeeeee','WEAK':'#fff2cc','UNC':'#fff2cc'}
CSS='<style>.scan{max-width:760px;width:100%;box-sizing:border-box;color:#18212a;background:white;padding:10px;font:14px system-ui;overflow-wrap:anywhere}.scan table{width:100%;table-layout:fixed;border-collapse:collapse}.scan th,.scan td{padding:6px;border-bottom:1px solid #ddd;text-align:right;overflow-wrap:anywhere}.scan th:first-child,.scan td:first-child{text-align:left}.scan p{margin:7px 0}.scan h3{font-size:15px;margin:8px 0}.scan summary{cursor:pointer;margin:8px 0}</style>'


def compact_table(group):
    return pd.DataFrame([{'Model':MODEL_CODES.get(r.model,r.model_label),'Status':STATUS_CODES[r.status]+('*' if getattr(r,'settlement_proxy',False) is True else ''),
                         'P (%)':span(getattr(r,'probability_low',np.nan),getattr(r,'probability_high',np.nan),100).replace(' to ','–').replace('Unavailable','—'),
                         'EV ($)':span(getattr(r,'expected_profit_low',np.nan),getattr(r,'expected_profit_high',np.nan)).replace(' to ','–').replace('Unavailable','—'),
                         'Stress ($)':getattr(r,'stressed_profit',np.nan)} for r in group.itertuples()])


def small_html(t,colored=False):
    parts=['<table><thead><tr>'+''.join('<th>'+escape(str(c))+'</th>' for c in t.columns)+'</tr></thead><tbody>']
    for r in t.to_dict('records'):
        parts.append('<tr style="background:'+COLORS.get(str(r.get('Status','')).rstrip('*'),'white')+'">')
        for v in r.values():
            text='—' if pd.isna(v) else f'{v:.2f}' if isinstance(v,(float,np.floating)) else str(v)
            parts.append('<td>'+escape(text)+'</td>')
        parts.append('</tr>')
    return ''.join(parts)+'</tbody></table>'


def grouped_table(group):
    """Five columns, with the model and selected side explicitly paired."""
    g=group.copy()
    model_order={m:i for i,m in enumerate(g.model.drop_duplicates())}
    g['_order']=g.model.map(model_order);g['_side']=g.side.map({'Yes':0,'No':1})
    g=g.sort_values(['_order','_side'])
    t=compact_table(g)
    t['Model']=[MODEL_CODES.get(r.model,r.model_label)+' / '+('Y' if r.side=='Yes' else 'N') for r in g.itertuples()]
    return t.rename(columns={'Model':'Model / side'})


def legend_tables(frame):
    models=frame[['model','model_label']].drop_duplicates()
    return pd.DataFrame({'Code':[MODEL_CODES.get(x,x) for x in models.model],'Model name':models.model_label.to_list()})


def payoff_table(group):
    rows=[]
    for side,g in group.groupby('side',sort=False):
        q=g[g.cost.notna()] if 'cost' in g else g.iloc[:0]
        if q.empty:rows.append({'Side':side,'Entry (¢)':'—','Budget ($)':'—','Win / lose ($)':'Unavailable','Reward/loss':'—'});continue
        r=q.iloc[0]
        rows.append({'Side':side,'Entry (¢)':f'{r.entry_cents:.2f}','Budget ($)':f'{r.cost:.2f}',
                     'Win / lose ($)':f'+{r.win_profit:.2f} / −{r.loss_amount:.2f}','Reward/loss':f'{r.reward_to_risk:.2f}×'})
    return pd.DataFrame(rows)


COMPACT_GUIDE=('Y = buy Yes; N = buy No. P = model probability that the selected side pays $1 under the contract condition; it is not confidence that the model is correct. EV = base expected net profit after purchase depth and estimated fees. Budget and win/loss payoffs use those base costs. '
               'Stress adds the extra friction scenario and applies the probability haircut to the model probability. GO (green) survives stress; WEAK (amber) is positive before stress only; '
               'UNC (amber) is unresolved; NEG (red) is negative in expectation; N/A (gray) is unavailable. '
               'A status marked * uses a conditional settlement proxy: its P, EV and stress depend on the stated runoff, ranked-choice or candidate assumptions. Color follows the assessment even with a star; the star separately flags the settlement assumption. Local P comes from the full predictive distribution. External P is a published point estimate or seat-histogram probability; equal endpoints are not a confidence interval. Simulation estimates have sampling error. All model rows are independent comparisons; there is no combined score.')


def scenario_note(frame):
    if frame.empty:return ''
    r=frame.iloc[0]
    return f'Base: quoted ask depth plus estimated fees. Stress only: add {r.friction_cents:g}¢ per share and reduce the selected-side probability by {r.haircut_pp:g} percentage points (minimum zero).'


def external_notes(group):
    notes=[]
    local=group[~group.model.isin(['Race to the WH','DDHQ'])]
    for reason,g in local.groupby('reason',sort=False):
        if g.status.eq('Unavailable').any() or ('settlement_proxy' in g and g.settlement_proxy.eq(True).any()):
            codes=', '.join(MODEL_CODES.get(m,m) for m in g.model.drop_duplicates())
            notes.append(codes+': '+reason)
    for model,g in group.groupby('model',sort=False):
        if model not in ['Race to the WH','DDHQ']:continue
        r=g.iloc[0];date=r.get('publisher_date')
        prefix=MODEL_CODES[model]+(' ('+str(date)+')' if pd.notna(date) else '')
        notes.append(prefix+': '+r.reason)
    return notes


def html(frame):
    if frame.empty:return CSS+'<div class="scan">No markets pass the initial screen.</div>'
    parts=[CSS,'<div class="scan"><h3>Model codes</h3>',small_html(legend_tables(frame)),'<p>'+escape(COMPACT_GUIDE)+'</p>','<p><b>'+escape(scenario_note(frame))+'</b></p>']
    for (mid,question),g in frame.groupby(['market_id','question'],sort=False):
        parts += ['<section style="border-top:2px solid #7d8792;margin-top:20px;padding-top:8px">',
                  f'<h3>{escape(question)}</h3><p>Contract {escape(str(mid))} · {g.iloc[0].shares:g} shares per position · <a href="{escape(g.iloc[0].url,quote=True)}">Market rules</a></p>',
                  small_html(payoff_table(g)),small_html(grouped_table(g),True),
                  *['<p>'+escape(n)+'</p>' for n in external_notes(g)],'</section>']
    return ''.join(parts)+'</div>'


def display(scanner):
    from IPython.display import display as show, HTML
    frame=build(scanner)
    print(f'{frame.market_id.nunique() if not frame.empty else 0} markets. Every model and both sides are grouped under each market.')
    show(HTML(html(frame)))


def publish(scanner,directory):
    from pathlib import Path
    directory=Path(directory);frame=build(scanner)
    frame.to_parquet(directory/'scanner_grouped.parquet',index=False)
    (directory/'scanner_grouped.html').write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Grouped model-market scan</title></head><body>'+html(frame)+'</body></html>')
    lines=['# All model-market pairs grouped by market','',COMPACT_GUIDE,'',scenario_note(frame),'']
    external_lines=[]
    if scanner.get('external'):
        from polymarket_external import METHOD,status_table
        external_lines=['## External forecast sources','',METHOD,'',status_table(scanner['external']).to_markdown(index=False),'','[Normalized publisher snapshot and receipts](external_forecasts.json)','']
        lines+=external_lines
    if not frame.empty:
        lines += ['## Model codes','',legend_tables(frame).to_markdown(index=False),'']
        for (mid,question),g in frame.groupby(['market_id','question'],sort=False):
            lines += [f'## {question}',f'Contract {mid}; {g.iloc[0].shares:g} shares per position.','',payoff_table(g).to_markdown(index=False),'',grouped_table(g).fillna('—').to_markdown(index=False,floatfmt='.2f'),'',*external_notes(g),'']
    else:lines+=['No market passes the initial screen.']
    (directory/'scanner_initial.md').write_text('\n'.join(lines)+'\n')
    return external_lines+['## All model-market pairs grouped by market','',f'{frame.market_id.nunique() if not frame.empty else 0} markets. All models and both sides appear together in five-column tables.','',
        '[Colored grouped tables](scanner_grouped.html) · [Markdown tables and model legend](scanner_initial.md) · [Full numeric detail](scanner_grouped.parquet) · [Coverage audit](scanner_audit.parquet)','']
