---
id: VDI-13-EXAMPLES
title: "Anti-patterns: examples"
topic: 13_Anti_Patterns
status: Seed
last_updated: 2026-11-23
---

# 13_Anti_Patterns — examples

# Good examples

## VDI-13-E01 Fixes recorded with evidence

Each AX fix in EDIT-NOTES has before/after numbers, for example true peak v3 -> v4 from -0.5 to -1.9 dBTP on AX-01 after measuring the AAC track. [AX ax-editnotes: v4 item 3]

## VDI-13-E02 Known-fail proof kept with the tool

shortskit kept a known-fail plan for v3 and the VDI gate keeps fixture manifests for all five v4 files, so a gate change can be re-proved. [AX ax-qa-v4: known-fail] [AX vdi-gate-proof]

## VDI-13-E03 Claim triage before editing

Review 3 and review 4 claims were each marked TRUE or FALSE against frames before any change was made. [AX ax-gr3] [AX ax-gr4]

# Bad examples

## VDI-13-E04 v4 release candidate

19 blockers across five files while the editor's gate passed 22/22. [AX ax-v5] [AX ax-qa-v4]

## VDI-13-E05 Evidence cropped in all five

'FAIL measure-max: 66ch is over 65ch; in a propo', 'changed evidenced sample-reve', 'UNKNOWN contrast-non-text: Not checked: pro'. [AX ax-gr4: #1]

## VDI-13-E06 Transcript-only reviews 1-3

'FACEPLATE', 'NOOSE RESEARCH', 'ASV LADS' were the reviewer's own speech recognition, not the captions. [AX ax-gr3: FALSE list]

## Rules these defects broke

- VDI-13-R01: Self-grading gate…
- VDI-13-R02: Reading from a truncating board
- VDI-13-R03: Fake or stitched product output
- VDI-13-R04: Wide terminal zoomed until lines crop
- VDI-13-R05: Flash shots and black panels at joins
- VDI-13-R06: Fades that cut quiet final consonants
- VDI-13-R07: Endings that stop on the last word
- VDI-13-R08: Captions from the script instead of the audio
- VDI-13-R09: Captions over other text
- VDI-13-R10: Over-processed voice (gates, pumping, clicks)
- VDI-13-R11: Ungraded, mismatched pickups
- VDI-13-R12: PII or plan walls on screen
- VDI-13-R13: Trusting a transcript-only AI review

# Implementation examples

## Using this list

vdi_search('flash shot') returns the anti-pattern card and the editing rule; vdi_checklist('edit') returns the rules with their gate checks.

## Running the gate

```bash
```
