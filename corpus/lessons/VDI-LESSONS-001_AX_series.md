---
id: VDI-LESSONS-001
title: Short-form video production — lessons learned (AX series, Nov 22–23 2026)
status: Living document. Append; never delete a lesson, mark it superseded.
owner: ASV Labs — Video Design Intelligence
last_updated: 2026-11-23
source: AX-01…AX-05 (five 40–47 s vertical shorts, the presenter on camera + real product screens), edits v1→v5, three AI reviews, one independent agent review, one blind audio A/B.
---

# Short-form video: what went wrong, and the rule that prevents it

Read this before scripting, filming, editing or reviewing any ASV Labs video. Every rule below
came from a real defect that shipped to at least one review round. Each has: **what happened →
rule → how to check it**.

---

## 1. Script and board

**1.1 The board truncated every spoken line.**
Our internal board generator ("Build board from script") cuts each SAY/DO/SHOW to three wrapped lines and appends
"…". The presenter read the boards exactly as written, so 18 lines across five shorts stopped
mid-sentence and needed pickups.
- **Rule:** read from the script doc, never the board, until the board bug is fixed (reported internally, Nov 22). After the fix: every board SAY must equal the script SAY character for
  character.
- **Check:** diff board text against script text before the shoot. Any "…" on a SAY line = stop.
- **Rule (Nov 23):** one SAY line per beat, 70 characters or less, so the board can't cut it
  even with the bug. Split a long beat into 4a/4b/4c instead of writing a longer line. Our later scripts follow this; a script check can enforce it before any board is built.

**1.2 Write lines short enough to say in one breath and to caption in two short lines.**
Long SAY lines were the ones that got truncated, rushed, and mis-captioned.
- **Rule:** ≤ ~12 words per sentence; one idea per beat; each beat names its screen (SHOW) and
  where the eye should land.

**1.3 What he says wins over what was written.**
the presenter ad-libbed ("an Army soldier" for "Army vet", "calls back a design contract",
"Probably doesn't exist."). Captions that followed the script instead of the audio were wrong
("I've built" vs said "I build"; "the ledger" vs said "a ledger").
- **Rule:** captions transcribe the audio, verbatim. Script deviations are listed for the owner
  to accept or re-record; editors never "fix" them silently, and never caption words not said.
- **Check:** diff the final transcript against the script; every difference is either on the
  owner-accepted list or fails.

**1.4 Every claim on screen must be shown by real footage from the same run.**
- **Rule:** before recording, list each spoken claim → the exact screen line that proves it →
  the run it comes from. "Fixes what fails" needs a run where something failed and was fixed.
  Design the demo so a real fail is likely (we had to re-record AX-01 because the first run
  passed 17/17 and could not support the line).

**1.5 Budget picture time per on-screen line when scripting.**
AX-01 "Guidance, tested templates, design checks." is 4.3 s; three evidence screens cut on the
words got 1.3 s each, under reading time.
- **Rule:** 1.6–2 s of picture per on-screen line. For a fast spoken list, start the first
  screen on the previous phrase, show one screen holding all the items, or slow the read.
- **Check:** measured still-and-lit time of each evidence line in the render ≥ 1.6 s.

---

## 2. Recording (talking head)

**2.1 Webcam footage is soft and can't be fixed in post.**
1620×1080 webcam cropped to 9:16 is a ~2× upscale. Sharpening produced a plastic look and a
halo on the wall; Real-ESRGAN was no better and cost 8.7 s/frame (~6.7 h for five shorts).
- **Rule:** phone rear camera, 4K, held vertical (or a real camera), eye level, light in front at
  ~45°. Fix softness at capture, not in the edit.

**2.2 Room echo.** The office is reflective; the raw takes are roomy with steady hiss.
- **Rule:** soft furnishings or a blanket behind the camera; mic close (lav or phone ≤ 30 cm).
- **Post:** DeepFilterNet (current chain) was ranked best in a blind A/B over raw and over the
  earlier gate/denoise chain. Do not push noise/echo removal further — the earlier, harder chain
  produced clicks in pauses, pumping and cut word endings.

**2.3 Pickups must match the original take.**
Pickups shot later were darker, warmer, softer and framed against a different part of the wall
(skin ΔE 6.3–9.6 at the cut vs 0.2–3.1 within a take).
- **Rule:** same spot, same framing (mark the tripod), same light (close curtains / same time of
  day), same shirt (note it per short), same mic. Shoot pickups the same day if possible.
- **Post check:** skin colour ΔE < 3.5 across every take↔pickup cut; grade pickups to the take.

**2.4 Voice memos ≠ webcam mic.** Voice-only pickups from a phone memo sound closer/drier.
- **Rule:** record voice-only pickups on the same mic and spot as the take; if not, match EQ and
  short-term loudness within 1 LU at the join and keep room tone running through it.

**2.5 Deliver the last word fully, then hold.**
Final consonants (/s/, /ts/, /st/) are quiet and were cut ("faceplants", "rest", "not a pass").
- **Rule (performer):** finish the word, then hold still and silent for 1 s.
- **Rule (edit):** detect word ends on the SOURCE, on a high-passed (≥ 3.5 kHz) envelope as well as
  full-band, each with a threshold relative to that file's own noise floor (an absolute −38 dBFS
  cut the tails);
  fade only after the consonant ends; ≥ 120 ms tail fades. End every short 0.6–0.8 s after the
  last word, audio decaying into room tone.
- **Check:** find each piece end of the final file in its source by cross-correlation; fail if
  the source keeps sounding 60–450 ms after the final goes quiet.

**2.6 Say each line twice, with a pause.** It made cutting and pickups possible. Keep doing it.

---

## 3. Screen footage

**3.1 Never fake product output.**
Rejected on Nov 18 (OC-01 v4 showed agent lines no real run produced) and enforced through AX.
- **Rule:** every terminal line, UI and result on screen comes from a real run or a live page,
  captured that day. Save the verbatim tool outputs (e.g. `opencode export <session>`) and the
  run's README next to the footage. No placeholders in anything called final.

**3.2 One spoken claim = one run.**
AX-01 showed the prompt from run 1 and the results from run 2; AX-04 put the repo's demo graph
(different model, different sources) between our own terminal beats as if it were the same file.
- **Rule:** each beat records its run id; adjacent beats inside one claim share a run id, or the
  frame carries a visible source label ("demo run from the lineage repo").

**3.3 Record terminals narrow, not wide.**
Zooming a wide terminal makes text big but crops lines at the frame edge ("changed evidenced
sample-reve" exactly when he says "names the source").
- **Rule:** record (or re-render the saved asciicast with shortskit/term.py) at 38–40 columns,
  ~39 px font at 1080 wide (28–30 px cap height), dark theme, clean prompt, short paths, so long
  lines wrap inside the frame. Text must stay byte-identical to the saved output.
- **Narrow replays garble typed commands:** readline emits " \r" wrap pairs at the recorded
  width. Strip only those (term.py --strip-wrap), note it in the edit notes, and diff the
  replayed text against the saved output.
- **Web pages:** capture at the css width where the needed line reaches 28 px inside x ≤ 950
  (about 290–430 css px, device scale 3–5), so the page reflows instead of being cropped.

**3.4 Personal data and plan walls.**
A site-masked email address (first letter and domain visible; redacted here) reached the cut; free-trial runs printed PLAN_REQUIRED and
RATE_LIMITED.
- **Rule:** use the approved test account; blur emails (including masked ones), codes, tokens.
  OCR-sweep every final for emails, codes, keys, PLAN_REQUIRED, RATE_LIMITED. Cut around plan
  walls unless the owner wants them shown.

**3.6 Clips can open on a blank frame.** ax01-signin-browser.mp4 is white until ~1.0 s.
- **Rule:** look at the first and last frame of every clip range before using it; start after
  the page has painted. Gate: no blank panel 2–11 frames, no shot under 12 frames.

**3.5 Label sample work.** Built demo pages carry "This is a sample page, not a customer site."
in the safe area, clear of captions.

---

## 4. Editing rules (all measured on the rendered file)

| Rule | Threshold | Why it exists |
|---|---|---|
| Evidence line fully in frame, both edges | ≥ 16 px margin, whole hold | Cropped lines in all five v4 shorts |
| Evidence line still while read | bbox drift < 6 px for ≥ 1.6 s | Panning lines (AX-04 verify readable still for 0.47 s) |
| Evidence text size | cap height ≥ 28 px at 1080 wide | Unreadable terminal text in v1–v3 |
| Zoom arrives on the word | pre-lap if speech moves on | 1.1 s holds in v3 |
| Captions own a band | nothing behind them but a plain panel or face/torso | Captions over terminal lines, pages, cards (v4) |
| Caption clearance | ≥ 48 px from lower thirds / end-card text | Collisions with @ASaltyVet card, Alstead URL, end card |
| Caption safe area | top 8 %, bottom 20 %, right 12 % clear | Platform UI |
| Caption timing | within ~0.3 s of the word | "or inferred." 0.42 s late |
| Shortest shot | ≥ 12 frames; no 1–3 frame flashes | Flash shots where hook meets intro (shot mark 2–3 frames after audio join) |
| Black/blank panel | ≤ 1 frame | Black camera panel before a screen arrived |
| Snap shot changes to audio joins | within 0.15 s → snap | cause of the flash shots |
| Word tails | no tail cut faster than 60 ms; fade after consonant | Cut /s/ /ts/ /st/ |
| Inter-sentence gap | ≥ 0.12 s, not longer than natural | "Rushed" joins flagged by review |
| Ending | 0.6–0.8 s hold after last word, fading | Every v4 ended ~0.13 s after the word |
| Level across joins | 1 s speech-level step < 2 dB; ≤ 1 LU at pickups | 2.0–3.2 dB at 11 joins in v4 |
| Room tone | continuous through joins, never digital zero | 8 ms dropouts at joins |
| Loudness | −14 LUFS ±0.5 integrated, true peak ≤ −1.5 dBTP on the final AAC | |
| Face grade | skin ΔE < 3.5 across face cuts | Pickup mismatch |
| Face processing | no halo, no smeared skin; soft-natural beats sharp-plastic | v4 face looked plastic |
| Layout churn | don't flip split ↔ full-frame within ~2 s | v2 cut churn |

---

## 5. Review: who to trust for what

**5.1 The Gemini web/app chat did not watch the videos.**
Attaching Drive videos in gemini.google.com delivered only transcripts; it said so on Nov 23.
Its earlier "caption misspellings" ("FACEPLATE", "NOOSE RESEARCH", "ASV LADS") and wrong
wardrobe descriptions were its own speech recognition and guesses.
- **Rule:** for AI video review use **Google AI Studio** with the video attached (it reports
  video tokens per file and quotes on-screen text exactly). Free when no API key is selected.

**5.2 Every AI review claim gets verified against frames/audio before acting.**
Even the AI Studio review mis-reported apostrophes ("links in the") at 540 px.

**5.3 The editor's own gate graded itself.**
v4 "passed 22/22" while having 19 blocking defects: caption checks compared the plan with
itself; safe area, cap height, holds were computed from the plan; "clean ending" always passed
because every piece had a fade; ASR tolerance lists excused real defects.
- **Rule:** every gate check reads the rendered mp4 (OCR of frames, envelopes vs source, shot
  detection, colour). No tolerance lists except owner-accepted spoken deviations. A word counts
  as heard only if both ASR models agree. Prove the gate: it must FAIL a known-bad file on each
  defect class it claims to catch.

**5.4 Independent review is mandatory.**
A reviewer agent that did not make the edit found what the editor and the gate missed. Run it
every release candidate.

**5.5 Audio needs ears, or a blind A/B.**
Spectrogram + transcript acceptance missed nothing in the end, but only a blind A/B (labels
hidden, AI Studio listening) established which cleanup chain was best. A human listen at every
flagged timestamp is still required before posting.

**5.6 ASR models mishear proper nouns.** "A Salty Vet", "Nous", "faceplants", "in plain"
failed in both small.en and medium.en. Keep a proper-noun list; check those by ear.

---

## 6. Logistics

- **Posting hold:** nothing is cleared until (1) the gate passes on the rendered file, (2) an
  independent review says READY, (3) the owner says so himself.
- **Cloud-agent file limits:** our cloud-drive connector capped downloads at ~10 MB and uploads at
  ~3 MB per call, so raw video moved over a local file bridge instead.
- **Review copies:** 540×960, < 2.9 MB, so Drive upload and AI review both work.
- **Naming:** `AX-03-pickup-team.m4a`, `AX-05-screen-10.mov`; versions `-edit-vN.mp4`.
- **Where things live:** one folder per series with `edits-vN/` for each round, and a working folder
  holding the edit tooling, plans, QA output and one README per screen capture (cited here as `ax:`).

---

## 7. Open questions (not yet answered)

- Does burned-in kinetic captioning (keyword colour) help or hurt watch time vs plain captions?
  No data yet; measure after posting.
- Is split-screen (screen top, face bottom) better than full-frame alternation for this format?
- What is the minimum readable hold for dense terminal text at phone size for a real viewer?
  1.6 s is a rule of thumb, not measured.
