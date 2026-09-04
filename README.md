# Architectural Decision Record Standard

The canonical Decision Records Standard used across our projects: one short
document per architecturally significant decision, written so a stranger six
months from now can see what we chose, why, and how close the alternatives
came.

**This README only explains the repo. The standard is defined in exactly one
file: [STANDARD.md](STANDARD.md).** AI agents should additionally load
[SKILLS.md](SKILLS.md), which operationalizes the standard into workflows and
a validation checklist.

## What's in here

| File | Role |
|---|---|
| `STANDARD.md` | the single-file definition: format, lifecycle, scoring, template — versioned in-document |
| `SKILLS.md` | for AI agents: how to write, promote, and supersede records; the validation checklist |

## Adopting the standard in a project

1. Copy `STANDARD.md` into the project at `docs/decisions/STANDARD.md` (the
   project-local copy; note the adopted version, and re-copy when you upgrade).
2. Create the project's `docs/decisions/README.md`: a short explanation that
   links to the standard (no definition — that lives only in `STANDARD.md`)
   plus the record index table.
3. Optionally copy `SKILLS.md` into the project's agent skills directory so
   coding agents apply the standard unprompted.
4. Write records by copying the template (STANDARD.md §7): an undecided
   recommendation lives as `docs/ANALYSIS-<TOPIC>.md` with `Status:
   proposed`; a decided record goes straight into
   `docs/decisions/NNN-<topic-slug>.md`. Promotion mechanics: STANDARD.md §6.
5. Keep the project's index current — one row per numbered record.

## Two rules worth knowing without opening the standard

- An `accepted` record is **never edited**. A changed decision is a new,
  higher-numbered record; the old one is marked `superseded by NNN` and kept.
- Every record is scored with an anchored 0–5 weighted decision matrix and a
  mandatory **closeness line**: how close the alternatives came, and the
  specific change that would flip the decision.
