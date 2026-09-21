"""Audited 2024 national House benchmark from the official Clerk compilation.

This is the Clerk's reported vote rounds (AK first count, ME-2 final RCV),
not a harmonized first-preference national tally. See NATIONAL_RESULT_2024.md.
"""
from collections import Counter, defaultdict
import re
import subprocess

from data_utils import csv_bytes, digest, table

URL = "https://clerk.house.gov/member_info/electionInfo/2024/statistics2024.pdf"
OUTCOME_ID = "2024-US-house-popular-vote-clerk"
EXCLUDED = {"Blank", "Blanks", "Blank Votes", "Over Votes", "Under Votes", "Void",
            "Continuing Ballots", "Exhausted Ballots"}
OTHER = {"Write-in", "Scattering", "All Others", "Other Write-ins", "Miscellaneous"}
FUSION = {"Conservative", "Working Families", "Common Sense", "Independent", "Common Sense Suffolk"}
TERRITORIES = {"DISTRICT OF COLUMBIA", "AMERICAN SAMOA", "GUAM", "NORTHERN MARIANA ISLANDS",
               "PUERTO RICO", "VIRGIN ISLANDS"}


def extract(text, states):
    """Read only the 50 states' House candidate blocks, never recap tables."""
    state = district = None
    active = False
    rows = []
    for page, body in enumerate(text.split("\f"), 1):
        for line in body.splitlines():
            label = line.strip()
            header = label.replace("—Continued", "")
            if header in states:
                if state != states[header]:
                    district, active = None, False
                state = states[header]
            if header in TERRITORIES:
                state, active = None, False
            if "FOR UNITED STATES REPRESENTATIVE" in label and state:
                active = True
            elif label.startswith("FOR ") or label.startswith("Recapitulation"):
                active = False
            if not active:
                continue
            if label == "AT LARGE":
                district = 0
            match = re.match(r"(\d+)\.\s+(.*)", label)
            if match:
                district, label = int(match[1]), match[2]
            match = re.match(r"(.+?)\s*\.{3,}\s+([\d,]+|\(1\))\s*$", label)
            if not match:
                if "..." in label:
                    raise ValueError(f"Unparsed House vote line on PDF page {page}: {label}")
                continue
            if district is None:
                raise ValueError("Vote line without district")
            value = match[2]
            rows.append(dict(page=page, state=state, district=district, label=match[1].strip(),
                             votes=None if value == "(1)" else int(value.replace(",", ""))))
    return rows


def reconcile(rows):
    ledger, candidates = [], {}
    previous_key = previous_candidate = previous_party = None
    for index, source in enumerate(rows, 1):
        r = dict(source, source_row=index, candidate="", party="", disposition="")
        key, label = (r["state"], r["district"]), r["label"]
        if key != previous_key:
            previous_candidate = previous_party = None
        previous_key = key
        if label in EXCLUDED:
            r["disposition"] = "excluded_non_candidate_or_rcv_summary"
            previous_candidate = previous_party = None
        else:
            if label in FUSION:
                if previous_candidate is None:
                    raise ValueError(f"Fusion line without preceding candidate: {r}")
                r.update(candidate=previous_candidate, party=previous_party, disposition="included_fusion_line")
            elif label in OTHER:
                r.update(candidate=f"Unallocated: {label}", party="OTHER", disposition="included_other_votes")
                previous_candidate = previous_party = None
            elif "," in label:
                name, affiliation = label.split(",", 1)
                d = bool(re.search(r"\bDemocrat(?:ic)?\b", affiliation))
                rep = bool(re.search(r"\bRepublican\b", affiliation))
                if d and rep:
                    raise ValueError(f"Ambiguous major-party candidate: {label}")
                party = "DEM" if d else "REP" if rep else "OTHER"
                r.update(candidate=name, party=party, disposition="included_candidate")
                previous_candidate, previous_party = name, party
            else:
                raise ValueError(f"Unclassified vote line: {r}")
            if r["votes"] is None:
                r["disposition"] = "unopposed_no_vote_reported"
            candidate_key = (*key, r["candidate"])
            if candidate_key not in candidates:
                candidates[candidate_key] = dict(state=r["state"], district=r["district"], candidate=r["candidate"],
                                                 party=r["party"], votes=r["votes"], source_rows=str(index))
            else:
                c = candidates[candidate_key]
                if r["disposition"] != "included_fusion_line" or c["party"] != r["party"] or c["votes"] is None:
                    raise ValueError(f"Unexpected repeated candidate: {r}")
                c["votes"] += r["votes"]
                c["source_rows"] += f"|{index}"
        ledger.append(r)
    candidates = list(candidates.values())
    totals = Counter()
    for c in candidates:
        totals[c["party"]] += c["votes"] or 0
    total = sum(totals.values())
    excluded = sum(r["votes"] or 0 for r in ledger if r["disposition"].startswith("excluded"))
    source_total = sum(r["votes"] or 0 for r in rows)
    assert total + excluded == source_total
    summary = dict(cycle=2024, source_url=URL, source_rows=len(rows),
                   districts=len({(r["state"], r["district"]) for r in rows}),
                   states=len({r["state"] for r in rows}), source_total=source_total,
                   excluded_votes=excluded, dem_votes=totals["DEM"], rep_votes=totals["REP"],
                   other_votes=totals["OTHER"], total_candidate_votes=total,
                   unreported_vote_contests=sorted(f"{r['state']}-{r['district']}" for r in candidates if r["votes"] is None),
                   dem_share=totals["DEM"]/total, rep_share=totals["REP"]/total,
                   dem_rep_margin=(totals["DEM"]-totals["REP"])/total,
                   vote_rounds="Clerk reported rounds: Alaska first count; Maine district 2 final RCV",
                   excluded_by_label=dict(Counter({label:sum(r["votes"] or 0 for r in ledger if r["label"]==label)
                                                   for label in sorted(EXCLUDED)})))
    return ledger, candidates, summary


def get_house_reference(snap, timeout):
    raw = snap.download("raw/house_2024/statistics2024.pdf", URL, timeout, attribution="U.S. House Clerk")
    if not raw.startswith(b"%PDF"):
        raise ValueError("Clerk source is not a PDF")
    text = subprocess.run(["pdftotext", "-layout", str(snap.stage/"raw/house_2024/statistics2024.pdf"), "-"],
                          check=True, capture_output=True).stdout
    snap.add("raw/house_2024/statistics2024.txt", text, source_pdf_sha256=digest(raw))
    _, state_rows = table((snap.stage/"tables/senate_results.csv").read_bytes(), {"state", "state_po"})
    states = {r["state"].upper():r["state_po"] for r in state_rows}
    ledger, candidates, summary = reconcile(extract(text.decode(), states))
    # Fixed official edition checks: fail visibly if source layout/coverage changes.
    if (summary["states"], summary["districts"], summary["source_total"]) != (50, 435, 149543421):
        raise ValueError(f"Clerk 2024 coverage/recap reconciliation failed: {summary}")
    if summary["unreported_vote_contests"] != ["FL-20", "OK-3"]:
        raise ValueError("Unexpected unreported House vote contests")
    for name, rows in [("house_2024_vote_ledger", ledger), ("house_2024_candidates", candidates)]:
        snap.add(f"tables/{name}.csv", csv_bytes(list(rows[0]), rows))
    summary["source_pdf_sha256"] = digest(raw)
    snap.write_json("house_2024_reference.json", summary)
    return summary


def outcome(reference):
    return dict(outcome_id=OUTCOME_ID, outcome_type="national_house_popular_vote", cycle=2024,
                geography="US", stage="general", special="false", dem_share=reference["dem_share"],
                rep_share=reference["rep_share"], dem_rep_margin=reference["dem_rep_margin"],
                status="official_clerk_candidate_vote_reference",
                review_reasons="mixed_rcv_rounds|two_unopposed_contests_no_vote_reported|not_senate_or_presidential_vote")
