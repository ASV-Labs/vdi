"""Where things live. Works from any working directory (MCP clients spawn servers from / or ~)."""
from __future__ import annotations

import os
from pathlib import Path

PKG = Path(__file__).resolve().parent
REPO = PKG.parent
RELEASE_DATA = PKG / "release_data"
EXAMPLES = REPO / "examples"
DOCS = REPO / "docs"


class CorpusNotFound(RuntimeError):
    pass


def corpus_dir() -> Path:
    """VDI_CORPUS_DIR first, then <repo>/corpus next to the package (editable install from a clone)."""
    env = os.environ.get("VDI_CORPUS_DIR")
    cand = Path(env).expanduser().resolve() if env else REPO / "corpus"
    if not (cand / "topics.json").is_file():
        raise CorpusNotFound(
            f"VDI corpus not found at {cand}. Install from a clone (git clone https://github.com/ASV-Labs/vdi && "
            f"pip install -e './vdi[mcp]') or set VDI_CORPUS_DIR to the repo's corpus/ folder.")
    return cand


def lessons_inbox() -> Path:
    return corpus_dir() / "lessons" / "LESSONS-INBOX.md"
