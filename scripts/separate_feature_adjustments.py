"""Separate priors, intercepts and feature contributions before correcting polls."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
import numpy as np
import pandas as pd
from momentum_approval_models import prepare_subset
from senate_seat_review import review_forecasts
from run_combination_diagnostics import refresh

TERMS = ['economy_momentum_wh', 'approval_wh']
LABELS = {'bias':'Corrected polling', 'blend_90':'Old 90/10 full-forecast blend',
          'blend_half':'Old 50/50 full-forecast blend', 'zero_intercept':'Residual features, 100%',
          'outcome_signal_10':'Outcome feature contribution, 10%',
          'outcome_signal_50':'Outcome feature contribution, 50%',
          'residual_signal_10':'Residual feature contribution, 10%',
          'residual_signal_50':'Residual feature contribution, 50%'}
NEW = ['outcome_signal_10','outcome_signal_50','residual_signal_10','residual_signal_50']


def contributions(fit):
    """Return slope-only effects at training-centered coordinates, in margin units."""
    if len(fit['test_scores']) != 1:
        raise ValueError('Expected one national context per forecast cycle')
    scores = fit['test_scores'][0]; result = {}
    for term in TERMS:
        if term not in fit['active_terms']:
            result[term] = 0.; continue
        value = scores[term]
        if value is None or not np.isfinite(value):
            value = fit['score_fills'][term]
        z = (value-fit['score_centers'][term])/fit['score_scales'][term]
        result[term] = z*fit['standardized_coefficients'][term]
    return result


def apply_signal(base, n_samples, signal, strength):
    """Keep the base intact; no prior/intercept argument can enter this layer."""
    base,n = np.asarray(base,float),np.asarray(n_samples)
    if base.shape != n.shape or not np.isfinite(base).all() or not np.isfinite(signal):
        raise ValueError('Finite aligned inputs required')
    if not np.isfinite(strength) or not 0 <= strength <= 1:
        raise ValueError('Strength must be in [0,1]')
    return np.clip(base + np.where(n>0,strength*signal,0.),-1,1)


def build(lab, source):
    lab,source = Path(lab).resolve(),Path(source).resolve()
    manifest = json.loads((source/'manifest.json').read_text())
    assert all(hashlib.sha256((source/k).read_bytes()).hexdigest()==v for k,v in manifest.items())
    settings = json.loads((source/'settings.json').read_text())
    assert all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in settings['sources'].values())
    pred = pd.read_parquet(source/'predictions.parquet')
    fits = json.loads((source/'fits.json').read_text())
    h = pd.read_parquet(settings['sources']['history']['path']);h=h[h.base.eq('fixed5_8')]
    cal = pd.read_parquet(settings['sources']['calendars']['path'])
    parts = [pred[pred.model.isin(['bias','blend_90','blend_half','zero_intercept'])].copy()]
    decompositions=[];audit=[]
    for (scenario,year),g in pred[pred.model.eq('bias')].groupby(['scenario','cycle']):
        components={}
        for family,model,base in [('outcome','fundamentals','prior'),('residual','zero_intercept','bias')]:
            f=next(f for f in fits if f['scenario']==scenario and f['cycle']==year and f['model']==model)
            assert f['training_max_cycle']<year and f['validation_cycle']<year
            values=contributions(f);signal=sum(values.values());components[family]=(values,signal,f)
            # Independently recreate the train-only design and fit, not just the saved contribution sum.
            tr=h[h.scenario.eq(scenario)&h.cycle.lt(year)&h.actual.notna()]
            te=h[h.scenario.eq(scenario)&h.cycle.eq(year)]
            if family=='residual':tr=tr[tr.n_samples.gt(0)];te=te[te.n_samples.gt(0)]
            p=prepare_subset(tr,te,cal[cal.scenario.eq(scenario)],base,'both')
            z=p['z'] if family=='outcome' else p['z'][:,1:]
            v=p['future'] if family=='outcome' else p['future'][:,1:]
            penalties=np.r_[0.,np.full(z.shape[1]-1,f['alpha'])] if family=='outcome' else np.full(z.shape[1],f['alpha'])
            a=np.vstack([np.sqrt(p['weights'])[:,None]*z,np.diag(np.sqrt(penalties))])
            b=np.r_[np.sqrt(p['weights'])*p['response'],np.zeros(z.shape[1])]
            beta=np.linalg.lstsq(a,b,rcond=None)[0]
            expected=v@beta-(beta[0] if family=='outcome' else 0.)
            assert np.allclose(expected,signal,atol=1e-11)
            audit.append(dict(scenario=scenario,cycle=year,family=family,max_difference=float(np.max(np.abs(expected-signal)))))
            for strength in [.1,.5]:
                model_id=f'{family}_signal_{int(100*strength)}'
                q=g.copy();q['model']=model_id;q['prediction']=apply_signal(g.prediction,g.n_samples,signal,strength)
                q['signal_strength']=strength;q['feature_signal']=signal
                q['applied_adjustment_pp']=100*(q.prediction-g.prediction)
                parts.append(q)
        for r in g.itertuples():
            row=dict(scenario=scenario,cycle=year,target_id=r.target_id,state=r.geography,n_samples=r.n_samples,
                     historical_prior_pp=100*r.prior,corrected_polling_pp=100*r.prediction,actual_pp=100*r.actual)
            for family,(vals,signal,f) in components.items():
                row.update({family+'_'+k+'_pp':100*v for k,v in vals.items()})
                row[family+'_intercept_pp']=100*f['standardized_coefficients']['intercept']
                row[family+'_feature_signal_pp']=100*signal
            assert np.isclose(np.clip((row['historical_prior_pp']+row['outcome_intercept_pp']+row['outcome_feature_signal_pp'])/100,-1,1),r.fundamentals)
            decompositions.append(row)
    newpred=pd.concat(parts,ignore_index=True)
    # Reconcile additive identity and preserve original no-poll fallback exactly.
    for model,g in newpred[newpred.model.isin(NEW)].groupby('model'):
        expected=np.clip(g.bias_prediction+np.where(g.n_samples.gt(0),g.signal_strength*g.feature_signal,0.),-1,1)
        assert np.allclose(g.prediction,expected,atol=1e-12)
        assert np.array_equal(g.loc[g.n_samples.eq(0),'prediction'],g.loc[g.n_samples.eq(0),'bias_prediction'])
    oldledger=pd.read_parquet(source/'full_seat_ledger.parquet');ledgers=[];totals=[]
    for (year,scenario,model),g in newpred.groupby(['cycle','scenario','model']):
        roster=oldledger[oldledger.cycle.eq(year)&oldledger.scenario.eq(scenario)&oldledger.model.eq('bias')]
        roster=roster[['state','seat_class','seat_id','target_id','contested','special','caucus','actual_caucus']]
        l,t=review_forecasts(roster,g,int(year),scenario,model);ledgers.append(l);totals.append(t)
    totals=pd.concat(totals,ignore_index=True)
    groups=[];membership=pd.read_parquet(settings['sources']['membership']['path'])
    # Reuse the exact existing competitive definition via the reference state-call mapping.
    reference=pd.read_parquet(source/'state_calls.parquet').query("model == 'bias'")
    competitive=reference[['scenario','target_id','history_selection_10pp']]
    calls=newpred.merge(competitive,on=['scenario','target_id'],validate='many_to_one')
    for (scenario,model),g in calls[calls.cycle.between(2016,2024)].groupby(['scenario','model']):
        for group,q in [('all',g),('competitive',g[g.history_selection_10pp.eq('competitive')])]:
            groups.append(dict(scenario=scenario,model=model,group=group,n=len(q),correct=int(((q.prediction>0)==(q.actual>0)).sum()),mae_pp=100*(q.prediction-q.actual).abs().groupby(q.cycle).mean().mean()))
    frames=dict(predictions=newpred,components=pd.DataFrame(decompositions),groups=pd.DataFrame(groups),seat_totals=totals,
                full_seat_ledger=pd.concat(ledgers,ignore_index=True),independent_audit=pd.DataFrame(audit))
    out=source.parent.parent/'separated_features'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True)
    for name,df in frames.items():df.to_parquet(out/(name+'.parquet'),index=False)
    (out/'settings.json').write_text(json.dumps(dict(source=str(source),source_manifest_sha256=hashlib.sha256((source/'manifest.json').read_bytes()).hexdigest(),
        formula='corrected_polling + strength * (momentum contribution + approval contribution)',strengths=[.1,.5],anchor='each fitted model training-weighted feature means',
        intercept='excluded explicitly',no_poll='unchanged corrected-polling prior fallback',fitting='reuse past-only fitted slopes; independently reconstruct all 30 fits; no new tuning',
        outcome_transfer='sensitivity only: slopes trained on actual minus prior, may double-count information in polls',
        residual_signal='slopes trained without intercept on actual minus historical corrected polling',promotion=False),indent=2)+'\n')
    (out/'separate_feature_adjustments.py').write_bytes(Path(__file__).read_bytes());refresh(out)
    return out,frames

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);a=p.parse_args()
    out,_=build(Path(__file__).resolve().parents[1],a.source);print(out)
