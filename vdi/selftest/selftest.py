"""Prove the quick check: the good fixture passes every check; every bad fixture FAILS the
check it was built to break. Run: python3 -m vdi selftest   (exit 0 = quick gate proven)."""
from __future__ import annotations

import shutil
import sys
import tempfile
import time
from pathlib import Path

from .. import check as gate
from . import make_fixtures

EXPECT_FAIL = {
    "bad_format": ["G-FORMAT"],
    "bad_loud": ["G-LOUDNESS", "G-TRUEPEAK"],
    "bad_black": ["G-BLACK"],
    "bad_flash": ["G-SHOT-MIN"],
    "bad_tail": ["G-TAIL"],
    "bad_zero": ["G-DIGITAL-ZERO"],
    "bad_join": ["G-JOIN-LEVEL"],
    "bad_edge": ["G-TEXT-EDGE"],
    "bad_safe": ["G-TEXT-SAFE"],
    "bad_small": ["G-TEXT-SIZE"],
    "bad_pii": ["G-PII"],
    "bad_face": ["G-FACE-MATCH"],
}


def main(keep: bool = False) -> int:
    t0 = time.time()
    out = Path.cwd() / "vdi-selftest-fixtures" if keep else Path(tempfile.mkdtemp(prefix="vdi_fx_"))
    print(f"building fixtures in {out} …")
    fx = make_fixtures.build(out)
    print(f"  built {len(fx)} files in {time.time() - t0:.0f} s")
    failures = []

    def expect(label, cond, detail=""):
        print(f"  {'ok ' if cond else 'BAD'}  {label}" + (f" — {detail}" if detail and not cond else ""))
        if not cond:
            failures.append(label)

    print("good fixture — every check must PASS:")
    rep = gate.run(str(fx["good"]), transcript=str(out / "transcript_good.txt"), script=str(out / "script.txt"))
    for r in rep["checks"]:
        expect(f"good {r['id']} = {r['status']}", r["status"] == "PASS", f"measured={r['measured']} findings={r['findings'][:3]}")
    expect("good verdict PASS-AUTOMATED", rep["verdict"] == "PASS-AUTOMATED")

    print("known-bad fixtures — the targeted check must FAIL:")
    for name, ids in EXPECT_FAIL.items():
        r = gate.run(str(fx[name]), only=ids)
        for cid in ids:
            res = next((c for c in r["checks"] if c["id"] == cid), None)
            expect(f"{name} → {cid} FAIL", res is not None and res["status"] == "FAIL",
                   f"got {res and res['status']} measured={res and res['measured']}")
    r = gate.run(str(fx["good"]), only=["G-DURATION"], max_duration=5)
    expect("good with 5 s ceiling → G-DURATION FAIL", r["checks"][0]["status"] == "FAIL")
    r = gate.run(str(fx["good"]), only=["G-SCRIPT-DIFF"], transcript=str(out / "transcript_bad.txt"), script=str(out / "script.txt"))
    expect("ad-libbed transcript → G-SCRIPT-DIFF FAIL", r["checks"][0]["status"] == "FAIL")
    r = gate.run(str(fx["good"]), only=["G-SCRIPT-DIFF"], transcript=str(out / "transcript_bad.txt"),
                 script=str(out / "script.txt"), accepted=str(out / "accepted.txt"))
    expect("same ad-libs owner-accepted → G-SCRIPT-DIFF PASS", r["checks"][0]["status"] == "PASS", str(r["checks"][0]))
    r = gate.run(str(fx["good"]), only=["G-SCRIPT-DIFF"])
    expect("no transcript → G-SCRIPT-DIFF NOT_RUN (never PASS)", r["checks"][0]["status"] == "NOT_RUN")


    if not keep:
        shutil.rmtree(out, ignore_errors=True)
    print(f"\nselftest: {'PASS — gate proven on every claimed defect class' if not failures else f'{len(failures)} FAILURE(S)'}"
          f" ({time.time() - t0:.0f} s)")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main(keep="--keep" in sys.argv))
