extends Node
## Local save adapter for the first playable slice.
## All saved fields are versioned so later builds can migrate them safely.

const SAVE_PATH := "user://legacy_beyond_save.json"
const SAVE_VERSION := 1

func save_snapshot(snapshot: Dictionary) -> Error:
	var payload := {
		"version": SAVE_VERSION,
		"saved_at_unix": Time.get_unix_time_from_system(),
		"snapshot": snapshot,
	}
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		return FileAccess.get_open_error()
	file.store_string(JSON.stringify(payload))
	file.close()
	return OK

func load_snapshot() -> Dictionary:
	if not FileAccess.file_exists(SAVE_PATH):
		return {}
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null:
		return {}
	var parsed := JSON.parse_string(file.get_as_text())
	file.close()
	if typeof(parsed) != TYPE_DICTIONARY:
		return {}
	if int(parsed.get("version", -1)) != SAVE_VERSION:
		return {}
	var snapshot = parsed.get("snapshot", {})
	return snapshot if typeof(snapshot) == TYPE_DICTIONARY else {}
