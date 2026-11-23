"""Fast tests (no models, no media): CLI wiring, release-gate packaging and pre-flight, path resolution.

The release gate's real end-to-end run needs Whisper models and footage, so CI mocks faster-whisper here;
the real E2E output is recorded in examples/v3/.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def run_vdi(*args, cwd="/tmp", env=None):
    e = dict(os.environ, **(env or {}))
    return subprocess.run([sys.executable, "-m", "vdi", *args], cwd=cwd, capture_output=True, text=True, env=e)


def test_release_spec_and_schema_load_from_package_data():
    from vdi import release
    from vdi.paths import RELEASE_DATA
    assert release.SPEC["version"] and release.SPEC["thresholds"]["evidence"]["min_hold_s"] == 1.6
    schema = json.loads((RELEASE_DATA / "manifest.schema.json").read_text())
    required = schema.get("required", [])
    assert "evidence_beats" in schema.get("properties", {})
    for m in (REPO / "examples" / "v4" / "manifests").glob("*.json"):
        data = json.loads(m.read_text())
        assert all(k in data for k in required), f"{m.name} misses {set(required) - set(data)}"


def test_release_parser_accepts_flag_and_positional_manifest():
    from vdi import release
    a = release.build_parser().parse_args(["v.mp4", "--manifest", "m.json"])
    assert a.manifest == "m.json"
    a = release.build_parser().parse_args(["v.mp4", "m.json"])
    assert a.manifest_pos == "m.json"


def test_release_refuses_without_manifest(tmp_path):
    video = tmp_path / "v.mp4"
    video.write_bytes(b"\0")
    r = run_vdi("release", str(video))
    assert r.returncode != 0 and "--manifest" in (r.stderr + r.stdout)


def test_release_preflight_names_missing_whisper(tmp_path, monkeypatch):
    from vdi import preflight, release
    video, man = tmp_path / "v.mp4", tmp_path / "m.json"
    video.write_bytes(b"\0")
    man.write_text("{}")
    real = preflight.importlib.util.find_spec
    monkeypatch.setattr(preflight.importlib.util, "find_spec", lambda m: None if m == "faster_whisper" else real(m))
    monkeypatch.setattr(preflight.shutil, "which", lambda b: "/usr/bin/" + b)
    a = release.build_parser().parse_args([str(video), "--manifest", str(man)])
    with pytest.raises(SystemExit) as e:
        release.preflight(a)
    assert e.value.code == 2


def test_release_preflight_passes_with_mocked_whisper(tmp_path, monkeypatch, capsys):
    from vdi import preflight, release
    video, man = tmp_path / "v.mp4", tmp_path / "m.json"
    video.write_bytes(b"\0")
    man.write_text("{}")
    monkeypatch.setattr(preflight.importlib.util, "find_spec", lambda m: object())
    monkeypatch.setattr(preflight.shutil, "which", lambda b: "/usr/bin/" + b)
    monkeypatch.setattr(preflight, "_has_eng", lambda: True, raising=False)
    a = release.build_parser().parse_args([str(video), "--manifest", str(man), "--skip-ocr"])
    release.preflight(a)  # must not exit
    assert "small.en + medium.en" in capsys.readouterr().err


def test_check_missing_file_is_exit_2():
    r = run_vdi("check", "/nonexistent/video.mp4")
    assert r.returncode == 2


def test_validate_from_any_cwd():
    r = run_vdi("validate")
    assert r.returncode == 0, r.stdout[-2000:]
    assert "grounded in an AX measurement" in r.stdout


def test_corpus_env_override_has_clear_error():
    r = run_vdi("validate", env={"VDI_CORPUS_DIR": "/nonexistent"})
    assert r.returncode != 0 and "VDI_CORPUS_DIR" in (r.stderr + r.stdout)


def test_write_tool_is_off_by_default():
    import importlib
    os.environ.pop("VDI_ENABLE_WRITE_TOOLS", None)
    srv = importlib.import_module("vdi.mcp_server")
    if srv.mcp is None:
        pytest.skip("mcp SDK not installed")
    import asyncio
    names = {t.name for t in asyncio.run(srv.mcp.list_tools())}
    assert "vdi_log_lesson" not in names and "vdi_quick_gate" in names and "vdi_search" in names
