# DOCTRINA v0.4.2 — Author-Faithful Reconstruction and Approval Protocol

This is a **two-pass protocol for examining actual in-progress normative–conceptual legal dissertations**. Research objects are legal **NORMS or CONCEPTS**, never entire jurisprudential theories. P1 prevents the agent from confusing the author with an opponent, a quoted source, a hypothetical scenario or the agent's own hidden premise. It does not decide whose legal argument is ultimately correct.

## Before Pass A

- Obtain the author's authorized manuscript, original edition/version and actual draft text (prefer UTF-8 extracted with manual layout verification). PDFs/DOCX have to be converted and checked separately; no automatic conversion is implied.
- Confirm object scope (norm/concept) and source integrity of any decisive quoted authority via P0. Keep full private drafts and reviewer identities outside public GitHub.
- Initialize the local P1 case against the independent original file. All original character offsets and lines must match the same file; LF/CRLF and Unicode are retained exactly.
- The novelty categories (normative, interpretative, conceptual) remain unavailable for evaluation at this stage.

## Pass A — reconstruct, do not criticize

**A1. Exact target and context.** Determine what heading/chapter and passage make the text relevant. Extract its exact quote and codepoint positions, read immediately surrounding passages, and mark uncertainty caused by missing context.

**A2. Speaking voice.** Each candidate receives one provisional classification: author, opponent, quoted source, hypothetical, or uncertain. Quoting an opponent is not the same as accepting the opponent's argument. Note concession, irony, conditionality, rhetorical question and rejection markers when they may change commitment.

**A3. Assertion mode.** Classify explicit, paraphrase, inferred, question or conditional. Do not turn a question into a conclusion, a conditional into an unconditional position, or an AI-proposed hidden premise into an explicit author's assertion.

**A4. Meaning hypothesis.** Record the smallest plausible proposition, actual source phrase, source position, provisional voice reason, qualifiers, and premise IDs. Distinguish:
- what is stated in the original text;
- what is paraphrased as an interpretive proposal;
- what is merely inferred or added by the reviewer;
- what is a different author's position the dissertation discusses.

**A5. Strongest alternative reading.** Formulate the most charitable plausible rival explanation of what the SAME AUTHOR intended (not yet a rebuttal to the author). Resolve ambiguities from the surrounding text and actual inspected sources. If still uncertain, retain uncertain instead of selecting a convenient classification.

**A6. Source-bound review.** Run the fidelity checker on the independent original manuscript. A JSON-only match cannot establish source fidelity; quote, offsets, context and SHA must be consistent. Show researcher the actual source span and full proposed meaning, not just a status code.

**A7. Human confirmation.** The researcher chooses accept, reject or revise in an actual local interactive terminal. A token ties the decision to the exact source version, proposition, voice/mode, contextual passages and transitive premise dependency. A reviewer label and reason are required. This is self-attested, not independently identity-authenticated, and AI must not impersonate the human.

## Pass B — only then assess argument

Once author voice and intended meaning are confirmed, examine the norm/concept with a properly bounded standard of legal reasoning: interpretive method, normative source, temporal context, premises and inferential warrant. Construct the strongest fair counterargument and possible reply. Each criticism must include the precise passage, reconstructed proposition, legal basis, and any uncertainty; do not declare a fallacy because an AI-generated graph omitted a genuine premise.

The minimal repair remains a **proposal** until the author approves a revised thesis. Subsequent changes in any source text, proposition, mode or premise reopen dependent checks and invalidate prior approvals. Revision is not proof of scholarly inadequacy, and disagreement is not automatically logical error.

## Reviewer decision and gate states

- **PROPOSED:** source-bound reconstruction has not received a valid human acceptance.
- **RESEARCHER_CONFIRMED:** source and current hypothesis have a local interactive self-attested acceptance; semantic adequacy is still not independently certified.
- **RESEARCHER_REJECTED / REVISION_REQUESTED:** do not treat the proposed meaning as author-approved.
- **STALE_APPROVAL:** original document or a proposition/premise in the dependency closure changed after the decision.
- **SOURCE_INVALID / UNREVIEWABLE:** source/version/quote/voice/context/approval problem blocks using the record as confirmed.
- **SELF_ATTESTED_FIDELITY_ONLY (aggregate):** all current reconstructed entries were accepted locally; NOT a grade, accuracy metric, signature, or validation of normative warrant.
- **BLOCKED_SOURCE_OR_APPROVAL:** defects prevent claiming P1 fidelity; no inference that the underlying thesis is substantively false.
- **LOCKED:** final originality audit remains unavailable.

## Reproducible synthetic illustration

Run a private case with no implicit approval using the bundled code. It contains an author's conceptual claim, an opponent claim expressly rejected by the writer, and a conditional conclusion. All are provisional:

1. python scripts/demo_fidelity.py --out /tmp/doctrina-p1-demo.json
2. python scripts/fidelity_cli.py check --case /tmp/doctrina-p1-demo.json --draft examples/fidelity_draft_synthetic.txt
3. python scripts/doctrina_cli.py check /tmp/doctrina-p1-demo.json --original-draft examples/fidelity_draft_synthetic.txt

For real cases, use fidelity_cli.py start, then propose, check, human-only decide, and sync after a revision. Never commit full documents or case JSON containing sensitive dissertation prose to a public repository.

## Three things a compliant audit MUST report

1. The author's actual claim and its **specific source anchor**, with who said it, modal limits, and original manuscript version.
2. What the auditor believes is missing, **why**, and how a charitable reading could resist the charge; separate mechanical findings from legal-substantive objections.
3. The researcher's explicit decision (or absence), any invalidated dependent approvals, and the remaining source or academic uncertainty.

Consult the detailed implementation record: docs/RFC-012-AUTHOR-FAITHFUL-RECONSTRUCTION.md. Academic quality measurement still requires independent knowledgeable reviewers and genuinely source-grounded discourse, not just passing synthetic tests.
