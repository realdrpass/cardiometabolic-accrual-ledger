"""Read the raw registry download, compressed or not.

Plain-language note: the repository ships the 13 October 2026 download as
data/raw/ctgov_studies.jsonl.gz. Its uncompressed contents match the SHA-256
fingerprint in data/raw/PROVENANCE.txt. Scripts read the uncompressed file if
present, otherwise the compressed one. You do not need to open this file.
"""
import gzip
import pathlib

RAW_DIR = pathlib.Path(__file__).resolve().parents[1] / "data" / "raw"
PLAIN = RAW_DIR / "ctgov_studies.jsonl"
GZ = RAW_DIR / "ctgov_studies.jsonl.gz"


def raw_lines():
    if PLAIN.exists():
        return PLAIN.open(encoding="utf-8")
    return gzip.open(GZ, "rt", encoding="utf-8")
