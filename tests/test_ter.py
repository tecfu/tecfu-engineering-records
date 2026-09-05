import tempfile
import unittest
from pathlib import Path

from ter.cli import main as ter_main
from ter.validator import (
    adopt,
    find_project_root,
    format_standards,
    install_standards,
    suite_metadata,
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
