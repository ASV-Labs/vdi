#!/usr/bin/env python3
"""Smoke test for the VDI MCP engine.
Part 1 (stdlib only): exercises every query corpus.py exposes.
Part 2 (needs the mcp SDK): spawns `python -m vdi mcp` over stdio from cwd=/ (as real clients do), does the MCP handshake, lists tools and calls each one.
Run: python3 tests/mcp_smoke.py      (part 2 is skipped with a note if the SDK is missing)"""
import asyncio, json, os, sys
from vdi.corpus import corpus, STAGES

c = corpus()
assert len(c.topics) == 13, "expected 13 topic packs"
rules = c.rules(); assert len(rules) >= 100, f"expected >= 100 rules, got {len(rules)}"
assert all(r["provenance"]["measured_internally"] or r["provenance"]["sourced"] or r["provenance"]["unverified"] for r in rules), "every rule needs provenance"
assert c.get("VDI-05-R01")["type"] == "rule" and c.get("VDI-06")["type"] == "topic" and c.get("VDI-LESSONS-001") and c.get("VDI-GATE")
assert c.get("VDI-99-R99") is None, "unknown id must return None"
s = c.search("word endings consonant"); assert s["items"], "search returned nothing"
assert c.search("caption", stage="captions")["items"], "stage-filtered search returned nothing"
for st in STAGES: assert c.checklist(st)["rules"] or st == "publish" and c.checklist(st)["gate_checks"], f"empty checklist for {st}"
assert c.checklist("nonsense") is None
b = c.brief("product-demo", "all", 45, True, True)
assert b["shot_list_skeleton"]["beats"][-1]["beat"] == "ending hold" and b["capture_checklist"] and b["gate_settings"]["manifest_template"]["evidence_beats"]
assert any("blocked globally" in w for w in c.brief("explainer", "shorts", 90, False, False)["warnings"]), "Shorts > 60 s must warn about copyright blocks"
assert "error" in c.brief("x", "myspace", 30, True, False)
L = c.lint_script("This studio site was built by an agent following Motif, and it was reviewed and merged by Nous Research under the MIT license.")
assert L["long_sentences"] == [1] and L["claims_needing_proof"] and "Motif" in L["proper_nouns_check_by_ear"]
g = c.gate(); assert g["thresholds"]["evidence"]["min_hold_s"] == 1.6 and g["cannot_check"]
print(f"ENGINE OK - topics {len(c.topics)}, rules {len(rules)}, items {len(c.items)}, chunks {len(c.chunks)}")

async def stdio():
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
    except ImportError:
        print("SKIP stdio handshake: mcp SDK not installed"); return
    def args(tool, payload):
        props = ((getattr(tool, "inputSchema", None) or getattr(tool, "input_schema", None)) or {}).get("properties", {})
        return {"params": payload} if "params" in props and set(props) <= {"params"} else payload
    async with stdio_client(StdioServerParameters(command=sys.executable, args=["-m", "vdi", "mcp"], cwd="/")) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = {t.name: t for t in (await s.list_tools()).tools}
            print("TOOLS:", ", ".join(sorted(tools)))
            need = {"vdi_search", "vdi_get", "vdi_brief", "vdi_checklist", "vdi_lint_script", "vdi_gate_spec", "vdi_list_topics"}
            assert need <= set(tools), f"missing tools {need - set(tools)}"
            calls = [("vdi_list_topics", {}), ("vdi_search", {"query": "flash shot at the join"}), ("vdi_get", {"id": "VDI-04-R02"}),
                     ("vdi_brief", {"video_type": "product-demo", "platform": "tiktok,shorts", "duration_s": 45, "has_talking_head": True, "has_screen_demo": True}),
                     ("vdi_checklist", {"stage": "captions"}), ("vdi_lint_script", {"text": "My agent said done. Motif said not yet."}), ("vdi_gate_spec", {})]
            for name, payload in calls:
                out = (await s.call_tool(name, args(tools[name], payload) if payload else {})).content[0].text
                json.loads(out); print(f"  {name}: {len(out)} chars JSON")
            err = (await s.call_tool("vdi_get", args(tools["vdi_get"], {"id": "VDI-99-R99"}))).content[0].text
            assert err.startswith("Error:"); print("  error path OK")
            print(f"STDIO OK - {len(tools)} tools listed and called over stdio")
asyncio.run(stdio())
