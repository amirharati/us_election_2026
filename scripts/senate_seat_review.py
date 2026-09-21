"""Review frozen forecasts with complete seat accounting, without refitting models.

Historical unmodeled races are shown explicitly. A separate incumbent-caucus
completion scenario supplies a 100-seat point tally; it is not scored as though
those calls came from the tested model. All counts refer to caucus blocs.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
import numpy as np
import pandas as pd

YEARS=[2016,2018,2020,2022,2024]
SPECIAL={2016:{},2018:{'MN':2,'MS':2},2020:{'AZ':3,'GA':3},2022:{'OK':2},2024:{'NE':2}}
ACTUAL_DEM={2016:48,2018:47,2020:50,2022:51,2024:47}
MODELS=['prior','polling','bias','bias__blend_all__last10']


def caucus_code(value):
    return {'Democrat':'D','Democratic':'D','DEM':'D','Republican':'R','REP':'R'}.get(value,'I')


def affiliation_at(term,date):
    """Use dated affiliation segments, not the most recent party on a long term."""
    segments=term.get('party_affiliations')
    if isinstance(segments,list):
        matches=[p for p in segments if str(p['start'])<=date<=str(p['end'])]
        if not matches:raise ValueError('Date not covered by affiliation history')
        chosen=max(matches,key=lambda p:str(p['start']))
        return chosen['party'],chosen.get('caucus',chosen['party'])
    caucus=term.get('caucus')
    return term['party'],caucus if isinstance(caucus,str) else term['party']


def roster_at(terms,date):
    eligible=terms[(terms.start<=date)&(terms.end>date)].copy();rows=[]
    for t in eligible.to_dict('records'):
        party,caucus=affiliation_at(t,date)
        rows.append(dict(state=t['state'],seat_class=int(t['class']),incumbent=t['name'],party=party,
            caucus=caucus_code(caucus),bioguide=t['bioguide'],affiliation_as_of=date))
    result=pd.DataFrame(rows)
    if len(result)!=100 or result.duplicated(['state','seat_class']).any() or not result.groupby('state').size().eq(2).all():
        raise ValueError('Roster does not identify exactly100unique seats')
    if not result.caucus.isin(['D','R']).all():raise ValueError('Unresolved independent caucus')
    return result


def historical_roster(terms,year,cutoff):
    before=roster_at(terms,cutoff);regular=((year-2016)//2+2)%3+1
    before['contested']=before.seat_class.eq(regular)|before.apply(lambda r:SPECIAL[year].get(r.state)==r.seat_class,axis=1)
    before['special']=before.contested&before.seat_class.ne(regular)
    before['target_id']=before.apply(lambda r:f'{year}-{r.state}-'+('special' if r.special else 'regular')+'-gen' if r.contested else None,axis=1)
    before['seat_id']=before.state+'-class'+before.seat_class.astype(str)
    # Labels enter only this separate outcome join; they do not set a forecast.
    after=roster_at(terms,f'{year+1}-01-31')[['state','seat_class','caucus']].rename(columns={'caucus':'actual_caucus'})
    result=before.merge(after,on=['state','seat_class'],validate='one_to_one')
    assert result.actual_caucus.eq('D').sum()==ACTUAL_DEM[year]
    assert result.loc[~result.contested,'caucus'].equals(result.loc[~result.contested,'actual_caucus'])
    return result


def review_forecasts(roster,forecasts,year,scenario,model,restrictions=None):
    q=forecasts[['target_id','prediction','actual','n_samples','n_firms']].copy()
    if q.target_id.duplicated().any():raise ValueError('Duplicate model target')
    if not set(q.target_id)<=set(roster.loc[roster.contested,'target_id']):raise ValueError('Forecast does not map to a scheduled seat')
    ledger=roster.merge(q,on='target_id',how='left',validate='many_to_one')
    ledger['cycle']=year;ledger['scenario']=scenario;ledger['model']=model
    ledger['model_called']=ledger.contested&ledger.prediction.notna()&ledger.prediction.ne(0)
    ledger['model_caucus']=np.where(ledger.model_called,np.where(ledger.prediction>0,'D','R'),None)
    ledger['completion_caucus']=ledger.model_caucus.where(ledger.model_called,ledger.caucus)
    ledger['call_basis']=np.select([~ledger.contested,ledger.model_called],['continuing_seat','model_margin_sign'],default='incumbent_caucus_completion_assumption')
    ledger['prediction_pp']=100*ledger.prediction;ledger['actual_margin_pp']=100*ledger.actual
    ledger['correct_model_call']=np.where(ledger.model_called&ledger.actual_caucus.notna(),ledger.model_caucus==ledger.actual_caucus,np.nan)
    if year<2026:
        admitted=ledger[ledger.model_called]
        assert admitted.actual.notna().all()
        assert np.array_equal(np.where(admitted.actual>0,'D','R'),admitted.actual_caucus)
    else:assert ledger.actual.isna().all()
    if restrictions is not None:
        ledger=ledger.merge(restrictions,on='target_id',how='left',validate='many_to_one')
    known=ledger[~ledger.contested|ledger.model_called]
    unknown=int((ledger.contested&~ledger.model_called).sum())
    nd=int(ledger.completion_caucus.eq('D').sum());nr=int(ledger.completion_caucus.eq('R').sum());assert nd+nr==100
    modeled=ledger[ledger.model_called];scored=year<2026
    summary=dict(cycle=year,scenario=scenario,model=model,contested=int(ledger.contested.sum()),continuing=int((~ledger.contested).sum()),
        continuing_D=int((~ledger.contested&ledger.caucus.eq('D')).sum()),continuing_R=int((~ledger.contested&ledger.caucus.eq('R')).sum()),
        modeled_contests=len(modeled),modeled_correct=int(modeled.correct_model_call.sum()) if scored else None,
        modeled_mae_pp=float(100*(modeled.prediction-modeled.actual).abs().mean()) if scored else None,
        modeled_D_wins=int(modeled.model_caucus.eq('D').sum()),modeled_R_wins=int(modeled.model_caucus.eq('R').sum()),
        unmodeled_contests=unknown,completion_D=nd,completion_R=nr,
        assigned_D_before_completion=int(known.completion_caucus.eq('D').sum()),assigned_R_before_completion=int(known.completion_caucus.eq('R').sum()),
        min_D_over_unmodeled=int(known.completion_caucus.eq('D').sum()),max_D_over_unmodeled=int(known.completion_caucus.eq('D').sum())+unknown,
        actual_D=int(ledger.actual_caucus.eq('D').sum()) if scored else None,
        actual_R=int(ledger.actual_caucus.eq('R').sum()) if scored else None,
        completion_correct=int((ledger.loc[ledger.contested,'completion_caucus']==ledger.loc[ledger.contested,'actual_caucus']).sum()) if scored else None,
        tally_status='model_plus_explicit_incumbent_completion' if unknown else 'conditional_DR_sign_tally_not_rule_certified')
    return ledger,pd.DataFrame([summary])


def run_review(lab,parent,source_dir):
    lab,parent,source_dir=map(lambda p:Path(p).resolve(),[lab,parent,source_dir])
    peer=max((parent/'state_peers').glob('*/manifest.json')).parent
    inputs=dict(predictions=peer/'state_calls.parquet',calendars=parent/'contextual/calendars.parquet',
                terms=source_dir/'senate_terms_recent.json',data_inputs=parent/'poll_error_models/data_inputs.json')
    metadata=json.loads(inputs['data_inputs'].read_text());snapshot=Path(metadata['dataset']['snapshot'])
    inputs.update(current_roster=snapshot/'tables/seat_ledger.parquet',current_contests=snapshot/'tables/current_contests.parquet',
                  restrictions=snapshot/'tables/result_restrictions.parquet',candidate_policy=lab/'config/candidate_review_2026.json')
    hashes={k:hashlib.sha256(v.read_bytes()).hexdigest() for k,v in inputs.items()}
    forecasts=pd.read_parquet(inputs['predictions']);forecasts=forecasts[forecasts.model.isin(MODELS)&forecasts.cycle.ge(2016)]
    terms=pd.read_json(inputs['terms']);cal=pd.read_parquet(inputs['calendars'])
    restrictions=pd.read_parquet(inputs['restrictions'])[['outcome_id','reasons']].rename(columns={'outcome_id':'target_id','reasons':'historical_exclusion_reason'})
    ledgers=[];summary=[]
    for (scenario,year),group in forecasts.groupby(['scenario','cycle']):
        if year==2026:
            roster=pd.read_parquet(inputs['current_roster']).rename(columns={'continuing_caucus':'held_caucus'})
            roster['caucus']=roster.held_caucus.map(caucus_code).where(roster.status.eq('continuing'),roster.party.map(caucus_code))
            roster['contested']=roster.status.eq('contested');roster['target_id']=roster.contest_id
            roster['actual_caucus']=None
        else:
            c=cal[cal.scenario.eq(scenario)&cal.cycle.eq(year)]
            assert len(c)==1;cutoff=str(c.context_id.iloc[0])[:10]
            roster=historical_roster(terms,int(year),cutoff)
        for model,q in group.groupby('model'):
            ledger,row=review_forecasts(roster,q,int(year),scenario,model,restrictions)
            ledgers.append(ledger);summary.append(row)
    full=pd.concat(ledgers,ignore_index=True);totals=pd.concat(summary,ignore_index=True)
    assert full.groupby(['cycle','scenario','model']).size().eq(100).all()
    # Duplicated CA same-seat special/regular ballots and later runoffs are never extra seats.
    counts={2016:34,2018:35,2020:35,2022:35,2024:34,2026:35}
    assert totals.contested.eq(totals.cycle.map(counts)).all()
    current=full[full.cycle.eq(2026)&full.model.eq('bias')&full.contested].copy()
    cc=pd.read_parquet(inputs['current_contests'])
    current=current.merge(cc[['contest_id','election_rule','seat_mapping_restrictions','seat_forecast_ready']],left_on='target_id',right_on='contest_id',suffixes=('','_manifest'),validate='one_to_one')
    policy=json.loads(inputs['candidate_policy'].read_text())['contests']
    current['independent_candidate_flag']=current.state.map(lambda s:any(c['party']=='IND' for c in policy[s]['candidates']))
    current['candidate_names']=current.state.map(lambda s:'; '.join(c['name']+' ('+c['party']+')' for c in policy[s]['candidates']))
    current['material_rule_flag']=current.election_rule.ne('plurality')|current.independent_candidate_flag
    current['within_1pp']=current.prediction_pp.abs()<1
    out=parent/'seat_review'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ');out.mkdir(parents=True)
    for name,df in dict(full_seat_ledger=full,seat_totals=totals,historical_states=full[full.cycle.lt(2026)&full.contested],current_states=current).items():
        df.to_parquet(out/(name+'.parquet'),index=False)
    settings=dict(version='senate-seat-review-v1',as_of=metadata['dataset']['as_of'],primary_model='bias',
        primary_recipe='current-cycle polling + last5calendar-cycle,8-year-decayed state error calibration; shrinkage onY-2',
        best_definition='retrospectively strongest simple late-cycle winner-call reference; not uniquely best or untouched holdout',
        historical_completion='pre-cutoff incumbent caucus retained for unmodeled races; explicitly separate from model calls',
        actual_convention='Senate membership Jan31following election, includes delayed Georgia2020 runoffs; caucus blocs',
        current_convention='continuing34D/31R plus sign of35D-R forecasts; conditional on rule/caucus/ballot mappings',
        certified_seat_forecast=False,independent_caucus='D total includes Democratic-caucusing independents',
        source_files={k:dict(path=str(v),sha256=hashes[k]) for k,v in inputs.items()})
    (out/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
    shutil.copy2(Path(__file__),out/Path(__file__).name)
    for k,p in inputs.items():assert hashlib.sha256(p.read_bytes()).hexdigest()==hashes[k]
    (out/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file() and p.name!='manifest.json'},indent=2)+'\n')
    print('Saved',out);print(totals[totals.model.eq('bias')].to_string(index=False))
    return out


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--parent',type=Path,required=True);p.add_argument('--source-dir',type=Path,required=True);a=p.parse_args()
    run_review(Path(__file__).resolve().parents[1],a.parent,a.source_dir)
