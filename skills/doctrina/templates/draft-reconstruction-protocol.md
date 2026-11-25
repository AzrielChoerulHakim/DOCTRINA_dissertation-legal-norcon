# DOCTRINA — Draft-to-Argument Reconstruction Protocol (Agent / Researcher)

This protocol is **the semantic reasoning step** for v0.4. The Python CLI only identifies text passages and checks structure/provenance. No external LLM or data service is required.

## Preconditions
1. Confirm research object = legal norm or legal concept. If it is a philosopher's complete theory, do not route to DOCTRINA.
2. Read the supplied text and retain exact passage ID, line locator, unmodified source wording and document version.
3. Never treat a speculative AI-proposed premise as an author-endorsed fact.

## Procedure

For each substantively relevant passage:

A. Record **author's exact claim**, if explicit, with passage ID and a verbatim anchor copied precisely from original text.
B. Separate the author's thesis from cited scholarly positions, opponent claims, hypothetical examples and descriptive legal statements.
C. Identify explicit premises, inferential warrant and conclusion. If some are not explicit, generate **hypotheses** with provenance=ai_proposed and attribution=proposed.
D. Distinguish doctrinal/positive-law claim, conceptual clarification, interpretive claim, normative proposal and empirical claim. The entire dissertation must have a real legal norm or concept as its object.
E. Identify scope and conditions: jurisdiction, legal validity timeframe, text version, exception, concept/conception, and relevant authority.
F. Identify the **single most dangerous inferential weakness** supported by the passage; show precisely what premise or warrant is missing.
G. Offer the **strongest fair possible researcher reply**, a minimal repair and an optional stronger reconstruction, clearly labeled suggestions—not endorsed text.
H. Trace downstream argument/chapter impact. Ask researcher to accept/reject/refine before marking material as approved.

## Safe v0.4 JSON annotation example

The following fields are added to each element in the case's claims array after verifying the draft (replace placeholders; never fake them):

    {
      "id": "C1",
      "kind": "conceptual",
      "role": "derived",
      "text": "Faithful claim statement (verified by researcher)",
      "passage_id": "T0001",
      "anchor_text": "Exact verbatim excerpt copied from T0001",
      "attribution": "author",
      "provenance": "author_explicit",
      "premises": ["P1"],
      "warrant": {
        "text": "The author's stated warrant, not the AI's guess",
        "normative_bridge": false
      },
      "inference": "interpretive",
      "chapter_id": "CH1",
      "quotes": [],
      "support": []
    }

If the researcher has not confirmed an AI-suggested interpretation, use attribution=proposed and provenance=ai_proposed. If an explicit direct quotation is asserted, its anchor must be verbatim. The JSON syntax above is illustrative only.

## Required output to the researcher
- Faithful map of claims and **their exact locations**.
- Reasons for each diagnosis; distinguish mechanical checks from substantive critique.
- Strongest objection and charitable defense.
- Two possible author-controlled revisions, including a minimal one.
- Unknown or unexamined source passages and legal versions.
- Downstream chapter dependencies and decisions still pending.
- A reminder that no novelty verdict is permitted before the final gate.
