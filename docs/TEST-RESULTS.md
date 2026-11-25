# DOCTRINA v0.3 — Test and Verification Record

**Date:** 25 November 2026  
**Test environment:** Python 3 (standard-library unittest). No external model, PDF corpus, database, or scholarly examiner is involved.

## Recorded mechanical results

| Item | Observed | Interpretation |
|---|---|---|
| Unit tests | **18/18 passed** (`tests/test_argument_graph.py`) | The expected mechanical rules produced the expected outputs on synthetic fixtures. |
| Normal in-progress example (`draft`) | `DRAFT_IN_PROGRESS`, 0 critical, 1 review | Open major objection does not silently become resolved. |
| Flawed synthetic reasoning (`draft`) | `INTERNAL_REVISION_REQUIRED`, 1 critical | A derived normative conclusion with no normative premise/bridge is flagged as IA-06. |
| Premature novelty request (`pre-originality`) | `ORIGINALITY_REVIEW_INCOMPLETE`, 6 critical | Pending reviews, open objection, and lack of researcher approval block routing to final novelty evaluation. |
| Revision of premise P2 | Downstream `C1`; chapters `CH1`, `CH2` | Changes are explicitly traced to affected chapter contracts. |
| Scholarly expert-reviewed real-draft tests | **0 executed** | This implementation is not validated for substantive doctoral judgments. |

The log is `unit-test-log.txt`. Deterministic demonstration machine outputs are `demo-flawed-report.json`, `demo-impact-report.json` and `demo-originality-gate.json`.

## Exact command

```bash
cd doctrina_v0_3
python -m unittest discover -s tests -v
python scripts/audit_argument_graph.py examples/flawed-normative-leap.json --mode draft
python scripts/audit_argument_graph.py examples/kepentingan-umum-illustrative.json --mode pre-originality
python scripts/audit_argument_graph.py examples/kepentingan-umum-illustrative.json --impact P2
```

The deliberately failed lint examples exit nonzero (`2`) **by design**. They are not failing unit tests.

## Strong limitations

- Python cannot infer conceptual contradiction, genuine validity, jurisprudential correctness, or whether an objection is actually defeated; it only checks explicitly recorded relationships and declarations.
- A declaration `readiness.internal_review = passed` is not evidence that expert review occurred. Manual and scholarly review is required before any real project can be marked ready.
- The synthetic premise and argument are not sourced assertions of Indonesian positive law.
- Source locators are structurally checked, not verified against original source bytes in this build.
- Novelty is never computed by this linter. The final gate simply decides whether **to start** a separate qualified contribution analysis.

## Release-blocking acceptance before v1

1. Use real authorized passages from an ongoing dissertation and retain source-specific anchors.
2. Have the researcher judge whether the reconstruction matches intended arguments.
3. Have a qualified reviewer independently assess the most serious internal findings, including false positives.
4. Verify that changing a chapter's vital premise causes appropriate downstream review and does not rewrite author's intention.
5. Verify the originality audit only runs once the preceding substantive checks have passed, without asserting originality by absence of matches.
