#!/usr/bin/env python3
"""Static gate for the Godot vertical-slice bootstrap.

This is deliberately not reported as an engine run. It checks project wiring
and source invariants until Godot is available for runtime tests.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required = {
    "project.godot": [
        'run/main_scene="res://scenes/other_world_prototype.tscn"',
        'SaveGame="*res://scripts/save_game.gd"',
        "size/viewport_width=240",
        "size/viewport_height=160",
    ],
    "scenes/other_world_prototype.tscn": [
        'path="res://scripts/other_world_prototype.gd"',
        'type="Node2D"',
    ],
    "scripts/save_game.gd": ["SAVE_VERSION := 1", "save_snapshot", "load_snapshot"],
    "scripts/other_world_prototype.gd": [
        "func _process", "func _handle_movement", "func _interact",
        "func _snapshot", "func _restore_snapshot", "func _draw",
    ],
}

for relative_path, tokens in required.items():
    content = (ROOT / relative_path).read_text(encoding="utf-8")
    for token in tokens:
        assert token in content, f"{relative_path}: missing {token!r}"

import json
manifest_path = ROOT / "assets" / "ASSET_MANIFEST.json"
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest.get("assets", []) == [], (
        "No assets may be approved until their source and redistribution rights are recorded."
    )
print("PASS: Godot bootstrap wiring is structurally present (static check only).")
