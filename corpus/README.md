---
id: VDI-CORPUS
title: "The VDI corpus: how to read it, and what applies to every pack"
topic: corpus
status: Seed
last_updated: 2026-11-23
---

# The corpus

13 topic packs plus the lessons they were built from. Licensed CC BY 4.0 (see `LICENSE` here); the
code in `vdi/` is MIT. Everything below applies to **every** pack and is written once here instead of
being copied into each.

## Status — read this first

- **Agent-written, not yet reviewed by a human.** Every pack is status **Seed**: complete in structure,
  thin in evidence. Nothing here may claim Reviewed, Approved or Final until the owner reviews it.
- **One series.** All internal evidence comes from the AX series: AX-01…AX-05, five 40–47 s vertical
  shorts, one presenter, one room, one product, edits v1–v5, Nov 22–23 2026.
- **No watch-time data yet.** None of these videos has posted, so no rule is backed by retention numbers.
- `vdi validate` prints the current provenance count and grounded ratio.

## Provenance labels

Every claim carries one:

- **`[AX <id>: <where>]`** — measured internally on the AX series. The id resolves to a row in that pack's
  `sources/sources.json`. Records that live outside this repo are cited as `ax:<record>` (e.g.
  `ax:V5-ADDENDUM.md`): internal production records — edit notes, review notes, measurement scripts — that
  are **not published** (they contain raw footage paths and unreleased material). The two lessons files and
  the v4 gate receipts *are* published (`corpus/lessons/`, `examples/v4/`).
- **`[SRC <id>]`** — from a cited document (platform help page, standard, guide), with url and access date.
- **`[UNVERIFIED]`** — a house rule or rule of thumb that has not been measured.

Never invent a number. Thin evidence is allowed only when it is labelled.

## Shared AX sources (used by most packs)

| id | what it is | where |
|---|---|---|
| lessons-001 | VDI-LESSONS-001: what went wrong on AX, the rule, the check | `corpus/lessons/VDI-LESSONS-001_AX_series.md` |
| ax-v5 | Independent reviewer's findings on the v4 edits, consolidated: per-short blockers with timestamps, tool fixes T1–T3 | `ax:V5-ADDENDUM.md` (not published) |
| ax-reviewer | Independent reviewer's working notes and measurement scripts (v4): ASR passes, clipping, level steps | `ax:review-independent/` (not published) |
| ax-editnotes | The editor's own measurements, v2–v4: face sharpening benchmark, denoise floors, true peak after AAC, holds | `ax:out/EDIT-NOTES.md` (not published) |
| ax-gr4 | AI review 4 of v4 in Google AI Studio (real video + audio input), each claim verified against frames; blind audio A/B | `ax:GEMINI-REVIEW-4.md` (not published) |
| vdi-gate-proof | The release gate run on the five known-bad v4 files | `docs/release-gate-proof-v4.md`, `examples/v4/receipts/` |

## How to use a pack

1. **`RULES.md`** first — Always / Never / Prefer, each rule with an id (`VDI-NN-Rnn`), a check and its
   provenance. This is the only place a rule's full text lives.
2. **`KNOWLEDGE.md`** — principles, patterns (`VDI-NN-Pnn`), anti-patterns (`VDI-NN-Ann`), implementation
   notes, glossary.
3. **`CHECKLISTS.md`** — build checklist (while producing), design-review questions (for the independent
   reviewer: answer each with a timestamp, frame or measurement; an unanswered question is a FAIL for the
   review), QA checks the gate runs for this topic, red flags (a reason to look, not proof of a defect),
   and the evaluation form for a release candidate.
4. **`EXAMPLES.md`** — real AX cases that failed or worked, with file and timestamp; commands and manifest
   fragments.
5. **`README.md`** — what the pack covers, and its **Known gaps**: check them before relying on a number.

Checklists and examples cite rules as "first clause… (VDI-NN-Rnn)"; `vdi validate` fails if a rule is
restated in full anywhere but `RULES.md`, or if a cited id doesn't exist.

## Glossary (all packs)

- **AX series** — AX-01…AX-05, the five shorts above; the evidence base for this corpus.
- **Rendered file** — the final mp4 as it will be posted; the only thing either gate measures.
- **Seed** — status of every pack: structurally complete, evidence thin, not reviewed by a human.
- **Evidence beat** — a span where a spoken claim must be proven by a readable line on screen, declared
  in the release-gate manifest (time window, exact text, run id, source label).

## What the release gate cannot check (applies to every pack)

`vdi release` measures the mp4 against the manifest. It cannot tell:

- whether a face looks plastic or haloed (no reliable metric; needs eyes);
- whether a voice sounds natural, warbly or pumped (needs ears or a blind A/B);
- proper nouns — both ASR models mishear them, so they are listed for a human listen, not passed or failed;
- whether on-screen material is a real run (it checks the declared run id and visible source label, not
  the truth of the run);
- whether a claim is true (it checks that the declared proof text is readable while the claim is spoken);
- a caption drawn over the face during a transition;
- anything outside the declared evidence beats — a beat the manifest forgets is not checked.

So "final" always needs three locks: the gate exits 0 on the exact file, an independent review says
READY, and the owner says so himself.

## Leads not yet used

Found in searches but not fetched or cited by any pack yet (candidates for the next pass):

- Netflix English (USA) Timed Text Style Guide — caption line length, reading speed, line breaks
- Netflix Timed Text Style Guide: General Requirements — minimum event duration, gaps, shot-change timing
- BBC Subtitle Guidelines (bbc.github.io/subtitle-guidelines) — reading rate, line breaks, sync
- W3C WCAG 2.2 Understanding SC 1.2.2 Captions (Prerecorded)
- Meta Business Help: ad specs — official Reels safe-zone percentages
- YouTube Help: recommended upload encoding settings
- Meta Marketing API: Reels ads
- TikTok TopView ad specifications
- EBU R 128 loudness recommendation
- AES TD1004 streaming loudness recommendation
- ITU-R BS.1770 loudness and true-peak algorithm

(The quick check's platform table, `vdi/data/platforms.yaml`, already cites several of these with access dates.)
