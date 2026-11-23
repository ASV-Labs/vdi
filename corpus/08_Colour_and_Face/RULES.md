---
id: VDI-08-RULES
title: "Colour and face processing: agent rules"
topic: 08_Colour_and_Face
status: Seed
last_updated: 2026-11-23
---

# 08_Colour_and_Face — agent rules

## Always

- **VDI-08-R01** · Always · stage: edit — Keep skin dE < 3.5 across every face-to-face cut. Check: Gate: face continuity (YuNet face box, skin pixels, CIE76). [AX ax-v5: T3] Threshold from AX within-take range [UNVERIFIED as a perception threshold]
- **VDI-08-R02** · Always · stage: edit — Grade each pickup to the take (skin lightness and colour) and match sharpness before composing. Check: Gate: face continuity. [AX ax-v5: T3]

## Never

- **VDI-08-R03** · Never · stage: edit — No halo and no smeared skin; if the choice is soft-natural or sharp-plastic, choose soft-natural. Check: Human review at 100% on a phone. [AX ax-gr4: #5] [AX lessons-001: 4 table]
- **VDI-08-R04** · Never · stage: edit — Do not add AI upscaling or face restoration to fix a soft source. Check: No such stage in the render chain. [AX ax-editnotes: v4 item 1 Real-ESRGAN not better]

## Prefer

- **VDI-08-R05** · Prefer · stage: edit — Prefer a gentle shadow lift and slight warmth for overhead-lit footage over strong local contrast. Check: Review frames. [AX ax-gr1: grade gently]
