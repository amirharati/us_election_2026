"""Independent polling residual reconstruction for each regression family."""
import json
from pathlib import Path
import numpy as np
from audit_score_model import design as raw_score_design
from audit_state_scores import reconstruct as reconstruct_state
from feature_scores import MODEL_COLUMNS
from standardized_score_baselines import VARIANTS as SCORE_VARIANTS
from contextual_baselines import CONTINUOUS, BINARY, CHANGE_FEATURES, VARIANTS as CONTEXT_VARIANTS


def reconstruct(train,test,calendars,model,alpha,state_penalty):
    residual=(train.actual-train.poll_baseline)
    if model in ['state_partial','state_intercepts']:
        pred,_,_,_=reconstruct_state(train.assign(prior=train.poll_baseline),
            test.assign(prior=test.poll_baseline),calendars,alpha,state_penalty,model)
        return pred
    if model in CONTEXT_VARIANTS:
        continuous=CONTINUOUS+(CHANGE_FEATURES if model=='interactions_changes' else [])
        cols=[c for c in continuous+BINARY if train[c].notna().any()]
        fill={c:float(train[c].mode().iloc[0] if c in BINARY else train[c].median()) for c in cols}
        center={c:0. if c in BINARY else float(train[c].fillna(fill[c]).mean()) for c in cols}
        scales={c:1. if c in BINARY else float(train[c].fillna(fill[c]).std(ddof=0)) for c in cols}
        scales={c:s if s>1e-12 else 1. for c,s in scales.items()}
        missing=[c for c in cols if train[c].isna().any()]
        interactions=[c for c in continuous if c in cols] if model!='additive' and 'wh_dem' in cols else []
        matrices=[]
        for frame in [train,test]:
            normalized={c:(frame[c].fillna(fill[c]).to_numpy(dtype=float)-center[c])/scales[c] for c in cols}
            values=list(normalized.values())+[frame[c].isna().to_numpy(dtype=float) for c in missing]
            if interactions:
                sign=2*frame.wh_dem.fillna(fill['wh_dem']).to_numpy()-1
                values.extend(normalized[c]*sign for c in interactions)
            matrices.append(np.column_stack(values))
        x,z=matrices
        y=residual.to_numpy()
        w=1/train.groupby('cycle').cycle.transform('size').to_numpy()
    else:
        means=residual.groupby(train.cycle).mean().sort_index()
        if model=='constant':
            return np.clip(test.poll_baseline.to_numpy()+means.mean(),-1,1)
        calendar=calendars.set_index('cycle',drop=False)
        test_cycles=sorted(test.cycle.unique())
        recipe=json.loads((Path(__file__).resolve().parents[1]/'config/fixed_feature_scores_v2.json').read_text())
        _,_,a,b,_,fills,available=raw_score_design(calendar.loc[means.index],calendar.loc[test_cycles],recipe)
        requested=MODEL_COLUMNS if model=='four_scores' else SCORE_VARIANTS[model]
        active=[c for c in requested if c in available]
        raw=a[active].fillna(fills)
        future=b[active].fillna(fills)
        if model!='four_scores':
            mu,sd=raw.mean(),raw.std(ddof=0)
            future=(future-mu)/sd
            raw=(raw-mu)/sd
        x=raw.to_numpy(dtype=float); z=future.set_axis(test_cycles).loc[test.cycle].to_numpy(dtype=float)
        y=means.to_numpy();w=np.ones(len(y))
    # Independent weighted normal equations with unpenalized intercept.
    mu=np.average(x,axis=0,weights=w)
    mean_y=np.average(y,weights=w)
    xc=x-mu
    beta=np.linalg.solve(xc.T@(w[:,None]*xc)+alpha*np.eye(x.shape[1]),xc.T@(w*(y-mean_y)))
    correction=mean_y+(z-mu)@beta
    return np.clip(test.poll_baseline.to_numpy()+correction,-1,1)
