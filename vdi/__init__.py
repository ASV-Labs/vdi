"""Video Design Intelligence (VDI): render gates, a corpus and an MCP server for honest, finished short-form video.

`vdi check` (quick, manifest-free) · `vdi release` (full gate, manifest + ASR) · `vdi mcp` (stdio server).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(__file__).resolve().parent / "data"
__version__ = "0.1.0"
