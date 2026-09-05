#!/usr/bin/env python3
"""tecfu-acr-standard — executable validator.

Suite mode (default):
    python3 validate.py
  checks this repo: naming convention, version/changelog/manifest agreement,
  cross-reference resolution, no legacy un-namespaced filenames.

Project mode:
    python3 validate.py --project PATH
  checks an adopting project's docs/ tree: filename regexes, numbering
  (monotonic, contiguous, unique), spec<->verification 1:1 pairing, exact
  heading order (read from the standards' own templates — single source of
  truth), unfilled placeholders, and index rows.

Self-test:
    python3 validate.py --self-test

Exit 0 = clean, 1 = failures found. Stdlib only.
"""

import re
import sys
from pathlib import Path

DIRS = {
    "decision-records": "DECISION-RECORDS",
    "functional-specs": "FUNCTIONAL-SPECS",
    "verification": "VERIFICATION",
    "postmortems": "POSTMORTEMS",
    "agent-instructions": "AGENT-INSTRUCTIONS",
    "changelogs": "CHANGELOGS",
    "design-docs": "DESIGN-DOCS",
    "backlogs": "BACKLOGS",
}

# project area -> (suite dir, standard file defining the template)
AREAS = {
    "docs/specs": ("functional-specs", "FUNCTIONAL-SPECS-STANDARD.md"),
    "docs/decisions": ("decision-records", "DECISION-RECORDS-STANDARD.md"),
    "docs/verification": ("verification", "VERIFICATION-STANDARD.md"),
    "docs/postmortems": ("postmortems", "POSTMORTEMS-STANDARD.md"),
}

NUM_RE = re.compile(r"^(\d{3})-[a-z0-9-]+\.md$")
VER_RE = re.compile(r"\*\*Version:\*\* (\d+\.\d+) \(\d{4}-\d{2}-\d{2}\)")
CHANGELOG_RE = re.compile(r"(?m)^- \*\*(\d+\.\d+) \(")
# namespaced cross-reference: [dir/]NAME-STANDARD.md or NAME-SKILLS.md
# (lookbehind blocks partial matches after a hyphen inside longer names)
REF_RE = re.compile(
    r"(?<![A-Z0-9-])(?:[a-z0-9-]+/)+[A-Z][A-Z0-9-]*-(?:STANDARD|SKILLS)\.md"
)
BARE_RE = re.compile(r"(?<![A-Z-])(?:STANDARD|SKILLS)\.md")


# ---------- reusable checks (exercised by --self-test) ----------

def check_numbering(names):
    """Filenames in one docs area: regex, unique numbers, contiguous from 001."""
    problems, nums = [], []
    for n in names:
        m = NUM_RE.match(n)
        if not m:
            problems.append(f"bad filename (want NNN-slug.md): {n}")
        else:
            nums.append(int(m.group(1)))
    dupes = sorted({x for x in nums if nums.count(x) > 1})
    if dupes:
        problems.append(f"duplicate numbers: {dupes}")
    for i, x in enumerate(sorted(set(nums)), 1):
        if x != i:
            problems.append(f"numbering not contiguous from 001: {x} at position {i}")
            break
    return problems


def check_headings_order(text, required):
    """Top-level '## ' headings must equal the required list, in order."""
    found = [h.strip() for h in re.findall(r"(?m)^## (.+?)\s*$", text)]
    if found != required:
        return [f"heading order mismatch: expected {required}, found {found}"]
    return []


def check_placeholders(text):
    """'{...}' placeholders outside code fences must be filled in."""
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    return [
        f"unfilled placeholder: {ln.strip()[:60]}"
        for ln in body.splitlines()
        if re.search(r"\{[^{}]+\}", ln)
    ]


def check_pairing(spec_nums, report_nums):
    """Verification reports are 1:1 with specs, keyed by the spec's number."""
    if spec_nums != report_nums:
        return [
            f"spec/verification pairing mismatch: specs {sorted(spec_nums)} "
            f"vs reports {sorted(report_nums)}"
        ]
    return []


# ---------- suite mode ----------

def check_suite(root):
    problems = []

    versions = {}
    for d, prefix in DIRS.items():
        std = root / d / f"{prefix}-STANDARD.md"
        skl = root / d / f"{prefix}-SKILLS.md"
        if not std.exists():
            problems.append(f"missing {std}")
            continue
        if not skl.exists():
            problems.append(f"missing {skl}")
        text = std.read_text()
        m = VER_RE.search(text)
        if not m:
            problems.append(f"{std}: no '**Version:** X.Y (date)' header")
            continue
        versions[d] = m.group(1)
        cm = CHANGELOG_RE.search(text)
        if not cm:
            problems.append(f"{std}: no changelog entries")
        elif cm.group(1) != m.group(1):
            problems.append(
                f"{std}: Version header {m.group(1)} != newest changelog entry {cm.group(1)}"
            )

    suite_md = root / "SUITE.md"
    if not suite_md.exists():
        problems.append("missing SUITE.md (version manifest)")
    else:
        stext = suite_md.read_text()
        if not re.search(r"\*\*Suite version:\*\* \d+\.\d+ \(\d{4}-\d{2}-\d{2}\)", stext):
            problems.append("SUITE.md: no '**Suite version:** X.Y (date)' line")
        for ver, path in re.findall(
            r"^\|\s*[^|]+\|[^|]+\|\s*(\d+\.\d+)\s*\|\s*([^|]+?)\s*\|", stext, re.M
        ):
            d = Path(path.strip()).parts[0] if "/" in path else None
            if d not in versions:
                problems.append(f"SUITE.md: row for unknown standard path: {path}")
            elif versions[d] != ver:
                problems.append(
                    f"SUITE.md: {d} listed at {ver} but file says {versions[d]}"
                )
        for d, ver in versions.items():
            if f"/{DIRS[d]}-STANDARD.md" not in stext:
                problems.append(f"SUITE.md: no row for {d}")

    for md in sorted(root.rglob("*.md")):
        if ".git" in md.parts:
            continue
        text = md.read_text()
        for ref in sorted(set(REF_RE.findall(text))):
            # refs into an adopting project's docs/ tree (docs/decisions/...)
            # only resolve in project mode
            if ref.startswith("docs/"):
                continue
            # references may be file-relative (../dir/...) or repo-root-relative
            # (dir/...); accept whichever resolves
            target = next(
                (c.resolve() for c in (md.parent / ref, root / ref) if c.exists()),
                None,
            )
            if target is None:
                problems.append(f"{md.relative_to(root)}: broken reference {ref}")
        for _ in BARE_RE.findall(text):
            problems.append(
                f"{md.relative_to(root)}: un-namespaced STANDARD.md/SKILLS.md reference"
            )
    return problems


# ---------- project mode ----------

def check_project(root):
    problems = []
    suite = Path(__file__).resolve().parent
    spec_nums = report_nums = None

    for area, (sdir, sfile) in AREAS.items():
        p = root / area
        if not p.is_dir():
            problems.append(f"missing {p} (adopt the standard first)")
            continue
        names = sorted(x.name for x in p.glob("*.md") if x.name != "README.md")
        problems += [f"{area}: {x}" for x in check_numbering(names)]

        req = headings_from_template(suite / sdir / sfile)
        if req is None:
            problems.append(f"cannot parse template headings from {sdir}/{sfile}")
        for name in names:
            text = (p / name).read_text()
            if req is not None:
                problems += [f"{area}/{name}: {x}" for x in check_headings_order(text, req)]
            problems += [f"{area}/{name}: {x}" for x in check_placeholders(text)]

        idx = p / "README.md"
        if not idx.exists():
            problems.append(f"missing index {idx}")
        else:
            idx_text = idx.read_text()
            for name in names:
                if name not in idx_text:
                    problems.append(f"{idx}: no index row for {name}")

        nums = {int(m.group(1)) for n in names if (m := NUM_RE.match(n))}
        if area == "docs/specs":
            spec_nums = nums
        if area == "docs/verification":
            report_nums = nums

    if spec_nums is not None and report_nums is not None:
        problems += check_pairing(spec_nums, report_nums)
    return problems


def headings_from_template(standard_path):
    """Extract the '## ' heading order from the standard's template block."""
    blocks = re.findall(r"```markdown\n(.*?)```", standard_path.read_text(), re.S)
    for block in reversed(blocks):
        hs = [h.strip() for h in re.findall(r"(?m)^## (.+?)\s*$", block)]
        if hs:
            return hs
    return None


# ---------- self-test ----------

def self_test():
    assert check_numbering(["001-a.md", "002-b.md"]) == []
    assert any("contiguous" in p for p in check_numbering(["001-a.md", "003-c.md"]))
    assert any("duplicate" in p for p in check_numbering(["001-a.md", "001-b.md"]))
    assert any("bad filename" in p for p in check_numbering(["1-a.md"]))
    assert check_headings_order("## A\n## B\n", ["A", "B"]) == []
    assert check_headings_order("## B\n## A\n", ["A", "B"])
    assert check_placeholders("text {todo} more") != []
    assert check_placeholders("```\n{todo}\n```\nclean") == []
    assert check_pairing({1, 2}, {1, 2}) == []
    assert check_pairing({1, 2}, {1})
    print("self-test OK (10 assertions)")
    return 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    root = Path(__file__).resolve().parent
    problems = check_suite(root)
    if "--project" in argv:
        i = argv.index("--project")
        if i + 1 >= len(argv):
            print("usage: validate.py --project PATH")
            return 2
        problems += check_project(Path(argv[i + 1]).resolve())
    for e in problems:
        print(f"FAIL  {e}")
    print(f"\n{len(problems)} failure(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
