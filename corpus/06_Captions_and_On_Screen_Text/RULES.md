---
id: VDI-06-RULES
title: "Captions and on-screen text: agent rules"
topic: 06_Captions_and_On_Screen_Text
status: Seed
last_updated: 2026-11-23
---

# 06_Captions_and_On_Screen_Text — agent rules

## Always

- **VDI-06-R01** · Always · stage: captions — Caption the final audio verbatim; never caption words that were not said; never 'fix' an ad-lib silently. Check: Gate: captions vs transcript (OCR of frames; small.en and medium.en must agree). [AX lessons-001: 1.3] [AX ax-v5: AX-01 6.1 s, AX-03 32.9 s]
- **VDI-06-R02** · Always · stage: captions — Keep captions inside the safe area: top 8%, bottom 20%, right 12% clear (AX house values for 1080x1920). Check: Gate: caption safe area. [AX lessons-001: 4 table] House values [UNVERIFIED]; platform safe zones in 09_Platform_Formats
- **VDI-06-R03** · Always · stage: captions — Keep >= 48 px between captions and any other on-screen text (lower thirds, end cards, screen lines). Check: Gate: caption clearance from other text. [AX ax-gr4: #2] [AX lessons-001: 4 table] Value [UNVERIFIED]
- **VDI-06-R04** · Always · stage: captions — Put nothing behind captions but a plain panel or the face/torso. Check: Review frames on split and full layouts. [AX lessons-001: 4 table] [AX ax-gr3: #2]
- **VDI-06-R05** · Always · stage: captions — Show each caption within ~0.3 s of its word. Check: Gate: caption timing (WARN only; OCR timing is +-0.2 s on animated captions). [AX ax-v5: AX-04 33.1 s 'or inferred.' 0.42 s late] Value [UNVERIFIED]
- **VDI-06-R06** · Always · stage: captions — Keep captions to two short lines; spell proper nouns exactly and check them by ear. Check: Proper-noun list in the manifest; gate lists them for a human listen. [AX ax-gr2: #1] [AX lessons-001: 5.6]

## Never

- **VDI-06-R07** · Never · stage: captions — Never generate captions from the plan text aligned to word timings; generate from the final audio and correct by ear. Check: Caption source recorded in the edit notes. [AX ax-editnotes: v4 'captions are now generated from the plan text'] [AX ax-v5: gate section]
- **VDI-06-R08** · Never · stage: captions — Never trust an AI reviewer's quoted caption misspellings without checking frames; they were its own ASR ('FACEPLATE', 'NOOSE RESEARCH', 'ASV LADS'). Check: Check frames at full resolution. [AX ax-gr3: FALSE list] [AX lessons-001: 5.1]

## Prefer

- **VDI-06-R09** · Prefer · stage: captions — Prefer captions at a reading load the platform recommends; TikTok's ads guidance suggests 5-10 words per second for text. Check: Count words per caption event / duration. [SRC tiktok-creative]
