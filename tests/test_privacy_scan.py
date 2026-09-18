import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "privacy_scan.py"


def run_scan(path, *extra):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path), *extra],
        text=True,
        capture_output=True,
    )


class PrivacyScanCliTests(unittest.TestCase):
    def test_clean_tree_returns_zero_and_empty_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("fictional public example\n")
            result = run_scan(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["findings"], [])

    def test_detects_user_home_paths_on_three_platforms(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sensitive = "\n".join(
                [
                    "/" + "Users" + "/alex/private.txt",
                    "/" + "home" + "/alex/private.txt",
                    "C:" + "\\" + "Users" + "\\" + "alex" + "\\private.txt",
                ]
            )
            (root / "paths.txt").write_text(sensitive)
            result = run_scan(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(result.stdout, result.stderr)
            kinds = {item["kind"] for item in json.loads(result.stdout)["findings"]}
            self.assertIn("user_home_path", kinds)

    def test_detects_credentials_headers_private_keys_and_sessions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            parts = [
                "g" + "hp_" + "a" * 36,
                "Authorization" + ": Bearer " + "secret-value",
                "-----BEGIN " + "PRIVATE KEY-----",
                "session" + "_token=secret-value",
            ]
            (root / "secrets.txt").write_text("\n".join(parts))
            result = run_scan(root)
            self.assertTrue(result.stdout, result.stderr)
            kinds = {item["kind"] for item in json.loads(result.stdout)["findings"]}
            self.assertTrue(
                {"token", "authorization_header", "private_key", "session_secret"}
                <= kinds
            )

    def test_ignores_git_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            hidden = root / ".git"
            hidden.mkdir()
            (hidden / "config").write_text("g" + "hp_" + "a" * 36)
            result = run_scan(root)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_custom_forbid_marker_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "note.md").write_text("PRIVATE_PROJECT_ALIAS")
            result = run_scan(root, "--forbid", "PRIVATE_PROJECT_ALIAS")
            self.assertTrue(result.stdout, result.stderr)
            findings = json.loads(result.stdout)["findings"]
            self.assertEqual(findings[0]["kind"], "custom_marker")


if __name__ == "__main__":
    unittest.main()
