"""Chronological regressions of actual minus the available polling forecast.

Only polled contests train or receive a polling correction. No-poll cases keep
the existing prior fallback, with explicit coverage and warm-up accounting.
"""
from itertools import product
import numpy as np
import pandas as pd
from simple_baselines import poll_predict, HALF_LIVES, PRIOR_STRENGTHS, DEFAULT_POLL
from score_baselines import fit_correction, ALPHAS
from standardized_score_baselines import fit_standardized, VARIANTS as SCORE_VARIANTS
from state_score_baselines import fit_state_correction, STATE_PENALTIES, MODELS as STATE_MODELS
from contextual_baselines import predict_variant, VARIANTS as CONTEXT_VARIANTS
from cycle_cv import fold_ledger, MIN_INNER_CYCLES

MODELS = ['constant','four_scores'] + list(SCORE_VARIANTS) + STATE_MODELS + CONTEXT_VARIANTS


def build_poll_history(targets, waves, scenario):
    """Freeze every cycle's polling forecast with only preceding-cycle tuning."""
    source = targets[targets.kind.eq('senate')].copy()
    if scenario == 'oct31':
        source = source[source.window_complete].copy()
    forecasts = []; grid = []
    for year in sorted(source.cycle.unique()):
        current = source[source.cycle.eq(year)]
        validation = source[source.cycle.eq(year-2) & source.actual.notna()]
        chosen = DEFAULT_POLL
        status = 'default_no_previous_cycle_polls'
        if len(validation):
            candidates = []
            for half, strength in product(HALF_LIVES, PRIOR_STRENGTHS):
                p = poll_predict(validation, waves, half, strength).set_index('target_id')
                truth = validation.set_index('target_id').actual
                mask = p.n_samples.gt(0)
                loss = float((p.loc[mask,'prediction']-truth.loc[p.index[mask]]).abs().mean()) if mask.any() else np.nan
                grid.append(dict(scenario=scenario,cycle=int(year),validation_cycle=int(year-2),
                    half_life=half,prior_strength=strength,validation_mae_pp=100*loss,
                    polled_validation_rows=int(mask.sum())))
                if np.isfinite(loss):
                    candidates.append((loss,half,strength))
            if candidates:
                best = min(candidates,key=lambda v:(round(v[0],12),-v[2],-v[1]))
                chosen = best[1:]
                status = 'last_cycle_tuned'
        p = poll_predict(current,waves,*chosen).rename(columns={'prediction':'poll_baseline'})
        f = current.merge(p,on='target_id',validate='one_to_one')
        f['scenario'] = scenario
        f['poll_half_life'] = chosen[0]
        f['poll_prior_strength'] = chosen[1]
        f['poll_validation_cycle'] = int(year-2)
        f['poll_tuning_status'] = status
        forecasts.append(f)
    return pd.concat(forecasts,ignore_index=True),pd.DataFrame(grid)


def fit_poll_correction(train, test, calendars, model, alpha=10., state_penalty=1.):
    """Reuse the regression designs with the chronological poll as the offset."""
    if model not in MODELS:
        raise ValueError('Unknown regression')
    if train.empty or test.empty or not train.n_samples.gt(0).all() or not test.n_samples.gt(0).all():
        raise ValueError('Polling-error fits require polled training and forecast contests')
    if train.actual.isna().any() or train.cycle.max() >= test.cycle.min():
        raise ValueError('Known past labels required')
    if not np.isfinite(train.poll_baseline).all() or not np.isfinite(test.poll_baseline).all():
        raise ValueError('Finite historical polling offsets required')
    tr = train.assign(prior=train.poll_baseline)
    te = test.assign(prior=test.poll_baseline)
    if model in SCORE_VARIANTS:
        prediction,info,_,_ = fit_standardized(tr,te,calendars,alpha,model)
    elif model in STATE_MODELS:
        prediction,info,_,_ = fit_state_correction(tr,te,calendars,alpha,state_penalty,model)
    elif model in CONTEXT_VARIANTS:
        prediction,info = predict_variant(tr,te,alpha,model)
    else:
        prediction,info,_,_ = fit_correction(tr,te,calendars,alpha,model)
    if model == 'constant':
        # The legacy fit stores four zero slopes for a uniform schema; none is learned.
        info['fitted_parameters'] = 1
    info.update(correction_model=model,offset='chronological polling forecast',
        fit_target='actual minus historical polling forecast; polled contests only',
        source_fit_status=info.get('status','fitted'),status='fitted',
        polled_training_rows=len(tr),polled_training_cycles=int(tr.cycle.nunique()))
    return prediction,info


def correction_folds(targets, history, scenario, start_cycle, minimum):
    folds = fold_ledger(targets[targets.kind.eq('senate')],scenario,minimum,start_cycle)
    for i,row in folds.iterrows():
        year = row.cycle
        past = history[history.cycle.lt(year)&history.actual.notna()&history.n_samples.gt(0)]
        inner = past[past.cycle.lt(year-2)]
        validation = past[past.cycle.eq(year-2)]
        test = history[history.cycle.eq(year)]
        counts = dict(inner_training_cycles=inner.cycle.nunique(),inner_training_rows=len(inner),
            inner_training_first=inner.cycle.min(),inner_training_last=inner.cycle.max(),
            validation_rows=len(validation),refit_cycles=past.cycle.nunique(),refit_rows=len(past),
            refit_last=past.cycle.max(),test_polled_rows=int(test.n_samples.gt(0).sum()),
            test_no_poll_rows=int(test.n_samples.eq(0).sum()))
        for key,value in counts.items():
            folds.loc[i,key] = value
        if row.status == 'pending_cutoff':
            continue
        if inner.cycle.nunique() < minimum:
            folds.loc[i,'status'] = 'warm_up_insufficient_training_cycles'
        elif validation.empty:
            folds.loc[i,'status'] = 'missing_previous_validation_cycle'
    return folds


def evaluate_poll_errors(targets, history, calendars, scenario, start_cycle=2002,
                         min_inner_cycles=MIN_INNER_CYCLES, models=None):
    names = MODELS if models is None else list(models)
    if not names or len(set(names)) != len(names) or not set(names) <= set(MODELS):
        raise ValueError('Unknown or duplicate correction model')
    source = history[history.scenario.eq(scenario)&history.kind.eq('senate')].copy()
    if source.target_id.duplicated().any():
        raise ValueError('Duplicate historical polling forecast')
    folds = correction_folds(targets,source,scenario,start_cycle,min_inner_cycles)
    cal = calendars[calendars.scenario.eq(scenario)].copy()
    predictions = []; fits = []; tuning = []
    for fold in folds.itertuples():
        if fold.status == 'pending_cutoff':
            continue
        year = int(fold.cycle)
        test = source[source.cycle.eq(year)]
        train = source[source.cycle.lt(year)&source.actual.notna()&source.n_samples.gt(0)]
        inner = train[train.cycle.lt(year-2)]
        validation = train[train.cycle.eq(year-2)]
        polled = test[test.n_samples.gt(0)]
        eligible = inner.cycle.nunique() >= min_inner_cycles and len(validation)>0
        common = test[['target_id','cycle','kind','geography','actual','n_samples','prior','prior_basis','poll_baseline']].copy()
        for name,col in [('prior','prior'),('polling','poll_baseline')]:
            predictions.append(common.assign(scenario=scenario,model=name,prediction=test[col].to_numpy(),
                correction_status='reference',poll_adjustment_pp=0. if name=='polling' else np.nan))
        for model in names:
            pred = test.poll_baseline.copy()
            row_status = pd.Series(np.where(test.n_samples.eq(0),'no_poll_unchanged_fallback','warmup_unchanged_polling'),index=test.index)
            if eligible and len(polled):
                candidates = []
                alphas = [None] if model == 'constant' else ALPHAS
                penalties = STATE_PENALTIES if model in STATE_MODELS else [None]
                for a,lam in product(alphas,penalties):
                    vp,info = fit_poll_correction(inner,validation,cal,model,a or 10.,lam or 1.)
                    loss = float(np.mean(np.abs(vp-validation.actual.to_numpy())))
                    candidates.append((loss,a,lam))
                    tuning.append(dict(scenario=scenario,cycle=year,model='poll_'+model,
                        validation_cycle=year-2,training_max_cycle=int(inner.cycle.max()),
                        training_cycles=int(inner.cycle.nunique()),training_rows=len(inner),
                        validation_rows=len(validation),alpha=a,state_penalty=lam,validation_mae_pp=100*loss))
                _,alpha,penalty = min(candidates,key=lambda v:(round(v[0],12),-(v[2] or 0),-(v[1] or 0)))
                pp,fit = fit_poll_correction(train,polled,cal,model,alpha or 10.,penalty or 1.)
                pred.loc[polled.index] = pp
                row_status.loc[polled.index] = 'polling_corrected'
                fit.update(selected_alpha=alpha,selected_state_penalty=penalty)
            else:
                fit = dict(correction_model=model,status='warmup_unchanged_polling' if not eligible else 'no_polled_test_targets',
                    polled_training_rows=len(train),polled_training_cycles=int(train.cycle.nunique()),
                    selected_alpha=None,selected_state_penalty=None)
            fit.update(scenario=scenario,cycle=year,model='poll_'+model,validation_cycle=year-2)
            fits.append(fit)
            predictions.append(common.assign(scenario=scenario,model='poll_'+model,prediction=pred.to_numpy(),
                correction_status=row_status.to_numpy(),poll_adjustment_pp=100*(pred-test.poll_baseline).to_numpy()))
    return (pd.concat(predictions,ignore_index=True) if predictions else pd.DataFrame()),pd.DataFrame(tuning),fits,folds
