# Media quality assurance

## Status vocabulary

- `PASS`: the check ran and met its criterion.
- `FAIL`: the check ran and violated its criterion.
- `NOT_VERIFIED`: the check could not run or lacks enough evidence.

Never turn a missing tool or skipped review into `PASS`.

## Automated checks

When FFprobe/FFmpeg are available, inspect:

- container decodes and duration is nonzero;
- expected video and audio streams exist;
- resolution, frame rate, pixel format, sample rate, and channel count;
- audio/video duration alignment;
- MP4 faststart atom ordering where applicable;
- black or near-black spans beyond the declared creative intent;
- long silence beyond the declared pause plan;
- final frame and audio tail are not clipped.

Thresholds belong to the project brief. The checker reports observations and conservative defaults; it cannot know every artistic intention.

## Human checks

Automated metadata is necessary but insufficient. Perform:

1. full watch with sound;
2. audio-only listen through the complete file;
3. mobile-size preview with platform UI safe areas;
4. opening, middle, and ending frame inspection;
5. subtitle spelling, line breaks, synchronization, and contrast;
6. narration/BGM balance and cut-boundary noise;
7. visual-era, identity, anatomy, text-artifact, and reuse checks;
8. title, cover, description, and disclosure consistency with the actual video.

Record who performed each check and when. A different reviewer is valuable for the final watch when available.

## Release package

Package only the approved video, covers, title/description/topic copy, disclosures, final script, subtitle file, narration audio, storyboard, evidence table, QA report, and release record required by the project. Exclude temporary renders, test images, caches, credentials, browser data, and unrelated source material.

Run the privacy scanner on the package itself before sharing it.
