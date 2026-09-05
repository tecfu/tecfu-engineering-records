# Engineering-records adoption (canonical suite)

This repository **defines** the `tecfu-engineering-records` suite; it is not
an adopting project. Adopters use `.engineering-records.yml` created by
`ter adopt` in *their* repositories.

For reference, the current suite version and format-standard versions are:

| Standard | Kind | Version | File |
|---|---|---|---|
| Decision records | format | 1.9 | decision-records/DECISION-RECORDS-STANDARD.md |
| Functional specification | format | 1.6 | functional-specs/FUNCTIONAL-SPECS-STANDARD.md |
| Verification report | format | 1.2 | verification/VERIFICATION-STANDARD.md |
| Postmortem | format | 1.2 | postmortems/POSTMORTEMS-STANDARD.md |
| Agent instructions | adoption | 1.2 | agent-instructions/AGENT-INSTRUCTIONS-STANDARD.md |
| Changelog | adoption | 1.1 | changelogs/CHANGELOGS-STANDARD.md |
| Design doc | adoption | 1.4 | design-docs/DESIGN-DOCS-STANDARD.md |
| Backlog | adoption | 1.1 | backlogs/BACKLOGS-STANDARD.md |

See `SUITE.md` and `src/ter/suite.json` for the machine-readable contract.
