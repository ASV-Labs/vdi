"""Platform data for the quick gate, and the lessons inbox writer.

The corpus itself (rules, topics, briefs, checklists) lives in the topic packs and is served by
vdi/corpus.py. This module only holds what `vdi check` needs to measure a file.
"""
from __future__ import annotations

import datetime as _dt
from functools import lru_cache

import yaml

from . import DATA
from .paths import lessons_inbox



def _load(name: str) -> dict:
    with open(DATA / name, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@lru_cache(maxsize=None)
def platforms() -> dict:
    return _load("platforms.yaml")


@lru_cache(maxsize=None)
def sources() -> dict[str, dict]:
    return {s["id"]: s for s in _load("sources.yaml")["sources"]}


def platform_spec(platform: str) -> dict:
    p = platforms()["platforms"]
    if platform not in p:
        raise ValueError(f"unknown platform {platform!r}; one of {list(p)}")
    return {"key": platform, **p[platform], "house_caption_zone": platforms()["house_caption_zone"],
            "house_master": platforms()["house_master"]}


def caption_zone(platform: str, ads: bool = False) -> dict:
    """Fractions to keep clear. Organic = house zone; ads = stricter of house and platform ad zone."""
    house = dict(platforms()["house_caption_zone"]["clear"])
    if not ads:
        return house
    ad = (platforms()["platforms"].get(platform) or {}).get("ad_safe_zone")
    if not ad:
        return house
    return {k: max(house[k], ad["clear"][k]) for k in house}


def log_lesson(what_happened: str, rule: str, check: str, source: str, author: str = "agent") -> str:
    """Append a lesson to 00_Lessons/LESSONS-INBOX.md for a curator to fold into VDI-LESSONS-* and the packs."""
    for name, val in (("what_happened", what_happened), ("rule", rule), ("check", check), ("source", source)):
        if not val or not val.strip():
            raise ValueError(f"{name} is required")
    stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    entry = (f"\n### {stamp} — {author}\n- **What happened:** {what_happened.strip()}\n"
             f"- **Rule:** {rule.strip()}\n- **Check:** {check.strip()}\n- **Source:** {source.strip()}\n")
    inbox = lessons_inbox()
    new = not inbox.exists()
    with open(inbox, "a", encoding="utf-8") as fh:
        if new:
            fh.write("# Lessons inbox\n\nNew defects logged by `vdi log-lesson` / `vdi_log_lesson`. Fold each into a VDI-LESSONS file and the packs, then delete it here.\n")
        fh.write(entry)
    return str(inbox)
