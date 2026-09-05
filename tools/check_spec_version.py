#!/usr/bin/env python3
"""Check an adopter's declared engineering-records version against upstream.

Usage: python3 tools/check_spec_version.py [manifest] [version-file]

The manifest defaults to .engineering-records.yml. The canonical version file
can be a local checkout or a raw URL. This intentionally uses only stdlib.
"""
import re
import sys
from pathlib import Path
from urllib.request import urlopen

LOCAL = Path(__file__).resolve().parents[1] / "spec" / "version.yml"
DEFAULT_MANIFEST = Path(".engineering-records.yml")
REMOTE = "https://raw.githubusercontent.com/tecfu/tecfu-engineering-records/main/spec/version.yml"


def parse(text):
    def value(key):
        m = re.search(rf"(?m)^\s*{re.escape(key)}:\s*[\"']?([^\"'\n]+?)[\"']?\s*$", text)
        return m.group(1).strip() if m else None
    return {k: value(k) for k in ("name", "version", "channel", "minimum_supported_version")}


def read_source(source):
    if source.startswith(("http://", "https://")):
        with urlopen(source, timeout=10) as response:
            return response.read().decode()
    return Path(source).read_text()


def main(argv):
    manifest = Path(argv[1]) if len(argv) > 1 else DEFAULT_MANIFEST
    source = argv[2] if len(argv) > 2 else (str(LOCAL) if LOCAL.exists() else REMOTE)
    if not manifest.exists():
        print(f"FAIL: missing {manifest}; declare the adopted spec version")
        return 1
    declared = parse(manifest.read_text())
    canonical = parse(read_source(source))
    problems = []
    if declared["name"] != "tecfu-engineering-records":
        problems.append("spec.name must be tecfu-engineering-records")
    if declared["version"] is None:
        problems.append("spec.version is missing")
    elif canonical["version"] and declared["version"] != canonical["version"]:
        problems.append(f"spec version {declared['version']} is stale — latest {canonical['version']}")
    if declared["channel"] != canonical["channel"]:
        problems.append(f"spec channel {declared['channel']!r} does not match canonical {canonical['channel']!r}")
    if problems:
        for p in problems: print(f"FAIL: {p}")
        return 1
    print(f"OK: tecfu-engineering-records {declared['version']} ({declared['channel']})")
    return 0

if __name__ == "__main__": sys.exit(main(sys.argv))
