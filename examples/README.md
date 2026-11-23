---
id: VDI-EXAMPLES
title: "Examples: real manifests and gate outputs"
topic: examples
status: Draft
last_updated: 2026-11-23
---

# Examples

Real artifacts from the AX series. **The footage is not published**, so none of these can be re-run from
this repo. The reproducible run is `vdi selftest --keep`, which builds synthetic good and bad shorts you can
point `vdi check` at.

## `v4/` — historical receipts

- `manifests/AX-0N-v4.manifest.json` — the release-gate manifests for the five v4 renders, written from the
  scripts, pickup notes and screen-capture READMEs. They declare intent (script, proper nouns, evidence beats
  with time window + exact text + run id, source audio), plus `known_blockers` from the independent review so
  the proof could score caught vs missed. Source-audio paths are `ax:` records (raw takes, not published).
- `receipts/AX-0N-v4.gate.{md,json}` + `summary.json` — produced by video_gate 0.1.0 (now `vdi release`;
  packaging changed paths only, not logic) on 2026-11-23. Scored in `docs/release-gate-proof-v4.md`: 33 of 59
  listed blockers caught, 14 partly, 12 missed.

## `v3/` — verified output from `vdi release` 0.1.0 on AX-01 v3 (footage not published)

The end-to-end run after packaging (`vdi release AX-01-edit-v3.mp4 --manifest AX-01-v3.manifest.json`,
2026-11-23, 285 s on 2 CPU cores, both Whisper models, OCR of 470 frames). Verdict **FAIL** — 13 FAIL,
1 WARN, 4 PASS.

Read it as proof that the packaged gate runs end to end, not as a calibrated verdict on v3:

- The manifest was written for **v4**; v3's edit differs, so evidence-beat windows and the script comparison
  are only approximately aligned.
- Only the voice-memo **pickups** were available as source audio (the camera take wasn't), so word endings
  were compared on the 9 pickup segments only.
- Where it overlaps with `vdi check` on the same file it agrees: 6-frame shot at 4.30 s, true peak −0.5 dBTP,
  end hold under 0.1 s.
- One OCR line contained a site-masked email; it is replaced with `[redacted email]`.
