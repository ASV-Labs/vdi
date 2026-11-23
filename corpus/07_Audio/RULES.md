---
id: VDI-07-RULES
title: "Audio (cleanup, loudness, joins, room tone): agent rules"
topic: 07_Audio
status: Seed
last_updated: 2026-11-23
---

# 07_Audio — agent rules

## Always

- **VDI-07-R01** · Always · stage: audio — Use a light neural denoiser (AX: DeepFilterNet 3 at an 18 dB attenuation limit) and stop there; do not stack gates and expanders. Check: Blind A/B against the raw cut when the chain changes. [AX ax-gr4: blind A/B] [AX ax-editnotes: v4 item 2]
- **VDI-07-R02** · Always · stage: audio — Hit the house loudness target on the final AAC: -14 LUFS +-0.5 integrated, true peak <= -1.5 dBTP. Check: Gate: ebur128 on the final file. [AX lessons-001: 4 table] Target is a house choice [UNVERIFIED]; YouTube's reference is not published [SRC prodadvice-yt]
- **VDI-07-R03** · Always · stage: audio — Take room tone from a real pause in the source take, through the same clean-up chain, with its loudest 10 ms frame near the floor; never loop 'the quietest part' of a tightly cut programme (it carries word tails that ASR hears as extra words). Check: Floor between phrases >= 30 dB under speech; 0.5 s after the last word below speech -30 dB (gate ending check). [AX lessons-002: 8.9 v5 first prep: spurious plurals heard by both ASR models]
- **VDI-07-R04** · Always · stage: audio — Keep room tone continuous through every join; never dip to digital zero. Check: Gate: no zero runs > 1 ms. [AX ax-v5: AX-05 15.83 s, 24.10 s] [AX ax-reviewer: zero runs 1-9 ms at joins]
- **VDI-07-R05** · Always · stage: audio — Keep the 1 s speech-level step across each join under 2 dB (<= 1 LU at pickups). Check: Gate: 1 s speech-level step. [AX ax-reviewer: 2.0-3.2 dB at 11 joins] Threshold [UNVERIFIED]
- **VDI-07-R06** · Always · stage: audio — Detect word ends on a >= 3.5 kHz envelope as well as full band before fading. Check: Gate: word endings against the source envelopes. [AX ax-v5: T1]
- **VDI-07-R07** · Always · stage: review — Listen (a human) at every flagged timestamp before posting; use a blind A/B to choose between chains. Check: Review notes list each flagged time with a verdict. [AX lessons-001: 5.5]

## Never

- **VDI-07-R08** · Never · stage: audio — Never push noise or echo removal further once words start to gate; the v3 chain cut endings and clicked in pauses. Check: Blind A/B, spectrogram of word tails. [AX ax-gr4: blind A/B Z worst] [AX lessons-001: 2.2]

## Prefer

- **VDI-07-R09** · Prefer · stage: audio — Optional, gentle: HPF 80-90 Hz, -2 dB around 300 Hz, +1.5 dB at 3-4 kHz with light de-ess, light 2.5:1 compression (AI Studio reviewer's advice, not yet tested). Check: A/B before adopting. [AX ax-gr4: audio advice] Not tested [UNVERIFIED]
