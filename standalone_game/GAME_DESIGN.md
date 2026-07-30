# GDD — Dragon Ball: Legacy Beyond

## 1. Visión

Un ARPG 2D de vista isométrica/3-4 superior con ritmo legible, exploración densa y combate de respuesta rápida. La referencia de sensación es *Buu's Fury*; la implementación, mapas, misiones, interfaces y reglas serán independientes.

El juego no pretende copiar binarios, código, mapas ni formatos de los títulos de GBA. Conserva una filosofía de diseño: zonas compactas, objetivos claros, combate físico/ki, progresión por niveles y personajes con habilidades diferenciadas.

## 2. Campaña GT: Black Star Dragon Balls → Baby

| Acto | Zonas principales | Jefes / hitos | Sistemas que se desbloquean |
|---|---|---|---|
| Prólogo | Mirador, Capsule Corp, nave Grand Tour | Tutorial Goku/Uub; despegue | Movimiento, ataque, ki, diálogo, misión principal |
| I — Amega | Amega ciudad, desierto, palacio Don Kee | Don Kee, Legic | Trunks y Pan; habilidades de grupo; inventario |
| II — Mundos extraños | Masu, Jaga Bada, planeta gusano | Gigante, Zunama, Para Brothers | Radar de Giru, puzles ambientales, primera Black Star Ball |
| III — Luud | Santuario Luud, torre de Doll Taki | Muchi Muchi, Lord Luud | Estados, rescate, combate de varios objetivos |
| IV — M-2 | Ciudad mecánica, fábrica Sigma, laboratorio Mew | Sigma Force, General Rilldo, Dr. Mew | Mejoras de Giru, modificación de habilidades, equipo tecnológico |
| V — Regreso | Tierra, hospital Pital, Lookout, Plant Tuffle | Baby, Baby Vegeta, Super Baby Vegeta | Transformaciones SSJ/SSJ3/SSJ4, aliados y combate de equipo |

El final de esta campaña abre el contenido posterior: Super 17, Shadow Dragons y la línea AF.

## 3. Bucle jugable

1. Recibir misión, pista o señal de Giru.
2. Explorar zona, combatir, conversar y resolver un obstáculo.
3. Obtener objeto, esfera, habilidad, aliado o acceso a otra región.
4. Derrotar jefe con patrón identificable y condición táctica.
5. Regresar a nave/centro seguro para equipo, habilidades, guardado y escenas.

## 4. Combate

### Acciones base
- Ataque físico ligero y pesado.
- Combo contextual; lanzamiento y remate al aturdir.
- Ki blast, técnica equipada y técnica definitiva.
- Bloqueo, esquiva y contraataque.
- Vuelo limitado por zona y habilidad; no trivializa puzles ni jefes.
- Transformación con coste de energía y multiplicadores configurables.

### Roles iniciales
| Personaje | Rol | Técnica distintiva |
|---|---|---|
| Goku niño | Equilibrado / movilidad | Kamehameha, Instant Transmission, SSJ, SSJ3, SSJ4 |
| Pan | Rápida / control | Maiden's Rage, salto aéreo, rescate y daño a objetivos ligeros |
| Trunks | Técnico / energía | Burning Attack, espada, interrupciones, utilidades de nave |
| Giru | Soporte | Radar, análisis, hackeo, misil y detección de secretos |

### Jefes
Todo jefe debe tener: telegráficos claros, ventana de castigo, fase de presión, una mecánica que requiera lectura y recompensas concretas. No se elevará dificultad solo inflando vida.

## 5. Progresión

- Nivel máximo: **600**.
- Atributos: Fuerza, Ki, Defensa, Velocidad, Vitalidad, Control.
- Estadísticas internas sin límite de byte; los límites se definen por tablas de balance y no por restricciones heredadas de GBA.
- Habilidades desbloqueadas por historia, entrenamiento, exploración y retos.
- Equipo: guantes, traje, botas, accesorio y reliquia; efectos visibles y no solo bonos planos.
- Transformaciones: árbol separado de técnicas, con dominio por uso, retos y eventos narrativos.

## 6. Contenido opcional

- Cápsulas ocultas, recuerdos de Z, desafíos de King Kai y simulaciones Capsule Corp.
- Misiones de NPC: supervivientes de Amega, culto de Luud, robots liberados de M-2.
- Arenas con reglas, jefes remix y pruebas de transformación.
- Enciclopedia: personajes, planetas, técnicas, enemigos y líneas temporales GT/AF.
- Easter eggs solo cuando respeten la exploración; nunca como sustituto de misiones principales.

## 7. Arquitectura técnica objetivo

- **Motor:** Godot 4.3+ (GDScript inicialmente; C# solo si un subsistema lo justifica).
- **Resolución base:** 480×270, escalado entero a 1080p/1440p/4K.
- **Datos:** recursos `.tres` o JSON validados para personajes, enemigos, misiones, diálogos, objetos y mapas.
- **Mapas:** TileMap por capas (suelo, colisión, decoración, interacción, navegación).
- **Guardado:** JSON con versión, migraciones y múltiples ranuras locales.
- **Pruebas:** escenas de prueba para input, daño, IA, inventario, guardado y cambios de mapa; build Windows validada antes de distribuir.

## 8. Primer vertical slice verificable

**Amega: llegada → recuperación de nave → Legic**

Criterios de listo:
- Menú inicial, nueva partida y guardado/carga funcionan.
- Goku niño, Pan y Trunks se pueden alternar.
- Un mapa exterior, pueblo, palacio y combate contra Legic conectados sin pantallas negras.
- Un NPC con diálogo ramificado, cofre, misión, tienda y dos secretos.
- Combate con ataque, ki, bloqueo, daño, enemigo común y jefe por fases.
- Build Windows probado desde carpeta limpia.
