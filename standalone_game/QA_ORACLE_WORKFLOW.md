# Oracle Workflow — calidad verificable, no tests de relleno

## Principio

El objetivo de **3.000 pruebas** es una meta de cobertura para una versión candidata, no un contador que se pueda declarar aprobado antes de tener juego, motor, mapas y contenido ejecutable. Ninguna prueba `pending`, `skipped` o simulada cuenta como prueba superada.

El oráculo de calidad responde tres preguntas por cada cambio:

1. ¿El juego abre, se puede jugar y guardar sin regresiones?
2. ¿El contenido cumple sus reglas de datos, progresión y desbloqueo?
3. ¿La experiencia es coherente: controles, combate, mapas, misiones, DLC y rendimiento?

## Puertas de calidad

| Puerta | Bloquea | Evidencia requerida |
|---|---|---|
| G0 — Datos | commits con datos inválidos | validación de esquema, IDs únicos, referencias existentes |
| G1 — Unidad | lógica de combate/progresión | tests automatizados de cálculo y estados |
| G2 — Integración | build candidata | nueva partida, guardado/carga, mapas, NPCs, misiones y transición |
| G3 — Regresión | release | smoke test de cada campaña y DLC desbloqueado |
| G4 — Rendimiento | release Windows | FPS, memoria, carga de mapas y ausencia de errores críticos |
| G5 — Playtest | declaración de "terminado" | sesiones humanas documentadas y bugs críticos cerrados |

## Distribución de las 3.000 pruebas objetivo

| Dominio | Casos objetivo |
|---|---:|
| Arranque, input, cámara, accesibilidad y UI | 180 |
| Guardado, carga, migración y perfiles | 220 |
| Movimiento, colisión, vuelo, teletransporte y mapas | 360 |
| Combate, daño, estados, IA y jefes | 720 |
| Ki, técnicas, transformaciones y fusiones | 420 |
| Nivel, stats, equipo, objetos y economía | 300 |
| Misiones, diálogos, NPCs, cofres y secretos | 300 |
| Campaña base Z | 180 |
| GT DLC y Bills hub | 150 |
| AF DLC, Void World y contenido postgame | 120 |
| Rendimiento, build Windows y regresiones | 50 |
| **Total** | **3.000** |

## Ciclo operativo

1. Elegir una unidad pequeña y jugable: por ejemplo, movimiento en Snake Way.
2. Escribir el criterio de aceptación y pruebas automatizables antes de añadir contenido.
3. Implementar la unidad.
4. Ejecutar G0/G1 y el smoke test local.
5. Registrar evidencia, resultado y regresiones.
6. Solo después integrar la siguiente unidad.
7. En cada hito, generar build Windows limpia y pasar G2–G4.

## Definición de terminado

No se declara 100% hasta que se cumpla todo:

- La campaña definida está implementada y es completables desde nueva partida.
- Cada DLC tiene requisitos, portal Bills, contenido, cierre y retorno funcional.
- Los assets incluidos tienen permiso/licencia registrados.
- 3.000/3.000 pruebas están ejecutadas; 0 críticas abiertas; las excepciones están documentadas.
- Build Windows reproducible y probada desde carpeta limpia.
- Playtests humanos completados para campaña base, GT y AF.

## Estado actual

El proyecto está en G0 de preproducción. No hay una build Godot, por lo que el contador real de pruebas ejecutadas es **0/3.000**. El primer hito útil es crear y probar el vertical slice de Otro Mundo; después se activan los tests reales de G0–G2.
