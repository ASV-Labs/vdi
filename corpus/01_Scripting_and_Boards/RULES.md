---
id: VDI-01-RULES
title: "Scripting and boards: agent rules"
topic: 01_Scripting_and_Boards
status: Seed
last_updated: 2026-11-23
---

# 01_Scripting_and_Boards — agent rules

## Always

- **VDI-01-R01** · Always · stage: script — Read from the full script, never from a board that can truncate, until the board tool is proven not to truncate. After a fix, every board SAY must equal the script SAY character for character. Check: Diff board text against script text before the shoot; any ellipsis on a SAY line stops the shoot. [AX lessons-001: 1.1] [AX ax-boards: all five boards]
- **VDI-01-R02** · Always · stage: script — One SAY line per beat, 70 characters or less, so a board that wraps and cuts at three lines cannot truncate it; split a long beat into 4a/4b/4c instead of writing a longer line. Check: vdi_lint_script fails any beat over 70 characters. [AX lessons-001: 1.1 (rule added Nov 23; OC scripts v3 follow it)] [AX ax-boards: 18 cut lines across five shorts]
- **VDI-01-R03** · Always · stage: script — Keep each sentence to about 12 words or fewer and one idea per beat. Check: vdi_lint_script flags sentences over 12 words. [AX lessons-001: 1.2] Threshold [UNVERIFIED]
- **VDI-01-R04** · Always · stage: script — Give every beat a SHOW line that names the exact screen line, page element or run output that proves it, and where the eye should land. Check: Every SAY containing a product claim has a SHOW naming a real screen line. [AX ax-v5: AX-01 20.1-23.0 s templates] [AX lessons-001: 1.4]
- **VDI-01-R05** · Always · stage: script — Write a claim list before recording: spoken claim -> exact screen line that proves it -> the run it comes from. Check: The manifest's evidence_beats list exists before the edit starts. [AX lessons-001: 1.4]
- **VDI-01-R06** · Always · stage: script — Design the demo so the claimed behaviour is likely to happen on camera (for 'fixes what fails', a run where something actually fails). Check: Rehearse the run once; if the claim did not occur, change the demo or the line. [AX lessons-001: 1.4] [AX ax-screens-agent: AX-01 first run passed 17/17]
- **VDI-01-R07** · Always · stage: script — Budget 1.6-2 s of picture per on-screen proof line; for a fast spoken list, start the first screen on the previous phrase, show one screen with all items, or slow the read. Check: Measured still-and-lit time of each evidence line >= 1.6 s (gate evidence check). [AX lessons-002: 8.7 AX-01 'Guidance, tested templates, design checks.' 4.3 s, 1.3 s per screen]
- **VDI-01-R08** · Always · stage: script — Keep a proper-noun list (names, products, handles) for captions and for checking by ear. Check: The manifest lists proper_nouns; the gate reports them for a human listen. [AX lessons-001: 5.6]

## Never

- **VDI-01-R09** · Never · stage: script — Never write a line whose meaning flips if one word is ad-libbed (for example 'a design library your agent calls' vs 'a library that calls'). Check: Read each line aloud once with likely ad-libs; flag lines where the swap changes who does what. [AX ax-reviewer: AX-01 'that calls over MCP' meaning inverted]

## Prefer

- **VDI-01-R10** · Prefer · stage: script — Prefer sentences that end on the key word, so a cut or a fade never lands on the payoff. Check: Last word of each sentence carries the point. [UNVERIFIED]
- **VDI-01-R11** · Prefer · stage: shoot — Have the performer say each line twice with a pause between; it made cutting and pickups possible. Check: Raw take has two reads of each line. [AX lessons-001: 2.6]
