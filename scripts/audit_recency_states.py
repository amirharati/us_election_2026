"""Independent weighted score recipe and dense joint-regression reconstruction."""
import json
from pathlib import Path
import numpy as np
import pandas as pd


def reconstruct(train,test,calendars,mode,half_life,alpha,state_penalty,
                columns=None,architecture='state'):
    if architecture not in ['state','shared']:
        raise ValueError('Unknown audit architecture')
    recipe=json.loads((Path(__file__).resolve().parents[1]/'config/fixed_feature_scores_v2.json').read_text())
    years=sorted(train.cycle.unique());target=int(test.cycle.iloc[0])
    raw_w=np.ones(len(years)) if half_life is None else 2.**(-(target-np.array(years))/half_life)
    cw=raw_w/raw_w.mean()
    indexed=calendars.set_index('cycle');trcal=indexed.loc[years];tecal=indexed.loc[[target]]
    frames=[trcal,tecal];component_matrices=[{},{}]
    for col,spec in recipe['components'].items():
        known=trcal[col].notna().to_numpy();values=trcal[col].to_numpy(dtype=float)[known];w=cw[known]
        if len(values):
            mean=np.dot(w,values)/w.sum();sd=np.sqrt(np.dot(w,(values-mean)**2)/w.sum())
        else:mean=sd=np.nan
        valid=len(values)>=recipe['minimum_history_values'] and sd>1e-12
        for frame,components in zip(frames,component_matrices):
            center=0. if spec['center']=='zero' else mean
            components[col]=spec['direction']*np.clip((frame[col].to_numpy(dtype=float)-center)/sd,
                -recipe['clip_component_abs'],recipe['clip_component_abs']) if valid else np.full(len(frame),np.nan)
    scores=[]
    for frame,components in zip(frames,component_matrices):
        sign=2*frame.wh_dem.to_numpy(dtype=float)-1
        values={}
        for name in ['economy_conditions','economy_momentum']:
            terms=[components[c]*spec['weight'] for c,spec in recipe['components'].items() if spec['score']==name]
            values[name+'_wh']=np.sum(terms,axis=0)*sign
        values['approval_wh']=np.clip((frame.approval_3m_pct.to_numpy(dtype=float)-recipe['approval_center_pct'])/recipe['approval_scale_pp'],
            -recipe['clip_component_abs'],recipe['clip_component_abs'])*sign
        values['disruption_any']=frame[recipe['disruption_column']].to_numpy(dtype=float)
        scores.append(pd.DataFrame(values,index=frame.index))
    a,b=scores;active=[];train_cols=[];test_cols=[]
    selected_columns=list(a) if columns is None else list(columns)
    if not selected_columns or len(set(selected_columns))!=len(selected_columns) or not set(selected_columns)<=set(a):
        raise ValueError('Unknown or duplicate score column')
    for c in selected_columns:
        known=a[c].notna().to_numpy()
        if not known.any():continue
        pairs=sorted(zip(a.loc[known,c].to_numpy(),cw[known]))
        values=np.array([v for v,_ in pairs]);weights=np.array([w for _,w in pairs]);cum=weights.cumsum();half=weights.sum()/2
        i=int(np.searchsorted(cum,half));fill=values[i]
        if i<len(values)-1 and abs(cum[i]-half)<=1e-12*weights.sum():fill=(values[i]+values[i+1])/2
        x=a[c].fillna(fill).to_numpy();mu=np.dot(cw,x)/cw.sum();sd=np.sqrt(np.dot(cw,(x-mu)**2)/cw.sum())
        if sd<=1e-12:continue
        active.append(c);train_cols.append((x-mu)/sd);test_cols.append((b[c].fillna(fill).to_numpy()-mu)/sd)
    x=np.column_stack([np.ones(len(a))]+train_cols)
    future=np.column_stack([np.ones(len(b))]+test_cols)
    z=pd.DataFrame(x,index=years).loc[train.cycle].to_numpy();v=np.repeat(future,len(test),axis=0)
    states=sorted(train.geography.unique()) if architecture=='state' else []
    matrix=np.column_stack([z]+[z*train.geography.eq(s).to_numpy()[:,None] for s in states])
    test_matrix=np.column_stack([v]+[v*test.geography.eq(s).to_numpy()[:,None] for s in states])
    weights=train.cycle.map(dict(zip(years,cw))).to_numpy()/train.groupby('cycle').cycle.transform('size').to_numpy()
    if mode=='direct':train_offset=np.zeros(len(train));test_offset=np.zeros(len(test))
    else:
        col='prior' if mode=='prior' else 'poll_baseline'
        train_offset=train[col].to_numpy();test_offset=test[col].to_numpy()
    penalties=[0.]+[alpha]*len(active)+[state_penalty]*(len(states)*(len(active)+1))
    gram=matrix.T@(weights[:,None]*matrix);system=gram+np.diag(penalties)
    beta=np.linalg.solve(system,matrix.T@(weights*(train.actual.to_numpy()-train_offset)))
    pred=np.clip(test_offset+test_matrix@beta,-1,1)
    df=float(np.trace(np.linalg.solve(system,gram)))
    k=len(active)+1;terms=['intercept']+active
    shared=dict(zip(terms,map(float,beta[:k])))
    deviations={s:dict(zip(terms,map(float,beta[k+i*k:k+(i+1)*k]))) for i,s in enumerate(states)}
    return pred,shared,deviations,df
