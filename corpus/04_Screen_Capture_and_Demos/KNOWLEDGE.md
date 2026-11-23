---
id: VDI-04-KNOWLEDGE
title: "Screen capture and product demos: knowledge"
topic: 04_Screen_Capture_and_Demos
status: Seed
last_updated: 2026-11-23
---

# 04_Screen_Capture_and_Demos — knowledge

# Principles

## 1. Never fake product output

Every terminal line, UI state and result on screen comes from a real run or a live page captured that day; OC-01 v4 was rejected on Nov 18 for agent lines no run produced. [AX lessons-001: 3.1]

## 2. One claim, one run

AX-01 showed the prompt from run 1 and the results from run 2; AX-04 put the repo's demo graph (grok-4.7, a URL source, 11/5) between terminal beats from tonight's glm-5.3 run as if it were the same file. [AX ax-v5: AX-01 26.5-28.2 s; AX-04 18.3-24.2 s] [AX lessons-001: 3.2]

## 3. Capture at the size it will be read

Zooming a wide terminal makes text big but crops lines at the frame edge ('changed evidenced sample-reve' exactly when he says 'names the source'). A 60x22 terminal at 30 px fits 1080 wide; 100 columns does not. [AX ax-gr4: #1] [AX ax-screens-ax04: recording pipeline]

# Patterns

## VDI-04-P01 Verbatim re-render

Take the saved output text (session export or .cast) and re-render it at about 40 columns and a 39 px font so the frame shows exactly the real bytes, wrapped to fit. [AX lessons-001: 3.3] [AX ax-screens-ax04: record_beat.py, render_beat.sh]

## VDI-04-P02 Run README

Per run: tool and model versions, account (named generically), prompt verbatim, what really happened (including failures), which beats it supports. [AX ax-screens-agent]

## VDI-04-P03 Designed-to-fail demo

Pick a task where the checker is likely to fail once, so the 'fix' claim is shown by the same run. [AX ax-screens-agent: AX-01b]

# Anti-patterns

| id | Anti-pattern | How it shows | Fix | Evidence |
|---|---|---|---|---|
| VDI-04-A01 | Wide terminal + zoom | Big text, lines cut at the frame edge. | Narrow terminal, verbatim re-render. | [AX ax-gr4: #1 all five] |
| VDI-04-A02 | Mixed runs | Prompt from one run, results from another. | One run per claim or a visible label. | [AX ax-v5: AX-01, AX-04] |
| VDI-04-A03 | Masked email on screen | Site-masked address still reveals the first letter and domain. | Blur the whole line. | [AX ax-v5: AX-01 25.6-26.5 s] |
| VDI-04-A04 | Plan wall in the cut | PLAN_REQUIRED / RATE_LIMITED lines from a free trial account. | Cut around them. | [AX ax-screens-agent] |

# Implementation notes

## Terminal recording pipeline (AX-04)

record_beat.py drives bash under asciinema with human-paced typing; render_beat.sh renders with agg (github-dark, DejaVu Sans Mono) to 1080x1080 H.264 30 fps. 60x22 at 30 px fits a 1080 frame. [AX ax-screens-ax04]

## Page capture

Capture at 330-390 CSS px wide at device scale 3 so 12-16 px text reaches ~28 px in a 1080 frame. [AX ax-editnotes: new captures]

## PII sweep

OCR every sampled frame of the final (10 fps) and match emails (including masked), codes next to the word 'code', API key prefixes, PLAN_REQUIRED and RATE_LIMITED. vdi/release.py check_pii.

## Gate checks that cover this topic

- **evidence lines**: Gate check_evidence: whole, still, >= 28 px, >= 1.6 s.
- **run ids and source labels**: Gate check_runs.
- **PII and plan-wall sweep**: Gate check_pii.

# Glossary

- **Run id**: Identifier of one real execution (agent session, terminal recording) that footage comes from.
- **Source label**: On-screen text that names where footage comes from when it is not the run being described.
- **Plan wall**: A response that only exists because of the account's plan (PLAN_REQUIRED, RATE_LIMITED).
- **Verbatim re-render**: Rendering the saved output text again at a different terminal width without changing a byte.
