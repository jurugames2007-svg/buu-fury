#!/usr/bin/env python3
"""Cross-reference validation for initial game content data."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

def load(name):
    with (DATA / name).open(encoding="utf-8") as source:
        return json.load(source)

def ids(records):
    values = [entry["id"] for entry in records]
    assert len(values) == len(set(values)), f"duplicate IDs: {values}"
    return set(values)

characters = load("characters.json")["characters"]
forms = load("transformations.json")["forms"]
techniques = load("techniques.json")["techniques"]
items = load("items.json")["items"]
enemies = load("enemies.json")["enemies"]
bosses = load("bosses.json")["bosses"]
maps = load("maps.json")["maps"]
quests = load("quests.json")["quests"]
portal_data = load("bills_portals.json")

character_ids, form_ids = ids(characters), ids(forms)
item_ids, enemy_ids, boss_ids = ids(items), ids(enemies), ids(bosses)
map_ids, quest_ids = ids(maps), ids(quests)
assert "base" in form_ids
for character in characters:
    assert set(character["forms"]).issubset(form_ids), character["id"]
for technique in techniques:
    assert set(technique["owner_ids"]).issubset(character_ids), technique["id"]
    if "required_form" in technique:
        assert technique["required_form"] in form_ids, technique["id"]
for enemy in enemies:
    assert set(enemy["map_ids"]).issubset(map_ids), enemy["id"]
for quest in quests:
    assert quest["map_id"] in map_ids, quest["id"]
assert portal_data["npc"]["map_id"] in map_ids
for portal in portal_data["portals"]:
    assert portal["target_map"] in map_ids, portal["id"]
assert any(portal["id"] == "gt_dlc" for portal in portal_data["portals"])
assert any(portal["id"] == "af_dlc" for portal in portal_data["portals"])
print("PASS: content validation: %d characters, %d forms, %d maps, %d bosses." % (len(characters), len(forms), len(maps), len(bosses)))
