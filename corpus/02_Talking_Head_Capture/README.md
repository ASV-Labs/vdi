---
id: VDI-02-README
title: "Talking-head capture (camera, light, framing, mic, room): overview"
topic: 02_Talking_Head_Capture
status: Seed
last_updated: 2026-11-23
---

# 02_Talking_Head_Capture — Talking-head capture (camera, light, framing, mic, room)

Capture rules for the on-camera parts: what camera, light, framing, microphone and room give footage that does not need rescue in the edit.

Stages: shoot.

## What this topic covers

- Camera and resolution for a 9:16 crop
- Light direction and eye-socket shadows
- Framing and headroom
- Microphone distance
- Room echo and noise
- Performer delivery: last word, hold, repeats

## Related topics

`03_Pickups_and_Continuity`, `07_Audio`, `08_Colour_and_Face`

# Overview

## The short version

- **Fix softness at capture, not in post.** A 1620x1080 webcam cropped to 9:16 is about a 2x upscale. Sharpening gave a plastic look and a halo on the wall; Real-ESRGAN measured no better (edge steepness 12.0 vs 11.9) and cost 8.6-8.8 s per frame, about 6.7 h for five shorts. [AX ax-editnotes: v4 item 1] [AX lessons-001: 2.1]
- **Fix the room before the take.** The office is reflective; raw takes had a floor only 15-18 dB below speech. Denoise helps, but the harder chain produced clicks, pumping and cut word endings. [AX ax-reviewer: audio quality] [AX ax-gr4: blind A/B]
- **Deliver the last word, then hold.** Quiet final consonants (/s/, /ts/, /st/) were the ones that got cut. A full last word plus a still, silent second gives the editor something to fade into. [AX lessons-001: 2.5]

## Where this sits in the workflow

Stages: shoot. The rules in `RULES.md` are keyed to these stages, so `vdi_checklist(stage)` and `vdi_brief(...)` in the MCP server can pull them.

# Known gaps

## Research gaps

1. **SEED** - No AX data from a phone 4K capture yet; the camera rule is inferred from the failure of the webcam path.
2. **SEED** - Light angle and mic distance are standard practice, not measured on AX.

## Research seeds (leads not yet used)

- Compare a phone-4K take with the webcam take on the AX edge-steepness benchmark.
- Measure floor-to-speech in the treated vs untreated room.
