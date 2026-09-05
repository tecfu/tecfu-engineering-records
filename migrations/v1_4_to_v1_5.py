"""Example 1.4 -> 1.5 migration scaffold.

The 1.5 release currently requires no document rewrite. This no-op module is
kept as an executable example and proves that a release can declare an
explicit migration path even when the migration is empty.
"""


def migrate(root):
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"project does not exist: {root}")
