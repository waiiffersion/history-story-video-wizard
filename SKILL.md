---
name: history-story-video-wizard
description: Turn a historical topic and sources into an evidence-gated, story-first narration and a verified short-video release package. Use when planning, writing, auditing, storyboarding, subtitling, rendering, or quality-checking historical videos; when claims or conflicting sources must be traced; or when a resumable production workflow is needed. Do not use for automatic account login, platform upload, scheduling, or publication.
---

# History Story Video Wizard

Build historical videos in a fixed order so research, story, audio, visuals, and release checks cannot silently overwrite one another.

## Operating contract

1. Create a project state file with `python3 scripts/project_state.py init <project-dir>`.
2. Research claims before prose. Read [references/evidence.md](references/evidence.md), then fill [assets/templates/evidence-table.md](assets/templates/evidence-table.md).
3. Define the human conflict before drafting. Read [references/storytelling.md](references/storytelling.md), then fill [assets/templates/story-promise.md](assets/templates/story-promise.md).
4. Draft narration for the ear, not for an essay. Keep source apparatus outside the spoken script unless the source identity is itself the story.
5. Audit the script with [assets/templates/script-audit.md](assets/templates/script-audit.md). Stop if evidence, causality, story, or spoken-language gates fail.
6. Lock approved text before making narration audio. Any later text change invalidates narration, timing, storyboard, assets, render, and media QA.
7. Follow [references/production.md](references/production.md): narration -> subtitle timing -> storyboard -> visual pilot -> assets -> render.
8. Follow [references/media-qa.md](references/media-qa.md), run `python3 scripts/media_qc.py <video>`, and record results in [assets/templates/release-record.md](assets/templates/release-record.md).
9. Run `python3 scripts/privacy_scan.py .` before sharing the package.

## State machine

Advance one state at a time and attach an evidence file for every transition:

`BRIEF_READY -> EVIDENCE_READY -> STORY_DRAFTED -> TEXT_AUDIT_PASS -> TEXT_APPROVED -> NARRATION_LOCKED -> SUBTITLE_TIMING_LOCKED -> STORYBOARD_LOCKED -> VISUAL_PILOT_PASS -> ASSET_READY -> RENDERED_CANDIDATE -> MEDIA_QA_PASS -> FINAL_APPROVED -> RELEASE_PACKAGE_READY`

`TEXT_APPROVED`, `FINAL_APPROVED`, upload authorization, and public release are different decisions. This Skill ends at `RELEASE_PACKAGE_READY`; it never logs in, uploads, schedules, or publishes.

## Non-negotiable boundaries

- Separate documented fact, source claim, scholarly inference, and creative reconstruction.
- Never invent dialogue, inner thoughts, motives, actions, numbers, or composite chronology and present them as fact.
- A later source is not automatically false, and an early source is not automatically true. Evaluate source identity, distance, independence, purpose, and corroboration.
- Do not hide uncertainty in titles, translations, images, or subtitles.
- Use synthetic examples only in this repository. Keep private paths, accounts, credentials, sessions, unpublished media, private hashes, and platform-specific authorization out of public artifacts.
- Missing media tools produce `NOT_VERIFIED`, never a false `PASS`.

## Reference routing

- Claim provenance, conflicting accounts, certainty language: [references/evidence.md](references/evidence.md)
- Hooks, causal spine, scene writing, colloquial narration: [references/storytelling.md](references/storytelling.md)
- Audio-first production order, visual pilot, storyboard rules: [references/production.md](references/production.md)
- Technical and human media checks: [references/media-qa.md](references/media-qa.md)
