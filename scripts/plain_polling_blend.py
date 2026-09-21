"""Compare frozen plain polling, corrected polling, and their equal Bayesian blends."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import shutil

import numpy as np
import pandas as pd
from model_labels import label_frame
import calibrate_margin_uncertainty as calibration

POINT_SOURCE = 'reports/bayesian_nonbayesian_blend/20260920T055636.585382Z'
CALIBRATION_SOURCE = 'reports/margin_probability_calibration/20260920T060740.888256Z'
NONBAYES_SOURCE = 'reports/official_repair_review/20260919T172552.860612Z'
BAYES_SOURCE = 'reports/signed_state_factor/20260920T052241.012596Z'
NAMES = ['Bayesian', 'Bias-corrected polling', 'Bayes + bias (50/50)', 'Plain polling', 'Bayes + plain (50/50)']
KEY = ['scenario','cycle','target_id']
RENAMES = {'Non-Bayesian':'Bias-corrected polling','50/50 blend':'Bayes + bias (50/50)'}
NEW_NAMES = {'Non-Bayesian':'Plain polling','50/50 blend':'Bayes + plain (50/50)'}


def independent_seats(probabilities, fixed_d):
    """Exact Poisson-binomial arithmetic, explicitly assuming independent contests."""
    p = np.asarray(probabilities, dtype=float)
    if p.ndim != 1 or not np.isfinite(p).all() or np.any((p<0)|(p>1)):
        raise ValueError('Finite one-dimensional win probabilities required')
    if not 0 <= fixed_d <= 100-len(p):
        raise ValueError('Invalid fixed seat count')
    frequency = np.array([1.])
    for v in p:
        frequency = np.convolve(frequency, [1-v,v])
    counts = fixed_d+np.arange(len(frequency))
    assert np.isclose(frequency.sum(),1.)
    assert np.isclose(frequency@counts,fixed_d+p.sum())
    low,high = counts[np.searchsorted(frequency.cumsum(),[.15,.85])]
    return dict(expected_D=float(fixed_d+p.sum()),expected_R=float(100-fixed_d-p.sum()),
                p_D_control=float(frequency[counts>=51].sum()),
                p_R_control=float(frequency[counts<=50].sum()),
                p_tied50=float(frequency[counts==50].sum()),D_lo70=int(low),D_hi70=int(high)), frequency


def verify(artifact):
    sha=calibration.sha
    for name,digest in json.loads((artifact/'manifest.json').read_text()).items():
        assert sha(artifact/name)==digest, artifact/name


def build(lab):
    lab=Path(lab).resolve();sha=calibration.sha
    old_point=lab/POINT_SOURCE;old_cal=lab/CALIBRATION_SOURCE;nb=lab/NONBAYES_SOURCE;bayes=lab/BAYES_SOURCE
    verify(old_point);verify(old_cal)
    old_settings=json.loads((old_point/'settings.json').read_text())
    assert sha(nb/'nonbayesian_predictions.parquet') == old_settings['sources']['nonbayes_predictions']['sha256']
    assert sha(lab/'scripts/calibrate_margin_uncertainty.py') == sha(old_cal/'calibrate_margin_uncertainty.py')
    sources={name:p for name,p in [('point_source_manifest',old_point/'manifest.json'),
        ('calibration_source_manifest',old_cal/'manifest.json'),('nonbayesian_predictions',nb/'nonbayesian_predictions.parquet'),
        ('bayesian_seats',bayes/'seats.parquet'),('working_designation',lab/'WORKING_MODEL.json')]}
    hashes={k:sha(p) for k,p in sources.items()}
    old_notebooks={p.name:sha(p) for p in lab.glob('*.ipynb')}
    data=pd.read_parquet(old_point/'paired_predictions.parquet')
    plain=pd.read_parquet(nb/'nonbayesian_predictions.parquet').query('model == "polling"')
    plain=plain[KEY+['actual','q_pp','prediction_pp','n_samples']].rename(columns={'prediction_pp':'plain_pp','n_samples':'plain_n_samples'})
    data=data.merge(plain,on=KEY,how='outer',validate='one_to_one',suffixes=('','_plain'),indicator=True)
    assert data._merge.eq('both').all(),'No silent unmatched targets'
    data=data.drop(columns='_merge')
    assert np.allclose(data.actual,data.actual_plain,equal_nan=True)
    assert np.allclose(data.q_pp,data.q_pp_plain,equal_nan=True)
    assert np.isfinite(data.plain_pp).all()
    no_poll=data.plain_n_samples.eq(0)
    assert np.allclose(data.loc[no_poll,'plain_pp'],data.loc[no_poll,'nonbayesian_pp']), 'Fallback mismatch'
    current_polled=data.cycle.eq(2026)&data.q_pp.notna()
    assert np.allclose(data.loc[current_polled,'plain_pp'],data.loc[current_polled,'q_pp'])
    data['plain_blend_pp']=.5*(data.bayesian_pp+data.plain_pp)
    # Reuse exactly the previous uncertainty rule. Only the two point-margin columns change.
    new_input=data.copy()
    new_input['nonbayesian_pp']=data.plain_pp
    new_input['blend_pp']=data.plain_blend_pp
    fresh,new_fits=calibration.calibrate(new_input)
    old=pd.read_parquet(old_cal/'predictions.parquet')
    control=fresh[fresh.model.eq('Bayesian')].merge(old[old.model.eq('Bayesian')],on=KEY,validate='one_to_one',suffixes=('','_old'))
    for col in ['margin_pp','sigma_pp','p_dem','lo70_pp','hi70_pp']:
        assert np.allclose(control[col],control[col+'_old'],equal_nan=True)
    predictions=pd.concat([old.assign(model=old.model.replace(RENAMES)),
        fresh[fresh.model.ne('Bayesian')].assign(model=lambda x:x.model.replace(NEW_NAMES))],ignore_index=True)
    old_fits=pd.read_parquet(old_cal/'calibration_fits.parquet')
    fits=pd.concat([old_fits.assign(model=old_fits.model.replace(RENAMES)),
                    new_fits.assign(model=new_fits.model.replace(NEW_NAMES))],ignore_index=True)
    predictions['model']=pd.Categorical(predictions.model,NAMES,ordered=True)
    predictions=predictions.sort_values(KEY+['model']).reset_index(drop=True)
    assert not predictions.duplicated(KEY+['model']).any()
    assert predictions[predictions.cycle.eq(2026)].actual_pp.isna().all()
    # Every component retains identical dates, targets, and outcomes. Point scoring starts in 2012.
    historical=predictions[predictions.actual_pp.notna()]
    cycle_scores=historical.groupby(['scenario','cycle','model'],observed=True).agg(
        n=('target_id','size'),correct=('correct','sum'),mae_pp=('absolute_error_pp','mean'),
        brier=('brier','mean'),coverage70=('coverage70','mean'),width70_pp=('width70_pp','mean'),
        interval_score70_pp=('interval_score70_pp','mean')).reset_index()
    summaries=[]
    for first in [2012,2016]:
        for (sc,model),q in cycle_scores[cycle_scores.cycle.ge(first)].groupby(['scenario','model'],observed=True):
            summaries.append(dict(first_cycle=first,scenario=sc,model=str(model),cycles=len(q),n=int(q.n.sum()),
                                  correct=int(q.correct.sum()),mae_pp=q.mae_pp.mean()))
    point_summary=pd.DataFrame(summaries)
    # All five models must have a probability for the same historical contest before comparison.
    valid=historical[historical.p_dem.notna()]
    complete=valid.groupby(KEY,observed=True).model.nunique().eq(5)
    matched=valid.merge(complete[complete].reset_index()[KEY],on=KEY,validate='many_to_one')
    probability_metrics=['brier','coverage70','width70_pp','interval_score70_pp']
    probability_cycles=matched.groupby(['scenario','cycle','model'],observed=True)[probability_metrics].mean().reset_index()
    probability_summary=probability_cycles.groupby(['scenario','model'],observed=True)[probability_metrics].mean().reset_index()
    probability_summary=probability_summary.merge(matched.groupby(['scenario','model'],observed=True).agg(
        n=('target_id','size'),cycles=('cycle','nunique')).reset_index(),validate='one_to_one')
    groups=[]
    for (scenario,model),q in historical[historical.cycle.ge(2016)].groupby(['scenario','model'],observed=True):
        for group,g in {'polled':q[q.q_pp.notna()],'no_polls':q[q.q_pp.isna()],
                        'competitive':q[q.history_selection_10pp.eq('competitive')],
                        'other_or_unknown':q[~q.history_selection_10pp.eq('competitive')]}.items():
            if len(g):groups.append(dict(scenario=scenario,model=str(model),group=group,n=len(g),
                correct=int(g.correct.sum()),mae_pp=g.groupby('cycle').absolute_error_pp.mean().mean()))
    seats_source=pd.read_parquet(bayes/'seats.parquet').query('model == "repaired_both__selected"')
    seats=[];frequencies=[]
    for (scenario,year,model),q in predictions.groupby(['scenario','cycle','model'],observed=True):
        ref=seats_source[seats_source.scenario.eq(scenario)&seats_source.cycle.eq(year)].iloc[0]
        fixed=int(ref.fixed_D);point=int(fixed+q.margin_pp.gt(0).sum())
        entry=dict(scenario=scenario,cycle=int(year),model=str(model),method='independent_states',
                   point_D=point,point_R=100-point,actual_D=ref.actual_D,fixed_D=fixed,
                   unmodeled_contested=int(ref.unmodeled_contested))
        if q.p_dem.notna().all():
            result,freq=independent_seats(q.p_dem,fixed)
            entry.update(result)
            frequencies.extend(dict(scenario=scenario,cycle=int(year),model=str(model),D_seats=fixed+i,probability=float(v)) for i,v in enumerate(freq))
        seats.append(entry)
    for r in seats_source.itertuples():
        seats.append(dict(scenario=r.scenario,cycle=int(r.cycle),model='Bayesian',method='original_joint_posterior',
                          point_D=int(r.point_D),point_R=int(r.point_R),actual_D=r.actual_D,fixed_D=int(r.fixed_D),
                          unmodeled_contested=int(r.unmodeled_contested),expected_D=r.expected_D_exact,
                          expected_R=100-r.expected_D_exact,p_D_control=r.p_D_at_least_51,
                          p_R_control=1-r.p_D_at_least_51,p_tied50=r.p_D_exactly_50,D_lo70=r.D_lo70,D_hi70=r.D_hi70))
    seats=pd.DataFrame(seats)
    current=predictions[predictions.cycle.eq(2026)]
    margin_rows=[];probability_rows=[];interval_rows=[];compact_rows=[]
    for tid,q in current.groupby('target_id',observed=True):
        r=q.iloc[0];state=r.geography+(' (special)' if r.special else '')
        margins={'State':state,'Raw polling input':r.q_pp};probs={'State':state};intervals={'State':state};compact={'State':state}
        for name in NAMES:
            v=q[q.model.eq(name)].iloc[0]
            margins[name]=v.margin_pp;probs[name]=100*v.p_dem
            intervals[name]=f'[{v.lo70_pp:+.1f}, {v.hi70_pp:+.1f}]'
            ps='<0.1%' if v.p_dem<.001 else '>99.9%' if v.p_dem>.999 else f'{100*v.p_dem:.1f}%'
            compact[name]=f'{v.margin_pp:+.2f} / {ps}'
        margin_rows.append(margins);probability_rows.append(probs);interval_rows.append(intervals);compact_rows.append(compact)
    assert len(current)==175 and len(compact_rows)==35
    # Freeze old component probabilities/intervals, not merely their point forecasts.
    same=predictions[predictions.model.isin(['Bayesian',*RENAMES.values()])].copy()
    same['model']=same.model.astype(str).replace({v:k for k,v in RENAMES.items()})
    same=same.merge(old,on=KEY+['model'],validate='one_to_one',suffixes=('','_old'))
    for col in ['margin_pp','p_dem','lo70_pp','hi70_pp']:
        assert np.allclose(same[col],same[col+'_old'],equal_nan=True)
    # Independent arithmetic must reproduce current Bayesian expected seats (dependence is irrelevant to expectation).
    current_seats=seats[seats.cycle.eq(2026)]
    both=current_seats[current_seats.model.eq('Bayesian')]
    assert np.allclose(both.expected_D,both.expected_D.iloc[0])
    assert all(sha(p)==hashes[k] for k,p in sources.items())
    assert all(sha(lab/name)==h for name,h in old_notebooks.items())
    out=lab/'reports/plain_polling_blend'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True)
    tables=dict(paired_inputs=data,predictions=predictions,calibration_fits=fits,cycle_scores=cycle_scores,
        point_summary=point_summary,probability_cycles=probability_cycles,probability_summary=probability_summary,
        point_subgroups=pd.DataFrame(groups),seats=seats,independent_seat_distributions=pd.DataFrame(frequencies),
        current_table=pd.DataFrame(compact_rows),current_margins=pd.DataFrame(margin_rows),
        current_probabilities=pd.DataFrame(probability_rows),current_intervals=pd.DataFrame(interval_rows))
    for name,table in tables.items():table.to_parquet(out/f'{name}.parquet',index=False)
    settings=dict(data_as_of='2026-09-17',plain_model_id='polling',bias_model_id='bias',
        bayesian_model_id='repaired_both__selected',blend_weight=.5,
        plain_definition='Saved recency/firm-weighted polling without learned historical error correction; existing tuned prior blend and no-poll fallback retained.',
        calibration='Identical prior-cycle pooled zero-centered RMS Gaussian rule; all earlier cycles equally weighted, three-cycle minimum, separate horizons.',
        control_threshold='D requires51; R wins50–50 under existing ledger convention.',
        independence_warning='New seat ranges and control probabilities are provisional independent-state scenarios; original Bayesian joint results are separate.',
        no_refit=True,no_refresh=True,no_promotion=True,
        sources={k:dict(path=str(p.relative_to(lab)),sha256=hashes[k]) for k,p in sources.items()},
        old_notebooks=old_notebooks)
    (out/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
    audit=dict(passed=True,paired_rows=len(data),prediction_rows=len(predictions),current_contests=35,
        matched_probability_contests_per_horizon=111,checks=['Manifest verification','Exact target matching',
        'Identical actuals and poll snapshots','Same no-poll fallback for plain and bias',
        'Current plain polling reproduces raw aggregate where available','Original three forecasts and uncertainty unchanged',
        'Same past-only calibration function','Shared probability evaluation targets','Current labels missing',
        'Poisson-binomial mass and expectation checks','Bayesian seat expectation parity','Input and old notebook preservation'])
    (out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    for filename in ['plain_polling_blend.py','calibrate_margin_uncertainty.py']:
        shutil.copy2(lab/'scripts'/filename,out/filename)
    report='''# Plain polling and a second Bayesian blend

Five explicitly named forecasts use identical frozen September17 data and contest sets: the existing Bayesian experiment, retained state-bias-corrected polling, their fixed50/50 blend, plain polling, and Bayesian/plain fixed50/50 blend. The first three forecasts, probabilities and intervals are reproduced unchanged.

**Plain polling** is the saved `polling` model without learned polling-error correction. It keeps its historical tuning of recency/firm weights and prior blending; no-poll contests use the same prior fallback as the bias model. For currently polled states, its prediction equals the raw polling aggregate. It is not a new equal-weight average or a zero forecast where polls are missing.

Both blends average margins, not probabilities. Each non-Bayesian model/blend gets its own zero-centered Gaussian RMS scale from all earlier-cycle out-of-sample errors, with equal cycle weights and the same three-cycle minimum. The new blend is calibrated from its own errors, retaining empirical component error dependence. Current means stay fixed. All previous limitations (pooled state scales, nonzero residual means, limited cycles and repeated exploratory model review) remain.

## Recent point accuracy,2016–2024 (140 contests per horizon)

MAE is absolute D−R margin error in percentage points, averaged equally over cycles. Lower is better. Correct winner counts use unrounded signs.

'''+label_frame(point_summary.query('first_cycle == 2016').round(4)).to_markdown(index=False)
    report+='\n\n## Probability and interval evaluation,2018–2024\n\nThree earlier calibration cycles are required, giving111 matched contests per horizon. Brier and interval score: lower is better;70% coverage should be near.70. Metrics average cycles equally.\n\n'+label_frame(probability_summary.round(4)).to_markdown(index=False)
    report+='\n\n## Current seats and control\n\nExpected seats sum marginals and do not require independence. Point totals count margin-sign winners. The `independent_states` rows explicitly assume independent outcomes; their ranges/control probabilities are provisional, not learned joint forecasts. Original correlated Bayesian results are separately retained. D needs51 seats; R wins a50–50 tie under the existing convention.\n\n'+label_frame(current_seats.round(4)).to_markdown(index=False)
    report+='\n\n## Every current contest: margin / P(D)\n\nPositive margins favor D; probabilities are chances of winning, not vote shares. No correlations are displayed. Existing independent-candidate proxy caveats, including Nebraska, remain.\n\n'+label_frame(tables['current_table']).to_markdown(index=False)
    report+='\n\n## Current70% marginal intervals\n\n'+label_frame(tables['current_intervals']).to_markdown(index=False)
    report+='\n\nPer-cycle results, older2012/2014 checks, competitive and polling-coverage subsets are saved alongside this report. Historical point-seat totals retain the same explicit incumbent-caucus completion assumptions for unmodeled contests. No promotion, weight search, refit of component means, or data refresh.\n'
    (out/'RESULTS.md').write_text(report)
    calibration.finalize(out)
    print('OUTPUT',out)
    print(point_summary.query('first_cycle == 2016').round(4).to_string(index=False))
    print(probability_summary.round(4).to_string(index=False))
    print(current_seats.round(4).to_string(index=False))
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1])
    build(parser.parse_args().lab)
