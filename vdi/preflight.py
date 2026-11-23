"""Fail fast, with the exact install line, before any long run."""
from __future__ import annotations

import importlib.util
import platform
import shutil
import sys

_BREW = {"ffmpeg": "ffmpeg", "ffprobe": "ffmpeg", "tesseract": "tesseract"}
_APT = {"ffmpeg": "ffmpeg", "ffprobe": "ffmpeg", "tesseract": "tesseract-ocr tesseract-ocr-eng"}


def _install_line(missing: list[str]) -> str:
    if platform.system() == "Darwin":
        return "brew install " + " ".join(sorted({_BREW[m] for m in missing}))
    return "sudo apt-get install -y " + " ".join(sorted({_APT[m] for m in missing}))


def require(binaries=("ffmpeg", "ffprobe"), modules=(), extra_hint: str = "") -> None:
    """Exit 2 with a clear message if a system binary or Python module is missing."""
    missing_bin = [b for b in binaries if not shutil.which(b)]
    missing_mod = [m for m in modules if importlib.util.find_spec(m) is None]
    if not missing_bin and not missing_mod:
        if "tesseract" in binaries:
            import subprocess
            langs = subprocess.run(["tesseract", "--list-langs"], capture_output=True, text=True).stdout
            if "eng" not in langs.split():
                sys.exit("vdi: tesseract has no English data ('eng'). Install it: " + _install_line(["tesseract"]))
        return
    msg = ["vdi: missing requirements — nothing was run."]
    if missing_bin:
        msg.append(f"  system: {', '.join(missing_bin)}  →  {_install_line(missing_bin)}")
    if missing_mod:
        msg.append(f"  python: {', '.join(missing_mod)}  →  pip install -e \".{extra_hint or ''}\"")
    print("\n".join(msg), file=sys.stderr)
    sys.exit(2)
