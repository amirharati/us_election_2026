"""Three complete margin forecasts and chronological convex combinations."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
import numpy as np
import pandas as pd
from recency_state_baselines import prepare_problem,predict_problem
from score_baselines import ALPHAS
from state_score_baselines import STATE_PENALTIES
from senate_seat_review import review_forecasts
from run_combination_diagnostics import refresh

FEATURES=['economy_momentum_wh','approval_wh']
MODELS=['polling','prior','features','fixed_50_25_25','fixed_90_5_5','learned']
LABELS=dict(zip(MODELS,['M1: corrected polling','M2: historical prior','M3: feature-only regression','Combined 50/25/25','Combined 90/5/5','Combined learned weights']))
GRID=np.array([(a,b,20-a-b) for a in range(21) for b in range(21-a)],float)/20


def prepare_direct(train,test,calendars):
    p=prepare_problem(train,test,calendars,'direct',8.)
    d=p['design'];indices=[0]+[i+1 for i,c in enumerate(d.active) if c in FEATURES]
    p['z']=p['z'][:,indices];p['future']=p['future'][:,indices]
    d.active=[c for c in d.active if c in FEATURES]
    for key in ['fills','centers','scales','dropped']:
        setattr(d,key,{c:v for c,v in getattr(d,key).items() if c in FEATURES})
    return p


def independent_prediction(p,alpha,penalty):
    """Full augmented weighted LS, independent of the block-elimination solver."""
    z=p['z'];states=sorted(p['train'].geography.unique());k=z.shape[1]
    x=np.zeros((len(z),k*(1+len(states))));x[:,:k]=z
    future=np.zeros((len(p['test']),x.shape[1]));future[:,:k]=p['future']
    for j,s in enumerate(states,1):
        use=p['train'].geography.eq(s).to_numpy();x[use,j*k:(j+1)*k]=z[use]
        use=p['test'].geography.eq(s).to_numpy();future[use,j*k:(j+1)*k]=p['future'][use]
    penalties=np.r_[0.,np.full(k-1,alpha),np.full(k*len(states),penalty)]
    a=np.vstack([np.sqrt(p['weights'])[:,None]*x,np.diag(np.sqrt(penalties))])
    b=np.r_[np.sqrt(p['weights'])*p['response'],np.zeros(x.shape[1])]
    beta=np.linalg.lstsq(a,b,rcond=None)[0]
    return np.clip(future@beta,-1,1)


def fit_direct(source,cal,year,audit=False):
    train=source[source.cycle.lt(year)&source.actual.notna()];test=source[source.cycle.eq(year)]
    inner=train[train.cycle.lt(year-2)];valid=train[train.cycle.eq(year-2)]
    if inner.cycle.nunique()<6 or valid.empty:raise ValueError('Insufficient previous-cycle direct-model training')
    ip=prepare_direct(inner,valid,cal);fp=prepare_direct(train,test,cal);choices=[]
    for a in ALPHAS:
        for penalty in STATE_PENALTIES:
            pp,_,_=predict_problem(ip,a,penalty)
            choices.append(dict(alpha=a,state_penalty=penalty,validation_mae_pp=float(100*np.abs(pp-valid.actual).mean())))
    best=min(choices,key=lambda r:(round(r['validation_mae_pp'],10),-r['state_penalty'],-r['alpha']))
    pred,fit,coef=predict_problem(fp,best['alpha'],best['state_penalty'],True)
    fit.update(scenario=source.scenario.iloc[0],cycle=int(year),validation_cycle=int(year-2),validation_mae_pp=best['validation_mae_pp'])
    if audit:
        expected=independent_prediction(fp,best['alpha'],best['state_penalty'])
        assert np.allclose(pred,expected,atol=1e-10)
        fit['independent_max_difference']=float(np.max(np.abs(pred-expected)))
        expected=independent_prediction(ip,best['alpha'],best['state_penalty'])
        assert np.isclose(100*np.abs(expected-valid.actual.to_numpy()).mean(),best['validation_mae_pp'])
    for r in choices:r.update(scenario=fit['scenario'],cycle=int(year),validation_cycle=int(year-2),training_max_cycle=int(inner.cycle.max()))
    coef['scenario']=fit['scenario'];coef['cycle']=year
    return test.assign(features=pred),fit,choices,coef


def combine(x,weights):
    x,w=np.asarray(x,float),np.asarray(weights,float)
    if x.ndim!=2 or x.shape[1]!=3 or w.shape!=(3,) or not np.isfinite(x).all() or not np.isfinite(w).all() or (w<0).any() or not np.isclose(w.sum(),1):
        raise ValueError('Three finite forecasts and nonnegative weights summing to one required')
    return x@w


def select_weights(history,target_cycle):
    """Last three completed prequential cycles, minimum two; equal cycle MAE."""
    past=history[history.cycle.lt(target_cycle)&history.actual.notna()]
    years=sorted(past.cycle.unique())[-3:]
    if len(years)<2:return None,[],years
    p=past[past.cycle.isin(years)]
    if p.duplicated(['cycle','target_id']).any():raise ValueError('Duplicate validation targets')
    rows=[]
    for w in GRID:
        error=np.abs(combine(p[['bias_prediction','prior','features']],w)-p.actual.to_numpy())
        loss=pd.Series(error,index=p.index).groupby(p.cycle).mean().mean()
        rows.append(dict(w_poll=float(w[0]),w_prior=float(w[1]),w_features=float(w[2]),validation_mae_pp=float(100*loss)))
    best=min(rows,key=lambda r:(round(r['validation_mae_pp'],10),-r['w_poll'],-r['w_prior']))
    for r in rows:r['selected']=r is best
    return best,rows,years


def assemble(components):
    parts=[];choices=[];weights=[];effects=[]
    for scenario,source in components.groupby('scenario'):
        for year,g in source.groupby('cycle'):
            x=g[['bias_prediction','prior','features']].to_numpy();common=g.copy()
            rules={'polling':(1.,0.,0.),'prior':(0.,1.,0.),'features':(0.,0.,1.),'fixed_50_25_25':(.5,.25,.25),'fixed_90_5_5':(.9,.05,.05)}
            best,grid,years=select_weights(source,year)
            for r in grid:choices.append(dict(scenario=scenario,cycle=int(year),validation_cycles=','.join(map(str,years)),**r))
            if best is not None:rules['learned']=(best['w_poll'],best['w_prior'],best['w_features'])
            for model,w in rules.items():
                pp=combine(x,w);parts.append(common.assign(model=model,prediction=pp))
                weights.append(dict(scenario=scenario,cycle=int(year),model=model,w_poll=w[0],w_prior=w[1],w_features=w[2],
                    selection_cycles=','.join(map(str,years)) if model=='learned' else '',validation_mae_pp=best['validation_mae_pp'] if model=='learned' else np.nan))
                if model in ['fixed_50_25_25','fixed_90_5_5','learned']:
                    for j,component in enumerate(['polling','prior','features']):
                        remainder=1-w[j]
                        if remainder<1e-12:
                            effects.append(dict(scenario=scenario,cycle=int(year),model=model,removed=component,target_id=None,status='undefined_only_active_component'));continue
                        ablated=np.array(w);ablated[j]=0;ablated/=remainder;without=combine(x,ablated)
                        for i,r in enumerate(g.itertuples()):
                            known=pd.notna(r.actual)
                            effects.append(dict(scenario=scenario,cycle=int(year),model=model,removed=component,target_id=r.target_id,
                                status='scored' if known else 'pending',component_weight=w[j],prediction=pp[i],without_prediction=without[i],actual=r.actual,
                                benefit_mae_pp=100*(abs(without[i]-r.actual)-abs(pp[i]-r.actual)) if known else np.nan,
                                call_benefit=int((pp[i]>0)==(r.actual>0))-int((without[i]>0)==(r.actual>0)) if known else np.nan))
    return pd.concat(parts,ignore_index=True),pd.DataFrame(weights),pd.DataFrame(choices),pd.DataFrame(effects)


def build(lab,source,progress=print):
    lab,source=Path(lab).resolve(),Path(source).resolve()
    manifest=json.loads((source/'manifest.json').read_text())
    assert all(hashlib.sha256((source/k).read_bytes()).hexdigest()==v for k,v in manifest.items())
    settings=json.loads((source/'settings.json').read_text())
    assert all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in settings['sources'].values())
    h=pd.read_parquet(settings['sources']['history']['path']);h=h[h.base.eq('fixed5_8')]
    cal=pd.read_parquet(settings['sources']['calendars']['path']);old=pd.read_parquet(source/'predictions.parquet')
    comps=[];fits=[];grids=[];coefficients=[]
    for scenario,s in h.groupby('scenario'):
        for year in sorted(old.loc[old.scenario.eq(scenario),'cycle'].unique()):
            if progress:progress(f'{scenario} {year}: direct two-feature outcome regression',flush=True)
            q,f,grid,coef=fit_direct(s,cal[cal.scenario.eq(scenario)],int(year),True)
            comps.append(q);fits.append(f);grids.extend(grid);coefficients.append(coef)
    components=pd.concat(comps,ignore_index=True)
    pred,weights,tuning,effects=assemble(components)
    for model,previous in [('polling','bias'),('prior','prior')]:
        p=pred[pred.model.eq(model)].merge(old[old.model.eq(previous)],on=['scenario','target_id'],suffixes=('_new','_old'),validate='one_to_one')
        assert np.array_equal(p.prediction_new,p.prediction_old)
    membership=pd.read_parquet(source/'state_calls.parquet').query("model=='bias'")[['scenario','target_id','history_selection_10pp']]
    pred=pred.merge(membership,on=['scenario','target_id'],validate='many_to_one')
    ledgers=[];totals=[];ledger=pd.read_parquet(source/'full_seat_ledger.parquet')
    for (scenario,year,model),g in pred.groupby(['scenario','cycle','model']):
        r=ledger[ledger.scenario.eq(scenario)&ledger.cycle.eq(year)&ledger.model.eq('bias')]
        l,t=review_forecasts(r[['state','seat_class','seat_id','target_id','contested','special','caucus','actual_caucus']],g,int(year),scenario,model)
        ledgers.append(l);totals.append(t)
    groups=[]
    for (scenario,model),g in pred[pred.cycle.between(2016,2024)].groupby(['scenario','model']):
        for group,q in [('all',g),('competitive',g[g.history_selection_10pp.eq('competitive')]),('polled',g[g.n_samples.gt(0)]),('no_polls',g[g.n_samples.eq(0)])]:
            if len(q):groups.append(dict(scenario=scenario,model=model,group=group,n=len(q),correct=int(((q.prediction>0)==(q.actual>0)).sum()),mae_pp=100*(q.prediction-q.actual).abs().groupby(q.cycle).mean().mean()))
    frames=dict(predictions=pred,components=components,weights=weights,weight_tuning=tuning,feature_tuning=pd.DataFrame(grids),
        coefficients=pd.concat(coefficients,ignore_index=True),ablation=effects,groups=pd.DataFrame(groups),seat_totals=pd.concat(totals,ignore_index=True),full_seat_ledger=pd.concat(ledgers,ignore_index=True))
    out=source.parent.parent/'three_models'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True)
    for name,frame in frames.items():frame.to_parquet(out/(name+'.parquet'),index=False)
    (out/'fits.json').write_text(json.dumps(fits,indent=2,allow_nan=False)+'\n')
    (out/'settings.json').write_text(json.dumps(dict(source=str(source),source_manifest_sha256=hashlib.sha256((source/'manifest.json').read_bytes()).hexdigest(),
        formula='w_poll*M1 + w_prior*M2 + w_features*M3; all are full D-R margins; weights sum to 1',
        features='Direct outcome regression, momentum+approval only, state coefficients shrunk to shared; no prior/poll offset; 8yrdecay; alpha/statepenalty tuned onY-2',
        learned='5-percentage-point simplex grid (231 rules), minimum2/last3 previous prequential cycles, equal-cycle MAE, ties favor polling then prior',
        no_poll='M1 retains existing prior fallback; M3 applies regardless of poll availability; combinations are literal weighted margins',
        ablation='remove one block and renormalize other weights without retuning; undefined when removed block has all weight',
        earliest_learned=2016,promotion=False),indent=2)+'\n')
    for filename in ['three_model_comparison.py','recency_state_baselines.py','state_score_baselines.py']:(out/filename).write_bytes((lab/'scripts'/filename).read_bytes())
    refresh(out);return out,frames

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);a=p.parse_args()
    out,_=build(Path(__file__).resolve().parents[1],a.source);print('Saved:',out)
