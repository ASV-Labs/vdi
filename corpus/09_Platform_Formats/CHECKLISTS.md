---
id: VDI-09-CHECKLISTS
title: "Platform formats (TikTok, Reels, YouTube Shorts, X): checklists"
topic: 09_Platform_Formats
status: Seed
last_updated: 2026-11-23
---

# 09_Platform_Formats — checklists

# Build checklist

## Stage: publish

- [ ] Deliver 9:16 at 1080x1920, 30 fps, H.264 + AAC (VDI-09-R01)
- [ ] Keep text and key visuals out of the platform UI… (VDI-09-R02)
- [ ] Keep Shorts that use any third-party content under one minute, or clear the rights… (VDI-09-R03)
- [ ] Assume sound on for Reels but caption anyway… (VDI-09-R04)
- [ ] Prefer 15-60 s for this series (AX shorts were 40-47 s)… (VDI-09-R06)
- [ ] For X, check the account's limit… (VDI-09-R07)

## Stage: audio

- [ ] Do not rely on platform normalisation to make a quiet mix louder… (VDI-09-R05)

# Design review checklist

- [ ] Is the master 1080x1920, 30 fps, H.264+AAC?
- [ ] Is all text inside every target platform's safe zone?
- [ ] Any copyrighted content in a Short over 60 s?

## Rules these questions test

- VDI-09-R01 (Always, publish): Deliver 9:16 at 1080x1920, 30 fps, H.264 + AAC
- VDI-09-R02 (Always, publish): Keep text and key visuals out of the platform UI…
- VDI-09-R03 (Always, publish): Keep Shorts that use any third-party content under one minute, or clear the rights…
- VDI-09-R04 (Always, publish): Assume sound on for Reels but caption anyway…
- VDI-09-R05 (Always, audio): Do not rely on platform normalisation to make a quiet mix louder…
- VDI-09-R06 (Prefer, publish): Prefer 15-60 s for this series (AX shorts were 40-47 s)…
- VDI-09-R07 (Prefer, publish): For X, check the account's limit…

# QA checklist

- [ ] **container**: check_container
- [ ] **caption safe area**: check_captions
- [ ] **loudness**: check_loudness

- Font legibility issues such as 0 vs O.
- Layout churn and pacing feel.

# Red flags

- Text in the bottom 20% or right rail
- A Short over 60 s with music
- Relying on platform normalisation

## Matching anti-patterns

- VDI-09-A01 Text under the UI: Safe area.
- VDI-09-A02 Over-a-minute Short with claimed music: Stay under 60 s or clear rights.

# Evaluation template

- **Video:** <file>

| # | Criterion | Severity | Result (PASS/FAIL) | Evidence (timestamp, frame, measurement) |
|---|---|---|---|---|
| 1 | Container format | blocker | | |
| 2 | Text inside safe zones | blocker | | |
| 3 | Rights for > 60 s Shorts | blocker | | |
| 4 | Length window | minor | | |
