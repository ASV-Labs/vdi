"""vdi check — the quick, manifest-free pre-check that measures the RENDERED FILE, never the edit plan.

It runs on any video with no manifest, so it is the fast first pass on drafts and on video types the
release gate has no manifest for. It does NOT replace the release gate (`vdi release`),
which needs a manifest and checks evidence beats, captions against two ASR models and word endings
against the source audio.

Exit codes: 0 = all automated checks passed (open items still listed), 1 = at least one check failed,
2 = the gate could not run. A pass is necessary, never sufficient.
"""
from __future__ import annotations

import difflib
import json
import os
import re
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import knowledge

# ── thresholds (from VDI-LESSONS-001 §4 measured table unless noted) ─────────
LUFS_TARGET, LUFS_TOL = -14.0, 0.5          # L1
TRUE_PEAK_MAX = -1.5                        # L1
MIN_SHOT_FRAMES = 12                        # L1
MAX_BLACK_FRAMES = 1                        # L1
TAIL_MIN, TAIL_MAX = 0.58, 0.85             # (0.6–0.8 s ± one 20 ms analysis frame)
ZERO_RUN_MS = 4.0                           # L1
JOIN_SPEECH_DB = 2.0                        # L1
JOIN_FLOOR_DB = 4.0                         # (room tone must not jump at a join)
EDGE_MARGIN_PX = 16                         # L1
MIN_CAP_PX = 28                             # L1
FACE_DE_MAX = 3.5                           # L1
FACE_DE_IMPLAUSIBLE = 20.0                  # worst real pickup measured on AX was 9.6
OCR_FPS = 2.0
OCR_CONF = 60          # layout checks (edge, zone, size)
OCR_CONF_PII = 30      # PII sweep: '@' and punctuation lower OCR confidence; a miss costs more than a false alarm


@dataclass
class Check:
    id: str
    title: str
    measures: str
    threshold: str
    needs: list = field(default_factory=list)
    proven_by: list = field(default_factory=list)


CHECKS = [
    Check("G-FORMAT", "Container, codecs and frame", "ffprobe: resolution vs platform, H.264, yuv420p, CFR, AAC 48 kHz, moov atom first",
          "exact platform resolution; H.264; yuv420p; AAC-LC 48 kHz; faststart", ["ffprobe"], ["bad_format"]),
    Check("G-DURATION", "Duration vs platform ceiling", "container duration", "≤ platform max_duration_s", ["ffprobe"], ["good --max-duration 10"]),
    Check("G-LOUDNESS", "Integrated loudness", "ITU-R BS.1770 integrated loudness via ffmpeg ebur128",
          f"{LUFS_TARGET} ±{LUFS_TOL} LUFS", ["ffmpeg"], ["bad_loud"]),
    Check("G-TRUEPEAK", "True peak", "ebur128 true peak on the encoded audio", f"≤ {TRUE_PEAK_MAX} dBTP", ["ffmpeg"], ["bad_loud"]),
    Check("G-BLACK", "Black frames / black panels", "full-frame and half-frame (split layout) near-black uniform frames",
          f"≤ {MAX_BLACK_FRAMES} consecutive frame", ["ffmpeg"], ["bad_black"]),
    Check("G-SHOT-MIN", "Shortest shot", "shot boundaries from frame differences", f"every shot ≥ {MIN_SHOT_FRAMES} frames", ["ffmpeg"], ["bad_flash", "bad_black"]),
    Check("G-TAIL", "End hold after last word", "last speech (full-band and ≥3.5 kHz envelope) → end of file",
          f"{TAIL_MIN:.2f}–{TAIL_MAX:.2f} s", ["ffmpeg"], ["bad_tail"]),
    Check("G-DIGITAL-ZERO", "Room tone continuity", "runs of exact-zero samples inside the programme", f"no run ≥ {ZERO_RUN_MS} ms", ["ffmpeg"], ["bad_zero"]),
    Check("G-JOIN-LEVEL", "Level across joins", "speech level and room-tone floor 1 s either side of each cut / supplied join",
          f"speech step < {JOIN_SPEECH_DB} dB; floor step < {JOIN_FLOOR_DB} dB", ["ffmpeg"], ["bad_join"]),
    Check("G-TEXT-EDGE", "Text cropped at frame edge", "OCR word boxes vs left/right edge, persistent ≥ 2 samples",
          f"≥ {EDGE_MARGIN_PX} px margin", ["ffmpeg", "tesseract"], ["bad_edge"]),
    Check("G-TEXT-SAFE", "Text in platform UI zone", "OCR word boxes vs keep-clear zone (house, or platform ad zone with --ads)",
          "no persistent text in zone", ["ffmpeg", "tesseract"], ["bad_safe"]),
    Check("G-TEXT-SIZE", "Readable text size", "tallest word box per OCR line, text held ≥ 1.5 s", f"≥ {MIN_CAP_PX} px on 1080 wide",
          ["ffmpeg", "tesseract"], ["bad_small"]),
    Check("G-PII", "Personal data and plan walls", "OCR sweep: emails (incl. masked), API-key patterns, codes, PLAN_REQUIRED, RATE_LIMITED",
          "zero hits", ["ffmpeg", "tesseract"], ["bad_pii"]),
    Check("G-FACE-MATCH", "Face colour across cuts", "mean CIELAB of detected face either side of each cut", f"ΔE76 < {FACE_DE_MAX}",
          ["ffmpeg", "scikit-image"], ["bad_face"]),
    Check("G-SCRIPT-DIFF", "Said vs scripted", "word diff of supplied transcript vs script; deviations must be owner-accepted",
          "0 unaccepted deviations", ["--transcript", "--script"], ["bad_script"]),
]
CHECK_IDS = [c.id for c in CHECKS]

OPEN_ITEMS = [
    ("RELEASE-GATE", "vdi release <final.mp4> --manifest <manifest.json> exits 0 on this exact file"),
    ("INDEPENDENT-REVIEW", "a person or agent that did not make the edit says READY"),
    ("OWNER", "the owner approves this exact file himself"),
    ("FACE-PROCESSING", "no plastic skin or halo — by eye on a phone (no gate measures it)"),
    ("EVIDENCE-HOLD", "every evidence line still and readable for >= 1.6 s (release gate measures declared beats)"),
    ("CAPTION-BAND", "captions never over evidence text; >= 48 px from lower thirds and end cards"),
    ("LISTEN", "a human listens at every flagged timestamp"),
]


# ── helpers ──────────────────────────────────────────────────────────────────
def _run(cmd: list[str], text=True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=text, check=False)


def probe(path: str) -> dict:
    r = _run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", path])
    if r.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {r.stderr.strip()}")
    return json.loads(r.stdout)


def _fps(stream: dict) -> float:
    num, den = stream.get("avg_frame_rate", "0/1").split("/")
    return float(num) / float(den) if float(den) else 0.0


def _moov_first(path: str) -> bool | None:
    try:
        with open(path, "rb") as fh:
            pos, size = 0, os.path.getsize(path)
            while pos < size:
                fh.seek(pos)
                hdr = fh.read(16)
                if len(hdr) < 8:
                    return None
                n = int.from_bytes(hdr[:4], "big")
                kind = hdr[4:8]
                if n == 1:
                    n = int.from_bytes(hdr[8:16], "big")
                if kind == b"moov":
                    return True
                if kind == b"mdat":
                    return False
                if n < 8:
                    return None
                pos += n
    except OSError:
        return None
    return None


def _audio(path: str, sr: int = 48000) -> np.ndarray:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                       capture_output=True, check=False)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode(errors="replace"))
    return np.frombuffer(r.stdout, dtype=np.float32)


def _gray_frames(path: str, w: int = 72, h: int = 128) -> np.ndarray:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-an", "-vf", f"scale={w}:{h}:flags=area,format=gray",
                        "-f", "rawvideo", "-"], capture_output=True, check=False)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode(errors="replace"))
    return np.frombuffer(r.stdout, dtype=np.uint8).reshape(-1, h, w)


def _frame_rgb(path: str, t: float) -> np.ndarray | None:
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(t, 0):.4f}", "-i", path, "-frames:v", "1",
                        "-vf", "scale=540:-2", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=False)
    if r.returncode != 0 or not r.stdout:
        return None
    arr = np.frombuffer(r.stdout, dtype=np.uint8)
    h = arr.size // (540 * 3)
    return arr[: h * 540 * 3].reshape(h, 540, 3)


def _res(cid, status, measured=None, threshold=None, findings=None, note=None):
    return {"id": cid, "status": status, "measured": measured, "threshold": threshold,
            "findings": findings or [], "note": note}


# ── audio analysis ───────────────────────────────────────────────────────────
def _ebur128(path: str) -> tuple[float | None, float | None]:
    r = _run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
    txt = r.stderr
    summary = txt[txt.rfind("Summary:"):] if "Summary:" in txt else txt
    i = re.search(r"I:\s+(-?[\d.]+|-inf)\s+LUFS", summary)
    tp = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf)\s+dBFS", summary)
    f = lambda m: (float(m.group(1)) if m and m.group(1) != "-inf" else None)
    return f(i), f(tp)


class _Speech:
    """20 ms frame analysis: RMS dB, ≥3.5 kHz band dB, speech mask."""
    HOP = 0.02

    def __init__(self, x: np.ndarray, sr: int = 48000):
        self.sr = sr
        n = int(self.HOP * sr)
        frames = x[: len(x) // n * n].reshape(-1, n)
        self.rms_db = 10 * np.log10(np.mean(frames.astype(np.float64) ** 2, axis=1) + 1e-12)
        spec = np.abs(np.fft.rfft(frames * np.hanning(n), axis=1)) ** 2
        freqs = np.fft.rfftfreq(n, 1 / sr)
        self.hf_db = 10 * np.log10(spec[:, freqs >= 3500].sum(axis=1) / n + 1e-12)
        self.floor = float(np.percentile(self.rms_db, 10))
        self.peak = float(np.percentile(self.rms_db, 95))
        thr = max(self.floor + 12, self.peak - 30)
        hf_floor = float(np.percentile(self.hf_db, 10))
        mask = self.rms_db > thr
        hf_mask = self.hf_db > max(hf_floor + 12, float(np.percentile(self.hf_db, 95)) - 30)
        self.mask = self._clean(mask)
        self.mask_any = self._clean(mask | hf_mask)
        self.speech_present = self.peak - self.floor > 15 and self.mask.sum() * self.HOP > 1.0

    @staticmethod
    def _clean(m: np.ndarray, min_run: int = 3) -> np.ndarray:
        m = m.copy()
        i = 0
        while i < len(m):
            if m[i]:
                j = i
                while j < len(m) and m[j]:
                    j += 1
                if j - i < min_run:
                    m[i:j] = False
                i = j
            else:
                i += 1
        return m

    def last_speech_end(self) -> float | None:
        idx = np.flatnonzero(self.mask_any)
        return None if idx.size == 0 else float((idx[-1] + 1) * self.HOP)

    def window(self, t0: float, t1: float):
        a, b = max(int(t0 / self.HOP), 0), min(int(t1 / self.HOP), len(self.rms_db))
        return self.rms_db[a:b], self.mask[a:b]


def _power_mean_db(db: np.ndarray) -> float:
    return float(10 * np.log10(np.mean(10 ** (db / 10))))


# ── video analysis ───────────────────────────────────────────────────────────
def _cuts(gray: np.ndarray) -> list[int]:
    """Frame indices where a new shot starts."""
    if len(gray) < 2:
        return []
    g = gray.astype(np.int16)
    diff = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))
    hist = np.stack([np.histogram(f, bins=32, range=(0, 256))[0] for f in gray]).astype(np.float64)
    hist /= hist.sum(axis=1, keepdims=True)
    hd = 0.5 * np.abs(np.diff(hist, axis=0)).sum(axis=1)
    med = np.median(diff) + 1e-6
    high = (diff > max(20.0, 6 * med)) | ((hd > 0.35) & (diff > 8))
    # A run of ≥ 3 consecutive high-change frames is motion (animated split, slide, scroll, zoom):
    # one boundary at its start. Runs of 1–2 are cuts — two adjacent spikes = a 1-frame flash.
    cuts, i = [], 0
    while i < len(high):
        if not high[i]:
            i += 1
            continue
        j = i
        while j < len(high) and high[j]:
            j += 1
        if j - i >= 3:
            cuts.append(i + 1)
        else:
            cuts.extend(k + 1 for k in range(i, j))
        i = j
    return cuts


def _black_runs(gray: np.ndarray) -> list[tuple[int, int, str]]:
    """(start, length, where) runs of near-black uniform full frames or half frames."""
    h = gray.shape[1]

    def dark(region):
        return (region.mean(axis=(1, 2)) < 20) & (region.reshape(len(region), -1).std(axis=1) < 6)

    out = []
    for where, region in (("full", gray), ("top half", gray[:, : h // 2]), ("bottom half", gray[:, h // 2:])):
        m = dark(region)
        if where != "full":
            m &= ~dark(gray)  # a half-panel black while the other half has picture
        i = 0
        while i < len(m):
            if m[i]:
                j = i
                while j < len(m) and m[j]:
                    j += 1
                out.append((i, j - i, where))
                i = j
            else:
                i += 1
    return out


# ── OCR ──────────────────────────────────────────────────────────────────────
PII_PATTERNS = [
    ("email", re.compile(r"[A-Za-z0-9._%+•*-]+@[A-Za-z0-9-]{2,}\.(?:\s?[A-Za-z]{2,})?")),  # OCR often splits "x@y." + "com"
    ("masked email", re.compile(r"\w?[•*·●]{2,}\w*@\w+")),
    ("gmail-like", re.compile(r"@(gmail|outlook|hotmail|yahoo|icloud|proton)\b", re.I)),
    ("api key", re.compile(r"\b(sk-[A-Za-z0-9_-]{12,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[bpa]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{20,})")),
    ("one-time code", re.compile(r"(code|otp|verification|2fa)\D{0,20}\b\d{4,8}\b", re.I)),
    ("plan wall", re.compile(r"PLAN[_ ]REQUIRED|RATE[_ ]LIMITED|upgrade to (pro|plus|premium)", re.I)),
]


def _ocr_frames(path: str, fps: float, workdir: str) -> list[dict]:
    import pytesseract
    # We parallelise across frames; an OpenMP-built tesseract (Debian/Ubuntu packages) would also spawn one
    # thread per core per process and grind to a halt. One thread per tesseract process.
    os.environ.setdefault("OMP_THREAD_LIMIT", "1")
    from PIL import Image, ImageOps

    pattern = os.path.join(workdir, "f_%05d.png")
    r = _run(["ffmpeg", "-v", "error", "-i", path, "-an", "-vf", f"fps={fps}", pattern])
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    files = sorted(Path(workdir).glob("f_*.png"))

    def ocr(i_f):
        i, f = i_f
        img = Image.open(f).convert("L")
        words = []
        for inv in (False, True):
            im = ImageOps.invert(img) if inv else img
            d = pytesseract.image_to_data(im, config="--psm 11", output_type=pytesseract.Output.DICT)
            for k in range(len(d["text"])):
                txt = d["text"][k].strip()
                try:
                    conf = float(d["conf"][k])
                except ValueError:
                    conf = -1
                if conf < OCR_CONF_PII or len(txt) < 2 or not re.search(r"[A-Za-z0-9]", txt):
                    continue
                box = (d["left"][k], d["top"][k], d["width"][k], d["height"][k])
                dup = next((w for w in words if _iou(box, w["box"]) > 0.5), None)
                if dup is not None:
                    if conf <= dup["conf"]:
                        continue
                    words.remove(dup)  # keep the higher-confidence read of the same word
                words.append({"text": txt, "box": box, "conf": conf,
                              "line": (inv, d["block_num"][k], d["par_num"][k], d["line_num"][k])})
        return {"i": i, "t": i / fps, "w": img.width, "h": img.height, "words": words}

    with ThreadPoolExecutor(max_workers=max(os.cpu_count() or 2, 2)) as ex:
        return list(ex.map(ocr, enumerate(files)))


def _iou(a, b) -> float:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    ix = max(0, min(ax + aw, bx + bw) - max(ax, bx))
    iy = max(0, min(ay + ah, by + bh) - max(ay, by))
    inter = ix * iy
    union = aw * ah + bw * bh - inter
    return inter / union if union else 0.0


def _persistent(hits: list[tuple[int, str, tuple]], min_samples: int) -> list[dict]:
    """hits: (sample index, key, info). Keep keys seen in ≥ min_samples consecutive samples."""
    by_key: dict[str, list] = {}
    for i, key, info in hits:
        by_key.setdefault(key, []).append((i, info))
    out = []
    for key, seq in by_key.items():
        idx = sorted(set(i for i, _ in seq))
        run, best, start, best_start = 1, 1, idx[0], idx[0]
        for a, b in zip(idx, idx[1:]):
            if b == a + 1:
                run += 1
            else:
                run, start = 1, b
            if run > best:
                best, best_start = run, start
        if best >= min_samples:
            info = next(inf for i, inf in seq if i == best_start)
            out.append({"key": key, "samples": best, "first_sample": best_start, **info})
    return out


# ── the gate ─────────────────────────────────────────────────────────────────
def run(path: str, platform: str = "youtube-shorts", ads: bool = False, transcript: str | None = None,
        script: str | None = None, accepted: str | None = None, joins: list[float] | None = None,
        only: list[str] | None = None, max_duration: float | None = None, ocr_fps: float = OCR_FPS) -> dict:
    if not Path(path).is_file():
        raise FileNotFoundError(path)
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise RuntimeError(f"{tool} not found on PATH")
    want = set(only or CHECK_IDS)
    spec = knowledge.platform_spec(platform)
    results: list[dict] = []
    info = probe(path)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    duration = float(info["format"].get("duration", 0))
    fps = _fps(v) if v else 0.0

    # G-FORMAT
    if "G-FORMAT" in want:
        f = []
        exp_w, exp_h = spec["resolution"]
        if not v:
            f.append({"t": None, "detail": "no video stream"})
        else:
            if (v["width"], v["height"]) != (exp_w, exp_h):
                f.append({"t": None, "detail": f"resolution {v['width']}×{v['height']}, platform expects {exp_w}×{exp_h}"})
            if v.get("codec_name") != "h264":
                f.append({"t": None, "detail": f"video codec {v.get('codec_name')}, expected h264"})
            if v.get("pix_fmt") not in ("yuv420p", "yuvj420p"):
                f.append({"t": None, "detail": f"pix_fmt {v.get('pix_fmt')}, expected yuv420p"})
            if v.get("r_frame_rate") != v.get("avg_frame_rate") and abs(_fps({"avg_frame_rate": v["r_frame_rate"]}) - fps) > 0.05:
                f.append({"t": None, "detail": f"variable frame rate (r={v.get('r_frame_rate')} avg={v.get('avg_frame_rate')})"})
        if not a:
            f.append({"t": None, "detail": "no audio stream"})
        else:
            if a.get("codec_name") != "aac":
                f.append({"t": None, "detail": f"audio codec {a.get('codec_name')}, expected aac"})
            if int(a.get("sample_rate", 0)) != 48000:
                f.append({"t": None, "detail": f"audio {a.get('sample_rate')} Hz, expected 48000"})
        if path.lower().endswith((".mp4", ".m4v", ".mov")) and _moov_first(path) is False:
            f.append({"t": None, "detail": "moov atom after mdat (not faststart) — re-mux with -movflags +faststart"})
        measured = {"width": v and v["width"], "height": v and v["height"], "vcodec": v and v.get("codec_name"),
                    "pix_fmt": v and v.get("pix_fmt"), "fps": round(fps, 3), "acodec": a and a.get("codec_name"),
                    "sample_rate": a and a.get("sample_rate"), "channels": a and a.get("channels")}
        results.append(_res("G-FORMAT", "FAIL" if f else "PASS", measured, f"{exp_w}×{exp_h} h264 yuv420p aac 48k faststart", f))

    # G-DURATION
    if "G-DURATION" in want:
        ceiling = max_duration if max_duration is not None else (spec.get("max_duration_s") or {}).get("value")
        if ceiling is None:
            results.append(_res("G-DURATION", "NOT_RUN", round(duration, 2), None, note=f"no published ceiling for {platform}"))
        else:
            results.append(_res("G-DURATION", "FAIL" if duration > ceiling else "PASS", round(duration, 2), f"≤ {ceiling} s",
                                [] if duration <= ceiling else [{"t": None, "detail": f"{duration:.1f} s > {ceiling} s"}]))

    # audio checks
    audio_ids = {"G-LOUDNESS", "G-TRUEPEAK", "G-TAIL", "G-DIGITAL-ZERO", "G-JOIN-LEVEL"} & want
    gray = None
    cuts: list[int] = []
    if {"G-BLACK", "G-SHOT-MIN", "G-JOIN-LEVEL", "G-FACE-MATCH"} & want and v:
        gray = _gray_frames(path)
        cuts = _cuts(gray)

    if audio_ids and not a:
        for cid in sorted(audio_ids):
            results.append(_res(cid, "FAIL", None, None, [{"t": None, "detail": "no audio stream"}]))
    elif audio_ids:
        if {"G-LOUDNESS", "G-TRUEPEAK"} & want:
            lufs, tp = _ebur128(path)
            if "G-LOUDNESS" in want:
                ok = lufs is not None and abs(lufs - LUFS_TARGET) <= LUFS_TOL
                results.append(_res("G-LOUDNESS", "PASS" if ok else "FAIL", lufs, f"{LUFS_TARGET} ±{LUFS_TOL} LUFS",
                                    [] if ok else [{"t": None, "detail": f"integrated {lufs} LUFS"}]))
            if "G-TRUEPEAK" in want:
                ok = tp is not None and tp <= TRUE_PEAK_MAX
                results.append(_res("G-TRUEPEAK", "PASS" if ok else "FAIL", tp, f"≤ {TRUE_PEAK_MAX} dBTP",
                                    [] if ok else [{"t": None, "detail": f"true peak {tp} dBTP"}]))
        x = _audio(path)
        sp = _Speech(x)
        if "G-DIGITAL-ZERO" in want:
            sr = 48000
            edge = int(0.02 * sr)
            z = np.abs(x) < 1e-7
            z[:edge] = False
            z[-edge:] = False
            f = []
            d = np.diff(np.concatenate([[0], z.view(np.int8), [0]]))
            starts, ends = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
            for s0, e0 in zip(starts, ends):
                ms = (e0 - s0) / sr * 1000
                if ms >= ZERO_RUN_MS:
                    f.append({"t": round(s0 / sr, 3), "detail": f"{ms:.1f} ms of digital zero"})
            results.append(_res("G-DIGITAL-ZERO", "FAIL" if f else "PASS", len(f), f"no run ≥ {ZERO_RUN_MS} ms", f[:20]))
        if "G-TAIL" in want:
            end = sp.last_speech_end()
            if not sp.speech_present or end is None:
                results.append(_res("G-TAIL", "NOT_RUN", None, None, note="no speech detected"))
            else:
                tail = round(duration - end, 3)
                ok = TAIL_MIN <= tail <= TAIL_MAX
                results.append(_res("G-TAIL", "PASS" if ok else "FAIL", tail, f"{TAIL_MIN}–{TAIL_MAX} s",
                                    [] if ok else [{"t": round(end, 2), "detail": f"last speech ends {tail:.2f} s before the end"}]))
        if "G-JOIN-LEVEL" in want:
            pts = sorted(set([round(c / fps, 3) for c in cuts] if fps else []) | set(joins or []))
            f, measured = [], []
            for t in pts:
                if t < 1.0 or t > duration - 1.0:
                    continue
                db0, m0 = sp.window(t - 1.0, t - 0.04)
                db1, m1 = sp.window(t + 0.04, t + 1.0)
                row = {"t": t}
                if m0.sum() * sp.HOP >= 0.3 and m1.sum() * sp.HOP >= 0.3:
                    step = _power_mean_db(db1[m1]) - _power_mean_db(db0[m0])
                    row["speech_step_db"] = round(step, 2)
                    if abs(step) >= JOIN_SPEECH_DB:
                        f.append({"t": t, "detail": f"speech level step {step:+.1f} dB across join"})
                fb0, fm0 = sp.window(t - 1.5, t - 0.04)
                fb1, fm1 = sp.window(t + 0.04, t + 1.5)
                if (~fm0).sum() * sp.HOP >= 0.15 and (~fm1).sum() * sp.HOP >= 0.15:
                    fstep = float(np.percentile(fb1[~fm1], 50) - np.percentile(fb0[~fm0], 50))
                    row["floor_step_db"] = round(fstep, 2)
                    if abs(fstep) >= JOIN_FLOOR_DB:
                        f.append({"t": t, "detail": f"room-tone floor step {fstep:+.1f} dB across join"})
                measured.append(row)
            status = "FAIL" if f else ("PASS" if measured else "NOT_RUN")
            results.append(_res("G-JOIN-LEVEL", status, measured, f"< {JOIN_SPEECH_DB} dB speech, < {JOIN_FLOOR_DB} dB floor", f,
                                note=None if measured else "no joins with speech on both sides"))

    # video structure
    if "G-BLACK" in want and gray is not None:
        f = []
        for s, n, where in _black_runs(gray):
            if s / fps > duration - 1.0:
                continue  # final fade
            if n > MAX_BLACK_FRAMES:
                f.append({"t": round(s / fps, 3), "detail": f"{n} frames black ({where})"})
        results.append(_res("G-BLACK", "FAIL" if f else "PASS", len(f), f"≤ {MAX_BLACK_FRAMES} frame", f))
    if "G-SHOT-MIN" in want and gray is not None:
        bounds = [0] + cuts + [len(gray)]
        shots = [(bounds[i], bounds[i + 1] - bounds[i]) for i in range(len(bounds) - 1)]
        f = [{"t": round(s / fps, 3), "detail": f"{n}-frame shot"} for s, n in shots if n < MIN_SHOT_FRAMES]
        results.append(_res("G-SHOT-MIN", "FAIL" if f else "PASS", {"shots": len(shots), "shortest_frames": min(n for _, n in shots)},
                            f"≥ {MIN_SHOT_FRAMES} frames", f))

    # face colour across cuts
    if "G-FACE-MATCH" in want and gray is not None:
        results.append(_face_match(path, cuts, fps, len(gray)))

    # OCR checks
    ocr_ids = {"G-TEXT-EDGE", "G-TEXT-SAFE", "G-TEXT-SIZE", "G-PII"} & want
    if ocr_ids and v:
        if not shutil.which("tesseract"):
            for cid in sorted(ocr_ids):
                results.append(_res(cid, "NOT_RUN", note="tesseract not installed"))
        else:
            with tempfile.TemporaryDirectory() as tmp:
                frames = _ocr_frames(path, ocr_fps, tmp)
            results.extend(_ocr_checks(frames, ocr_ids, platform, ads, ocr_fps))

    # said vs scripted
    if "G-SCRIPT-DIFF" in want:
        results.append(_script_diff(transcript, script, accepted))

    order = {c: i for i, c in enumerate(CHECK_IDS)}
    results.sort(key=lambda r: order.get(r["id"], 99))
    failed = [r["id"] for r in results if r["status"] == "FAIL"]
    not_run = [r["id"] for r in results if r["status"] == "NOT_RUN"]
    warned = [r["id"] for r in results if r["status"] == "WARN"]
    manual = [{"id": k, "rule": v} for k, v in OPEN_ITEMS]
    verdict = "FAIL" if failed else "PASS-AUTOMATED"
    return {"file": str(Path(path).resolve()), "platform": platform, "ads": ads, "duration_s": round(duration, 3),
            "fps": round(fps, 3), "verdict": verdict, "failed": failed, "not_run": not_run,
            "warn_check_by_eye": warned, "checks": results,
            "manual_still_required": manual,
            "meaning": ("do not post." if failed else
                        "Quick-gate checks passed. NOT cleared to post: the release gate, independent review and owner "
                        "sign-off below are still required."
                        + (f" WARN checks to verify by eye: {', '.join(warned)}." if warned else ""))}


def _face_match(path: str, cuts: list[int], fps: float, nframes: int) -> dict:
    try:
        from skimage import color, data
        from skimage.feature import Cascade
    except ImportError:
        return _res("G-FACE-MATCH", "NOT_RUN", note="scikit-image not installed")
    det = Cascade(data.lbp_frontal_face_cascade_filename())

    def face_lab(t):
        img = _frame_rgb(path, t)
        if img is None:
            return None
        g = (color.rgb2gray(img) * 255).astype(np.uint8)
        # presenter faces are ≥ 10% of frame width; wall photos and screen patterns are not
        faces = det.detect_multi_scale(img=g, scale_factor=1.2, step_ratio=1, min_size=(54, 54), max_size=(420, 420))
        best = None
        for fc in sorted(faces, key=lambda d: -d["width"] * d["height"]):
            r, c, h, w = fc["r"], fc["c"], fc["height"], fc["width"]
            crop = img[r + h // 4: r + 3 * h // 4, c + w // 4: c + 3 * w // 4]
            if crop.size == 0:
                continue
            lab = color.rgb2lab(crop / 255.0).reshape(-1, 3).mean(axis=0)
            # skin plausibility: rejects detector misfires on terminals, pages and backgrounds
            if 25 <= lab[0] <= 90 and 3 <= lab[1] <= 35 and 3 <= lab[2] <= 40:
                best = lab
                break
        return best

    def side(frames_idx):
        labs = [x for x in (face_lab((i + 0.5) / fps) for i in frames_idx) if x is not None]
        return np.median(np.stack(labs), axis=0) if labs else None

    bounds = [0] + cuts + [nframes]
    f, warn, measured = [], [], []
    for k, cut in enumerate(cuts):
        prev_start, next_end = bounds[k], bounds[k + 2]
        before = sorted({max(prev_start, cut - d) for d in (2, 5, 8)})
        after = sorted({min(next_end - 1, cut + d) for d in (1, 4, 7)})
        lb, la = side(before), side(after)
        if la is None or lb is None:
            continue
        de = float(np.linalg.norm(la - lb))
        t = round(cut / fps, 3)
        measured.append({"t": t, "deltaE76": round(de, 2)})
        if de > FACE_DE_IMPLAUSIBLE:
            warn.append({"t": t, "detail": f"ΔE76 {de:.0f} is implausible for one presenter — detector disagreement or a "
                                           f"different subject; check this cut by eye"})
        elif de >= FACE_DE_MAX:
            f.append({"t": t, "detail": f"face ΔE76 {de:.1f} across cut"})
    status = "FAIL" if f else ("WARN" if warn else ("PASS" if measured else "NOT_RUN"))
    if status == "PASS" and len(measured) < 0.5 * len(cuts):
        status = "WARN"  # never PASS on a minority of cuts
        warn.append({"t": None, "detail": f"only {len(measured)} of {len(cuts)} cuts measured — check the rest by eye"})
    cov = f"face measured at {len(measured)} of {len(cuts)} cuts (scikit-image LBP detector; unmeasured cuts need an eye check)"
    return _res("G-FACE-MATCH", status, measured, f"ΔE76 < {FACE_DE_MAX}", f + warn, note=cov)


def _ocr_checks(frames: list[dict], ids: set, platform: str, ads: bool, fps: float) -> list[dict]:
    out = []
    zone = knowledge.caption_zone(platform, ads)
    edge_hits, safe_hits, size_hits, pii = [], [], [], []
    for fr in frames:
        W, H = fr["w"], fr["h"]
        lines: dict = {}
        for w in fr["words"]:
            if w["conf"] < OCR_CONF:
                continue  # low-confidence words feed the PII sweep only
            x, y, bw, bh = w["box"]
            lines.setdefault(w["line"], []).append(w)
            if x < EDGE_MARGIN_PX or x + bw > W - EDGE_MARGIN_PX:
                side = "left" if x < EDGE_MARGIN_PX else "right"
                edge_hits.append((fr["i"], f"{side}:{y // 40}", {"t": fr["t"], "text": w["text"], "box": w["box"]}))
            cx, cy = x + bw / 2, y + bh / 2
            # zone check only on text-like words: OCR finds 1–2 letter "words" in faces and textures
            if len(re.sub(r"[^A-Za-z0-9]", "", w["text"])) < 3 or w["conf"] < 70:
                continue
            zones = []
            if y < zone["top"] * H: zones.append("top")
            if y + bh > (1 - zone["bottom"]) * H: zones.append("bottom")
            if x < zone["left"] * W: zones.append("left")
            if x + bw > (1 - zone["right"]) * W: zones.append("right")
            for zname in zones:
                safe_hits.append((fr["i"], f"{zname}:{int(cy // 60)}:{int(cx // 120)}", {"t": fr["t"], "text": w["text"], "zone": zname, "box": w["box"]}))
        for key, ws in lines.items():
            ws = [w for w in ws if len(re.sub(r"\W", "", w["text"])) >= 3]
            if len(ws) < 2:
                continue
            tallest = max(w["box"][3] for w in ws)
            if tallest < MIN_CAP_PX:
                y = min(w["box"][1] for w in ws)
                size_hits.append((fr["i"], f"{y // 30}", {"t": fr["t"], "text": " ".join(w["text"] for w in ws)[:80], "height_px": tallest}))
        text = " ".join(w["text"] for w in sorted(fr["words"], key=lambda w: (w["box"][1] // 20, w["box"][0])))
        for name, rx in PII_PATTERNS:
            for m in rx.finditer(text):
                pii.append({"t": fr["t"], "detail": f"{name}: {m.group(0)[:60]}"})
    if "G-TEXT-EDGE" in ids:
        p = _persistent(edge_hits, 2)
        f = [{"t": h["t"], "detail": f"text at {h['key'].split(':')[0]} edge: {h['text']!r} box={h['box']} ({h['samples']} samples)"} for h in p]
        out.append(_res("G-TEXT-EDGE", "FAIL" if f else "PASS", len(f), f"≥ {EDGE_MARGIN_PX} px", f[:20]))
    if "G-TEXT-SAFE" in ids:
        p = _persistent(safe_hits, 2)
        f = [{"t": h["t"], "detail": f"text in {h['zone']} UI zone: {h['text']!r} ({h['samples']} samples)"} for h in p]
        out.append(_res("G-TEXT-SAFE", "FAIL" if f else "PASS", len(f), {"zone_clear": zone, "ads": ads}, f[:20]))
    if "G-TEXT-SIZE" in ids:
        need = max(int(round(1.5 * fps)), 2)
        p = _persistent(size_hits, need)
        f = [{"t": h["t"], "detail": f"{h['height_px']} px text held {h['samples'] / fps:.1f} s: {h['text']!r}"} for h in p]
        out.append(_res("G-TEXT-SIZE", "FAIL" if f else "PASS", len(f), f"≥ {MIN_CAP_PX} px", f[:20]))
    if "G-PII" in ids:
        seen, f = set(), []
        for h in pii:
            if h["detail"] not in seen:
                seen.add(h["detail"])
                f.append(h)
        out.append(_res("G-PII", "FAIL" if f else "PASS", len(f), "0 hits", f[:20]))
    return out


def _words(text: str) -> list[str]:
    text = re.sub(r"^\s*(SAY|VO)\s*[:\-–]\s*", "", text, flags=re.I | re.M)
    text = "\n".join(l for l in text.splitlines() if not re.match(r"^\s*(SHOW|DO|ON ?SCREEN)\s*[:\-–]", l, re.I))
    return re.findall(r"[a-z0-9']+", text.lower().replace("’", "'"))


def _script_diff(transcript: str | None, script: str | None, accepted: str | None) -> dict:
    if not transcript or not script:
        return _res("G-SCRIPT-DIFF", "NOT_RUN", note="needs --transcript (from two agreeing ASR models) and --script")
    said_raw = Path(transcript).read_text(encoding="utf-8")
    if transcript.endswith(".json"):
        j = json.loads(said_raw)
        segs = j.get("segments", j) if isinstance(j, dict) else j
        said_raw = " ".join((s.get("text") or s.get("word") or "") for s in segs)
    said, scripted = _words(said_raw), _words(Path(script).read_text(encoding="utf-8"))
    pairs = []  # (said phrase, scripted phrase) the owner accepted
    if accepted and Path(accepted).is_file():
        for line in Path(accepted).read_text(encoding="utf-8").splitlines():
            line = line.split("#")[0].strip()
            if line:
                said_p, _, script_p = line.partition("=>")
                pairs.append((" ".join(_words(said_p)), " ".join(_words(script_p))))

    def within(part: str, whole: str) -> bool:
        return f" {part} " in f" {whole} " if part else True

    f, acc = [], []
    sm = difflib.SequenceMatcher(a=scripted, b=said, autojunk=False)
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == "equal":
            continue
        s_txt, w_txt = " ".join(scripted[a0:a1]), " ".join(said[b0:b1])
        item = {"t": None, "detail": f"{op}: scripted '{s_txt}' → said '{w_txt}'"}
        ok = any(within(w_txt, sp) and within(s_txt, cp) and (w_txt or s_txt) for sp, cp in pairs)
        (acc if ok else f).append(item)
    return _res("G-SCRIPT-DIFF", "FAIL" if f else "PASS", {"deviations": len(f) + len(acc), "accepted": len(acc)},
                "0 unaccepted deviations", f[:40], note=f"{len(acc)} owner-accepted deviation(s)" if acc else None)


def format_report(rep: dict) -> str:
    lines = [f"vdi check — {Path(rep['file']).name}", f"platform {rep['platform']}{' (ads zone)' if rep['ads'] else ''} · "
             f"{rep['duration_s']} s · {rep['fps']} fps", ""]
    for r in rep["checks"]:
        m = r["measured"]
        ms = json.dumps(m, ensure_ascii=False) if isinstance(m, (dict, list)) else m
        if isinstance(ms, str) and len(ms) > 90:
            ms = ms[:87] + "..."
        lines.append(f"  {r['status']:<8} {r['id']:<15} measured={ms}  threshold={r['threshold']}" + (f"  ({r['note']})" if r["note"] else ""))
        for fnd in r["findings"][:8]:
            t = f"{fnd['t']:>7.2f}s " if isinstance(fnd.get("t"), (int, float)) else "         "
            lines.append(f"           {t}{fnd['detail']}")
        if len(r["findings"]) > 8:
            lines.append(f"           … {len(r['findings']) - 8} more")
    lines += ["", f"VERDICT: {rep['verdict']} — {rep['meaning']}"]
    if rep["verdict"] != "FAIL":
        lines.append("Manual items still required:")
        lines += [f"  - {m['id']}: {m['rule']}" for m in rep["manual_still_required"]]
    return "\n".join(lines)
