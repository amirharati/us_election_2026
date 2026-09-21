"""Explicit surprise labels, baseline weights and final-margin comparisons."""
from pathlib import Path
import pandas as pd
from surprise_fusion import MAIN,LABELS
from seat_review_tables import margin,seats
from run_combination_diagnostics import refresh


def performance(f,group='all',controls=False):
 rows=[]
 models=MAIN if not controls else ['fixed50','fixed50_no_surprise','fixed90','fixed90_no_surprise','learned','learned_no_surprise']
 for model in models:
  row={'Model':LABELS.get(model,model.replace('_',' '))}
  for scenario,name in [('matched_live','Sep17'),('oct31','Oct31')]:
   r=f['groups'].query('model==@model and scenario==@scenario and group==@group').iloc[0]
   row[name+' correct']=f'{r.correct}/{r.n}';row[name+' MAE (pp)']=round(r.mae_pp,3)
  rows.append(row)
 return pd.DataFrame(rows)


def cycles(f,scenario):
 rows=[]
 for year in range(2006,2026,2):
  q=f['seat_totals'].query('cycle==@year and scenario==@scenario').set_index('model')
  row={'Cycle':year}
  for m in MAIN:
   row[LABELS[m]]=f'{int(q.loc[m,"modeled_correct"])}/{int(q.loc[m,"modeled_contests"])}' if m in q.index else 'Warm-up'
  rows.append(row)
 return pd.DataFrame(rows)


def states(f,year=2026,scenario='matched_live'):
 p=f['predictions'].query('cycle==@year and scenario==@scenario');base=p.query("model=='polling'").set_index('target_id');v=p.pivot(index='target_id',columns='model',values='prediction')*100;rows=[]
 for target,r in base.iterrows():
  row={'State':r.geography+(' special' if '-special-' in target else ''),'Poll samples':int(r.n_samples),'Corrected polling':margin(100*r.bias_prediction),'Prior':margin(100*r.prior),
       'Predicted surprise (D−R pp)':'— no polls' if pd.isna(r.predicted_surprise) else round(100*r.predicted_surprise,3),
       'Actual surprise (pp)':'—' if pd.isna(r.actual_surprise) else round(100*r.actual_surprise,3),'Actual margin':'Pending' if pd.isna(r.actual) else margin(100*r.actual)}
  row.update({LABELS[m]:margin(v.loc[target,m]) if m in v.columns else 'Warm-up' for m in ['fixed50','fixed90','learned']});rows.append(row)
 return pd.DataFrame(rows).sort_values('State')


def weights(f):
 return f['weights'].query("model=='learned'")[['scenario','cycle','prior_share','surprise_strength','selection_cycles','validation_mae_pp']].round(4)


def seats_table(f):
 rows=[]
 for (scenario,year),q in f['seat_totals'].groupby(['scenario','cycle']):
  q=q.set_index('model');r=q.loc['polling'];row={'Cycle':year,'Horizon':scenario,'Actual':'Pending' if pd.isna(r.actual_D) else seats(r.actual_D,r.actual_R),'Unmodeled completion assumptions':int(r.unmodeled_contests)}
  row.update({LABELS[m]:seats(q.loc[m,'completion_D'],q.loc[m,'completion_R']) if m in q.index else 'Warm-up' for m in MAIN});rows.append(row)
 return pd.DataFrame(rows)


def report(lab,out):
 lab,out=Path(lab),Path(out);f={p.stem:pd.read_parquet(p) for p in out.glob('*.parquet')}
 text='''# Surprise prediction and polling/prior combination

Notebook Sections118–121. Current inputs remain the frozen September17,2026snapshot. This restores the intended feature target: **surprise relative to corrected polling**, not a standalone final vote margin.

## Exact model and weight meanings

Let C be the retained corrected-polling forecast, P the historical state prior and S the economic/approval surprise forecast. Training labels are `actual D−R margin − historical out-of-time C`. Thus R+15predicted and R+8actual gives **+7ppDemocratic surprise**, despite a Republican victory. Only polled training rows contribute labels; no-poll rows do not silently become polling errors.

S uses the earlier shared two-factor zero-intercept residual regression: economic momentum and national presidential approval, both accounting for White House party. It has **no state historical baseline and no extra intercept**. All previous eligible polled cycles, eight-year decay, training-only preprocessing/imputation andY−2ridge tuning remain. The response is shared across states, unlike the flexible state-specific direct-outcome model in Sections113–117. Zero contribution means the training-average context after centering; no causal or monotonic sign constraint is imposed. For2026there are14past polled cycles/246outcome rows, two nominal coefficients/about1.03effective degrees of freedom.

Final forecast is **`clip((1−a)*C + a*P + b*S)`**. Here a is the prior share of the baseline; b is the surprise multiplier. S is a delta, so it is never directly averaged as though it were a complete margin.

For a requested triple `(polling, prior, surprise)`, normalize the first two entries only:

| Requested setting | Corrected-polling baseline share | Prior baseline share | Surprise multiplier |
|---|---:|---:|---:|
|50/25/25|2/3|1/3|0.25|
|90/5/5|18/19|1/19|0.05|

These are explicitly new **delta-based interpretations**, not the literal three-full-forecast mixtures in Sections113–116. With S=0, the baseline retains its full scale. We also show C+S, P alone, and the exact same fused baseline with surprise disabled, to separate the value of S from the value of prior mixing.

Learned a and b range independently from0to1in0.05steps (441pairs), chosen on equal-cycle **polled** MAE over minimum2/last3completed prequential cycles. Ties prefer less prior then less surprise. Each historical S forecast was trained before its own label. No outer-test/current labels select their own weights. Learned combinations start2016; standalone/fixed forecasts start2012.2006–2010remain warm-up. The fit of S stays anchored to C; when the final baseline includes P, the weights empirically test how useful that correction transfers, rather than claiming it was trained against each blended baseline.

No-poll states retain the existing prior fallback for every arm. S and its label are missing there; the **applied** correction is zero by policy, not a measured zero surprise. All current outcomes remain missing.

## Recent2016–2024: matched138contests

'''+performance(f).to_markdown(index=False)+'\n\n### Historically competitive states\n\n'+performance(f,'competitive').to_markdown(index=False)
 for scenario,title in [('matched_live','September17'),('oct31','October31')]:text+='\n\n## '+title+': correct winner calls by cycle\n\n'+cycles(f,scenario).to_markdown(index=False)
 text+='\n\n## Surprise itself: prediction versus actual surprise\n\n'+f['surprise_metrics'].round(3).to_markdown(index=False)+'''

Positive surprise means Democrats exceed corrected polling; negative means Republicans exceed it. This is not a winner prediction or win probability. Zero-surprise MAE scores the unchanged C forecast; surprise MAE measures how well S predicts the individual remaining errors. `actual_mean_pp` is the cycle-average remaining error over its polled targets, while the shared model predicts one S per cycle.

A major failure is October2020: S predicts **+3.012ppDemocratic surprise** but the actual mean is **−4.611pp**. Its polled-target MAE worsens4.892→7.623pp. The learned combination chose full surprise using earlier2014/2016/2018results, so this is a genuine held-out failure, not current-label tuning. Changing the target makes the interpretation appropriate, but does not guarantee a correct sign or improved forecasts.

## Learned baseline share and surprise strength\n\n'''+weights(f).to_markdown(index=False)+'\n\n## Identical baseline, surprise on versus off\n\n'+performance(f,controls=True).to_markdown(index=False)+'''

For the learned recipes, S adds one recentSeptembercorrect call relative to the same chosen baseline without S (123→124), but the full learned recipe remains below C alone (125). AtOctoberit loses two calls (132→130), mainly2020. Fixed-setting surprise contributions improve earlier marginMAE slightly and worsen lateMAE slightly without changing their aggregate call counts. These outcomes have been explored repeatedly; no automatic promotion.

## Current2026

S=**+1.032ppD**, decomposed into+0.447economic momentum and+0.585approval. The learned selector chooses **a=0,b=.85** from2020/2022/2024Septembervalidation forecasts, so it retains C as baseline and adds **+0.877ppD** to each polled target. There is no Texas-specific reversed economic slope or state baseline inside S.

Current conditional totals: C50D/50R; prior47/53; C+fullS50/50;50/25/25interpretation48/52;90/5/5interpretation50/50;learned50/50. The heavier-prior fixed setting can still flipAK/TXRepublican because the prior is explicitly given one-third baseline weight, not because the surprise is Republican-favorable. Learned Texas isD+1.55and MichiganR+2.90; the original state polling-error correction remains in C.

'''+states(f).to_markdown(index=False)+'\n\n## Full chamber totals and historical actuals\n\n'+seats_table(f).to_markdown(index=False)+'''

D includes Democratic-caucusing independents. Historical full totals retain explicit incumbent-caucus assumptions for unmodeled races; these assumptions are excluded from model accuracy. Actuals use following-January31membership including Georgia2020runoffs. Current ballot/independent/RCV/runoff restrictions remain; no expected seats, control probabilities or calibrated uncertainty is claimed. Margin errors are percentage points and summaryMAE averages cycles equally; correct calls pool admitted contests.

## Historical states, predictions and actuals

'''
 for year in range(2012,2026,2):
  for scenario in ['matched_live','oct31']:text+=f'\n\n### {year}, {scenario}\n\n'+states(f,year,scenario).to_markdown(index=False)
 text+='''

## Audit and rerun

Independently reconstruct15final and60inner residual fits with augmented least squares; C/P/C+S each reproduce427saved forecasts from the earlier residual experiment. Five new tests verify the surprise target, prior independence, future-label protection, weight interpretation, missingness and chronological selection. All components, contributions, candidate losses, weights, outcomes and100-seat ledgers are frozen with hashes. Four appended plain-Python notebook cells are checked in-process; previous outputs are preserved. Full RunAll can rebuild from pinned sources; no data refresh or forecast promotion is implicit.

'''+f'Artifacts: `{out.relative_to(lab)}`. Scripts: `surprise_fusion.py`, `surprise_fusion_tables.py`.\n'
 (lab/'SURPRISE_FUSION_RESULTS.md').write_text(text);(out/'SURPRISE_FUSION_RESULTS.md').write_text(text)
 (out/'surprise_fusion_tables.py').write_bytes(Path(__file__).read_bytes());refresh(out);return f
