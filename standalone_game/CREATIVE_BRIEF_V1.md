# Creative Brief v1 — The Complete Saga

> Estado: dirección creativa aprobada para el diseño. Este documento organiza el prompt creativo del proyecto; no declara contenido ya implementado.

## Identidad

**Título de trabajo:** *Dragon Ball: Legacy Beyond — The Complete Saga*  
**Formato:** ARPG 2D de acción, exploración y progresión, con lectura visual de 16-bit/GBA y ejecución nativa para Windows.

La meta es una obra fan original y extensa: una campaña inspirada en los arcos Z de *Legacy of Goku* y *Buu's Fury*, seguida por GT y AF como DLCs accesibles mediante Bills. La implementación no reutiliza ROMs, código ni recursos comerciales sin permiso.

## Dirección visual aprobada

- Lienzo lógico **240×160** y escalado entero; filtro scanline opcional, nunca obligatorio.
- Pixel art 16-bit, siluetas legibles, paletas saturadas y fondos de alto contraste.
- Sprites base de 32×32 px; jefes entre 48×48 y 96×96 px según fase.
- Tiles de 16×16 px, con mínimo 20 piezas útiles por bioma antes de declararlo jugable.
- Animaciones mínimas: idle 2, caminar 4, ataque 3–4, transformación 8 fotogramas.
- HUD con HP verde, Ki amarillo/naranja, retrato, estado de transformación y recursos especiales.
- Portraits propios de 64×64 con expresiones neutral, feliz, enfadado, sorprendido y herido.

## Progresión

| Límite | Valor objetivo |
|---|---:|
| Nivel | 600 |
| HP / Ki | 99.999 |
| Fuerza / Defensa | 9.999 |
| Velocidad | 999% |

Los valores se almacenarán como enteros de 32 bits y multiplicadores de punto flotante; nunca se limitarán a bytes o enteros de 16 bits. Los puntos de atributo se eligen al subir de nivel, con el espíritu de *Buu's Fury*.

## Transformaciones

| Línea | Hito principal |
|---|---|
| Base → SSJ1 → SSJ2 → SSJ3 | campaña Z/base |
| SSJ4 | GT: Baby y entrenamiento de cola/Blutz Waves |
| SSJ5 | AF: Ice / Karat |
| SSJ6 | AF: Zeta |
| SSJ7 fases 1–4 | AF: Void World / Irina / Kicknape |

Cada forma requiere: habilidad desbloqueable, coste de Ki, condiciones narrativas, multiplicadores, aura y animaciones diferenciadas. Las cifras de poder se balancearán para que los jefes sigan siendo tácticos; no se usarán multiplicadores como única dificultad.

## Orden de campañas y DLC

1. **Legacy / Z** — Saiyan, Namek, Androides/Cell y Majin Buu.
2. **GT DLC** — Baby, Super 17 y Shadow Dragons.
3. **AF DLC I** — Ice y Karat.
4. **AF DLC II** — Evil Goku y Zeta.
5. **AF DLC III: Void World** — Irina, Kicknape y SSJ7.
6. **Epílogo** — equilibrio, secretos y futuros desafíos.

Bills funciona como NPC hub de postgame en el Mundo Sagrado. Sus portales presentan requisito, estado, nivel sugerido y recompensa principal de cada DLC.

## Roster inicial planificado

- Base/Z: Goku, Gohan, Vegeta, Goten, Trunks, Piccolo, Videl, Gotenks, Vegito.
- GT: Goku niño, Pan, Trunks GT, Uub/Majuub, Vegeta GT, Gogeta SSJ4.
- AF: Goku/Vegeta/Gohan SSJ5, Irina; jefes de versus como Ice, Karat, Evil Goku, Zeta y Kicknape.

No todos deben estar disponibles al inicio: cada personaje necesita identidad de combate, árbol de técnicas, sprites, retratos, animaciones y pruebas antes de incorporarse.

## Sistemas prioritarios

1. Combate: combo, ki, carga, bloqueo, esquiva, teletransporte y técnicas equipables.
2. Transformaciones con auras, temporizador de Ki y riesgo/recompensa.
3. Misiones, NPCs, cofres, tiendas, equipo, secretos y bestiario.
4. Vuelo, teletransporte, Dragon Radar, portales y navegación mundial.
5. Fusión con IA como base; multijugador local solo después de validar el combate individual.
6. Cámara del Tiempo, gravedad, torneos, pesca, supervivencia y desafíos como contenido secundario.

## Producción de mapas

Las 40+ áreas propuestas se producirán por paquetes: bioma, tileset, colisión, NPCs, enemigos, misión, secretos, música y jefe. Un mapa no cuenta como terminado solo por tener una imagen de fondo.

Prioridad de producción:

1. Otro Mundo / Snake Way / primeras zonas de campaña Z.
2. Ciudad Satán y nave de Babidi.
3. Mundo Sagrado + Bills hub.
4. Amega y primer paquete GT.
5. Void World como paquete visual AF avanzado.

## Jefes de referencia

- GT: Baby (tres fases), Super 17 (absorción de Ki), siete Shadow Dragons y Omega.
- AF: Ice (cuatro fases), Karat, Evil Goku, Zeta y Kicknape (cinco fases).
- Secretos: Broly, Cell Max, Black Goku, Jiren y modos What If.

Todo jefe requiere un diseño de telegráficos, estados, ataques, arena, transición y recompensa antes de producir su sprite final.

## Regla de assets

Los recursos fanmade solo pasan al build con autor/fuente/licencia en `assets/ASSET_MANIFEST.json`. Assets de GBA, anime u otros juegos comerciales se usan como referencia privada de lectura visual y no se redistribuyen.
