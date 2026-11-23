---
id: VDI-05-KNOWLEDGE
title: "Editing and pacing (cuts, holds, joins, endings, layout churn): knowledge"
topic: 05_Editing_and_Pacing
status: Seed
last_updated: 2026-11-23
---

# 05_Editing_and_Pacing — knowledge

# Principles

## 1. Measure the render, not the plan

The v4 editor's gate computed holds, cap heights and clean endings from the plan and passed 22/22; the files had 19 blocking defects. [AX ax-v5: gate section] [AX ax-qa-v4]

## 2. Picture and sound cut together

Picture cut at the audio join and the shot mark landed 2-3 frames later, so the zoom reset twice: a 2-3 frame flash at the hook/intro join in AX-01..04. [AX ax-v5: T2] [AX ax-reviewer: picture]

## 3. Fade after the consonant, not before

Cut lists ended a piece 0.17 s after the last 10 ms frame above -38 dBFS, then faded 60 ms; quiet final /s/, /ts/, /st/ fell below that and were cut. [AX ax-v5: T1]

## 4. Shorts loop

On a looping feed an ending 0.13 s after the last word sounds chopped. [AX ax-gr4: #3]

# Patterns

## VDI-05-P01 Join snapping

Picture cut points that fall within 0.15 s of an audio join are moved onto the join. [AX ax-v5: T2]

## VDI-05-P02 Pre-lap

The zoom or screen arrives slightly before the word that describes it, so the hold starts on the word. [AX lessons-001: 4 table]

## VDI-05-P03 Looped ending

Last word complete, then 0.6-0.8 s of room tone decaying to the loop point. [AX ax-gr4: #3]

# Anti-patterns

| id | Anti-pattern | How it shows | Fix | Evidence |
|---|---|---|---|---|
| VDI-05-A01 | Flash shot at the hook join | 2-3 frame shot as the zoom resets. | Snap to the join. | [AX ax-v5: T2] |
| VDI-05-A02 | Chopped ending | File ends ~0.1 s after the last word. | 0.6-0.8 s hold. | [AX ax-gr4: #3] |
| VDI-05-A03 | Pan across the evidence | Line readable only while moving. | Narrower capture, still frame. | [AX ax-v5: AX-04 27.3-29.5 s] |
| VDI-05-A04 | Layout churn | Split -> full -> split inside two seconds. | One layout per beat. | [AX ax-editnotes: v4 item 9] |

# Implementation notes

## Shot detection used by the gate

Decode at 180x320, per-pixel luma change > 12 levels, a change event when > 35% of a region changes, consecutive changed frames merged as one transition; a shot is the time between settled transitions. Regions: whole, upper half, lower half. vdi/release.py check_shots.

## Word-ending check

Align the final to each source by cross-correlation; at each segment end find the last frame where the final still reproduces the source (full band within 6 dB and >= 3.5 kHz within 9 dB); measure how long the source's speech continues past it before a >= 130 ms pause. >= 60 ms lost = FAIL. check_word_endings.

## Ending hold

Last 10 ms frame within 28 dB of speech level (full band or >= 3.5 kHz) to file end; 0.6-1.0 s passes. check_ending.

## Gate checks that cover this topic

- **shot lengths**: check_shots
- **black or blank panels**: check_blank
- **word endings**: check_word_endings
- **ending hold**: check_ending
- **inter-sentence gaps**: check_sentence_gaps
- **evidence lines**: check_evidence

# Glossary

- **Flash shot**: A shot of 1-3 frames, usually from a mistimed cut or a zoom reset.
- **Pre-lap**: Bringing picture in slightly before the matching sound.
- **Layout churn**: Switching between split and full-frame layouts too often.
- **Tail**: The decay of a word or room tone after the last voiced sound.
