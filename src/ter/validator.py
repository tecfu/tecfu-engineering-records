from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from importlib.resources import files

_MANIFEST = ".engineering-records.yml"
_VERSION_RE = re.compile(r"\*\*Version:\*\*\s+(\d+\.\d+)\s+\(")
_STANDARD_LINE = re.compile(r"^\s*-\s+([a-z0-9-]+)\s*$")


def suite_metadata() -> dict:
    return json.loads(files("ter").joinpath("suite.json").read_text())


def _manifest(path: Path) -> dict:
    result = {"spec": {}, "standards": []}
    section = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.strip() == "spec:":
            section = "spec"; continue
        if line.strip() == "standards:":
            section = "standards"; continue
        if section == "spec":
            m = re.match(r"^\s+(name|version|channel):\s*[\"']?([^\"']+?)[\"']?\s*$", line)
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


def validate(root: Path) -> list[str]:
    root = root.resolve()
    meta = suite_metadata()
    problems: list[str] = []
    manifest_path = root / _MANIFEST
    if not manifest_path.is_file():
        return [f"missing {_MANIFEST}; run 'ter adopt' to create it"]
    manifest = _manifest(manifest_path)
    spec = manifest["spec"]
    if spec.get("name") != meta["name"]:
        problems.append(f"{_MANIFEST}: spec.name must be {meta['name']!r}")
    if spec.get("version") != meta["suite_version"]:
        problems.append(f"{_MANIFEST}: spec.version is {spec.get('version')!r}; installed suite is {meta['suite_version']}")
    if spec.get("channel", "stable") not in {"stable", "preview"}:
        problems.append(f"{_MANIFEST}: spec.channel must be stable or preview")
    declared = set(manifest["standards"])
    known = set(meta["standards"])
    for name in sorted(declared - known):
        problems.append(f"{_MANIFEST}: unknown standard: {name}")
    for name in sorted(known - declared):
        problems.append(f"{_MANIFEST}: missing standard declaration: {name}")
    for name, info in meta["standards"].items():
        if name not in declared:
            continue
        p = root / info["target"]
        if not p.is_file():
            problems.append(f"missing required spec file: {info['target']}")
            continue
        actual = _standard_version(p)
        if actual != info["version"]:
            problems.append(f"{info['target']}: version {actual!r}; expected {info['version']}")
    for area in ("specs", "decisions", "verification", "postmortems"):
        p = root / "docs" / area
        if not p.is_dir():
            problems.append(f"missing required docs area: docs/{area}")
        elif not (p / "README.md").is_file():
            problems.append(f"missing required index: docs/{area}/README.md")
    return problems


def adopt(root: Path, force: bool = False) -> list[str]:
    meta = suite_metadata()
    path = root / _MANIFEST
    if path.exists() and not force:
        return [f"{_MANIFEST} already exists; use --force to replace it"]
    lines = ["spec:", f"  name: {meta['name']}", f"  version: \"{meta['suite_version']}\"", "  channel: stable", "", "standards:"]
    lines += [f"  - {name}" for name in meta["standards"]]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return []


def update(root: Path, force: bool = False) -> list[str]:
    meta = suite_metadata()
    problems: list[str] = []
    package_root = files("ter").joinpath("standards")
    for name, info in meta["standards"].items():
        source = Path(package_root.joinpath(info["source"]))
        target = root / info["target"]
        if target.exists() and not force:
            actual = _standard_version(target)
            if actual != info["version"]:
                problems.append(f"{info['target']}: stale copy; use --force only after reviewing changes")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    if not (root / _MANIFEST).exists():
        problems.extend(adopt(root))
    return problems


def check_update() -> tuple[str, str]:
    meta = suite_metadata()
    return meta["suite_version"], meta["minimum_supported_suite"]
