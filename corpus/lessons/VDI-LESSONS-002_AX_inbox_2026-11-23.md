---
id: VDI-LESSONS-002
title: "AX lessons inbox, folded in 2026-11-23"
status: Living document. Append; never delete a lesson, mark it superseded.
owner: ASV Labs - Video Design Intelligence
last_updated: 2026-11-23
source: ax:LESSONS-INBOX.md (append-only inbox written by the agents editing AX v5), read 2026-11-23 ~07:20 PT, seven entries dated 2026-11-23.
---

# Lessons from the AX inbox (v5 work), 2026-11-23

> Note (2026-11-23, later): the coordinator merged 8.1-8.4, 8.6 and 8.7 into VDI-LESSONS-001 (sections 1.1, 1.5, 2.5, 3.3, 3.6), synced here from `ax:VIDEO-LESSONS.md`, which is the source of truth for merged lessons. This file stays as the dated inbox record.

Each entry is summarised from `ax:LESSONS-INBOX.md` (that file is the primary record; it lives
outside this repo). Format as in VDI-LESSONS-001: what happened -> rule -> check. Where an entry refines a
VDI-LESSONS-001 rule, that is noted.

## 8.1 Evidence lines cropped at the frame edge (refines 3.3)
- **What happened:** v4 zoomed wide terminal recordings until the spoken line reached 28 px, pushing the start
  or end of the line off frame (AX-05 26.6 s FAIL label off the left edge; AX-04 27.3 s "changed ...
  sample-revenue.csv" cut).
- **Rule:** never zoom a wide recording to reach text size. Re-render the saved asciicast in a narrow terminal
  (38-40 columns, 39 px font at 1080 wide gives 28-30 px cap height) and diff the replayed text against the
  saved run output. Record terminals at about 40 columns in the first place.
- **Check:** OCR the rendered frame; the declared line is read whole, its ink sits >= 16 px inside the frame
  and left of the right 12%, glyph height >= 28 px. (Implemented in `video_gate.py` check_evidence.)

## 8.2 Narrow re-render garbles typed commands
- **What happened:** replaying a cast at fewer columns than it was recorded showed typed commands overwriting
  themselves, because readline had emitted " \r" wrap pairs at the original width (AX-04 beat6/beat7 casts).
- **Rule:** strip only the readline wrap pairs for display, say so in the edit notes, and diff the replayed
  text with the saved output so nothing else changed.
- **Check:** replayed plain text == saved run text (byte comparison after joining wrapped rows).

## 8.3 Web evidence too small unless captured at phone width (refines 3.3)
- **What happened:** 12-16 px page text captured at 540 CSS px could only reach 28 px in a 1080 frame by
  cropping the page sideways (AX-03 Alstead rows, AX-04 GitHub README/PR).
- **Rule:** capture at the CSS width where the needed line reaches 28 px inside x <= 950 (290-430 CSS px,
  device scale 3-5), so the page reflows instead of being cropped.
- **Check:** the same OCR evidence check; headings and commands may not touch either frame edge.

## 8.4 Word endings cut because the cut threshold was absolute (refines 2.5)
- **What happened:** pieces ended 0.17 s after the last frame above -38 dBFS with a 60 ms fade; quiet final
  /s/, /ts/, /st/ were cut ("faceplants", "rest.", "first.", "not a pass.").
- **Rule:** find the end of a piece on two envelopes of the source (cleaned full band, raw audio above
  3.5 kHz), each with a threshold relative to that file's own floor; fade after both are quiet; fade
  >= 120 ms.
- **Check:** locate each piece end of the final in its source by cross-correlation; fail if the source keeps
  sounding 60-450 ms after the final goes quiet. (Implemented in `video_gate.py` check_word_endings.)

## 8.5 A QA gate that reads the plan passes by construction (restates 5.3)
- **Rule:** every gate check measures the rendered mp4; the plan may only say what should be there. Keep a
  known-bad file and require the gate to fail it before trusting a pass.
- **Check:** run the gate on the previous rejected version; it must fail and name the reviewer's blockers.
  (Done for v4: `docs/release-gate-proof-v4.md`.)

## 8.6 Screen recordings can start on a blank frame
- **What happened:** `screens/agent/ax01-signin-browser.mp4` is white until about 1.0 s; a shot starting at
  t_in 0.6 would have opened on a white flash.
- **Rule:** look at the first and last frame of every clip range before using it; start after the page has
  painted.
- **Check:** no blank panel for 2-11 frames, plus per-panel scene-change detection (no shot < 12 frames).
  Note: the VDI gate's blank-panel check looks for near-black rows; a white flash is not detected yet
  (gap recorded in `05_Editing_and_Pacing/README.md (Known gaps)`).

## 8.7 Three screens cannot each hold 1.6 s inside a 4.3 s spoken list
- **What happened:** AX-01 "Guidance, tested templates, design checks." is 4.3 s; three evidence screens cut
  on the words got 1.3 s each, under the 1.6 s reading time.
- **Rule:** when scripting, budget 1.6-2 s of picture per on-screen line. For a fast spoken list, start the
  first screen on the previous phrase, show one screen with all the items, or slow the read.
- **Check:** measured still-and-lit time of each evidence line in the rendered file >= 1.6 s.

---

*Entries below were added to the inbox after the coordinator's merge (read 2026-11-23, inbox lines 46-65).*

## 8.8 Black frame at a voice-over join (frame time vs rounded cut time)
- **What happened:** AX-01 v5 first render had 2 near-black frames at 47.57 s; v4 had the black camera panel at
  20.07 s. Frame k is at k/30 = 47.566666 s, the cut was stored as 47.5667 s, so the frame on the cut was drawn
  as the previous (camera) shot while the camera track was already black.
- **Rule:** assign frames to shots and segments by frame index, or compare with a small epsilon after the frame
  time; never compare k/fps with a rounded cut time.
- **Check:** per-frame mean luma (< 8 = black) of the whole frame and of the camera panel on the rendered mp4;
  blank for more than 1 frame fails. (VDI gate: check_blank.)

## 8.9 "Room tone" bed was a loop of speech fragments
- **What happened:** v5 first prep took the quietest 0.8 s of the assembled programme as room tone; a tightly cut
  programme has no 0.8 s without speech, so the loop carried word tails at about -25 dBFS under everything. Both
  ASR models then heard spurious plurals ("works", "contrasts", "lengths", "cards") and the gate saw sound at
  every join and after the last word.
- **Rule:** take room tone from the source take (a real pause, through the same clean-up chain), require its
  loudest 10 ms frame to be near the floor (here -69 to -71 dBFS before gain), and lay it at the programme's own
  floor level.
- **Check:** floor between phrases >= 30 dB under speech, no digital zero; the 0.5 s after the last word below
  speech -30 dB.

## 8.10 Camera shot or old screen showing for a few frames around a voice-over piece
- **What happened:** shots were timed from word positions, joins from the audio cut list; where a shot mark landed
  2-13 frames from a join the picture changed twice (AX-01 4.40/4.58 s, AX-04 41.10/41.36 s, the v4 flash
  shots), and where a voice-over piece began under a camera shot the previous screen came back for half a second.
- **Rule:** snap a shot start to any on-camera join within 12 frames; a screen that takes over at a voice-over
  piece starts exactly with the piece; a camera shot never starts inside a voice-over piece.
- **Check:** per-panel scene-change detection on the render; fail any stretch under 12 frames between two picture
  changes. (VDI gate: check_shots.)

## 8.11 Hide half-cut neighbours instead of cropping into them
- **What happened:** at 28 px text size a phone-width page shows only about 310 CSS px of height, so the rows
  above and below the spoken line were cut through (AX-03 "it." fragment, half a button, half a heading).
- **Rule:** mask the capture to whole rows or blocks around the evidence (a window of source rows on the page's
  own background), and start terminal views on a row boundary.
- **Check:** by eye at 540x960 on the mid-frame of each screen beat: no glyph row cut by the panel edge. (Not in
  the VDI gate yet.)
