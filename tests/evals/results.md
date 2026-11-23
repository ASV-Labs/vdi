# VDI MCP guidance evals - results

Run 2026-11-23 08:49 with `python3 mcp/evals/run_evals.py`: **19/19 pass**.

These are deterministic checks that the engine returns the expected guidance for questions an editing agent would ask. They do not measure how well a model uses the tools (no LLM-in-the-loop run yet).

| id | question | tool | result | expected ids found | phrases missing |
|---|---|---|---|---|---|
| Q01 | My last word keeps getting clipped at the end of a pickup. What rule and check apply? | vdi_search | PASS | VDI-05-R06, VDI-07-R06 | - |
| Q02 | How long should the short hold after the last word? | vdi_search | PASS | VDI-05-R07 | - |
| Q03 | Can I show the prompt from one agent run and the result from another in the same claim? | vdi_search | PASS | VDI-04-R02 | - |
| Q04 | Should captions follow the script or the audio? | vdi_search | PASS | VDI-06-R01 | - |
| Q05 | How do I record a terminal so lines are not cropped? | vdi_search | PASS | VDI-04-R03 | - |
| Q06 | Is the Gemini web app a valid video reviewer? | vdi_search | PASS | - | - |
| Q07 | What skin colour difference is allowed at a cut between a take and a pickup? | vdi_search | PASS | VDI-03-R01, VDI-08-R01 | - |
| Q08 | What is the shortest allowed shot? | vdi_get | PASS | - | - |
| Q09 | What must be true before a video is called final? | vdi_checklist | PASS | VDI-11-R01 | - |
| Q10 | Brief for a 90 s YouTube Short explainer with no presenter: any platform warning? | vdi_brief | PASS | - | - |
| Q11 | Brief for a 45 s product demo with presenter: does it include capture, pickup and screen rules and an ending hold? | vdi_brief | PASS | VDI-02-R01, VDI-03-R01, VDI-04-R01 | - |
| Q12 | Lint: does a 24-word claim sentence get flagged with the claim and the proper nouns? | vdi_lint_script | PASS | - | - |
| Q13 | Lint: a SAY beat over 70 characters fails the board rule | vdi_lint_script | PASS | - | - |
| Q14 | What loudness target and true peak does the gate use, and does YouTube turn quiet videos up? | vdi_checklist | PASS | VDI-07-R02 | - |
| Q15 | What can the gate NOT check? | vdi_gate_spec | PASS | - | - |
| Q16 | What does Meta say about sound on Reels? | vdi_search | PASS | - | - |
| Q17 | Masked emails and PLAN_REQUIRED on screen: what is the rule? | vdi_checklist | PASS | VDI-04-R07, VDI-04-R08 | - |
| Q18 | Is a tolerance list of misheard words allowed in the gate? | vdi_search | PASS | VDI-11-R03 | - |
| Q19 | Lint: a beat of 70 characters or less passes the board rule | vdi_lint_script | PASS | - | - |
