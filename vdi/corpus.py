#!/usr/bin/env python3
"""corpus.py - read-only engine over the Video Design Intelligence corpus (stdlib only).

Loads the topic packs' markdown, the lessons file, the gate spec and manifest schema, and answers the
queries the MCP server exposes: search, get by id, production brief, stage checklist, script lint, gate
spec. Nothing here writes to disk. Rule ids look like VDI-05-R03; patterns -Pnn, anti-patterns -Ann,
examples -Enn; topic ids VDI-05; files can also be fetched by repo-relative path.
"""
from __future__ import annotations
import glob, json, os, re
from functools import lru_cache

from .paths import REPO, RELEASE_DATA, EXAMPLES, corpus_dir
STAGES = ["script", "shoot", "pickups", "screen", "edit", "captions", "audio", "review", "publish"]
PLATFORMS = ["tiktok", "reels", "shorts", "x"]
RULE_RE = re.compile(r"^- \*\*(VDI-(\d\d)-R\d\d)\*\* · (\w+) · stage: ([\w, ]+) — (.*)$")
HEAD_RE = re.compile(r"^## (VDI-(\d\d)-[PE]\d\d) (.*)$")
ANTI_RE = re.compile(r"^\| (VDI-(\d\d)-A\d\d) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$")
LABEL_RE = re.compile(r"\[(AX|SRC) ([a-z0-9-]+)(?::([^\]]*))?\]|\[UNVERIFIED[^\]]*\]")
WORD_RE = re.compile(r"[a-z0-9]+")
STOP = set("a an the and or of to in on for with is are be it its this that as at by from not no do does".split())

def _read(p):
    with open(p, encoding="utf-8") as f: return f.read()

def _strip_fm(txt):
    if txt.startswith("---\n"):
        e = txt.find("\n---", 4)
        if e > 0: return txt[e + 4:].lstrip("\n")
    return txt

def provenance(text):
    """Split labels in a text into measured / sourced / unverified."""
    out = {"measured_internally": [], "sourced": [], "unverified": False}
    for m in LABEL_RE.finditer(text):
        if m.group(0).startswith("[UNVERIFIED"): out["unverified"] = True
        elif m.group(1) == "AX": out["measured_internally"].append((m.group(2) + (": " + m.group(3).strip() if m.group(3) else "")))
        else: out["sourced"].append(m.group(2))
    return out

def _tok(s): return [w for w in WORD_RE.findall(s.lower()) if w not in STOP]

class Corpus:
    def __init__(self, root=None):
        root = str(root or corpus_dir())
        self.root = root
        self.topics = json.load(open(os.path.join(root, "topics.json")))
        self.by_num = {t["num"]: t for t in self.topics}
        self.gate_spec = json.load(open(RELEASE_DATA / "gate-spec.json"))
        self.manifest_schema = json.load(open(RELEASE_DATA / "manifest.schema.json"))
        self.items, self.chunks, self.files, self.sources = {}, [], {}, {}
        for t in self.topics:
            self.items[f"VDI-{t['num']}"] = dict(id=f"VDI-{t['num']}", type="topic", topic=t["folder"], title=t["title"],
                                                 stages=t["stages"], text=t["summary"], path=f"corpus/{t['folder']}/README.md")
            for p in sorted(glob.glob(os.path.join(root, t["folder"], "**", "*.md"), recursive=True)):
                rel = "corpus/" + os.path.relpath(p, root); body = _strip_fm(_read(p)); self.files[rel] = body
                self._parse(t, rel, body)
            sj = os.path.join(root, t["folder"], "sources", "sources.json")
            if os.path.exists(sj):
                for s in json.load(open(sj))["sources"]: self.sources[s["id"]] = s
        extra = {"corpus/lessons/VDI-LESSONS-001_AX_series.md": os.path.join(root, "lessons", "VDI-LESSONS-001_AX_series.md"),
                 "corpus/lessons/VDI-LESSONS-002_AX_inbox_2026-11-23.md": os.path.join(root, "lessons", "VDI-LESSONS-002_AX_inbox_2026-11-23.md"),
                 "AGENTS.md": str(REPO / "AGENTS.md"), "docs/release-gate.md": str(REPO / "docs" / "release-gate.md"),
                 "docs/release-gate-proof-v4.md": str(REPO / "docs" / "release-gate-proof-v4.md"),
                 "docs/quick-check.md": str(REPO / "docs" / "quick-check.md")}
        for rel, p in extra.items():
            if os.path.exists(p):
                body = _strip_fm(_read(p)); self.files[rel] = body
                self._chunk(None, rel, body)
        lp = os.path.join(root, "lessons", "VDI-LESSONS-001_AX_series.md")
        if os.path.exists(lp):
            self.items["VDI-LESSONS-001"] = dict(id="VDI-LESSONS-001", type="lessons", topic="lessons", title="AX series lessons", text=_strip_fm(_read(lp)), path="corpus/lessons/VDI-LESSONS-001_AX_series.md")
        lp2 = os.path.join(root, "lessons", "VDI-LESSONS-002_AX_inbox_2026-11-23.md")
        if os.path.exists(lp2):
            self.items["VDI-LESSONS-002"] = dict(id="VDI-LESSONS-002", type="lessons", topic="lessons", title="AX lessons, v5 edit (2026-11-23)", text=_strip_fm(_read(lp2)), path="corpus/lessons/VDI-LESSONS-002_AX_inbox_2026-11-23.md")
        self.items["VDI-GATE"] = dict(id="VDI-GATE", type="gate-spec", topic="release-gate", title="Release gate spec", text=json.dumps(self.gate_spec, indent=1), path="vdi/release_data/gate-spec.json")

    def _parse(self, t, rel, body):
        lines = body.splitlines()
        for i, line in enumerate(lines):
            m = RULE_RE.match(line)
            if m:
                rid, num, kind, stage, rest = m.groups()
                text, _, tail = rest.partition(" Check: ")
                check = LABEL_RE.split(tail)[0].strip() if tail else ""
                self.items[rid] = dict(id=rid, type="rule", topic=t["folder"], kind=kind, stages=[s.strip() for s in stage.split(",")],
                                       text=text.strip(), check=re.sub(r"\s*\[.*$", "", tail).strip(), provenance=provenance(rest), path=rel, raw=line)
                continue
            m = HEAD_RE.match(line)
            if m:
                iid, num, title = m.groups(); body_lines = []
                for l2 in lines[i + 1:]:
                    if l2.startswith("## "): break
                    body_lines.append(l2)
                txt = "\n".join(body_lines).strip()
                typ = "pattern" if "-P" in iid else "example"
                self.items[iid] = dict(id=iid, type=typ, topic=t["folder"], title=title, text=txt, provenance=provenance(txt), path=rel)
                continue
            m = ANTI_RE.match(line)
            if m:
                aid, num, name, shows, fix, ev = m.groups()
                self.items[aid] = dict(id=aid, type="anti-pattern", topic=t["folder"], title=name, text=f"{shows} Fix: {fix}", evidence=ev, provenance=provenance(ev), path=rel)
        self._chunk(t, rel, body)

    def _chunk(self, t, rel, body):
        stage_list = t["stages"] if t else []
        cur, buf = None, []
        def flush():
            txt = "\n".join(buf).strip()
            if len(txt) > 40: self.chunks.append(dict(path=rel, topic=t["folder"] if t else rel.split("/")[0], heading=cur, text=txt, stages=stage_list, tokens=_tok((cur or "") + " " + txt)))
        for line in body.splitlines():
            if line.startswith("#"):
                flush(); cur, buf = line.lstrip("# ").strip(), []
            elif line.startswith("- **VDI-"):
                flush(); buf = [line]; flush(); buf = []
            else: buf.append(line)
        flush()

    # ---------------------------------------------------------------- queries
    def search(self, query, topic=None, stage=None, limit=10):
        q = _tok(query)
        if not q: return dict(query=query, total=0, items=[], note="Empty query after removing stop words.")
        res = []
        for c in self.chunks:
            if topic and not (c["topic"].startswith(topic) or topic.lower() in c["topic"].lower()): continue
            if stage and stage not in c["stages"] and f"stage: {stage}" not in c["text"]: continue
            hit = sum(1 for w in set(q) if w in c["tokens"])
            if not hit: continue
            # distinct query terms matched dominate; raw counts only break ties; rules (prescriptive) rank first
            score = 10 * hit + min(5, sum(c["tokens"].count(w) for w in q)) + 2 * sum(1 for w in q if w in (c["heading"] or "").lower())
            if c["text"].startswith("- **VDI-"): score += 8
            if score: res.append((score, c))
        res.sort(key=lambda x: -x[0])
        items = []
        for sc, c in res[:limit]:
            rid = re.match(r"- \*\*(VDI-\d\d-R\d\d)", c["text"])
            items.append(dict(score=sc, id=rid.group(1) if rid else None, topic=c["topic"], path=c["path"], heading=c["heading"],
                              text=c["text"][:600], provenance=provenance(c["text"])))
        return dict(query=query, topic=topic, stage=stage, total=len(res), items=items)

    def get(self, id_):
        key = id_.strip()
        if key.upper() in self.items: return self.items[key.upper()]
        if key in self.files: return dict(id=key, type="file", path=key, text=self.files[key])
        if "corpus/" + key in self.files: return dict(id="corpus/" + key, type="file", path="corpus/" + key, text=self.files["corpus/" + key])
        if key in self.sources: return dict(id=key, type="source", **self.sources[key])
        for t in self.topics:
            if key.lower() in (t["folder"].lower(), t["folder"][3:].lower()): return self.items[f"VDI-{t['num']}"]
        return None

    def rules(self, stage=None, topic=None):
        out = [r for r in self.items.values() if r["type"] == "rule"]
        if stage: out = [r for r in out if stage in r["stages"]]
        if topic: out = [r for r in out if r["topic"].startswith(topic)]
        return sorted(out, key=lambda r: r["id"])

    def checklist(self, stage):
        if stage not in STAGES: return None
        rs = self.rules(stage=stage)
        gate = [c for c in GATE_BY_STAGE.get(stage, [])]
        return dict(stage=stage, rules=[dict(id=r["id"], kind=r["kind"], rule=r["text"], check=r["check"], provenance=r["provenance"]) for r in rs],
                    gate_checks=gate, exit_condition=EXIT, note="Rules are Seed status: derived from one series (AX) and cited sources; [UNVERIFIED] marks house rules.")

    def brief(self, video_type, platform, duration_s, has_talking_head, has_screen_demo):
        plats = [p.strip().lower() for p in re.split(r"[,\s]+", platform or "") if p.strip()]
        if "all" in plats or not plats: plats = list(PLATFORMS)
        bad = [p for p in plats if p not in PLATFORMS]
        if bad: return dict(error=f"unknown platform(s) {bad}; use any of {PLATFORMS} or 'all'")
        warnings = []
        th = self.gate_spec["thresholds"]
        if duration_s < th["container"]["min_duration_s"] or duration_s > th["container"]["max_duration_s"]:
            warnings.append(f"{duration_s} s is outside the house window {th['container']['min_duration_s']}-{th['container']['max_duration_s']} s (gate container check will FAIL unless gate-spec.json is changed for this video) [UNVERIFIED window]")
        if "shorts" in plats and duration_s > 60: warnings.append("YouTube: a Short over one minute with an active copyright claim is blocked globally; use no third-party audio/footage or clear it [SRC yt-shorts-3min]")
        if "x" in plats and duration_s > 140: warnings.append("X: secondary docs report a 140 s limit for standard uploads [SRC ayrshare-x]")
        if "reels" in plats and duration_s > 90: warnings.append("Instagram previously advised against Reels over 90 s [SRC smt-ig-3min]")
        stages = ["script"] + (["shoot", "pickups"] if has_talking_head else []) + (["screen"] if has_screen_demo else []) + ["edit", "captions", "audio", "review", "publish"]
        def pick(stage, topics=None):
            return [dict(id=r["id"], kind=r["kind"], rule=r["text"], check=r["check"], provenance=r["provenance"])
                    for r in self.rules(stage=stage) if not topics or r["topic"][:2] in topics]
        script_rules = pick("script")
        capture = (pick("shoot") + pick("pickups") if has_talking_head else []) + (pick("screen") if has_screen_demo else [])
        edit = pick("edit") + pick("captions") + pick("audio")
        if not has_talking_head: edit = [r for r in edit if r["id"][:6] not in ("VDI-08",)]
        return dict(
            video_type=video_type, platforms=plats, duration_s=duration_s, has_talking_head=has_talking_head, has_screen_demo=has_screen_demo,
            status="Seed guidance: from one series (AX) plus cited platform docs; nothing reviewed by a human.",
            exit_condition=EXIT, warnings=warnings,
            format=dict(width=th["container"]["width"], height=th["container"]["height"], fps=th["container"]["fps"],
                        codecs=f"{th['container']['video_codec']} + {th['container']['audio_codec']}",
                        loudness=f"{th['loudness']['integrated_lufs']} LUFS +-{th['loudness']['tolerance_lu']}, true peak <= {th['loudness']['max_true_peak_dbtp']} dBTP on the final AAC",
                        caption_safe_area="top 8%, bottom 20%, right 12% clear (AX house) [UNVERIFIED]",
                        platform_notes=[PLATFORM_NOTES[p] for p in plats]),
            shot_list_skeleton=skeleton(video_type, duration_s, has_talking_head, has_screen_demo),
            script_rules=script_rules, capture_checklist=capture, edit_rules=edit,
            edit_thresholds={k: {kk: vv for kk, vv in v.items() if kk != "basis"} for k, v in th.items() if k in ("shots", "blank_panel", "word_endings", "ending", "sentence_gaps", "join_level", "dropouts", "captions", "evidence", "face")},
            review_plan=dict(rules=pick("review"), steps=[
                "Run `vdi check` on every draft render, then `vdi release <final.mp4> --manifest <manifest.json>`; fix every FAIL.",
                "Make a 540x960 review copy under 2.9 MB; review it with an AI tool that ingests the video itself (AX: Google AI Studio), and verify every claim it makes against frames/audio.",
                "Independent review (not the editor) with each topic's CHECKLISTS.md; answer every question with a timestamp.",
                "Human listen at every flagged timestamp; blind A/B if the audio chain changed.",
                "Owner's own OK. Only then call it final."]),
            gate_settings=dict(command="vdi release <final.mp4> --manifest <manifest.json>", precheck="vdi check <render.mp4> --platform <p>",
                               manifest_template=manifest_template(video_type, has_talking_head, has_screen_demo),
                               cannot_check=self.gate_spec["cannot_check"]),
            stages=stages)

    def lint_script(self, text):
        return lint(text)

    def gate(self):
        proof = None
        pp = str(EXAMPLES / "v4" / "receipts" / "summary.json")
        if os.path.exists(pp): proof = json.load(open(pp))
        return dict(usage="vdi release <final.mp4> --manifest <manifest.json> [--out DIR] ; exit 0 = PASS (WARN allowed), 1 = FAIL, 2 = could not run. Manifest-free pre-check: vdi check <render.mp4>",
                    rule=self.gate_spec["rule"], version=self.gate_spec["version"], status=self.gate_spec["status"],
                    thresholds=self.gate_spec["thresholds"], cannot_check=self.gate_spec["cannot_check"],
                    manifest_schema=self.manifest_schema, proof_on_known_bad_files=proof,
                    docs=["docs/release-gate.md", "docs/release-gate-proof-v4.md", "docs/quick-check.md"])

    def list_topics(self):
        return [dict(id=f"VDI-{t['num']}", folder=t["folder"], title=t["title"], stages=t["stages"], summary=t["summary"],
                     rules=len(self.rules(topic=t["folder"]))) for t in self.topics]

EXIT = ("No 'final' until (1) `vdi release` exits 0 on the rendered mp4, (2) an independent review says READY, "
        "(3) the owner says so himself. (AGENTS.md)")

GATE_BY_STAGE = {
 "script": ["spoken words vs script (after the edit: every difference must be owner-accepted)"],
 "shoot": ["word endings against the source envelopes (needs a clean final consonant and a hold)", "face continuity (capture sheet makes pickups match)"],
 "pickups": ["face continuity (skin dE < 3.5)", "1 s speech-level step across joins (< 2 dB)", "room tone through joins (no digital zero)"],
 "screen": ["evidence lines (whole, still, >= 28 px, >= 1.6 s)", "run ids and source labels", "PII and plan-wall sweep"],
 "edit": ["shot lengths (>= 12 frames)", "black or blank panels", "word endings", "ending hold 0.6-1.0 s", "inter-sentence gaps >= 0.12 s", "evidence lines", "face continuity"],
 "captions": ["captions match the final audio (both ASR models agree)", "caption safe area", "caption clearance >= 48 px", "caption timing (WARN only)"],
 "audio": ["loudness and true peak on the final", "1 s speech-level step across joins", "room tone through joins", "word endings"],
 "review": ["all gate checks; plus independent review and owner OK (not automatable)"],
 "publish": ["container (1080x1920, 30 fps, H.264+AAC, house duration window)", "caption safe area"],
}

PLATFORM_NOTES = {
 "tiktok": "TikTok: ads docs recommend 9:16 at >= 540x960; non-Spark ads up to 10 min; safe zone depends on dimension and ad caption length (use TikTok's overlay files) [SRC tiktok-specs]. Ads guidance: hook in the first 6 s, proposition in the first 3 s, text at 5-10 words per second, >= 720p, DIY style [SRC tiktok-creative]. Organic limits not fetched (SEED).",
 "reels": "Instagram Reels: up to 3 min since Jan 2025; earlier guidance was not to exceed 90 s [SRC smt-ig-3min]. Meta recommends 9:16 with audio, key messages in the Reels safe zone; >75% of Reels views on Instagram are sound on [SRC meta-reels-blog]. Reported overlay: 14% top, 35% bottom, 6% sides (secondary) [SRC adkit-meta-safe].",
 "shorts": "YouTube Shorts: square or vertical up to 3 min (standard channels, uploads after 15 Oct 2024); over 1 min with an active copyright claim = blocked globally [SRC yt-shorts-3min]. Retention metric: 'Stayed to watch' [SRC yt-analytics]. Playback normalisation turns loud content down, never quiet content up [SRC prodadvice-yt].",
 "x": "X: secondary docs report 0.5-140 s, aspect 1:3 to 3:1, max 1280x1024 for API uploads [SRC ayrshare-x]. Not verified against X's own pages (SEED).",
}

def skeleton(video_type, dur, th, sd):
    hold = 0.7; body = max(5.0, dur - hold)
    beats = [("hook", 0.10, "ON CAMERA" if th else "SCREEN + on-screen text", "Problem or proposition in the first sentence; start on the first syllable; punch-in lands on the payoff word. [SRC tiktok-creative] [AX lessons-001: hooks]")]
    if th: beats.append(("who / what", 0.10, "ON CAMERA + lower third", "Name and company in one breath; lower third clear of captions by >= 48 px. [AX ax-gr4: #2]"))
    if sd:
        beats += [("set up the demo", 0.12, "SCREEN (real run)", "Show the real prompt/command, typed; narrow terminal 44-60 columns at 30 px. [AX lessons-001: 3.3]"),
                  ("claim 1 + proof", 0.18, "SCREEN (same run)", "Each spoken claim lands on its proof line, whole and still >= 1.6 s. [AX lessons-001: 1.4, 4]"),
                  ("claim 2 + proof", 0.18, "SCREEN (same run)", "One run per claim, or a visible source label. [AX lessons-001: 3.2]")]
    else:
        beats += [("point 1", 0.22, "ON CAMERA" if th else "SCREEN", "One idea per beat, <= ~12 words per sentence. [AX lessons-001: 1.2]"),
                  ("point 2", 0.22, "ON CAMERA or real B-roll" if th else "SCREEN", "Real footage only; no generated centerpiece. [AX wdi-27]")]
    beats.append(("payoff / proof of result", 0.12, "SCREEN" if sd else ("ON CAMERA" if th else "SCREEN"), "The result the hook promised, shown, not just said. [AX lessons-001: 1.4]"))
    beats.append(("CTA", 0.10, "ON CAMERA" if th else "SCREEN + end card", "One action; no URL read aloud; end card text clear of captions. [AX ax-boards: CTA DO lines]"))
    tot = sum(b[1] for b in beats); t = 0.0; out = []
    for name, w, where, note in beats:
        d = body * w / tot; out.append(dict(beat=name, start_s=round(t, 1), end_s=round(t + d, 1), shot=where, note=note)); t += d
    out.append(dict(beat="ending hold", start_s=round(t, 1), end_s=round(dur, 1), shot="hold last frame", note="0.6-0.8 s after the last word, audio decaying into room tone. [AX ax-gr4: #3] [UNVERIFIED value]"))
    return dict(video_type=video_type, note="Proportional skeleton; re-time beats to the words once the script exists.", beats=out)

def manifest_template(video_type, th, sd):
    return {"id": "<series-id>-v1", "platform": "tiktok,reels,shorts", "script_text": "<full intended script>",
            "proper_nouns": ["<names, products, handles>"], "accepted_deviations": [],
            "caption_band_px": [1000, 1380],
            "source_audio": ([{"path": "<raw take .mov>", "label": "take", "kind": "camera"}] if th else []) + [{"path": "<each pickup / voice-over file>", "label": "pickup", "kind": "voice"}],
            "evidence_beats": ([{"id": "b01", "t0": 0.0, "t1": 0.0, "text": "<exact proof line>", "run_id": "<run id>", "source_label": None, "claim": "<claim id>"}] if sd else [])}

CLAIM_WORDS = re.compile(r"\b(build|builds|built|check|checks|checked|fix|fixes|fixed|pass|passes|passed|fail|fails|failed|merged|reviewed|official|open[- ]source|license|licensed|free|no card|trial|tested|verified|proves?|measured|every|never|always|only|first|fastest|best|guarantee[sd]?|secure|catalog|refused|names?|says?)\b", re.I)

def lint(text):
    paras = [p.strip() for p in re.split(r"\n\s*\n|\n", text or "") if p.strip()]
    sentences = []
    for p in paras:
        for s in re.split(r"(?<=[.!?])\s+", p):
            if s.strip(): sentences.append(s.strip())
    out_s, flags = [], []
    for i, s in enumerate(sentences):
        n = len(re.findall(r"[A-Za-z0-9'’@.-]+", s))
        f = []
        if n > 20: f.append("over 20 words: split it (FAIL) [AX lessons-001: 1.2]")
        elif n > 12: f.append("over ~12 words: likely to be rushed, truncated or mis-captioned (WARN) [AX lessons-001: 1.2] [UNVERIFIED threshold]")
        claims = sorted(set(m.group(0).lower() for m in CLAIM_WORDS.finditer(s)))
        nums = re.findall(r"\b\d[\d.,:%x]*\b", s)
        if claims or nums: f.append("claim: needs an on-screen proof line from the same run while it is said [AX lessons-001: 1.4]")
        out_s.append(dict(n=i + 1, text=s, words=n, claim_words=claims, numbers=nums, flags=f))
    proper = set()
    for s in sentences:
        toks = re.findall(r"@?[A-Za-z][A-Za-z0-9'’.-]*", s)
        for j, w in enumerate(toks):
            if w.startswith("@") or re.search(r"[A-Z].*[A-Z]", w) or re.search(r"\d", w) or (j > 0 and w[0].isupper() and w.lower() not in ("i", "i'm", "i’m")):
                proper.add(w.strip(".,"))
    board = [dict(beat=k + 1, chars=len(p), text=p[:80], verdict="FAIL: over 70 characters; split into 4a/4b/4c") for k, p in enumerate(paras) if len(p) > 70]
    hook = out_s[0] if out_s else None
    return dict(sentences=out_s, sentence_count=len(out_s),
                long_sentences=[s["n"] for s in out_s if s["words"] > 12],
                board_truncation_risk=dict(beats=board, max_chars_per_beat=70, passes=not board, note="One SAY line per beat, 70 characters or less (one beat per line or paragraph in the input). ASV Command's 'Build board from script' cuts SAY lines at three wrapped lines with an ellipsis and the performer reads boards verbatim (18 cut lines on AX). [AX lessons-001: 1.1]"),
                claims_needing_proof=[dict(n=s["n"], text=s["text"], claim_words=s["claim_words"], numbers=s["numbers"]) for s in out_s if s["claim_words"] or s["numbers"]],
                proper_nouns_check_by_ear=sorted(proper),
                hook=dict(text=hook["text"], words=hook["words"], ok=hook["words"] <= 12) if hook else None,
                notes=["Captions must follow what is actually said; list deviations for the owner. [AX lessons-001: 1.3]",
                       "ASR models mishear proper nouns; put every name above on the manifest's proper_nouns list. [AX lessons-001: 5.6]"])

@lru_cache(maxsize=1)
def corpus():
    return Corpus()
