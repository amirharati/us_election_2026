"""Run interstate signal experiments and reconstruct selected fits independently."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
import numpy as np
import pandas as pd
from state_peer_models import evaluate,relationships,BASES,HALF_LIFE,INTERCEPT_MASS,MIN_PAIRS
from winner_classification import classification_report
from senate_summary import senate_report


def independent_fit(history,fit):
    """Scalar preprocessing + augmented normal equations, independently of SVD fitter."""
    year,state,base=fit['cycle'],fit['geography'],fit['base'];col=BASES[base]
    tr=history[history.cycle.lt(year)&history.cycle.ge(year-2*fit['lookback'])]
    q=tr[tr.geography.eq(state)&tr.actual.notna()]
    if base!='prior':q=q[q.n_samples.gt(0)]
    response=(q.actual-q[col]).groupby(q.cycle).mean().sort_index()
    if len(response)<MIN_PAIRS:
        assert fit['status']=='insufficient_target_history';return 0.,0.
    years=response.index.to_list();w=np.array([2.**(-((year-2)-y)/HALF_LIFE) for y in years])
    columns=[];current=[]
    for donor in fit['donors']:
        d=tr[tr.geography.eq(donor)&tr.n_samples.gt(0)]
        signal=(d.poll_baseline-d.prior).groupby(d.cycle).mean()
        vals=np.array([signal.get(y,np.nan) for y in years]);known=np.isfinite(vals)
        mean=sum(w[known]*vals[known])/sum(w[known]);sd=np.sqrt(sum(w[known]*(vals[known]-mean)**2)/sum(w[known]))
        assert known.sum()>=MIN_PAIRS and donor!=state
        assert np.isclose(mean,fit['means'][donor]) and np.isclose(sd,fit['scales'][donor])
        columns.append(np.array([(v-mean)/sd if np.isfinite(v) else 0. for v in vals]))
        now=history[history.cycle.eq(year)&history.geography.eq(donor)&history.n_samples.gt(0)]
        raw=float((now.poll_baseline-now.prior).mean());assert np.isclose(raw,fit['current_signals'][donor])
        current.append((raw-mean)/sd)
    x=np.column_stack([np.ones(len(years)),*columns]);reg=np.diag([INTERCEPT_MASS]+[fit['alpha']]*len(columns))
    gram=x.T@(w[:,None]*x);beta=np.linalg.solve(gram+reg,x.T@(w*response.to_numpy()))
    expected=np.array([fit['intercept'],*fit['coefficients'].values()])
    difference=float(np.max(np.abs(beta-expected)));assert difference<1e-10
    df=float(np.trace(np.linalg.solve(gram+reg,gram)));assert np.isclose(df,fit['effective_df'])
    correction=float(np.r_[1.,current]@beta);assert np.isclose(correction,fit['total_adjustment'])
    return difference,correction


def run_experiment(lab,parent):
    lab,parent=Path(lab).resolve(),Path(parent).resolve()
    stack=max((parent/'bias_momentum_stack').glob('*/manifest.json')).parent
    sources=dict(history=stack/'prequential_bias_history.parquet',membership=parent/'cv/competitive/membership.parquet',
                 references=stack/'predictions.parquet',data_inputs=parent/'poll_error_models/data_inputs.json')
    hashes={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in sources.items()}
    h=pd.read_parquet(sources['history']);h=h[h.base.eq('fixed5_8')].copy();before=h.copy(deep=True)
    out=parent/'state_peers'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True)
    print('State-peer experiment:',out,flush=True)
    frames,fits=evaluate(h,progress=lambda m:print(m,flush=True))
    p=frames['predictions'];calls,_,_,_=classification_report(p)
    calls,cycles,summary=senate_report(calls,pd.read_parquet(sources['membership']))
    groups=[]
    for period,start in [('recent2016',2016),('all2012',2012)]:
        for (scenario,model),g in calls[calls.classification_status.eq('cv_scored')&calls.cycle.ge(start)].groupby(['scenario','model']):
            for label,q in [('all',g),('competitive',g[g.history_selection_10pp.eq('competitive')]),
                    ('not_selected',g[g.history_selection_10pp.eq('not_selected')]),('unknown_history',g[g.history_selection_10pp.eq('unknown_history')]),
                    ('no_polls',g[g.n_samples.eq(0)]),('sparse_1to3_firms',g[g.n_samples.gt(0)&g.n_firms.le(3)]),
                    ('well_polled_4plus_firms',g[g.n_firms.ge(4)])]:
                if len(q):groups.append(dict(period=period,scenario=scenario,model=model,group=label,n=len(q),correct=int(q.correct.sum()),
                    mae_pp=100*(q.prediction-q.actual).abs().groupby(q.cycle).mean().mean()))
    groups=pd.DataFrame(groups)
    for _,g in groups.groupby(['period','scenario','model']):
        d=g.set_index('group')
        for labels in [['competitive','not_selected','unknown_history'],['no_polls','sparse_1to3_firms','well_polled_4plus_firms']]:
            assert d.loc[labels,'n'].sum()==d.loc['all','n']
            assert d.loc[labels,'correct'].sum()==d.loc['all','correct']
    # Independently reconstruct each unique selected state fit; verify duplicate blend reuse too.
    audit=[];cache={}
    prediction_groups=dict(tuple(p.groupby(['scenario','cycle','model','geography'])))
    source_groups={key:g.set_index('target_id') for key,g in h.groupby(['scenario','cycle','geography'])}
    scenario_history=dict(tuple(h.groupby('scenario')))
    for f in fits:
        key=(f['scenario'],f['cycle'],f['geography'],f['base'],f['architecture'],f['alpha'],f['lookback'])
        if key not in cache:cache[key]=independent_fit(scenario_history[f['scenario']],f)
        difference,correction=cache[key]
        assert np.isclose(correction,f['total_adjustment'])
        sample=prediction_groups[(f['scenario'],f['cycle'],f['model'],f['geography'])]
        # Match the final saved prediction including clipping and coverage-aware blend.
        source=source_groups[(f['scenario'],f['cycle'],f['geography'])]
        for row in sample.itertuples():
            r=source.loc[row.target_id];basevalue=r[BASES[f['base']]]
            expected=np.clip(basevalue+correction,-1,1) if f['base']=='prior' or r.n_samples>0 else basevalue
            if '__blend_' in f['model']:
                own=r[BASES[f['model'].split('__')[0]]]
                expected=(1-row.peer_weight)*own+row.peer_weight*expected
            assert np.isclose(expected,row.prediction,atol=1e-11)
        audit.append(dict(scenario=f['scenario'],cycle=f['cycle'],model=f['model'],geography=f['geography'],max_coefficient_difference=difference))
    print('Independently verified',len(cache),'unique state fits;',len(fits),'saved fit applications',flush=True)
    # Every chosen hyperparameter must minimize its own earlier-cycle table.
    for s in frames['selections'].itertuples():
        grid=frames['tuning'];g=grid[grid.scenario.eq(s.scenario)&grid.cycle.eq(s.cycle)&grid.model.eq(s.model)]
        def order(r):
            scale=-1 if r['scale']=='none' else float('inf') if r['scale']=='all' else 0 if r['scale']=='not_applicable' else float(r['scale'])
            return round(r['validation_mae_pp']/100,12),scale,-r['alpha']
        chosen=min(g.to_dict('records'),key=order)
        assert chosen['alpha']==s.alpha and chosen['scale']==s.scale and np.isclose(chosen['validation_mae_pp'],s.validation_mae_pp)
        assert g.validation_cycle.eq(s.cycle-2).all()
    # Exact unchanged reference parity with previous experiments.
    refs=pd.read_parquet(sources['references']);parity={}
    for model,old in [('prior','prior'),('polling','polling'),('bias','base_fixed5_8')]:
        a=p[p.model.eq(model)][['scenario','target_id','prediction']]
        b=refs[refs.model.eq(old)][['scenario','target_id','prediction']]
        q=a.merge(b,on=['scenario','target_id'],validate='one_to_one',suffixes=('_a','_b'))
        assert len(q)==len(a) and np.allclose(q.prediction_a,q.prediction_b,atol=1e-12);parity[model]=len(q)
    pd.testing.assert_frame_equal(h,before)
    assert p[p.cycle.eq(2026)].actual.isna().all() and not p[p.cycle.eq(2026)].scenario.eq('oct31').any()
    # Reliability of individual states is descriptive held-out performance, never a selection input.
    scored=calls[calls.classification_status.eq('cv_scored')&calls.cycle.ge(2016)]
    scored=scored.assign(absolute_error_pp=100*(scored.prediction-scored.actual).abs())
    reliability=scored.groupby(['scenario','model','geography']).agg(cycles=('cycle','nunique'),contests=('target_id','size'),
        correct=('correct','sum'),mae_pp=('absolute_error_pp','mean')).reset_index()
    reliability['accuracy']=reliability.correct.astype(float)/reliability.contests
    rel=pd.concat([relationships(g,2026,w).assign(scenario=scenario) for scenario,g in h.groupby('scenario') for w in [5,10]],ignore_index=True)
    current=p[p.cycle.eq(2026)].pivot(index=['scenario','target_id','geography','n_samples','n_firms'],columns='model',values='prediction')*100
    changes=[]
    for (scenario,model),g in scored.groupby(['scenario','model']):
        if '__' not in model:continue
        base=model.split('__')[0];ref=scored[scored.scenario.eq(scenario)&scored.model.eq(base)][['target_id','prediction','correct']]
        q=g.merge(ref,on='target_id',suffixes=('','_base'),validate='one_to_one')
        q=q[np.sign(q.prediction)!=np.sign(q.prediction_base)].copy();q['change']=np.where(q.correct,'repaired','spoiled')
        changes.append(q[['scenario','cycle','geography','target_id','model','actual','prediction_base','prediction','change','n_samples','n_firms','history_selection_10pp']])
    fit_table=pd.DataFrame([{k:f[k] for k in ['scenario','cycle','model','geography','base','architecture','alpha','lookback','training_cycles','effective_cycles',
        'training_max_cycle','intercept','peer_adjustment','total_adjustment','status','effective_df']}|{'donor_count':len(f['donors'])} for f in fits])
    frames.update(state_calls=calls,cycle_metrics=cycles,summary=summary,groups=groups,relationships=rel,state_reliability=reliability,
        current_states=current.reset_index(),fit_summary=fit_table,independent_audit=pd.DataFrame(audit),changed_calls=pd.concat(changes,ignore_index=True))
    for name,frame in frames.items():frame.to_parquet(out/(name+'.parquet'),index=False)
    (out/'fits.json').write_text(json.dumps(fits,indent=2,allow_nan=False)+'\n')
    settings=dict(version='interstate-observable-poll-shifts-v1',training_windows=[10,5],history_half_life_years=HALF_LIFE,
        min_pair_cycles=MIN_PAIRS,intercept_pseudo_cycles=INTERCEPT_MASS,alpha_grid=[1,10,100],
        observable_predictor='donor chronological poll forecast minus donor chronological prior; target state excluded',
        blend='peer weight scale/(scale+n_firms); no polls -> peer weight1; explicit no-peer candidate',
        missing='training observed donor mean, standardized to zero; absent current donors excluded',
        tuning='Y-2 MAE; fixed architecture/window reported separately; none favored in blend ties',
        references=parity,independent_unique_state_fits=len(cache),automatic_model_promotion=False,
        source_files={k:dict(path=str(path),sha256=hashes[k]) for k,path in sources.items()})
    (out/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
    shutil.copy2(sources['data_inputs'],out/'source_data_inputs.json')
    for name in ['state_peer_models.py','run_state_peers.py','winner_classification.py','senate_summary.py']:
        shutil.copy2(lab/'scripts'/name,out/name)
    for k,path in sources.items():assert hashlib.sha256(path.read_bytes()).hexdigest()==hashes[k]
    (out/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name!='manifest.json'},indent=2)+'\n')
    print('Complete:',out,flush=True)
    return out,frames,fits


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--parent',type=Path,required=True);args=parser.parse_args()
    run_experiment(Path(__file__).resolve().parents[1],args.parent)
