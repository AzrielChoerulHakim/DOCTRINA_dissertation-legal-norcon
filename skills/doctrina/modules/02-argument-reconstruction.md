# Module 02 — Faithful Argument Reconstruction

**Input:** verbatim draft passage(s) and exact locations; candidate passages produced by the v0.4 CLI are NOT yet claims. If the original text is unavailable, any reconstruction remains provisional. Read ../templates/draft-reconstruction-protocol.md before annotating.

For each argument unit:
1. Copy exact relevant passage (or label faithful paraphrase), distinguish author's claim from literature cited and rival views.
2. Identify **claim**, **claim_kind**, **premises**, **warrant**, **backing**, **qualifier**, **conditions of applicability**, **inference_kind** and **objection**. Record passage_id, matching exact anchor_text, attribution and provenance. An AI conjecture is attributed proposed / ai_proposed, never author_explicit without an exact inspected author passage.
3. Identify senses of contested concepts (e.g., legal validity vs moral legitimacy). Never conflate concept and conception.
4. Mark domain: jurisdiction, timeframe, institutional and theoretical assumptions.
5. Trace which later conclusions depend on this unit; create stable IDs even when the prose changes.
6. Record exact page/heading/chapter locators in the researcher's draft and source locator, when actually inspected.

**Output:** Argument Review Card plus `argument-ledger` items and a concise author-voice reconstruction.

**Failure:** writing a stronger argument in the author's name without indicating it was reconstructed or approved.

**Scope:** a legal norm or legal concept only. Argument reconstruction is an agent/researcher reasoning task, not automatic paragraph segmentation. Substantive fidelity remains subject to the researcher's confirmation.
