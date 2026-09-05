---
name: backlogs
description: >
  Execute the Backlog Standard (backlogs/BACKLOGS-STANDARD.md): groom tracked work
  into Connextra stories, and decide which items need a spec, an analysis,
  or neither. Use whenever the user asks to groom an epic, split work into
  stories, write user stories, or check whether a work item needs suite
  documents.
---

# Backlogs — agent workflows

Source of truth: `BACKLOGS-STANDARD.md` (next to this file). If this file ever
disagrees with `BACKLOGS-STANDARD.md`, the standard wins — fix this file.

## Skill: groom an epic

Trigger: the user asks to split an epic/feature into stories or groom the
backlog.

1. Split into Connextra stories — "As a {role}, I want {capability}, so that
   {benefit}" — one capability per item, in the project's tracker.
2. Apply the extraction thresholds (BACKLOGS-STANDARD.md §2) to each story:
   - changes user-observable behavior → flag it: needs a `PROPOSAL-*` spec
     before implementation (functional-specs §1);
   - is a contested choice → flag it: needs an `ANALYSIS-*` doc → decision
     record (decision-records §1);
   - neither → leave it a plain task.
3. Report the split with the flags — don't create the suite documents
   unprompted; grooming flags, the owner decides.

## Skill: check a work item

Trigger: the user asks whether an item needs a spec or a record.

1. Run the thresholds: observable behavior change? contested significant
   choice? neither?
2. Answer with the routing (agent-instructions §4) and, if below every
   threshold, say so plainly — the paragraph in the ticket is the right size.

## Validation checklist

- [ ] Stories use the Connextra format, one capability each.
- [ ] Stories live in the tracker — never recreated as suite documents.
- [ ] Flags cite the threshold that fired (functional-specs §1 /
      decision-records §1).
- [ ] Suite documents cite tracker IDs in References, not the other way
      around.

## Anti-patterns

- Mirroring tracker state into the suite, or requirements into the tracker —
  one home each.
- Stories bundling several capabilities — split again.
- Writing a spec or ANALYSIS doc during grooming — grooming flags the need;
  the owner schedules it.
