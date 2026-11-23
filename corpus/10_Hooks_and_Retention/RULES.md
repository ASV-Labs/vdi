---
id: VDI-10-RULES
title: "Hooks and retention: agent rules"
topic: 10_Hooks_and_Retention
status: Seed
last_updated: 2026-11-23
---

# 10_Hooks_and_Retention — agent rules

## Always

- **VDI-10-R01** · Always · stage: script — State the problem or proposition in the first sentence; the AX hooks are one or two short lines ('Your coding agent ships fast. It also ships ugly.'). Check: vdi_lint_script: first sentence <= ~12 words. [AX ax-scripts: hooks] [SRC tiktok-creative]
- **VDI-10-R02** · Always · stage: edit — Start on the first syllable: no lead breath or dead air (AX v2 starts 50 ms before the first sound). Check: First speech within ~0.1 s of the file start. [AX ax-gr2: #2] [AX ax-editnotes: v2 hooks] Value [UNVERIFIED]
- **VDI-10-R03** · Always · stage: edit — Make the hook's punch-in land on the payoff word (AX: 110-111%, stopping at 985 source rows because the webcam goes soft). Check: Review the hook at phone size. [AX ax-gr2: #2] [AX ax-editnotes: v2, v4]
- **VDI-10-R04** · Always · stage: edit — Do not let the hook's punch-in create a flash shot at the join to the intro. Check: Gate: shot lengths. [AX ax-v5: T2]

## Never

- **VDI-10-R06** · Never · stage: edit — Never add a cheap synthetic whoosh/impact to a hook; AX rejected it for lack of real assets. Check: No stock SFX without a source. [AX ax-editnotes: v2 rejected]
- **VDI-10-R07** · Never · stage: script — Never follow the hook with an ad-lib that undercuts it ('Where did that number come from? Probably doesn't exist.'). Check: Script diff on the first 6 s. [AX ax-v5: AX-04 3.5 s]

## Prefer

- **VDI-10-R05** · Prefer · stage: edit — Prefer an early real screen beat when the face would otherwise hold for ~30 s. Check: Time to first screen. [AX ax-gr3: #5 AX-02]
