# RFC-010 — DOCTRINA Post-Batch Development Plan

**Status:** proposed engineering and validation roadmap, derived from the limited P003–P009 dissertation pilots (25 November 2026)  
**Evidence:** [PILOT-BATCH-P003-P009-RESULTS.md](PILOT-BATCH-P003-P009-RESULTS.md), [P003–P009 data](../examples/dissertation_batch_003_009.json), [test suite](../tests/test_pilot_batch_003_009.py)  
**Prior baselines:** [RFC-007, NORMA/KONSEP objects](RFC-007-NORM-CONCEPT-SCOPE.md), [RFC-008, three novelty types](RFC-008-THREE-TYPE-NOVELTY-BASELINE.md), [RFC-009, v0.4 core](RFC-009-REASONING-CORE-IMPLEMENTATION.md)

## Implementation progress — 25 November 2026

- **P0 / v0.4.1 original-source grounding: IMPLEMENTED and mechanically validated.** Source manifest, local PDF/text verifier, SHA-256/page-specific excerpt checks, 20 negative/positive verifier tests, and 2 CLI tests were added. Two independently pinned *real* original PDF sources (one university dissertation, one official court judgment) passed verification on a fresh retrieval. Detailed evidence: [RFC-011](RFC-011-SOURCE-GROUNDING.md).
- **P1–P5: NOT YET IMPLEMENTED/VALIDATED** as substantive release features. The next approved engineering dependency is P1, author-faithful argument reconstruction.
- Results remain restricted to source **text integrity** and structural compatibility; the 77 unit tests are *not* a measurement of doctoral-quality reasoning or novelty correctness.

## 1. Decision and evidence limitations

DOCTRINA **is ready for controlled pilot study**, not for claims of academic validity or dissertation grading. The additional batch covers **seven distinct published doctoral dissertations**, four concept-object cases (P003, P004, P005, P007) and three norm-object cases (P006, P008, P009). Alongside previous P002, eight published theses have been used for limited excerpt-level tests.

**Observed technical evidence:** the v0.4 code accepted all seven object classifications, preserved a deliberately marked *AI-proposed* argument reconstruction, held novelty at its final gate, and recorded open objections. A negative control demonstrated that removing a genuine normative premise from an auditor-constructed ledger can manufacture an IA-06 flag. The automated test suite reported **55/55 passes** on the P003–P009 test commit. These tests measure the expected behavior of software on the **annotations we wrote**, not semantic correctness of those annotations. No independent scholarly evaluation or original-author approval occurred. The runner did not inspect, download, hash or compare original PDF bytes; the fragments came from publicly indexed university-PDF text read by the auditor.

**Priority decision:** do **not** add more novelty types, mandate reform proposals, score doctoral quality, or develop a general-theory examiner. The central obstacle is *source-grounded and author-faithful legal inference*, and the plan tackles that before further final-stage contribution claims.

## 2. Risk-driven backlog

| Priority / Release | Deliverable | Batch evidence | Exit criterion | Exclusions |
|---|---|---|---|---|
| P0 — v0.4.1 | **Original-Source Grounding Layer** | R-01: source excerpt checked against an auditor-supplied microtext, not original PDF bytes; all P003–P009 | Each passage claimed as directly inspected has immutable source ID, edition/version, PDF/HTML content hash, page/locator, excerpt and retrieval audit state; unverified excerpt flagged, not silently accepted | Does not judge meaning from matching text |
| P1 — v0.4.2 | **Author-Faithful Reconstruction Layer** | R-02/R-08: graph premises and chapter IDs are invented audit hypotheses; P009 false IA-06 possible | 100% of author-attributed passages have source anchors; AI-proposed warrants, opponents and hypotheticals kept separate; author or competent independent reviewer explicitly confirms fidelity; errors tracked rather than rewritten silently | Does not endorse thesis or infer automatic truth |
| P2 — v0.4.3 | **Norm/Concept Justification Examiner** | R-03–R-07: validity versus legitimacy, norm temporal scope, nonprescriptive conceptual critique, inadequacy of Boolean normative bridge | For each claimed defect, explain actual norm/concept, inference type, exact supporting source, a missing/contested step, strongest charitable reply, undercutting/rebutting objection, and uncertainty; ambiguous cases retained as contestable | No theory-as-object, no mandatory statute reform |
| P3 — v0.5.0 | **Cross-Chapter Thesis Spine & Revision Impact** | R-08: synthetic CH1/CH2 misrepresents real chapter structure | Original manuscript headings/locations tracked; norm/concept revisions propagate to dependent sections and invalidate their stale approvals; reviewer can inspect changed before/after text | No automatic manuscript rewriting |
| P4 — v0.5.1 | **Independent Scholarly Validation Protocol** | No researcher confirmation or independent reviewer in batch; semantic false-positive rates unknown | Authorized substantive paragraphs from norm/concept dissertations; at least two qualified assessors independently label claims, inferential adequacy, legal sources, rival responses; disagreements adjudicated; measure substantive diagnostic precision/recall and false-positive categories on an independently labeled set | 55 tests are regression tests, not academic metrics |
| P5 — v0.6.0 | **Final Three-Type Originality Audit** | R-09: novelty must never be inferred from topic or search absence | Only after internal, dialectical, whole-dissertation and defense gates plus author approval: compare **verified propositions** to inspected prior scholarship; exactly one primary *normative / interpretative / conceptual* contribution if supported; secondary optional, or NOT_READY/INDETERMINATE | No novelty percentage or university pass certificate |

No invented release deadlines: implement in dependency order. A lower phase is not academically accepted until the listed evidence and exit criteria are independently inspected.

## 3. Detailed work packages

### WP-01 Source provenance (P0)

**Problem:** the local CLI guarantees only that the excerpt matches the *same excerpt-containing JSON*. In particular, P003–P009 were not automatically aligned to the full public PDF. This is the highest risk for misleading confidence.

**Build**
1. Introduce `sources-v1.schema.json`: `source_id`, `repository_url`, `download_url`, `content_sha256`, `retrieved_at`, `publication_year`, `edition`, `jurisdiction`, `applicability_date`, `extraction_method`, `page_index`, `printed_page`, `anchor_text`, `text_span`, `verification_state`.
2. Add an **optional local-only** PDF/text extraction workflow. Verify exact passage against original downloaded text; report image/scanned ambiguity and distinguish PDF page index from print pagination. Keep original source bytes and unpublished manuscripts out of the public repo.
3. Make claims with state `inspected` fail source-integrity audit if matching provenance/offset cannot be rechecked. Use `partial` for web snippets and short inspected passages.
4. Provide fixtures for a misquoted sentence, a real source with an absent page locator, ambiguous OCR, and a misleading edition/time.
5. Record licenses, access conditions, and permission; maintain a clear no-fulltext public commit policy.

**Exit:** reproducible origin-to-excerpt check on at least one authorized complete public thesis PDF and one verified original legal source; reports distinguish `VERIFIED_EXACT`, `VERIFIED_NORMALIZED`, `PARTIAL`, `UNVERIFIED`. No source metadata is converted into substantive support merely because its URL exists.

### WP-02 Fidelity and annotation (P1)

**Problem:** author voice can be confused with citations, counterpositions, reader speculation and hypothetical premises. P009 shows false critical flags can emerge solely from an auditor's omitted premise.

**Build**
1. Add stable identifiers for original passage, *actual* chapter heading, claim, claim author/subject, cited position, conjectured warrant, source locator and approval; preserve quote unchanged.
2. Require two-stage reconstruction: (a) neutral, faithful paraphrase of argument with exact basis, (b) criticism. Do not permit inference to begin without the first stage.
3. Add a **reconstruction challenge**: the most convincing contrary reading of the *same author* and what in surrounding paragraphs could resolve it.
4. Version author approval, revision decision, open disagreement and `AI_PROPOSED_NOT_APPROVED` state.
5. Use minimal textual spans with enough immediate context; do not treat an isolated quote as a complete author position.

**Exit:** no silent AI-as-author substitution; source-anchored reconstruction can be accepted/corrected by author or reviewer, and edits do not silently propagate approval.

### WP-03 Jurisprudential inference (P2)

**Problem:** the current `normative_bridge: true/false` checks **presence**, not reasonableness, and does not evaluate whether an interpretation genuinely follows from sources.

**Build**
1. For **norms** require legal system, text/version, date, conditions, authority, derogations, norm conflict, alternative reading and applicability; separately represent `positive_law_assertion`, `normative_evaluation`, and `reform_proposal`.
2. For **concepts**, record concept versus conception versus stipulative definition, necessary/sufficient conditions if asserted, hard cases, immanent criticism and an explicit nonprescriptive outcome type.
3. For each transition `premise → conclusion` record the relevant inferential standard and substantive warrant, its authority, strongest objection and strongest defender response; a Boolean is insufficient.
4. A failure must identify a precise missing step and give the condition that would defeat the diagnosis; contested scholarly interpretation is not automatically a logical fallacy.
5. Add date-aware legal authority checks: P008 thesis (2014) must not be graded by a ruling delivered in 2015 without expressly changing the evaluation target.

**Acceptance challenge matrix:**
- P003: concept of standing → private-law standing rule; exemptions require separate source.
- P004: emerging legal concept → no mandatory reform.
- P005: biological ontology ≠ statutory invalidity.
- P006: legitimacy standard ≠ universally valid positive-law condition.
- P007: unenforceable/imperfect right ≠ automatic category contradiction.
- P008: thesis year versus subsequent precedent.
- P009: normative premises present, but substantive adequacy remains contestable.

**Exit:** against an expert-adjudicated comparison sample, no unsupported automated academic verdict; the tool asks legally material source-grounded questions, distinguishes negative and prescriptive outcomes, and records uncertainty.

### WP-04 Chapter-spine integration (P3)

**Build:** recover actual chapter headings/paragraph locators from source text; model `passage → proposition → subsection → chapter task → central thesis`; propagate any material norm/definition/warrant changes. Explicitly mark when a chapter is only background or when an author's position develops dialectically, rather than diagnosing every change as self-contradiction.

**Exit:** one change to a load-bearing definition generates the exact impacted paragraph and chapter IDs; changed claims and dependent approvals are marked `RE_REVIEW_REQUIRED`. Real authored chapter titles replace synthetic placeholders.

### WP-05 Scholarly validation (P4)

**Build:** source-authorized evaluation corpus of at least 20 **distinct, substantive argument passages** from multiple norm/concept dissertations (pilot candidates may supply leads, but their published availability alone does not establish permission to republish large passages). Have at least two independent trained legal/methodological reviewers annotate *where the author's argument is*, whether suggested defects are real, the best defense, and legal-source limits. Keep adjudicated disagreements, not only unanimous examples. Blind the model to reviewers' findings; report precision and recall of substantive defects against the adjudicated baseline, rate of ungrounded citations, attribution mistakes and false positives on critical or non-prescriptive conclusions.

**Exit:** publish **methods and aggregate metrics** with privacy safeguards; any acceptance threshold must be agreed before tuning, never cherry-picked after results. Failure case records drive engineering revisions.

### WP-06 Final novelty gate (P5)

**Build:** proposition-level comparison with actual prior research and verified legal sources. Provide exactly three classes:
- `normative`: new, justified normative criterion/order/reformulation;
- `interpretative`: defensible distinctive legal reading with meaningful consequence;
- `conceptual`: defensible clarification/redistribution of meaning and legal boundary.

The contribution's type is what the central defended thesis actually changes, not what object the work began with. **One primary, secondary optional.** Final verdict is held until internal, dialectical, chapter integration, defense and human approval complete. Missing texts ⇒ `INDETERMINATE` or `NOT_READY`, not a novelty score.

**Exit:** an explicitly complete source comparison matrix and documented strongest earlier scholarship; novelty abstention works on insufficient sources; no early certainty.

## 4. Engineering architecture (minimum viable, avoid premature platform)

```
Authorized local dissertation file & authoritative legal materials
        ↓
Source provenance + source-version verification (WP-01)
        ↓
Draft passage segmentation → author-faithful claim reconstruction (WP-02)
        ↓
Norm / Concept-specific inferential examination (WP-03)
        ↓
Objections + author decisions + argument graph (WP-03 / WP-04)
        ↓
Cross-chapter impact and defense rehearsal (WP-04)
        ↓
Independent evaluation and calibration (WP-05)
        ↓
FINAL three-type novelty comparison only (WP-06)
```

- **No need yet** for a hosted SaaS UI, web crawler, embeddings stack, large vector DB, local model service or large-scale automation; first close the source-grounding and fidelity gaps.
- **Public repo:** skill instructions, schemas, code, synthetic examples, legally reusable excerpt fixtures, regression tests and aggregate methods.
- **Private local workspace:** full dissertations if access terms permit, author drafts, source extractions, annotated passages, reviewer identifiers and confidential client material.
- Run deterministic checks in Python, interpretive assessment with the agent and researcher, independent validation with qualified legal reviewers. Retain the difference between their outcomes.

## 5. Workflow and decisions

| Stage | Entry | Mandatory output | Human decision |
|---|---|---|---|
| Intake | Norm/concept + legal system/usage | Authenticated research object | Researcher approves object |
| Source grounding | Edition/version, primary sources | Passages and exact locators or explicit uncertainty | Researcher/reviewer resolves unavailable text |
| Reconstruction | Original draft, source passages | Author-faithful proposition graph | Author confirms intended claim |
| Internal + dialectical review | Confirmed positions | Concrete objection, defense, repairs, open limits | Author accepts/rejects revisions |
| Integration + defense | Stable argument and chapters | Dependency rerun + defensible responses | Author acknowledges unresolved objections |
| Originality | Entire argument stable, compared literature | Normative/interpretative/conceptual contribution matrix | Qualified final review, no automatic grade |

## 6. Change-management acceptance checklist

Do **not** mark v0.5/v0.6 as substantively ready merely because GitHub Actions pass. Each release must link:
- a tagged schema/migration and maintained legacy regression tests;
- authorized source corpus and reproducible passage verifications;
- at least one **positive, negative and indeterminate** case per supported inferential pattern;
- the strongest rebutting scholarly interpretation and the researcher's response, if available;
- a documented limitation when original source or author confirmation is missing;
- no early novelty evaluation, no theory as research object, no mandatory norm reform.

## 7. Exact next action

**Implement WP-01 first**, not a novelty classifier or interface. Add source-version manifest, PDF/text locator verifier, test fixtures for incorrect page/quote/date and a reproducible result attached to CI. Then revisit P003–P009 with verified source text; only after this should human reviewers assess semantic fidelity. This makes the next phase empirically checkable rather than merely more elaborate documentation.
