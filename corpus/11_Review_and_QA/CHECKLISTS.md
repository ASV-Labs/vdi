---
id: VDI-11-CHECKLISTS
title: "Review and QA (AI review limits, independent review, blind A/B, gate design): checklists"
topic: 11_Review_and_QA
status: Seed
last_updated: 2026-11-23
---

# 11_Review_and_QA — checklists

# Build checklist

## Stage: review

- [ ] No 'final' without… (VDI-11-R01)
- [ ] Every gate check reads the rendered mp4 (OCR of frames, envelopes vs source, shot detection, colour)… (VDI-11-R02)
- [ ] No tolerance lists except owner-accepted spoken deviations… (VDI-11-R03)
- [ ] Run the gate on known-bad files and keep the result with the gate… (VDI-11-R04)
- [ ] Use an AI reviewer that receives the video itself (AX… (VDI-11-R05)
- [ ] Verify every AI review claim against frames and audio before acting (VDI-11-R06)
- [ ] Use a blind A/B (labels hidden) to choose between audio chains… (VDI-11-R07)
- [ ] Never let the editor's own gate be the only gate (VDI-11-R08)
- [ ] Never use AI-review timestamps without re-checking them against the file's own word timings (VDI-11-R09)

# Design review checklist

- [ ] Did the gate run on the rendered file and exit 0?
- [ ] Has an independent reviewer said READY?
- [ ] Has the owner said so himself?
- [ ] Were AI review claims verified against frames?

## Rules these questions test

- VDI-11-R01 (Always, review): No 'final' without…
- VDI-11-R02 (Always, review): Every gate check reads the rendered mp4 (OCR of frames, envelopes vs source, shot detection, colour)…
- VDI-11-R03 (Always, review): No tolerance lists except owner-accepted spoken deviations…
- VDI-11-R04 (Always, review): Run the gate on known-bad files and keep the result with the gate…
- VDI-11-R05 (Always, review): Use an AI reviewer that receives the video itself (AX…
- VDI-11-R06 (Always, review): Verify every AI review claim against frames and audio before acting
- VDI-11-R07 (Always, review): Use a blind A/B (labels hidden) to choose between audio chains…
- VDI-11-R08 (Never, review): Never let the editor's own gate be the only gate
- VDI-11-R09 (Never, review): Never use AI-review timestamps without re-checking them against the file's own word timings

# QA checklist

- [ ] **all gate checks**: vdi/release.py
- [ ] **independent review**: Human or separate agent; not the editor
- [ ] **owner OK**: Recorded in release notes

- Font legibility issues such as 0 vs O.
- Layout churn and pacing feel.

# Red flags

- A gate that never fails
- Tolerance lists
- Reviewer quotes that do not match frames
- 'Final' without the owner's OK

## Matching anti-patterns

- VDI-11-A01 Self-grading gate: Measure the mp4.
- VDI-11-A02 Transcript-only AI review: Attach the video in a tool that ingests it.
- VDI-11-A03 One-model ASR: Both models must agree.

# Evaluation template

- **Video:** <file>

| # | Criterion | Severity | Result (PASS/FAIL) | Evidence (timestamp, frame, measurement) |
|---|---|---|---|---|
| 1 | Gate PASS on render | blocker | | |
| 2 | Independent READY | blocker | | |
| 3 | Owner OK | blocker | | |
| 4 | AI claims verified | major | | |
