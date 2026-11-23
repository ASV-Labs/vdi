---
id: VDI-03-CHECKLISTS
title: "Pickups and continuity: checklists"
topic: 03_Pickups_and_Continuity
status: Seed
last_updated: 2026-11-23
---

# 03_Pickups_and_Continuity — checklists

# Build checklist

## Stage: pickups

- [ ] Shoot on-camera pickups at the same spot and framing (mark the tripod), same light (close curtains… (VDI-03-R01)
- [ ] Record voice-only pickups on the same mic and spot as the take (VDI-03-R02)
- [ ] Read each pickup line twice and include a word or two of lead-in, so the join can sit in a natural… (VDI-03-R05)

## Stage: edit

- [ ] If the mic differs, match EQ (long-term spectrum on speech frames) and short-term level, and keep… (VDI-03-R03)
- [ ] Grade each on-camera pickup to the take's skin lightness and colour, and match sharpness, before… (VDI-03-R04)
- [ ] Never assume 'same camera, same spot' from a note… (VDI-03-R06)
- [ ] Prefer to place a voice-only pickup under screen footage, so picture continuity is not at stake (VDI-03-R07)
- [ ] Prefer the original take's words where they are clean, using the pickup only for the missing part… (VDI-03-R08)

# Design review checklist

- [ ] Does each on-camera pickup match the take's spot, light, wardrobe and framing?
- [ ] Is any voice pickup on a different mic, and was it matched?
- [ ] Are joins placed in natural pauses?
- [ ] Was each join re-transcribed by both ASR models?

## Rules these questions test

- VDI-03-R01 (Always, pickups): Shoot on-camera pickups at the same spot and framing (mark the tripod), same light (close curtains…
- VDI-03-R02 (Always, pickups): Record voice-only pickups on the same mic and spot as the take
- VDI-03-R03 (Always, edit): If the mic differs, match EQ (long-term spectrum on speech frames) and short-term level, and keep…
- VDI-03-R04 (Always, edit): Grade each on-camera pickup to the take's skin lightness and colour, and match sharpness, before…
- VDI-03-R05 (Always, pickups): Read each pickup line twice and include a word or two of lead-in, so the join can sit in a natural…
- VDI-03-R06 (Never, edit): Never assume 'same camera, same spot' from a note…
- VDI-03-R07 (Prefer, edit): Prefer to place a voice-only pickup under screen footage, so picture continuity is not at stake
- VDI-03-R08 (Prefer, edit): Prefer the original take's words where they are clean, using the pickup only for the missing part…

# QA checklist

- [ ] **face continuity (skin dE < 3.5)**: Gate check_faces.
- [ ] **1 s speech-level step across joins**: Gate check_join_levels.
- [ ] **room tone through joins**: Gate check_dropouts.
- [ ] **word endings against the source envelopes**: Gate check_word_endings.

- Font legibility issues such as 0 vs O.
- Layout churn and pacing feel.

# Red flags

- Background changes at a cut inside one section
- Skin noticeably darker or warmer after a cut
- Presence or level jump at a join
- A join that drops to digital silence

## Matching anti-patterns

- VDI-03-A01 Afternoon pickup: Same day, same marks, or grade and reframe to match.
- VDI-03-A02 Memo-to-camera jump: Mic-match EQ and level; keep room tone.
- VDI-03-A03 Join to digital zero: Crossfade over room tone.

# Evaluation template

- **Video:** <file>

| # | Criterion | Severity | Result (PASS/FAIL) | Evidence (timestamp, frame, measurement) |
|---|---|---|---|---|
| 1 | Skin dE < 3.5 at every face cut | blocker | | |
| 2 | 1 s level step < 2 dB at every join | blocker | | |
| 3 | No digital-zero at joins | major | | |
| 4 | Background spot matches | major | | |
