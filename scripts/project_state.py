#!/usr/bin/env python3
"""Manage a strictly ordered, evidence-bound production state file."""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


STATES = [
    "BRIEF_READY",
    "EVIDENCE_READY",
    "STORY_DRAFTED",
    "TEXT_AUDIT_PASS",
    "TEXT_APPROVED",
    "NARRATION_LOCKED",
    "SUBTITLE_TIMING_LOCKED",
    "STORYBOARD_LOCKED",
    "VISUAL_PILOT_PASS",
    "ASSET_READY",
    "RENDERED_CANDIDATE",
    "MEDIA_QA_PASS",
    "FINAL_APPROVED",
    "RELEASE_PACKAGE_READY",
]
STATE_FILE = "PROJECT_STATE.json"


class StateError(ValueError):
    pass


def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def state_path(project):
    return Path(project).resolve() / STATE_FILE


def write_state(path, data):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def load_state(project):
    path = state_path(project)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise StateError("invalid state file: {}".format(error)) from error
    validate_structure(data)
    return path, data


def validate_structure(data):
    if data.get("schema_version") != 1:
        raise StateError("invalid schema version")
    current = data.get("current_state")
    history = data.get("history")
    if current not in STATES or not isinstance(history, list) or not history:
        raise StateError("invalid state structure")
    recorded = [item.get("state") for item in history]
    expected = STATES[: STATES.index(current) + 1]
    if recorded != expected:
        raise StateError("invalid state history sequence")


def cmd_init(args):
    project = Path(args.project).resolve()
    project.mkdir(parents=True, exist_ok=True)
    path = project / STATE_FILE
    if path.exists():
        raise StateError("state file already exists")
    data = {
        "schema_version": 1,
        "current_state": STATES[0],
        "history": [
            {
                "state": STATES[0],
                "at": now_utc(),
                "evidence_path": None,
                "evidence_sha256": None,
                "note": "project initialized",
            }
        ],
    }
    write_state(path, data)
    print(json.dumps(data, ensure_ascii=False))


def relative_evidence(project, evidence):
    project = Path(project).resolve()
    evidence = Path(evidence).resolve()
    if not evidence.is_file():
        raise StateError("evidence file does not exist")
    try:
        relative = evidence.relative_to(project)
    except ValueError as error:
        raise StateError("evidence must be inside the project directory") from error
    return relative.as_posix(), sha256_file(evidence)


def cmd_advance(args):
    path, data = load_state(args.project)
    current_index = STATES.index(data["current_state"])
    if current_index + 1 >= len(STATES):
        raise StateError("project is already at the final state")
    expected = STATES[current_index + 1]
    if args.state != expected:
        raise StateError("next state must be {}".format(expected))
    evidence_path, evidence_hash = relative_evidence(args.project, args.evidence)
    data["current_state"] = args.state
    data["history"].append(
        {
            "state": args.state,
            "at": now_utc(),
            "evidence_path": evidence_path,
            "evidence_sha256": evidence_hash,
            "note": args.note or "",
        }
    )
    write_state(path, data)
    print(json.dumps(data["history"][-1], ensure_ascii=False))


def validate_evidence(project, data):
    project = Path(project).resolve()
    errors = []
    for event in data["history"][1:]:
        relative = event.get("evidence_path")
        expected_hash = event.get("evidence_sha256")
        if not relative or not expected_hash:
            errors.append("missing evidence metadata for {}".format(event.get("state")))
            continue
        candidate = (project / relative).resolve()
        try:
            candidate.relative_to(project)
        except ValueError:
            errors.append("evidence path escapes project: {}".format(relative))
            continue
        if not candidate.is_file():
            errors.append("evidence file missing: {}".format(relative))
        elif sha256_file(candidate) != expected_hash:
            errors.append("evidence hash mismatch: {}".format(relative))
    return errors


def cmd_status(args):
    _, data = load_state(args.project)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_validate(args):
    _, data = load_state(args.project)
    errors = validate_evidence(args.project, data)
    if errors:
        raise StateError("; ".join(errors))
    print(json.dumps({"status": "PASS", "current_state": data["current_state"]}))


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("project")
    init_parser.set_defaults(func=cmd_init)

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("project")
    status_parser.set_defaults(func=cmd_status)

    advance_parser = subparsers.add_parser("advance")
    advance_parser.add_argument("project")
    advance_parser.add_argument("state", choices=STATES)
    advance_parser.add_argument("--evidence", required=True)
    advance_parser.add_argument("--note")
    advance_parser.set_defaults(func=cmd_advance)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("project")
    validate_parser.set_defaults(func=cmd_validate)
    return parser


def main():
    args = build_parser().parse_args()
    try:
        args.func(args)
    except StateError as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
