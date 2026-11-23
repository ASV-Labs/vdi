---
id: VDI-04-CHECKLISTS
title: "Screen capture and product demos: checklists"
topic: 04_Screen_Capture_and_Demos
status: Seed
last_updated: 2026-11-23
---

# 04_Screen_Capture_and_Demos — checklists

# Build checklist

## Stage: screen

- [ ] Use only real runs and live pages captured that day… (VDI-04-R01)
- [ ] Record each beat's run id… (VDI-04-R02)
- [ ] Record terminals narrow (about 40 columns), or re-render the saved asciicast narrow… (VDI-04-R03)
- [ ] When re-rendering a cast at fewer columns, strip only the readline wrap pairs, note it in the edit… (VDI-04-R04)
- [ ] Look at the first and last frame of every clip range before using it… (VDI-04-R05)
- [ ] Capture web pages at the CSS width where the needed line reaches 28 px inside x <= 950 (about… (VDI-04-R06)
- [ ] Use the approved test account… (VDI-04-R07)
- [ ] Cut around PLAN_REQUIRED and RATE_LIMITED lines unless the owner wants them shown (VDI-04-R08)
- [ ] Label sample work on screen ('This is a sample page, not a customer site.') inside the safe area… (VDI-04-R09)
- [ ] Mask the capture to whole rows or blocks around the evidence line (a window on the page's own… (VDI-04-R10)
- [ ] Never intercut two runs inside one claim without a visible label, even if both runs are real (VDI-04-R11)
- [ ] Never pan across a line while it is being read… (VDI-04-R12)

# Design review checklist

- [ ] Is every screen line from a real run captured that day?
- [ ] Do adjacent beats in one claim share a run id?
- [ ] Is every evidence line whole and still in frame?
- [ ] Any email, code, token or plan wall visible?

## Rules these questions test

- VDI-04-R01 (Always, screen): Use only real runs and live pages captured that day…
- VDI-04-R02 (Always, screen): Record each beat's run id…
- VDI-04-R03 (Always, screen): Record terminals narrow (about 40 columns), or re-render the saved asciicast narrow…
- VDI-04-R04 (Always, screen): When re-rendering a cast at fewer columns, strip only the readline wrap pairs, note it in the edit…
- VDI-04-R05 (Always, screen): Look at the first and last frame of every clip range before using it…
- VDI-04-R06 (Always, screen): Capture web pages at the CSS width where the needed line reaches 28 px inside x <= 950 (about…
- VDI-04-R07 (Always, screen): Use the approved test account…
- VDI-04-R08 (Always, screen): Cut around PLAN_REQUIRED and RATE_LIMITED lines unless the owner wants them shown
- VDI-04-R09 (Always, screen): Label sample work on screen ('This is a sample page, not a customer site.') inside the safe area…
- VDI-04-R10 (Always, screen): Mask the capture to whole rows or blocks around the evidence line (a window on the page's own…
- VDI-04-R11 (Never, screen): Never intercut two runs inside one claim without a visible label, even if both runs are real
- VDI-04-R12 (Never, screen): Never pan across a line while it is being read…

# QA checklist

- [ ] **evidence lines**: Gate check_evidence: whole, still, >= 28 px, >= 1.6 s.
- [ ] **run ids and source labels**: Gate check_runs.
- [ ] **PII and plan-wall sweep**: Gate check_pii.

- Font legibility issues such as 0 vs O.
- Layout churn and pacing feel.

# Red flags

- Line cut at the frame edge
- Two different model names on screen inside one claim
- A pan across the line being read
- Any '@' followed by a domain on screen

## Matching anti-patterns

- VDI-04-A01 Wide terminal + zoom: Narrow terminal, verbatim re-render.
- VDI-04-A02 Mixed runs: One run per claim or a visible label.
- VDI-04-A03 Masked email on screen: Blur the whole line.
- VDI-04-A04 Plan wall in the cut: Cut around them.

# Evaluation template

- **Video:** <file>

| # | Criterion | Severity | Result (PASS/FAIL) | Evidence (timestamp, frame, measurement) |
|---|---|---|---|---|
| 1 | All screen content from real runs | blocker | | |
| 2 | One run per claim or visible label | blocker | | |
| 3 | Evidence whole, still, >= 28 px, >= 1.6 s | blocker | | |
| 4 | No PII or plan walls | blocker | | |
