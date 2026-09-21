"""Execute, audit and report two small changes to the forecast combination."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
import numpy as np
import pandas as pd
from combination_diagnostics import evaluate,prepare_subset,solve_intercept,PROFILES,INTERCEPT_PENALTY_RATIO,MAIN,MODELS,LABELS,blend
from winner_classification import classification_report
from senate_summary import senate_report
from senate_seat_review import roster_at,historical_roster,review_forecasts
from seat_review_tables import margin,seats


def audit_problem(problem,alpha,profile):
    z=problem['z'];v=problem['future'];w=problem['weights']
    if profile=='zero':z=z[:,1:];v=v[:,1:];penalty=np.full(z.shape[1],alpha)
    else:penalty=np.r_[0. if profile=='free' else INTERCEPT_PENALTY_RATIO*w.sum(),np.full(z.shape[1]-1,alpha)]
    a=np.vstack([np.sqrt(w)[:,None]*z,np.diag(np.sqrt(penalty))]);b=np.r_[np.sqrt(w)*problem['response'],np.zeros(z.shape[1])]
    coef=np.linalg.lstsq(a,b,rcond=None)[0];prediction=np.clip(problem['offset']+v@coef,-1,1)
    return prediction,np.r_[0.,coef] if profile=='zero' else coef


def load_terms(source_dir):
    import yaml
    rows=[]
    for name in ['legislators_current','legislators_historical']:
        for person in yaml.load((source_dir/(name+'.txt')).read_text(),Loader=yaml.CSafeLoader):
            for term in person['terms']:
                if term['type']!='sen' or str(term['end'])<'2011-01-01':continue
                r=json.loads(json.dumps(term,default=str));r.update(name=person['name']['first']+' '+person['name']['last'],bioguide=person['id']['bioguide']);rows.append(r)
    return pd.DataFrame(rows)


def roster(terms,year,cutoff):
    if year>=2016:return historical_roster(terms,year,cutoff)
    if year not in [2012,2014]:raise ValueError('Only scored older cycles supported')
    before=roster_at(terms,cutoff);regular=1 if year==2012 else 2;special={} if year==2012 else {'HI':3,'OK':3,'SC':3}
    before['contested']=before.seat_class.eq(regular)|before.apply(lambda r:special.get(r.state)==r.seat_class,axis=1)
    before['special']=before.contested&before.seat_class.ne(regular)
    before['target_id']=before.apply(lambda r:f'{year}-{r.state}-'+('special' if r.special else 'regular')+'-gen' if r.contested else None,axis=1)
    before['seat_id']=before.state+'-class'+before.seat_class.astype(str)
    after=roster_at(terms,f'{year+1}-01-31')[['state','seat_class','caucus']].rename(columns={'caucus':'actual_caucus'})
    result=before.merge(after,on=['state','seat_class'],validate='one_to_one')
    assert result.actual_caucus.eq('D').sum()=={2012:55,2014:46}[year]
    assert result.contested.sum()=={2012:33,2014:36}[year]
    assert (result.loc[~result.contested,'caucus']==result.loc[~result.contested,'actual_caucus']).all()
    return result


def run(lab,parent,progress=print):
    lab,parent=Path(lab).resolve(),Path(parent).resolve()
    original=parent/'momentum_approval/20260918T171057.326361Z'
    review=parent/'seat_review/20260918T181911.299982Z'
    source=lab/'reports/seat_review_sources/20260918'
    sources=dict(history=parent/'bias_momentum_stack/20260918T152736.975887Z/prequential_bias_history.parquet',
        calendars=parent/'contextual/calendars.parquet',references=original/'predictions.parquet',membership=parent/'cv/competitive/membership.parquet',
        prior_seat_ledger=review/'full_seat_ledger.parquet',legislators_current=source/'legislators_current.txt',legislators_historical=source/'legislators_historical.txt')
    hashes={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in sources.items()}
    history=pd.read_parquet(sources['history']);history=history[history.base.eq('fixed5_8')].copy();before=history.copy(deep=True)
    cal=pd.read_parquet(sources['calendars']);frames,fits=evaluate(history,cal,progress=progress)
    predictions=frames['predictions'];references=pd.read_parquet(sources['references']);parity={}
    for model,old in [('prior','prior'),('polling','polling'),('bias','bias'),('constant','bias__constant'),('original_both','bias__both'),('fundamentals','prior__both')]:
        a=predictions[predictions.model.eq(model)];b=references[references.model.eq(old)]
        q=a.merge(b,on=['scenario','target_id'],suffixes=('_a','_b'),validate='one_to_one')
        assert len(q)==len(a)==len(b)
        assert np.allclose(q.prediction_a,q.prediction_b,atol=1e-11);parity[model]=len(q)
    # Rebuild every final fit and every inner candidate using augmented LS.
    audits=[]
    for f in fits:
        fundamental=f['model']=='fundamentals'
        sourceh=history[history.scenario.eq(f['scenario'])]
        tr=sourceh[sourceh.cycle.lt(f['cycle'])&sourceh.actual.notna()]
        te=sourceh[sourceh.cycle.eq(f['cycle'])]
        if not fundamental:tr=tr[tr.n_samples.gt(0)];te=te[te.n_samples.gt(0)]
        if te.empty:te=sourceh[sourceh.cycle.eq(f['cycle'])].iloc[:1]
        problem=prepare_subset(tr,te,cal[cal.scenario.eq(f['scenario'])],'prior' if fundamental else 'bias','both')
        profile='free' if fundamental else f['profile']
        pred,coef=audit_problem(problem,f['alpha'],profile)
        if fundamental:
            rows=frames['fundamental_history'];saved=rows[rows.scenario.eq(f['scenario'])&rows.cycle.eq(f['cycle'])].set_index('target_id').loc[te.target_id,'fundamentals']
        else:saved=predictions[predictions.model.eq(f['model'])&predictions.scenario.eq(f['scenario'])&predictions.cycle.eq(f['cycle'])].set_index('target_id').loc[te.target_id,'prediction']
        assert np.allclose(saved,pred,atol=1e-11)
        assert np.allclose(coef,list(f['standardized_coefficients'].values()),atol=1e-11)
        mean=np.average(problem['response'],weights=problem['weights'])
        expected=0. if profile=='zero' else mean/(11 if profile=='shrunk' else 1)
        assert np.isclose(coef[0],expected,atol=1e-11)
        audits.append(dict(scenario=f['scenario'],cycle=f['cycle'],model=f['model'],max_difference=float(np.max(np.abs(saved-pred)))))
    for (scenario,year,model),g in frames['tuning'].groupby(['scenario','cycle','model']):
        tr=history[history.scenario.eq(scenario)&history.cycle.lt(year-2)&history.actual.notna()]
        va=history[history.scenario.eq(scenario)&history.cycle.eq(year-2)]
        if model!='fundamentals':tr=tr[tr.n_samples.gt(0)];va=va[va.n_samples.gt(0)]
        problem=prepare_subset(tr,va,cal[cal.scenario.eq(scenario)],'prior' if model=='fundamentals' else 'bias','both')
        for r in g.itertuples():
            pred,_=audit_problem(problem,r.alpha,'free' if model=='fundamentals' else r.profile)
            assert np.isclose(100*np.abs(pred-va.actual.to_numpy()).mean(),r.validation_mae_pp,atol=1e-10)
    for (scenario,year),g in frames['blend_selection'].groupby(['scenario','cycle']):
        va=history[history.scenario.eq(scenario)&history.cycle.eq(year-2)&history.n_samples.gt(0)]
        fh=frames['fundamental_history'];fh=fh[fh.scenario.eq(scenario)&fh.cycle.eq(year-2)].set_index('target_id')
        ff=fh.loc[va.target_id,'fundamentals'].to_numpy()
        for r in g.itertuples():
            expected=r.polling_weight*va.bias_prediction.to_numpy()+(1-r.polling_weight)*ff
            assert np.isclose(100*np.abs(expected-va.actual.to_numpy()).mean(),r.validation_mae_pp)
        chosen=min(g.to_dict('records'),key=lambda x:(round(x['validation_mae_pp']/100,12),-x['polling_weight']))
        assert chosen['selected']
    bp=predictions[predictions.model.isin(['blend_half','blend_90','blend_selected','fundamental_fallback'])]
    assert bp.prediction.ge(bp[['bias_prediction','fundamentals']].min(axis=1)-1e-12).all()
    assert bp.prediction.le(bp[['bias_prediction','fundamentals']].max(axis=1)+1e-12).all()
    assert np.array_equal(bp.loc[bp.n_samples.eq(0),'prediction'],bp.loc[bp.n_samples.eq(0),'fundamentals'])
    calls,_,_,_=classification_report(predictions)
    calls,cycles,summary=senate_report(calls,pd.read_parquet(sources['membership']))
    frames.update(state_calls=calls,cycle_metrics=cycles,summary=summary,independent_audit=pd.DataFrame(audits))
    groups=[]
    for period,start in [('2012_onward',2012),('2016_onward',2016)]:
        for (scenario,model),g in calls[calls.classification_status.eq('cv_scored')&calls.cycle.ge(start)].groupby(['scenario','model']):
            for name,q in [('all',g),('competitive',g[g.history_selection_10pp.eq('competitive')]),('polled',g[g.n_samples.gt(0)]),('no_polls',g[g.n_samples.eq(0)])]:
                if len(q):groups.append(dict(period=period,scenario=scenario,model=model,group=name,n=len(q),correct=int(q.correct.sum()),mae_pp=100*(q.prediction-q.actual).abs().groupby(q.cycle).mean().mean()))
    frames['groups']=pd.DataFrame(groups)
    terms=load_terms(source);prior_ledger=pd.read_parquet(sources['prior_seat_ledger']);ledgers=[];totals=[]
    for (year,scenario),g in predictions.groupby(['cycle','scenario']):
        if year>=2016:
            r=prior_ledger[prior_ledger.cycle.eq(year)&prior_ledger.scenario.eq(scenario)&prior_ledger.model.eq('bias')]
            r=r[['state','seat_class','seat_id','target_id','contested','special','caucus','actual_caucus']].copy()
        else:r=roster(terms,int(year),str(cal.loc[cal.cycle.eq(year)&cal.scenario.eq(scenario),'context_id'].iloc[0])[:10])
        for model,q in g.groupby('model'):
            ledger,total=review_forecasts(r,q,int(year),scenario,model);ledgers.append(ledger);totals.append(total)
    frames['full_seat_ledger']=pd.concat(ledgers,ignore_index=True);frames['seat_totals']=pd.concat(totals,ignore_index=True)
    current=predictions[predictions.cycle.eq(2026)].pivot(index=['target_id','geography','n_samples'],columns='model',values='prediction')*100
    frames['current_states']=current.reset_index()
    ftab=[]
    for f in fits:
        r={k:f.get(k) for k in ['model','scenario','cycle','alpha','profile','matched_alpha','intercept_penalty','training_cycles','training_rows','training_max_cycle','effective_df','extra_adjustment_pp','validation_mae_pp']}
        r['intercept_pp']=100*f['standardized_coefficients']['intercept'];ftab.append(r)
    frames['fit_summary']=pd.DataFrame(ftab)
    pd.testing.assert_frame_equal(history,before)
    out=parent/'combination_diagnostics'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True)
    for name,df in frames.items():df.to_parquet(out/(name+'.parquet'),index=False)
    (out/'fits.json').write_text(json.dumps(fits,indent=2,allow_nan=False)+'\n')
    settings=dict(version='intercept-and-convex-blend-v2',start_requested=2006,earliest_scored=2012,min_inner_polled_cycles=6,
        feature_set=['economy_momentum_wh','approval_wh'],intercept_shrinkage_ratio=INTERCEPT_PENALTY_RATIO,
        fixed_blend_weights=[.5,.9],blend_weights=[0,.25,.5,.75,1],blend_validation='previous-cycle polled contests MAE; ties favor polling; constituents separately out-of-time',
        no_poll_policy='residual arms retain prior; blends use fundamentals, with separate fallback-only control',
        fundamentals='historical state prior + shared momentum and approval residual regression; all older outcomes; train-only transforms; alpha onY-2;8yrdecay',
        warmup='2006/2008/2010 shown but not scored; reconstructed2010fundamentals only for2012blend validation',
        audit_final_fits=len(audits),audit_inner_candidates=len(frames['tuning']),audit_blend_candidates=len(frames['blend_selection']),reference_parity=parity,automatic_promotion=False,
        sources={k:dict(path=str(p),sha256=hashes[k]) for k,p in sources.items()})
    (out/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
    for name in ['combination_diagnostics.py','run_combination_diagnostics.py','momentum_approval_models.py','recency_state_baselines.py']:
        shutil.copy2(lab/'scripts'/name,out/name)
    for k,p in sources.items():assert hashlib.sha256(p.read_bytes()).hexdigest()==hashes[k]
    refresh(out);print('Saved:',out,flush=True);return out,frames,fits


def refresh(out):
    (out/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name!='manifest.json'},indent=2)+'\n')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--parent',type=Path,required=True);a=p.parse_args()
    run(Path(__file__).resolve().parents[1],a.parent)
