---
id: VDI-08-README
title: "Colour and face processing: overview"
topic: 08_Colour_and_Face
status: Seed
last_updated: 2026-11-23
---

# 08_Colour_and_Face — Colour and face processing

Grade faces to match across cuts, measure it as skin dE on the rendered file, and keep face processing soft and natural rather than sharp and plastic.

Stages: edit.

## What this topic covers

- Skin colour continuity across cuts
- Grading pickups to the take
- Sharpening and denoise limits
- Halo and plastic-skin artefacts

## Related topics

`02_Talking_Head_Capture`, `03_Pickups_and_Continuity`, `05_Editing_and_Pacing`

# Overview

## The short version

- **Soft-natural beats sharp-plastic.** v4's denoise + sharpen read as mild plastic smoothing with a faint halo against the white wall. [AX ax-gr4: #5] [AX lessons-001: 4 table]
- **Skin colour is the continuity signal.** Within a take, skin dE across cuts was 0.2-3.1; at take<->pickup cuts 6.3-9.6. [AX ax-reviewer: face grade]
- **Grade midtones, keep the wall white.** v2 matched skin on midtones only so the white wall stayed white. [AX ax-editnotes: v2 face grade]

## Where this sits in the workflow

Stages: edit. The rules in `RULES.md` are keyed to these stages, so `vdi_checklist(stage)` and `vdi_brief(...)` in the MCP server can pull them.

# Known gaps

## Research gaps

1. **SEED** - No metric for 'plastic' or 'halo' in the gate.
2. **SEED** - The dE threshold is from AX data, not perceptual testing.

## Research seeds (leads not yet used)

- Find a no-reference sharpness/naturalness metric usable on faces.
- Test dE visibility on phone screens.
