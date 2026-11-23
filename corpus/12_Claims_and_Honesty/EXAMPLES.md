---
id: VDI-12-EXAMPLES
title: "Claims and honesty: examples"
topic: 12_Claims_and_Honesty
status: Seed
last_updated: 2026-11-23
---

# 12_Claims_and_Honesty — examples

# Good examples

## VDI-12-E01 AX-05 FAIL -> fix -> PASS

One run shows the real FAIL, the UNKNOWN, the fix note and the PASS. [AX ax-screens-agent: AX-05]

## Rules these examples support

- VDI-12-R01: For every spoken claim, list the exact screen line that proves it and the run it comes from, before…
- VDI-12-R02: Every line, UI and result on screen comes from a real run or live page captured that day…
- VDI-12-R03: When a beat shows a different run (for example a repo's demo), put a visible source label on it…
- VDI-12-R04: Show the licence, price or status on screen when it is said (for example the repo's LICENSE line on…
- VDI-12-R05: List every spoken deviation that changes a claim for the owner (for example 'a design library that…

# Bad examples

## VDI-12-E02 AX-04 MIT License

Said over the PR page; nothing shows a licence. [AX ax-v5: AX-04] Gate: evidence beat b13 FAIL. [AX vdi-gate-proof: AX-04]

## VDI-12-E03 AX-04 demo graph

Different model and source from the run being described, unlabeled. [AX ax-v5: AX-04]

## Rules these defects broke

- VDI-12-R01: For every spoken claim, list the exact screen line that proves it and the run it comes from, before…
- VDI-12-R02: Every line, UI and result on screen comes from a real run or live page captured that day…
- VDI-12-R03: When a beat shows a different run (for example a repo's demo), put a visible source label on it…
- VDI-12-R04: Show the licence, price or status on screen when it is said (for example the repo's LICENSE line on…
- VDI-12-R05: List every spoken deviation that changes a claim for the owner (for example 'a design library that…
- VDI-12-R06: Never promise what the product does not offer (AX-03…
- VDI-12-R07: Never call anything final, ready or reviewed without the gate, an independent review and the…

# Implementation examples

## Evidence beat for a licence

{"id": "b13-mit", "t0": 40.0, "t1": 41.7, "text": "MIT License", "run_id": "capture-github-repo", "claim": "license"}

## Running the gate

```bash
```
