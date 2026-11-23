---
id: VDI-11-KNOWLEDGE
title: "Review and QA (AI review limits, independent review, blind A/B, gate design): knowledge"
topic: 11_Review_and_QA
status: Seed
last_updated: 2026-11-23
---

# 11_Review_and_QA — knowledge

# Principles

## 1. A gate that reads the plan grades itself

v4 'passed 22/22' with 19 blocking defects: caption checks compared the plan with itself; safe area, cap height and holds were computed from the plan; 'clean ending' always passed because every piece had a fade; ASR tolerance lists excused real defects. [AX lessons-001: 5.3] [AX ax-v5: gate section] [AX ax-qa-v4]

## 2. Prove the gate on known-bad files

A gate must FAIL a known-bad file on each defect class it claims to catch. The VDI gate was run on the five v4 files. [AX lessons-001: 5.3] [AX vdi-gate-proof]

## 3. The Gemini web app did not watch the videos

Attaching Drive videos in gemini.google.com delivered only transcripts; its 'caption misspellings' and wardrobe notes were its own guesses. AI Studio with the video attached quoted on-screen text exactly. [AX lessons-001: 5.1] [AX ax-gr3] [AX ax-gr4]

## 4. An independent reviewer finds what the editor cannot

A reviewer agent that did not make the edit found what the editor and its gate missed. [AX lessons-001: 5.4] [AX ax-reviewer]

# Patterns

## VDI-11-P01 Three locks

Gate on the render + independent review + owner OK. [AX lessons-001: 6]

## VDI-11-P02 Known-bad proof

Keep failing fixtures (manifests for known-bad files) and expect FAIL with named blockers. [AX vdi-gate-proof]

## VDI-11-P03 Claim triage

AI review claims sorted into TRUE (verified) and FALSE (checked) before any edit. [AX ax-gr3] [AX ax-gr4]

# Anti-patterns

| id | Anti-pattern | How it shows | Fix | Evidence |
|---|---|---|---|---|
| VDI-11-A01 | Self-grading gate | Checks computed from the plan. | Measure the mp4. | [AX ax-qa-v4] |
| VDI-11-A02 | Transcript-only AI review | Reviewer guesses captions and wardrobe from a transcript. | Attach the video in a tool that ingests it. | [AX lessons-001: 5.1] |
| VDI-11-A03 | One-model ASR | A word counts as heard if any model hears it. | Both models must agree. | [AX ax-v5: gate section] |

# Implementation notes

## Run the gate

vdi release final.mp4 --manifest manifest.json ; exit 0 = all checks PASS (WARN allowed), 1 = FAIL. Runtime ~8 min for a 45 s short on 2 cores; OCR and ASR are cached.

## Review copy

540x960, < 2.9 MB so Drive upload and AI review both work. [AX lessons-001: 6]

## What the gate cannot see

Plastic face, voice naturalness, truth of a claim, captions over the face in a transition, 0 vs O, layout churn, anything not declared in the manifest. vdi/release_data/gate-spec.json cannot_check.

## Gate checks that cover this topic

- **all gate checks**: vdi/release.py
- **independent review**: Human or separate agent; not the editor
- **owner OK**: Recorded in release notes

# Glossary

- **Gate**: Automated release check on the rendered file.
- **Independent review**: Review by someone (or an agent) who did not make the edit.
- **Known-bad fixture**: A file with documented defects used to prove the gate fails.
- **Blind A/B**: Comparison with labels hidden from the judge.
