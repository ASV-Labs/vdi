#!/usr/bin/env python3
"""Deterministic guidance evals for the VDI MCP engine (no API key, stdlib only).
Each case calls the same engine function the MCP tool wraps and checks that the expected guidance comes
back: at least one expected rule id among the returned ids, and every expected phrase in the JSON result.
Writes tests/evals/results.json and results.md. Exit 0 only if every case passes."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
from vdi.corpus import corpus
c = corpus()
CALL = {"vdi_search": lambda a: c.search(a["query"], a.get("topic"), a.get("stage"), a.get("limit", 10)),
        "vdi_get": lambda a: c.get(a["id"]), "vdi_brief": lambda a: c.brief(**a), "vdi_checklist": lambda a: c.checklist(a["stage"]),
        "vdi_lint_script": lambda a: c.lint_script(a["text"]), "vdi_gate_spec": lambda a: c.gate()}
cases = json.load(open(os.path.join(HERE, "evals.json")))["cases"]; rows = []; ok_n = 0
for k in cases:
    out = CALL[k["tool"]](k["args"]); blob = json.dumps(out, ensure_ascii=False)
    ids = [i for i in k.get("expect_ids_any", []) if i in blob]
    ph = [p for p in k.get("expect_phrases", []) if p.lower() in blob.lower()]
    ok = (not k.get("expect_ids_any") or bool(ids)) and len(ph) == len(k.get("expect_phrases", []))
    ok_n += ok
    rows.append(dict(id=k["id"], question=k["question"], tool=k["tool"], passed=ok, ids_found=ids,
                     phrases_missing=[p for p in k.get("expect_phrases", []) if p not in ph]))
    print(f"{'PASS' if ok else 'FAIL'}  {k['id']}  {k['tool']:<16} ids {ids or '-'}  missing {rows[-1]['phrases_missing'] or '-'}")
print(f"\n{ok_n}/{len(cases)} guidance evals pass")
json.dump(dict(ran_at=time.strftime("%Y-%m-%d %H:%M:%S"), passed=ok_n, total=len(cases), cases=rows), open(os.path.join(HERE, "results.json"), "w"), indent=1)
md = ["# VDI MCP guidance evals - results", "", f"Run {time.strftime('%Y-%m-%d %H:%M')} with `python3 mcp/evals/run_evals.py`: **{ok_n}/{len(cases)} pass**.", "",
      "These are deterministic checks that the engine returns the expected guidance for questions an editing agent would ask. They do not measure how well a model uses the tools (no LLM-in-the-loop run yet).", "",
      "| id | question | tool | result | expected ids found | phrases missing |", "|---|---|---|---|---|---|"]
for r in rows: md.append(f"| {r['id']} | {r['question']} | {r['tool']} | {'PASS' if r['passed'] else 'FAIL'} | {', '.join(r['ids_found']) or '-'} | {', '.join(r['phrases_missing']) or '-'} |")
open(os.path.join(HERE, "results.md"), "w").write("\n".join(md) + "\n")
sys.exit(0 if ok_n == len(cases) else 1)
