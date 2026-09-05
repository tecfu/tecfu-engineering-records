#!/usr/bin/env python3
"""Fixture-based integration tests for validate.py --project mode.

Each tests/fixtures/<name>/ is materialized into a temp project and the
real validator runs against it (subprocess, exit code and output).

Layout convention:
  _base/            fully compliant project; every fixture starts from it
  <name>/           overlay copied over _base (same-named files overwrite)
  <name>/FULL       marker: fixture is standalone, _base is NOT applied

Before validating, the harness "adopts" the project: copies the current
suite standards into every area dir present and generates docs/ADOPTION.md
with rows at the current suite versions — so fixtures never rot on
version bumps and each fixture isolates exactly one failure mode.
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
import validate  # noqa: E402  (AREAS is the single source of area layout)

FIXTURES = REPO / "tests" / "fixtures"

# fixture -> (expected exit code, substrings that must appear in output)
CASES = {
    "valid-project": (0, []),
    "missing-verification": (1, ["docs/verification", "adopt the standard first"]),
    "duplicate-number": (1, ["duplicate numbers: [1]"]),
    "bad-headings": (1, ["heading order mismatch"]),
    "broken-reference": (1, ["broken link 001-missing.md"]),
    "unadopted-standard": (
        1,
        [
            "docs/specs",
            "docs/decisions",
            "docs/verification",
            "docs/postmortems",
            "adopt the standard first",
        ],
    ),
    "stale-index": (1, ["no index row for 001-export-for-telemetry.md"]),
    "bad-matrix": (1, ["Closeness says 9 points but matrix totals differ by 7"]),
    "missing-closeness": (1, ["no Closeness line after the Decision matrix"]),
    "bad-acceptance": (1, ["duplicate AC id AC-1.1"]),
}


def materialize(name, dest):
    """Build the fixture project at dest: base + overlay + adoption."""
    src = FIXTURES / name
    if not (src / "FULL").exists():
        shutil.copytree(FIXTURES / "_base", dest)
    shutil.copytree(src, dest, dirs_exist_ok=True)
    (dest / "FULL").unlink(missing_ok=True)
    # adopt: copy the current standards into every area dir present
    for area, (sdir, sfile) in validate.AREAS.items():
        d = dest / area
        if d.is_dir():
            shutil.copy(REPO / sdir / sfile, d / sfile)
    # adoption manifest: one row per copied file, at current suite versions
    copies = sorted(str(p.relative_to(dest)) for p in dest.rglob("*-STANDARD.md"))
    if copies:
        suite_rows = {}
        for line in (REPO / "SUITE.md").read_text().splitlines():
            cells = [c.strip() for c in line.split("|")]
            if len(cells) >= 5 and cells[4].endswith("-STANDARD.md"):
                suite_rows[Path(cells[4]).name] = (cells[1], cells[3])
        lines = ["# Adoption", "", "| Standard | Version | File |", "|---|---|---|"]
        for c in copies:
            std_name, ver = suite_rows.get(Path(c).name, ("?", "?"))
            lines.append(f"| {std_name} | {ver} | {c} |")
        (dest / "docs" / "ADOPTION.md").write_text("\n".join(lines) + "\n")


class FixtureTests(unittest.TestCase):
    def test_fixtures(self):
        for name, (code, substrings) in CASES.items():
            with self.subTest(fixture=name):
                with tempfile.TemporaryDirectory() as td:
                    root = Path(td) / name
                    materialize(name, root)
                    r = subprocess.run(
                        [sys.executable, str(REPO / "validate.py"), "--project", str(root)],
                        capture_output=True,
                        text=True,
                    )
                out = r.stdout + r.stderr
                self.assertEqual(r.returncode, code, out)
                for s in substrings:
                    self.assertIn(s, out)
                if code == 0:
                    self.assertNotIn("FAIL", out)

    def test_all_fixtures_covered(self):
        names = {p.name for p in FIXTURES.iterdir() if p.is_dir()} - {"_base"}
        self.assertEqual(names, set(CASES))


if __name__ == "__main__":
    unittest.main()
