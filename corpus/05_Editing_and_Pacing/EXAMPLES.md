---
id: VDI-05-EXAMPLES
title: "Editing and pacing (cuts, holds, joins, endings, layout churn): examples"
topic: 05_Editing_and_Pacing
status: Seed
last_updated: 2026-11-23
---

# 05_Editing_and_Pacing — examples

# Good examples

## VDI-05-E01 v4 evidence holds (plan)

v4 pre-lapped zooms and kept lines lit under the next phrase so plan holds reached 1.6 s; the rendered file still cropped several lines, which is why holds are measured on frames. [AX ax-editnotes: v4 item 4] [AX vdi-gate-proof]

## Rules these examples support

- VDI-05-R01: No shot shorter than 12 frames…
- VDI-05-R02: Snap any shot start within 0.15 s of an audio join to the join
- VDI-05-R03: Assign frames to shots and segments by frame index (or compare with a small epsilon after the frame…
- VDI-05-R04: A screen that takes over at a voice-over piece starts exactly with the piece…
- VDI-05-R05: Never show a black or blank panel for more than one frame…
- VDI-05-R06: Detect word ends on a >= 3.5 kHz envelope as well as full band, each with a threshold relative to…
- VDI-05-R07: End every short 0.6-0.8 s after the last word, audio decaying into room tone
- VDI-05-R08: Keep at least 0.12 s of pause between sentences, and no longer than natural
- VDI-05-R09: Hold each evidence line whole, still (drift < 6 px) and >= 28 px for >= 1.6 s…
- VDI-05-R12: Prefer holding a screen through a line and cutting to a pickup at its join over a 12-frame face…

# Bad examples

## VDI-05-E02 Hook/intro flash, AX-01..04

AX-01 4.30 s, AX-02 4.70 s, AX-03 3.50 s, AX-04 4.73 s. [AX ax-v5: T2]

## VDI-05-E03 Black camera panel

AX-01 20.07 s for 2 frames; AX-04 38.07 s for ~7 frames. [AX ax-v5: T2]

## VDI-05-E04 Cut tails

AX-01 'faceplants' (/ts/ 130 ms past the end), AX-02 'rest.', AX-04 'confidence.', AX-05 'not a pass.' [AX ax-v5: per-short blockers] [AX ax-reviewer: clipped phonemes]

## Rules these defects broke

- VDI-05-R01: No shot shorter than 12 frames…
- VDI-05-R02: Snap any shot start within 0.15 s of an audio join to the join
- VDI-05-R03: Assign frames to shots and segments by frame index (or compare with a small epsilon after the frame…
- VDI-05-R04: A screen that takes over at a voice-over piece starts exactly with the piece…
- VDI-05-R05: Never show a black or blank panel for more than one frame…
- VDI-05-R06: Detect word ends on a >= 3.5 kHz envelope as well as full band, each with a threshold relative to…
- VDI-05-R07: End every short 0.6-0.8 s after the last word, audio decaying into room tone
- VDI-05-R08: Keep at least 0.12 s of pause between sentences, and no longer than natural
- VDI-05-R09: Hold each evidence line whole, still (drift < 6 px) and >= 28 px for >= 1.6 s…
- VDI-05-R10: Do not flip split <-> full frame within ~2 s…
- VDI-05-R11: Never let a pause-trim rule cut into a soft word…

# Implementation examples

## Gate finding (AX-01 v4)

'2-frame shot at 4.30 s (whole)', '41% of the frame height went black for 2 frames at 20.07-20.13 s', 'hold 0.09 s after the last sound'. [AX vdi-gate-proof: AX-01]

## Running the gate

```bash
```
