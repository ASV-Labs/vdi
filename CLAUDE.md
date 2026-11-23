# CLAUDE.md

Read **`AGENTS.md`** (VDI-001). It is the operating contract for every agent using this repo, and it governs you.

- Before scripting or editing a video: `vdi_brief` (MCP) or the packs' `RULES.md`; write the gate manifest before the edit.
- `vdi check <render> --platform <p>` on every draft render — a pre-check, not a release.
- Never call a video final until `vdi release <final.mp4> --manifest <m.json>` exits 0 on the exact file, an
  independent review says READY, and the owner says so himself.
- Before finishing repo work: `vdi validate` exits 0; `vdi selftest` passes if you touched `vdi/check.py`.
- Statuses are Draft and Seed only. Unverified stays labelled [UNVERIFIED]; checks that didn't run are NOT_RUN.
