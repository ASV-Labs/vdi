---
id: VDI-06-EXAMPLES
title: "Captions and on-screen text: examples"
topic: 06_Captions_and_On_Screen_Text
status: Seed
last_updated: 2026-11-23
---

# 06_Captions_and_On_Screen_Text — examples

# Good examples

## VDI-06-E01 v4 caption band on split layouts

v4 put a band between screen and camera so captions never sat on the screen half in split layouts. [AX ax-editnotes: v4 item 10]

## Rules these examples support

- VDI-06-R01: Caption the final audio verbatim…
- VDI-06-R02: Keep captions inside the safe area…
- VDI-06-R03: Keep >= 48 px between captions and any other on-screen text (lower thirds, end cards, screen lines)
- VDI-06-R04: Put nothing behind captions but a plain panel or the face/torso
- VDI-06-R05: Show each caption within ~0.3 s of its word
- VDI-06-R06: Keep captions to two short lines…
- VDI-06-R09: Prefer captions at a reading load the platform recommends…

# Bad examples

## VDI-06-E02 AX-01 'I've built'

Caption reads 'I've built'; medium.en, the source take and the script say 'I build'. [AX ax-v5: AX-01 6.1 s] Gate caught it. [AX vdi-gate-proof: AX-01]

## VDI-06-E03 AX-03 'the ledger'

Caption 'and the ledger'; all passes on the memo hear 'and a ledger'. [AX ax-v5: AX-03 32.9 s]

## VDI-06-E04 Captions over screen content

Terminal lines, the barber page, Alstead cards, the Ferrow bio. [AX ax-gr4: #2]

## Rules these defects broke

- VDI-06-R01: Caption the final audio verbatim…
- VDI-06-R02: Keep captions inside the safe area…
- VDI-06-R03: Keep >= 48 px between captions and any other on-screen text (lower thirds, end cards, screen lines)
- VDI-06-R04: Put nothing behind captions but a plain panel or the face/torso
- VDI-06-R05: Show each caption within ~0.3 s of its word
- VDI-06-R06: Keep captions to two short lines…
- VDI-06-R07: Never generate captions from the plan text aligned to word timings…
- VDI-06-R08: Never trust an AI reviewer's quoted caption misspellings without checking frames…

# Implementation examples

## Gate caption finding

'6.1 s caption "I've built": "ive" heard by only one ASR model' (AX-01 v4). [AX vdi-gate-proof: AX-01]

## Running the gate

```bash
```
