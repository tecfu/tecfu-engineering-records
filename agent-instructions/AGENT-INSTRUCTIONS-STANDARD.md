# Agent Instructions — Standard

**Version:** 1.1 (2026-09-05)

The single-file definition of the document that wires this suite into a
project's coding agents: what a project's `AGENTS.md` contains, so every
agent — and every human — routes documentation to the right standard without
being told twice.

**Adoption:** this standard's deliverable is the project's own `AGENTS.md`,
written per §3–§5. The standard itself stays in the suite repo — projects
follow it, they don't copy it. **AI agents:** `AGENT-INSTRUCTIONS-SKILLS.md` (next to this file)
defines the bootstrap and maintenance workflows.

**Companion standards:** all of them — the routing table (§4) names each;
that table is the point of this file.

## 1. Scope, use cases & purpose

**Scope:** defines the agent instructions file for a project — root
`AGENTS.md`: what routes to which standard, which commands agents run, and
what they must never do. Not for: per-task prompts, agent tool configuration,
or the suite's `<NAME>-SKILLS.md` workflows themselves (each standard's
directory owns those).

**Use cases:**

- a new coding-agent session starts cold and still routes documents
  correctly;
- a human asks an agent to "write the spec" and gets the house format
  without re-explaining;
- preventing known agent failure modes: claiming done without verification,
  editing accepted records, writing documents below threshold.

**Purpose:** so the suite applies itself — agents follow the same routing
every session, with no tribal knowledge.

## 2. File conventions

- One file per project: `AGENTS.md` at the project root. Keep it to **one
  page** — it loads into every agent session; length taxes every call.
- No numbering, no lifecycle: it is a living document, unlike the numbered
  records and specs it routes to. Changes are ordinary commits.
- Point to the suite, don't copy it: link each standard's
  `<NAME>-STANDARD.md` and `<NAME>-SKILLS.md`; copy the SKILLS files into
  the agent skills directory when the tooling supports it.

## 3. Required content

`AGENTS.md` MUST contain exactly these headings, in this order:

1. **Summary** — what the project is, one paragraph.
2. **Standards** — the routing table (§4), naming where each standard lives.
3. **Commands** — build, test, lint, verify: the exact commands agents run,
   no discovery required.
4. **Boundaries** — the never-list: never edit an accepted decision record or
   an approved spec's requirement text; never declare done without a passing
   verification report; never write a suite document below its threshold; a
   paragraph in the ticket is the right size for small work.

## 4. The routing table

The heart of the file. Every row: trigger → document → standard to load.

| When the work… | Write | Standard |
|---|---|---|
| changes what users observe | a spec (`PROPOSAL-*`) | `functional-specs/` |
| is a contested, architecturally significant choice | a record (`ANALYSIS-*`) | `decision-records/` |
| implements an approved spec | a verification report | `verification/` |
| broke something that reached users | a postmortem | `postmortems/` |
| needs design exploration first | a design doc (unnumbered) | `design-docs/` |
| ships a release | changelog entries | `changelogs/` |
| lands in the tracker | a story (Connextra) | `backlogs/` |
| is below every threshold | a paragraph in the ticket/PR | — |

## 5. The template

```markdown
# AGENTS.md — {project name}

## Summary

{One paragraph: what this project is, its users, its stack.}

## Standards

This project follows the Tecfu documentation suite. Route documents by the
table; load the named standard's `<NAME>-STANDARD.md` (and its
`<NAME>-SKILLS.md` if you are an agent) before writing anything.

{The §4 table, with paths filled in.}

## Commands

- Build: {command}
- Test: {command}
- Lint: {command}
- Verify: {command, e.g. the spec-verification runner}

## Boundaries

- Never edit an accepted decision record or an approved spec's requirement
  text; supersede or amend instead.
- Never declare a spec done without a passing verification report in
  docs/verification/.
- Never write a suite document for work below its threshold — a paragraph in
  the ticket is the right size.
- When two standards could apply, the routing table wins; when the table is
  ambiguous, ask.
```

## 6. Lineage & sources

- **AGENTS.md convention** (agents.md; adopted across coding agents 2025) —
  the root-file shape; also the earlier `CLAUDE.md` and
  `.cursorrules`/`copilot-instructions.md` practice it consolidated.
- **House skills-file pattern** — every standard in this suite ships agent
  workflows next to its definition; this standard routes between them.

## 7. Changelog

- **1.1 (2026-09-05)** — self-describing filenames: the standard and its skills file are named `AGENT-INSTRUCTIONS-STANDARD.md` and `AGENT-INSTRUCTIONS-SKILLS.md`, in the suite and in project adoption copies.
- **1.0 (2026-09-04)** — initial version: required AGENTS.md headings (§3),
  routing table (§4), template (§5).
