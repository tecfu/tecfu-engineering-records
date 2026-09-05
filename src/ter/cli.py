from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .validator import (
    adopt,
    check_update,
    find_project_root,
    install_standards,
    validate,
)


def _resolve_root(path: str | Path) -> Path:
    """Resolve path; if no manifest here, walk parents for adoption root."""
    start = Path(path).resolve()
    if (start / ".engineering-records.yml").is_file():
        return start
    found = find_project_root(start)
    return found if found is not None else start


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="ter",
        description="TecFu Engineering Records — adoption validator and standard installer",
    )
    parser.add_argument("--version", action="version", version=f"ter {__version__}")
    sub = parser.add_subparsers(dest="command")

    p_validate = sub.add_parser(
        "validate",
        help="validate an adopting repository (.engineering-records.yml + format standards)",
    )
    p_validate.add_argument("path", nargs="?", default=".")
    p_validate.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="on success print nothing; failures still go to stderr (ideal for git hooks)",
    )

    p_adopt = sub.add_parser(
        "adopt",
        help="create .engineering-records.yml (format standards by default; partial via --standard)",
    )
    p_adopt.add_argument("path", nargs="?", default=".")
    p_adopt.add_argument("--force", action="store_true")
    p_adopt.add_argument(
        "--standard",
        action="append",
        dest="standards",
        metavar="NAME",
        help="declare only this standard (repeatable); default = all format standards",
    )

    p_install = sub.add_parser(
        "install-standards",
        help="copy declared format STANDARD (and SKILLS) files from the package into the project",
    )
    p_install.add_argument("path", nargs="?", default=".")
    p_install.add_argument(
        "--force",
        action="store_true",
        help="overwrite existing copies even when versions differ",
    )

    p_update = sub.add_parser(
        "check-update",
        help="show installed suite version and minimum supported floor",
    )
    p_update.add_argument("path", nargs="?", default=".", help=argparse.SUPPRESS)

    args = parser.parse_args(argv)
    raw_path = Path(getattr(args, "path", ".")).resolve()

    if args.command == "validate":
        root = _resolve_root(raw_path)
        problems = validate(root)
        if problems:
            for problem in problems:
                print(f"ERROR: {problem}", file=sys.stderr)
            return 1
        if not args.quiet:
            print(f"OK: {root} conforms to tecfu-engineering-records suite")
        return 0

    if args.command == "adopt":
        # adopt intentionally uses the given path (create manifest here)
        root = raw_path
        problems = adopt(root, force=args.force, standards=args.standards)
        if problems:
            for problem in problems:
                print(f"ERROR: {problem}", file=sys.stderr)
            return 1
        print(f"Created {root / '.engineering-records.yml'}")
        print("Next: ter install-standards . && ter validate .")
        return 0

    if args.command == "install-standards":
        root = _resolve_root(raw_path)
        problems = install_standards(root, force=args.force)
        if problems:
            for problem in problems:
                print(f"ERROR: {problem}", file=sys.stderr)
            return 1
        print(f"Installed format standards under {root / 'docs'}")
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
