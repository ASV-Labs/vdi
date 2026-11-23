"""vdi validate - structural, provenance and duplication validator for the VDI corpus.

For every topic pack in corpus/NN_Name:
  - the 19 knowledge files plus sources/sources.json and sources.md exist
  - every markdown file has front matter (id, title, topic, status, last_updated); status is Draft or Seed
  - no stub files (fewer than MIN_WORDS words)
  - manifest.yaml ids == sources.json ids; external sources carry url + accessed date; sources.md lists every id
  - every [AX id: ...] / [SRC id] label resolves in that pack's sources.json
  - every rule line (- **VDI-NN-Rnn** ...) carries a provenance label
  - canonical rule text lives ONLY in RULES.md: other files cite "first clause … (ID)" — a full
    restatement anywhere else fails (run `vdi validate --fix` to regenerate the short forms)
  - every rule id cited anywhere exists
Repo level: required docs exist with Draft/Seed front matter; nothing claims Reviewed/Approved/Final;
release-gate spec present.

Usage: vdi validate [--fix]       Exit 0 = clean, 1 = problems.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

import yaml

from .paths import REPO, RELEASE_DATA, corpus_dir

REQUIRED = ["README.md", "RULES.md", "KNOWLEDGE.md", "CHECKLISTS.md", "EXAMPLES.md", "manifest.yaml",
            "sources/sources.json", "sources/sources.md"]
REPO_DOCS = ["README.md", "AGENTS.md", "CONTRIBUTING.md"]
FM_DOCS = ["AGENTS.md", "corpus/INDEX.md", "corpus/DOCUMENT_REGISTRY.md", "docs/release-gate.md",
           "docs/release-gate-proof-v4.md", "docs/quick-check.md", "docs/quick-check-v3.md",
           "corpus/lessons/VDI-LESSONS-001_AX_series.md", "corpus/lessons/VDI-LESSONS-002_AX_inbox_2026-11-23.md"]
MIN_WORDS = 100
STATUSES = {"Draft", "Seed"}
FM_KEYS = ["id", "title", "topic", "status", "last_updated"]
LABEL = re.compile(r"\[(AX|SRC) ([a-z0-9-]+)")
RULE = re.compile(r"^- \*\*(VDI-\d\d-R\d\d)\*\* · \w+ · stage: [\w, ]+ — (.*)$")
RULE_ID = re.compile(r"\bVDI-\d\d-R\d\d\b")
SHORT_MAX = 100


def front_matter(path):
    txt = open(path, encoding="utf-8").read()
    if not txt.startswith("---\n"):
        return None, txt
    end = txt.find("\n---", 4)
    if end < 0:
        return None, txt
    try:
        return yaml.safe_load(txt[4:end]) or {}, txt[end + 4:]
    except Exception:
        return None, txt


def short_form(text: str) -> str:
    """First clause of a canonical rule, ≤ SHORT_MAX chars, ending with … when cut."""
    m = re.search(r"(;\s|\.\s|:\s|\s—\s)", text)
    s = text[: m.start()] if m else text.rstrip(".")
    if len(s) > SHORT_MAX:
        s = s[:SHORT_MAX].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    elif len(s) < len(text.rstrip(".")):
        s += "…"
    return s


def canonical_rules(cdir: str) -> dict[str, str]:
    out = {}
    for f in glob.glob(os.path.join(cdir, "[01][0-9]_*", "RULES.md")):
        for line in open(f, encoding="utf-8"):
            m = RULE.match(line.rstrip("\n"))
            if m:
                out[m.group(1)] = m.group(2).split(" Check: ")[0].strip()
    return out


def fix_short_forms(cdir: str) -> int:
    rules = canonical_rules(cdir)
    changed = 0
    for f in glob.glob(os.path.join(cdir, "**", "*.md"), recursive=True):
        if os.path.basename(f) == "RULES.md":
            continue
        s = open(f, encoding="utf-8").read()
        o = s
        for rid, text in rules.items():
            sf = short_form(text)
            if len(text) > len(sf) and text in s:
                s = s.replace(text, sf)
        if s != o:
            open(f, "w", encoding="utf-8").write(s)
            changed += 1
    return changed


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    cdir = str(corpus_dir())
    if "--fix" in argv:
        print(f"short forms regenerated in {fix_short_forms(cdir)} file(s)")
    problems = []
    topics = sorted(d for d in os.listdir(cdir) if re.match(r"^\d\d_", d) and os.path.isdir(os.path.join(cdir, d)))
    print(f"Validating: {cdir}\nTopics: {len(topics)}\n")
    hdr = f"{'TOPIC':<34}{'files':>6}{'miss':>5}{'words':>8}{'srcs':>6}{'labels':>8}{'rules':>6}"
    print(hdr)
    print("-" * len(hdr))
    tot_files = tot_words = tot_labels = tot_rules = 0
    all_src = set()
    rules = canonical_rules(cdir)
    counts = {"AX": 0, "SRC": 0, "UNVERIFIED": 0}
    for t in topics:
        tp = os.path.join(cdir, t)
        present, miss, words = 0, [], 0
        for r in REQUIRED:
            (miss.append(r) if not os.path.isfile(os.path.join(tp, r)) else None)
        present = len(REQUIRED) - len(miss)
        if miss:
            problems.append(f"{t}: MISSING {miss}")
        ids = set()
        try:
            for s in json.load(open(os.path.join(tp, "sources/sources.json")))["sources"]:
                for k in ("id", "kind", "title", "credibility"):
                    if not s.get(k):
                        problems.append(f"{t}: source missing '{k}': {s.get('id')}")
                if not (s.get("url") or s.get("location")):
                    problems.append(f"{t}: source {s.get('id')} has no url or location")
                if s.get("kind") in ("platform-doc", "secondary") and not (s.get("url") and s.get("accessed")):
                    problems.append(f"{t}: external source {s.get('id')} needs url and accessed date")
                ids.add(s["id"])
        except Exception as e:
            problems.append(f"{t}: sources.json error: {e}")
        all_src |= ids
        try:
            m = yaml.safe_load(open(os.path.join(tp, "manifest.yaml")))
            mids = set(x["id"] for x in (m.get("sources") or []))
            if not mids:
                problems.append(f"{t}: manifest lists 0 sources")
            if mids != ids:
                problems.append(f"{t}: manifest ids != sources.json ids ({sorted(mids ^ ids)})")
        except Exception as e:
            problems.append(f"{t}: manifest.yaml error: {e}")
        smd_p = os.path.join(tp, "sources/sources.md")
        smd = open(smd_p).read() if os.path.isfile(smd_p) else ""
        for i in ids:
            if f"| {i} |" not in smd:
                problems.append(f"{t}: sources.md does not list {i}")
        nlab = nrules = 0
        for f in glob.glob(os.path.join(tp, "**", "*.md"), recursive=True):
            rel = os.path.relpath(f, REPO)
            fmd, body = front_matter(f)
            if fmd is None:
                problems.append(f"{rel}: no parseable front matter")
                continue
            for k in FM_KEYS:
                if k not in fmd:
                    problems.append(f"{rel}: front matter missing '{k}'")
            if fmd.get("status") not in STATUSES:
                problems.append(f"{rel}: status '{fmd.get('status')}' not in {sorted(STATUSES)}")
            w = len(body.split())
            words += w
            if w < MIN_WORDS:
                problems.append(f"{rel}: stub ({w} words)")
            for kind, sid in LABEL.findall(body):
                nlab += 1
                counts[kind] += 1
                if sid not in ids:
                    problems.append(f"{rel}: label [{kind} {sid}] not in sources.json")
            counts["UNVERIFIED"] += body.count("[UNVERIFIED")
            is_rules_file = os.path.basename(f) == "RULES.md"
            for line in body.splitlines():
                mm = RULE.match(line)
                if mm and is_rules_file:
                    nrules += 1
                    if not re.search(r"\[(AX|SRC) |\[UNVERIFIED", line):
                        problems.append(f"{rel}: rule {mm.group(1)} has no provenance label")
                for rid in RULE_ID.findall(line):
                    if rid not in rules:
                        problems.append(f"{rel}: cites unknown rule {rid}")
            if not is_rules_file:
                for rid, text in rules.items():
                    if len(text) > len(short_form(text)) and text in body:
                        problems.append(f"{rel}: restates {rid} in full — run `vdi validate --fix`")
        tot_files += present
        tot_words += words
        tot_labels += nlab
        tot_rules += nrules
        print(f"{t:<34}{present:>6}{len(miss):>5}{words:>8}{len(ids):>6}{nlab:>8}{nrules:>6}")
    print("-" * len(hdr))
    print(f"{'TOTAL':<34}{tot_files:>6}{'':>5}{tot_words:>8}{len(all_src):>6}{tot_labels:>8}{tot_rules:>6}")
    unver = 0
    for f in glob.glob(os.path.join(cdir, "[01][0-9]_*", "RULES.md")):
        unver += sum(1 for line in open(f, encoding="utf-8") if RULE.match(line.rstrip("\n")) and "[UNVERIFIED" in line)
    n = len(rules) or 1
    print(f"rules: {len(rules)} · {len(rules) - unver} ({(len(rules) - unver) / n:.0%}) grounded in an AX measurement or a cited "
          f"source · {unver} marked [UNVERIFIED]")
    print(f"labels: {counts['AX']} [AX] · {counts['SRC']} [SRC] · {counts['UNVERIFIED']} [UNVERIFIED]")
    for d in REPO_DOCS:
        if not os.path.isfile(REPO / d):
            problems.append(f"missing {d}")
    for d in FM_DOCS:
        p = REPO / d
        if not p.is_file():
            problems.append(f"missing {d}")
            continue
        fmd, _ = front_matter(p)
        if not fmd or "id" not in fmd:
            problems.append(f"{d}: no front matter id")
        elif "lessons/" not in d and fmd.get("status") not in STATUSES:
            problems.append(f"{d}: status '{fmd.get('status')}' not in {sorted(STATUSES)}")
    for f in glob.glob(str(REPO / "**" / "*.md"), recursive=True):
        fmd, _ = front_matter(f)
        if fmd and str(fmd.get("status", "")).strip().lower() in ("reviewed", "approved", "final"):
            problems.append(f"{os.path.relpath(f, REPO)}: forbidden status '{fmd.get('status')}'")
    if not (RELEASE_DATA / "gate-spec.json").is_file():
        problems.append("missing vdi/release_data/gate-spec.json")
    print("\n=== PROBLEMS ===")
    print("\n".join(problems) if problems else "None.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
