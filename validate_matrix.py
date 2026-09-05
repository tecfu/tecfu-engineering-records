#!/usr/bin/env python3
"""Validate the normalized weights required by DECISION-RECORDS-STANDARD.md.

Usage:
    python3 validate_matrix.py [PATH]

PATH defaults to the repository root. In project mode, pass the project root
and decision records are read from docs/decisions/. The validator checks that
each criterion shows both its 1-10 raw weight and normalized percentage, and
that the normalized percentages sum to 100% (within 0.1 percentage point for
rounding).
"""

import re
import sys
from pathlib import Path

ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|.*\|\s*[^|]+\s*\|\s*$")
WEIGHT_RE = re.compile(r"\((\d+)\s*/\s*(\d+(?:\.\d+)?)%\)")
TOTAL_RE = re.compile(r"^\|\s*\*\*Total\*\*\s*\|(.+)$", re.I)
TABLE_START = re.compile(r"^## Decision matrix\s*$")


def check_matrix(text, path="<text>"):
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if TABLE_START.match(line.strip()))
    except StopIteration:
        return []

    rows = []
    total = False
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        if not line.strip().startswith("|"):
            continue
        if set(line.strip(" |")) <= {"-", ":"}:
            continue
        if TOTAL_RE.match(line):
            total = True
            continue
        if "Criterion (weight)" in line:
            continue
        rows.append(line)

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
            problems.append(f"{path}: criterion '{criterion}' must show raw and normalized weight, e.g. '(4 / 40%)'")
            continue
        raw = int(match.group(1))
        normalized = float(match.group(2))
        if not 1 <= raw <= 10:
            problems.append(f"{path}: criterion '{criterion}' raw weight {raw} is not 1-10")
        if not 0 < normalized <= 100:
            problems.append(f"{path}: criterion '{criterion}' normalized weight {normalized:g}% is invalid")
        percentages.append(normalized)

    if percentages and abs(sum(percentages) - 100.0) > 0.1:
        problems.append(
            f"{path}: normalized weights sum to {sum(percentages):g}%, not 100%"
        )
    if rows and not total:
        problems.append(f"{path}: decision matrix must include a **Total** row")
    return problems


def main(argv):
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parent
    decision_dirs = [root / "decision-records"]
    project = root / "docs" / "decisions"
    if project.is_dir():
        decision_dirs.append(project)

    files = []
    for directory in decision_dirs:
        if directory.is_dir():
            files.extend(sorted(directory.glob("*.md")))
    # Include project fixtures in the suite so CI exercises the rule.
    fixtures = root / "tests" / "fixtures"
    if fixtures.is_dir():
        files.extend(sorted(fixtures.glob("**/docs/decisions/*.md")))

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
