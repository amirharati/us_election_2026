"""Version-specific basis/N/availability overlay, keeping source observations intact."""
from datetime import date
from pathlib import Path
from collections import Counter
import json,re
from data_utils import LAB,latest,digest,csv_bytes
from prepare_data import read
from build_audit_tables import enrich
CONFIG=LAB/'config/basis_availability_v1.json'
ROOT=LAB/'reports/source_audit/basis_availability'

def allowed(meta,mode,cutoff):
    """Targeted sensitivity: unreviewed rows are retained, never certified available."""
    if mode not in {'retrospective','exclude_announced_after','exclude_later_linked','evidence_required_in_reviewed_subset'}:raise ValueError(mode)
    s=meta['availability_status'];d=meta['documented_release_date']
    if mode=='retrospective':return True
    if s=='not_reviewed':return True
    if s=='documented_before_cutoff':return bool(d and d<=cutoff)
    if s=='announced_after_cutoff':return False
    if mode=='exclude_announced_after':return True
    if s=='found_release_after_cutoff':return bool(d and d<=cutoff)
    if mode=='exclude_later_linked':return True
    if mode=='evidence_required_in_reviewed_subset':return False
    raise ValueError(mode)

def select_available(rows,metadata,mode,cutoff,selector):
    """Version-level gate must precede selection of a preferred question."""
    return selector([r for r in rows if allowed(metadata[r['observation_id']],mode,cutoff)])


def researchco(config):
    root=LAB/'reports/source_audit/estimate_basis'
    proof=json.loads((root/'audit_facts.json').read_text())['cases'][1]
    assert digest((root/'oh_tables.pdf').read_bytes())==proof['pdf_sha256']
    assert digest((root/'oh_tables.txt').read_bytes())==proof['text_sha256']
    pages=(root/'oh_tables.txt').read_text().split('\f');out={}
    for q,a in config['researchco_questions'].items():
        page=config['researchco_pages'][a['state']];s=pages[page-1];bases=list(re.finditer(r'Base: (\d+) (likely|decided) voters in ([A-Za-z ]+)',s));blocks=[];start=0
        for b in bases[:4 if a['state']=='CA' else 2]:
            block=s[start:b.start()];rows=list(re.finditer(r'^([^\n]+?)\(([DR])\)\s+(\d+)%',block,re.M));assert len(rows)==2
            values={x.group(2):int(x.group(3))/100 for x in rows}
            blocks.append(dict(**values,N=int(b.group(1)),basis=b.group(2)));start=b.end()
        full,decided=blocks[2*a['pair_index']:2*a['pair_index']+2]
        assert full['basis']=='likely' and full['N']==450 and decided['basis']=='decided'
        out[q]=dict(**a,page=page,full=full,decided=decided)
    return out

def build(observations=None,outcomes=None):
    p,_=latest(LAB/'data/reviewed');observations=observations if observations is not None else read(p/'tables/observations.csv')
    outcomes=outcomes if outcomes is not None else read(p/'tables/outcomes.csv')
    config=json.loads(CONFIG.read_text())
    for proof in json.loads((ROOT/'provenance.json').read_text()):assert digest((ROOT/proof['file']).read_bytes())==proof['sha256']
    old=json.loads((LAB/'config/estimate_basis_annotations.json').read_text())
    metadata,_=enrich(observations,outcomes,old,date(2026,9,16))
    rc=researchco(config);timing={r['observation_id']:r for r in config['timing']};seen=set();comparisons=[]
    for o,m in zip(observations,metadata):
        m.update(population_n=None,question_construct='unknown',availability_status='not_reviewed',documented_release_date='',availability_evidence='',
                 availability_notes='',archive_created_date=o['source_available_date'],n_conflict_values='',metadata_version=config['version'])
        q=o['source_question_id']
        if o['cycle']=='2022' and o['dataset']=='senate' and q in rc and o['source'] in ('538','538_archive'):
            a=rc[q];assert (o['geography'],o['source_poll_id'])==(a['state'],a['poll_id'])
            assert all(abs(float(o[k])-a['decided'][v])<1e-9 for k,v in [('dem_share','D'),('rep_share','R')]) and float(o['sample_size'])==450
            m.update(reported_n_basis='survey',estimate_basis='decided',survey_n=450,estimate_n=a['decided']['N'],basis_review_status='source_basis_verified',
                     question_construct='candidate_vote_intention',basis_evidence=f'reports/source_audit/estimate_basis/oh_tables.pdf#page={a["page"]}',basis_notes='Reported survey N retained; published decided base separate; includes already cast votes.')
            comparisons.append(dict(observation_id=o['observation_id'],state=a['state'],question=q,source=o['source'],survey_n=450,estimate_n=a['decided']['N'],
                full_margin_pp=100*(a['full']['D']-a['full']['R']),decided_margin_pp=100*(a['decided']['D']-a['decided']['R']),page=a['page']))
        if o['observation_id'] in timing:
            a=timing[o['observation_id']];seen.add(o['observation_id'])
            assert all(o[k]==v for k,v in a['expected'].items()),'Stale timing annotation'
            m.update(availability_status=a['status'],documented_release_date=a['documented_release_date'] or '',availability_evidence=a['evidence'],availability_notes=a['notes'])
            pid=o['source_poll_id']
            if pid=='81635':m.update(question_construct='congress_control_preference',estimate_basis='full_sample',survey_n=1540,estimate_n=float(o['sample_size']),reported_n_basis='published_column_base',basis_review_status='source_basis_verified',basis_evidence='reports/source_audit/national_2022_timing/premise_topline.pdf',basis_notes='Column base shown in weighted table; do not infer effective N or unweighted respondent count.')
            elif pid=='83374':m.update(question_construct='district_vote_intention',estimate_basis='forced_choice_followup',estimate_n=1434,reported_n_basis='estimate',basis_review_status='source_basis_verified',basis_evidence='reports/source_audit/national_2022_timing/wpa_topline.pdf#page=4',basis_notes='Q11 asks undecided respondents a forced-choice follow-up; public table says RV.')
            elif pid=='82000':m.update(question_construct='district_vote_intention',estimate_basis='two_party_prompt',estimate_n=1000,reported_n_basis='estimate',basis_review_status='source_basis_verified',basis_evidence='reports/source_audit/national_2022_timing/cen_topline.pdf')
            elif pid in ('81259','81621') and o['population']=='a':m.update(question_construct='district_vote_intention',estimate_basis='full_sample',survey_n=float(o['sample_size']),estimate_n=float(o['sample_size']),reported_n_basis='survey',basis_review_status='source_basis_verified',basis_evidence=a['evidence'])
        if o['source']=='538_archive' and o['cycle']=='2022' and o['dataset']=='generic_ballot':
            if (o['source_poll_id'],q)==('81591','165185'):
                assert float(o['sample_size'])==1071 and float(o['dem_share'])==.48 and float(o['rep_share'])==.49
                m.update(reported_n_basis='population',population_n=1071,estimate_n=1068,basis_review_status='source_basis_verified',basis_evidence='reports/source_audit/national_2022_timing/yougov.pdf#page=10',basis_notes='Ballot Q6 unweighted base1068 vs broader LV1071; no effective N inferred.')
            if (o['source_poll_id'],q)==('81566','165093'):
                assert float(o['sample_size'])==688 and float(o['dem_share'])==.48 and float(o['rep_share'])==.5
                m.update(reported_n_basis='conflicting_publisher_bases',n_conflict_values='688|708',basis_review_status='publisher_sources_conflict',basis_evidence='NATIONAL_2022_TIMING_AUDIT.md',basis_notes='Both primary sources match shares but disagree on N; estimate N stays unknown.')
    assert seen==set(timing)
    summary=dict(version=config['version'],observations=len(metadata),basis_reviewed=sum(r['basis_review_status']!='not_reviewed' for r in metadata),
        timing_reviewed=len(seen),researchco_versions=len(comparisons),researchco_questions=len(rc),reported_n_unchanged=True,
        availability=dict(Counter(r['availability_status'] for r in metadata)))
    provenance=dict(reviewed_snapshot=p.name,reviewed_manifest_sha256=digest((p/'manifest.json').read_bytes()),
        files={str(f.relative_to(LAB)):digest(f.read_bytes()) for f in [CONFIG,Path(__file__),ROOT/'provenance.json',ROOT/'web_review.json',LAB/'config/estimate_basis_annotations.json',LAB/'reports/source_audit/national_2022_timing/audit_facts.json',LAB/'reports/source_audit/estimate_basis/audit_facts.json']})
    return dict(metadata=metadata,researchco=comparisons,summary=summary,provenance=provenance)

def write(result):
    out=LAB/'reports/data_review'
    for name in ('metadata','researchco'):
        rs=result[name];fields=list(dict.fromkeys(k for r in rs for k in r));(out/f'basis_availability_{name}.csv').write_bytes(csv_bytes(fields,rs))
    (out/'basis_availability_summary.json').write_text(json.dumps(dict(**result['summary'],provenance=result['provenance']),indent=2)+'\n')
if __name__=='__main__':
    result=build();write(result);print(json.dumps(result['summary'],indent=2))
