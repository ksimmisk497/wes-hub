#!/usr/bin/env python3
"""Run this after adding HTML files to vendor/games/"""
import json, re
from pathlib import Path
games = Path(__file__).parent / "games"
out = Path(__file__).parent / "games-manifest.json"
existing = {}
if out.is_file():
    try:
        existing = {
            entry.get("file"): entry
            for entry in json.loads(out.read_text(encoding="utf-8"))
            if isinstance(entry, dict) and entry.get("file")
        }
    except (json.JSONDecodeError, OSError):
        existing = {}
manifest = []
for p in sorted(games.iterdir()):
    if not p.is_file():
        continue
    name = p.name
    t = name
    if t.startswith("cl"):
        t = t[2:]
    t = re.sub(r"\.(html?|txt|docx)$", "", t, flags=re.I)
    t = re.sub(r"([a-z])([A-Z])", r"\1 \2", t)
    t = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", t)
    t = re.sub(r"[_-]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip() or name
    letter = t[0].upper() if t else "#"
    if not letter.isalpha():
        letter = "#"
    previous = existing.get(name, {})
    entry = {
        "file": name,
        "title": previous.get("title") or t,
        "letter": previous.get("letter") or letter,
    }
    logo = previous.get("logo")
    if logo and (out.parent.parent / logo).is_file():
        entry["logo"] = logo
        if previous.get("logoSource"):
            entry["logoSource"] = previous["logoSource"]
    manifest.append(entry)
manifest.sort(key=lambda x: (x["letter"], x["title"].lower()))
out.write_text(json.dumps(manifest, indent=2))
print("wrote", len(manifest), "games ->", out)
