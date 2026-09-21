"""Small, standard-library helpers for auditable polling snapshots."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import tempfile
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import time

LAB = Path(__file__).resolve().parents[1]


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def fetch(url, timeout=45):
    """GET public data; retry transient errors, never substitute cached content."""
    for attempt in range(3):
        try:
            req = Request(url, headers={"User-Agent": "US-election-2026-educational-lab/1.0"})
            with urlopen(req, timeout=timeout) as response:
                return response.read()
        except (HTTPError, URLError, TimeoutError) as exc:
            if isinstance(exc, HTTPError) and exc.code < 500 and exc.code != 429:
                raise
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def table(raw, required, delimiter=","):
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")), delimiter=delimiter)
    fields = reader.fieldnames or []
    if len(fields) != len(set(fields)):
        raise ValueError("Duplicate column names")
    missing = set(required) - set(fields)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    rows = list(reader)
    if not rows:
        raise ValueError("Empty dataset: refusing to publish a snapshot")
    if any(None in row or any(v is None for v in row.values()) for row in rows):
        raise ValueError("Malformed table: inconsistent row widths")
    return fields, rows


def csv_bytes(fields, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode()


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def latest(root):
    pointer = root / "latest.json"
    if not pointer.exists():
        return None
    name = json.loads(pointer.read_text())["snapshot"]
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve() / "snapshots"):
        raise ValueError("Invalid latest snapshot path")
    manifest = json.loads((path / "manifest.json").read_text())
    for name, info in manifest["files"].items():
        if digest((path / name).read_bytes()) != info["sha256"]:
            raise ValueError(f"Snapshot checksum mismatch: {path / name}")
    return path, manifest


class Snapshot:
    """Stage a complete bundle; atomically publish latest only after validation.

    Lock concurrent writers. A failed download never changes the latest pointer.
    Identical files reuse the prior snapshot. last_check.json tracks successful
    checks, including unchanged checks, separately from data retrieval dates.
    """

    def __init__(self, root, kind):
        self.root = Path(root).resolve()
        self.kind = kind
        self.files = {}

    def __enter__(self):
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = self.root / ".download.lock"
        try:
            self.lock.mkdir()
        except FileExistsError:
            raise RuntimeError(f"Another download may be running: {self.lock}. "
                               "Remove this directory only if no downloader is running.")
        try:
            self.previous = latest(self.root)
            self.started = utc_now()
            self.stage = Path(tempfile.mkdtemp(prefix=".staging-", dir=self.root))
            return self
        except BaseException:
            self.lock.rmdir()
            raise

    def add(self, name, raw, **metadata):
        target = self.stage / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        self.files[name] = {"sha256": digest(raw), "bytes": len(raw), **metadata}

    def download(self, name, url, timeout, **metadata):
        raw = fetch(url, timeout)
        self.add(name, raw, url=url, retrieved_at=utc_now(), **metadata)
        return raw

    def write_json(self, name, value):
        self.add(name, json_bytes(value))

    def finish(self, summary, changes=None):
        hashes = {k: v["sha256"] for k, v in self.files.items()}
        prior_hashes = ({k: v["sha256"] for k, v in self.previous[1]["files"].items()
                         if k != "changes.json"} if self.previous else {})
        unchanged = bool(self.previous) and hashes == prior_hashes
        if unchanged:
            path = self.previous[0]
        else:
            if changes is not None:
                self.write_json("changes.json", changes)
            manifest = {"schema_version": 1, "kind": self.kind,
                        "retrieved_at": self.started, "files": self.files,
                        "summary": summary}
            (self.stage / "manifest.json").write_bytes(json_bytes(manifest))
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
            path = self.root / "snapshots" / stamp
            path.parent.mkdir(exist_ok=True)
            self.stage.rename(path)
            atomic_json(self.root / "latest.json", {"snapshot": str(path.relative_to(self.root))})
        atomic_json(self.root / "last_check.json", {
            "checked_at": utc_now(), "unchanged": unchanged,
            "snapshot": str(path.relative_to(self.root))})
        print(f"{'Unchanged' if unchanged else 'Saved'}: {path}")
        print(json.dumps(summary, indent=2, sort_keys=True))
        return path

    def __exit__(self, *_):
        if self.stage.exists():
            shutil.rmtree(self.stage)
        self.lock.rmdir()


def atomic_json(path, value):
    fd, name = tempfile.mkstemp(prefix=".pointer-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(json_bytes(value))
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def poll_changes(old_rows, new_rows):
    """Compare whole polls, preserving multiple questions/answers and duplicates."""
    def grouped(rows):
        groups = {}
        for row in rows:
            groups.setdefault(row["poll_id"], []).append(json.dumps(row, sort_keys=True))
        return {key: sorted(values) for key, values in groups.items()}
    old, new = grouped(old_rows), grouped(new_rows)
    added = sorted(new.keys() - old.keys())
    removed = sorted(old.keys() - new.keys())
    revised = sorted(k for k in old.keys() & new.keys() if old[k] != new[k])
    return {"added_poll_ids": added, "removed_poll_ids": removed,
            "revised_poll_ids": revised, "counts": {
                "added": len(added), "removed": len(removed), "revised": len(revised)}}
