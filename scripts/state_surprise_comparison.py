"""Shared versus partially pooled state surprise slopes, with no intercepts."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
import pandas as pd
from momentum_approval_models import prepare_subset
from score_baselines import ALPHAS
from surprise_fusion import assemble,combine
from senate_seat_review import review_forecasts
from run_combination_diagnostics import refresh

STATE_PENALTIES=[.1,1.,10.,100.,float('inf')]
ARMS=['polling_plus_surprise','fixed50','fixed90','learned']
LABELS={'polling':'Corrected polling','prior':'Historical prior','state__shared_weights':'State S, shared fusion weights'}
for family in ['shared','state']:
 for arm,label in [('polling_plus_surprise','polling + full S'),('fixed50','50/25/25 interpretation'),('fixed90','90/5/5 interpretation'),('learned','learned fusion')]:
  LABELS[family+'__'+arm]=family.title()+' S, '+label
MAIN=['polling']+[f+'__'+a for a in ARMS for f in ['shared','state']]+['state__shared_weights']


def solve(z,y,w,states,alpha,state_penalty):
    """Joint ridge fit: shared slopes beta, state deviations d_s; no constants."""
    z,y,w,states=np.asarray(z,float),np.asarray(y,float),np.asarray(w,float),np.asarray(states,str)
    if z.ndim!=2 or len(z)!=len(y) or len(y)!=len(w) or len(y)!=len(states) or not np.isfinite(z).all() or not np.isfinite(y).all() or not np.isfinite(w).all() or not (w>0).all():raise ValueError('Finite aligned training data required')
    if not np.isfinite(alpha) or alpha<=0 or not state_penalty>0:raise ValueError('Positive penalties required')
    k=z.shape[1];gram=z.T@(w[:,None]*z);normal=gram+alpha*np.eye(k);rhs=z.T@(w*y)
    if np.isinf(state_penalty):
        shared=np.linalg.solve(normal,rhs) if k else np.empty(0)
        return shared,{},float(np.trace(np.linalg.solve(normal,gram))) if k else 0.
    blocks={}
    for state in sorted(set(states)):
        use=states==state;x,ww,yy=z[use],w[use],y[use]
        cross=x.T@(ww[:,None]*x);b=cross+state_penalty*np.eye(k);inv=np.linalg.solve(b,np.eye(k)) if k else b
        t=x.T@(ww*yy);normal-=cross@inv@cross.T;rhs-=cross@inv@t;blocks[state]=(cross,inv,t)
    shared=np.linalg.solve(normal,rhs) if k else np.empty(0);invshared=np.linalg.solve(normal,np.eye(k)) if k else normal
    deviations={};ptrace=alpha*np.trace(invshared)
    for state,(cross,inv,t) in blocks.items():
        deviations[state]=inv@(t-cross.T@shared);h=inv@cross.T
        ptrace+=state_penalty*np.trace(inv+h@invshared@h.T)
    return shared,deviations,float(k*(1+len(blocks))-ptrace)


def predict(p,alpha,penalty):
    z,v=p['z'][:,1:],p['future'][:,1:]
    sh,dev,df=solve(z,p['response'],p['weights'],p['train'].geography,alpha,penalty)
    coefficients=np.array([sh+dev.get(s,np.zeros(len(sh))) for s in p['test'].geography])
    contributions=v*coefficients
    return contributions.sum(axis=1),sh,dev,df,contributions


def independent(p,alpha,penalty):
    z,v=p['z'][:,1:],p['future'][:,1:];k=z.shape[1]
    states=[] if np.isinf(penalty) else sorted(p['train'].geography.unique())
    x=np.zeros((len(z),k*(1+len(states))));future=np.zeros((len(v),x.shape[1]));x[:,:k]=z;future[:,:k]=v
    for j,s in enumerate(states,1):
        use=p['train'].geography.eq(s).to_numpy();x[use,j*k:(j+1)*k]=z[use]
        use=p['test'].geography.eq(s).to_numpy();future[use,j*k:(j+1)*k]=v[use]
    penalties=np.r_[np.full(k,alpha),np.full(k*len(states),penalty)]
    a=np.vstack([np.sqrt(p['weights'])[:,None]*x,np.diag(np.sqrt(penalties))]);b=np.r_[np.sqrt(p['weights'])*p['response'],np.zeros(x.shape[1])]
    coef=np.linalg.lstsq(a,b,rcond=None)[0] if x.shape[1] else np.empty(0)
    return future@coef


def fit(source,cal,year):
    tr=source[source.cycle.lt(year)&source.actual.notna()&source.n_samples.gt(0)];te=source[source.cycle.eq(year)];apply=te[te.n_samples.gt(0)]
    inner=tr[tr.cycle.lt(year-2)];valid=tr[tr.cycle.eq(year-2)]
    if inner.cycle.nunique()<6 or valid.empty:raise ValueError('Insufficient chronological training')
    ip=prepare_subset(inner,valid,cal,'bias','both');fp=prepare_subset(tr,apply if len(apply) else te.iloc[:1],cal,'bias','both')
    candidates=[]
    for alpha in ALPHAS:
        for penalty in STATE_PENALTIES:
            s,*_=predict(ip,alpha,penalty);loss=float(100*np.abs(np.clip(valid.bias_prediction+s,-1,1)-valid.actual).mean())
            candidates.append(dict(alpha=alpha,state_penalty=penalty,validation_mae_pp=loss,scenario=source.scenario.iloc[0],cycle=int(year),validation_cycle=int(year-2),training_max_cycle=int(inner.cycle.max())))
    best=min(candidates,key=lambda r:(round(r['validation_mae_pp'],10),-r['state_penalty'],-r['alpha']))
    s,sh,dev,df,contrib=predict(fp,best['alpha'],best['state_penalty'])
    expected=independent(fp,best['alpha'],best['state_penalty']);assert np.allclose(s,expected,atol=1e-10)
    vs=independent(ip,best['alpha'],best['state_penalty']);assert np.isclose(100*np.abs(np.clip(valid.bias_prediction+vs,-1,1)-valid.actual).mean(),best['validation_mae_pp'])
    q=te.copy();q['predicted_surprise']=np.nan;q.loc[apply.index,'predicted_surprise']=s if len(apply) else np.empty(0)
    q['actual_surprise']=np.where(q.n_samples.gt(0)&q.actual.notna(),q.actual-q.bias_prediction,np.nan)
    names=fp['design'].active
    for name,col in [('economy_momentum_wh','momentum_contribution'),('approval_wh','approval_contribution')]:
        q[col]=np.nan;q.loc[apply.index,col]=(contrib[:,names.index(name)] if name in names else np.zeros(len(apply))) if len(apply) else np.empty(0)
    records=[]
    for state in sorted(set(tr.geography)|set(te.geography)):
        tt=tr[tr.geography.eq(state)];total=sh+dev.get(state,np.zeros(len(sh)))
        for j,name in enumerate(names):records.append(dict(scenario=source.scenario.iloc[0],cycle=int(year),state=state,term=name,shared_coefficient=float(sh[j]),state_deviation=float(total[j]-sh[j]),total_coefficient=float(total[j]),training_rows=len(tt),training_cycles=int(tt.cycle.nunique()),status='shared_no_state_history' if tt.empty else 'shared_limit' if np.isinf(best['state_penalty']) else 'partially_pooled'))
    info=dict(scenario=source.scenario.iloc[0],cycle=int(year),alpha=best['alpha'],state_penalty=None if np.isinf(best['state_penalty']) else best['state_penalty'],shared_limit=bool(np.isinf(best['state_penalty'])),validation_mae_pp=best['validation_mae_pp'],training_cycles=int(tr.cycle.nunique()),training_rows=len(tr),training_states=int(tr.geography.nunique()),training_max_cycle=int(tr.cycle.max()),effective_df=df,nominal_parameters=len(names)*(1+(0 if np.isinf(best['state_penalty']) else tr.geography.nunique())),intercept=0.,independent_max_difference=float(np.max(np.abs(s-expected))),**fp['design'].metadata())
    return q,info,candidates,pd.DataFrame(records)


def build(lab,shared_source):
    lab,shared_source=Path(lab).resolve(),Path(shared_source).resolve()
    manifest=json.loads((shared_source/'manifest.json').read_text());assert all(hashlib.sha256((shared_source/k).read_bytes()).hexdigest()==v for k,v in manifest.items())
    shared_settings=json.loads((shared_source/'settings.json').read_text());original=Path(shared_settings['source'])
    assert hashlib.sha256((original/'manifest.json').read_bytes()).hexdigest()==shared_settings['source_manifest_sha256']
    settings=json.loads((original/'settings.json').read_text())
    assert all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in settings['sources'].values())
    h=pd.read_parquet(settings['sources']['history']['path']);h=h[h.base.eq('fixed5_8')]
    cal=pd.read_parquet(settings['sources']['calendars']['path']);shared=pd.read_parquet(shared_source/'components.parquet')
    comps=[];fits=[];tuning=[];coefs=[]
    for scenario,source in h.groupby('scenario'):
        for year in sorted(shared.loc[shared.scenario.eq(scenario),'cycle'].unique()):
            q,f,g,c=fit(source,cal[cal.scenario.eq(scenario)],int(year));comps.append(q);fits.append(f);tuning+=g;coefs.append(c)
    state=pd.concat(comps,ignore_index=True);statepred,sw,sg=assemble(state)
    sharedpred=pd.read_parquet(shared_source/'predictions.parquet');sharedw=pd.read_parquet(shared_source/'weights.parquet')
    parts=[sharedpred[sharedpred.model.isin(['polling','prior'])]];ws=[]
    for family,pp,ww in [('shared',sharedpred,sharedw),('state',statepred,sw)]:
        pp=pp[~pp.model.isin(['polling','prior'])].copy();pp['model']=family+'__'+pp.model;parts.append(pp)
        ww=ww.copy();ww['model']=family+'__'+ww.model;ws.append(ww)
    # Hold the shared model's selected final a/b fixed when replacing only S.
    for r in sharedw[sharedw.model.eq('learned')].itertuples():
        q=state[(state.scenario==r.scenario)&(state.cycle==r.cycle)].copy()
        q['prediction'],q['baseline_before_surprise'],delta=combine(q.bias_prediction,q.prior,q.predicted_surprise,q.n_samples,r.prior_share,r.surprise_strength)
        q['model']='state__shared_weights';q['prior_pull_pp']=100*(q.baseline_before_surprise-q.bias_prediction);q['added_surprise_pp']=100*delta;parts.append(q)
        ws.append(pd.DataFrame([dict(scenario=r.scenario,cycle=r.cycle,model='state__shared_weights',prior_share=r.prior_share,surprise_strength=r.surprise_strength,selection_cycles=r.selection_cycles,validation_mae_pp=np.nan)]))
    pred=pd.concat(parts,ignore_index=True).drop(columns=['history_selection_10pp'],errors='ignore')
    membership=sharedpred[sharedpred.model.eq('polling')][['scenario','target_id','history_selection_10pp']]
    pred=pred.merge(membership,on=['scenario','target_id'],validate='many_to_one')
    ledger=pd.read_parquet(shared_source/'full_seat_ledger.parquet');ledgers=[];totals=[];groups=[]
    for (scenario,year,model),q in pred.groupby(['scenario','cycle','model']):
        r=ledger[ledger.scenario.eq(scenario)&ledger.cycle.eq(year)&ledger.model.eq('polling')]
        l,t=review_forecasts(r[['state','seat_class','seat_id','target_id','contested','special','caucus','actual_caucus']],q,int(year),scenario,model);ledgers.append(l);totals.append(t)
    for (scenario,model),q in pred[pred.cycle.between(2016,2024)].groupby(['scenario','model']):
        for group,g in [('all',q),('competitive',q[q.history_selection_10pp.eq('competitive')]),('polled',q[q.n_samples.gt(0)]),('no_polls',q[q.n_samples.eq(0)])]:
            if len(g):groups.append(dict(scenario=scenario,model=model,group=group,n=len(g),correct=int(((g.prediction>0)==(g.actual>0)).sum()),mae_pp=100*(g.prediction-g.actual).abs().groupby(g.cycle).mean().mean()))
    components=pd.concat([shared.assign(family='shared'),state.assign(family='state')],ignore_index=True)
    frames=dict(predictions=pred,components=components,weights=pd.concat(ws,ignore_index=True),state_weight_tuning=sg,state_penalty_tuning=pd.DataFrame(tuning),coefficients=pd.concat(coefs,ignore_index=True),groups=pd.DataFrame(groups),seat_totals=pd.concat(totals,ignore_index=True),full_seat_ledger=pd.concat(ledgers,ignore_index=True))
    assert pred.loc[pred.n_samples.eq(0),'predicted_surprise'].isna().all()
    assert np.allclose(pred.loc[pred.n_samples.eq(0),'prediction'],pred.loc[pred.n_samples.eq(0),'prior'])
    out=shared_source.parent.parent/'state_surprise'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True)
    for name,df in frames.items():df.to_parquet(out/(name+'.parquet'),index=False)
    (out/'fits.json').write_text(json.dumps(fits,indent=2,allow_nan=False)+'\n')
    (out/'settings.json').write_text(json.dumps(dict(shared_source=str(shared_source),shared_manifest_sha256=hashlib.sha256((shared_source/'manifest.json').read_bytes()).hexdigest(),
        comparison='shared vs state economic/approval surprise coefficients; both intercept-free; no state-specific fusion weights',
        penalties=[.1,1,10,100,'infinite_shared_limit'],selection='alpha/statepenalty onY-2; a/b last2-3prequential polled cycles; shared-weight-locked control',
        no_poll='S unavailable; existing prior retained',promotion=False),indent=2)+'\n')
    (out/'state_surprise_comparison.py').write_bytes(Path(__file__).read_bytes());refresh(out);return out,frames

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--shared-source',type=Path,required=True);a=p.parse_args()
    out,_=build(Path(__file__).resolve().parents[1],a.shared_source);print('Saved:',out)
