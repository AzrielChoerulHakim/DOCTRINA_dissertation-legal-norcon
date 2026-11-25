# DOCTRINA v0.3 — Internal Argumentation for Ongoing Doctoral Dissertations

**Status:** functional design prototype + executable structural argument lint; not a certified doctoral examiner or a full legal reasoner.

**Design shift from v0.2:** the central objective is the *internal examination of the argument within an ongoing normative–conceptual law dissertation*. Final evaluation of originality occurs **after** internal audit, dialectical challenge, dissertation integration and a human-reviewed defense rehearsal. Prior scholarship remains available throughout for doctrinal and conceptual interpretation.

## Start here

- `skills/doctrina/SKILL.md` — human/agent workflow router.
- `docs/RFC-005-ARGUMENT-FIRST-DOCTORAL-REVIEW.md` — specification and audit methodology.
- `skills/doctrina/modules/` — seven focused stage instructions.
- `skills/doctrina/templates/` — review card, ledger, decision-log templates.
- `examples/kepentingan-umum-illustrative.json` — **synthetic** argument graph; not an assertion of Indonesian positive law.
- `scripts/audit_argument_graph.py` — dependency, premises, quoted-source and inference lint.
- `tests/test_argument_graph.py` — executable regression tests.
- `docs/TEST-RESULTS.md` — generated run record after execution.

## Local demonstration

```bash
python scripts/audit_argument_graph.py examples/kepentingan-umum-illustrative.json --mode draft
python scripts/audit_argument_graph.py examples/kepentingan-umum-illustrative.json --mode pre-originality
python -m unittest discover -s tests -v
```

Only Python standard library is required for the script. Full argument assessment, source-checking, theory interpretation and conceptual adjudication are **human-in-the-loop**.

## Authority and confidentiality

No unfinished dissertation, client material or copyrighted full-text corpus is included. The example is original and synthetic. Keep actual unpublished manuscripts outside public GitHub; publish only schemas, procedures, anonymized fixtures and licensed source snippets.

## Provenance

Initial repository import from **DOCTRINA v0.3 — Internal Argumentation Engine**. The initial package is a prototype and is **not academically validated**. Source history: project RFC-005 and the local v0.3 package.
