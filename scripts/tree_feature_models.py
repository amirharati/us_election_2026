"""Chronological, cycle-balanced trees and whole-cycle bootstrap forests.

No polls in these predictors. Feature importance is diagnostic; never select
features from outer-test outcomes before reusing those outcomes as evaluation.
"""
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor,export_text
from feature_scores import FixedFeatureScores,MODEL_COLUMNS

DEPTHS=[2,4,8]
N_TREES=100
SEED=20260918
RAW_GROUPS={
 'sentiment':['consumer_sentiment_3m','personal_finances_better_3m_pct','issue_salience_economy'],
 'prices':['inflation_yoy_pct','cpi_24m_pct','gasoline_yoy_pct'],
 'employment_growth':['unemployment_pct','real_income_yoy_pct','real_gdp_yoy_pct'],
 'markets_uncertainty':['market_excess_return_3m_pct','vix_3m','epu_3m'],
 'approval':['approval_3m_pct','approval_dem_3m_pct','approval_rep_3m_pct'],
 'war_disruption':['gpr_3m','infectious_news_3m','covid_stringency_3m',
                   'health_disruption_4y','financial_disruption_4y','security_disruption_4y','extraordinary_event_any_4y'],
 'political':['wh_dem','house_dem','senate_dem','unified_government','split_congress',
              'wh_matches_house','wh_matches_senate','wh_party_days_in_power','is_presidential_cycle']}
for name,stem in [('sentiment','consumer_sentiment_3m'),('prices','inflation_yoy_pct'),
                  ('employment_growth','unemployment_pct'),('approval','approval_3m_pct')]:
    RAW_GROUPS[name]+=[stem+'__'+suffix for suffix in ['start_jan01','previous_oct31','change_jan01','change_previous_oct31']]
RAW_GROUPS['prices'] += [c+'__pct_change_'+a for c in ['cpi_level','gasoline_cpi_level'] for a in ['jan01','previous_oct31']]
BINARY={'disruption_any','wh_dem','house_dem','senate_dem','unified_government','split_congress','wh_matches_house',
 'wh_matches_senate','is_presidential_cycle','health_disruption_4y','financial_disruption_4y',
 'security_disruption_4y','extraordinary_event_any_4y'}


class TreeDesign:
    def __init__(self,feature_set):
        if feature_set not in ['scores','raw']:raise ValueError('Unknown feature set')
        self.feature_set=feature_set

    def materialize(self,cal):
        q=cal.copy();q['is_presidential_cycle']=q.cycle.mod(4).eq(0).astype(float)
        if self.feature_set=='scores':
            scored,_=self.scorer.transform(q)
            q=scored[MODEL_COLUMNS].copy();q.index=cal.index
        return q

    def fit(self,cal,states):
        if cal.cycle.duplicated().any() or cal.scenario.nunique()!=1:raise ValueError('Unique same-horizon cycle calendars required')
        self.training_cycles=sorted(map(int,cal.cycle.unique()))
        if self.feature_set=='scores':self.scorer=FixedFeatureScores().fit(cal)
        q=self.materialize(cal)
        groups=({c:[c] for c in MODEL_COLUMNS} if self.feature_set=='scores' else RAW_GROUPS)
        self.stats={};self.names=[];self.groups=[];self.dropped={}
        for group,columns in groups.items():
            for c in columns:
                s=q[c].astype(float)
                if np.isinf(s).any():raise ValueError('Infinite feature')
                if not s.notna().any():self.dropped[c]='all_missing_training';continue
                fill=float(s.mode().iloc[0] if c in BINARY else s.median())
                mu=0. if c in BINARY else float(s.fillna(fill).mean())
                sd=1. if c in BINARY else float(s.fillna(fill).std(ddof=0))
                if sd<1e-12:sd=1.
                # Trees do not require scaling; this preserves consistent WH-signed interactions.
                self.stats[c]={'fill':fill,'center':mu,'scale':sd,'group':group,'missing':bool(s.isna().any()),
                    'signed':self.feature_set=='raw' and group!='political'}
                self.names.append(c);self.groups.append(group)
                if self.stats[c]['missing']:self.names.append(c+'__missing');self.groups.append(group)
                if self.stats[c]['signed']:self.names.append(c+'__x_wh_sign');self.groups.append(group)
        self.wh_fill=float(cal.wh_dem.mode().iloc[0]) if cal.wh_dem.notna().any() else .5
        self.states=sorted(set(states))
        for state in self.states:self.names.append('state_'+state);self.groups.append('state_identity')
        return self

    def transform(self,frame,cal):
        q=self.materialize(cal);q.index=cal.cycle
        sign=pd.Series(2*cal.wh_dem.fillna(self.wh_fill).to_numpy()-1,index=cal.cycle)
        values=[]
        for c,s in self.stats.items():
            z=(q[c].fillna(s['fill'])-s['center'])/s['scale']
            values.append(frame.cycle.map(z).to_numpy(float))
            if s['missing']:values.append(frame.cycle.map(q[c].isna().astype(float)).to_numpy(float))
            if s['signed']:values.append(frame.cycle.map(z*sign).to_numpy(float))
        values += [frame.geography.eq(state).to_numpy(float) for state in self.states]
        x=np.column_stack(values)
        if not np.isfinite(x).all():raise ValueError('Nonfinite or absent transformed features')
        return x

    def metadata(self):
        return dict(feature_set=self.feature_set,training_cycles=self.training_cycles,names=self.names,groups=self.groups,
                    stats=self.stats,dropped=self.dropped,states=self.states,wh_fill=self.wh_fill,
                    score_normalizer=self.scorer.metadata() if self.feature_set=='scores' else None)


def prepare(train,test,calendars,feature_set,mode):
    if train.empty or test.empty or train.actual.isna().any() or train.cycle.max()>=test.cycle.min():raise ValueError('Known earlier training required')
    if test.cycle.nunique()!=1:raise ValueError('One held-out cycle required')
    if mode not in ['direct','prior']:raise ValueError('Unknown response')
    if not train.kind.eq('senate').all() or not test.kind.eq('senate').all():raise ValueError('Senate only')
    cal=calendars.set_index('cycle',drop=False)
    trcal=cal.loc[sorted(train.cycle.unique())].reset_index(drop=True)
    tecal=cal.loc[sorted(test.cycle.unique())].reset_index(drop=True)
    design=TreeDesign(feature_set).fit(trcal,train.geography)
    x=design.transform(train,trcal);v=design.transform(test,tecal)
    weights=1/train.groupby('cycle').cycle.transform('size').to_numpy()
    response=train.actual.to_numpy()-(train.prior.to_numpy() if mode=='prior' else 0.)
    offset=test.prior.to_numpy() if mode=='prior' else np.zeros(len(test))
    return dict(x=x,v=v,weights=weights,response=response,offset=offset,design=design,train=train,test=test,mode=mode)


def fit_predict(problem,family,depth,drop_group=None,n_trees=N_TREES,details=False):
    if family not in ['tree','forest']:raise ValueError('Unknown tree family')
    p=problem;keep=np.array([g!=drop_group for g in p['design'].groups])
    x=p['x'][:,keep];v=p['v'][:,keep]
    names=np.array(p['design'].names)[keep];groups=np.array(p['design'].groups)[keep]
    years=sorted(p['train'].cycle.unique());cy=p['train'].cycle.to_numpy()
    rng=np.random.default_rng(SEED);estimators=[];predictions=[];min_cycles=[];draws=[]
    for i in range(1 if family=='tree' else n_trees):
        if family=='tree':counts={int(y):1 for y in years}
        else:
            sampled=rng.choice(years,size=len(years),replace=True)
            counts={int(y):int((sampled==y).sum()) for y in years}
        w=p['weights']*np.array([counts[int(y)] for y in cy]);mask=w>0
        est=DecisionTreeRegressor(max_depth=depth,min_samples_leaf=5,min_weight_fraction_leaf=.01,
            max_features=1. if family=='tree' else .7,random_state=SEED+i)
        est.fit(x[mask],p['response'][mask],sample_weight=w[mask]);estimators.append(est)
        predictions.append(est.predict(v))
        if details:
            leaves=est.apply(x[mask]);observed=cy[mask]
            min_cycles.append(min(len(set(observed[leaves==leaf])) for leaf in set(leaves)))
            draws.append(counts)
    prediction=np.clip(p['offset']+np.mean(predictions,axis=0),-1,1)
    if not details:return prediction,None,None
    importance=np.mean([e.feature_importances_ for e in estimators],axis=0)
    imp=pd.DataFrame(dict(feature=names,group=groups,impurity_importance=importance))
    info=dict(family=family,depth=int(depth),mode=p['mode'],feature_set=p['design'].feature_set,
        training_cycles=list(map(int,years)),training_rows=len(p['train']),training_max_cycle=int(max(years)),
        test_cycle=int(p['test'].cycle.iloc[0]),features=len(names),trees=len(estimators),
        mean_leaves=float(np.mean([e.get_n_leaves() for e in estimators])),minimum_distinct_cycles_per_leaf=int(min(min_cycles)),
        minimum_leaf_cycles_by_tree=min_cycles,cycle_bootstrap_counts=draws,preprocessing=p['design'].metadata(),
        rule_text=export_text(estimators[0],feature_names=list(names)) if family=='tree' else None)
    return prediction,info,imp


def evaluate(history,calendars,start_cycle=2012,n_trees=N_TREES,importance_start=2016,progress=None):
    predictions=[];tuning=[];fits=[];imps=[];ablations=[];folds=[]
    for scenario,source in history[history.kind.eq('senate')].groupby('scenario'):
        cal=calendars[calendars.scenario.eq(scenario)]
        for year in sorted(y for y in source.cycle.unique() if y>=start_cycle):
            test=source[source.cycle.eq(year)]
            if scenario=='oct31' and not test.window_complete.all():continue
            train=source[source.cycle.lt(year)&source.actual.notna()]
            inner=train[train.cycle.lt(year-2)];valid=train[train.cycle.eq(year-2)]
            if inner.cycle.nunique()<6 or valid.empty:continue
            status='cv_scored' if test.actual.notna().all() else 'forecast_only_no_outcomes'
            if test.actual.notna().any() and test.actual.isna().any():raise ValueError('Partly known test cycle')
            common=test[['scenario','target_id','cycle','kind','geography','actual','n_samples','prior','prior_basis','poll_baseline']].copy()
            common['status']=status
            folds.append(dict(scenario=scenario,cycle=int(year),status=status,inner_cycles=int(inner.cycle.nunique()),
                inner_rows=len(inner),validation_cycle=int(year-2),validation_rows=len(valid),
                refit_cycles=int(train.cycle.nunique()),refit_rows=len(train),test_rows=len(test)))
            for name,column in [('prior','prior'),('polling','poll_baseline')]:
                predictions.append(common.assign(model=name,prediction=test[column].to_numpy()))
            for feature_set in ['scores','raw']:
                for mode in ['direct','prior']:
                    ip=prepare(inner,valid,cal,feature_set,mode);fp=prepare(train,test,cal,feature_set,mode)
                    for family in ['tree','forest']:
                        model=f'{family}_{feature_set}_{mode}';candidates=[]
                        for depth in DEPTHS:
                            vp,_,_=fit_predict(ip,family,depth,n_trees=n_trees)
                            loss=float(np.abs(vp-valid.actual.to_numpy()).mean());candidates.append((loss,depth))
                            tuning.append(dict(scenario=scenario,cycle=int(year),model=model,depth=depth,
                                validation_cycle=int(year-2),training_max_cycle=int(inner.cycle.max()),mae_pp=100*loss))
                        loss,depth=min(candidates,key=lambda v:(round(v[0],12),v[1]))
                        pp,f,imp=fit_predict(fp,family,depth,n_trees=n_trees,details=True)
                        f.update(scenario=scenario,cycle=int(year),model=model,validation_cycle=int(year-2),validation_mae_pp=100*loss)
                        fits.append(f);imps.append(imp.assign(scenario=scenario,cycle=int(year),model=model))
                        predictions.append(common.assign(model=model,prediction=pp))
                        # Refit group removals with the same preselected depth and random stream.
                        # This is held-out diagnostic importance, not a feature-selection CV result.
                        if family=='forest' and year>=importance_start and status=='cv_scored':
                            baseline=100*np.abs(pp-test.actual.to_numpy()).mean()
                            for group in sorted(set(fp['design'].groups)):
                                ap,_,_=fit_predict(fp,family,depth,drop_group=group,n_trees=n_trees)
                                error=100*np.abs(ap-test.actual.to_numpy()).mean()
                                ablations.append(dict(scenario=scenario,cycle=int(year),model=model,group=group,
                                    depth=depth,n=len(test),base_mae_pp=baseline,without_group_mae_pp=error,
                                    removal_cost_pp=error-baseline,
                                    base_correct=int((np.sign(pp)==np.sign(test.actual)).sum()),
                                    without_correct=int((np.sign(ap)==np.sign(test.actual)).sum())))
            if progress:progress(f'{scenario} {year}: 8 models completed')
    return (pd.concat(predictions,ignore_index=True),pd.DataFrame(folds),pd.DataFrame(tuning),fits,
            pd.concat(imps,ignore_index=True),pd.DataFrame(ablations))
