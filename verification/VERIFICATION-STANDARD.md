# Verification Report — Standard

**Version:** 1.2 (2026-09-05)

The single-file definition of how our projects prove a spec was delivered:
one report per approved spec, mapping every acceptance criterion to
re-runnable evidence — written so a stranger can see not just what was
promised, but that it was met.

**Adoption:** a project adopts this standard by copying this file to
`docs/verification/VERIFICATION-STANDARD.md` in that project, keeping its reports and
index there, and noting the adopted version. **AI agents:** `VERIFICATION-SKILLS.md`
(next to this file) defines the workflows and the report-validation
checklist; follow it when asked to write or re-run a report.

**Companion standards:** `../functional-specs/FUNCTIONAL-SPECS-STANDARD.md` — the criteria a
report verifies come from an approved spec's Acceptance criteria section;
`../decision-records/DECISION-RECORDS-STANDARD.md` — a report never decides how to fix a
failure; that is a record.

## 1. Scope, use cases & purpose

**Scope:** a report is required for every approved spec before the work is
declared done — one report per spec, covering every criterion. Not for:
changes with no approved spec (PR checks and the ticket paragraph cover
them), exploratory testing notes, or deciding how to fix what failed (that
is a decision record).

**Use cases:**

- declaring "done" with evidence instead of assertion;
- re-verification after a fix or a spec amendment — re-run, re-report;
- audits and handoffs — a stranger sees what was tested, where, and when;
- catching silent scope drift — a criterion with no evidence shows as
  `blocked`, not invisible.

**Purpose:** so "done" is a fact with evidence, not a claim — the spec's
acceptance criteria decide done, the report shows they were met.

## 2. File conventions

- Reports live in the adopting project's `docs/verification/`, named after
  the spec they verify: `NNN-<spec-slug>.md` — the number **is the spec's
  number** (`001-offline-export-for-telemetry.md` verifies
  `docs/specs/001-offline-export-for-telemetry.md`). One report per spec.
- A report is written when implementation is ready to check, not before.
- Copy the template from §6 to start.

## 3. Lifecycle

Reports have no proposal phase — they are written after the fact. The header
`Status:` is the verdict of the **latest run**: `pass`, `partial`, or
`failed`. Each run appends a dated line to Runs (§4) recording the spec
revision it checked; the Results table always reflects the latest run. When
a spec is superseded, its last report stays, unedited.

The report index in the project's `docs/verification/README.md` must stay
current (one line per report: spec number, verdict, date).

## 4. Format

Sections, in order. The report **MUST** contain exactly these headings, in
this order — a section that does not apply is written as `None.` rather than
deleted; nested `###` headings MAY be added beneath them. Keep the report
to one sitting — if the Results table outgrows a screen, the spec it
verifies is probably too big.

1. **Title** — "Verification of 001 — Offline export for telemetry".
2. **Status / Date / Spec / Verifier** — four header lines.
3. **Environment** — build/commit tested, version, where it ran
   (local / CI / staging), when.
4. **Results** — the per-criterion table (§5).
5. **Gaps** — fail/blocked criteria only, with owner and next step.
6. **Runs** — one dated line per verification run, with the spec revision
    checked.
7. **References** — spec, related records, run logs.

## 5. Rules

- **Every criterion, no omissions.** Each acceptance criterion (`AC-N.M`)
  from the spec appears as a row, in spec order. More rows than criteria
  means the report is wrong — or the spec needed an amendment.
- **Evidence must be re-runnable.** A command plus expected output, a test
  name, or a link to a run log. "Manually checked, looks fine" is not
  evidence — state exactly what was done and observed, or script it.
- **No evidence = `blocked`, never `pass`.**
- **Evidence names its type.** `deterministic` (same result every run),
  `environment-dependent` (re-run in the recorded Environment), or
  `observational` (a named person did X and observed Y). Re-runnable is not
  the same as reproducible — say which one you have.
- **The report never changes the contract.** A failure means fix, amend
  (spec §3), or supersede — never reinterpret a criterion to pass it. If
  testing shows the criterion itself was wrong, that is a dated amendment in
  the spec's Amendments section.
- **Status must match the table:** any fail/blocked → `partial` or `failed`;
  all pass → `pass`.

## 6. The template

```markdown
# Verification of {NNN} — {spec title}

**Status:** {pass | partial | failed}
**Date:** {YYYY-MM-DD of the latest run}
**Spec:** {link to docs/specs/NNN-<slug>.md}
**Verifier:** {who or what ran it}

## Environment

{Build/commit tested, version, where it ran (local / CI / staging), when.}

## Results

{One row per acceptance criterion (`AC-N.M`) from the spec — all of them, in
order. Evidence must be re-runnable: a command plus expected output, a test
name, or a link to a run log — and must name its type.}

| Criterion | Result | Type | Evidence |
|---|---|---|---|
| AC-1.1: Given…, when…, then… | {pass / fail / blocked} | {deterministic / environment-dependent / observational} | {test name, command, or link} |
| AC-1.2: … | {…} | {…} | {…} |

## Gaps

{Fail and blocked criteria only: reason, owner, next step. None. if pass.}

- {criterion — reason — owner: {who}, next: {…}}
- None.

## Runs

{One dated line per verification run, with the spec revision checked (short
commit of the spec file, or `amendment N`); the latest run's verdict is the
header Status:.}

- {YYYY-MM-DD — {pass/partial/failed} — spec @ {short commit} — {scope, e.g.
  "12/12 criteria"}}

## References

{Links: the spec, related decision records, prior reports, run logs.}
```

## 7. Lineage & sources

- **ISO/IEC/IEEE 29148:2018** — "verifiable" as a defining characteristic of
  a requirement; verification as a first-class activity, not an afterthought.
- **Given/When/Then — Dan North, "Introducing BDD" (2006)** — acceptance
  criteria written to be runnable; this report is where they get run.
- **Karl Wiegers & Joy Beatty, *Software Requirements* (2013)** —
  requirements verification practice.
- **House DNA** — the immutability rule: the report records verdicts, the
  spec keeps owning the contract.

## 8. Changelog

- **1.2 (2026-09-05)** — external review: AC-N.M rows (§4–§6); typed evidence — deterministic / environment-dependent / observational (§5); spec revision recorded per run (§3, §4, §6); nested headings and one-sitting length (§4).
- **1.1 (2026-09-05)** — self-describing filenames: the standard and its skills file are named `VERIFICATION-STANDARD.md` and `VERIFICATION-SKILLS.md`, in the suite and in project adoption copies.
- **1.0 (2026-09-04)** — initial version: one report per spec keyed by the
  spec's number (§2), run-log lifecycle (§3), exact-heading format (§4),
  re-runnable-evidence rule (§5), template (§6).
