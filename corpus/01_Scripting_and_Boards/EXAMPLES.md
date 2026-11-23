---
id: VDI-01-EXAMPLES
title: "Scripting and boards: examples"
topic: 01_Scripting_and_Boards
status: Seed
last_updated: 2026-11-23
---

# 01_Scripting_and_Boards — examples

# Good examples

## VDI-01-E01 AX-01b run designed to fail

The second AX-01 run was set up so a real FAIL (measure-max 66ch > 65ch) happened, then a fix and a PASS, so 'Fixes what fails' had proof from one run. [AX ax-screens-agent: AX-01b]

## VDI-01-E02 Say it twice

Every AX take has each line read twice, which gave the editor a second read when the first had a stumble. [AX lessons-001: 2.6]

## Rules these examples support

- VDI-01-R01: Read from the full script, never from a board that can truncate, until the board tool is proven not…
- VDI-01-R02: One SAY line per beat, 70 characters or less, so a board that wraps and cuts at three lines cannot…
- VDI-01-R03: Keep each sentence to about 12 words or fewer and one idea per beat
- VDI-01-R04: Give every beat a SHOW line that names the exact screen line, page element or run output that…
- VDI-01-R05: Write a claim list before recording…
- VDI-01-R06: Design the demo so the claimed behaviour is likely to happen on camera (for 'fixes what fails', a…
- VDI-01-R07: Budget 1.6-2 s of picture per on-screen proof line…
- VDI-01-R08: Keep a proper-noun list (names, products, handles) for captions and for checking by ear
- VDI-01-R10: Prefer sentences that end on the key word, so a cut or a fade never lands on the payoff
- VDI-01-R11: Have the performer say each line twice with a pause between…

# Bad examples

## VDI-01-E03 Board truncation, all five shorts

18 lines stopped where the board cut them; pickups were needed for every short. [AX ax-boards: all five] [AX lessons-001: 1.1]

## VDI-01-E04 AX-01 first run passed 17/17

The script said 'Fixes what fails' but the first recorded run never failed, so the line had no proof and the run had to be redone. [AX ax-screens-agent: AX-01 first run]

## Rules these defects broke

- VDI-01-R01: Read from the full script, never from a board that can truncate, until the board tool is proven not…
- VDI-01-R02: One SAY line per beat, 70 characters or less, so a board that wraps and cuts at three lines cannot…
- VDI-01-R03: Keep each sentence to about 12 words or fewer and one idea per beat
- VDI-01-R04: Give every beat a SHOW line that names the exact screen line, page element or run output that…
- VDI-01-R05: Write a claim list before recording…
- VDI-01-R06: Design the demo so the claimed behaviour is likely to happen on camera (for 'fixes what fails', a…
- VDI-01-R07: Budget 1.6-2 s of picture per on-screen proof line…
- VDI-01-R08: Keep a proper-noun list (names, products, handles) for captions and for checking by ear
- VDI-01-R09: Never write a line whose meaning flips if one word is ad-libbed (for example 'a design library your…

# Implementation examples

## Lint output (excerpt, AX-01 script)

Running vdi_lint_script on the AX-01 script flags 'This studio site was built by an agent following Motif.' as a claim needing proof, and 'Motif', 'MCP', 'ASV Labs' as proper nouns to check by ear. See mcp/evals/ for the recorded run.

## Running the gate

```bash
```
