---
id: VDI-12-CHECKLISTS
title: "Claims and honesty: checklists"
topic: 12_Claims_and_Honesty
status: Seed
last_updated: 2026-11-23
---

# 12_Claims_and_Honesty — checklists

# Build checklist

## Stage: script

- [ ] For every spoken claim, list the exact screen line that proves it and the run it comes from, before… (VDI-12-R01)
- [ ] Never promise what the product does not offer (AX-03… (VDI-12-R06)

## Stage: screen

- [ ] Every line, UI and result on screen comes from a real run or live page captured that day… (VDI-12-R02)
- [ ] When a beat shows a different run (for example a repo's demo), put a visible source label on it… (VDI-12-R03)
- [ ] Show the licence, price or status on screen when it is said (for example the repo's LICENSE line on… (VDI-12-R04)

## Stage: review

- [ ] List every spoken deviation that changes a claim for the owner (for example 'a design library that… (VDI-12-R05)
- [ ] Never call anything final, ready or reviewed without the gate, an independent review and the… (VDI-12-R07)

# Design review checklist

- [ ] Is every claim proven on screen while it is said?
- [ ] Does any claim mix runs?
- [ ] Are samples labelled?
- [ ] Does any ad-lib change a claim?

## Rules these questions test

- VDI-12-R01 (Always, script): For every spoken claim, list the exact screen line that proves it and the run it comes from, before…
- VDI-12-R02 (Always, screen): Every line, UI and result on screen comes from a real run or live page captured that day…
- VDI-12-R03 (Always, screen): When a beat shows a different run (for example a repo's demo), put a visible source label on it…
- VDI-12-R04 (Always, screen): Show the licence, price or status on screen when it is said (for example the repo's LICENSE line on…
- VDI-12-R05 (Always, review): List every spoken deviation that changes a claim for the owner (for example 'a design library that…
- VDI-12-R06 (Never, script): Never promise what the product does not offer (AX-03…
- VDI-12-R07 (Never, review): Never call anything final, ready or reviewed without the gate, an independent review and the…

# QA checklist

- [ ] **evidence lines**: check_evidence
- [ ] **run ids and source labels**: check_runs
- [ ] **spoken words vs script**: check_script

- Font legibility issues such as 0 vs O.
- Layout churn and pacing feel.

# Red flags

- A spoken number, licence or status with no screen
- Two model names in one claim
- Unlabelled sample work
- 'Final' in a file name before the owner's OK

## Matching anti-patterns

- VDI-12-A01 Spoken-only claim: Evidence beat or cut the claim.
- VDI-12-A02 Stitched proof: One run per claim.
- VDI-12-A03 Generated centerpiece: Real footage only.

# Evaluation template

- **Video:** <file>

| # | Criterion | Severity | Result (PASS/FAIL) | Evidence (timestamp, frame, measurement) |
|---|---|---|---|---|
| 1 | Every claim has proof on screen | blocker | | |
| 2 | One run per claim or label | blocker | | |
| 3 | Samples labelled | major | | |
| 4 | Claim-changing ad-libs accepted by owner | blocker | | |
