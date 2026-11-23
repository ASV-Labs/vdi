---
id: VDI-MCP
title: "MCP server"
topic: docs
status: Draft
last_updated: 2026-11-23
---

# `vdi mcp` — MCP server over Video Design Intelligence

MCP server (stdio) that gives an agent video-production guidance from this corpus: rules with
provenance, a production brief, stage checklists, a script linter and the release-gate spec. All logic is in `vdi/corpus.py` (standard library only); `vdi/mcp_server.py` is the thin MCP wrapper.

Local only. Nothing here deploys or calls the network. Two tools act on the local machine: `vdi_quick_gate` reads a
video file you name, and `vdi_log_lesson` appends to `corpus/lessons/LESSONS-INBOX.md` — the latter is **off** unless
the server runs with `VDI_ENABLE_WRITE_TOOLS=1`.

## Tools

| Tool | Purpose |
|---|---|
| `vdi_list_topics` | The 13 topic packs with ids, stages, summaries, rule counts. Call first to orient. |
| `vdi_search(query, topic?, stage?, limit?)` | Ranked chunks from the topic packs, the AX lessons file and the gate docs, each with provenance (measured internally / sourced / unverified). Rules rank first. |
| `vdi_get(id)` | One item: rule `VDI-05-R03`, pattern `-P`, anti-pattern `-A`, example `-E`, topic `VDI-06`, `VDI-LESSONS-001`, `VDI-GATE`, a source id, or a repo-relative file path. |
| `vdi_brief(video_type, platform, duration_s, has_talking_head, has_screen_demo)` | **The workflow tool.** Format and platform notes with sources, warnings for the chosen length, a timed shot-list skeleton, script rules, capture checklist, edit rules with the gate thresholds, review plan, gate settings with a manifest template. |
| `vdi_checklist(stage)` | Rules for one stage (`script, shoot, pickups, screen, edit, captions, audio, review, publish`) plus the gate checks that measure it. |
| `vdi_lint_script(text)` | Sentence length (over ~12 words warns, over 20 fails), one SAY per beat at most 70 characters (FAIL otherwise: split into 4a/4b/4c), claims that need on-screen proof, proper nouns to check by ear, hook length. |
| `vdi_gate_spec()` | How to run `vdi/release.py`, thresholds with their basis, what it cannot check, the manifest schema, and its results on the known-bad AX v4 files. |

| `vdi_quick_gate(video_path, platform?, ads?, only?)` | Runs `vdi check` on a local rendered video: 15 measured checks, no manifest. A pre-check, not a release. |
| `vdi_log_lesson(...)` | Contributor tool, off by default: append a new defect to the lessons inbox. |

Read tools are annotated read-only, idempotent and closed-world; every tool returns JSON.

## Run

```bash
pip install -e ".[mcp]"        # mcp SDK needs Python >= 3.10 (SDK 1.x and 2.x both work)
vdi mcp                        # stdio
```

Register with a client as a stdio server whose command is `vdi` with args `["mcp"]` (config snippets in the README).
Works with the mcp SDK 1.x (`FastMCP`) and 2.x (`MCPServer`); tested with mcp 2.3.0 on Python 3.13. The corpus is
found next to the package (editable install from a clone) or via `VDI_CORPUS_DIR`, so the server works from any
working directory.

## Tests

```bash
python3 tests/mcp_smoke.py          # engine checks + real stdio handshake calling every registered tool (from cwd=/)
python3 tests/evals/run_evals.py     # 19 guidance questions with expected answers; writes tests/evals/results.{md,json}
```

Latest results are in `tests/evals/results.md`. The evals are deterministic (no API key): they check that the
engine returns the expected rule ids and phrases. No LLM-in-the-loop eval has been run.

## Limits

- The guidance is **Seed**: evidence from one series (AX-01..05) and a handful of fetched platform pages.
  Nothing has been reviewed by a human. Provenance is attached to every rule so the agent can tell.
- Search is keyword ranking over markdown chunks, not semantic search.
- The brief's shot-list skeleton is proportional, not timed to a real script.
