---
id: VDI-QG
title: "vdi check: the manifest-free pre-check"
topic: docs
status: Draft
last_updated: 2026-11-23
---

# `vdi check` — the quick pre-check

`vdi check` is a fast first pass on a **rendered** video that needs **no manifest**. Use it on
every draft render, and on any video the release gate has no manifest for. It does **not** replace
the release gate (`vdi release`), which checks declared evidence beats, captions
against two ASR models and word endings against the source audio. Release still needs: release
gate exit 0 → independent review READY → owner approval (see `AGENTS.md`).

```bash
pip install -e .                                  # + ffmpeg, tesseract on PATH
vdi check final.mp4 --platform youtube-shorts            # exit 0 pass / 1 fail / 2 couldn't run
vdi check final.mp4 --platform instagram-reels --ads     # stricter ad safe zone
vdi check final.mp4 --script s.md --transcript t.txt --accepted a.txt   # said vs scripted
vdi selftest                          # proves every check on synthetic known-bad files (~90 s)
vdi platform tiktok                   # platform spec with sources
vdi log-lesson --what … --rule … --check … --source …
```

MCP (`vdi mcp`): `vdi_quick_gate`; `vdi_log_lesson` when `VDI_ENABLE_WRITE_TOOLS=1`.

## Checks

| Check | Measures on the render | Fails when | Proven by fixture |
|---|---|---|---|
| G-FORMAT | ffprobe | resolution ≠ platform, not H.264/yuv420p, VFR, not AAC 48 kHz, moov not first | bad_format |
| G-DURATION | container duration | over the platform ceiling | good with 5 s ceiling |
| G-LOUDNESS | ebur128 integrated | outside −14 ±0.5 LUFS | bad_loud |
| G-TRUEPEAK | ebur128 true peak | above −1.5 dBTP | bad_loud |
| G-BLACK | near-black uniform full or half frames | > 1 frame (except the final second) | bad_black |
| G-SHOT-MIN | frame-difference cuts; ≥ 3-frame motion runs = one transition | any shot < 12 frames | bad_flash (good contains an 8-frame animated slide and must pass) |
| G-TAIL | last speech (full band or ≥ 3.5 kHz) → end | outside 0.58–0.85 s | bad_tail |
| G-DIGITAL-ZERO | exact-zero sample runs | any ≥ 4 ms inside the programme | bad_zero |
| G-JOIN-LEVEL | speech level and room-tone floor ±1 s at each cut / `--joins` | speech step ≥ 2 dB or floor step ≥ 4 dB | bad_join |
| G-TEXT-EDGE | OCR word boxes (2 fps, normal + inverted) | text within 16 px of left/right edge for ≥ 2 samples | bad_edge |
| G-TEXT-SAFE | OCR word boxes vs keep-clear zone | text-like words in the zone for ≥ 2 samples | bad_safe |
| G-TEXT-SIZE | tallest word per OCR line | < 28 px text held ≥ 1.5 s | bad_small |
| G-PII | OCR text | emails (incl. masked), key shapes, codes, PLAN_REQUIRED / RATE_LIMITED | bad_pii |
| G-FACE-MATCH | median CIELAB of detected face, ±3 frames per side of each cut | ΔE76 ≥ 3.5 (ΔE > 20 → WARN; < 50% of cuts measured → WARN, never PASS) | bad_face |
| G-SCRIPT-DIFF | word diff of supplied transcript vs script | any deviation not owner-accepted; NOT_RUN without a transcript | bad_script |

House caption zone (organic): clear top 8%, bottom 20%, left 4%, right 12%. Ad zones per platform
are in `vdi/data/platforms.yaml`, and every number there carries a source (`vdi/data/sources.yaml`)
and a status (verified / secondary / house / seed).

## Real footage

`docs/quick-check-v3.md`: all five AX v3 renders FAIL, with the eye-verified findings listed. Two
false-positive classes were found on real footage and fixed (animated transitions read as cuts;
face-detector misfires). Weakest check: G-FACE-MATCH (scikit-image detector measures 0–30% of
cuts on AX footage; low coverage reports WARN).

## Limits

No ASR (pass a transcript from two agreeing models), no evidence-beat semantics, no word-ending
comparison against the source take, and no stillness tracking of evidence lines. Those belong to
the release gate.
