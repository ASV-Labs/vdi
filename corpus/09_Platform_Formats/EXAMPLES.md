---
id: VDI-09-EXAMPLES
title: "Platform formats (TikTok, Reels, YouTube Shorts, X): examples"
topic: 09_Platform_Formats
status: Seed
last_updated: 2026-11-23
---

# 09_Platform_Formats — examples

# Good examples

## VDI-09-E01 AX container

All five v4 files: 1080x1920, 30 fps, H.264 + AAC, 40.5-47.2 s. [AX ax-reviewer: container]

## Rules these examples support

- VDI-09-R01: Deliver 9:16 at 1080x1920, 30 fps, H.264 + AAC
- VDI-09-R02: Keep text and key visuals out of the platform UI…
- VDI-09-R03: Keep Shorts that use any third-party content under one minute, or clear the rights…
- VDI-09-R04: Assume sound on for Reels but caption anyway…
- VDI-09-R05: Do not rely on platform normalisation to make a quiet mix louder…
- VDI-09-R06: Prefer 15-60 s for this series (AX shorts were 40-47 s)…
- VDI-09-R07: For X, check the account's limit…

# Bad examples

## VDI-09-E02 AX-01 NOW OPEN label

Supporting label sat in the top 4% / right 12% of the frame, under platform UI. [AX ax-v5: AX-01 12.9-15.4 s]

## Rules these defects broke

- VDI-09-R01: Deliver 9:16 at 1080x1920, 30 fps, H.264 + AAC
- VDI-09-R02: Keep text and key visuals out of the platform UI…
- VDI-09-R03: Keep Shorts that use any third-party content under one minute, or clear the rights…
- VDI-09-R04: Assume sound on for Reels but caption anyway…
- VDI-09-R05: Do not rely on platform normalisation to make a quiet mix louder…

# Implementation examples

## Manifest platform field

"platform": "tiktok,reels,shorts" in each fixture manifest; the gate uses gate-spec.json values today, per-platform profiles are a gap.

## Running the gate

```bash
```
