"""Historical competitiveness screen, fixed before each held-out cycle's outcome.

Three previous two-year calendar cycles, not three observed races spanning an
unbounded interval. Use any close admitted Senate contest (not a mean that can
cancel opposite-party wins). Require two distinct historical cycles. This screen
is descriptive and does not alter model fits or hyperparameter selection.
"""
import json
import numpy as np
import pandas as pd


def competitive_ledger(predictions, history, thresholds=(10., 5.), lookback_cycles=3, min_cycles=2):
    if lookback_cycles < 1 or not 1 <= min_cycles <= lookback_cycles:
        raise ValueError('Invalid cycle-history policy')
    if not thresholds or any(not np.isfinite(t) or t <= 0 for t in thresholds):
        raise ValueError('Thresholds must be positive and finite')
    if len(set(thresholds)) != len(thresholds):
        raise ValueError('Duplicate thresholds')
    if history.target_id.duplicated().any():
        raise ValueError('Duplicate historical target')
    h=history[history.kind.eq('senate') & history.actual.notna()].copy()
    if not np.isfinite(h.actual).all():raise ValueError('Nonfinite historical outcome')
    rows=[]
    states=predictions[predictions.kind.eq('senate')][['cycle','geography']].drop_duplicates()
    for target in states.sort_values(['cycle','geography']).itertuples():
        allowed=list(range(int(target.cycle)-2*lookback_cycles,int(target.cycle),2))
        recent=h[h.geography.eq(target.geography)&h.cycle.isin(allowed)].sort_values(['cycle','target_id'])
        cycles=int(recent.cycle.nunique())
        evidence=[dict(target_id=r.target_id,cycle=int(r.cycle),margin_pp=100*float(r.actual))
                  for r in recent.itertuples()]
        minimum=100*recent.actual.abs().min() if len(recent) else np.nan
        for threshold in thresholds:
            state=('unknown_history' if cycles<min_cycles else
                   'competitive' if minimum<=threshold else 'not_selected')
            rows.append(dict(cycle=int(target.cycle),geography=target.geography,threshold_pp=float(threshold),
                selection=state,history_cycles=cycles,history_contests=len(recent),
                history_first=int(recent.cycle.min()) if len(recent) else np.nan,
                history_last=int(recent.cycle.max()) if len(recent) else np.nan,
                minimum_prior_absolute_margin_pp=minimum,history_json=json.dumps(evidence),
                allowed_cycles_json=json.dumps(allowed),lookback_cycles=lookback_cycles,min_history_cycles=min_cycles))
    return pd.DataFrame(rows)


def competitive_report(calls, ledger):
    """Same calls and targets for each model; keep national as a separate panel."""
    records=[];parts=[]
    for threshold in sorted(ledger.threshold_pp.unique(),reverse=True):
        l=ledger[ledger.threshold_pp.eq(threshold)].drop(columns='threshold_pp')
        selected=calls.merge(l,on=['cycle','geography'],how='left',validate='many_to_one')
        if selected.loc[selected.kind.eq('senate'),'selection'].isna().any():
            raise ValueError('Missing state selection')
        selected['threshold_pp']=threshold
        selected.loc[selected.kind.eq('national'),'selection']='national_always_included'
        selected['evaluation_included']=selected.selection.isin(['competitive','national_always_included'])
        parts.append(selected)
        for (scenario,kind,cycle),all_rows in selected[selected.classification_status.eq('cv_scored')].groupby(['scenario','kind','cycle']):
            if all_rows.groupby('model').target_id.apply(frozenset).nunique()!=1:
                raise ValueError('Models have different targets')
            if not all_rows.groupby('target_id').actual.nunique().eq(1).all():
                raise ValueError('Conflicting labels')
            for scope in ['all_targets','with_polls','no_polls']:
                group=all_rows[all_rows.evaluation_included]
                if scope=='with_polls':group=group[group.n_samples.gt(0)]
                if scope=='no_polls':group=group[group.n_samples.eq(0)]
                for model in sorted(all_rows.model.unique()):
                    q=group[group.model.eq(model)];n=len(q)
                    d=q.actual.gt(0);r=q.actual.lt(0);correct=int(q.correct.sum())
                    err=100*(q.prediction-q.actual)
                    records.append(dict(threshold_pp=threshold,scenario=scenario,kind=kind,cycle=int(cycle),scope=scope,model=model,
                        n=n,correct=correct,wrong=int((~q.correct & q.predicted_party.ne('uncalled')).sum()),
                        uncalled=int(q.predicted_party.eq('uncalled').sum()),
                        accuracy=correct/n if n else np.nan,
                        actual_D=int(d.sum()),actual_R=int(r.sum()),correct_D=int((d&q.correct).sum()),correct_R=int((r&q.correct).sum()),
                        balanced_accuracy=(float(q.loc[d,'correct'].mean())+float(q.loc[r,'correct'].mean()))/2 if d.any() and r.any() else np.nan,
                        mae_pp=float(err.abs().mean()),bias_pp=float(err.mean()),
                        targets_with_polls=int(q.n_samples.gt(0).sum())))
    scores=pd.DataFrame(records);summaries=[]
    for period,sub in [('all_scored_cycles',scores),('2016_onward',scores[scores.cycle.ge(2016)])]:
        for key,g in sub.groupby(['threshold_pp','scenario','kind','scope','model']):
            n=int(g.n.sum());nd=g.actual_D.sum();nr=g.actual_R.sum();nonempty=g[g.n.gt(0)]
            summaries.append(dict(zip(['threshold_pp','scenario','kind','scope','model'],key),period=period,
                n=n,correct=int(g.correct.sum()),scored_cycles=len(nonempty),
                first_cycle=nonempty.cycle.min(),last_cycle=nonempty.cycle.max(),
                pooled_accuracy=g.correct.sum()/n if n else np.nan,
                macro_cycle_accuracy=nonempty.accuracy.mean(),
                pooled_balanced_accuracy=(g.correct_D.sum()/nd+g.correct_R.sum()/nr)/2 if nd and nr else np.nan,
                pooled_mae_pp=(nonempty.mae_pp*nonempty.n).sum()/n if n else np.nan,
                macro_cycle_mae_pp=nonempty.mae_pp.mean()))
    return pd.concat(parts,ignore_index=True),scores,pd.DataFrame(summaries)
