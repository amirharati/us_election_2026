"""Independent arithmetic review of saved four-score runs; no model changes.

Rebuilds dated economic inputs from monthly data, score scales/weights and median
fills from calendar rows, and ridge fits with normal equations (not sklearn or the
model's score transformer). Rechecks prior chronology and inner selection.
"""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from load_final_dataset import open_run_dataset

COLUMNS=['economy_conditions_wh','economy_momentum_wh','approval_wh','disruption_any']


def same(a,b):
    np.testing.assert_allclose(np.asarray(a,dtype=float),np.asarray(b,dtype=float),atol=1e-10,rtol=1e-9,equal_nan=True)


def design(train,test,recipe):
    """Independent fixed-score formula, no imports from scoring implementation."""
    stats={};outputs=[];component_records=[]
    for name,spec in recipe['components'].items():
        known=train[name].dropna().to_numpy(dtype=float)
        sd=float(np.std(known,ddof=0)) if len(known) else np.nan
        center=float(np.mean(known)) if len(known) and spec['center']=='history_mean' else 0.
        stats[name]=dict(n=len(known),scale=sd,center=center)
    for frame in [train,test]:
        values=pd.DataFrame(index=frame.index);parts={}
        for name,spec in recipe['components'].items():
            st=stats[name];z=(frame[name]-st['center'])/st['scale'] if st['n']>=3 and st['scale']>1e-12 else pd.Series(np.nan,index=frame.index)
            parts[name]=spec['direction']*np.clip(z,-recipe['clip_component_abs'],recipe['clip_component_abs'])
        for score in ['economy_conditions','economy_momentum']:
            names=[c for c,s in recipe['components'].items() if s['score']==score]
            weighted=pd.DataFrame({c:parts[c]*recipe['components'][c]['weight'] for c in names})
            raw=weighted.sum(axis=1,min_count=len(names))
            values[score+'_wh']=raw*(2*frame.wh_dem-1)
        values['approval_wh']=np.clip((frame.approval_3m_pct-50)/10,-3,3)*(2*frame.wh_dem-1)
        values['disruption_any']=frame.extraordinary_event_any_4y
        outputs.append(values)
    a,b=outputs;fills={c:float(a[c].median()) for c in COLUMNS if a[c].notna().any()}
    active=[c for c in COLUMNS if c in fills and np.std(a[c].fillna(fills[c]),ddof=0)>1e-12]
    x=a[active].fillna(fills).to_numpy();z=b[active].fillna(fills).to_numpy()
    return x,z,a,b,stats,fills,active


def solve(x,y,z,alpha):
    xm=x.mean(axis=0);ym=y.mean()
    beta=np.linalg.solve((x-xm).T@(x-xm)+alpha*np.eye(x.shape[1]),(x-xm).T@(y-ym))
    intercept=float(ym-xm@beta)
    return z@beta+intercept,beta,intercept


def review(run,output):
    run=Path(run);output=Path(output);output.mkdir(parents=True,exist_ok=False)
    for folder in [run,run.parent/'feature_scores']:
        for name,sha in json.loads((folder/'manifest.json').read_text()).items():
            assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==sha,(folder,name)
    recipe=json.loads((run/'fixed_feature_scores_v2.json').read_text())
    data=open_run_dataset(run/'data_inputs.json')
    cal=pd.read_parquet(run.parent/'feature_scores/source_calendars.parquet')
    monthly=data.load_table('feature_monthly_inputs')
    sources={k:g.assign(month=pd.PeriodIndex(g.month,freq='M')).set_index('month') for k,g in monthly.groupby('series')}
    def raw_at(source,cutoff,kind='level',lag=12):
        g=sources[source];cutoff=pd.Timestamp(cutoff);last=cutoff.to_period('M')-1
        g=g[(g.index<=last)&(pd.to_datetime(g.reference_end)<=cutoff)]
        if g.empty:return np.nan
        anchor=g.index.max()
        if (cutoff-pd.Timestamp(g.loc[anchor,'reference_end'])).days>120:return np.nan
        indices=pd.period_range(anchor-2,anchor,freq='M') if kind=='mean' else pd.PeriodIndex([anchor-lag,anchor]) if kind=='growth' else pd.PeriodIndex([anchor])
        values=g.reindex(indices).value.to_numpy()
        if not np.isfinite(values).all():return np.nan
        return 100*(values[-1]/values[0]-1) if kind=='growth' else np.mean(values)
    checked_inputs=0
    for row in cal.itertuples():
        levels={'consumer_sentiment_3m':('sentiment','mean',12),'unemployment_pct':('unemployment','level',12),
                'inflation_yoy_pct':('cpi','growth',12),'cpi_24m_pct':('cpi','growth',24),
                'gasoline_yoy_pct':('gasoline','growth',12),'approval_3m_pct':('approval_all','mean',12)}
        for name,(source,kind,lag) in levels.items():
            end=raw_at(source,row.context_id,kind,lag);same(end,getattr(row,name));checked_inputs+=1
            if name in ['consumer_sentiment_3m','unemployment_pct','inflation_yoy_pct']:
                for anchor,date in [('jan01',row.start_cutoff),('previous_oct31',row.previous_cutoff)]:
                    same(end-raw_at(source,date,kind,lag),getattr(row,name+'__change_'+anchor));checked_inputs+=1
        for name,source in [('cpi_level','cpi'),('gasoline_cpi_level','gasoline')]:
            for anchor,date in [('jan01',row.start_cutoff),('previous_oct31',row.previous_cutoff)]:
                base=raw_at(source,date);end=raw_at(source,row.context_id)
                change=100*(end/base-1) if pd.notna(base) and base>0 and pd.notna(end) else np.nan
                same(change,getattr(row,name+'__pct_change_'+anchor));checked_inputs+=1
        flags=[row.health_disruption_4y,row.financial_disruption_4y,row.security_disruption_4y]
        value=1. if 1 in flags else 0. if all(pd.notna(v) and v==0 for v in flags) else np.nan
        same(value,row.extraordinary_event_any_4y)
    # Recreate Senate selection and prior independently of the model helpers.
    original=data.load_table('contest_inputs_reference');labels=data.load_table('labels')
    targets={}
    for scenario,calendar in cal.groupby('scenario'):
        replace=[c for c in calendar if c in original and c!='cycle']
        t=original.drop(columns=replace).merge(calendar,on='cycle',validate='many_to_one')
        t=t.merge(labels[['target_id','dem_rep_margin','diagnostic_eligible']],on='target_id',validate='one_to_one').rename(columns={'dem_rep_margin':'actual'})
        ok=t.diagnostic_eligible.eq(True)&t.actual.notna()&t.stage.isin(['gen','general'])&t.historical_horizon_comparable&pd.to_datetime(t.election_date).gt(pd.to_datetime(t.context_id))
        t=t[(ok|t.cycle.eq(2026))&t.cycle.mod(2).eq(0)&t.geography.ne('US')].sort_values(['cycle','geography','target_id']).reset_index(drop=True)
        priors=[]
        for row in t.itertuples():
            old=t[t.cycle.lt(row.cycle)&t.actual.notna()];local=old[old.geography.eq(row.geography)]
            bycycle=local.groupby('cycle').actual.mean()
            if len(bycycle):value=.5*bycycle.iloc[-1]+.5*bycycle.mean()
            elif pd.notna(row.prior_state_pres_margin):value=row.prior_state_pres_margin
            elif len(old):value=old.groupby('cycle').actual.mean().mean()
            else:value=0.
            priors.append(value)
        t['prior']=priors;targets[scenario]=t
    fits=json.loads((run/'fits.json').read_text());calls=pd.read_parquet(run/'state_calls.parquet')
    saved_components=pd.read_parquet(run/'components.parquet');saved_contributions=pd.read_parquet(run/'contributions.parquet')
    fitrows=[];checked_stats=0;checked_coefficients=0
    for f in fits:
        if f['model']!='four_scores' or f['status']!='fitted':continue
        scenario,year=f['scenario'],f['cycle'];calendar=cal[cal.scenario.eq(scenario)].set_index('cycle',drop=False)
        t=targets[scenario];train=t[t.cycle.lt(year)&t.actual.notna()];test=t[t.cycle.eq(year)]
        y=(train.actual-train.prior).groupby(train.cycle).mean().sort_index()
        x,z,a,b,stats,fills,active=design(calendar.loc[y.index],calendar.loc[[year]],recipe)
        assert list(y.index)==f['training_cycle_ids'] and len(train)==f['training_rows']
        assert active==f['active_terms']
        for c,st in stats.items():
            recorded=f['normalizer']['statistics'][c]
            assert st['n']==recorded['n'];same(st['center'],recorded['center']);same(st['scale'],recorded['scale']);checked_stats+=1
        for c,v in fills.items():same(v,f['score_fills'][c])
        same(a.to_numpy(),pd.DataFrame(f['training_score_rows']).set_index('cycle').reindex(y.index)[COLUMNS].to_numpy())
        correction,beta,intercept=solve(x,y.to_numpy(),z,f['alpha'])
        same(intercept,f['intercept']);same(beta,[f['coefficients'][c] for c in active]);checked_coefficients+=len(beta)+1
        rows=calls[calls.scenario.eq(scenario)&calls.cycle.eq(year)&calls.model.eq('four_scores')].set_index('target_id').loc[test.target_id]
        same(rows.prior_margin,test.prior);same(rows.prediction,np.clip(test.prior+correction[0],-1,1))
        contribution=saved_contributions[saved_contributions.scenario.eq(scenario)&saved_contributions.cycle.eq(year)]
        same(b[COLUMNS].to_numpy(),contribution[COLUMNS].to_numpy())
        records=saved_components[saved_components.scenario.eq(scenario)&saved_components.cycle.eq(year)]
        for row in records.itertuples():
            spec=recipe['components'][row.component];st=stats[row.component]
            value=calendar.loc[year,row.component];same(value,row.input_value)
            score=spec['direction']*np.clip((value-st['center'])/st['scale'],-3,3) if st['n']>=3 and st['scale']>1e-12 else np.nan
            same(score,row.component_score);same(score*spec['weight'],row.contribution)
        fitrows.append(dict(scenario=scenario,cycle=year,training_cycles=len(y),training_contests=len(train),
            electoral_parameters=len(active)+1,alpha=f['alpha'],dropped='|'.join(f['dropped_terms'])))
    # Independently reproduce every inner validation loss and selected alpha.
    tuning=pd.read_parquet(run/'tuning.parquet')
    for row in tuning.itertuples():
        t=targets[row.scenario];inner=t[t.cycle.lt(row.validation_cycle)&t.actual.notna()];valid=t[t.cycle.eq(row.validation_cycle)]
        y=(inner.actual-inner.prior).groupby(inner.cycle).mean().sort_index()
        calendar=cal[cal.scenario.eq(row.scenario)].set_index('cycle',drop=False)
        x,z,_,_,_,_,_=design(calendar.loc[y.index],calendar.loc[[row.validation_cycle]],recipe)
        correction,_,_=solve(x,y.to_numpy(),z,row.alpha)
        loss=100*np.mean(abs(np.clip(valid.prior+correction[0],-1,1)-valid.actual))
        same(loss,row.validation_mae_pp)
    for (scenario,year),g in tuning.groupby(['scenario','cycle']):
        selected=min(g.itertuples(),key=lambda r:(round(r.validation_mae_pp/100,12),-r.alpha)).alpha
        f=next(f for f in fits if f['scenario']==scenario and f['cycle']==year and f['model']=='four_scores')
        same(selected,f['alpha'])
    # Macro mean across five cycles versus pooled classification across contests.
    cycles=pd.read_parquet(run/'cycle_metrics.parquet');q=cycles[cycles.scenario.eq('oct31')&cycles.subset.eq('all_admitted')&cycles.scope.eq('all_targets')&cycles.cycle.ge(2016)&cycles.status.eq('cv_scored')]
    recent=q.pivot(index='cycle',columns='model',values='state_mae_pp')[['prior','four_scores']]
    recent['improvement_pp']=recent.prior-recent.four_scores
    current=max(f['cycle'] for f in fits);components=saved_components[saved_components.scenario.eq('matched_live')&saved_components.cycle.eq(current)]
    blocks=components.groupby(['score','group']).contribution.sum().unstack()
    outputs=dict(parameters=pd.DataFrame(fitrows),recent_improvements=recent.reset_index(),current_components=components,current_blocks=blocks.reset_index())
    for name,frame in outputs.items():frame.to_parquet(output/(name+'.parquet'),index=False)
    summary=dict(status='passed',source_model_run=str(run.resolve()),source_manifest_sha256=hashlib.sha256((run/'manifest.json').read_bytes()).hexdigest(),
        raw_calendar_formula_checks=checked_inputs,normalization_components_checked=checked_stats,
        model_fits_checked=len(fitrows),electoral_coefficients_checked=checked_coefficients,inner_candidate_losses_checked=len(tuning),
        recent_cycles=len(recent),cycles_with_lower_state_mae=int(recent.improvement_pp.gt(0).sum()),
        mean_state_mae_improvement_pp=float(recent.improvement_pp.mean()),
        meaning='Arithmetic/recipe agreement, not a claim of causal validity or certified historical release vintages')
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (output/'audit_score_model.py').write_bytes(Path(__file__).read_bytes())
    (output/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file()},indent=2)+'\n')
    return summary,outputs


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();summary,_=review(args.run,args.output);print(json.dumps(summary,indent=2))
