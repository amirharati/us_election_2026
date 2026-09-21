#!/usr/bin/env python3
"""Offline checks of the latest feature source bundles, without modifying data."""
import argparse
import json
from pathlib import Path

from data_utils import LAB, latest
from feature_download import iter_csv


def verify(root):
    verified = []
    for pointer in sorted(Path(root).glob("*/*/latest.json")):
        path, manifest = latest(pointer.parent)  # Independently rehash every declared file.
        summary = json.loads((path / "summary.json").read_text())
        request = json.loads((path / "request.json").read_text())
        if summary["model_ready"] is not False:
            raise ValueError(f"Acquisition bundle must not claim model readiness: {path}")
        if summary["source"] != pointer.parent.parent.name:
            raise ValueError(f"Wrong source identity: {path}")
        if pointer.parent.name != f"{request['mode']}_{request['year']}":
            raise ValueError(f"Wrong requested year/mode: {path}")
        for filename, info in summary["artifacts"].items():
            raw_name = "raw/" + filename
            if raw_name not in manifest["files"]:
                raise ValueError(f"Missing source artifact: {path / raw_name}")
            if "selected_rows" in info:
                name = "tables/" + Path(filename).stem + ".csv"
                raw = (path / name).read_bytes()
                # An empty current-year extract is valid, but still needs its header.
                if info["selected_rows"]:
                    fields, rows = iter_csv(raw)
                    if sum(1 for _ in rows) != info["selected_rows"]:
                        raise ValueError(f"Extract row count differs from manifest: {path / name}")
                else:
                    import csv
                    rows = list(csv.reader(raw.decode("utf-8").splitlines()))
                    if len(rows) != 1 or rows[0] != info["columns"]:
                        raise ValueError(f"Invalid empty-year extract: {path / name}")
        verified.append(str(path))
    if not verified:
        raise ValueError("No feature snapshots found")
    return verified


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=LAB / "data/features")
    args = parser.parse_args()
    try:
        paths = verify(args.output_dir)
        print(f"Verified {len(paths)} latest feature bundles: checksums, identities, raw files and extract row counts.")
    except Exception as exc:
        parser.exit(1, f"Feature verification failed: {exc}\n")
