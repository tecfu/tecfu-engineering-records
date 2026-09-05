---
name: postmortems
description: >
  Execute the Postmortem Standard (postmortems/POSTMORTEMS-STANDARD.md): write a
  blameless postmortem for an incident or a disappointed feature, publish it
  with routed actions, supersede one, and validate against the format. Use
  whenever the user asks for a postmortem, incident writeup, retrospective
  on a failure, or asks why something broke (answer from the postmortems).
---

# Postmortems — agent workflows

Source of truth: `POSTMORTEMS-STANDARD.md` (next to this file; an adopting project keeps
its copy at `docs/postmortems/POSTMORTEMS-STANDARD.md`). These workflows are the
standard, operationalized. If this file ever disagrees with `POSTMORTEMS-STANDARD.md`,
the standard wins — fix this file.

## Skill: write a postmortem

Trigger: an incident reached users, an approved spec shipped and
disappointed, or a premortem line came true.

1. Check the threshold (POSTMORTEMS-STANDARD.md §1). Below it — bug caught pre-release,
   nothing learned: a fix and a failing verification report cover it.
2. Copy the template (`POSTMORTEMS-STANDARD.md` §6) verbatim; save as
   `docs/postmortems/NNN-<topic-slug>.md` with the next free number —
   re-list the directory immediately before naming; if your number was
   taken while you worked, take the next one (`validate.py` flags
   duplicates),
   `Status: draft`.
3. Fill every `{placeholder}`. Keep §4 headings exactly, in order; a section
   that does not apply gets `None.`.
4. Timeline: facts only, dated, UTC. Root causes: systems, not people;
   label speculation. Never name a person as a cause.
5. End Root causes with the premortem check — find the premortem line in the
   relevant spec or record and quote it.
6. Actions: owner + date + destination each. Route them: architecture →
   ANALYSIS doc → decision record; behavior → spec amendment/supersession;
   tracking → tracker item.
7. Run the validation checklist; present the draft for review.
8. No index row yet — the row appears at publication.

## Skill: publish a postmortem

Trigger: actions are agreed.

1. Set `Status: published` and `Date:` to the publication date.
2. Add the index row to the project's `docs/postmortems/README.md`.
3. Touch nothing else. From here the document is frozen — action progress
   lives where each action was routed, never in the postmortem.

## Skill: supersede a postmortem

Trigger: the story materially changed after publication.

1. Write a new postmortem (write skill above).
2. In the old one, change **only** the `Status:` line to `superseded by NNN`.
3. Never delete it.

## Validation checklist (run on every postmortem you write or touch)

- [ ] Filename: `^\d{3}-[a-z0-9-]+\.md$`.
- [ ] Headings exactly in §4 order: Title; Status/Date/Author/Incident
      header lines; Summary; Impact; Timeline; Root causes; Lessons; Actions;
      References.
- [ ] `Status:` ∈ {draft, published, superseded by NNN}.
- [ ] No `{placeholders}` remain anywhere.
- [ ] Timeline has dates and times; no analysis inside it.
- [ ] Root causes name systems, not people; speculation is labeled.
- [ ] Premortem check present in Root causes, quoting the source line.
- [ ] Every action has owner + date + routed destination.
- [ ] If `published` and you are not running the supersede skill: stop —
      published postmortems are immutable (POSTMORTEMS-STANDARD.md §3).

## Anti-patterns

- Naming a person as a cause — blame is the fastest way to kill honest
  postmortems.
- Actions without a destination ("improve monitoring") — route it or cut it.
- Patching the instance while the class stays broken.
- Updating a published postmortem's body instead of superseding it.
- Merging several incidents into one epic — one incident per postmortem.
