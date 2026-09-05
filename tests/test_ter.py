import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from ter.cli import main as ter_main
from ter.validator import (
    adopt,
    find_project_root,
    format_standards,
    install_hooks,
    install_standards,
    suite_metadata,
    uninstall_hooks,
    validate,
)


class ValidatorTests(unittest.TestCase):
    def test_suite_metadata_has_format_and_adoption(self):
        meta = suite_metadata()
        self.assertEqual(meta["suite_version"], "1.5")
        fmt = format_standards(meta)
        self.assertIn("functional-specs", fmt)
        self.assertIn("decision-records", fmt)
        self.assertEqual(fmt["functional-specs"]["kind"], "format")
        self.assertEqual(meta["standards"]["agent-instructions"]["kind"], "adoption")
        self.assertNotIn("target", meta["standards"]["agent-instructions"])

    def test_missing_manifest_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            problems = validate(Path(tmp))
            self.assertTrue(any("missing .engineering-records.yml" in p for p in problems))

    def test_manifest_is_created_with_format_standards_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(adopt(root), [])
            text = (root / ".engineering-records.yml").read_text(encoding="utf-8")
            self.assertIn("functional-specs", text)
            self.assertIn("decision-records", text)
            self.assertNotIn("agent-instructions", text)
            self.assertNotIn("changelogs", text)

    def test_partial_adoption(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(adopt(root, standards=["decision-records"]), [])
            problems = validate(root)
            self.assertTrue(
                any("docs/decisions/DECISION-RECORDS-STANDARD.md" in p for p in problems)
            )
            self.assertFalse(
                any("functional-specs" in p and "missing" in p for p in problems)
            )

    def test_install_standards_and_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(
                adopt(root, standards=["functional-specs", "decision-records"]), []
            )
            problems = install_standards(root)
            self.assertEqual(problems, [])
            self.assertTrue((root / "docs/specs/FUNCTIONAL-SPECS-STANDARD.md").is_file())
            self.assertTrue(
                (root / "docs/decisions/DECISION-RECORDS-STANDARD.md").is_file()
            )
            self.assertTrue((root / "docs/specs/README.md").is_file())
            problems = validate(root)
            self.assertEqual(problems, [], problems)

    def test_packaged_standards_exist(self):
        from ter.validator import _packaged_standard

        p = _packaged_standard("functional-specs/FUNCTIONAL-SPECS-STANDARD.md")
        self.assertTrue(p.is_file(), p)

    def test_find_project_root_walks_parents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(adopt(root, standards=["decision-records"]), [])
            nested = root / "src" / "pkg"
            nested.mkdir(parents=True)
            self.assertEqual(find_project_root(nested), root.resolve())
            self.assertIsNone(find_project_root(Path(tmpfile_empty := tempfile.mkdtemp())))

    def test_validate_from_subdirectory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(
                adopt(root, standards=["functional-specs", "decision-records"]), []
            )
            self.assertEqual(install_standards(root), [])
            nested = root / "a" / "b"
            nested.mkdir(parents=True)
            problems = validate(nested)
            self.assertEqual(problems, [], problems)

    def test_quiet_validate_prints_nothing_on_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(
                adopt(root, standards=["functional-specs", "decision-records"]), []
            )
            self.assertEqual(install_standards(root), [])
            # capture via running main
            import io
            from contextlib import redirect_stdout, redirect_stderr

            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = ter_main(["validate", "--quiet", str(root)])
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue(), "")
            self.assertEqual(err.getvalue(), "")


if __name__ == "__main__":
    unittest.main()


class HookTests(unittest.TestCase):
    def _repo(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name) / "proj"
        root.mkdir()
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        return root

    def test_install_uninstall_roundtrip(self):
        root = self._repo()
        self.assertEqual(install_hooks(root), [])
        hook = root / ".git" / "hooks" / "pre-push"
        text = hook.read_text()
        self.assertIn("ter-managed git hook", text)
        self.assertIn("ter validate", text)
        self.assertTrue(os.access(hook, os.X_OK))
        self.assertEqual(install_hooks(root), [])  # idempotent reinstall
        self.assertEqual(uninstall_hooks(root), [])
        self.assertFalse(hook.exists())

    def test_install_refuses_foreign_hook(self):
        root = self._repo()
        hook = root / ".git" / "hooks" / "pre-push"
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text("#!/bin/sh\necho custom\n")
        self.assertIn("refusing to overwrite", install_hooks(root)[0])
        self.assertIn("not ter-managed", uninstall_hooks(root)[0])
        self.assertEqual(hook.read_text(), "#!/bin/sh\necho custom\n")
        self.assertEqual(install_hooks(root, force=True), [])  # forced replace
        self.assertIn("ter-managed git hook", hook.read_text())

    def test_install_outside_git_repo(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertIn("not a git repository", install_hooks(Path(td))[0])

    def _no_ter_env(self):
        """PATH with only the tools the shim needs — an installed ter on PATH
        (as in the CI test environment) must not change these outcomes."""
        bin_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, bin_dir, ignore_errors=True)
        for tool in ("sh", "git", "cat", "python3"):
            src = shutil.which(tool)
            if src:
                os.symlink(src, bin_dir / tool)
        return {**os.environ, "PATH": str(bin_dir)}

    def test_shim_fails_closed_without_validator(self):
        root = self._repo()
        self.assertEqual(install_hooks(root), [])
        hook = root / ".git" / "hooks" / "pre-push"
        r = subprocess.run(["sh", str(hook)], input="", capture_output=True,
                           text=True, cwd=root, env=self._no_ter_env())
        self.assertEqual(r.returncode, 1)
        self.assertIn("no validator found", r.stderr)

    def test_shim_runs_vendored_validator(self):
        root = self._repo()
        self.assertEqual(install_hooks(root), [])
        hook = root / ".git" / "hooks" / "pre-push"
        stub = root / "scripts" / "ter" / "validate.py"
        stub.parent.mkdir(parents=True)
        stub.write_text("import sys\nsys.exit(0)\n")
        r = subprocess.run(["sh", str(hook)], input="", capture_output=True,
                           text=True, cwd=root, env=self._no_ter_env())
        self.assertEqual(r.returncode, 0, r.stderr)

