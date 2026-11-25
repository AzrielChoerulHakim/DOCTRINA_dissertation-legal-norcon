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
        "source_id": "EDINBURGH_MCMILLAN_2018",
        "source_kind": "thesis_pdf",
        "repository_url": "https://hdl.handle.net/1842/31550",
        "download_url": "https://era.ed.ac.uk/server/api/core/bitstreams/2e0c8ff5-f9a8-4939-bf8e-4e79ac078f07/content",
        "local_path": "mcmillan-2018.pdf",
        "anchor_text": "The Human Embryo",
        "publication_year": 2018,
        "edition": "University of Edinburgh thesis deposit",
        "extraction_method": "pypdf",
        "printed_page": "title",
    },
    {
        "source_id": "DURHAM_DYRKOLBOTN_2016",
        "source_kind": "thesis_pdf",
        "repository_url": "https://etheses.dur.ac.uk/11559/",
        "download_url": "https://etheses.dur.ac.uk/11559/1/thesis_revised.pdf",
        "local_path": "dyrkolbotn-2016.pdf",
        "anchor_text": "economic development takings",
        "publication_year": 2016,
        "edition": "Durham University thesis deposit",
        "extraction_method": "pypdf",
        "printed_page": "title",
    },
    {
        "source_id": "EDINBURGH_DOWNEY_2017",
        "source_kind": "thesis_pdf",
        "repository_url": "https://hdl.handle.net/1842/25946",
        "download_url": "https://era.ed.ac.uk/bitstream/handle/1842/25946/Downey2017.pdf?sequence=1",
        "local_path": "downey-2017.pdf",
        "anchor_text": "Emerging Legal Concepts",
        "publication_year": 2017,
        "edition": "University of Edinburgh thesis deposit",
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
    pinned_path = Path(__file__).resolve().parents[1] / "sources" / "public-originals-pinned.json"
    pinned_manifest = json.loads(pinned_path.read_text(encoding="utf-8"))
    pinned = {s["source_id"]: s for s in pinned_manifest["sources"]}
    reports = []
    proposed_pins = []
    for item in PUBLIC_CASES:
        case = dict(item)
        case["retrieved_at"] = date.today().isoformat()
        original = originals / case["local_path"]
        try:
            download_public(case["download_url"], original)
            if case["source_id"] in pinned:
                fixed = pinned[case["source_id"]]
                if fixed["download_url"] != case["download_url"] or fixed["local_path"] != case["local_path"]:
                    raise ValueError("PIN_SOURCE_MISMATCH: downloaded target differs from committed pinned original")
                check = verify_source(fixed, originals)
                check["preliminary_unpinned_discovery"] = False
                check["pin_source"] = "sources/public-originals-pinned.json"
                check["original_pdf_size_bytes"] = original.stat().st_size
            else:
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
    # Explicitly require the two PREVIOUSLY COMMITTED pins to match FRESH downloads.
    expected_ids = {"EDINBURGH_MCMILLAN_2018", "EWCA_GULATI_2015"}
    verified_pinned = {x.get("source_id") for x in reports
                       if x.get("state") in {"VERIFIED_EXACT", "VERIFIED_NORMALIZED"}
                       and x.get("preliminary_unpinned_discovery") is False}
    print("COMMITTED_PIN_VERIFICATION",
          "PASSED" if expected_ids.issubset(verified_pinned) else "FAILED",
          sorted(verified_pinned))
    return 0 if expected_ids.issubset(verified_pinned) else 2


if __name__ == "__main__":
    raise SystemExit(main())
