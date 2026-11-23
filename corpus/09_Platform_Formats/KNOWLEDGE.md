---
id: VDI-09-KNOWLEDGE
title: "Platform formats (TikTok, Reels, YouTube Shorts, X): knowledge"
topic: 09_Platform_Formats
status: Seed
last_updated: 2026-11-23
---

# 09_Platform_Formats — knowledge

# Principles

## 1. Design inside every platform at once

AX ships one 1080x1920 30 fps H.264+AAC file of 15-60 s with captions in a conservative safe area, so the same file fits TikTok, Reels and Shorts. [AX lessons-001: 4 table] House format [UNVERIFIED as optimal]

## 2. Ads documentation is not organic documentation

TikTok's specs and creative guidance cited here are for ads; organic posting limits and UI can differ. [SRC tiktok-specs] [SRC tiktok-creative]

## 3. Re-check limits before relying on them

Lengths changed recently: YouTube Shorts up to three minutes (standard channels, uploads after 15 Oct 2024) and Instagram Reels up to three minutes (Jan 2025). [SRC yt-shorts-3min] [SRC smt-ig-3min]

# Patterns

## VDI-09-P01 One master, conservative safe area

One vertical master whose text sits inside the intersection of the platforms' UI-free areas. [AX lessons-001: 4 table]

## VDI-09-P02 Overlay check

Place the platform's own safe-zone overlay over a frame grab of every text-bearing beat before posting. [SRC tiktok-specs: downloadable safe zone files]

# Anti-patterns

| id | Anti-pattern | How it shows | Fix | Evidence |
|---|---|---|---|---|
| VDI-09-A01 | Text under the UI | Captions or evidence in the bottom band or right rail. | Safe area. | [AX ax-v5: AX-01 NOW OPEN in top 4% / right 12%] |
| VDI-09-A02 | Over-a-minute Short with claimed music | Blocked globally if a claim is active. | Stay under 60 s or clear rights. | [SRC yt-shorts-3min] |

# Implementation notes

## Platform table (as of 2026-11-23)

YouTube Shorts: square or vertical, up to 3 min [SRC yt-shorts-3min]. TikTok In-Feed ads: 9:16 >= 540x960 recommended, up to 10 min non-Spark, <= 500 MB, >= 516 kbps [SRC tiktok-specs]. Instagram Reels: up to 3 min since Jan 2025 [SRC smt-ig-3min]; 9:16 with audio recommended for Reels ads [SRC meta-reels-blog]. X: 0.5-140 s, 1:3-3:1 (secondary) [SRC ayrshare-x].

## Gate settings

vdi/release_data/gate-spec.json holds the AX house values (1080x1920, 30 fps, 15-60 s, -14 LUFS, safe area 8/20/12). Change them there, per platform, and note why.

## Gate checks that cover this topic

- **container**: check_container
- **caption safe area**: check_captions
- **loudness**: check_loudness

# Glossary

- **Safe zone**: Area of the frame not covered by the platform's buttons, captions and navigation.
- **Spark Ads**: TikTok ads that use an organic post.
- **Stayed to watch**: YouTube Shorts metric: percentage of times viewers stayed past the initial seconds. [SRC yt-analytics]
