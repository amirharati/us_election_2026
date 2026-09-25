"""Self-contained model inputs and revision-aware current evidence ingestion.

Provider archives are disposable cache. Historical labels and trained assets are
never changed by live refresh. A compact bundle contains its own checksums,
normalized feature records, screened poll tables, and source receipts.
"""
from pathlib import Path
from datetime import date
import io
import json
import shutil
import tempfile
import hashlib
import numpy as np
import pandas as pd
from data_utils import LAB, atomic_json
from alignment_features import FeatureStore, SPEC, sha

HOME = LAB/'data/compact'
TABLES = ['contest_inputs_reference','labels','polls','poll_quality','poll_identity',
          'poll_metadata','poll_availability','current_contests','seat_ledger','answers']


def seal(path):
    path = Path(path)
    files = {str(p.relative_to(path)): dict(sha256=sha(p), bytes=p.stat().st_size)
             for p in sorted(path.rglob('*')) if p.is_file() and p.name != 'manifest.json'}
    atomic_json(path/'manifest.json', dict(kind='compact_model_inputs', schema_version=1, files=files))
    return path


class CompactDataset:
    def __init__(self, snapshot):
        self.snapshot = Path(snapshot).resolve()
        self.manifest = json.loads((self.snapshot/'manifest.json').read_text())
        if self.manifest.get('kind') != 'compact_model_inputs': raise ValueError('Not compact model inputs')
        self.manifest_sha256 = sha(self.snapshot/'manifest.json')
        for name, info in self.manifest['files'].items():
            p = (self.snapshot/name).resolve()
            if not p.is_relative_to(self.snapshot) or sha(p) != info['sha256']:
                raise ValueError('Compact input checksum mismatch: '+name)
        self.policy = json.loads((self.snapshot/'policy.json').read_text())
        self.provenance = json.loads((self.snapshot/'provenance.json').read_text())
        self.summary = json.loads((self.snapshot/'summary.json').read_text())
        self.checks = self.validate()

    def load_table(self, name):
        rel = 'tables/'+name+'.parquet'
        if rel not in self.manifest['files']: raise KeyError(name)
        p = self.snapshot/rel
        if sha(p) != self.manifest['files'][rel]['sha256']: raise ValueError('Changed compact table: '+name)
        return pd.read_parquet(p)

    def feature_store(self):
        monthly = pd.read_parquet(self.snapshot/'feature_monthly.parquet')
        political = json.loads((self.snapshot/'political.json').read_text())
        return FeatureStore.from_monthly(monthly, political, self.policy['as_of'])

    def validate(self):
        polls = self.load_table('polls'); labels = self.load_table('labels')
        contests = self.load_table('contest_inputs_reference')
        if not polls.observation_id.is_unique or not labels.target_id.is_unique:
            raise ValueError('Duplicate compact poll/target identity')
        if not contests.target_id.is_unique or set(contests.target_id) != set(labels.target_id):
            raise ValueError('Compact contest/label mismatch')
        if not set(polls.target_id.dropna()) <= set(labels.target_id): raise ValueError('Dangling compact poll target')
        for name in ['poll_quality','poll_identity','poll_metadata','poll_availability']:
            t = self.load_table(name)
            if not t.observation_id.is_unique or set(t.observation_id) != set(polls.observation_id):
                raise ValueError('Incomplete compact metadata: '+name)
        future = labels[labels.cycle.eq(2026)]
        if len(future) != 36 or not future[['dem_share','rep_share','dem_rep_margin']].isna().all().all():
            raise ValueError('Current outcome leakage or missing contests')
        if {'dem_share','rep_share','dem_rep_margin','poll_error'} & set(contests):
            raise ValueError('Outcome in compact predictor table')
        seats = self.load_table('seat_ledger')
        if len(seats) != 100 or not seats.seat_id.is_unique: raise ValueError('Invalid seat ledger')
        if not set(self.load_table('answers').observation_id) <= set(polls.observation_id):
            raise ValueError('Dangling compact answer')
        return dict(compact_checksums=True, poll_rows=len(polls), targets=len(labels), future_labels_blank=True)


def export(snapshot, destination):
    """One-time extraction from an already audited legacy bundle."""
    from load_final_dataset import open_dataset
    from contextual_baselines import make_store
    from refresh_2026 import verified_receipt
    data = open_dataset(snapshot); store = make_store(data)
    out = Path(destination); out.mkdir(parents=True, exist_ok=False)
    (out/'tables').mkdir(); (out/'feeds').mkdir()
    for name in TABLES: data.load_table(name).to_parquet(out/'tables'/f'{name}.parquet', index=False)
    pd.DataFrame(store.records).to_parquet(out/'feature_records.parquet', index=False)
    monthly = pd.DataFrame(store.monthly_rows); monthly['month'] = monthly.month.astype(str)
    monthly.to_parquet(out/'feature_monthly.parquet', index=False)
    atomic_json(out/'political.json', store.political)
    atomic_json(out/'policy.json', data.policy); atomic_json(out/'summary.json', data.summary)
    atomic_json(out/'provenance.json', dict(format='compact-v1', extracted_from=str(Path(snapshot).resolve().relative_to(LAB)),
        source_manifest_sha256=sha(Path(snapshot)/'manifest.json'),
        historical_inputs='Frozen reviewed labels and model series; raw-source audit performed at extraction',
        source_manifests=data.provenance['manifests']))
    if out.name == 'frozen':
        seal(out); CompactDataset(out)
        return out
    accepted = LAB/data.provenance['accepted_snapshot']
    ac = json.loads((accepted/'config.json').read_text())
    raw = LAB/ac['snapshots']['current_raw']['path']
    for label, name in [('senate','tables/senate_general_answers.csv'), ('generic_ballot','raw/silver_bulletin_generic.csv')]:
        pd.read_csv(raw/name, dtype=str, keep_default_na=False).to_parquet(out/'feeds'/f'{label}.parquet', index=False)
    for name in ['contests_2026.csv','chamber_2026.json']:
        shutil.copyfile(raw/'config'/name, out/'feeds'/name)
    receipts = {'polls': verified_receipt(raw)}
    inputs = json.loads((LAB/data.provenance['prepared_feature_snapshot']/'inputs.json').read_text())
    for entry in inputs['bundles']:
        bundle = LAB/entry['path']; request = json.loads((bundle/'request.json').read_text())
        if request['mode'] == 'current':
            source = request['source']; r = verified_receipt(bundle)
            r['retrieved_at'] = json.loads((bundle/'manifest.json').read_text())['retrieved_at']
            if source not in receipts or r['retrieved_at'] > receipts[source].get('retrieved_at',''): receipts[source] = r
    # Store receipts and source hashes, not mandatory local archive paths.
    receipts = {k:{a:b for a,b in v.items() if a != 'snapshot'} for k,v in receipts.items()}
    atomic_json(out/'sources.json', receipts)
    atomic_json(out/'provenance.json', dict(format='compact-v1', extracted_from=str(Path(snapshot).resolve().relative_to(LAB)),
        source_manifest_sha256=sha(Path(snapshot)/'manifest.json'),
        historical_inputs='Frozen reviewed labels and model series; raw-source audit performed at extraction',
        source_manifests=data.provenance['manifests']))
    seal(out); CompactDataset(out)
    return out


def feature_update(path, results):
    """Replace changed providers' current normalized records; preserve history.

    Whole current-feed replacement handles source removals as well as revised
    observations. Historical source records remain available as in the original
    historical+current preparation pipeline.
    """
    from prepare_features import Builder, stable
    from types import SimpleNamespace
    records = pd.read_parquet(path/'feature_records.parquet')
    old = json.loads((path/'sources.json').read_text())
    for r in results:
        source = r['source']
        if source == 'polls' or 'raw_snapshot' not in r or r['manifest_sha256'] == old[source]['manifest_sha256']: continue
        raw = Path(r['raw_snapshot']); m = json.loads((raw/'manifest.json').read_text())
        artifacts = []
        for name, info in m['files'].items():
            if not name.startswith('raw/'): continue
            origin = dict(path=str((raw/name).relative_to(LAB)), retrieved_at=info.get('retrieved_at',m['retrieved_at']))
            artifacts.append(dict(id=stable((source,Path(name).name,info['sha256']))[:24], source=source,
                path=origin['path'], sha256=info['sha256'], origins=[origin]))
        with tempfile.TemporaryDirectory(dir=LAB/'cache', prefix='feature-normalize-') as temp:
            stage = Path(temp)
            class SelectedBuilder(Builder):
                def write(self, name, row, key=None):
                    specs = [s for s in SPEC.values() if s[0] == self.source+'/'+name]
                    if not specs: return
                    if self.source == 'ucsb':
                        keep = any(row.get('measure') == s[1] and row.get('respondent_party') == s[2] for s in specs)
                    else:
                        keep = any((s[1] is None or row.get('series') == s[1]) and
                                   (s[2] is None or row.get('group') == s[2]) for s in specs)
                    if keep: super().write(name,row,key)
            b = SelectedBuilder(SimpleNamespace(stage=stage))
            try:
                for a in artifacts: b.run(a)
            finally: b.finish()
            atomic_json(stage/'catalog.json', b.catalog)
            atomic_json(stage/'inputs.json', dict(artifacts=artifacts))
            political = json.loads((path/'political.json').read_text())
            s = FeatureStore(stage, political, json.loads((path/'policy.json').read_text())['as_of'], records_only=True)
            new = pd.DataFrame(s.records)
            if new.empty: raise ValueError('No model series from refreshed provider: '+source)
            new['scope'] = 'current'
            records = pd.concat([records[~(records.source.eq(source)&records.scope.eq('current'))],new],ignore_index=True)
    records.to_parquet(path/'feature_records.parquet', index=False)


def _csv_types(rows):
    """Match the established CSV normalizer's null and dtype interpretation."""
    from data_utils import csv_bytes
    fields = list(dict.fromkeys(k for r in rows for k in r))
    return pd.read_csv(io.BytesIO(csv_bytes(fields,rows)),low_memory=False)


def poll_update(path, result, as_of):
    from prepare_data import current_questions, select_current
    from normalize_data import current_senate, current_generic
    from audit_refresh_2026 import csv_form, compare
    from build_accepted_data import current_identity, default_metadata, disposition
    from audit_survey_identity import label
    source = json.loads((path/'sources.json').read_text())['polls']
    old = {n:pd.read_parquet(path/'feeds'/f'{n}.parquet').to_dict('records') for n in ['senate','generic_ballot']}
    raw = old
    if 'raw_snapshot' in result and result['manifest_sha256'] != source['manifest_sha256']:
        p = Path(result['raw_snapshot'])
        if (p/'config/contests_2026.csv').read_bytes() != (path/'feeds/contests_2026.csv').read_bytes():
            raise ValueError('Contest roster changed; explicit mapping review required')
        raw = {}
        for name, rel in [('senate','tables/senate_general_answers.csv'),('generic_ballot','raw/silver_bulletin_generic.csv')]:
            frame = pd.read_csv(p/rel,dtype=str,keep_default_na=False)
            if list(frame) != list(old[name][0]): raise ValueError('Poll source schema changed')
            raw[name] = frame.to_dict('records')
        from audit_refresh_2026 import validate_race_ids
        validate_race_ids(old['senate'],raw['senate'],json.loads((LAB/'config/candidate_review_2026.json').read_text()))
    review = json.loads((LAB/'config/candidate_review_2026.json').read_text())
    facts = json.loads((LAB/'config/survey_identity_v1.json').read_text())
    from current_poll_review import reviewed_feed
    supplements=json.loads((LAB/'config/supplemental_polls_2026.json').read_text())
    reviewed_rows, receipts=reviewed_feed(raw['senate'],supplements,as_of)
    model_raw=dict(raw,senate=reviewed_rows)
    (path/'review').mkdir(exist_ok=True)
    atomic_json(path/'review/candidate_review.json',review)
    atomic_json(path/'review/supplemental_polls.json',supplements)
    atomic_json(path/'review/receipts.json',receipts)
    pd.DataFrame(reviewed_rows).to_parquet(path/'feeds/reviewed_senate.parquet',index=False)
    qs, ans = current_questions(reviewed_rows,review,as_of); select_current(qs,as_of,14)
    obs, answers = current_senate(csv_form(qs),csv_form(ans))
    national, national_answers = current_generic(raw['generic_ballot'],as_of)
    obs += national; answers += national_answers
    # Content-derived version avoids new identities for unchanged source data.
    version = hashlib.sha256((result['manifest_sha256']+json.dumps(review,sort_keys=True)+json.dumps(supplements,sort_keys=True)).encode()).hexdigest()[:20]
    links = {member:x['canonical'] for x in facts['sample_links'] for member in x['members']}
    pending = {member for x in facts['pending_duplicates'] for member in x['members']}
    for o in obs:
        o['canonical_sample_group_id'] = links.get(o['sample_group_id'],o['sample_group_id'])
        o['identity_review_status'] = ('confirmed_sample_link' if o['sample_group_id'] in links else
            'possible_duplicate_retained' if o['sample_group_id'] in pending else 'no_documented_link')
        o['poll_error_vs_result'] = None
    obs = csv_form(obs)
    template = pd.read_parquet(path/'tables/poll_metadata.parquet')
    aliases = {label(n):a['canonical'] for a in facts['aliases'] for n in a['names']}
    identity=[]; metadata=[]; quality=[]; polls=[]
    ids = {o['observation_id']:'refresh/'+version+'/'+o['observation_id'] for o in obs}
    for o in obs:
        oid=ids[o['observation_id']]
        x=dict(o); x.pop('poll_error_vs_result',None)
        x.pop('question_basis',None)  # Reviewed basis belongs in poll_metadata; preserve poll schema.
        x.update(observation_id=oid,origin_bundle='refresh',origin_snapshot=version,origin_observation_id=o['observation_id'])
        i=current_identity(o,model_raw,aliases,facts);i['observation_id']=oid
        pr=review.get('poll_reviews',{}).get(o['source_poll_id'],{})
        if pr.get('sample_group_id'):
            i['canonical_sample_group_id']=pr['sample_group_id']
            i['sample_identity_status']='conservative_same_firm_overlap'
        identity.append(i)
        b=default_metadata(o,list(template));b['observation_id']=oid
        # A known publication/archive date is a conservative availability bound.
        # Never make supplementary polls visible to a replay before publication.
        b['documented_release_date']=o['source_available_date']
        b['availability_status']='known_publication_or_archive_bound'
        if o.get('question_basis')=='initial':
            b['question_construct']='vote_intention';b['estimate_basis']='full_sample'
            b['basis_review_status']='primary_release_reviewed'
        metadata.append(b)
        x['canonical_sample_group_id']=i['canonical_sample_group_id']
        status,reason=disposition(x,None,{})
        quality.append(dict(observation_id=oid,cycle=x['cycle'],geography=x['geography'],dataset=x['dataset'],
            source=x['source'],outcome_id=x['outcome_id'],review_status=status,review_reason=reason))
        if x.get('superseded_by'):
            x['origin_superseded_by']=x['superseded_by'];x['superseded_by']='|'.join(ids[k] for k in x['superseded_by'].split('|'))
        polls.append(x)
    p=_csv_types(polls); meta=_csv_types(metadata); ident=_csv_types(identity); qual=_csv_types(quality)
    current=pd.read_parquet(path/'tables/current_contests.parquet')
    p['alignment_date']=pd.to_datetime(p.poll_end.fillna(p.poll_date))
    valid=p.alignment_date.notna()&p.alignment_date.le(pd.Timestamp(as_of))
    p['context_id']=p.alignment_date.dt.strftime('%Y-%m-%d').where(valid)
    p['alignment_status']=np.where(p.alignment_date.isna(),'missing_poll_date',np.where(valid,'dated','after_dataset_cutoff'))
    p['target_id']=p.geography.map(current.set_index('state').contest_id)
    p.loc[p.dataset.eq('generic_ballot'),'target_id']='2026-US-house-popular-vote-future'
    qual=qual.merge(p[['observation_id','context_id','target_id','alignment_status']],on='observation_id',validate='one_to_one')
    availability=meta[['observation_id','documented_release_date','availability_status','archive_created_date']].copy()
    availability['snapshot_observed_date']=pd.Timestamp(as_of)
    availability=availability.merge(p[['observation_id','context_id']],on='observation_id',validate='one_to_one')
    # Carry forward the original observation receipt for unchanged logical rows.
    before=pd.read_parquet(path/'tables/polls.parquet')
    before_av=pd.read_parquet(path/'tables/poll_availability.parquet').set_index('observation_id')
    old_dates=before.set_index('origin_observation_id').observation_id.map(before_av.snapshot_observed_date).to_dict()
    availability['snapshot_observed_date']=[old_dates.get(o,pd.Timestamp(as_of)) for o in p.origin_observation_id]
    release=pd.to_datetime(availability.documented_release_date); cutoff=pd.to_datetime(availability.context_id)
    availability['poll_known_by_context_date']=pd.Series(pd.NA,index=availability.index,dtype='boolean')
    availability.loc[release.gt(cutoff),'poll_known_by_context_date']=False
    availability.loc[release.le(cutoff)|cutoff.ge(availability.snapshot_observed_date),'poll_known_by_context_date']=True
    answers=[{**a,'observation_id':ids[a['observation_id']]} for a in answers]
    replacements=dict(polls=p,poll_metadata=meta,poll_identity=ident,poll_quality=qual,
                      poll_availability=availability,answers=_csv_types(answers))
    historical_ids=set(before.loc[before.cycle.lt(2026),'observation_id'])
    for name, frame in replacements.items():
        dest=path/'tables'/f'{name}.parquet'; historical=pd.read_parquet(dest)
        historical=historical[historical.observation_id.isin(historical_ids)]
        pd.concat([historical,frame],ignore_index=True).to_parquet(dest,index=False)
    for i,c in current.iterrows():
        pool=[q for q in qs if q['state']==c.state]
        current.loc[i,['source_questions','accepted_questions','selected_questions']]=[len(pool),sum(q['accepted_matchup'] for q in pool),sum(q['selection']=='selected' for q in pool)]
        current.loc[i,'polling_status']='source_present' if pool else 'no_source_polls'
    current.to_parquet(path/'tables/current_contests.parquet',index=False)
    for name, rows in raw.items(): pd.DataFrame(rows).to_parquet(path/'feeds'/f'{name}.parquet',index=False)
    return {name:compare(old[name],raw[name]) for name in raw}


def prepare(base, results, as_of, destination):
    """Build and validate a candidate; caller promotes only after inference succeeds."""
    CompactDataset(base)
    out=Path(destination);shutil.copytree(base,out)
    policy=json.loads((out/'policy.json').read_text());policy['as_of']=str(as_of)
    atomic_json(out/'policy.json',policy)
    changes=poll_update(out,next(r for r in results if r['source']=='polls'),as_of)
    feature_update(out,results)
    records=pd.read_parquet(out/'feature_records.parquet')
    store=FeatureStore.from_records(records,json.loads((out/'political.json').read_text()),as_of)
    monthly=pd.DataFrame(store.monthly_rows);monthly['month']=monthly.month.astype(str)
    monthly.to_parquet(out/'feature_monthly.parquet',index=False)
    frame=pd.read_parquet(out/'tables/contest_inputs_reference.parquet')
    context=store.at(str(as_of))[0]
    for col,value in context.items():
        if col in frame: frame.loc[frame.cycle.eq(2026),col]=value
    frame.loc[frame.cycle.eq(2026),'forecast_days_to_election']=(pd.to_datetime(frame.loc[frame.cycle.eq(2026),'election_date'])-pd.Timestamp(as_of)).dt.days
    frame.to_parquet(out/'tables/contest_inputs_reference.parquet',index=False)
    receipts=json.loads((out/'sources.json').read_text())
    for r in results:
        receipts[r['source']]={k:v for k,v in r.items() if k not in ['source','snapshot','raw_snapshot']}
    atomic_json(out/'sources.json',receipts)
    atomic_json(out/'changes.json',changes)
    provenance=json.loads((out/'provenance.json').read_text())
    provenance['previous_compact_manifest']=sha(Path(base)/'manifest.json')
    provenance['update']='Replace current poll feed and changed current feature partitions; historical partitions unchanged'
    atomic_json(out/'provenance.json',provenance)
    summary=json.loads((out/'summary.json').read_text());summary['as_of']=str(as_of)
    atomic_json(out/'summary.json',summary)
    seal(out);CompactDataset(out)
    return out


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--extract',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(export(a.extract,a.output))

if __name__=='__main__':main()
