---
id: VDI-07-EXAMPLES
title: "Audio (cleanup, loudness, joins, room tone): examples"
topic: 07_Audio
status: Seed
last_updated: 2026-11-23
---

# 07_Audio — examples

# Good examples

## VDI-07-E01 v4 voice chain

Ranked best in the blind A/B: low echo, clean floor, natural, no artifacts. [AX ax-gr4: Y best]

## Rules these examples support

- VDI-07-R01: Use a light neural denoiser (AX…
- VDI-07-R02: Hit the house loudness target on the final AAC…
- VDI-07-R03: Take room tone from a real pause in the source take, through the same clean-up chain, with its…
- VDI-07-R04: Keep room tone continuous through every join…
- VDI-07-R05: Keep the 1 s speech-level step across each join under 2 dB (<= 1 LU at pickups)
- VDI-07-R06: Detect word ends on a >= 3.5 kHz envelope as well as full band before fading
- VDI-07-R07: Listen (a human) at every flagged timestamp before posting…
- VDI-07-R09: Optional, gentle…

# Bad examples

## VDI-07-E02 v3 chain

Ranked worst: clicks in pauses, gating, cut word endings. [AX ax-gr4: Z worst]

## VDI-07-E03 Join holes

Every join dips to -57..-90 dB re speech for ~10 ms; exact-zero runs 8-9 ms at AX-04 1.73 s and AX-05 15.83 s. [AX ax-reviewer: audio quality]

## Rules these defects broke

- VDI-07-R01: Use a light neural denoiser (AX…
- VDI-07-R02: Hit the house loudness target on the final AAC…
- VDI-07-R03: Take room tone from a real pause in the source take, through the same clean-up chain, with its…
- VDI-07-R04: Keep room tone continuous through every join…
- VDI-07-R05: Keep the 1 s speech-level step across each join under 2 dB (<= 1 LU at pickups)
- VDI-07-R06: Detect word ends on a >= 3.5 kHz envelope as well as full band before fading
- VDI-07-R07: Listen (a human) at every flagged timestamp before posting…
- VDI-07-R08: Never push noise or echo removal further once words start to gate…

# Implementation examples

## Gate dropouts on AX-01 v4

'12.86 s: 7 ms of digital zero', '34.27 s: 4 ms', '45.03 s: 5 ms'. [AX vdi-gate-proof: AX-01]

## Running the gate

```bash
```
