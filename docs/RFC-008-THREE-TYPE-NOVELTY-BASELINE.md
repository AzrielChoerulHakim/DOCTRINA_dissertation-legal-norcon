# RFC-008 — DOCTRINA Contribution Architecture: Three Novelty Types

**Status:** ACCEPTED AS DESIGN BASELINE — instruction-level only, NOT validated academic novelty classifier  
**Date:** 25 November 2026  
**Supersedes:** any open-ended novelty classifications in older RFCs.  
**Depends on:** [RFC-007](RFC-007-NORM-CONCEPT-SCOPE.md): research object is exclusively a legal **norm** or legal **concept**.  
**Sequence rule:** final originality review always occurs **after** internal argument examination, dialectical stress, dissertation integration, defense rehearsal and researcher's provisional sign-off.

## 1. Scope decision

Exactly three contribution types are recognized for the **final originality audit**:

1. **NORMATIVE NOVELTY** (novelty_type: normative): a defensibly justified original normative construction, criterion, ordering, resolution, or proposed reformulation relevant to the examined norm/concept. A suggestion to change statutory text is neither necessary nor sufficient.
2. **INTERPRETATIVE NOVELTY** (novelty_type: interpretative): a distinct, well-supported legal interpretation or interpretive method applied to an identified norm/concept that yields a meaningful difference relative to the strongest existing readings. Simply disagreeing with precedent or scholarship is not enough.
3. **CONCEPTUAL NOVELTY** (novelty_type: conceptual): a defensible clarification, delimitation, differentiation, or reconstruction of an identified **legal concept**, resolving a demonstrable conceptual difficulty. It need not invent a new term or general theory.

**No fourth novelty type** is a separate output class in DOCTRINA. More general labels (empirical, methodological, theoretical, technological, interdisciplinary, philosophical) may contextualize the **method and support**, but are not used as novelty categories for this narrow dissertation skill. The categories are **DOCTRINA's operational taxonomy**, not a universal or formally mandated jurisprudential taxonomy.

An approved dissertation selects **exactly one primary type** for the contribution it eventually claims. A secondary type is permitted only if independently justified. An object classified as \`norm\` may yield an interpretative or conceptual contribution; an object classified as \`concept\` may yield a normative or interpretative contribution. Do not conflate research-object type and novelty type.

## 2. Contribution chain: what has to be proven

For each **proposed** contribution, the reviewer must be able to trace:

\`\`\`
Identified legal norm or concept
  → real doctrinal / interpretative / conceptual problem
  → author-stated thesis and defended premises
  → adequate inferential and source warrants
  → serious opposing reading / challenge addressed
  → stable effects on chapters and legal implications
  → comparison against actual inspected prior propositions
  → bounded conclusion about contribution
\`\`\`

A grammatically novel formulation, a different title, a new combination of names, or a statute not previously studied is **not** evidence of substantive novelty. Absence of search results is not proof of originality. If primary legal materials or opposing scholarship are unavailable, mark the final assessment indeterminate.

## 3. Review tests by type

| Type | Necessary questions | Failure patterns |
|---|---|---|
| **Normative** | What concrete normative problem? What proposed norm, criterion or justifiable ordering follows? Which valid legal sources/principles and normative premises support it? How would exceptions and affected legal positions change? | Restatement of existing law; policy preference without normative bridge; unsupported universal remedy; confusion of law in force with law as proposed. |
| **Interpretative** | Which exact norm/concept and contested passage? What is the author’s interpretation, which interpretive method justifies it, and why is it more adequate than strongest alternatives? What changes in legal consequences? | Unmotivated alternative reading; selective quotation; failure to consider legal hierarchy/time; interpretation disconnected from the source. |
| **Conceptual** | What legal concept and conflicting usages are at stake? How does the author clarify boundary or differentiate conceptions? Which difficult cases become more intelligible? What legally material implications follow? | Renaming without resolving a problem; changing meanings unnoticed; reproducing an existing conception as a purported new concept; requiring a general new jurisprudential theory. |

The rubric is **proposition-level, qualitative and source-bound**; no pseudo-objective originality percentage or score.

## 4. Final originality module contract

**Prerequisites (all required):**
- Research object accepted under RFC-007.
- The author’s central claims are adequately reconstructed from actual inspected draft text and approved by the researcher.
- Internal argument review has no known unaddressed **foundational** defect (in inspected scope).
- Major dialectical objections have reasoned responses or acknowledged limits.
- Dissertation chapter dependencies have been re-reviewed after material changes.
- Defense rehearsal includes actual researcher responses or a clearly marked absence; unaddressed foundational weaknesses block final audit.
- Researcher explicitly authorizes the **final** contribution comparison.
- The source corpus is disclosed with jurisdictions, relevant dates, text access and search boundaries.

**Deliverables:** (i) stabilized thesis proposition IDs; (ii) exact prior-research propositions, with verified text locators; (iii) proposition-by-proposition difference matrix; (iv) one primary and optional independently supported secondary novelty type; (v) substantive justification and legally material consequence; (vi) strongest outstanding objections and coverage limitations.

**Permitted final statuses:**
- \`NOT_READY\`: prerequisites missing; DOCTRINA must not imply that novelty assessment occurred.
- \`CANDIDATE\`: a claim has been formulated but not yet sufficiently compared.
- \`SUPPORTED_WITH_LIMITATIONS\`: bounded proposition-level evidence supports a contribution, subject to stated limits.
- \`INSUFFICIENTLY_SUPPORTED\`: examined evidence does not substantiate the claimed new contribution.
- \`INDETERMINATE\`: source access, scope of comparison, or academic disagreement prevents a justified determination.

A supported contribution is **not** a decision that a university will accept the dissertation; examiners and supervisors retain authority.

**Re-entry loop:** if final comparison shows that the supposedly novel proposition was already available or materially dependent on an unexamined source, re-open argument construction and integration, then repeat final audit only after review. Do not relabel novelty to evade the problem.

## 5. Explicitly not early-stage novelty testing

Reviewing prior research from the beginning remains mandatory for accurate interpretation, doctrinal genealogy and criticism. Earlier stages may keep a **non-evaluative comparison ledger** of known claims, but **no primary novelty determination** may be certified until the final gate.

The final taxonomy may be used as **planning vocabulary** at the beginning ("possible contribution") but must be tagged \`tentative / unevaluated\`. This avoids a workflow that invents novelty early and then forces the dissertation to fit it.

## 6. Implementation priorities

1. **P0 / Object schema:** Require \`research_object.primary_type: norm | concept\`, text/source locator and review scope. Schema migration and tests; preserve existing v0.3 examples.
2. **P1 / Two jurisprudential object analyzers:** Norm-source status, interpretive alternatives and exceptions; concept uses, definitions, boundaries and hard cases.
3. **P2 / Semantic argument examiner:** Author-faithful parsing of real draft passages with explicit provenance and justified changes in claim type, not merely JSON connections.
4. **P3 / Argument spine / revision impact:** Each change of definition, norm, premise or claimed legal consequence triggers dependent chapter re-review. Prevent automatic inheritance of prior review approvals.
5. **P4 / Adversarial and human validation:** Human-rated cases covering real normative / interpretative / conceptual argument quality and misclassification false positives.
6. **P5 / Last-gate originality classifier:** Implement exactly three types and statuses above, subject to prerequisites and actual inspected scholarship. Never claim independent truth/certification from an LLM.

### Three acceptance fixtures (illustrative, not law findings)

- **Normative candidate:** a justified additional limiting condition for use of a public-interest norm; test legal authority, competing premises, consequences and whether the condition is already known.
- **Interpretative candidate:** a different defensible reading of an ambiguous provision yielding a distinct legal consequence; compare textual, systematic and other method-appropriate reasons with the strongest earlier interpretations.
- **Conceptual candidate:** a clear, defended separation of state interest, government interest and public interest as legal conceptions in a specified legal context; compare prior definitions and address hard cases.

Each example must have a corresponding **non-novel or inadequately defended negative case**, plus an **indeterminate case** that contains insufficient source access. The checker must avoid declaring success just because the form is complete.

## 7. Epistemic and data safeguards

- No unpublished dissertation text in this public repository without express author permission and suitable privacy controls.
- Source quotation must be exact and checked at the cited passage/edition; source absence must be disclosed.
- Theories are **tools** for norm/concept analysis, never a primary research object or a required theoretical invention.
- The current Python script \`scripts/audit_argument_graph.py\` is a deterministic structural linter and **does not classify academic novelty**.
- This RFC changes the DESIGN BASELINE only. No schema, runtime capability, CI or expert validation is silently claimed to have been delivered.

## 8. Design decision

> **DOCTRINA evaluates the defensibility of an author's arguments about legal norms or legal concepts first. At the final stage only, it evaluates the bounded contribution of the stabilized thesis under one of three labels: normative, interpretative, or conceptual.**

This preserves methodological focus and makes the final novelty classification responsive to actually demonstrated scholarship rather than marketing language.
