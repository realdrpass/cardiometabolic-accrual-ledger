#!/usr/bin/env python3
"""Step 1: download every candidate trial record from ClinicalTrials.gov.

Plain-language note: this script asks the government trial registry for every
trial that might belong in the ledger and saves the answers exactly as received.
It casts a deliberately wide net (broad disease search terms). The precise
inclusion rules are applied later, in 02_build.py, so they can be read and
changed in one place. You do not need to open this file.

Output: data/raw/ctgov_studies.jsonl  (one JSON study record per line)
        data/raw/ctgov_studies.jsonl.gz (compressed copy committed to the repository)
        data/raw/query.json            (the exact query sent, for reproducibility)
        data/raw/PROVENANCE.txt        (file hash, URL, access date)

Run:  python code/01_fetch.py
"""
import gzip
import json
import shutil
import pathlib
import subprocess
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
API = "https://clinicaltrials.gov/api/v2/studies"

# Wide condition net. Exact include/exclude rules live in 02_build.py.
COND = (
    "diabetes OR obesity OR overweight OR hypertension OR preeclampsia OR "
    "\"heart failure\" OR dyslipidemia OR hypercholesterolemia OR hyperlipidemia OR "
    "hypertriglyceridemia OR hyperlipoproteinemia"
)
# Structural inclusion criteria from the build spec.
ADVANCED = (
    "AREA[StudyType]INTERVENTIONAL"
    " AND AREA[Phase](PHASE2 OR PHASE3 OR PHASE4)"
    " AND AREA[InterventionType]DRUG"
    " AND AREA[StudyFirstPostDate]RANGE[2008-01-01,2025-12-31]"
    " AND AREA[LocationCountry]\"United States\""
)
FIELDS = "protocolSection,derivedSection,hasResults"
PAGE = 1000


def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return json.load(r)
        except Exception as e:  # network hiccup: back off and retry
            print(f"  retry {attempt + 1}: {e}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    raise SystemExit("ClinicalTrials.gov did not respond after 5 tries.")


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    params = {"query.cond": COND, "filter.advanced": ADVANCED, "fields": FIELDS,
              "pageSize": PAGE, "countTotal": "true", "format": "json"}
    (RAW / "query.json").write_text(json.dumps({"endpoint": API, **params}, indent=2))

    out = RAW / "ctgov_studies.jsonl"
    n, total, token = 0, None, None
    with out.open("w") as f:
        while True:
            p = dict(params)
            if token:
                p["pageToken"] = token
                p.pop("countTotal", None)
            data = get(p)
            total = data.get("totalCount", total)
            for s in data.get("studies", []):
                f.write(json.dumps(s, separators=(",", ":")) + "\n")
                n += 1
            print(f"  fetched {n} of {total}")
            token = data.get("nextPageToken")
            if not token:
                break
            time.sleep(0.5)

    if total is not None and n != total:
        raise SystemExit(f"Count mismatch: registry said {total}, saved {n}.")
    with out.open("rb") as src, gzip.GzipFile(RAW / "ctgov_studies.jsonl.gz", "wb", mtime=0) as dst:
        shutil.copyfileobj(src, dst)
    for fpath in (out, RAW / "query.json"):
        subprocess.run([sys.executable, str(ROOT / "code" / "provenance.py"), str(fpath),
                        API + " (paged query; parameters in query.json)",
                        "--log", str(RAW / "PROVENANCE.txt"),
                        "--note", f"{n} studies; registry totalCount={total}"], check=True)
    print(f"Saved {n} study records to {out}")


if __name__ == "__main__":
    main()
