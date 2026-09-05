#!/usr/bin/env python3
"""Validate normalized decision-matrix weights.

Usage:
    python3 validate_matrix.py [PATH]
    python3 validate_matrix.py --self-test

PATH defaults to the repository root. In project mode, pass the project root
and decision records are read from docs/decisions/. The validator checks that
each criterion shows both its 1-10 raw weight and normalized percentage, and
that normalized percentages sum to 100% (within 0.1 percentage point for
rounding).
"""

import re
import sys
from pathlib import Path

WEIGHT_RE = re.compile(r"\((\d+)\s*/\s*(\d+(?:\.\d+)?)%\)")
TOTAL_RE = re.compile(r"^\|\s*\*\*Total\*\*\s*\|(.+)$", re.I)
TABLE_START = re.compile(r"^## Decision matrix\s*$")
SEPARATOR_RE = re.compile(r"^\|(?:\s*:?-+:?\s*\|)+\s*$")


def check_matrix(text, path="<text>"):
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if TABLE_START.match(line.strip()))
    except StopIteration:
        return []

    rows = []
    total = False
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if not stripped.startswith("|") or SEPARATOR_RE.match(stripped):
            continue
        if TOTAL_RE.match(stripped):
            total = True
            continue
        if "Criterion (weight)" in stripped:
            continue
        rows.append(stripped)

    if not rows:
        return []

    problems = []
    percentages = []
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if not cells:
            continue
        criterion = cells[0]
        match = WEIGHT_RE.search(criterion)
        if not match:
            problems.append(
                f"{path}: criterion '{criterion}' must show raw and normalized "
                "weight, e.g. '(4 / 40%)'"
            )
            continue
        raw = int(match.group(1))
        normalized = float(match.group(2))
        if not 1 <= raw <= 10:
            problems.append(f"{path}: criterion '{criterion}' raw weight {raw} is not 1-10")
        if not 0 < normalized <= 100:
            problems.append(
                f"{path}: criterion '{criterion}' normalized weight {normalized:g}% is invalid"
            )
        percentages.append(normalized)

    if percentages and abs(sum(percentages) - 100.0) > 0.1:
        problems.append(
            f"{path}: normalized weights sum to {sum(percentages):g}%, not 100%"
        )
    if rows and not total:
        problems.append(f"{path}: decision matrix must include a **Total** row")
    return problems


def self_test():
    valid = """
## Decision matrix
| Criterion (weight) | A | B | Basis |
|---|---|---|---|
| cost (5 / 62.5%) | 4 | 2 | benchmark |
| simplicity (3 / 37.5%) | 3 | 4 | judgment |
| **Total** | **72.5%** | **60.0%** | — |
"""
    assert check_matrix(valid) == []

    bad = """
## Decision matrix
| Criterion (weight) | A | B | Basis |
|---|---|---|---|
| cost (5) | 4 | 2 | benchmark |
| simplicity (3) | 3 | 4 | judgment |
"""
    errors = check_matrix(bad)
    assert any("must show raw and normalized weight" in e for e in errors)
    assert any("must include a **Total** row" in e for e in errors)

    unbalanced = """
## Decision matrix
| Criterion (weight) | A | B | Basis |
|---|---|---|---|
| cost (5 / 50%) | 4 | 2 | benchmark |
| simplicity (3 / 30%) | 3 | 4 | judgment |
| **Total** | **72.5%** | **60.0%** | — |
"""
    errors = check_matrix(unbalanced)
    assert any("sum to 80%, not 100%" in e for e in errors)
    print("self-test OK (3 assertions)")


def main(argv):
    if len(argv) == 2 and argv[1] == "--self-test":
        self_test()
        return 0

    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parent
    decision_dirs = [root / "decision-records"]
    project = root / "docs" / "decisions"
    if project.is_dir():
        decision_dirs.append(project)

    files = []
    for directory in decision_dirs:
        if directory.is_dir():
            files.extend(sorted(directory.glob("*.md")))

    problems = []
    for path in sorted(set(files)):
        if path.name.endswith("-STANDARD.md") or path.name.endswith("-SKILLS.md"):
            continue
        problems.extend(check_matrix(path.read_text(), str(path.relative_to(root))))

    for problem in problems:
        print(f"FAIL  {problem}")
    print(f"\n{len(problems)} failure(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
