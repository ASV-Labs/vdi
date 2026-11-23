---
id: VDI-02-CHECKLISTS
title: "Talking-head capture (camera, light, framing, mic, room): checklists"
topic: 02_Talking_Head_Capture
status: Seed
last_updated: 2026-11-23
---

# 02_Talking_Head_Capture — checklists

# Build checklist

## Stage: shoot

- [ ] Use a phone rear camera at 4K held vertical, or a real camera… (VDI-02-R01)
- [ ] Put the key light in front of the face at about 45 degrees, at eye level… (VDI-02-R02)
- [ ] Frame the face for the 9:16 crop at capture… (VDI-02-R03)
- [ ] Mic close… (VDI-02-R04)
- [ ] Damp the room… (VDI-02-R05)
- [ ] Finish the last word fully, then hold still and silent for one second (VDI-02-R06)
- [ ] Say each line twice with a pause (VDI-02-R07)
- [ ] Note wardrobe, framing marks, light state and mic for every take, so pickups can match (VDI-02-R08)

## Stage: edit

- [ ] Never try to rescue a soft webcam face with heavy sharpening or upscaling (VDI-02-R09)

# Design review checklist

- [ ] Is the source resolution enough for 1080x1920 without heavy upscale?
- [ ] Are the eyes lit?
- [ ] Is the floor between words well below speech?
- [ ] Does each section end with a held second of silence?

## Rules these questions test

- VDI-02-R01 (Always, shoot): Use a phone rear camera at 4K held vertical, or a real camera…
- VDI-02-R02 (Always, shoot): Put the key light in front of the face at about 45 degrees, at eye level…
- VDI-02-R03 (Always, shoot): Frame the face for the 9:16 crop at capture…
- VDI-02-R04 (Always, shoot): Mic close…
- VDI-02-R05 (Always, shoot): Damp the room…
- VDI-02-R06 (Always, shoot): Finish the last word fully, then hold still and silent for one second
- VDI-02-R07 (Always, shoot): Say each line twice with a pause
- VDI-02-R08 (Always, shoot): Note wardrobe, framing marks, light state and mic for every take, so pickups can match
- VDI-02-R09 (Never, edit): Never try to rescue a soft webcam face with heavy sharpening or upscaling

# QA checklist

- [ ] **word endings against the source envelopes**: Indirect: good capture leaves a clean consonant and a hold for the edit.
- [ ] **face continuity**: Capture sheet makes pickups match.

- Font legibility issues such as 0 vs O.
- Layout churn and pacing feel.

# Red flags

- Landscape webcam as the main camera
- Overhead light only
- Mic more than an arm's length away
- Takes that end on the last word with no hold

## Matching anti-patterns

- VDI-02-A01 Webcam crop: Shoot vertical at 4K.
- VDI-02-A02 Overhead light: Key light in front at 45 degrees.
- VDI-02-A03 Mic at arm's length in a bare room: Lav or phone close; damp the room.

# Evaluation template

- **Video:** <file>

| # | Criterion | Severity | Result (PASS/FAIL) | Evidence (timestamp, frame, measurement) |
|---|---|---|---|---|
| 1 | Source covers 1080x1920 without >1.1x upscale | major | | |
| 2 | Eyes lit, no overhead-only light | major | | |
| 3 | Floor >= 25 dB below speech in raw | major | | |
| 4 | Tail hold after last word | blocker | | |
