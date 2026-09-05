# Changelog — Standard (adoption)

**Version:** 1.1 (2026-09-05)

An **adoption standard**: it defines no new format. It binds our projects to
two settled conventions — **Keep a Changelog** and **Semantic Versioning** —
and wires them into the suite's pipeline. Where this file and the adopted
conventions disagree, the conventions win.

**Adoption:** a project adopts by creating `CHANGELOG.md` at its root per
Keep a Changelog and versioning releases per SemVer. This file stays in the
suite repo — projects follow it, they don't copy it. **AI agents:**
`CHANGELOGS-SKILLS.md` (next to this file) defines the release and entry workflows.

## 1. Scope, use cases & purpose

**Scope:** every project release and its human-readable record. Not for:
suite-document versioning (each standard versions itself in-document),
tracker history, or git tags alone — the changelog is the prose layer over
the tags.

**Use cases:**

- cutting a release — what happened, in consumer language;
- agents asked to "update the changelog" or "bump the version";
- consumers checking what changed and whether it breaks them.

**Purpose:** so consumers get the same changelog shape and the same version
semantics everywhere — without us maintaining a format.

## 2. What we adopt

- **Keep a Changelog** (keepachangelog.com, 1.1.0): one `CHANGELOG.md` at
  the project root; an `Unreleased` section; entries categorized as Added /
  Changed / Deprecated / Removed / Fixed / Security; prose written for
  humans, newest first.
- **Semantic Versioning** (semver.org, 2.0.0): MAJOR.MINOR.PATCH — breaking
  changes bump MAJOR, features MINOR, fixes PATCH; pre-release and build
  metadata as specified there.

## 3. House rules (thin)

- **Released sections are immutable.** Entries land in `Unreleased`; at
  release they move to a `## [x.y.z] — YYYY-MM-DD` heading. Never edit a
  released section — fix forward with a new entry (house DNA: same rule as
  accepted records and approved specs).
- **Cite the suite.** An entry that closes an approved spec cites it
  ("…implements spec 001"); an entry landing a significant decision cites
  the record. The changelog links; it never duplicates requirements or
  matrices.
- **Docs-only changes get entries too** — suite documents that change ship
  under Changed, citing the standard's version bump.
- **The bump matches the class of change** — a breaking removal is MAJOR
  even if it feels small.

## 4. Starter skeleton

```markdown
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed
### Fixed
```

## 5. Lineage & sources

- **Keep a Changelog** — Olivier Lacan and contributors.
- **Semantic Versioning** — Tom Preston-Werner.
- **House DNA** — the immutability-and-supersede rule the rest of the suite
  runs on, applied to released entries.

## 6. Changelog

- **1.1 (2026-09-05)** — self-describing filenames: the standard and its skills file are named `CHANGELOGS-STANDARD.md` and `CHANGELOGS-SKILLS.md`, in the suite and in project adoption copies.
- **1.0 (2026-09-04)** — initial adoption: Keep a Changelog 1.1.0 + SemVer
  2.0.0 (§2), immutability and citation house rules (§3), starter skeleton
  (§4).
