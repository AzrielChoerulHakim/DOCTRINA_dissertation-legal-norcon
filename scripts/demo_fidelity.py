#!/usr/bin/env python3
"""DOCTRINA P1 reproducible synthetic multi-voice demonstration.

No actual dissertation, human assent, or independently verified semantic
interpretation is included; proposal status remains explicitly provisional.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from doctrina_core import new_case
from doctrina_fidelity import begin, propose

ROOT = Path(__file__).resolve().parents[1]
TEXT_FILE = ROOT / "examples" / "fidelity_draft_synthetic.txt"


def example():
    text = TEXT_FILE.read_text(encoding="utf-8")
    case = new_case(text, "concept", "Kepentingan umum",
                    locus="penggunaan istilah dalam norma hipotetis",
                    jurisdiction="Indonesia", source_filename=TEXT_FILE.name)
    case["research_object"]["concept_usages"] = [{
        "usage": "kepentingan umum",
        "locator": "T0001 (contoh sintetik)",
        "inspection_status": "unverified",
    }]
    case = begin(case, text)

    def item(rid, pid, quote, voice, mode, proposition, basis, premises=()):
        passage = next(p for p in case["draft"]["passages"] if p["id"] == pid)
        at = passage["verbatim"].index(quote)
        return {
            "id": rid, "passage_id": pid,
            "span": {"start": at, "end": at+len(quote), "quote": quote},
            "voice": voice, "mode": mode,
            "proposition": proposition,
            "voice_basis": basis,
            "premise_ids": list(premises),
            "context_passage_ids": [pid],
            "proposed_by": "synthetic_example_not_author_approved",
        }

    case = propose(case, item(
        "P1", "T0001", "konsep kepentingan umum memerlukan batas yang dapat diuji",
        "author", "explicit",
        "Penulis menganggap pembatasan konsep kepentingan umum diperlukan.",
        "Kalimat disandarkan pada penulis dan belum disetujui secara semantik",
    ))
    case = propose(case, item(
        "P2", "T0002", "seluruh penetapan negara selalu sah",
        "opponent", "explicit",
        "Pendapat lawan menyatakan penetapan negara selalu sah.",
        "Frasa eksplisit berada setelah 'Menurut pihak lain' dan kemudian ditolak penulis",
    ))
    case = propose(case, item(
        "C1", "T0003", "Jika norma itu tidak menjelaskan syaratnya, maka penerapannya perlu dikaji lebih lanjut",
        "author", "conditional",
        "Hanya bila norma gagal menentukan syaratnya, penerapannya perlu dikaji lebih lanjut.",
        "Kalimat memiliki antecedent 'Jika ...' yang wajib dipertahankan",
        premises=["P1"],
    ))
    return case


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    case = example()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(case, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(f"Created {args.out}; 3 candidate records, ZERO approvals, originality LOCKED")


if __name__ == "__main__":
    main()
