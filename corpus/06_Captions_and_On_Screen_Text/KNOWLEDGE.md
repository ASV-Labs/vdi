---
id: VDI-06-KNOWLEDGE
title: "Captions and on-screen text: knowledge"
topic: 06_Captions_and_On_Screen_Text
status: Seed
last_updated: 2026-11-23
---

# 06_Captions_and_On_Screen_Text — knowledge

# Principles

## 1. Captions say what was said

Captions that followed the script were wrong where he ad-libbed ('I've built' vs said 'I build'; 'the ledger' vs said 'a ledger'). [AX lessons-001: 1.3] [AX ax-v5: AX-01 6.1 s, AX-03 32.9 s]

## 2. Captions own a band

Captions over terminal lines, pages, cards and lower thirds made both unreadable (AX-01 'wins and the' on the end-card URL, AX-02 'my account' on the @ASaltyVet lower third, AX-03 'for updates.' on the URL). [AX ax-gr4: #2]

## 3. A word is heard only if two models agree

The v4 gate counted a word as heard if one model heard it once; real defects ('in plain', 'faceplants', 'the ledger') hid behind that and a tolerance list. [AX ax-v5: gate section] [AX lessons-001: 5.3]

# Patterns

## VDI-06-P01 Caption band

A fixed horizontal band (on AX, y about 1000-1380 of 1920) where only captions live, with a plain plate on split layouts. [AX ax-editnotes: v4 item 10]

## VDI-06-P02 Verbatim + accepted list

Captions from the audio; the owner reviews the list of script deviations. [AX lessons-001: 1.3]

## VDI-06-P03 Two-model agreement

Transcribe the final with small.en and medium.en; only words both hear count as confirmed. [AX lessons-001: 5.3]

# Anti-patterns

| id | Anti-pattern | How it shows | Fix | Evidence |
|---|---|---|---|---|
| VDI-06-A01 | Script captions | Captions copied from the script over an ad-libbed line. | Caption the audio. | [AX ax-v5: AX-01 6.1 s] |
| VDI-06-A02 | Caption on the URL | Caption overlaps the end card or lower third. | >= 48 px clearance; move one of them. | [AX ax-gr4: #2] |
| VDI-06-A03 | Tolerance list | Known misheard words excused by the gate. | No tolerance list; proper nouns go to a human listen. | [AX ax-qa-v4: asr_tolerance] [AX ax-v5: gate section] |

# Implementation notes

## Caption OCR in the gate

OCR the caption band of every frame at 10 fps on a bright-pixel mask; a band row is a caption only if at least half its words match words spoken within +-1.5 s; words must be read in >= 40% of an event's frames (removes OCR garble but keeps a stable wrong word). vdi/release.py caption_events.

## Two models

faster-whisper small.en and medium.en, int8 on CPU, audio passed as a float32 numpy array (the av decode path is broken in this environment). [AX ax-reviewer: tr.py]

## Clearance

Whole-frame OCR rows (conf >= 60, >= 4 alphanumerics) within 48 px of a caption box, excluding the caption's own words, in >= 3 frames of the event.

## Gate checks that cover this topic

- **captions match the final audio**: check_captions
- **caption safe area**: check_captions
- **caption clearance**: check_caption_clearance
- **caption timing**: check_captions (WARN)

# Glossary

- **Caption band**: The horizontal strip reserved for captions.
- **Safe area**: The part of the frame not covered by platform UI.
- **Agreed word**: A word both ASR models transcribe identically at the same position.
- **Lower third**: Name/title text in the lower part of the frame.
