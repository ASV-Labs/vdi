---
id: VDI-10-KNOWLEDGE
title: "Hooks and retention: knowledge"
topic: 10_Hooks_and_Retention
status: Seed
last_updated: 2026-11-23
---

# 10_Hooks_and_Retention — knowledge

# Principles

## 1. Lead with the proposition

TikTok's ads guidance: put the hook in the first 6 seconds and introduce the proposition in the first 3. [SRC tiktok-creative]

## 2. Platforms measure the first seconds

YouTube reports 'Stayed to watch' for Shorts: the share of times viewers stayed past the initial seconds; engaged views exclude loops. [SRC yt-analytics]

## 3. No retention data from AX yet

None of the AX shorts has been posted; every hook rule here is from platform guidance or reviewer opinion, not from measured watch time. [AX lessons-001: 7 open questions]

# Patterns

## VDI-10-P01 Two-line hook

Setup line, then the turn ('My agent said done. Motif said not yet.'). [AX ax-scripts: AX-05]

## VDI-10-P02 Payoff punch

Punch-in that lands on the payoff word ('ugly', 'permission', 'team'). [AX ax-gr2: #2]

## VDI-10-P03 Early proof

A real screen within the first ~15 s. [AX ax-gr3: #5]

# Anti-patterns

| id | Anti-pattern | How it shows | Fix | Evidence |
|---|---|---|---|---|
| VDI-10-A01 | Lead breath | Dead air before the first word. | Start on the syllable. | [AX ax-gr2: #2] |
| VDI-10-A02 | Undercut hook | An ad-lib after the hook that changes its meaning. | Cut it if the join is clean. | [AX ax-v5: AX-04] |

# Implementation notes

## Measuring after posting

Use 'Stayed to watch' (Shorts) and the platform equivalents to compare hooks; log results back into this topic with dates. [SRC yt-analytics]

## Hook check in the gate

The gate does not judge hook quality; it checks the hook's mechanics (no flash shot, captions match, start of speech).

## Gate checks that cover this topic

- **shot lengths (hook join)**: check_shots
- **spoken words vs script (first 6 s)**: check_script

# Glossary

- **Hook**: The first one or two sentences and shots, meant to stop the scroll.
- **Payoff word**: The word that carries the hook's point.
- **Stayed to watch**: YouTube Shorts metric of viewers staying past the initial seconds. [SRC yt-analytics]
