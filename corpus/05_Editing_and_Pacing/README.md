---
id: VDI-05-README
title: "Editing and pacing (cuts, holds, joins, endings, layout churn): overview"
topic: 05_Editing_and_Pacing
status: Seed
last_updated: 2026-11-23
---

# 05_Editing_and_Pacing — Editing and pacing (cuts, holds, joins, endings, layout churn)

Edit rules measured on the rendered file: shot lengths, black panels, holds on evidence, word tails at cuts, gaps between sentences, endings and layout stability.

Stages: edit.

## What this topic covers

- Shot length and flash frames
- Snapping picture cuts to audio joins
- Evidence holds and pre-laps
- Word tails and fades
- Inter-sentence gaps
- Endings on a looping feed
- Layout churn (split vs full frame)

## Related topics

`04_Screen_Capture_and_Demos`, `06_Captions_and_On_Screen_Text`, `07_Audio`, `11_Review_and_QA`

# Overview

## The short version

- **Measure the render, not the plan.** The v4 editor's gate computed holds, cap heights and clean endings from the plan and passed 22/22; the files had 19 blocking defects. [AX ax-v5: gate section] [AX ax-qa-v4]
- **Picture and sound cut together.** Picture cut at the audio join and the shot mark landed 2-3 frames later, so the zoom reset twice: a 2-3 frame flash at the hook/intro join in AX-01..04. [AX ax-v5: T2] [AX ax-reviewer: picture]
- **Fade after the consonant, not before.** Cut lists ended a piece 0.17 s after the last 10 ms frame above -38 dBFS, then faded 60 ms; quiet final /s/, /ts/, /st/ fell below that and were cut. [AX ax-v5: T1]
- **Shorts loop.** On a looping feed an ending 0.13 s after the last word sounds chopped. [AX ax-gr4: #3]

## Where this sits in the workflow

Stages: edit. The rules in `RULES.md` are keyed to these stages, so `vdi_checklist(stage)` and `vdi_brief(...)` in the MCP server can pull them.

# Known gaps

## Research gaps

1. **SEED** - 12 frames, 1.6 s, 0.12 s and 0.6-0.8 s are house rules, not viewer-tested.
2. **SEED** - The gate's blank-panel check finds near-black rows only; a white first frame (lessons-002 8.6) is not detected yet.
3. **SEED** - Layout churn is not measured by the gate.
4. **SEED** - Whether split-screen beats full-frame alternation for watch time is unknown (lessons-001 7).

## Research seeds (leads not yet used)

- A/B the ending hold length on a looping feed for rewatch rate.
- Add a layout classifier (face / split / full) to the gate.
