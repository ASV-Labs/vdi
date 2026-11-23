---
id: VDI-09-RULES
title: "Platform formats (TikTok, Reels, YouTube Shorts, X): agent rules"
topic: 09_Platform_Formats
status: Seed
last_updated: 2026-11-23
---

# 09_Platform_Formats — agent rules

## Always

- **VDI-09-R01** · Always · stage: publish — Deliver 9:16 at 1080x1920, 30 fps, H.264 + AAC. Check: Gate: container check. [AX lessons-001: 4 table] TikTok ads recommend 9:16 at >= 540x960 [SRC tiktok-specs]; YouTube Shorts accept square or vertical [SRC yt-shorts-3min]
- **VDI-09-R02** · Always · stage: publish — Keep text and key visuals out of the platform UI. AX house safe area for captions: top 8%, bottom 20%, right 12% clear. Meta's Reels overlays are reported at 14% top, 35% bottom, 6% sides; check the platform's own overlay file for ads. Check: Gate: caption safe area; evidence safe area (top 8%, bottom 20%). [AX lessons-001: 4 table] [SRC adkit-meta-safe] (secondary) [SRC meta-reels-blog] TikTok safe zone depends on dimension and ad caption length [SRC tiktok-specs]
- **VDI-09-R03** · Always · stage: publish — Keep Shorts that use any third-party content under one minute, or clear the rights: a Short over one minute with an active copyright claim is blocked globally. Check: Rights check before posting anything over 60 s. [SRC yt-shorts-3min]
- **VDI-09-R04** · Always · stage: publish — Assume sound on for Reels but caption anyway; Meta reports over 75% of Reels views on Instagram are sound on. Check: Captions present and verbatim. [SRC meta-reels-blog]
- **VDI-09-R05** · Always · stage: audio — Do not rely on platform normalisation to make a quiet mix louder: YouTube turns loud content down and does not turn quiet content up. Check: Gate: loudness check on the final. [SRC prodadvice-yt]

## Prefer

- **VDI-09-R06** · Prefer · stage: publish — Prefer 15-60 s for this series (AX shorts were 40-47 s); longer is allowed on Shorts and Reels but Instagram previously advised against Reels over 90 s. Check: Gate: container duration (house window). [AX lessons-001: header] [SRC smt-ig-3min] Window [UNVERIFIED]
- **VDI-09-R07** · Prefer · stage: publish — For X, check the account's limit: secondary docs report 0.5-140 s and aspect 1:3 to 3:1 for standard uploads. Check: Check before posting. [SRC ayrshare-x] (secondary)
