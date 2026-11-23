---
id: VDI-01-CHECKLISTS
title: "Scripting and boards: checklists"
topic: 01_Scripting_and_Boards
status: Seed
last_updated: 2026-11-23
---

# 01_Scripting_and_Boards — checklists

# Build checklist

## Stage: script

- [ ] Read from the full script, never from a board that can truncate, until the board tool is proven not… (VDI-01-R01)
- [ ] One SAY line per beat, 70 characters or less, so a board that wraps and cuts at three lines cannot… (VDI-01-R02)
- [ ] Keep each sentence to about 12 words or fewer and one idea per beat (VDI-01-R03)
- [ ] Give every beat a SHOW line that names the exact screen line, page element or run output that… (VDI-01-R04)
- [ ] Write a claim list before recording… (VDI-01-R05)
- [ ] Design the demo so the claimed behaviour is likely to happen on camera (for 'fixes what fails', a… (VDI-01-R06)
- [ ] Budget 1.6-2 s of picture per on-screen proof line… (VDI-01-R07)
- [ ] Keep a proper-noun list (names, products, handles) for captions and for checking by ear (VDI-01-R08)
- [ ] Never write a line whose meaning flips if one word is ad-libbed (for example 'a design library your… (VDI-01-R09)
- [ ] Prefer sentences that end on the key word, so a cut or a fade never lands on the payoff (VDI-01-R10)

## Stage: shoot

- [ ] Have the performer say each line twice with a pause between… (VDI-01-R11)

# Design review checklist

- [ ] Does every SAY that makes a claim have a SHOW naming the proof line?
- [ ] Is any SAY long enough that a board might truncate it?
- [ ] Would any likely ad-lib invert the meaning of a line?
- [ ] Is there a proper-noun list?

## Rules these questions test

- VDI-01-R01 (Always, script): Read from the full script, never from a board that can truncate, until the board tool is proven not…
- VDI-01-R02 (Always, script): One SAY line per beat, 70 characters or less, so a board that wraps and cuts at three lines cannot…
- VDI-01-R03 (Always, script): Keep each sentence to about 12 words or fewer and one idea per beat
- VDI-01-R04 (Always, script): Give every beat a SHOW line that names the exact screen line, page element or run output that…
- VDI-01-R05 (Always, script): Write a claim list before recording…
- VDI-01-R06 (Always, script): Design the demo so the claimed behaviour is likely to happen on camera (for 'fixes what fails', a…
- VDI-01-R07 (Always, script): Budget 1.6-2 s of picture per on-screen proof line…
- VDI-01-R08 (Always, script): Keep a proper-noun list (names, products, handles) for captions and for checking by ear
- VDI-01-R09 (Never, script): Never write a line whose meaning flips if one word is ad-libbed (for example 'a design library your…
- VDI-01-R10 (Prefer, script): Prefer sentences that end on the key word, so a cut or a fade never lands on the payoff
- VDI-01-R11 (Prefer, shoot): Have the performer say each line twice with a pause between…

# QA checklist

- [ ] **spoken words vs script**: Every difference between the transcript (both ASR models agreeing) and the script is on the owner-accepted list.

- Font legibility issues such as 0 vs O.
- Layout churn and pacing feel.

# Red flags

- An ellipsis on a board SAY line
- A SAY beat over 70 characters
- A claim beat with SHOW: 'the app' or 'the homepage' only
- A sentence over ~20 words
- No claim ledger before recording

## Matching anti-patterns

- VDI-01-A01 Truncated board: Read from the script; diff board vs script.
- VDI-01-A02 Claim with no screen: Add a SHOW line naming the proof, or cut the claim.
- VDI-01-A03 Silent script 'fixes': Caption the audio; list the deviation for the owner.

# Evaluation template

- **Video:** <file>

| # | Criterion | Severity | Result (PASS/FAIL) | Evidence (timestamp, frame, measurement) |
|---|---|---|---|---|
| 1 | Board SAY equals script SAY | blocker | | |
| 2 | Each claim has a SHOW proof line | blocker | | |
| 3 | Sentences <= ~12 words | minor | | |
| 4 | Proper-noun list present | major | | |
