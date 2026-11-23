---
id: VDI-11-EXAMPLES
title: "Review and QA (AI review limits, independent review, blind A/B, gate design): examples"
topic: 11_Review_and_QA
status: Seed
last_updated: 2026-11-23
---

# 11_Review_and_QA — examples

# Good examples

## VDI-11-E01 Independent reviewer on v4

Measured clipped phonemes in ms, join levels, flash frames, skin dE and a screen-by-screen claims audit the editor had missed. [AX ax-reviewer]

## VDI-11-E02 AI Studio review 4

Watched the real video and quoted terminal text correctly. [AX ax-gr4]

## Rules these examples support

- VDI-11-R01: No 'final' without…
- VDI-11-R02: Every gate check reads the rendered mp4 (OCR of frames, envelopes vs source, shot detection, colour)…
- VDI-11-R03: No tolerance lists except owner-accepted spoken deviations…
- VDI-11-R04: Run the gate on known-bad files and keep the result with the gate…
- VDI-11-R05: Use an AI reviewer that receives the video itself (AX…
- VDI-11-R06: Verify every AI review claim against frames and audio before acting
- VDI-11-R07: Use a blind A/B (labels hidden) to choose between audio chains…

# Bad examples

## VDI-11-E03 v4 gate 22/22

Passed files with 19 blockers. [AX ax-qa-v4] [AX ax-v5]

## VDI-11-E04 Gemini app reviews 1-3

Transcript-only; invented caption misspellings and wardrobe. [AX ax-gr3: FALSE list] [AX lessons-001: 5.1]

## Rules these defects broke

- VDI-11-R01: No 'final' without…
- VDI-11-R02: Every gate check reads the rendered mp4 (OCR of frames, envelopes vs source, shot detection, colour)…
- VDI-11-R03: No tolerance lists except owner-accepted spoken deviations…
- VDI-11-R04: Run the gate on known-bad files and keep the result with the gate…
- VDI-11-R05: Use an AI reviewer that receives the video itself (AX…
- VDI-11-R06: Verify every AI review claim against frames and audio before acting
- VDI-11-R07: Use a blind A/B (labels hidden) to choose between audio chains…
- VDI-11-R08: Never let the editor's own gate be the only gate
- VDI-11-R09: Never use AI-review timestamps without re-checking them against the file's own word timings

# Implementation examples

## Gate proof

All five v4 files FAIL the VDI gate; caught and missed blockers are listed per file in docs/release-gate-proof-v4.md. [AX vdi-gate-proof]

## Running the gate

```bash
```
