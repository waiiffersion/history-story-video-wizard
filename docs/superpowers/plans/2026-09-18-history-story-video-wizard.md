# History Story Video Wizard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publicly release a privacy-safe, installable, evidence-gated historical story video Skill.

**Architecture:** A concise `SKILL.md` routes to four focused references. Deterministic Python scripts manage resumable state, privacy scanning, and optional FFmpeg media checks. Templates provide stable project artifacts without bundling any private production data.

**Tech Stack:** Markdown, Python 3.9+, standard library, optional FFmpeg/FFprobe, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-18-history-story-video-wizard-design.md`

## Global Constraints

- Public files must not contain personal names, account identifiers, unpublished assets, absolute user paths, credentials, session data, private hashes, or project-specific authorizations.
- The Skill ends at a verified release package; it does not log in, upload, schedule, or publish to a live platform.
- Examples use synthetic historical material and are labeled synthetic.
- Python runtime support starts at 3.9 and uses only the standard library.
- External model calls and FFmpeg are optional capabilities, never assumed.

---

### Task 1: Scaffold the public Skill repository

**Files:**
- Create: `SKILL.md`
- Create: `agents/openai.yaml`
- Create: `README.md`
- Create: `README.en.md`
- Create: `LICENSE`
- Create: `.gitignore`

**Interfaces:**
- Consumes: approved design specification.
- Produces: installable Skill metadata and public repository entry points.

- [ ] Initialize `history-story-video-wizard` with `references`, `scripts`, and `assets` resources.
- [ ] Replace scaffold text with a discriminating description, platform-neutral state machine, approval boundaries, and reference routing.
- [ ] Add Chinese and English README files with one-line installation, capability boundaries, workflow diagram, and synthetic quick start.
- [ ] Add MIT license and repository ignores.
- [ ] Run `quick_validate.py` and verify exit code 0.

### Task 2: Create evidence and storytelling guidance

**Files:**
- Create: `references/evidence.md`
- Create: `references/storytelling.md`
- Create: `assets/templates/evidence-table.md`
- Create: `assets/templates/story-promise.md`
- Create: `assets/templates/script-audit.md`

**Interfaces:**
- Consumes: a historical topic and user-supplied or researched sources.
- Produces: evidence table, story promise, candidate narration, and audit result.

- [ ] Write source-identity rules that separate contemporaneous evidence, transmitted accounts, later conflicting traditions, and adaptations without treating age alone as truth.
- [ ] Write claim-level certainty and contested-version rules that prohibit invented dialogue, motives, actions, numbers, and composite timelines.
- [ ] Write the knowledge-to-story method: burden question, causal spine, relationship plus anomalous action opening, visible scenes, colloquial narration, consequence, and new understanding.
- [ ] Add templates with explicit pass/fail fields and source-to-claim traceability.
- [ ] Verify all references are linked from `SKILL.md` and contain no private identifiers.

### Task 3: Create production and media QA guidance

**Files:**
- Create: `references/production.md`
- Create: `references/media-qa.md`
- Create: `assets/templates/storyboard.csv`
- Create: `assets/templates/release-record.md`

**Interfaces:**
- Consumes: approved narration text and locked narration audio.
- Produces: subtitle timing, storyboard, visual pilot result, candidate video, QA report, and release package.

- [ ] Define the fixed order `text -> narration -> subtitle timing -> storyboard -> visual pilot -> assets -> render -> QA`.
- [ ] Define two style anchors plus two or three highest-risk action shots before batch generation.
- [ ] Define optional realism checks for material texture, physical weight, motivated micro-expression, and scene depth without forcing motion or atmosphere into every shot.
- [ ] Define proportional technical and human media checks, including decode, stream metadata, black frames, silence, subtitle safety, full watch, audio-only listen, and mobile preview.
- [ ] Add storyboard and release record templates.

### Task 4: Implement resumable project state

**Files:**
- Create: `scripts/project_state.py`
- Create: `tests/test_project_state.py`

**Interfaces:**
- Produces commands `init`, `status`, `advance`, and `validate` over `PROJECT_STATE.json`.

- [ ] Write tests for initialization, valid sequential advancement, skipped-state rejection, evidence hashing, and corrupted-state rejection.
- [ ] Run the tests and verify they fail before implementation.
- [ ] Implement the minimal standard-library state manager.
- [ ] Run the tests and verify all state tests pass.

### Task 5: Implement privacy scanning

**Files:**
- Create: `scripts/privacy_scan.py`
- Create: `tests/test_privacy_scan.py`

**Interfaces:**
- Produces exit code 0 plus JSON for a clean tree; nonzero plus findings for user-home paths, likely credentials, cookies, authorization headers, private keys, or configured private markers.

- [ ] Write tests for macOS/Linux/Windows user paths, common token prefixes, authorization headers, private-key blocks, ignored `.git` content, and clean synthetic examples.
- [ ] Run the tests and verify they fail before implementation.
- [ ] Implement recursive text scanning with binary and `.git` exclusion.
- [ ] Run the tests and verify all privacy tests pass.

### Task 6: Implement optional media QA

**Files:**
- Create: `scripts/media_qc.py`
- Create: `tests/test_media_qc.py`

**Interfaces:**
- Produces a JSON report with `PASS`, `FAIL`, or `NOT_VERIFIED` for container, video stream, audio stream, duration alignment, faststart, black frames, and long silence.

- [ ] Write unit tests for frame-rate parsing, stream evaluation, faststart atom order, and `NOT_VERIFIED` when FFmpeg tools are absent.
- [ ] Run the tests and verify they fail before implementation.
- [ ] Implement probe parsing and optional subprocess checks without third-party packages.
- [ ] Run unit tests; if FFmpeg is unavailable, verify integration fields are `NOT_VERIFIED`, not `PASS`.

### Task 7: Add synthetic example and CI

**Files:**
- Create: `examples/synthetic-case/README.md`
- Create: `examples/synthetic-case/BRIEF.md`
- Create: `examples/synthetic-case/EVIDENCE.md`
- Create: `examples/synthetic-case/STORY_PROMISE.md`
- Create: `.github/workflows/test.yml`

**Interfaces:**
- Consumes: no real person, account, platform, or historical claim.
- Produces: a safe walkthrough and automated Python 3.9/3.12 validation.

- [ ] Write a clearly labeled fictional case that demonstrates claim boundaries and state progression without masquerading as history.
- [ ] Add CI steps for unit tests, skill validation, and privacy scanning.
- [ ] Run the full local test suite and privacy scan.

### Task 8: Independent repository verification and public release

**Files:**
- Verify: every tracked file in the new repository.

**Interfaces:**
- Consumes: completed local repository.
- Produces: a public GitHub repository URL and verified remote commit.

- [ ] Initialize an independent Git repository inside the new project directory.
- [ ] Run skill validation, full unit tests, privacy scan, placeholder scan, and tracked-file inventory.
- [ ] Confirm `git diff --cached` contains only the public Skill repository.
- [ ] Commit the verified files.
- [ ] Create a public GitHub repository using the existing logged-in GitHub session without reading or exposing credentials.
- [ ] Push `main`, then reload the public repository page and confirm README, license, file tree, and commit are visible.
- [ ] Add concise description and topics: `agent-skill`, `codex`, `historical-research`, `storytelling`, `video-production`, `ffmpeg`.
