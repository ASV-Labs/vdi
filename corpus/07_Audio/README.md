---
id: VDI-07-README
title: "Audio (cleanup, loudness, joins, room tone): overview"
topic: 07_Audio
status: Seed
last_updated: 2026-11-23
---

# 07_Audio — Audio (cleanup, loudness, joins, room tone)

Voice cleanup that does not damage words, loudness and true peak measured on the encoded file, joins that keep room tone, and listening rules for what meters cannot judge.

Stages: audio.

## What this topic covers

- Noise and echo reduction
- Loudness and true peak after encoding
- Joins: level, EQ, room tone, dropouts
- Word tails
- Blind A/B for chain choices

## Related topics

`02_Talking_Head_Capture`, `03_Pickups_and_Continuity`, `05_Editing_and_Pacing`, `09_Platform_Formats`, `11_Review_and_QA`

# Overview

## The short version

- **Clean, but stop before the words break.** DeepFilterNet (18 dB limit) ranked best in a blind A/B over the raw cut and the earlier gate/denoise chain; the harder chain produced clicks in pauses, pumping and cut word endings. [AX ax-gr4: blind A/B] [AX lessons-001: 2.2]
- **Measure peaks on the encoded file.** The limiter was set to -1.5 dB before AAC encoding; the encoded file read about -0.5 dBTP. v4 set the ceiling by measuring the AAC track. [AX ax-editnotes: v2 note, v4 item 3]
- **Two meters disagree; trust the plain one too.** The editor's gate (momentary LUFS, 1.6 s, top-8 dB mean) said steps <= 1.3 LU; a plain 1 s speech-frame RMS said 2.0-3.2 dB at 11 joins. [AX ax-reviewer: level step] [AX ax-v5: gate section]
- **Platforms normalise down, not up.** YouTube turns content louder than its reference down and does not turn quieter content up; the reference value is not published by YouTube. [SRC prodadvice-yt]

## Where this sits in the workflow

Stages: audio. The rules in `RULES.md` are keyed to these stages, so `vdi_checklist(stage)` and `vdi_brief(...)` in the MCP server can pull them.

# Known gaps

## Research gaps

1. **SEED** - No platform publishes a single upload loudness target for short-form; -14 LUFS is a house choice. EBU R128, AES TD1004 and ITU-R BS.1770 were not fetched this session.
2. **SEED** - Nothing on AX was judged by a human ear; spectrograms and transcripts only. [AX ax-editnotes: 'Not judged by a human ear']

## Research seeds (leads not yet used)

- Fetch AES TD1004 and EBU R128 for streaming loudness recommendations.
- Measure what TikTok and Instagram do to an uploaded file's loudness (download and meter).
