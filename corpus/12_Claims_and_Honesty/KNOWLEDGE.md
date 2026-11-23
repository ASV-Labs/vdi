---
id: VDI-12-KNOWLEDGE
title: "Claims and honesty: knowledge"
topic: 12_Claims_and_Honesty
status: Seed
last_updated: 2026-11-23
---

# 12_Claims_and_Honesty — knowledge

# Principles

## 1. Show it or do not say it

AX-04 said 'MIT License' over the PR page with nothing on screen showing a licence; AX-01 said 'tested templates' with no templates on screen. [AX ax-v5: AX-04 40.2-41.7 s; AX-01 20.1-23.0 s]

## 2. Real output only, from the same run

Never fake product output; adjacent beats in one claim share a run id or carry a label. [AX lessons-001: 3.1, 3.2]

## 3. Label what is a sample

Sample pages carry 'This is a sample page, not a customer site.'; the AX-04 data file is labelled sample. [AX lessons-001: 3.5] [AX ax-screens-ax04]

# Patterns

## VDI-12-P01 Claim ledger -> manifest

The claim ledger becomes the gate manifest's evidence beats. [AX lessons-001: 1.4]

## VDI-12-P02 Honest edges

Say what the screen shows, including failures (AX-05 shows a real FAIL and an UNKNOWN). [AX ax-screens-agent: AX-05]

# Anti-patterns

| id | Anti-pattern | How it shows | Fix | Evidence |
|---|---|---|---|---|
| VDI-12-A01 | Spoken-only claim | Licence or feature said, nothing shown. | Evidence beat or cut the claim. | [AX ax-v5: AX-04 MIT] |
| VDI-12-A02 | Stitched proof | Prompt from one run, result from another. | One run per claim. | [AX ax-v5: AX-01] |
| VDI-12-A03 | Generated centerpiece | Generated or invented visuals presented as product. | Real footage only. | [AX wdi-27: real-vs-generated doctrine] |

# Implementation notes

## Manifest fields

Each evidence beat: id, t0, t1, exact text that must be readable, run_id, source_label (or null), claim id. vdi/release_data/manifest.schema.json.

## What the gate verifies

That the declared proof text is readable, whole and still while the claim is spoken, and that run changes inside a claim carry a readable label. It does not verify that the run happened or that the claim is true.

## Gate checks that cover this topic

- **evidence lines**: check_evidence
- **run ids and source labels**: check_runs
- **spoken words vs script**: check_script

# Glossary

- **Claim**: A statement about what a product does, is, or has done.
- **Proof line**: The exact on-screen text that shows the claim.
- **Source label**: Visible text naming where non-run footage comes from.
