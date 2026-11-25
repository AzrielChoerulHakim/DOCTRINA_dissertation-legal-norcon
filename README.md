# DOCTRINA v0.4.2 — Norm / Concept Dissertation Review with Author-Faithful Reconstruction

**Status:** local-first norm/concept structural audit + v0.4.1 original-source verification + **P1 version-bound authorial reconstruction and human-only interactive self-attestation**. Backward-compatible with legacy v0.3 structural lint. **Not independent semantic accuracy, verified researcher identity, legal validity, or doctoral novelty certification.**

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

## v0.4.2 — Fundamental Author-Faithful Reconstruction (P1)

The original manuscript, not an AI-generated graph, controls the scope of the author's claim. P1 now tracks exact UTF-8 draft bytes, Unicode spans, voice (author / opponent / quoted / hypothetical / uncertain), assertion mode (explicit / paraphrase / inferred / question / conditional), surrounding context, and load-bearing premise dependencies. **No proposal becomes author-approved by editing a JSON field.** A local reviewer must explicitly approve/reject/revise an individual versioned proposal; interactive TTY is required and decisions become stale after a source, claim or premise revision. This is self-attested, not a digital signature or independent proof of interpretive fidelity.

Run a reproducible three-proposition synthetic case with zero implicit approvals:

\`\`\`bash
python scripts/demo_fidelity.py --out /tmp/doctrina-p1-demo.json
python scripts/fidelity_cli.py check \
  --case /tmp/doctrina-p1-demo.json \
  --draft examples/fidelity_draft_synthetic.txt \
  --format markdown --out /tmp/doctrina-p1-review.md
python scripts/doctrina_cli.py check /tmp/doctrina-p1-demo.json \
  --original-draft examples/fidelity_draft_synthetic.txt
\`\`\`

- [Author-fidelity specification and scope boundaries](docs/RFC-012-AUTHOR-FAITHFUL-RECONSTRUCTION.md)
- [P1 two-pass argument reconstruction protocol](skills/doctrina/templates/draft-reconstruction-protocol.md)
- [Fidelity model, dependency fingerprints and approval gates](scripts/doctrina_fidelity.py)
- [Researcher-local interactive fidelity CLI](scripts/fidelity_cli.py)
- [P1 JSON schema](schemas/reconstruction-v1.schema.json)
- [Synthetic case generator](scripts/demo_fidelity.py) and [source](examples/fidelity_draft_synthetic.txt)
- [P1 test suite](tests/test_fidelity_p1.py) and [core integration tests](tests/test_fidelity_core_integration.py)

**Important:** the checker validates exact text and structurally recorded assent, not the substantive fairness of a paraphrase. The P1 human decision is self-attested; independent double-review and semantic metrics are **still needed**. New actual manuscript reviews must pass P1 before substantive argument diagnosis. The earlier seven published doctoral pilots have not retrospectively become author-approved.

## v0.4.1 — Verify original PDF/text sources before relying on decisive quotations

The source verifier examines the **actual local file bytes** against a previously recorded SHA-256, then searches the specified **0-based PDF page** for a short source excerpt. It differentiates exact, conservatively normalized, partial and unverified matches. This is evidence grounding, NOT a ruling about the document's doctrinal meaning or current legal validity.

```bash
python -m pip install 'pypdf>=4,<8'
python scripts/doctrina_cli.py verify-sources \
  --manifest private-sources.json \
  --source-root private-originals \
  --out integrity-report.local.json
```

See [RFC-011 — Source Grounding](docs/RFC-011-SOURCE-GROUNDING.md), [original-source schema](schemas/sources-v1.schema.json), [source verifier](scripts/verify_sources.py), and [source grounding tests](tests/test_source_grounding.py). The [public source-pin manifest](sources/public-originals-pinned.json) stores **only hashes, exact page indices, short excerpts and metadata** for one Edinburgh PhD thesis and one UK Court of Appeal judgment; full PDFs are never committed. GitHub Actions verifies original sources in a separate network-dependent step, and the artifact contains no original PDF bytes. The pilot script also records unavailable original sources rather than claiming success.

**Next roadmap:** author-faithful reconstruction (P1), norm/concept inference adequacy (P2), real-chapter dependencies (P3), independent scholarly validation (P4), and three-type originality gate **last** (P5).

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
