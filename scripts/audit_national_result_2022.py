"""Offline FEC 2022 House benchmark audit; no changes to source snapshots.

Optional extraction: python audit_national_result_2022.py --extract (openpyxl).
Default audit uses the hash-checked JSON extraction and Python standard library.
"""
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

AUDIT = Path(__file__).resolve().parents[1] / 'reports/source_audit/national_2022_result'
SHEETS = ['1. 2022 Publication Information', '6. Table 5 House by Party',
          '8. US House Results by State', '9. 2022 Party Labels']
PARTIES = ('DEM', 'REP', 'OTHER')
NONVOTING = {'AS', 'DC', 'GU', 'MP', 'VI'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract():
    import openpyxl
    book = openpyxl.load_workbook(AUDIT / 'fec2022.xlsx', read_only=True, data_only=True)
    values = {s: list(book[s].values) for s in SHEETS}
    book.close()
    target = AUDIT / 'fec_workbook_values.json'
    target.write_text(json.dumps(values, indent=1, default=str) + '\n')
    (AUDIT / 'extraction.json').write_text(json.dumps({
        'input': 'fec2022.xlsx', 'input_sha256': sha(AUDIT / 'fec2022.xlsx'),
        'output': target.name, 'output_sha256': sha(target),
        'method': 'openpyxl read_only=True, data_only=True; full sheet rows in source order',
        'openpyxl_version': openpyxl.__version__, 'sheets': SHEETS,
        'source_row_number': '1-based position in the worksheet; blank rows retained',
    }, indent=2) + '\n')


def major_party(label):
    # Primary/general transition labels: only the general-party part establishes D/R.
    label = label.strip().replace('*', '')
    if label in {'D', 'DFL', 'D/WF', 'D/IP/WF', 'W(D)/D'}:
        return 'DEM'
    if label == 'R':
        return 'REP'
    return 'OTHER'


def audit():
    for p in json.loads((AUDIT / 'provenance.json').read_text()):
        assert sha(AUDIT / p['file']) == p['sha256'], p['file']
    meta = json.loads((AUDIT / 'extraction.json').read_text())
    assert sha(AUDIT / meta['input']) == meta['input_sha256']
    assert sha(AUDIT / meta['output']) == meta['output_sha256']
    source = json.loads((AUDIT / meta['output']).read_text())
    rows = source['8. US House Results by State']
    lines = []
    for number, row in enumerate(rows[1:], 2):
        if not (row[8] and row[10] and row[15] is not None):
            continue
        numeric = isinstance(row[15], (int, float))
        assert numeric or row[15] == 'Unopposed', (number, row[15])
        if numeric:
            assert row[15] >= 0 and int(row[15]) == row[15]
        state, district = row[1], str(row[3]).strip().zfill(2)
        disposition = ('nonvoting_delegation' if state in NONVOTING else
                       'extra_unexpired_term' if 'Unexpired' in district else
                       'included_numeric' if numeric else 'included_missing_unopposed_count')
        lines.append(dict(source_row=number, state=state, district=district,
                          candidate=row[8].strip(), fec_id=str(row[4] or '').strip(),
                          source_party=row[10].strip(), ballot_party=major_party(row[10]),
                          votes=int(row[15]) if numeric else None,
                          combined_control=row[19], disposition=disposition))
    # Reproduce all 55 FEC state/delegation party summaries BEFORE adjusting scope/fusion.
    state_totals = defaultdict(Counter)
    contest_totals = Counter()
    for r in lines:
        state_totals[r['state']][r['ballot_party']] += r['votes'] or 0
        contest_totals[(r['state'], r['district'])] += r['votes'] or 0
    state_checks = []
    for row in source['6. Table 5 House by Party']:
        if row[0] not in state_totals:
            continue
        for party, expected in zip(PARTIES, row[4:7]):
            expected = expected if isinstance(expected, (int, float)) else 0
            observed = state_totals[row[0]][party]
            assert observed == expected, (row[0], party, observed, expected)
            state_checks.append(dict(state=row[0], party=party, reconstructed=observed,
                                     fec_table5=expected, difference=observed-expected))
    assert len(state_checks) == 55 * 3
    district_checks = []
    for row in rows:
        if row[9] == 'District Votes:' and isinstance(row[15], (int, float)):
            key = (row[1], str(row[3]).strip().zfill(2))
            assert contest_totals[key] == row[15], (key, contest_totals[key], row[15])
            district_checks.append(dict(state=key[0], district=key[1],
                                        reconstructed=contest_totals[key], fec_total=row[15]))
    # Candidate names scoped to contest: FEC IDs are NOT guaranteed unique/correct.
    groups, ids = defaultdict(list), defaultdict(set)
    for r in lines:
        name = re.sub(r'\s+', ' ', r['candidate']).rstrip(' #').casefold()
        groups[(r['state'], r['district'], name)].append(r)
        if r['fec_id'].startswith('H'):
            ids[(r['state'], r['district'], r['fec_id'])].add(name)
    fusion_checks = []
    for key, group in groups.items():
        majors = {r['ballot_party'] for r in group} - {'OTHER'}
        assert len(majors) <= 1, (key, majors)
        assert len({r['source_party'] for r in group}) == len(group), key
        controls = {int(r['combined_control']) for r in group
                    if isinstance(r['combined_control'], (int, float))}
        if controls:
            total = sum(r['votes'] or 0 for r in group)
            assert controls == {total}, (key, total, controls)
            fusion_checks.append(dict(state=key[0], district=key[1], candidate=key[2],
                                      reconstructed=total, fec_combined=next(iter(controls))))
        for r in group:
            r['candidate_party'] = next(iter(majors)) if majors else 'OTHER'
    selected = [r for r in lines if r['disposition'].startswith('included')]
    assert len({r['state'] for r in selected}) == 50
    assert len({(r['state'], r['district']) for r in selected}) == 435
    missing = [r for r in selected if r['votes'] is None]
    assert {(r['state'], r['district']) for r in missing} == {('FL', '05'), ('LA', '04')}
    def totals(rs, field):
        return {p: sum(r['votes'] or 0 for r in rs if r[field] == p) for p in PARTIES}
    def stats(label, counts):
        total = sum(counts.values())
        return dict(reference=label, **counts, total_votes=total,
                    dem_share_pp=100*counts['DEM']/total, rep_share_pp=100*counts['REP']/total,
                    margin_pp=100*(counts['DEM']-counts['REP'])/total,
                    two_party_margin_pp=100*(counts['DEM']-counts['REP'])/(counts['DEM']+counts['REP']))
    fifty = [r for r in lines if r['state'] not in NONVOTING]
    stages = [stats('FEC scope: includes delegations and IN special', totals(lines, 'ballot_party')),
              stats('50 states, includes IN special', totals(fifty, 'ballot_party')),
              stats('Regular contests, ballot-party lines', totals(selected, 'ballot_party')),
              stats('Regular contests, candidate affiliation (audit reference)', totals(selected, 'candidate_party'))]
    collisions = [dict(state=k[0], district=k[1], fec_id=k[2], names=' | '.join(sorted(v)))
                  for k, v in ids.items() if len(v) > 1]
    return dict(lines=lines, state_checks=state_checks, district_checks=district_checks,
                fusion_checks=fusion_checks, id_collisions=collisions, missing=missing, stages=stages,
                benchmark=stages[-1])


if __name__ == '__main__':
    import sys
    if '--extract' in sys.argv:
        extract()
    result = audit()
    print(json.dumps({k: result[k] for k in ('benchmark', 'id_collisions')}, indent=2))
    print('Checks:', {k: len(result[k]) for k in ('lines', 'state_checks', 'district_checks', 'fusion_checks')})
