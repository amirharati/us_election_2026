"""Paired shared/state surprise evaluation and final-weight controls."""
from pathlib import Path
import json
import pandas as pd
from state_surprise_comparison import MAIN,LABELS
from seat_review_tables import margin,seats
from run_combination_diagnostics import refresh


def performance(f,group='all'):
 rows=[]
 for model in MAIN:
  row={'Model':LABELS[model]}
  for s,name in [('matched_live','Sep17'),('oct31','Oct31')]:
   r=f['groups'].query('scenario==@s and model==@model and group==@group').iloc[0]
   row[name+' correct']=f'{r.correct}/{r.n}';row[name+' MAE (pp)']=round(r.mae_pp,3)
  rows.append(row)
 return pd.DataFrame(rows)


def cycles(f,s):
 rows=[]
 models=['polling','shared__polling_plus_surprise','state__polling_plus_surprise','shared__learned','state__learned','state__shared_weights']
 for y in range(2012,2026,2):
  q=f['seat_totals'].query('scenario==@s and cycle==@y').set_index('model');row={'Cycle':y}
  row.update({LABELS[m]:f'{int(q.loc[m,"modeled_correct"])}/{int(q.loc[m,"modeled_contests"])}' if m in q.index else 'Warm-up' for m in models});rows.append(row)
 return pd.DataFrame(rows)


def states(f,y=2026,s='matched_live'):
 p=f['predictions'].query('scenario==@s and cycle==@y');v=p.pivot(index='target_id',columns='model',values='prediction')*100
 base=p.query("model=='polling'").set_index('target_id');c=f['components'].query('scenario==@s and cycle==@y').pivot(index='target_id',columns='family',values='predicted_surprise')*100
 rows=[]
 for target,r in base.iterrows():
  row={'State':r.geography+(' special' if '-special-' in target else ''),'Poll samples':int(r.n_samples),'Actual margin':'Pending' if pd.isna(r.actual) else margin(100*r.actual),'Corrected polling':margin(100*r.bias_prediction),
       'Shared S (pp)':round(c.loc[target,'shared'],3) if pd.notna(c.loc[target,'shared']) else '— no polls','State-capable S (pp)':round(c.loc[target,'state'],3) if pd.notna(c.loc[target,'state']) else '— no polls'}
  row.update({LABELS[m]:margin(v.loc[target,m]) if m in v else 'Warm-up' for m in ['shared__learned','state__learned','state__shared_weights']});rows.append(row)
 return pd.DataFrame(rows).sort_values('State')


def seats_table(f):
 rows=[]
 for (s,y),q in f['seat_totals'].groupby(['scenario','cycle']):
  q=q.set_index('model');r=q.loc['polling'];row={'Cycle':y,'Horizon':s,'Actual':'Pending' if pd.isna(r.actual_D) else seats(r.actual_D,r.actual_R),'Completion assumptions':int(r.unmodeled_contests)}
  row.update({LABELS[m]:seats(q.loc[m,'completion_D'],q.loc[m,'completion_R']) if m in q.index else 'Warm-up' for m in MAIN});rows.append(row)
 return pd.DataFrame(rows)


def report(lab,out):
 lab,out=Path(lab),Path(out);f={p.stem:pd.read_parquet(p) for p in out.glob('*.parquet')};fits=json.loads((out/'fits.json').read_text())
 fit_table=pd.DataFrame(fits)[['scenario','cycle','alpha','state_penalty','shared_limit','training_cycles','training_rows','effective_df']]
 f['fit_summary']=fit_table
 text='''# Shared versus state-specific surprise coefficients

Notebook Sections122–124. This changes the economic/approval regression coefficients, **not** the final polling/prior/surprise weights into state-specific weights.

Both versions predict `actual final margin − historical corrected polling` on polled training rows. Shared: `S = x·beta`. State-capable: `S_s = x·(beta + d_s)`, with state deviations shrunk toward shared coefficients. **Neither model has an intercept, state constant or historical-state baseline.** Zero centered feature inputs give zero surprise in every state. There are no monotonic sign constraints.

Keep the same two party-aware national score inputs, training-only normalization/fills, all earlier polled cycles, eight-year decay and previous-cycle validation. Shared slope penalty is chosen from.1/1/10/100; state deviation penalty from.1/1/10/100/infinity. Infinity is the shared limit, so validation can reject state differentiation. Both penalties are selected jointly onY−2marginMAE. A new polled state without local training history uses shared slopes. No-poll states retain their prior; surprise estimates and labels remain missing.

Fixed final recipes remain identical to Sections118–121: baseline prior share1/3with.25Sfor50/25/25, or1/19with.05Sfor90/5/5. For each model family, a global baseline prior share and surprise strength can also be selected independently using the same minimum2/last3prequential-cycle protocol. The **state S, shared fusion weights** control swaps only S while locking the final weights to those selected for the shared model. This distinguishes changing slopes from changing the downstream selection path. Corrected polling and priors are identical across comparisons.

## Recent2016–2024: identical138contests

'''+performance(f).to_markdown(index=False)+'\n\n### Historically competitive states\n\n'+performance(f,'competitive').to_markdown(index=False)
 for s,title in [('matched_live','September17'),('oct31','October31')]:text+='\n\n## '+title+': correct winner calls by cycle\n\n'+cycles(f,s).to_markdown(index=False)
 text+='\n\n## Selected state shrinkage and model size\n\n'+fit_table.round(3).to_markdown(index=False)+'''

`shared_limit=True` means infinite state penalty; blank numeric penalty in that row represents this explicit limit, not missing selection. Ten of15final fits choose the shared limit; five allow state deviations. Stronger complexity is retained only when the previous-cycle score prefers it, but this does not guarantee a benefit on the next cycle.

## Learned global fusion weights and the locked control

'''+f['weights'][f['weights'].model.isin(['shared__learned','state__learned','state__shared_weights'])][['scenario','cycle','model','prior_share','surprise_strength','selection_cycles']].round(3).to_markdown(index=False)+'''

The state-capable recipe has no consistent historical advantage. Full-S September calls tie124/138while MAE worsens7.282→7.437pp; October calls129→128despite slightly lowerMAE5.665→5.646. Fixed light weighting gains oneOctobercall131→132but still has higherMAE than corrected polling alone. With separately selected fusion weights, state-capable results tie124earlier and worsen130→128late.

Holding the shared fusion weights fixed gives the same124/130calls as shared; earlierMAE worsens7.352→7.478while late forecasts match. Thus some degradation in the independently selected late recipe comes from downstream weight selection influenced by different earlier state-model forecasts. These are exploratory results, not a model-promotion claim.

## Current2026

Previous-cycle validation chooses alpha10and **complete shrinkage to the shared slopes**. Both families therefore predict the same **+1.032ppDsurprise** on polled states (+.447momentum,+.585approval). State-specific coefficient freedom adds nothing to the currently selected S.

Their separately selected final multipliers differ: shared a=0,b=.85; state-capable a=0,b=.05. This is because the historical Sforecasts supplied to the weight selector differ, even though the2026Svalues coincide. Holding shared weights fixed makes the current forecasts identical. Shared learned adds+.877ppD; state-capable learned adds+.052ppD. Both give conditional50D/50R. Fixed heavy-prior recipe48/52and light recipe50/50also match between families.

'''+states(f).to_markdown(index=False)+'\n\n## Full chamber totals and historical actuals\n\n'+seats_table(f).to_markdown(index=False)+'''

D includes Democratic-caucusing independents. Historical full totals include explicit incumbent-caucus completion assumptions for unmodeled races, excluded from model accuracy. Current ballot/independent/RCV/runoff limitations remain; these are point-call scenarios, not expected seats or control probabilities. SummaryMAE averages cycles equally; correct calls pool modeled contests. State tables for any historical cycle/horizon can be displayed with the notebook selector. All predictions, actuals and coefficients are retained in parquet artifacts.

## Audit

The intercept-free block solver is checked against a full augmented weighted least-squares system. Fifteen final and15selected inner fits are independently reconstructed; all300penalty candidates are saved. Tests verify exact shared-limit parity, zero surprise at zero features, unseen-state fallback, differing state slopes, and independence from current labels/supplied priors. Shared forecasts are reused unchanged; current Sparity, no-poll invariance, paired metrics, global-weight losses and full100-seat ledgers are audited. No automatic promotion. New notebook cells are evaluated in-process; earlier outputs are preserved.

'''+f'Artifacts: `{out.relative_to(lab)}`. Scripts: `state_surprise_comparison.py`, `state_surprise_tables.py`.\n'
 (lab/'STATE_SURPRISE_RESULTS.md').write_text(text);(out/'STATE_SURPRISE_RESULTS.md').write_text(text)
 (out/'state_surprise_tables.py').write_bytes(Path(__file__).read_bytes());refresh(out);return f
