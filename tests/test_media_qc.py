import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "media_qc.py"


def load_module():
    if not SCRIPT.exists():
        raise AssertionError("media_qc.py is missing")
    spec = importlib.util.spec_from_file_location("media_qc", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MediaQcUnitTests(unittest.TestCase):
    def test_parse_frame_rate_handles_fraction_and_zero_denominator(self):
        module = load_module()
        self.assertAlmostEqual(module.parse_frame_rate("30000/1001"), 29.970, places=3)
        self.assertIsNone(module.parse_frame_rate("30/0"))
        self.assertIsNone(module.parse_frame_rate("not-a-rate"))

    def test_evaluate_streams_requires_video_and_audio(self):
        module = load_module()
        probe = {
            "streams": [
                {"codec_type": "video", "width": 1080, "height": 1920},
                {"codec_type": "audio", "sample_rate": "48000", "channels": 2},
            ]
        }
        result = module.evaluate_streams(probe)
        self.assertEqual(result["video_stream"]["status"], "PASS")
        self.assertEqual(result["audio_stream"]["status"], "PASS")

        missing_audio = module.evaluate_streams({"streams": probe["streams"][:1]})
        self.assertEqual(missing_audio["audio_stream"]["status"], "FAIL")

    def test_faststart_requires_moov_before_mdat(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            fast = Path(tmp) / "fast.mp4"
            slow = Path(tmp) / "slow.mp4"
            fast.write_bytes(b"header-moov-metadata-mdat-payload")
            slow.write_bytes(b"header-mdat-payload-moov-metadata")
            self.assertEqual(module.check_faststart(fast)["status"], "PASS")
            self.assertEqual(module.check_faststart(slow)["status"], "FAIL")

    def test_missing_external_tools_are_not_verified(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / "candidate.mp4"
            media.write_bytes(b"synthetic-media")
            with mock.patch.object(module.shutil, "which", return_value=None):
                report = module.inspect_media(media)
            self.assertEqual(report["container"]["status"], "NOT_VERIFIED")
            self.assertEqual(report["black_frames"]["status"], "NOT_VERIFIED")
            self.assertEqual(report["long_silence"]["status"], "NOT_VERIFIED")


if __name__ == "__main__":
    unittest.main()
