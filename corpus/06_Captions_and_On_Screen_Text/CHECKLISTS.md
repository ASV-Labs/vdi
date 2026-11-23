---
id: VDI-06-CHECKLISTS
title: "Captions and on-screen text: checklists"
topic: 06_Captions_and_On_Screen_Text
status: Seed
last_updated: 2026-11-23
---

# 06_Captions_and_On_Screen_Text — checklists

# Build checklist

## Stage: captions

- [ ] Caption the final audio verbatim… (VDI-06-R01)
- [ ] Keep captions inside the safe area… (VDI-06-R02)
- [ ] Keep >= 48 px between captions and any other on-screen text (lower thirds, end cards, screen lines) (VDI-06-R03)
- [ ] Put nothing behind captions but a plain panel or the face/torso (VDI-06-R04)
- [ ] Show each caption within ~0.3 s of its word (VDI-06-R05)
- [ ] Keep captions to two short lines… (VDI-06-R06)
- [ ] Never generate captions from the plan text aligned to word timings… (VDI-06-R07)
- [ ] Never trust an AI reviewer's quoted caption misspellings without checking frames… (VDI-06-R08)
- [ ] Prefer captions at a reading load the platform recommends… (VDI-06-R09)

# Design review checklist

- [ ] Do captions match the final audio word for word?
- [ ] Are captions in the safe area and clear of other text?
- [ ] Are proper nouns spelled exactly?
- [ ] Was any caption generated from the script?

## Rules these questions test

- VDI-06-R01 (Always, captions): Caption the final audio verbatim…
- VDI-06-R02 (Always, captions): Keep captions inside the safe area…
- VDI-06-R03 (Always, captions): Keep >= 48 px between captions and any other on-screen text (lower thirds, end cards, screen lines)
- VDI-06-R04 (Always, captions): Put nothing behind captions but a plain panel or the face/torso
- VDI-06-R05 (Always, captions): Show each caption within ~0.3 s of its word
- VDI-06-R06 (Always, captions): Keep captions to two short lines…
- VDI-06-R07 (Never, captions): Never generate captions from the plan text aligned to word timings…
- VDI-06-R08 (Never, captions): Never trust an AI reviewer's quoted caption misspellings without checking frames…
- VDI-06-R09 (Prefer, captions): Prefer captions at a reading load the platform recommends…

# QA checklist

- [ ] **captions match the final audio**: check_captions
- [ ] **caption safe area**: check_captions
- [ ] **caption clearance**: check_caption_clearance
- [ ] **caption timing**: check_captions (WARN)

- Font legibility issues such as 0 vs O.
- Layout churn and pacing feel.

# Red flags

- Caption text identical to the script where the audio differs
- Caption touching a lower third or URL
- A tolerance list of misheard words
- Captions in the bottom 20%

## Matching anti-patterns

- VDI-06-A01 Script captions: Caption the audio.
- VDI-06-A02 Caption on the URL: >= 48 px clearance; move one of them.
- VDI-06-A03 Tolerance list: No tolerance list; proper nouns go to a human listen.

# Evaluation template

- **Video:** <file>

| # | Criterion | Severity | Result (PASS/FAIL) | Evidence (timestamp, frame, measurement) |
|---|---|---|---|---|
| 1 | Captions equal the audio | blocker | | |
| 2 | Safe area | blocker | | |
| 3 | >= 48 px clearance | major | | |
| 4 | Timing within ~0.3 s | minor | | |
| 5 | Proper nouns exact | major | | |
