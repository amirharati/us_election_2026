"""Direct state regression and controlled recency/offset comparisons.

All variants use the same partially pooled four-score state regression. Time
weights retain all earlier cycles and have mean one, preserving penalty units.
"""
import numpy as np
import pandas as pd
from feature_scores import FixedFeatureScores, MODEL_COLUMNS
from score_baselines import ALPHAS
from state_score_baselines import solve_partial, STATE_PENALTIES
from poll_error_baselines import correction_folds
from cycle_cv import MIN_INNER_CYCLES

HALF_LIVES = {'equal': None, 'half8': 8., 'half16': 16.}
ARMS = {'direct_all': ('direct', False), 'prior_all': ('prior', False),
        'prior_since_poll_start': ('prior', False),
        'prior_polled': ('prior', True), 'polling_polled': ('polling', True)}


def cycle_weights(cycles, target_cycle, half_life):
    years = np.asarray(cycles, dtype=float)
    if len(years)==0 or len(set(years))!=len(years) or not (years<target_cycle).all():
        raise ValueError('Distinct past training cycles required')
    if half_life is not None and (not np.isfinite(half_life) or half_life<=0):
        raise ValueError('Positive half-life or None required')
    raw = np.ones(len(years)) if half_life is None else np.exp2(-(target_cycle-years)/half_life)
    weights = raw/raw.mean()
    return weights, float(weights.sum()**2/(weights@weights))


def weighted_median(values, weights):
    values,weights = np.asarray(values,dtype=float),np.asarray(weights,dtype=float)
    order=np.argsort(values,kind='stable');v=values[order];w=weights[order]
    half=w.sum()/2;cs=w.cumsum();i=int(np.searchsorted(cs,half))
    if i<len(v)-1 and np.isclose(cs[i],half,rtol=0,atol=1e-12*w.sum()):
        return float((v[i]+v[i+1])/2)
    return float(v[i])


class WeightedScoreDesign:
    def fit(self, calendars, weights):
        weights=np.asarray(weights,dtype=float)
        if len(weights)!=len(calendars) or not np.isfinite(weights).all() or not (weights>0).all():
            raise ValueError('Positive weights aligned with training calendars required')
        self.summary=FixedFeatureScores().fit(calendars)
        for c,stat in self.summary.stats.items():
            values=calendars[c].to_numpy(dtype=float);known=np.isfinite(values)
            if not known.any():
                stat['effective_values']=0.;continue
            v,w=values[known],weights[known]
            mean=float(np.average(v,weights=w));sd=float(np.sqrt(np.average((v-mean)**2,weights=w)))
            stat.update(mean=mean,scale=sd,center=0. if self.summary.specs[c]['center']=='zero' else mean,
                effective_values=float(w.sum()**2/(w@w)),
                status='insufficient_history' if len(v)<self.summary.config['minimum_history_values'] else ('ok' if sd>1e-12 else 'constant_history'))
        scores,_=self.summary.transform(calendars)
        self.active=[];self.fills={};self.centers={};self.scales={};self.dropped={}
        for c in MODEL_COLUMNS:
            values=scores[c].to_numpy(dtype=float);known=np.isfinite(values)
            if not known.any():
                self.dropped[c]='all_missing_training';continue
            fill=weighted_median(values[known],weights[known]);self.fills[c]=fill
            filled=np.where(known,values,fill)
            mu=float(np.average(filled,weights=weights));sd=float(np.sqrt(np.average((filled-mu)**2,weights=weights)))
            if sd<=1e-12:
                self.dropped[c]='constant_after_weighted_median_fill';continue
            self.active.append(c);self.centers[c]=mu;self.scales[c]=sd
        return self

    def transform(self, calendars, require_later=False):
        scores,_=self.summary.transform(calendars,require_later=require_later)
        x=np.column_stack([(scores[c].astype(float).fillna(self.fills[c]).to_numpy()-self.centers[c])/self.scales[c]
            for c in self.active]) if self.active else np.zeros((len(calendars),0))
        return x,scores

    def metadata(self):
        normalizer=self.summary.metadata()
        normalizer['normalization']='training-cycle time-weighted component mean/population SD; fixed centers/directions/ingredient weights'
        return dict(normalizer=normalizer,active_terms=self.active,score_fills=self.fills,
            score_centers=self.centers,score_scales=self.scales,dropped_terms=self.dropped,
            final_scaling='time-weighted training median fill, then weighted mean/population SD, including binary')


def offset(frame, mode):
    if mode=='direct':return np.zeros(len(frame))
    if mode=='prior':return frame.prior.to_numpy(dtype=float,copy=True)
    if mode=='polling':return frame.poll_baseline.to_numpy(dtype=float,copy=True)
    raise ValueError('Unknown target/offset mode')


def prepare_problem(train,test,calendars,mode,half_life):
    if train.empty or test.empty or train.actual.isna().any() or train.cycle.max()>=test.cycle.min():
        raise ValueError('Known past training labels and later forecast rows required')
    if test.cycle.nunique()!=1 or not train.kind.eq('senate').all() or not test.kind.eq('senate').all():
        raise ValueError('One Senate forecast cycle required')
    if calendars.cycle.duplicated().any() or train.geography.isna().any() or test.geography.isna().any():
        raise ValueError('Unique calendars and known state identities required')
    years=sorted(train.cycle.unique());target=int(test.cycle.iloc[0])
    cw,ess=cycle_weights(years,target,half_life)
    cal=calendars.set_index('cycle',drop=False)
    trcal=cal.loc[years].reset_index(drop=True);tecal=cal.loc[[target]].reset_index(drop=True)
    design=WeightedScoreDesign().fit(trcal,cw)
    x,scores=design.transform(trcal);v,test_scores=design.transform(tecal,require_later=True)
    z=pd.DataFrame(np.column_stack([np.ones(len(x)),x]),index=years).loc[train.cycle].to_numpy()
    future=np.repeat(np.column_stack([np.ones(len(v)),v]),len(test),axis=0)
    by_year=pd.Series(cw,index=years)
    row_weights=train.cycle.map(by_year).to_numpy()/train.groupby('cycle').cycle.transform('size').to_numpy()
    response=train.actual.to_numpy()-offset(train,mode)
    if not np.isfinite(response).all() or not np.isfinite(offset(test,mode)).all():
        raise ValueError('Finite targets and offsets required')
    return dict(train=train,test=test,design=design,z=z,future=future,response=response,
        weights=row_weights,cycle_weights=by_year,effective_cycles=ess,mode=mode,half_life=half_life,
        scores=scores,test_scores=test_scores)


def predict_problem(problem,alpha,state_penalty,details=False):
    p=problem;train,test=p['train'],p['test'];design=p['design'];terms=['intercept']+design.active
    shared,deviations,complexity=solve_partial(p['z'],p['response'],p['weights'],
        train.geography.to_numpy(),alpha,state_penalty,'state_partial')
    effect=np.array([p['future'][i]@(shared+deviations.get(row.geography,np.zeros(len(terms)))) for i,row in enumerate(test.itertuples())])
    raw=offset(test,p['mode'])+effect;prediction=np.clip(raw,-1,1)
    if not details:return prediction,None,None
    states={};coefficients=[]
    for state in sorted(set(train.geography)|set(test.geography)):
        delta=deviations.get(state,np.zeros(len(terms)));total=shared+delta
        mask=train.geography.eq(state).to_numpy();tr=train[mask]
        sw=pd.Series(p['weights'][mask],index=tr.cycle).groupby(level=0).sum().to_numpy()
        raw_coef=total.copy()
        if design.active:
            raw_coef[1:]/=np.array([design.scales[c] for c in design.active])
            raw_coef[0]-=sum(raw_coef[j+1]*design.centers[c] for j,c in enumerate(design.active))
        state_info=dict(training_rows=len(tr),training_cycles=int(tr.cycle.nunique()),
            effective_cycles=float(sw.sum()**2/(sw@sw)) if len(sw) else 0.,
            status='state_coefficients' if len(tr) else 'shared_only_no_state_history',
            deviation=dict(zip(terms,map(float,delta))),total=dict(zip(terms,map(float,total))),
            raw_total=dict(zip(terms,map(float,raw_coef))))
        states[state]=state_info
        for j,term in enumerate(terms):
            coefficients.append(dict(geography=state,term=term,shared_coefficient=float(shared[j]),
                state_deviation=float(delta[j]),total_coefficient=float(total[j]),
                raw_total_coefficient=float(raw_coef[j]),training_rows=len(tr),
                training_cycles=int(tr.cycle.nunique()),effective_cycles=state_info['effective_cycles'],state_status=state_info['status']))
    info=dict(status='fitted',target_mode=p['mode'],half_life_years=p['half_life'],
        alpha=float(alpha),state_penalty=float(state_penalty),training_rows=len(train),
        training_cycles=int(train.cycle.nunique()),training_states=int(train.geography.nunique()),
        training_first_cycle=int(train.cycle.min()),training_max_cycle=int(train.cycle.max()),effective_cycles=p['effective_cycles'],
        cycle_weights={str(int(c)):float(w) for c,w in p['cycle_weights'].items()},
        weight_sum=float(p['weights'].sum()),weight_rule='raw 2^(-(forecast_cycle-cycle)/half_life); normalize cycle weights to mean one; divide within cycle by contest count',
        shared_coefficients=dict(zip(terms,map(float,shared))),states=states,
        clipped_predictions=int((np.abs(raw)>1).sum()),**complexity,**design.metadata())
    info['training_score_rows']=p['scores'][['cycle']+MODEL_COLUMNS].replace({np.nan:None}).to_dict('records')
    info['test_score_rows']=p['test_scores'][['cycle']+MODEL_COLUMNS].replace({np.nan:None}).to_dict('records')
    return prediction,info,pd.DataFrame(coefficients)


def evaluate_recency(targets,history,calendars,scenario,start_cycle=2002,
                     min_inner_cycles=MIN_INNER_CYCLES,arms=None):
    names=list(ARMS) if arms is None else list(arms)
    if not names or len(names)!=len(set(names)) or not set(names)<=set(ARMS):
        raise ValueError('Unknown or duplicate arm')
    source=history[history.scenario.eq(scenario)&history.kind.eq('senate')].copy()
    folds=correction_folds(targets,source,scenario,start_cycle,min_inner_cycles)
    cal=calendars[calendars.scenario.eq(scenario)]
    predictions=[];tuning=[];fits=[];coefficients=[]
    for fold in folds.itertuples():
        if fold.status not in ['cv_scored','forecast_only_no_outcomes','incomplete_test_outcomes']:continue
        year=int(fold.cycle);test=source[source.cycle.eq(year)]
        past=source[source.cycle.lt(year)&source.actual.notna()]
        common=test[['target_id','cycle','kind','geography','actual','n_samples','prior','prior_basis','poll_baseline']].copy()
        for name,column in [('prior','prior'),('polling','poll_baseline')]:
            predictions.append(common.assign(scenario=scenario,model=name,prediction=test[column].to_numpy(),
                prediction_status='reference'))
        for arm in names:
            mode,polled_only=ARMS[arm]
            train=past[past.n_samples.gt(0)] if polled_only else past
            if arm=='prior_since_poll_start':
                # Date-range control, retaining unpolled contests within that range.
                first_poll_cycle=int(past.loc[past.n_samples.gt(0),'cycle'].min())
                train=train[train.cycle.ge(first_poll_cycle)]
            forecast=test[test.n_samples.gt(0)] if polled_only else test
            inner=train[train.cycle.lt(year-2)];valid=train[train.cycle.eq(year-2)]
            if valid.empty:raise ValueError('Previous-cycle validation support required')
            fit_forecast=forecast if len(forecast) else test.iloc[:1]
            selected={};finals={}
            for strategy,half in HALF_LIVES.items():
                problem=prepare_problem(inner,valid,cal,mode,half)
                candidates=[]
                for alpha in ALPHAS:
                    for penalty in STATE_PENALTIES:
                        vp,_,_=predict_problem(problem,alpha,penalty)
                        loss=float(np.mean(np.abs(vp-valid.actual.to_numpy())))
                        candidates.append((loss,alpha,penalty))
                        tuning.append(dict(scenario=scenario,cycle=year,arm=arm,weight_strategy=strategy,
                            half_life_years=half,validation_cycle=year-2,training_max_cycle=int(inner.cycle.max()),
                            training_rows=len(inner),training_cycles=int(inner.cycle.nunique()),
                            effective_cycles=problem['effective_cycles'],validation_rows=len(valid),
                            alpha=alpha,state_penalty=penalty,validation_mae_pp=100*loss))
                loss,alpha,penalty=min(candidates,key=lambda v:(round(v[0],12),-v[2],-v[1]))
                selected[strategy]=(loss,alpha,penalty)
                final_problem=prepare_problem(train,fit_forecast,cal,mode,half)
                pp,fit,coef=predict_problem(final_problem,alpha,penalty,details=True)
                fit.update(arm=arm,scenario=scenario,cycle=year,validation_cycle=year-2,
                    selected_validation_mae_pp=100*loss,polled_training_only=polled_only,
                    polled_validation_only=polled_only,applied_rows=len(forecast),unchanged_no_poll_rows=len(test)-len(forecast))
                final_prediction=pd.Series(offset(test,mode),index=test.index)
                if len(forecast):final_prediction.loc[forecast.index]=pp
                row_status=pd.Series('unchanged_no_poll_fallback',index=test.index)
                for i,row in forecast.iterrows():row_status.loc[i]=fit['states'][row.geography]['status']
                finals[strategy]=(final_prediction,fit,coef,row_status)
            # A separately reported past-only selection; no outer-test label enters this choice.
            preference={'equal':0,'half16':1,'half8':2}
            chosen=min(selected,key=lambda s:(round(selected[s][0],12),preference[s],-selected[s][2],-selected[s][1]))
            for label,strategy in [(s,s) for s in HALF_LIVES]+[('selected',chosen)]:
                pred,fit,coef,row_status=finals[strategy]
                model=arm+'__'+label
                f=dict(fit,model=model,weight_strategy=label,selected_weight_strategy=strategy)
                fits.append(f)
                coefficients.append(coef.assign(scenario=scenario,cycle=year,model=model,arm=arm,
                    weight_strategy=label,selected_weight_strategy=strategy))
                predictions.append(common.assign(scenario=scenario,model=model,arm=arm,weight_strategy=label,
                    selected_weight_strategy=strategy,prediction=pred.to_numpy(),prediction_status=row_status.to_numpy(),
                    adjustment_vs_prior_pp=100*(pred.to_numpy()-test.prior.to_numpy()),
                    adjustment_vs_polling_pp=100*(pred.to_numpy()-test.poll_baseline.to_numpy())))
    concat=lambda rows:pd.concat(rows,ignore_index=True) if rows else pd.DataFrame()
    return concat(predictions),pd.DataFrame(tuning),fits,concat(coefficients),folds
