"""Explicit expanding-window CV accounting for the notebook's chronological fits.

This reports the existing fold predictions, rather than choosing new parameters
after seeing their errors. The preceding-cycle inner holdout remains unchanged.
"""
import numpy as np
import pandas as pd

MIN_INNER_CYCLES = 6


def fold_ledger(targets, scenario, min_inner_cycles=MIN_INNER_CYCLES, start_cycle=2002):
    if min_inner_cycles<1:raise ValueError('Require a positive minimum training history')
    rows=[]
    for kind,source in targets.groupby('kind'):
        for year in sorted(y for y in source.cycle.unique() if y>=start_cycle):
            test=source[source.cycle.eq(year)]
            inner=source[source.cycle.lt(year-2)&source.actual.notna()]
            validation=source[source.cycle.eq(year-2)&source.actual.notna()]
            refit=source[source.cycle.lt(year)&source.actual.notna()]
            n_inner=inner.cycle.nunique()
            complete=(scenario!='oct31' or test.window_complete.all())
            if not complete:status='pending_cutoff'
            elif n_inner<min_inner_cycles:status='warm_up_insufficient_training_cycles'
            elif validation.empty:status='missing_previous_validation_cycle'
            elif test.actual.isna().all():status='forecast_only_no_outcomes'
            elif test.actual.isna().any():status='incomplete_test_outcomes'
            else:status='cv_scored'
            rows.append(dict(scenario=scenario,kind=kind,cycle=int(year),validation_cycle=int(year-2),
                status=status,min_inner_cycles=min_inner_cycles,inner_training_cycles=int(n_inner),
                inner_training_first=int(inner.cycle.min()) if len(inner) else np.nan,
                inner_training_last=int(inner.cycle.max()) if len(inner) else np.nan,
                inner_training_rows=len(inner),validation_rows=len(validation),
                refit_cycles=int(refit.cycle.nunique()),refit_rows=len(refit),
                refit_last=int(refit.cycle.max()) if len(refit) else np.nan,
                test_rows=len(test),test_outcomes=int(test.actual.notna().sum()),
                cutoff_first=str(test.context_id.min()),cutoff_last=str(test.context_id.max())))
    return pd.DataFrame(rows)


def long_predictions(original, contextual, poll_references):
    """Unify named model predictions; preserve exact existing numeric results."""
    keys=['target_id','cycle','kind','geography','actual','n_samples']
    parts=[]
    for model in ['prior','polling','features']:
        p=original[keys].copy();p['prediction']=original[model].to_numpy()
        p['model']=model;p['scenario']='original_horizon';parts.append(p)
    for model in ['prior','polling']:
        p=poll_references[keys+['scenario']].copy()
        p['prediction']=poll_references[model].to_numpy();p['model']=model;parts.append(p)
    p=contextual.rename(columns={'variant':'model'})
    p=p[['target_id','cycle','kind','geography','actual','prediction','model','scenario']].merge(
        poll_references[['target_id','scenario','n_samples']],on=['target_id','scenario'],validate='many_to_one')
    parts.append(p)
    result=pd.concat(parts,ignore_index=True)
    if result.duplicated(['scenario','model','target_id']).any():raise ValueError('Duplicate forecast')
    if not np.isfinite(result.prediction).all():raise ValueError('Missing/nonfinite forecast')
    return result


def cv_report(folds, predictions):
    keys=['scenario','kind','cycle']
    if folds.duplicated(keys).any():raise ValueError('Duplicate fold')
    selected=predictions.merge(folds[keys+['status']],on=keys,validate='many_to_one',how='left')
    if selected.status.isna().any():raise ValueError('Prediction without a fold')
    scored=selected[selected.status.eq('cv_scored')].copy()
    if scored.actual.isna().any():raise ValueError('Unknown outcome in CV')
    expected_folds=set(map(tuple,folds.loc[folds.status.eq('cv_scored'),keys].to_numpy()))
    actual_folds=set(map(tuple,scored[keys].drop_duplicates().to_numpy()))
    if expected_folds!=actual_folds:raise ValueError('Missing scored fold predictions')
    expected_models=selected.groupby(['scenario','kind']).model.apply(frozenset)
    records=[]
    for fold_key,g in scored.groupby(keys):
        if frozenset(g.model)!=expected_models.loc[fold_key[:2]]:raise ValueError('Missing model in scored fold')
        target_sets=g.groupby('model').target_id.apply(frozenset)
        if target_sets.nunique()!=1:raise ValueError('Models scored on different targets')
        per_target=g.groupby('target_id')
        if not per_target.actual.nunique().eq(1).all():raise ValueError('Models have conflicting labels')
        if not per_target.n_samples.nunique().eq(1).all():raise ValueError('Models have conflicting poll coverage')
        expected=folds.set_index(keys).loc[fold_key,'test_rows']
        if len(target_sets.iloc[0])!=expected:raise ValueError('Missing scored targets')
        for scope,q in [('all_targets',g),('with_polls',g[g.n_samples.gt(0)])]:
            for model,r in q.groupby('model'):
                error=100*(r.prediction-r.actual)
                records.append(dict(zip(keys,fold_key),scope=scope,model=model,n=len(r),
                    targets_with_polls=int(r.n_samples.gt(0).sum()),fallback_targets=int(r.n_samples.eq(0).sum()),
                    mae_pp=float(error.abs().mean()),rmse_pp=float(np.sqrt(np.mean(error**2))),
                    bias_pp=float(error.mean()),sign_accuracy=float((r.prediction.gt(0)==r.actual.gt(0)).mean())))
    scores=pd.DataFrame(records)
    if scores.empty:return selected,scores,pd.DataFrame()
    summary=scores.groupby(['scenario','kind','scope','model']).agg(
        scored_cycles=('cycle','nunique'),first_cycle=('cycle','min'),last_cycle=('cycle','max'),
        target_rows=('n','sum'),macro_MAE_pp=('mae_pp','mean'),macro_RMSE_pp=('rmse_pp','mean'),
        macro_bias_pp=('bias_pp','mean'),macro_sign_accuracy=('sign_accuracy','mean')).reset_index()
    return selected,scores,summary
