# Spec migrations

Migrations are optional, explicit transformations for releases that require
consumer document changes. They are not run automatically: an adopter reviews
the diff and commits the result in its own repository.

## Naming

Name each migration `vX_Y_to_vA_B.py` and expose:

```python
def migrate(root):
    """Transform the adopter at Path root in an idempotent way."""
```

Keep migrations deterministic, idempotent, stdlib-only where practical, and
safe to run from CI. A migration should change documents, not silently change
architecture or application code.

## 1.6 → 1.7

`v1_6_to_v1_7.py` appends the new final `Implementation work` metadata section
to functional specs that do not already contain it. It writes `None.` so the
absence of externally tracked work is explicit. Existing work tracking and all
requirements remain unchanged.

Run:

```bash
python3 tools/migrate.py --list
python3 tools/migrate.py --from 1.6 --to 1.7 /path/to/project
```

For a release with no document migration, no migration module is necessary;
the adopter still updates its declared version and runs the validator.
