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

## Install

Package version tracks the suite version (**1.6.0** ↔ suite **1.5**). Requires Python 3.10+.

```bash
# From this repository (until published to PyPI)
python3 -m pip install "git+https://github.com/tecfu/tecfu-engineering-records.git"

# Or, once on PyPI:
# pipx install tecfu-engineering-records
# python3 -m pip install tecfu-engineering-records

ter --version
ter --help
```

Adopt a project in three steps:

```bash
ter adopt .                          # create .engineering-records.yml
ter install-standards .              # copy format STANDARD (+ SKILLS) files
ter validate .                       # check the adoption contract
```

Partial adoption: `ter adopt . --standard decision-records --standard functional-specs`.

Full walkthrough (format vs adoption standards, CI, upgrades): [Adopting in a project](#adopting-in-a-project).

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

The recommended way to use the suite is the distributable `ter` CLI (Python
3.10+). Package version tracks the suite version (currently **1.6.0** ↔ suite **1.5**).

```bash
pipx install tecfu-engineering-records
# or: python3 -m pip install tecfu-engineering-records
ter --version
ter --help
```

> Until the package is published to PyPI, install from this repository:
> `python3 -m pip install "git+https://github.com/tecfu/tecfu-engineering-records.git"`.

### Adopt the suite

```bash
# 1. Create the adoption manifest (declares format standards by default)
ter adopt .

# Partial adoption — only the standards you need:
ter adopt . --standard decision-records --standard functional-specs

# 2. Copy the declared format STANDARD (+ SKILLS) files from the package
ter install-standards .

# 3. Validate the contract
ter validate .
```

`.engineering-records.yml` is the **authoritative adoption contract**. It
records the suite version and which standards the project has declared.

- **Format standards** (`functional-specs`, `decision-records`,
  `verification`, `postmortems`) are **copied** into `docs/.../` when
  declared. `ter install-standards` does this from the packaged files.
- **Adoption standards** (`agent-instructions`, `changelogs`, `design-docs`,
  `backlogs`) are **followed in place** — do **not** copy their STANDARD
  files. They produce `AGENTS.md`, `CHANGELOG.md`, `docs/design/`, and
  tracker stories respectively.

`ter validate` checks the manifest, that each declared format standard is
present and at the expected version, and that the corresponding `docs/` area
and index exist. For full document-graph checks (numbering, heading order,
spec↔verification pairing, link integrity, matrix arithmetic), also run the
suite's richer validator against the project:

```bash
python3 /path/to/tecfu-engineering-records/validate.py --project .
python3 /path/to/tecfu-engineering-records/validate_matrix.py   # optional
```

Replace an existing manifest with `ter adopt . --force`. Overwrite stale
standard copies with `ter install-standards . --force` after reviewing the
diff.

### Enforce with git hooks

Gate commits and pushes on `ter validate` via pre-commit and/or
`ter hooks install`. See [Git hooks](#git-hooks).


### Keep the validator current

```bash
ter check-update
# prints: suite=<version>  and  minimum-supported=<floor>
```

When the suite advances, bump `spec.version` in `.engineering-records.yml`,
run any migration under `migrations/`, then `ter install-standards . --force`
and `ter validate .`.

CI example:

```yaml
- name: Install TecFu Engineering Records validator
  run: python3 -m pip install tecfu-engineering-records
- name: Validate engineering records
  run: ter validate .
```

### Standards files (summary)

| Kind | Standards | In the project |
|------|-----------|----------------|
| format | functional-specs, decision-records, verification, postmortems | Copy `*-STANDARD.md` (+ skills) under `docs/.../` |
| adoption | agent-instructions, changelogs, design-docs, backlogs | Follow in place; do not copy the STANDARD file |

Undecided work lives beside the indexes until promoted:
`docs/ANALYSIS-<TOPIC>.md` (decision records), `docs/PROPOSAL-<TOPIC>.md`
(functional specs). Lifecycle and templates live only in each standard's own
file.



## Git hooks

`ter validate` is non-interactive (exit `0` / `1`). Use `--quiet` so success
is silent and failures still print to stderr. The CLI walks parents for
`.engineering-records.yml`, so hooks work from subdirectories.

Hooks must not mutate the tree: do **not** run `ter adopt` or
`ter install-standards` inside a hook.

### Option A — `ter hooks install` (pre-push, no extra tools)

```bash
ter hooks install          # writes .git/hooks/pre-push — no git config changes
ter hooks uninstall        # remove the ter-managed shim only
```

- Runs before every **push**; blocks the push on validation failure.
- Prefer the installed `ter` package; falls back to a suite vendored at
  `scripts/ter/validate.py` when present.
- Idempotent; refuses to overwrite a non-ter pre-push hook unless you pass
  `--force`.
- Bypass one push with `git push --no-verify`. Keep CI as the backstop.

### Option B — pre-commit (path-filtered, on commit)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/tecfu/tecfu-engineering-records
    rev: v1.6.0   # pin a release tag
    hooks:
      - id: ter-validate
```

```bash
pipx install pre-commit   # once
pre-commit install
pre-commit run ter-validate --all-files
```

Runs `ter validate --quiet` when staged paths touch
`.engineering-records.yml` or `docs/specs|decisions|verification|postmortems/`.
Skip one commit with `SKIP=ter-validate git commit`, or
`git commit --no-verify` when you must.

Until the package is on PyPI, pre-commit installs the hook environment from
this Git repo at the pinned `rev`.

### Hand-rolled hook

```bash
#!/bin/sh
# .git/hooks/pre-commit  (chmod +x) — or pre-push
ter validate --quiet || exit 1
```

Prefer Option A or B unless you need a custom layout.

### What the hook checks

`ter validate` checks the **adoption contract**: manifest, declared format
standard copies and versions, and required docs areas/indexes.

For full **document-graph** checks (numbering, headings, pairing, links), run
in CI (or pre-push if you accept the cost):

```bash
python3 /path/to/tecfu-engineering-records/validate.py --project .
```

Nested suite checkouts (directories that contain `SUITE.md`, e.g. a vendored
`scripts/ter/`) are skipped by project-mode validation so template sources
and suite test fixtures are not treated as adopter content.

You can combine both options: pre-commit on day-to-day commits, and
`ter hooks install` to gate pushes.


## Tooling

The suite validates itself.

- **`SUITE.md`** — the version manifest: one row per standard. `validate.py`
  fails when the table and the standard files disagree.
- **`ter`** — the distributable adoption CLI (`validate`, `adopt`, `install-standards`, `check-update`). Install with pip/pipx and
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
