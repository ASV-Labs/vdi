---
id: VDI-11-SOURCES
title: "11_Review_and_QA: sources"
topic: 11_Review_and_QA
status: Seed
last_updated: 2026-11-23
---

# 11_Review_and_QA — sources

Generated from `sources.json` (the source of truth). Kinds: internal-evidence = an AX production record (cited as `ax:<record>`; not published), platform-doc = the platform's own page, secondary = third-party reporting. Every AX and SRC provenance label in this pack resolves to a row below.

| id | kind | credibility | title | where |
|---|---|---|---|---|
| ax-gr1 | internal-evidence | internal-unreliable-reviewer | Gemini review 1 of the raw takes (gemini.google.com, transcript-only) | ax:GEMINI-REVIEW-1.md (accessed 2026-11-23) |
| ax-gr3 | internal-evidence | internal-unreliable-reviewer | Gemini review 3 of v2 finals (transcript-only), with Claude's verification | ax:GEMINI-REVIEW-3.md (accessed 2026-11-23) |
| ax-gr4 | internal-evidence | internal-measured | Review 4 of v4 (Google AI Studio, real video+audio input), verified by Claude; blind audio A/B | ax:GEMINI-REVIEW-4.md (accessed 2026-11-23) |
| ax-qa-v4 | internal-evidence | internal-counterexample | shortskit v4 QA gate (qa_gate.py) and README | ax:shortskit/qa_gate.py, shortskit/README.md (accessed 2026-11-23) |
| ax-reviewer | internal-evidence | internal-measured | Independent reviewer's working notes and measurement scripts (v4) | ax:review-independent/meas/NOTES-working.md and review-independent/scripts/ (accessed 2026-11-23) |
| ax-v5 | internal-evidence | internal-measured | V5 addendum: independent reviewer's findings on v4, consolidated | ax:V5-ADDENDUM.md (accessed 2026-11-23) |
| lessons-001 | internal-evidence | internal-measured | VDI-LESSONS-001: Short-form video production lessons (AX series, Nov 22-23 2026) | corpus/lessons/VDI-LESSONS-001_AX_series.md (this repo) (accessed 2026-11-23) |
| vdi-gate-proof | internal-evidence | internal-measured | VDI gate proof run on the five known-bad v4 files | docs/release-gate-proof-v4.md and examples/v4/receipts/ (this repo) (accessed 2026-11-23) |
