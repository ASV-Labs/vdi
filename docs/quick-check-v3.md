---
id: VDI-QG-PROOF
title: "Quick gate on the five AX v3 files"
topic: docs
status: Draft
last_updated: 2026-11-23
---

# Quick gate on real footage: AX v3

Release-gate proof on v4: `docs/release-gate-proof-v4.md`. This file covers `vdi check`.

Synthetic proof: `vdi selftest` (one known-good and one known-bad fixture per check; all pass).
This file records the gate on **real** known-bad renders, so we know which checks are proven on
footage and which are proven only on fixtures.

## Run 1 — AX-01…05 edit v3 (2026-11-23)

Files: `AX-0N-edit-v3.mp4` (1080×1920, 30 fps, 40.8–47.0 s; footage not published),
platform `youtube-shorts`, organic zone, no transcript. The v4 finals named in VDI-LESSONS-001
were not on the MacBook, so v3 was used. VDI-LESSONS-001 records v1–v3 as defective (unreadable text, late zooms,
cropped lines, ends on the word).

**Verdict: FAIL on all five** (exit 1). Raw JSON reports are not published (they contain OCR text of a test account's email). The G-FACE-MATCH column reflects the re-run after the face-check fix below.

| Check | AX-01 | AX-02 | AX-03 | AX-04 | AX-05 | Verified how |
|---|---|---|---|---|---|---|
| G-TRUEPEAK (≤ −1.5 dBTP) | −0.5 FAIL | −0.5 FAIL | −0.4 FAIL | −0.7 FAIL | −0.4 FAIL | measured (ebur128) |
| G-TAIL (0.6–0.8 s) | 0.11 FAIL | 0.08 FAIL | 0.11 FAIL | 0.21 FAIL | 0.39 FAIL | matches VDI-LESSONS-001 §2.5 "ended on the word" |
| G-SHOT-MIN (≥ 12 fr) | FAIL | FAIL | FAIL | FAIL | FAIL | **eye-verified** AX-01 4.30 s: 6-frame punch-in, then a cut to another take; AX-01 33.2 s: two jumps within 3 frames |
| G-JOIN-LEVEL (< 2 dB) | FAIL | FAIL | FAIL | FAIL | FAIL | measured 2.3–3.6 dB steps; **not yet ear-verified** |
| G-TEXT-EDGE (≥ 16 px) | FAIL | FAIL | FAIL | FAIL | FAIL | **eye-verified** AX-01 20.5 s: page cropped both sides ("Gemini" cut at the right, "Your" at x = 0) |
| G-TEXT-SAFE (house zone) | FAIL | FAIL | FAIL | FAIL | FAIL | **eye-verified** AX-01 20.5 s: headline in the top 8%; the caption also sits over page body text (manual check) |
| G-TEXT-SIZE (≥ 28 px) | FAIL | FAIL | FAIL | FAIL | PASS | measured 22–27 px body text held 1.5–4.5 s; matches VDI-LESSONS-001 §4 "unreadable text in v1–v3" |
| G-PII | FAIL | PASS | PASS | PASS | PASS | **eye-verified** AX-01 25.5 s: the masked test-account email from VDI-LESSONS-001 §3.4, still on screen in v3 (OCR read the site-masked address and matched the email pattern) |
| G-FACE-MATCH (ΔE < 3.5) | WARN* | FAIL 4.4 | FAIL 10.4/11.8 | NOT_RUN | FAIL 15.4 | AX-02 25.9 s pickup mismatch **eye-verified** in an earlier pass (brighter, softer, different wall) |
| G-FORMAT, G-DURATION, G-LOUDNESS, G-BLACK, G-DIGITAL-ZERO | PASS | PASS | PASS | PASS | PASS | v3 doesn't contain these defects; the black panel and 8 ms dropouts appeared in v4 |
| G-SCRIPT-DIFF | NOT_RUN | | | | | no transcript supplied |

\* AX-01's face was measured at 8 of 27 cuts. Since the coverage rule, a minority-coverage result is WARN, not PASS.

## False positives found on real footage, and fixed

1. **Animated split transitions read as cuts.** AX-01 at 10.87 s: the face shrinks to the bottom
   while the page slides in, giving 6 consecutive high-change frames, which were reported as six
   1-frame shots. **Fix:** a run of ≥ 3 consecutive high-change frames is one transition; runs of
   1–2 stay cuts, so 1- and 2-frame flashes are still caught. The good fixture now contains an
   8-frame animated slide and must pass.
2. **Face detector misfires.** Values of ΔE 28–58 came from the detector picking non-face regions
   (eye-checked: AX-01 24.0 s is the same take on both sides). **Fix:** minimum face size of 10%
   of frame width; a skin-tone plausibility filter; a median over up to 3 frames per side;
   ΔE > 20 → WARN ("check by eye"), never FAIL or PASS; under 50% cut coverage → WARN.

## What is still unproven on real footage

- G-BLACK, G-DIGITAL-ZERO: proven on fixtures only. Run the gate on the v4 renders (black panel and
  8 ms dropouts per L1) when they're available.
- G-JOIN-LEVEL: the measured steps match L1's magnitudes but need an ear check at the flagged
  timestamps.
- G-FACE-MATCH coverage is low (0–30% of cuts) with the scikit-image LBP detector. A better
  detector (e.g. OpenCV YuNet, which needs its ONNX model vendored) is the next improvement.
- G-SCRIPT-DIFF needs transcripts from two ASR models.
