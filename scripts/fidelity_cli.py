#!/usr/bin/env python3
"""DOCTRINA P1 — local-only and fail-closed authorial reconstruction workflow.

P1 is NOT an automatic premise extractor, electronic signature, or independent
measure of semantic fidelity. Local researcher decisions require an actual TTY
and an explicit, claim-specific typed challenge.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from doctrina_core import read_case
from doctrina_fidelity import (
    begin, propose, inspect, render_report, approval_challenge, add_decision,
    version_sync,
)


def save(path: str, case: dict) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(case, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="action", required=True)
    start = sub.add_parser("start", help="Bind reconstruction to independently supplied draft")
    start.add_argument("--case", required=True)
    start.add_argument("--draft", required=True)
    start.add_argument("--out", required=True)
    candidate = sub.add_parser("propose", help="Add AI/reviewer candidate, NEVER auto-approved")
    candidate.add_argument("--case", required=True)
    candidate.add_argument("--id", required=True)
    candidate.add_argument("--passage", required=True)
    candidate.add_argument("--span-start", type=int, required=True)
    candidate.add_argument("--span-end", type=int, required=True)
    candidate.add_argument("--quote", required=True)
    candidate.add_argument("--voice", required=True,
                           choices=["author", "opponent", "quoted_source", "hypothetical", "uncertain"])
    candidate.add_argument("--mode", required=True,
                           choices=["explicit", "paraphrase", "inferred", "question", "conditional"])
    candidate.add_argument("--proposition", required=True)
    candidate.add_argument("--voice-basis", required=True)
    candidate.add_argument("--context", nargs="*", default=[])
    candidate.add_argument("--premises", nargs="*", default=[])
    candidate.add_argument("--out", required=True)
    check = sub.add_parser("check", help="Independent original-draft fidelity audit")
    check.add_argument("--case", required=True)
    check.add_argument("--draft", required=True)
    check.add_argument("--out")
    check.add_argument("--format", choices=["json", "markdown"], default="json")
    decide = sub.add_parser("decide", help="Interactive HUMAN self-attestation only")
    decide.add_argument("--case", required=True)
    decide.add_argument("--draft", required=True)
    decide.add_argument("--id", required=True)
    decide.add_argument("--reviewer", required=True)
    decide.add_argument("--decision", choices=["accept", "reject", "revise"], required=True)
    decide.add_argument("--reason", required=True)
    decide.add_argument("--out", required=True)
    sync = sub.add_parser("sync", help="Update to revised original draft; prior approvals become stale")
    sync.add_argument("--case", required=True)
    sync.add_argument("--draft", required=True)
    sync.add_argument("--out", required=True)
    return p


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.action == "start":
            case = begin(read_case(args.case), Path(args.draft).read_text(encoding="utf-8"))
            save(args.out, case)
            print(f"Initialized local fidelity ledger: {args.out} (no claims invented or approved)")
            return 0
        if args.action == "propose":
            case = read_case(args.case)
            record = {
                "id": args.id, "passage_id": args.passage,
                "span": {"start": args.span_start, "end": args.span_end, "quote": args.quote},
                "voice": args.voice, "mode": args.mode, "proposition": args.proposition,
                "voice_basis": args.voice_basis,
                "context_passage_ids": args.context, "premise_ids": args.premises,
                "proposed_by": "reviewer_or_ai_unapproved",
            }
            case = propose(case, record)
            save(args.out, case)
            print(f"Proposed {args.id}; researcher's confirmation required, not implied")
            return 0
        if args.action == "check":
            case = read_case(args.case)
            original = Path(args.draft).read_text(encoding="utf-8")
            result = inspect(case, original)
            out = render_report(case, original) if args.format == "markdown" else json.dumps(
                result, ensure_ascii=False, indent=2) + "\n"
            if args.out:
                target = Path(args.out)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(out, encoding="utf-8")
                print(f"Written {args.out}: {result['gate']}")
            else:
                print(out, end="")
            return 2 if result["gate"] in {"BLOCKED_SOURCE_OR_APPROVAL", "NOT_INITIALIZED"} else 0
        if args.action == "sync":
            case = version_sync(read_case(args.case),
                                Path(args.draft).read_text(encoding="utf-8"))
            save(args.out, case)
            print(f"Updated source version; ALL previous approvals require re-verification: {args.out}")
            return 0
        if args.action == "decide":
            if not sys.stdin.isatty() or not sys.stdout.isatty():
                raise ValueError(
                    "Refusing non-interactive approval. Run in a real local terminal; "
                    "an AI agent must not impersonate a researcher."
                )
            case = read_case(args.case)
            original = Path(args.draft).read_text(encoding="utf-8")
            record = next((r for r in case.get("reconstruction", {}).get("records", [])
                           if r.get("id") == args.id), None)
            if record is None:
                raise ValueError("Unknown reconstruction ID")
            print("LOCAL SELF-ATTESTATION — NOT VERIFIED IDENTITY / NOT AN E-SIGNATURE")
            print("Voice:", record.get("voice"), "Mode:", record.get("mode"))
            print("Original quote:", record.get("span", {}).get("quote"))
            print("Proposed interpretation:", record.get("proposition"))
            print("Premise IDs:", record.get("premise_ids"))
            print("Researcher decision:", args.decision, "Reason:", args.reason)
            challenge = approval_challenge(case, args.id)
            print("To record YOUR explicit decision, type exactly:", challenge)
            typed = input("Decision confirmation: ")
            out = add_decision(case, original, args.id, args.reviewer, args.decision,
                               args.reason, typed)
            save(args.out, out)
            print(f"Recorded local self-attested decision for {args.id}; verify with 'check'.")
            return 0
        return 2
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError, KeyError) as exc:
        print(f"DOCTRINA P1: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
