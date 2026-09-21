"""Add already-trained momentum/approval stacks to the frozen Senate seat review."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from senate_seat_review import review_forecasts
from seat_review_tables import margin,seats

MODELS=['polling','bias','bias__constant','bias__momentum','bias__approval','bias__both','bias__selected']
LABELS=dict(zip(MODELS,['Polling, uncorrected','Polling + state bias','Bias + constant control','Bias + momentum','Bias + approval','Bias + momentum + approval','Bias + past-selected extra']))
CORE=['polling','bias','bias__momentum','bias__both','bias__selected']

def state_table(ledger,models=CORE):
    rows=[]
    for key,g in ledger[ledger.contested&ledger.model.isin(models)].groupby(['cycle','scenario','state','seat_class']):
        y,sc,state,cls=key;r=g.iloc[0];row=dict(Cycle=y,State=state+(' (special)' if r.special else ''))
        for m in models:row[LABELS[m]]=margin(g.loc[g.model.eq(m),'prediction_pp'].iloc[0])
        row.update({'Actual margin':margin(r.actual_margin_pp) if y<2026 else 'Pending',
            'Actual winner bloc':r.actual_caucus if y<2026 else 'Pending',
            'Coverage':'unmodeled; keep '+r.caucus if not r.model_called else ('prior fallback' if r.n_samples==0 else 'polled')})
        rows.append(row)
    return pd.DataFrame(rows)


def performance(groups,group='all'):
    q=groups[groups.group.eq(group)].copy();q['Model']=q.model.map(LABELS)
    return q.pivot(index='Model',columns='scenario',values=['n','correct','mae_pp']).reindex([LABELS[m] for m in MODELS]).round(3)


def seat_table(totals):
    rows=[]
    for (year,scenario),g in totals.groupby(['cycle','scenario']):
        r=g.iloc[0];row=dict(Cycle=year,Horizon=scenario)
        for m in MODELS:
            a=g[g.model.eq(m)].iloc[0];row[LABELS[m]]=seats(a.completion_D,a.completion_R)
        row['Actual total']=seats(r.actual_D,r.actual_R) if year<2026 else 'Pending'
        row['Unmodeled completion assumptions']=int(r.unmodeled_contests);rows.append(row)
    return pd.DataFrame(rows)


def build(lab,review,feature_run):
    lab,review,feature_run=map(lambda p:Path(p).resolve(),[lab,review,feature_run])
    files=dict(ledger=review/'full_seat_ledger.parquet',predictions=feature_run/'predictions.parquet',
        calls=feature_run/'state_calls.parquet',fits=feature_run/'fits.json',tuning=feature_run/'tuning.parquet',fit_summary=feature_run/'fit_summary.parquet')
    hashes={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in files.items()}
    old=pd.read_parquet(files['ledger']);pred=pd.read_parquet(files['predictions'])
    pred=pred[pred.cycle.ge(2016)&pred.model.isin(MODELS)].copy()
    ledgers=[];totals=[]
    for (year,scenario),group in pred.groupby(['cycle','scenario']):
        reference=old[old.cycle.eq(year)&old.scenario.eq(scenario)&old.model.eq('bias')]
        assert len(reference)==100
        roster=reference[['state','seat_class','seat_id','target_id','contested','special','caucus','actual_caucus']]
        for model,q in group.groupby('model'):
            expected=reference.loc[reference.model_called,'target_id'];assert set(q.target_id)==set(expected)
            q=q.merge(reference.loc[reference.model_called,['target_id','n_firms']],on='target_id',validate='one_to_one')
            ledger,total=review_forecasts(roster,q,int(year),scenario,model)
            ledgers.append(ledger);totals.append(total)
    ledger=pd.concat(ledgers,ignore_index=True);totals=pd.concat(totals,ignore_index=True)
    # Exact references: extra-feature review must never alter the original baselines.
    for model in ['polling','bias']:
        k=['cycle','scenario','seat_id'];a=old[old.model.eq(model)].set_index(k);b=ledger[ledger.model.eq(model)].set_index(k).reindex(a.index)
        for col in ['prediction_pp','actual_margin_pp']:
            assert np.allclose(a[col],b[col],equal_nan=True)
        assert a.completion_caucus.equals(b.completion_caucus)
    calls=pd.read_parquet(files['calls']);calls=calls[calls.cycle.ge(2016)&calls.model.isin(MODELS)]
    groups=[]
    for (scenario,model),g in calls[calls.classification_status.eq('cv_scored')].groupby(['scenario','model']):
        for name,q in [('all',g),('competitive',g[g.history_selection_10pp.eq('competitive')]),('polled',g[g.n_samples.gt(0)]),('no_polls',g[g.n_samples.eq(0)])]:
            if len(q):groups.append(dict(scenario=scenario,model=model,group=name,n=len(q),correct=int(q.correct.sum()),mae_pp=100*(q.prediction-q.actual).abs().groupby(q.cycle).mean().mean()))
    groups=pd.DataFrame(groups)
    fit_summary=pd.read_parquet(files['fit_summary']);fit_summary=fit_summary[fit_summary.cycle.ge(2016)&fit_summary.model.isin(MODELS)]
    tuning=pd.read_parquet(files['tuning']);tuning=tuning[tuning.base.eq('bias')&tuning.cycle.ge(2016)]
    fits=json.loads(files['fits'].read_text());contributions=[]
    for f in fits:
        if f['cycle']!=2026 or f['model'] not in MODELS or f['model']=='bias__selected':continue
        beta=f['standardized_coefficients'];total=100*beta['intercept']
        contributions.append(dict(model=f['model'],component='intercept',contribution_pp=total))
        for term in f['active_terms']:
            raw=f['test_scores'][0][term];raw=f['score_fills'][term] if raw is None or not np.isfinite(raw) else raw
            z=(raw-f['score_centers'][term])/f['score_scales'][term]
            value=100*beta[term]*z;total+=value
            contributions.append(dict(model=f['model'],component=term,contribution_pp=value))
        q=pred[pred.cycle.eq(2026)&pred.model.eq(f['model'])&pred.n_samples.gt(0)]
        assert np.allclose(q.added_correction_pp,total)
    no=pred[pred.n_samples.eq(0)]
    assert np.allclose(no.prediction,no.poll_baseline)
    assert ledger.groupby(['cycle','scenario','model']).size().eq(100).all()
    out=review/'feature_stacks';out.mkdir(exist_ok=True)
    frames=dict(ledger=ledger,totals=totals,groups=groups,fit_summary=fit_summary,tuning=tuning,current_contributions=pd.DataFrame(contributions))
    for name,df in frames.items():df.to_parquet(out/(name+'.parquet'),index=False)
    write_report(lab,out,frames)
    for k,p in files.items():assert hashlib.sha256(p.read_bytes()).hexdigest()==hashes[k]
    (out/'settings.json').write_text(json.dumps(dict(models=MODELS,refit=False,current_as_of='2026-09-17',
        inputs={k:dict(path=str(p),sha256=hashes[k]) for k,p in files.items()},
        feature_definition='shared WH-party-aware economic momentum and overall approval-level scores; fitted to remaining prequential bias errors',
        historical_completion='same pre-cutoff incumbent-caucus assumptions as prior review',certified_seat_forecast=False),indent=2)+'\n')
    (out/'feature_stack_seat_review.py').write_bytes(Path(__file__).read_bytes());refresh(out)
    return out,frames


def write_report(lab,out,f):
    pieces=['''# Polling + state-bias correction + extra factors

Executed as a review of the existing trained momentum/approval models, not a new fit. The preceding `bias` reference uses **polling plus historical state forecasting-error correction only**. It has no economic or approval input. Calibration is not synonymous with regularization: local state corrections can be strong; for2026 the selected state-bias shrinkage is zero.

## Combined model

`final margin = polling + state-bias correction + intercept + momentum coefficient × momentum + approval coefficient × approval`.

The second layer learns actual minus the **historical out-of-time bias-corrected prediction**, so the corrections are not independently trained against the same original polling error and then double-counted. National score coefficients are shared across states. Each historical fold uses earlier cycles only; penalties and the optional feature selector use Y−2. Train-only score construction, imputation and standardization are preserved. Feature history has an8-year half-life; the state-bias layer separately uses its last5calendar-cycle/8-year recipe.

Economic momentum summarizes changes in sentiment, unemployment, inflation/CPI and gasoline costs since January1 and the previous October31, with sensible signs and train-only scaling. Approval is the overall approval-level score. Both are signed by White House party, so favorable conditions support the governing party. The compact combination does not include the separate disruption flag or economic-level score. No new feature search is introduced.

We show momentum-only, approval-only and both, plus a constant-only control and the previous-cycle selector (none/constant/momentum/approval/both). Constant-only distinguishes a general remaining forecast bias from the incremental feature effect. Fixed “both” means those features are included; their ridge penalty is still selected from earlier data. No-poll states keep their prior unchanged.

## Historical2016–2024: identical138races at each horizon

''',performance(f['groups']).to_markdown(),'\n\n`matched_live` is September17 of each cycle, verified against the saved calendars; `oct31` is October31. This corrects older prose describing the earlier comparison as uniformly47days to Election Day. Correct counts pool races; margin MAE averages each cycle, in D−R percentage points. These historically explored models remain exploratory rather than independently confirmed.\n\n### Historically competitive52races\n\n',performance(f['groups'],'competitive').to_markdown(),'''

Momentum alone improves earlier calls125→126 and MAE7.364→7.205 relative to bias alone. Adding both scores instead gives123correct and MAE7.208. October favors bias alone:132correct/5.230pp versus128/5.627with both. Thus extra factors do not consistently improve the strongest reference; the constant control explains much of the earlier MAE change.

## Every cycle: final seat totals versus actuals

''',seat_table(f['totals']).to_markdown(index=False),'''

Totals include continuing seats and explicitly retain incumbent caucus in unmodeled historical contests; these assumptions are excluded from modeled accuracy. They are illustrative complete-chamber scenarios, not a validated model of every historical contest. D includes Democratic-caucusing independents. Current totals remain conditional on scalar D−R signs: full ballot, independent-caucus, ranked-choice and runoff handling is not yet certified. These are not expected seats/control probabilities.

## Current2026: every contested seat

Uncorrected polling52D/48R; bias-only50D/50R; fixed bias+momentum47D/53R; fixed bias+approval47D/53R; fixed bias+both47D/53R. Relative to bias-only, these fixed additions move AK/ME/TX from D to R. Alaska with both is only R+0.014pp, effectively tied. The same winner changes under constant-only show that this seat shift does not isolate a feature benefit.

The previous-cycle selector picks **no extra correction for2026**, retaining50D/50R. Current actual results are Pending. Fourteen no-poll states retain the same prior;21polled states receive the shared extra adjustment.

''',state_table(f['ledger'][f['ledger'].cycle.eq(2026)],MODELS).to_markdown(index=False),'''

### Why the extra layer moves toward Republicans despite current conditions

For the fixed two-score model, the additional D−R correction is approximately **−1.420pp intercept +0.105pp momentum +0.198pp approval =−1.117pp** per polled state. The feature contributions themselves favor Democrats, but they are small relative to the negative residual intercept. This does not mean the model interprets bad economic conditions as helping the incumbent party. The constant-only control is essential for that distinction.

The two-score fit uses14earlier polled cycles (1998–2024),246state outcomes, but the national inputs vary by cycle—not246independent economic environments. Ridge alpha100 strongly shrinks the two slopes. Three nominal parameters including the intercept have about1.235effective degrees of freedom.

''',f['current_contributions'].round(4).to_markdown(index=False),'\n\n### Current extra-layer fit/selection metadata\n\n',f['fit_summary'][f['fit_summary'].cycle.eq(2026)].round(4).to_markdown(index=False),'\n\n## Historical state-by-state forecasts alongside actuals\n\n']
    for (year,scenario),g in f['ledger'][f['ledger'].cycle.lt(2026)].groupby(['cycle','scenario']):
        pieces.extend([f'### {year}, {scenario}\n\n',state_table(g).to_markdown(index=False),'\n\n'])
    pieces.append('Notebook Sections102–104. Models and source snapshots are unchanged; this review adds comparable state/seat displays. Baseline parity, missing-poll invariance, current contribution sums, unique100-seat ledgers and input/artifact hashes are checked.\n')
    report=''.join(pieces);(lab/'FEATURE_STACK_SEAT_REVIEW.md').write_text(report);(out/'FEATURE_STACK_SEAT_REVIEW.md').write_text(report)


def refresh(out):
    (out/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name!='manifest.json'},indent=2)+'\n')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--review-dir',type=Path,required=True);p.add_argument('--feature-run',type=Path,required=True);a=p.parse_args()
    out,f=build(Path(__file__).resolve().parents[1],a.review_dir,a.feature_run);print(out);print(seat_table(f['totals'][f['totals'].cycle.eq(2026)]).to_string(index=False))
