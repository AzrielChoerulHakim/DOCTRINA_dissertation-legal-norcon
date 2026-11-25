# DOCTRINA — Norm / Concept Dissertation Argumentation (v0.3.1 Scope)

**Status:** functional design prototype + executable structural argument lint; not a certified doctoral examiner or a full legal reasoner.

**CURRENT RESEARCH OBJECT SCOPE: ONLY NORMA or KONSEP.** The dissertation must identify a specific legal norm or a specific legal concept as the primary research object. Theories may support interpretation but are **not** research objects, targets for proof/falsification, or required original outputs. See [RFC-007: Norm / Concept Scope Freeze](docs/RFC-007-NORM-CONCEPT-SCOPE.md).

**Design shift from v0.2:** the central objective is the *internal examination of the argument within an ongoing normative–conceptual law dissertation*. Final evaluation of originality occurs **after** internal audit, dialectical challenge, dissertation integration and a human-reviewed defense rehearsal. Prior scholarship remains available throughout for doctrinal and conceptual interpretation.

## What DOCTRINA actually examines

- **NORMA:** text/source, applicability, hierarchy, interpretation, exceptions, coherence and normative consequences of an identifiable legal rule or principle.
- **KONSEP:** meaning, competing definitions/conceptions, boundary cases, internal coherence and implications of an identifiable legal concept.
- **Central process:** reconstruct the author's claims about the norm/concept, challenge their internal warrants and cross-chapter dependencies, then evaluate the strongest alternative interpretation. **Originality is assessed last.**
- **Theory:** a supporting tool only. DOCTRINA does not evaluate whole theories as doctoral research objects or demand the creation of a general legal theory.

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

## Methodological research and scope decisions

- **CURRENT SCOPE:** [RFC-007 — NORMA / KONSEP Only](docs/RFC-007-NORM-CONCEPT-SCOPE.md) supersedes any broader historical examples involving theories as research objects.
- [RFC-006 — Normative–Conceptual Doctoral Research](docs/RFC-006-NORMATIVE-CONCEPTUAL-DOCTORAL-RESEARCH.md) distinguishes doctrinal, conceptual, interpretive, ontological, critical and normative claims, and proposes five high-risk transitions to audit.
- [Conceptual Research Charter](skills/doctrina/templates/conceptual-research-charter.md) provides a live-draft worksheet for the author's actual research problem, methodology, theory roles, argument scope, chapter spine and human revision decisions.
- **Release status:** `SKILL.md` now declares the NORMA/KONSEP-only scope (v0.3.1 instructions). The Python linter and its 18 previously documented mechanical tests remain v0.3 and **do not yet enforce research-object typing**. RFC-006 and RFC-007 contain research/design rules; implementing a schema migration, expert review and regression tests remains future work. No semantic doctoral-reasoning capability has been certified.
