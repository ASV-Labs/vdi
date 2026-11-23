---
id: VDI-02-EXAMPLES
title: "Talking-head capture (camera, light, framing, mic, room): examples"
topic: 02_Talking_Head_Capture
status: Seed
last_updated: 2026-11-23
---

# 02_Talking_Head_Capture — examples

# Good examples

## VDI-02-E01 Same spot, same light for on-camera pickups (intended)

PICKUPS.md records same camera and wardrobe for the on-camera updates; the reviewer later found the background spot and light differed, which is why the capture sheet exists. [AX ax-pickups: on-camera pickups] [AX ax-reviewer: picture]

## Rules these examples support

- VDI-02-R01: Use a phone rear camera at 4K held vertical, or a real camera…
- VDI-02-R02: Put the key light in front of the face at about 45 degrees, at eye level…
- VDI-02-R03: Frame the face for the 9:16 crop at capture…
- VDI-02-R04: Mic close…
- VDI-02-R05: Damp the room…
- VDI-02-R06: Finish the last word fully, then hold still and silent for one second
- VDI-02-R07: Say each line twice with a pause
- VDI-02-R08: Note wardrobe, framing marks, light state and mic for every take, so pickups can match

# Bad examples

## VDI-02-E02 Soft webcam face

All five shorts: webcam-soft face; v4's sharpen + denoise read as plastic with a halo on the white wall. [AX ax-gr4: #5] [AX ax-editnotes: still weak]

## VDI-02-E03 Roomy raw takes

Floor 15-18 dB below speech in the raw takes. [AX ax-reviewer: audio quality]

## Rules these defects broke

- VDI-02-R01: Use a phone rear camera at 4K held vertical, or a real camera…
- VDI-02-R02: Put the key light in front of the face at about 45 degrees, at eye level…
- VDI-02-R03: Frame the face for the 9:16 crop at capture…
- VDI-02-R04: Mic close…
- VDI-02-R05: Damp the room…
- VDI-02-R06: Finish the last word fully, then hold still and silent for one second
- VDI-02-R07: Say each line twice with a pause
- VDI-02-R08: Note wardrobe, framing marks, light state and mic for every take, so pickups can match
- VDI-02-R09: Never try to rescue a soft webcam face with heavy sharpening or upscaling

# Implementation examples

## Benchmark script

ax:bench/face_bench.py compared sharpening options on one frame (AX evidence, read-only).

## Running the gate

```bash
```
