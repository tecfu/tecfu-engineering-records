# Backlog — Standard (adoption)

**Version:** 1.1 (2026-09-05)

An **adoption standard**: the backlog lives in the project's issue tracker —
the suite defines no tracker format. This file fixes only the house rules
that connect tracked work to the suite's documents.

**Adoption:** projects follow this standard; the file stays in the suite
repo. **AI agents:** `BACKLOGS-SKILLS.md` (next to this file).

## 1. Scope, use cases & purpose

**Scope:** tracked work items (epics, stories, tasks) and their connection
to the suite. Not for: tracker fields, states, and boards (the tracker owns
those), prioritization method, or sprint process.

**Use cases:**

- grooming an epic into stories;
- deciding whether a work item needs a spec, an analysis, or neither;
- linking delivered work back to the documents that promised it.

**Purpose:** so the tracker stays the single place work is *tracked*, while
the suite stays the single place work is *specified* — no duplication in
either direction.

## 2. House rules (thin)

- **One home:** the project's tracker, named in its `AGENTS.md`
  (agent-instructions standard). The suite never duplicates tracker state,
  and the tracker never duplicates suite documents.
- **Story shape:** the Connextra format — "As a {role}, I want {capability},
  so that {benefit}" — one capability per item. The same format functional
  specs use (functional-specs §5), so a story graduates into a spec without
  rewriting.
- **Extraction thresholds:** an item that will change user-observable
  behavior needs a spec before implementation; an item that is a contested
  choice needs an `ANALYSIS-*` doc → decision record; anything else stays a
  plain task. The functional-specs §1 threshold governs — when in doubt, a
  paragraph in the ticket, not a document.
- **Links go one way:** suite documents cite tracker IDs in References;
  tracker items may link back, but the suite's index tables never depend on
  the tracker.

## 3. Lineage & sources

- **Connextra user-story format**, popularized by Mike Cohn, *User Stories
  Applied* (2004) — already the suite's story DNA (functional-specs §5).
- **House DNA** — the threshold rules from functional-specs §1 and
  decision-records §1, applied at grooming time.

## 4. Changelog

- **1.1 (2026-09-05)** — self-describing filenames: the standard and its skills file are named `BACKLOGS-STANDARD.md` and `BACKLOGS-SKILLS.md`, in the suite and in project adoption copies.
- **1.0 (2026-09-04)** — initial adoption: tracker-owns-tracking,
  Connextra story shape, extraction thresholds (§2).
