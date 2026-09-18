# History Story Video Wizard

An installable Codex/agent Skill that turns a historical topic and sources into a traceable narration, locked audio workflow, storyboard, subtitles, verified video candidate, and release package.

It does not promise virality and does not log in, upload, schedule, or publish. Its job is to make every production stage explicit, evidence-bound, resumable, and testable.

## What it adds

- Claim-level provenance and certainty instead of a single “sourced” label for the whole script.
- A knowledge-to-story method based on human pressure, anomalous action, choice, cost, and changed understanding.
- A fixed text -> narration -> timing -> storyboard -> pilot -> assets -> render -> QA order.
- Evidence hashes that prevent stale scripts, audio, subtitles, or renders from being mixed.
- Optional FFmpeg checks that distinguish `PASS`, `FAIL`, and `NOT_VERIFIED`.
- A privacy scan for personal home paths, likely secrets, authorization headers, sessions, and custom private markers.

## Install

Copy this repository into your Codex Skills directory, or ask Codex to install the Skill from its GitHub repository.

## Quick start

```bash
python3 scripts/project_state.py init work/demo
cp assets/templates/evidence-table.md work/demo/EVIDENCE.md
cp assets/templates/story-promise.md work/demo/STORY_PROMISE.md
python3 scripts/project_state.py advance work/demo EVIDENCE_READY --evidence work/demo/EVIDENCE.md
python3 scripts/privacy_scan.py .
```

See [examples/synthetic-case](examples/synthetic-case) for a fully fictional walkthrough.

## Boundaries

- No automatic account login, upload, scheduling, or publication.
- No real project media, accounts, personal paths, credentials, authorization records, or unpublished scripts.
- No virality guarantee. The Skill improves evidence discipline, narrative clarity, production consistency, and verifiability.

## License

MIT
