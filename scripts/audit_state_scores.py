"""Independent augmented-matrix reconstruction of partial-pooling fits."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from audit_score_model import design as raw_design
from feature_scores import MODEL_COLUMNS


def reconstruct(train, test, calendars, alpha, state_penalty, model):
    recipe = json.loads((Path(__file__).resolve().parents[1]/'config/fixed_feature_scores_v2.json').read_text())
    calendar = calendars.set_index('cycle', drop=False)
    train_years = sorted(train.cycle.unique())
    test_years = sorted(test.cycle.unique())
    _, _, a, b, _, fills, available = raw_design(calendar.loc[train_years],
        calendar.loc[test_years], recipe)
    active = [c for c in MODEL_COLUMNS if c in available]
    raw = a[active].fillna(fills)
    mu, sd = raw.mean(), raw.std(ddof=0)
    x = ((raw-mu)/sd).to_numpy()
    v = ((b[active].fillna(fills)-mu)/sd).to_numpy()
    z = pd.DataFrame(np.column_stack([np.ones(len(x)), x]), index=train_years).loc[train.cycle].to_numpy()
    z_test = pd.DataFrame(np.column_stack([np.ones(len(v)), v]), index=test_years).loc[test.cycle].to_numpy()
    states = sorted(train.geography.unique())
    indices = list(range(z.shape[1])) if model == 'state_partial' else [0]
    matrix = np.column_stack([z]+[z[:, indices]*train.geography.eq(s).to_numpy()[:, None] for s in states])
    future = np.column_stack([z_test]+[z_test[:, indices]*test.geography.eq(s).to_numpy()[:, None] for s in states])
    weights = 1/train.groupby('cycle').cycle.transform('size').to_numpy()
    penalties = [0.] + [alpha]*len(active) + [state_penalty]*(len(states)*len(indices))
    gram = matrix.T @ (weights[:, None]*matrix)
    system = gram + np.diag(penalties)
    beta = np.linalg.solve(system, matrix.T @ (weights*(train.actual-train.prior).to_numpy()))
    prediction = np.clip(test.prior.to_numpy()+future@beta, -1, 1)
    df = float(np.trace(np.linalg.solve(system, gram)))
    terms = ['intercept']+active
    k, q = len(terms), len(indices)
    shared = dict(zip(terms, map(float, beta[:k])))
    deviations = {}
    for j, state in enumerate(states):
        d = np.zeros(k); d[indices] = beta[k+j*q:k+(j+1)*q]
        deviations[state] = dict(zip(terms, map(float, d)))
    return prediction, shared, deviations, df
