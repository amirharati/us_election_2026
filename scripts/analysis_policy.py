"""Explicit reference overlay for the next experiments; normalized inputs stay intact."""
from copy import deepcopy
import json
from data_utils import LAB
from audit_national_result_2022 import audit as audit_2022
from audit_national_result_2024 import audit as audit_2024


def apply_references(outcomes, historical=None):
    policy=json.loads((LAB/'config/analysis_policy_v1.json').read_text())
    b22=audit_2022()['benchmark']
    b24=audit_2024(historical)['benchmark']
    benchmarks={2022:dict(dem_share=b22['DEM']/b22['total_votes'],rep_share=b22['REP']/b22['total_votes'],
                          dem_rep_margin=b22['margin_pp']/100),2024:b24}
    result=deepcopy(outcomes)
    versions=[]
    for cycle,b in benchmarks.items():
        matches=[r for r in result if r['outcome_type']=='national_house_popular_vote'
                 and r['geography']=='US' and int(r['cycle'])==cycle]
        if len(matches)!=1:raise ValueError(f'Expected one national House outcome for {cycle}')
        row=matches[0]
        versions.append(dict(outcome_id=row['outcome_id'],cycle=cycle,original_status=row['status'],
            original_margin_pp=100*float(row['dem_rep_margin']),analysis_margin_pp=100*b['dem_rep_margin'],
            change_margin_pp=100*(b['dem_rep_margin']-float(row['dem_rep_margin'])),
            analysis_reference=policy['national_result_versions'][str(cycle)],policy_version=policy['policy_version']))
        row.update({f:b[f] for f in ('dem_share','rep_share','dem_rep_margin')})
        row['status']='audited_first_choice_reference'
        row['review_reasons']='reported_candidate_votes_only|two_unopposed_counts_missing|not_turnout_standardized'
    return result,versions
