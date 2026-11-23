---
id: VDI-04-RULES
title: "Screen capture and product demos: agent rules"
topic: 04_Screen_Capture_and_Demos
status: Seed
last_updated: 2026-11-23
---

# 04_Screen_Capture_and_Demos — agent rules

## Always

- **VDI-04-R01** · Always · stage: screen — Use only real runs and live pages captured that day; save the verbatim tool output (session export, asciicast) and a README next to the footage. Check: Each screen file has a README with run id, time, tool versions and verbatim output. [AX lessons-001: 3.1] [AX ax-screens-agent: README format]
- **VDI-04-R02** · Always · stage: screen — Record each beat's run id; adjacent beats inside one spoken claim share a run id, or the frame carries a visible source label (for example 'demo run from the lineage repo'). Check: Gate: run ids and source labels check (label must be readable by OCR). [AX lessons-001: 3.2] [AX ax-v5: AX-04 graph]
- **VDI-04-R03** · Always · stage: screen — Record terminals narrow (about 40 columns), or re-render the saved asciicast narrow: 38-40 columns at a 39 px font gives 28-30 px cap height at 1080 wide. Never zoom a wide recording to reach text size. Text stays byte-identical to the saved output. Check: Gate: evidence line whole, >= 16 px inside both edges, left of the right 12%, glyph height >= 28 px. [AX lessons-002: 8.1] [AX lessons-001: 3.3] [AX ax-screens-ax04: 100 columns does not fit at 28 px]
- **VDI-04-R04** · Always · stage: screen — When re-rendering a cast at fewer columns, strip only the readline wrap pairs, note it in the edit notes, and diff the replayed text with the saved output. Check: Replayed plain text equals saved run text after joining wrapped rows. [AX lessons-002: 8.2 AX-04 beat6/beat7 casts]
- **VDI-04-R05** · Always · stage: screen — Look at the first and last frame of every clip range before using it; start after the page has painted. Check: Frame grab at t_in and t_out of every screen clip. [AX lessons-002: 8.6 ax01-signin-browser.mp4 white until ~1.0 s]
- **VDI-04-R06** · Always · stage: screen — Capture web pages at the CSS width where the needed line reaches 28 px inside x <= 950 (about 290-430 CSS px, device scale 3-5), so the page reflows instead of being cropped sideways. Check: Capture metadata records viewport width; gate evidence check. [AX lessons-002: 8.3] [AX ax-editnotes: new captures at 330-350 px] [AX lessons-001: 3.3]
- **VDI-04-R07** · Always · stage: screen — Use the approved test account; blur emails (including site-masked ones that still show a first letter and a domain), sign-in codes, tokens and keys. Check: Gate: PII sweep (OCR of every sampled frame) finds none. [AX lessons-001: 3.4] [AX ax-v5: AX-01 25.6-26.5 s]
- **VDI-04-R08** · Always · stage: screen — Cut around PLAN_REQUIRED and RATE_LIMITED lines unless the owner wants them shown. Check: Gate: PII sweep includes plan-wall strings. [AX ax-screens-agent: free-plan responses] [AX lessons-001: 3.4]
- **VDI-04-R09** · Always · stage: screen — Label sample work on screen ('This is a sample page, not a customer site.') inside the safe area, clear of captions. Check: Evidence beat for the label is readable. [AX lessons-001: 3.5]
- **VDI-04-R10** · Always · stage: screen — Mask the capture to whole rows or blocks around the evidence line (a window on the page's own background) and start terminal views on a row boundary; never show half-cut neighbouring rows. Check: By eye at 540x960 on the mid-frame of each screen beat (not in the gate yet). [AX lessons-002: 8.11 AX-03 'it.' fragment, half a button]

## Never

- **VDI-04-R11** · Never · stage: screen — Never intercut two runs inside one claim without a visible label, even if both runs are real. Check: Run-id check. [AX ax-screens-agent: 'don't intercut ... in the same beat'] [AX ax-v5: AX-01, AX-04]
- **VDI-04-R12** · Never · stage: screen — Never pan across a line while it is being read; reframe or re-render the verbatim text so the whole line fits still. Check: Gate: line bbox drift < 6 px for >= 1.6 s. [AX ax-v5: AX-04 27.3-29.5 s] [AX ax-editnotes: AX-04 verify row panned]
