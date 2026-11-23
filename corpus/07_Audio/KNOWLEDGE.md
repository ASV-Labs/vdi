---
id: VDI-07-KNOWLEDGE
title: "Audio (cleanup, loudness, joins, room tone): knowledge"
topic: 07_Audio
status: Seed
last_updated: 2026-11-23
---

# 07_Audio — knowledge

# Principles

## 1. Clean, but stop before the words break

DeepFilterNet (18 dB limit) ranked best in a blind A/B over the raw cut and the earlier gate/denoise chain; the harder chain produced clicks in pauses, pumping and cut word endings. [AX ax-gr4: blind A/B] [AX lessons-001: 2.2]

## 2. Measure peaks on the encoded file

The limiter was set to -1.5 dB before AAC encoding; the encoded file read about -0.5 dBTP. v4 set the ceiling by measuring the AAC track. [AX ax-editnotes: v2 note, v4 item 3]

## 3. Two meters disagree; trust the plain one too

The editor's gate (momentary LUFS, 1.6 s, top-8 dB mean) said steps <= 1.3 LU; a plain 1 s speech-frame RMS said 2.0-3.2 dB at 11 joins. [AX ax-reviewer: level step] [AX ax-v5: gate section]

## 4. Platforms normalise down, not up

YouTube turns content louder than its reference down and does not turn quieter content up; the reference value is not published by YouTube. [SRC prodadvice-yt]

# Patterns

## VDI-07-P01 Chain A/B

Same 11 s, labels hidden, ranked by a listener (AX used AI Studio listening); keep the winner, do not stack more processing. [AX ax-gr4]

## VDI-07-P02 Encode-then-limit

Measure true peak on the AAC file and set the limiter ceiling from that. [AX ax-editnotes: v4 item 3]

## VDI-07-P03 Room-tone crossfade

Crossfade joins over room tone, never through silence. [AX ax-v5: AX-05]

# Anti-patterns

| id | Anti-pattern | How it shows | Fix | Evidence |
|---|---|---|---|---|
| VDI-07-A01 | Gate chain | Expander/gate + afftdn: clicks in pauses, pumping, cut endings. | Single neural denoiser with a limit. | [AX ax-gr4: blind A/B] |
| VDI-07-A02 | Pre-encode limiter only | Peaks rise after AAC encoding. | Measure on the encoded file. | [AX ax-editnotes: v2] |
| VDI-07-A03 | Meter shopping | Using the meter that says PASS. | Report a plain 1 s RMS step too. | [AX ax-reviewer: level step] |

# Implementation notes

## Loudness

ffmpeg -i final.mp4 -af ebur128=peak=true -f null - ; read I and Peak from the summary. vdi/release.py check_loudness.

## Floors (AX v4)

Floor between words relative to speech, v3 -> v4: AX-01 -22 -> -37 dB, AX-02 -21 -> -36, AX-03 -24 -> -40, AX-04 -26 -> -41, AX-05 -26 -> -41. [AX ax-editnotes: v4 item 2]

## Dropouts

Decode at 48 kHz, find runs of exact-zero samples > 1 ms away from the file edges; merge runs within 30 ms. check_dropouts.

## Gate checks that cover this topic

- **loudness and true peak**: check_loudness
- **1 s speech-level step**: check_join_levels
- **room tone through joins**: check_dropouts
- **word endings**: check_word_endings

# Glossary

- **LUFS**: Loudness units relative to full scale (ITU-R BS.1770 family).
- **dBTP**: True-peak level, including inter-sample peaks.
- **Room tone**: The room's own sound with no speech; used to fill joins.
- **DeepFilterNet**: Neural speech enhancement model used on AX (deep-filter 0.5.6 binary).
