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
  truth), unfilled placeholders, index rows, and the adoption manifest
  (docs/ADOPTION.md) against the copied standard files and current suite
  versions (staleness).

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
# adopted copies of the standards, e.g. docs/specs/FUNCTIONAL-SPECS-STANDARD.md
COPIED_RE = re.compile(r"^[A-Z][A-Z0-9-]*-(?:STANDARD|SKILLS)\.md$")
# adoption manifest row: | Standard | Version | File |
ADOPTION_ROW_RE = re.compile(
    r"^\|\s*([^|]+?)\s*\|\s*(\d+\.\d+)\s*\|\s*([^|]+?)\s*\|", re.M
)


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


def suite_versions(suite):
    """Current suite versions, keyed by standard prefix (DECISION-RECORDS…)."""
    out = {}
    for d, prefix in DIRS.items():
        p = suite / d / f"{prefix}-STANDARD.md"
        if p.exists() and (m := VER_RE.search(p.read_text())):
            out[prefix] = m.group(1)
    return out


def check_adoption(rows, copies, current):
    """Adoption manifest rows vs copied standard files vs suite versions.

    rows: [(standard, version, path)]; copies: {path: version-or-None};
    current: {prefix: version} from the suite.
    """
    problems, declared = [], set()
    for _name, ver, path in rows:
        declared.add(path)
        if path not in copies:
            problems.append(f"row for missing copy: {path}")
            continue
        if copies[path] is None:
            problems.append(f"{path}: copy has no '**Version:**' header")
        elif copies[path] != ver:
            problems.append(
                f"{path} listed at {ver} but copy says {copies[path]}"
            )
        prefix = path.rsplit("/", 1)[-1].replace("-STANDARD.md", "")
        if prefix in current and current[prefix] != ver:
            problems.append(
                f"{path} at {ver} is stale — suite has {current[prefix]}; re-copy"
            )
    for path in copies:
        if path not in declared:
            problems.append(f"no row for adopted copy: {path}")
    return problems


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
        # adopted copies of the standards live here too; they are validated
        # via the adoption manifest below, not as numbered content documents
        docs = [n for n in names if not COPIED_RE.match(n)]
        problems += [f"{area}: {x}" for x in check_numbering(docs)]

        req = headings_from_template(suite / sdir / sfile)
        if req is None:
            problems.append(f"cannot parse template headings from {sdir}/{sfile}")
        for name in docs:
            text = (p / name).read_text()
            if req is not None:
                problems += [f"{area}/{name}: {x}" for x in check_headings_order(text, req)]
            problems += [f"{area}/{name}: {x}" for x in check_placeholders(text)]

        idx = p / "README.md"
        if not idx.exists():
            problems.append(f"missing index {idx}")
        else:
            idx_text = idx.read_text()
            for name in docs:
                if name not in idx_text:
                    problems.append(f"{idx}: no index row for {name}")

        nums = {int(m.group(1)) for n in docs if (m := NUM_RE.match(n))}
        if area == "docs/specs":
            spec_nums = nums
        if area == "docs/verification":
            report_nums = nums

    if spec_nums is not None and report_nums is not None:
        problems += check_pairing(spec_nums, report_nums)

    copies = {}
    for pth in sorted(root.rglob("*-STANDARD.md")):
        m = VER_RE.search(pth.read_text())
        copies[str(pth.relative_to(root))] = m.group(1) if m else None
    if copies:
        man = root / "docs" / "ADOPTION.md"
        if not man.exists():
            problems.append(
                "missing docs/ADOPTION.md (adoption manifest) — declare the "
                "adopted standards and their versions"
            )
        else:
            rows = [
                (a, v, pth)
                for a, v, pth in ADOPTION_ROW_RE.findall(man.read_text())
            ]
            problems += [
                f"ADOPTION.md: {x}"
                for x in check_adoption(rows, copies, suite_versions(suite))
            ]
    return problems


def _fenced_blocks(text):
    """All ```-fenced blocks as (info_string, content); tolerates nested fences."""
    blocks, lines, i, n = [], text.splitlines(), 0, len(text.splitlines())
    while i < n:
        m = re.match(r"^(`{3,})(.*)$", lines[i])
        if not m:
            i += 1
            continue
        fence, info = m.group(1), m.group(2).strip()
        j = i + 1
        while j < n and not re.match(rf"^`{{{len(fence)},}}\s*$", lines[j]):
            j += 1
        blocks.append((info, "\n".join(lines[i + 1 : j])))
        i = j + 1
    return blocks


def headings_from_template(standard_path):
    """Extract the '## ' heading order from the standard's template block.

    The template is the fenced markdown block whose H1 carries a `{...}`
    placeholder (e.g. `# {short noun-phrase title}`) — selected by shape,
    not position, so example blocks before or after it cannot hijack the
    required heading list. Returns None (caller fails loudly) if absent.
    """
    for info, block in reversed(_fenced_blocks(standard_path.read_text())):
        if info not in ("markdown", "md"):
            continue
        h1 = re.search(r"(?m)^# .*\{.*$", block)
        hs = [h.strip() for h in re.findall(r"(?m)^## (.+?)\s*$", block)]
        if h1 and hs:
            return hs
    return None


# ---------- self-test ----------

def self_test():
    import tempfile

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

    # adoption manifest: agree, mismatch, stale, missing row, ghost row
    sv = {"DECISION-RECORDS": "1.6"}
    copy = "docs/decisions/DECISION-RECORDS-STANDARD.md"
    ok = [("Decision records", "1.6", copy)]
    assert check_adoption(ok, {copy: "1.6"}, sv) == []
    assert any("stale" in p for p in check_adoption(
        [("Decision records", "1.5", copy)], {copy: "1.5"}, sv))
    assert any("copy says" in p for p in check_adoption(ok, {copy: "1.4"}, sv))
    assert any("no row" in p for p in check_adoption([], {copy: "1.6"}, sv))
    assert any("missing copy" in p for p in check_adoption(
        [("Decision records", "1.6", "docs/decisions/GHOST.md")], {copy: "1.6"}, sv))

    # template heading extraction: shape-selected, survives nested fences
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "S.md"
        p.write_text(
            "```markdown\n# Example\n## Wrong\n```\n"
            "body text\n"
            "```markdown\n# {title}\n## Right\n## Order\n```\n"
        )
        assert headings_from_template(p) == ["Right", "Order"]
        # nested fence inside the template must not truncate the heading list
        p.write_text("```markdown\n# {t}\n## A\n```markdown\n``\n## B\n```\n")
        assert headings_from_template(p) == ["A", "B"]
        p.write_text("no template here\n")
        assert headings_from_template(p) is None

    print("self-test OK (18 assertions)")
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
