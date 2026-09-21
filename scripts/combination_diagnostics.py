"""Chronological intercept controls and constrained polling/fundamentals blends."""
import numpy as np
import pandas as pd
from momentum_approval_models import prepare_subset,predict_subset
from score_baselines import ALPHAS
from poll_error_baselines import correction_folds

PROFILES=['free','zero','shrunk']
INTERCEPT_PENALTY_RATIO=10.
BLEND_WEIGHTS=[0.,.25,.5,.75,1.]
MODELS=['prior','polling','bias','constant','original_both','zero_intercept','shrunk_intercept',
        'zero_matched_alpha','shrunk_matched_alpha','fundamentals','fundamental_fallback','blend_half','blend_90','blend_selected']
MAIN=['polling','bias','original_both','zero_intercept','shrunk_intercept','fundamentals','blend_half','blend_90','blend_selected']
LABELS=dict(zip(MODELS,['Prior','Polling','Bias only','Bias + constant','Original extra factors','Zero extra intercept',
    'Shrunk extra intercept','Zero, original alpha','Shrunk, original alpha','Fundamentals only',
    'Bias + fundamentals fallback','50/50 blend','90/10 blend','Past-selected blend']))


def solve_intercept(problem,alpha,profile):
    if profile not in PROFILES or not np.isfinite(alpha) or alpha<=0:raise ValueError('Invalid intercept/penalty')
    p=problem;z=p['z'];v=p['future'];w=p['weights'];terms=p['design'].active
    if profile=='zero':
        z=z[:,1:];v=v[:,1:];penalty=np.full(len(terms),alpha)
    else:penalty=np.r_[0. if profile=='free' else INTERCEPT_PENALTY_RATIO*w.sum(),np.full(len(terms),alpha)]
    gram=z.T@(w[:,None]*z);normal=gram+np.diag(penalty)
    coef=np.linalg.solve(normal,z.T@(w*p['response'])) if z.shape[1] else np.empty(0)
    delta=v@coef;raw=p['offset']+delta;prediction=np.clip(raw,-1,1)
    beta=np.r_[0.,coef] if profile=='zero' else coef
    df=float(np.trace(np.linalg.solve(normal,gram))) if len(coef) else 0.
    info=dict(profile=profile,alpha=float(alpha),intercept_penalty=float(INTERCEPT_PENALTY_RATIO*w.sum()) if profile=='shrunk' else (None if profile=='zero' else 0.),
        weight_mass=float(w.sum()),standardized_coefficients=dict(zip(['intercept']+terms,map(float,beta))),
        effective_df=df,nominal_parameters=len(terms)+(profile!='zero'),training_cycles=int(p['train'].cycle.nunique()),training_rows=len(p['train']),
        training_max_cycle=int(p['train'].cycle.max()),training_mean_residual_pp=float(100*np.average(p['response'],weights=w)),
        extra_adjustment_pp=float(100*delta[0]),clipped_predictions=int(np.sum(np.abs(raw)>1)),
        cycle_weights={str(int(k)):float(value) for k,value in p['cycle_weights'].items()},
        **p['design'].metadata(),training_scores=p['scores'][['cycle']+terms].replace({np.nan:None}).to_dict('records'),
        test_scores=p['test_scores'][['cycle']+terms].replace({np.nan:None}).to_dict('records'))
    return prediction,info


def blend(c,f,n_samples,weight):
    if not np.isfinite(weight) or not 0<=weight<=1:raise ValueError('Convex weight in [0,1] required')
    c,f,n=map(np.asarray,[c,f,n_samples])
    if c.shape!=f.shape or c.shape!=n.shape or not np.isfinite(c).all() or not np.isfinite(f).all():raise ValueError('Finite aligned constituents required')
    actual_weight=np.where(n>0,weight,0.)
    return actual_weight*c+(1-actual_weight)*f


def select_weight(validation):
    q=validation[validation.n_samples.gt(0)]
    if q.empty or q.actual.isna().any() or q.cycle.nunique()!=1:raise ValueError('One known polled validation cycle required')
    candidates=[]
    for w in BLEND_WEIGHTS:
        pred=blend(q.bias_prediction,q.fundamentals,q.n_samples,w)
        candidates.append(dict(polling_weight=w,validation_mae_pp=float(100*np.abs(pred-q.actual).mean())))
    best=min(candidates,key=lambda r:(round(r['validation_mae_pp']/100,12),-r['polling_weight']))
    return best,candidates


def fit_fundamentals(source,cal,year,minimum=6):
    train=source[source.cycle.lt(year)&source.actual.notna()];test=source[source.cycle.eq(year)]
    inner=train[train.cycle.lt(year-2)];valid=train[train.cycle.eq(year-2)]
    if inner.cycle.nunique()<minimum or valid.empty:raise ValueError('Insufficient fundamentals history')
    ip=prepare_subset(inner,valid,cal,'prior','both');p=prepare_subset(train,test,cal,'prior','both')
    candidates=[]
    for a in ALPHAS:
        pred,_=predict_subset(ip,a);candidates.append((float(np.abs(pred-valid.actual).mean()),a))
    loss,alpha=min(candidates,key=lambda x:(round(x[0],12),-x[1]))
    pred,fit=predict_subset(p,alpha,True)
    fit.update(cycle=int(year),scenario=source.scenario.iloc[0],model='fundamentals',validation_cycle=int(year-2),validation_mae_pp=100*loss)
    grid=[dict(scenario=fit['scenario'],cycle=int(year),model='fundamentals',alpha=a,validation_cycle=int(year-2),validation_mae_pp=100*l) for l,a in candidates]
    return test.assign(fundamentals=pred),fit,grid


def evaluate(history,calendars,start_cycle=2006,minimum=6,progress=None):
    parts=[];fits=[];grids=[];folds=[];fundparts=[];selections=[]
    for scenario,source in history.groupby('scenario'):
        source=source.copy();cal=calendars[calendars.scenario.eq(scenario)]
        fold=correction_folds(source,source,scenario,start_cycle,minimum);folds.append(fold)
        eligible=fold[fold.status.isin(['cv_scored','forecast_only_no_outcomes'])]
        # Reconstruct the previous cycle's FUNDAMENTALS forecast before selecting a blend.
        # Its training uses all earlier result cycles, not only years with polls.
        needed=sorted(set(eligible.cycle.astype(int))|set(eligible.cycle.astype(int)-2))
        funds={}
        for year in needed:
            funds[year],fit,grid=fit_fundamentals(source,cal,year,minimum);fits.append(fit);grids.extend(grid)
            fundparts.append(funds[year][['scenario','cycle','target_id','fundamentals']])
        for row in eligible.itertuples():
            year=int(row.cycle)
            if progress:progress(f'{scenario} {year}: intercept controls and convex blend')
            test=funds[year];past=source[source.cycle.lt(year)&source.actual.notna()&source.n_samples.gt(0)]
            inner=past[past.cycle.lt(year-2)];valid=past[past.cycle.eq(year-2)]
            apply=test[test.n_samples.gt(0)];fit_test=apply if len(apply) else test.iloc[:1]
            ip=prepare_subset(inner,valid,cal,'bias','both');fp=prepare_subset(past,fit_test,cal,'bias','both')
            common=test[['target_id','cycle','kind','geography','actual','n_samples','n_firms','prior','poll_baseline','bias_prediction','fundamentals','scenario']].copy()
            common['status']=row.status
            def add(model,values,**metadata):parts.append(common.assign(model=model,prediction=np.asarray(values),**metadata))
            for model,col in [('prior','prior'),('polling','poll_baseline'),('bias','bias_prediction'),('fundamentals','fundamentals')]:add(model,test[col])
            selected={}
            for profile in PROFILES:
                choices=[];model={'free':'original_both','zero':'zero_intercept','shrunk':'shrunk_intercept'}[profile]
                for alpha in ALPHAS:
                    vp,_=solve_intercept(ip,alpha,profile);loss=float(np.abs(vp-valid.actual.to_numpy()).mean())
                    choices.append((loss,alpha));grids.append(dict(scenario=scenario,cycle=year,model=model,profile=profile,alpha=alpha,validation_cycle=year-2,validation_mae_pp=100*loss))
                loss,alpha=min(choices,key=lambda x:(round(x[0],12),-x[1]));selected[profile]=alpha
                pp,f=solve_intercept(fp,alpha,profile);values=test.bias_prediction.to_numpy(copy=True)
                values[test.n_samples.gt(0).to_numpy()]=pp if len(apply) else np.empty(0)
                f.update(model=model,scenario=scenario,cycle=year,validation_cycle=year-2,validation_mae_pp=100*loss,matched_alpha=False)
                fits.append(f);add(model,values)
            # Hold original alpha fixed to distinguish intercept change from retuning.
            for profile in ['zero','shrunk']:
                model=profile+'_matched_alpha';pp,f=solve_intercept(fp,selected['free'],profile)
                values=test.bias_prediction.to_numpy(copy=True);values[test.n_samples.gt(0).to_numpy()]=pp if len(apply) else np.empty(0)
                f.update(model=model,scenario=scenario,cycle=year,validation_cycle=year-2,matched_alpha=True)
                fits.append(f);add(model,values)
            constant=float(np.average(fp['response'],weights=fp['weights']))
            add('constant',np.where(test.n_samples.gt(0),np.clip(test.bias_prediction+constant,-1,1),test.bias_prediction))
            best,grid=select_weight(funds[year-2])
            for entry in grid:selections.append(dict(scenario=scenario,cycle=year,validation_cycle=year-2,selected=entry['polling_weight']==best['polling_weight'],**entry))
            for model,w in [('fundamental_fallback',1.),('blend_half',.5),('blend_90',.9),('blend_selected',best['polling_weight'])]:
                add(model,blend(test.bias_prediction,test.fundamentals,test.n_samples,w),polling_weight=np.where(test.n_samples.gt(0),w,0.),nominal_polling_weight=w)
    return dict(predictions=pd.concat(parts,ignore_index=True),folds=pd.concat(folds,ignore_index=True),
        tuning=pd.DataFrame(grids),blend_selection=pd.DataFrame(selections),fundamental_history=pd.concat(fundparts,ignore_index=True)),fits
