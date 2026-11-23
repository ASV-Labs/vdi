---
id: VDI-13-RULES
title: "Anti-patterns: agent rules"
topic: 13_Anti_Patterns
status: Seed
last_updated: 2026-11-23
---

# 13_Anti_Patterns — agent rules

## Never

- **VDI-13-R01** · Never · stage: review — Self-grading gate: checks computed from the edit plan. Check: Gate code reads only the mp4 and source audio. [AX ax-qa-v4] [AX lessons-001: 5.3]
- **VDI-13-R02** · Never · stage: script — Reading from a truncating board. Check: Board vs script diff. [AX lessons-001: 1.1]
- **VDI-13-R03** · Never · stage: screen — Fake or stitched product output. Check: Run ids + labels; run README. [AX lessons-001: 3.1, 3.2]
- **VDI-13-R04** · Never · stage: screen — Wide terminal zoomed until lines crop. Check: Gate: evidence whole in frame. [AX ax-gr4: #1]
- **VDI-13-R05** · Never · stage: edit — Flash shots and black panels at joins. Check: Gate: shots, black panels. [AX ax-v5: T2]
- **VDI-13-R06** · Never · stage: edit — Fades that cut quiet final consonants. Check: Gate: word endings. [AX ax-v5: T1]
- **VDI-13-R07** · Never · stage: edit — Endings that stop on the last word. Check: Gate: ending hold. [AX ax-gr4: #3]
- **VDI-13-R08** · Never · stage: captions — Captions from the script instead of the audio. Check: Gate: captions vs transcript. [AX ax-v5: AX-01, AX-03]
- **VDI-13-R09** · Never · stage: captions — Captions over other text. Check: Gate: clearance. [AX ax-gr4: #2]
- **VDI-13-R10** · Never · stage: audio — Over-processed voice (gates, pumping, clicks). Check: Blind A/B. [AX ax-gr4: blind A/B]
- **VDI-13-R11** · Never · stage: pickups — Ungraded, mismatched pickups. Check: Gate: skin dE; level step. [AX ax-v5: T3]
- **VDI-13-R12** · Never · stage: screen — PII or plan walls on screen. Check: Gate: PII sweep. [AX ax-v5: AX-01 email]
- **VDI-13-R13** · Never · stage: review — Trusting a transcript-only AI review. Check: Use a reviewer that ingests the video; verify claims. [AX lessons-001: 5.1]
