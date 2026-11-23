---
id: VDI-02-KNOWLEDGE
title: "Talking-head capture (camera, light, framing, mic, room): knowledge"
topic: 02_Talking_Head_Capture
status: Seed
last_updated: 2026-11-23
---

# 02_Talking_Head_Capture — knowledge

# Principles

## 1. Fix softness at capture, not in post

A 1620x1080 webcam cropped to 9:16 is about a 2x upscale. Sharpening gave a plastic look and a halo on the wall; Real-ESRGAN measured no better (edge steepness 12.0 vs 11.9) and cost 8.6-8.8 s per frame, about 6.7 h for five shorts. [AX ax-editnotes: v4 item 1] [AX lessons-001: 2.1]

## 2. Fix the room before the take

The office is reflective; raw takes had a floor only 15-18 dB below speech. Denoise helps, but the harder chain produced clicks, pumping and cut word endings. [AX ax-reviewer: audio quality] [AX ax-gr4: blind A/B]

## 3. Deliver the last word, then hold

Quiet final consonants (/s/, /ts/, /st/) were the ones that got cut. A full last word plus a still, silent second gives the editor something to fade into. [AX lessons-001: 2.5]

# Patterns

## VDI-02-P01 Capture sheet

Per short: camera, lens/zoom, tripod mark, light state (curtains, time), wardrobe, mic, room treatment. It is what makes a later pickup match. [AX lessons-001: 2.3]

## VDI-02-P02 Double read

Each line read twice with a pause; the editor picks the better read and has a spare for pickups. [AX lessons-001: 2.6]

## VDI-02-P03 Tail hold

Performer holds still and silent for a second after the last word of every section. [AX lessons-001: 2.5]

# Anti-patterns

| id | Anti-pattern | How it shows | Fix | Evidence |
|---|---|---|---|---|
| VDI-02-A01 | Webcam crop | Landscape webcam cropped to vertical, then sharpened. | Shoot vertical at 4K. | [AX ax-editnotes: v4 item 1] |
| VDI-02-A02 | Overhead light | Eye sockets in shadow; grading cannot recover. | Key light in front at 45 degrees. | [AX ax-gr1: every clip] |
| VDI-02-A03 | Mic at arm's length in a bare room | Roomy, hissy takes that need aggressive cleanup. | Lav or phone close; damp the room. | [AX lessons-001: 2.2] |

# Implementation notes

## Test frame

Before the take, record five seconds, crop to 1080x1920 and look at it at phone size: face sharp, eyes lit, no wasted headroom.

## Room check

Record ten seconds of silence and a clap; the silence floor and the clap tail tell you whether to add damping. A floor less than ~25 dB below speech is a warning sign [UNVERIFIED].

## Webcam benchmark (AX)

Options measured on one AX-01 frame: v3 crop + unsharp 11.9; full column + temporal denoise + contrast-adaptive sharpen 15.1 (+50% render time); Real-ESRGAN 12.0 at 8.6-8.8 s/frame. [AX ax-editnotes: v4 item 1]

## Gate checks that cover this topic

- **word endings against the source envelopes**: Indirect: good capture leaves a clean consonant and a hold for the edit.
- **face continuity**: Capture sheet makes pickups match.

# Glossary

- **Upscale factor**: Output pixels per source pixel along the short side; ~2x for a 1080-row webcam cropped and scaled to 1920 tall.
- **Room tone**: The sound of the room with nobody talking; recorded so joins can be filled.
- **Edge steepness**: Mean of the top 2% of image gradients; the AX benchmark's sharpness measure.
