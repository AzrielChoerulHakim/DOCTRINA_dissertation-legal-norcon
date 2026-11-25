# RFC-011 — DOCTRINA v0.4.1 Original-Source Grounding Implementation

**Status:** implemented source-integrity *mechanics*, subject to source-specific, pinned-original integration evidence.  
**Prior design:** [RFC-010](RFC-010-POST-BATCH-DEVELOPMENT-PLAN.md), Work Package 01 (P0).  
**Research scope:** dissertation on **legal norm or legal concept** only. Normative, interpretative and conceptual novelty remain final-stage concerns.

## Verified original-source integration evidence

Fresh, separate GitHub Actions execution after committing source pins:

- **Edinburgh University PhD dissertation (McMillan, 2018)** — original PDF downloaded from the official university bitstream; SHA-256 `e2334f05eed785d95ffa4fd8a25adc798ba34fe7657e457d9ca53dc51294b706`, **PDF page index 1**, short title excerpt matched `VERIFIED_EXACT`.
- **Court of Appeal judgment *MGN v Gulati* (2015)** — original PDF downloaded from judiciary.uk; SHA-256 `c5b738a70d81f0d0f7242cc78d85b68d4768e792018742f8a3be6d9fdae91e81`, **PDF page index 0**, neutral citation excerpt matched `VERIFIED_EXACT`.

Previously pinned hashes/page indices: [source manifest](../sources/public-originals-pinned.json). **Independent fresh retrieval verification:** [GitHub Actions 45572099628](https://github.com/AzrielChoerulHakim/DOCTRINA_dissertation-legal-norcon/actions/runs/45572099628), with log entry `COMMITTED_PIN_VERIFICATION PASSED`.

Other attempts: Oxford open repository returned HTTP 403; Durham URL returned HTTP 404; Edinburgh Downey source was accessible but the selected title excerpt had not been anchored to a unique PDF page. These cases were **not counted as verified**. Their failures do not invalidate the two independently pinned examples.

**Important precision:** the two pinned excerpts are short source-identification passages. They verify source-byte/page/quotation infrastructure, **not a thesis's substantive inferential warrants or the applicability of the court ruling to a specific legal claim**.

## What has been implemented

- \`scripts/verify_sources.py\`: **offline** original-source verification for local UTF-8 sources and local PDF files with extractable text (via \`pypdf\`). No OCR, network, upload, discovery service or source corpus is bundled. 
- \`schemas/sources-v1.schema.json\`: explicit metadata for source ID, official repository URL, source file, SHA-256, edition, legal system, legal applicability *claim*, retrieval date, extraction method, 0-based PDF page index, separately declared printed page, exact original excerpt and assessment state.
- \`tests/test_source_grounding.py\`: 20 mechanical controls involving generated synthetic original PDFs; including wrong original hash, wrong page, wrong quote, missing/corrupted PDF, image-only document, path traversal, unpinned source, Unicode/whitespace normalization and legal-validity overclaim checks.
- \`scripts/verify_published_sources_ci.py\`: **CI-only public-source integration trial** that downloads selected openly published university dissertations and a Court of Appeal PDF into the GitHub runner's temporary directory and reports hashes, page discoveries and failures. **Original PDFs are never uploaded to the repository or CI artifact.**
- \`.github/workflows/test.yml\`: runs mechanical unit tests and optionally attempts real-source integration. Its network integration step uses \`continue-on-error\` so temporary access failures do not falsify the status of deterministic regression tests. **Inspect its own step conclusion and attached evidence before asserting verification succeeded.**

## Verifier trust states

| Output | Exact meaning | Does not prove |
|---|---|---|
| \`VERIFIED_EXACT\` | The provided excerpt occurs **verbatim** on the specified PDF page (or text source), and PDF/text bytes match a provided SHA-256. | The author's interpretation is fair; law was valid on a stated date; the entire source has been examined. |
| \`VERIFIED_NORMALIZED\` | The excerpt matches after **conservative** Unicode normalization, line-hyphen removal or whitespace collapse; byte hash and page location match. | Exact glyph placement or meaning beyond the located text. |
| \`PARTIAL\` | A candidate match is found but a source byte hash or page locator is not pinned, or the source has no searchable text. | That the passage can already substantiate a scholarly conclusion. |
| \`UNVERIFIED\` | Source unavailable, text not found on declared page, wrong hash, unsafe path, invalid format or other blocking integrity error. | That source necessarily fails to support the claim; it could be an extraction/access failure. |

**Crucial distinction:** a SHA-256 calculated **and accepted in the same first run** demonstrates integrity of the local copy at that moment. It is not yet an independently pinned source identity. A researcher or CI must separately record the expected digest and page in a **versioned manifest**, then verify a fresh retrieval against those pins.

## Local runbook

Only source files that may legally be accessed should be used. Put original files in a private or local directory, never public GitHub.

Create a source manifest containing the original source's *previously pinned* hash, PDF page index and a short exact excerpt:

\`\`\`json
{
  "sources": [
    {
      "source_id": "DEMO-01",
      "source_kind": "thesis_pdf",
      "repository_url": "https://university.example.edu/example-record",
      "local_path": "local-thesis.pdf",
      "content_sha256": "REPLACE_WITH_64_HEX_SHA256",
      "retrieved_at": "2026-11-25",
      "publication_year": 2020,
      "edition": "published university repository PDF",
      "extraction_method": "pypdf",
      "page_index": 1,
      "printed_page": "i",
      "anchor_text": "REPLACE_WITH_EXACT_BRIEF_EXCERPT"
    }
  ]
}
\`\`\`

Run:

\`\`\`bash
python -m pip install 'pypdf>=4,<8'
python scripts/verify_sources.py \
  --manifest private-source-manifest.json \
  --source-root private-originals \
  --out private-source-verification.json

python -m unittest discover -s tests -v
\`\`\`

The program exits nonzero when a source is \`UNVERIFIED\`. An \`PARTIAL\` result is *not an error in the technical test*: its deliberate epistemic limit must be resolved before calling a passage inspected. The original SHA-256 digest is reported, but **no full source text** is included in output.

## Integrity boundaries and failure modes

1. Source-PDF pages and printed-page labels are distinct. This program can verify **0-based PDF page index**; the printed page label is metadata and requires human confirmation.
2. The program checks bytes and extracted text. It cannot verify a PDF's **legal authority, current force, authenticity beyond repository provenance, edition history or interpretive adequacy** merely because SHA/quote match.
3. A screenshot/image-only PDF may have no extractable text: return \`PARTIAL\` and request careful manual inspection. OCR is deliberately not run automatically.
4. Normalized match is not equivalent to verbatim match. Case/punctuation are not automatically discarded; all transformations are disclosed.
5. Source metadata such as effective date, publication year and claimed jurisdiction do **not** constitute verified legal facts. To establish law-in-force, obtain authoritative legislative/case-law source and check temporal status separately.
6. A link, third-party snippet, metadata record or user-created excerpt **must not** be promoted to a directly verified original-source passage. The actual bytes need to be independently obtained, pinned and checked.
7. Runtime file paths are confined to the declared source root (including symlink targets), to reduce accidental leakage of private workspace data.
8. The public repository contains only implementation, small synthetic test PDFs generated at test time, short public textual examples, and aggregate reports.

## Release gate

**P0 code functionality:** established by deterministic PDF/text tests when the regression suite passes.  
**P0 real-original integration:** established **only** for the sources independently pinned and successfully reverified against their previously recorded digests. Source downloads blocked by access controls must remain \`UNVERIFIED\` and not be counted as verified.  
**P1–P5 roadmap:** not implemented by this change; follow [RFC-010](RFC-010-POST-BATCH-DEVELOPMENT-PLAN.md).

### Next recommended development

P1 \`Author-Faithful Reconstruction Layer\` after source grounding: compare each AI-proposed claim to the specific source paragraph, distinguish explicit author premises from opponent quotations and AI-proposed hidden warrants, retain researcher confirmation, and measure false positives of semantic criticism against independent reviewers.
