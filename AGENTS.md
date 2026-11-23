---
id: VDI-001
title: "Agent contract"
topic: root
status: Draft
last_updated: 2026-11-23
---

# AGENTS.md — operating contract for agents making video with VDI

This repo exists so agent-made short-form videos don't ship with the defects the AX series shipped with.
It binds every agent (Claude, Codex, Cursor, anything else) that scripts, shoots, edits, reviews or
publishes video from it. `CLAUDE.md` points here.

## The one rule

**Nothing is "final" until three things are true, in this order:**

1. `vdi release <final.mp4> --manifest <manifest.json>` **exits 0 on the rendered file** — the exact mp4
   that will be posted. Keep its `.gate.md` and `.gate.json` with the release.
2. **An independent review says READY.** Independent = a person or agent that did not make the edit.
3. **The owner says so himself.** Not a bot, not a reviewer, not the editor on his behalf.

A gate pass is necessary, never sufficient. Neither gate can see a plastic face, a warbly voice, a false
claim, or anything the manifest forgot to declare (`corpus/README.md` lists the blind spots). Until all
three locks hold, the file is a release candidate (`-edit-vN.mp4`), never final.

## Every video, in order

1. **Brief.** MCP `vdi_brief(video_type, platform, duration_s, has_talking_head, has_screen_demo)`, or the
   `RULES.md` of the packs for your stages (map below).
2. **Read the lessons once.** `corpus/lessons/VDI-LESSONS-001_AX_series.md` (and 002). Every rule traces to
   them or to a cited source.
3. **Lint the script.** `vdi_lint_script(text)`: long sentences, board-truncation risk, claims with no proof
   line. Fix before recording.
4. **Write the manifest before the edit** (schema `vdi/release_data/manifest.schema.json`, examples in
   `examples/v4/manifests/`): script, proper nouns, evidence beats (time window, exact text, run id, source
   label, claim id), source audio. The manifest declares intent; the gate checks the render against it.
5. **`vdi check` on every draft render** (MCP `vdi_quick_gate`): no manifest, a few minutes, catches format,
   loudness, flash shots, black panels, ending hold, dropouts, join steps, cropped/unsafe/small text, PII and
   face-colour jumps.
6. **`vdi release` on the candidate**, then independent review, then the owner.

| Stage | Packs (`corpus/`) |
|---|---|
| script | `01_Scripting_and_Boards`, `10_Hooks_and_Retention`, `12_Claims_and_Honesty` |
| shoot | `02_Talking_Head_Capture` |
| pickups | `03_Pickups_and_Continuity` |
| screen | `04_Screen_Capture_and_Demos`, `12_Claims_and_Honesty` |
| edit | `05_Editing_and_Pacing`, `08_Colour_and_Face`, `10_Hooks_and_Retention` |
| captions | `06_Captions_and_On_Screen_Text` |
| audio | `07_Audio` |
| review | `11_Review_and_QA`, `12_Claims_and_Honesty` |
| publish | `09_Platform_Formats` |

`13_Anti_Patterns` applies at every stage. `vdi_checklist(stage)` returns the rules for one stage.

## Hard rules (from defects that shipped)

- **Never fake product output.** Every screen line comes from a real run or live page captured that day;
  one spoken claim = one run, or a visible source label.
- **Captions transcribe the final audio**, never the script. A word counts as heard only if two ASR models
  agree.
- **Gates measure the mp4, never the plan.** No tolerance lists except owner-accepted spoken deviations.
- **AI review only with the video attached**; verify every AI claim against frames and audio before acting.
- **No personal data, codes, tokens or plan walls on screen.** Use a test account; never write its address
  anywhere.
- **Never report a check as passed when it didn't run** — that is `NOT_RUN`.

## Provenance

Every claim carries `[AX <id>: where]` (measured internally on the AX series), `[SRC <id>]` (cited, with url
and access date) or `[UNVERIFIED]`. Never invent a number. Statuses are Seed (packs) and Draft (docs, gates);
nothing here is human-reviewed yet.

## Changing the repo

New defects: log them at once (`vdi log-lesson`, or MCP `vdi_log_lesson` with `VDI_ENABLE_WRITE_TOOLS=1`).
Before finishing any change: `vdi validate` (exit 0), `vdi selftest` if you touched `vdi/check.py`, and the
tests in `CONTRIBUTING.md`.

## Refusals (do these, not workarounds)

- Asked to "just post it"? Run the gate on the rendered file anyway, then ask for the independent review and
  the owner's OK. A gate run costs minutes; a bad post costs a re-edit and trust.
- Tempted to add a tolerance list because ASR mishears a word? Put proper nouns on the manifest's list (they
  go to a human listen); everything else must be heard by both models or re-recorded.
- Tempted to fill a beat with footage from another run because it looks the same? Label it on screen or
  re-record the run.
