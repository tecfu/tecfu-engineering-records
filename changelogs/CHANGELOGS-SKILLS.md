---
name: changelogs
description: >
  Execute the Changelog Standard (changelogs/CHANGELOGS-STANDARD.md): add Keep a
  Changelog entries to Unreleased, cut a release with a SemVer bump, and
  validate the changelog. Use whenever the user asks to update the
  changelog, write release notes, cut/bump a release or version, or asks
  what changed between versions (answer from CHANGELOG.md).
---

# Changelogs — agent workflows

Source of truth: `CHANGELOGS-STANDARD.md` (next to this file), which adopts
[Keep a Changelog](https://keepachangelog.com) 1.1.0 and
[SemVer](https://semver.org) 2.0.0. These workflows are the standard,
operationalized. If this file ever disagrees with `CHANGELOGS-STANDARD.md` or the
adopted conventions, the conventions win — fix this file.

## Skill: add entries

Trigger: work lands that a consumer would care about (or the user asks to
"update the changelog").

1. Open `CHANGELOG.md`; everything goes under `## [Unreleased]`.
2. Pick the category: Added / Changed / Deprecated / Removed / Fixed /
   Security. One line per consumer-visible change, prose for humans.
3. Cite the suite: a change closing an approved spec cites it
   ("…implements spec 001"); a significant decision cites the record NNN.
4. No requirements, no matrices, no internal jargon — link the spec or
   record instead.

## Skill: cut a release

Trigger: the owner declares a release.

1. Decide the bump from the content of `Unreleased` against SemVer: any
   breaking change → MAJOR; new consumer-facing functionality → MINOR;
   fixes only → PATCH. The bump matches the class of change, not its size.
2. Replace `## [Unreleased]` with `## [x.y.z] — YYYY-MM-DD`; start a fresh
   empty `Unreleased` with the standard categories.
3. Touch nothing in previously released sections — ever.
4. Tag per project convention; the changelog entry and the tag agree on the
   version string.

## Validation checklist

- [ ] Format matches Keep a Changelog 1.1.0 (categories, `Unreleased`,
      dated `## [x.y.z]` headings).
- [ ] Version strings are valid SemVer and consistent between changelog,
      tag, and manifest.
- [ ] Entries cite the specs/records they close where applicable.
- [ ] No released section was edited — history only grows.
- [ ] Entries are prose a consumer can read, not internal ticket dumps.

## Anti-patterns

- Editing a released section — fix forward with a new entry.
- Bumping MAJOR/MINOR/PATCH by vibe instead of by change class.
- "Misc fixes and improvements" — every entry names what changed and cites
  its spec/record.
- Duplicating spec requirements inside changelog entries — link, don't copy.
- Changelog-as-commit-log — consumer-visible changes only.
