---
id: VDI-04-README
title: "Screen capture and product demos: overview"
topic: 04_Screen_Capture_and_Demos
status: Seed
last_updated: 2026-11-23
---

# 04_Screen_Capture_and_Demos — Screen capture and product demos

How to capture terminals, agent runs and web pages so every line on screen is real, from the run the words describe, readable at phone size, and free of personal data and plan walls.

Stages: screen.

## What this topic covers

- Real runs only; saved verbatim output
- One spoken claim = one run
- Narrow terminals (44-60 columns, 30 px font)
- Phone-width page captures
- PII, sign-in codes and plan walls
- Sample-work labels

## Related topics

`01_Scripting_and_Boards`, `05_Editing_and_Pacing`, `06_Captions_and_On_Screen_Text`, `12_Claims_and_Honesty`

# Overview

## The short version

- **Never fake product output.** Every terminal line, UI state and result on screen comes from a real run or a live page captured that day; OC-01 v4 was rejected on Nov 18 for agent lines no run produced. [AX lessons-001: 3.1]
- **One claim, one run.** AX-01 showed the prompt from run 1 and the results from run 2; AX-04 put the repo's demo graph (grok-4.7, a URL source, 11/5) between terminal beats from tonight's glm-5.3 run as if it were the same file. [AX ax-v5: AX-01 26.5-28.2 s; AX-04 18.3-24.2 s] [AX lessons-001: 3.2]
- **Capture at the size it will be read.** Zooming a wide terminal makes text big but crops lines at the frame edge ('changed evidenced sample-reve' exactly when he says 'names the source'). A 60x22 terminal at 30 px fits 1080 wide; 100 columns does not. [AX ax-gr4: #1] [AX ax-screens-ax04: recording pipeline]

## Where this sits in the workflow

Stages: screen. The rules in `RULES.md` are keyed to these stages, so `vdi_checklist(stage)` and `vdi_brief(...)` in the MCP server can pull them.

# Known gaps

## Research gaps

1. **SEED** - Readable hold of 1.6 s at phone size is a rule of thumb; never measured with real viewers. [UNVERIFIED]
2. **SEED** - No tested method yet for verifying that footage is from the declared run (the gate checks declarations and labels, not truth).

## Research seeds (leads not yet used)

- Viewer test of minimum readable hold for dense terminal text on a phone.
- Embed run ids in captured frames (tiny corner text) so the gate can verify them by OCR.
