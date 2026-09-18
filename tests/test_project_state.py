import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "project_state.py"


def run_state(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *map(str, args)],
        text=True,
        capture_output=True,
    )


class ProjectStateCliTests(unittest.TestCase):
    def test_init_creates_brief_ready_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "demo"
            result = run_state("init", project)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((project / "PROJECT_STATE.json").read_text())
            self.assertEqual(data["current_state"], "BRIEF_READY")
            self.assertEqual(data["schema_version"], 1)

    def test_advance_records_relative_evidence_and_sha256(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "demo"
            self.assertEqual(run_state("init", project).returncode, 0)
            evidence = project / "EVIDENCE.md"
            evidence.write_text("synthetic evidence\n")

            result = run_state(
                "advance",
                project,
                "EVIDENCE_READY",
                "--evidence",
                evidence,
                "--note",
                "claim table complete",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((project / "PROJECT_STATE.json").read_text())
            event = data["history"][-1]
            self.assertEqual(event["evidence_path"], "EVIDENCE.md")
            self.assertEqual(
                event["evidence_sha256"],
                hashlib.sha256(b"synthetic evidence\n").hexdigest(),
            )

    def test_skipping_a_state_is_rejected_without_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "demo"
            init_result = run_state("init", project)
            self.assertEqual(init_result.returncode, 0, init_result.stderr)
            evidence = project / "draft.md"
            evidence.write_text("draft\n")
            before = (project / "PROJECT_STATE.json").read_text()

            result = run_state(
                "advance", project, "STORY_DRAFTED", "--evidence", evidence
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("next state", result.stderr.lower())
            self.assertEqual((project / "PROJECT_STATE.json").read_text(), before)

    def test_validate_rejects_corrupted_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "demo"
            project.mkdir()
            (project / "PROJECT_STATE.json").write_text("{broken")
            result = run_state("validate", project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid", result.stderr.lower())

    def test_validate_detects_changed_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "demo"
            init_result = run_state("init", project)
            self.assertEqual(init_result.returncode, 0, init_result.stderr)
            evidence = project / "EVIDENCE.md"
            evidence.write_text("version one\n")
            self.assertEqual(
                run_state(
                    "advance", project, "EVIDENCE_READY", "--evidence", evidence
                ).returncode,
                0,
            )
            evidence.write_text("version two\n")
            result = run_state("validate", project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("hash mismatch", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
