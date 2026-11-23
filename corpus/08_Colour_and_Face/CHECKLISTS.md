---
id: VDI-08-CHECKLISTS
title: "Colour and face processing: checklists"
topic: 08_Colour_and_Face
status: Seed
last_updated: 2026-11-23
---

# 08_Colour_and_Face — checklists

# Build checklist

## Stage: edit

- [ ] Keep skin dE < 3.5 across every face-to-face cut (VDI-08-R01)
- [ ] Grade each pickup to the take (skin lightness and colour) and match sharpness before composing (VDI-08-R02)
- [ ] No halo and no smeared skin… (VDI-08-R03)
- [ ] Do not add AI upscaling or face restoration to fix a soft source (VDI-08-R04)
- [ ] Prefer a gentle shadow lift and slight warmth for overhead-lit footage over strong local contrast (VDI-08-R05)

# Design review checklist

- [ ] Is skin colour continuous across every face cut?
- [ ] Any halo or plastic skin at phone size?
- [ ] Were pickups graded to the take?

## Rules these questions test

- VDI-08-R01 (Always, edit): Keep skin dE < 3.5 across every face-to-face cut
- VDI-08-R02 (Always, edit): Grade each pickup to the take (skin lightness and colour) and match sharpness before composing
- VDI-08-R03 (Never, edit): No halo and no smeared skin…
- VDI-08-R04 (Never, edit): Do not add AI upscaling or face restoration to fix a soft source
- VDI-08-R05 (Prefer, edit): Prefer a gentle shadow lift and slight warmth for overhead-lit footage over strong local contrast

# QA checklist

- [ ] **face continuity**: check_faces
- [ ] **face look**: Human review only: the gate cannot measure plastic or halo.

- Font legibility issues such as 0 vs O.
- Layout churn and pacing feel.

# Red flags

- Face looks waxy or smoothed at phone size
- Bright outline around the head against a light wall
- Skin warmer or darker after a cut
- A pickup framed against a different part of the room
- An AI upscale or face-restoration step in the render chain
- Sharpening strength raised to compensate for a soft source

## Matching anti-patterns

- VDI-08-A01 Plastic face: Lighter processing; better capture.
- VDI-08-A02 Ungraded pickup: Grade to take.

# Evaluation template

- **Video:** <file>

| # | Criterion | Severity | Result (PASS/FAIL) | Evidence (timestamp, frame, measurement) |
|---|---|---|---|---|
| 1 | Skin dE < 3.5 at face cuts | blocker | | |
| 2 | No halo/plastic skin | major | | |
