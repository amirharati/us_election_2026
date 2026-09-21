"""Complete the direct/surprise × shared/state comparison on frozen inputs."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
import pandas as pd
from three_model_comparison import prepare_direct
from score_baselines import ALPHAS
from senate_seat_review import review_forecasts
from run_combination_diagnostics import refresh

LABELS={'polling':'Corrected polling','prior':'Historical prior','direct_shared':'Direct: shared regression',
        'direct_state':'Direct: state regression','surprise_shared':'Polling + shared surprise','surprise_state':'Polling + state surprise'}

def solve(p,alpha):
    """Shared linear ridge; unpenalized intercept, no state columns or offsets."""
    z,w=p['z'],p['weights'];penalty=np.r_[0.,np.repeat(alpha,z.shape[1]-1)]
    gram=z.T@(w[:,None]*z);normal=gram+np.diag(penalty)
    beta=np.linalg.solve(normal,z.T@(w*p['response']))
    augmented=np.vstack([np.sqrt(w)[:,None]*z,np.diag(np.sqrt(penalty))])
    expected=np.linalg.lstsq(augmented,np.r_[np.sqrt(w)*p['response'],np.zeros(len(beta))],rcond=None)[0]
    assert np.allclose(beta,expected,atol=1e-10)
    return np.clip(p['future']@beta,-1,1),beta,float(np.trace(np.linalg.solve(normal,gram)))

def fit(source,cal,year):
    tr=source[source.cycle.lt(year)&source.actual.notna()];te=source[source.cycle.eq(year)]
    inner=tr[tr.cycle.lt(year-2)];valid=tr[tr.cycle.eq(year-2)]
    if inner.cycle.nunique()<6 or valid.empty:raise ValueError('Six inner cycles and a previous validation cycle required')
    ip=prepare_direct(inner,valid,cal);fp=prepare_direct(tr,te,cal)
    grid=[]
    for alpha in ALPHAS:
        v,_,_=solve(ip,alpha)
        grid.append(dict(scenario=source.scenario.iloc[0],cycle=int(year),alpha=alpha,validation_cycle=int(year-2),training_max_cycle=int(inner.cycle.max()),validation_mae_pp=float(100*np.abs(v-valid.actual).mean())))
    best=min(grid,key=lambda r:(round(r['validation_mae_pp'],10),-r['alpha']))
    pred,beta,df=solve(fp,best['alpha']);terms=['intercept']+fp['design'].active
    info=dict(scenario=source.scenario.iloc[0],cycle=int(year),alpha=best['alpha'],validation_cycle=int(year-2),validation_mae_pp=best['validation_mae_pp'],
        training_cycles=int(tr.cycle.nunique()),training_rows=len(tr),training_max_cycle=int(tr.cycle.max()),training_first_cycle=int(tr.cycle.min()),effective_cycles=fp['effective_cycles'],
        nominal_parameters=3,active_parameters=len(beta),effective_df=df,coefficients=dict(zip(terms,map(float,beta))),half_life_years=8.,**fp['design'].metadata())
    q=te.assign(prediction=pred,model='direct_shared');q['shared_intercept_pp']=100*beta[0]
    for name,column in [('economy_momentum_wh','momentum_pp'),('approval_wh','approval_pp')]:
        q[column]=100*fp['future'][:,terms.index(name)]*beta[terms.index(name)] if name in terms else 0.
    assert q.prediction.nunique()==1
    return q,info,grid

def verify(path):
    m=json.loads((path/'manifest.json').read_text())
    assert all(hashlib.sha256((path/k).read_bytes()).hexdigest()==v for k,v in m.items())
    return hashlib.sha256((path/'manifest.json').read_bytes()).hexdigest()

def build(lab,state_source,direct_source):
    lab,state_source,direct_source=map(lambda x:Path(x).resolve(),[lab,state_source,direct_source])
    hashes={str(p):verify(p) for p in [state_source,direct_source]}
    settings=json.loads((direct_source/'settings.json').read_text());original=Path(settings['source'])
    assert verify(original)==settings['source_manifest_sha256']
    src=json.loads((original/'settings.json').read_text())['sources']
    assert all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in src.values())
    h=pd.read_parquet(src['history']['path']);h=h[h.base.eq('fixed5_8')];cal=pd.read_parquet(src['calendars']['path'])
    state=pd.read_parquet(state_source/'predictions.parquet');direct=pd.read_parquet(direct_source/'predictions.parquet')
    parts=[];fits=[];tuning=[]
    for scenario,s in h.groupby('scenario'):
        for year in sorted(state.loc[state.scenario.eq(scenario),'cycle'].unique()):
            q,f,g=fit(s,cal[cal.scenario.eq(scenario)],int(year));parts.append(q);fits.append(f);tuning+=g
    for model,old in [('polling','polling'),('prior','prior'),('surprise_shared','shared__polling_plus_surprise'),('surprise_state','state__polling_plus_surprise')]:
        parts.append(state[state.model.eq(old)].assign(model=model))
    parts.append(direct[direct.model.eq('features')].assign(model='direct_state'))
    pred=pd.concat(parts,ignore_index=True).drop(columns=['history_selection_10pp'],errors='ignore')
    member=state[state.model.eq('polling')][['scenario','target_id','history_selection_10pp']]
    pred=pred.merge(member,on=['scenario','target_id'],validate='many_to_one')
    assert pred.groupby('model').size().nunique()==1
    ledger=pd.read_parquet(state_source/'full_seat_ledger.parquet');ledgers=[];totals=[]
    for (scenario,year,model),q in pred.groupby(['scenario','cycle','model']):
        r=ledger[ledger.scenario.eq(scenario)&ledger.cycle.eq(year)&ledger.model.eq('polling')]
        l,t=review_forecasts(r[['state','seat_class','seat_id','target_id','contested','special','caucus','actual_caucus']],q,int(year),scenario,model);ledgers.append(l);totals.append(t)
    groups=[]
    for (scenario,model),q in pred[pred.cycle.between(2016,2024)].groupby(['scenario','model']):
        for group,g in [('all',q),('competitive',q[q.history_selection_10pp.eq('competitive')])]:
            groups.append(dict(scenario=scenario,model=model,group=group,n=len(g),correct=int(((g.prediction>0)==(g.actual>0)).sum()),mae_pp=float(100*(g.prediction-g.actual).abs().groupby(g.cycle).mean().mean())))
    frames=dict(predictions=pred,groups=pd.DataFrame(groups),tuning=pd.DataFrame(tuning),seat_totals=pd.concat(totals,ignore_index=True),full_seat_ledger=pd.concat(ledgers,ignore_index=True))
    out=state_source.parent.parent/'shared_direct'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True)
    for name,q in frames.items():q.to_parquet(out/(name+'.parquet'),index=False)
    (out/'fits.json').write_text(json.dumps(fits,indent=2,allow_nan=False)+'\n')
    (out/'settings.json').write_text(json.dumps(dict(sources=hashes,source_inputs=src,target='actual final D-R margin',formula='clip(intercept + beta_economy*x_economy + beta_approval*x_approval)',training='all earlier admitted Senate outcomes; equal cycle mass before 8-year decay; train-only normalization/fills; alpha chosen on Y-2',no_poll='direct model predicts regardless of polls; no supplied prior/poll offset',scope='One new shared direct model; existing reference forecasts retained unchanged; no new fusion tuning',promotion=False),indent=2)+'\n')
    (out/Path(__file__).name).write_bytes(Path(__file__).read_bytes());refresh(out)
    return out,frames

def performance(f,group='all'):
    rows=[]
    for model,label in LABELS.items():
        row={'Model':label}
        for scenario,title in [('matched_live','Sep17'),('oct31','Oct31')]:
            r=f['groups'].query('scenario==@scenario and model==@model and group==@group').iloc[0]
            row[title+' correct']=f'{r.correct}/{r.n}';row[title+' MAE (pp)']=round(r.mae_pp,3)
        rows.append(row)
    return pd.DataFrame(rows)

def states(f,year=2026,scenario='matched_live'):
    from seat_review_tables import margin
    p=f['predictions'].query('cycle==@year and scenario==@scenario');v=p.pivot(index='target_id',columns='model',values='prediction')
    b=p[p.model.eq('polling')].set_index('target_id');rows=[]
    for target,r in b.iterrows():
        row={'State':r.geography+(' special' if '-special-' in target else ''),'Actual':'Pending' if pd.isna(r.actual) else margin(100*r.actual)}
        row.update({label:margin(100*v.loc[target,m]) for m,label in LABELS.items()});rows.append(row)
    return pd.DataFrame(rows).sort_values('State')

def cycle_table(f):
    from seat_review_tables import seats
    rows=[]
    for (scenario,year),g in f['seat_totals'].groupby(['scenario','cycle']):
        q=g.set_index('model');r=q.loc['polling'];row={'Cycle':year,'Horizon':scenario,'Actual seats':'Pending' if pd.isna(r.actual_D) else seats(r.actual_D,r.actual_R),'Unmodeled completion':int(r.unmodeled_contests)}
        for model,label in LABELS.items():
            t=q.loc[model];row[label+' calls']='Pending' if year==2026 else f'{int(t.modeled_correct)}/{int(t.modeled_contests)}'
            row[label+' seats']=seats(t.completion_D,t.completion_R)
        rows.append(row)
    return pd.DataFrame(rows)

def report(lab,out):
    lab,out=Path(lab),Path(out);f={p.stem:pd.read_parquet(p) for p in out.glob('*.parquet')}
    fits=json.loads((out/'fits.json').read_text());f['fits']=pd.DataFrame(fits)
    text='''# Shared direct regression: complete the four regression cases

Notebook Sections 125–126. New model: one shared intercept and shared economic-momentum/approval coefficients predict final D−R margin directly. This is linear ridge regression (three nominal parameters), with the same four positive alpha choices, eight-year decay, train-only score normalization/median fills and previous-cycle validation as the state direct model. All older admitted Senate outcomes train it, including unpolled states. Each cycle has equal total row weight before decay. No state indicators or supplied prior/poll offset enter the model.

With national inputs and shared coefficients, every state gets the same direct forecast in a cycle. This estimates a response related to the mean admitted contest margin, NOT national popular vote or an equally representative panel of all states: the contested/covered states change by cycle. Repeated state rows are not independent national feature contexts. A global intercept is appropriate for this direct outcome control; the two surprise models remain intercept-free. No new mixtures are tuned or old forecasts replaced.

The table completes direct/shared, direct/state, surprise/shared and surprise/state. Surprise rows add the full predicted adjustment to the same corrected polling baseline (not separately learned final fusion). Direct models train on all admitted past outcomes; surprise models need polled error labels, so their training coverage differs. Current and historical evaluation contests match across all rows.

## 2016–2024, same contests

'''+performance(f).to_markdown(index=False)+'\n\n## Historically competitive subset\n\n'+performance(f,'competitive').to_markdown(index=False)+'\n\n## Training and coefficients\n\n'+f['fits'][['scenario','cycle','alpha','training_cycles','training_rows','effective_cycles','active_parameters','effective_df','coefficients']].to_markdown(index=False)+'\n\n## Current state forecasts\n\n'+states(f).to_markdown(index=False)+'\n\n## Per-cycle winner calls and full chamber scenarios\n\n'+cycle_table(f).to_markdown(index=False)+'''

Historical modeled-contest accuracy excludes incumbent-caucus completion assumptions used for missing contests. D includes Democratic-caucusing independents. Chamber totals are conditional point calls, not expected seats/control probabilities; ballot, independent, RCV/runoff and coverage limitations remain. MAE averages cycles equally. Earlier 2006–2010 cycles remain warm-up; direct/fixed comparisons here score 2012–2024, with 2026 outcomes pending. No model promotion follows from repeatedly explored historical results.
'''
    (lab/'SHARED_DIRECT_RESULTS.md').write_text(text);(out/'SHARED_DIRECT_RESULTS.md').write_text(text);refresh(out);return f
