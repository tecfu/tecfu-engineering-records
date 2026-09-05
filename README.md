# Tecfu standards — a documentation suite for humans and LLMs

The canonical standards used across our projects. Two core standards, one
pipeline: a **functional spec** says what a change must do; **decision
records** capture the architecturally significant how-and-why decisions made
while building it. Supporting standards close the loop around them.

**A decision record** is a short, numbered, immutable document that captures
one architecturally significant choice: what we picked, the alternatives we
scored, and how close they came.

**A functional spec** is a short, numbered document that pins down one change:
what a user will observably get, as testable requirements with Given/When/Then
criteria that decide when it's done.

Each standard is defined in exactly one file, versioned in-document — AI
agents additionally load the matching SKILLS file.

## How the two core standards overlap and diverge

```text
┌─────────────────────────────┬──────────────────────────────────────┼─────────────────────────────┐
|       FUNCTIONAL SPEC       |              SHARED DNA              |       DECISION RECORD       |
|     the WHAT — behavior     |                                      |   the HOW & WHY — choices   |
|      a user can observe     |· one numbered doc, one topic         |     made while building     |
|                             |· numbers never reused                |                             |
|· numbered, testable FRs     |· immutable once agreed —             |· status quo on the table    |
|· Given/When/Then = done     |  superseded, never rewritten         |· anchored 0–5 matrix        |
|· must/should/may only       |· open questions + premortem          |  + mandatory closeness line |
|· no design content          |· exact headings, same order          |· decision + consequences    |
|· proposal → promotion       |· stranger-proof in 6 months          |· accepted → immutable       |
|· docs/specs/NNN-slug.md     |                                      |· docs/decisions/NNN-slug.md |
└─────────────────────────────┼──────────────────────────────────────┘                             │
                              │  pipeline: spec the WHAT → record the HOW & WHY → build → verify;  │
                              │  "done" = every acceptance criterion has a passing report          │
                              └────────────────────────────────────────────────────────────────────┘
```

Rendered as ASCII so it survives any markdown viewer, including plain `cat`.

## The suite

**Format standards** define a document and its lifecycle; **adoption
standards** bind projects to a settled external convention instead of
inventing one.

| Standard | Kind | Location | Answers |
|---|---|---|---|
| Decision records (architecture) | format | [`decision-records/`](decision-records/DECISION-RECORDS-STANDARD.md) | How is it built, and why this way? |
| Functional specification | format | [`functional-specs/`](functional-specs/FUNCTIONAL-SPECS-STANDARD.md) | What must the system do? |
| Verification report | format | [`verification/`](verification/VERIFICATION-STANDARD.md) | Was the spec actually met — with evidence? |
| Postmortem | format | [`postmortems/`](postmortems/POSTMORTEMS-STANDARD.md) | What broke, why, and what changes now? |
| Agent instructions | format | [`agent-instructions/`](agent-instructions/AGENT-INSTRUCTIONS-STANDARD.md) | How do agents route work into the suite? |
| Changelog | adoption | [`changelogs/`](changelogs/CHANGELOGS-STANDARD.md) | What shipped, and what does the version mean? |
| Design doc | adoption | [`design-docs/`](design-docs/DESIGN-DOCS-STANDARD.md) | How do we explore a design before committing it? |
| Backlog | adoption | [`backlogs/`](backlogs/BACKLOGS-STANDARD.md) | How is tracked work connected to specs? |

## How the suite covers a system

```text
THE SYSTEM — defined in one paragraph: the project's AGENTS.md Summary
├── WHAT it does — the behavior surface
│   ├── docs/specs/NNN-*.md         functional spec: one behavior change, frozen on approval
│   └── docs/verification/NNN-*.md  verification report: one per spec, evidence per criterion
├── HOW it's built — the decision surface
│   ├── docs/decisions/NNN-*.md     decision record: one significant choice, immutable once accepted
│   └── docs/design/<topic>.md      design doc: unnumbered working paper; promotes out, then closes
├── WHEN reality disagrees
│   └── docs/postmortems/NNN-*.md   postmortem: one incident, blameless, every action routed home
├── WHEN it ships
│   └── CHANGELOG.md                changelog: released entries immutable, each cites its NNNs
└── BEFORE any of the above
    ├── docs/ANALYSIS-<TOPIC>.md    record proposal — becomes a decision record or dies
    ├── docs/PROPOSAL-<TOPIC>.md    spec proposal — becomes a functional spec or dies
    └── the tracker                 backlog: Connextra stories; thresholds flag what needs a spec
```

Read it as coverage: every behavior change is promised by a spec and proven
by a report; every significant choice is made in a record; design exploration
feeds both and keeps nothing durable of its own; failures feed back through
postmortems; releases land in the changelog. Non-functional promises
(latency, uptime, internal SLOs that surface only under load, compliance
obligations, security properties) are treated the same way when they can be
stated as measurable outcomes under defined conditions: they become
quantified spec criteria (with measurement method and verification path);
the architectural approaches chosen to meet them become decision records.
See the writing-rules section of the functional-specs standard and the scope
section of the decision-records standard.

**Composition lives in the indexes, not in a new document type.** The two
project index files are the coverage maps:

- `docs/specs/README.md` — the **capability map**: which spec covers each
capability the system exposes.
- `docs/decisions/README.md` — the **structure map**: which records shape
each component of the system.

A capability or component with no rows is a visible gap. Work below every
threshold is deliberately uncovered — a paragraph in the ticket, not a
document.

## Adopting in a project

### Install the validator

The recommended way to use the suite is to install the distributable `ter`
command-line tool. It is a normal Python package and requires Python 3.10 or
newer.

For an isolated global installation, use `pipx`:

```bash
pipx install tecfu-engineering-records
```

Or install it into an existing Python environment with pip:

```bash
python3 -m pip install tecfu-engineering-records
```

Verify the installation:

```bash
ter --version
ter --help
```

### Adopt the suite

From the root of the project you want to bring under the standard:

```bash
ter adopt .
```

This creates `.engineering-records.yml`, which records the suite version and
the standards the project has adopted. The validator treats that manifest as
the project's adoption contract.

Then validate the project:

```bash
ter validate .
```

Validation fails if the adoption manifest is missing or inconsistent, a
standard is missing or stale, or the declared suite/standard versions are not
supported by the installed validator.

`ter adopt` can be run against another project directory as well:

```bash
ter adopt /path/to/project
ter validate /path/to/project
```

If you intentionally need to replace an existing adoption manifest, use:

```bash
ter adopt . --force
```

### Keep the validator current

Check the compatibility information exposed by the installed distribution:

```bash
ter check-update
```

The installed validator is versioned independently from the standards it
validates. Projects can remain on an older supported suite version rather
than being forced to upgrade immediately; when a suite version reaches its
support floor, upgrade the project and migrate its adopted standards as
needed.

For CI, install the same distributable and run the validator as a required
check:

```yaml
- name: Install TecFu Engineering Records validator
  run: python3 -m pip install tecfu-engineering-records

- name: Validate engineering records
  run: ter validate .
```

The canonical repository's own CI additionally runs the validator's
self-tests and the full suite validator. The `validate` job is intentionally
kept as the stable status-check name so repositories can require it through
GitHub branch protection or rulesets.

### Standards files

**Format standards** are adopted by copying the directory's
`<NAME>-STANDARD.md` into the project — `docs/decisions/DECISION-RECORDS-STANDARD.md`,
`docs/specs/FUNCTIONAL-SPECS-STANDARD.md`, `docs/verification/VERIFICATION-STANDARD.md`,
`docs/postmortems/POSTMORTEMS-STANDARD.md` — noting the adopted version in
the project's adoption manifest, and re-copying when you upgrade.

Keep each area's index current — the spec and record indexes double as the
capability and structure maps above — and copy the matching
`<NAME>-SKILLS.md` files into the project's agent skills directory so coding
agents apply the standards unprompted.

**Adoption standards** are not copied — projects follow them where they
stand: `CHANGELOG.md` per Keep a Changelog + SemVer, design docs in
`docs/design/`, the backlog in the project's tracker. The exception is
[agent-instructions](agent-instructions/AGENT-INSTRUCTIONS-STANDARD.md): following it *produces*
the project's `AGENTS.md` — the routing table that tells every agent which
standard applies to which work.

Undecided work lives beside the indexes until promoted:
`docs/ANALYSIS-<TOPIC>.md` (decision records), `docs/PROPOSAL-<TOPIC>.md`
(functional specs). Lifecycle, format, template, and promotion mechanics are
defined only in each standard's own file.

## Tooling

The suite validates itself.

- **`SUITE.md`** — the version manifest: one row per standard. `validate.py`
  fails when the table and the standard files disagree.
- **`ter`** — the distributable validator CLI. Install it with pip/pipx and
  use `ter adopt`, `ter validate`, and `ter check-update` in adopting
  repositories.
- **`validate.py`** — the canonical repository validator (stdlib only).
  `python3 validate.py` checks this repo: naming convention, version/changelog/
  manifest agreement, cross-reference resolution, and Markdown-link
  integrity. `python3 validate.py --project <path>` checks an adopting
  project: numbering (monotonic, contiguous, unique), spec↔verification 1:1
  pairing, exact heading order read from the standards' own templates,
  unfilled placeholders, index rows, the docs/ADOPTION.md adoption manifest
  against the copied standards and the current suite (staleness), and the
  document graph — every relative Markdown link resolves, and supersedes /
  `Reconsiders:` / `superseded by` / `Spec:` / index-row edges point at
  documents that exist. Content sanity: decision-matrix arithmetic
  (weights 1-10, scores 0-5, per-criterion Basis) with the Closeness margin
  recomputed from the matrix totals, and acceptance-criteria structure
  (`AC-N.M` ids, unique, under their `FR-N` group). Fixture-based integration
  tests (`tests/test_fixtures.py`) run the real validator against
  deliberately-broken project fixtures in `tests/fixtures/`.

- **`.github/workflows/validate.yml`** — runs all three on every push and PR.
