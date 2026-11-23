---
id: VDI-13-KNOWLEDGE
title: "Anti-patterns: knowledge"
topic: 13_Anti_Patterns
status: Seed
last_updated: 2026-11-23
---

# 13_Anti_Patterns — knowledge

# Principles

## 1. Every anti-pattern here shipped to at least one review round

Each entry came from a real AX defect. [AX lessons-001: intro]

## 2. Name it, then measure it

An anti-pattern is only useful to an agent if it has a detection: a gate check, a lint rule or a review question. [AX ax-v5: gate section]

# Patterns

## VDI-13-P01 Anti-pattern card

Name / how it shows / rule / detection / evidence. Each card links to the topic that owns the fix.

## VDI-13-P02 Gate coverage map

For each anti-pattern, whether the gate detects it (yes / partly / no). See implementation-notes.md.

# Anti-patterns

| id | Anti-pattern | How it shows | Fix | Evidence |
|---|---|---|---|---|
| VDI-13-A01 | Self-grading gate | PASS 22/22 on known-bad files. | Measure the render; prove on known-bad files. | [AX ax-qa-v4] |
| VDI-13-A02 | Truncated board | Lines end mid-sentence. | Read the script. | [AX ax-boards] |
| VDI-13-A03 | Stitched runs | Prompt and result from different runs. | One run per claim or a label. | [AX ax-v5: AX-01, AX-04] |
| VDI-13-A04 | Cropped evidence | Line cut at frame edge. | Narrow capture. | [AX ax-gr4: #1] |
| VDI-13-A05 | Flash shot | 2-3 frame shot. | Snap to join. | [AX ax-v5: T2] |
| VDI-13-A06 | Cut tails | /s/ /ts/ /st/ lost. | HF envelope; fade after consonant. | [AX ax-v5: T1] |
| VDI-13-A07 | Chopped ending | No hold after the last word. | 0.6-0.8 s hold. | [AX ax-gr4: #3] |
| VDI-13-A08 | Script captions | Caption differs from audio. | Caption the audio. | [AX ax-v5: AX-01 6.1 s] |
| VDI-13-A09 | Caption collisions | Caption over URL/lower third. | Clearance. | [AX ax-gr4: #2] |
| VDI-13-A10 | Plastic face | Halo, smeared skin. | Lighter processing, better capture. | [AX ax-gr4: #5] |
| VDI-13-A11 | Mismatched pickups | dE 6.3-9.6 at cuts. | Same setup; grade to take. | [AX ax-v5: T3] |
| VDI-13-A12 | Join holes | Digital zero at joins. | Room tone. | [AX ax-v5: AX-05] |
| VDI-13-A13 | PII on screen | Masked email visible. | Blur; OCR sweep. | [AX ax-v5: AX-01] |
| VDI-13-A14 | Transcript-only AI review | Invented misspellings. | Video-ingesting reviewer; verify. | [AX ax-gr3] |

# Implementation notes

## Gate coverage (from the v4 proof)

Detected by the gate: cropped/moving/small evidence, flash shots, black panels, cut tails, chopped endings, rushed joins, level steps, dropouts, script deviations, caption text vs audio, caption clearance, PII/plan walls, unlabeled run changes, pickup grade jumps. Not detected: plastic face/halo, voice naturalness, caption over the face in a transition, 0 vs O in a font, layout churn, truth of a claim. Partly: caption timing (WARN only). [AX vdi-gate-proof]

## Gate checks that cover this topic

- **gate**: vdi/release.py covers most entries; see implementation-notes.md for gaps

# Glossary

- **Anti-pattern**: A recurring failure with a known fix.
- **Detection**: How the failure is found: gate check, lint, or review question.
