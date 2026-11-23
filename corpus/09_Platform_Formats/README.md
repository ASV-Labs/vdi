---
id: VDI-09-README
title: "Platform formats (TikTok, Reels, YouTube Shorts, X): overview"
topic: 09_Platform_Formats
status: Seed
last_updated: 2026-11-23
---

# 09_Platform_Formats — Platform formats (TikTok, Reels, YouTube Shorts, X)

What each platform documents about aspect ratio, length, safe zones and sound, what is only reported second-hand, and the AX house format that sits inside all of them.

Stages: publish.

## What this topic covers

- Aspect ratio and resolution
- Length limits
- Safe zones (platform UI)
- Sound-on behaviour and loudness normalisation
- Ads specs vs organic posts

## Related topics

`06_Captions_and_On_Screen_Text`, `07_Audio`, `10_Hooks_and_Retention`

# Overview

## The short version

- **Design inside every platform at once.** AX ships one 1080x1920 30 fps H.264+AAC file of 15-60 s with captions in a conservative safe area, so the same file fits TikTok, Reels and Shorts. [AX lessons-001: 4 table] House format [UNVERIFIED as optimal]
- **Ads documentation is not organic documentation.** TikTok's specs and creative guidance cited here are for ads; organic posting limits and UI can differ. [SRC tiktok-specs] [SRC tiktok-creative]
- **Re-check limits before relying on them.** Lengths changed recently: YouTube Shorts up to three minutes (standard channels, uploads after 15 Oct 2024) and Instagram Reels up to three minutes (Jan 2025). [SRC yt-shorts-3min] [SRC smt-ig-3min]

## Where this sits in the workflow

Stages: publish. The rules in `RULES.md` are keyed to these stages, so `vdi_checklist(stage)` and `vdi_brief(...)` in the MCP server can pull them.

# Known gaps

## Research gaps

1. **SEED** - SEED: Meta's own safe-zone percentages not fetched (secondary only).
2. **SEED** - SEED: no official organic TikTok length/safe-zone page fetched; ads pages only.
3. **SEED** - SEED: X limits from a secondary source.
4. **SEED** - No per-platform gate profiles yet.

## Research seeds (leads not yet used)

- Fetch Meta Business Help ad specs 980593475366490.
- Fetch YouTube recommended upload encoding settings (answer 1722171).
- Fetch TikTok organic upload guidance and TopView specs.
- Download each platform's safe-zone overlay and measure it.
