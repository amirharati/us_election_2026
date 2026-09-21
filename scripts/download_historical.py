#!/usr/bin/env python3
"""Download polling errors and complete historical election-result archives."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
from urllib.parse import urlencode

from data_utils import LAB, Snapshot, csv_bytes, latest, table
from house_reference import get_house_reference

POLLS_URL = "https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/raw_polls.csv"
DATAVERSE = "https://dataverse.harvard.edu/api"
DATASETS = {
    "senate_results": ("doi:10.7910/DVN/PEJ5QU", r"1976-\d{4}-senate.*\.(tab|csv)$"),
    "presidential_results": ("doi:10.7910/DVN/42MVDX", r"1976-\d{4}-president.*\.(tab|csv)$"),
}

# Fixed captures of the original publisher's CSVs, not third-party reconstructions.
ARCHIVE_POLLS = {
    "senate": ("20250306125405", {"party", "candidate_name", "candidate_id", "pct", "stage"}),
    "generic_ballot": ("20250306091811", {"dem", "rep", "stage"}),
}


def get_archive_polls(snap, timeout):
    summary = {}
    for dataset, (capture, extra) in ARCHIVE_POLLS.items():
        original = f"https://projects.fivethirtyeight.com/polls-page/data/{dataset}_polls_historical.csv"
        raw = snap.download(f"raw/538_archive_{dataset}.csv",
                            f"https://web.archive.org/web/{capture}id_/{original}", timeout,
                            original_url=original, archive_capture=capture,
                            attribution="FiveThirtyEight / ABC News", license="CC BY 4.0")
        fields, rows = table(raw, {"poll_id", "question_id", "race_id", "cycle", "state",
                                  "start_date", "end_date", "election_date", "sample_size", "population"} | extra)
        if not {"2018", "2020", "2022", "2024"} <= {r["cycle"] for r in rows}:
            raise ValueError(f"{dataset}: archive is missing expected cycles")
        snap.add(f"tables/538_archive_{dataset}.csv", csv_bytes(fields, rows))
        summary[dataset] = {"rows": len(rows), "rows_by_cycle": dict(sorted(Counter(r["cycle"] for r in rows).items())),
                            "unit": "candidate answer" if dataset == "senate" else "poll question"}
    return summary


def augment_polls(output_dir, timeout=45):
    """Add full poll archives to the verified bundle without refreshing results."""
    previous = latest(Path(output_dir))
    if not previous:
        raise ValueError("Download the base historical bundle first")
    with Snapshot(output_dir, "historical") as snap:
        for name, info in previous[1]["files"].items():
            if name not in {"summary.json", "changes.json"} and "538_archive_" not in name:
                snap.add(name, (previous[0]/name).read_bytes(),
                         **{k:v for k,v in info.items() if k not in {"sha256", "bytes"}})
        summary = json.loads((previous[0]/"summary.json").read_text())
        summary["full_poll_archives"] = get_archive_polls(snap, timeout)
        snap.write_json("summary.json", summary)
        return snap.finish(summary)


def get_results(snap, label, doi, pattern, timeout):
    url = f"{DATAVERSE}/datasets/:persistentId/?{urlencode({'persistentId': doi})}"
    raw = snap.download(f"raw/{label}_metadata.json", url, timeout)
    version = json.loads(raw)["data"]["latestVersion"]
    if version["versionState"] != "RELEASED":
        raise ValueError(f"{doi}: latest version is not released")
    files = version["files"]
    matches = [f for f in files if re.fullmatch(pattern, f["dataFile"]["filename"])]
    if len(matches) != 1:
        raise ValueError(f"Expected one {label} file, found {len(matches)}; inspect source metadata")
    item = matches[0]
    if item.get("restricted"):
        raise ValueError(f"{doi}: results file is restricted")
    f = item["dataFile"]
    filename = f["filename"]
    raw = snap.download(f"raw/{label}/{filename}", f"{DATAVERSE}/access/datafile/{f['id']}", timeout,
                        doi=doi, dataset_version=f"{version['versionNumber']}.{version['versionMinorNumber']}",
                        license=version.get("license"), datafile_id=f["id"])
    required = {"year", "state_po", "candidate", "candidatevotes", "totalvotes", "party_simplified"}
    if label == "senate_results":
        required |= {"stage", "special", "mode"}
    fields, rows = table(raw, required, "\t" if filename.endswith(".tab") else ",")
    years = sorted({int(r["year"]) for r in rows})
    if len({r["state_po"] for r in rows}) < 50 or years[-1] < 2024:
        raise ValueError(f"{label}: expected all states and results through at least 2024")
    snap.add(f"tables/{label}.csv", csv_bytes(fields, rows))
    for support in files:
        sf = support["dataFile"]
        if sf["id"] != f["id"] and not support.get("restricted") and sf["filesize"] < 1_000_000:
            name = Path(sf["filename"]).name
            snap.download(f"raw/{label}/{name}", f"{DATAVERSE}/access/datafile/{sf['id']}", timeout,
                          doi=doi, datafile_id=sf["id"])
    return {"candidate_rows": len(rows), "years": years,
            "states": len({r["state_po"] for r in rows}),
            "warning": "Raw result rows, not reconciled contests; see DATA.md before aggregating."}


def augment_house_result(output_dir, timeout=45):
    """Add the official 2024 House reference without refreshing polling or other results."""
    previous = latest(Path(output_dir))
    if not previous:
        raise ValueError("Download the base historical bundle first")
    with Snapshot(output_dir, "historical") as snap:
        for name, info in previous[1]["files"].items():
            if name not in {"summary.json", "changes.json"} and "house_2024" not in name:
                snap.add(name, (previous[0]/name).read_bytes(),
                         **{k:v for k,v in info.items() if k not in {"sha256", "bytes"}})
        summary = json.loads((previous[0]/"summary.json").read_text())
        summary["house_2024_reference"] = get_house_reference(snap, timeout)
        snap.write_json("summary.json", summary)
        return snap.finish(summary)


def run(output_dir, refresh=False, timeout=45):
    if not refresh:
        current = latest(Path(output_dir))
        if current:
            print(f"Historical snapshot verified: {current[0]}\nUse --refresh to check source updates.")
            return current[0]
    with Snapshot(output_dir, "historical") as snap:
        raw = snap.download("raw/fivethirtyeight_raw_polls.csv", POLLS_URL, timeout,
                            license="CC BY 4.0", attribution="FiveThirtyEight")
        fields, rows = table(raw, {"cycle", "type_simple", "poll_id", "race_id", "location",
                                  "polldate", "electiondate", "time_to_election",
                                  "margin_poll", "margin_actual", "cand1_party", "cand2_party"})
        senate = [r for r in rows if r["type_simple"] == "Sen-G"]
        if not senate:
            raise ValueError("No Senate general-election polls found")
        snap.add("tables/senate_polls.csv", csv_bytes(fields, senate))
        # Retain generic ballot for an optional national-factor extension.
        generic = [r for r in rows if r["type_simple"] == "House-G-US"]
        snap.add("tables/generic_ballot_polls.csv", csv_bytes(fields, generic))
        horizons = [float(r["time_to_election"]) for r in senate]
        summary = {"senate_poll_rows": len(senate), "generic_ballot_rows": len(generic),
                   "senate_cycles": dict(sorted(Counter(r["cycle"] for r in senate).items())),
                   "senate_days_to_election_range": [min(horizons), max(horizons)]}
        for label, (doi, pattern) in DATASETS.items():
            summary[label] = get_results(snap, label, doi, pattern, timeout)
        summary["full_poll_archives"] = get_archive_polls(snap, timeout)
        summary["house_2024_reference"] = get_house_reference(snap, timeout)
        summary["limitations"] = [
            "Polling and result coverage differ; inspect years before backtesting.",
            "Historical files retrieved today are revised archives, not publication-time snapshots.",
            "Result tables include special elections, stages and party lines requiring reconciliation."]
        snap.write_json("summary.json", summary)
        return snap.finish(summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=LAB / "data/historical")
    parser.add_argument("--refresh", action="store_true", help="Recheck sources instead of using the verified cache")
    parser.add_argument("--augment-polls", action="store_true", help="Add full 2018–2024 poll archives to the cached bundle")
    parser.add_argument("--augment-house-result", action="store_true", help="Add the official 2024 national House vote reference")
    parser.add_argument("--timeout", type=float, default=45)
    args = parser.parse_args()
    try:
        if args.augment_house_result:
            augment_house_result(args.output_dir, args.timeout)
        elif args.augment_polls:
            augment_polls(args.output_dir, args.timeout)
        else:
            run(args.output_dir, args.refresh, args.timeout)
    except Exception as exc:
        parser.exit(1, f"Download failed; previous snapshot preserved: {exc}\n")


if __name__ == "__main__":
    main()
