"""Small chronological shared corrections: momentum, approval, or both.

Compare a prior, raw polling baseline and prequential state-bias polling.
Keep history decay fixed; choose penalties/optional feature subset on Y-2 only.
"""
import numpy as np
import pandas as pd
from recency_state_baselines import prepare_problem
from score_baselines import ALPHAS
from poll_error_baselines import correction_folds

FEATURES={'constant':[], 'momentum':['economy_momentum_wh'],
          'approval':['approval_wh'], 'both':['economy_momentum_wh','approval_wh']}
BASES=['prior','polling','bias']
HALF_LIFE=8.
PREFERENCE={'none':0,'constant':1,'momentum':2,'approval':3,'both':4}


def prepare_subset(train,test,calendars,base,feature_set):
    if base not in BASES or feature_set not in FEATURES:raise ValueError('Unknown base/features')
    if base!='prior' and not train.n_samples.gt(0).all():raise ValueError('Polling correction trains only polled outcomes')
    if base=='bias':
        for frame in [train,test]:
            known=frame.bias_training_max_cycle.notna()
            if not frame.loc[known,'bias_training_max_cycle'].lt(frame.loc[known,'cycle']).all():
                raise ValueError('Nonchronological bias offset')
            if not np.isfinite(frame.bias_prediction).all():raise ValueError('Missing prequential bias offset')
        train=train.assign(poll_baseline=train.bias_prediction)
        test=test.assign(poll_baseline=test.bias_prediction)
    mode='prior' if base=='prior' else 'polling'
    p=prepare_problem(train,test,calendars,mode,HALF_LIFE)
    design=p['design'];requested=FEATURES[feature_set]
    indices=[0]+[i+1 for i,c in enumerate(design.active) if c in requested]
    p['z']=p['z'][:,indices];p['future']=p['future'][:,indices]
    design.active=[c for c in design.active if c in requested]
    for key in ['fills','centers','scales','dropped']:
        setattr(design,key,{c:v for c,v in getattr(design,key).items() if c in requested})
    p['base']=base;p['feature_set']=feature_set
    p['offset']=test.prior.to_numpy() if base=='prior' else test.poll_baseline.to_numpy()
    return p


def predict_subset(p,alpha=1.,details=False):
    if alpha<=0:raise ValueError('Positive ridge penalty required')
    z,w=p['z'],p['weights'];design=p['design']
    gram=z.T@(w[:,None]*z);normal=gram+np.diag([0.]+[alpha]*len(design.active))
    beta=np.linalg.solve(normal,z.T@(w*p['response']))
    raw=p['offset']+p['future']@beta;prediction=np.clip(raw,-1,1)
    if not details:return prediction,None
    terms=['intercept']+design.active;raw_beta=beta.copy()
    for j,c in enumerate(design.active,1):
        raw_beta[j]/=design.scales[c];raw_beta[0]-=raw_beta[j]*design.centers[c]
    names=FEATURES[p['feature_set']]
    info=dict(base=p['base'],feature_set=p['feature_set'],alpha=float(alpha) if names else None,
        half_life_years=HALF_LIFE,training_cycles=int(p['train'].cycle.nunique()),training_rows=len(p['train']),
        training_first_cycle=int(p['train'].cycle.min()),training_max_cycle=int(p['train'].cycle.max()),
        training_cycle_ids=sorted(map(int,p['train'].cycle.unique())),effective_cycles=p['effective_cycles'],
        cycle_weights={str(int(y)):float(v) for y,v in p['cycle_weights'].items()},
        standardized_coefficients=dict(zip(terms,map(float,beta))),raw_score_coefficients=dict(zip(terms,map(float,raw_beta))),
        nominal_parameters=1+len(names),active_parameters=len(beta),effective_df=float(np.trace(np.linalg.solve(normal,gram))),
        clipped_predictions=int((np.abs(raw)>1).sum()),**design.metadata())
    info['training_scores']=p['scores'][['cycle']+names].replace({np.nan:None}).to_dict('records')
    info['test_scores']=p['test_scores'][['cycle']+names].replace({np.nan:None}).to_dict('records')
    return prediction,info


def evaluate(history,calendars,start_cycle=2012,min_inner_cycles=6):
    # history is the saved fixed5/8 prequential bias history, including raw polling/prior fields.
    predictions=[];grids=[];fits=[];fold_parts=[]
    for scenario,source in history.groupby('scenario'):
        if source.target_id.duplicated().any():raise ValueError('Duplicate target')
        cal=calendars[calendars.scenario.eq(scenario)]
        folds=correction_folds(source,source,scenario,start_cycle,min_inner_cycles);fold_parts.append(folds)
        for fold in folds.itertuples():
            if fold.status not in ['cv_scored','forecast_only_no_outcomes']:continue
            year=int(fold.cycle);test=source[source.cycle.eq(year)]
            common=test[['scenario','target_id','cycle','kind','geography','actual','n_samples','prior','prior_basis','poll_baseline']].copy()
            common['status']=fold.status
            for base in BASES:
                offset_col={'prior':'prior','polling':'poll_baseline','bias':'bias_prediction'}[base]
                base_prediction=test[offset_col].to_numpy(copy=True)
                predictions.append(common.assign(model=base,prediction=base_prediction,base=base,feature_set='none'))
                train=source[source.cycle.lt(year)&source.actual.notna()]
                if base!='prior':train=train[train.n_samples.gt(0)]
                inner=train[train.cycle.lt(year-2)];valid=train[train.cycle.eq(year-2)]
                apply=test if base=='prior' else test[test.n_samples.gt(0)]
                fit_test=apply if len(apply) else test.iloc[:1]
                none_loss=float(np.abs(valid[offset_col]-valid.actual).mean())
                grid_common=dict(scenario=scenario,cycle=year,base=base,validation_cycle=year-2,
                    training_max_cycle=int(inner.cycle.max()),training_cycles=int(inner.cycle.nunique()),validation_rows=len(valid))
                grids.append(dict(grid_common,feature_set='none',alpha=None,validation_mae_pp=100*none_loss))
                choices=[(none_loss,'none',None)];finals={'none':base_prediction};fit_by_name={}
                for feature_set in FEATURES:
                    ip=prepare_subset(inner,valid,cal,base,feature_set);fp=prepare_subset(train,fit_test,cal,base,feature_set)
                    candidates=[]
                    for alpha in (ALPHAS if FEATURES[feature_set] else [1.]):
                        vp,_=predict_subset(ip,alpha);loss=float(np.abs(vp-valid.actual.to_numpy()).mean())
                        candidates.append((loss,alpha))
                        grids.append(dict(grid_common,feature_set=feature_set,alpha=alpha if FEATURES[feature_set] else None,validation_mae_pp=100*loss))
                    loss,alpha=min(candidates,key=lambda v:(round(v[0],12),-v[1]))
                    pp,f=predict_subset(fp,alpha,True)
                    pred=pd.Series(base_prediction.copy(),index=test.index)
                    if len(apply):pred.loc[apply.index]=pp
                    model=base+'__'+feature_set
                    f.update(scenario=scenario,cycle=year,model=model,validation_cycle=year-2,
                        validation_mae_pp=100*loss,applied_rows=len(apply),unchanged_no_poll_rows=len(test)-len(apply))
                    fits.append(f);fit_by_name[feature_set]=f;finals[feature_set]=pred.to_numpy()
                    choices.append((loss,feature_set,alpha if FEATURES[feature_set] else None))
                    predictions.append(common.assign(model=model,base=base,feature_set=feature_set,
                        prediction=pred.to_numpy(),base_prediction=base_prediction,added_correction_pp=100*(pred.to_numpy()-base_prediction)))
                loss,selected,alpha=min(choices,key=lambda v:(round(v[0],12),PREFERENCE[v[1]],-(v[2] or 0)))
                if selected=='none':
                    f=dict(base=base,feature_set='none',alpha=None,nominal_parameters=0,active_parameters=0,effective_df=0.,
                        training_cycles=int(train.cycle.nunique()),training_rows=len(train),training_first_cycle=int(train.cycle.min()),
                        training_max_cycle=int(train.cycle.max()),applied_rows=0,unchanged_no_poll_rows=int(test.n_samples.eq(0).sum()))
                else:f=dict(fit_by_name[selected])
                f.update(scenario=scenario,cycle=year,model=base+'__selected',selected_features=selected,
                    validation_cycle=year-2,validation_mae_pp=100*loss)
                fits.append(f)
                predictions.append(common.assign(model=base+'__selected',base=base,feature_set=selected,
                    prediction=finals[selected],base_prediction=base_prediction,
                    added_correction_pp=100*(finals[selected]-base_prediction)))
    return pd.concat(predictions,ignore_index=True),pd.concat(fold_parts,ignore_index=True),pd.DataFrame(grids),fits
