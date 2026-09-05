from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .validator import adopt, check_update, validate


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="ter", description="TecFu Engineering Records validator")
    parser.add_argument("--version", action="version", version=f"ter {__version__}")
    sub = parser.add_subparsers(dest="command")

    p_validate = sub.add_parser("validate", help="validate an adopting repository")
    p_validate.add_argument("path", nargs="?", default=".")

    p_adopt = sub.add_parser("adopt", help="create the adoption manifest")
    p_adopt.add_argument("path", nargs="?", default=".")
    p_adopt.add_argument("--force", action="store_true")

    p_update = sub.add_parser("check-update", help="show the installed suite compatibility floor")
    p_update.add_argument("path", nargs="?", default=".", help=argparse.SUPPRESS)

    args = parser.parse_args(argv)
    root = Path(getattr(args, "path", "."))

    if args.command == "validate":
        problems = validate(root)
        if problems:
            for problem in problems:
                print(f"ERROR: {problem}", file=sys.stderr)
            return 1
        print(f"OK: {root.resolve()} conforms to tecfu-engineering-records suite")
        return 0

    if args.command == "adopt":
        problems = adopt(root, args.force)
        if problems:
            for problem in problems:
                print(f"ERROR: {problem}", file=sys.stderr)
            return 1
        print(f"Created {root / '.engineering-records.yml'}")
        return 0

    if args.command == "check-update":
        latest, minimum = check_update()
        print(f"suite={latest}")
        print(f"minimum-supported={minimum}")
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
