---
name: functional-specs
description: >
  Execute the Functional Specification Standard (FUNCTIONAL-SPECS-STANDARD.md): write a
  proposed spec (PROPOSAL-*.md), write a numbered spec for an already-agreed
  change, promote a spec on approval/decline, supersede a spec, and validate
  specs against the format. Use whenever the user asks to write a functional
  spec, define requirements, specify what a feature must do, draft acceptance
  criteria, promote a proposal, or asks what a feature is supposed to do
  (answer from the specs).
---

# Functional specs — agent workflows

Source of truth: `FUNCTIONAL-SPECS-STANDARD.md` (next to this file; an adopting project keeps its
copy at `docs/specs/FUNCTIONAL-SPECS-STANDARD.md`). These workflows are the standard,
operationalized. If this file ever disagrees with `FUNCTIONAL-SPECS-STANDARD.md`, the
standard wins — fix this file.

What a spec is for: **what** a user-visible change must do. How to build it
and why: decision records (`../decision-records/SKILLS.md` in this repo,
project's `docs/decisions/`). If you find design content in a spec, move it out; if a
decision changes user-visible behavior, update the spec (supersede skill).

## Skill: write a spec

Trigger: the user asks to specify a feature/change, write requirements, or
define acceptance criteria. First check the threshold (FUNCTIONAL-SPECS-STANDARD.md §1:
observable behavior change). Below it — refactor, behavior-preserving fix,
small tweak: a paragraph in the ticket/PR, not a spec.

1. Copy the template (`FUNCTIONAL-SPECS-STANDARD.md` §7) verbatim.
2. Save it as:
   - `docs/PROPOSAL-<TOPIC>.md` with `Status: proposed` when not yet agreed
     (uppercase kebab topic, e.g. `PROPOSAL-OFFLINE-EXPORT.md`);
   - `docs/specs/NNN-<topic-slug>.md` with the next free number when already
     agreed (lowercase kebab, e.g. `001-offline-export-for-telemetry.md`).
3. Fill every `{placeholder}`. Keep the §4 headings exactly, in order; a
   section that does not apply gets `None.` — never delete a heading.
4. Write requirements per §5: numbered `FR-N`, one testable statement each,
   must/should/may deliberate, no design content, boundary cases covered or
   explicitly disclaimed.
5. Write acceptance criteria: ≥1 Given/When/Then per requirement, runnable as
   a test.
6. Run the validation checklist below; fix everything it flags before
   presenting the spec.
7. Indexing: numbered spec → add its row to the project's
   `docs/specs/README.md`. Proposed spec → no index row yet; the row appears
   at promotion.

## Skill: promote a spec

Trigger: the approver approves or declines a proposed `PROPOSAL-<TOPIC>.md`.

1. `git mv docs/PROPOSAL-<TOPIC>.md docs/specs/NNN-<topic-slug>.md` using the
   next free number — never reuse, never renumber.
2. Set `Status:` to `approved` or `declined`; set `Date:` to the approval
   date.
3. Add the index row to the project's `docs/specs/README.md`.
4. Touch nothing else in the spec.

## Skill: supersede a spec

Trigger: after approval, what the feature does must change — not just what a
requirement meant.

1. Write a new spec for the new behavior (write skill above; it starts as a
   proposed PROPOSAL file unless the replacement is already agreed).
2. In the old spec, change **only** the `Status:` line to
   `superseded by NNN`. This is the single permitted edit to an approved
   spec.
3. Never delete the old spec; the record of what was promised when work
   started is the point.

Clarifications only (a requirement meant X all along, now written down):
append a dated one-liner under Amendments instead. Requirement text is never
rewritten.

## Validation checklist (run on every spec you write or touch)

- [ ] Filename: `^\d{3}-[a-z0-9-]+\.md$` (spec) or `^PROPOSAL-[A-Z0-9-]+\.md$` (proposed).
- [ ] Headings exactly in §4 order: Title; Status/Date/Author/Approver header
      lines; Summary; Goals & non-goals; Users & scenarios; Functional
      requirements; Acceptance criteria; Open questions & unknowns;
      Amendments; References.
- [ ] `Status:` ∈ {proposed, approved, declined, superseded by NNN}.
- [ ] No `{placeholders}` remain anywhere.
- [ ] Every requirement: numbered `FR-N`, single (non-compound) testable
      statement, must/should/may used deliberately.
- [ ] Vague-word scan: no unquantified "fast", "robust", "user-friendly",
      "efficient", "intuitive" in requirements.
- [ ] No design content (components, libraries, data models, "we'll use X") —
      that belongs in a decision record.
- [ ] Every requirement has ≥1 Given/When/Then acceptance criterion.
- [ ] Goals & non-goals both present (non-goals may be "None.", heading stays).
- [ ] Open questions each have an owner; premortem line present.
- [ ] If the spec is `approved` and you are not running the promote or
      supersede skill: stop — approved specs are frozen (FUNCTIONAL-SPECS-STANDARD.md §3).

## Anti-patterns

- Design content in a spec ("we'll use Redis") — split it into a
  `docs/ANALYSIS-*.md` and, once decided, a decision record.
- Unquantified adjectives, compound requirements, criteria that can't fail.
- Rewriting an approved spec's requirement text instead of appending to
  Amendments or superseding.
- Merging two features into one spec — split into two documents (§2).
- Numbering proposed specs, renumbering specs, or reusing numbers.
- Writing a spec for something below the §1 threshold (refactors, regression
  fixes, small tweaks) — a paragraph in the ticket is the right size.
