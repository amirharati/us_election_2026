"""Publisher-specific discovery and download adapters.

Registry includes alternative providers. Access-dependent sources accept explicit
public report URLs or authorized local exports; they never manufacture data.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit, parse_qs, urlencode

from data_utils import csv_bytes, utc_now
from feature_download import Artifact, Links, NeedsAccess


def source(url, features, note, access="public", historical_only=False):
    return dict(url=url, feature_ids=features.split(), note=note, access=access,
                historical_only=historical_only,
                terms="See publisher/source links; public access does not imply unrestricted redistribution.")


SOURCES = {
    "fred": source("https://fred.stlouisfed.org/", "F03 F04 F05 F06 F09 F10", "BLS/BEA/Nasdaq/Fed series through FRED; optional API vintages."),
    "bls": source("https://www.bls.gov/developers/", "F03 F05", "Direct BLS monthly CPI/unemployment JSON; optional native series IDs; ten-year API chunks."),
    "bea": source("https://www.bea.gov/data/income-saving/disposable-personal-income", "F04 F06", "BEA real per-capita income/GDP/PCE prices via FRED distribution."),
    "oecd": source("https://fred.stlouisfed.org/series/USACSCICP02STSAM", "F01", "OECD standardized US confidence via FRED; not an independent extra survey."),
    "michigan": source("https://data.sca.isr.umich.edu/tables.php", "F01 F02", "Discover current signed Excel table links; retain historical tables and source period."),
    "ucsb": source("https://www.presidency.ucsb.edu/statistics/data/presidential-job-approval-all-data", "F07 F08", "President-specific approval tables; preserve source/party/methodology notes."),
    "silver_bulletin": source("https://www.natesilver.net/p/trump-approval-ratings-nate-silver-bulletin", "F07", "Discover published raw approval CSV; history only as far as publisher supplies."),
    "fivethirtyeight": source("https://github.com/fivethirtyeight/data/blob/master/trump-approval-ratings/README.md", "F07", "Legacy raw approval archive: provide a verified archived CSV URL/export; no current feed.", "export_or_url", historical_only=True),
    "cboe": source("https://www.cboe.com/tradable_products/vix/vix_historical_data", "F10", "VIX spot OHLC daily history, refreshed in full."),
    "french": source("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html", "F09", "Daily and monthly market factor ZIPs; 2025 method transition."),
    "gpr": source("https://www.matteoiacoviello.com/gpr.htm", "F11", "Monthly and daily Excel files, with historical constructions retained."),
    "epu": source("https://www.policyuncertainty.com/us_monthly.html", "F15", "Monthly/categorical Excel plus daily news index CSV."),
    "infectious_emv": source("https://www.policyuncertainty.com/infectious_EMV.html", "F13", "Daily infectious-disease news/market stress proxy, not mortality."),
    "cdc": source("https://data.cdc.gov/National-Center-for-Health-Statistics/Excess-Deaths-Associated-with-COVID-19/xkkf-xrst", "F13", "Excess-deaths CSV and portal metadata; old product may be stale in current mode."),
    "cdc_nhsn": source("https://www.cdc.gov/nhsn/psc/hospital-respiratory-dashboard.html", "F13", "CDC historical/current HRD exports plus metadata; reporting regimes remain distinct."),
    "who": source("https://data.who.int/dashboards/covid19/data", "F13", "Weekly COVID cases/deaths; full raw global file, US extract."),
    "owid": source("https://docs.owid.io/projects/etl/api/covid/", "F13", "Current compact COVID catalog CSV and metadata; US extract."),
    "oxcgrt": source("https://github.com/OxCGRT/covid-policy-dataset", "F14", "Final 2020–2022 national/subnational policy archive; no 2026 feed.", historical_only=True),
    "ucdp": source("https://ucdp.uu.se/downloads/", "F11", "Historical annual GED ZIP or latest current-year monthly candidate CSV."),
    "policy_agendas": source("https://www.maxwell.syr.edu/research/article/gallup-s-most-important-problem", "F12", "Coded Gallup MIP historical CSV and codebook; year coverage audited from file."),
    "yougov": source("https://yougov.com/en-us/content/the-economist", "F02 F07 F08 F12", "Current archive report PDFs; historical reports require explicit URLs."),
    "ipsos": source("https://www.ipsos.com/en-us/latest-us-opinion-polls", "F02 F07 F08 F12", "Explicit original topline/crosstab URLs; archive search is not a complete dataset.", "export_or_url"),
    "ap_norc": source("https://apnorc.org/projects/", "F02 F07 F08 F12", "Explicit original topline/crosstab URLs.", "export_or_url"),
    "gallup": source("https://news.gallup.com/interactives/507569/presidential-job-approval-center.aspx", "F01 F07 F08 F12", "Authorized export or public trend/report URL; bulk approval export needs access.", "export_or_url"),
    "conference_board": source("https://www.conference-board.org/data", "F01", "Authorized historical/current export; no subscription is purchased.", "export_or_url"),
    "roper": source("https://ropercenter.cornell.edu/ipoll/", "F07 F08 F12", "Authorized survey export; institutional access may be required.", "export_or_url"),
    "gtd": source("https://www.start.umd.edu/data-tools/GTD", "F11", "Form/licensed export needed; public overview covers 1970–2020.", "export_or_url"),
    "acled": source("https://acleddata.com/methodology/united-states-scope-and-coverage-acled-data", "F14", "Authorized CSV export or download URL; access entitlement required.", "export_or_url"),
    "congress": source("https://github.com/unitedstates/congress-legislators", "incumbency", "Historical/current legislators JSON; officeholding is not running-incumbent status."),
}

FRED_SERIES = {
    "fred": ["CPIAUCSL", "CUSR0000SETB01", "A229RX0", "UNRATE", "GDPC1", "NASDAQCOM", "STLFSI4"],
    "bls": ["CPIAUCSL", "UNRATE"],
    "bea": ["A229RX0", "GDPC1", "PCEPI"],
    "oecd": ["USACSCICP02STSAM"],
}


def explicit_exports(c, args):
    """Archive actual reports/exports; do not call an index page a data export."""
    for i, url in enumerate(args.document_url):
        suffix = Path(urlsplit(url).path).suffix.lower().lstrip(".")
        if "output=csv" in url:
            suffix = "csv"
        if suffix not in {"csv", "json", "xlsx", "xls", "pdf", "zip"}:
            raise ValueError("Explicit document URL must identify CSV/JSON/Excel/PDF/ZIP")
        c.add(Artifact(f"export_{i:03d}.{suffix}", url, suffix,
                       note="Explicit publisher export; date coverage and survey meaning require preparation."))
    for i, path in enumerate(args.input_file):
        suffix = path.suffix.lower().lstrip(".")
        c.add(Artifact(f"import_{i:03d}.{suffix}", "", suffix,
                       note="User-provided authorized export; original public release date unverified."),
              (path.read_bytes(), {"local_source": str(path.resolve()), "retrieved_at": utc_now()}))


def fred(c, args, provider):
    for series in args.series or FRED_SERIES[provider]:
        if not re.fullmatch(r"[A-Za-z0-9_]+", series):
            raise ValueError("Invalid FRED series identifier")
        if args.vintage:
            key = os.environ.get("FRED_API_KEY")
            if not key:
                raise NeedsAccess("Set FRED_API_KEY for historical-vintage downloads; latest values are not a substitute.")
            params = dict(series_id=series, api_key=key, file_type="json",
                          realtime_start=args.vintage, realtime_end=args.vintage,
                          observation_start=f"{args.start_year}-01-01", limit=100000)
            url = "https://api.stlouisfed.org/fred/series/observations?" + urlencode(params)
            raw = c.add(Artifact(series + ".json", url, "json"))
            obj = json.loads(raw)
            rows = obj["observations"]
            if len(rows) != obj["count"]:
                raise ValueError("FRED response was paginated/truncated")
            data = csv_bytes(["date", "value", "realtime_start", "realtime_end"], rows)
            c.add(Artifact(series + ".csv", "", "csv", ("date", "value"), ("date",), ("date",)),
                  (data, {"derived_from": series + ".json", "requested_vintage": args.vintage}))
        else:
            url = "https://fred.stlouisfed.org/graph/fredgraph.csv?" + urlencode({"id": series})
            from feature_download import read_csv, request_fred_csv
            raw, meta = request_fred_csv(url, args.timeout)
            fields, _ = read_csv(raw)
            dt = "observation_date" if "observation_date" in fields else "DATE"
            c.add(Artifact(series + ".csv", url, "csv", (dt, series), (dt,), (dt,),
                           note="Latest-revised FRED distribution; upstream source units retained; no vintage certification."), (raw, meta))


def bls(c, args):
    # Anonymous BLS API supports at most ten years per request. Current refreshes
    # include two prior calendar years; --start-year controls historical coverage.
    start = args.start_year if args.mode == "historical" else max(args.start_year, args.year - 2)
    end = args.year - 1 if args.mode == "historical" else args.year
    for series in args.series or ["CUSR0000SA0", "LNS14000000"]:
        if not re.fullmatch(r"[A-Za-z0-9]+", series):
            raise ValueError("Invalid BLS native series identifier")
        rows = []
        for first in range(start, end + 1, 10):
            last = min(first + 9, end)
            url = f"https://api.bls.gov/publicAPI/v2/timeseries/data/{series}?" + urlencode({"startyear": first, "endyear": last})
            raw = c.add(Artifact(f"{series}_{first}_{last}.json", url, "json"))
            obj = json.loads(raw)
            if obj.get("status") != "REQUEST_SUCCEEDED":
                raise RuntimeError("BLS API rejected request: " + str(obj.get("message")))
            datasets = obj.get("Results", {}).get("series", [])
            if len(datasets) != 1 or datasets[0].get("seriesID") != series:
                raise ValueError("BLS returned unexpected series")
            data = datasets[0].get("data", [])
            if not data:
                raise ValueError(f"BLS returned no observations for {series}, {first}–{last}")
            for row in data:
                if not first <= int(row["year"]) <= last:
                    raise ValueError("BLS ignored requested year range")
                if row["period"] == "M13":
                    continue  # Annual averages remain in raw JSON, not monthly table.
                if not re.fullmatch(r"M(0[1-9]|1[0-2])", row["period"]):
                    raise ValueError("Only monthly BLS series supported")
                rows.append({"date": f"{row['year']}-{row['period'][1:]}-01",
                             "series_id": series, "value": row["value"],
                             "footnotes": json.dumps(row.get("footnotes", []), sort_keys=True)})
        rows.sort(key=lambda row: row["date"])
        c.add(Artifact(series + ".csv", "", "csv", ("date", "value"), ("date",), ("series_id", "date"),
                       note=f"Direct BLS API, requested {start}–{end}; current refresh revisits two prior years; source units retained."),
              (csv_bytes(["date", "series_id", "value", "footnotes"], rows), {"derived_from": "BLS JSON chunks"}))


def michigan(c, args):
    base = SOURCES["michigan"]["url"]
    links = c.page(base, "michigan_tables.html")
    wanted = {"1a", "1b", "5b", "6", "8", "10"}
    found = set()
    for link in links:
        params = parse_qs(urlsplit(link["href"]).query)
        category, number = params.get("c", [""])[0], params.get("n", [""])[0]
        if params.get("f") == ["xls"] and number in wanted and category in {"YB", "RB"}:
            # YB=current monthly table; RB=historical table. Always retain both,
            # since current tables can carry short histories and lag the headline.
            c.add(Artifact(f"{category}_{number}.xls", urljoin(base, link["href"]), "xls",
                           note=f"Publisher table c={category}, n={number}, y={params.get('y')}, m={params.get('m')}; dates not parsed."))
            found.add((category, number))
    if len(found) != 12:
        raise ValueError(f"Michigan table inventory changed: found {sorted(found)}")


def ucsb(c, args):
    base = SOURCES["ucsb"]["url"]
    links = c.page(base, "approval_index.html")
    urls = sorted({urljoin(base, a["href"]) for a in links if re.search(r"/[^/]+public-approval$", a["href"])})
    if args.mode == "current":
        # Discover the currently listed administration, not a hard-coded name.
        urls = list(dict.fromkeys(urljoin(base, a["href"]) for a in links
                                 if re.search(r"/[^/]+public-approval$", a["href"])))[:1]
    if not urls:
        raise ValueError("No presidential approval tables discovered")
    for url in urls:
        raw = c.add(Artifact(url.rsplit("/", 1)[-1] + ".html", url, "html",
                             note="Source table plus methodological/interpolation notes; no numerical normalization yet."))
        if b"<table" not in raw.lower() or b"approv" not in raw.lower():
            raise ValueError("Expected an approval data table")


def silver(c, args):
    base = SOURCES["silver_bulletin"]["url"]
    links = c.page(base, "approval_tracker.html")
    matches = {urljoin(base, a["href"]) for a in links
               if "docs.google.com/spreadsheets/" in a["href"] and "download" in a["text"].lower()}
    if len(matches) != 1:
        raise ValueError("Expected one publisher-linked approval CSV")
    c.add(Artifact("approval_polls.csv", matches.pop(), "csv",
                   ("pollster", "startdate", "enddate"), ("enddate",), ("poll_id",),
                   note="Raw poll versions, including potentially overlapping populations/questions."))


def ucdp(c, args):
    base = SOURCES["ucdp"]["url"]
    links = c.page(base, "ucdp_downloads.html")
    if args.mode == "historical":
        matches = {a["href"] for a in links if re.search(r"/ged/ged\d+-csv\.zip$", a["href"], re.I)}
        if len(matches) != 1:
            raise ValueError("Expected one annual GED CSV archive")
        c.add(Artifact("ged_historical.zip", urljoin(base, matches.pop()), "zip",
                       note="Full latest annual release; includes revised older years, not historical as-of vintages."))
    else:
        matches = []
        for a in links:
            match = re.search(r"/candidateged/GEDEvent_v(\d+)_0_(\d+)\.csv$", a["href"], re.I)
            if match and int(match[1]) == args.year % 100:
                matches.append((int(match[2]), a["href"]))
        if not matches:
            raise ValueError("No monthly candidate release for requested year")
        url = urljoin(base, max(matches)[1])
        c.add(Artifact("ged_candidate.csv", url, "csv", ("id", "date_start", "date_end"),
                       ("date_end",), ("id",), note="Latest monthly release only; earlier monthly files collected below."))
        # Candidate monthly releases are monthly slices, not guaranteed cumulative.
        # Fetch every current-year monthly release from the publisher's archive.
        archive = "https://ucdp.uu.se/downloads/olddw.html"
        for a in c.page(archive, "ucdp_old_versions.html"):
            match = re.search(r"GEDEvent_v(\d+)_0_(\d+)\.csv$", a["href"], re.I)
            if match and int(match[1]) == args.year % 100 and int(match[2]) < max(matches)[0]:
                name = f"ged_candidate_{int(match[2]):02d}.csv"
                if name in c.report:
                    continue
                c.add(Artifact(name, urljoin(archive, a["href"]), "csv",
                               ("id", "date_start", "date_end"), ("date_end",), ("id",),
                               note="Monthly candidate slice; cross-release event deduplication remains a preparation step."))


def collect_source(name, c, args):
    if args.input_file or args.document_url:
        explicit_exports(c, args)
        return
    if SOURCES[name]["access"] == "export_or_url":
        raise NeedsAccess("Use --input-file with an authorized export or --document-url for a public report; " + SOURCES[name]["url"])
    if name == "bls":
        if args.vintage:
            raise NeedsAccess("Direct BLS API returns latest revisions; use the FRED adapter with --vintage and FRED_API_KEY.")
        return bls(c, args)
    if name in FRED_SERIES:
        return fred(c, args, name)
    if name == "michigan":
        return michigan(c, args)
    if name == "ucsb":
        return ucsb(c, args)
    if name == "silver_bulletin":
        return silver(c, args)
    if name == "cboe":
        c.add(Artifact("vix.csv", "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv",
                       "csv", ("DATE", "OPEN", "HIGH", "LOW", "CLOSE"), ("DATE",), ("DATE",)))
    elif name == "french":
        for suffix in ["", "_daily"]:
            c.add(Artifact("ff_factors" + suffix + ".zip", "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors" + suffix + "_CSV.zip", "zip",
                           note="Original factor CSV archive; preamble, multiple sections and percent units require dedicated preparation."))
    elif name == "gpr":
        for stem in ["data_gpr_export", "data_gpr_daily_recent"]:
            c.add(Artifact(stem + ".xls", "https://www.matteoiacoviello.com/gpr_files/" + stem + ".xls", "xls"))
    elif name == "epu":
        for stem in ["US_Policy_Uncertainty_Data", "Categorical_EPU_Data"]:
            c.add(Artifact(stem + ".xlsx", "https://www.policyuncertainty.com/media/" + stem + ".xlsx", "xlsx"))
        c.add(Artifact("daily_epu.csv", "https://www.policyuncertainty.com/media/All_Daily_Policy_Data.csv", "csv",
                       ("year", "month", "day"), ("year", "month", "day"), ("year", "month", "day")))
    elif name == "infectious_emv":
        c.add(Artifact("infectious_emv.csv", "https://www.policyuncertainty.com/media/All_Infectious_EMV_Data.csv", "csv",
                       ("year", "month", "day", "daily_infect_emv_index"), ("year", "month", "day"), ("year", "month", "day")))
    elif name == "cdc":
        c.add(Artifact("excess_deaths_metadata.json", "https://data.cdc.gov/api/views/xkkf-xrst.json", "json", role="metadata"))
        c.add(Artifact("excess_deaths.csv", "https://data.cdc.gov/api/views/xkkf-xrst/rows.csv?accessType=DOWNLOAD", "csv",
                       ("Week Ending Date", "State", "Observed Number"), ("Week Ending Date",),
                       ("Week Ending Date", "State", "Type", "Outcome"),
                       note="Full export avoids Socrata page truncation; inspect latest date rather than assuming current surveillance."))
    elif name == "cdc_nhsn":
        # Both are publisher exports; current HRD does not replace the older
        # reporting regime. Preserve files separately even when dates overlap.
        datasets = ["rhwp-grxi", "ua7e-t2fy"] if args.mode == "historical" else ["ua7e-t2fy"]
        for dataset in datasets:
            c.add(Artifact(f"{dataset}_metadata.json", f"https://data.cdc.gov/api/views/{dataset}.json", "json", role="metadata"))
            c.add(Artifact(f"{dataset}.csv", f"https://data.cdc.gov/api/views/{dataset}/rows.csv?accessType=DOWNLOAD", "csv",
                           ("Week Ending Date", "Geographic aggregation"), ("Week Ending Date",),
                           ("Week Ending Date", "Geographic aggregation"),
                           note="Wide original metrics; geography/completeness/suppression and reporting-method changes require preparation."))
    elif name == "who":
        c.add(Artifact("who_covid_weekly.csv", "https://srhdpeuwpubsa.blob.core.windows.net/whdh/COVID/WHO-COVID-19-global-data.csv", "csv",
                       ("Date_reported", "Country_code", "New_deaths"), ("Date_reported",), ("Date_reported", "Country_code"),
                       {"Country_code": ["US"]}, note="Raw global file preserved; table filters US; report dates are not release vintages."))
    elif name == "owid":
        base = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact"
        c.add(Artifact("owid_metadata.json", base + ".meta.json", "json", role="metadata"))
        c.add(Artifact("owid_covid.csv", base + ".csv", "csv", ("date", "country"), ("date",), ("country", "date"),
                       {"country": ["United States"]}, note="Current ETL catalog, not the discontinued GitHub CSV."))
    elif name == "oxcgrt":
        for scope in ["national", "subnational"]:
            filename = f"OxCGRT_compact_{scope}_v1.csv"
            c.add(Artifact(filename, "https://raw.githubusercontent.com/OxCGRT/covid-policy-dataset/main/data/" + filename,
                           "csv", ("CountryCode", "Date"), ("Date",),
                           ("CountryCode", "RegionCode", "Jurisdiction", "Date"), {"CountryCode": ["USA"]},
                           note="Frozen 2020–2022 archive; distinctions between vaccinated/unvaccinated policies retained."))
    elif name == "ucdp":
        return ucdp(c, args)
    elif name == "policy_agendas":
        base = SOURCES[name]["url"]
        links = c.page(base, "policy_agendas.html")
        found = []
        for a in links:
            if "Download Dataset" in a["text"] and ".csv" in a["href"]:
                found.append(urljoin(base, a["href"]))
            if "Download Codebook" in a["text"] and ".pdf" in a["href"]:
                c.add(Artifact("mip_codebook.pdf", urljoin(base, a["href"]), "pdf", role="metadata"))
        if len(set(found)) != 1:
            raise ValueError("Expected one MIP CSV")
        c.add(Artifact("mip.csv", found[0], "csv", ("id", "year", "percent", "majortopic"), ("year",), ("id",),
                       note="Annual coded survey proportions. January 1 is only a year key, NOT publication date; full-year values need cutoff review."))
    elif name == "yougov":
        if args.mode == "historical":
            raise NeedsAccess("Supply historical YouGov report URLs with --document-url; current index does not expose a complete historical archive.")
        base = SOURCES[name]["url"]
        links = c.page(base, "yougov_economist.html")
        reports = {a["href"] for a in links if ".pdf" in a["href"] and
                   re.search(r"tables|toplines", a["text"], re.I) and str(args.year) in a["text"]}
        if not reports:
            raise ValueError("No current-year report PDFs found")
        for i, url in enumerate(sorted(reports)):
            c.add(Artifact(f"report_{i:03d}.pdf", url, "pdf", note="Reports visible on current archive page; not complete year coverage."))
    elif name == "congress":
        for scope in ["historical", "current"]:
            c.add(Artifact(f"legislators-{scope}.json", f"https://raw.githubusercontent.com/unitedstates/congress-legislators/gh-pages/legislators-{scope}.json", "json",
                           note="Latest maintained officeholding history; candidacy/ballot status not established."))
    else:
        raise ValueError(f"No adapter for {name}")
