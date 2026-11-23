---
id: VDI-08-KNOWLEDGE
title: "Colour and face processing: knowledge"
topic: 08_Colour_and_Face
status: Seed
last_updated: 2026-11-23
---

# 08_Colour_and_Face — knowledge

# Principles

## 1. Soft-natural beats sharp-plastic

v4's denoise + sharpen read as mild plastic smoothing with a faint halo against the white wall. [AX ax-gr4: #5] [AX lessons-001: 4 table]

## 2. Skin colour is the continuity signal

Within a take, skin dE across cuts was 0.2-3.1; at take<->pickup cuts 6.3-9.6. [AX ax-reviewer: face grade]

## 3. Grade midtones, keep the wall white

v2 matched skin on midtones only so the white wall stayed white. [AX ax-editnotes: v2 face grade]

# Patterns

## VDI-08-P01 Skin-anchored grade

Measure Lab of skin in the take near each cut; adjust the pickup's midtones to match. [AX ax-v5: T3]

## VDI-08-P02 Face-box measurement

Detect the face, use its inner box to avoid hair and background, mask skin in YCrCb, average Lab. [AX vdi-gate-proof: check_faces]

# Anti-patterns

| id | Anti-pattern | How it shows | Fix | Evidence |
|---|---|---|---|---|
| VDI-08-A01 | Plastic face | Denoise + sharpen smear skin and halo edges. | Lighter processing; better capture. | [AX ax-gr4: #5] |
| VDI-08-A02 | Ungraded pickup | Pickup darker/warmer than the take. | Grade to take. | [AX ax-v5: T3] |

# Implementation notes

## Gate method

Frames at 180x320; OpenCV FaceDetectorYN (YuNet 2023mar, downloaded to ~/.cache/vdi-gate/models on first run, not stored in the repo); face box height >= 12% of the frame; skin mask in YCrCb; mean Lab over three frames each side of every picture change or audio join; CIE76 dE.

## Sharpness check (reviewer)

Laplacian variance of the inner face: pickups 7-10 vs takes 15-29 on AX, showing pickups were softer. [AX ax-reviewer: face grade]

## Gate checks that cover this topic

- **face continuity**: check_faces
- **face look**: Human review only: the gate cannot measure plastic or halo.

# Glossary

- **Skin dE**: Colour distance between mean skin Lab values either side of a cut.
- **Halo**: A bright or dark outline around edges from over-sharpening.
- **Midtones**: The middle of the tonal range, where skin usually sits.
