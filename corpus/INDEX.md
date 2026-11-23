---
id: VDI-INDEX
title: "Corpus index"
topic: corpus
status: Draft
last_updated: 2026-11-23
---

# INDEX - Video Design Intelligence

Map of the corpus. Start with `AGENTS.md`, then `corpus/README.md` (how to read a pack, provenance, shared sources), the lessons, then the packs for your stage. Every topic pack is **Seed** status: structurally complete, evidence from one series, not reviewed by a human.

## Instruments

| Path | What it is |
|---|---|
| `AGENTS.md` | The contract: no final without the release gate on the rendered file, an independent review, and the owner's OK. |
| `corpus/README.md` | Status, provenance labels, shared AX sources, how to read a pack, what the gates can't check. |
| `corpus/lessons/` | VDI-LESSONS-001 (what went wrong on AX-01..05 and the rule that prevents it) and 002 (lessons from the v5 edit). |
| `vdi check` | Quick pre-check, no manifest (`vdi/check.py`, `docs/quick-check.md`). |
| `vdi release` | Release gate with manifest + two ASR models (`vdi/release.py`, `vdi/release_data/`, `docs/release-gate.md`). |
| `vdi mcp` | MCP server (stdio): search, get, brief, checklist, script lint, gate spec, quick check (`docs/mcp.md`). |
| `vdi validate` | Corpus validator: files, front matter, provenance, no duplicated rule text. |
| `examples/` | Real manifests and gate receipts (v4), the E2E release-gate output on v3. |

Each pack: `README.md` (scope + known gaps), `RULES.md` (canonical rules), `KNOWLEDGE.md`, `CHECKLISTS.md`, `EXAMPLES.md`, `manifest.yaml`, `sources/`.

## Topic packs

| # | Folder | Stages | Summary |
|---|---|---|---|
| 01 | `corpus/01_Scripting_and_Boards/` | script | How to write a short-form script and the board the performer reads from, so every line can be said in one breath, captioned in two short lines, proven on screen, and read without truncation. |
| 02 | `corpus/02_Talking_Head_Capture/` | shoot | Capture rules for the on-camera parts: what camera, light, framing, microphone and room give footage that does not need rescue in the edit. |
| 03 | `corpus/03_Pickups_and_Continuity/` | pickups | How to record and cut in replacement lines so the viewer cannot hear or see the join: same spot, light, wardrobe, framing and mic, and how to check it on the rendered file. |
| 04 | `corpus/04_Screen_Capture_and_Demos/` | screen | How to capture terminals, agent runs and web pages so every line on screen is real, from the run the words describe, readable at phone size, and free of personal data and plan walls. |
| 05 | `corpus/05_Editing_and_Pacing/` | edit | Edit rules measured on the rendered file: shot lengths, black panels, holds on evidence, word tails at cuts, gaps between sentences, endings and layout stability. |
| 06 | `corpus/06_Captions_and_On_Screen_Text/` | captions | Captions transcribe the final audio verbatim, sit in their own band inside the platform safe area, never cover other text, and are checked by OCR against what both ASR models heard. |
| 07 | `corpus/07_Audio/` | audio | Voice cleanup that does not damage words, loudness and true peak measured on the encoded file, joins that keep room tone, and listening rules for what meters cannot judge. |
| 08 | `corpus/08_Colour_and_Face/` | edit | Grade faces to match across cuts, measure it as skin dE on the rendered file, and keep face processing soft and natural rather than sharp and plastic. |
| 09 | `corpus/09_Platform_Formats/` | publish | What each platform documents about aspect ratio, length, safe zones and sound, what is only reported second-hand, and the AX house format that sits inside all of them. |
| 10 | `corpus/10_Hooks_and_Retention/` | script, edit | What the first seconds must do, how platforms measure whether viewers stay, and the hook and pacing practice that AX used, with the honest gap that nothing on AX has been posted and measured yet. |
| 11 | `corpus/11_Review_and_QA/` | review | Who and what to trust for review: a gate that measures the rendered file, an independent reviewer, an AI reviewer that actually watches the video, blind A/B for audio, and the owner's own OK. |
| 12 | `corpus/12_Claims_and_Honesty/` | script, screen, review | Every claim in a video is shown by real footage from the same run, sample work is labelled, ad-libs that change a claim go to the owner, and nothing is called final without evidence. |
| 13 | `corpus/13_Anti_Patterns/` | script, shoot, pickups, screen, edit, captions, audio, review, publish | The named failures from the AX series in one place, each with how it shows up, the rule that prevents it and whether the gate catches it. |

## Each topic folder

`README.md` · `manifest.yaml` · `README.md (Known gaps)` · `README.md (Known gaps)` · `sources/sources.{json,md}` · `KNOWLEDGE.md{overview,principles,patterns,anti-patterns,implementation-notes,glossary}.md` · `CHECKLISTS.md / RULES.md{agent-rules,build-checklist,design-review-checklist,qa-checklist,red-flags}.md` · `EXAMPLES.md{good,bad,implementation}-examples.md` · `CHECKLISTS.md`

Rule ids look like `VDI-05-R03` (topic 05, rule 3); patterns `-Pnn`, anti-patterns `-Ann`, examples `-Enn`. Any of them can be fetched with the MCP tool `vdi_get`.

## Cross-references

- Web Design Intelligence `27_Cinematic_Video` (sister corpus, read-only): real filmed footage as web design material; the real-vs-generated doctrine that `12_Claims_and_Honesty` also applies to video.
