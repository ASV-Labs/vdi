---
id: VDI-12-RULES
title: "Claims and honesty: agent rules"
topic: 12_Claims_and_Honesty
status: Seed
last_updated: 2026-11-23
---

# 12_Claims_and_Honesty — agent rules

## Always

- **VDI-12-R01** · Always · stage: script — For every spoken claim, list the exact screen line that proves it and the run it comes from, before recording. Check: Manifest evidence_beats cover every claim. [AX lessons-001: 1.4]
- **VDI-12-R02** · Always · stage: screen — Every line, UI and result on screen comes from a real run or live page captured that day; save verbatim outputs with a README. Check: Run README per screen file. [AX lessons-001: 3.1]
- **VDI-12-R03** · Always · stage: screen — When a beat shows a different run (for example a repo's demo), put a visible source label on it inside the safe area and outside the caption band. Check: Gate: source label readable by OCR. [AX ax-v5: AX-04 graph label]
- **VDI-12-R04** · Always · stage: screen — Show the licence, price or status on screen when it is said (for example the repo's LICENSE line on 'MIT License'). Check: Evidence beat for each such claim. [AX ax-v5: AX-04 MIT]
- **VDI-12-R05** · Always · stage: review — List every spoken deviation that changes a claim for the owner (for example 'a design library that calls over MCP' inverts who calls whom). Check: Owner-accepted list in the manifest. [AX ax-reviewer: script vs spoken]

## Never

- **VDI-12-R06** · Never · stage: script — Never promise what the product does not offer (AX-03: 'Do not promise a seat'; Alstead is an invite-only alpha). Check: Script review against the product page. [AX ax-scripts: AX-03 CTA]
- **VDI-12-R07** · Never · stage: review — Never call anything final, ready or reviewed without the gate, an independent review and the owner's OK; a status of Draft or Seed until then. Check: Release record. [AX lessons-001: 6]
