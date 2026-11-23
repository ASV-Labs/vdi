---
id: VDI-REGISTRY
title: "Document registry"
topic: corpus
status: Draft
last_updated: 2026-11-23
---

# DOCUMENT_REGISTRY

Every governed document in this corpus with its status. Statuses are **Draft** (front door, gate, server) and **Seed** (topic packs). Nothing has been reviewed by a human; no document may be marked Reviewed, Approved or Final until the owner reviews it.

| id | document | status | depends on | notes |
|---|---|---|---|---|
| VDI-001 | `AGENTS.md` | Draft | VDI-LESSONS-001, VDI-010 | Contract: no final without gate on the render + independent review + owner OK. |
| - | `CLAUDE.md` | pointer | VDI-001 | Pointer only, no front matter. |
| - | `CONTRIBUTING.md` | pointer | VDI-001 | How a lesson becomes a rule and a gate check. |
| VDI-CORPUS | `corpus/README.md` | Seed | all packs | Shared status, provenance, sources, glossary, blind spots. |
| VDI-README | `README.md` | Draft | all | Honest status. |
| VDI-INDEX | `corpus/INDEX.md` | Draft | topics | Map. |
| VDI-LESSONS-001 | `corpus/lessons/VDI-LESSONS-001_AX_series.md` | Living | - | Canonical seed; synced 2026-11-23 from the internal lessons file. |
| VDI-LESSONS-002 | `corpus/lessons/VDI-LESSONS-002_AX_inbox_2026-11-23.md` | Living | VDI-LESSONS-001 | Dated record of lessons from the v5 edit (8.1–8.11), cited by pack rules. |
| VDI-010 | `docs/release-gate.md` | Draft | VDI-LESSONS-001 | What the gate measures and how to run it. |
| VDI-GATE-SPEC | `vdi/release_data/gate-spec.json` | Draft | VDI-010 | Thresholds with basis; cannot_check list. |
| VDI-GATE-MANIFEST | `vdi/release_data/manifest.schema.json` | Draft | VDI-010 | Manifest declares intent. |
| VDI-011 | `docs/release-gate-proof-v4.md` | Draft | VDI-010 | Gate run on the five known-bad v4 files: caught vs missed. |
| VDI-QG | `docs/quick-check.md` | Draft | VDI-010 | `vdi check`: manifest-free pre-check; synthetic self-test proves each check. |
| VDI-QG-PROOF | `docs/quick-check-v3.md` | Draft | VDI-QG | `vdi check` on the five AX v3 files: all FAIL; false positives found and fixed. |
| VDI-LESSONS-INBOX | `corpus/lessons/LESSONS-INBOX.md` | Living | VDI-LESSONS-001 | Local inbox created by `vdi log-lesson`; not committed. |
| VDI-MCP | `docs/mcp.md` | Draft | topics, VDI-010 | MCP server; smoke test and evals. |
| - | `examples/README.md` | Draft | VDI-011 | What each example is and whether it can be re-run. |
| VDI-01 | `corpus/01_Scripting_and_Boards/` | Seed | VDI-LESSONS-001 | Scripting and boards |
| VDI-02 | `corpus/02_Talking_Head_Capture/` | Seed | VDI-LESSONS-001 | Talking-head capture (camera, light, framing, mic, room) |
| VDI-03 | `corpus/03_Pickups_and_Continuity/` | Seed | VDI-LESSONS-001 | Pickups and continuity |
| VDI-04 | `corpus/04_Screen_Capture_and_Demos/` | Seed | VDI-LESSONS-001 | Screen capture and product demos |
| VDI-05 | `corpus/05_Editing_and_Pacing/` | Seed | VDI-LESSONS-001 | Editing and pacing (cuts, holds, joins, endings, layout churn) |
| VDI-06 | `corpus/06_Captions_and_On_Screen_Text/` | Seed | VDI-LESSONS-001 | Captions and on-screen text |
| VDI-07 | `corpus/07_Audio/` | Seed | VDI-LESSONS-001 | Audio (cleanup, loudness, joins, room tone) |
| VDI-08 | `corpus/08_Colour_and_Face/` | Seed | VDI-LESSONS-001 | Colour and face processing |
| VDI-09 | `corpus/09_Platform_Formats/` | Seed | VDI-LESSONS-001 | Platform formats (TikTok, Reels, YouTube Shorts, X) |
| VDI-10 | `corpus/10_Hooks_and_Retention/` | Seed | VDI-LESSONS-001 | Hooks and retention |
| VDI-11 | `corpus/11_Review_and_QA/` | Seed | VDI-LESSONS-001 | Review and QA (AI review limits, independent review, blind A/B, gate design) |
| VDI-12 | `corpus/12_Claims_and_Honesty/` | Seed | VDI-LESSONS-001 | Claims and honesty |
| VDI-13 | `corpus/13_Anti_Patterns/` | Seed | VDI-LESSONS-001 | Anti-patterns |

Validator: `vdi validate` (required files, front matter, provenance labels resolve, no duplicated rule text).
