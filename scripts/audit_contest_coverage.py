"""Offline contest census; coverage assignments never repair training labels.

An observation has one ledger row. Ambiguous same-day contests remain unallocated.
Raw-source counts include superseded versions and are not independent poll counts.
"""
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
import csv
import json

from data_utils import LAB, latest, digest

FACTS = LAB / 'reports/source_audit/contest_census/schedule_facts.json'
CYCLES = (2016, 2017, 2018, 2020, 2022, 2024, 2026)


def read(path):
    with Path(path).open(newline='') as f:
        return list(csv.DictReader(f))


def expected_contests(facts):
    classes = facts['classes']
    assert [len(classes[str(i)]) for i in (1, 2, 3)] == [33, 33, 34]
    counts = Counter(s for states in classes.values() for s in states)
    assert len(counts) == 50 and set(counts.values()) == {2}
    rows = []
    for year, cl in [(2016, 3), (2018, 1), (2020, 2), (2022, 3), (2024, 1), (2026, 2)]:
        start = date(year, 11, 2)
        election = start + timedelta(days=(1-start.weekday()) % 7)
        for state in classes[str(cl)]:
            runoff = next((r for r in facts['regular_runoffs'] if (r['cycle'], r['state']) == (year, state)), None)
            rows.append(dict(cycle=year, state=state, seat_class=cl, special=False,
                initial_date=str(election), runoff_date=runoff['date'] if runoff else '',
                evidence=f'class_{cl}' + ('|' + runoff['source'] if runoff else '')))
    rows.extend(dict(**{k: r[k] for k in ('cycle', 'state', 'seat_class', 'initial_date', 'runoff_date')},
                     special=True, evidence=r['source']) for r in facts['specials'])
    for r in rows:
        r['contest_id'] = f"{r['cycle']}-{r['state']}-class{r['seat_class']}-{'special' if r['special'] else 'regular'}"
        r['physical_seat'] = f"{r['state']}-class{r['seat_class']}"
        r['evidence_urls'] = '|'.join(facts['sources'][s]['url'] for s in r['evidence'].split('|'))
    assert len(rows) == len({r['contest_id'] for r in rows}) == 211
    assert sorted(r['state'] for r in rows if r['cycle'] == 2026) == facts['calendar2026_states']
    return sorted(rows, key=lambda r: (r['cycle'], r['state'], r['special']))


def assign_poll(row, expected, outcome_contests):
    """Coverage identity only; preserve any failed candidate/label join separately."""
    possible = [c for c in expected if c['cycle'] == int(row['cycle']) and c['state'] == row['geography']
                and row['election_date'] in (c['initial_date'], c['runoff_date']) and row['election_date']]
    cl = {'Class I': 1, 'Class II': 2, 'Class III': 3}.get(row['source_seat_name'])
    if cl:
        possible = [c for c in possible if c['seat_class'] == cl]
    joined = outcome_contests.get(row['outcome_id'])
    if joined:
        possible = [c for c in possible if c['contest_id'] == joined]
    ids = [c['contest_id'] for c in possible]
    status = 'assigned' if len(ids) == 1 else 'ambiguous_parallel_contests' if ids else 'date_or_identity_unresolved'
    return (ids[0] if len(ids) == 1 else ''), '|'.join(ids), status


def build(paths=None, weight_cases=None, weight_eligibility=None):
    paths = paths or {k: latest(LAB/'data'/k)[0] for k in ('historical', 'prepared', 'normalized', '2026')}
    facts = json.loads(FACTS.read_text())
    expected = expected_contests(facts)
    obs = read(paths['normalized']/'tables/poll_observations.csv')
    outcomes = read(paths['normalized']/'tables/election_outcomes.csv')
    prepared = read(paths['prepared']/'tables/historical_contests.csv')
    features = read(paths['normalized']/'tables/state_features.csv')
    current = read(paths['normalized']/'tables/current_contests.csv')
    weight_cases = weight_cases if weight_cases is not None else read(LAB/'reports/data_review/cross_cycle_weighting_cases.csv')
    weight_eligibility = weight_eligibility if weight_eligibility is not None else read(LAB/'reports/data_review/cross_cycle_weighting_eligibility.csv')
    wc = {(int(r['cycle']), r['area']): r for r in weight_cases if r['family'] == 'senate'}
    we = {r['observation_id']: r['reason'] for r in weight_eligibility if r['area'] != 'US'}
    ob = {r['outcome_id']: r for r in outcomes}
    outcome_contests, result_ledger = {}, []
    for r in prepared:
        if int(r['cycle']) not in CYCLES: continue
        cs = [c for c in expected if (c['cycle'], c['state'], c['special']) == (int(r['cycle']), r['state'], r['special'] == 'true')]
        cid = cs[0]['contest_id'] if len(cs) == 1 else ''
        if cid: outcome_contests[r['contest_id']] = cid
        # MIT "gen" is not a reliable election-stage label in this special case.
        ambiguous_stage = r['contest_id'] == '2018-MS-special-gen'
        stage = '' if ambiguous_stage else 'runoff' if 'runoff' in r['stage'] else 'initial' if r['stage'] == 'gen' else ''
        result_ledger.append(dict(outcome_id=r['contest_id'], contest_id=cid, cycle=int(r['cycle']), state=r['state'],
            source_stage=r['stage'], coverage_stage=stage, result_year=r['result_year'],
            mapping_status='stage_definition_review' if ambiguous_stage else 'assigned' if cid and stage else 'unresolved',
            status=ob[r['contest_id']]['status'], review_reasons=r['review_reasons'],
            baseline_eligible=r['baseline_eligible'], total_votes=r['total_votes']))
    polls = [r for r in obs if r['dataset'] == 'senate' and 2016 <= int(r['cycle']) <= 2026]
    assert all(int(r['cycle']) in CYCLES for r in polls), 'Unexpected odd-year cycle: extend the census'
    poll_ledger = []
    byid = {c['contest_id']: c for c in expected}
    for r in polls:
        cid, candidates, mapping = assign_poll(r, expected, outcome_contests)
        c = byid.get(cid)
        case = wc.get((int(r['cycle']), r['geography']))
        reason = ('superseded_source_version' if r['selection_status'] == 'superseded_by_full_archive' else
                  'coverage_' + mapping if not cid else
                  r['selection_status'] if int(r['cycle']) == 2026 else
                  we[r['observation_id']] if case and case['outcome_id'] in outcome_contests and
                    outcome_contests[case['outcome_id']] == cid else
                  'missing_result' if not any(x['contest_id'] == cid for x in result_ledger) else
                  'result_or_election_rule_restricted')
        poll_ledger.append(dict(observation_id=r['observation_id'], cycle=int(r['cycle']), state=r['geography'],
            contest_id=cid, candidate_contest_ids=candidates, coverage_mapping=mapping,
            stage=('runoff' if r['election_date'] == c['runoff_date'] else 'initial') if c else '',
            source=r['source'], source_file=r['source_file'], source_rows=r['source_rows'],
            sample_group_id=r['sample_group_id'], source_poll_id=r['source_poll_id'], source_question_id=r['source_question_id'],
            election_date=r['election_date'], days_to_election=r['days_to_election'],
            source_seat_name=r['source_seat_name'], outcome_id=r['outcome_id'],
            matchup_status=r['matchup_status'], selection_status=r['selection_status'],
            quality_flags=r['quality_flags'], diagnostic_disposition=reason))
    assert len({r['observation_id'] for r in poll_ledger}) == len(polls)
    # Reconcile every archived question / legacy row with normalized coverage universe.
    source_counts = []
    for source, file in [('538', 'senate_polls.csv'), ('538_archive', '538_archive_senate.csv')]:
        raw = read(paths['historical']/'tables'/file)
        for cycle in CYCLES:
            rr = [r for r in raw if int(r['cycle']) == cycle]
            raw_ids = {(r['poll_id'], r['question_id'], r['race_id']) for r in rr}
            nn = [r for r in polls if r['source'] == source and int(r['cycle']) == cycle]
            expected_n = len(raw_ids) if source == '538_archive' else len(rr)
            assert expected_n == len(nn), (source, cycle, expected_n, len(nn))
            source_counts.append(dict(source=source, cycle=cycle, raw_candidate_or_pair_rows=len(rr),
                expected_normalized_questions=expected_n, normalized_questions=len(nn)))
    qq = read(paths['prepared']/'tables/current_questions.csv')
    assert len(qq) == sum(r['source'] == 'nyt' for r in polls)
    source_counts.append(dict(source='nyt', cycle=2026, raw_candidate_or_pair_rows='',
        expected_normalized_questions=len(qq), normalized_questions=sum(r['source'] == 'nyt' for r in polls)))
    stages, contests = [], []
    for c in expected:
        cid = c['contest_id']; rs = [r for r in result_ledger if r['contest_id'] == cid]
        ps = [r for r in poll_ledger if r['contest_id'] == cid]
        active = [r for r in ps if r['diagnostic_disposition'] != 'superseded_source_version']
        ambiguous = [r for r in poll_ledger if not r['contest_id'] and cid in r['candidate_contest_ids'].split('|')]
        st = []
        for stage, dt in [('initial', c['initial_date']), ('runoff', c['runoff_date'])]:
            if not dt: continue
            sr = [r for r in rs if r['coverage_stage'] == stage]
            status = ('not_due' if c['cycle'] == 2026 else 'stage_definition_review' if any(r['mapping_status'] == 'stage_definition_review' for r in rs)
                      else 'present' if sr else 'missing_result_stage')
            st.append(dict(contest_id=cid, cycle=c['cycle'], state=c['state'], stage=stage, election_date=dt,
                result_status=status, outcome_ids='|'.join(r['outcome_id'] for r in sr),
                raw_assigned_questions=sum(r['stage'] == stage for r in ps),
                active_assigned_questions=sum(r['stage'] == stage for r in active)))
        stages.extend(st)
        selected = sum(r['diagnostic_disposition'] == 'selected' for r in ps)
        case = wc.get((c['cycle'], c['state'])) if not c['special'] else None
        baseline = bool(case and outcome_contests.get(case['outcome_id']) == cid)
        if baseline: assert selected == int(case['polls']), cid
        # Exclusive summary status; separate axes below retain overlapping limitations.
        coverage = ('selected_window' if selected else 'ambiguous_poll_assignment' if ambiguous and not active else
            'no_raw_poll_in_sources' if not ps and not ambiguous else 'no_active_poll_version' if not active else
            'current_matchup_rejected' if c['cycle'] == 2026 and not any(r['matchup_status'] == 'accepted' for r in active) else
            'current_no_selected_recent_poll' if c['cycle'] == 2026 else
            'missing_result' if not rs else 'result_or_rule_restricted' if not baseline else
            'outside_window_only' if any(r['diagnostic_disposition'] == 'outside_window' for r in active) else 'all_poll_versions_rejected')
        contests.append(dict(**c, expected_stages=len(st), present_result_rows=len(rs),
            missing_result_stages=sum(r['result_status'] == 'missing_result_stage' for r in st),
            stage_definition_review=any(r['result_status'] == 'stage_definition_review' for r in st),
            outcome_statuses='|'.join(sorted({r['status'] for r in rs})),
            outcome_review_reasons='|'.join(sorted({v for r in rs for v in r['review_reasons'].split('|') if v})),
            raw_assigned_questions=len(ps), active_assigned_questions=len(active),
            active_sample_groups=len({r['sample_group_id'] for r in active}),
            ambiguous_questions_unallocated=len(ambiguous), baseline_eligible=baseline,
            selected_window_polls=selected, coverage_status=coverage))
    assert len([c for c in contests if c['cycle'] == 2026]) == len(current)
    expected_now = {(c['state'], c['seat_class'], c['special'], c['initial_date']) for c in contests if c['cycle'] == 2026}
    assert expected_now == {(r['state'], int(r['seat_class']), r['special'].lower() == 'true', r['election_date']) for r in current}
    feature_keys = {(int(r['cycle']), r['state']) for r in features}
    assert len(feature_keys) == len(features)
    states = sorted({c['state'] for c in expected})
    grid = []
    for year in range(2016, 2027):
        for state in states:
            starts = [c for c in contests if c['cycle'] == year and c['state'] == state]
            held = [s for s in stages if s['election_date'].startswith(str(year)) and s['state'] == state]
            grid.append(dict(calendar_year=year, state=state, new_contests=len(starts), voting_stages=len(held),
                calendar_status='election_scheduled_or_held' if held else 'no_senate_general_election',
                cycle_feature_present=(year, state) in feature_keys,
                feature_status='present' if (year, state) in feature_keys else 'odd_year_features_not_built' if year%2 else 'missing_even_cycle_features'))
    assert all((y, s) in feature_keys for y in CYCLES if y%2 == 0 for s in states)
    cycles = []
    for year in CYCLES:
        cc = [c for c in contests if c['cycle'] == year]
        pp = [r for r in poll_ledger if r['cycle'] == year]
        cycles.append(dict(cycle=year, expected_contests=len(cc), regular=sum(not c['special'] for c in cc),
            special=sum(c['special'] for c in cc), expected_stages=sum(c['expected_stages'] for c in cc),
            result_rows=sum(c['present_result_rows'] for c in cc), missing_stages=sum(c['missing_result_stages'] for c in cc),
            stage_review_contests=sum(c['stage_definition_review'] for c in cc),
            raw_questions=len(pp), assigned_questions=sum(bool(r['contest_id']) for r in pp),
            unallocated_questions=sum(not r['contest_id'] for r in pp),
            no_raw_poll_contests=sum(c['coverage_status'] == 'no_raw_poll_in_sources' for c in cc),
            baseline_eligible=sum(c['baseline_eligible'] for c in cc),
            selected_window_contests=sum(c['selected_window_polls'] > 0 for c in cc),
            selected_window_polls=sum(c['selected_window_polls'] for c in cc)))
    reasons = Counter((r['cycle'], r['state'], r['contest_id'], r['diagnostic_disposition']) for r in poll_ledger)
    reason_rows = [dict(cycle=k[0], state=k[1], contest_id=k[2], reason=k[3], questions=n) for k, n in sorted(reasons.items())]
    result_reasons = Counter((r['cycle'], r['state'], reason) for r in result_ledger
                            for reason in filter(None, r['review_reasons'].split('|')))
    result_reason_rows = [dict(cycle=k[0], state=k[1], reason=k[2], outcome_rows=n)
                          for k, n in sorted(result_reasons.items())]
    national = []
    for year in CYCLES:
        if year % 2: continue
        pp = [r for r in obs if r['dataset'] == 'generic_ballot' and int(r['cycle']) == year]
        oo = [r for r in outcomes if r['outcome_type'] == 'national_house_popular_vote' and int(r['cycle']) == year]
        national.append(dict(cycle=year, raw_questions=len(pp), active_questions=sum(r['selection_status'] != 'superseded_by_full_archive' for r in pp),
            normalized_outcome_status='|'.join(r['status'] for r in oo) or 'not_due',
            analysis_label_status='audited_2022_FEC' if year == 2022 else 'audited_2024_first_choice' if year == 2024 else 'provisional_source_label' if year < 2026 else 'not_due'))
    source_provenance = FACTS.parent/'provenance.json'
    saved_sources = []
    for entry in json.loads(source_provenance.read_text()):
        if 'sha256' in entry:
            source_file = FACTS.parent/entry['file']
            assert digest(source_file.read_bytes()) == entry['sha256']
            saved_sources.append(source_file)
    files = [FACTS, source_provenance, Path(__file__), LAB/'config/analysis_policy_v1.json',
             LAB/'reports/data_review/cross_cycle_weighting_cases.csv',
             LAB/'reports/data_review/cross_cycle_weighting_eligibility.csv'] + saved_sources + [p/'manifest.json' for p in paths.values()]
    provenance = dict(scope=facts['scope'], schedule_reviewed=facts['reviewed_date'],
        snapshots={k:p.name for k,p in paths.items()}, inputs={str(p.relative_to(LAB)):digest(p.read_bytes()) for p in files},
        note='Coverage-only mapping; no outcome or normalized source changes. Current selected counts use the saved refresh window, historical counts use policy-v1 days 1–15. Question counts are not independent samples.')
    return dict(contests=contests, stages=stages, polls=poll_ledger, results=result_ledger, calendar=grid,
                cycles=cycles, reasons=reason_rows, result_reasons=result_reason_rows,
                source_reconciliation=source_counts, national=national, provenance=provenance)


def write_report(result, out=None):
    out = Path(out or LAB/'reports/data_review'); out.mkdir(parents=True, exist_ok=True)
    for name, rows in result.items():
        if name == 'provenance':
            (out/'contest_census_provenance.json').write_text(json.dumps(rows, indent=2)+'\n')
        else:
            with (out/f'contest_census_{name}.csv').open('w', newline='') as f:
                w=csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


if __name__ == '__main__':
    result = build(); write_report(result)
    print(json.dumps(result['cycles'], indent=2))
