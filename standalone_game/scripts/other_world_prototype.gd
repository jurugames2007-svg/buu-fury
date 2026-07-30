extends Node2D
## First executable vertical-slice skeleton: Other World / Snake Way.
## It intentionally uses primitive pixel shapes until approved fanmade art is ready.

const WORLD := Rect2(8, 24, 224, 126)
const PLAYER_SPEED := 58.0
const PLAYER_MAX_HP := 100
const PLAYER_MAX_KI := 100.0
const ENEMY_MAX_HP := 40

var player := Vector2(52, 98)
var player_hp := PLAYER_MAX_HP
var player_ki := PLAYER_MAX_KI
var enemy := Vector2(174, 92)
var enemy_hp := ENEMY_MAX_HP
var npc := Vector2(102, 58)
var attack_cooldown := 0.0
var save_cooldown := 0.0
var message := "Snake Way prototype: speak with King Kai."
var message_time := 0.0
var quest_started := false
var enemy_alive := true
var font: Font

func _ready() -> void:
	font = ThemeDB.fallback_font
	queue_redraw()

func _process(delta: float) -> void:
	attack_cooldown = maxf(0.0, attack_cooldown - delta)
	save_cooldown = maxf(0.0, save_cooldown - delta)
	message_time = maxf(0.0, message_time - delta)
	_handle_movement(delta)
	_handle_actions()
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
		player += direction.normalized() * PLAYER_SPEED * delta
		player.x = clampf(player.x, WORLD.position.x + 4.0, WORLD.end.x - 4.0)
		player.y = clampf(player.y, WORLD.position.y + 4.0, WORLD.end.y - 4.0)
	if Input.is_key_pressed(KEY_R):
		player_ki = minf(PLAYER_MAX_KI, player_ki + 24.0 * delta)

func _handle_actions() -> void:
	if Input.is_key_pressed(KEY_SPACE) and attack_cooldown <= 0.0:
		attack_cooldown = 0.28
		if enemy_alive and player.distance_to(enemy) <= 34.0:
			enemy_hp = max(0, enemy_hp - 10)
			player_ki = maxf(0.0, player_ki - 4.0)
			_show_message("Goku strikes! Enemy HP: %d" % enemy_hp, 1.0)
			if enemy_hp <= 0:
				enemy_alive = false
				_show_message("Training enemy defeated. Return to King Kai.", 3.0)
		else:
			_show_message("Attack missed — get closer.", 0.7)
	if Input.is_key_pressed(KEY_E):
		_interact()
	if Input.is_key_pressed(KEY_F5) and save_cooldown <= 0.0:
		save_cooldown = 0.8
		var result := SaveGame.save_snapshot(_snapshot())
		_show_message("Saved." if result == OK else "Save error: %d" % result, 1.5)
	if Input.is_key_pressed(KEY_F9) and save_cooldown <= 0.0:
		save_cooldown = 0.8
		_restore_snapshot(SaveGame.load_snapshot())

func _interact() -> void:
	if player.distance_to(npc) > 24.0:
		return
	if not quest_started:
		quest_started = true
		_show_message("King Kai: Defeat the training enemy, Goku!", 3.0)
	elif enemy_alive:
		_show_message("King Kai: The enemy is still waiting on Snake Way.", 2.5)
	else:
		_show_message("King Kai: Good work! Vertical-slice quest complete.", 3.0)

func _snapshot() -> Dictionary:
	return {
		"player_x": player.x,
		"player_y": player.y,
		"player_hp": player_hp,
		"player_ki": player_ki,
		"enemy_hp": enemy_hp,
		"enemy_alive": enemy_alive,
		"quest_started": quest_started,
	}

func _restore_snapshot(snapshot: Dictionary) -> void:
	if snapshot.is_empty():
		_show_message("No compatible save found.", 1.5)
		return
	player = Vector2(float(snapshot.get("player_x", player.x)), float(snapshot.get("player_y", player.y)))
	player_hp = int(snapshot.get("player_hp", PLAYER_MAX_HP))
	player_ki = float(snapshot.get("player_ki", PLAYER_MAX_KI))
	enemy_hp = int(snapshot.get("enemy_hp", ENEMY_MAX_HP))
	enemy_alive = bool(snapshot.get("enemy_alive", true))
	quest_started = bool(snapshot.get("quest_started", false))
	_show_message("Save loaded.", 1.5)

func _show_message(text: String, duration: float) -> void:
	message = text
	message_time = duration

func _draw() -> void:
	# Sky and Snake Way placeholder geometry.
	draw_rect(Rect2(Vector2.ZERO, Vector2(240, 160)), Color("16203d"))
	draw_rect(WORLD, Color("365f45"))
	draw_rect(Rect2(8, 82, 224, 20), Color("d9a54b"))
	draw_rect(Rect2(8, 102, 224, 2), Color("7d4c2c"))
	# King Kai NPC, player and enemy.
	draw_circle(npc, 7.0, Color("4fa8e5"))
	draw_circle(npc + Vector2(0, -7), 4.0, Color("ffd39b"))
	draw_circle(player, 6.0, Color("f08c35"))
	draw_rect(Rect2(player + Vector2(-3, -10), Vector2(6, 3)), Color("1f1f1f"))
	if enemy_alive:
		draw_circle(enemy, 7.0, Color("b34a5b"))
		draw_rect(Rect2(enemy + Vector2(-9, -12), Vector2(18, 3)), Color("251c27"))
		draw_rect(Rect2(enemy + Vector2(-9, -12), Vector2(18.0 * float(enemy_hp) / ENEMY_MAX_HP, 3)), Color("e45353"))
	_draw_hud()

func _draw_hud() -> void:
	draw_rect(Rect2(4, 4, 232, 16), Color(0.02, 0.03, 0.08, 0.88))
	draw_string(font, Vector2(8, 11), "GOKU", HORIZONTAL_ALIGNMENT_LEFT, -1, 7, Color.WHITE)
	draw_rect(Rect2(35, 6, 66, 4), Color("3a2424"))
	draw_rect(Rect2(35, 6, 66.0 * float(player_hp) / PLAYER_MAX_HP, 4), Color("49ba65"))
	draw_rect(Rect2(35, 13, 66, 4), Color("3b3121"))
	draw_rect(Rect2(35, 13, 66.0 * player_ki / PLAYER_MAX_KI, 4), Color("f2c94c"))
	draw_string(font, Vector2(108, 11), "E Talk  SPACE Attack  R Charge", HORIZONTAL_ALIGNMENT_LEFT, -1, 6, Color("d5def3"))
	draw_string(font, Vector2(108, 18), "F5 Save  F9 Load", HORIZONTAL_ALIGNMENT_LEFT, -1, 6, Color("9ca9c7"))
	if message_time > 0.0:
		draw_rect(Rect2(5, 132, 230, 22), Color(0.02, 0.03, 0.08, 0.92))
		draw_string(font, Vector2(9, 142), message, HORIZONTAL_ALIGNMENT_LEFT, 222, 7, Color.WHITE)
