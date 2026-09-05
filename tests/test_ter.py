import tempfile
import unittest
from pathlib import Path

from ter.validator import (
    adopt,
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
            # adoption standards are not auto-declared
            self.assertNotIn("agent-instructions", text)
            self.assertNotIn("changelogs", text)

    def test_partial_adoption(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(adopt(root, standards=["decision-records"]), [])
            problems = validate(root)
            # missing copy of the one declared format standard
            self.assertTrue(any("docs/decisions/DECISION-RECORDS-STANDARD.md" in p for p in problems))
            # should not demand functional-specs
            self.assertFalse(any("functional-specs" in p and "missing" in p for p in problems))

    def test_install_standards_and_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(adopt(root, standards=["functional-specs", "decision-records"]), [])
            problems = install_standards(root)
            self.assertEqual(problems, [])
            self.assertTrue((root / "docs/specs/FUNCTIONAL-SPECS-STANDARD.md").is_file())
            self.assertTrue((root / "docs/decisions/DECISION-RECORDS-STANDARD.md").is_file())
            self.assertTrue((root / "docs/specs/README.md").is_file())
            problems = validate(root)
            self.assertEqual(problems, [], problems)

    def test_packaged_standards_exist(self):
        from ter.validator import _packaged_standard

        p = _packaged_standard("functional-specs/FUNCTIONAL-SPECS-STANDARD.md")
        self.assertTrue(p.is_file(), p)


if __name__ == "__main__":
    unittest.main()
