# Dragon Ball: Legacy Beyond — proyecto ejecutable

Nueva aventura 2D de acción/RPG para **Windows**, inspirada en el ritmo, exploración, progreso y lectura de combate de *Buu's Fury*, pero creada como aplicación independiente en **Godot 4**. No depende de una ROM, emulador ni de la memoria de Game Boy Advance.

## Estructura de campañas

El juego se organizará como una experiencia base y dos expansiones desbloqueables:

1. **Campaña base — Buu's Fury Reborn:** una recreación original de la campaña de Majin Buu con el ritmo de exploración, combate y progreso de *Buu's Fury*. Será jugable de principio a fin sin DLC.
2. **GT DLC — Black Star Dragon Balls → Baby:** continúa tras el final de la campaña base. Incluye Goku niño, Pan, Trunks, Giru, los planetas de la búsqueda y la saga Baby.
3. **AF DLC — Divine Aftermath:** contenido posterior con Zaiko, Karat, Evil Goku, Angel Z y las líneas del Vacío. Se desbloquea mediante el NPC de Bills.

La puerta de entrada diegética será **Bills**, un NPC en el Mundo Sagrado de los Kaioshin / Otro Mundo. Tras terminar la historia base, ofrece el portal de GT; al completar los hitos definidos de GT, ofrece el portal AF. El jugador podrá volver libremente a los capítulos ya desbloqueados.

## Principios

- Combate de acción en tiempo real: ataques físicos, ki, bloqueo, esquiva, cargas y transformaciones.
- Exploración con mapas conectados, NPCs, cofres, misiones, secretos y jefes.
- Personajes jugables: Goku niño, Pan, Trunks; más Gohan, Vegeta, Goten, Uub/Majuub y fusiones según la historia.
- Progresión ampliada: nivel máximo 600; estadísticas y equipo escalables, sin los límites de GBA.
- Guardado local, configuración de teclado/control y builds nativas para Windows.

## Estado actual

La etapa actual es **preproducción técnica y narrativa**. El siguiente entregable será un vertical slice jugable de la campaña base en el Otro Mundo, con Goku, Snake Way, NPCs, misión, combate y guardado. GT y AF se mostrarán como campañas bloqueadas hasta que la historia base esté terminada. El diseño de campaña y reglas de recursos están en [`GAME_DESIGN.md`](GAME_DESIGN.md) y [`ASSET_POLICY.md`](ASSET_POLICY.md).

## Ejecutar cuando exista el proyecto Godot

1. Instalar Godot 4.3 o superior.
2. Abrir `standalone_game/project.godot`.
3. Ejecutar la escena principal con F6/F5.

El archivo `project.godot` se añadirá junto al primer prototipo funcional; no se publicará un `.exe` sin prueba de arranque, controles, combate y guardado.
