# DOCTRINA v0.4 — Norm / Concept Dissertation Reasoning Core

**Status:** local-first v0.4 object/provenance and argument-review prototype with a backward-compatible v0.3 graph linter. **Not an autonomous semantic legal examiner or doctoral novelty-certification tool.**

**CURRENT RESEARCH OBJECT SCOPE: ONLY NORMA or KONSEP.** The dissertation must identify a specific legal norm or a specific legal concept as the primary research object. Theories may support interpretation but are **not** research objects, targets for proof/falsification, or required original outputs. See [RFC-007: Norm / Concept Scope Freeze](docs/RFC-007-NORM-CONCEPT-SCOPE.md).

**Design shift from v0.2:** the central objective is the *internal examination of the argument within an ongoing normative–conceptual law dissertation*. Final evaluation of originality occurs **after** internal audit, dialectical challenge, dissertation integration and a human-reviewed defense rehearsal. Prior scholarship remains available throughout for doctrinal and conceptual interpretation.

## What DOCTRINA actually examines

- **NORMA:** text/source, applicability, hierarchy, interpretation, exceptions, coherence and normative consequences of an identifiable legal rule or principle.
- **KONSEP:** meaning, competing definitions/conceptions, boundary cases, internal coherence and implications of an identifiable legal concept.
- **Central process:** reconstruct the author's claims about the norm/concept, challenge their internal warrants and cross-chapter dependencies, then evaluate the strongest alternative interpretation. **Originality is assessed last.**
- **Three final originality types only:** `normative`, `interpretative`, and `conceptual`. One primary contribution type is chosen from demonstrated findings; a secondary type is optional. A distinct title or rewording does not prove novelty.
- **Theory:** a supporting tool only. DOCTRINA does not evaluate whole theories as doctoral research objects or demand the creation of a general legal theory.

## Start here

- `skills/doctrina/SKILL.md` — human/agent workflow router.
- `docs/RFC-005-ARGUMENT-FIRST-DOCTORAL-REVIEW.md` — specification and audit methodology.
- [RFC-008: Three-Type Novelty Baseline](docs/RFC-008-THREE-TYPE-NOVELTY-BASELINE.md) — final-gate contribution contract.
- [`final-novelty-matrix.md`](skills/doctrina/templates/final-novelty-matrix.md) — proposition-level final comparison (not for early certification).
- `skills/doctrina/modules/` — seven focused stage instructions.
- `skills/doctrina/templates/` — review card, ledger, decision-log templates.
- `examples/kepentingan-umum-illustrative.json` — **synthetic** argument graph; not an assertion of Indonesian positive law.
- `scripts/audit_argument_graph.py` — dependency, premises, quoted-source and inference lint.
- `tests/test_argument_graph.py` — executable regression tests.
- `docs/TEST-RESULTS.md` — generated run record after execution.

## v0.4 local-first draft workflow

The new CLI reads local UTF-8 drafts, records original paragraph passages and their exact line/character positions, and produces source-linked reports after researcher/agent annotation. **It deliberately does not invent premises or make semantic conclusions from text segmentation.**

```bash
python scripts/doctrina_cli.py init --input examples/dissertation-draft-synthetic.txt --object concept --title "Kepentingan umum" --locus "simulasi" --out /tmp/doctrina-case.json
python scripts/doctrina_cli.py check /tmp/doctrina-case.json
python scripts/doctrina_cli.py report /tmp/doctrina-case.json --out /tmp/doctrina-review.md
python -m unittest discover -s tests -v
```

The CLI intake is intentionally incomplete until a real claim reconstruction is confirmed by the researcher. Follow [Draft Reconstruction Protocol](skills/doctrina/templates/draft-reconstruction-protocol.md) for the semantic agent-led step. Do not commit unpublished manuscripts or any associated private case/report to this public repo.

- [Data schema v0.4](schemas/case-v0.4.schema.json)
- [Implementation and limitations — RFC-009](docs/RFC-009-REASONING-CORE-IMPLEMENTATION.md)
- [New v0.4 tests](tests/test_doctrina_core.py) and [GitHub Actions workflow](.github/workflows/test.yml)

## Legacy v0.3 demonstration

```bash
python scripts/audit_argument_graph.py examples/kepentingan-umum-illustrative.json --mode draft
python scripts/audit_argument_graph.py examples/kepentingan-umum-illustrative.json --mode pre-originality
python -m unittest discover -s tests -v
```

Only Python standard library is required for the script. Full argument assessment, source-checking, theory interpretation and conceptual adjudication are **human-in-the-loop**.

## Real dissertation excerpt pilots and next roadmap

**Research pilots:** P002 (Gutierrez Raymondova, Edinburgh, 2021) and **seven additional real doctoral dissertations** P003–P009 (four legal concepts, three legal norms). This is **excerpt-level hypothesis testing on auditor-reconstructed graphs**, not validation of complete dissertations, of source-PDF bytes or of scholarly correctness.

- [Seven-dissertation critical comparison and methodological limits](docs/PILOT-BATCH-P003-P009-RESULTS.md)
- [RFC-010 — Evidence-driven post-batch development roadmap](docs/RFC-010-POST-BATCH-DEVELOPMENT-PLAN.md)
- [P003–P009 source registry and short quotation fixtures](examples/dissertation_batch_003_009.json)
- [Seven pilot tests and negative controls](tests/test_pilot_batch_003_009.py)
- [Reproducible machine report generator](scripts/run_dissertation_batch.py)
- [GitHub Actions: download machine reports](https://github.com/AzrielChoerulHakim/DOCTRINA_dissertation-legal-norcon/actions/workflows/test.yml)

```bash
python -m unittest discover -s tests -v
python scripts/run_dissertation_batch.py --out-dir /tmp/doctrina-batch
```

**Current regression result:** 55/55 unit tests passed in the recorded P003–P009 run; CI also generated source-limited machine reports. This is **not a claim of semantic accuracy**, which awaits original-source anchoring and independent legal reviewers. The plan prioritizes source provenance, author-faithful reconstruction and normative/conceptual inference *before* final novelty assessment.

## Authority and confidentiality

No unfinished dissertation, client material or copyrighted full-text corpus is included. The example is original and synthetic. Keep actual unpublished manuscripts outside public GitHub; publish only schemas, procedures, anonymized fixtures and licensed source snippets.

## Provenance

Initial repository import from **DOCTRINA v0.3 — Internal Argumentation Engine**. The initial package is a prototype and is **not academically validated**. Source history: project RFC-005 and the local v0.3 package.

## Methodological research and scope decisions

- **CURRENT SCOPE:** [RFC-007 — NORMA / KONSEP Only](docs/RFC-007-NORM-CONCEPT-SCOPE.md) supersedes any broader historical examples involving theories as research objects.
- [RFC-006 — Normative–Conceptual Doctoral Research](docs/RFC-006-NORMATIVE-CONCEPTUAL-DOCTORAL-RESEARCH.md) distinguishes doctrinal, conceptual, interpretive, ontological, critical and normative claims, and proposes five high-risk transitions to audit.
- [Conceptual Research Charter](skills/doctrina/templates/conceptual-research-charter.md) provides a live-draft worksheet for the author's actual research problem, methodology, theory roles, argument scope, chapter spine and human revision decisions.
- **Release status:** v0.4 implements a norm/concept-only intake schema, local draft passage extraction, provenance validation and Markdown argument review. Legacy v0.3 argument-graph tests still apply; automated novelty assessment and validated semantic jurisprudential reasoning remain out of scope. Researchers retain control over their interpretations and revisions.
