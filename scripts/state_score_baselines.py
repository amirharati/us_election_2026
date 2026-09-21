"""Partially pooled state Senate corrections with chronological regularization.

Common national scores, shared coefficients plus penalized state deviations.
Each historical cycle retains total squared-loss weight one.
"""
import numpy as np
import pandas as pd
from standardized_score_baselines import StandardizedDesign
from feature_scores import MODEL_COLUMNS
from score_baselines import ALPHAS
from cycle_cv import fold_ledger, MIN_INNER_CYCLES

STATE_PENALTIES = [.1, 1., 10., 100.]
MODELS = ['state_partial', 'state_intercepts']


def solve_partial(z, residual, weights, states, alpha, state_penalty, model):
    """Solve the penalized joint fit via small block elimination, not two stages."""
    if model not in MODELS:
        raise ValueError('Unknown state correction model')
    if alpha <= 0 or state_penalty <= 0:
        raise ValueError('Positive penalties required')
    z = np.asarray(z, dtype=float)
    residual = np.asarray(residual, dtype=float)
    weights = np.asarray(weights, dtype=float)
    states = np.asarray(states, dtype=str)
    if not (np.isfinite(z).all() and np.isfinite(residual).all()
            and np.isfinite(weights).all() and (weights > 0).all()):
        raise ValueError('Finite inputs and positive weights required')
    k = z.shape[1]
    indices = np.arange(k) if model == 'state_partial' else np.array([0])
    q = len(indices)
    penalty = np.diag([0.] + [float(alpha)] * (k - 1))
    schur = z.T @ (weights[:, None] * z) + penalty
    rhs = z.T @ (weights * residual)
    blocks = {}
    for state in sorted(set(states)):
        use = states == state
        x, w, y = z[use], weights[use], residual[use]
        d = x[:, indices]
        cross = x.T @ (w[:, None] * d)
        b = d.T @ (w[:, None] * d) + state_penalty * np.eye(q)
        t = d.T @ (w * y)
        inv = np.linalg.solve(b, np.eye(q))
        schur -= cross @ inv @ cross.T
        rhs -= cross @ inv @ t
        blocks[state] = (cross, inv, t)
    shared = np.linalg.solve(schur, rhs)
    inv_shared = np.linalg.solve(schur, np.eye(k))
    deviations = {}
    penalty_trace = alpha * np.trace(inv_shared[1:, 1:])
    for state, (cross, inv, t) in blocks.items():
        deviation = np.zeros(k)
        deviation[indices] = inv @ (t - cross.T @ shared)
        deviations[state] = deviation
        h = inv @ cross.T
        penalty_trace += state_penalty * np.trace(inv + h @ inv_shared @ h.T)
    nominal = k + len(blocks) * q
    # trace(H) = dimension - trace((X'WX + P)^-1 P).
    effective_df = float(nominal - penalty_trace)
    return shared, deviations, dict(nominal_parameters=nominal,
        shared_parameters=k, state_parameters_each=q,
        effective_df=effective_df, deviation_indices=indices.tolist())


def fit_state_correction(train, test, calendars, alpha, state_penalty,
                         model='state_partial'):
    if train.empty or test.empty or train.actual.isna().any():
        raise ValueError('Known training labels and forecast rows required')
    if train.cycle.max() >= test.cycle.min():
        raise ValueError('Training must precede forecast cycles')
    if not train.kind.eq('senate').all() or not test.kind.eq('senate').all():
        raise ValueError('Senate only')
    if train.geography.isna().any() or test.geography.isna().any():
        raise ValueError('State identity required')
    if calendars.cycle.duplicated().any():
        raise ValueError('One calendar per cycle required')
    calendar = calendars.set_index('cycle', drop=False)
    train_years = sorted(train.cycle.unique())
    train_cal = calendar.loc[train_years].reset_index(drop=True)
    test_cal = calendar.loc[sorted(test.cycle.unique())].reset_index(drop=True)
    design = StandardizedDesign(MODEL_COLUMNS).fit(train_cal)
    x, scores, _ = design.transform(train_cal)
    v, test_scores, _ = design.transform(test_cal, require_later=True)
    terms = ['intercept'] + design.active
    indexed = pd.DataFrame(np.column_stack([np.ones(len(x)), x]), index=train_cal.cycle)
    z = indexed.loc[train.cycle].to_numpy()
    forecast = pd.DataFrame(np.column_stack([np.ones(len(v)), v]), index=test_cal.cycle)
    z_test = forecast.loc[test.cycle].to_numpy()
    weights = 1 / train.groupby('cycle').cycle.transform('size').to_numpy()
    residual = (train.actual - train.prior).to_numpy()
    shared, deviations, complexity = solve_partial(z, residual, weights,
        train.geography.to_numpy(), alpha, state_penalty, model)
    all_states = sorted(set(train.geography) | set(test.geography))
    state_coefficients = {}; state_rows = []
    for state in all_states:
        delta = deviations.get(state, np.zeros(len(terms)))
        total = shared + delta
        tr = train[train.geography.eq(state)]
        status = 'fitted_state_deviation' if len(tr) else 'shared_fallback_no_state_history'
        raw = total.copy()
        if design.active:
            raw[1:] /= np.array([design.scales[c] for c in design.active])
            raw[0] -= sum(raw[j+1] * design.centers[c] for j, c in enumerate(design.active))
        state_coefficients[state] = dict(total=dict(zip(terms, map(float, total))),
            deviation=dict(zip(terms, map(float, delta))),
            raw_total=dict(zip(terms, map(float, raw))),
            training_cycles=int(tr.cycle.nunique()), training_rows=len(tr), status=status)
        for j, term in enumerate(terms):
            state_rows.append(dict(geography=state, term=term, shared_coefficient=float(shared[j]),
                state_deviation=float(delta[j]), total_coefficient=float(total[j]),
                raw_total_coefficient=float(raw[j]), training_cycles=int(tr.cycle.nunique()),
                training_rows=len(tr), status=status))
    corrections = []; contributions = []
    for i, row in enumerate(test.itertuples()):
        delta = deviations.get(row.geography, np.zeros(len(terms)))
        common = z_test[i] * shared
        local = z_test[i] * delta
        correction = float((common + local).sum())
        corrections.append(correction)
        for j, term in enumerate(terms):
            contributions.append(dict(target_id=row.target_id, cycle=int(row.cycle),
                geography=row.geography, term=term, model=model,
                standardized_input=float(z_test[i, j]),
                shared_contribution_pp=100*float(common[j]),
                state_contribution_pp=100*float(local[j]),
                total_contribution_pp=100*float(common[j]+local[j]),
                correction_pp=100*correction,
                state_status=state_coefficients[row.geography]['status']))
    raw = test.prior.to_numpy() + np.array(corrections)
    info = dict(model=model, status='fitted', alpha=float(alpha),
        state_penalty=float(state_penalty), training_cycles=len(train_years),
        training_rows=len(train), training_states=int(train.geography.nunique()),
        training_cycle_ids=list(map(int, train_years)), training_max_cycle=int(train.cycle.max()),
        fit_target='state actual - prior; total weight one per cycle',
        shared_coefficients=dict(zip(terms, map(float, shared))),
        states=state_coefficients, clipped_predictions=int((np.abs(raw)>1).sum()),
        **complexity, **design.metadata())
    info['training_score_rows'] = scores[['cycle']+MODEL_COLUMNS].replace({np.nan: None}).to_dict('records')
    info['test_score_rows'] = test_scores[['cycle']+MODEL_COLUMNS].replace({np.nan: None}).to_dict('records')
    info['test_missing_scores'] = {str(int(r.cycle)): [c for c in MODEL_COLUMNS
        if pd.isna(getattr(r, c))] for r in test_scores.itertuples()}
    return np.clip(raw, -1, 1), info, pd.DataFrame(contributions), pd.DataFrame(state_rows)


def evaluate_states(targets, calendars, scenario, start_cycle=2002,
                    min_inner_cycles=MIN_INNER_CYCLES, models=None):
    names = MODELS if models is None else list(models)
    if not names or len(set(names)) != len(names) or not set(names) <= set(MODELS):
        raise ValueError('Unknown or duplicate model')
    source = targets[targets.kind.eq('senate')].copy()
    cal = calendars[calendars.scenario.eq(scenario)].copy()
    folds = fold_ledger(source, scenario, min_inner_cycles, start_cycle)
    predictions = []; grids = []; fits = []; parts = []; coefficients = []
    for fold in folds.itertuples():
        if fold.status == 'pending_cutoff':
            continue
        year = int(fold.cycle)
        test = source[source.cycle.eq(year)]
        train = source[source.cycle.lt(year) & source.actual.notna()]
        inner = train[train.cycle.lt(year-2)]
        validation = train[train.cycle.eq(year-2)]
        eligible = inner.cycle.nunique() >= min_inner_cycles and len(validation) > 0
        for model in names:
            alpha = penalty = None
            if eligible:
                candidates = []
                for a in ALPHAS:
                    for lam in STATE_PENALTIES:
                        pred, fit, _, _ = fit_state_correction(inner, validation, cal, a, lam, model)
                        loss = float(np.mean(np.abs(pred-validation.actual.to_numpy())))
                        candidates.append((loss, a, lam))
                        grids.append(dict(scenario=scenario, cycle=year, model=model,
                            validation_cycle=year-2, training_max_cycle=fit['training_max_cycle'],
                            training_cycles=fit['training_cycles'], alpha=a, state_penalty=lam,
                            validation_mae_pp=100*loss))
                _, alpha, penalty = min(candidates, key=lambda v: (round(v[0], 12), -v[2], -v[1]))
                pred, fit, part, coeff = fit_state_correction(train, test, cal, alpha, penalty, model)
                parts.append(part.assign(scenario=scenario))
                coefficients.append(coeff.assign(scenario=scenario, cycle=year, model=model))
            else:
                pred = test.prior.to_numpy()
                fit = dict(model=model, status='warmup_prior_fallback', training_cycles=int(train.cycle.nunique()))
            fit.update(scenario=scenario, cycle=year, validation_cycle=year-2)
            fits.append(fit)
            out = test[['target_id','cycle','kind','geography','context_id','actual','prior','prior_basis']].copy()
            predictions.append(out.assign(scenario=scenario, model=model, prediction=pred,
                selected_alpha=alpha, selected_state_penalty=penalty))
    concat = lambda rows: pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    return concat(predictions), pd.DataFrame(grids), fits, concat(parts), concat(coefficients), folds
