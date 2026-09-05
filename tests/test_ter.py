import tempfile
import unittest
from pathlib import Path

from ter.validator import adopt, validate


class ValidatorTests(unittest.TestCase):
    def test_missing_manifest_fails(self):
        with tempfile.TemporaryDirectory() as td:
            problems = validate(Path(td))
            self.assertTrue(any("missing .engineering-records.yml" in p for p in problems))

    def test_manifest_requires_standard_files(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.assertEqual(adopt(root), [])
            problems = validate(root)
            self.assertTrue(any("missing required spec file" in p for p in problems))

    def test_manifest_is_created_with_all_standards(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.assertEqual(adopt(root), [])
            text = (root / ".engineering-records.yml").read_text()
            for name in ("functional-specs", "decision-records", "verification", "postmortems"):
                self.assertIn(f"  - {name}", text)


if __name__ == "__main__":
    unittest.main()
