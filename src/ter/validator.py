"""Distributable adoption validator for tecfu-engineering-records.

Validates an adopting project's .engineering-records.yml, copied format
standards, and required docs areas. Adoption standards (agent-instructions,
changelogs, design-docs, backlogs) are followed in place and are not copied.

For full document-graph checks (numbering, headings, pairing, links), run the
suite's validate.py --project against the same path after installing the
format standards.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from importlib.resources import files

_MANIFEST = ".engineering-records.yml"

def find_project_root(start: Path | None = None) -> Path | None:
    """Walk parents from *start* looking for .engineering-records.yml.

    Returns the directory that contains the adoption manifest, or None if
    none is found before the filesystem root. Prefer this over cwd when
    invoked from a subdirectory (e.g. git hooks, nested shells).
    """
    cur = (start or Path.cwd()).resolve()
    if cur.is_file():
        cur = cur.parent
    for candidate in (cur, *cur.parents):
        if (candidate / _MANIFEST).is_file():
            return candidate
    return None
_VERSION_RE = re.compile(r"\*\*Version:\*\*\s+(\d+\.\d+)\s+\(")
_STANDARD_LINE = re.compile(r"^\s*-\s+([a-z0-9-]+)\s*$")

# Format standards that must be copied when declared.
_FORMAT_KINDS = {"format"}


def suite_metadata() -> dict:
    return json.loads(files("ter").joinpath("suite.json").read_text(encoding="utf-8"))


def format_standards(meta: dict | None = None) -> dict:
    meta = meta or suite_metadata()
    return {k: v for k, v in meta["standards"].items() if v.get("kind") == "format"}


def adoption_standards(meta: dict | None = None) -> dict:
    meta = meta or suite_metadata()
    return {k: v for k, v in meta["standards"].items() if v.get("kind") == "adoption"}


def _manifest(path: Path) -> dict:
    """Parse a minimal YAML subset used by .engineering-records.yml."""
    result: dict = {"spec": {}, "standards": []}
    section = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.strip() == "spec:":
            section = "spec"
            continue
        if line.strip() == "standards:":
            section = "standards"
            continue
        if section == "spec":
            m = re.match(
                r"^\s+(name|version|channel):\s*[\"']?([^\"']+?)[\"']?\s*$", line
            )
            if m:
                result["spec"][m.group(1)] = m.group(2).strip()
        elif section == "standards":
            m = _STANDARD_LINE.match(line)
            if m:
                result["standards"].append(m.group(1))
    return result


def _standard_version(path: Path) -> str | None:
    m = _VERSION_RE.search(path.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def _packaged_standard(relative: str) -> Path:
    """Resolve a standard file shipped inside the ter package."""
    return Path(str(files("ter").joinpath("standards").joinpath(relative)))


def validate(root: Path) -> list[str]:
    """Validate an adopting project. Partial adoption is allowed: only
    declared format standards are required to be present and current.

    If *root* has no `.engineering-records.yml`, walks parents via
    `find_project_root` so hooks and subdir invocations still work.
    """
    root = root.resolve()
    meta = suite_metadata()
    problems: list[str] = []
    manifest_path = root / _MANIFEST
    if not manifest_path.is_file():
        found = find_project_root(root)
        if found is None:
            return [f"missing {_MANIFEST}; run 'ter adopt' to create it"]
        root = found
        manifest_path = root / _MANIFEST

    manifest = _manifest(manifest_path)
    spec = manifest["spec"]
    if spec.get("name") != meta["name"]:
        problems.append(f"{_MANIFEST}: spec.name must be {meta['name']!r}")
    if not spec.get("version"):
        problems.append(f"{_MANIFEST}: missing spec.version")
    else:
        # Soft check: warn-style problem if behind minimum; hard fail if
        # newer than installed suite (unknown future).
        declared_ver = spec["version"]
        if declared_ver != meta["suite_version"]:
            problems.append(
                f"{_MANIFEST}: spec.version is {declared_ver!r}; "
                f"installed suite is {meta['suite_version']!r} "
                f"(run ter check-update; upgrade or re-adopt as needed)"
            )
    if spec.get("channel", "stable") not in {"stable", "preview"}:
        problems.append(f"{_MANIFEST}: spec.channel must be stable or preview")

    declared = set(manifest["standards"])
    known = set(meta["standards"])
    fmt = format_standards(meta)

    for name in sorted(declared - known):
        problems.append(f"{_MANIFEST}: unknown standard: {name}")

    if not declared:
        problems.append(
            f"{_MANIFEST}: standards list is empty — declare at least one "
            f"format standard ({', '.join(sorted(fmt))})"
        )

    # Only format standards that are declared must have copies + docs areas.
    for name in sorted(declared & set(fmt)):
        info = fmt[name]
        target = root / info["target"]
        if not target.is_file():
            problems.append(
                f"missing required copy: {info['target']} "
                f"(run 'ter install-standards' or copy from the suite)"
            )
            continue
        actual = _standard_version(target)
        if actual != info["version"]:
            problems.append(
                f"{info['target']}: version {actual!r}; expected {info['version']!r}"
            )
        area = info.get("docs_area")
        if area:
            p = root / area
            if not p.is_dir():
                problems.append(f"missing required docs area: {area}")
            elif not (p / "README.md").is_file():
                problems.append(f"missing required index: {area}/README.md")

    # Adoption standards may be declared for documentation; they must not
    # require a copied STANDARD file.
    for name in sorted(declared & set(adoption_standards(meta))):
        info = meta["standards"][name]
        # If someone incorrectly copied a STANDARD into a path we used to
        # require, do not fail — just skip.
        _ = info

    return problems


def adopt(root: Path, force: bool = False, standards: list[str] | None = None) -> list[str]:
    """Create .engineering-records.yml.

    By default declares all format standards (the usual full adoption).
    Pass standards=[...] for partial adoption.
    """
    meta = suite_metadata()
    path = root / _MANIFEST
    if path.exists() and not force:
        return [f"{_MANIFEST} already exists; use --force to replace it"]

    fmt_names = list(format_standards(meta))
    chosen = standards if standards is not None else fmt_names
    unknown = [s for s in chosen if s not in meta["standards"]]
    if unknown:
        return [f"unknown standard(s): {', '.join(unknown)}"]
    if not chosen:
        return ["must declare at least one standard"]

    lines = [
        "spec:",
        f"  name: {meta['name']}",
        f"  version: \"{meta['suite_version']}\"",
        "  channel: stable",
        "",
        "standards:",
    ]
    lines += [f"  - {name}" for name in chosen]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return []


def install_standards(root: Path, force: bool = False) -> list[str]:
    """Copy declared format standards (and skills) from the package into the project."""
    root = root.resolve()
    meta = suite_metadata()
    manifest_path = root / _MANIFEST
    if not manifest_path.is_file():
        return [f"missing {_MANIFEST}; run 'ter adopt' first"]

    manifest = _manifest(manifest_path)
    declared = set(manifest["standards"])
    problems: list[str] = []
    fmt = format_standards(meta)

    for name in sorted(declared & set(fmt)):
        info = fmt[name]
        source = _packaged_standard(info["source"])
        if not source.is_file():
            problems.append(f"package missing standard file: {info['source']}")
            continue
        target = root / info["target"]
        if target.exists() and not force:
            actual = _standard_version(target)
            if actual != info["version"]:
                problems.append(
                    f"{info['target']}: stale at {actual!r} "
                    f"(expected {info['version']!r}); re-run with --force after review"
                )
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        # skills (optional companion)
        skills_rel = info.get("skills_source")
        if skills_rel:
            skills_src = _packaged_standard(skills_rel)
            if skills_src.is_file():
                skills_dst = target.parent / skills_src.name
                if force or not skills_dst.exists():
                    shutil.copyfile(skills_src, skills_dst)
        area = info.get("docs_area")
        if area:
            idx = root / area / "README.md"
            if not idx.exists():
                idx.parent.mkdir(parents=True, exist_ok=True)
                idx.write_text(
                    f"# {area.split('/')[-1].title()}\n\n"
                    f"Index for {name}. Keep one row per numbered document.\n",
                    encoding="utf-8",
                )
    return problems


# Back-compat alias used by older call sites / tests
def update(root: Path, force: bool = False) -> list[str]:
    return install_standards(root, force=force)


def check_update() -> tuple[str, str]:
    meta = suite_metadata()
    return meta["suite_version"], meta["minimum_supported_suite"]


# ---------- git hooks ----------

_HOOK_MARKER = "ter-managed git hook (tecfu-engineering-records)"
_HOOK_SHIM = f"""#!/bin/sh
# {_HOOK_MARKER} — installed by `ter hooks install`.
# Remove with `ter hooks uninstall`, or delete this file.
# Bypass a single push with: git push --no-verify
root="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 1
cat >/dev/null 2>&1  # drain pre-push ref lines
if command -v ter >/dev/null 2>&1; then
  exec ter validate --quiet "$root"
fi
if [ -f "$root/scripts/ter/validate.py" ]; then
  exec python3 "$root/scripts/ter/validate.py" --project "$root"
fi
echo "ter: no validator found — pip install tecfu-engineering-records or vendor the suite at scripts/ter/ (bypass: git push --no-verify)" >&2
exit 1
"""


def _pre_push_hook(root: Path) -> Path:
    """Path of the pre-push hook in the default git hooks dir (no core.hooksPath)."""
    out = subprocess.run(
        ["git", "rev-parse", "--git-path", "hooks"],
        cwd=root, capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise RuntimeError(f"{root}: not a git repository")
    return (root / out.stdout.strip()).resolve() / "pre-push"


def install_hooks(root: Path, force: bool = False) -> list[str]:
    """Write the pre-push shim into the repo's default hooks dir.

    The shim prefers the installed `ter` package and falls back to a suite
    vendored at scripts/ter/validate.py, so both consumption modes gate
    without per-machine git config.
    """
    try:
        hook = _pre_push_hook(root.resolve())
    except RuntimeError as e:
        return [str(e)]
    if hook.exists() and _HOOK_MARKER not in hook.read_text(encoding="utf-8") and not force:
        return [f"{hook}: existing pre-push hook is not ter-managed; "
                "refusing to overwrite (use --force to replace it)"]
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text(_HOOK_SHIM, encoding="utf-8")
    hook.chmod(0o755)
    return []


def uninstall_hooks(root: Path) -> list[str]:
    """Remove the ter-managed pre-push shim; never touches foreign hooks."""
    try:
        hook = _pre_push_hook(root.resolve())
    except RuntimeError as e:
        return [str(e)]
    if not hook.exists():
        return [f"{hook}: no pre-push hook installed"]
    if _HOOK_MARKER not in hook.read_text(encoding="utf-8"):
        return [f"{hook}: not ter-managed; refusing to remove"]
    hook.unlink()
    return []
