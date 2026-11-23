# VDI — Video Design Intelligence

[![ci](https://github.com/ASV-Labs/vdi/actions/workflows/ci.yml/badge.svg)](https://github.com/ASV-Labs/vdi/actions/workflows/ci.yml)
· code MIT · corpus CC BY 4.0 · v0.1.0

**Render gates, a sourced rulebook and an MCP server for short-form product videos that are honest and
finished — built from one series that wasn't.**

We made five 40–47 s vertical shorts: a founder on camera, real terminal and web screens. After four edit
rounds the editor's own checker said **22/22 passed**. An independent reviewer found **19 blocking defects**:
captions that didn't match the words, lines cropped at the frame edge, a flash shot at the hook, endings cut
on the last consonant, a masked email still on screen. The checker had graded the edit plan against itself.

VDI is what we built from that: every rule traces to a measured defect or a cited source, and the gates
measure **the rendered mp4, never the plan**.

```text
$ vdi check AX-01-edit-v3.mp4 --platform youtube-shorts          # a real, known-bad render
vdi check — AX-01-edit-v3.mp4
platform youtube-shorts · 46.967 s · 30.0 fps

  PASS     G-FORMAT        1080×1920 h264 yuv420p aac 48k faststart
  PASS     G-LOUDNESS      measured=-14.1  threshold=-14.0 ±0.5 LUFS
  FAIL     G-TRUEPEAK      measured=-0.5  threshold=≤ -1.5 dBTP
  FAIL     G-SHOT-MIN      measured={"shots": 28, "shortest_frames": 2}  threshold=≥ 12 frames
              4.30s 6-frame shot
             33.23s 2-frame shot
  FAIL     G-TAIL          measured=0.107  threshold=0.58–0.85 s
             46.86s last speech ends 0.11 s before the end
  FAIL     G-JOIN-LEVEL    10.87s speech level step +3.4 dB across join  (+12 more)
  FAIL     G-TEXT-EDGE     19.50s text at right edge: 'Guidance' box=(916, 570, 152, 26) (8 samples)
  FAIL     G-TEXT-SIZE     18.50s 25 px text held 4.5 s: 'CLI and Grok.'
  FAIL     G-PII           25.50s email: [redacted — a site-masked address still on screen]
  WARN     G-FACE-MATCH    only 8 of 27 cuts measured — check the rest by eye
  NOT_RUN  G-SCRIPT-DIFF   needs --transcript (from two agreeing ASR models) and --script
  …
VERDICT: FAIL — do not post.            (excerpt of a real run; 15 checks, ~3 min on 2 CPU cores)
```

## What's in it

| | What | Proof |
|---|---|---|
| **`vdi check`** | Quick pre-check, **no manifest**. 15 checks on any rendered video: format, loudness/true peak, flash shots, black panels, end hold, digital-zero dropouts, level steps at joins, OCR for cropped / unsafe-zone / too-small text, PII and plan walls, face colour across cuts, said-vs-scripted. Minutes on a laptop. | `vdi selftest` builds a clean short plus one broken short per check; every check must fail its broken file and pass the clean one. On five real known-bad renders (AX v3) all five FAIL — [details](docs/quick-check-v3.md). |
| **`vdi release`** | Full release gate. Checks the render against a **manifest** you write before the edit (script, proper nouns, evidence beats: "this exact line must be readable on screen while this claim is spoken"). Two Whisper models must agree on every word; word endings are compared with the source takes. | On the five known-bad v4 files: **33 of 59** listed blockers caught, **14** partly, **12 missed** (5 of the misses are "plastic-looking face", which it can't measure) — [receipts](docs/release-gate-proof-v4.md). |
| **`corpus/`** | 13 topic packs (scripting → publishing), 118 rules with ids, checklists, real examples with timestamps, lessons. | Every claim is labelled `[AX …]` (measured on the series), `[SRC …]` (cited, with access date) or `[UNVERIFIED]`. **101 of 118 rules (86%)** rest on a measurement or a source; 17 are marked unverified house rules. `vdi validate` prints the counts. |
| **`vdi mcp`** | MCP server for Claude, Cursor & co: search, get, production brief, stage checklists, script linter, gate spec, quick check. | `tests/mcp_smoke.py` (real stdio handshake) + 19 guidance evals, in CI. |

**Status, plainly:** agent-written and **not yet reviewed by a human**. Evidence comes from one series (one
presenter, one room, one product). None of the videos has posted yet, so no rule is backed by watch-time
data. The packs say so where it matters ("Known gaps"), and the labels let you tell measured from assumed.

## Try it in two minutes

```bash
git clone https://github.com/ASV-Labs/vdi && cd vdi
pip install -e ".[mcp]"                     # Python 3.10+
brew install ffmpeg tesseract               # or: sudo apt-get install ffmpeg tesseract-ocr

vdi selftest --keep                         # ~90 s: builds fixtures in ./vdi-selftest-fixtures and proves every check
vdi check vdi-selftest-fixtures/bad_tail.mp4     # see a failure: the video ends on the last word
vdi check path/to/your/video.mp4 --platform instagram-reels   # your own render, no setup
```

`vdi` checks for ffmpeg and tesseract before it runs and prints the install line if one is missing.
Exit codes everywhere: **0** pass · **1** fail · **2** couldn't run. A check that couldn't run says `NOT_RUN`,
never `PASS`.

**Release gate** (heavier):

```bash
pip install -e ".[release]"                 # faster-whisper, opencv, scipy
vdi release final.mp4 --manifest final.manifest.json     # manifest examples: examples/v4/manifests/
```

First run downloads two Whisper models (~2 GB). On 2 CPU cores expect 8–10 minutes for a 45 s short;
results are cached per file. It logs progress as it goes.

**Tested on:** Linux and macOS, Python 3.10 and 3.13 (CI). Windows is untested.

## Use it from an agent (MCP)

Claude Code:

```bash
claude mcp add vdi -- vdi mcp
```

Claude Desktop / Cursor (`claude_desktop_config.json` or `.cursor/mcp.json`) — use the absolute path from
`which vdi` if your client doesn't inherit your shell's PATH:

```json
{ "mcpServers": { "vdi": { "command": "vdi", "args": ["mcp"] } } }
```

Tools: `vdi_brief` (start here), `vdi_checklist`, `vdi_lint_script`, `vdi_search`, `vdi_get`, `vdi_gate_spec`,
`vdi_list_topics`, `vdi_quick_gate`. A contributor tool that writes to the lessons inbox, `vdi_log_lesson`, is
off unless you set `VDI_ENABLE_WRITE_TOOLS=1`. Details: [docs/mcp.md](docs/mcp.md).

## What the gates can't catch

No metric here can judge a plastic-looking face, a voice that sounds processed, whether a claim is *true*
(only whether its proof line is readable while it's said), whether footage is really from the run it claims,
or anything the manifest forgot to declare. So "final" always takes three locks: the gate passes on the exact
file, **an independent reviewer** (not the editor) says READY, and **the owner** says so. See
[AGENTS.md](AGENTS.md).

**False positives:** we don't yet have a human-verified *good* real render to prove the absence of false
alarms on finished footage — every AX render so far is known-bad, which is the point. Two false-positive
classes showed up on real footage and are fixed and covered by the self-test (animated split-screen
transitions read as cuts; face-detector misfires, which now report `WARN`, never a silent result). If a check
flags something on your real video that isn't there, please [open an issue](CONTRIBUTING.md#reporting-a-gate-error).

## Layout

```text
vdi/              code: cli, check (quick gate), release (full gate), corpus engine, MCP server, validator, selftest
corpus/           13 topic packs + lessons; README.md explains provenance and how to read a pack (CC BY 4.0)
examples/v4/      real manifests and gate receipts from the five known-bad v4 renders (footage not published)
examples/v3/      verified output of `vdi release` on AX-01 v3 after packaging (footage not published)
docs/             release gate, quick check, MCP, proofs
tests/            CLI/packaging tests, MCP smoke test, guidance evals
```

`ax:<record>` in citations = an internal production record (edit notes, review notes, measurement scripts)
that isn't published; the lessons and gate receipts are.

## Contributing

The most useful contributions are a real file the gates get wrong, and a defect from a real edit that no
rule covers. How a lesson becomes a rule and then a gate check (only with a known-bad fixture that proves it):
[CONTRIBUTING.md](CONTRIBUTING.md).

Built by [ASV Labs](https://github.com/ASV-Labs) · [@ASaltyVet](https://x.com/ASaltyVet). Code MIT
([LICENSE](LICENSE)); corpus, docs and examples CC BY 4.0 ([corpus/LICENSE](corpus/LICENSE)).
