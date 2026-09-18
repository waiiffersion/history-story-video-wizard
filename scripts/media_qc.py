#!/usr/bin/env python3
"""Run conservative, optional media checks and emit a JSON report."""

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def result(status, detail):
    return {"status": status, "detail": detail}


def parse_frame_rate(value):
    try:
        if "/" in value:
            numerator, denominator = value.split("/", 1)
            denominator = float(denominator)
            if denominator == 0:
                return None
            return float(numerator) / denominator
        return float(value)
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def evaluate_streams(probe):
    streams = probe.get("streams", [])
    video = next((item for item in streams if item.get("codec_type") == "video"), None)
    audio = next((item for item in streams if item.get("codec_type") == "audio"), None)
    video_result = (
        result(
            "PASS",
            {
                "codec": video.get("codec_name"),
                "width": video.get("width"),
                "height": video.get("height"),
                "frame_rate": parse_frame_rate(video.get("avg_frame_rate", "")),
                "pixel_format": video.get("pix_fmt"),
            },
        )
        if video
        else result("FAIL", "video stream missing")
    )
    audio_result = (
        result(
            "PASS",
            {
                "codec": audio.get("codec_name"),
                "sample_rate": audio.get("sample_rate"),
                "channels": audio.get("channels"),
            },
        )
        if audio
        else result("FAIL", "audio stream missing")
    )
    return {"video_stream": video_result, "audio_stream": audio_result}


def check_faststart(path):
    path = Path(path)
    if path.suffix.lower() not in {".mp4", ".mov", ".m4v"}:
        return result("NOT_VERIFIED", "atom ordering applies to MP4-family containers")
    try:
        data = path.read_bytes()
    except OSError as error:
        return result("FAIL", str(error))
    moov = data.find(b"moov")
    mdat = data.find(b"mdat")
    if moov < 0 or mdat < 0:
        return result("NOT_VERIFIED", "moov or mdat atom not found")
    return result("PASS" if moov < mdat else "FAIL", "moov={} mdat={}".format(moov, mdat))


def run_json(command):
    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "command failed")
    return json.loads(completed.stdout)


def detect_with_ffmpeg(ffmpeg, path, filter_name, marker):
    command = [ffmpeg, "-hide_banner", "-i", str(path), "-vf" if filter_name == "blackdetect" else "-af", filter_name, "-f", "null", "-"]
    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.returncode != 0:
        return result("NOT_VERIFIED", completed.stderr.strip()[-500:])
    matches = [line.strip() for line in completed.stderr.splitlines() if marker in line]
    return result("PASS" if not matches else "FAIL", matches or "no spans detected")


def inspect_media(path):
    path = Path(path)
    report = {"file": path.name}
    ffprobe = shutil.which("ffprobe")
    ffmpeg = shutil.which("ffmpeg")

    if not path.is_file():
        missing = result("FAIL", "file does not exist")
        report.update(
            {
                "container": missing,
                "video_stream": missing,
                "audio_stream": missing,
                "duration_alignment": missing,
                "faststart": missing,
                "black_frames": missing,
                "long_silence": missing,
            }
        )
        report["overall"] = "FAIL"
        return report

    if not ffprobe:
        unavailable = result("NOT_VERIFIED", "ffprobe is unavailable")
        report.update(
            {
                "container": unavailable,
                "video_stream": unavailable,
                "audio_stream": unavailable,
                "duration_alignment": unavailable,
                "faststart": check_faststart(path),
            }
        )
    else:
        try:
            probe = run_json(
                [
                    ffprobe,
                    "-v",
                    "error",
                    "-show_format",
                    "-show_streams",
                    "-of",
                    "json",
                    str(path),
                ]
            )
            duration = float(probe.get("format", {}).get("duration", 0) or 0)
            report["container"] = result(
                "PASS" if duration > 0 else "FAIL",
                {"format": probe.get("format", {}).get("format_name"), "duration": duration},
            )
            report.update(evaluate_streams(probe))
            stream_durations = []
            for stream in probe.get("streams", []):
                try:
                    stream_durations.append(float(stream["duration"]))
                except (KeyError, TypeError, ValueError):
                    pass
            if len(stream_durations) >= 2:
                delta = max(stream_durations) - min(stream_durations)
                report["duration_alignment"] = result(
                    "PASS" if delta <= 0.25 else "FAIL", {"delta_seconds": delta}
                )
            else:
                report["duration_alignment"] = result(
                    "NOT_VERIFIED", "stream durations unavailable"
                )
            report["faststart"] = check_faststart(path)
        except (RuntimeError, ValueError, json.JSONDecodeError) as error:
            failed = result("FAIL", str(error))
            report.update(
                {
                    "container": failed,
                    "video_stream": failed,
                    "audio_stream": failed,
                    "duration_alignment": failed,
                    "faststart": check_faststart(path),
                }
            )

    if ffmpeg:
        report["black_frames"] = detect_with_ffmpeg(
            ffmpeg, path, "blackdetect=d=0.5:pix_th=0.10", "black_start:"
        )
        report["long_silence"] = detect_with_ffmpeg(
            ffmpeg, path, "silencedetect=n=-50dB:d=2", "silence_start:"
        )
    else:
        report["black_frames"] = result("NOT_VERIFIED", "ffmpeg is unavailable")
        report["long_silence"] = result("NOT_VERIFIED", "ffmpeg is unavailable")

    statuses = [value.get("status") for value in report.values() if isinstance(value, dict)]
    report["overall"] = (
        "FAIL" if "FAIL" in statuses else "NOT_VERIFIED" if "NOT_VERIFIED" in statuses else "PASS"
    )
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media")
    parser.add_argument("--json", dest="output")
    args = parser.parse_args()
    report = inspect_media(args.media)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 1 if report["overall"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
