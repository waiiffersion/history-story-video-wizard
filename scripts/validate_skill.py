#!/usr/bin/env python3
"""Validate the portable structure of a Codex Skill without dependencies."""

import argparse
import json
import re
import sys
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text):
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError("frontmatter is missing")
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as error:
        raise ValueError("frontmatter closing marker is missing") from error
    values = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError("frontmatter line is invalid: {}".format(line))
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def validate(root):
    root = Path(root).resolve()
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        raise ValueError("SKILL.md is missing")
    metadata = parse_frontmatter(skill_path.read_text(encoding="utf-8"))
    allowed = {"name", "description"}
    extras = sorted(set(metadata) - allowed)
    if extras:
        raise ValueError("unsupported frontmatter keys: {}".format(", ".join(extras)))
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if not NAME_PATTERN.fullmatch(name):
        raise ValueError("skill name must use lowercase kebab-case")
    if name != root.name:
        raise ValueError("skill name does not match directory name")
    if not description or len(description) > 1024:
        raise ValueError("description must contain 1 to 1024 characters")
    agent = root / "agents" / "openai.yaml"
    if not agent.is_file():
        raise ValueError("agents/openai.yaml is missing")
    return {"status": "PASS", "name": name}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".")
    args = parser.parse_args()
    try:
        report = validate(args.path)
    except (OSError, UnicodeError, ValueError) as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
