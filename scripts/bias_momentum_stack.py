"""Chronological stacking of state polling-bias calibration and shared momentum.

Each training offset is a prequential bias forecast computed before its own label
was known. Never fit the second layer to in-sample first-layer predictions.
"""
import numpy as np
import pandas as pd
from state_poll_bias import fit_bias, PROFILES, SHRINKAGES
from momentum_recency_baselines import prepare_momentum, predict_momentum, TERM
from recency_state_baselines import HALF_LIVES
from score_baselines import ALPHAS
from poll_error_baselines import correction_folds
from cycle_cv import MIN_INNER_CYCLES

BASES = ('fixed5_8', 'past_selected')


def build_bias_history(history, scenario):
    source=history[history.scenario.eq(scenario)&history.kind.eq('senate')].copy()
    if source.target_id.duplicated().any():raise ValueError('Duplicate polling forecast')
    parts=[];grids=[];fits=[]
    for year in sorted(source.cycle.unique()):
        year=int(year);test=source[source.cycle.eq(year)]
        past=source[source.cycle.lt(year)&source.actual.notna()]
        inner=past[past.cycle.lt(year-2)]
        valid=past[past.cycle.eq(year-2)&past.n_samples.gt(0)]
        # Early bias forecasts are needed to train the later stack honestly.
        # Without earlier polled training/validation, use an explicit fixed default.
        can_tune=len(valid)>0 and inner.n_samples.gt(0).any()
        candidate_cache={}
        if can_tune:
            for profile,(window,half) in PROFILES.items():
                for strength in SHRINKAGES:
                    vp,_,_=fit_bias(inner,valid,window,half,'state',strength)
                    candidate_cache[(profile,strength)]=float(np.abs(vp-valid.actual.to_numpy()).mean())
        preference={p:i for i,p in enumerate(PROFILES)}
        for base in BASES:
            profiles=['last5_half8'] if base=='fixed5_8' else list(PROFILES)
            if can_tune:
                candidates=[(loss,profile,k) for (profile,k),loss in candidate_cache.items() if profile in profiles]
                loss,profile,strength=min(candidates,key=lambda x:(round(x[0],12),preference[x[1]],-x[2]))
                for value,name,k in candidates:
                    grids.append(dict(scenario=scenario,cycle=year,base=base,profile=name,shrinkage=k,
                        validation_cycle=year-2,training_max_cycle=int(inner.loc[inner.n_samples.gt(0),'cycle'].max()),
                        validation_mae_pp=100*value))
                tuning_status='previous_cycle_tuned'
            else:
                profile='last5_half8' if base=='fixed5_8' else 'all_equal'
                strength=3.;loss=None;tuning_status='default_insufficient_earlier_polled_validation'
            window,half=PROFILES[profile]
            prediction,fit,_=fit_bias(past,test,window,half,'state',strength)
            fit.update(scenario=scenario,cycle=year,base=base,profile=profile,
                validation_cycle=year-2,tuning_status=tuning_status,
                validation_mae_pp=100*loss if loss is not None else None)
            fits.append(fit)
            status=test.geography.map({s:v['status'] for s,v in fit['states'].items()}).where(test.n_samples.gt(0),'unchanged_no_poll_fallback')
            parts.append(test.assign(base=base,bias_prediction=prediction,
                bias_adjustment_pp=100*(prediction-test.poll_baseline.to_numpy()),bias_profile=profile,
                bias_shrinkage=strength,bias_training_max_cycle=fit['training_max_cycle'],
                bias_validation_cycle=year-2,bias_tuning_status=tuning_status,bias_prediction_status=status.to_numpy()))
    return pd.concat(parts,ignore_index=True),pd.DataFrame(grids),fits


def prepare_stack(train,test,calendars,half_life):
    for frame in [train,test]:
        if not np.isfinite(frame.bias_prediction).all():raise ValueError('Finite chronological bias offsets required')
        known=frame.bias_training_max_cycle.notna()
        if not frame.loc[known,'bias_training_max_cycle'].lt(frame.loc[known,'cycle']).all():
            raise ValueError('Bias offset used own/future cycle labels')
    # Preserve the raw poll column in the caller; reuse the exact momentum design.
    return prepare_momentum(train.assign(poll_baseline=train.bias_prediction),
                            test.assign(poll_baseline=test.bias_prediction),calendars,half_life)


def predict_stack(problem,alpha,constant=False,details=False):
    if constant:
        correction=float(np.average(problem['response'],weights=problem['weights']))
        raw=problem['test'].poll_baseline.to_numpy()+correction
        prediction=np.clip(raw,-1,1)
        if not details:return prediction,None
        info=dict(status='fitted',stage='constant',half_life_years=problem['half_life'],alpha=None,
            training_rows=len(problem['train']),training_cycles=int(problem['train'].cycle.nunique()),
            training_max_cycle=int(problem['train'].cycle.max()),effective_cycles=problem['effective_cycles'],
            cycle_weights={str(int(c)):float(w) for c,w in problem['cycle_weights'].items()},
            shared_coefficients={'intercept':correction},nominal_parameters=1,effective_df=1.,
            active_terms=[],clipped_predictions=int((np.abs(raw)>1).sum()))
        return prediction,info
    prediction,info,_=predict_momentum(problem,'shared',alpha,details=details)
    if details:info['stage']='momentum'
    return prediction,info


def evaluate_stack(targets, history, calendars, scenario, start_cycle=2002,
                   min_inner_cycles=MIN_INNER_CYCLES):
    # 'history' contains both first-layer recipes and full original polling columns.
    support=history[history.scenario.eq(scenario)&history.base.eq(BASES[0])]
    folds=correction_folds(targets,support,scenario,start_cycle,min_inner_cycles)
    cal=calendars[calendars.scenario.eq(scenario)]
    parts=[];grids=[];fits=[]
    for fold in folds.itertuples():
        if fold.status not in ['cv_scored','forecast_only_no_outcomes','incomplete_test_outcomes']:continue
        year=int(fold.cycle)
        for base in BASES:
            source=history[history.scenario.eq(scenario)&history.base.eq(base)]
            test=source[source.cycle.eq(year)]
            train=source[source.cycle.lt(year)&source.actual.notna()&source.n_samples.gt(0)]
            inner=train[train.cycle.lt(year-2)];valid=train[train.cycle.eq(year-2)]
            polled=test[test.n_samples.gt(0)];fit_test=polled if len(polled) else test.iloc[:1]
            common=test[['target_id','cycle','kind','geography','actual','n_samples','prior','prior_basis','poll_baseline']].copy()
            if base==BASES[0]:
                for name,col in [('prior','prior'),('polling','poll_baseline')]:
                    parts.append(common.assign(scenario=scenario,model=name,prediction=test[col].to_numpy(),prediction_status='reference'))
            parts.append(common.assign(scenario=scenario,model='base_'+base,base=base,
                prediction=test.bias_prediction.to_numpy(),prediction_status=test.bias_prediction_status.to_numpy()))
            finals={};selections={}
            for strategy,half in HALF_LIVES.items():
                problem=prepare_stack(inner,valid,cal,half)
                candidates=[]
                for alpha in ALPHAS:
                    vp,_=predict_stack(problem,alpha)
                    loss=float(np.mean(np.abs(vp-valid.actual.to_numpy())))
                    candidates.append((loss,alpha))
                    grids.append(dict(scenario=scenario,cycle=year,base=base,stage='momentum',weight_strategy=strategy,
                        half_life_years=half,alpha=alpha,validation_cycle=year-2,
                        training_max_cycle=int(inner.cycle.max()),training_cycles=int(inner.cycle.nunique()),
                        validation_rows=len(valid),validation_mae_pp=100*loss))
                loss,alpha=min(candidates,key=lambda x:(round(x[0],12),-x[1]))
                pp,fit=predict_stack(prepare_stack(train,fit_test,cal,half),alpha,details=True)
                fit.update(scenario=scenario,cycle=year,base=base,validation_cycle=year-2,
                    selected_validation_mae_pp=100*loss,applied_rows=len(polled),unchanged_no_poll_rows=len(test)-len(polled))
                pred=test.bias_prediction.copy()
                if len(polled):pred.loc[polled.index]=pp
                finals[strategy]=(pred,fit);selections[strategy]=(loss,alpha)
            preference={'equal':0,'half16':1,'half8':2}
            chosen=min(selections,key=lambda k:(round(selections[k][0],12),preference[k],-selections[k][1]))
            for label,strategy in [(s,s) for s in HALF_LIVES]+[('selected',chosen)]:
                pred,fit=finals[strategy];model='stack_'+base+'__'+label
                fits.append(dict(fit,model=model,weight_strategy=label,selected_weight_strategy=strategy))
                parts.append(common.assign(scenario=scenario,model=model,base=base,prediction=pred.to_numpy(),
                    bias_prediction=test.bias_prediction.to_numpy(),second_stage_adjustment_pp=100*(pred.to_numpy()-test.bias_prediction.to_numpy()),
                    prediction_status=np.where(test.n_samples.gt(0),'bias_plus_momentum','unchanged_no_poll_fallback')))
            # Same second-layer history weights; isolates an intercept from momentum.
            problem=prepare_stack(inner,valid,cal,8.)
            vp,_=predict_stack(problem,1.,constant=True)
            loss=float(np.abs(vp-valid.actual.to_numpy()).mean())
            pp,fit=predict_stack(prepare_stack(train,fit_test,cal,8.),1.,constant=True,details=True)
            pred=test.bias_prediction.copy()
            if len(polled):pred.loc[polled.index]=pp
            model='stack_'+base+'__constant8'
            fit.update(scenario=scenario,cycle=year,base=base,model=model,weight_strategy='half8',selected_weight_strategy='half8',
                validation_cycle=year-2,selected_validation_mae_pp=100*loss,applied_rows=len(polled),unchanged_no_poll_rows=len(test)-len(polled))
            fits.append(fit)
            grids.append(dict(scenario=scenario,cycle=year,base=base,stage='constant',weight_strategy='half8',half_life_years=8.,
                alpha=None,validation_cycle=year-2,training_max_cycle=int(inner.cycle.max()),
                training_cycles=int(inner.cycle.nunique()),validation_rows=len(valid),validation_mae_pp=100*loss))
            parts.append(common.assign(scenario=scenario,model=model,base=base,prediction=pred.to_numpy(),
                bias_prediction=test.bias_prediction.to_numpy(),second_stage_adjustment_pp=100*(pred.to_numpy()-test.bias_prediction.to_numpy()),
                prediction_status=np.where(test.n_samples.gt(0),'bias_plus_constant','unchanged_no_poll_fallback')))
    return pd.concat(parts,ignore_index=True),pd.DataFrame(grids),fits,folds
