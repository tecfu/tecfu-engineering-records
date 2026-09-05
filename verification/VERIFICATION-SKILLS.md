---
name: verification
description: >
  Execute the Verification Report Standard (verification/VERIFICATION-STANDARD.md): write
  a report proving a spec's acceptance criteria pass, re-run a report after a
  fix or amendment, and validate reports against the format. Use whenever the
  user asks to verify a spec, prove "done", check acceptance criteria, or
  produce evidence that requirements are met.
---

# Verification reports — agent workflows

Source of truth: `VERIFICATION-STANDARD.md` (next to this file; an adopting project keeps
its copy at `docs/verification/VERIFICATION-STANDARD.md`). These workflows are the
standard, operationalized. If this file ever disagrees with `VERIFICATION-STANDARD.md`,
the standard wins — fix this file.

## Skill: write a verification report

Trigger: implementation of an approved spec is ready to check, or the user
asks to verify a spec / prove done.

1. Read the spec's Acceptance criteria section — the source of truth for the
   report's rows.
2. Copy the template (`VERIFICATION-STANDARD.md` §6) verbatim; save as
   `docs/verification/NNN-<spec-slug>.md` — the spec's number, not a new one.
3. Run every criterion. Record the environment (commit, version, where) in
   §Environment and one row per criterion in §Results with re-runnable
   evidence (command + expected output, test name, or run-log link).
4. No evidence for a criterion → `blocked`, never `pass`.
5. Set header `Status:` from the table: any fail/blocked → `partial` or
   `failed`; all pass → `pass`. Add the dated line to §Runs.
6. Run the validation checklist below; fix everything it flags.
7. Add the index row to the project's `docs/verification/README.md`.

If implementation is incomplete, report what is real: `partial` with gaps —
never a pass you intend to earn later.

## Skill: re-run a report

Trigger: a fix landed or the spec was amended; the user asks to re-verify.

1. Re-run all criteria against the new build; update §Environment, §Results,
   §Gaps, and header `Status:` to the latest run.
2. Append a dated line to §Runs — history is never deleted, only appended.
3. Update the index row.
4. If a criterion itself changed: stop — that is a spec amendment
   (functional-specs §3) or supersession, not an edit here.

## Validation checklist (run on every report you write or touch)

- [ ] Filename: `^\d{3}-[a-z0-9-]+\.md$` and the number matches an existing
      spec in `docs/specs/`.
- [ ] Headings exactly in §4 order: Title; Status/Date/Spec/Verifier header
      lines; Environment; Results; Gaps; Runs; References.
- [ ] `Status:` ∈ {pass, partial, failed} and consistent with the Results
      table (any fail/blocked ⇒ not `pass`).
- [ ] One row per acceptance criterion, in spec order — none skipped, none
      invented.
- [ ] Every `pass` row has re-runnable evidence (command, test name, or log
      link) — no "manually checked".
- [ ] Every fail/blocked row appears in Gaps with an owner and next step.
- [ ] Runs has a dated line for the latest run matching the header Status.
- [ ] No `{placeholders}` remain anywhere.

## Anti-patterns

- Passing a criterion without re-runnable evidence — the most expensive lie
  in the pipeline.
- Adding rows for behavior the spec never promised — that is scope drift;
  propose a spec amendment instead.
- Reinterpreting a failing criterion to pass it — fix, amend, or supersede.
- Deleting or rewriting past Runs lines — append, never erase.
- Writing a report for a spec that isn't approved yet — verify what exists,
  not what is proposed.
