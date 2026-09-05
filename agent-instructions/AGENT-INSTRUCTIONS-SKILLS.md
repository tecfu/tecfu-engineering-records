---
name: agent-instructions
description: >
  Execute the Agent Instructions Standard (agent-instructions/AGENT-INSTRUCTIONS-STANDARD.md):
  bootstrap a project's AGENTS.md with the routing table, commands, and
  boundaries; maintain it as the suite grows. Use whenever the user asks to
  write or update AGENTS.md / agent instructions, or asks where a piece of
  work should be documented (answer from the routing table).
---

# Agent instructions — agent workflows

Source of truth: `AGENT-INSTRUCTIONS-STANDARD.md` (next to this file). These workflows are the
standard, operationalized. If this file ever disagrees with `AGENT-INSTRUCTIONS-STANDARD.md`,
the standard wins — fix this file.

## Skill: bootstrap a project's AGENTS.md

Trigger: a project adopts the suite and has no `AGENTS.md` (or an unrelated
one).

1. Copy the template (`AGENT-INSTRUCTIONS-STANDARD.md` §5) to the project root as `AGENTS.md`.
2. Fill Summary from the project's README — one paragraph, no marketing.
3. Fill the routing table with the suite directories that project adopted,
   using real paths (e.g. `decision-records/DECISION-RECORDS-STANDARD.md` →
   `docs/decisions/DECISION-RECORDS-STANDARD.md` in the project). Drop rows for standards the
   project didn't adopt — never route to something that isn't there.
4. Fill Commands by running each once; record what actually works, not what
   the README claims.
5. Keep Boundaries verbatim from the template — they encode suite-wide
   immutability and evidence rules.
6. One page maximum; cut anything that isn't routing, commands, or
   boundaries.

## Skill: maintain AGENTS.md

Trigger: the project adopts a new standard, commands change, or routing
proved ambiguous in practice.

1. Update only the affected row/section; the file is living — normal commit,
   no ceremony.
2. If a routing row was ambiguous in a real session: sharpen the row's
   trigger wording. Ambiguity in the table becomes mistakes at scale.

## Validation checklist

- [ ] Exactly the §3 headings, in order: Summary; Standards; Commands;
      Boundaries.
- [ ] One page or less.
- [ ] Every routing row points to a standard the project actually adopted,
      at a path that exists.
- [ ] Commands were executed successfully at least once before being
      recorded.
- [ ] Boundaries kept intact (no softening of the never-list).
- [ ] No duplication of a standard's content — routing and pointers only.

## Anti-patterns

- Copying standards into AGENTS.md instead of linking them — the file loads
  into every session; duplication taxes every call.
- Routing to a standard the project hasn't adopted.
- Recording commands that were never run.
- Adding per-task instructions, style guides, or process essays — this file
  is a router, not a handbook.
