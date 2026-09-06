# Functional Specification — Standard

**Version:** 1.7 (2026-09-06)

The single-file definition of how our projects specify user-visible behavior:
one short document per behavior change, written so the people building it know
exactly what "done" means — numbered, testable requirements and
Given/When/Then acceptance criteria.

**Adoption:** a project adopts this standard by copying this file to
`docs/specs/FUNCTIONAL-SPECS-STANDARD.md` in that project, keeping its specs and index there,
and noting the adopted version. **AI agents:** `FUNCTIONAL-SPECS-SKILLS.md` (next to this file)
defines the execution workflows and the spec-validation checklist; follow it
when asked to write, approve, or supersede a spec.

**Companion standard:** `../decision-records/DECISION-RECORDS-STANDARD.md` (this repo) — the
decision-records
standard. A functional spec answers **what** the system must do; decision
records answer **how** it is built and **why** that way. The pipeline is:
functional spec (what) → decision records for the architecturally significant
hows (in the project's `docs/decisions/`) → build, with the spec's acceptance
criteria as the done checklist.

Any change to this standard bumps the version and appends a line to the
changelog (§9).

## 1. Scope, use cases & purpose

**Scope:** a spec is required for any change a user — human or machine — can
**observe**: a new capability, changed behavior, a new or changed interface or
contract.

Do **not** write a spec for: pure refactors, bug fixes that restore documented
behavior (that is a regression test), decisions about how to build something
(that is a decision record), or small changes best covered by one paragraph in
the ticket or PR. Unlike decision records, an over-written spec is waste, not
insurance — when in doubt, **don't** write a spec; write a paragraph.

**Use cases:**

- specifying a feature before it is built — scope arguments end at Goals &
  non-goals (§4);
- agreeing "done" up front — the acceptance criteria are the done checklist
  during build;
- answering "what is this feature supposed to do?" — from the spec, not from
  a chat thread;
- handoff — an implementer who wasn't in the room gets the same contract as
  the one who was.

**Purpose:** so the people building a change know exactly what "done" means —
numbered, testable requirements and Given/When/Then acceptance criteria — and
so what was promised is on record when questions come up later.

## 2. File conventions

- Approved specs live in the adopting project's `docs/specs/`, named
  `NNN-short-noun-phrase.md` — 3-digit zero-padded sequential number
  (`001-offline-export-for-telemetry.md`). Numbers are monotonic,
  **contiguous from 001**, and **never reused**: a gap (a missing number)
  is an error — it means a file was deleted or a number skipped; never
  renumber to close it, restore the file or let the next free number fill
  it. Numbers are assigned **when the spec is approved**, not when the
  draft is written.
- A draft that has not been approved yet lives in the project's `docs/` as
  `PROPOSAL-<TOPIC>.md` (uppercase topic, no number) — same format,
  `Status: proposed`. On approval or decline it is promoted (§6).
- One feature/change per spec. A document that specifies two features is
  split into two documents.
- Copy the template from §7 to start.

## 3. Lifecycle

| Status | Meaning |
|---|---|
| `proposed` | draft written, not yet agreed |
| `approved` | agreed; the behavior is in force |
| `declined` | considered and not pursued (keep the file — it prevents re-litigating) |
| `superseded by NNN` | replaced by a newer spec; the old file stays, unedited |

Approved specs are **append-only records**: the requirement text is
immutable; status changes only through lifecycle transitions; clarifications
discovered during build are appended to the Amendments section as dated
one-liners; anything that changes **what the feature does** — not just what
a requirement meant — is a new spec that supersedes this one. The
requirement text is the record of what was promised when work started;
Amendments is the honest log of what changed mid-flight.

The spec index in the project's `docs/specs/README.md` must stay current (one
line per numbered spec) — and it is the **capability map**: specs grouped
under the capability they deliver, so the behavior surface of the whole
system is one page and a capability with no spec is a visible gap. The index
links and groups; it never restates a spec's requirements.

## 4. Format

Sections, in order. The spec **MUST** contain exactly these top-level
headings, in this order — a section that does not apply is written as `None.`
rather than deleted, so specs stay diffable and machine-checkable; nested
`###` headings MAY be added beneath them. Keep the spec to one sitting —
past roughly 800 words, split it or tighten it. Write inverted-pyramid: a
reader who stops after the Summary still knows what is changing.

1. **Title** — short noun phrase: "Offline export for telemetry".
2. **Status / Date / Author / Approver** — four header lines.
3. **Summary** — 1–3 sentences: what changes, for whom, why now.
4. **Goals & non-goals** — two short lists. Non-goals fence the spec: they
   name what this deliberately does not cover, so scope arguments end here.
5. **Users & scenarios** — who uses this and the 2–4 scenarios that matter.
6. **Functional requirements** — the numbered, testable behavior list (§5).
7. **Acceptance criteria** — Given/When/Then criteria per requirement,
   identified `AC-N.M` (§5); the done checklist.
8. **Open questions & unknowns** — unresolved questions with owners, ending
   with the premortem line.
9. **Amendments** — `None.` until approval; dated one-liners after.
10. **References** — related decision records, prior/successor specs, design
    docs, external sources.
11. **Implementation work** — optional traceability metadata linking external
    implementation work to the requirements and, when useful, acceptance
    criteria. This is not part of the functional contract.

## 5. Writing rules

- **Testable or it doesn't go in.** Every requirement (`FR-N`) must be
  falsifiable: an input goes in, an observable outcome comes out, and a human
  or test can pass/fail it. Unquantified vague words — "fast", "robust",
  "user-friendly", "efficient" — are banned; quantify ("under 2 s at p95") or
  cut.
- **One requirement, one behavior — many checks allowed.** No compound
  and-joined requirements; each `FR-N` passes or fails independently. A
  requirement MAY need several acceptance criteria (happy path, boundaries,
  failure modes) — identify them `AC-N.M` under `FR-N` (`AC-1.1`, `AC-1.2`,
  …). Verification walks every AC, not every FR.
- **Normative keywords, used deliberately.** When normative force is
  intended, use uppercase RFC 2119 keywords: MUST (the spec fails without
  it), SHOULD (strong preference, a reason may overrule), MAY (explicitly
  optional). Lowercase "must" is ordinary English.
- **Behavior only — no design.** A functional spec says what the system does,
  never how: no components, libraries, data models, protocols, "we'll use X".
  That sentence belongs in `docs/ANALYSIS-<TOPIC>.md` and becomes a decision
  record (companion standard §2). The split in practice: *a question about
  what a user sees or gets* → this spec; *a question about structure,
  dependencies, interfaces, or construction* → a decision record. If a
  requirement can only be met one way and that way is expensive to reverse,
  the requirement is fine — but the choice needs its own record.
- **Cover the edges or disclaim them.** Requirements address the boundary
  cases that matter (empty input, oversized input, concurrent use, failure,
  unauthorized access) or explicitly state a case is unhandled — here or in
  non-goals. Silence is not a disclaimer.
- **Non-functional and quality attributes.** Even internal or load-only
  properties (latency under load, availability SLOs, compliance obligations,
  security properties that surface only under attack) are expressible as
  requirements when they are observable under defined conditions. Treat them
  the same way as any other FR:
  - Quantify the threshold and the conditions (e.g. "p95 end-to-end latency
    MUST be < 250 ms at 1 000 concurrent users measured by the staging load
    test suite").
  - Name the measurement method and the verification path in the acceptance
    criteria (or point to a verification report that will supply them).
  - Prefer ISO/IEC 25010 quality characteristics as vocabulary when useful
    (performance efficiency, reliability, security, maintainability, etc.).
  - An SLI/SLO pair is a natural form: the SLI specification becomes the
    observable outcome; the SLO becomes the numeric threshold; the
    verification report records the SLI implementation and the run evidence.
  - Purely internal design choices that realise an NFR (caching strategy,
    replication topology, threat-model mitigations) belong in a decision
    record, not in the functional requirements text. The observable promise
    stays here; the architectural approach stays there.
  Vague quality wishes ("be secure", "scale well", "be compliant") are
  banned exactly as "fast" or "robust" are banned — turn them into
  measurable criteria or move them out of the spec.
- **Implementation traceability is metadata, not behavior.** The
  `Implementation work` section MAY be omitted when no external work tracker
  is used. When implementation work is tracked, each work item SHOULD link
  to the `FR-N` requirements it realizes and MAY link to specific `AC-N.M`
  criteria. Jira is a common example, but the format MUST remain
  vendor-neutral: GitHub Issues, Linear, Azure Boards, or another tracker are
  equally valid. The work tracker does not become authoritative over the
  specification; changes to behavior still require the spec lifecycle in §3.
  Work items MAY be updated as implementation progresses without changing the
  requirements. A spec with no tracked work SHOULD say `None.` in the section.

## 6. Proposals and promotion

A `PROPOSAL-<TOPIC>.md` document **is** a spec in `proposed` state: identical
format (§4), writing rules (§5) and template (§7) — only without a number.
Nothing else distinguishes it.

Promotion, when the approver approves or declines:

1. move the file: `docs/PROPOSAL-<TOPIC>.md` →
   `docs/specs/NNN-<topic-slug>.md` with the next free number — re-list the
   directory immediately before naming; if your number was taken while you
   worked, take the next one (`validate.py` flags duplicates);
2. set `Status:` to `approved` or `declined` and `Date:` to the decision date;
3. add the index row in the project's `docs/specs/README.md`.

The proposal is not kept separately — the promoted spec *is* the proposal,
now numbered.

## 7. The template

Copy this skeleton to `NNN-short-noun-phrase.md` (or, while unapproved, to
`PROPOSAL-<TOPIC>.md`):

```markdown
# {short noun-phrase title, e.g. "Offline export for telemetry"}

**Status:** {proposed | approved | declined | superseded by NNN}
**Date:** {YYYY-MM-DD of approval}
**Author:** {who wrote the spec}
**Approver:** {who agreed; for `declined`, who declined}

## Summary

{1–3 sentences: what changes, for whom, why now. A reader who stops here
still knows the change.}

## Goals & non-goals

{Two short lists. Non-goals fence the spec — name what this deliberately
does not cover, so scope arguments end here.}

Goals:
- {…}

Non-goals:
- {…}

## Users & scenarios

{Who uses this and the 2–4 scenarios that matter. User-story form:
"As a {role}, I want {capability}, so that {benefit}."}

- As a {role}, I want {…}, so that {…}.

## Functional requirements

{Numbered FR-N, one testable statement each; uppercase RFC 2119 keywords
(MUST/SHOULD/MAY) where normative force is intended. Behavior only — no
components, libraries, or data models; those are decision records
(docs/decisions/). Cover the boundary cases that matter or state explicitly
that a case is unhandled.}

- **FR-1:** The system shall {observable behavior}.
- **FR-2:** {…}

## Acceptance criteria

{Acceptance criteria per requirement, identified AC-N.M. This is the done
checklist — each criterion must be runnable as a manual or automated test.}

- **FR-1:**
  - AC-1.1 — Given {context}, when {action}, then {observable outcome}.
  - AC-1.2 — Given {boundary case}, when {action}, then {outcome}.

## Open questions & unknowns

{Unresolved questions and assumptions to verify, each with an owner (+ date
where known). End with the premortem line:}

- {question / unknown — owner: {who}}
- Premortem: if this ships and disappoints, the most likely cause is {…}.

## Amendments

{None. until approval. After approval: dated one-liners only — the
requirement text above is never rewritten.}

- None.

## References

{Links: related decision records (docs/decisions/NNN-*.md), prior/successor
specs, design docs, external sources behind any claim.}

## Implementation work

Optional traceability metadata. Link each work item to the `FR-N` requirements
it realizes and, when useful, to specific `AC-N.M` criteria. Use `None.` when
there is no externally tracked implementation work.

| Work item | Implementation | Requirements | Acceptance criteria | Status |
|---|---|---|---|---|
| [ENG-421](https://tracker.example/browse/ENG-421) | [PR #87](https://github.com/example/project/pull/87) | FR-1, FR-2 | AC-1.1, AC-2.1 | Done |
| [ENG-422](https://tracker.example/browse/ENG-422) | [PR #91](https://github.com/example/project/pull/91) | FR-3 | AC-3.1–3.2 | In progress |
```

## 8. Lineage & sources

The convention this standard is based on, in order of influence:

- **IEEE Std 830-1998** (*Recommended Practice for Software Requirements
  Specifications*) — the classic SRS tradition: requirements are numbered,
  testable, and separate from design. Withdrawn 2011, superseded by
  **ISO/IEC/IEEE 29148:2018**, which defines the characteristics of good
  requirements (necessary, verifiable, unambiguous) and the shall/should
  vocabulary this standard borrows.
- **Karl Wiegers & Joy Beatty, *Software Requirements*** (3rd ed., Microsoft
  Press, 2013) — the modern practitioner reference; source of the testability
  and one-requirement-one-check rules (§5).
- **Volere template** — Suzanne & James Robertson; the other long-lived
  requirements template; source of the "scope fence" framing of non-goals.
- **RFC 2119** (Bradner, 1997) — must/should/may keywords.
- **Given/When/Then** — Dan North, "Introducing BDD" (2006); Gherkin/
  Cucumber; acceptance criteria written to be runnable, not decorative.
- **User stories** — the "As a … I want … so that …" format (Connextra;
  popularized by Mike Cohn, *User Stories Applied*, 2004).
- **PR/FAQ** — Amazon's Working Backwards (Bryar & Carr, *Working Backwards*,
  2021): write the user-facing outcome first; the Summary's inversion
  borrows this.
- **Goals / non-goals** — the Google design-doc convention.
- **Companion: decision records** — `../decision-records/DECISION-RECORDS-STANDARD.md`
  (Nygard 2011; Fowler); the how-and-why half of the same pipeline.
- **ISO/IEC 25010:2023** (SQuaRE — System and software quality models) —
  product-quality characteristics used as vocabulary for non-functional /
  quality-attribute requirements (§5).
- **Google SRE / Site Reliability Workbook** — SLI specification vs
  implementation, and SLOs as measurable targets that become acceptance
  criteria and verification evidence (§5).

## 9. Changelog

- **1.7 (2026-09-06)** — added optional `Implementation work` traceability
  metadata as the final spec section; defined vendor-neutral work-item links,
  requirement/acceptance-criterion traceability, non-authoritative tracker
  semantics, and `None.` for specs without tracked implementation work.
- **1.6 (2026-09-05)** — writing rules (§5): explicit guidance for
  non-functional and quality attributes (quantified thresholds, measurement
  method, verification path, ISO 25010 vocabulary, SLI/SLO form); pure
  design realisations of NFRs stay in decision records.
- **1.5 (2026-09-05)** — file conventions (§2): numbering gaps are errors —
  numbers are contiguous from 001; never renumber, restore the file or let the
  next free number fill the gap.
- **1.4 (2026-09-05)** — external review: append-only immutability model (§3); AC-N.M acceptance-criterion identifiers (§4, §5, §7); uppercase RFC 2119 keywords (§5, §7); collision-safe numbering (§6); nested headings and one-sitting length (§4).
- **1.3 (2026-09-05)** — self-describing filenames: the standard and its skills file are named `FUNCTIONAL-SPECS-STANDARD.md` and `FUNCTIONAL-SPECS-SKILLS.md`, in the suite and in project adoption copies.
- **1.2 (2026-09-05)** — spec index upgraded to the **capability map**
  (specs grouped by capability; gaps visible) — the what-side half of the
  suite's coverage hierarchy (README).
- **1.1 (2026-09-04)** — §1 renamed to **Scope, use cases & purpose**
  (explicit use cases and purpose); repo namespaced into per-standard
  directories.
- **1.0 (2026-09-04)** — initial version: what-vs-how split with the
  decision-records standard (intro, §1, §5), exact-heading format with
  Amendments (§4), testability and RFC 2119 rules (§5), proposal↔spec
  promotion lifecycle (§2, §3, §6), template (§7).
