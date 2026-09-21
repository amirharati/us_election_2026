"""Chronological fusion of saved out-of-cycle Senate forecasts (not fitted values)."""
import numpy as np
import pandas as pd

INPUTS=['polling','bias','momentum','bias_momentum','direct','prior','latest_result']
ARMS={'fusion_all':INPUTS,
      'fusion_prior':['bias','direct','prior'],
      'fusion_latest':['bias','direct','latest_result']}
ALPHAS=[.1,1.,10.,100.]
KEYS=['scenario','target_id']


def build_inputs(stack,direct,history,membership):
    mapping={'polling':'polling','bias':'base_fixed5_8','momentum':'momentum_shared__half8',
             'bias_momentum':'stack_fixed5_8__half8','prior':'prior'}
    base=stack[stack.model.eq('polling')].drop(columns=['model','prediction']).copy()
    if base.duplicated(KEYS).any():raise ValueError('Duplicate target')
    # Require exact matching support and target metadata; never silently inner-join gaps.
    for name,model in {**mapping,'direct':'direct_all__selected'}.items():
        source=direct if name=='direct' else stack
        q=source[source.model.eq(model)]
        if set(map(tuple,q[KEYS].to_numpy()))!=set(map(tuple,base[KEYS].to_numpy())):
            raise ValueError('Base model target coverage differs')
        q=q[KEYS+['actual','cycle','geography','prediction']]
        joined=base[KEYS+['actual','cycle','geography']].merge(q,on=KEYS,validate='one_to_one',suffixes=('_a','_b'))
        for c in ['actual','cycle','geography']:
            if not (joined[c+'_a'].eq(joined[c+'_b'])|(joined[c+'_a'].isna()&joined[c+'_b'].isna())).all():
                raise ValueError('Conflicting model metadata')
        if name in base:base=base.drop(columns=name)
        base=base.merge(q[KEYS+['prediction']].rename(columns={'prediction':name}),on=KEYS,validate='one_to_one')
    values=[];cycles=[];basis=[]
    for row in base.itertuples():
        old=history[history.scenario.eq(row.scenario)&history.kind.eq('senate')&history.geography.eq(row.geography)
                    &history.cycle.lt(row.cycle)&history.actual.notna()]
        if len(old):
            y=int(old.cycle.max());values.append(float(old.loc[old.cycle.eq(y),'actual'].mean()))
            cycles.append(y);basis.append('latest_earlier_state_senate_cycle_mean')
        else:values.append(row.prior);cycles.append(np.nan);basis.append('existing_prior_fallback_no_senate_history')
    base['latest_result']=values;base['latest_result_cycle']=cycles;base['latest_result_basis']=basis
    m=membership[membership.threshold_pp.eq(10)][['cycle','geography','selection']]
    base=base.merge(m,on=['cycle','geography'],how='left',validate='many_to_one')
    if base.selection.isna().any() or not np.isfinite(base[INPUTS]).all().all():raise ValueError('Incomplete inputs')
    return base


def fit_fusion(train,test,columns,alpha):
    if train.empty or test.empty or train.cycle.max()>=test.cycle.min() or train.actual.isna().any():
        raise ValueError('Known earlier-cycle training required')
    x=train[columns].to_numpy(float);v=test[columns].to_numpy(float)
    if not np.isfinite(x).all() or not np.isfinite(v).all():raise ValueError('Finite base predictions required')
    w=1/train.groupby('cycle').cycle.transform('size').to_numpy()
    mu=np.average(x,axis=0,weights=w);sd=np.sqrt(np.average((x-mu)**2,axis=0,weights=w))
    active=sd>1e-12;scale=np.where(active,sd,1.)
    z=np.column_stack([np.ones(len(x)),((x-mu)/scale)[:,active]])
    future=np.column_stack([np.ones(len(v)),((v-mu)/scale)[:,active]])
    penalty=np.diag([0.]+[float(alpha)]*int(active.sum()))
    gram=z.T@(w[:,None]*z);normal=gram+penalty
    coef=np.linalg.solve(normal,z.T@(w*train.actual.to_numpy()))
    raw=np.zeros(len(columns));raw[active]=coef[1:]/scale[active]
    intercept=float(coef[0]-mu@raw)
    pred=np.clip(future@coef,-1,1)
    fit=dict(columns=list(columns),alpha=float(alpha),intercept=intercept,coefficients=dict(zip(columns,map(float,raw))),
        standardized_coefficients=coef.tolist(),centers=mu.tolist(),scales=scale.tolist(),active=active.tolist(),
        nominal_parameters=1+len(columns),effective_df=float(np.trace(np.linalg.solve(normal,gram))),
        train_cycles=sorted(map(int,train.cycle.unique())),train_rows=len(train),
        clipped_predictions=int((np.abs(future@coef)>1).sum()))
    return pred,fit


def evaluate(inputs,min_inner_cycles=3):
    parts=[];fits=[];grids=[];folds=[]
    for scenario,source in inputs.groupby('scenario',sort=True):
        for year in sorted(source.cycle.unique()):
            test=source[source.cycle.eq(year)]
            train=source[source.cycle.lt(year)&source.actual.notna()]
            inner=train[train.cycle.lt(year-2)];valid=train[train.cycle.eq(year-2)]
            eligible=inner.cycle.nunique()>=min_inner_cycles and len(valid)>0
            status='cv_scored' if test.actual.notna().all() else 'forecast_only_no_outcomes'
            if test.actual.notna().any() and test.actual.isna().any():raise ValueError('Partial cycle labels')
            folds.append(dict(scenario=scenario,cycle=int(year),inner_cycles=int(inner.cycle.nunique()),
                refit_cycles=int(train.cycle.nunique()),inner_rows=len(inner),refit_rows=len(train),
                validation_cycle=int(year-2),validation_rows=len(valid),test_rows=len(test),
                status=status if eligible else 'warm_up_insufficient_meta_history'))
            if not eligible:continue
            common=test.copy();common['status']=status
            for name in INPUTS:
                parts.append(common.assign(model=name,prediction=test[name].to_numpy()))
            parts.append(common.assign(model='equal_average',prediction=test[INPUTS].mean(axis=1).to_numpy()))
            for name,columns in ARMS.items():
                candidates=[]
                for alpha in ALPHAS:
                    p,_=fit_fusion(inner,valid,columns,alpha)
                    loss=float(np.abs(p-valid.actual.to_numpy()).mean())
                    candidates.append((loss,alpha))
                    grids.append(dict(scenario=scenario,cycle=int(year),model=name,alpha=alpha,
                        validation_cycle=int(year-2),training_max_cycle=int(inner.cycle.max()),validation_mae_pp=100*loss))
                loss,alpha=min(candidates,key=lambda v:(round(v[0],12),-v[1]))
                p,f=fit_fusion(train,test,columns,alpha)
                f.update(scenario=scenario,cycle=int(year),model=name,validation_mae_pp=100*loss,validation_cycle=int(year-2))
                fits.append(f);parts.append(common.assign(model=name,prediction=p))
    return pd.concat(parts,ignore_index=True),pd.DataFrame(folds),pd.DataFrame(grids),fits


def correlations(inputs):
    rows=[]
    for (scenario,),source in inputs[inputs.actual.notna()].groupby(['scenario']):
        for period,q in [('all_2012_onward',source),('recent_2016_onward',source[source.cycle.ge(2016)])]:
            for subset,g in [('all',q),('competitive',q[q.selection.eq('competitive')]),
                             ('not_selected',q[q.selection.eq('not_selected')]),('unknown',q[q.selection.eq('unknown_history')]),
                             ('polled',q[q.n_samples.gt(0)]),('no_polls',q[q.n_samples.eq(0)])]:
                if len(g)<3:continue
                pred=g[INPUTS];err=pred.subtract(g.actual,axis=0)
                centered=err-err.groupby(g.cycle).transform('mean')
                for kind,values in [('prediction',pred),('error',err),('within_cycle_error',centered)]:
                    corr=values.corr()
                    for a in INPUTS:
                        for b in INPUTS:
                            rows.append(dict(scenario=scenario,period=period,subset=subset,kind=kind,
                                model_a=a,model_b=b,r=corr.loc[a,b],n=len(g),cycles=int(g.cycle.nunique())))
        for year,g in source.groupby('cycle'):
            for kind,v in [('prediction',g[INPUTS]),('error',g[INPUTS].subtract(g.actual,axis=0))]:
                c=v.corr()
                for a in INPUTS:
                    for b in INPUTS:rows.append(dict(scenario=scenario,period=str(year),subset='all',kind=kind,
                        model_a=a,model_b=b,r=c.loc[a,b],n=len(g),cycles=1))
    return pd.DataFrame(rows)
