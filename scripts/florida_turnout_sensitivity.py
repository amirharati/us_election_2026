"""Anchored Florida Senate poll sensitivity to lower Republican turnout.

Inputs: ActiVote October27 2026 release. This is a deterministic sensitivity,
not a model forecast or an estimate of the likelihood of a turnout scenario.
"""
import csv
import json
from pathlib import Path

SOURCE = 'https://www.activote.net/polls/2026/fl-u-s-senate/2026-10-27/'


def simulate(target_gap_pp):
    # Baseline electorate counts in arbitrary units; their total is one.
    # D/I counts and all group preferences stay fixed. Only R count changes.
    r0, d0 = .45, .32
    non_r0 = 1 - r0
    g = target_gap_pp / 100
    if not -d0 / non_r0 <= g < 1:
        raise ValueError('Infeasible electorate gap')
    r = (d0 + g * non_r0) / (1 - g)
    total = r + non_r0
    # Anchor published 53/47 topline, changing only Republican votes.
    # Rounded published party crosstabs do not reproduce the topline exactly.
    moody = (.53 + .97 * (r - r0)) / total
    nixon = (.47 + .03 * (r - r0)) / total
    assert abs(moody + nixon - 1) < 1e-12
    assert abs((r - d0) / total - g) < 1e-12
    return dict(target_r_minus_d_pp=target_gap_pp,
                republican_share_pct=100*r/total,
                democratic_share_pct=100*d0/total,
                independent_other_share_pct=100*(non_r0-d0)/total,
                republican_turnout_reduction_pct=100*(1-r/r0),
                moody_pct=100*moody, nixon_pct=100*nixon,
                moody_minus_nixon_pp=100*(moody-nixon))


def main():
    out=Path(__file__).resolve().parents[1]/'outputs/reports/research/florida_turnout'
    out.mkdir(parents=True,exist_ok=True)
    rows=[simulate(g) for g in [13,10,8,5,3]]
    assert abs(rows[0]['moody_pct']-53)<1e-10
    assert all(a['nixon_pct']<b['nixon_pct'] for a,b in zip(rows,rows[1:]))
    with (out/'scenarios.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    metadata=dict(source=SOURCE,field_dates=['2026-10-17','2026-10-27'],
        baseline=dict(r_share_pct=45,d_share_pct=32,moody_pct=53,nixon_pct=47,
                      moody_among_republicans_pct=97,nixon_among_republicans_pct=3),
        method='Reduce Republican voter count only; hold all other voter counts and within-group preferences fixed. Anchor published topline and subtract removed Republican votes before renormalizing.',
        limitations=['One-poll deterministic sensitivity; not a forecast or win probability.',
                     'Party composition gaps are not party-specific turnout rates.',
                     'Published rounded party shares sum to 99%; residual non-R/D share is grouped as independent/other.',
                     'Published rounded party crosstabs do not exactly reconstruct the topline; anchoring preserves the original 53/47 result.',
                     'Subgroup sampling uncertainty and changing voter preferences are not modeled.'])
    (out/'assumptions.json').write_text(json.dumps(metadata,indent=2)+'\n')
    for r in rows:
        print('R+{target_r_minus_d_pp:g}: Moody {moody_pct:.2f}, Nixon {nixon_pct:.2f}; R turnout reduction {republican_turnout_reduction_pct:.2f}%'.format(**r))


if __name__=='__main__':
    main()
