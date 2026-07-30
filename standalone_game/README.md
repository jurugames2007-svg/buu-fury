# Dragon Ball: Legacy Beyond — proyecto ejecutable

Nueva aventura 2D de acción/RPG para **Windows**, inspirada en el ritmo, exploración, progreso y lectura de combate de *Buu's Fury*, pero creada como aplicación independiente en **Godot 4**. No depende de una ROM, emulador ni de la memoria de Game Boy Advance.

## Objetivo de la primera campaña

**Dragon Ball GT — Black Star Dragon Balls → Baby**

La primera versión completa cubre el inicio en el Mirador, el viaje por Amega, Masu, Jaga Bada, Luud, M-2 y el regreso a la Tierra hasta el enfrentamiento contra Baby. Después se conectará con AF mediante capítulos opcionales y postgame.

## Principios

- Combate de acción en tiempo real: ataques físicos, ki, bloqueo, esquiva, cargas y transformaciones.
- Exploración con mapas conectados, NPCs, cofres, misiones, secretos y jefes.
- Personajes jugables: Goku niño, Pan, Trunks; más Gohan, Vegeta, Goten, Uub/Majuub y fusiones según la historia.
- Progresión ampliada: nivel máximo 600; estadísticas y equipo escalables, sin los límites de GBA.
- Guardado local, configuración de teclado/control y builds nativas para Windows.

## Estado actual

La etapa actual es **preproducción técnica y narrativa**. El siguiente entregable de desarrollo será un vertical slice jugable de Amega con Goku, Pan, Trunks, Giru, Don Kee y Legic. El diseño de campaña y reglas de recursos están en [`GAME_DESIGN.md`](GAME_DESIGN.md) y [`ASSET_POLICY.md`](ASSET_POLICY.md).

## Ejecutar cuando exista el proyecto Godot

1. Instalar Godot 4.3 o superior.
2. Abrir `standalone_game/project.godot`.
3. Ejecutar la escena principal con F6/F5.

El archivo `project.godot` se añadirá junto al primer prototipo funcional; no se publicará un `.exe` sin prueba de arranque, controles, combate y guardado.
