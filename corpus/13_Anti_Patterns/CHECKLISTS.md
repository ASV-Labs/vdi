---
id: VDI-13-CHECKLISTS
title: "Anti-patterns: checklists"
topic: 13_Anti_Patterns
status: Seed
last_updated: 2026-11-23
---

# 13_Anti_Patterns — checklists

# Build checklist

## Stage: script

- [ ] Reading from a truncating board (VDI-13-R02)

## Stage: pickups

- [ ] Ungraded, mismatched pickups (VDI-13-R11)

## Stage: screen

- [ ] Fake or stitched product output (VDI-13-R03)
- [ ] Wide terminal zoomed until lines crop (VDI-13-R04)
- [ ] PII or plan walls on screen (VDI-13-R12)

## Stage: edit

- [ ] Flash shots and black panels at joins (VDI-13-R05)
- [ ] Fades that cut quiet final consonants (VDI-13-R06)
- [ ] Endings that stop on the last word (VDI-13-R07)

## Stage: captions

- [ ] Captions from the script instead of the audio (VDI-13-R08)
- [ ] Captions over other text (VDI-13-R09)

## Stage: audio

- [ ] Over-processed voice (gates, pumping, clicks) (VDI-13-R10)

## Stage: review

- [ ] Self-grading gate… (VDI-13-R01)
- [ ] Trusting a transcript-only AI review (VDI-13-R13)

# Design review checklist

- [ ] Which anti-patterns from this list could apply to this video?
- [ ] Is each one checked by the gate, a lint rule or a named reviewer step?

## Rules these questions test

- VDI-13-R01 (Never, review): Self-grading gate…
- VDI-13-R02 (Never, script): Reading from a truncating board
- VDI-13-R03 (Never, screen): Fake or stitched product output
- VDI-13-R04 (Never, screen): Wide terminal zoomed until lines crop
- VDI-13-R05 (Never, edit): Flash shots and black panels at joins
- VDI-13-R06 (Never, edit): Fades that cut quiet final consonants
- VDI-13-R07 (Never, edit): Endings that stop on the last word
- VDI-13-R08 (Never, captions): Captions from the script instead of the audio
- VDI-13-R09 (Never, captions): Captions over other text
- VDI-13-R10 (Never, audio): Over-processed voice (gates, pumping, clicks)
- VDI-13-R11 (Never, pickups): Ungraded, mismatched pickups
- VDI-13-R12 (Never, screen): PII or plan walls on screen
- VDI-13-R13 (Never, review): Trusting a transcript-only AI review

# QA checklist

- [ ] **gate**: vdi/release.py covers most entries; see implementation-notes.md for gaps

- Font legibility issues such as 0 vs O.
- Layout churn and pacing feel.

# Red flags

- Any item on this list seen in a release candidate

## Matching anti-patterns

- VDI-13-A01 Self-grading gate: Measure the render; prove on known-bad files.
- VDI-13-A02 Truncated board: Read the script.
- VDI-13-A03 Stitched runs: One run per claim or a label.
- VDI-13-A04 Cropped evidence: Narrow capture.
- VDI-13-A05 Flash shot: Snap to join.
- VDI-13-A06 Cut tails: HF envelope; fade after consonant.
- VDI-13-A07 Chopped ending: 0.6-0.8 s hold.
- VDI-13-A08 Script captions: Caption the audio.
- VDI-13-A09 Caption collisions: Clearance.
- VDI-13-A10 Plastic face: Lighter processing, better capture.
- VDI-13-A11 Mismatched pickups: Same setup; grade to take.
- VDI-13-A12 Join holes: Room tone.
- VDI-13-A13 PII on screen: Blur; OCR sweep.
- VDI-13-A14 Transcript-only AI review: Video-ingesting reviewer; verify.

# Evaluation template

- **Video:** <file>

| # | Criterion | Severity | Result (PASS/FAIL) | Evidence (timestamp, frame, measurement) |
|---|---|---|---|---|
| 1 | No listed anti-pattern present | blocker | | |
