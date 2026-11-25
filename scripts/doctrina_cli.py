#!/usr/bin/env python3
"""DOCTRINA v0.4 local-only command line: init, migrate, check, report."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

from doctrina_core import new_case, migrate_legacy, read_case, review, markdown_report


def write_content(path: str, text: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")


def options() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    intake = subs.add_parser("init", help="Segment a local UTF-8 draft into candidate passages, not invented claims")
    intake.add_argument("--input", required=True, help="Local draft in UTF-8 plain text")
    intake.add_argument("--object", required=True, choices=["norm", "concept"])
    intake.add_argument("--title", required=True)
    intake.add_argument("--locus", default="")
    intake.add_argument("--jurisdiction", default="")
    intake.add_argument("--temporal-scope", default="")
    intake.add_argument("--out", required=True, help="Local JSON research case; do not publish private drafts")

    migrate = subs.add_parser("migrate", help="Migrate v0.3 ledger, marking all old claims unanchored")
    migrate.add_argument("--input", required=True)
    migrate.add_argument("--object", required=True, choices=["norm", "concept"])
    migrate.add_argument("--title", required=True)
    migrate.add_argument("--locus", default="")
    migrate.add_argument("--jurisdiction", default="")
    migrate.add_argument("--temporal-scope", default="")
    migrate.add_argument("--out", required=True)

    check = subs.add_parser("check", help="Mechanical provenance/object/argument checks")
    check.add_argument("case", help="v0.4 JSON case")
    check.add_argument("--out", help="Save JSON findings to a local path")
    report = subs.add_parser("report", help="Anchored Markdown argument review, no inferred truth claims")
    report.add_argument("case", help="v0.4 JSON case")
    report.add_argument("--out", help="Save Markdown report to a local path")
    return parser


def main(argv=None) -> int:
    args = options().parse_args(argv)
    try:
        if args.command == "init":
            source = Path(args.input)
            draft = source.read_text(encoding="utf-8")
            data = new_case(draft, args.object, args.title, locus=args.locus,
                            jurisdiction=args.jurisdiction, temporal_scope=args.temporal_scope,
                            source_filename=source.name)
            write_content(args.out, json.dumps(data, ensure_ascii=False, indent=2)+"\n")
            print(f"Created {args.out} with {len(data['draft']['passages'])} unclassified passages; no semantic claims inferred")
            return 0
        if args.command == "migrate":
            old = read_case(args.input)
            data = migrate_legacy(old, args.object, args.title, locus=args.locus,
                                  jurisdiction=args.jurisdiction, temporal_scope=args.temporal_scope)
            write_content(args.out, json.dumps(data, ensure_ascii=False, indent=2)+"\n")
            print(f"Migrated {args.out}; historical claims need new original-draft anchors")
            return 0
        data = read_case(args.case)
        if args.command == "check":
            result = review(data)
            output = json.dumps(result, ensure_ascii=False, indent=2)+"\n"
            if args.out:
                write_content(args.out, output)
                print(f"Wrote {args.out} (gate: {result['gate']})")
            else:
                print(output, end="")
            return 2 if result["counts"]["critical"] else 0
        if args.command == "report":
            result = markdown_report(data)
            if args.out:
                write_content(args.out, result)
                print(f"Wrote {args.out}")
            else:
                print(result)
            return 0
        return 2
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"DOCTRINA error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
