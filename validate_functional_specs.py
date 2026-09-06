#!/usr/bin/env python3
"""Validate functional-spec implementation traceability.

This complements validate.py. It checks the optional final `Implementation work`
section in adopting projects and verifies that work items point at real FR-N and
AC-N.M identifiers from the same spec.

Usage:
    python3 validate_functional_specs.py --project PATH
    python3 validate_functional_specs.py --self-test
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

NUM_RE = re.compile(r"^\d{3}-[a-z0-9-]+\.md$")
PROPOSAL_RE = re.compile(r"^PROPOSAL-[A-Z0-9-]+\.md$")
HEADING_RE = re.compile(r"(?m)^## (.+?)\s*$")
FR_RE = re.compile(r"\bFR-(\d+)\b")
AC_RE = re.compile(r"\bAC-(\d+)\.(\d+)\b")
SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")


def section(text: str, heading: str) -> str | None:
    """Return the body of one top-level section, or None when absent."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line == f"## {heading}":
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for i in range(start, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return "\n".join(lines[start:end]).strip()


def identifiers(text: str, pattern: re.Pattern[str]) -> set[str]:
    return {m.group(0) for m in pattern.finditer(text)}


def check_spec(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []

    headings = [h.strip() for h in HEADING_RE.findall(text)]
    if "Implementation work" not in headings:
        return [f"{path}: missing final 'Implementation work' section"]
    if headings[-1] != "Implementation work":
        problems.append(f"{path}: 'Implementation work' must be the final top-level section")

    work = section(text, "Implementation work")
    if work is None or not work or work == "None.":
        return problems

    requirements = section(text, "Functional requirements") or ""
    criteria = section(text, "Acceptance criteria") or ""
    known_fr = identifiers(requirements, FR_RE)
    known_ac = identifiers(criteria, AC_RE)

    lines = [line.strip() for line in work.splitlines() if line.strip()]
    table_lines = [line for line in lines if line.startswith("|")]
    if not table_lines:
        return problems + [
            f"{path}: non-empty Implementation work must use a Markdown table or `None.`"
        ]
    if len(table_lines) < 3:
        return problems + [f"{path}: Implementation work table has no data rows"]

    header = [cell.strip().lower() for cell in table_lines[0].strip("|").split("|")]
    required_columns = {"work item", "requirements", "status"}
    missing = required_columns - set(header)
    if missing:
        problems.append(
            f"{path}: Implementation work table is missing columns: {', '.join(sorted(missing))}"
        )
        return problems

    separator_cells = [cell.strip() for cell in table_lines[1].strip("|").split("|")]
    if len(separator_cells) != len(header) or not all(SEPARATOR_RE.fullmatch(cell) for cell in separator_cells):
        problems.append(f"{path}: Implementation work table is missing its separator row")
        return problems

    indexes = {name: header.index(name) for name in required_columns}
    ac_index = header.index("acceptance criteria") if "acceptance criteria" in header else None

    for row_no, row in enumerate(table_lines[2:], start=3):
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if len(cells) != len(header):
            problems.append(
                f"{path}: Implementation work row {row_no} has {len(cells)} cells; expected {len(header)}"
            )
            continue

        work_item = cells[indexes["work item"]]
        requirement_ids = identifiers(cells[indexes["requirements"]], FR_RE)
        status = cells[indexes["status"]]
        if not work_item:
            problems.append(f"{path}: Implementation work row {row_no} has an empty Work item")
        if not requirement_ids:
            problems.append(f"{path}: Implementation work row {row_no} must reference at least one FR-N")
        for fr in sorted(requirement_ids):
            if fr not in known_fr:
                problems.append(f"{path}: Implementation work row {row_no} references missing {fr}")
        if not status:
            problems.append(f"{path}: Implementation work row {row_no} has an empty Status")

        if ac_index is not None:
            for ac in sorted(identifiers(cells[ac_index], AC_RE)):
                if ac not in known_ac:
                    problems.append(f"{path}: Implementation work row {row_no} references missing {ac}")

    return problems


def validate_project(root: Path) -> list[str]:
    specs_dir = root / "docs" / "specs"
    if not specs_dir.is_dir():
        return [f"missing {specs_dir}"]
    problems: list[str] = []
    for path in sorted(specs_dir.glob("*.md")):
        if path.name == "README.md" or path.name.endswith("-STANDARD.md"):
            continue
        if not (NUM_RE.match(path.name) or PROPOSAL_RE.match(path.name)):
            continue
        problems.extend(check_spec(path))
    return problems


def self_test() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        spec_dir = root / "docs" / "specs"
        spec_dir.mkdir(parents=True)
        spec = spec_dir / "001-export.md"
        spec.write_text(
            """# Export\n\n**Status:** approved\n\n## Summary\n\nx\n\n## Goals & non-goals\n\nNone.\n\n## Users & scenarios\n\nNone.\n\n## Functional requirements\n\n- **FR-1:** The system MUST export records.\n- **FR-2:** The system MUST reject invalid exports.\n\n## Acceptance criteria\n\n- **FR-1:**\n  - AC-1.1 — Given x, when y, then z.\n- **FR-2:**\n  - AC-2.1 — Given x, when y, then z.\n\n## Open questions & unknowns\n\n- None.\n- Premortem: none.\n\n## Amendments\n\nNone.\n\n## References\n\nNone.\n\n## Implementation work\n\n| Work item | Implementation | Requirements | Acceptance criteria | Status |\n|---|---|---|---|---|\n| [ENG-1](https://tracker.example/ENG-1) | [PR #1](https://github.com/example/pull/1) | FR-1 | AC-1.1 | Done |\n| [ENG-2](https://tracker.example/ENG-2) | [PR #2](https://github.com/example/pull/2) | FR-2 | AC-2.1 | In progress |\n""",
            encoding="utf-8",
        )
        assert check_spec(spec) == []

        bad = spec.read_text(encoding="utf-8").replace("FR-2 | AC-2.1", "FR-9 | AC-9.1")
        spec.write_text(bad, encoding="utf-8")
        errors = check_spec(spec)
        assert any("missing FR-9" in e for e in errors)
        assert any("missing AC-9.1" in e for e in errors)

        restored = spec.read_text(encoding="utf-8").replace("FR-9 | AC-9.1", "FR-2 | AC-2.1")
        spec.write_text(restored, encoding="utf-8")
        assert check_spec(spec) == []

    print("functional-spec implementation-work self-test OK")
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    if "--project" not in argv:
        print("usage: validate_functional_specs.py --project PATH | --self-test")
        return 2
    i = argv.index("--project")
    if i + 1 >= len(argv):
        print("usage: validate_functional_specs.py --project PATH")
        return 2
    problems = validate_project(Path(argv[i + 1]).resolve())
    for problem in problems:
        print(f"FAIL  {problem}")
    print(f"\n{len(problems)} failure(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
