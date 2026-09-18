# Audio-first production

## Fixed order

Use this order without collapsing stages:

`approved text -> narration -> subtitle timing -> storyboard -> visual pilot -> assets -> render -> QA`

Why: narration determines real duration and pauses; timing determines shot boundaries; the storyboard assigns one visual task to each section; the pilot tests the visual language before expensive batch work.

If approved text changes, invalidate every downstream artifact. If narration changes, invalidate timing and everything after it. If timing changes, re-check storyboard and render.

## Narration direction

Create a director copy that marks only meaningful pauses, emphasis, pace changes, and pronunciation. Do not turn every sentence into stage directions.

Listen for:

- fixed names and phrases that must not split;
- cause-and-effect sentences whose pause changes meaning;
- emotional turns that need space;
- plosive clicks, clipped joins, repeated syllables, or abrupt silence;
- a consistent voice, pace, and loudness across repairs.

Lock the audio file by hash before timing subtitles.

## Subtitles

- Time subtitles to the locked audio, not estimated reading speed.
- Keep each group semantically complete and short enough to read on a phone.
- Never strand punctuation at the beginning of a line.
- Keep translations no more certain than the source-language narration.
- Define safe margins for platform UI, but keep platform presets outside the core Skill.
- Review rendered subtitles visually; a valid subtitle file does not prove the burned result is readable.

## Storyboard

One shot has one primary job: establish place, reveal a person, show an action, show a cost, expose evidence, or bridge time. Record the linked subtitle range and evidence-claim IDs.

Do not require motion in every shot. Choose stillness, hard cuts, restrained parallax, or generated motion only when it improves the meaning. Decorative movement that competes with narration fails.

## Visual pilot before batch production

Generate or assemble only:

- two style anchors establishing character, period, texture, color, and depth;
- two or three highest-risk action shots;
- one subtitle-safe composition if the frame is crowded.

Approve the pilot before producing the remaining assets. Failure invalidates the visual direction, not the approved narration.

## Visual realism checks

Apply only where relevant:

- material texture belongs to the period and object;
- bodies, cloth, weapons, smoke, and architecture carry believable weight;
- facial expression is motivated by visible action, not generic melodrama;
- foreground, subject, and background create readable depth;
- no accidental text, watermarks, modern objects, extra limbs, duplicated faces, or anachronistic design.

## Render candidate

Record output path, input hashes, encoder settings, duration, resolution, frame rate, audio format, subtitle status, and declared AI assistance. A render is only a candidate until media QA and full human review pass.
