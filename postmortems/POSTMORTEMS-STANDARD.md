# Postmortem — Standard

**Version:** 1.2 (2026-09-05)

The single-file definition of how our projects learn from failure: one
blameless document per incident, written so the premortem question ("if this
fails, the most likely cause is…") finally gets its answer — and the answer
changes something.

**Adoption:** a project adopts this standard by copying this file to
`docs/postmortems/POSTMORTEMS-STANDARD.md` in that project, keeping its postmortems and
index there, and noting the adopted version. **AI agents:** `POSTMORTEMS-SKILLS.md`
(next to this file) defines the workflows and the validation checklist; follow
it when asked to write or publish a postmortem.

**Companion standards:** `../decision-records/DECISION-RECORDS-STANDARD.md` — postmortem
actions that are architecturally significant become records;
`../functional-specs/FUNCTIONAL-SPECS-STANDARD.md` — actions that change user-visible behavior
amend or supersede specs; `../verification/VERIFICATION-STANDARD.md` — a spec that passed
verification but disappointed anyway still gets a postmortem.

## 1. Scope, use cases & purpose

**Scope:** a postmortem is required for any incident with material user
impact, any broken promise an approved spec made (shipped and disappointed),
and any premortem line that came true. Material means: users noticed, data
was at risk, a promise broke, or the failure class could repeat; transient
single-user blips with nothing learned can stay a ticket paragraph. Not for:
bugs caught before release (a failing
verification report and a fix cover them), near-misses with nothing learned,
or individual mistakes without systemic cause — the postmortem is about the
system that allowed the mistake. When in doubt, write it: an over-written
postmortem is cheap, a repeated incident is not.

**Use cases:**

- production incidents and outages;
- features that shipped but didn't deliver — the spec's premortem answered;
- repeated mistakes — the second time something breaks the same way;
- onboarding honesty — new engineers see what actually goes wrong here.

**Purpose:** so failure converts to system change, not blame — every action
lands in a document that owns it.

## 2. File conventions

- Postmortems live in the adopting project's `docs/postmortems/`, named
  `NNN-short-noun-phrase.md` — 3-digit zero-padded sequential number,
  monotonic, **never reused**, assigned when written — re-list the directory
  immediately before naming; if your number was taken while you worked,
  take the next one (`validate.py` flags duplicates).
- One incident per postmortem. A week with three small incidents gets three
  short ones, not one epic.
- Copy the template from §6 to start.

## 3. Lifecycle

| Status | Meaning |
|---|---|
| `draft` | written; actions not yet agreed |
| `published` | actions have owners and dates; the document is frozen |
| `superseded by NNN` | replaced by a newer postmortem; the old one stays, unedited |

Published postmortems are **immutable**: action progress is tracked where the
action was routed (tracker, record, spec) — never by editing the postmortem.
If the story materially changes, write the next one and supersede this one.

The postmortem index in the project's `docs/postmortems/README.md` must stay
current (one line per postmortem).

## 4. Format

Sections, in order. The postmortem **MUST** contain exactly these headings,
in this order — a section that does not apply is written as `None.` rather
than deleted; nested `###` headings MAY be added beneath them. Keep it as
short as the incident deserves — past roughly 800 words of prose (tables
excluded), tighten.

1. **Title** — short noun phrase: "Fleet overflow lost telemetry batches".
2. **Status / Date / Author / Incident** — four header lines.
3. **Summary** — 1–3 sentences: what broke, who/what it hit, how long.
4. **Impact** — scope and severity: users, data, duration, cost where known.
5. **Timeline** — dated events from trigger to resolution, factual, UTC.
6. **Root causes** — system conditions that made it possible; speculation
   labeled; ends with the premortem check.
7. **Lessons** — surprises, what the premortem missed, what went well.
8. **Actions** — each with owner, date, and destination.
9. **References** — specs, records, reports, dashboards, tickets.

## 5. Rules

- **Blameless:** name systems, processes, and designs — never people. "The
  deploy script had no rollback check", never "Alice forgot".
- **Facts in Timeline; analysis in Root causes;** label speculation as
  speculation.
- **Fix the class, not the instance:** prefer an action that prevents the
  category of failure over one that patches this occurrence.
- **Every action has an owner, a date, and a destination:** architecture →
  decision record; behavior → spec amendment or supersession; tracking →
  tracker item. An action without a destination is a wish.
- **Answer the premortem:** quote the premortem line from the relevant spec
  or record and say whether it predicted this. This is the loop-closer. If
  no applicable premortem exists (infrastructure, third-party, and
  operational failures often have none), write `Premortem check: None — no
  applicable premortem existed.` — never manufacture a connection.

## 6. The template

```markdown
# {short noun-phrase title, e.g. "Fleet overflow lost telemetry batches"}

**Status:** {draft | published | superseded by NNN}
**Date:** {YYYY-MM-DD of publication}
**Author:** {who wrote it}
**Incident:** {date, or link to the tracker/ticket}

## Summary

{1–3 sentences: what broke, who or what it hit, how long it lasted.}

## Impact

{Scope and severity: users, data, duration, cost where known. No blame,
no causes — those come later.}

## Timeline

{Dated events from trigger to resolution, factual, times in UTC. No
analysis here — only what happened.}

- {YYYY-MM-DD HH:MM UTC — {event}}

## Root causes

{Why this was possible: the system conditions, not the people. Contributing
factors welcome; label speculation as speculation. End with the premortem
check:}

- {cause 1 — {one-clause evidence}}
- Premortem check: {"{the premortem line from spec/record NNN}" — predicted
  / didn't predict this, because {…}.}
  (or: `None — no applicable premortem existed.`)

## Lessons

{What surprised us, what the premortem missed, what went well and should be
kept.}

## Actions

{Each with owner, date, and destination.}

- {action — owner: {who}, by: {date} — routed to: {record / spec / tracker}}

## References

{Links: specs, decision records, verification reports, dashboards, tickets.}
```

## 7. Lineage & sources

- **Google SRE, "Postmortem Culture"** (sre.google) — blameless postmortems;
  focus on systems over individuals; the Impact/Timeline/Actions shape.
- **5 Whys** — Taiichi Ohno, Toyota Production System: root cause over
  proximate cause.
- **Premortem** — Gary Klein (HBR, 2007): the line both house standards
  mandate, which this standard answers after the fact.

## 8. Changelog

- **1.2 (2026-09-05)** — external review: materiality threshold in scope (§1); premortem check may be `None` (§5, §6); nested headings and length guidance (§4); collision-safe numbering (§2).
- **1.1 (2026-09-05)** — self-describing filenames: the standard and its skills file are named `POSTMORTEMS-STANDARD.md` and `POSTMORTEMS-SKILLS.md`, in the suite and in project adoption copies.
- **1.0 (2026-09-04)** — initial version: blameless format with mandatory
  premortem check (§4, §5), draft→published lifecycle with routing rule
  (§3, §5), template (§6).
