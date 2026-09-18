import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_skill.py"


def run_validator(path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path)], text=True, capture_output=True
    )


class ValidateSkillCliTests(unittest.TestCase):
    def test_current_repository_is_valid(self):
        result = run_validator(ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "PASS")

    def test_missing_frontmatter_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SKILL.md").write_text("# no frontmatter\n")
            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("frontmatter", result.stderr.lower())

    def test_name_must_match_directory_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "expected-name"
            root.mkdir()
            (root / "SKILL.md").write_text(
                "---\nname: another-name\ndescription: useful skill\n---\n"
            )
            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("name does not match directory", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
