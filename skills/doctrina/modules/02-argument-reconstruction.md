# Module 02 — P1 Author-Faithful Reconstruction

**Purpose:** reconstruct the **author's argument about a legal norm or concept** without altering its authorship, modality or inferential commitments. This is a prerequisite for serious internal criticism, not a theory-examination module or a novelty assessment.

**Binding sources:** actual authorized dissertation draft with original byte-preserving UTF-8 extraction; separate P0 verified primary-law/journal sources where relied upon. Do not claim direct source inspection from an agent-selected excerpt alone.

## Pass A — source-bound reconstruction (NO evaluation yet)

1. **Read context before classifying a claim:** the target passage AND its relevant adjacent passages, heading, quotation context and author reference. Capture the actual draft SHA, passage ID, exact Unicode quote span, line locator and document version.
2. **Classify voice separately from text:** "author", "opponent", "quoted_source", "hypothetical", or "uncertain". A position quoted by the author is not automatically accepted. Preserve reported speech, concessions, irony, negations, and the author's explicit rejection of rival claims.
3. **Classify mode:** "explicit", "paraphrase", "inferred", "question", or "conditional". Record the condition, uncertainty and potential cases where no assertion was made. An inferred hidden premise is NEVER an explicitly quoted author claim.
4. **Reconstruct a candidate proposition:** copy exact supporting quote, articulate a faithful proposed interpretation, list explicit and proposed premises separately, explain why the voice and modal classification seem warranted, and identify the **best rival reading of the same author**. Do not use external theory or source metadata to silently complete missing text.
5. **Check mechanically:** run scripts/fidelity_cli.py check against an **independent original draft**; a match with the self-contained JSON is insufficient. Any quote/hash/line/source-context discrepancy prevents promotion to approved.
6. **Request researcher decision:** present the original quote, full surrounding context, provisional interpretation, source locators, alternative reading, and linked premise/claim IDs. The researcher explicitly accepts, rejects or demands revision. Only an actual interactive local reviewer can record self-attested approval. Do not impersonate or automate consent.

## Pass B — argument review (only after Pass A)

1. Determine the dissertation's own claim, claim kind, backing and inferential warrant; distinguish legal validity, normative legitimacy, conceptual meaning and empirical consequences.
2. Examine the **strongest plausible reconstruction**, not the weakest sentence chosen by the reviewer. Test counterexamples, exceptions, legal authority, the author's reply to major objections, and any norm/concept-specific ambiguity.
3. Label findings as mechanically verified structure, a grounded substantive objection, a contestable interpretation, or a source/author-context uncertainty. **A failed P1 gate is a failure of evidence/approval, not proof that the author's thesis is false.**
4. Suggest minimal repairs or a defended alternative, but NEVER alter the author’s thesis and present it as their view without a new explicit decision.
5. Trace dependent premises, propositions and chapters. Revisions to the original draft, phrase, voice, mode, or any load-bearing premise invalidate earlier decisions and require new P1 checks.

## Technical review objects

- schemas/reconstruction-v1.schema.json: required P1 record and decision structure.
- scripts/doctrina_fidelity.py: deterministic source, quote-span, voice/approval relationship, dependency fingerprints and stale detection.
- scripts/fidelity_cli.py: start / propose / check / decide / sync. The decide operation refuses a non-interactive terminal.
- scripts/doctrina_cli.py check CASE --original-draft ORIGINAL: integrated P1 + graph review.
- docs/RFC-012-AUTHOR-FAITHFUL-RECONSTRUCTION.md: integrity rules and limitations.

The old provenance=researcher_approved or author_explicit field in a v0.4 JSON claim is **NOT itself approval**. New P1 case reviews require matching confirmed record, voice, mode, proposition and original source. Recorded decisions are *locally self-attested* (not a verifiable signature); separate scholarly validation of semantic accuracy remains mandatory.

**Output:** source-bound, proposed argument ledger; exact source-linked claim and premise IDs; honest ambiguity and objection; researcher decision record; dependent review status. Originality evaluation remains locked until the final dissertation gate.
