# RFC-009 — DOCTRINA v0.4 Norm/Concept Reasoning Core

**Implementation target:** branch main, directly in the user-owned repository  
**Research domain:** doctoral **normative–conceptual** legal dissertation, focusing on legal **norms or concepts**, NOT theory-as-object  
**Prior baselines:** RFC-005 (internal review), RFC-007 (object scope), RFC-008 (three novelty types)  
**Release classification:** usable **structural/provenance prototype**, not a semantically validated legal examiner

## Implemented components

### 1. Object schema / scope enforcement (P0)

- JSON schema: schemas/case-v0.4.schema.json.
- Standard-library validator: scripts/doctrina_core.py.
- Only research_object.primary_type = norm or concept is valid. Theory is rejected as an object, though arguments may cite a theory in a limited instrumental role.
- Norm-specific fields: jurisdiction, temporal scope, authoritative legal_materials, source locator and direct inspection status.
- Concept-specific fields: actual located concept_usages, contested meaning, boundaries and legal significance.
- Missing source inspection produces a warning/review limitation. A declaration that a source was inspected is not itself proof.

The v0.4 JSON data model is **versioned**. Existing v0.3 ledgers can be migrated explicitly but are marked unanchored and need the original manuscript.

### 2. Draft passage intake + author-faithful argument reconstruction (P1)

- CLI init reads a **local UTF-8 text file**, preserves source passages verbatim with Unicode character offsets and line numbers and a SHA-256 hash of the input text.
- These passages are **not claims**. Segmentation does not infer meaning, premise, conclusion or theory.
- The SKILL.md/Module 02 agent workflow reconstructs actual claims from user-supplied draft with the researcher, recording author/opponent attribution, explicit or proposed premise, excerpt anchor, claimed inference and warrant.
- Proposed AI reconstructions MUST be marked provenance=ai_proposed and attribution=proposed. A proposed premise must never be silently passed as an explicit assertion by the researcher.
- The checker verifies claimed excerpts appear in the indicated original passage. It cannot verify that the reconstructed **paraphrase** is meaningfully faithful without researcher judgment.

### 3. Internal argument report (P2)

- CLI check combines the new v0.4 provenance/scope validator with existing v0.3 argument-graph lint for populated claims, preserving the old test suite and graph semantics.
- CLI report prints claim ID, author position, draft passage/lines, verbatim anchor, premises, warrant, researcher response, revision option and mechanical findings. If these are unknown it says so, rather than manufacturing them.
- Norm or concept review questions are included for specialist examination.
- The script reports defects and evidence gaps; does NOT decide legal validity, contested conceptual meaning, interpretive superiority, scholarly novelty or doctoral sufficiency.

### 4. Originality sequence locked

The internal v0.4 case contains originality.stage=locked, final_status=NOT_READY. Attempts to make an originality verdict during the internal review are flagged. The separate Module 07 continues to allow exactly one primary novelty type: normative, interpretative or conceptual. It remains the **last** stage after internal, dialectical, chapter integration, defense and researcher approval. The Python checker does not certify novelty.

## Local runbook (never publish unpublished dissertation passages)

From the repository root:

    python scripts/doctrina_cli.py init \
      --input examples/dissertation-draft-synthetic.txt \
      --object concept --title "Kepentingan umum" --locus "ilustrasi" \
      --out /tmp/doctrina-case.json

    python scripts/doctrina_cli.py check /tmp/doctrina-case.json
    python scripts/doctrina_cli.py report /tmp/doctrina-case.json --out /tmp/doctrina-review.md

Manually/with the agent and researcher's verification, populate claims in the JSON case. Run check and report again. The initial case has RECONSTRUCTION_PENDING because no genuine author assertions were yet identified. This is normal and **not** an error in the dissertation.

To migrate an old, already prepared v0.3 ledger:

    python scripts/doctrina_cli.py migrate \
      --input examples/kepentingan-umum-illustrative.json \
      --object concept --title "Kepentingan umum" --out /tmp/doctrina-migrated.json

Review its original missing manuscript anchors before relying on any of its argument claims.

Regression tests:

    python -m unittest discover -s tests -v

On push to main, GitHub Actions (.github/workflows/test.yml) is configured to run the regression suites and a synthetic CLI smoke test, if Actions is enabled for this repository.

## Result categories / interpretation

- DRAFT_RECONSTRUCTION_REQUIRED: source was ingested but no defensible claim reconstruction exists.
- INTERNAL_REVISION_REQUIRED: one or more **mechanically detected critical** scope, provenance or graph flaws; does not independently establish a substantive logical fallacy.
- STRUCTURAL_REVIEW_WITH_LIMITATIONS: records exist but warnings/source uncertainty remain.
- STRUCTURAL_REVIEW_COMPLETE_NOT_SEMANTICALLY_VALIDATED: no declared mechanical findings in available text; not scholarly clearance.

## Safety and research integrity

1. Store full unpublished drafts in local/private work areas, NOT in the public DOCTRINA repository. .gitignore helps only if files follow the excluded patterns; never assume it prevents all accidental publication.
2. Prefer licensed/open material for repository examples; current example is purely synthetic.
3. A source's bibliographic metadata is not verification of its substantive argument.
4. Original PDF/DOCX conversion is NOT part of this CLI. Convert a draft to UTF-8 text with suitable tools and inspect the conversion. Scanned sources may require human verification.
5. A correct source locator does not prove that a legal interpretation or normative bridge is sound.
6. A full dissertation may contain legitimate interpretive circularity or a critical aporia; neither is a formal fallacy merely because graph structure looks cyclical.
7. Expert and researcher review remains essential for norm validity, concept boundary interpretation, alternative readings, legal consequences and novelty.

## Known implementation limitations

- The CLI is not an autonomous semantic legal-reading model. The deployed skill can conduct the reconstruction conversationally, but its proposed claims still need author confirmation.
- Passage segmentation currently uses blank-line paragraph boundaries; headings, footnotes and complex DOCX/PDF layouts require preprocessing and validation.
- Source-state labels and readiness approvals are declared values, not independently authenticated digital signatures.
- The old deterministic graph linter continues its older taxonomy and cannot infer missing legal implications from prose on its own.
- No confidential unpublished dissertation has been inserted into the public repository.
- Test count measures structural regression only, NOT academic reliability.

## Next non-automatable research validation

Acquire researcher-authorized norm/interpretation/concept excerpts from active doctoral research. Have at least two expert reviewers independently annotate intended propositions, inferential objections, hard cases and reasonable alternative interpretations. Record false positives and failure cases. Only then can DOCTRINA make claims about diagnostic quality.
