---
id: VDI-010
title: "Release gate: what it measures and how to run it"
topic: docs
status: Draft
last_updated: 2026-11-23
---

# The release gate (`vdi release`)

`vdi release` (code: `vdi/release.py`) is the first of the three locks in `AGENTS.md`: no "final" until it exits 0 on the
**rendered** mp4, an independent review says READY, and the owner says so himself.

It exists because the AX v4 editor's gate passed 22/22 on files with 19 blocking defects: its checks were
computed from the edit plan, compared the plan with itself, and excused misheard words with tolerance
lists (`VDI-LESSONS-001` §5.3; evidence in `ax:V5-ADDENDUM.md` and `ax:shortskit/qa_gate.py`).
This gate reads nothing from an edit plan.

## Run

```bash
vdi release <final.mp4> --manifest <manifest.json> [--out DIR] [--cache DIR]
```

- Exit 0 = every check PASS (WARN allowed); 1 = at least one FAIL; 2 = could not run.
- Writes `<id>.gate.json` and a one-page `<id>.gate.md` (default `./gate-results/`).
- Install: `pip install -e ".[release]"` (faster-whisper, opencv, scipy) plus ffmpeg and tesseract 5 with English
  data. `vdi release` checks all of these first and prints the install line for anything missing.
- First run downloads the Whisper `small.en` and `medium.en` models (~2 GB, Hugging Face cache) and the YuNet
  face model (opencv_zoo, ~230 KB, `~/.cache/vdi-gate/models/`). Neither is in the repo. Audio is passed to
  faster-whisper as a float32 numpy array, so no `av` decode is needed.
- Runtime on 2 CPU cores, no GPU: about 8-10 minutes for a 40-47 s short (OCR of every frame at 10 fps and
  two ASR models dominate). OCR and ASR results are cached per file hash, so re-runs after a manifest
  change take about a minute.

## The manifest

Schema: `vdi/release_data/manifest.schema.json`. It declares **intent**: the script text, proper nouns, owner-accepted spoken
deviations (the only tolerance allowed), the caption band, the source audio files, and the evidence beats
(time window, exact text that must be readable, run id, source label, claim id). Write it before the edit,
from the script and the claim ledger. Examples: `examples/v4/manifests/AX-0N-v4.manifest.json`.

## What each check measures (all on the rendered file)

| Check | How | Threshold |
|---|---|---|
| container | ffprobe | 1080x1920, 30 fps, H.264 + AAC, 15-60 s |
| loudness and true peak | ffmpeg `ebur128=peak=true` on the final AAC | -14 +-0.5 LUFS, <= -1.5 dBTP |
| shot lengths | frames at 180x320; > 35% of a region (whole / upper half / lower half) changing by > 12 levels = a change; consecutive changed frames = one transition | no shot < 12 frames |
| black panels | rows that just went near-black (mean < 8, max < 40), >= 20% of the height | > 1 frame between content fails |
| face continuity | YuNet face box, skin pixels in YCrCb, mean Lab 3 frames either side of every picture change and audio join | skin dE < 3.5 |
| word endings | final aligned to each source file by cross-correlation of 0.5 s windows; at each segment end, how long the source's speech (full band or >= 3.5 kHz, > 9 dB over floor) continues past the last reproduced frame, bridging stop closures shorter than 130 ms | lost tail < 60 ms before a pause |
| ending hold | last 10 ms frame within 28 dB of speech level (full band or >= 3.5 kHz) to the file end | 0.6-1.0 s, last 100 ms decayed |
| inter-sentence gaps | at each sentence end in the medium.en transcript, longest run of frames 25 dB below speech | >= 0.12 s |
| join level steps | joins found by the alignment; power of speech frames in 1 s either side | < 2 dB |
| dropouts | runs of exact-zero samples at 48 kHz | none > 1 ms |
| script | small.en and medium.en both transcribe the final; words both agree on are diffed against the script (with owner-accepted deviations applied) | every difference accepted; disagreements reported |
| captions | tesseract on the caption band (bright-pixel mask) at 10 fps; a band row is a caption only if half its words were spoken nearby; words kept if read in >= 40% of an event's frames; each word must be heard by both models | no caption word unheard or heard by one model only |
| caption timing | first OCR frame of a caption vs its agreed word | WARN only (> 0.35 s late) |
| caption safe area / clearance | caption word boxes; whole-frame OCR rows near them | top 8%, bottom 20%, right 12% clear; >= 48 px from other text |
| evidence lines | whole-frame tesseract at 10 fps in the beat window; best row (or two stacked rows for wrapped titles) covering >= 90% of the expected text; edges >= 16 px; outside top 8% / bottom 20%; glyph height; drift of the matched words | still, readable, >= 28 px for >= 1.6 s |
| run ids and labels | adjacent beats in one claim with different run ids need a declared source label that OCR can read | label readable in >= 50% of the beat's frames |
| PII / plan walls | regex over whole-frame OCR of every sampled frame: emails incl. masked, 6-digit codes next to "code", key/token prefixes, PLAN_REQUIRED, RATE_LIMITED | none |

Thresholds and their basis (AX measurement, source, or house rule) are in `vdi/release_data/gate-spec.json`.

## What it cannot check

Listed in `vdi/release_data/gate-spec.json` (`cannot_check`): plastic face or halo; voice naturalness; whether a proper noun
was said right (both ASR models mishear names, so they are reported for a human listen); whether footage
really comes from the declared run; whether a claim is true; captions drawn over the face during a
transition; 0 vs O in a font; layout churn and pacing feel; anything the manifest does not declare. Its
false-positive rate on a good file is unknown: no known-good reference file exists yet.

## Proof

The gate was run on the five known-bad AX v4 files. Every one FAILs; caught and missed blockers per file are
in `docs/release-gate-proof-v4.md`, raw reports in `examples/v4/receipts/`.
