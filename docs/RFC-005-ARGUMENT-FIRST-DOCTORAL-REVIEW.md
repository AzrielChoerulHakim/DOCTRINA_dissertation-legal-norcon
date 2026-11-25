# RFC-005 — DOCTRINA v0.3
## Internal Argumentation Engine for Ongoing Normative–Conceptual Legal Dissertations

**Date:** 25 November 2026  
**Status:** implementation prototype / methodological review required  
**Supersedes:** v0.2 module routing in RFC-004 where it places contribution/originality before dissertation integration and defense.  
**Retains:** epistemic discipline, conceptual modes, human researcher authority, source provenance, and university adapters.  
**Explicitly excludes:** generic article writing, one-click doctoral certification, bulk RAG, autonomous publication, blanket forced deductive syllogisms and claims that originality can be verified by title search.

## 1. Design problem and thesis

The core failure of a live doctoral dissertation is often not the absence of references but an **internal gap in how its propositions justify one another**: a chapter changes the meaning of a concept midstream; the conclusion presupposes what it sets out to establish; the author moves from a descriptive exposition of legal doctrine to a prescriptive recommendation without normative warrant; a critique attributes a position to a theorist that the theorist does not hold; an early foundational premise is abandoned in later chapters without updating conclusions.

DOCTRINA's priority is therefore **an author's evolving argumentative spine** — *which proposition is defended, on what grounds, by which inferential move, within which conceptual scope, against which plausible objection, and with what consequences for subsequent chapters*. The system is continuously useful **during drafting**, not just after the dissertation has been completed.

Scientific standards are not replaced by flowcharts. A machine can detect dangling references and textually declared inconsistencies, not judge every philosophical inference, doctrinal meaning or adequacy of a normative premise. Keep the machine verdict narrower than the academic evaluation.

## 2. New workflow and the final originality gate

| Stage | Core work | Gate to advance | Re-entry trigger |
|---|---|---|---|
| S1 — Conceptual framing | Problem, concept vs conception, thesis question, jurisdiction/method | Researcher confirms provisional target | Conceptual ambiguity undermines thesis |
| S2 — Theoretical/method warrant | Roles of theories, legal materials, inference mode and scope | Method capable of answering question | Later claim changes its philosophical commitments |
| S3 — Argument reconstruction | Central thesis, individual argument units, warrants, supporting premises, qualifiers | Faithful, located reconstruction of selected draft | Text changes; a hidden assumption emerges |
| S4 — Internal stress | IA-01..IA-16: missing warrants, circularity, term shift, contradictions, normative bridge, method overreach | No unresolved *known* foundational internal defect in review scope | Any repaired premise changes downstream claim |
| S5 — Dialectical stress | Strongest rival, counterexamples, underminers, justified concession | Major objections addressed or transparently narrowed | Counterexample defeats universal claim |
| S6 — Dissertation integration | Sentence → paragraph → subsection → chapter → central thesis, continuous revision monitoring | Chapter contracts and central spine stable in inspected scope | New chapter/revision invalidates earlier conclusion |
| S7 — Defense rehearsal | Questions about inferential/interpretive/methodological commitments | Researcher resolves blocking vulnerabilities | Weak defense reveals hidden premise |
| **S8 — Final originality audit** | Only now compare *stabilized* contribution proposition by proposition to prior scholarship | Limited, transparent contribution finding | New prior-work evidence reopens central premise |

**Critical distinction:** genealogy and literature comparison continue throughout S1–S7. The *formal novelty judgment* is last, and if it changes the researcher's central thesis, S3–S7 are repeated before any subsequent novelty conclusion.

## 3. Ongoing work and the unit of examination

DOCTRINA asks: What exactly is the author's current object — a premise, paragraph, subsection, chapter, central thesis, or entire draft? It does **not** demand that all dissertation chapters already exist. The result is bounded by inspected text.

Six review scales:
- **Sentence**: kind, modality, definition, jurisdiction, time, meaning.
- **Paragraph**: premise–warrant–conclusion, unstated premise, qualifier.
- **Subsection**: inferential progression, repeated or unearned claims.
- **Chapter**: subthesis, argument task, opponent treatment, dependencies.
- **Dissertation**: central thesis, cross-chapter drift, theory/method consistency.
- **Revision**: forward dependency propagation and reviewer sign-off.

At any scale, distinguish the original author text, a faithful researcher-approved paraphrase, and an **AI-proposed charitable reconstruction**. The latter is never silently attributed to the author.

## 4. Argument model and inferential modes

Base argument unit:

```text
Claim C (with kind, domain, qualifier and location)
  supported by P1, P2, ... (explicit, reconstructed, or stipulated)
  via W (warrant; state whether a normative bridge is asserted)
  backed by B (normative ground, interpretation, doctrinal authority, argument)
  vulnerable to O (counterexample, premise objection, warrant undercutter)
  affects C2, C3 ... and named chapters
```

This adopts **Toulmin-inspired** argument reconstruction as a pedagogical scaffold, not as a mandatory philosophical logic. The scheme supports deductive, interpretive, defeasible, normative-constructive, genealogical, analogical, abductive and critical argumentative moves; their adequacy standards differ.

MacCormick's emphasis on consistency, coherence and consequences is useful **as a set of questions for legal justification**, not a universal replacement for the dissertation author's chosen jurisprudential method. Critical/genealogical and deconstructive inquiries need not end in legal codification or a harmonious closed system. Legal argument frequently is defeasible; an objection can undercut the inference without proving the conclusion's opposite.

## 5. Internal testing protocol (PRIMARY)

For the selected textual scope:

1. **Charitable reconstruction:** recover *the most defensible reading consistent with the author's actual words*. Mark conjectural linking premises.
2. **Reconstruct burden:** What does the author undertake to prove? Which statement has mere descriptive force, and which has an evaluative/prescriptive force?
3. **Premise review:** Examine each premise's own warrant, source category, assumptions and source limits; beware treating a citation as a proof.
4. **Inference review:** Does the conclusion follow on the *author's stated kind of inference*? Avoid treating all conclusions as mathematical entailments.
5. **Meaning and scope:** Are the same concepts used consistently? Watch legal validity vs legitimacy, interpretive meaning vs normative desirability, historical vs present law, theory object vs adopted normative framework.
6. **Counterexample:** Build limiting cases/exception structure; identify defeasible rather than categorical claims.
7. **Recursive dependency:** Test prior claims on which the present claim relies and later claims that rely on the target.
8. **Minimal repair:** Present smallest defensible textual/argumentative repair, plus one more radical reframing, with trade-offs and author decision.
9. **Document gate:** Problem, location, impact, residual uncertainty, researcher approval and re-audit trigger.

### Hard stops and review-only warnings

**Hard stop for internal stabilization:** important derived conclusion without an identifiable warrant or justifiable inference; normative prescription supported only by description; undiscussed contradiction in same standpoint, time, jurisdiction and conceptual sense; primary-source attribution falsely claimed verified; foundational premise undermined by current writer's own accepted premises.

**Review flag, not automatic failure:** circular graph where reflective equilibrium/hermeneutical interpretation may be methodologically sound; semantic tension between rival views; theoretical disagreement intentionally staged; missing support in an incomplete draft; theory switching with explicit justification; intentionally unresolved aporia.

**Never a machine verdict:** whether a theorist's strongest possible argument has been fairly reconstructed; whether the jurisprudential conception is sound; whether an interpretation is correct under authoritative legal practice; whether a dissertation is fit to pass doctoral examination.

## 6. Graph and review contracts

`claims[]`: `id`, `text`, `kind`, `role`, `premises[]`, `inference`, `warrant`, `chapter_id`, `scope`, `quotes[]`, `support[]`, `contradicts[]` (declared only).  
`chapters[]`: `id`, `title`, `argumentative_task`, `claim_ids[]`.  
`objections[]`: `id`, `target_id`, `severity`, `status`, `text`, `researcher_reply`.  
`sources[]`: bibliographic metadata with source IDs.  
`readiness`: declaration of completed internal/dialectical/integration/defense review **and researcher approval**; these are not independently attested by Python.

A deterministic linter must:
- detect missing/duplicate claim IDs, dangling premise and chapter links, absent derived warrants;
- flag normative bridge missing from a derived normative claim with only non-normative premises;
- prevent quotation claims from being marked inspected without source and locator;
- detect declared self-support and possible longer dependency cycles;
- warn on declared contradictions but demand human scope comparison before calling them real;
- trace transitive downstream claims and all affected chapters;
- bar the final originality-stage *routing* if serious open objections, required review declarations or author approval are absent.

The linter **does not** read PDFs, decide source truth or similarity, infer natural-language semantic contradictions, validate novelty or prove soundness. Passing means its known checks did not find a violation.

## 7. Live revision demonstration

Synthetic example, not a claim about Indonesian positive law:

- P1 — legal definition and normative justification are distinguishable.
- P2 — rights restrictions need independent justification (declared normative premise).
- C1 — labeling a purpose 'kepentingan umum' is not by itself a sufficient justification of every rights restriction.
- C1 depends on P1 and P2, with an expressly **proposed** normative-constructive warrant.
- O1 — could substantive justification already have been built into the rule? The conclusion must be qualified to 'label alone' and not deny all formal mechanisms of justification.

When P2 is revised, C1 and any dependent chapter must be re-reviewed. A connected graph does not certify the adequacy of P2 or the claim that it conforms to any actual Indonesian legal provision.

## 8. Final originality audit: last, but not omitted

No novelty percentages, no claim that the final thesis is unique merely because a search engine returned no matching titles, no automatic certification based on bibliographic metadata.

When internal+dialectical+integration+defense review are complete, construct an exact **contribution delta matrix**: stabilized proposition, existing prior propositions and their source locators, what changes or is defended by the dissertation, kinds of contribution (correction/extension/new justification/critique/reconstruction), source coverage and plausible counterexamples. Compare author/coauthored prior scholarship as necessary, but only here judge the bounded originality status. Return to internal testing if a relevant prior contribution undermines the thesis itself.

## 9. Quality assurance and acceptance tests

### Mechanical unit-test scenarios
M01 positive complete synthetic argument; M02 missing derived warrant; M03 dangling premise; M04 unsupported normative prescription; M05 explicit normative bridge; M06 graph cycle flagged as review only; M07 unverified quotation blocked; M08 open serious objection blocks final gate; M09 revision propagates to dependents and chapter IDs; M10 incomplete review blocks final gate; M11 self-dependency blocked; M12 duplicate ID detected; M13 metadata alone cannot substantiate passage; M14 completion declaration permits **only routing** to final novelty evaluation, not novelty verdict; M15 lack of researcher approval; M16 dangling chapter claim; M17 declared semantic tension kept as review; M18 revision impact on unknown claim.

### Scholarly gold cases (not yet executed)
A01 descriptive/prescriptive transition in an actual dissertation paragraph; A02 two defensible conceptions with term shift; A03 deliberate negative/deconstructive thesis; A04 apparent cycle justified by reflective equilibrium; A05 source-passage matched but the interpretation unsupported; A06 identical terminology across legal systems with non-identical normativity; A07 changes made in Chapter III that undermine Chapter V; A08 substantive objection not answered by mere citation; A09 strong opponent fairly represented; A10 final originality comparison after repaired argument.

These A tests need full authorized source passages and competent disciplinary reviewers; they are not 'passed' because the written scenario exists.

## 10. Tools / libraries policy

**Required:** portable Agent Skills specification; the provided Python standard-library lint is optional in chat-only use. **Later, if validated:** `networkx` for convenient graph visualization, `pypdf` for source locators, `pytest` for advanced test harness. DOCTRINA's conceptual validity is not outsourced to these tools. No compulsory LLM chain, graph database, vector index or server.

## 11. Sources, limits, and synthesis

The following published works provide *conceptual inspiration*, not an endorsement or exact implementation of DOCTRINA:

1. Stephen Toulmin, *The Uses of Argument* (1958), six-part framework overview: Purdue University OWL https://owl.purdue.edu/owl/general_writing/academic_writing/historical_perspectives_on_argumentation/toulmin_argument.html . This establishes labels, not legal truth.
2. Neil MacCormick, *Legal Reasoning and Legal Theory*, OUP chapter summaries, including second-order justification, consistency and coherence: https://academic.oup.com/book/10467 and https://academic.oup.com/book/10467/chapter-abstract/158338649 . These are publisher descriptions, not a claim of full-book inspection.
3. Stanford Encyclopedia of Philosophy, *Defeasible Reasoning*, https://plato.stanford.edu/entries/reasoning-defeasible/ . Supports the distinction between defeasible and deductive reasoning.
4. Giovanni Sartor, *Interpretation, Argumentation, and the Determinacy of Law*, https://doi.org/10.1111/raju.12389 . Models interpretive arguments as defeasible and challengeable.
5. H. Prakken & G. Sartor, *Law and Logic: A Review from an Argumentation Perspective*, *Artificial Intelligence* 227 (2015), 214–245; open manuscript https://pure.rug.nl/ws/portalfiles/portal/98715514/Law_and_logic_a_review_from_an_argumentation_perspective.pdf . Argumentation theory is relevant to legal justificatory structures, but mathematical models cannot mechanically decide doctoral soundness.
6. DOI/metadata services and external scholarship remain usable from the beginning for relevant substantive understanding; originality adjudication happens only at the final gate.

No complete dissertation or original philosophical treatise was newly audited for this RFC; the older pilot of Novelli is a separate case and does not establish v0.3 pass rates.

## 12. Release and authority

**Current:** structural prototype, instruction modules and sample tests. **Next scholarly acceptance threshold:** two real chapter passages from an ongoing normative-conceptual dissertation, independently reviewed by a researcher and an expert, showing that (a) DOCTRINA reconstructs the actual argument faithfully, (b) can identify at least one genuinely significant inferential weakness *without inventing it*, (c) can propose a repair that author accepts or rationally rejects, (d) rechecks affected downstream conclusions, and (e) defers novelty adjudication until last.

DOCTRINA may mark a workflow *ready for the final originality audit* but cannot mark the dissertation as original, academically valid or fit to graduate. No GitHub publication or commit is authorized under this RFC.