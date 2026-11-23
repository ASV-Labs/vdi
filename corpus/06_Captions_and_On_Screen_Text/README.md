---
id: VDI-06-README
title: "Captions and on-screen text: overview"
topic: 06_Captions_and_On_Screen_Text
status: Seed
last_updated: 2026-11-23
---

# 06_Captions_and_On_Screen_Text — Captions and on-screen text

Captions transcribe the final audio verbatim, sit in their own band inside the platform safe area, never cover other text, and are checked by OCR against what both ASR models heard.

Stages: captions.

## What this topic covers

- Verbatim captions from the audio
- Caption band, safe area, clearance
- Timing
- Lower thirds and end cards
- Proper nouns
- Reading load

## Related topics

`01_Scripting_and_Boards`, `09_Platform_Formats`, `11_Review_and_QA`, `04_Screen_Capture_and_Demos`

# Overview

## The short version

- **Captions say what was said.** Captions that followed the script were wrong where he ad-libbed ('I've built' vs said 'I build'; 'the ledger' vs said 'a ledger'). [AX lessons-001: 1.3] [AX ax-v5: AX-01 6.1 s, AX-03 32.9 s]
- **Captions own a band.** Captions over terminal lines, pages, cards and lower thirds made both unreadable (AX-01 'wins and the' on the end-card URL, AX-02 'my account' on the @ASaltyVet lower third, AX-03 'for updates.' on the URL). [AX ax-gr4: #2]
- **A word is heard only if two models agree.** The v4 gate counted a word as heard if one model heard it once; real defects ('in plain', 'faceplants', 'the ledger') hid behind that and a tolerance list. [AX ax-v5: gate section] [AX lessons-001: 5.3]

## Where this sits in the workflow

Stages: captions. The rules in `RULES.md` are keyed to these stages, so `vdi_checklist(stage)` and `vdi_brief(...)` in the MCP server can pull them.

# Known gaps

## Research gaps

1. **SEED** - Whether burned-in keyword-coloured captions help or hurt watch time vs plain captions: no data (lessons-001 7).
2. **SEED** - Caption line length and reading speed standards (Netflix, BBC, WCAG) were searched but not fetched this session; see README.md (Known gaps).

## Research seeds (leads not yet used)

- Fetch Netflix and BBC caption guidelines for line length and reading speed.
- Fetch WCAG 1.2.2 for what captions must include.
- A/B kinetic vs plain captions after posting.
