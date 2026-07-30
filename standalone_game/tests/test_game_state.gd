extends SceneTree
## Headless deterministic tests for core progression and DLC gate rules.

var failures: Array[String] = []

func expect(condition: bool, label: String) -> void:
	if not condition:
		failures.append(label)

func _init() -> void:
	var state = preload("res://scripts/game_state.gd").new()
	expect(state.level == 1, "new game starts at level 1")
	expect(not state.bills_portals()[0]["unlocked"], "GT portal starts locked")
	expect(not state.bills_portals()[1]["unlocked"], "AF portal starts locked")

	state.set_story_flag("z_kid_buu_defeated")
	expect(state.bills_portals()[0]["unlocked"], "GT portal unlocks after Kid Buu")
	expect(not state.bills_portals()[1]["unlocked"], "AF remains locked before Baby")

	state.set_story_flag("gt_baby_defeated")
	expect(state.bills_portals()[1]["unlocked"], "AF portal unlocks after Baby")

	var gained := state.grant_experience(1000000)
	expect(gained > 0, "experience grants levels")
	expect(state.unspent_points == gained * 3, "three stat points per level")
	expect(state.spend_stat_point("strength"), "valid stat spend succeeds")
	expect(not state.spend_stat_point("unknown_stat"), "unknown stat spend fails")

	var save_data := state.export_save_data()
	var loaded = preload("res://scripts/game_state.gd").new()
	expect(loaded.import_save_data(save_data), "valid save imports")
	expect(loaded.level == state.level, "save preserves level")
	expect(loaded.has_story_flag("z_kid_buu_defeated"), "save preserves base completion")
	expect(loaded.has_story_flag("gt_baby_defeated"), "save preserves GT completion")
	expect(not loaded.import_save_data({"schema_version": 999}), "unknown save schema is rejected")

	if failures.is_empty():
		print("PASS: GameState tests passed (13 assertions).")
		quit(0)
	for failure in failures:
		push_error("FAIL: " + failure)
	quit(1)
