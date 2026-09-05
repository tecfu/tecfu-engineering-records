#!/usr/bin/env python3
"""Run versioned engineering-records migrations.

Migrations are deliberately explicit and idempotent. A migration is a Python
module under migrations/ named `vX_Y_to_vA_B.py` exposing `migrate(root)`.

Usage:
  python3 tools/migrate.py --list
  python3 tools/migrate.py --from 1.4 --to 1.5 PROJECT
"""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "migrations"


def versions():
    out = []
    for p in MIGRATIONS.glob("v*_to_v*.py"):
        m = re.fullmatch(r"v(\d+)_(\d+)_to_v(\d+)_(\d+)\.py", p.name)
        if m:
            out.append(((int(m[1]), int(m[2])), (int(m[3]), int(m[4])), p))
    return sorted(out)


def key(v):
    return tuple(map(int, v.split(".")))


def main(argv):
    if "--list" in argv:
        for a, b, p in versions(): print(f"{a[0]}.{a[1]} -> {b[0]}.{b[1]}: {p.name}")
        return 0
    if len(argv) != 6 or argv[1] != "--from" or argv[3] != "--to":
        print("usage: migrate.py --from X.Y --to X.Y PROJECT", file=sys.stderr)
        return 2
    current, target, root = key(argv[2]), key(argv[4]), Path(argv[5]).resolve()
    if current >= target:
        print(f"nothing to migrate: {argv[2]} -> {argv[4]}")
        return 0
    edges = {(a, b): p for a, b, p in versions()}
    while current < target:
        candidates = [(b, p) for (a, b), p in edges.items() if a == current and b <= target]
        if not candidates:
            print(f"no migration path from {current[0]}.{current[1]} to {target[0]}.{target[1]}", file=sys.stderr)
            return 1
        nxt, path = min(candidates)
        spec = importlib.util.spec_from_file_location("migration", path)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        print(f"migrating {current[0]}.{current[1]} -> {nxt[0]}.{nxt[1]} ({path.name})")
        module.migrate(root)
        current = nxt
    print(f"migration complete: {current[0]}.{current[1]}")
    return 0

if __name__ == "__main__": sys.exit(main(sys.argv))
