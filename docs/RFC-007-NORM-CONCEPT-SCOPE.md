# RFC-007 — DOCTRINA Object Scope Freeze: NORMA / KONSEP

**Date:** 25 November 2026  
**Decision:** accepted project scope; applies immediately to `SKILL.md` and Module 01.  
**Implementation status:** instruction-level scope now; Python graph linter and 18 regression tests retain their v0.3 behavior until an explicit schema migration.  
**Overrides:** broad examples in RFC-005 and RFC-006 only insofar as they imply **theory as research object**, autonomous theory construction, or evaluation of a philosopher's entire theoretical system.

## 1. Non-negotiable research object

**DOCTRINA supports exactly two primary objects of dissertation research:**

- **NORMA** — one or more legal norms, provisions, principles within a defined legal system, or their normative relationship, operation, hierarchy, coherence, interpretation, scope or justification.
- **KONSEP** — a legal concept used in norms, doctrine or legal practices, including its meaning, structure, boundary, competing legal conceptions, internal contradiction, interpretation, justification and normative implications.

A dissertation can combine both, but its **primary object must still be recorded** as `norm` or `concept`. Cases that study a concept *through* a statute remain eligible. Cases that test an entire legal/philosophical theory **as the object** are outside the current scope. Do not auto-expand into theory-building.

### Examples of valid targets

1. **Norm object:** the legal provisions on land acquisition for public interest in a specified jurisdiction/time. Test contradictions between provisions, interpretation, authority, justificatory sufficiency, normative consequences and defensible remedies.
2. **Concept object:** the concept of `kepentingan umum`. Test how statutory/dogmatic meanings relate, whether its boundaries and criteria cohere, its interaction with rights and legal validity, and its effects within positive law.
3. **Norm–concept combination:** a legal definition in statute is examined as a concept while its prescriptive consequences and applicability are examined as norms.

### Explicitly out of scope

- "Is Kelsen's Pure Theory of Law true or false?" as the dissertation's primary question.
- "Develop a comprehensive new legal theory from scratch" as the required output.
- General criticism/comparison of philosophical theories when no identifiable **legal norm or concept** is the subject of the research.

A theorist may still be cited, interpreted responsibly and used as a **limited analytical lens or reference**. The agent must verify that it does not misrepresent those sources, but does not claim to validate or falsify the whole theory.

## 2. Object-first research charter

Before an internal dissertation review, record:

```yaml
research_object:
  primary_type: norm        # norm | concept
  title: "Kepentingan umum dalam pengadaan tanah"
  jurisdiction: "Indonesia" # if relevant
  temporal_scope: "as of the relevant date"
  exact_locus: "specific provision or concept usage"
  secondary_type: concept   # optional; only norm | concept
  source_scope: []
research_question: "..."
current_thesis: "..."       # author statement or explicitly proposed
```

Do not invent a source, article number, provision status, legal validity or the author's exact thesis.

## 3. Research route A: NORMA

1. **Identify and localize norm:** exact text, legal authority, legal level, scope, time, conditions, exceptions and affected legal positions.
2. **Map the normative problem:** internal inconsistency; hierarchy; ambiguous applicability; competing interpretations; conflict with a principle/other norms; justificatory deficit; or underdetermination.
3. **Reconstruct the author's argument:** propositions, relevant sources, inferential warrants and anticipated exceptions.
4. **Test internally:** validity vs legitimacy; scope of legal effects; unsupported 'ought' claims; normative hierarchy; unexamined exceptions; overgeneralization; change of premise across chapters.
5. **Stress-test interpretation:** strongest rival reading, counterexample and any source-status limits.
6. **Integrate:** check how the proposed legal reading or reformulation affects the rest of the dissertation.
7. **Rehearse defense.**
8. **Final contribution/originality audit only after stabilization.**

## 4. Research route B: KONSEP

1. **Identify concept and usages:** explicit textual instances, legal definitions, implicit assumptions and doctrinal deployments.
2. **Separate concept/conceptions:** the legal category itself vs competing meanings or evaluative models assigned to it.
3. **Identify conceptual difficulty:** contested boundary, equivocation, internal contradiction, overly broad/narrow extension, conflict in usage, unjustified implications.
4. **Reconstruct argument:** specify explanatory premises, interpretive criteria and possible normative bridges.
5. **Test internally:** term drift, category mistake, rhetorical definition, unjustified necessary/sufficient conditions, descriptive-to-normative leap.
6. **Test against hard cases and rival readings,** without turning the task into certification of a named theory.
7. **Integrate conceptual findings into legal effects and the chapter thesis; defend it.**
8. **Final originality audit last.**

The outcome may be clarification, a qualified interpretation, critique, defensible reconstruction **of a norm or concept**, or an explicit limit/aporia. A new general theory is never mandatory.

## 5. Role of theory: support, not object

- **Permitted:** theory as a limited interpretive/analytical instrument; source of a normative argument that is explicitly defended; background of a doctrinal disagreement; rival interpretive lens for a **specific norm/concept**.
- **Disallowed in this scope:** tests claiming the whole theory is true/false; theory's global "compatibility score"; theories as the primary research object; automatic synthesis of general jurisprudential theory.
- **Audit requirement:** do not misquote or attribute unsupported positions to a theorist; state theoretical assumptions and their limits.
- **Methodological pluralism remains:** do not force a deconstructive conceptual critique to produce legal reform, nor treat a legitimate interpretive circle as a formal fallacy.

## 6. Two review rubrics

### Norma
- Is the relevant rule/text/version and jurisdiction identified?
- Are hierarchy, temporal validity and conditions/exceptions accounted for?
- Is the proposed interpretation supported by actual legal materials and a defensible interpretive warrant?
- Are legal validity, legitimacy, policy desirability and empirical effectiveness kept distinct?
- Does the proposed normative conclusion genuinely follow from the author's grounds?
- Are opposing readings and downstream effects handled?

### Konsep
- Is the target legal concept distinguished from a particular conception or definition?
- Are source uses and contexts located?
- Are concept boundaries, contrary cases and implications explained?
- Is the chosen clarification/critique justified without equivocation?
- Are normative implications separately warranted rather than presumed?
- Are changes in conceptual commitments across chapters reconciled?

**Both rubrics:** preserve text provenance; classify findings as structural vs substantive; propose minimal repair; record researcher acceptance; re-review changed downstream claims. **Neither** declares doctoral success or novelty by a passing lint.

## 7. Impact on existing repository

**Immediate instruction updates:** README, root `SKILL.md`, Module 01, Module 03 and Conceptual Research Charter all apply `norm` / `concept` scope. Historical RFC-005/006 remain as research history, but their theory-as-object alternatives must not control live routing.

**Deferred technical work:** a schema version supporting mandatory primary object type; migration of synthetic fixtures; non-breaking automated `research_object` checks; dedicated jurisprudential case studies on norms and concepts. Until implemented and tested, claim no machine-enforced scope.

**Release gate:** no new novelty audit before argument stability; no private dissertation uploaded into the public repository.
