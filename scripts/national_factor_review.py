"""National-strength, history-weighting, and leave-state-polls-out experiments."""
from pathlib import Path
from datetime import datetime,timezone
import json
import numpy as np
import pandas as pd
import simple_national_model as model
import working_election_model as working
import coverage_balance as scoring
import simple_bayesian_polling as v1
import national_tails_waves as chamber

SOURCE='20260920T000314.601869Z'
STRENGTHS={'N_off':0.,'N_half':.5,'N_current':1.,'N_double':2.}
TIE_ORDER=['N_current','N_half','N_double','N_off']
CONFIG=dict(strength_variance_multipliers=STRENGTHS,history_half_lives=[4.,8.,16.],
    other_cycle_type_weight=.5,validation_cycles=3,selection_metric='seat_crps',draws=30000,seed=197139,as_of='2026-09-17')


def allocation(base,multiplier,budget):
    if not np.isfinite(multiplier) or multiplier<0:raise ValueError('Invalid national variance multiplier')
    requested=float(base*multiplier);upper=float(np.min(budget)*(1-1e-8))
    return min(requested,upper),bool(requested>upper)


def choose(scores,year):
    q=scores[scores.cycle.lt(year)&scores.model.isin(STRENGTHS)]
    years=sorted(q.cycle.unique())[-3:]
    if len(years)<3:return 'N_current',years,'early_fixed_fallback'
    q=q[q.cycle.isin(years)]
    if len(q)!=3*len(STRENGTHS) or q.duplicated(['cycle','model']).any():raise ValueError('Incomplete validation grid')
    s=q.groupby('model').seat_crps.mean()
    if not np.isfinite(s).all():raise ValueError('Nonfinite validation score')
    chosen=min(TIE_ORDER,key=lambda name:(s[name],TIE_ORDER.index(name)))
    return chosen,years,'last_three_past_cycles_seat_CRPS'


def inputs(test,budget,a,poll):
    """Independent scalar precision derivation of the national update."""
    ids=np.flatnonzero(test.q_pp.notna());si=np.array([v1.STATES.index(s) for s in test.geography.iloc[ids]])
    if not np.allclose(poll['bias_covariance'],np.diag(np.diag(poll['bias_covariance'])),atol=1e-10) or poll['common_variance']!=0:
        raise ValueError('This input decomposition requires independent polling and bias errors')
    V=np.asarray(budget)[si];P=poll['budget'][si];B=np.diag(poll['bias_covariance'])[si]
    F=16/test.firm_mass.to_numpy()[ids];d=V-a+P+B+F
    variance=1/(1/a+np.sum(1/d)) if a>0 else 0.
    weight=variance/d;prior_pp=100*test.prior.to_numpy()[ids];raw=test.q_pp.to_numpy()[ids];bias=poll['bias_mean'][si]
    surprise=raw-bias-prior_pp
    table=pd.DataFrame(dict(state=test.geography.iloc[ids].to_numpy(),target_id=test.target_id.iloc[ids].to_numpy(),
        raw_poll_pp=raw,historical_bias_pp=bias,corrected_poll_pp=raw-bias,prior_pp=prior_pp,surprise_pp=surprise,
        residual_variance_pp2=d,weight=weight,contribution_pp=weight*surprise))
    return table,dict(N_mean_pp=float(weight@surprise),N_variance=variance,prior_weight=1-float(weight.sum()))


def mask_one(test,index):
    hidden=test.copy();hidden.loc[hidden.index[index],'q_pp']=np.nan
    return hidden


def chamber_summary(seats):
    rows=[]
    for period,first in [('recent_2016_2024',2016),('tuned_2018_2024',2018),('all_2012_2024',2012)]:
        for (sc,name),q in seats[seats.cycle.between(first,2024)].groupby(['scenario','model']):
            rows.append(dict(period=period,scenario=sc,model=name,cycles=len(q),**q[['seat_crps','seat_wis','expected_seat_error','coverage70','coverage95','width70','width95']].mean().to_dict()))
    return pd.DataFrame(rows)


def build(lab):
    lab=Path(lab).resolve();designation,source,working_tables=working.load(lab)
    if source.name!=SOURCE or designation['model_id']!='no_U_K1':raise ValueError('This pinned review requires the approved no_U_K1 source')
    source_sha=v1.verify(source);source_settings=json.loads((source/'settings.json').read_text());prior=Path(source_settings['prior_source'])
    out=lab/'reports/national_factor_review'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for name in ['fits','forecasts','recipe']:(out/name).mkdir(parents=True,exist_ok=True)
    print('OUTPUT',out,flush=True)
    settings=dict(config=CONFIG,source=str(source),source_sha256=source_sha,prior_source=str(prior),prior_source_sha256=v1.verify(prior),
        working_designation_sha256=v1.sha(lab/'WORKING_MODEL.json'),promotion=False,data_refreshed=False,
        old_notebook_hashes={p.name:v1.sha(p) for p in lab.glob('*.ipynb') if p.name!='NATIONAL_FACTOR_REVIEW.ipynb'})
    v1.json_write(out/'settings.json',settings)
    upstream=Path(source_settings['upstream']);roster=pd.read_parquet(upstream/'full_seat_ledger.parquet')
    predictions=[];folds=[];seats=[];hidden_rows=[];input_rows=[];weights=[];profiles=[];fit_rows=[];checks=[]
    for r in working_tables['folds'].sort_values(['scenario','cycle']).itertuples():
        sc,year=r.scenario,int(r.cycle)
        test=working_tables['predictions'][working_tables['predictions'].scenario.eq(sc)&working_tables['predictions'].cycle.eq(year)].sort_values('target_id').reset_index(drop=True)
        fit=dict(np.load(source/f'fits/{sc}_{year}_movement_K1.npz'));pf=dict(np.load(source/f'fits/{sc}_{year}_poll.npz'))
        budget=fit['budget'];poll=model.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        bank={name:(*allocation(r.N_variance,mult,budget),8.) for name,mult in STRENGTHS.items()}
        for half in [4.,8.,16.]:
            years=fit['years'];w=np.exp2(-(year-years)/half)*np.where(years%4==year%4,1.,.5)
            if half==8:np.testing.assert_allclose(w,fit['training_weights'],atol=1e-12)
            for t,ww,x in zip(years,w,fit['training_values']):
                finite=x[np.isfinite(x)]
                weights.append(dict(scenario=sc,forecast_cycle=year,half_life=half,source_cycle=int(t),weight=float(ww),normalized_cycle_weight=float(ww/w.sum()),
                    observed_states=len(finite),mean_residual_pp=float(finite.mean()),rms_residual_pp=float(np.sqrt(np.mean(finite**2)))))
            if half==8:continue
            new=model.fit_common(fit['training_values'],fit['training_noise'],w,budget)
            name=f'history{int(half)}';bank[name]=(new['common_variance'],False,half)
            path=f'fits/{sc}_{year}_{name}.npz';np.savez_compressed(out/path,**{k:v for k,v in new.items() if isinstance(v,np.ndarray)},years=years)
            fit_rows.append(dict(scenario=sc,cycle=year,model=name,half_life=half,N_variance=new['common_variance'],
                optimizer_success=new['optimizer_success'],at_lower=new['at_lower'],at_upper=new['at_upper'],training_max_cycle=int(years.max()),objective=new['objective'],path=path))
            profiles.extend(dict(scenario=sc,cycle=year,model=name,N_variance=x,nll=y) for x,y in zip(new['profile_grid'],new['profile_nll']))
        rng=np.random.default_rng(CONFIG['seed']+year+10000*(sc=='oct31'));z=rng.standard_normal((CONFIG['draws'],len(test)))
        for name,(a,capped,half) in bank.items():
            p,cov,stats,meta=model.predict(test,budget,a,poll);p['model']=name
            table,scalar=inputs(test,budget,a,poll)
            np.testing.assert_allclose(stats['N_mean_pp'],scalar['N_mean_pp'],atol=1e-9)
            np.testing.assert_allclose(stats['N_sd_pp']**2,scalar['N_variance'],atol=1e-9)
            obs=meta['observed'];P=poll['budget'][[v1.STATES.index(s) for s in test.geography.iloc[obs]]]
            B=np.diag(poll['bias_covariance'])[[v1.STATES.index(s) for s in test.geography.iloc[obs]]]
            V=budget[[v1.STATES.index(s) for s in test.geography.iloc[obs]]];F=16/test.firm_mass.to_numpy()[obs]
            local_gain=(V-a)/(V-a+P+B+F)
            combined=100*test.prior.to_numpy()[obs]+local_gain*p.poll_surprise_pp.to_numpy()[obs]+(1-local_gain)*stats['N_mean_pp']
            np.testing.assert_allclose(combined,p.prediction_pp.to_numpy()[obs],atol=1e-9)
            table=table.assign(scenario=sc,cycle=year,model=name)
            input_rows.append(table);predictions.append(p)
            draws=p.prediction_pp.to_numpy()+z@np.linalg.cholesky(cov).T
            rr=roster[roster.scenario.eq(sc)&roster.cycle.eq(year)]
            ss,counts=chamber.seat_summary(rr,test,p,draws);ss.update(scenario=sc,cycle=year,model=name)
            frequency=np.bincount(counts,minlength=101);seats.append(scoring.seat_scores(ss,frequency))
            path=f'forecasts/{sc}_{year}_{name}.npz'
            np.savez_compressed(out/path,target_ids=test.target_id.to_numpy(str),mean=p.prediction_pp.to_numpy(),covariance=cov,
                prior_covariance=meta['prior_covariance'],seat_count_frequency=frequency,gain=meta['gain'])
            folds.append(dict(scenario=sc,cycle=year,model=name,N_variance=a,base_N_variance=r.N_variance,
                effective_multiplier=a/r.N_variance if r.N_variance>0 else np.nan,capped=capped,half_life=half,
                training_max_cycle=int(fit['years'].max()),prior_weight=scalar['prior_weight'],forecast_path=path,**stats))
            if name=='N_current':
                cols=['prediction_pp','p_dem','lo70_pp','hi70_pp','lo95_pp','hi95_pp']
                sourcefreq=np.load(source/r.forecast_path)['seat_count_frequency']
                checks.append(np.allclose(p[cols],test[cols],atol=1e-9) and np.array_equal(frequency,sourcefreq))
            for idx in np.flatnonzero(test.q_pp.notna()):
                hidden=mask_one(test,idx);hp,hcov,hs,hm=model.predict(hidden,budget,a,poll)
                trace,hscalar=inputs(hidden,budget,a,poll)
                np.testing.assert_allclose(hs['N_mean_pp'],hscalar['N_mean_pp'],atol=1e-9)
                if test.target_id.iloc[idx] in set(trace.target_id):raise AssertionError('Hidden poll entered national update')
                target=hp.iloc[[idx]].copy().assign(model=name,held_out_poll_pp=test.q_pp.iloc[idx],
                    full_prediction_pp=p.prediction_pp.iloc[idx],full_N_pp=stats['N_mean_pp'],hidden_N_pp=hs['N_mean_pp'],
                    hidden_N_sd_pp=hs['N_sd_pp'],other_polled_states=len(trace))
                hidden_rows.append(target)
        print(sc,year,'six settings and hidden-state checks complete',flush=True)
    p=pd.concat(predictions,ignore_index=True);seats=pd.DataFrame(seats);folds=pd.DataFrame(folds);hidden=pd.concat(hidden_rows,ignore_index=True)
    trace=[];selected=[];selected_seats=[];selected_folds=[];selected_hidden=[]
    for sc,group in p.groupby('scenario'):
        for year in sorted(group.cycle.unique()):
            chosen,years,status=choose(seats[seats.scenario.eq(sc)],year)
            def take(table):return table[table.scenario.eq(sc)&table.cycle.eq(year)&table.model.eq(chosen)].assign(model='N_seat_selected',selected_model=chosen)
            selected.append(take(p));selected_seats.append(take(seats));selected_folds.append(take(folds));selected_hidden.append(take(hidden))
            for name in STRENGTHS:
                q=seats[seats.scenario.eq(sc)&seats.cycle.isin(years)&seats.model.eq(name)]
                trace.append(dict(scenario=sc,forecast_cycle=year,candidate=name,selected_model=chosen,validation_cycles=','.join(map(str,years)),
                    validation_max_cycle=max(years) if years else np.nan,status=status,mean_validation_CRPS=q.seat_crps.mean()))
    p=pd.concat([p,*selected],ignore_index=True);seats=pd.concat([seats,*selected_seats],ignore_index=True);folds=pd.concat([folds,*selected_folds],ignore_index=True);hidden=pd.concat([hidden,*selected_hidden],ignore_index=True)
    # Artificially hidden states were originally polled; keep this separate from naturally missing polls.
    hidden_scored=hidden.copy();hidden_scored['q_pp']=hidden_scored.held_out_poll_pp
    tables=dict(predictions=p,seats=seats,folds=folds,inputs=pd.concat(input_rows,ignore_index=True),history_weights=pd.DataFrame(weights),
        fit_diagnostics=pd.DataFrame(fit_rows),fit_profiles=pd.DataFrame(profiles),tuning=pd.DataFrame(trace),hidden_predictions=hidden,
        summary=scoring.summarize_scores(p),hidden_summary=scoring.summarize_scores(hidden_scored),chamber_summary=chamber_summary(seats))
    for name,table in tables.items():table.to_parquet(out/(name+'.parquet'),index=False)
    v1.json_write(out/'reproduction.json',dict(passed=all(checks),folds=len(checks)))
    for path in (lab/'scripts').glob('*.py'):(out/'recipe'/path.name).write_bytes(path.read_bytes())
    (out/'NATIONAL_FACTOR_REVIEW.md').write_bytes((lab/'NATIONAL_FACTOR_REVIEW.md').read_bytes())
    v1.manifest(out);audit(out,lab);report(out,lab)
    v1.json_write(out.parent/'latest.json',dict(artifact=out.name,manifest_sha256=v1.sha(out/'manifest.json')))
    return out


def audit(out,lab):
    out,lab=Path(out),Path(lab);v1.verify(out);s=json.loads((out/'settings.json').read_text());source=Path(s['source'])
    p=pd.read_parquet(out/'predictions.parquet');f=pd.read_parquet(out/'folds.parquet');seats=pd.read_parquet(out/'seats.parquet');h=pd.read_parquet(out/'hidden_predictions.parquet');t=pd.read_parquet(out/'tuning.parquet');i=pd.read_parquet(out/'inputs.parquet');w=pd.read_parquet(out/'history_weights.parquet');fits=pd.read_parquet(out/'fit_diagnostics.parquet')
    _,_,working_tables=working.load(lab)
    c=dict(source_unchanged=v1.verify(source)==s['source_sha256'],prior_source_unchanged=v1.verify(s['prior_source'])==s['prior_source_sha256'],
        working_designation_unchanged=v1.sha(lab/'WORKING_MODEL.json')==s['working_designation_sha256'],
        older_notebooks_preserved=all(v1.sha(lab/name)==digest for name,digest in s['old_notebook_hashes'].items()),
        current_strength_reproduces_working=json.loads((out/'reproduction.json').read_text())['passed'],
        no_future_training=bool(f.training_max_cycle.lt(f.cycle).all() and w.source_cycle.lt(w.forecast_cycle).all() and fits.training_max_cycle.lt(fits.cycle).all()),
        positive_weights=bool(i.weight.ge(0).all()),weights_sum_below_one=bool(i.groupby(['scenario','cycle','model']).weight.sum().lt(1+1e-10).all()),
        hidden_observation_missing=bool(h.q_pp.isna().all() and h.held_out_poll_pp.notna().all()),
        hidden_local_update_zero=bool(h.local_electoral_update_pp.eq(0).all()),
        hidden_mean_equals_prior_plus_other_N=bool(np.allclose(h.prediction_pp,100*h.prior+h.hidden_N_pp,atol=1e-9)),
        off_means_exact_prior=bool(np.allclose(h[h.model.eq('N_off')].prediction_pp,100*h[h.model.eq('N_off')].prior)),
        current_labels_missing=bool(p[p.cycle.eq(2026)][['actual','wis_pp','brier']].isna().all().all() and h[h.cycle.eq(2026)][['actual','wis_pp','brier']].isna().all().all()),
        future_seat_scores_missing=bool(seats[seats.cycle.eq(2026)][['actual_D','seat_crps']].isna().all().all()),
        unique_full_forecasts=not p.duplicated(['scenario','target_id','model']).any(),unique_hidden_forecasts=not h.duplicated(['scenario','target_id','model']).any(),
        fit_optimizers_succeeded=bool(fits.optimizer_success.all()),no_U=bool(f.U_mean_pp.eq(0).all()))
    same=[];reconstructed=[];selected=[];hidden_reconstructed=[]
    for r in f[f.model.ne('N_seat_selected')].itertuples():
        test=working_tables['predictions'][working_tables['predictions'].scenario.eq(r.scenario)&working_tables['predictions'].cycle.eq(r.cycle)].sort_values('target_id').reset_index(drop=True)
        fit=dict(np.load(source/f'fits/{r.scenario}_{r.cycle}_movement_K1.npz'));pf=dict(np.load(source/f'fits/{r.scenario}_{r.cycle}_poll.npz'));poll=model.fixed_common(pf['training_values'],pf['training_noise'],pf['training_weights'],pf['budget'],0.,9.)
        q=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.cycle)&p.model.eq(r.model)].sort_values('target_id');z=np.load(out/r.forecast_path)
        expected,cov,stats,_=model.predict(test,fit['budget'],r.N_variance,poll)
        same.append(np.array_equal(q.target_id,test.target_id) and np.array_equal(q.prior,test.prior) and np.allclose(np.diag(z['prior_covariance']),fit['budget'][[v1.STATES.index(st) for st in test.geography]]))
        ss=seats[seats.scenario.eq(r.scenario)&seats.cycle.eq(r.cycle)&seats.model.eq(r.model)].iloc[0]
        reconstructed.append(np.allclose(q.prediction_pp,expected.prediction_pp,atol=1e-9) and np.allclose(z['covariance'],cov,atol=1e-9) and abs(ss.expected_D_exact-ss.fixed_D-q.p_dem.sum())<1e-9 and z['seat_count_frequency'].sum()==CONFIG['draws'])
        for idx in np.flatnonzero(test.q_pp.notna()):
            hidden=mask_one(test,idx);trace,scalar=inputs(hidden,fit['budget'],r.N_variance,poll)
            saved=h[h.scenario.eq(r.scenario)&h.cycle.eq(r.cycle)&h.model.eq(r.model)&h.target_id.eq(test.target_id.iloc[idx])].iloc[0]
            hidden_reconstructed.append(test.target_id.iloc[idx] not in set(trace.target_id) and abs(saved.prediction_pp-100*test.prior.iloc[idx]-scalar['N_mean_pp'])<1e-9 and abs(saved.hidden_N_sd_pp**2-scalar['N_variance'])<1e-9)
    for r in t.drop_duplicates(['scenario','forecast_cycle']).itertuples():
        chosen,years,status=choose(seats[seats.scenario.eq(r.scenario)],r.forecast_cycle)
        a=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq('N_seat_selected')].sort_values('target_id');b=p[p.scenario.eq(r.scenario)&p.cycle.eq(r.forecast_cycle)&p.model.eq(chosen)].sort_values('target_id')
        selected.append(chosen==r.selected_model and status==r.status and ','.join(map(str,years))==r.validation_cycles and all(y<r.forecast_cycle for y in years) and np.allclose(a.prediction_pp,b.prediction_pp))
    c.update(prior_centers_and_budgets_preserved=all(same),full_forecasts_and_seats_reconstructed=all(reconstructed),hidden_predictions_reconstructed_independently=all(hidden_reconstructed),past_only_seat_selector_reconstructed=all(selected))
    result=dict(passed=all(c.values()),checks=c,forecast_rows=len(p),hidden_rows=len(h),new_recency_fits=len(fits),older_notebooks=len(s['old_notebook_hashes']))
    v1.json_write(out/'audit.json',result)
    if not result['passed']:raise AssertionError([k for k,v in c.items() if not v])
    v1.manifest(out);return result


def report(out,lab):
    out,lab=Path(out),Path(lab);summary=pd.read_parquet(out/'summary.parquet');ch=pd.read_parquet(out/'chamber_summary.parquet');hidden=pd.read_parquet(out/'hidden_summary.parquet');f=pd.read_parquet(out/'folds.parquet');seats=pd.read_parquet(out/'seats.parquet');t=pd.read_parquet(out/'tuning.parquet');inputs_table=pd.read_parquet(out/'inputs.parquet');p=pd.read_parquet(out/'predictions.parquet')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for ax,sc in zip(axes,['matched_live','oct31']):
        for table,label in [(summary,'Normal polling'),(hidden,'State polls hidden')]:
            q=table[table.period.eq('recent_2016_2024')&table.group.eq('all')&table.scenario.eq(sc)].set_index('model')
            ax.plot([0,.5,1,2],[q.loc[name,'absolute_error_pp'] for name in STRENGTHS],marker='o',label=label)
        ax.set(title=sc,xlabel='National variance multiplier',ylabel='Cycle-average margin MAE (pp)');ax.legend()
    fig.tight_layout();fig.savefig(out/'hidden_state_error.png',dpi=145);plt.close(fig)
    q=inputs_table[inputs_table.cycle.eq(2026)&inputs_table.model.eq('N_current')].sort_values('contribution_pp')
    fig,ax=plt.subplots(figsize=(9,6));ax.barh(q.state,q.contribution_pp,color=np.where(q.contribution_pp.ge(0),'#377eb8','#e66101'));ax.axvline(0,color='black',lw=.7);ax.set(xlabel='Contribution to national D−R shift (pp)',title='2026 national factor: each state’s weighted polling surprise');fig.tight_layout();fig.savefig(out/'current_inputs.png',dpi=145);plt.close(fig)
    text='# National electoral factor review\n\nFrozen September17 data; U=0, K1, historical bias/noise and marginal prior budgets fixed. Variance multipliers0/.5/1/2 plus separate4/16year history diagnostics. Working designation unchanged.\n\n'
    cols=['scenario','model','n','correct','absolute_error_pp','wis_pp','brier','coverage70','coverage95']
    for period in ['recent_2016_2024','tuned_2018_2024','all_2012_2024']:
        text+='## '+period+'\n\n'+summary[summary.period.eq(period)&summary.group.eq('all')][cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Recent joint chamber scores\n\n'+ch[ch.period.eq('recent_2016_2024')].round(4).to_markdown(index=False)+'\n\n'
    text+='## Leave-state-polls-out\n\nEach row predicts an originally polled state after hiding its own current aggregate. Different hidden states are different inference runs, not one joint chamber forecast.\n\n'+hidden[hidden.period.eq('recent_2016_2024')&hidden.group.eq('all')][cols].round(4).to_markdown(index=False)+'\n\n'
    text+='## Chronological chamber selection\n\n'+t.drop_duplicates(['scenario','forecast_cycle'])[['scenario','forecast_cycle','selected_model','validation_cycles','status']].to_markdown(index=False)+'\n\n'
    text+='## Current national inputs\n\nInput=raw state poll−historical bias−historical prior. Reliability weights include local election uncertainty, local polling variance, bias uncertainty and firm information; they do not sum to1 because the zero-centered national prior retains weight.\n\n'+q[['state','raw_poll_pp','historical_bias_pp','prior_pp','surprise_pp','weight','contribution_pp']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Current factors and seats\n\n'+f[f.cycle.eq(2026)][['model','N_variance','effective_multiplier','capped','N_mean_pp','N_sd_pp','prior_weight']].round(4).to_markdown(index=False)+'\n\n'+seats[seats.cycle.eq(2026)][['model','point_D','point_R','expected_D_exact','D_lo70','D_hi70','D_lo95','D_hi95']].round(4).to_markdown(index=False)+'\n\n'
    text+='## Historical caps\n\n'+f[f.capped][['scenario','cycle','model','effective_multiplier']].to_markdown(index=False)+'\n\n'
    text+='## Current state predictions\n\n'+p[p.cycle.eq(2026)].pivot(index='geography',columns='model',values='prediction_pp').round(3).to_markdown()+'\n\n'
    text+='## Limits\n\nFive recent elections provide limited chamber evidence. Shared parameter estimates remain empirical Bayes. Hiding well-polled states tests information transfer but does not reproduce the population of naturally unpolled states. State priors/candidate context and completion assumptions remain unchanged. Small seat-score differences depend partly on finite simulation. No new national polling series, economics, approval, signed regional factors or state-specific loadings are used.\n'
    (lab/'NATIONAL_FACTOR_REVIEW_RESULTS.md').write_text(text);(out/'NATIONAL_FACTOR_REVIEW_RESULTS.md').write_text(text);v1.manifest(out)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--lab',type=Path,default=Path(__file__).resolve().parents[1]);args=parser.parse_args();build(args.lab)
