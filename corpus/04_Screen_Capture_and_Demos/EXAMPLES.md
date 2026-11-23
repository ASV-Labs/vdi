---
id: VDI-04-EXAMPLES
title: "Screen capture and product demos: examples"
topic: 04_Screen_Capture_and_Demos
status: Seed
last_updated: 2026-11-23
---

# 04_Screen_Capture_and_Demos — examples

# Good examples

## VDI-04-E01 AX-04 terminal beats

Three real commands at 60x22, 30 px, recorded from one Hermes turn on glm-5.3, with the exact output reproduced in the README. [AX ax-screens-ax04]

## VDI-04-E02 AX-01b check beat

Contrast, touch-target, measure FAIL and re-check PASS all from one run. [AX ax-editnotes: v4 item 8]

## Rules these examples support

- VDI-04-R01: Use only real runs and live pages captured that day…
- VDI-04-R02: Record each beat's run id…
- VDI-04-R03: Record terminals narrow (about 40 columns), or re-render the saved asciicast narrow…
- VDI-04-R04: When re-rendering a cast at fewer columns, strip only the readline wrap pairs, note it in the edit…
- VDI-04-R05: Look at the first and last frame of every clip range before using it…
- VDI-04-R06: Capture web pages at the CSS width where the needed line reaches 28 px inside x <= 950 (about…
- VDI-04-R07: Use the approved test account…
- VDI-04-R08: Cut around PLAN_REQUIRED and RATE_LIMITED lines unless the owner wants them shown
- VDI-04-R09: Label sample work on screen ('This is a sample page, not a customer site.') inside the safe area…
- VDI-04-R10: Mask the capture to whole rows or blocks around the evidence line (a window on the page's own…

# Bad examples

## VDI-04-E03 AX-01 prompt from the wrong run

26.5-28.2 s typed prompt is 'Design the ...' (run 1) while results are from AX-01b ('Build the pricing page ...'). [AX ax-v5: AX-01]

## VDI-04-E04 AX-04 unlabeled demo graph

18.3-24.2 s graph from the repo's demo (grok-4.7, URL source, 11/5) between glm-5.3 terminal beats, no label. [AX ax-v5: AX-04]

## VDI-04-E05 AX-01 masked email

'We sent a 6-digit code to [site-masked address]' on screen 25.6-26.5 s. [AX ax-v5: AX-01] Gate found it by OCR. [AX vdi-gate-proof: AX-01 PII]

## Rules these defects broke

- VDI-04-R01: Use only real runs and live pages captured that day…
- VDI-04-R02: Record each beat's run id…
- VDI-04-R03: Record terminals narrow (about 40 columns), or re-render the saved asciicast narrow…
- VDI-04-R04: When re-rendering a cast at fewer columns, strip only the readline wrap pairs, note it in the edit…
- VDI-04-R05: Look at the first and last frame of every clip range before using it…
- VDI-04-R06: Capture web pages at the CSS width where the needed line reaches 28 px inside x <= 950 (about…
- VDI-04-R07: Use the approved test account…
- VDI-04-R08: Cut around PLAN_REQUIRED and RATE_LIMITED lines unless the owner wants them shown
- VDI-04-R09: Label sample work on screen ('This is a sample page, not a customer site.') inside the safe area…
- VDI-04-R10: Mask the capture to whole rows or blocks around the evidence line (a window on the page's own…
- VDI-04-R11: Never intercut two runs inside one claim without a visible label, even if both runs are real
- VDI-04-R12: Never pan across a line while it is being read…

# Implementation examples

## Manifest evidence beat

{"id": "b09-changed", "t0": 27.3, "t1": 29.5, "text": "changed evidenced sample-revenue.csv", "run_id": "ax04-hermes-glm53-2026-11-22", "claim": "q3-note-lineage"} (examples/v4/manifests/AX-04-v4.manifest.json)

## Running the gate

```bash
```
