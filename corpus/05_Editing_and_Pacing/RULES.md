---
id: VDI-05-RULES
title: "Editing and pacing (cuts, holds, joins, endings, layout churn): agent rules"
topic: 05_Editing_and_Pacing
status: Seed
last_updated: 2026-11-23
---

# 05_Editing_and_Pacing — agent rules

## Always

- **VDI-05-R01** · Always · stage: edit — No shot shorter than 12 frames; no 1-3 frame flashes. Check: Gate: scene detection per region (whole, upper, lower half). [AX ax-v5: T2] Threshold [UNVERIFIED]
- **VDI-05-R02** · Always · stage: edit — Snap any shot start within 0.15 s of an audio join to the join. Check: Gate: shot lengths; flash frames at joins. [AX ax-v5: T2] [AX lessons-001: 4 table]
- **VDI-05-R03** · Always · stage: edit — Assign frames to shots and segments by frame index (or compare with a small epsilon after the frame time); never compare k/fps with a rounded cut time. Check: Gate: black-panel check. [AX lessons-002: 8.8 AX-01 v5 47.57 s, v4 20.07 s]
- **VDI-05-R04** · Always · stage: edit — A screen that takes over at a voice-over piece starts exactly with the piece; a camera shot never starts inside a voice-over piece; snap shot starts to on-camera joins within 12 frames. Check: Gate: shot lengths. [AX lessons-002: 8.10 AX-01 4.40/4.58 s, AX-04 41.10/41.36 s]
- **VDI-05-R05** · Always · stage: edit — Never show a black or blank panel for more than one frame; start the screen shot at the voice-over join. Check: Gate: black-panel check (rows that just went black, > 1 frame). [AX ax-v5: T2 AX-01 20.07 s, AX-04 38.07 s]
- **VDI-05-R06** · Always · stage: edit — Detect word ends on a >= 3.5 kHz envelope as well as full band, each with a threshold relative to that source file's own floor (not an absolute dBFS); fade only after both are quiet; tail fades >= 120 ms; no tail cut faster than 60 ms. Check: Gate: word endings against the source envelopes. [AX ax-v5: T1] [AX lessons-002: 8.4] [AX lessons-001: 2.5, 4 table]
- **VDI-05-R07** · Always · stage: edit — End every short 0.6-0.8 s after the last word, audio decaying into room tone. Check: Gate: ending hold 0.6-1.0 s, last 100 ms >= 30 dB below speech. [AX ax-gr4: #3] [AX lessons-001: 4 table] Values [UNVERIFIED]
- **VDI-05-R08** · Always · stage: edit — Keep at least 0.12 s of pause between sentences, and no longer than natural. Check: Gate: inter-sentence gaps. [AX ax-gr4: #4] [AX lessons-001: 4 table] Threshold [UNVERIFIED]
- **VDI-05-R09** · Always · stage: edit — Hold each evidence line whole, still (drift < 6 px) and >= 28 px for >= 1.6 s; pre-lap the zoom so it arrives on the word. Check: Gate: evidence lines. [AX lessons-001: 4 table] [AX ax-reviewer: AX-04 verify readable still 0.47 s] Values [UNVERIFIED]

## Never

- **VDI-05-R10** · Never · stage: edit — Do not flip split <-> full frame within ~2 s; hold one layout for the whole beat. Check: Review by eye (gate does not measure layout churn). [AX ax-editnotes: v4 item 9] [AX lessons-001: 4 table]
- **VDI-05-R11** · Never · stage: edit — Never let a pause-trim rule cut into a soft word; keep pauses next to soft words longer. Check: Gate: word endings; sentence gaps. [AX ax-reviewer: clipped phonemes]

## Prefer

- **VDI-05-R12** · Prefer · stage: edit — Prefer holding a screen through a line and cutting to a pickup at its join over a 12-frame face shot between them. Check: Review shot list around pickups. [AX ax-v5: AX-05 28.14-28.53 s]
