---
id: VDI-05-CHECKLISTS
title: "Editing and pacing (cuts, holds, joins, endings, layout churn): checklists"
topic: 05_Editing_and_Pacing
status: Seed
last_updated: 2026-11-23
---

# 05_Editing_and_Pacing — checklists

# Build checklist

## Stage: edit

- [ ] No shot shorter than 12 frames… (VDI-05-R01)
- [ ] Snap any shot start within 0.15 s of an audio join to the join (VDI-05-R02)
- [ ] Assign frames to shots and segments by frame index (or compare with a small epsilon after the frame… (VDI-05-R03)
- [ ] A screen that takes over at a voice-over piece starts exactly with the piece… (VDI-05-R04)
- [ ] Never show a black or blank panel for more than one frame… (VDI-05-R05)
- [ ] Detect word ends on a >= 3.5 kHz envelope as well as full band, each with a threshold relative to… (VDI-05-R06)
- [ ] End every short 0.6-0.8 s after the last word, audio decaying into room tone (VDI-05-R07)
- [ ] Keep at least 0.12 s of pause between sentences, and no longer than natural (VDI-05-R08)
- [ ] Hold each evidence line whole, still (drift < 6 px) and >= 28 px for >= 1.6 s… (VDI-05-R09)
- [ ] Do not flip split <-> full frame within ~2 s… (VDI-05-R10)
- [ ] Never let a pause-trim rule cut into a soft word… (VDI-05-R11)
- [ ] Prefer holding a screen through a line and cutting to a pickup at its join over a 12-frame face… (VDI-05-R12)

# Design review checklist

- [ ] Any shot under 12 frames?
- [ ] Any black panel?
- [ ] Does every evidence line hold whole and still for 1.6 s?
- [ ] Does the short end 0.6-0.8 s after the last word?
- [ ] Any layout flip inside 2 s?

## Rules these questions test

- VDI-05-R01 (Always, edit): No shot shorter than 12 frames…
- VDI-05-R02 (Always, edit): Snap any shot start within 0.15 s of an audio join to the join
- VDI-05-R03 (Always, edit): Assign frames to shots and segments by frame index (or compare with a small epsilon after the frame…
- VDI-05-R04 (Always, edit): A screen that takes over at a voice-over piece starts exactly with the piece…
- VDI-05-R05 (Always, edit): Never show a black or blank panel for more than one frame…
- VDI-05-R06 (Always, edit): Detect word ends on a >= 3.5 kHz envelope as well as full band, each with a threshold relative to…
- VDI-05-R07 (Always, edit): End every short 0.6-0.8 s after the last word, audio decaying into room tone
- VDI-05-R08 (Always, edit): Keep at least 0.12 s of pause between sentences, and no longer than natural
- VDI-05-R09 (Always, edit): Hold each evidence line whole, still (drift < 6 px) and >= 28 px for >= 1.6 s…
- VDI-05-R10 (Never, edit): Do not flip split <-> full frame within ~2 s…
- VDI-05-R11 (Never, edit): Never let a pause-trim rule cut into a soft word…
- VDI-05-R12 (Prefer, edit): Prefer holding a screen through a line and cutting to a pickup at its join over a 12-frame face…

# QA checklist

- [ ] **shot lengths**: check_shots
- [ ] **black or blank panels**: check_blank
- [ ] **word endings**: check_word_endings
- [ ] **ending hold**: check_ending
- [ ] **inter-sentence gaps**: check_sentence_gaps
- [ ] **evidence lines**: check_evidence

- Font legibility issues such as 0 vs O.
- Layout churn and pacing feel.

# Red flags

- Zoom resets right after an audio join
- Ending under 0.3 s after the last word
- A screen line that only reads while panning
- Pause-trim settings that cut soft words

## Matching anti-patterns

- VDI-05-A01 Flash shot at the hook join: Snap to the join.
- VDI-05-A02 Chopped ending: 0.6-0.8 s hold.
- VDI-05-A03 Pan across the evidence: Narrower capture, still frame.
- VDI-05-A04 Layout churn: One layout per beat.

# Evaluation template

- **Video:** <file>

| # | Criterion | Severity | Result (PASS/FAIL) | Evidence (timestamp, frame, measurement) |
|---|---|---|---|---|
| 1 | No shot < 12 frames | blocker | | |
| 2 | No black panel > 1 frame | blocker | | |
| 3 | No word tail lost >= 60 ms | blocker | | |
| 4 | Ending hold 0.6-1.0 s | blocker | | |
| 5 | Sentence gaps >= 0.12 s | major | | |
| 6 | No layout churn < 2 s | minor | | |
