---
id: VDI-01-KNOWLEDGE
title: "Scripting and boards: knowledge"
topic: 01_Scripting_and_Boards
status: Seed
last_updated: 2026-11-23
---

# 01_Scripting_and_Boards — knowledge

# Principles

## 1. The performer reads what is in front of them

On AX the board tool cut each SAY at three wrapped lines and added an ellipsis; the presenter read the boards exactly, so 18 lines across five shorts stopped mid-sentence and needed pickups. Whatever surface the performer reads is the script in practice. [AX ax-boards: board header note] [AX lessons-001: 1.1]

## 2. One idea per beat, one breath per sentence

Long SAY lines were the ones that got truncated, rushed and mis-captioned on AX. Short sentences are easier to say twice, cut, pick up and caption. [AX lessons-001: 1.2] The ~12-word ceiling is a house rule. [UNVERIFIED]

## 3. Every beat names its screen

A beat without a SHOW line produced screen time with nothing that proved the words (AX-01 'tested templates' had no templates on screen, 20.1-23.0 s). [AX ax-v5: AX-01 20.1-23.0 s]

## 4. What he says wins over what was written

Ad-libs happen ('an Army soldier', 'calls back a design contract', 'Probably doesn't exist.'). The script is the intent; the final audio is the truth; the owner decides which deviations stand. [AX lessons-001: 1.3] [AX ax-reviewer: script vs spoken]

# Patterns

## VDI-01-P01 SAY / DO / SHOW beat card

Each beat carries what is said, what the performer does, and the exact screen. The SHOW names the line that proves the SAY, not just 'the app'. [AX ax-scripts: beat format]

## VDI-01-P02 Claim ledger

A three-column list kept with the script: claim, proof line, run id. The edit's evidence beats and the gate manifest are generated from it. [AX lessons-001: 1.4]

## VDI-01-P03 Accepted-deviation list

Differences between script and audio are listed for the owner, who accepts them or asks for a re-record; captions follow the audio. [AX lessons-001: 1.3] [AX ax-v5: leave-as-spoken list]

# Anti-patterns

| id | Anti-pattern | How it shows | Fix | Evidence |
|---|---|---|---|---|
| VDI-01-A01 | Truncated board | Lines end with an ellipsis; takes stop mid-sentence. | Read from the script; diff board vs script. | [AX ax-boards: board header] [AX lessons-001: 1.1] |
| VDI-01-A02 | Claim with no screen | A product claim is spoken over generic footage. | Add a SHOW line naming the proof, or cut the claim. | [AX ax-v5: AX-01 templates] |
| VDI-01-A03 | Silent script 'fixes' | Editor changes captions to match the script instead of the audio. | Caption the audio; list the deviation for the owner. | [AX ax-v5: AX-01 'I've built' vs 'I build'; AX-03 'the' vs 'a ledger'] |

# Implementation notes

## Board diff

Export the board's SAY text and the script's SAY text per beat; compare exactly. Any '...' or '…' at the end of a SAY, or any character difference, fails. [AX lessons-001: 1.1]

## Lint before shoot

Run vdi_lint_script(text) on the full script, one beat per line: it fails any beat over 70 characters (split it into 4a/4b/4c) [AX lessons-001: 1.1], and reports sentence length, claims that need on-screen proof and proper nouns to check by ear.

## Manifest from the script

Copy the script text, proper nouns and claim ledger straight into the gate manifest (vdi/release_data/manifest.schema.json) so the final file is checked against intent.

## Gate checks that cover this topic

- **spoken words vs script**: Every difference between the transcript (both ASR models agreeing) and the script is on the owner-accepted list.

# Glossary

- **SAY / DO / SHOW**: The three parts of a beat: spoken words, performer action, screen content.
- **Board**: The card view the performer reads from during the take (ASV Command 'Build board from script').
- **Pickup**: A line recorded after the main take to replace or complete it.
- **Accepted deviation**: A spoken difference from the script that the owner has accepted; the only allowed script/audio difference in the gate.
- **Claim ledger**: List of spoken claims with the screen line and run that prove each.
