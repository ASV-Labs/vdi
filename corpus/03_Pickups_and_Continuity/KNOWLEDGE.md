---
id: VDI-03-KNOWLEDGE
title: "Pickups and continuity: knowledge"
topic: 03_Pickups_and_Continuity
status: Seed
last_updated: 2026-11-23
---

# 03_Pickups_and_Continuity — knowledge

# Principles

## 1. A pickup is part of the take, not a patch

Pickups shot later were darker, warmer, softer and framed against a different part of the wall: skin dE 6.3-9.6 at the cut vs 0.2-3.1 within a take. [AX ax-v5: T3] [AX ax-reviewer: face grade]

## 2. Voice memos are a different microphone

Phone voice memos sounded closer and drier than the webcam mic; joins needed EQ, level and room-tone matching. [AX ax-pickups: memo mic note] [AX lessons-001: 2.4]

## 3. Joins are checked on the final, with numbers

The v4 gate said the largest level step was 1.3 LU; the independent reviewer measured 2.0-3.2 dB 1 s speech-level steps at 11 joins. Measure the rendered file, by a method that does not share the editor's assumptions. [AX ax-reviewer: level step] [AX ax-editnotes: v4 gate table]

# Patterns

## VDI-03-P01 Pickup sheet

Per line: where it plays (on camera or under screen), the take it must match, device, spot, wardrobe, light. [AX ax-gr1: pickups table]

## VDI-03-P02 Grade-to-take

Measure skin Lab in the take near the cut; apply a gain to the pickup's midtones until dE < 3.5; check sharpness. [AX ax-v5: T3]

## VDI-03-P03 Mic match

Long-term average spectrum of speech frames from each source; EQ the pickup to the take; level-match; room tone bed under the join. [AX ax-editnotes: pickups]

# Anti-patterns

| id | Anti-pattern | How it shows | Fix | Evidence |
|---|---|---|---|---|
| VDI-03-A01 | Afternoon pickup | Pickup shot hours later in different light and a different spot. | Same day, same marks, or grade and reframe to match. | [AX ax-reviewer: AX-02 36.2 s, AX-03 9.9-15.1 s backgrounds differ] |
| VDI-03-A02 | Memo-to-camera jump | Voice memo line sits next to camera audio with a presence step. | Mic-match EQ and level; keep room tone. | [AX ax-gr4: #6 AX-01 0:29-0:34, AX-05 0:40] |
| VDI-03-A03 | Join to digital zero | Fade to silence at a join leaves an 8 ms hole. | Crossfade over room tone. | [AX ax-v5: AX-05 15.83 s, 24.10 s] |

# Implementation notes

## Skin dE at a cut

Detect the face (YuNet), take the inner face box, mask skin pixels in YCrCb, average Lab on three frames each side of the cut, CIE76 distance. vdi/release.py check_faces. Threshold 3.5 from AX within-take range 0.2-3.1. [AX ax-reviewer: facegrade]

## 1 s level step

Mean power of speech frames (10 ms frames within 18 dB of the file's speech level) in 1 s before vs 1 s after each join; < 2 dB. [AX ax-reviewer: audio.py]

## Finding joins without the plan

The gate cross-correlates 0.5 s windows of the final's speech against each source file, so joins are found from the rendered audio. [AX vdi-gate-proof: alignment]

## Gate checks that cover this topic

- **face continuity (skin dE < 3.5)**: Gate check_faces.
- **1 s speech-level step across joins**: Gate check_join_levels.
- **room tone through joins**: Gate check_dropouts.
- **word endings against the source envelopes**: Gate check_word_endings.

# Glossary

- **Join**: A point in the final where audio changes source or skips within a source.
- **dE (CIE76)**: Euclidean distance between two Lab colours; ~1 is just noticeable, AX takes vary 0.2-3.1 within a take.
- **Mic match**: EQ and level adjustment so a pickup recorded on another mic sounds like the take.
