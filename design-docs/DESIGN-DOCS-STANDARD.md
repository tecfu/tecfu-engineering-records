# Design Doc — Standard (adoption)

**Version:** 1.3 (2026-09-05)

An **adoption standard**: design docs follow the well-known Google design-doc
convention; this file fixes only where they live, how they relate to the
suite, and what must happen before one is closed.

**Position in the suite:** the design doc is the **working paper** — where a
design gets explored in prose, diagrams, and dead ends. It is mutable and
un-numbered precisely because it is not the record: durable outputs are
promoted out of it into the numbered documents. The suite deliberately has
no bespoke design-doc format — it has the doc that feeds the specs and
records.

**Adoption:** projects follow this standard; the file stays in the suite
repo. **AI agents:** `DESIGN-DOCS-SKILLS.md` (next to this file).

## 1. Scope, use cases & purpose

**Scope:** the exploratory document for how to build something non-trivial —
system context, options sketched, trade-offs thought through. Not for:
decided things (decision records), promised behavior (functional specs), or
evidence of done (verification reports) — when a design doc starts producing
those as final output, it has finished its job.

**Use cases:**

- starting a non-trivial feature or system;
- capturing a design discussion that would otherwise live in chat;
- onboarding a second implementer into the thinking before records exist.

**Purpose:** so exploration has a home that doesn't have to be tidy — while
guaranteeing nothing durable stays buried in it.

## 2. File conventions

- Live in the project's `docs/design/`, named `<topic>.md` (kebab-case, no
  number — working papers don't take numbers).
- Mutable and unversioned. When a design is abandoned, mark the top with a
  link to its successor instead of deleting (cheap history).
- One topic per doc.
- The project's `docs/design/README.md` holds the design-doc index (one
  line per doc: topic, status, promoted-to) and must stay current — design
  docs are unnumbered, so the index is the only inventory.

## 3. The promotion rule

A design doc is **closed only when its durable outputs have landed**:

- contested or architecturally significant choices → decision records
  (`ANALYSIS-*` → `NNN`, decision-records §6);
- user-visible behavior → functional specs (`PROPOSAL-*` → `NNN`,
  functional-specs §6);
- open questions that matter → the Open questions sections of those
  documents, each with an owner.

Until then it stays open. "Do nothing" can be the right answer: a design
exploration that concludes no durable output is warranted closes with
`Promoted to: None — concluded no durable output was warranted`, one line
recording the conclusion. Otherwise, closing also requires: every
`Promoted to:` link resolves to a real document, and the premortem line is
present in Open questions — postmortems look for it. A closed design doc
carries a `Promoted to:` line listing what it produced, if anything.

## 4. Format (adopted)

Google design-doc sections, kept thin: **Context & scope; Goals & non-goals;
Design; Alternatives considered; Rollout plan; Open questions.** The six
headings MUST be present, in this order — a section that does not apply is
written as `None.` — but the convention owns the depth: see the template
and lineage; we don't redefine it.

## 5. Template (thin)

```markdown
# {topic}

**Status:** {open | closed} — Promoted to: {links, once closed}

## Context & scope

{Why this is being designed, for whom, under what constraints.}

## Goals & non-goals

{What this design tries to achieve; what it deliberately doesn't.}

## Design

{The proposal: diagrams, components, data, flows — the how, at whatever
depth the topic needs.}

## Alternatives considered

{Options rejected and why — the raw material for decision records.}

## Rollout plan

{How it ships, in what order, what could go wrong.}

## Open questions

{Each with an owner; a premortem line once the design is near final.}
```

## 6. Lineage & sources

- **Google design docs** — "Design docs at Google" (Malte Ubl & Ian Lewis);
  the goals/non-goals + alternatives shape, already cited in the suite.
- **House promotion mechanics** — decision-records §6 and functional-specs
  §6; a design doc is their shared upstream.

## 7. Changelog

- **1.3 (2026-09-05)** — external review: closing with no durable output is a
  legitimate terminal outcome — `Promoted to: None — concluded no durable
  output was warranted` (§3); the close-time gate applies only when there is
  something to promote.
- **1.2 (2026-09-05)** — self-describing filenames: the standard and its skills file are named `DESIGN-DOCS-STANDARD.md` and `DESIGN-DOCS-SKILLS.md`, in the suite and in project adoption copies.
- **1.1 (2026-09-05)** — index requirement (§2), close-time gate: promotion
  links resolve + premortem present (§3), MUST-level headings (§4).
- **1.0 (2026-09-04)** — initial adoption: Google design-doc convention
  (§4), working-paper lifecycle with the promotion rule (§2, §3), thin
  template (§5).
