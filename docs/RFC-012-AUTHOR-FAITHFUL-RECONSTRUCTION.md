# RFC-012 — DOCTRINA P1 Author-Faithful Reconstruction Layer

**Status:** IMPLEMENTED AS A SOURCE-BOUND / RESEARCHER-CONTROLLED MECHANICAL GATE; **semantic fidelity validation remains pending independent academic reviewers**.  
**Release:** v0.4.2, 25 November 2026.  
**Object constraint:** legal **norm** or **legal concept** only (RFC-007). Legal or philosophical theories may be analytical instruments, not research objects.  
**Originality:** always LOCKED here; final categories only normative, interpretative, conceptual (RFC-008).  
**Previous P0 prerequisite:** [RFC-011 original-source grounding](RFC-011-SOURCE-GROUNDING.md).

## 1. Fundamental failure this phase addresses

Previous v0.4 graph data allowed JSON fields \`provenance=author_explicit\` or \`researcher_approved\` to appear **without evidence that the researcher approved them**. An AI-generated paraphrase could be mistaken for the writer's thesis, and an overlooked premise could make a sound argument look formally defective (\`IA-06\`). A phrase matching an auditor-selected source excerpt did not establish that the voice behind the phrase belonged to the dissertation author.

P1 therefore prioritizes *fidelity before criticism*: preservation of original wording, independent rechecking against the actual draft bytes, attribution/voice distinction, provisional AI proposals, and human decisions that expire when the source or its inferential dependencies change.

## 2. What was implemented

### Core and integration

- \`scripts/doctrina_fidelity.py\` — P1 record model, original-file SHA-256 and Unicode-span verification, nearby passage context, author vs opponent vs source quotation vs hypothetical vs uncertain voice, explicit/paraphrased/inferred/question/conditional mode, approval fingerprints, dependency-based invalidation, report statuses.
- \`scripts/fidelity_cli.py\` — local-first \`start\`, \`propose\`, \`check\`, \`decide\`, \`sync\` workflow. **The approve/reject/revise command requires an actual interactive terminal**. Noninteractive execution is rejected to prevent automated scripts or AI from silently self-attesting as the author.
- \`schemas/reconstruction-v1.schema.json\` — versioned \`reconstruction.protocol=1.0\` contract. A P1 object is an **optional strict extension** of the existing \`case-v0.4\` format; earlier fixtures continue to run as structural-only legacy examples, but do not qualify as having passed P1.
- \`scripts/doctrina_core.py\` / \`scripts/doctrina_cli.py\` — when a \`reconstruction\` block exists, audits **fail closed** if the independently supplied original draft is absent or its hash differs. Existing graph assertions cannot silently inherit author approval; the same text, voice, explicitness and live attestation must match.
- \`tests/test_fidelity_p1.py\`, \`tests/test_fidelity_core_integration.py\`, \`tests/test_fidelity_p1_hardening.py\` — original-source, source-hash, speaker-role, hidden-premise, quote-span, disputed context, repeated quote, TTY, revision, graph drift, and dependency tests.

### Invariants

1. **Never infer claims from paragraph segmentation.** P1 proposals are entered explicitly and remain unapproved until a researcher accepts them.
2. **Every extracted claim has an exact original quote span** in the independently provided UTF-8 draft. Passages' character offsets, line positions and verbatim bytes are rechecked against the original.
3. **Provenance and voice are separate.** Quoting an opponent does not mean adopting that opponent's thesis; a question is not an assertion; a conditional proposition must retain its qualifier.
4. **Semantic content remains explicitly provisional.** Source SHA, quote-span and string equality cannot establish whether the proposed paraphrase faithfully represents the author's meaning.
5. **Review decisions are version-bound.** Fingerprints include the full source hash, reconstruction record and transitive premise dependencies. A revised draft or premise causes earlier decisions to become stale.
6. **No synthetic human approvals.** Programmatic test fixtures simulate decisions but are not real endorsements; production CLI only permits local interactive self-attestation. This is **not** verified identity, digital signature or a claim of compliance with any legal electronic-signature standard.
7. **Previously approved case graphs cannot override P1**: altered propositions, external voice recast as author, questions made assertions, unqualified conditionals, or missing live confirmation result in findings.
8. **Open interpretive disputes are not deemed logical errors.** The engine validates the record's integrity and declared ownership of an assertion, not the philosophical truth of premises.

## 3. Required two-stage human/AI argument review

### Pass A — descriptive author-faithful reconstruction (NO evaluation)

For a selected paragraph, record:

- literal quote, exact offset, actual chapter/location and nearby context;
- voice: author / opponent / quoted source / hypothetical / uncertain;
- mode: explicit / paraphrase / inferred / question / conditional;
- proposition as a **proposed interpretation**, including scope and qualification;
- its stated premises and any proposed hidden premise as a **separate, explicitly provisional** record;
- the strongest reasonable alternative reading of what the **author meant**, especially if a cited opponent is quoted or rejected.

A reviewer must first decide whether Pass A is actually faithful to the source. **Do not** take an empty approval field as consent.

### Pass B — argumentative assessment only after fidelity review

Now examine the specific legal norm or concept, inferential warrants, contrary interpretations, source versions, jurisdiction, material qualifications, and possible consequential chapters. Identify a defect only if it is still present after reconstructing the strongest charitable reading. The most severe problem must be traceable to a specific claim and supporting original passage, not merely a label from the graph linter.

The P1 code **cannot automate Pass A's semantic attribution** nor Pass B's substantive jurisprudential adequacy. It enables a reproducible record and prevents false claims of automated validation.

## 4. Local working example (all sensitive work remains off-repository)

Starting from a v0.4 case produced by \`scripts/doctrina_cli.py init\`:

\`\`\`bash
python scripts/fidelity_cli.py start \
  --case /private/case.json --draft /private/dissertation.txt \
  --out /private/p1-case.json

# Inspect actual paragraph and find the precise Unicode character offsets.
# The quote, voice classification and propositional interpretation must be reviewed.
python scripts/fidelity_cli.py propose \
  --case /private/p1-case.json --id P1 --passage T0001 \
  --span-start 0 --span-end 20 --quote "ACTUAL 20 CHARACTER QUOTE" \
  --voice author --mode explicit \
  --proposition "Proposed faithful reconstruction" \
  --voice-basis "Reason this is the author's own voice" \
  --context T0001 --out /private/p1-proposed.json

python scripts/fidelity_cli.py check \
  --case /private/p1-proposed.json --draft /private/dissertation.txt \
  --format markdown --out /private/p1-review.md

# ONLY the real researcher runs this interactively, reads displayed source/
# proposal and types the claim-specific confirmation token.
python scripts/fidelity_cli.py decide \
  --case /private/p1-proposed.json --draft /private/dissertation.txt \
  --id P1 --reviewer "Researcher" --decision accept \
  --reason "Source and proposed meaning checked" \
  --out /private/p1-reviewed.json

# Unified graph + P1 check always requires the same external original file:
python scripts/doctrina_cli.py check /private/p1-reviewed.json \
  --original-draft /private/dissertation.txt
\`\`\`

All quoted arguments in examples above are **placeholders**, not an assertion about a real law or thesis. To edit a draft, update the input text and run \`fidelity_cli.py sync\` to produce a new version; the previous approvals remain on record but are **stale**. A record or premise revision also needs new explicit confirmation.

## 5. Cases that P1 must explicitly decline to certify

- A quotation matches the model's own sample but not the original draft: **BLOCKED**.
- The original source is missing, whose file hash differs, or whose line/character offsets are inconsistent: **BLOCKED**.
- A model-generated claim is entered as \`author_explicit\` without a source-anchored, confirmed match: **BLOCKED** when P1 is present.
- A speaker's opponent or cited source is treated as the dissertation author's own opinion: **BLOCKED**.
- A question becomes an asserted conclusion, or an antecedent is omitted from a conditional claim: **BLOCKED**.
- A confirmed proposition or any of its premises changes: prior approval is **STALE**, including dependent claims.
- The author rejects the reconstruction: state **RESEARCHER_REJECTED**; do not improve the argument under the author's name.
- An acceptable record that has not been reviewed: **RESEARCHER_REVIEW_REQUIRED**, not a pass.
- A claim that is explicit but supported by a mistaken legal interpretation: P1 can confirm voice/source but **cannot** establish correctness; P2 is needed.

## 6. Current release evidence versus remaining validation

P1 automated tests test integrity and behavior using **synthetic** paragraphs with explicit intentionally wrong conditions. The existing published dissertation excerpt batch remains **unapproved by original authors**. DO NOT retroactively relabel those prior pilots as author-verified or semantically sound.

**Implemented P1 code exit:** source and role fields stay traceable; approvals tied to version/fingerprint; non-tty command refusal; old graph checks remain compatible; GitHub Actions runs all regressions.

**Not yet satisfied as an academic acceptance gate:** independent original-author confirmations on real unpublished text (or a competent researcher's actual review), blinded double-annotation, inter-reviewer disagreement adjudication, and measured fidelity precision/recall. Those belong in P4 validation after P2 and P3 development. An absence of these measurements must be visible on reports, not silently implied.

## 7. Next priority

Follow [RFC-010](RFC-010-POST-BATCH-DEVELOPMENT-PLAN.md): **P2 Norm/Concept Justification Examiner**. Its work must begin from **accepted P1 records**, not raw unverified model reconstructions; test normative bridges substantively with sources and strongest available objections, while avoiding invented universal legal claims or mandatory theory-building.
