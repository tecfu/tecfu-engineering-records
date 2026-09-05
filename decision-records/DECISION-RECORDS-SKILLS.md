---
name: decision-records
description: >
  Execute the Architectural Decision Record Standard (DECISION-RECORDS-STANDARD.md): write a
  proposed decision record (ANALYSIS-*.md), write a numbered record for an
  already-made decision, promote a record on accept/reject, supersede a
  record, and validate records against the format. Use whenever the user asks
  to document a decision, record a design choice, weigh alternatives, promote
  an analysis, or asks why something was decided (answer from the records).
---

# Decision records — agent workflows

Source of truth: `DECISION-RECORDS-STANDARD.md` (next to this file; an adopting project keeps its copy
at `docs/decisions/DECISION-RECORDS-STANDARD.md`). These workflows are the standard,
operationalized. If this file ever disagrees with `DECISION-RECORDS-STANDARD.md`, the standard
wins — fix this file.

## Skill: write a decision record

Trigger: the user asks to record/document a decision, choose between
alternatives, or "write an ADR". First check the significance test
(DECISION-RECORDS-STANDARD.md §1: affects structure, non-functional characteristics,
dependencies, interfaces, or construction technique — or is expensive to
reverse). Below the threshold: a normal code comment or commit message, not a
record.

1. Copy the template (`DECISION-RECORDS-STANDARD.md` §7) verbatim.
2. Save it as:
   - `docs/ANALYSIS-<TOPIC>.md` with `Status: proposed` when the owner has
     not decided yet (uppercase kebab topic, e.g. `ANALYSIS-HYBRID-OVERFLOW.md`);
   - `docs/decisions/NNN-<topic-slug>.md` with the next free number when the
     decision is already made (lowercase kebab, e.g. `001-swarm-for-onprem-fleet.md`).
     Re-list the directory immediately before naming — if your number was
     taken while you worked, take the next one (`validate.py` flags duplicates).
3. Fill every `{placeholder}`. Keep the §4 headings exactly, in order; a
   section that does not apply gets `None.` — never delete a heading.
4. Build the matrix (§5): 4–7 criteria with weights 1–10 (normalized to 100%),
   scores 0–5 per the anchor table, totals as % of maximum. Include the
   status quo as an option — "do nothing" is a real option — unless it is
   not viable, in which case say why in one line.
5. Add the mandatory **Closeness** line: the margin between the top two, and
   the specific weight shift or score change that would flip the winner.
6. Run the validation checklist below; fix everything it flags before
   presenting the record.
7. Indexing: numbered record → add its row to the project's
   `docs/decisions/README.md`. Proposed record → no index row yet; the row
   appears at promotion.

## Skill: promote a record

Trigger: the owner accepts or rejects a proposed `ANALYSIS-<TOPIC>.md`.

1. `git mv docs/ANALYSIS-<TOPIC>.md docs/decisions/NNN-<topic-slug>.md`
   using the next free number — never reuse, never renumber. Re-list the
   directory immediately before naming; if your number was taken while you
   worked, take the next one (`validate.py` flags duplicates).
2. Set `Status:` to `accepted` or `rejected`; set `Date:` to the decision
   date.
3. Add the index row to the project's `docs/decisions/README.md`.
4. Touch nothing else in the record.

## Skill: supersede a record

Trigger: circumstances changed and a decided record no longer holds.

1. Write a new record for the new decision (write skill above; it starts as a
   proposed ANALYSIS file unless the replacement is already decided).
2. In the old record, change **only** the `Status:` line to
   `superseded by NNN`. Status lines are the only in-place edit a decided
   record ever gets: supersede here, or append `— reconsidered by NNN` to a
   rejected record (DECISION-RECORDS-STANDARD.md §3).
3. Never delete the old record; its history is the point.

## Validation checklist (run on every record you write or touch)

- [ ] Filename: `^\d{3}-[a-z0-9-]+\.md$` (record) or `^ANALYSIS-[A-Z0-9-]+\.md$` (proposed).
- [ ] Headings exactly in §4 order: Title; Status/Date/Deciders/Supersedes
      header lines; Context and problem statement; Decision drivers;
      Considered options; Decision matrix; Trade-offs; Decision; Consequences;
      Open questions & unknowns; References.
- [ ] `Status:` ∈ {proposed, accepted, rejected, superseded by NNN, deprecated}.
- [ ] No `{placeholders}` remain anywhere.
- [ ] Matrix: 4–7 criteria; weights 1–10; normalized weights sum to 100%;
      scores ∈ 0–5; totals = Σ(score × weight) / (5 × Σweights) as %.
- [ ] Status quo appears in Considered options and as a matrix column.
- [ ] **Closeness** line present, with margin and a concrete flip condition.
- [ ] Decision is 1–2 sentences, active voice, "We will …".
- [ ] Open questions end with the premortem line.
- [ ] If the record is `accepted` and you are not running the promote or
      supersede skill: stop — accepted records are immutable (DECISION-RECORDS-STANDARD.md §3).

## Anti-patterns

- Numbering proposed records, renumbering records, or reusing numbers.
- Skipping the status-quo option or the closeness line to save effort.
- Letting the matrix pick the winner silently: if the Decision disagrees
  with the matrix, Trade-offs MUST say why.
- Merging two decisions into one record — split into two documents (§2).
- Editing an accepted record in place, or deleting a superseded one.
