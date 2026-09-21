"""Paired review of saved uncorrected and bias-corrected polling; no refitting."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from seat_review_tables import margin,seats

NAMES={'matched_live':'September17','oct31':'October31'}

def state_table(q):
    rows=[]
    for r in q.sort_values(['cycle','state','seat_class']).itertuples():
        scored=pd.notna(r.actual_caucus) and r.model_called
        rows.append(dict(Cycle=r.cycle,State=r.state+(' (special)' if r.special else ''),
            **{'Uncorrected prediction':margin(r.polling_pp),'Bias-corrected prediction':margin(r.bias_pp),
               'Correction (pp)':round(r.correction_pp,2) if r.model_called else np.nan,
               'Actual margin':margin(r.actual_margin_pp) if r.cycle<2026 else 'Pending',
               'Actual winner':r.actual_caucus if r.cycle<2026 else 'Pending',
               'Uncorrected correct?':('Yes' if r.polling_call==r.actual_caucus else 'No') if scored else ('Not modeled' if r.cycle<2026 else 'Pending'),
               'Corrected correct?':('Yes' if r.bias_call==r.actual_caucus else 'No') if scored else ('Not modeled' if r.cycle<2026 else 'Pending'),
               'Poll samples':int(r.n_samples) if pd.notna(r.n_samples) else 0,
               'Coverage':('No admitted forecast; completion: keep '+r.caucus) if not r.model_called else ('Prior fallback' if r.n_samples==0 else 'Polled')}))
    return pd.DataFrame(rows)


def build(lab,review):
    lab,review=Path(lab).resolve(),Path(review).resolve()
    settings=json.loads((review/'settings.json').read_text())
    sources={'ledger':review/'full_seat_ledger.parquet','seat_totals':review/'seat_totals.parquet',
             'calls':Path(settings['source_files']['predictions']['path'])}
    hashes={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in sources.items()}
    d=pd.read_parquet(sources['ledger']);tot=pd.read_parquet(sources['seat_totals'])
    key=['cycle','scenario','state','seat_class']
    p=d[d.contested&d.model.eq('polling')].copy();b=d[d.contested&d.model.eq('bias')].copy()
    cols=['prediction_pp','model_caucus','model_called','n_samples','actual_margin_pp','actual_caucus']
    z=p.merge(b[key+cols],on=key,validate='one_to_one',suffixes=('_polling','_bias'))
    for c in ['model_called','n_samples','actual_margin_pp','actual_caucus']:
        assert z[c+'_polling'].equals(z[c+'_bias']),c
        z[c]=z[c+'_polling']
    z=z.rename(columns={'prediction_pp_polling':'polling_pp','prediction_pp_bias':'bias_pp',
        'model_caucus_polling':'polling_call','model_caucus_bias':'bias_call'})
    z['correction_pp']=z.bias_pp-z.polling_pp
    z['changed_call']=z.model_called&z.polling_call.ne(z.bias_call)
    calls=pd.read_parquet(sources['calls']);membership=calls[calls.model.eq('polling')][['cycle','scenario','target_id','history_selection_10pp']]
    z=z.merge(membership,on=['cycle','scenario','target_id'],how='left',validate='many_to_one')
    assert z[z.n_samples.eq(0)&z.model_called].correction_pp.eq(0).all()
    z['polling_correct']=z.polling_call.eq(z.actual_caucus).where(z.model_called&z.cycle.lt(2026))
    z['bias_correct']=z.bias_call.eq(z.actual_caucus).where(z.model_called&z.cycle.lt(2026))
    metrics=[]
    for (scenario,year),q in z[z.cycle.lt(2026)&z.model_called].groupby(['scenario','cycle']):
        metrics.append(dict(Cycle=year,Horizon=NAMES[scenario],Races=len(q),
            **{'Uncorrected correct':int(q.polling_correct.sum()),'Corrected correct':int(q.bias_correct.sum()),
               'Uncorrected MAE (pp)':float((q.polling_pp-q.actual_margin_pp).abs().mean()),
               'Corrected MAE (pp)':float((q.bias_pp-q.actual_margin_pp).abs().mean()),
               'Calls fixed':int((~q.polling_correct.astype(bool)&q.bias_correct.astype(bool)).sum()),
               'Calls spoiled':int((q.polling_correct.astype(bool)&~q.bias_correct.astype(bool)).sum())}))
    metrics=pd.DataFrame(metrics)
    groups=[]
    for scenario,q in z[z.cycle.lt(2026)&z.model_called].groupby('scenario'):
        for label,g in [('All admitted',q),('Polled only',q[q.n_samples>0]),('Prior fallback',q[q.n_samples==0]),('Historically competitive',q[q.history_selection_10pp=='competitive'])]:
            if not len(g):continue
            row=dict(Horizon=NAMES[scenario],Group=label,Races=len(g))
            for stem,display in [('polling','Uncorrected'),('bias','Corrected')]:
                c=int(g[stem+'_correct'].sum());row[display+' correct']=c;row[display+' accuracy (%)']=100*c/len(g)
                row[display+' mean cycle MAE (pp)']=(g[stem+'_pp']-g.actual_margin_pp).abs().groupby(g.cycle).mean().mean()
            groups.append(row)
    groups=pd.DataFrame(groups);seat_rows=[]
    for (year,scenario),g in tot[tot.model.isin(['bias','polling'])].groupby(['cycle','scenario']):
        b=g[g.model=='bias'].iloc[0];p=g[g.model=='polling'].iloc[0]
        seat_rows.append(dict(Cycle=year,Horizon=NAMES[scenario],**{'Uncorrected total*':seats(p.completion_D,p.completion_R),
            'Corrected total*':seats(b.completion_D,b.completion_R),'Actual total':seats(b.actual_D,b.actual_R) if year<2026 else 'Pending',
            'Completion assumptions':int(b.unmodeled_contests)}))
    seat_table=pd.DataFrame(seat_rows)
    out=review/'polling_vs_bias';out.mkdir(exist_ok=True)
    frames=dict(paired_states=z,cycle_metrics=metrics,group_metrics=groups,seat_comparison=seat_table,
                historical_changed_calls=z[z.cycle.lt(2026)&z.changed_call],current_states=z[z.cycle.eq(2026)])
    for name,df in frames.items():df.to_parquet(out/(name+'.parquet'),index=False)
    write_report(lab,out,frames)
    for k,p in sources.items():assert hashlib.sha256(p.read_bytes()).hexdigest()==hashes[k]
    (out/'settings.json').write_text(json.dumps(dict(primary='bias',comparison='polling',refit=False,
        polling_definition='Existing recency/firm-weighted polling baseline, including its already-selected prior blend/fallback, with no learned error correction.',
        actuals='Historical only; missing forecasts never filled with outcomes.',
        sources={k:dict(path=str(p),sha256=hashes[k]) for k,p in sources.items()}),indent=2)+'\n')
    (out/'polling_bias_comparison.py').write_bytes(Path(__file__).read_bytes());refresh(out)
    return out,frames


def write_report(lab,out,f):
    pieces=['''# Uncorrected polling versus state-bias correction

Same frozen inputs, same historical races, same forecast date, no refitting. The retained reference is `bias`; the comparison is `polling` before any learned polling-error correction. The uncorrected baseline retains the existing firm/recency weights and any already-selected historical prior blend; with no polls it falls back to the prior. It is not a newly fitted equal-weight poll average. Bias correction is applied only to polled races. No-poll predictions therefore match exactly.

Positive margin is D−R in percentage points; D +x favors Democrats and R +x favors Republicans. Historical predictions and actual outcomes appear together; 2026 actuals remain Pending. The earlier horizon is September17 each cycle, and the late horizon is October31. Latest 2026 inputs end September17. Architectures have been explored on these outcomes, so this remains an exploratory chronological comparison.

## Historical performance, 2016–2024

''',f['group_metrics'].round(3).to_markdown(index=False),'\n\nThe competitive group uses the previously defined past-results-only rule (at least one absolute margin ≤10pp within the previous three two-year calendar cycles, requiring outcomes in at least two of them; insufficient history stays separate). Correct calls pool races; aggregate margin MAE averages each cycle’s MAE.\n\n',f['cycle_metrics'].round(3).to_markdown(index=False),'''

Correction improves recent overall calls from122→125 of138 in September and126→132 in October. It is not uniformly better: October2016 calls fall26→25, and October2018 margin MAE worsens even though winner calls improve. Safe-state prior fallbacks are unchanged. Better winner accuracy need not improve a full-chamber seat tally because individual errors can offset and missing contests need completion assumptions.

## Final seat totals: predictions and actuals

''',f['seat_comparison'].to_markdown(index=False),'''

*Historical totals include the same explicit incumbent-caucus completion assumptions for unmodeled contests (5–9 per cycle); these are not scored model predictions. D includes Democratic-caucusing independents. Current totals are conditional D−R sign counts, not calibrated expected seats/control probabilities; independent/RCV/runoff/complete-ballot restrictions remain unresolved.

## Current2026: every contested seat

Uncorrected52D/48R versus corrected50D/50R. Only Michigan and Ohio change winner (D→R); all other calls match. Fourteen no-poll contests use the identical prior in both models. The 21 polled contests receive the learned state/shared correction.

''',state_table(f['current_states']).round(3).to_markdown(index=False),'\n\n## Historical changes in winner calls\n\n']
    for scenario,g in f['historical_changed_calls'].groupby('scenario'):
        pieces.extend([f'### {NAMES[scenario]}\n\n',state_table(g).to_markdown(index=False),'\n\n'])
    pieces.append('## Every historical state: both models and actuals\n\n')
    for (year,scenario),g in f['paired_states'][f['paired_states'].cycle.lt(2026)].groupby(['cycle','scenario']):
        pieces.extend([f'### {year}, {NAMES[scenario]}\n\n',state_table(g).to_markdown(index=False),'\n\n'])
    pieces.append('Notebook: BASELINE_MODELS.ipynb Sections99–101. No current forecast was tuned to agree with published forecasters. No calibrated uncertainty or model promotion is implied.\n')
    report=''.join(pieces);(lab/'POLLING_VS_BIAS_REVIEW.md').write_text(report);(out/'POLLING_VS_BIAS_REVIEW.md').write_text(report)


def refresh(out):
    (out/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name!='manifest.json'},indent=2)+'\n')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--review-dir',type=Path,required=True);a=p.parse_args()
    out,frames=build(Path(__file__).resolve().parents[1],a.review_dir)
    print(out);print(frames['group_metrics'].round(3).to_string(index=False))
