"""One fixed momentum score: shared or partially pooled polling corrections.

The polling offset and eligible targets are unchanged. Historical cycle weights
also govern train-only score construction/imputation/scaling. Outer labels never
select penalties or history decay.
"""
import numpy as np
import pandas as pd
from recency_state_baselines import prepare_problem, predict_problem, HALF_LIVES
from state_score_baselines import STATE_PENALTIES
from score_baselines import ALPHAS
from poll_error_baselines import correction_folds
from cycle_cv import MIN_INNER_CYCLES

TERM = 'economy_momentum_wh'
ARCHITECTURES = ('shared', 'state')


def prepare_momentum(train, test, calendars, half_life):
    if not train.n_samples.gt(0).all():
        raise ValueError('Only polled contests may train a polling correction')
    problem = prepare_problem(train, test, calendars, 'polling', half_life)
    design = problem['design']
    indices = [0] + [i + 1 for i, c in enumerate(design.active) if c == TERM]
    problem['z'] = problem['z'][:, indices]
    problem['future'] = problem['future'][:, indices]
    design.active = [c for c in design.active if c == TERM]
    for name in ['fills', 'centers', 'scales', 'dropped']:
        setattr(design, name, {c: v for c, v in getattr(design, name).items() if c == TERM})
    return problem


def predict_momentum(problem, architecture, alpha, state_penalty=None, details=False):
    if architecture not in ARCHITECTURES:
        raise ValueError('Unknown momentum architecture')
    if alpha <= 0:
        raise ValueError('Positive ridge penalty required')
    if architecture == 'state':
        pred, info, coef = predict_problem(problem, alpha, state_penalty, details)
        if details:
            info.update(architecture=architecture, requested_terms=[TERM])
        return pred, info, coef
    p = problem; design = p['design']; train = p['train']; test = p['test']
    z, weights = p['z'], p['weights']
    gram = z.T @ (weights[:, None] * z)
    penalty = np.diag([0.] + [alpha] * len(design.active))
    system = gram + penalty
    beta = np.linalg.solve(system, z.T @ (weights * p['response']))
    raw = test.poll_baseline.to_numpy() + p['future'] @ beta
    prediction = np.clip(raw, -1, 1)
    if not details:
        return prediction, None, None
    terms = ['intercept'] + design.active
    raw_beta = beta.copy()
    if design.active:
        raw_beta[1] /= design.scales[TERM]
        raw_beta[0] -= raw_beta[1] * design.centers[TERM]
    states = {}; rows = []
    for state in sorted(set(train.geography) | set(test.geography)):
        mask = train.geography.eq(state).to_numpy(); tr = train[mask]
        sw = pd.Series(weights[mask], index=tr.cycle).groupby(level=0).sum().to_numpy()
        effective = float(sw.sum() ** 2 / (sw @ sw)) if len(sw) else 0.
        states[state] = dict(training_rows=len(tr), training_cycles=int(tr.cycle.nunique()),
            effective_cycles=effective, status='shared_coefficients',
            deviation=dict.fromkeys(terms, 0.), total=dict(zip(terms, map(float, beta))),
            raw_total=dict(zip(terms, map(float, raw_beta))))
        for i, term in enumerate(terms):
            rows.append(dict(geography=state, term=term, shared_coefficient=float(beta[i]),
                state_deviation=0., total_coefficient=float(beta[i]), raw_total_coefficient=float(raw_beta[i]),
                training_rows=len(tr), training_cycles=int(tr.cycle.nunique()),
                effective_cycles=effective, state_status='shared_coefficients'))
    info = dict(status='fitted', architecture=architecture, requested_terms=[TERM],
        target_mode='polling', half_life_years=p['half_life'], alpha=float(alpha), state_penalty=None,
        training_rows=len(train), training_cycles=int(train.cycle.nunique()),
        training_states=int(train.geography.nunique()), training_first_cycle=int(train.cycle.min()),
        training_max_cycle=int(train.cycle.max()), effective_cycles=p['effective_cycles'],
        cycle_weights={str(int(c)): float(w) for c, w in p['cycle_weights'].items()},
        weight_sum=float(weights.sum()), weight_rule='mean-one cycle decay; divide by contests within cycle',
        shared_coefficients=dict(zip(terms, map(float, beta))), states=states,
        nominal_parameters=len(terms), shared_parameters=len(terms), state_parameters_each=0,
        effective_df=float(np.trace(np.linalg.solve(system, gram))), deviation_indices=[],
        clipped_predictions=int((np.abs(raw) > 1).sum()), **design.metadata())
    info['training_score_rows'] = p['scores'][['cycle', TERM]].replace({np.nan: None}).to_dict('records')
    info['test_score_rows'] = p['test_scores'][['cycle', TERM]].replace({np.nan: None}).to_dict('records')
    return prediction, info, pd.DataFrame(rows)


def evaluate_momentum(targets, history, calendars, scenario, start_cycle=2002,
                      min_inner_cycles=MIN_INNER_CYCLES):
    source = history[history.scenario.eq(scenario) & history.kind.eq('senate')].copy()
    if source.target_id.duplicated().any():
        raise ValueError('Duplicate historical polling forecast')
    folds = correction_folds(targets, source, scenario, start_cycle, min_inner_cycles)
    cal = calendars[calendars.scenario.eq(scenario)]
    predictions = []; grids = []; fits = []; coefficients = []
    for fold in folds.itertuples():
        if fold.status not in ['cv_scored', 'forecast_only_no_outcomes', 'incomplete_test_outcomes']:
            continue
        year = int(fold.cycle); test = source[source.cycle.eq(year)]
        train = source[source.cycle.lt(year) & source.actual.notna() & source.n_samples.gt(0)]
        inner = train[train.cycle.lt(year - 2)]; valid = train[train.cycle.eq(year - 2)]
        polled = test[test.n_samples.gt(0)]
        # A placeholder allows an audited fit even when no target can receive it.
        fit_test = polled if len(polled) else test.iloc[:1]
        common = test[['target_id', 'cycle', 'kind', 'geography', 'actual', 'n_samples',
                       'prior', 'prior_basis', 'poll_baseline']].copy()
        for name, column in [('prior', 'prior'), ('polling', 'poll_baseline')]:
            predictions.append(common.assign(scenario=scenario, model=name,
                prediction=test[column].to_numpy(), prediction_status='reference'))
        # Reuse exactly the same weighted preprocessing between architectures.
        inner_problems = {s: prepare_momentum(inner, valid, cal, half) for s, half in HALF_LIVES.items()}
        final_problems = {s: prepare_momentum(train, fit_test, cal, half) for s, half in HALF_LIVES.items()}
        for architecture in ARCHITECTURES:
            finals = {}; selected = {}
            penalties = STATE_PENALTIES if architecture == 'state' else [None]
            for strategy, half in HALF_LIVES.items():
                candidates = []
                for alpha in ALPHAS:
                    for penalty in penalties:
                        vp, _, _ = predict_momentum(inner_problems[strategy], architecture, alpha, penalty)
                        loss = float(np.mean(np.abs(vp - valid.actual.to_numpy())))
                        candidates.append((loss, alpha, penalty))
                        grids.append(dict(scenario=scenario, cycle=year, architecture=architecture,
                            weight_strategy=strategy, half_life_years=half, validation_cycle=year - 2,
                            training_max_cycle=int(inner.cycle.max()), training_rows=len(inner),
                            training_cycles=int(inner.cycle.nunique()), validation_rows=len(valid),
                            alpha=alpha, state_penalty=penalty, validation_mae_pp=100 * loss))
                loss, alpha, penalty = min(candidates, key=lambda x: (round(x[0], 12), -(x[2] or 0), -x[1]))
                selected[strategy] = (loss, alpha, penalty)
                pp, fit, coef = predict_momentum(final_problems[strategy], architecture, alpha, penalty, True)
                fit.update(scenario=scenario, cycle=year, validation_cycle=year - 2,
                    selected_validation_mae_pp=100 * loss, polled_training_only=True,
                    applied_rows=len(polled), unchanged_no_poll_rows=len(test) - len(polled))
                pred = test.poll_baseline.copy()
                if len(polled):
                    pred.loc[polled.index] = pp
                statuses = pd.Series('unchanged_no_poll_fallback', index=test.index)
                for i, row in polled.iterrows():
                    statuses.loc[i] = fit['states'][row.geography]['status']
                finals[strategy] = (pred, fit, coef, statuses)
            preference = {'equal': 0, 'half16': 1, 'half8': 2}
            chosen = min(selected, key=lambda s: (round(selected[s][0], 12), preference[s],
                                                  -(selected[s][2] or 0), -selected[s][1]))
            for label, strategy in [(s, s) for s in HALF_LIVES] + [('selected', chosen)]:
                pred, fit, coef, statuses = finals[strategy]
                model = 'momentum_' + architecture + '__' + label
                fits.append(dict(fit, model=model, weight_strategy=label, selected_weight_strategy=strategy))
                coefficients.append(coef.assign(scenario=scenario, cycle=year, model=model))
                predictions.append(common.assign(scenario=scenario, model=model, architecture=architecture,
                    weight_strategy=label, selected_weight_strategy=strategy, prediction=pred.to_numpy(),
                    prediction_status=statuses.to_numpy(),
                    adjustment_vs_polling_pp=100 * (pred.to_numpy() - test.poll_baseline.to_numpy())))
    concat = lambda rows: pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    return concat(predictions), pd.DataFrame(grids), fits, concat(coefficients), folds
