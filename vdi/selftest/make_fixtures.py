"""Build synthetic fixtures: one known-good short and one known-bad short per gate check.

Each bad fixture changes exactly one thing from the good one, so a FAIL can only come from
the defect it was built to contain. Faces use scikit-image's public-domain astronaut photo.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ..check import _ebur128

W, H, FPS, SR = 1080, 1920, 30, 48000
SHOT_S = 3.0
N_SHOTS = 3
DUR = SHOT_S * N_SHOTS            # 9.0 s
SPEECH_START, SPEECH_END = 0.3, DUR - 0.7   # 0.7 s end hold
MONO = ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "/System/Library/Fonts/Menlo.ttc",
        "/Library/Fonts/Courier New.ttf", "C:/Windows/Fonts/consola.ttf"]
SANS_B = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
          "/Library/Fonts/Arial Bold.ttf", "C:/Windows/Fonts/arialbd.ttf"]

TERMINAL = [
    ["$ lineage verify", "checked 17 claims", "2 failed: source", "missing"],
    ["$ lineage fix", "re-ran sample-04", "source found: a", "ledger entry"],
    ["$ lineage verify", "checked 17 claims", "17 passed", "done in 41 s"],
]
CAPTIONS = ["It checks every claim.", "Then it fixes the miss.", "Seventeen for seventeen."]
BG = [(22, 22, 26), (112, 112, 120), (22, 22, 26)]


def _font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)  # Pillow >= 10.1 ships a scalable default font


def _face(tint=None) -> Image.Image:
    from skimage import data
    img = data.astronaut()[0:300, 100:400]
    im = Image.fromarray(img).resize((540, 540), Image.LANCZOS)
    if tint is not None:
        a = np.asarray(im).astype(np.float32) * np.array(tint, dtype=np.float32)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return im


def shot_image(k: int, *, term_font=44, term_x=90, extra_line=None, caption_y=1010, tint=None,
               lines=None, panel_full=False) -> Image.Image:
    im = Image.new("RGB", (W, H), BG[k])
    d = ImageDraw.Draw(im)
    d.rectangle([0 if panel_full else 60, 170, W if panel_full else 1020, 900], fill=(10, 12, 14))
    f = _font(MONO, term_font)
    y = 210
    for line in (lines or TERMINAL[k]) + ([extra_line] if extra_line else []):
        d.text((term_x, y), line, font=f, fill=(225, 230, 225))
        y += int(term_font * 1.6)
    cf = _font(SANS_B, 56)
    text = CAPTIONS[k]
    tw = d.textlength(text, font=cf)
    d.rectangle([(W - tw) / 2 - 24, caption_y - 14, (W + tw) / 2 + 24, caption_y + 80], fill=(0, 0, 0))
    d.text(((W - tw) / 2, caption_y), text, font=cf, fill=(255, 255, 255))
    im.paste(_face(tint), (270, 1170))
    return im


# ── audio ────────────────────────────────────────────────────────────────────
def speech_audio(seed=7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = int(DUR * SR)
    t = np.arange(n) / SR
    room = rng.normal(0, 1, n)
    room = np.convolve(room, np.ones(24) / 24, mode="same")
    room *= 10 ** (-58 / 20) / (np.sqrt(np.mean(room ** 2)) + 1e-12)
    voice = np.zeros(n)
    syl, gap, word_gap = 0.17, 0.06, 0.22
    cur = SPEECH_START
    k = 0
    while cur + syl <= SPEECH_END - 0.06:
        a, b = int(cur * SR), int((cur + syl) * SR)
        tt = t[a:b] - cur
        f0 = 135 + 12 * np.sin(2 * np.pi * 3 * tt)
        ph = 2 * np.pi * np.cumsum(f0) / SR
        sig = sum((0.6 / h) * np.sin(h * ph + h) for h in range(1, 12))
        env = np.sin(np.pi * np.clip(tt / syl, 0, 1)) ** 0.6
        voice[a:b] += sig * env
        k += 1
        cur += syl + (word_gap if k % 3 == 0 else gap)
    # final /s/: HF consonant ending exactly at SPEECH_END
    a, b = int((SPEECH_END - 0.09) * SR), int(SPEECH_END * SR)
    hiss = rng.normal(0, 1, b - a)
    hiss = hiss - np.convolve(hiss, np.ones(6) / 6, mode="same")
    voice[a:b] += 0.35 * hiss * np.hanning(b - a) ** 0.3
    return voice, room


def master(voice, room, target=-14.0, tmp: Path = None) -> np.ndarray:
    g = 1.0
    for _ in range(4):
        y = 0.55 * np.tanh(voice * g / 0.55) + room
        wav = tmp / "_m.wav"
        write_wav(wav, y)
        lufs, _ = _ebur128(str(wav))
        g *= 10 ** ((target - lufs) / 20)
    return 0.55 * np.tanh(voice * g / 0.55) + room


def write_wav(path: Path, y: np.ndarray, sr=SR):
    import wave
    pcm = (np.clip(y, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())


# ── encode ───────────────────────────────────────────────────────────────────
def encode(out: Path, frames: list[Image.Image], audio: np.ndarray, tmp: Path, size=(W, H), sr=SR, dur=DUR):
    wav = tmp / (out.stem + ".wav")
    write_wav(wav, audio[: int(dur * SR)], SR)
    w, h = size
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(FPS),
           "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-ar", str(sr), "-movflags", "+faststart",
           "-t", f"{dur}", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    cache: dict[int, bytes] = {}
    for im in frames[: int(round(dur * FPS))]:
        key = id(im)
        if key not in cache:
            cache[key] = np.asarray(im.resize(size) if size != (W, H) else im, dtype=np.uint8).tobytes()
        p.stdin.write(cache[key])
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError(f"ffmpeg failed for {out}")


_SLIDES: dict = {}


def _slide(a: Image.Image, b: Image.Image, n: int = 8) -> list[Image.Image]:
    """Animated slide transition a → b over n frames (the AX split-screen move). Must NOT read as cuts."""
    key = (id(a), id(b))
    if key not in _SLIDES:
        frames = []
        for k in range(1, n + 1):
            off = int(H * k / (n + 1))
            im = a.copy()
            im.paste(b.crop((0, 0, W, off)), (0, H - off))
            frames.append(im)
        _SLIDES[key] = frames
    return _SLIDES[key]


def timeline(shots: list[Image.Image]) -> list[Image.Image]:
    per = int(SHOT_S * FPS)
    tl = [shots[i // per] for i in range(per * N_SHOTS)]
    # shots 1→2 change by an animated slide ending on the 3.0 s boundary; 2→3 is a hard cut
    tl[per - 8: per] = _slide(shots[0], shots[1])
    return tl


SCRIPT = """SAY: It checks every claim.
SHOW: terminal, lineage verify, 2 failed

SAY: Then it fixes the miss.
SHOW: terminal, lineage fix, source found

SAY: Seventeen for seventeen.
SHOW: terminal, 17 passed
"""


def build(out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp = out_dir / "_tmp"
    tmp.mkdir(exist_ok=True)
    voice, room = speech_audio()
    good_audio = master(voice, room, tmp=tmp)
    shots = [shot_image(k) for k in range(N_SHOTS)]
    fx: dict[str, Path] = {}

    def make(name, frames=None, audio=None, **kw):
        p = out_dir / f"{name}.mp4"
        encode(p, frames or timeline(shots), good_audio if audio is None else audio, tmp, **kw)
        fx[name] = p

    make("good")
    make("bad_loud", audio=np.clip(good_audio * 10 ** (8 / 20), -1, 1))
    tl = timeline(shots)
    black = Image.new("RGB", (W, H), (0, 0, 0))
    tl_black = tl[:]
    for i in range(135, 138):
        tl_black[i] = black
    make("bad_black", frames=tl_black)
    flash = Image.new("RGB", (W, H), (235, 235, 240))
    tl_flash = tl[:]
    tl_flash[135:137] = [flash, flash]
    make("bad_flash", frames=tl_flash)
    make("bad_tail", dur=SPEECH_END + 0.1)
    z = good_audio.copy()
    z[int(4.5 * SR): int(4.512 * SR)] = 0.0
    make("bad_zero", audio=z)
    v2 = voice.copy()
    v2[int(3.0 * SR): int(6.0 * SR)] *= 10 ** (4.5 / 20)
    make("bad_join", audio=master(v2, room, tmp=tmp))
    # a zoomed wide terminal: panel fills the frame edge to edge and lines run off the right side
    make("bad_edge", frames=timeline([shots[0], shot_image(1, panel_full=True, term_x=120, lines=[
        "$ lineage fix --source sample-review", "changed evidenced sample-reviewer-04", "source named in the ledger entry"]), shots[2]]))
    make("bad_safe", frames=timeline([shots[0], shot_image(1, caption_y=1700), shots[2]]))
    make("bad_small", frames=timeline([shots[0], shot_image(1, term_font=20, lines=["re-ran sample-04 with source", "found ledger entry for claim", "verified against original page"]), shots[2]]))
    make("bad_pii", frames=timeline([shots[0], shot_image(1, extra_line="demo.user@example.com"), shots[2]]))
    make("bad_face", frames=timeline([shots[0], shot_image(1, tint=(0.86, 0.80, 0.72)), shots[2]]))
    small = [im for im in timeline(shots)]
    make("bad_format", frames=small, size=(720, 1280), sr=44100)

    (out_dir / "script.txt").write_text(SCRIPT, encoding="utf-8")
    (out_dir / "transcript_good.txt").write_text("It checks every claim. Then it fixes the miss. Seventeen for seventeen.", encoding="utf-8")
    (out_dir / "transcript_bad.txt").write_text("It checks every claim. Then it fixes a miss. Seventeen out of seventeen.", encoding="utf-8")
    (out_dir / "accepted.txt").write_text("fixes a miss => fixes the miss\nout of => for\n", encoding="utf-8")
    (out_dir / "script_board_truncated.txt").write_text(SCRIPT.replace("Then it fixes the miss.", "Then it fixes the…"), encoding="utf-8")
    for f in tmp.iterdir():
        f.unlink()
    tmp.rmdir()
    return fx



