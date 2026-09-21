"""Predict remaining polling surprise, then combine polling/prior and that delta."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
import pandas as pd
from momentum_approval_models import prepare_subset
from combination_diagnostics import solve_intercept
from score_baselines import ALPHAS
from run_combination_diagnostics import audit_problem,refresh
from senate_seat_review import review_forecasts

MAIN=['polling','prior','polling_plus_surprise','fixed50','fixed90','learned']
LABELS=dict(zip(MAIN,['Corrected polling','Historical prior','Polling + full surprise','50/25/25 interpretation','90/5/5 interpretation','Learned baseline + surprise']))
GRID=[(a/20,b/20) for a in range(21) for b in range(21)]


def recipe(triple):
    w=np.asarray(triple,float)
    if w.shape!=(3,) or not np.isfinite(w).all() or (w<0).any() or not np.isclose(w.sum(),1) or w[:2].sum()<=0:
        raise ValueError('Nonnegative triple summing to1 and a nonzero baseline required')
    return float(w[1]/w[:2].sum()),float(w[2])


def combine(c,p,s,n_samples,prior_share,surprise_strength):
    c,p,s,n=map(np.asarray,[c,p,s,n_samples])
    if not(c.shape==p.shape==s.shape==n.shape) or not np.isfinite(c).all() or not np.isfinite(p).all():raise ValueError('Finite aligned baseline inputs required')
    if not all(np.isfinite(v) and 0<=v<=1 for v in [prior_share,surprise_strength]):raise ValueError('Weights in [0,1] required')
    if not np.isfinite(s[n>0]).all():raise ValueError('A surprise forecast is required for polled targets')
    baseline=(1-prior_share)*c+prior_share*p
    delta=np.where(n>0,s,0.)*surprise_strength
    return np.clip(baseline+delta,-1,1),baseline,delta


def fit_surprise(source,cal,year):
    train=source[source.cycle.lt(year)&source.actual.notna()&source.n_samples.gt(0)]
    test=source[source.cycle.eq(year)];apply=test[test.n_samples.gt(0)]
    inner=train[train.cycle.lt(year-2)];valid=train[train.cycle.eq(year-2)]
    if inner.cycle.nunique()<6 or valid.empty:raise ValueError('Six earlier polled cycles plus validation required')
    ip=prepare_subset(inner,valid,cal,'bias','both');fp=prepare_subset(train,apply if len(apply) else test.iloc[:1],cal,'bias','both')
    assert np.array_equal(fp['response'],train.actual.to_numpy()-train.bias_prediction.to_numpy())
    choices=[]
    for a in ALPHAS:
        pp,_=solve_intercept(ip,a,'zero');loss=float(100*np.abs(pp-valid.actual.to_numpy()).mean())
        expected,_=audit_problem(ip,a,'zero');assert np.allclose(expected,pp,atol=1e-11)
        choices.append(dict(alpha=a,validation_mae_pp=loss,cycle=year,scenario=source.scenario.iloc[0],validation_cycle=year-2,training_max_cycle=int(inner.cycle.max())))
    best=min(choices,key=lambda r:(round(r['validation_mae_pp'],10),-r['alpha']))
    pred,fit=solve_intercept(fp,best['alpha'],'zero');expected,coef=audit_problem(fp,best['alpha'],'zero')
    assert np.allclose(expected,pred,atol=1e-11)
    beta=np.array(list(fit['standardized_coefficients'].values()));raw_s=fp['future']@beta
    assert np.allclose(beta,coef,atol=1e-11) and beta[0]==0
    q=test.copy();q['predicted_surprise']=np.nan;q.loc[apply.index,'predicted_surprise']=raw_s if len(apply) else np.empty(0)
    q['actual_surprise']=np.where(q.n_samples.gt(0)&q.actual.notna(),q.actual-q.bias_prediction,np.nan)
    q['surprise_status']=np.where(q.n_samples.gt(0),'predicted','unavailable_no_polls')
    q['momentum_contribution']=np.nan;q['approval_contribution']=np.nan
    for name,column in [('economy_momentum_wh','momentum_contribution'),('approval_wh','approval_contribution')]:
        if name in fit['active_terms']:
            j=list(fit['standardized_coefficients']).index(name);q.loc[apply.index,column]=fp['future'][:,j]*beta[j] if len(apply) else np.empty(0)
        else:q.loc[apply.index,column]=0.
    assert np.allclose(q.loc[apply.index,'predicted_surprise'],q.loc[apply.index,['momentum_contribution','approval_contribution']].sum(axis=1))
    fit.update(cycle=int(year),scenario=source.scenario.iloc[0],validation_cycle=int(year-2),validation_mae_pp=best['validation_mae_pp'],target='actual minus historical corrected-polling margin; polled rows only')
    return q,fit,choices


def select(history,year):
    p=history[history.cycle.lt(year)&history.actual.notna()&history.n_samples.gt(0)]
    years=sorted(p.cycle.unique())[-3:]
    if len(years)<2:return None,[],years
    p=p[p.cycle.isin(years)];rows=[]
    for a,b in GRID:
        pred,_,_=combine(p.bias_prediction,p.prior,p.predicted_surprise,p.n_samples,a,b)
        loss=pd.Series(np.abs(pred-p.actual.to_numpy()),index=p.index).groupby(p.cycle).mean().mean()
        rows.append(dict(prior_share=a,surprise_strength=b,validation_mae_pp=100*float(loss)))
    best=min(rows,key=lambda r:(round(r['validation_mae_pp'],10),r['prior_share'],r['surprise_strength']))
    for r in rows:r['selected']=r is best
    return best,rows,years


def assemble(history):
    preds=[];weights=[];grids=[]
    for scenario,source in history.groupby('scenario'):
        for year,q in source.groupby('cycle'):
            rules={'polling':(0.,0.),'prior':(1.,0.),'polling_plus_surprise':(0.,1.),'fixed50':recipe([.5,.25,.25]),'fixed90':recipe([.9,.05,.05])}
            best,grid,years=select(source,year)
            if best:rules['learned']=(best['prior_share'],best['surprise_strength'])
            for r in grid:grids.append(dict(scenario=scenario,cycle=int(year),selection_cycles=','.join(map(str,years)),**r))
            for model,(a,b) in list(rules.items()):
                if model in ['fixed50','fixed90','learned']:rules[model+'_no_surprise']=(a,0.)
            for model,(a,b) in rules.items():
                pred,baseline,delta=combine(q.bias_prediction,q.prior,q.predicted_surprise,q.n_samples,a,b)
                rows=q.copy();rows['model']=model;rows['prediction']=pred;rows['baseline_before_surprise']=baseline
                rows['prior_pull_pp']=100*(baseline-q.bias_prediction);rows['added_surprise_pp']=100*delta
                rows['clip_change_pp']=100*(pred-baseline-delta);preds.append(rows)
                weights.append(dict(scenario=scenario,cycle=int(year),model=model,prior_share=a,surprise_strength=b,
                    selection_cycles=','.join(map(str,years)) if model.startswith('learned') else '',validation_mae_pp=best['validation_mae_pp'] if model.startswith('learned') else np.nan))
    return pd.concat(preds,ignore_index=True),pd.DataFrame(weights),pd.DataFrame(grids)


def build(lab,source):
    lab,source=Path(lab).resolve(),Path(source).resolve()
    manifest=json.loads((source/'manifest.json').read_text());assert all(hashlib.sha256((source/k).read_bytes()).hexdigest()==v for k,v in manifest.items())
    settings=json.loads((source/'settings.json').read_text());assert all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in settings['sources'].values())
    h=pd.read_parquet(settings['sources']['history']['path']);h=h[h.base.eq('fixed5_8')]
    cal=pd.read_parquet(settings['sources']['calendars']['path']);old=pd.read_parquet(source/'predictions.parquet')
    components=[];fits=[];penalties=[]
    for scenario,s in h.groupby('scenario'):
        for year in sorted(old.loc[old.scenario.eq(scenario),'cycle'].unique()):
            q,f,grid=fit_surprise(s,cal[cal.scenario.eq(scenario)],int(year));components.append(q);fits.append(f);penalties+=grid
    components=pd.concat(components,ignore_index=True);pred,w,grid=assemble(components)
    for model,old_model in [('polling','bias'),('prior','prior'),('polling_plus_surprise','zero_intercept')]:
        a=pred[pred.model.eq(model)].merge(old[old.model.eq(old_model)],on=['scenario','target_id'],suffixes=('_a','_b'),validate='one_to_one')
        assert len(a)==len(components) and np.allclose(a.prediction_a,a.prediction_b,atol=1e-11)
    membership=pd.read_parquet(source/'state_calls.parquet').query("model=='bias'")[['scenario','target_id','history_selection_10pp']]
    pred=pred.merge(membership,on=['scenario','target_id'],validate='many_to_one')
    ledger=pd.read_parquet(source/'full_seat_ledger.parquet');ledgers=[];totals=[]
    for (scenario,year,model),q in pred.groupby(['scenario','cycle','model']):
        r=ledger[ledger.scenario.eq(scenario)&ledger.cycle.eq(year)&ledger.model.eq('bias')]
        l,t=review_forecasts(r[['state','seat_class','seat_id','target_id','contested','special','caucus','actual_caucus']],q,int(year),scenario,model)
        ledgers.append(l);totals.append(t)
    groups=[]
    for (scenario,model),q in pred[pred.cycle.between(2016,2024)].groupby(['scenario','model']):
        for group,g in [('all',q),('competitive',q[q.history_selection_10pp.eq('competitive')]),('polled',q[q.n_samples.gt(0)]),('no_polls',q[q.n_samples.eq(0)])]:
            if len(g):groups.append(dict(scenario=scenario,model=model,group=group,n=len(g),correct=int(((g.prediction>0)==(g.actual>0)).sum()),mae_pp=100*(g.prediction-g.actual).abs().groupby(g.cycle).mean().mean()))
    surprise_metrics=[]
    for (scenario,year),q in components[components.actual_surprise.notna()].groupby(['scenario','cycle']):
        surprise_metrics.append(dict(scenario=scenario,cycle=int(year),n=len(q),actual_mean_pp=100*q.actual_surprise.mean(),predicted_mean_pp=100*q.predicted_surprise.mean(),zero_surprise_mae_pp=100*q.actual_surprise.abs().mean(),surprise_mae_pp=100*(q.actual_surprise-q.predicted_surprise).abs().mean()))
    frames=dict(components=components,predictions=pred,weights=w,weight_tuning=grid,surprise_tuning=pd.DataFrame(penalties),groups=pd.DataFrame(groups),surprise_metrics=pd.DataFrame(surprise_metrics),seat_totals=pd.concat(totals,ignore_index=True),full_seat_ledger=pd.concat(ledgers,ignore_index=True))
    out=source.parent.parent/'surprise_fusion'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True)
    for name,df in frames.items():df.to_parquet(out/(name+'.parquet'),index=False)
    (out/'fits.json').write_text(json.dumps(fits,indent=2,allow_nan=False)+'\n')
    (out/'settings.json').write_text(json.dumps(dict(source=str(source),source_manifest_sha256=hashlib.sha256((source/'manifest.json').read_bytes()).hexdigest(),
        target='actual - historical corrected polling, on polled rows only',formula='clip((1-prior_share)*C + prior_share*P + surprise_strength*S)',
        fixed50={'prior_share':1/3,'surprise_strength':.25},fixed90={'prior_share':1/19,'surprise_strength':.05},
        shared_surprise='momentum + approval; zero extra intercept, no state offsets;8yrhistory decay, train-only transforms;Y-2ridge tuning',
        no_poll='surprise and surprise label missing; applied adjustment zero; retain prior',
        learning='441 prior-share/surprise-strength pairs,5ppsteps, minimum2/last3past prequential cycles; equal-cycle polledMAE; ties prefer less prior then less surprise',
        promotion=False),indent=2)+'\n')
    (out/'surprise_fusion.py').write_bytes(Path(__file__).read_bytes());refresh(out);return out,frames

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);a=p.parse_args()
    out,_=build(Path(__file__).resolve().parents[1],a.source);print('Saved:',out)
