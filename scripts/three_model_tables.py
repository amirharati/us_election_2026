"""Readable three-forecast comparison, literal weights and component ablations."""
from pathlib import Path
import json
import pandas as pd
from three_model_comparison import MODELS,LABELS
from seat_review_tables import margin,seats
from run_combination_diagnostics import refresh


def performance(f,group='all'):
 rows=[]
 for m in MODELS:
  row={'Model':LABELS[m]}
  for scenario,label in [('matched_live','Sep17'),('oct31','Oct31')]:
   r=f['groups'].query('scenario==@scenario and model==@m and group==@group').iloc[0]
   row[label+' correct']=f'{r.correct}/{r.n}';row[label+' MAE (pp)']=round(r.mae_pp,3)
  rows.append(row)
 return pd.DataFrame(rows)


def cycles(f,scenario,metric='calls'):
 rows=[]
 for year in range(2006,2026,2):
  q=f['seat_totals'].query('scenario==@scenario and cycle==@year').set_index('model')
  row={'Cycle':year,'Status':'Scored' if len(q) else 'Warm-up'}
  for m in MODELS:
   if m not in q.index:row[LABELS[m]]='Warm-up';continue
   r=q.loc[m];row[LABELS[m]]=f'{int(r.modeled_correct)}/{int(r.modeled_contests)}' if metric=='calls' else round(r.modeled_mae_pp,3)
  rows.append(row)
 return pd.DataFrame(rows)


def weights(f):
 return f['weights'].query("model=='learned'")[['scenario','cycle','selection_cycles','w_poll','w_prior','w_features','validation_mae_pp']].round(3)


def states(f,year=2026,scenario='matched_live'):
 p=f['predictions'].query('cycle==@year and scenario==@scenario');v=p.pivot(index='target_id',columns='model',values='prediction')*100
 b=p.query("model=='polling'").set_index('target_id');rows=[]
 coef=f['coefficients'].query('cycle==@year and scenario==@scenario').drop_duplicates('geography').set_index('geography')
 for target,r in b.iterrows():
  row={'State':r.geography+(' special' if '-special-' in target else ''),'Poll samples':int(r.n_samples),'Actual margin':'Pending' if pd.isna(r.actual) else margin(100*r.actual)}
  row.update({LABELS[m]:margin(v.loc[target,m]) if m in v else 'Warm-up' for m in MODELS})
  row['M3 state-history cycles']=int(coef.loc[r.geography,'training_cycles'])
  rows.append(row)
 return pd.DataFrame(rows).sort_values('State')


def seat_table(f):
 rows=[]
 for (scenario,year),q in f['seat_totals'].groupby(['scenario','cycle']):
  q=q.set_index('model');r=q.loc['polling'];row={'Cycle':year,'Horizon':scenario,'Actual':'Pending' if pd.isna(r.actual_D) else seats(r.actual_D,r.actual_R),'Unmodeled completion assumptions':int(r.unmodeled_contests)}
  row.update({LABELS[m]:seats(q.loc[m,'completion_D'],q.loc[m,'completion_R']) if m in q.index else 'Warm-up' for m in MODELS});rows.append(row)
 return pd.DataFrame(rows)


def ablation(f):
 rows=[]
 for (s,m,removed),g in f['ablation'].query('cycle>=2016 and cycle<=2024').groupby(['scenario','model','removed']):
  q=g[g.status.eq('scored')]
  rows.append({'Horizon':s,'Combination':LABELS[m],'Component kept vs removed':LABELS[removed],
    'Scored races':len(q),'MAE benefit of including (pp)':round(q.groupby('cycle').benefit_mae_pp.mean().mean(),3) if len(q) else None,
    'Net correct-call benefit':int(q.call_benefit.sum()) if len(q) else None,
    'Undefined cycles':int(g.loc[g.status.str.startswith('undefined'),'cycle'].nunique())})
 return pd.DataFrame(rows)


def report(lab,out):
 lab,out=Path(lab),Path(out);f={p.stem:pd.read_parquet(p) for p in out.glob('*.parquet')}
 text='''# Three standalone predictions and their weighted combinations

Notebook Sections113–116. This supersedes the proposed additive interpretation for this experiment: all three constituents now predict a **complete state D−R margin**, so the requested weights are literal convex forecast weights.

## Four prediction views

1. **M1, corrected polling:** exact retained polling + historical state forecast-error correction. Its existing prior regularization/no-poll fallback is unchanged.
2. **M2, historical prior:** exact retained state historical-result baseline. This is separate from polling-bias correction; both learn from history in different ways.
3. **M3, feature-only outcome regression:** economic momentum + presidential approval, signed for the White House party, predict the actual final margin directly. No polling input and no M2 prior offset. State-specific intercepts and slopes are shrunk toward shared coefficients using the existing partially pooled regression. State identity therefore matters, and state lean is learned from historical outcomes; this model is not independent of the history used by M2. There is no externally supplied historical-prior prediction hidden in M3.
4. **Combined prediction:** `w1*M1 + w2*M2 + w3*M3`. Compare fixed50/25/25, fixed90/5/5 and weights selected from previous cycles. All weights are nonnegative and sum to1. These are three variants of the fourth view, hence six columns in the tables.

M3 uses all earlier admitted Senate outcomes with the existing8-year historical decay, training-only score normalization/median imputation, and only the two active score families. Ridge alpha and state-deviation penalty are selected onY−2; refit using all earlier cycles. Intercepts here belong to a complete outcome forecast, unlike the excluded extra intercept in the earlier polling-residual experiment. National features alone do not differentiate states; state coefficients do. An unseen state receives the shared prediction, never a covert M2 offset.

The learned combination selects among231 simplex weight triples at5-percentage-point increments, minimizing equally weighted cycle MAE over the **last three completed prequential forecast cycles**, with a minimum of two. Ties favor more polling, then more prior. For2016the history is2012/2014; from2018onward it is three cycles.2012/2014have standalone/fixed results but insufficient combination-training history. Each validation constituent was trained before its own outcome; no test-cycle/current outcomes choose their own weights. No extra intercept or unconstrained fusion coefficients are fitted.

No-poll states: M1 retains its existing prior fallback; M3 can predict regardless of polls; combinations use the same literal weights everywhere. The components share historical information and are not independent evidence. These are repeatedly explored historical outcomes, not an untouched confirmatory test.

## Recent2016–2024: same138modeled contests for every method

'''+performance(f).to_markdown(index=False)+'\n\n### Historically competitive states\n\n'+performance(f,'competitive').to_markdown(index=False)
 for s,title in [('matched_live','September17'),('oct31','October31')]:
  text+='\n\n## '+title+': correct winner calls by cycle\n\n'+cycles(f,s).to_markdown(index=False)
  text+='\n\n### Mean absolute margin error by cycle (pp)\n\n'+cycles(f,s,'mae').to_markdown(index=False)
 text+='\n\n## Learned weights\n\n'+weights(f).to_markdown(index=False)+'''

Current2026 selection is **95% corrected polling /0% prior /5% features**, trained on2020/2022/2024earlier-horizon predictions. Every historical October selection is100%polling, reproducing its132/138calls exactly. Earlier learned weighting gives123/138versus125/138for M1, so learning weights has not improved recent accuracy. Fixed90/5/5slightly improves earlier margin MAE but loses one call; fixed50/25/25does worse overall.

## Which component helps or hurts inside the combination?

Remove one component and renormalize the two remaining weights, without retuning. A **positive benefit** means including that component improved the full combination relative to its removal; negative means it hurt. Margin benefit averages cycle-level error differences; call benefit is net additional correct modeled calls. This is a predictive comparison, not a causal effect. It is undefined when the removed component has all the weight, and that is recorded rather than fabricated. A zero-weight component has no effect. These comparisons differ from asking whether the full combination beats M1 alone.

'''+ablation(f).to_markdown(index=False)+'''

For example, features at5%help the September90/5/5mix by one call relative to removing that component, yet the complete mix still loses one call against M1. At25%, features hurt both horizons. This shows why standalone quality and conditional contribution are different questions.

## Current2026: predicted margins and full chamber totals

M1 point tally50D/50R; M2 47D/53R; M3 56D/44R; fixed50/25/25and90/5/5both49D/51R; learned50D/50R. These are fragile margin-sign tallies, not expected seats. Explicit prior weighting can still move a state Republican even if national inputs help Democrats; that prior influence is now visible in its own column.

M3 currently has no admitted state-specific training outcome for **AK, GA, LA and ME**, so these four share its national prediction. That reflects the scalar D−R training restrictions, not an absence of real elections. Current M3 selects alpha.1/statepenalty.1, with141nominal parameters and about106.46effective degrees of freedom across25national cycles/725state outcome rows. This model is more flexible than the shared residual model; its weaker historical results and sparse-state fallback are reasons not to promote it.

'''+states(f).to_markdown(index=False)+'\n\n## Full chamber totals by cycle, beside actuals\n\n'+seat_table(f).to_markdown(index=False)+'''

D includes Democratic-caucusing independents. Full historical totals add continuing seats and explicitly retain the incumbent caucus in unmodeled races; those completion assumptions do not count as model accuracy. Actuals are following-January31membership including Georgia2020runoffs. Current ballot/independent/RCV/runoff restrictions remain. Neither full-chamber uncertainty nor control probabilities are modeled here. MAE uses D−R percentage points and equal weight across cycles; correct calls pool admitted contests. Missing actuals stay missing.

## Historical states: all six predictions and actual outcomes

'''
 for year in range(2012,2026,2):
  for scenario in ['matched_live','oct31']:
   text+=f'\n\n### {year}, {scenario}\n\n'+states(f,year,scenario).to_markdown(index=False)
 text+='''

## Reproduction and audit

All15final M3fits and their selected inner validation fits are independently reconstructed using full augmented weighted least squares, separate from the block solver. Tests verify direct-model independence from supplied prior/poll values, future-label independence in fitting and combination selection, convex weights, warm-up/tie rules and undefined ablations. M1/M2 exactly reproduce the frozen references; paired coverage and complete100-seat ledgers are checked. Source/artifact hashes, all240feature-penalty candidates,2541weight candidates, coefficients, folds' training history, component forecasts and per-state ablations are retained. New notebook cells are executed in-process; no full-notebook kernel rerun is claimed.

'''+f'Artifacts: `{out.relative_to(lab)}`.\n'
 (lab/'THREE_MODEL_RESULTS.md').write_text(text);(out/'THREE_MODEL_RESULTS.md').write_text(text)
 (out/'three_model_tables.py').write_bytes(Path(__file__).read_bytes());refresh(out);return f
