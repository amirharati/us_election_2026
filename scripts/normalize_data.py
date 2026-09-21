"""Normalize all downloaded Senate/generic polls; retain exclusions and older data.

Fractions throughout, ISO dates, separate poll observations and outcome labels.
This is a source normalization layer, not a poll weighting or model fitting step.
"""
from collections import Counter, defaultdict
import json
from pathlib import Path
import argparse

from data_utils import LAB, Snapshot, digest, latest
from prepare_data import day, number, read, write_table, surname


def share(value):
    value = number(value)
    return value / 100 if value is not None and 0 <= value <= 100 else None


def blank(value):
    return "" if value is None or str(value).strip().upper() in {"", "NA", "N/A"} else str(value).strip()


def empty_observation(source, dataset, line, poll_id, question_id):
    # IDs are local to the versioned bundle; source rows make every conversion auditable.
    return dict(observation_id=f"{source}:{dataset}:{line}", source=source, dataset=dataset,
                source_file="", source_rows=str(line), source_poll_id=poll_id,
                source_question_id=question_id, source_race_id="",
                sample_group_id=f"{source}:{poll_id}", cycle=None, geography="",
                geography_type="", election_date="", poll_start="", poll_end="", poll_date="",
                date_basis="", source_available_date="", days_to_election=None,
                pollster="", population="unknown", sample_size=None, methodology="",
                partisan="", source_url="", dem_share=None, rep_share=None,
                dem_rep_margin=None, non_dem_rep_share=None, response_coverage="",
                reported_answer_sum=None, outcome_id="", matchup_status="",
                selection_status="retained_no_time_filter", scalar_seat_mapping_ready=False,
                quality_flags="", source_stage="", source_seat_name="", tracking="",
                hypothetical="", superseded_by="")


def derive(o):
    d, r = o["dem_share"], o["rep_share"]
    if d is not None and r is not None:
        o["dem_rep_margin"] = round(d-r, 12)
        o["non_dem_rep_share"] = round(1-d-r, 12)
    if o["poll_date"] and o["election_date"]:
        o["days_to_election"] = (day(o["election_date"])-day(o["poll_date"])).days
    issues = [f for f in o["quality_flags"].split("|") if f]
    if o["sample_size"] is None or o["sample_size"] <= 0:
        issues.append("missing_or_invalid_sample_size")
    if o["non_dem_rep_share"] is not None and o["non_dem_rep_share"] < -1e-9:
        issues.append("dem_rep_sum_above_one_rounding_or_source_issue")
    o["quality_flags"] = "|".join(sorted(set(issues)))
    return o


def historical(rows, dataset, poll_audit):
    observations, answers, reported = [], [], []
    for line, r in enumerate(rows, 2):
        o = empty_observation("538", dataset, line, r["poll_id"], r["question_id"])
        senate = dataset == "senate"
        o.update(source_file=f"historical/tables/{'senate_polls' if senate else 'generic_ballot_polls'}.csv",
                 source_race_id=r["race_id"], cycle=int(r["cycle"]), geography=r["location"],
                 geography_type="state" if senate else "national", election_date=r["electiondate"],
                 poll_date=r["polldate"], date_basis="median_field_date_only",
                 pollster=r["pollster"], sample_size=number(r["samplesize"]),
                 methodology=blank(r["methodology"]), partisan=blank(r["partisan"]),
                 response_coverage="two_exported_candidates_only",
                 quality_flags="historical_population_and_publication_date_unavailable")
        for party, field in [("DEM", "dem_share"), ("REP", "rep_share")]:
            ids = [i for i in (1, 2) if r[f"cand{i}_party"] == party]
            if len(ids) == 1:
                o[field] = share(r[f"cand{ids[0]}_pct"])
        for i in (1, 2):
            answers.append(dict(observation_id=o["observation_id"], source_row=line,
                                candidate_id=r[f"cand{i}_id"], candidate_name=r[f"cand{i}_name"],
                                source_party=r[f"cand{i}_party"], party=r[f"cand{i}_party"],
                                support_share=share(r[f"cand{i}_pct"]), exact_duplicate=False,
                                party_override=False))
        if senate:
            a = poll_audit[str(line)]
            o.update(outcome_id=a["contest_id"], matchup_status=a["status"],
                     scalar_seat_mapping_ready=a["baseline_eligible"] == "True")
        else:
            o.update(outcome_id=f"{r['cycle']}-US-house-popular-vote-source-only",
                     matchup_status="generic_party_question")
        # Preserve source-linked result claims in a separate table, not the predictor row.
        reported.append(dict(observation_id=o["observation_id"],
                             candidate1_party=r["cand1_party"], candidate1_result_share=share(r["cand1_actual"]),
                             candidate2_party=r["cand2_party"], candidate2_result_share=share(r["cand2_actual"]),
                             verification="see_historical_poll_audit" if senate else "source_reported_not_independently_reconciled"))
        observations.append(derive(o))
    return observations, answers, reported


def current_senate(questions, answer_rows):
    answers_by_q = defaultdict(list)
    for r in answer_rows:
        answers_by_q[r["question_key"]].append(r)
    observations, answers = [], []
    for line, q in enumerate(questions, 2):
        o = empty_observation("nyt", "senate", line, q["poll_id"], q["question_id"])
        ars = answers_by_q[q["question_key"]]
        unique = [a for a in ars if a["exact_duplicate"] == "False"]
        o.update(source_file="2026/tables/senate_general_answers.csv",
                 source_rows="|".join(a["source_row"] for a in ars), source_race_id=q["race_id"],
                 cycle=2026, geography=q["state"], geography_type="state", election_date="2026-11-03",
                 poll_start=q["start_date"], poll_end=q["end_date"], poll_date=q["end_date"],
                 date_basis="field_end", source_available_date=q["created_date"], pollster=q["pollster"],
                 population=q["population"].strip().lower(), sample_size=number(q["sample_size"]),
                 methodology=q["methodology"], partisan=q["partisan"], source_url=q["source_url"],
                 response_coverage="all_exported_answers", reported_answer_sum=number(q["response_sum"])/100,
                 matchup_status="accepted" if q["accepted_matchup"] == "True" else "quarantined",
                 selection_status=q["selection"], scalar_seat_mapping_ready=q["scalar_seat_mapping_ready"] == "True",
                 quality_flags=q["reasons"])
        if q["ranked_choice_round"]:
            o["quality_flags"] += "|rcv_round_"+q["ranked_choice_round"]
        for party, field in [("DEM", "dem_share"), ("REP", "rep_share")]:
            candidates = [a for a in unique if a["reviewed_party"] == party]
            if len(candidates) == 1:
                o[field] = share(candidates[0]["pct"])
        for a in ars:
            answers.append(dict(observation_id=o["observation_id"], source_row=int(a["source_row"]),
                                candidate_id=a["candidate_id"], candidate_name=a["candidate_name"],
                                source_party=a["source_party"], party=a["reviewed_party"],
                                support_share=share(a["pct"]), exact_duplicate=a["exact_duplicate"] == "True",
                                party_override=a["party_override"] == "True"))
        observations.append(derive(o))
    return observations, answers


def current_generic(rows, cutoff):
    observations, answers = [], []
    for line, r in enumerate(rows, 2):
        o = empty_observation("silver_bulletin", "generic_ballot", line, r["poll_id"], r["question_id"])
        o.update(source_file="2026/raw/silver_bulletin_generic.csv", cycle=2026,
                 geography="US", geography_type="national", election_date="2026-11-03",
                 poll_start=str(day(r["startdate"])), poll_end=str(day(r["enddate"])),
                 poll_date=str(day(r["enddate"])), date_basis="field_end",
                 source_available_date=str(day(r["createddate"])), pollster=r["pollster"],
                 population=r["population"].strip().lower(), sample_size=number(r["samplesize"]),
                 partisan=blank(r["partisan"]), source_url=r["url"],
                 dem_share=share(r["dem"]), rep_share=share(r["rep"]),
                 response_coverage="two_exported_parties_only", matchup_status="generic_party_question")
        flags = []
        if o["dem_share"] is None or o["rep_share"] is None:
            flags.append("invalid_party_share")
        if o["population"] not in {"lv", "rv", "a"} or r["subgroup"].strip() != "All polls":
            flags.append("unsupported_population_or_subgroup")
        if day(o["poll_start"]) > day(o["poll_end"]):
            flags.append("invalid_field_dates")
        if max(day(o["poll_end"]), day(o["source_available_date"])) > cutoff:
            flags.append("not_available_at_cutoff")
        if r["multiversions"].strip():
            flags.append("source_marks_multiple_versions_review")
        net = number(r["net"])
        if o["dem_share"] is not None and o["rep_share"] is not None and net is not None:
            if abs(100*(o["dem_share"]-o["rep_share"])-net) > .11:
                flags.append("published_net_disagrees")
        o["quality_flags"] = "|".join(flags)
        for party, field in [("DEM", "dem_share"), ("REP", "rep_share")]:
            answers.append(dict(observation_id=o["observation_id"], source_row=line,
                                candidate_id="", candidate_name="Generic party choice",
                                source_party=party, party=party, support_share=o[field],
                                exact_duplicate=False, party_override=False))
        observations.append(derive(o))
    # Separate questions share sample_group_id; do not confuse them with independent polls.
    seen = set()
    for o in observations:
        key = (o["source_poll_id"], o["source_question_id"])
        if key in seen:
            o["quality_flags"] += "|repeated_poll_question_id_review"
        seen.add(key)
    return observations, answers


def normalize_outcomes(contests, candidates, generic):
    grouped = defaultdict(list)
    for c in candidates:
        grouped[c["contest_id"]].append(c)
    out = []
    for c in contests:
        row = dict(outcome_id=c["contest_id"], outcome_type="senate_contest_stage", cycle=int(c["cycle"]),
                   geography=c["state"], stage=c["stage"], special=c["special"],
                   dem_share=None, rep_share=None, dem_rep_margin=None,
                   status="reconciled_baseline" if c["baseline_eligible"] == "True" else "review_required",
                   review_reasons=c["review_reasons"])
        # Margins can be negative: percentage share validation must not be applied to margins.
        row["dem_rep_margin"] = number(c["dem_rep_margin"])/100 if number(c["dem_rep_margin"]) is not None else None
        for party, field in [("DEMOCRAT", "dem_share"), ("REPUBLICAN", "rep_share")]:
            rs = [r for r in grouped[c["contest_id"]] if r["party"] == party]
            if len(rs) == 1:
                row[field] = share(rs[0]["pct"])
        out.append(row)
    by_cycle = defaultdict(set)
    for r in generic:
        pair = {r["cand1_party"]: share(r["cand1_actual"]), r["cand2_party"]: share(r["cand2_actual"])}
        by_cycle[r["cycle"]].add((pair.get("DEM"), pair.get("REP")))
    for cycle, values in sorted(by_cycle.items()):
        if len(values) != 1:
            raise ValueError(f"Conflicting generic-ballot attached outcomes for {cycle}")
        d, r = next(iter(values))
        out.append(dict(outcome_id=f"{cycle}-US-house-popular-vote-source-only", outcome_type="national_house_popular_vote",
                        cycle=int(cycle), geography="US", stage="general", special="false", dem_share=d, rep_share=r,
                        dem_rep_margin=d-r if d is not None and r is not None else None,
                        status="source_reported_not_independently_reconciled",
                        review_reasons="not_senate_vote_or_seat_total"))
    return out


def normalize_features(rows):
    out = []
    for row in rows:
        r = dict(row)
        for field in ("prior_state_pres_margin", "prior_national_pres_margin", "prior_state_lean"):
            value = number(r[field])
            r[field] = value / 100 if value is not None else None
        out.append(r)
    return out


def full_archive(rows, dataset, state_codes, result_contests, result_candidates):
    """Retain all questions and answers; join by geography/stage/candidate identity.

    Never use poll-to-result distance to accept a matchup. Ambiguous parallel
    contests (e.g. California's regular/special 2024 races) remain unjoined.
    """
    groups = defaultdict(list)
    for line, r in enumerate(rows, 2):
        groups[(r["poll_id"], r["question_id"], r["race_id"])].append((line, r))
    candidate_groups = defaultdict(list)
    for r in result_candidates:
        candidate_groups[r["contest_id"]].append(r)
    observations, answers, ledger = [], [], []
    for (pid, qid, rid), entries in groups.items():
        line, r = entries[0]
        o = empty_observation("538_archive", dataset, line, pid, qid)
        # Both exports use 538 poll IDs: alternate questions must share one sample group.
        o.update(sample_group_id=f"538:{pid}", source_file=f"historical/tables/538_archive_{dataset}.csv",
                 source_rows="|".join(str(i) for i,_ in entries), source_race_id=rid,
                 cycle=int(r["cycle"]), geography=state_codes[r["state"].upper()] if dataset == "senate" else "US",
                 geography_type="state" if dataset == "senate" else "national",
                 election_date=str(day(r["election_date"])) if r["election_date"] else "", poll_start=str(day(r["start_date"])),
                 poll_end=str(day(r["end_date"])), poll_date=str(day(r["end_date"])), date_basis="field_end",
                 source_available_date=str(day(r["created_at"])) if r["created_at"] else "",
                 pollster=r["display_name"] or r["pollster"], sample_size=number(r["sample_size"]),
                 population=r["population"].lower() or "unknown", methodology=r["methodology"],
                 partisan=r["partisan"], source_url=r["url"], source_stage=r["stage"],
                 source_seat_name=r["seat_name"], tracking=r["tracking"], hypothetical=r.get("hypothetical", ""),
                 response_coverage="all_exported_answers" if dataset == "senate" else "exported_party_choices")
        flags = []
        metadata = ["cycle", "state", "start_date", "end_date", "election_date", "population", "sample_size", "stage"]
        if any(len({a[k] for _,a in entries}) != 1 for k in metadata):
            flags.append("conflicting_question_metadata")
        if not o["election_date"]:
            flags.append("missing_election_date")
        if day(o["poll_start"]) > day(o["poll_end"]) or (o["election_date"] and day(o["poll_end"]) > day(o["election_date"])):
            flags.append("invalid_field_dates")
        if r["subpopulation"] or o["population"] not in {"lv", "rv", "a", "v", "unknown"}:
            flags.append("unsupported_population_or_subgroup")
        if dataset == "senate":
            unique, seen = [], set()
            for i,a in entries:
                key = (a["candidate_id"], a["party"], a["pct"])
                duplicate = key in seen
                answers.append(dict(observation_id=o["observation_id"], source_row=i,
                                    candidate_id=a["candidate_id"], candidate_name=a["candidate_name"],
                                    source_party=a["party"], party=a["party"], support_share=share(a["pct"]),
                                    exact_duplicate=duplicate, party_override=False))
                if not duplicate: unique.append(a)
                seen.add(key)
            for party, field in [("DEM", "dem_share"), ("REP", "rep_share")]:
                matches = [a for a in unique if a["party"] == party]
                if len(matches) == 1: o[field] = share(matches[0]["pct"])
            values = [share(a["pct"]) for a in unique]
            o["reported_answer_sum"] = sum(values) if None not in values else None
            if None in values: flags.append("invalid_answer_share")
            if o["reported_answer_sum"] is not None and o["reported_answer_sum"] > 1.001:
                flags.append("answer_sum_above_one_review")
            if r["hypothetical"] == "true": flags.append("hypothetical_matchup")
            if r["ranked_choice_round"] or r["ranked_choice_reallocated"] == "true":
                flags.append("ranked_choice_review")
            matches = []
            for c in result_contests:
                if (not o["election_date"] or int(c["result_year"]) != day(o["election_date"]).year or c["state"] != o["geography"]
                        or c["stage"] != {"general":"gen", "runoff":"runoff"}.get(r["stage"], "unreviewed")):
                    continue
                actual = candidate_groups[c["contest_id"]]
                if all(len([a for a in unique if a["party"] == party]) == 1 and
                       len([a for a in actual if a["party"] == label and surname(a["candidate"]) ==
                            surname(next(a["candidate_name"] for a in unique if a["party"] == party))]) == 1
                       for party,label in [("DEM","DEMOCRAT"),("REP","REPUBLICAN")]):
                    matches.append(c)
            o["matchup_status"] = "unmatched_candidate_or_stage"
            if len(matches) == 1:
                c = matches[0]
                o.update(outcome_id=c["contest_id"], matchup_status="matched_candidate_identity",
                         scalar_seat_mapping_ready=c["baseline_eligible"] == "True" and not flags)
            elif len(matches) > 1:
                o["matchup_status"] = "ambiguous_parallel_contests"
        else:
            if len(entries) != 1: flags.append("repeated_poll_question_id_review")
            o.update(dem_share=share(r["dem"]), rep_share=share(r["rep"]), matchup_status="generic_party_question")
            if r["state"] or r["stage"] != "general": flags.append("not_national_generic_general")
            if int(r["cycle"]) <= 2022: o["outcome_id"] = f"{r['cycle']}-US-house-popular-vote-source-only"
            for party in ["DEM", "REP", "IND"]:
                if r[party.lower()]:
                    answers.append(dict(observation_id=o["observation_id"], source_row=line, candidate_id="",
                                        candidate_name="Generic party choice", source_party=party, party=party,
                                        support_share=share(r[party.lower()]), exact_duplicate=False, party_override=False))
        o["quality_flags"] = "|".join(flags)
        observations.append(derive(o))
        ledger.append({k:o[k] for k in ["observation_id", "source_rows", "cycle", "geography", "source_poll_id",
                                        "source_question_id", "source_race_id", "outcome_id", "matchup_status", "quality_flags"]})
    return observations, answers, ledger


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=LAB/"data/normalized")
    args = parser.parse_args()
    h, c, p = [latest(LAB/"data"/kind) for kind in ("historical", "2026", "prepared")]
    if not all([h, c, p]):
        parser.error("Download and prepare the source bundles first")
    prov = json.loads((p[0]/"provenance.json").read_text())
    if (prov["historical_snapshot"], prov["current_snapshot"]) != (h[0].name, c[0].name):
        parser.error("Prepared data is stale relative to raw downloads; rerun prepare_data.py")
    cutoff = day(prov["as_of"])
    generic = read(h[0]/"tables/generic_ballot_polls.csv")
    audit = {r["source_row"]: r for r in read(p[0]/"tables/historical_poll_audit.csv")}
    observations, answers, reported = [], [], []
    for dataset, rows in [("senate", read(h[0]/"tables/senate_polls.csv")), ("generic_ballot", generic)]:
        os, ans, claims = historical(rows, dataset, audit)
        observations.extend(os); answers.extend(ans); reported.extend(claims)
    os, ans = current_senate(read(p[0]/"tables/current_questions.csv"), read(p[0]/"tables/current_answers.csv"))
    observations.extend(os); answers.extend(ans)
    generic_file = c[0]/"raw/silver_bulletin_generic.csv"
    if generic_file.exists():
        os, ans = current_generic(read(generic_file), cutoff)
        observations.extend(os); answers.extend(ans)
    outcomes = normalize_outcomes(read(p[0]/"tables/historical_contests.csv"), read(p[0]/"tables/historical_candidates.csv"), generic)
    house_file = h[0]/"house_2024_reference.json"
    if house_file.exists():
        from house_reference import outcome
        house_outcome = outcome(json.loads(house_file.read_text()))
        if any(r["outcome_type"] == "national_house_popular_vote" and r["cycle"] == 2024 for r in outcomes):
            raise ValueError("Duplicate national 2024 reference; reconcile before proceeding")
        outcomes.append(house_outcome)
    archive_ledger, overlaps = [], []
    state_codes = {r["state"].upper():r["state_po"] for r in read(h[0]/"tables/senate_results.csv")}
    for dataset in ["senate", "generic_ballot"]:
        file = h[0]/f"tables/538_archive_{dataset}.csv"
        if not file.exists(): continue
        os, ans, ledger = full_archive(read(file), dataset, state_codes,
                                      read(p[0]/"tables/historical_contests.csv"), read(p[0]/"tables/historical_candidates.csv"))
        archive_polls = defaultdict(list)
        for o in os:
            archive_polls[(o["source_poll_id"], o["geography"], o["cycle"])].append(o["observation_id"])
        for o in observations:
            key = (o["source_poll_id"], o["geography"], o["cycle"])
            if o["source"] == "538" and o["dataset"] == dataset and key in archive_polls:
                o.update(selection_status="superseded_by_full_archive", superseded_by="|".join(archive_polls[key]))
                overlaps.append({"legacy_observation_id":o["observation_id"], "archive_observation_ids":o["superseded_by"],
                                 "reason":"same_538_poll_id_geography_cycle; prefer_full_export_questions_and_metadata"})
        observations.extend(os); answers.extend(ans); archive_ledger.extend(ledger)
    national_outcomes = {r["cycle"]:r["outcome_id"] for r in outcomes if r["outcome_type"] == "national_house_popular_vote"}
    for o in observations:
        if o["dataset"] == "generic_ballot" and o["geography"] == "US":
            o["outcome_id"] = national_outcomes.get(o["cycle"], "")
    features = normalize_features(read(p[0]/"tables/all_state_features.csv"))
    current_contests = normalize_features(read(p[0]/"tables/current_features.csv"))
    assert len({o["observation_id"] for o in observations}) == len(observations)
    summary = dict(as_of=str(cutoff), observations=len(observations), answers=len(answers), outcomes=len(outcomes),
                   by_source_dataset=dict(Counter(o["source"]+":"+o["dataset"] for o in observations)),
                   unknown_population=sum(o["population"] == "unknown" for o in observations),
                   missing_sample_size=sum(o["sample_size"] is None for o in observations),
                   current_generic_present=generic_file.exists(),
                   current_generic_quality_flags=dict(Counter(f for o in observations if o["source"] == "silver_bulletin" for f in o["quality_flags"].split("|") if f)),
                   older_polls_retained=True, time_weighting_applied=False, forecast_ready=False)
    summary.update(state_feature_rows=len(features), current_contests=len(current_contests))
    summary.update(full_archive_questions=len(archive_ledger), legacy_rows_superseded=len(overlaps))
    with Snapshot(args.output_dir, "normalized") as bundle:
        for name, rows in [("poll_observations", observations), ("poll_answers", answers),
                           ("election_outcomes", outcomes), ("source_reported_outcomes", reported),
                           ("state_features", features), ("current_contests", current_contests)]:
            write_table(bundle, name, rows)
        write_table(bundle, "archive_poll_audit", archive_ledger, ("observation_id",))
        write_table(bundle, "archive_overlap_ledger", overlaps, ("legacy_observation_id",))
        bundle.write_json("provenance.json", {"snapshots": {label: snap[0].name for label, snap in [("historical", h), ("2026", c), ("prepared", p)]},
                          "manifest_sha256": {label: digest((snap[0]/"manifest.json").read_bytes()) for label, snap in [("historical", h), ("2026", c), ("prepared", p)]},
                          "script_sha256": {name: digest((LAB/"scripts"/name).read_bytes()) for name in ["normalize_data.py", "prepare_data.py", "data_utils.py", "house_reference.py"]},
                          "as_of": str(cutoff), "units": "All support shares and margins are fractions; sample_size is reported respondent count.",
                          "current_generic_columns_used": ["dem", "rep", "net"],
                          "aggregator_model_outputs_not_used": ["adjusted_dem", "adjusted_rep", "adjusted_net", "weight", "influence"],
                          "identity_scope": "Observation IDs are local to this versioned bundle; sample_group_id is source poll ID, not proof of cross-source independence."})
        bundle.write_json("summary.json", summary)
        bundle.finish(summary)


if __name__ == "__main__":
    main()
