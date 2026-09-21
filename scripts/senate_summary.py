"""Senate-only summaries of unchanged state forecasts; no House inputs.

Equal weight per admitted contest. Aggregate margin direction is neither a
national popular-vote winner nor Senate control. Retain state errors beside it
because opposite state errors can cancel in an aggregate.
"""
import numpy as np
import pandas as pd


def senate_report(calls, membership):
    senate=calls[calls.kind.eq('senate')].copy()
    keys=['scenario','target_id']
    if senate.duplicated(keys+['model']).any():raise ValueError('Duplicate forecast')
    prior=senate[senate.model.eq('prior')][keys+['prediction']].rename(columns={'prediction':'prior_margin'})
    senate=senate.merge(prior,on=keys,how='left',validate='many_to_one')
    if senate.prior_margin.isna().any():raise ValueError('Missing matching prior')
    for threshold in [10.,5.]:
        m=membership[membership.threshold_pp.eq(threshold)][['cycle','geography','selection']].rename(
            columns={'selection':f'history_selection_{int(threshold)}pp'})
        senate=senate.merge(m,on=['cycle','geography'],how='left',validate='many_to_one')
        if senate[f'history_selection_{int(threshold)}pp'].isna().any():raise ValueError('Missing membership')
    records=[]
    for key,group in senate.groupby(['scenario','cycle']):
        if group.groupby('model').target_id.apply(frozenset).nunique()!=1:
            raise ValueError('Different model targets')
        for col in ['actual','n_samples','classification_status']:
            if not group.groupby('target_id')[col].nunique(dropna=False).eq(1).all():
                raise ValueError('Conflicting target metadata')
        if group.classification_status.nunique()!=1:raise ValueError('Mixed fold status')
        status=group.classification_status.iloc[0]
        if status=='cv_scored' and group.actual.isna().any():raise ValueError('Unknown scored outcome')
        for subset,selected in [('all_admitted',group),
                ('historically_competitive_10pp',group[group.history_selection_10pp.eq('competitive')]),
                ('historically_competitive_5pp',group[group.history_selection_5pp.eq('competitive')])]:
            for scope in ['all_targets','with_polls']:
                sample=selected if scope=='all_targets' else selected[selected.n_samples.gt(0)]
                for model in sorted(group.model.unique()):
                    q=sample[sample.model.eq(model)];n=len(q)
                    known=n>0 and q.actual.notna().all()
                    scored=known and status=='cv_scored'
                    prediction=float(q.prediction.mean()) if n else np.nan
                    actual=float(q.actual.mean()) if known else np.nan
                    error=100*(prediction-actual) if scored else np.nan
                    correct=int(q.correct.sum()) if scored else np.nan
                    records.append(dict(scenario=key[0],cycle=int(key[1]),model=model,subset=subset,scope=scope,
                        fold_status=status,status='empty_subset' if n==0 else status,
                        n=n,states=int(q.geography.nunique()),polled_contests=int(q.n_samples.gt(0).sum()),
                        no_poll_contests=int(q.n_samples.eq(0).sum()),
                        prior_margin_pp=100*q.prior_margin.mean() if n else np.nan,
                        predicted_margin_pp=100*prediction,actual_margin_pp=100*actual,
                        correction_pp=100*(q.prediction-q.prior_margin).mean() if n else np.nan,
                        aggregate_error_pp=error,aggregate_absolute_error_pp=abs(error),
                        state_mae_pp=100*(q.prediction-q.actual).abs().mean() if scored else np.nan,
                        state_correct=correct,state_accuracy=correct/n if scored else np.nan,
                        # A tie cannot be turned into a party win. No chamber-control interpretation.
                        aggregate_direction_correct=(np.sign(prediction)==np.sign(actual)) if scored and actual!=0 else np.nan,
                        prior_presidential_fallbacks=int(q.prior_basis.eq('lagged_state_presidential_result_fallback').sum())
                            if 'prior_basis' in q else np.nan))
    aggregate=pd.DataFrame(records);summaries=[]
    for period,start in [('all_scored_cycles',0),('2016_onward',2016)]:
        scored=aggregate[aggregate.status.eq('cv_scored')&aggregate.cycle.ge(start)]
        for key,g in scored.groupby(['scenario','subset','scope','model']):
            n=int(g.n.sum())
            summaries.append(dict(zip(['scenario','subset','scope','model'],key),period=period,
                scored_cycles=len(g),contests=n,correct=int(g.state_correct.sum()),
                pooled_state_accuracy=g.state_correct.sum()/n,
                macro_state_accuracy=g.state_accuracy.mean(),
                aggregate_mae_pp=g.aggregate_absolute_error_pp.mean(),
                aggregate_bias_pp=g.aggregate_error_pp.mean(),
                mean_state_mae_pp=g.state_mae_pp.mean(),
                aggregate_direction_accuracy=g.aggregate_direction_correct.mean()))
    return senate,aggregate,pd.DataFrame(summaries)
