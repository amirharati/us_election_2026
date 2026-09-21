#!/usr/bin/env python3
"""Refresh 2026 polls, preserving snapshots and reporting source revisions."""
import argparse
from collections import Counter
from datetime import datetime
import json
from pathlib import Path

from data_utils import LAB, Snapshot, csv_bytes, poll_changes, table

SENATE_URL = "https://www.nytimes.com/newsgraphics/polls/senate.csv"
GENERIC_URL = ("https://docs.google.com/spreadsheets/d/e/"
               "2PACX-1vRsvXNCZ0ubJr8D_yNcU5q6C0_HBa35K7oDK03KpO7Ca43UwdXaIdvVLWoXEmHHph0EREz5430Hm5yZ/pub?output=csv")
REQUIRED = {"poll_id", "question_id", "candidate_id", "candidate_name", "race_id",
            "state", "cycle", "stage", "office_type", "start_date", "end_date",
            "created_at", "sample_size", "population", "subpopulation", "party", "pct",
            "election_date", "url"}


def poll_date(value):
    for fmt in ("%m/%d/%y", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Unrecognized poll date: {value!r}")


def select_general(raw):
    fields, rows = table(raw, REQUIRED)
    selected = [r for r in rows if r["cycle"] == "2026" and r["stage"].lower() in
                {"general", "special general", "general runoff", "runoff", "special runoff"}
                and r["office_type"].lower() == "u.s. senate"]
    if not selected:
        raise ValueError("No 2026 Senate general-election observations")
    for r in selected:
        if not all(r[k] for k in ("poll_id", "question_id", "candidate_id", "state", "race_id")):
            raise ValueError("Missing poll/question/candidate/state/race identifier")
        if not 0 <= float(r["pct"]) <= 100:
            raise ValueError("Candidate percentage outside 0..100")
        if poll_date(r["start_date"]) > poll_date(r["end_date"]):
            raise ValueError("Poll starts after it ends")
    return fields, rows, selected


def coverage(rows, contests):
    expected = {r["state"] for r in contests}
    unexpected = {r["state"] for r in rows} - expected
    if unexpected:
        raise ValueError(f"Polls refer to states outside the contest manifest: {sorted(unexpected)}. "
                         "Review new elections and update config/contests_2026.csv first.")
    report = []
    for contest in contests:
        a = [r for r in rows if r["state"] == contest["state"]]
        report.append({**contest, "poll_count": len({r["poll_id"] for r in a}),
                       "question_count": len({r["question_id"] for r in a}), "answer_rows": len(a),
                       "latest_poll_end": max((poll_date(r["end_date"]).isoformat() for r in a), default=""),
                       "status": "polls_need_matchup_review" if a else "no_polls_in_source"})
    return report


def run(output_dir, include_generic=False, timeout=45):
    with Snapshot(output_dir, "2026") as snap:
        config = (LAB / "config/contests_2026.csv").read_bytes()
        _, contests = table(config, {"contest_id", "state", "seat_class", "special", "election_date"})
        if len({r["state"] for r in contests}) != len(contests):
            raise ValueError("Multiple contests in one state require explicit source race-ID mapping")
        snap.add("config/contests_2026.csv", config)
        snap.add("config/chamber_2026.json", (LAB / "config/chamber_2026.json").read_bytes())
        raw = snap.download("raw/nyt_senate.csv", SENATE_URL, timeout,
                            license="CC BY 4.0", attribution="The New York Times")
        fields, all_rows, rows = select_general(raw)
        # This is a broad extraction, NOT a nominee-filtered modeling table.
        snap.add("tables/senate_general_answers.csv", csv_bytes(fields, rows))
        report = coverage(rows, contests)
        snap.add("coverage.csv", csv_bytes(list(report[0]), report))
        previous_rows = []
        if snap.previous:
            _, previous_rows = table((snap.previous[0] / "tables/senate_general_answers.csv").read_bytes(), REQUIRED)
        changes = poll_changes(previous_rows, rows)
        changes["scope"] = "2026 general-election extraction; comparison is by whole poll_id, not candidate row"
        changes["previous_snapshot"] = str(snap.previous[0].relative_to(snap.root)) if snap.previous else None
        summary = {"source_answer_rows": len(all_rows), "general_answer_rows": len(rows),
                   "distinct_polls": len({r["poll_id"] for r in rows}),
                   "distinct_questions": len({r["question_id"] for r in rows}),
                   "states_with_polls": len({r["state"] for r in rows}),
                   "contests": len(contests),
                   "states_without_polls": [r["state"] for r in report if not r["poll_count"]],
                   "latest_poll_end": max(poll_date(r["end_date"]).isoformat() for r in rows),
                   "stage_counts_all_source_rows": dict(Counter(r["stage"] for r in all_rows)),
                   "model_ready": False,
                   "warning": "Answer rows include alternative matchups, populations and non-candidate responses. "
                              "Audit nominees, overlap, independents and election rules before modeling."}
        if include_generic:
            generic = snap.download("raw/silver_bulletin_generic.csv", GENERIC_URL, timeout,
                                    attribution="Silver Bulletin; see DATA.md for reuse terms")
            _, gr = table(generic, {"poll_id", "pollster", "startdate", "enddate", "dem", "rep"})
            summary["generic_ballot_rows"] = len(gr)
            summary["generic_latest_poll_end"] = max(poll_date(r["enddate"]).isoformat() for r in gr)
        snap.write_json("summary.json", summary)
        result = snap.finish(summary, changes)
        print(f"Poll changes: {changes['counts']}")
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=LAB / "data/2026")
    parser.add_argument("--include-generic-ballot", action="store_true", help="Also refresh the optional national input")
    parser.add_argument("--timeout", type=float, default=45)
    args = parser.parse_args()
    try:
        run(args.output_dir, args.include_generic_ballot, args.timeout)
    except Exception as exc:
        parser.exit(1, f"Download failed; previous snapshot preserved: {exc}\n")


if __name__ == "__main__":
    main()
