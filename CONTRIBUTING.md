# Contributing

VDI only grows from evidence. Two kinds of contribution are especially welcome: **a real file the
gates get wrong** (a false pass or a false fail) and **a defect from a real edit** that no rule covers yet.

## How a lesson becomes a rule

1. **Lesson.** Something went wrong in a real video. Write it down as *what happened → the rule that
   prevents it → how to check it → source* (file, version, timestamp, who measured it). Locally:
   `vdi log-lesson --what … --rule … --check … --source …` appends to `corpus/lessons/LESSONS-INBOX.md`.
   In a PR: add it to a dated `corpus/lessons/VDI-LESSONS-NNN_*.md`. Lessons are appended, never deleted;
   a superseded lesson is marked superseded.
2. **Rule.** Add it to the right pack's `RULES.md` in the existing format
   (`- **VDI-NN-Rnn** · Always|Never|Prefer · stage: … — rule. Check: how. [provenance]`) with a provenance
   label: `[AX id: where]` for internal measurements, `[SRC id]` for a cited document (add it to
   `sources/sources.json` with url and access date), or `[UNVERIFIED]`. Never invent a number.
3. **Short forms.** Checklists and examples cite rules as "first clause… (VDI-NN-Rnn)". Run
   `vdi validate --fix` to regenerate them from `RULES.md`; never restate a rule in full elsewhere.
4. **Gate check (if it can be measured).** A new check in `vdi/check.py` merges only with a synthetic
   known-bad fixture in `vdi/selftest/make_fixtures.py` that it **fails**, while the known-good fixture
   still passes every check. `vdi selftest` enforces this. A check that can't be proven this way doesn't
   go in the gate; it goes in the pack's checklist instead.

## Reporting a gate error

Open an issue with: the command, the check id, the measured value, the timestamp, and what is actually on
screen or in the audio there (a frame grab or a short clip if you can share one). False positives on
real, finished videos are the most useful reports we can get — we don't yet have a human-verified good
render (see the README).

## Before opening a PR

```bash
vdi validate                    # corpus structure, provenance, no duplicated rule text — must exit 0
vdi selftest                    # every check fails its known-bad fixture — must pass
python3 -m pytest -q tests/     # CLI, packaging, release-gate pre-flight (mocked)
python3 tests/mcp_smoke.py      # MCP engine + stdio handshake
python3 tests/evals/run_evals.py
```

Status values are **Seed** (topic packs) and **Draft** (docs, gates). Nothing may be marked Reviewed,
Approved or Final until a human has reviewed it. Keep third-party text to short quotes and keep third-party
media out of the repo.
