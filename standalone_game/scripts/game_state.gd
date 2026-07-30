extends Node
## Persistent gameplay rules shared by the base campaign, Bills hub and DLCs.
## Values intentionally exceed GBA limits; saves use JSON-safe integers.

const SAVE_SCHEMA_VERSION := 1
const MAX_LEVEL := 600
const STAT_CAPS := {
	"hp": 99999,
	"ki": 99999,
	"strength": 9999,
	"defense": 9999,
	"speed_percent": 999,
}

var level := 1
var experience := 0
var unspent_points := 0
var stats := {
	"hp": 120,
	"ki": 80,
	"strength": 12,
	"defense": 10,
	"speed_percent": 100,
}
var story_flags: Dictionary = {}
var unlocked_forms: Dictionary = {"base": true}

func reset_new_game() -> void:
	level = 1
	experience = 0
	unspent_points = 0
	stats = {
		"hp": 120,
		"ki": 80,
		"strength": 12,
		"defense": 10,
		"speed_percent": 100,
	}
	story_flags.clear()
	unlocked_forms = {"base": true}

func xp_to_next_level(current_level: int) -> int:
	# Gentle early curve and long endgame curve; balance tables can replace this.
	return 100 + current_level * current_level * 25

func grant_experience(amount: int) -> int:
	if amount <= 0 or level >= MAX_LEVEL:
		return 0
	experience += amount
	var levels_gained := 0
	while level < MAX_LEVEL and experience >= xp_to_next_level(level):
		experience -= xp_to_next_level(level)
		level += 1
		unspent_points += 3
		levels_gained += 1
	if level >= MAX_LEVEL:
		experience = 0
	return levels_gained

func spend_stat_point(stat_id: String, amount: int = 1) -> bool:
	if amount <= 0 or not stats.has(stat_id) or not STAT_CAPS.has(stat_id):
		return false
	if unspent_points < amount:
		return false
	var current := int(stats[stat_id])
	var cap := int(STAT_CAPS[stat_id])
	if current >= cap:
		return false
	var applied := mini(amount, cap - current)
	stats[stat_id] = current + applied
	unspent_points -= applied
	return applied > 0

func set_story_flag(flag_id: String, enabled: bool = true) -> void:
	story_flags[flag_id] = enabled

func has_story_flag(flag_id: String) -> bool:
	return bool(story_flags.get(flag_id, false))

func bills_portals() -> Array[Dictionary]:
	return [
		{
			"id": "gt_dlc",
			"label": "GT DLC: Grand Tour",
			"unlocked": has_story_flag("z_kid_buu_defeated"),
			"requirement": "Defeat Kid Buu in the base campaign.",
		},
		{
			"id": "af_dlc",
			"label": "AF DLC: Divine Aftermath",
			"unlocked": has_story_flag("gt_baby_defeated"),
			"requirement": "Complete the GT Baby arc.",
		},
	]

func export_save_data() -> Dictionary:
	return {
		"schema_version": SAVE_SCHEMA_VERSION,
		"level": level,
		"experience": experience,
		"unspent_points": unspent_points,
		"stats": stats.duplicate(true),
		"story_flags": story_flags.duplicate(true),
		"unlocked_forms": unlocked_forms.duplicate(true),
	}

func import_save_data(data: Dictionary) -> bool:
	if int(data.get("schema_version", -1)) != SAVE_SCHEMA_VERSION:
		return false
	level = clampi(int(data.get("level", 1)), 1, MAX_LEVEL)
	experience = max(0, int(data.get("experience", 0)))
	unspent_points = max(0, int(data.get("unspent_points", 0)))
	var incoming_stats = data.get("stats", {})
	if typeof(incoming_stats) != TYPE_DICTIONARY:
		return false
	for stat_id in STAT_CAPS:
		stats[stat_id] = clampi(int(incoming_stats.get(stat_id, stats[stat_id])), 0, int(STAT_CAPS[stat_id]))
	story_flags = data.get("story_flags", {}).duplicate(true) if typeof(data.get("story_flags", {})) == TYPE_DICTIONARY else {}
	unlocked_forms = data.get("unlocked_forms", {"base": true}).duplicate(true) if typeof(data.get("unlocked_forms", {})) == TYPE_DICTIONARY else {"base": true}
	unlocked_forms["base"] = true
	return true
