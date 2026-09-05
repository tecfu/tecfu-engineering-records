---
name: design-docs
description: >
  Execute the Design Doc Standard (design-docs/DESIGN-DOCS-STANDARD.md): write a design
  doc for exploring how to build something, and close it by promoting its
  durable outputs into specs and decision records. Use whenever the user
  asks to explore a design, write up an architecture exploration, or close
  out a design discussion.
---

# Design docs — agent workflows

Source of truth: `DESIGN-DOCS-STANDARD.md` (next to this file), adopting the Google
design-doc convention. If this file ever disagrees with `DESIGN-DOCS-STANDARD.md`, the
standard wins — fix this file.

## Skill: write a design doc

Trigger: non-trivial work needs its how explored before anything is decided
or promised.

1. Check the threshold first (`DESIGN-DOCS-STANDARD.md` §1):
   - single-PR / obvious trade-offs → no design doc; a paragraph in the
     ticket is enough;
   - behavior already agreed → `PROPOSAL-*` spec;
   - choice already contested and significant → `ANALYSIS-*` decision
     record;
   - a short spike answers the questions faster → prefer the spike;
   - writing "to show broad consideration" or for promo visibility → refuse
     and say so.
   A design doc is only for the murky middle.
2. Copy the template (`DESIGN-DOCS-STANDARD.md` §5); save as
   `docs/design/<topic>.md`, `Status: open`. Keep it short — proportional
   depth, not exhaustive theater.
3. Design and Alternatives are the meat — sketch options and what kills
   them (including status quo and "already solved elsewhere"); that is the
   raw material for decision records later. Inventing alternatives for
   their own sake is an anti-pattern.
4. Open questions each get an owner; add the premortem line when the design
   is near final.

## Skill: close a design doc

Trigger: the design is settled enough to commit.

1. Run the promotion rule (`DESIGN-DOCS-STANDARD.md` §3): every contested choice →
   decision record; every user-visible behavior → spec; every mattered open
   question → a document's Open questions with an owner.
2. Set `Status: closed` and add the `Promoted to:` line listing what it
   produced; confirm every link in it resolves and the premortem line is
   present in Open questions (DESIGN-DOCS-STANDARD.md §3 close-time gate).
3. Add or update the index row in the project's `docs/design/README.md`
   (topic, status, promoted-to).
4. Closing with nothing to promote is legitimate — set `Promoted to: None —
   concluded no durable output was warranted`. "Do nothing" can be the
   right answer; one line records it.

## Validation checklist

- [ ] Lives at `docs/design/<topic>.md` — kebab-case, no number.
- [ ] Headings per §4: Context & scope; Goals & non-goals; Design;
      Alternatives considered; Rollout plan; Open questions.
- [ ] Open questions have owners; premortem line present once near-final.
- [ ] If `closed`: Promoted to: line present, every promoted link
      resolves to a real document, and the premortem line is present in
      Open questions.
- [ ] Index row in `docs/design/README.md` matches the doc's current
      status.
- [ ] No numbered-document content claimed as final inside the doc —
      decisions and behavior live in records and specs, not here.

## Anti-patterns

- A design doc as the final record — decided things belong in decision
  records, promised behavior in specs.
- Design docs that never close — the promotion rule is the point.
- Numbering design docs or freezing them like records — they are working
  papers.
- Skipping Alternatives considered when real options exist — unpromoted, it
  is the most valuable section for the records that follow.
- Cargo-cult docs: inventing alternatives for their own sake, padding every
  section, or writing a design doc for a single-PR change "to show broad
  consideration". Prefer a spike or a ticket paragraph.
- Treating "Promoted to: None" as failure — killing a weak idea early is a
  successful outcome.
