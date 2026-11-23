---
id: VDI-11-README
title: "Review and QA (AI review limits, independent review, blind A/B, gate design): overview"
topic: 11_Review_and_QA
status: Seed
last_updated: 2026-11-23
---

# 11_Review_and_QA — Review and QA (AI review limits, independent review, blind A/B, gate design)

Who and what to trust for review: a gate that measures the rendered file, an independent reviewer, an AI reviewer that actually watches the video, blind A/B for audio, and the owner's own OK.

Stages: review.

## What this topic covers

- Gate design rules
- Independent review
- AI video review (what works, what does not)
- Blind A/B
- Release hold

## Related topics

`05_Editing_and_Pacing`, `06_Captions_and_On_Screen_Text`, `07_Audio`, `12_Claims_and_Honesty`, `13_Anti_Patterns`

# Overview

## The short version

- **A gate that reads the plan grades itself.** v4 'passed 22/22' with 19 blocking defects: caption checks compared the plan with itself; safe area, cap height and holds were computed from the plan; 'clean ending' always passed because every piece had a fade; ASR tolerance lists excused real defects. [AX lessons-001: 5.3] [AX ax-v5: gate section] [AX ax-qa-v4]
- **Prove the gate on known-bad files.** A gate must FAIL a known-bad file on each defect class it claims to catch. The VDI gate was run on the five v4 files. [AX lessons-001: 5.3] [AX vdi-gate-proof]
- **The Gemini web app did not watch the videos.** Attaching Drive videos in gemini.google.com delivered only transcripts; its 'caption misspellings' and wardrobe notes were its own guesses. AI Studio with the video attached quoted on-screen text exactly. [AX lessons-001: 5.1] [AX ax-gr3] [AX ax-gr4]
- **An independent reviewer finds what the editor cannot.** A reviewer agent that did not make the edit found what the editor and its gate missed. [AX lessons-001: 5.4] [AX ax-reviewer]

## Where this sits in the workflow

Stages: review. The rules in `RULES.md` are keyed to these stages, so `vdi_checklist(stage)` and `vdi_brief(...)` in the MCP server can pull them.

# Known gaps

## Research gaps

1. **SEED** - The gate's own false-positive rate on good files is unknown: no good (passing) reference file exists yet.
2. **SEED** - AI Studio's reliability beyond AX is not measured.

## Research seeds (leads not yet used)

- Make a known-good fixture (a short that passes review) to measure the gate's false positives.
- Repeat the AI Studio review with a second model and compare.
