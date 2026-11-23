"""vdi — one CLI for Video Design Intelligence.

  vdi check <video> [--platform P] [--ads] [--json] [--out F]     quick pre-check, no manifest (seconds-minutes)
  vdi release <video> --manifest M [--out DIR]                    full release gate: ASR + OCR (8-10 min/short)
  vdi selftest [--keep]                                           prove every `check` fails its known-bad fixture
  vdi validate [--fix]                                            corpus structure, provenance, duplication
  vdi mcp                                                         MCP server on stdio (for Claude, Cursor, …)
  vdi platform <key>                                              platform spec with sources
  vdi log-lesson --what --rule --check --source                   append to corpus/lessons/LESSONS-INBOX.md

Exit codes: 0 pass · 1 fail · 2 could not run.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from . import __version__, knowledge
from .preflight import require


def _check(a) -> int:
    from . import check
    require(binaries=("ffmpeg", "ffprobe"))
    if not shutil.which("tesseract"):
        print("vdi check: tesseract not found — the 4 OCR checks will report NOT_RUN "
              "(brew install tesseract / apt-get install tesseract-ocr)", file=sys.stderr)
    if not Path(a.video).is_file():
        print(f"vdi check: video not found: {a.video}", file=sys.stderr)
        return 2
    try:
        rep = check.run(a.video, platform=a.platform, ads=a.ads, transcript=a.transcript, script=a.script,
                        accepted=a.accepted, joins=[float(x) for x in a.joins.split(",")] if a.joins else None,
                        only=a.only.split(",") if a.only else None, max_duration=a.max_duration, ocr_fps=a.ocr_fps)
    except Exception as e:  # noqa: BLE001
        print(f"vdi check could not run: {e}", file=sys.stderr)
        return 2
    if a.out:
        Path(a.out).write_text(json.dumps(rep, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(json.dumps(rep, indent=2, ensure_ascii=False, default=str) if a.json else check.format_report(rep))
    return 1 if rep["verdict"] == "FAIL" else 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else list(argv)
    if argv and argv[0] == "release":  # the release gate owns its own argument parser
        from . import release
        try:
            return release.main(argv[1:])
        except SystemExit as e:
            raise
        except Exception:  # noqa: BLE001
            import traceback
            traceback.print_exc()
            return 2

    p = argparse.ArgumentParser(prog="vdi", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version=f"vdi {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)
    plats = list(knowledge.platforms()["platforms"])

    g = sub.add_parser("check", aliases=["quick-gate"], help="quick pre-check of a rendered video (no manifest)")
    g.add_argument("video")
    g.add_argument("--platform", default="youtube-shorts", choices=plats)
    g.add_argument("--ads", action="store_true", help="use the platform's (stricter) ad safe zone")
    g.add_argument("--transcript", help="transcript text/JSON (from two agreeing ASR models)")
    g.add_argument("--script", help="script to compare the transcript with")
    g.add_argument("--accepted", help="owner-accepted deviations, one per line: said words => scripted words")
    g.add_argument("--joins", help="comma-separated audio join times (s), added to detected cuts")
    g.add_argument("--only", help="comma-separated check ids, e.g. G-LOUDNESS,G-TAIL")
    g.add_argument("--max-duration", type=float, help="override the platform length ceiling (s)")
    g.add_argument("--ocr-fps", type=float, default=2.0)
    g.add_argument("--json", action="store_true")
    g.add_argument("--out", help="also write the JSON report here")

    sub.add_parser("release", help="full release gate (see `vdi release --help`)")
    st = sub.add_parser("selftest", help="build synthetic fixtures and prove every check")
    st.add_argument("--keep", action="store_true", help="keep fixtures in ./vdi-selftest-fixtures to try `vdi check` on")
    v = sub.add_parser("validate", help="validate the corpus")
    v.add_argument("--fix", action="store_true", help="regenerate rule short forms from RULES.md first")
    sub.add_parser("mcp", help="run the MCP server on stdio")
    pl = sub.add_parser("platform", help="platform spec with sources")
    pl.add_argument("platform", choices=plats)
    ll = sub.add_parser("log-lesson", help="append a lesson to corpus/lessons/LESSONS-INBOX.md")
    for k in ("what", "rule", "check", "source"):
        ll.add_argument(f"--{k}", required=True)
    ll.add_argument("--author", default="agent")

    a = p.parse_args(argv)
    if a.cmd in ("check", "quick-gate"):
        return _check(a)
    if a.cmd == "selftest":
        require(binaries=("ffmpeg", "ffprobe", "tesseract"), modules=("skimage", "pytesseract", "PIL"))
        from .selftest import selftest
        return selftest.main(keep=a.keep)
    if a.cmd == "validate":
        from . import validate
        return validate.main(["--fix"] if a.fix else [])
    if a.cmd == "mcp":
        from . import mcp_server
        mcp_server.run()
        return 0
    if a.cmd == "platform":
        print(json.dumps(knowledge.platform_spec(a.platform), indent=2, ensure_ascii=False, default=str))
        return 0
    if a.cmd == "log-lesson":
        print(knowledge.log_lesson(a.what, a.rule, a.check, a.source, a.author))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
