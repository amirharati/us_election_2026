"""Historical state polling-error calibration without economic features.

Estimate final-minus-poll margin offsets. Compare shared bias with local state
means shrunk toward shared bias. A local observation is one state-cycle mean;
windows are calendar cycles, never the last N observed races. Decay weights are
anchored at Y-2 (the most recent possible training cycle), making shrinkage
strength comparable across windows in units of a recent state-cycle observation.
"""
import numpy as np
import pandas as pd
from poll_error_baselines import correction_folds
from cycle_cv import MIN_INNER_CYCLES

WINDOWS = {'all': None, 'last5': 5, 'last3': 3}
DECAYS = {'equal': None, 'half16': 16., 'half8': 8.}
PROFILES = {w+'_'+d: (n, half) for w,n in WINDOWS.items() for d,half in DECAYS.items()}
SHRINKAGES = [0., 1., 3., 10.]
ARCHITECTURES = ('shared', 'state')


def fit_bias(train, test, lookback=None, half_life=None, architecture='state', shrinkage=3.):
    if architecture not in ARCHITECTURES:
        raise ValueError('Unknown bias architecture')
    if test.empty or test.cycle.nunique()!=1 or not test.kind.eq('senate').all():
        raise ValueError('One nonempty Senate forecast cycle required')
    year = int(test.cycle.iloc[0])
    if not train.kind.eq('senate').all() or (len(train) and not train.cycle.lt(year).all()):
        raise ValueError('Only past Senate training rows allowed')
    if lookback is not None and (not isinstance(lookback,int) or lookback<1):
        raise ValueError('Positive number of calendar cycles required')
    if half_life is not None and (not np.isfinite(half_life) or half_life<=0):
        raise ValueError('Positive half-life required')
    if not np.isfinite(shrinkage) or shrinkage<0:
        raise ValueError('Nonnegative shrinkage strength required')
    if train.target_id.duplicated().any() or test.target_id.duplicated().any():
        raise ValueError('Duplicate contest')
    if not np.isfinite(test.poll_baseline).all():
        raise ValueError('Finite forecast polling offsets required')
    eligible = train[train.actual.notna() & train.n_samples.gt(0)].copy()
    if lookback is not None:
        eligible = eligible[eligible.cycle.isin(range(year-2*lookback,year,2))].copy()
    if not np.isfinite(eligible[['actual','poll_baseline']].to_numpy()).all():
        raise ValueError('Finite historical outcomes and polling offsets required')
    eligible['residual'] = eligible.actual-eligible.poll_baseline
    by_cycle = eligible.groupby('cycle').residual.mean()
    years = by_cycle.index.to_numpy(dtype=int)
    weights = np.ones(len(years)) if half_life is None else np.exp2(-((year-2)-years)/half_life)
    weight_map = dict(zip(map(int,years),map(float,weights)))
    shared = float(np.average(by_cycle,weights=weights)) if len(years) else 0.
    state_cycles = eligible.groupby(['geography','cycle']).agg(
        residual=('residual','mean'),contests=('target_id','size')).reset_index()
    state_cycles['weight'] = state_cycles.cycle.map(weight_map).astype(float)
    states={};ledger=[]
    for state in sorted(set(eligible.geography)|set(test.geography)):
        local = state_cycles[state_cycles.geography.eq(state)]
        w = local.weight.to_numpy();mass=float(w.sum())
        local_mean = float(np.average(local.residual,weights=w)) if mass else None
        reliability = mass/(mass+shrinkage) if mass else 0.
        bias = shared if architecture=='shared' else (reliability*local_mean+(1-reliability)*shared if mass else shared)
        status = ('no_window_history_zero_correction' if not len(years) else
                  'shared_bias' if architecture=='shared' else
                  'shared_fallback_no_state_history' if not mass else 'state_bias')
        info=dict(local_cycles=len(local),local_contests=int(local.contests.sum()),
            first_cycle=int(local.cycle.min()) if len(local) else None,
            last_cycle=int(local.cycle.max()) if len(local) else None,
            recency_weight_mass=mass,effective_cycles=float(mass**2/(w@w)) if mass else 0.,
            local_mean_residual=local_mean,shared_bias=shared,
            local_fraction=reliability if architecture=='state' else 0.,bias=float(bias),status=status)
        states[state]=info;ledger.append(dict(geography=state,**info))
    correction=test.geography.map({s:v['bias'] for s,v in states.items()}).to_numpy()
    applied=test.n_samples.gt(0).to_numpy()
    raw=test.poll_baseline.to_numpy()+np.where(applied,correction,0.)
    pred=np.where(applied,np.clip(raw,-1,1),test.poll_baseline.to_numpy())
    fit=dict(status='fitted' if len(years) else 'no_window_history',architecture=architecture,
        lookback_cycles=lookback,half_life_years=half_life,shrinkage=float(shrinkage) if architecture=='state' else None,
        training_rows=len(eligible),training_cycles=len(years),training_states=int(eligible.geography.nunique()),
        training_first_cycle=int(years.min()) if len(years) else None,
        training_max_cycle=int(years.max()) if len(years) else None,
        training_state_cycles=len(state_cycles),cycle_weights=weight_map,
        shared_bias=shared,effective_cycles=float(weights.sum()**2/(weights@weights)) if len(weights) else 0.,
        applied_rows=int(applied.sum()),unchanged_no_poll_rows=int((~applied).sum()),
        clipped_predictions=int((applied&(np.abs(raw)>1)).sum()),states=states,
        state_cycle_residuals=state_cycles.to_dict('records'))
    return pred,fit,pd.DataFrame(ledger)


def evaluate_bias(targets, history, scenario, start_cycle=2002, min_inner_cycles=MIN_INNER_CYCLES):
    source=history[history.scenario.eq(scenario)&history.kind.eq('senate')].copy()
    if source.target_id.duplicated().any():raise ValueError('Duplicate polling forecast')
    folds=correction_folds(targets,source,scenario,start_cycle,min_inner_cycles)
    predictions=[];fits=[];grids=[];state_rows=[]
    for fold in folds.itertuples():
        if fold.status not in ['cv_scored','forecast_only_no_outcomes','incomplete_test_outcomes']:continue
        year=int(fold.cycle);test=source[source.cycle.eq(year)]
        past=source[source.cycle.lt(year)&source.actual.notna()]
        inner=past[past.cycle.lt(year-2)]
        valid=past[past.cycle.eq(year-2)&past.n_samples.gt(0)]
        common=test[['target_id','cycle','kind','geography','actual','n_samples','prior','prior_basis','poll_baseline']].copy()
        for model,col in [('prior','prior'),('polling','poll_baseline')]:
            predictions.append(common.assign(scenario=scenario,model=model,prediction=test[col].to_numpy(),prediction_status='reference'))
        for architecture in ARCHITECTURES:
            fitted={};selection={}
            for profile,(window,half) in PROFILES.items():
                candidates=[]
                for strength in SHRINKAGES if architecture=='state' else [0.]:
                    vp,inner_fit,_=fit_bias(inner,valid,window,half,architecture,strength)
                    loss=float(np.abs(vp-valid.actual.to_numpy()).mean())
                    candidates.append((loss,strength))
                    grids.append(dict(scenario=scenario,cycle=year,architecture=architecture,profile=profile,
                        lookback_cycles=window,half_life_years=half,shrinkage=strength if architecture=='state' else None,
                        validation_cycle=year-2,training_max_cycle=inner_fit['training_max_cycle'],
                        training_cycles=inner_fit['training_cycles'],training_rows=inner_fit['training_rows'],
                        validation_rows=len(valid),validation_mae_pp=100*loss))
                loss,strength=min(candidates,key=lambda c:(round(c[0],12),-c[1]))
                pred,fit,ledger=fit_bias(past,test,window,half,architecture,strength)
                fit.update(scenario=scenario,cycle=year,validation_cycle=year-2,selected_validation_mae_pp=100*loss)
                fitted[profile]=(pred,fit,ledger);selection[profile]=(loss,strength)
            preference={p:i for i,p in enumerate(PROFILES)}
            best=min(selection,key=lambda p:(round(selection[p][0],12),preference[p],-selection[p][1]))
            for label,profile in [(p,p) for p in PROFILES]+[('selected',best)]:
                pred,fit,ledger=fitted[profile];model='bias_'+architecture+'__'+label
                fits.append(dict(fit,model=model,profile=label,selected_profile=profile))
                state_rows.append(ledger.assign(scenario=scenario,cycle=year,model=model))
                status=test.geography.map({s:v['status'] for s,v in fit['states'].items()}).where(test.n_samples.gt(0),'unchanged_no_poll_fallback')
                predictions.append(common.assign(scenario=scenario,model=model,architecture=architecture,
                    profile=label,selected_profile=profile,prediction=pred,prediction_status=status.to_numpy(),
                    adjustment_vs_polling_pp=100*(pred-test.poll_baseline.to_numpy())))
    concat=lambda rows:pd.concat(rows,ignore_index=True) if rows else pd.DataFrame()
    return concat(predictions),pd.DataFrame(grids),fits,concat(state_rows),folds
