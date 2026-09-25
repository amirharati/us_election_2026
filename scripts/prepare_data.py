"""Offline, versioned preparation. No fitting, imputation, or forecast generation."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import date, datetime, timedelta
import json
import math
from pathlib import Path
import re
import unicodedata

from data_utils import LAB, Snapshot, csv_bytes, digest, latest


def read(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def number(value):
    try:
        n = float(value)
        return n if math.isfinite(n) else None
    except (TypeError, ValueError):
        return None


def day(value):
    for fmt in ("%Y-%m-%d", "%m/%d/%y", "%m/%d/%y %H:%M", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Unrecognized date: {value!r}")


def normalized(name):
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return " ".join(re.findall(r"[a-z0-9]+", name.lower()))


def surname(name):
    tokens = normalized(name.split(",")[0]).split()
    while tokens and tokens[-1] in {"jr", "sr", "ii", "iii", "iv"}:
        tokens.pop()
    return tokens[-1] if tokens else ""


def nonvote(name):
    return normalized(name).replace(" ", "") in {"overvotes", "undervotes"}


def senate_results(rows):
    """Aggregate fusion lines by candidate, preserving every source row reference."""
    groups = defaultdict(list)
    for line, r in enumerate(rows, 2):
        key = (int(r["year"]), r["state_po"], r["special"].lower(), r["stage"].lower())
        groups[key].append((line, r))
    contests, candidates = [], []
    for (year, state, special, stage), entries in sorted(groups.items()):
        cid = f"{year}-{state}-{'special' if special == 'true' else 'regular'}-{stage.replace(' ', '_')}"
        source_entries = entries
        excluded = [(line, r) for line, r in entries if nonvote(r["candidate"])]
        entries = [(line, r) for line, r in entries if not nonvote(r["candidate"])]
        totals = {number(r["totalvotes"]) for _, r in source_entries}
        votes = [number(r["candidatevotes"]) for _, r in entries]
        valid = (len(totals) == 1 and None not in totals and next(iter(totals)) > 1
                 and all(v is not None and v >= 0 for v in votes))
        total = next(iter(totals)) if len(totals) == 1 else None
        source_total = total
        nonvotes = [number(r["candidatevotes"]) for _, r in excluded]
        if (valid and excluded and None not in nonvotes
                and abs(sum(votes)+sum(nonvotes)-total) < abs(sum(votes)-total)
                and abs(sum(votes)+sum(nonvotes)-total) <= max(5, total*.001)):
            total -= sum(nonvotes)
        if valid:
            valid = abs(sum(votes) - total) <= max(5, total * .001)
        grouped = defaultdict(list)
        for line, r in entries:
            # Empty aggregate vote categories must not merge with named candidates.
            key = normalized(r["candidate"]) or f"unnamed-{line}"
            grouped[key].append((line, r))
        local = []
        for _, items in sorted(grouped.items()):
            parties = {r["party_simplified"].upper() for _, r in items}
            major = parties & {"DEMOCRAT", "REPUBLICAN"}
            party = next(iter(major)) if len(major) == 1 else "OTHER"
            nv = [number(r["candidatevotes"]) for _, r in items]
            n = sum(nv) if None not in nv else None
            cr = {"contest_id": cid, "candidate": items[0][1]["candidate"], "party": party,
                  "votes": n, "pct": 100*n/total if valid and n is not None else None,
                  "source_rows": "|".join(str(i) for i, _ in items), "fusion_lines": len(items)}
            local.append(cr)
            candidates.append(cr)
        major = {p: [r for r in local if r["party"] == p] for p in ("DEMOCRAT", "REPUBLICAN")}
        reasons = []
        if not valid:
            reasons.append("invalid_or_placeholder_vote_totals")
        if any(r["unofficial"].lower() == "true" for _, r in entries):
            reasons.append("unofficial_source_result")
        if any(len(v) != 1 for v in major.values()):
            reasons.append("not_unique_dem_rep_pair")
        margin = (major["DEMOCRAT"][0]["pct"] - major["REPUBLICAN"][0]["pct"]
                  if valid and all(len(v) == 1 for v in major.values()) else None)
        # Conservative first baseline; special/alternative-rule observations stay visible.
        if special == "true" or stage != "gen" or year % 2 or state in {"LA", "AK", "ME", "GA"}:
            reasons.append("election_rule_or_special_review")
        contests.append({"contest_id": cid, "result_year": year,
                         "cycle": 2020 if year == 2021 and state == "GA" else year,
                         "state": state, "special": special, "stage": stage,
                         "source_totalvotes": source_total, "total_votes": total, "dem_rep_margin": margin,
                         "excluded_nonvote_source_rows": "|".join(str(line) for line, _ in excluded),
                         "baseline_eligible": not reasons, "review_reasons": "|".join(reasons)})
    return contests, candidates


def join_historical(polls, contests, candidates):
    by_contest = defaultdict(list)
    lookup = defaultdict(list)
    for r in candidates:
        by_contest[r["contest_id"]].append(r)
    for r in contests:
        lookup[(r["result_year"], r["state"])].append(r)
    out = []
    seen = set()
    for line, p in enumerate(polls, 2):
        record = {"source_row": line, "poll_id": p["poll_id"], "question_id": p["question_id"],
                  "race_id": p["race_id"], "cycle": int(p["cycle"]), "state": p["location"],
                  "pollster": p["pollster"], "poll_date": p["polldate"],
                  "election_date": p["electiondate"], "sample_size": number(p["samplesize"]),
                  "days_to_election": (day(p["electiondate"]) - day(p["polldate"])).days,
                  "contest_id": "", "dem_rep_margin": None, "result_margin": None,
                  "status": "", "baseline_eligible": False}
        key = tuple(sorted(p.items()))
        if key in seen:
            record["status"] = "exact_duplicate"
        elif {p["cand1_party"], p["cand2_party"]} != {"DEM", "REP"}:
            record["status"] = "non_dem_rep_pair_retained_in_source"
        else:
            sign = 1 if p["cand1_party"] == "DEM" else -1
            shares = [number(p[f"cand{i}_pct"]) for i in (1, 2)]
            if any(x is None or not 0 <= x <= 100 for x in shares) or sum(shares) > 101:
                record["status"] = "invalid_poll_shares"
            else:
                record["dem_rep_margin"] = sign * (shares[0] - shares[1])
                matches = []
                options = lookup[(day(p["electiondate"]).year, p["location"])]
                for c in options:
                    cs = by_contest[c["contest_id"]]
                    # Name AND published result share must agree; never match using poll error.
                    ok = True
                    for i in (1, 2):
                        party = "DEMOCRAT" if p[f"cand{i}_party"] == "DEM" else "REPUBLICAN"
                        actual = number(p[f"cand{i}_actual"])
                        hits = [r for r in cs if r["party"] == party
                                and surname(r["candidate"]) == surname(p[f"cand{i}_name"])
                                and actual is not None and r["pct"] is not None
                                and abs(actual-r["pct"]) <= .25]
                        ok = ok and len(hits) == 1
                    if ok:
                        matches.append(c)
                if len(matches) == 1:
                    c = matches[0]
                    record.update(contest_id=c["contest_id"], result_margin=c["dem_rep_margin"],
                                  status="matched", baseline_eligible=c["baseline_eligible"])
                else:
                    record["status"] = ("missing_result_year_state" if not options else
                                        "ambiguous_result_join" if len(matches) > 1 else "candidate_or_result_share_mismatch")
        if record["sample_size"] is None or record["sample_size"] <= 0 or record["days_to_election"] < 0:
            record.update(status="invalid_sample_or_date", baseline_eligible=False)
        seen.add(key)
        out.append(record)
    return out


def presidential_features(rows, audit=None):
    groups = defaultdict(list)
    for r in rows:
        groups[(int(r["year"]), r["state_po"])].append(r)
    states, national = {}, defaultdict(lambda: [0., 0.])
    for key, rs in groups.items():
        excluded = [r for r in rs if nonvote(r["candidate"])]
        rs = [r for r in rs if r not in excluded]
        totals = {number(r["totalvotes"]) for r in rs}
        votes = [number(r["candidatevotes"]) for r in rs]
        if len(totals) != 1 or None in totals or None in votes or min(votes) < 0:
            raise ValueError(f"Invalid presidential totals: {key}")
        total = next(iter(totals))
        source_total = total
        excluded_votes = sum(number(r["candidatevotes"]) for r in excluded)
        if (excluded and abs(sum(votes)+excluded_votes-total) < abs(sum(votes)-total)
                and abs(sum(votes) + excluded_votes - total) <= max(5, total*.001)):
            total -= excluded_votes
        if total <= 0 or abs(sum(votes)-total) > max(5, total*.001):
            raise ValueError(f"Presidential votes do not reconcile: {key}")
        # Assign fusion-line votes to the candidate's major party, not line label.
        cs = defaultdict(list)
        for r in rs:
            cs[normalized(r['candidate'])].append(r)
        difference = 0.
        for crs in cs.values():
            parties = {r["party_simplified"].upper() for r in crs}
            major = parties & {"DEMOCRAT", "REPUBLICAN"}
            if len(major) > 1:
                raise ValueError(f"Conflicting presidential candidate parties: {key}")
            sign = 1 if "DEMOCRAT" in major else -1 if "REPUBLICAN" in major else 0
            difference += sign * sum(number(r["candidatevotes"]) for r in crs)
        states[key] = 100 * difference / total
        if audit is not None:
            audit.append({"year": key[0], "state": key[1], "valid_votes": total,
                          "source_totalvotes": source_total,
                          "sum_candidate_votes": sum(votes), "dem_rep_margin": states[key],
                          "excluded_nonvote_rows": len(excluded),
                          "excluded_nonvotes": excluded_votes})
        national[key[0]][0] += difference
        national[key[0]][1] += total
    national = {y: 100*d/t for y, (d, t) in national.items()}
    for year in national:
        if len({state for y, state in states if y == year}) != 51:
            raise ValueError(f"National presidential denominator requires 50 states + DC: {year}")
    return states, national


def lag_features(cycle, state, states, national):
    year = max(y for y in national if y < cycle)
    margin = states[(year, state)]
    president = {1998: "DEM", 2000: "DEM", 2002: "REP", 2004: "REP", 2006: "REP", 2008: "REP",
                 2010: "DEM", 2012: "DEM", 2013: "DEM", 2014: "DEM", 2016: "DEM", 2017: "REP",
                 2018: "REP", 2020: "REP", 2022: "DEM", 2024: "DEM", 2026: "REP"}
    return {"prior_presidential_year": year, "prior_state_pres_margin": margin,
            "prior_national_pres_margin": national[year],
            "prior_state_lean": margin - national[year],
            "presidential_year": cycle % 4 == 0,
            "president_party": president[cycle],
            "split": "train" if cycle <= 2016 else "validation" if cycle == 2018 else
                     "test" if cycle in {2020, 2022} else "forecast" if cycle == 2026 else "unused"}


def forecast_side_shares(answers):
    """Current-election proxy: strongest D/IND candidate minus strongest REP.

    Keep actual affiliations on answer rows. Never add competing candidates' votes.
    Multiple opponents require a candidate-level model for exact win probabilities.
    """
    left = [number(a["pct"]) for a in answers if a["reviewed_party"] in {"DEM", "IND"}]
    right = [number(a["pct"]) for a in answers if a["reviewed_party"] == "REP"]
    return (max(left) if left and None not in left else None,
            max(right) if right and None not in right else None)


def current_questions(rows, review, asof):
    from current_poll_review import canonical_candidate
    groups = defaultdict(list)
    for line, r in enumerate(rows, 2):
        groups[(r["poll_id"], r["question_id"], r["race_id"], r["ranked_choice_round"])].append((line, r))
    questions, answers = [], []
    for key, entries in sorted(groups.items()):
        r = entries[0][1]
        state = r["state"]
        spec = review["contests"][state]
        expected = {c["candidate_id"]: c for c in spec["candidates"] if c["candidate_id"]}
        qid = "|".join(key)
        qr = review.get("question_reviews", {}).get(key[1], {})
        pr = review.get("poll_reviews", {}).get(key[0], {})
        reasons, flags = [], []
        if pr.get('date_basis') and pr['date_basis'] != 'field_end':
            flags.append(pr['date_basis'])
        if qr and (qr['poll_id'] != key[0] or qr['state'] != state):
            raise ValueError('Stale question review: '+qid)
        if qr.get('basis') in {'informed', 'conditional', 'ambiguous'}:
            reasons.append('reviewed_'+qr['basis']+'_question')
        if not spec["candidates"]:
            reasons.append("pending_matchup_review")
        unique, seen = [], set()
        for line, a in entries:
            fingerprint = tuple(sorted(a.items()))
            duplicate = fingerprint in seen
            seen.add(fingerprint)
            candidate = canonical_candidate(a, spec)
            correct_party = candidate['party'] if candidate else a['party']
            canonical_id = candidate['candidate_id'] if candidate else a['candidate_id']
            if canonical_id != a['candidate_id']: flags.append('reviewed_candidate_alias')
            answers.append({"question_key": qid, "source_row": line, "candidate_id": a["candidate_id"],
                            "candidate_name": a["candidate_name"], "source_party": a["party"],
                            "canonical_candidate_id": canonical_id, "canonical_candidate_name": candidate["name"] if candidate else a["candidate_name"], "reviewed_party": correct_party, "pct": a["pct"],
                            "exact_duplicate": duplicate, "party_override": correct_party != a["party"]})
            if not duplicate:
                unique.append(dict(a, canonical_candidate_id=canonical_id, reviewed_party=correct_party))
        ids = [a["canonical_candidate_id"] for a in unique]
        if len(ids) != len(set(ids)):
            reasons.append("conflicting_candidate_answers")
        # Require the reviewed Republican and at least one reviewed D/IND opponent.
        # Additional independents do not invalidate an otherwise usable matchup.
        republicans = {k for k, c in expected.items() if c["party"] == "REP"}
        opponents = {k for k, c in expected.items() if c["party"] in {"DEM", "IND"}}
        if (len(expected) != len(spec["candidates"]) or not republicans
                or not republicans <= set(ids) or not opponents.intersection(ids)):
            reasons.append("missing_reviewed_contender")
        required = set(spec.get('required_ballot_candidate_ids', republicans | opponents))
        if required - set(ids):
            reasons.append('conditional_missing_ballot_contender')
        elif set(expected) - set(ids):
            flags.append('partial_ballot_coverage')
        if any(a["reviewed_party"] in {"DEM", "REP"} and a["canonical_candidate_id"] not in expected for a in unique):
            reasons.append("unreviewed_or_former_contender")
        shares = [number(a["pct"]) for a in unique]
        if any(v is None or not 0 <= v <= 100 for v in shares) or sum(v or 0 for v in shares) > 102:
            reasons.append("invalid_response_percentages")
        metadata = ("state", "start_date", "end_date", "sample_size", "population", "subpopulation", "election_date", "stage")
        if any(len({a[k] for a in unique}) != 1 for k in metadata):
            reasons.append("inconsistent_question_metadata")
        start, end, created = day(r["start_date"]), day(r["end_date"]), day(r["created_at"])
        if start > end or end > day(r["election_date"]):
            reasons.append("invalid_field_dates")
        if max(end, created) > asof:
            reasons.append("not_available_at_cutoff")
        if r["population"] not in {"lv", "rv", "a"} or r["subpopulation"]:
            reasons.append("unsupported_population_or_subgroup")
        if r["stage"] != "general" or r["election_date"] != "2026-11-03":
            reasons.append("different_election_stage")
        if any(a.get("hypothetical", "").upper() in {"TRUE", "YES", "1"} for a in unique):
            reasons.append("explicitly_hypothetical_question")
        sample_size = number(r['sample_size'])
        if sample_size is None and pr.get('sample_size'):
            sample_size = pr['sample_size']; flags.append('reviewed_missing_sample_size')
        if sample_size is None or sample_size <= 0:
            reasons.append("invalid_sample_size")
        d, rep = forecast_side_shares(unique)
        if qr.get('expected_shares'):
            actual={a['candidate_id']:number(a['pct']) for a in unique}
            if any(actual.get(k)!=v for k,v in qr['expected_shares'].items()):
                raise ValueError('Source revised reviewed question; review again: '+qid)
        margin = d-rep if d is not None and rep is not None else None
        questions.append({"question_key": qid, "poll_id": key[0], "question_id": key[1],
                          "race_id": key[2], "state": state, "pollster_id": r["pollster_id"],
                          "pollster": r["pollster"], "start_date": str(start), "end_date": str(end),
                          "created_date": str(created), "population": r["population"],
                          "sample_size": sample_size, "partisan": r["partisan"],
                          "methodology": r["methodology"], "source_url": r["url"],
                          "ranked_choice_round": r["ranked_choice_round"],
                          "ranked_choice_final": r["ranked_choice_final"],
                          "dem_rep_margin": margin, "response_sum": sum(v or 0 for v in shares),
                          "answer_count": len(unique), "accepted_matchup": not reasons,
                          "reasons": "|".join(reasons), "review_flags": "|".join(sorted(set(flags))),
                          "question_basis": qr.get('basis','initial_unverified'),
                          "ballot_candidate_count": sum(a['reviewed_party'] not in {'NONE',''} for a in unique),
                          "data_source": 'reviewed_supplement' if r.get('source')=='reviewed_supplement' else 'nyt',
                          "date_basis": pr.get('date_basis','field_end'),
                          "election_rule": spec["rule"],
                          "scalar_seat_mapping_ready": spec["scalar_seat_mapping_ready"],
                          "selection": "excluded"})
    # Prefer fuller ballot versions within the same sample/population/RCV round.
    # Do not average a two-way hypothetical with a fuller actual-ballot question.
    families = defaultdict(list)
    for q in questions:
        if q['accepted_matchup']:
            families[(q['poll_id'],q['state'],q['population'],q['ranked_choice_round'])].append(q)
    for family in families.values():
        largest=max(q['ballot_candidate_count'] for q in family)
        for q in family:
            if q['ballot_candidate_count'] < largest:
                q['accepted_matchup']=False
                q['reasons']='alternative_reduced_ballot_same_sample'
    return questions, answers


def select_current(questions, asof, window):
    """One question per poll; then conservatively remove overlapping same-house surveys."""
    per_poll = defaultdict(list)
    for q in questions:
        if not q["accepted_matchup"]:
            continue
        if day(q["end_date"]) < asof - timedelta(days=window):
            q["selection"] = "outside_recency_window"
            continue
        per_poll[(q["poll_id"], q["state"])].append(q)
    choices = []
    for qs in per_poll.values():
        qs.sort(key=lambda q: ({"lv": 0, "rv": 1, "a": 2}[q["population"]],
                               0 if q["ranked_choice_final"] == "TRUE" else 1,
                               -q["answer_count"], -q["sample_size"], q["question_key"]))
        choices.append(qs[0])
        for q in qs[1:]:
            q["selection"] = "alternative_question_same_poll"
    kept = defaultdict(list)
    for q in sorted(choices, key=lambda q: (q["end_date"], q["start_date"], q["sample_size"], q["question_key"]), reverse=True):
        key = (q["pollster_id"] or q["pollster"], q["state"])
        overlap = any(q["start_date"] <= k["end_date"] and k["start_date"] <= q["end_date"] for k in kept[key])
        q["selection"] = "overlapping_same_pollster" if overlap else "selected"
        if not overlap:
            kept[key].append(q)


def historical_windows(polls, horizons, window):
    eligible = [p for p in polls if p["baseline_eligible"] and p["status"] == "matched"]
    groups = defaultdict(list)
    for p in eligible:
        groups[(p["contest_id"], p["election_date"])].append(p)
    out = []
    for (cid, election), ps in sorted(groups.items()):
        for horizon in horizons:
            cutoff = day(election) - timedelta(days=horizon)
            options = [p for p in ps if cutoff-timedelta(days=window) <= day(p["poll_date"]) <= cutoff]
            # Archive has poll median dates, not field intervals/publication dates.
            # Keep one most recent observation per house to limit repeat-survey dependence.
            chosen = {}
            for p in sorted(options, key=lambda p: (p["poll_date"], p["sample_size"], p["question_id"]), reverse=True):
                chosen.setdefault(p["pollster"], p)
            for p in chosen.values():
                out.append({"contest_id": cid, "cycle": p["cycle"], "horizon_days": horizon,
                            "cutoff": str(cutoff), "source_row": p["source_row"],
                            "poll_id": p["poll_id"], "question_id": p["question_id"],
                            "window_may_be_archive_truncated": horizon + window > 61,
                            "availability_quality": "median_field_date_proxy_not_publication_date"})
    return out


def backtest_cases(features, windows, horizons):
    """Include held-out and unpolled outcomes, not just races surviving a poll join."""
    counts = Counter((r["contest_id"], r["horizon_days"]) for r in windows)
    out = []
    for r in features:
        if not r["baseline_eligible"] or r["cycle"] > 2022:
            continue
        first = date(r["cycle"], 11, 1)
        election = first + timedelta(days=(0-first.weekday()) % 7 + 1)
        for horizon in horizons:
            n = counts[(r["contest_id"], horizon)]
            out.append({"contest_id": r["contest_id"], "cycle": r["cycle"], "state": r["state"],
                        "split": r["split"], "horizon_days": horizon,
                        "cutoff": str(election-timedelta(days=horizon)),
                        "selected_poll_count": n, "poll_information": "available" if n else "prior_only",
                        "target_dem_rep_margin": r["dem_rep_margin"]})
    return out


def write_table(bundle, name, rows, empty_fields=()):
    fields = list(rows[0]) if rows else list(empty_fields)
    if not fields:
        raise ValueError(f"Cannot infer empty table schema: {name}")
    bundle.add(f"tables/{name}.csv", csv_bytes(fields, rows), rows=len(rows))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    parser.add_argument("--window-days", type=int, default=14)
    parser.add_argument("--historical-dir", type=Path, default=LAB/"data/historical")
    parser.add_argument("--current-dir", type=Path, default=LAB/"data/2026")
    parser.add_argument("--output-dir", type=Path, default=LAB/"data/prepared")
    args = parser.parse_args()
    if args.window_days <= 0:
        parser.error("--window-days must be positive")
    h, c = latest(args.historical_dir), latest(args.current_dir)
    if not h or not c:
        parser.error("Run both downloaders first")
    review = json.loads((LAB/"config/candidate_review_2026.json").read_text())
    if args.as_of < day(review["review_date"]):
        parser.error("Current nominee review cannot be used before its review date")
    if args.as_of >= date(2026, 11, 3):
        parser.error("This preparation contract is for pre-election 2026 snapshots")
    contests, candidates = senate_results(read(h[0]/"tables/senate_results.csv"))
    hp = join_historical(read(h[0]/"tables/senate_polls.csv"), contests, candidates)
    pres_audit = []
    states, national = presidential_features(read(h[0]/"tables/presidential_results.csv"), pres_audit)
    state_panel = [{"cycle": year, "state": state, **lag_features(year, state, states, national)}
                   for year in range(1998, 2027, 2)
                   for state in sorted({s for _, s in states} - {"DC"})]
    historical_features = [{**r, **lag_features(r["cycle"], r["state"], states, national)}
                           for r in contests if 1998 <= r["cycle"] <= 2024]
    questions, answers = current_questions(read(c[0]/"tables/senate_general_answers.csv"), review, args.as_of)
    select_current(questions, args.as_of, args.window_days)
    selected = [q for q in questions if q["selection"] == "selected"]
    current_features = []
    for r in read(LAB/"config/contests_2026.csv"):
        qs = [q for q in selected if q["state"] == r["state"]]
        current_features.append({**r, **lag_features(2026, r["state"], states, national),
                                 "as_of": str(args.as_of), "selected_poll_count": len(qs),
                                 "poll_information": "available" if qs else "prior_only",
                                 "latest_selected_poll_end": max((q["end_date"] for q in qs), default=""),
                                 "matchup_review": review["contests"][r["state"]]["status"],
                                 "election_rule": review["contests"][r["state"]]["rule"]})
    windows = historical_windows(hp, [14, 30, 50], args.window_days)
    cases = backtest_cases(historical_features, windows, [14, 30, 50])
    summary = {"as_of": str(args.as_of), "historical_result_contests": len(contests),
               "historical_poll_status": dict(Counter(p["status"] for p in hp)),
               "historical_baseline_eligible_polls": sum(p["baseline_eligible"] for p in hp),
               "current_questions": len(questions), "current_matchup_accepted": sum(q["accepted_matchup"] for q in questions),
               "current_selection": dict(Counter(q["selection"] for q in questions)),
               "current_exclusion_reasons": dict(Counter(reason for q in questions for reason in q["reasons"].split("|") if reason)),
               "selected_states": len({q["state"] for q in selected}),
               "prior_only_states": [r["state"] for r in current_features if r["poll_information"] == "prior_only"],
               "party_override_answer_rows": sum(a["party_override"] for a in answers),
               "nominee_review_age_days": (args.as_of-day(review["review_date"])).days,
               "historical_window_observations": len(windows), "all_state_feature_rows": len(state_panel),
               "historical_backtest_cases": len(cases),
               "historical_prior_only_cases": sum(r["poll_information"] == "prior_only" for r in cases),
               "presidential_nonvote_rows_excluded": sum(r["excluded_nonvote_rows"] for r in pres_audit),
               "forecast_ready": False}
    with Snapshot(args.output_dir, "prepared") as bundle:
        for name, rs in [("historical_contests", contests), ("historical_candidates", candidates),
                         ("historical_poll_audit", hp), ("historical_features", historical_features),
                         ("all_state_features", state_panel), ("presidential_result_audit", pres_audit),
                         ("historical_window_observations", windows), ("current_questions", questions),
                         ("historical_backtest_cases", cases),
                         ("current_answers", answers), ("current_features", current_features)]:
            write_table(bundle, name, rs)
        for name in ["candidate_review_2026.json", "contests_2026.csv", "chamber_2026.json"]:
            bundle.add(f"config/{name}", (LAB/"config"/name).read_bytes())
        code = {p.name: digest(p.read_bytes()) for p in [Path(__file__), LAB/"scripts/data_utils.py"]}
        bundle.write_json("provenance.json", {"historical_snapshot": h[0].name, "current_snapshot": c[0].name,
                          "historical_manifest_sha256": digest((h[0]/"manifest.json").read_bytes()),
                          "current_manifest_sha256": digest((c[0]/"manifest.json").read_bytes()),
                          "script_sha256": code, "as_of": str(args.as_of), "window_days": args.window_days,
                          "historical_horizons": [14, 30, 50], "result_match_tolerance_pp": .25,
                          "split": {"train": "1998-2016", "validation": [2018], "test": [2020, 2022]},
                          "availability_warning": "Historical publication times unavailable; current created_at is source ingestion, not necessarily publication."})
        bundle.write_json("summary.json", summary)
        bundle.finish(summary)


if __name__ == "__main__":
    main()
