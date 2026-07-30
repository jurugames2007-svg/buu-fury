extends Node2D
## First executable vertical slice: Other World / Snake Way.
## Uses primitive pixel shapes until approved fanmade art is available.

const WORLD := Rect2(8, 24, 224, 126)
const PLAYER_SPEED := 58.0
const PLAYER_MAX_HP := 100
const PLAYER_MAX_KI := 100.0
const ENEMY_MAX_HP := 40
const ENEMY_SPEED := 24.0
const MELEE_RANGE := 34.0
const ENEMY_RANGE := 16.0

var player := Vector2(52, 98)
var player_hp := PLAYER_MAX_HP
var player_ki := PLAYER_MAX_KI
var last_facing := Vector2.RIGHT
var player_invulnerability := 0.0
var enemy := Vector2(174, 92)
var enemy_hp := ENEMY_MAX_HP
var enemy_attack_cooldown := 0.0
var enemy_alive := true
var npc := Vector2(102, 58)
var projectiles: Array[Dictionary] = []
var attack_cooldown := 0.0
var ki_cooldown := 0.0
var save_cooldown := 0.0
var message := "Snake Way prototype: speak with King Kai."
var message_time := 0.0
var quest_started := false
var quest_complete := false
var font: Font

func _ready() -> void:
	font = ThemeDB.fallback_font
	queue_redraw()

func _process(delta: float) -> void:
	attack_cooldown = maxf(0.0, attack_cooldown - delta)
	ki_cooldown = maxf(0.0, ki_cooldown - delta)
	enemy_attack_cooldown = maxf(0.0, enemy_attack_cooldown - delta)
	player_invulnerability = maxf(0.0, player_invulnerability - delta)
	save_cooldown = maxf(0.0, save_cooldown - delta)
	message_time = maxf(0.0, message_time - delta)
	_handle_movement(delta)
	_handle_actions()
	_update_projectiles(delta)
	_update_enemy(delta)
	queue_redraw()

func _handle_movement(delta: float) -> void:
	var direction := Vector2.ZERO
	if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
		direction.y -= 1.0
	if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
		direction.y += 1.0
	if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		direction.x -= 1.0
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		direction.x += 1.0
	if direction.length_squared() > 0.0:
		last_facing = direction.normalized()
		player += last_facing * PLAYER_SPEED * delta
		_clamp_player_to_world()
	if Input.is_key_pressed(KEY_R):
		player_ki = minf(PLAYER_MAX_KI, player_ki + 24.0 * delta)

func _handle_actions() -> void:
	if Input.is_key_pressed(KEY_SPACE) and attack_cooldown <= 0.0:
		attack_cooldown = 0.28
		if enemy_alive and player.distance_to(enemy) <= MELEE_RANGE:
			_damage_enemy(10, "Goku strikes!")
		else:
			_show_message("Attack missed — get closer.", 0.7)
	if Input.is_key_pressed(KEY_F) and ki_cooldown <= 0.0:
		_fire_ki_blast()
	if Input.is_key_pressed(KEY_E):
		_interact()
	if Input.is_key_pressed(KEY_F5) and save_cooldown <= 0.0:
		save_cooldown = 0.8
		var result := SaveGame.save_snapshot(_snapshot())
		_show_message("Saved." if result == OK else "Save error: %d" % result, 1.5)
	if Input.is_key_pressed(KEY_F9) and save_cooldown <= 0.0:
		save_cooldown = 0.8
		_restore_snapshot(SaveGame.load_snapshot())

func _fire_ki_blast() -> void:
	if player_ki < 10.0:
		_show_message("Not enough Ki.", 0.8)
		return
	ki_cooldown = 0.35
	player_ki -= 10.0
	var direction := last_facing
	if enemy_alive and player.distance_to(enemy) > 1.0:
		direction = player.direction_to(enemy)
	projectiles.append({"position": player + direction * 8.0, "velocity": direction * 112.0, "life": 1.4})
	_show_message("Ki Blast!", 0.5)

func _update_projectiles(delta: float) -> void:
	for index in range(projectiles.size() - 1, -1, -1):
		var blast: Dictionary = projectiles[index]
		blast["position"] += blast["velocity"] * delta
		blast["life"] -= delta
		projectiles[index] = blast
		if enemy_alive and blast["position"].distance_to(enemy) <= 10.0:
			_damage_enemy(14, "Ki Blast hits!")
			projectiles.remove_at(index)
		elif blast["life"] <= 0.0 or not WORLD.grow(8.0).has_point(blast["position"]):
			projectiles.remove_at(index)

func _update_enemy(delta: float) -> void:
	if not enemy_alive:
		return
	var distance := enemy.distance_to(player)
	if distance > ENEMY_RANGE:
		enemy += enemy.direction_to(player) * ENEMY_SPEED * delta
		enemy.x = clampf(enemy.x, WORLD.position.x + 4.0, WORLD.end.x - 4.0)
		enemy.y = clampf(enemy.y, WORLD.position.y + 4.0, WORLD.end.y - 4.0)
	elif enemy_attack_cooldown <= 0.0:
		enemy_attack_cooldown = 1.1
		_damage_player(8)

func _damage_enemy(amount: int, text: String) -> void:
	if not enemy_alive:
		return
	enemy_hp = max(0, enemy_hp - amount)
	player_ki = minf(PLAYER_MAX_KI, player_ki + 2.0)
	_show_message("%s Enemy HP: %d" % [text, enemy_hp], 1.0)
	if enemy_hp <= 0:
		enemy_alive = false
		_show_message("Training enemy defeated. Return to King Kai.", 3.0)

func _damage_player(amount: int) -> void:
	if player_invulnerability > 0.0:
		return
	player_invulnerability = 0.5
	player_hp = max(0, player_hp - amount)
	_show_message("Goku takes %d damage!" % amount, 0.9)
	if player_hp <= 0:
		player_hp = PLAYER_MAX_HP
		player_ki = PLAYER_MAX_KI
		player = Vector2(52, 98)
		enemy = Vector2(174, 92)
		enemy_hp = ENEMY_MAX_HP
		enemy_alive = true
		_show_message("Goku recovered at Snake Way.", 2.0)

func _interact() -> void:
	if player.distance_to(npc) > 24.0:
		return
	if not quest_started:
		quest_started = true
		_show_message("King Kai: Defeat the training enemy, Goku!", 3.0)
	elif enemy_alive:
		_show_message("King Kai: The enemy is still waiting on Snake Way.", 2.5)
	elif not quest_complete:
		quest_complete = true
		GameState.set_story_flag("z_snake_way_training_complete")
		GameState.grant_experience(150)
		_show_message("King Kai: Good work! Quest complete — +150 EXP.", 3.0)
	else:
		_show_message("King Kai: Keep training. Bills will appear after Kid Buu.", 3.0)

func _clamp_player_to_world() -> void:
	player.x = clampf(player.x, WORLD.position.x + 4.0, WORLD.end.x - 4.0)
	player.y = clampf(player.y, WORLD.position.y + 4.0, WORLD.end.y - 4.0)

func _snapshot() -> Dictionary:
	return {
		"player_x": player.x,
		"player_y": player.y,
		"player_hp": player_hp,
		"player_ki": player_ki,
		"enemy_x": enemy.x,
		"enemy_y": enemy.y,
		"enemy_hp": enemy_hp,
		"enemy_alive": enemy_alive,
		"quest_started": quest_started,
		"quest_complete": quest_complete,
		"game_state": GameState.export_save_data(),
	}

func _restore_snapshot(snapshot: Dictionary) -> void:
	if snapshot.is_empty():
		_show_message("No compatible save found.", 1.5)
		return
	player = Vector2(float(snapshot.get("player_x", player.x)), float(snapshot.get("player_y", player.y)))
	player_hp = clampi(int(snapshot.get("player_hp", PLAYER_MAX_HP)), 1, PLAYER_MAX_HP)
	player_ki = clampf(float(snapshot.get("player_ki", PLAYER_MAX_KI)), 0.0, PLAYER_MAX_KI)
	enemy = Vector2(float(snapshot.get("enemy_x", enemy.x)), float(snapshot.get("enemy_y", enemy.y)))
	enemy_hp = clampi(int(snapshot.get("enemy_hp", ENEMY_MAX_HP)), 0, ENEMY_MAX_HP)
	enemy_alive = bool(snapshot.get("enemy_alive", true))
	quest_started = bool(snapshot.get("quest_started", false))
	quest_complete = bool(snapshot.get("quest_complete", false))
	var saved_state = snapshot.get("game_state", {})
	if typeof(saved_state) == TYPE_DICTIONARY:
		GameState.import_save_data(saved_state)
	_clamp_player_to_world()
	_show_message("Save loaded.", 1.5)

func _show_message(text: String, duration: float) -> void:
	message = text
	message_time = duration

func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO, Vector2(240, 160)), Color("16203d"))
	draw_rect(WORLD, Color("365f45"))
	draw_rect(Rect2(8, 82, 224, 20), Color("d9a54b"))
	draw_rect(Rect2(8, 102, 224, 2), Color("7d4c2c"))
	_draw_actor(npc, Color("4fa8e5"), Color("ffd39b"))
	var player_color := Color("ffffff") if player_invulnerability > 0.0 else Color("f08c35")
	_draw_actor(player, player_color, Color("1f1f1f"))
	if enemy_alive:
		draw_circle(enemy, 7.0, Color("b34a5b"))
		draw_rect(Rect2(enemy + Vector2(-9, -12), Vector2(18, 3)), Color("251c27"))
		draw_rect(Rect2(enemy + Vector2(-9, -12), Vector2(18.0 * float(enemy_hp) / ENEMY_MAX_HP, 3)), Color("e45353"))
	for blast in projectiles:
		draw_circle(blast["position"], 3.0, Color("f6e56b"))
	_draw_hud()

func _draw_actor(position: Vector2, body_color: Color, head_color: Color) -> void:
	draw_circle(position, 6.0, body_color)
	draw_circle(position + Vector2(0, -6), 3.0, head_color)

func _draw_hud() -> void:
	draw_rect(Rect2(4, 4, 232, 16), Color(0.02, 0.03, 0.08, 0.88))
	draw_string(font, Vector2(8, 11), "GOKU L%d" % GameState.level, HORIZONTAL_ALIGNMENT_LEFT, -1, 7, Color.WHITE)
	draw_rect(Rect2(42, 6, 59, 4), Color("3a2424"))
	draw_rect(Rect2(42, 6, 59.0 * float(player_hp) / PLAYER_MAX_HP, 4), Color("49ba65"))
	draw_rect(Rect2(42, 13, 59, 4), Color("3b3121"))
	draw_rect(Rect2(42, 13, 59.0 * player_ki / PLAYER_MAX_KI, 4), Color("f2c94c"))
	draw_string(font, Vector2(105, 11), "E Talk  SPACE Hit  F Ki", HORIZONTAL_ALIGNMENT_LEFT, -1, 6, Color("d5def3"))
	draw_string(font, Vector2(105, 18), "R Charge  F5 Save  F9 Load", HORIZONTAL_ALIGNMENT_LEFT, -1, 6, Color("9ca9c7"))
	if message_time > 0.0:
		draw_rect(Rect2(5, 132, 230, 22), Color(0.02, 0.03, 0.08, 0.92))
		draw_string(font, Vector2(9, 142), message, HORIZONTAL_ALIGNMENT_LEFT, 222, 7, Color.WHITE)
