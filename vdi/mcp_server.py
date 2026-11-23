#!/usr/bin/env python3
"""vdi mcp - MCP server exposing the Video Design Intelligence corpus and gates to agents.

Read-only guidance for making short-form video: search and fetch rules, a production brief, stage
checklists, a script linter and the release-gate spec (read-only), plus `vdi_quick_gate` (reads a local
video) and `vdi_log_lesson` (writes corpus/lessons/LESSONS-INBOX.md; OFF unless VDI_ENABLE_WRITE_TOOLS=1).
Logic lives in vdi/corpus.py. Local stdio only: nothing here deploys or reaches the network.

Run:  vdi mcp        Deps: pip install -e ".[mcp]"   (Python >= 3.10)
"""
from __future__ import annotations
import json, os, sys
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from vdi.corpus import corpus, STAGES  # shared engine

try:                                   # mcp SDK 1.x
    from mcp.server.fastmcp import FastMCP as _Server
except ImportError:
    try:                               # mcp SDK 2.x renamed FastMCP to MCPServer
        from mcp.server.mcpserver import MCPServer as _Server
    except ImportError:                # allow import/compile without the SDK installed
        _Server = None
try:
    from mcp.types import ToolAnnotations
except ImportError:
    ToolAnnotations = None

mcp = _Server("vdi_mcp") if _Server else None
_RO = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}

def ann(title):
    return ToolAnnotations(title=title, **_RO) if ToolAnnotations else {"title": title, **_RO}

def _json(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)

class SearchInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    query: str = Field(..., min_length=2, description="Free text, e.g. 'word endings cut', 'caption safe area', 'pickup grade'")
    topic: Optional[str] = Field(None, description="Topic number or folder, e.g. '05' or '06_Captions_and_On_Screen_Text'")
    stage: Optional[str] = Field(None, description="One of: " + ", ".join(STAGES))
    limit: int = Field(10, ge=1, le=50)

class GetInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    id: str = Field(..., min_length=3, description="Rule/pattern/anti-pattern/example id (VDI-05-R03, VDI-04-A02), topic id (VDI-06), VDI-LESSONS-001, VDI-GATE, a source id, or a repo-relative file path")

class BriefInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    video_type: str = Field(..., min_length=2, description="e.g. 'product-demo', 'explainer', 'announcement', 'opinion'")
    platform: str = Field("all", description="tiktok, reels, shorts, x (comma separated) or 'all'")
    duration_s: float = Field(..., gt=0, le=600, description="Planned length in seconds")
    has_talking_head: bool = Field(..., description="Is a person on camera?")
    has_screen_demo: bool = Field(..., description="Are real product screens / terminal runs shown?")

class StageInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    stage: str = Field(..., description="One of: " + ", ".join(STAGES))

class LintInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(..., min_length=1, description="The script: one beat per line or paragraph")

def _register():
    @mcp.tool(name="vdi_search", annotations=ann("Search video guidance"))
    async def vdi_search(params: SearchInput) -> str:
        """Search the VDI corpus (13 topic packs, the AX lessons file, the gate docs). Optional filters: topic, stage. Returns ranked chunks with path, heading, text and provenance (measured internally / sourced / unverified). Use vdi_get for a full rule or file."""
        p = params
        if p.stage and p.stage not in STAGES: return f"Error: unknown stage '{p.stage}'. Use one of {STAGES}."
        return _json(corpus().search(p.query, p.topic, p.stage, p.limit))

    @mcp.tool(name="vdi_get", annotations=ann("Get a rule, topic, source or file"))
    async def vdi_get(params: GetInput) -> str:
        """Fetch one item by id: a rule (VDI-05-R03: text, check, stages, provenance), pattern (-P), anti-pattern (-A), example (-E), topic (VDI-06), the lessons file (VDI-LESSONS-001), the gate spec (VDI-GATE), a source id (e.g. yt-shorts-3min) or a repo-relative markdown path."""
        r = corpus().get(params.id)
        if not r: return f"Error: nothing with id '{params.id}'. Use vdi_search, or ids like VDI-05-R01, VDI-06, VDI-LESSONS-001, VDI-GATE."
        return _json(r)

    @mcp.tool(name="vdi_brief", annotations=ann("Compose a production brief"))
    async def vdi_brief(params: BriefInput) -> str:
        """THE workflow tool. Returns a production brief for one short: format and platform notes (with sources), warnings for the chosen length, a timed shot-list skeleton, script rules, capture checklist (talking head and/or screen demo), edit rules with the gate's thresholds, the review plan, and gate settings including a manifest template. Call it before writing the script."""
        p = params
        return _json(corpus().brief(p.video_type, p.platform, p.duration_s, p.has_talking_head, p.has_screen_demo))

    @mcp.tool(name="vdi_checklist", annotations=ann("Checklist for one production stage"))
    async def vdi_checklist(params: StageInput) -> str:
        """Rules for one stage (script, shoot, pickups, screen, edit, captions, audio, review, publish) across all topics, each with its check and provenance, plus the gate checks that measure that stage on the rendered file."""
        r = corpus().checklist(params.stage)
        if r is None: return f"Error: unknown stage '{params.stage}'. Use one of {STAGES}."
        return _json(r)

    @mcp.tool(name="vdi_lint_script", annotations=ann("Lint a short-form script"))
    async def vdi_lint_script(params: LintInput) -> str:
        """Lint a script: sentence length (over ~12 words warns, over 20 fails), board-truncation rule (one SAY line per beat, FAIL over 70 characters: split into 4a/4b/4c), claims that need on-screen proof (claim words and numbers), proper nouns to check by ear, and hook length."""
        return _json(corpus().lint_script(params.text))

    @mcp.tool(name="vdi_gate_spec", annotations=ann("Video gate spec"))
    async def vdi_gate_spec() -> str:
        """The release gate: how to run it, its thresholds (with the basis of each), what it cannot check, the manifest schema, and its results on the five known-bad AX v4 files."""
        return _json(corpus().gate())

    @mcp.tool(name="vdi_list_topics", annotations=ann("List topic packs"))
    async def vdi_list_topics() -> str:
        """List the 13 topic packs with ids, stages, summaries and rule counts. Call first to orient."""
        return _json(corpus().list_topics())

def _register_quick_gate():
    """Tools backed by the vdi/ package (quick gate + lessons inbox). These are the only tools that act:
    one reads a local video file, the other appends to corpus/lessons/LESSONS-INBOX.md. Nothing deploys."""

    @mcp.tool(name="vdi_quick_gate", annotations=ann("Quick gate on a rendered video (no manifest)"))
    async def vdi_quick_gate(video_path: str, platform: str = "youtube-shorts", ads: bool = False,
                             only: Optional[str] = None) -> str:
        """Fast manifest-free pre-check of a rendered video on THIS machine: format, duration, loudness, true peak,
        black frames, shortest shot, end hold, digital-zero dropouts, join level steps, OCR text cropping / UI-zone /
        size, PII and plan walls, face colour across cuts. Needs ffmpeg; OCR checks need tesseract. Returns per-check
        status with measured values. A PASS here is NOT release: the release gate (`vdi release` with a
        manifest), independent review and owner sign-off are still required. platform: youtube-shorts | youtube-long |
        tiktok | instagram-reels | x | linkedin. only: comma-separated check ids (see docs/quick-check.md)."""
        from vdi import check
        p = os.path.expanduser(video_path)
        if not os.path.isfile(p):
            return _json({"error": f"file not found: {p}"})
        try:
            return _json(check.run(p, platform=platform, ads=ads, only=only.split(",") if only else None))
        except Exception as e:  # missing ffmpeg/tesseract, unreadable file
            return _json({"error": str(e)})

    if os.environ.get("VDI_ENABLE_WRITE_TOOLS") != "1":
        return  # contributor tool: writes to the corpus, so it is opt-in

    write_ann = (ToolAnnotations(title="Log a new production lesson", readOnlyHint=False, destructiveHint=False,
                                 idempotentHint=False, openWorldHint=False) if ToolAnnotations else {"title": "Log a new production lesson"})

    @mcp.tool(name="vdi_log_lesson", annotations=write_ann)
    async def vdi_log_lesson(what_happened: str, rule: str, check: str, source: str, author: str = "agent") -> str:
        """Append a new defect/lesson to corpus/lessons/LESSONS-INBOX.md for a curator to fold into VDI-LESSONS-* and the
        topic packs. All fields required: what happened (concrete: file, version, timestamp), the rule that prevents
        it, how to check it, and the source (file, review, measurement)."""
        from vdi import knowledge
        return _json({"appended_to": knowledge.log_lesson(what_happened, rule, check, source, author)})


if mcp:
    _register()
    _register_quick_gate()

def run():
    if not mcp:
        sys.stderr.write("The 'mcp' package is not installed. Run: pip install -e \".[mcp]\"\n"); sys.exit(1)
    mcp.run()


if __name__ == "__main__":
    run()
