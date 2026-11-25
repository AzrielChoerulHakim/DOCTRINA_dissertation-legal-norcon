#!/usr/bin/env python3
"""DOCTRINA v0.4.1: verify an excerpt against bytes of an ORIGINAL LOCAL source.

This is a deterministic text/locator integrity tool, NOT proof of scholarly
interpretation, historical legal validity, copyright permission, or novelty.
No downloads, uploads, network calls, OCR, or private-content publishing.
For PDFs: 'pypdf' is an optional local dependency.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any

STATES = ("VERIFIED_EXACT", "VERIFIED_NORMALIZED", "PARTIAL", "UNVERIFIED")
KINDS = ("thesis_pdf", "legal_pdf", "pdf", "text_utf8")


def normalize(source: str) -> str:
    """Conservative PDF normalization. Case and punctuation are significant."""
    source = source.replace("\u00ad", "")
    source = re.sub(r"(?<=\w)-[ \t]*\r?\n[ \t]*(?=\w)", "", source)
    source = unicodedata.normalize("NFKC", source)
    return re.sub(r"\s+", " ", source).strip()


def _record(state: str, code: str, message: str) -> dict[str, str]:
    return {"state": state, "code": code, "explanation": message}


def _path(source_root: Path, local_path: Any) -> Path:
    """Reject directory traversal and symlinks leading outside the allowed root."""
    if not isinstance(local_path, str) or not local_path.strip():
        raise ValueError("Source entry needs local_path relative to --source-root")
    rel = Path(local_path)
    if rel.is_absolute() or any(x == ".." for x in rel.parts):
        raise ValueError("local_path must be relative and cannot traverse parent dirs")
    root = source_root.resolve()
    path = (root / rel).resolve()
    if not path.is_relative_to(root):
        raise ValueError("Resolved local_path leaves the source root")
    return path


def _pages(path: Path, kind: str) -> list[str]:
    if kind == "text_utf8":
        # A text document is treated as one source page, never a verified PDF.
        return [path.read_text(encoding="utf-8")]
    if kind not in ("thesis_pdf", "legal_pdf", "pdf"):
        raise ValueError("Invalid source_kind")
    with path.open("rb") as fh:
        if fh.read(5) != b"%PDF-":
            raise ValueError("PDF_HEADER_MISSING")
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("PDF_EXTRACTION_DEPENDENCY_MISSING: install pypdf") from exc
    reader = PdfReader(str(path), strict=False)
    if reader.is_encrypted:
        raise ValueError("ENCRYPTED_PDF_NOT_SUPPORTED")
    return [page.extract_text() or "" for page in reader.pages]


def verify_source(entry: dict[str, Any], source_root: Path) -> dict[str, Any]:
    """Verify one declared source; retain no full text in the returned report."""
    sid = entry.get("source_id", "UNIDENTIFIED") if isinstance(entry, dict) else "INVALID"
    result: dict[str, Any] = {
        "source_id": sid, "state": "UNVERIFIED",
        "source_kind": entry.get("source_kind") if isinstance(entry, dict) else None,
        "sha256_actual": None, "page_index_verified": None, "match_offset": None,
        "evidence": [], "limitations": [],
    }
    def evidence(state: str, code: str, explanation: str) -> None:
        result["evidence"].append(_record(state, code, explanation))
    if not isinstance(entry, dict):
        evidence("UNVERIFIED", "INVALID_ENTRY", "Source must be a JSON object")
        return result
    if not isinstance(sid, str) or not sid.strip():
        evidence("UNVERIFIED", "SOURCE_ID_REQUIRED", "Stable source ID required")
        return result
    kind = entry.get("source_kind")
    if kind not in KINDS:
        evidence("UNVERIFIED", "SOURCE_KIND_INVALID", "Use thesis_pdf/legal_pdf/pdf/text_utf8")
        return result
    anchor = entry.get("anchor_text")
    if not isinstance(anchor, str) or not anchor.strip():
        evidence("UNVERIFIED", "ANCHOR_REQUIRED", "A nonempty EXACT original-source excerpt is required")
        return result
    if len(anchor.split()) > 25:
        result["limitations"].append("Excerpt exceeds the 25-word public fixture convention; keep outputs private and consider copyright")
    try:
        p = _path(source_root, entry.get("local_path"))
    except ValueError as exc:
        evidence("UNVERIFIED", "UNSAFE_PATH", str(exc))
        return result
    if not p.is_file():
        evidence("UNVERIFIED", "SOURCE_FILE_MISSING", "Original file not present in local source root")
        return result
    actual = hashlib.sha256(p.read_bytes()).hexdigest()
    result["sha256_actual"] = actual
    expected = entry.get("content_sha256")
    if expected and (not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected)):
        evidence("UNVERIFIED", "INVALID_EXPECTED_HASH", "Expected hash must be a lowercase SHA-256 hex digest")
        return result
    if expected and expected != actual:
        evidence("UNVERIFIED", "HASH_MISMATCH", "Original bytes differ from pinned SHA-256; no excerpt may be certified")
        return result
    try:
        pages = _pages(p, kind)
    except (RuntimeError, ValueError, UnicodeError, OSError, Exception) as exc:
        # A malformed or image-only PDF must never be upgraded to VERIFIED.
        evidence("UNVERIFIED", "EXTRACTION_FAILED", type(exc).__name__ + ": " + str(exc)[:180])
        return result
    method = "utf8_text" if kind == "text_utf8" else "pypdf"
    result["extraction_method_actual"] = method
    declared = entry.get("extraction_method")
    if declared and declared != method:
        evidence("UNVERIFIED", "EXTRACTION_METHOD_MISMATCH", "Declared extraction method does not match actual method")
        return result
    if not pages or all(not text.strip() for text in pages):
        result["state"] = "PARTIAL"
        evidence("PARTIAL", "NO_EXTRACTABLE_TEXT", "No searchable text; manual image inspection/OCR review required")
        return result
    idx = entry.get("page_index")
    if isinstance(idx, bool) or (idx is not None and (not isinstance(idx, int) or idx < 0 or idx >= len(pages))):
        evidence("UNVERIFIED", "INVALID_PAGE_INDEX", "0-based PDF page_index is invalid or outside document")
        return result

    def match(text: str) -> tuple[str | None, int | None]:
        exact = text.find(anchor)
        if exact >= 0:
            return "VERIFIED_EXACT", exact
        if normalize(anchor) and normalize(anchor) in normalize(text):
            return "VERIFIED_NORMALIZED", None
        return None, None

    if idx is None:
        candidates = [(i, match(t)[0]) for i, t in enumerate(pages) if match(t)[0]]
        result["discovered_page_indices"] = [i for i, _ in candidates]
        result["state"] = "PARTIAL" if candidates else "UNVERIFIED"
        evidence(result["state"], "PAGE_LOCATOR_UNCONFIRMED" if candidates else "ANCHOR_NOT_FOUND",
                 "Text search found candidate page(s), but no researcher-confirmed 0-based page_index was supplied"
                 if candidates else "Declared anchor not found in extracted source")
        return result
    state, offset = match(pages[idx])
    if state is None:
        candidates = [i for i, text in enumerate(pages) if i != idx and match(text)[0]]
        evidence("UNVERIFIED", "ANCHOR_OFF_PAGE" if candidates else "ANCHOR_NOT_FOUND",
                 "Anchor absent from declared PDF page_index; alternative matches: " + repr(candidates[:12]))
        result["discovered_page_indices"] = candidates[:12]
        return result
    result["page_index_verified"] = idx
    result["match_offset"] = offset
    if not expected:
        result["state"] = "PARTIAL"
        evidence("PARTIAL", "HASH_NOT_PINNED", "Excerpt matched source file, but original byte hash was not pinned")
    else:
        result["state"] = state
        evidence(state, "EXACT_MATCH" if state == "VERIFIED_EXACT" else "NORMALIZED_MATCH",
                 "Declared source excerpt matched pinned original bytes at specified PDF page")
    if state == "VERIFIED_NORMALIZED":
        result["limitations"].append("Whitespace/Unicode normalization used; exact glyph layout not certified")
    if kind != "text_utf8" and entry.get("printed_page") in (None, ""):
        result["limitations"].append("Printed page label not independently established; PDF page index is 0-based")
    if entry.get("applicability_date"):
        result["limitations"].append("Applicability_date is DECLARED metadata, not proof the law was in force then")
    if entry.get("publication_year"):
        result["limitations"].append("Publication year is DECLARED metadata, not verified by matching the anchor")
    if not entry.get("repository_url"):
        result["limitations"].append("Repository provenance URL not recorded")
    if not entry.get("retrieved_at"):
        result["limitations"].append("Retrieval date not recorded")
    return result


def verify_manifest(manifest: dict[str, Any], root: Path) -> dict[str, Any]:
    if not isinstance(manifest, dict) or not isinstance(manifest.get("sources"), list):
        raise ValueError("Manifest must be JSON object with sources array")
    results = []
    used = set()
    for entry in manifest["sources"]:
        result = verify_source(entry, root)
        sid = result["source_id"]
        if sid in used:
            result["state"] = "UNVERIFIED"
            result["evidence"].append(_record("UNVERIFIED", "DUPLICATE_SOURCE_ID", "Source ID reused"))
        used.add(sid)
        results.append(result)
    counts = {state: sum(x["state"] == state for x in results) for state in STATES}
    return {
        "schema_version": "sources-v1",
        "status": "SOURCE_TEXT_VERIFICATION_ONLY",
        "counts": counts,
        "results": results,
        "disclaimer": "Matching text and SHA-256 DO NOT establish legal validity, interpretive correctness, historical applicability or novelty",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        report = verify_manifest(manifest, args.source_root)
        output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(output, encoding="utf-8")
            print(f"Wrote {args.out}: {report['counts']}")
        else:
            print(output, end="")
        return 2 if report["counts"]["UNVERIFIED"] else 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == "__main__":
    sys.exit(main())
