"""Shared acquisition engine for environmental features; no model joins here.

Only standard-library dependencies. Original files remain intact. CSV extracts
preserve source units; spreadsheet/PDF interpretation is a later preparation step.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime
import gzip
from html.parser import HTMLParser
import io
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen
import zipfile

from data_utils import LAB, Snapshot, atomic_json, csv_bytes, digest, latest, utc_now

VERSION = 1
MAX_BYTES = 250_000_000
SECRET_KEYS = {"api_key", "apikey", "key", "token", "access_token", "registrationkey"}


class NeedsAccess(RuntimeError):
    """A source requires a credential, supplied export, or explicit report URL."""


def public_url(url):
    parts = urlsplit(url)
    if parts.username or parts.password:
        raise ValueError("Credentials in URLs are not supported")
    return urlunsplit((parts.scheme, parts.netloc, parts.path,
                      urlencode([(k, "REDACTED" if k.lower() in SECRET_KEYS else v)
                                 for k, v in parse_qsl(parts.query, keep_blank_values=True)]), ""))


def request_bytes(url, timeout=30, headers=None):
    """Bounded public GET, gzip decoding, transient retries, redacted errors."""
    if urlsplit(url).scheme != "https":
        raise ValueError("Only HTTPS downloads are supported")
    safe = public_url(url)
    for attempt in range(3):
        try:
            req = Request(url, headers={"User-Agent": "US-election-2026-educational-lab/1.0",
                                       "Accept-Encoding": "identity", **(headers or {})})
            with urlopen(req, timeout=timeout) as response:
                raw = response.read(MAX_BYTES + 1)
                metadata = {"url": safe, "resolved_url": public_url(response.url),
                            "retrieved_at": utc_now(),
                            "content_type": response.headers.get("Content-Type", ""),
                            "etag": response.headers.get("ETag", ""),
                            "http_last_modified": response.headers.get("Last-Modified", "")}
            if len(raw) > MAX_BYTES:
                raise ValueError("Source exceeds download size limit")
            if raw.startswith(b"\x1f\x8b"):
                with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
                    raw = stream.read(MAX_BYTES + 1)
                metadata["transport_decoding"] = "gzip"
            if not raw or len(raw) > MAX_BYTES:
                raise ValueError("Empty or oversized decoded response")
            return raw, metadata
        except HTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504} or attempt == 2:
                raise RuntimeError(f"HTTP {exc.code}: {safe}") from None
        except (URLError, TimeoutError, OSError):
            if attempt == 2:
                raise RuntimeError(f"Network/timeout failure: {safe}") from None
        time.sleep(attempt + 1)


def request_fred_csv(url, timeout=30):
    """Use curl's HTTP/1.1 transport for FRED graph exports when available.

    This endpoint can time out with urllib or fail HTTP/2 streams. Keep TLS
    verification, HTTPS redirects, bounded download sizes and source validation.
    Other providers and the optional authenticated vintage API are unchanged.
    """
    import shutil
    import subprocess
    import tempfile
    parts = urlsplit(url)
    if parts.scheme != 'https' or parts.hostname != 'fred.stlouisfed.org' or parts.path != '/graph/fredgraph.csv':
        raise ValueError('Expected a public FRED graph CSV URL')
    safe = public_url(url)
    curl = shutil.which('curl')
    if curl is None:
        return request_bytes(url, timeout)
    with tempfile.TemporaryDirectory(prefix='fred-csv-') as temp:
        data = Path(temp)/'data.csv'; headers = Path(temp)/'headers.txt'
        command = [curl, '--http1.1', '--silent', '--show-error', '--fail', '--location',
                   '--proto', '=https', '--proto-redir', '=https',
                   '--connect-timeout', str(min(timeout,10)), '--max-time', str(timeout),
                   '--max-filesize', str(MAX_BYTES), '--dump-header', str(headers),
                   '--output', str(data), '--write-out', '%{url_effective}', url]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=timeout+5)
        except subprocess.TimeoutExpired:
            raise RuntimeError(f'FRED CSV download timed out after {timeout}s: {safe}') from None
        if result.returncode:
            detail = result.stderr.strip().replace(url,safe)[:500]
            raise RuntimeError(f'FRED CSV download failed (curl {result.returncode}): {detail}')
        if not data.exists() or not 0 < data.stat().st_size <= MAX_BYTES:
            raise ValueError('Empty or oversized FRED CSV response')
        response_headers = {}
        for line in headers.read_text().splitlines():
            if line.startswith('HTTP/'): response_headers = {}
            elif ':' in line:
                key,value=line.split(':',1);response_headers[key.lower()]=value.strip()
        return data.read_bytes(), dict(url=safe,resolved_url=public_url(result.stdout.strip()),
            retrieved_at=utc_now(),content_type=response_headers.get('content-type',''),
            etag=response_headers.get('etag',''),http_last_modified=response_headers.get('last-modified',''),
            transport='curl_http1.1')


class Links(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.links, self.active = [], None
        self.feed(raw.decode("utf-8", errors="replace"))

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.active = {**dict(attrs), "text": ""}

    def handle_data(self, text):
        if self.active is not None:
            self.active["text"] += text

    def handle_endtag(self, tag):
        if tag == "a" and self.active is not None:
            if self.active.get("href"):
                self.links.append(self.active)
            self.active = None


@dataclass
class Artifact:
    name: str
    url: str
    kind: str
    required: tuple = ()
    date_columns: tuple = ()
    keys: tuple = ()
    filters: dict = field(default_factory=dict)
    role: str = "data"
    note: str = ""


def parse_date(value):
    value = str(value).strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}", value):
        value = value[:10]
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%Y%m%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unrecognized source date: {value!r}")


def iter_csv(raw, required=()):
    import csv
    if b"<html" in raw[:1000].lower() or b"<!doctype html" in raw[:1000].lower():
        raise ValueError("HTML returned instead of data")
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    fields = reader.fieldnames or []
    if not fields or len(fields) != len(set(fields)) or not set(required) <= set(fields):
        raise ValueError(f"Unexpected CSV header; required={required}, received={fields[:20]}")
    def rows():
        count = 0
        for row in reader:
            if None in row or None in row.values():
                raise ValueError("Malformed CSV row")
            count += 1
            yield row
        if not count:
            raise ValueError("Empty CSV")
    return fields, rows()


def read_csv(raw, required=()):
    fields, rows = iter_csv(raw, required)
    return fields, list(rows)


def validate(raw, spec):
    if spec.kind == "csv":
        fields, rows = iter_csv(raw, spec.required)
        return {"columns": fields}, (fields, rows)
    if spec.kind == "json":
        obj = json.loads(raw)
        if not obj or (isinstance(obj, dict) and (obj.get("error") or obj.get("error_code"))):
            raise ValueError("Empty/error JSON")
        return {"validation": "json"}, None
    if spec.kind in {"zip", "xlsx"}:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            infos = archive.infolist()
            if not infos or sum(i.file_size for i in infos) > 1_000_000_000:
                raise ValueError("Empty or oversized archive")
            if archive.testzip() is not None:
                raise ValueError("Corrupt archive member")
            if spec.kind == "xlsx" and "xl/workbook.xml" not in archive.namelist():
                raise ValueError("Not an Excel workbook")
        return {"validation": spec.kind, "members": len(infos),
                "dates": "not_extracted"}, None
    if spec.kind == "xls":
        # Some publishers use .xls names for OOXML; accept either real format.
        if raw.startswith(b"PK"):
            return validate(raw, Artifact(spec.name, spec.url, "xlsx"))
        if not raw.startswith(bytes.fromhex("d0cf11e0a1b11ae1")):
            raise ValueError("Not a binary Excel workbook")
        return {"validation": "xls_magic", "dates": "not_extracted"}, None
    if spec.kind == "pdf":
        if not raw.startswith(b"%PDF-") or b"%%EOF" not in raw[-8192:]:
            raise ValueError("Incomplete or non-PDF response")
        return {"validation": "pdf_envelope", "dates": "not_extracted"}, None
    if spec.kind == "html":
        if not any(v in raw[:5000].lower() for v in [b"<html", b"<!doctype html"]):
            raise ValueError("Not an HTML page")
        if any(v in raw[:15000].lower() for v in [b"just a moment...", b"access denied", b"verify you are human"]):
            raise ValueError("Publisher challenge page, not source content")
        return {"validation": "html", "dates": "not_extracted"}, None
    raise ValueError(f"Unsupported data format: {spec.kind}")


def add_index(index, row, keys):
    hashed = digest(json.dumps(row, sort_keys=True).encode())
    key = json.dumps([row.get(c, "") for c in keys]) if keys else hashed
    index.setdefault(key, []).append(hashed)


def compare_indices(a, b, keys):
    added, removed = sorted(b.keys() - a.keys()), sorted(a.keys() - b.keys())
    revised = sorted(k for k in a.keys() & b.keys() if sorted(a[k]) != sorted(b[k]))
    return {"key_columns": list(keys), "comparison": "grouped_keys" if keys else "row_multiset",
            "added": added, "removed": removed, "revised": revised,
            "counts": {"added": len(added), "removed": len(removed), "revised": len(revised)}}


def row_changes(old, new, keys):
    """Compare multisets per source key; retain question versions and duplicates."""
    a, b = {}, {}
    for row in old:
        add_index(a, row, keys)
    for row in new:
        add_index(b, row, keys)
    return compare_indices(a, b, keys)


class Collector:
    def __init__(self, snap, args):
        self.snap, self.args = snap, args
        self.report, self.diffs = {}, {}
        self.cache = {}

    def get(self, url):
        if url not in self.cache:
            self.cache[url] = request_bytes(url, self.args.timeout)
        return self.cache[url]

    def page(self, url, name):
        spec = Artifact(name, url, "html", role="discovery")
        raw, meta = self.get(url)
        validate(raw, spec)
        self.snap.add("discovery/" + name, raw, **meta, role="discovery")
        return Links(raw).links

    def add(self, spec, supplied=None):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", spec.name):
            raise ValueError("Invalid artifact filename")
        raw, meta = self.get(spec.url) if supplied is None else supplied
        info, parsed = validate(raw, spec)
        name = "raw/" + spec.name
        self.snap.add(name, raw, **meta, role=spec.role, source_note=spec.note)
        info.update({"role": spec.role, "note": spec.note,
                     "availability_certified": False})
        if parsed is not None:
            fields, all_rows = parsed
            selected, dates, index = [], [], {}
            count = 0
            if not set(spec.filters) <= set(fields):
                raise ValueError(f"Missing geographic/filter columns: {list(spec.filters)}")
            if spec.date_columns:
                if not set(spec.date_columns) <= set(fields):
                    raise ValueError(f"Missing date columns: {spec.date_columns}")
            start = date(self.args.start_year, 1, 1)
            end = date(self.args.year, 1, 1)
            for r in all_rows:
                count += 1
                add_index(index, r, spec.keys)
                if not all(r[k] in values for k, values in spec.filters.items()):
                    continue
                if spec.date_columns:
                    values = [r[c] for c in spec.date_columns]
                    if len(values) > 1:
                        parts = [int(float(v)) for v in values]
                        dt = date(*(parts + [1] if len(parts) == 2 else parts))
                    else:
                        dt = parse_date(values[0])
                    dates.append(dt)
                    eligible = (start <= dt < end if self.args.mode == "historical" else
                                dt.year == self.args.year and dt <= date.today())
                    if not eligible:
                        continue
                selected.append(r)
            info["rows"] = count
            if spec.date_columns:
                info.update({"first_source_date": min(dates).isoformat() if dates else None,
                             "last_source_date": max(dates).isoformat() if dates else None,
                             "current_year_rows": sum(d.year == self.args.year and d <= date.today() for d in dates),
                             "future_dated_source_rows": sum(d > date.today() for d in dates),
                             "date_scope": "explicit_year_filter",
                             "freshness": "has_current_year_rows" if any(d.year == self.args.year and d <= date.today() for d in dates)
                             else "no_current_year_observations"})
            else:
                info["date_scope"] = "full_file_dates_not_extracted"
            table_name = "tables/" + Path(spec.name).stem + ".csv"
            self.snap.add(table_name, csv_bytes(fields, selected), role="source_units_extract")
            info["selected_rows"] = len(selected)
            # Compare full source, not only current-year extract: catch historical revisions.
            old_index = {}
            if self.snap.previous and (self.snap.previous[0] / name).exists():
                old_fields, old = iter_csv((self.snap.previous[0] / name).read_bytes())
                if old_fields != fields:
                    raise ValueError(f"Schema changed for {spec.name}; previous snapshot preserved")
                for row in old:
                    add_index(old_index, row, spec.keys)
            self.diffs[spec.name] = compare_indices(old_index, index, spec.keys)
        else:
            old_info = self.snap.previous[1]["files"].get(name) if self.snap.previous else None
            self.diffs[spec.name] = {"comparison": "file_hash", "changed": old_info is None or old_info["sha256"] != digest(raw)}
        self.report[spec.name] = info
        return raw


def run_source(source, args):
    from feature_sources import SOURCES, collect_source
    spec = SOURCES[source]
    root = args.output_dir / source / f"{args.mode}_{args.year}"
    # Source-specific scope affects cache identity; reject mismatched cached requests.
    request = {"source": source, "mode": args.mode, "year": args.year,
               "start_year": args.start_year, "vintage": args.vintage,
               "series": args.series, "document_urls": [public_url(u) for u in args.document_url],
               "input_files": {str(p.resolve()): digest(p.read_bytes()) for p in args.input_file},
               "version": VERSION}
    existing = latest(root)
    if args.mode == "historical" and not args.refresh and existing:
        previous_request = json.loads((existing[0] / "request.json").read_text())
        if previous_request == request:
            print(f"Verified historical cache: {source}: {existing[0]}")
            return {"source": source, "status": "cached", "snapshot": str(existing[0])}
        raise ValueError("Historical request changed; use --refresh or a different output directory")
    if args.mode == "current" and spec.get("historical_only") and not args.input_file and not args.document_url:
        return {"source": source, "status": "historical_only", "reason": spec["note"]}
    with Snapshot(root, "feature_source") as snap:
        collector = Collector(snap, args)
        collect_source(source, collector, args)
        if not any(v["role"] == "data" for v in collector.report.values()):
            raise ValueError("No data artifacts; discovery pages alone are not a completed download")
        snap.write_json("request.json", request)
        snap.write_json("source.json", spec)
        summary = {"source": source, "mode": args.mode, "year": args.year,
                   "artifacts": collector.report, "model_ready": False,
                   "raw_scope": "Full upstream files retained unless source API parameters say otherwise",
                   "historical_vintage": args.vintage or "latest-revised; historical availability unverified",
                   "warning": "Year filtering is not a release-date/as-of join. Raw files may span many years."}
        snap.write_json("summary.json", summary)
        path = snap.finish({"source": source, "mode": args.mode, "year": args.year,
                            "artifact_count": len(collector.report), "model_ready": False,
                            "details": "summary.json"}, {"artifacts": collector.diffs})
        return {"source": source, "status": "saved_or_unchanged", "snapshot": str(path),
                "artifacts": len(collector.report)}


def main(source=None, mode=None):
    from feature_sources import SOURCES
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["historical", "current"], default=mode or "current")
    parser.add_argument("--year", type=int, default=date.today().year)
    parser.add_argument("--start-year", type=int, default=1976)
    parser.add_argument("--sources", nargs="+", choices=sorted(SOURCES), default=[source] if source else None)
    parser.add_argument("--list-sources", action="store_true")
    parser.add_argument("--refresh", action="store_true", help="Recheck cached historical files; current mode always rechecks")
    parser.add_argument("--output-dir", type=Path, default=LAB / "data/features")
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--series", nargs="+", help="Override FRED-family series IDs")
    parser.add_argument("--vintage", help="FRED-family dated vintage; requires FRED_API_KEY; no silent fallback")
    parser.add_argument("--document-url", action="append", default=[], help="Explicit publisher export/report URL (repeatable)")
    parser.add_argument("--input-file", action="append", type=Path, default=[], help="Import a legitimately obtained export (repeatable)")
    args = parser.parse_args()
    if args.list_sources:
        for name, spec in SOURCES.items():
            print(f"{name:20} {spec['access']:18} {spec['note']}")
        return 0
    if not 1900 <= args.start_year < args.year <= date.today().year or args.timeout <= 0:
        parser.error("Require 1900 <= start-year < year <= current year and a positive timeout")
    # Alternative mirrors are selectable, but do not repeatedly download the
    # same FRED values or make a public batch fail for subscriptions not configured.
    names = args.sources or [n for n, s in SOURCES.items()
                            if s["access"] == "public" and n not in {"bea"}
                            and not (n == "yougov" and args.mode == "historical")]
    if source and names != [source]:
        parser.error("Use the batch entry point to select different sources")
    if (args.series or args.vintage or args.document_url or args.input_file) and len(names) != 1:
        parser.error("Series, vintage, document and import overrides require exactly one source")
    if args.vintage:
        try:
            vintage = date.fromisoformat(args.vintage)
        except ValueError:
            parser.error("Vintage must be YYYY-MM-DD")
        if vintage > date.today():
            parser.error("Vintage cannot be in the future")
        if names[0] not in {"fred", "bls", "bea", "oecd"}:
            parser.error("--vintage is supported only by FRED-family downloaders")
    results = []
    for name in names:
        print(f"Downloading {name} ({args.mode}, reference year {args.year})", flush=True)
        try:
            results.append(run_source(name, args))
        except NeedsAccess as exc:
            results.append({"source": name, "status": "needs_access", "reason": str(exc)})
            print(f"Access needed: {name}: {exc}", flush=True)
        except Exception as exc:
            # Do not print tracebacks/URLs containing credentials supplied by a provider.
            message = str(exc)
            for key in (os.environ.get("FRED_API_KEY"),):
                if key:
                    message = message.replace(key, "REDACTED")
            results.append({"source": name, "status": "failed", "reason": message})
            print(f"Failed (previous snapshot preserved): {name}: {message}", flush=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    report = {"checked_at": utc_now(), "mode": args.mode, "year": args.year, "results": results}
    reports = args.output_dir / "runs"
    reports.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S.%f")
    atomic_json(reports / f"{stamp}_{args.mode}.json", report)
    print(json.dumps(report, indent=2))
    return 1 if any(r["status"] in {"failed", "needs_access"} for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
