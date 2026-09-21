"""Transparent margin baselines; chronological last-cycle tuning, no model blending."""
from itertools import product
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

CONTINUOUS = ['consumer_sentiment_3m', 'inflation_yoy_pct', 'unemployment_pct', 'approval_3m_pct']
BINARY = ['wh_dem', 'is_presidential_cycle']
FEATURES = CONTINUOUS + BINARY
HALF_LIVES = [30, 90]
PRIOR_STRENGTHS = [0., 2.]
ALPHAS = [0.1, 1., 10.]
DEFAULT_POLL = (90, 2.)
DEFAULT_ALPHA = 1.
TABLES = ['contest_inputs_reference', 'labels', 'polls', 'poll_quality',
          'poll_identity', 'poll_metadata', 'poll_availability', 'current_contests']


def prepare_inputs(data, contest_inputs=None):
    """Only general-stage comparable outcomes; retain all current rows as diagnostics."""
    inputs = data.load_table('contest_inputs_reference') if contest_inputs is None else contest_inputs.copy()
    labels = data.load_table('labels')
    targets = inputs.merge(labels[['target_id', 'dem_rep_margin', 'diagnostic_eligible',
                                  'status', 'review_reasons']], on='target_id', validate='one_to_one')
    targets = targets.rename(columns={'dem_rep_margin': 'actual', 'status': 'label_status'})
    targets['kind'] = np.where(targets.geography.eq('US'), 'national', 'senate')
    historical_ok = (targets.diagnostic_eligible.eq(True) & targets.actual.notna()
                     & targets.stage.isin(['gen', 'general']) & targets.historical_horizon_comparable)
    targets['included'] = historical_ok | targets.cycle.eq(2026)
    exclusions = targets.loc[~targets.included, ['target_id', 'cycle', 'geography', 'stage', 'review_reasons', 'label_status']].copy()
    targets = targets[targets.included & targets.cycle.mod(2).eq(0)].copy()
    targets = targets.sort_values(['cycle', 'kind', 'geography', 'target_id']).reset_index(drop=True)
    targets = add_priors(targets)

    polls = data.load_table('polls')
    quality = data.load_table('poll_quality')[['observation_id', 'review_status']]
    identity = data.load_table('poll_identity')[['observation_id', 'canonical_firm']]
    metadata = data.load_table('poll_metadata')[['observation_id', 'estimate_basis', 'question_construct']]
    availability = data.load_table('poll_availability')[['observation_id', 'documented_release_date']]
    polls = polls.merge(quality, on='observation_id', validate='one_to_one').merge(identity, on='observation_id', validate='one_to_one')
    polls = polls.drop(columns=['estimate_basis']).merge(metadata, on='observation_id', validate='one_to_one')
    polls = polls.merge(availability, on='observation_id', validate='one_to_one')
    polls = polls.merge(targets[['target_id', 'context_id']].rename(columns={'context_id': 'forecast_cutoff'}),
                        on='target_id', how='left', validate='many_to_one')
    polls['field_end'] = pd.to_datetime(polls.poll_end.fillna(polls.poll_date))
    polls['cutoff'] = pd.to_datetime(polls.forecast_cutoff)
    polls['release'] = pd.to_datetime(polls.documented_release_date)
    polls['age_days'] = (polls.cutoff - polls.field_end).dt.days
    start = pd.to_datetime((polls.cycle-1).astype(str)+'-01-01')
    reason = pd.Series('eligible', index=polls.index)
    # First applicable reason is saved; no result/error-based poll ranking.
    rules = [
        ('excluded_target', polls.forecast_cutoff.isna()),
        ('source_or_matchup_restriction', ~polls.review_status.isin(['usable_retrospective', 'provisional', 'current_screened'])),
        ('missing_margin', polls.dem_rep_margin.isna()),
        ('superseded_version', polls.origin_superseded_by.notna() | polls.superseded_by.notna()),
        ('hypothetical_matchup', polls.hypothetical.eq(True)),
        ('different_question_or_basis', polls.question_construct.eq('congress_control_preference') |
         polls.estimate_basis.isin(['decided', 'forced_choice_followup'])),
        ('missing_field_date', polls.field_end.isna()),
        ('after_forecast_cutoff', polls.field_end.gt(polls.cutoff)),
        ('before_two_year_cycle', polls.field_end.lt(start)),
        ('known_release_after_cutoff', polls.release.gt(polls.cutoff)),
    ]
    for name, mask in rules:reason.loc[reason.eq('eligible') & mask] = name
    polls['baseline_status'] = reason
    audit = polls[['observation_id', 'target_id', 'cycle', 'geography', 'baseline_status', 'field_end', 'cutoff', 'release']].copy()
    eligible = polls[reason.eq('eligible')].copy()
    eligible['canonical_firm'] = eligible.canonical_firm.fillna(eligible.pollster).fillna('unknown')
    eligible['sample_key'] = eligible.canonical_sample_group_id.fillna(eligible.sample_group_id).fillna(eligible.observation_id)
    eligible['basis_rank'] = np.where(eligible.estimate_basis.eq('full_sample'), 0, 1)
    eligible['population_rank'] = eligible.population.map({'lv':0, 'rv':1, 'v':2, 'a':3, 'unknown':4}).fillna(4)
    # One sample contribution per target: prefer full basis, then LV/RV/V/A/unknown;
    # average tied question versions instead of selecting by favorable margin.
    keys = ['target_id', 'sample_key']
    rank = eligible.basis_rank*10 + eligible.population_rank
    best = rank.groupby([eligible[k] for k in keys]).transform('min')
    chosen = eligible[rank.eq(best)].copy()
    waves = chosen.groupby(keys, sort=True).agg(
        margin=('dem_rep_margin','mean'), field_end=('field_end','max'), cutoff=('cutoff','first'),
        firm=('canonical_firm','first'), versions=('observation_id','size'),
        observation_ids=('observation_id', lambda s:'|'.join(s)),
        reported_n=('sample_size','max'), publication_unknown=('release', lambda s:bool(s.isna().any())),
    ).reset_index()
    waves['age_days'] = (waves.cutoff-waves.field_end).dt.days
    selected_ids = set(chosen.observation_id)
    audit.loc[audit.baseline_status.eq('eligible') & ~audit.observation_id.isin(selected_ids), 'baseline_status'] = 'alternative_population_or_basis'
    return targets, waves, audit, exclusions


def add_priors(targets):
    """For every row, only earlier-cycle labels; latest state cycle + old state mean."""
    result = targets.copy();rows=[]
    for row in result.itertuples():
        history = result[(result.kind==row.kind) & (result.cycle<row.cycle) & result.actual.notna()]
        local = history[history.geography.eq(row.geography)]
        if len(local):
            # Tied same-cycle contests are averaged; never silently choose a seat.
            cycle_mean = local.groupby('cycle').actual.mean()
            last = int(cycle_mean.index.max())
            prior = .5*cycle_mean.loc[last] + .5*cycle_mean.mean()
            basis = 'half_latest_same_state_cycle_half_state_history' if row.kind=='senate' else 'half_latest_national_cycle_half_national_history'
            rows.append((prior,last,len(cycle_mean),basis))
        elif row.kind=='senate' and pd.notna(getattr(row,'prior_state_pres_margin',np.nan)):
            # Some states have no admitted Senate margin because of election-rule
            # restrictions. Use an explicitly labeled lagged election result,
            # shared by both baselines, instead of pretending they are identical.
            rows.append((row.prior_state_pres_margin,row.prior_presidential_year,0,'lagged_state_presidential_result_fallback'))
        elif len(history):
            rows.append((history.groupby('cycle').actual.mean().mean(), int(history.cycle.max()),0,'earlier_kind_cycle_mean_fallback'))
        else:rows.append((0.,np.nan,0,'no_earlier_label_neutral_fallback'))
    result[['prior','prior_latest_cycle','prior_state_cycles','prior_basis']] = pd.DataFrame(rows,index=result.index)
    return result


def poll_predict(targets, waves, half_life, prior_strength):
    rows=[]
    grouped={key:frame for key,frame in waves.groupby('target_id')}
    for row in targets.itertuples():
        w=grouped.get(row.target_id)
        if w is None or w.empty:
            rows.append(dict(target_id=row.target_id,prediction=row.prior,n_samples=0,n_firms=0,
                             data_weight=0.,prior_fraction=1.,poll_mean=np.nan,publication_unknown_samples=0))
            continue
        # Equal total firm weight before recency decay. Prior strength is measured
        # in equivalent fresh firms, not respondent counts or question versions.
        weight=np.exp2(-w.age_days.to_numpy()/half_life)/w.groupby('firm').firm.transform('size').to_numpy()
        total=weight.sum();mean=np.dot(weight,w.margin)/total
        prediction=(total*mean+prior_strength*row.prior)/(total+prior_strength)
        rows.append(dict(target_id=row.target_id,prediction=prediction,n_samples=len(w),n_firms=w.firm.nunique(),
                         data_weight=total,prior_fraction=prior_strength/(total+prior_strength),poll_mean=mean,
                         publication_unknown_samples=int(w.publication_unknown.sum())))
    return pd.DataFrame(rows)


class TrainingTransform:
    """Train-only median/mode, continuous standardization and missing indicators."""
    def fit(self, frame):
        self.columns=[c for c in FEATURES if frame[c].notna().any()]
        self.dropped=[c for c in FEATURES if c not in self.columns]
        self.fill={};self.center={};self.scale={};self.indicators=[]
        for c in self.columns:
            s=frame[c].astype(float)
            self.fill[c]=float(s.mode().iloc[0] if c in BINARY else s.median())
            filled=s.fillna(self.fill[c])
            self.center[c]=float(filled.mean()) if c in CONTINUOUS else 0.
            sd=float(filled.std(ddof=0)) if c in CONTINUOUS else 1.
            self.scale[c]=sd if sd>1e-12 else 1.
            if s.isna().any():self.indicators.append(c)
        self.names=self.columns+[c+'__missing' for c in self.indicators]
        return self

    def transform(self, frame):
        a=[(frame[c].astype(float).fillna(self.fill[c]).to_numpy()-self.center[c])/self.scale[c] for c in self.columns]
        a += [frame[c].isna().astype(float).to_numpy() for c in self.indicators]
        return np.column_stack(a) if a else np.zeros((len(frame),0))


def feature_predict(train, test, alpha):
    transform=TrainingTransform().fit(train)
    info=dict(training_rows=len(train),training_cycles=int(train.cycle.nunique()),
              training_max_cycle=int(train.cycle.max()) if len(train) else None,
              fills=transform.fill,centers=transform.center,scales=transform.scale,
              dropped=transform.dropped,indicators=transform.indicators)
    if train.cycle.nunique()<3 or not transform.names:
        info.update(status='insufficient_history_prior_only',coefficients={})
        return test.prior.to_numpy(dtype=float),info
    model=Ridge(alpha=alpha)
    # Every cycle has total loss weight one; states sharing national inputs do
    # not give a cycle with more eligible races a larger tuning/training weight.
    weight=1/train.groupby('cycle').cycle.transform('size').to_numpy()
    model.fit(transform.transform(train), train.actual-train.prior, sample_weight=weight)
    raw=test.prior.to_numpy()+model.predict(transform.transform(test))
    info.update(status='ridge_residual',intercept=float(model.intercept_),
                coefficients=dict(zip(transform.names,map(float,model.coef_))),clipped=int((np.abs(raw)>1).sum()))
    return np.clip(raw,-1,1),info


def run_baselines(targets, waves, start_cycle=2002):
    """Tune on Y-2 using data before Y-2; refit on all labels before Y."""
    predictions=[];tuning=[];fits=[]
    for kind in ['senate','national']:
        universe=targets[targets.kind.eq(kind)].copy()
        cycles=sorted(y for y in universe.cycle.unique() if y>=start_cycle)
        for year in cycles:
            current=universe[universe.cycle.eq(year)]
            earlier=universe[universe.cycle.lt(year)&universe.actual.notna()]
            validation=universe[universe.cycle.eq(year-2)&universe.actual.notna()]
            inner=universe[universe.cycle.lt(year-2)&universe.actual.notna()]
            tuned_poll=DEFAULT_POLL;tuned_alpha=DEFAULT_ALPHA
            poll_status='default_no_previous_cycle_polls';feature_status='default_insufficient_inner_history'
            if len(validation):
                candidates=[]
                for half,strength in product(HALF_LIVES,PRIOR_STRENGTHS):
                    vp=poll_predict(validation,waves,half,strength).set_index('target_id')
                    truth=validation.set_index('target_id').actual
                    mask=vp.n_samples.gt(0)
                    score=float((vp.loc[mask,'prediction']-truth.loc[vp.index[mask]]).abs().mean()) if mask.any() else np.nan
                    candidates.append((score,half,strength))
                    tuning.append(dict(kind=kind,cycle=year,model='polling',validation_cycle=year-2,
                                       fit_max_cycle=int(inner.cycle.max()) if len(inner) else np.nan,
                                       half_life=half,prior_strength=strength,alpha=np.nan,mae=score,n_validation=int(mask.sum())))
                finite=[c for c in candidates if np.isfinite(c[0])]
                if finite:
                    # Fixed tie rule: prefer stronger shrinkage, then longer half-life.
                    best=min(finite,key=lambda c:(round(c[0],12),-c[2],-c[1]))
                    tuned_poll=best[1:];poll_status='last_cycle_tuned'
                if inner.cycle.nunique()>=3:
                    candidates=[]
                    for alpha in ALPHAS:
                        pred,_=feature_predict(inner,validation,alpha)
                        score=float(np.mean(np.abs(pred-validation.actual.to_numpy())))
                        candidates.append((score,alpha))
                        tuning.append(dict(kind=kind,cycle=year,model='features',validation_cycle=year-2,
                                           fit_max_cycle=int(inner.cycle.max()),half_life=np.nan,prior_strength=np.nan,
                                           alpha=alpha,mae=score,n_validation=len(validation)))
                    tuned_alpha=min(candidates,key=lambda c:(round(c[0],12),-c[1]))[1]
                    feature_status='last_cycle_tuned'
            pp=poll_predict(current,waves,*tuned_poll)
            fp,fit=feature_predict(earlier,current,tuned_alpha)
            fit.update(kind=kind,cycle=int(year),alpha=tuned_alpha);fits.append(fit)
            result=current[['target_id','cycle','kind','geography','special','context_id','actual','prior','prior_latest_cycle','prior_basis']].copy()
            result=result.merge(pp.rename(columns={'prediction':'polling'}),on='target_id',validate='one_to_one')
            result['features']=fp;result['half_life']=tuned_poll[0];result['prior_strength']=tuned_poll[1];result['alpha']=tuned_alpha
            result['validation_cycle']=year-2;result['poll_tuning']=poll_status;result['feature_tuning']=feature_status
            result['feature_fit_status']=fit['status'];result['training_max_cycle']=int(earlier.cycle.max()) if len(earlier) else np.nan
            result['missing_features']=current[FEATURES].isna().sum(axis=1).to_numpy()
            predictions.append(result)
    return pd.concat(predictions,ignore_index=True),pd.DataFrame(tuning),fits


def score_predictions(predictions):
    rows=[]
    scored=predictions[predictions.actual.notna()]
    for (kind,cycle),group in scored.groupby(['kind','cycle']):
        for scope,subset in [('all_eligible',group),('with_polls',group[group.n_samples.gt(0)])]:
            if subset.empty:continue
            for model in ['prior','polling','features']:
                error=100*(subset[model]-subset.actual)
                rows.append(dict(kind=kind,cycle=cycle,scope=scope,model=model,n=len(subset),
                                 mae_pp=float(error.abs().mean()),rmse_pp=float(np.sqrt(np.mean(error**2))),
                                 bias_pp=float(error.mean()),winner_accuracy=float((subset[model].gt(0)==subset.actual.gt(0)).mean())))
    return pd.DataFrame(rows)
