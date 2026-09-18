#!/usr/bin/env python3
"""Scan a public tree for common private paths and likely secrets."""

import argparse
import json
import re
from pathlib import Path


EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
MAX_TEXT_BYTES = 2 * 1024 * 1024


def patterns(custom_markers):
    slash = r"/"
    backslash = r"\\"
    entries = [
        (
            "user_home_path",
            re.compile(slash + r"(?:Users|home)" + slash + r"[^/\s]+" + slash),
        ),
        (
            "user_home_path",
            re.compile(r"[A-Za-z]:" + backslash + r"Users" + backslash + r"[^\\\s]+" + backslash, re.I),
        ),
        ("token", re.compile(r"g" + r"hp_[A-Za-z0-9]{30,}")),
        ("token", re.compile(r"github" + r"_pat_[A-Za-z0-9_]{20,}")),
        ("token", re.compile(r"s" + r"k-[A-Za-z0-9_-]{20,}")),
        (
            "authorization_header",
            re.compile(r"Authorization\s*:\s*(?:Bearer|Basic)\s+\S+", re.I),
        ),
        (
            "private_key",
            re.compile(r"-----BEGIN\s+(?:RSA\s+|EC\s+|OPENSSH\s+)?PRIVATE\s+KEY-----"),
        ),
        (
            "session_secret",
            re.compile(r"(?:cookie|session(?:_token)?|refresh_token)\s*[=:]\s*[^\s]+", re.I),
        ),
    ]
    entries.extend(
        ("custom_marker", re.compile(re.escape(marker)))
        for marker in custom_markers
        if marker
    )
    return entries


def iter_files(root):
    root = Path(root)
    if root.is_file():
        yield root
        return
    for path in root.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def read_text(path):
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if len(data) > MAX_TEXT_BYTES or b"\x00" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def scan(root, custom_markers):
    root = Path(root).resolve()
    findings = []
    checks = patterns(custom_markers)
    for path in iter_files(root):
        text = read_text(path)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for kind, regex in checks:
                if regex.search(line):
                    try:
                        relative = path.resolve().relative_to(root).as_posix()
                    except ValueError:
                        relative = path.name
                    findings.append(
                        {"file": relative, "line": line_number, "kind": kind}
                    )
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--forbid", action="append", default=[])
    parser.add_argument("--output")
    args = parser.parse_args()

    findings = scan(args.path, args.forbid)
    report = {
        "status": "PASS" if not findings else "FAIL",
        "scanned_root": Path(args.path).resolve().name,
        "findings": findings,
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
