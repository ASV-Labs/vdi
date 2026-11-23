---
id: VDI-07-CHECKLISTS
title: "Audio (cleanup, loudness, joins, room tone): checklists"
topic: 07_Audio
status: Seed
last_updated: 2026-11-23
---

# 07_Audio — checklists

# Build checklist

## Stage: audio

- [ ] Use a light neural denoiser (AX… (VDI-07-R01)
- [ ] Hit the house loudness target on the final AAC… (VDI-07-R02)
- [ ] Take room tone from a real pause in the source take, through the same clean-up chain, with its… (VDI-07-R03)
- [ ] Keep room tone continuous through every join… (VDI-07-R04)
- [ ] Keep the 1 s speech-level step across each join under 2 dB (<= 1 LU at pickups) (VDI-07-R05)
- [ ] Detect word ends on a >= 3.5 kHz envelope as well as full band before fading (VDI-07-R06)
- [ ] Never push noise or echo removal further once words start to gate… (VDI-07-R08)
- [ ] Optional, gentle… (VDI-07-R09)

## Stage: review

- [ ] Listen (a human) at every flagged timestamp before posting… (VDI-07-R07)

# Design review checklist

- [ ] Was the cleanup chain chosen by blind A/B?
- [ ] Is loudness measured on the final AAC?
- [ ] Any join with a level or presence jump?
- [ ] Has a human listened at every flagged time?

## Rules these questions test

- VDI-07-R01 (Always, audio): Use a light neural denoiser (AX…
- VDI-07-R02 (Always, audio): Hit the house loudness target on the final AAC…
- VDI-07-R03 (Always, audio): Take room tone from a real pause in the source take, through the same clean-up chain, with its…
- VDI-07-R04 (Always, audio): Keep room tone continuous through every join…
- VDI-07-R05 (Always, audio): Keep the 1 s speech-level step across each join under 2 dB (<= 1 LU at pickups)
- VDI-07-R06 (Always, audio): Detect word ends on a >= 3.5 kHz envelope as well as full band before fading
- VDI-07-R07 (Always, review): Listen (a human) at every flagged timestamp before posting…
- VDI-07-R08 (Never, audio): Never push noise or echo removal further once words start to gate…
- VDI-07-R09 (Prefer, audio): Optional, gentle…

# QA checklist

- [ ] **loudness and true peak**: check_loudness
- [ ] **1 s speech-level step**: check_join_levels
- [ ] **room tone through joins**: check_dropouts
- [ ] **word endings**: check_word_endings

- Font legibility issues such as 0 vs O.
- Layout churn and pacing feel.

# Red flags

- True peak measured only before encoding
- Clicks or pumping in pauses
- Words that end abruptly
- Silence (digital zero) at joins

## Matching anti-patterns

- VDI-07-A01 Gate chain: Single neural denoiser with a limit.
- VDI-07-A02 Pre-encode limiter only: Measure on the encoded file.
- VDI-07-A03 Meter shopping: Report a plain 1 s RMS step too.

# Evaluation template

- **Video:** <file>

| # | Criterion | Severity | Result (PASS/FAIL) | Evidence (timestamp, frame, measurement) |
|---|---|---|---|---|
| 1 | Integrated -14 +-0.5 LUFS on the final | major | | |
| 2 | True peak <= -1.5 dBTP on the final | major | | |
| 3 | No digital zero at joins | major | | |
| 4 | Level steps < 2 dB | blocker | | |
| 5 | Human listen at flagged times | blocker | | |
