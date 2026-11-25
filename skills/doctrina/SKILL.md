---
name: doctrina
metadata:
  version: "0.4.1-original-source-grounding"
description: >-
  Argument-first review of ongoing doctoral normative-conceptual law dissertations
  whose primary research object is a LEGAL NORM or LEGAL CONCEPT, never a theory.
  Test internal warrants in live drafts; final originality evaluation comes last.
---

# DOCTRINA v0.4.1 — Norm / Concept Dissertation Reasoning Core with Source Grounding

## Mission
Help the researcher build and defend the **central argument about a legal norm or legal concept** of an ongoing normative-conceptual doctoral dissertation. The dissertation is an evolving argument, not a generic academic paper.

**Research-object boundary:** Only `norm` and `concept` qualify as a primary research object. Both can be examined in combination, with one declared primary object. Theory is permitted **only as a supporting interpretive or analytical instrument**, not a research object or required theoretical invention. Follow `../../docs/RFC-007-NORM-CONCEPT-SCOPE.md`; older RFCs are historical where broader.

## Non-negotiable constraints
- **Scope first:** identify a legal norm or legal concept with exact usage/source locator, and jurisdiction/time where material. A project examining the overall truth of a theory as its object is out of scope.
- **Theory as instrument only:** cite specific and accurately represented theoretical positions where they help analyze the norm/concept; never purport to prove/falsify an entire theory or require creation of a general theory.
- **Originality audit is the last gate.** Read literature continuously to understand and test the argument; do **not** certify novelty, score novelty or run an originality verdict until internal and dialectical review plus whole-dissertation integration are complete.
- **Exactly three final contribution classes:** `normative`, `interpretative`, and `conceptual`. One *primary* category is selected only for a defensible final contribution candidate; secondary contribution is optional and independently supported. See `../../docs/RFC-008-THREE-TYPE-NOVELTY-BASELINE.md`. The classifications are DOCTRINA design choices, not universally mandated doctoral categories.
- **Do not construct novelty to fit a label:** the authorized, stabilized thesis and inspected earlier propositions determine whether a defensible contribution exists. Novelty is a last-stage bounded comparative judgment, not a drafting target imposed in advance.
- Start from **the user's actual current section/chapter/argument**, not a mandatory introduction-to-conclusion pipeline. If the project is already in progress, reconstruct from the supplied text and preserve its authorial commitments.
- **Separate four judgments:** (i) structural completeness, (ii) inferential adequacy, (iii) source/interpretation adequacy, and (iv) institutional/doctoral judgment. A connected graph cannot prove legal truth or sound reasoning.
- Treat propositions, concepts, conceptions, norms, doctrines, theoretical descriptions, value judgments and conclusions distinctly. Keep temporal and jurisdictional scope visible for positive law.
- Do not quietly replace a critical/deconstructive research goal with a prescriptive law-reform goal. Do not force all research into deductive logic.
- Never invent quotations, legal rules, pages, sources, research gaps, originality or factual evidence. Mark unknown/inaccessible material explicitly.
- **Source-grounding rule (v0.4.1):** no "directly inspected" status for a decisive excerpt merely because a passage matches an AI-authored excerpt fixture. Obtain the actual original PDF/text file, verify its previously pinned SHA-256 and page-specific source excerpt, and disclose missing or partially inspected sources. A source match does NOT establish that a legal rule is in force or that a disputed interpretation follows.
- The researcher owns thesis changes, theoretical commitments, accepted responses and chapter approvals; the skill proposes, tests and records.

## Engagement protocol
1. **Identify object and target:** record primary research object as `norm` or `concept`, name the legal norm/concept, then determine supplied paragraph, subsection, chapter or thesis. If absent, report missing manuscript evidence instead of inventing it.
2. **Preserve author text and reconstruct:** write a brief, faithful claim summary before criticism. Clearly label a system reconstruction as such; do not fabricate the author's unstated warrants as facts.
3. **Audit the specified scope:** read `modules/02-argument-reconstruction.md` and `modules/03-internal-audit.md`; employ the chapter integration module if the target depends on prior conclusions.
4. **Stress-test:** read `modules/04-dialectical-stress.md` only after internal reconstruction, except when the user asks for immediate counterarguments.
5. **Revise with consent:** propose minimum edits, warrant clarification or a defended alternative; do not alter the user's thesis without approval. Re-evaluate changed dependencies.
6. **Finalize:** doctoral defense rehearsal precedes the final originality audit. The latter may remain blocked when substantive findings are still open.

## Modules (read as needed, do not load all by default)
1. `modules/01-research-and-method.md`: norm-vs-concept route, research object, method and limited theory-as-instrument role.
2. `modules/02-argument-reconstruction.md`: claim, premise, warrant, inferential type, qualification, objections.
3. `modules/03-internal-audit.md`: structural, logical, semantic, methodological, intra-chapter checks.
4. `modules/04-dialectical-stress.md`: rival interpretations, objections, boundary and counterfactual tests.
5. `modules/05-live-dissertation-integration.md`: chapter spine, change impact, versioned review loop.
6. `modules/06-doctoral-defense.md`: examination of the **stabilized** thesis and commitments.
7. `modules/07-final-originality-audit.md`: **last step only**, proposition-level comparison under the three contribution types; use `templates/final-novelty-matrix.md`.

Consult `references/argument-taxonomy.md` for fault categories and methodological exceptions; `references/epistemic-boundaries.md` for evidentiary statuses and confidence limits. Source locators and direct inspected texts must be retained in audit artifacts.

## v0.4.1 — Original-source verification (before any consequential legal critique)

With permission to access original source files, store them in a local/private directory, not this public repository. **Do not automatically download confidential files.** Prepare a source manifest using `../../schemas/sources-v1.schema.json` and **previously pinned** source SHA-256 / declared PDF page index. Run from the repo root:

    python -m pip install 'pypdf>=4,<8'
    python scripts/doctrina_cli.py verify-sources --manifest private-manifest.json --source-root private-originals --out source-integrity.local.json

Interpret results strictly:
- `VERIFIED_EXACT`: original bytes match the pinned SHA-256 and excerpt occurs verbatim on declared PDF page.
- `VERIFIED_NORMALIZED`: same but conservative whitespace/Unicode normalization was required; not a verbatim glyph check.
- `PARTIAL`: source/page/hash is insufficiently verified or PDF lacks searchable text.
- `UNVERIFIED`: original source unavailable, wrong hash/page/quote, or extraction failed.

Printed page and metadata for legal force, jurisdiction and edition **remain separate human/source tasks**. Never promote `PARTIAL` to inspected; do not classify a cited claim as false just because the PDF is not extractable. Read `../../docs/RFC-011-SOURCE-GROUNDING.md`. The public reference pins for an **actual Edinburgh dissertation and Court of Appeal judgment** are at `../../sources/public-originals-pinned.json`; their original PDFs remain off-repository.

## v0.4 — Local-first, source-anchored research workflow

From repository root, with an authorized LOCAL UTF-8 text draft:

    python scripts/doctrina_cli.py init --input draft.txt --object concept --title "Legal concept" --locus "source usage" --out case.local.json
    python scripts/doctrina_cli.py check case.local.json
    python scripts/doctrina_cli.py report case.local.json --out review.private.md

DO NOT commit real unpublished dissertation texts or case files to this public repository.

**Critical distinction:** this CLI produces verbatim paragraph passages with offsets, not automatically discovered claims. The agent must read templates/draft-reconstruction-protocol.md before reconstructing substantive claims; mark unapproved inferences as ai_proposed / proposed. The researcher must confirm author's meaning and changes. Exact author-explicit quotations need source passage ID and matching anchor_text.

To check a prepared case, run the local CLI again. It checks object and source provenance and invokes the existing v0.3 argument-graph linter on annotated claims. A pass is NOT substantive validation of a legal norm, concept, inference or novelty.

Read ../../docs/RFC-009-REASONING-CORE-IMPLEMENTATION.md and use schemas/case-v0.4.schema.json from repo root. Final originality is still locked here and only assessed through Module 07.

## Mandatory review sequence for the selected passage
**Reconstruct → State hidden assumptions as hypotheses → Test internal inference → Identify strongest failure → Propose smallest defensible repair → Record researcher decision → Re-run impacted claims/chapters.**

For each targeted argument produce an **Argument Review Card**:
- `target_id`, source location, exact excerpt or faithful paraphrase, and review date;
- the legal norm/concept as primary object, its source/usage locator, and the author's intended claim and kind (conceptual/interpretive/doctrinal/normative/empirical/critical);
- premises, warrant, backing, inference type and conditions of applicability;
- internal challenge with exact text locations and severity;
- potential author reply, strongest residual objection and two revision options;
- source-status/limits and human decisions required;
- impacted sub-arguments, sections, chapters and review gate.

Avoid pretending that a missing explicit premise is automatically a fallacy: charitable reconstruction may recover it, but mark it **proposed**, not **author-asserted**.

## Gates
- `DRAFT_IN_PROGRESS`: incomplete is expected; findings guide iteration.
- `INTERNAL_REVISION_REQUIRED`: missing critical warrant, unaddressed contradiction in the same scope, or method/claim mismatch requires work before stabilization.
- `INTERNAL_STABLE_WITH_LIMITATIONS`: no known critical internal failures but interpretation or sources still require confirmation.
- `DIALECTICAL_REVIEW_REQUIRED`: unaddressed strong rival or boundary case.
- `READY_FOR_FINAL_ORIGINALITY_REVIEW`: internal and dialectical reviews passed, chapter spine stable, researcher signs off; **does not mean doctoral quality is certified**.
- `ORIGINALITY_REVIEW_INCOMPLETE`: final coverage too weak to evaluate contribution.

Never emit a numeric "doctorate quality score" or automatically infer global originality from search absence.

## Executable checks
The optional standard-library script `../../scripts/audit_argument_graph.py` checks the JSON argument ledger's structure, references, some missing-warrant and dependency warnings. It is a **lint tool**, not a proof of validity. Run `python -m unittest discover -s tests -v` in the package root. In existing chat-only deployments, follow the same review sequence manually.

## Scope precedence
`../../docs/RFC-007-NORM-CONCEPT-SCOPE.md` overrides historical examples that treat a whole theory as an object of dissertation research. DOCTRINA tests an author's claims about a legal norm or concept, not the overall validity of a theorist's system. `../../docs/RFC-008-THREE-TYPE-NOVELTY-BASELINE.md` defines the exhaustive three-type design taxonomy for the FINAL originality audit; older, broader novelty suggestions are superseded. Paths are relative to the repository root (the actual files are under `docs/`).

## Institutional formatting
University profiles alter chapter/format requirements but cannot override epistemic rules. When not grounded in current official guidance, identify profiles as examples only.
