#!/usr/bin/env python3
"""Open update PRs for registered adopters.

Requires `gh` and GH_TOKEN with permission to push branches/open PRs in each
registered repository. Registry entries are objects with `repository` and
optional `branch` (default: main).
"""
import json, os, re, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "adopters.json"
VERSION = re.search(r'^version:\s*["\']?([0-9]+\.[0-9]+)', (ROOT / "spec/version.yml").read_text(), re.M).group(1)


def run(*args, cwd=None):
    return subprocess.run(args, cwd=cwd, text=True, check=True, capture_output=True).stdout.strip()


def main():
    if not os.environ.get("GH_TOKEN"):
        raise SystemExit("GH_TOKEN is required")
    for entry in json.loads(REGISTRY.read_text())["repositories"]:
        repo = entry["repository"]
        branch = entry.get("branch", "main")
        with tempfile.TemporaryDirectory() as td:
            run("gh", "repo", "clone", repo, td)
            path = Path(td) / ".engineering-records.yml"
            if not path.exists():
                print(f"SKIP {repo}: no .engineering-records.yml")
                continue
            text = path.read_text()
            updated = re.sub(r'(?m)^(\s*version:\s*)["\']?[0-9]+\.[0-9]+["\']?\s*$', rf'\g<1>"{VERSION}"', text, count=1)
            if updated == text:
                print(f"SKIP {repo}: already at {VERSION}")
                continue
            path.write_text(updated)
            name = f"chore/update-engineering-records-{VERSION.replace('.', '-') }"
            run("git", "checkout", "-b", name, cwd=td)
            run("git", "add", ".engineering-records.yml", cwd=td)
            run("git", "commit", "-m", f"chore: update engineering-records to {VERSION}", cwd=td)
            run("git", "push", "-u", "origin", name, cwd=td)
            out = run("gh", "pr", "create", "--base", branch, "--head", name,
                      "--title", f"chore: update engineering-records to {VERSION}",
                      "--body", f"Automated adoption update to canonical tecfu-engineering-records {VERSION}. CI will verify the copied standards and migration requirements.", cwd=td)
            print(f"{repo}: {out}")

if __name__ == "__main__": main()
