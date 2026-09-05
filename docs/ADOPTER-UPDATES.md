# Adopter update automation

The canonical suite can open update PRs in registered adopting repositories.

Add repositories to `adopters.json` as:

```json
{
  "repositories": [
    {"repository": "owner/project", "branch": "main"}
  ]
}
```

The `update adopters` workflow runs when a release is published or manually.
It requires the repository secret `ADOPTER_UPDATE_TOKEN`, with the minimum
write/pull-request permissions necessary for the registered repositories.
A GitHub App installation token is preferred over a long-lived personal token.

The updater changes only `.engineering-records.yml`. The adopter's CI then
validates copied standards and reports any migration work required. This keeps
an upstream release from silently modifying consumer documentation.
