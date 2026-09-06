"""Migrate functional specs from 1.6 to 1.7.

The new final `Implementation work` section is metadata and does not change
requirements. This migration appends `None.` to specs that do not yet track
external implementation work. It is idempotent and leaves existing work
tracking untouched.
"""

from pathlib import Path


_SECTION = "## Implementation work"


def migrate(root: Path):
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"project does not exist: {root}")

    specs = root / "docs" / "specs"
    if not specs.is_dir():
        return

    for path in sorted(specs.glob("*.md")):
        if path.name == "README.md" or path.name.endswith("-STANDARD.md"):
            continue
        text = path.read_text(encoding="utf-8")
        if _SECTION in text:
            continue
        path.write_text(
            text.rstrip() + "\n\n" + _SECTION + "\n\nNone.\n",
            encoding="utf-8",
        )
