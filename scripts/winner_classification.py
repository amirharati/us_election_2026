"""Classify existing chronological margin forecasts without refitting or retuning.

D/R margin leader is the target; election-rule/independent exclusions are inherited.
Actual ties/unknowns are not binary outcomes. An exactly zero prediction is an
uncalled forecast and counts as not correct, never silently as Republican.
"""
import numpy as np
import pandas as pd

GROUP = ['scenario', 'kind', 'cycle', 'model', 'scope', 'subset']


def margin_leader(values):
    result = pd.Series('unknown', index=values.index, dtype='object')
    result.loc[values.gt(0)] = 'D'
    result.loc[values.lt(0)] = 'R'
    result.loc[values.eq(0)] = 'tie'
    return result


def classification_report(predictions, close_margin_pp=5.):
    if not np.isfinite(close_margin_pp) or close_margin_pp <= 0:
        raise ValueError('Close-race threshold must be positive and finite')
    rows = predictions.copy()
    if rows.duplicated(['scenario', 'model', 'target_id']).any():
        raise ValueError('Duplicate forecast')
    if not np.isfinite(rows.prediction).all():
        raise ValueError('Missing or nonfinite forecast')
    if not np.isfinite(rows.actual.dropna()).all():
        raise ValueError('Nonfinite outcome')
    rows['predicted_party'] = margin_leader(rows.prediction).replace('tie', 'uncalled')
    rows['actual_party'] = margin_leader(rows.actual)
    rows['classification_status'] = rows.status
    is_cv = rows.status.eq('cv_scored')
    if rows.loc[is_cv, 'actual'].isna().any():
        raise ValueError('Unknown outcome marked CV scored')
    rows.loc[is_cv & rows.actual.eq(0), 'classification_status'] = 'actual_tie_excluded'
    rows['correct'] = pd.Series(pd.NA, index=rows.index, dtype='boolean')
    scored = rows.classification_status.eq('cv_scored')
    rows.loc[scored, 'correct'] = rows.loc[scored, 'predicted_party'].eq(rows.loc[scored, 'actual_party'])
    rows['actual_margin_pp'] = 100 * rows.actual
    rows['predicted_margin_pp'] = 100 * rows.prediction
    rows['poll_coverage'] = np.where(rows.n_samples.gt(0), 'usable_polls', 'no_polls')
    rows['close_result'] = rows.actual.notna() & rows.actual.abs().le(close_margin_pp/100)
    records = []
    matrices = []
    for key, group in rows[scored].groupby(['scenario', 'kind', 'cycle']):
        if group.groupby('model').target_id.apply(frozenset).nunique() != 1:
            raise ValueError('Models scored on different targets')
        if not group.groupby('target_id').actual.nunique().eq(1).all():
            raise ValueError('Conflicting outcomes')
        if not group.groupby('target_id').n_samples.nunique().eq(1).all():
            raise ValueError('Conflicting poll coverage')
        for scope, covered in [('all_targets', group), ('with_polls', group[group.n_samples.gt(0)]),
                               ('no_polls', group[group.n_samples.eq(0)])]:
            for subset, sample in [('all_results', covered), (f'close_result_{close_margin_pp:g}pp', covered[covered.close_result])]:
                # Keep zero-denominator folds explicit rather than reporting 0% accuracy.
                for model in sorted(group.model.unique()):
                    q = sample[sample.model.eq(model)]
                    n = len(q)
                    d = q.actual_party.eq('D'); r = q.actual_party.eq('R')
                    d_ok = int((d & q.correct.fillna(False)).sum())
                    r_ok = int((r & q.correct.fillna(False)).sum())
                    correct = int(q.correct.sum())
                    wrong = int((~q.correct & q.predicted_party.ne('uncalled')).sum())
                    uncalled = int(q.predicted_party.eq('uncalled').sum())
                    rec = dict(zip(GROUP, (*key, model, scope, subset)))
                    rec.update(n=n, correct=correct, wrong=wrong, uncalled=uncalled,
                               actual_D=int(d.sum()), actual_R=int(r.sum()),
                               correct_D=d_ok, correct_R=r_ok,
                               accuracy=correct/n if n else np.nan,
                               recall_D=d_ok/d.sum() if d.any() else np.nan,
                               recall_R=r_ok/r.sum() if r.any() else np.nan,
                               balanced_accuracy=(d_ok/d.sum()+r_ok/r.sum())/2 if d.any() and r.any() else np.nan,
                               targets_with_polls=int(q.n_samples.gt(0).sum()))
                    records.append(rec)
                    for actual in ['D', 'R']:
                        for predicted in ['D', 'R', 'uncalled']:
                            matrices.append(dict(zip(GROUP, (*key, model, scope, subset)),
                                actual_party=actual, predicted_party=predicted,
                                count=int((q.actual_party.eq(actual) & q.predicted_party.eq(predicted)).sum())))
    scores = pd.DataFrame(records)
    summaries = []
    if not scores.empty:
        for period, selected in [('all_scored_cycles', scores), ('2016_onward', scores[scores.cycle.ge(2016)])]:
            for key, g in selected.groupby(['scenario', 'kind', 'model', 'scope', 'subset']):
                nonempty = g[g.n.gt(0)]
                n = int(g.n.sum())
                nd = int(g.actual_D.sum()); nr = int(g.actual_R.sum())
                summaries.append(dict(zip(['scenario','kind','model','scope','subset'], key),
                    period=period, scored_cycles=len(nonempty),
                    first_cycle=nonempty.cycle.min(), last_cycle=nonempty.cycle.max(),
                    n=n, correct=int(g.correct.sum()), wrong=int(g.wrong.sum()), uncalled=int(g.uncalled.sum()),
                    pooled_accuracy=g.correct.sum()/n if n else np.nan,
                    macro_cycle_accuracy=nonempty.accuracy.mean(),
                    pooled_balanced_accuracy=(g.correct_D.sum()/nd+g.correct_R.sum()/nr)/2 if nd and nr else np.nan))
    return rows, scores, pd.DataFrame(summaries), pd.DataFrame(matrices)
