# Design Decision Records — Standard

**Version:** 1.6 (2026-09-05)

The single-file definition of how our projects record design decisions: one
short document per architecturally significant decision, written so a stranger
six months from now can see what we chose, why, and how close the alternatives
came.

**Adoption:** a project adopts this standard by copying this file to
`docs/decisions/DECISION-RECORDS-STANDARD.md` in that project, keeping its records and index
there, and noting the adopted version. **AI agents:** `DECISION-RECORDS-SKILLS.md` (next to this file)
defines the execution workflows and the record-validation checklist; follow
it when asked to write, promote, or supersede a record.

**Companion standard:** `../functional-specs/FUNCTIONAL-SPECS-STANDARD.md` (this repo) — the functional-spec
standard covering **what** user-visible behavior a change must deliver and its
acceptance criteria; this standard covers **how** it is built and **why**.
Specs and records must agree: a record that changes observable behavior is
paired with a spec amendment or supersession, and vice versa.

Any change to this standard bumps the version and appends a line to the
changelog (§9).

## 1. Scope, use cases & purpose

**Scope:** a record is required for any **architecturally significant**
decision (Nygard's test): one that affects the system's structure,
non-functional characteristics, dependencies, interfaces, or construction
technique — or that is hard/expensive to reverse. Examples: choosing an
orchestrator, adopting a format/tool, defining a contract boundary, picking a
data store, changing a deployment model.

Do **not** write records for: local style choices, single-function refactors,
anything fully reversible in minutes. When in doubt, write it — an
over-recorded decision is cheap, an under-recorded one is not.

**Use cases:**

- choosing between contested alternatives — the matrix (§5) forces a number
  on every judgment and a closeness line on the result;
- answering "why did we do it this way?" — from the record, not from
  someone's memory;
- onboarding — a new engineer reads the records and today's architecture
  explains itself;
- stopping re-litigation — a settled decision stays settled; reopening it
  means superseding, not re-arguing in a hallway.

**Purpose:** so a stranger six months from now can see what we chose, why,
and how close the alternatives came — without needing the context the
original deciders had.

## 2. File conventions

- Decided records live in the adopting project's `docs/decisions/`, named
  `NNN-short-noun-phrase.md` — 3-digit zero-padded sequential number
  (`001-swarm-for-onprem-fleet.md`). Numbers are monotonic and **never
  reused**, and are assigned **when the decision is made**, not when the
  analysis is written.
- A recommendation that has not been decided yet lives in the project's
  `docs/` as `ANALYSIS-<TOPIC>.md` (uppercase topic, no number) — same
  format, `Status: proposed`. On accept/reject it is promoted (§6).
- One decision per file. A document that argues two decisions is split into
  two documents.
- Copy the template from §7 to start.

## 3. Lifecycle

| Status | Meaning |
|---|---|
| `proposed` | recommendation written, not yet agreed |
| `accepted` | agreed; the decision is in force |
| `rejected` | considered and declined (keep the record — it prevents re-litigating) |

A `rejected` record may carry one later annotation — the **only** permitted
edit to a decided record besides the supersede line: append
`— reconsidered by NNN` to the Status line. A new proposal that revisits
rejected ground cites the old record in References: `Reconsiders: NNN`.
| `superseded by NNN` | replaced by a newer decision; the old record stays, unedited |
| `deprecated` | no longer applies (outdated by context, not by a successor) |

Records are **immutable once accepted**: never edit a decision in place. When
circumstances change, write the next record and mark the old one `superseded by
NNN`. This is the single most important rule in this standard — the value of
the collection is the honest history (Fowler: "the time to change old
decisions will be clear from changes in the project's context").

The record index in the project's `docs/decisions/README.md` must stay
current (one line per record) — and it is the **structure map**: records
grouped under the component or area they shape, so the decision surface of
the whole system is one page and a component with no records is a visible
gap. The index links and groups; it never restates a record's content.

## 4. Format

Sections, in order. The record **MUST** contain exactly these headings, in
this order — a section that does not apply is written as `None.` rather than
deleted, so records stay diffable and machine-checkable; nested `###`
headings MAY be added beneath them. Keep the record to one sitting — past
roughly 800 words, split the decision or tighten it. Write inverted-pyramid:
the decision up top, details later.

1. **Title** — short noun phrase: "Swarm for on-prem fleet".
2. **Status / Date / Deciders / Supersedes** — four header lines.
3. **Context and problem statement** — the forces at play (technical,
   operational, political, cost), value-neutral, tensions called out. What
   problem is being solved; state it as a question where possible.
4. **Decision drivers** — the criteria that matter *for this decision*, as a
   short list. These become the rows of the matrix.
5. **Considered options** — 2+ options; include the status quo ("do
   nothing") when it is a viable alternative, and if it is not, say why in
   one line. Each: 1–3 sentences on what it is and why it's on the table.
6. **Decision matrix** — the scoring table (§5 below).
7. **Trade-offs** — per option: what it buys and what it costs, in prose. This
   is where the numbers' blind spots get addressed. A decision the matrix
   doesn't support is allowed — say so here.
8. **Decision** — "We will …", active voice, full sentences. The one thing.
9. **Consequences** — positive / negative / neutral. What becomes easier, what
   becomes harder, follow-ups with owners. (An ADR's consequences become the
   context of the next decision.)
10. **Open questions & unknowns** — unresolved questions, assumptions to
    verify, risks — each with an owner and, where known, a date. Add a
    premortem line: *"If this fails in a year, the most likely cause is…"*
11. **References** — links to analysis docs, specs, papers, prior records.

## 5. Scoring rules

The matrix makes trade-offs explicit and forces a number on every judgment.
It is a **forcing function, not the decider** — the Decision section may (and
should) overrule the table, but must explain why in Trade-offs.

- **Scale: 0–5 per criterion, anchored:**

  | Score | Anchor |
  |---|---|
  | 0 | fails the criterion outright |
  | 1 | poor — misses it by a wide margin |
  | 2 | marginal — meets it only partially |
  | 3 | meets — acceptable |
  | 4 | strong — clearly exceeds |
  | 5 | best-in-class on this criterion |

- **Criteria:** 4–7 max (more is noise). Weight 1–10 each; show the
  normalized %. Justify each weight in one clause (why this one matters for
  *this* decision). If weight disagreement is the actual dispute, derive them
  by AHP pairwise comparison (Saaty 1–9 scale) instead of guessing.
- **Weighted total:** `Σ (score × weight) / (5 × total weight)` → 0–100%.
- **Basis, per criterion.** Every score cites its basis: a measurement or a
  link, or `judgment — {why}`. Measured beats argued; an unwritten basis is
  a guess — mark it as such or drop the criterion.
- **Closeness (required):** after the table, one line: the margin between the
  top two totals (in points) and **what would flip the decision** — the
  specific weight shift or score change that changes the winner (this is the
  lightweight form of AHP sensitivity analysis). A 2-point margin with a
  stated flip condition is a different kind of decision than an 18-point one,
  and future readers need to see which.

## 6. Analysis documents and promotion

An `ANALYSIS-<TOPIC>.md` document **is** a decision record in `proposed`
state: identical format (§4), matrix (§5) and template (§7) — only without a
number. Nothing else distinguishes it.

Promotion, when the owner accepts or rejects:

1. move the file: `docs/ANALYSIS-<TOPIC>.md` →
   `docs/decisions/NNN-<topic-slug>.md` with the next free number — re-list
   the directory immediately before naming; if your number was taken while
   you worked, take the next one (`validate.py` flags duplicates);
2. set `Status:` to `accepted` or `rejected` and `Date:` to the decision date;
3. add the index row in the project's `docs/decisions/README.md`.

The analysis is not kept separately — the promoted record *is* the analysis,
now numbered. Deep-dive companions that are not decisions (diagnoses,
surveys) stay un-numbered and are cited from References.

## 7. The template

Copy this skeleton to `NNN-short-noun-phrase.md` (or, while undecided, to
`ANALYSIS-<TOPIC>.md`):

```markdown
# {NNN} — {short noun-phrase title, e.g. "Swarm for on-prem fleet"}

**Status:** {proposed | accepted | rejected | superseded by NNN | deprecated}
**Date:** {YYYY-MM-DD of the decision}
**Deciders:** {who agreed; for `rejected`, who rejected}
**Supersedes:** {NNN, or —}

## Context and problem statement

{The forces at play — technical, operational, cost, political — in
value-neutral language; call out the tensions. 2–6 sentences or a short
narrative. Where possible, state the problem as a question:
"Which X do we use, given Y and Z?"}

## Decision drivers

{The criteria that matter for this decision; these become the matrix rows.
4–7, one line each, in priority order:}

- {criterion 1} — {one-clause why it matters here}
- {criterion 2} — {…}
- {criterion 3} — {…}

## Considered options

{Include the status quo when viable; if not, one line on why not. 1–3
sentences per option: what it is, why it's on the table.}

- **A — {name}:** {…}
- **B — {name}:** {…}
- **C — status quo ({what we do today}):** {…}

## Decision matrix

{Weights 1–10 (normalized % shown); scores anchored 0–5: 0 fails outright,
1 poor, 2 marginal, 3 meets, 4 strong, 5 best-in-class. Total =
Σ (score × weight) / (5 × Σweights), as % of the maximum possible.}

| Criterion (weight) | A | B | C (status quo) | Basis |
|---|---|---|---|---|
| {criterion 1} (4 / 40%) | {0–5} | {0–5} | {0–5} | {measurement, link, or judgment} |
| {criterion 2} (3 / 30%) | {0–5} | {0–5} | {0–5} | {…} |
| {criterion 3} (3 / 30%) | {0–5} | {0–5} | {0–5} | {…} |
| **Total** | **{xx}%** | **{xx}%** | **{xx}%** | — |

**Closeness:** {winner} leads {runner-up} by {n} points. {The specific weight
shift or score change that would flip the decision — e.g. "if the weight on
{criterion} drops below {x}, B wins."} {If the decision below does not follow
the table: say so, and why — see Trade-offs.}

## Trade-offs

{Per option: what it buys, what it costs. The prose the numbers can't carry:
reversibility, lock-in, team skills, migration cost, ceiling on future growth.
Mark any option's known ceiling explicitly (what breaks first, and when).}

- **A:** {…}
- **B:** {…}
- **C (status quo):** {…}

## Decision

{One or two full sentences, active voice, no hedging: "We will {X}."}

## Consequences

**Positive:** {what becomes easier / what we gain}
**Negative:** {what becomes harder, what we give up; known ceilings}
**Neutral / follow-ups:** {concrete next steps, each with an owner}

## Open questions & unknowns

{Unresolved questions and assumptions to verify, each with an owner (+ date
where known). End with the premortem line:}

- {question / unknown — owner: {who}}
- Premortem: if this fails in a year, the most likely cause is {…}.

## References

{Links: analysis docs (e.g. docs/ANALYSIS-*.md), specs, papers, prior/successor
decision records, external sources behind any 2026-specific claim. Revisiting
rejected ground? Cite it here: `Reconsiders: NNN`.}
```

## 8. Lineage & sources

The convention this standard is based on, in order of influence:

- **ADR (Architecture Decision Record)** — Michael Nygard, 2011
  ("Documenting Architecture Decisions", cognitect.com); still the current
  convention per Martin Fowler's bliki entry (updated 2026-03-24). Format:
  short, numbered, immutable, `Context / Decision / Consequences / Status`;
  statuses proposed/accepted/deprecated/superseded; one decision per record.
- **MADR** (Markdown Architectural Decision Records, github.com/adr/madr) —
  the community-evolved template: `Context and Problem Statement`, `Decision
  Drivers`, `Considered Options`, `Decision Outcome`, `Pros and Cons of the
  Options`; lives in `docs/decisions/`.
- **AWS & Google Cloud ADR guidance** — both platforms now ship ADR guidance
  (AWS Prescriptive Guidance "Using architectural decision records"; Google
  Cloud Architecture Center ADR pages); use cases: onboarding, architecture
  evolution, sharing best practices.
- **Research base:** Tofan et al. 2014, "Past and Future of Software
  Architectural Decisions: A Systematic Mapping Study" (144 publications) —
  the foundational survey of architectural-decision documentation.
- **Weighted decision matrix** — Pugh matrix, Steven Pugh *Total Design*
  (1980); "trade-off analysis" is a standard technique in the IEEE SWEBOK
  (Software Engineering Process knowledge area).
- **AHP (Analytic Hierarchy Process)** — Thomas Saaty (1980): pairwise
  criterion weighting with consistency check and sensitivity analysis; the
  rigorous fallback when matrix weights are contested, and the origin of the
  "what would flip the decision" requirement in §5.
- **Open questions** — the "open issues" convention from RFC-style processes
  (IETF RFCs, Python PEPs, Go proposals).
- **Premortem** — Gary Klein, "Performing a Premortem" (Harvard
  Business Review, 2007): "if this fails, why?" before commitment.

## 9. Changelog

- **1.6 (2026-09-05)** — external review: status quo optional when not viable (§4, §7); per-criterion score basis (§5); reconsidered-by annotation and `Reconsiders: NNN` (§3, §7); collision-safe numbering (§6); nested headings and one-sitting length (§4).
- **1.5 (2026-09-05)** — self-describing filenames: the standard and its skills file are named `DECISION-RECORDS-STANDARD.md` and `DECISION-RECORDS-SKILLS.md`, in the suite and in project adoption copies.
- **1.4 (2026-09-05)** — record index upgraded to the **structure map**
  (records grouped by component; gaps visible) — the how-side half of the
  suite's coverage hierarchy (README).
- **1.3 (2026-09-04)** — §1 renamed to **Scope, use cases & purpose**
  (explicit use cases and purpose); repo namespaced into per-standard
  directories (companion now at `../functional-specs/FUNCTIONAL-SPECS-STANDARD.md`).
- **1.2 (2026-09-04)** — added companion pointer to the functional-spec
  standard (../functional-specs/FUNCTIONAL-SPECS-STANDARD.md).
- **1.1 (2026-09-04)** — generalized from a single repo to the cross-project
  standard (adoption semantics in the intro, §2, §6); §4 headings made
  normative (exact headings in order, `None.` fillers, stable skeleton);
  added DECISION-RECORDS-SKILLS.md pointer for AI agents.
- **1.0 (2026-09-04)** — initial version: ADR-based format (§4), anchored
  0–5 weighted matrix with mandatory closeness line (§5), analysis↔record
  promotion lifecycle (§2, §6), template (§7).
