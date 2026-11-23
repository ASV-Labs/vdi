#!/usr/bin/env python3
"""vdi release - the VDI release gate for short-form video (formerly video_gate.py; logic unchanged).

    vdi release <final.mp4> --manifest <manifest.json> [--out DIR] [--cache DIR] [--skip-asr] [--skip-ocr]

Every check measures the RENDERED file: ffprobe/ebur128 on the container, frames decoded from the
mp4 (shot detection, blank panels, skin colour), tesseract OCR of frames (captions, evidence lines,
source labels, PII), faster-whisper small.en AND medium.en on the final audio (both must agree), and
the final audio's envelopes compared with the SOURCE audio files named in the manifest (word endings,
joins, level steps). Nothing is read from an edit plan.

The manifest declares intent only: the script text, proper nouns, owner-accepted spoken deviations,
evidence beats (time window, exact text that must be readable, run id, source label, claim id) and
the source audio paths. See vdi/release_data/manifest.schema.json and examples/v4/manifests/.

Exit code: 0 = every check PASS (WARN allowed), 1 = at least one FAIL, 2 = could not run.
Output: <out>/<id>.gate.json and <out>/<id>.gate.md (one page).

Needs: ffmpeg/ffprobe, tesseract 5 (+eng), and `pip install -e ".[release]"` (faster-whisper, opencv, scipy).
First run downloads the small.en and medium.en Whisper models (roughly 2 GB) to the Hugging Face cache.
Runtime on 2 CPU cores, no GPU: roughly 5-8 minutes for a 45 s short (ASR and OCR dominate).
OCR and ASR results are cached per file hash, so a re-run after a manifest change is fast.
"""
from __future__ import annotations
import argparse, difflib, hashlib, json, os, re, subprocess, sys, time
from concurrent.futures import ProcessPoolExecutor
import numpy as np

from .paths import RELEASE_DATA
SPEC = json.load(open(RELEASE_DATA / "gate-spec.json"))
# OCR runs in a process pool; keep OpenMP-built tesseract (Debian/Ubuntu) to one thread per process.
os.environ.setdefault("OMP_THREAD_LIMIT", "1")
TH = SPEC["thresholds"]
SR = 16000

# ----------------------------------------------------------------- small helpers
def sh(cmd, binary=False):
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0 and not binary:
        raise RuntimeError(f"command failed: {' '.join(cmd[:4])}...: {r.stderr.decode()[-400:]}")
    return r.stdout if binary else r.stdout.decode() + r.stderr.decode()

def file_hash(path, n=8 << 20):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        h.update(f.read(n)); f.seek(0, 2); h.update(str(f.tell()).encode())
    return h.hexdigest()[:16]

def decode_audio(path, sr=SR):
    raw = sh(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], binary=True)
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0

def db(x):
    return 20 * np.log10(np.maximum(x, 1e-10))

def env_db(x, sr=SR, ms=10):
    n = int(sr * ms / 1000); k = len(x) // n
    return db(np.sqrt((x[:k * n].reshape(k, n) ** 2).mean(1)))

def norm_word(w):
    w = w.lower().replace("\u2019", "'").replace("\u2018", "'")
    w = re.sub(r"[^a-z0-9@']", "", w)
    return w.replace("'", "")

def words_of(text):
    return [norm_word(w) for w in re.split(r"[\s\u2014\u2013/-]+", text) if norm_word(w)]

def result(name, status, measured, detail=None, catches=None):
    r = {"check": name, "status": status, "measured": measured}
    if detail is not None: r["detail"] = detail
    if catches: r["defect_class"] = catches
    return r

# ----------------------------------------------------------------- 1 container + loudness
def check_container(path):
    out = json.loads(sh(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path]))
    v = next(s for s in out["streams"] if s["codec_type"] == "video")
    a = next((s for s in out["streams"] if s["codec_type"] == "audio"), None)
    dur = float(out["format"]["duration"]); c = TH["container"]
    num, den = map(int, v["r_frame_rate"].split("/")); fps = num / den
    probs = []
    if (v["width"], v["height"]) != (c["width"], c["height"]): probs.append(f"size {v['width']}x{v['height']}")
    if abs(fps - c["fps"]) > 0.01: probs.append(f"fps {fps:.3f}")
    if v["codec_name"] != c["video_codec"]: probs.append(f"video {v['codec_name']}")
    if not a or a["codec_name"] != c["audio_codec"]: probs.append(f"audio {a['codec_name'] if a else 'none'}")
    if not (c["min_duration_s"] <= dur <= c["max_duration_s"]): probs.append(f"duration {dur:.2f} s")
    meas = f"{v['width']}x{v['height']} {fps:.2f} fps {v['codec_name']}+{a['codec_name'] if a else '-'} {dur:.2f} s"
    return result("container", "FAIL" if probs else "PASS", meas, probs or None), dict(w=v["width"], h=v["height"], fps=fps, dur=dur)

def check_loudness(path):
    log = sh(["ffmpeg", "-nostats", "-i", path, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", log)[-1])
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", log)
    TP = float(tp[-1]) if tp else float("nan")
    L = TH["loudness"]; probs = []
    if abs(I - L["integrated_lufs"]) > L["tolerance_lu"]: probs.append(f"integrated {I:.1f} LUFS")
    if not TP <= L["max_true_peak_dbtp"]: probs.append(f"true peak {TP:.1f} dBTP")
    return result("loudness and true peak (ebur128 on the final file)", "FAIL" if probs else "PASS",
                  f"{I:.1f} LUFS integrated, true peak {TP:.1f} dBTP", probs or None)

# ----------------------------------------------------------------- 2 frames: shots, blank panels, skin
def decode_small_frames(path, w=180, h=320):
    raw = sh(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], binary=True)
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)

REGIONS = {"whole": (0.0, 1.0), "upper half": (0.0, 0.5), "lower half": (0.5, 1.0)}

def check_shots(frames, fps):
    T = TH["shots"]; g = frames.mean(axis=3).astype(np.float32); N, H, W = g.shape
    d = np.abs(g[1:] - g[:-1]) > T["pixel_delta"]
    fails, info = [], {}
    for name, (a, b) in REGIONS.items():
        frac = d[:, int(a * H):int(b * H)].mean(axis=(1, 2))
        idx = [i + 1 for i in range(N - 1) if frac[i] > T["hard_change_fraction"]]
        ev = []
        for c in idx:
            if ev and c - ev[-1][-1] <= T["merge_gap_frames"]: ev[-1].append(c)
            else: ev.append([c])
        info[name] = [round(e[0] / fps, 2) for e in ev]
        # shot = from the end of one change event (transition settled) to the start of the next
        bounds = [(0, ev[0][0])] if ev else [(0, N)]
        for e1, e2 in zip(ev, ev[1:]): bounds.append((e1[-1], e2[0]))
        if ev: bounds.append((ev[-1][-1], N))
        for s, e in bounds[1:-1] if len(bounds) > 2 else []:
            if e - s < T["min_shot_frames"]:
                fails.append(dict(region=name, t=round(s / fps, 2), frames=int(e - s)))
    # de-duplicate the same flash seen in several regions
    seen, uniq = set(), []
    for f in sorted(fails, key=lambda x: x["t"]):
        k = round(f["t"] * 5)
        if k in seen: continue
        seen.add(k); uniq.append(f)
    meas = f"{len(info['whole'])} hard changes (whole frame); shortest-shot violations: {len(uniq)}"
    det = [f"{u['frames']}-frame shot at {u['t']:.2f} s ({u['region']})" for u in uniq]
    return result(f"shot lengths (scene detection per region, < {T['min_shot_frames']} frames fails)",
                  "FAIL" if uniq else "PASS", meas, det or None, "flash shots"), info

def check_blank(frames, fps):
    """A panel goes black: a band of near-black rows covering >= 20% of the frame height, for more than one
    frame, where the same rows showed content just before. Dark UI (terminal backgrounds, luma ~10-17)
    is above the black threshold; a long empty region is reported as WARN, not FAIL."""
    T = TH["blank_panel"]; g = frames.mean(axis=3); N, H, W = g.shape
    black_rows = (g.mean(axis=2) < 8) & (g.max(axis=2) < 40)            # N x H
    content_rows = g.std(axis=2) > 12
    fails, warns = [], []
    i = 1
    while i < N:
        R = black_rows[i] & content_rows[i - 1]                          # rows that just went black
        if R.mean() >= 0.2:
            j = i
            while j + 1 < N and (black_rows[j + 1] & R).sum() >= 0.8 * R.sum(): j += 1
            n = j - i + 1
            if n > T["max_blank_frames"] and j < N - 1:
                item = f"{R.mean() * 100:.0f}% of the frame height went black for {n} frames at {i / fps:.2f}-{(j + 1) / fps:.2f} s"
                (fails if n <= T["long_run_frames"] else warns).append(item)
            i = j + 1
        else: i += 1
    st = "FAIL" if fails else ("WARN" if warns else "PASS")
    return result("black or blank panels (> 1 frame between content fails)", st,
                  f"{len(fails)} short black-panel runs, {len(warns)} long ones", (fails + [f"WARN {w}" for w in warns]) or None,
                  "black panel before a screen")

YUNET = os.path.expanduser("~/.cache/vdi-gate/models/yunet.onnx")
YUNET_URL = "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
_det = {}

def face_detector(w, h):
    import cv2
    if not os.path.exists(YUNET):
        os.makedirs(os.path.dirname(YUNET), exist_ok=True)
        subprocess.run(["curl", "-sSL", "-o", YUNET, YUNET_URL])
    if (w, h) not in _det:
        _det[(w, h)] = cv2.FaceDetectorYN.create(YUNET, "", (w, h), 0.85)
    return _det[(w, h)]

def skin_stats(frame):
    """Mean Lab of skin pixels inside the largest detected face (YuNet), or None if no sizeable face."""
    import cv2
    H, W = frame.shape[:2]
    try:
        _, faces = face_detector(W, H).detect(frame)
    except Exception:
        return None
    if faces is None: return None
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])[:4]
    if h < 0.12 * H: return None
    x0, y0 = int(x + 0.2 * w), int(y + 0.25 * h); x1, y1 = int(x + 0.8 * w), int(y + 0.85 * h)
    crop = frame[max(0, y0):y1, max(0, x0):x1]
    if crop.size == 0: return None
    ycc = cv2.cvtColor(crop, cv2.COLOR_BGR2YCrCb)
    m = (ycc[..., 1] > 133) & (ycc[..., 1] < 180) & (ycc[..., 2] > 85) & (ycc[..., 2] < 135) & (ycc[..., 0] > 50)
    if m.mean() < 0.25: return None
    lab = cv2.cvtColor(crop, cv2.COLOR_BGR2LAB).astype(np.float32)[m]
    lab[:, 0] *= 100 / 255; lab[:, 1:] -= 128
    return lab.mean(0), float(w * h)

def check_faces(frames, fps, boundaries):
    """Skin colour either side of every picture change and audio join. dE (CIE76) of mean skin Lab."""
    T = TH["face"]; N = len(frames); out, fails = [], []
    for t in sorted(set(round(b, 2) for b in boundaries)):
        i = int(round(t * fps))
        A = [skin_stats(frames[k]) for k in (i - 7, i - 5, i - 3) if 0 <= k < N]
        B = [skin_stats(frames[k]) for k in (i + 2, i + 4, i + 6) if 0 <= k < N]
        A = [a for a in A if a]; B = [b for b in B if b]
        if len(A) < 2 or len(B) < 2: continue
        la = np.mean([a[0] for a in A], 0); lb = np.mean([b[0] for b in B], 0)
        aa = np.mean([a[1] for a in A]); ab = np.mean([b[1] for b in B])
        if not (0.5 <= ab / aa <= 2.0): continue        # not a face-to-face cut
        dE = float(np.linalg.norm(lb - la)); out.append((t, dE))
        if dE >= T["max_skin_delta_e"]:
            fails.append(f"{t:.2f} s: skin dE {dE:.1f} (L {la[0]:.0f}->{lb[0]:.0f}, b {la[2]:.0f}->{lb[2]:.0f})")
    meas = f"{len(out)} face-to-face boundaries measured" + (f", largest dE {max(d for _, d in out):.1f}" if out else "")
    return result(f"face continuity (skin dE < {T['max_skin_delta_e']} across cuts)", "FAIL" if fails else "PASS",
                  meas, fails or None, "pickup grade mismatch")

# ----------------------------------------------------------------- 3 ASR (both models)
def transcribe(audio, model_name, cache):
    p = os.path.join(cache, f"asr-{model_name}.json")
    if os.path.exists(p): return json.load(open(p))
    from faster_whisper import WhisperModel
    m = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=2)
    segs, _ = m.transcribe(audio, word_timestamps=True, vad_filter=False, beam_size=5)
    out = [[round(w.start, 3), round(w.end, 3), w.word.strip(), round(w.probability, 3)] for s in segs for w in s.words]
    json.dump(out, open(p, "w")); return out

def agree_words(small, medium):
    """Words both models heard (same normalised word, aligned). Returns agreed list and disagreements."""
    a = [norm_word(w[2]) for w in small]; b = [norm_word(w[2]) for w in medium]
    agreed, disagree = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                s, m = small[i1 + k], medium[j1 + k]
                agreed.append(dict(t0=(s[0] + m[0]) / 2, t1=(s[1] + m[1]) / 2, w=norm_word(m[2]), raw=m[2]))
        else:
            disagree.append(dict(t=(medium[j1][0] if j1 < len(medium) else small[i1][0]),
                                 small=" ".join(w[2] for w in small[i1:i2]), medium=" ".join(w[2] for w in medium[j1:j2])))
    return agreed, disagree

# ----------------------------------------------------------------- 4 alignment to sources
def bandpass(x, lo=300, hi=3400, sr=SR):
    from scipy import signal
    return signal.sosfiltfilt(signal.butter(4, [lo / (sr / 2), hi / (sr / 2)], "band", output="sos"), x).astype(np.float32)

def highpass(x, f, sr=SR):
    from scipy import signal
    return signal.sosfiltfilt(signal.butter(4, f / (sr / 2), "high", output="sos"), x).astype(np.float32)

class Source:
    def __init__(self, path, label):
        self.path, self.label = path, label
        self.x = decode_audio(path); self.bp = bandpass(self.x)
        self.env = env_db(self.x); self.envh = env_db(highpass(self.x, TH["word_endings"]["hf_cutoff_hz"]))
        self.cum = np.concatenate([[0.0], np.cumsum(self.bp.astype(np.float64) ** 2)])

def align(final, sources, speech_level):
    """Locate each 0.5 s window of the final's speech in the sources by normalised cross-correlation.
    Returns segments: [{src, offset, t0, t1, ncc}] in final time, offset = src_time - final_time."""
    fb = bandpass(final); e = env_db(final); W, HOP = int(0.5 * SR), int(0.1 * SR)
    ffts = {}
    for k, s in enumerate(sources):
        n = 1 << int(np.ceil(np.log2(len(s.bp) + W))); ffts[k] = (n, np.fft.rfft(s.bp, n))
    wins = []
    for st in range(0, len(fb) - W, HOP):
        fr = e[st // 160:(st + W) // 160]
        if (fr > speech_level - 25).mean() < 0.5: continue
        w = fb[st:st + W]; ew = float((w.astype(np.float64) ** 2).sum())
        if ew <= 0: continue
        best = (0.0, None, None)
        for k, s in enumerate(sources):
            n, F = ffts[k]
            c = np.fft.irfft(F * np.conj(np.fft.rfft(w, n)), n)[:len(s.bp) - W + 1]
            es = s.cum[W:] - s.cum[:-W]
            ncc = c / np.sqrt(es[:len(c)] * ew + 1e-12)
            j = int(np.argmax(ncc))
            if ncc[j] > best[0]: best = (float(ncc[j]), k, j / SR - st / SR)
        if best[0] >= 0.45: wins.append(dict(t0=st / SR, t1=(st + W) / SR, src=best[1], off=best[2], ncc=best[0]))
    segs = []
    for w in wins:
        if segs and segs[-1]["src"] == w["src"] and abs(segs[-1]["off"] - w["off"]) < 0.02 and w["t0"] <= segs[-1]["t1"] + 0.35:
            s = segs[-1]; s["t1"] = w["t1"]; s["n"] += 1; s["ncc"] = max(s["ncc"], w["ncc"])
        else:
            segs.append(dict(src=w["src"], off=w["off"], t0=w["t0"], t1=w["t1"], n=1, ncc=w["ncc"]))
    segs = [s for s in segs if s["n"] >= 2]
    # merge segments split only by a short mismatch
    merged = []
    for s in segs:
        if merged and merged[-1]["src"] == s["src"] and abs(merged[-1]["off"] - s["off"]) < 0.02:
            merged[-1]["t1"] = s["t1"]; merged[-1]["n"] += s["n"]
        else: merged.append(s)
    return merged

def joins_from(segs):
    out = []
    for a, b in zip(segs, segs[1:]):
        tj = (a["t1"] + b["t0"]) / 2 if b["t0"] > a["t1"] else (a["t1"] - 0.25 + b["t0"] + 0.25) / 2
        kind = "source change" if a["src"] != b["src"] else "cut inside one source"
        out.append(dict(t=round(tj, 2), a=a, b=b, kind=kind))
    return out

def check_word_endings(final, sources, segs, labels, dur):
    """At every segment end: where does the final stop reproducing the source, and does the source's
    speech (full band or >=3.5 kHz) carry on past that point? Lost tail >= 60 ms before a pause = FAIL."""
    T = TH["word_endings"]; ef = env_db(final); efh = env_db(highpass(final, T["hf_cutoff_hz"]))
    ffloor = np.percentile(ef, 8); ffloorh = np.percentile(efh, 8)
    fails, warns, rows = [], [], []
    for si, s in enumerate(segs):
        src = sources[s["src"]]; off = s["off"]
        i0, i1 = int(s["t0"] * 100), int(s["t1"] * 100)
        j = lambda i: int(round(i + off * 100))
        idx = [i for i in range(i0, min(i1, len(ef))) if 0 <= j(i) < len(src.env) and src.env[j(i)] > np.percentile(src.env, 50)]
        if len(idx) < 10: continue
        g = float(np.median([ef[i] - src.env[j(i)] for i in idx])); gh = float(np.median([efh[i] - src.envh[j(i)] for i in idx]))
        lo_ = max(0, j(i0) - 100); hi_ = min(len(src.env), j(i1) + 150)
        sfl = np.percentile(src.env[lo_:hi_], 8); sflh = np.percentile(src.envh[lo_:hi_], 8)
        nxt = segs[si + 1]["t0"] if si + 1 < len(segs) else dur
        last_agree = None
        for i in range(max(i0, i1 - 50), min(len(ef), int(min(nxt + 0.4, dur) * 100))):
            k = j(i)
            if not (0 <= k < len(src.env)): break
            speech = src.env[k] > sfl + T["over_floor_db"] or src.envh[k] > sflh + T["over_floor_db"]
            if not speech: continue
            ok = abs(ef[i] - (src.env[k] + g)) < 6 and abs(efh[i] - (src.envh[k] + gh)) < 9
            if ok: last_agree = i
        if last_agree is None: continue
        # how long does the source's speech run on after the last reproduced frame? Gaps shorter than a
        # pause (stop closures, e.g. the /t/ before /s/ in "faceplants") are bridged.
        k0 = j(last_agree) + 1; last_sp = -1; quiet = 0; pause = False; pq = T["pause_after_ms"] // 10
        for q in range(0, 50):
            if k0 + q >= len(src.env): pause = True; break
            if src.env[k0 + q] > sfl + T["over_floor_db"] or src.envh[k0 + q] > sflh + T["over_floor_db"]:
                last_sp = q; quiet = 0
            elif src.env[k0 + q] < sfl + 6 and src.envh[k0 + q] < sflh + 6:
                quiet += 1
                if quiet >= pq: pause = True; break
        lost_ms = (last_sp + 1) * 10
        t_cut = (last_agree + 1) / 100
        lw = [w for w in labels if w[1] <= t_cut + 0.12]
        word = lw[-1][2] if lw else "?"
        rows.append(dict(t=round(t_cut, 2), source=src.label, last_word=word, lost_ms=lost_ms, pause_after=pause))
        if lost_ms >= T["max_lost_tail_ms"]:
            msg = f"{t_cut:.2f} s '{word}': source speech runs {lost_ms} ms past the point the final stops reproducing it ({src.label})"
            (fails if pause else warns).append(msg if pause else msg + "; the source does not pause right after, so this may be a deliberate mid-phrase cut")
    st = "FAIL" if fails else ("WARN" if warns else "PASS")
    return result("word endings against the source envelopes (full band and >= 3.5 kHz)", st,
                  f"{len(rows)} segment ends compared; {len(fails)} lost tails before a pause",
                  (fails + [f"WARN {w}" for w in warns]) or None, "cut word endings"), rows

def check_ending(final, dur):
    T = TH["ending"]; e = env_db(final); eh = env_db(highpass(final, 3500))
    sp = np.percentile(e, 90); sph = np.percentile(eh, 90)
    speech = np.where((e > sp - 28) | (eh > sph - 28))[0]
    last = (speech[-1] + 1) / 100 if len(speech) else 0
    hold = dur - last; tail = float(np.sqrt((final[-int(0.1 * SR):] ** 2).mean()))
    probs = []
    if hold < T["min_hold_s"]: probs.append(f"last sound ends {hold:.2f} s before the file ends (needs {T['min_hold_s']}-{T['max_hold_s']} s)")
    if hold > T["max_hold_s"]: probs.append(f"{hold:.2f} s of tail after the last sound (max {T['max_hold_s']})")
    if db(tail) > sp - T["decayed_below_speech_db"]: probs.append(f"last 100 ms at {db(tail) - sp:.0f} dB re speech: not decayed")
    return result("ending hold after the last word", "FAIL" if probs else "PASS", f"hold {hold:.2f} s after the last sound at {last:.2f} s",
                  probs or None, "abrupt ending")

def check_sentence_gaps(final, medium):
    T = TH["sentence_gaps"]; e = env_db(final); sp = np.percentile(e, 90)
    quiet = e < sp - T["silence_below_speech_db"]; fails, n = [], 0
    for a, b in zip(medium, medium[1:]):
        if not re.search(r"[.?!]$", a[2]): continue
        n += 1
        i0 = max(0, int((a[1] - 0.15) * 100)); i1 = min(len(e), int((b[0] + 0.15) * 100))
        best = run = 0
        for i in range(i0, i1):
            run = run + 1 if quiet[i] else 0; best = max(best, run)
        if best / 100 < T["min_gap_s"]:
            fails.append(f"{a[1]:.2f} s '{a[2]}' -> '{b[2]}': longest pause {best * 10} ms")
    return result(f"inter-sentence gaps (>= {T['min_gap_s']} s below speech -{T['silence_below_speech_db']} dB)",
                  "FAIL" if fails else "PASS", f"{n} sentence boundaries, {len(fails)} rushed", fails or None, "rushed joins")

def check_join_levels(final, joins):
    T = TH["join_level"]; n = int(0.01 * SR); e = env_db(final); sp = np.percentile(e, 90)
    def lvl(t0, t1):
        i0, i1 = max(0, int(t0 * 100)), min(len(e), int(t1 * 100))
        fr = [i for i in range(i0, i1) if e[i] > sp - T["speech_frames_within_db"]]
        if len(fr) < 10: return None
        x = np.concatenate([final[i * n:(i + 1) * n] for i in fr]); return db(np.sqrt((x ** 2).mean()))
    fails, rows = [], []
    for jn in joins:
        L, R = lvl(jn["t"] - T["window_s"], jn["t"]), lvl(jn["t"], jn["t"] + T["window_s"])
        if L is None or R is None: continue
        step = float(R - L); rows.append((jn["t"], step))
        if abs(step) >= T["max_step_db"]: fails.append(f"{jn['t']:.2f} s ({jn['kind']}): {step:+.1f} dB")
    meas = f"{len(rows)} joins measured" + (f", largest step {max(abs(s) for _, s in rows):.1f} dB" if rows else "")
    return result(f"1 s speech-level step across joins (< {T['max_step_db']} dB)", "FAIL" if fails else "PASS", meas, fails or None, "level steps at joins")

def check_dropouts(path):
    x = decode_audio(path, 48000); z = x == 0; runs = []; s = None
    for i in np.flatnonzero(np.diff(np.concatenate([[0], z.astype(np.int8), [0]]))):
        if s is None: s = i
        else:
            if (i - s) / 48 > TH["dropouts"]["max_zero_run_ms"]: runs.append((s / 48000, (i - s) / 48))
            s = None
    runs = [(a_, b_) for a_, b_ in runs if a_ > 0.05 and a_ < len(x) / 48000 - 0.05]
    merged = []
    for a_, b_ in runs:
        if merged and a_ - merged[-1][1] < 0.03: merged[-1][1] = a_ + b_ / 1000; merged[-1][2] += b_
        else: merged.append([a_, a_ + b_ / 1000, b_])
    runs = merged
    det = [f"{a_:.2f} s: {c_:.0f} ms of digital zero" for a_, _, c_ in runs[:12]]
    return result("room tone through joins (no digital-zero dropouts)", "FAIL" if runs else "PASS",
                  f"{len(runs)} zero runs > {TH['dropouts']['max_zero_run_ms']} ms", det or None, "dropouts at joins")

# ----------------------------------------------------------------- 5 OCR
def _ocr_frame(args):
    import cv2, pytesseract
    idx, path, band = args
    im = cv2.imread(path)
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    def data(img, cfg, y_off=0):
        d = pytesseract.image_to_data(img, config=cfg, output_type=pytesseract.Output.DICT)
        words = []
        for k in range(len(d["text"])):
            t = d["text"][k].strip()
            if not t or float(d["conf"][k]) < 0: continue
            words.append(dict(t=t, c=float(d["conf"][k]), x=int(d["left"][k]), y=int(d["top"][k]) + y_off,
                              w=int(d["width"][k]), h=int(d["height"][k])))
        return words
    whole = data(g, "--psm 11")
    caps = []
    if band:
        y0, y1 = band
        hsv = cv2.cvtColor(im[y0:y1], cv2.COLOR_BGR2HSV)
        bright = ((hsv[..., 2] > 215) & (hsv[..., 1] < 60)) | ((hsv[..., 2] > 215) & (hsv[..., 1] > 120) & (hsv[..., 0] < 35))
        caps = data(np.where(bright, 0, 255).astype(np.uint8), "--psm 6", y_off=y0)
    return idx, whole, caps

def rows_of(words, min_conf=40):
    """Group OCR words into visual rows: cluster by vertical centre, then split each cluster at wide
    horizontal gaps (columns). Returns rows left to right with text and box."""
    ws = sorted([w for w in words if w["c"] >= min_conf], key=lambda w: w["y"] + w["h"] / 2)
    clusters = []
    for w in ws:
        cy = w["y"] + w["h"] / 2
        if clusters and abs(clusters[-1]["cy"] - cy) < 0.45 * max(clusters[-1]["h"], w["h"]):
            c = clusters[-1]; c["w"].append(w); c["cy"] = float(np.mean([x["y"] + x["h"] / 2 for x in c["w"]])); c["h"] = max(c["h"], w["h"])
        else:
            clusters.append(dict(cy=cy, h=w["h"], w=[w]))
    out = []
    for c in clusters:
        line = sorted(c["w"], key=lambda w: w["x"]); parts = [[line[0]]]
        for w in line[1:]:
            if w["x"] - (parts[-1][-1]["x"] + parts[-1][-1]["w"]) > 3 * c["h"]: parts.append([w])
            else: parts[-1].append(w)
        for p_ in parts:
            out.append(dict(text=" ".join(w["t"] for w in p_), x0=min(w["x"] for w in p_), x1=max(w["x"] + w["w"] for w in p_),
                            y0=min(w["y"] for w in p_), y1=max(w["y"] + w["h"] for w in p_), words=p_,
                            conf=float(np.mean([w["c"] for w in p_]))))
    return out

def run_ocr(path, fps_v, dur, band, cache, sample_fps):
    """OCR every sampled frame (sample_fps) at 1080x1920. Frames are written to a temp folder as PNG
    (lossless) so memory stays flat; near-identical consecutive frames reuse the previous OCR."""
    import cv2, tempfile, shutil, multiprocessing as mp
    p = os.path.join(cache, f"ocr-{sample_fps}fps-{band[0] if band else 0}-{band[1] if band else 0}.json")
    if os.path.exists(p): return {float(k): v for k, v in json.load(open(p)).items()}
    tmp = tempfile.mkdtemp(prefix="vdi-ocr-")
    try:
        sh(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={sample_fps},scale=1080:1920", os.path.join(tmp, "%05d.png")])
        files = sorted(os.listdir(tmp)); jobs, alias, prev, prev_idx = [], {}, None, None
        for i, f in enumerate(files):
            small = cv2.imread(os.path.join(tmp, f), cv2.IMREAD_REDUCED_COLOR_8).astype(np.int16)
            if prev is not None and small.shape == prev.shape and np.abs(small - prev).mean() < 0.6: alias[i] = prev_idx
            else: jobs.append((i, os.path.join(tmp, f), band)); prev, prev_idx = small, i
        res = {}
        with ProcessPoolExecutor(max_workers=2, mp_context=mp.get_context("spawn")) as ex:
            for idx, whole, caps in ex.map(_ocr_frame, jobs, chunksize=4):
                res[idx] = dict(whole=whole, caps=caps)
        for k, v in alias.items(): res[k] = res[v]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    out = {round(k / sample_fps, 3): v for k, v in sorted(res.items())}
    json.dump(out, open(p, "w")); return out

# ----------------------------------------------------------------- 6 captions
CONFUSE = str.maketrans({"l": "i", "1": "i", "|": "i", "0": "o"})

def ckey(w):
    """Normalise a word for OCR-vs-ASR comparison (folds l/I/1 and 0/O confusions)."""
    return norm_word(w).translate(CONFUSE)

def caption_events(ocr, band, transcript_words):
    """Caption events from the caption band. A band row counts as a caption only if at least half of its
    words match words spoken (either ASR model) within +-1.5 s; other band text is screen text.
    Frames are clustered into events; a word is kept only if OCR read it in >= 40% of the event's
    frames (and >= 2 frames), which removes OCR garble but keeps a stable wrong word."""
    spoken = [(w[0], ckey(w[2])) for w in transcript_words]
    per_frame = []
    for t in sorted(ocr):
        rows = [r for r in rows_of(ocr[t]["caps"], 50) if re.search(r"[A-Za-z]{2}", r["text"])]
        near = set(k for (ts, k) in spoken if t - 1.5 <= ts <= t + 1.0)
        caps = []
        for r in rows:
            ws = [ckey(w["t"]) for w in r["words"] if ckey(w["t"])]
            if not ws: continue
            hit = sum(1 for w in ws if any(fuzzy_eq(w, k) for k in near))
            if hit / len(ws) >= 0.5: caps.append(r)
        per_frame.append((t, caps))
    evs, cur = [], None
    for t, caps in per_frame:
        words = set(ckey(w["t"]) for r in caps for w in r["words"] if ckey(w["t"]))
        if not words:
            if cur: evs.append(cur); cur = None
            continue
        if cur and t - cur["t1"] < 0.25 and len(words & cur["union"]) / max(1, len(words | cur["union"])) >= 0.3:
            cur["frames"].append((t, caps)); cur["t1"] = t; cur["union"] |= words
        else:
            if cur: evs.append(cur)
            cur = dict(t0=t, t1=t, frames=[(t, caps)], union=set(words))
    if cur: evs.append(cur)
    out = []
    for e in evs:
        n = len(e["frames"])
        if n < 2: continue
        cnt = {}
        for _, caps in e["frames"]:
            for w in set(ckey(w["t"]) for r in caps for w in r["words"] if ckey(w["t"])): cnt[w] = cnt.get(w, 0) + 1
        stable = [w for w, c in cnt.items() if c >= max(2, 0.4 * n)]
        if not stable: continue
        # reading order of stable words from the frame that contains most of them
        best = max(e["frames"], key=lambda fc: sum(1 for r in fc[1] for w in r["words"] if ckey(w["t"]) in stable))
        order = [w["t"] for r in sorted(best[1], key=lambda r: r["y0"]) for w in r["words"] if ckey(w["t"]) in stable]
        boxes = []
        for t, caps in e["frames"]:
            ws = [w for r in caps for w in r["words"] if ckey(w["t"]) in stable]
            boxes.append((t, (min(w["x"] for w in ws), min(w["y"] for w in ws), max(w["x"] + w["w"] for w in ws), max(w["y"] + w["h"] for w in ws)) if ws else None))
        first = next((t for t, caps in e["frames"] if any(ckey(w["t"]) == ckey(order[0]) for r in caps for w in r["words"])), e["t0"]) if order else e["t0"]
        out.append(dict(t0=e["t0"], t1=e["t1"], text=" ".join(order), key=" ".join(ckey(w) for w in order), boxes=boxes, n=n, first_word_t=first))
    return out

def fuzzy_eq(a, b):
    if a == b: return True
    if len(a) >= 5 and len(b) >= 5: return difflib.SequenceMatcher(None, a, b).ratio() >= 0.8
    return False

def check_captions(evs, agreed, small, medium, manifest, size):
    C = TH["captions"]; W, H = size
    proper = {norm_word(p): p for pn in manifest.get("proper_nouns", []) for p in [pn] for _ in [0]}
    proper_words = set(w for p in manifest.get("proper_nouns", []) for w in words_of(p))
    one_model = [dict(t0=w[0], w=ckey(w[2])) for w in small + medium]
    agreed_k = [dict(a, w=ckey(a["raw"])) for a in agreed]
    mism, unconf, check_ear, late, safe, nevs = [], [], [], [], [], 0
    for e in evs:
        nevs += 1
        cw = e["key"].split()
        win = [a for a in agreed_k if e["t0"] - 1.2 <= a["t0"] <= e["t1"] + 1.0]
        for w in cw:
            if len(w) < 2 and w not in ("a", "i"): continue
            if any(fuzzy_eq(w, a["w"]) for a in win): continue
            if any(w == a["w"] + b_["w"] for a, b_ in zip(win, win[1:])): continue   # OCR merged two words ("not a" -> "nota")
            if any(fuzzy_eq(w, ckey(p)) for p in proper_words): check_ear.append(f"{e['t0']:.1f} s '{w}' (proper noun; ASR models disagree or miss it)"); continue
            if any(fuzzy_eq(w, o["w"]) for o in one_model if e["t0"] - 1.2 <= o["t0"] <= e["t1"] + 1.0):
                unconf.append(f"{e['t0']:.1f} s caption '{e['text']}': '{w}' heard by only one ASR model"); continue
            mism.append(f"{e['t0']:.1f} s caption '{e['text']}': '{w}' not in the final audio's transcript")
        # timing: onset of first caption word vs the agreed word
        if cw:
            cands = [a for a in agreed_k if a["w"] == cw[0] and abs(a["t0"] - e["first_word_t"]) < 1.5]
            if cands:
                a = min(cands, key=lambda a: abs(a["t0"] - e["first_word_t"])); d = e["first_word_t"] - a["t0"]
                if d > C["max_late_s"]: late.append(f"{e['t0']:.2f} s '{e['text']}' appears {d:.2f} s after the word")
                if -d > C["max_early_s"]: late.append(f"{e['t0']:.2f} s '{e['text']}' appears {-d:.2f} s before the word")
        bad = [b for _, b in e["boxes"] if b and (b[1] < C["safe_top_frac"] * H or b[3] > (1 - C["safe_bottom_frac"]) * H
                                                    or b[2] > (1 - C["safe_right_frac"]) * W or b[0] < C["edge_margin_px"])]
        if len(bad) >= 2: safe.append(f"{e['t0']:.1f} s '{e['text']}' box {bad[0]} outside the safe area")
    res = []
    res.append(result("captions match the final audio (OCR of frames vs transcript; both ASR models must agree)",
                      "FAIL" if (mism or unconf) else ("WARN" if check_ear else "PASS"),
                      f"{nevs} caption events read; {len(mism)} words not heard, {len(unconf)} heard by one model only, {len(check_ear)} proper nouns to check by ear",
                      (mism + unconf + [f"WARN check by ear: {c}" for c in check_ear]) or None, "caption text differs from speech"))
    res.append(result(f"caption timing (onset within {C['max_late_s']} s of the word; WARN only: OCR of animated captions is +-0.2 s)", "WARN" if late else "PASS",
                      f"{len(late)} late/early caption events", late or None, "late captions"))
    res.append(result("caption safe area (top 8%, bottom 20%, right 12% clear)", "FAIL" if safe else "PASS",
                      f"{len(safe)} events outside", safe or None, "captions in platform UI"))
    return res

def check_caption_clearance(evs, ocr):
    C = TH["captions"]; fails = []
    for e in evs:
        hits = 0; example = None
        for t, box in e["boxes"]:
            if not box or t not in ocr: continue
            x0, y0, x1, y1 = box; m = C["clearance_px"]
            for r in rows_of(ocr[t]["whole"], 60):
                if len(re.sub(r"[^A-Za-z0-9]", "", r["text"])) < 4: continue
                if r["x1"] < x0 - m or r["x0"] > x1 + m or r["y1"] < y0 - m or r["y0"] > y1 + m: continue
                # same text as the caption itself? skip
                if difflib.SequenceMatcher(None, " ".join(words_of(r["text"])), e["key"]).ratio() > 0.5: continue
                if any(fuzzy_eq(w, cw) for w in words_of(r["text"]) for cw in e["key"].split()): continue
                inside = not (r["y1"] < y0 or r["y0"] > y1)
                hits += 1; example = example or f"'{r['text'][:40]}' {'under' if inside else 'within ' + str(m) + ' px of'} the caption"
        if hits >= 3:
            fails.append(f"{e['t0']:.1f}-{e['t1']:.1f} s caption '{e['text'][:40]}': {example}")
    return result(f"caption clearance from other on-screen text (>= {TH['captions']['clearance_px']} px)", "FAIL" if fails else "PASS",
                  f"{len(fails)} caption events crowd other text", fails or None, "captions over screen text")

# ----------------------------------------------------------------- 7 evidence beats, labels, runs
def coverage(expected, text):
    a = re.sub(r"\s+", " ", expected.lower()).strip(); b = re.sub(r"\s+", " ", text.lower()).strip()
    if not a or not b: return 0.0
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return sum(m.size for m in sm.get_matching_blocks()) / len(a)

def best_row(expected, words, W, exclude=()):
    """Best OCR row (or two stacked rows, for text that wraps on a card or title) covering the expected text."""
    best = (0.0, None)
    def under_caption(r):
        return any(not (r["x1"] < b[0] or r["x0"] > b[2] or r["y1"] < b[1] or r["y0"] > b[3]) for b in exclude if b)
    rows = [r for r in rows_of(words, 30) if not under_caption(r)]
    cands = list(rows)
    for a in rows:
        for b in rows:
            h = max(a["y1"] - a["y0"], b["y1"] - b["y0"])
            if b is a or not (0 <= b["y0"] - a["y1"] < 1.2 * h) or b["x1"] < a["x0"] or b["x0"] > a["x1"]: continue
            cands.append(dict(text=a["text"] + " " + b["text"], x0=min(a["x0"], b["x0"]), x1=max(a["x1"], b["x1"]),
                              y0=a["y0"], y1=b["y1"], words=a["words"] + b["words"], conf=(a["conf"] + b["conf"]) / 2))
    for r in cands:
        c = coverage(expected, r["text"])
        if c > best[0] or (c == best[0] and best[1] is not None and len(r["text"]) < len(best[1]["text"])): best = (c, r)
    return best

def glyph_px(row):
    hs = [w["h"] for w in row["words"] if re.search(r"[A-Z0-9bdfhklt]", w["t"]) and not re.search(r"[gjpqy,;]", w["t"])]
    if hs: return float(np.median(hs))
    return 0.75 * float(np.median([w["h"] for w in row["words"]]))

def matched_box(expected, row):
    """Box of the words in the row that belong to the expected text (so extra words do not move it)."""
    exp = set(re.sub(r"[^a-z0-9]", "", w.lower()) for w in expected.split())
    ws = [w for w in row["words"] if re.sub(r"[^a-z0-9]", "", w["t"].lower()) in exp] or row["words"]
    return min(w["x"] for w in ws), min(w["y"] for w in ws)

def check_evidence(beats, ocr, size, cap_events=()):
    E = TH["evidence"]; W, H = size; out_rows, fails = [], []
    ts = sorted(ocr)
    for b in beats:
        fr = [t for t in ts if b["t0"] <= t <= b["t1"]]
        if not fr: fails.append(f"{b['id']}: window {b['t0']}-{b['t1']} s has no frames"); continue
        step = (fr[1] - fr[0]) if len(fr) > 1 else 0.1
        best_cov, best_txt, px = 0.0, "", []
        run, best_run, anchor, reasons = 0, 0, None, set()
        capbox = {}
        for e in cap_events:
            for t_, bx in e["boxes"]: capbox.setdefault(t_, []).append(bx)
        for t in fr:
            cov, row = best_row(b["text"], ocr[t]["whole"], W, capbox.get(t, ()))
            if cov > best_cov: best_cov, best_txt = cov, row["text"] if row else ""
            ok = False
            if row is not None and cov >= E["min_text_coverage"]:
                inframe = row["x0"] >= E["edge_margin_px"] and row["x1"] <= W - E["edge_margin_px"]
                rail = row["x1"] > (1 - E["safe_right_frac"]) * W
                safe = row["y0"] >= E["safe_top_frac"] * H and row["y1"] <= (1 - E["safe_bottom_frac"]) * H
                g = glyph_px(row); px.append(g)
                if not inframe: reasons.add("line touches the frame edge")
                if not safe: reasons.add(f"line outside the safe area (y {row['y0']}-{row['y1']})")
                if rail and inframe: reasons.add(f"line enters the right 12% (platform rail), ink to x={row['x1']}")
                if g < E["min_glyph_px_at_1080"]: reasons.add(f"glyph height {g:.0f} px < {E['min_glyph_px_at_1080']}")
                ok = inframe and safe and not rail and g >= E["min_glyph_px_at_1080"]
                mb = matched_box(b["text"], row)
                if ok and anchor is not None and (abs(mb[0] - anchor[0]) > E["max_drift_px"] or abs(mb[1] - anchor[1]) > E["max_drift_px"]):
                    best_run = max(best_run, run); run = 0; reasons.add("line moves while read"); anchor = None
            elif row is not None and cov >= 0.5:
                reasons.add(f"line incomplete in frame (best read '{row['text'][:60]}')")
            if ok:
                if anchor is None: anchor = matched_box(b["text"], row)
                run += 1
            else:
                best_run = max(best_run, run); run = 0; anchor = None
        best_run = max(best_run, run); hold = best_run * step
        status = "ok" if hold >= E["min_hold_s"] else "FAIL"
        if best_cov < 0.5: reasons.add("expected text not found on screen")
        rowd = dict(id=b["id"], text=b["text"], window=[b["t0"], b["t1"]], readable_still_hold_s=round(hold, 2),
                    best_coverage=round(best_cov, 2), best_read=best_txt[:80], glyph_px=round(float(np.median(px)), 1) if px else None,
                    run_id=b.get("run_id"), status=status, reasons=sorted(reasons) if status == "FAIL" else [])
        out_rows.append(rowd)
        if status == "FAIL":
            fails.append(f"{b['id']} [{b['t0']}-{b['t1']} s] '{b['text'][:50]}': still+readable {hold:.1f} s (needs {E['min_hold_s']}); "
                         + "; ".join(sorted(reasons))[:300])
    return result(f"evidence lines (whole line in frame, still, >= {E['min_glyph_px_at_1080']} px, >= {E['min_hold_s']} s)",
                  "FAIL" if fails else "PASS", f"{len(beats)} beats, {len(fails)} failing", fails or None,
                  "cropped / moving / unreadable evidence"), out_rows

def check_runs(beats, ocr):
    fails, checked = [], 0
    ts = sorted(ocr)
    def label_seen(b):
        fr = [t for t in ts if b["t0"] <= t <= b["t1"]]
        hits = sum(1 for t in fr if max((coverage(b["source_label"], r["text"]) for r in rows_of(ocr[t]["whole"], 30)), default=0) >= 0.85)
        return fr and hits / len(fr) >= 0.5
    for b in beats:
        if b.get("source_label"):
            checked += 1
            if not label_seen(b): fails.append(f"{b['id']}: declared source label '{b['source_label']}' not readable on screen in {b['t0']}-{b['t1']} s")
    by_claim = {}
    for b in beats: by_claim.setdefault(b.get("claim"), []).append(b)
    for claim, bs in by_claim.items():
        if not claim: continue
        bs = sorted(bs, key=lambda b: b["t0"])
        for a, b in zip(bs, bs[1:]):
            checked += 1
            if a.get("run_id") != b.get("run_id") and not (b.get("source_label") and label_seen(b)) and not (a.get("source_label") and label_seen(a)):
                fails.append(f"claim '{claim}': beat {a['id']} (run {a.get('run_id')}) next to beat {b['id']} (run {b.get('run_id')}) with no readable source label")
    return result("run ids and source labels (one claim = one run, or a visible label)", "FAIL" if fails else "PASS",
                  f"{checked} checks", fails or None, "mixed runs presented as one")

PII = [("email", re.compile(r"[A-Za-z0-9._%+\-\u2022*\u00b7]+\s?@\s?[A-Za-z0-9-]+\.(com|net|org|io|dev|co|ai|app)\b", re.I)),
       ("token", re.compile(r"\b(sk-[A-Za-z0-9]{12,}|ghp_[A-Za-z0-9]{12,}|github_pat_\w{10,}|xox[abpr]-[\w-]{10,}|AKIA[0-9A-Z]{12,}|eyJ[\w-]{10,}\.[\w-]{10,})")),
       ("secret assignment", re.compile(r"(api[_-]?key|secret|access[_-]?token|bearer)\s*[:=]\s*\S{8,}", re.I)),
       ("PLAN_REQUIRED", re.compile(r"plan[_ ]?required", re.I)),
       ("RATE_LIMITED", re.compile(r"rate[_ ]?limit(ed)?", re.I))]

def redact(kind, text):
    """Reports must not carry the personal data they found: keep only the kind and the shape."""
    if kind in ("PLAN_REQUIRED", "RATE_LIMITED"): return text[:40]
    return f"[{kind} redacted, {len(text)} chars]"

def check_pii(ocr):
    hits = {}
    for t in sorted(ocr):
        rows = rows_of(ocr[t]["whole"], 30)
        text = "\n".join(r["text"] for r in rows)
        for name, rx in PII:
            for m in rx.finditer(text):
                hits.setdefault((name, redact(name, m.group(0))), []).append(t)
        if re.search(r"\bcode\b", text, re.I):
            for m in re.finditer(r"(?<![\d#])\d{6}(?!\d)", text):
                hits.setdefault(("sign-in code", "[6 digits redacted]"), []).append(t)
    det = [f"{n} '{s}' at {min(ts):.1f}-{max(ts):.1f} s ({len(ts)} frames)" for (n, s), ts in hits.items() if len(ts) >= 2]
    return result("PII and plan-wall sweep (OCR of every sampled frame)", "FAIL" if det else "PASS",
                  f"{len(det)} findings", det or None, "personal data / plan walls on screen")

def check_script(agreed, disagree, manifest):
    """Diff what both models heard against the intended script. Every difference must be owner-accepted."""
    expected = " ".join(words_of(manifest["script_text"]))
    for d in manifest.get("accepted_deviations", []):          # owner accepted: expect the spoken form
        sc, sp_ = " ".join(words_of(d.get("script", ""))), " ".join(words_of(d["spoken"]))
        if sc and f" {sc} " in f" {expected} ": expected = f" {expected} ".replace(f" {sc} ", f" {sp_} ", 1).strip()
    script = expected.split(); heard = [a["w"] for a in agreed]
    acc = [(" ".join(words_of(d.get("script", ""))), " ".join(words_of(d["spoken"]))) for d in manifest.get("accepted_deviations", [])]
    proper = set(w for p in manifest.get("proper_nouns", []) for w in words_of(p))
    devs, ear = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, script, heard, autojunk=False).get_opcodes():
        if tag == "equal": continue
        s = " ".join(script[i1:i2]); h = " ".join(heard[j1:j2])
        t = agreed[j1]["t0"] if j1 < len(agreed) else (agreed[-1]["t1"] if agreed else 0)
        if any({s, h} <= {a_s, a_h} or (s and h and s in (a_s, a_h) and h in (a_s, a_h)) for a_s, a_h in acc): continue
        t = agreed[j1 - 1]["t1"] if j1 > 0 else t
        t1_ = agreed[j2]["t0"] if j2 < len(agreed) else t + 2
        heard_by = [f"small.en '{d['small']}' / medium.en '{d['medium']}'" for d in disagree if t - 0.6 <= d["t"] <= t1_ + 0.3]
        if s and set(script[i1:i2]) <= proper and not h:
            ear.append(f"~{t:.1f} s '{s}' (proper noun not confirmed by both models)"); continue
        if s and not h and heard_by:
            devs.append(f"~{t:.1f} s script '{s}' not confirmed: the models disagree ({'; '.join(heard_by)})"); continue
        devs.append(f"~{t:.1f} s script '{s or '-'}' / heard by both models '{h or '-'}'" + (f" (models also disagree nearby: {'; '.join(heard_by)})" if heard_by else ""))
    unconf = [f"{d['t']:.1f} s small.en '{d['small']}' vs medium.en '{d['medium']}'" for d in disagree if d["small"] or d["medium"]]
    st = "FAIL" if devs else ("WARN" if ear else "PASS")
    return result("spoken words vs script (differences must be on the owner-accepted list)", st,
                  f"{len(devs)} unaccepted differences; {len(unconf)} spots where the two ASR models disagree",
                  (devs + [f"WARN check by ear: {e}" for e in ear] + [f"INFO models disagree: {u}" for u in unconf[:25]]) or None,
                  "unaccepted script deviations / misheard words")

# ----------------------------------------------------------------- report
def write_md(rep, path):
    L = [f"# VDI gate: {rep['id']} - {rep['verdict']}", "",
         f"File: `{rep['file']}`  ", f"Manifest: `{rep['manifest']}`  ", f"Run: {rep['ran_at']} ({rep['runtime_s']:.0f} s)  ",
         "Every check below measured the rendered file. PASS here is necessary, never sufficient: an independent review and the owner's own OK are still required.", "",
         "| Check | Result | Measured |", "|---|---|---|"]
    for c in rep["checks"]:
        L.append(f"| {c['check']} | **{c['status']}** | {c['measured']} |")
    L += ["", "## Findings", ""]
    for c in rep["checks"]:
        if c.get("detail") and c["status"] != "PASS" or (c.get("detail") and any(str(d).startswith("WARN") for d in c["detail"])):
            L.append(f"**{c['check']}**")
            for d in c["detail"][:14]: L.append(f"- {d}")
            if len(c["detail"]) > 14: L.append(f"- ... {len(c['detail']) - 14} more in the JSON")
            L.append("")
    if rep.get("evidence"):
        L += ["## Evidence beats", "", "| Beat | Expected text | Still+readable | Glyph px | Best read | Result |", "|---|---|---|---|---|---|"]
        for e in rep["evidence"]:
            L.append(f"| {e['id']} | {e['text'][:44]} | {e['readable_still_hold_s']} s | {e['glyph_px']} | {e['best_read'][:40].replace('|', '/')} | {e['status']} |")
        L.append("")
    L += ["## Not checked by this gate", ""] + [f"- {x}" for x in SPEC["cannot_check"]]
    open(path, "w").write("\n".join(L) + "\n")

def build_parser():
    ap = argparse.ArgumentParser(prog="vdi release", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video"); ap.add_argument("manifest_pos", nargs="?", metavar="MANIFEST", help=argparse.SUPPRESS)
    ap.add_argument("--manifest", help="gate manifest JSON (schema: vdi/release_data/manifest.schema.json)")
    ap.add_argument("--out", default="gate-results"); ap.add_argument("--cache", default=None)
    ap.add_argument("--skip-asr", action="store_true"); ap.add_argument("--skip-ocr", action="store_true")
    return ap


def preflight(a):
    from .preflight import require
    if not os.path.isfile(a.video): sys.exit(f"vdi release: video not found: {a.video}")
    if not a.manifest or not os.path.isfile(a.manifest): sys.exit("vdi release: --manifest <manifest.json> is required (see examples/v4/manifests/)")
    mods = ["numpy", "scipy", "cv2"] + ([] if a.skip_asr else ["faster_whisper"]) + ([] if a.skip_ocr else ["pytesseract"])
    require(binaries=("ffmpeg", "ffprobe") + (() if a.skip_ocr else ("tesseract",)), modules=mods, extra_hint="[release]")
    if not a.skip_asr:
        print("vdi release: runs two Whisper models (small.en + medium.en). First run downloads ~2 GB; on 2 CPU cores expect "
              "8-10 min for a 45 s short. Progress is logged below; results are cached per file.", file=sys.stderr, flush=True)


def main(argv=None):
    a = build_parser().parse_args(argv)
    a.manifest = a.manifest or a.manifest_pos
    preflight(a); t_start = time.time()
    man = json.load(open(a.manifest)); vid = man.get("id") or os.path.basename(a.video)
    cache = a.cache or os.path.join(os.path.expanduser("~/.cache/vdi-gate"), file_hash(a.video)); os.makedirs(cache, exist_ok=True)
    os.makedirs(a.out, exist_ok=True)
    log = lambda m: print(f"[{time.time() - t_start:6.1f}s] {m}", file=sys.stderr, flush=True)
    checks = []
    c, info = check_container(a.video); checks.append(c); dur, fps = info["dur"], info["fps"]; size = (info["w"], info["h"])
    checks.append(check_loudness(a.video)); log("container + loudness")
    frames = decode_small_frames(a.video); log(f"decoded {len(frames)} small frames")
    sc, cuts = check_shots(frames, fps); checks.append(sc); checks.append(check_blank(frames, fps)); log("shots + blank panels")
    final = decode_audio(a.video); e = env_db(final); sp = float(np.percentile(e, 90))
    sources = []
    for s in man.get("source_audio", []):
        if os.path.exists(s["path"]): sources.append(Source(s["path"], s.get("label", os.path.basename(s["path"]))))
        else: log(f"missing source audio {s['path']}")
    segs = align(final, sources, sp) if sources else []; joins = joins_from(segs)
    log(f"aligned to {len(sources)} sources: {len(segs)} segments, {len(joins)} joins")
    checks.append(check_faces(frames, fps, cuts["whole"] + cuts["upper half"] + cuts["lower half"] + [j["t"] for j in joins])); del frames
    small = medium = []; agreed, disagree = [], []
    if not a.skip_asr:
        small = transcribe(final, "small.en", cache); log("small.en"); medium = transcribe(final, "medium.en", cache); log("medium.en")
        agreed, disagree = agree_words(small, medium)
    if segs:
        wc, wrows = check_word_endings(final, sources, segs, medium or small, dur); checks.append(wc)
    else:
        wrows = []; checks.append(result("word endings against the source envelopes (full band and >= 3.5 kHz)", "FAIL", "no source audio aligned", ["could not locate the final's speech in any source file"]))
    checks.append(check_ending(final, dur))
    if medium: checks.append(check_sentence_gaps(final, medium))
    checks.append(check_join_levels(final, joins)); checks.append(check_dropouts(a.video)); log("audio checks")
    if not a.skip_asr: checks.append(check_script(agreed, disagree, man))
    ev_rows = []
    if not a.skip_ocr:
        band = man.get("caption_band_px")
        ocr = run_ocr(a.video, fps, dur, band, cache, TH["ocr"]["sample_fps"]); log(f"OCR {len(ocr)} frames")
        evs = caption_events(ocr, band, small + medium) if band else []
        if band and not a.skip_asr: checks += check_captions(evs, agreed, small, medium, man, size)
        if band: checks.append(check_caption_clearance(evs, ocr))
        beats = man.get("evidence_beats", [])
        ec, ev_rows = check_evidence(beats, ocr, size, evs); checks.append(ec)
        checks.append(check_runs(beats, ocr)); checks.append(check_pii(ocr)); log("OCR checks")
    verdict = "FAIL" if any(c["status"] == "FAIL" for c in checks) else "PASS"
    rep = dict(id=vid, file=a.video, manifest=a.manifest, gate_version=SPEC["version"], verdict=verdict,
               ran_at=time.strftime("%Y-%m-%d %H:%M:%S"), runtime_s=time.time() - t_start,
               counts=dict(fail=sum(c["status"] == "FAIL" for c in checks), warn=sum(c["status"] == "WARN" for c in checks), passed=sum(c["status"] == "PASS" for c in checks)),
               checks=checks, evidence=ev_rows, word_endings=wrows,
               segments=[dict(src=sources[s["src"]].label, t0=round(s["t0"], 2), t1=round(s["t1"], 2), offset=round(s["off"], 3)) for s in segs],
               joins=[dict(t=j["t"], kind=j["kind"]) for j in joins], cannot_check=SPEC["cannot_check"])
    base = os.path.join(a.out, f"{vid}.gate")
    json.dump(rep, open(base + ".json", "w"), indent=1, default=float); write_md(rep, base + ".md")
    print(f"{vid}: {verdict}  ({rep['counts']['fail']} FAIL, {rep['counts']['warn']} WARN, {rep['counts']['passed']} PASS)  -> {base}.md")
    return 1 if verdict == "FAIL" else 0

if __name__ == "__main__":
    try: sys.exit(main())
    except Exception as ex:
        import traceback; traceback.print_exc(); sys.exit(2)
