"""Older Gaussian/Student pair on exactly the main model's polling evidence.

Historical calibration is retained from the earlier architecture. This supplies
alternatives, not a fresh training run or additional independent evidence.
"""
import numpy as np
import pandas as pd
import election_lab as lab

OLD_GAUSSIAN='Older Gaussian'
OLD_STUDENT='Student-t research helper'
MATCHED_STUDENT='Matched Student-t (df5)'


def older_pair(main_rows,calendar=None,include_student=True):
    """Return paired posterior tables/joint draws and MCMC diagnostics.

The caller supplies one cycle/horizon. calendar replaces current context only;
feature normalization and coefficient fits remain historical and frozen.
"""
    sc=main_rows.scenario.iloc[0];year=int(main_rows.cycle.iloc[0])
    q=pd.read_parquet(lab.ASSETS/'student/base_predictions.parquet')
    q=q[q.scenario.eq(sc)&q.cycle.eq(year)].sort_values('target_id').reset_index(drop=True)
    if list(q.target_id)!=list(main_rows.target_id):raise ValueError('Alternative contest mapping changed')
    for c in ['q_pp','firm_mass','sample_count','as_of','context_id','actual']:
        if c in main_rows:q[c]=main_rows[c].to_numpy()
    folds=pd.read_parquet(lab.ASSETS/'student/folds.parquet')
    row=folds[folds.scenario.eq(sc)&folds.cycle.eq(year)].iloc[0]
    fit=dict(np.load(lab.ASSETS/'student_base'/row.source_fit_path));fit['a']=float(fit['a'])
    if fit['years'].max()>=year:raise ValueError('Future alternative training data')
    if calendar is not None:
        design,_,z,*_=lab.features.prepare_design(calendar,fit['years'],fit['training_weights'],year)
        fit['z']=z[[design.active.index(t) for t in fit['terms']]]
    g,C,_,prior=lab.features.predict(q,fit['budget'],lab.load_poll(sc,year),fit,fit['z'])
    gp=lab.scored(g,OLD_GAUSSIAN)
    seed=lab.SEED+year+10000*(sc=='oct31')
    gd=gp.margin_pp.to_numpy()+np.random.default_rng(seed).standard_normal((lab.DRAWS,len(q)))@np.linalg.cholesky(C).T
    result={OLD_GAUSSIAN:dict(predictions=gp,draws=gd,covariance=C)}
    diagnostics=[]
    if include_student:
        sp,d=lab.rerun_student(sc,year,test=q,feature_z=fit['z'])
        result[OLD_STUDENT]=dict(predictions=sp,draws=d['samples'],covariance=d['covariance'])
        diagnostics.append(d['diagnostics'].assign(model=OLD_STUDENT))
    return result,diagnostics


def matched_tail(main_rows,fit,lam,expected_covariance):
    import matched_student as student
    sc=main_rows.scenario.iloc[0];year=int(main_rows.cycle.iloc[0])
    args=student.inputs(main_rows,fit,lam,lab.load_poll(sc,year))
    (mean,cov),K=student.control(args)
    np.testing.assert_allclose(mean,main_rows.prediction_pp,atol=1e-8)
    np.testing.assert_allclose(cov,expected_covariance,atol=1e-8)
    result=student.sample(*args,nu=5,seed=lab.SEED+year+10000*(sc=='oct31'))
    pred=student.scored(main_rows,result)
    # Common tables need the contest mapping retained for display/accounting.
    for col in ['as_of','outcome_type','special']:
        if col in main_rows:pred[col]=main_rows[col].to_numpy()
    return dict(predictions=pred,draws=result['samples'],covariance=result['covariance']),result['diagnostics'].assign(model=MATCHED_STUDENT)
