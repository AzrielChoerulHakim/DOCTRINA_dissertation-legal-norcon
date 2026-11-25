#!/usr/bin/env python3
"""CI-only integration experiment on TWO public, original PDF documents.

Downloads into a TEMP DIRECTORY, never committed. Re-verifies SHA-256, PDF page
and original text anchor with verify_sources.py. Discover-stage hashes are not
cryptographically trusted pins until reviewed and recorded in repository.
"""
from __future__ import annotations
import argparse
import json
import urllib.request
from datetime import date
from pathlib import Path

from verify_sources import verify_source

PUBLIC_CASES = [
    {
        "source_id": "OXFORD_DPHIL_LIAU_2020",
        "source_kind": "thesis_pdf",
        "repository_url": "https://ora.ox.ac.uk/objects/uuid:f2acd5c9-7173-43a3-bd86-3b1019409d1b",
        "download_url": "https://ora.ox.ac.uk/objects/uuid:f2acd5c9-7173-43a3-bd86-3b1019409d1b/files/dxp68kg308",
        "local_path": "lia u-2020.pdf".replace(" ", ""),
        "anchor_text": "STANDING IN PRIVATE LAW",
        "publication_year": 2020,
        "edition": "Oxford open repository thesis deposit",
        "extraction_method": "pypdf",
        "printed_page": "title",
    },
    {
        "source_id": "EWCA_GULATI_2015",
        "source_kind": "legal_pdf",
        "repository_url": "https://www.judiciary.uk/wp-content/uploads/2015/12/representative-claimants-v-mgn.pdf",
        "download_url": "https://www.judiciary.uk/wp-content/uploads/2015/12/representative-claimants-v-mgn.pdf",
        "local_path": "gulati-2015.pdf",
        "anchor_text": "Neutral Citation Number: [2015] EWCA Civ 1291",
        "publication_year": 2015,
        "edition": "Court of Appeal judgment 17 December 2015",
        "jurisdiction": "England and Wales",
        "applicability_date": "2015-12-17",
        "extraction_method": "pypdf",
        "printed_page": "1",
    },
]


def download_public(url: str, out: Path) -> None:
    req = urllib.request.Request(url, headers={
        "User-Agent": "DOCTRINA-Research-Verification/0.4.1 (public-original-document-integrity)",
        "Accept": "application/pdf",
    })
    out.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with urllib.request.urlopen(req, timeout=45) as response, out.open("wb") as fh:
        while True:
            chunk = response.read(65536)
            if not chunk:
                break
            total += len(chunk)
            if total > 35 * 1024 * 1024:
                raise ValueError("PUBLIC_PDF_TOO_LARGE (35 MB limit)")
            fh.write(chunk)
    if out.stat().st_size < 500:
        raise ValueError("PDF_TOO_SMALL / possible HTML error page")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    work = args.out_dir
    originals = work / "private-original-bytes"
    originals.mkdir(parents=True, exist_ok=True)
    reports = []
    proposed_pins = []
    for item in PUBLIC_CASES:
        case = dict(item)
        case["retrieved_at"] = date.today().isoformat()
        original = originals / case["local_path"]
        try:
            download_public(case["download_url"], original)
            first = verify_source({**case, "page_index": None}, originals)
            pages = first.get("discovered_page_indices", [])
            proposed = {**case, "page_index": pages[0] if len(pages) == 1 else None,
                        "content_sha256": first["sha256_actual"]}
            check = verify_source(proposed, originals) if proposed["page_index"] is not None else first
            check["preliminary_unpinned_discovery"] = True
            check["proposed_hash_pin"] = first["sha256_actual"]
            check["original_pdf_size_bytes"] = original.stat().st_size
            proposed_pins.append(proposed)
        except Exception as exc:
            check = {"source_id": case["source_id"], "state": "UNVERIFIED",
                     "error": type(exc).__name__ + ": " + str(exc)[:220],
                     "preliminary_unpinned_discovery": True}
        reports.append(check)
        print(case["source_id"], check.get("state"), check.get("page_index_verified"),
              check.get("sha256_actual"), check.get("error", ""))
    (work / "source-discovery-report.json").write_text(
        json.dumps({"status": "PRELIMINARY_ONLY_NOT_PRE-PINNED",
                    "results": reports}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    (work / "proposed-source-pins.json").write_text(
        json.dumps({"sources": proposed_pins}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    # Never upload original bytes as a workflow artifact.
    return 0 if all(x.get("state") in {"VERIFIED_EXACT", "VERIFIED_NORMALIZED"} for x in reports) else 2


if __name__ == "__main__":
    raise SystemExit(main())
