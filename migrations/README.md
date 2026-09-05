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

Run:

```bash
python3 tools/migrate.py --list
python3 tools/migrate.py --from 1.4 --to 1.5 /path/to/project
```

For a release with no document migration, no migration module is necessary;
the adopter still updates its declared version and runs the validator.
