---
id: VDI-011
title: "Gate proof on the five known-bad AX v4 files"
topic: docs
status: Draft
last_updated: 2026-11-23
---

# PROOF - the gate on the known-bad v4 files

> **Historical receipts.** Produced by video_gate 0.1.0 (now `vdi release`; logic unchanged by packaging) on 2026-11-23. The v4 footage is not published, so these runs can't be reproduced from this repo; the reproducible run is `vdi selftest --keep`.

The five `AX-0N-edit-v4.mp4` files were rejected by an independent reviewer (`ax:V5-ADDENDUM.md`) and by AI Studio review 4 (`ax:GEMINI-REVIEW-4.md`). A gate that claims to catch a defect class must FAIL them on it. Manifests (`examples/v4/manifests/`) were written from the scripts, pickup notes and screen-capture READMEs (`ax:SCRIPTS.md`, `ax:PICKUPS.md`); they declare intent, not what v4 did. Reports: `examples/v4/receipts/AX-0N-v4.gate.{md,json}`. Gate version 0.1.0, run 2026-11-23 (cold runs 8-10 min each on 2 shared cores; re-runs from cache ~1 min).

**Result: all five FAIL (exit 1).** Of 59 listed blockers: **33 caught, 14 partly caught, 12 missed.** Five of the misses are the face-processing item (plastic skin, halo), which the gate does not measure.

| File | Verdict | FAIL / WARN / PASS checks | Listed blockers | Caught | Partly | Missed |
|---|---|---|---|---|---|---|
| AX-01 v4 | FAIL | 13 / 1 / 4 | 15 | 11 | 3 | 1 |
| AX-02 v4 | FAIL | 11 / 1 / 6 | 10 | 5 | 3 | 2 |
| AX-03 v4 | FAIL | 11 / 1 / 6 | 10 | 5 | 2 | 3 |
| AX-04 v4 | FAIL | 12 / 2 / 4 | 14 | 7 | 3 | 4 |
| AX-05 v4 | FAIL | 9 / 1 / 8 | 10 | 5 | 3 | 2 |

Blocker ids: K = V5-ADDENDUM per-short item, T = V5-ADDENDUM tool fix T1-T3, G = GEMINI-REVIEW-4 item, L = reviewer's measured level steps (NOTES-working.md).

## AX-01 v4

| id | Listed blocker | Gate | What the gate reported |
|---|---|---|---|
| K1 | End 'faceplants' loses /ts/; no hold | **CAUGHT** | word endings 47.00 s: 300 ms of source speech not reproduced; ending hold 0.09 s; 'faceplants' not confirmed by both ASR models (script + caption) |
| K2 | 27.5 s 'in plain' heard as 'and play' | **CAUGHT** | script check: both models hear 'and play' |
| K3 | 6.1 s caption 'I've built' vs said 'I build' | **CAUGHT** | caption check: 'I've built' heard by one model only |
| K4 | Typed prompt from run 1, results from AX-01b | **CAUGHT** | evidence b05 expects 'opencode run "Build the pricing page'; frames read 'Design the ...' |
| K5 | Masked email on screen 25.6-26.5 s | **CAUGHT** | PII sweep: email at 25.7-26.4 s |
| K6 | 'Sign in to connect your agent' flashes ~4 frames | **PARTIAL** | evidence b04 'Enter your code' readable still only 0.5 s; the 4-frame page itself is inside a slide and is not flagged as a shot |
| K7 | NOW OPEN label in top 4% / right 12% | **CAUGHT** | evidence b01: glyph 17 px, y 77-96 (top 8%) |
| K8 | No templates on screen on 'tested templates' | **CAUGHT** | evidence b02: 'templates' not readable 20.1-23.0 s |
| T1 | Word endings cut: Guidance, templates, English | **CAUGHT** | word endings 20.59 s 110 ms, 21.89 s 140 ms, 28.49 s 100 ms (reviewer: 100/130/80 ms) |
| T2 | Flash shot 4.30 s; black camera panel 20.07 s | **CAUGHT** | 2-frame shot at 4.30 s; 2 black frames at 20.07 s |
| G1 | Evidence text cropped at the right edge | **CAUGHT** | evidence b06-b08: line touches the frame edge |
| G2 | Caption 'wins and the' on the end-card URL | **CAUGHT** | caption clearance 45.7-46.5 s |
| G4 | Rushed joins 0:23-0:27 and 0:30-0:33 | **PARTIAL** | gaps 22.96 s (70 ms) and 28.42 s (80 ms); nothing flagged in 0:30-0:33 |
| G5 | Face: plastic smoothing and halo | **MISSED** | not measurable by the gate (cannot_check) |
| G6 | Level/presence steps (reviewer: 4.30, 8.97, 10.87, 34.27 s; Gemini ~0:29-0:34) | **PARTIAL** | 1 s steps 4.20 s +2.6 dB and 9.00 s +2.1 dB; 10.87 and 34.27 s measured under 2 dB here |

## AX-02 v4

| id | Listed blocker | Gate | What the gate reported |
|---|---|---|---|
| K1 | End 'rest.' cut; no hold | **CAUGHT** | word endings 40.45 s 160 ms; ending hold 0.02 s |
| K2 | 27.27 s 'first.' loses /t/ | **CAUGHT** | word endings 27.26 s 90 ms |
| T2 | Flash shot 4.70 s | **CAUGHT** | 2-frame shot at 4.70 s |
| T3 | Pickup grade at 25.87 s and 36.27 s | **PARTIAL** | skin dE 7.9 at 25.80 s; 36.27 s not measured (no face detected either side during the transition; a long black region 36.30-38.00 s is reported as WARN) |
| G1 | Evidence text cropped | **PARTIAL** | all 5 evidence beats fail, but mostly for size/position; cropping itself only on b01/b02 wraps |
| G2 | Caption 'my account' on the @ASaltyVet lower third | **CAUGHT** | caption clearance 37.1-37.9 s |
| G3 | Ending abrupt | **CAUGHT** | ending hold 0.02 s, last 100 ms not decayed |
| G4 | Rushed 0:03-0:04, 0:21-0:22 | **MISSED** | flagged 9.62, 27.26, 28.54 s instead; the listed spots measured >= 0.12 s |
| G5 | Face plastic/halo | **MISSED** | cannot_check |
| L | 1 s level steps 11.30 s +2.5, 30.33 s +2.2 dB | **PARTIAL** | 11.20 s +2.2 dB; 30.33 s not over 2 dB here |

## AX-03 v4

| id | Listed blocker | Gate | What the gate reported |
|---|---|---|---|
| K1 | Caption 'and the ledger' vs said 'a ledger' | **CAUGHT** | caption check: 'the' not in the final audio's transcript |
| K2 | 7.23 s 'agents,' loses ~60 ms of /s/ | **CAUGHT** | word endings 7.22 s 140 ms |
| T2 | Flash shot 3.50 s | **CAUGHT** | 3-frame shot at 3.50 s |
| T3 | Pickup grade at 9.88, 15.10, 18.20 s | **PARTIAL** | dE 6.9 at 15.10 s, 4.1-4.2 at 18.2 s; 9.88 s not flagged |
| G1 | Evidence cropped | **PARTIAL** | evidence beats fail (wrapped/partial reads); not all for cropping |
| G2 | Caption 'for updates.' touches the URL lower third | **MISSED** | not flagged (clearance found other collisions: 'FREE AND PERSONAL' heading, page text) |
| G3 | Ending abrupt | **CAUGHT** | ending hold 0.11 s; last word 'updates' tail 300 ms lost |
| G4 | Rushed 0:03-0:04 | **MISSED** | flagged 9.76 s and 29.20 s instead |
| G5 | Face plastic/halo | **MISSED** | cannot_check |
| L | 1 s level steps 27.27 s +2.3, 29.33 s +3.2 dB | **CAUGHT** | 27.10 s +2.5 dB, 29.20 s +2.8 dB |

## AX-04 v4

| id | Listed blocker | Gate | What the gate reported |
|---|---|---|---|
| K1 | Demo graph (other run) unlabeled between terminal beats | **CAUGHT** | run-id check: label 'demo run from the lineage repo' not readable; run changes inside claim q3-note-lineage |
| K2 | 35.4 s 'confidence.' loses its ending | **MISSED** | no lost tail found at 35.4 s (a +2.4 dB level step at 35.50 s is flagged) |
| K3 | 'changed ... sample-revenue.csv' not whole and still | **CAUGHT** | evidence b09: never read whole; b08 'verdict: stale' moves and touches the edge |
| K4 | Caption 'source.' over his face for 2 frames | **MISSED** | cannot_check |
| K5 | 33.1 s caption 'or inferred.' 0.42 s late | **PARTIAL** | caption timing WARN: 0.44 s late (timing is WARN-only) |
| K6 | 'MIT License' said with no licence on screen | **CAUGHT** | evidence b13: 'MIT License' not on screen 40.0-41.7 s |
| K7 | Ad-lib 'Probably doesn't exist.' | **CAUGHT** | script check: unaccepted addition at 3.2 s |
| K8 | P0GL0L zeros read as O | **MISSED** | cannot_check (OCR reads the zeros as O too) |
| T2 | Flash 4.73 s; black panel ~7 frames at 38.07 s | **CAUGHT** | 2-frame shot at 4.73 s; 8 black frames at 38.07 s |
| G1 | Evidence cropped; graph node text cut | **PARTIAL** | graph beats fail (glyph 26 px, moving, label missing); terminal beats b07-b09 touch the edge |
| G3 | Ending abrupt | **CAUGHT** | ending hold 0.28 s |
| G4 | Rushed 0:04-0:05, 0:19-0:21, 0:35-0:36 | **PARTIAL** | 18.24 s flagged; 29.70 s flagged; 0:04-0:05 and 0:35-0:36 not |
| G5 | Face plastic/halo | **MISSED** | cannot_check |
| L | Level steps 13.73, 35.53, 38.07 s; 9 ms zero at 1.73 s | **CAUGHT** | 13.60 s +2.4, 35.50 s +2.4, 38.00 s +2.3 dB; 9 ms of digital zero at 1.73 s |

## AX-05 v4

| id | Listed blocker | Gate | What the gate reported |
|---|---|---|---|
| K1 | 33.6 s 'not a pass.' loses /s/ | **CAUGHT** | word endings 33.68 s 210 ms |
| K2 | 12-frame face shot then pickup at 28.14-28.53 s | **PARTIAL** | 5- and 8-frame shots at 28.27-28.37 s flagged; the 12-frame shot itself sits exactly at the threshold |
| K3 | FAIL line label off the left edge | **CAUGHT** | evidence b04: best read 'AIL sticky-chrome ...'; line also enters the right 12% |
| K4 | Digital zero at 15.83 s and 24.10 s | **CAUGHT** | 9 ms at 15.83 s, 8 ms at 24.09 s |
| T3 | Pickup grade at 28.53 s (dE 6.3) | **MISSED** | largest dE measured 3.3; the reviewer's 540 px frame method found 6.3 |
| G1 | Evidence cropped | **CAUGHT** | evidence b04-b07 touch the edge or read partially |
| G3 | Ending abrupt | **CAUGHT** | ending hold 0.17 s |
| G4 | Rushed 0:17-0:18, 0:28-0:29 | **PARTIAL** | 28.38 s flagged (50 ms); 0:17-0:18 not |
| G5 | Face plastic/halo | **MISSED** | cannot_check |
| G6 | Level/presence step at ~0:40 CTA | **PARTIAL** | 43.60 s +2.3 dB and 17.90 s +2.1 dB flagged; nothing at 40 s exactly |

## Findings not on the reviewers' lists (unconfirmed)

These are reported by the gate but were not in V5-ADDENDUM or review 4. Some are real (the ad-libs match the reviewer's script-vs-spoken notes; join dropouts match the reviewer's 'every join dips' note); others are probably false positives. None has been checked by a human.

- Script deviations that are real ad-libs but not on the owner-accepted list (for example AX-01 'right now' and 'code' missing, 'It builds.' missing; AX-02 'No agent writes its own permissions.' never spoken; AX-05 'not a pass' for 'never a pass'). The gate is right to fail them until the owner accepts them.
- Likely ASR false positives: AX-01 'contrast' heard as 'contrasts' by both models; AX-04 'plugin' heard as 'plug in'.
- Possible false positives: AX-01 6-frame shot at 36.37 s (upper half, Ferrow scroll); AX-01 skin dE 4.1 at 42.97 s and AX-04 dE 4.4 at 1.75 s (inside takes); AX-01 'Motif.' tail 160 ms at 37.72 s; several AX-05 short shots in the lower half (13.27, 39.53 s).
- Evidence beats can fail for manifest reasons (a beat window or expected text written imprecisely) as well as for render defects. Each failing beat lists its reasons so a reviewer can tell which.

## What this proves and what it does not

- It proves the gate measures the rendered file and fails these five on most of the defect classes the reviewers listed, including the ones the v4 gate passed by construction (cropped evidence, captions over content, caption words, ending holds, mixed runs).
- It does not prove the gate passes a good file: no known-good reference exists yet, so the false-positive rate is unknown.
- Thresholds were partly calibrated on these files (shot-change merging, pause length for stop closures, black-row detection). That is overfitting risk; re-prove on the next series' known-bad and known-good files.
- Missed classes: face processing look, captions over the face in a transition, 0 vs O, some pickup grade jumps at transitions (no face detected), some rushed joins and level steps the reviewers heard but the 1 s / 0.12 s measures do not reach.
