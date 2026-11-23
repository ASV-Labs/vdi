---
id: VDI-11-RULES
title: "Review and QA (AI review limits, independent review, blind A/B, gate design): agent rules"
topic: 11_Review_and_QA
status: Seed
last_updated: 2026-11-23
---

# 11_Review_and_QA — agent rules

## Always

- **VDI-11-R01** · Always · stage: review — No 'final' without: (1) the VDI gate passing on the rendered file, (2) an independent review saying READY, (3) the owner's own OK. Check: Release notes record all three. [AX lessons-001: 6 posting hold]
- **VDI-11-R02** · Always · stage: review — Every gate check reads the rendered mp4 (OCR of frames, envelopes vs source, shot detection, colour); nothing is computed from the plan. Check: Code review of the gate; known-bad proof. [AX lessons-001: 5.3] [AX ax-v5: gate section]
- **VDI-11-R03** · Always · stage: review — No tolerance lists except owner-accepted spoken deviations; a word counts as heard only if both ASR models agree. Check: Manifest has no tolerance field. [AX lessons-001: 5.3]
- **VDI-11-R04** · Always · stage: review — Run the gate on known-bad files and keep the result with the gate; record what it catches and what it cannot. Check: docs/release-gate-proof-v4.md exists and is current. [AX lessons-001: 5.3] [AX vdi-gate-proof]
- **VDI-11-R05** · Always · stage: review — Use an AI reviewer that receives the video itself (AX: Google AI Studio with the file attached), at a review copy of 540x960 under 2.9 MB. Check: Reviewer quotes on-screen text exactly. [AX lessons-001: 5.1, 6] [AX ax-gr4]
- **VDI-11-R06** · Always · stage: review — Verify every AI review claim against frames and audio before acting. Check: Each claim marked TRUE/FALSE with evidence. [AX lessons-001: 5.2] [AX ax-gr3] [AX ax-gr4: FALSE list]
- **VDI-11-R07** · Always · stage: review — Use a blind A/B (labels hidden) to choose between audio chains; a human listens at every flagged timestamp before posting. Check: A/B record and listen log. [AX lessons-001: 5.5] [AX ax-gr4]

## Never

- **VDI-11-R08** · Never · stage: review — Never let the editor's own gate be the only gate. Check: Independent review on every release candidate. [AX lessons-001: 5.4]
- **VDI-11-R09** · Never · stage: review — Never use AI-review timestamps without re-checking them against the file's own word timings. Check: Use the final's ASR word times. [AX ax-gr1: timestamps do not match]
