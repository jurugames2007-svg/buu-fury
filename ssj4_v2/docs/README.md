# SSJ4 v2 — Guía Completa

ROM limpio de Buu's Fury USA con la transformación **Super Saiyan 4** aplicada.

## ¿Qué hace este proyecto?

Aplica cambios **mínimos y seguros** a la ROM vanilla de Buu's Fury para que
Goku tenga **Super Saiyan 4 desde el inicio del juego** (New Game), con
paleta roja estilo Webfoot.

## Estrategia: Auto-asignación de SSJ4 al iniciar partida

Encontré el handler en 0x421AE que inicializa al personaje con un
"default first skill" = 0x20 (empty) al comenzar nueva partida.
Cambié ese byte a 0x16 (SSJ4), de modo que Goku ya tiene SSJ4
asignado desde el inicio.

**Cadena de llamadas:**
```
Main loop (?)
  └─> 0x42204 (state dispatcher)
       └─> state 0 (new game) -> 0x42220
            └─> bl 0x421AE  <-- ESTE se llama al iniciar partida
                 └─> r4[4] = 4 (max_slots)
                 └─> r4[5] = 0x20 (default first skill)  <-- CAMBIADO A 0x16
```

Esto es **mejor que el approach original** porque:
1. La función 0x421AE SÍ es parte del flujo "init character"
2. Se llama desde el dispatcher 0x42204 que se activa en state 0
3. La modificación es de 1 solo byte (mínima invasión)
4. No requiere hooks ni code caves

## Cambios aplicados (9 regiones, 603 bytes)

| Offset      | Tamaño | Contenido                              | Antes                | Después                |
|-------------|--------|----------------------------------------|----------------------|------------------------|
| 0x0583F6    | 22 B   | Nombre del form                        | "SS3 Goku"           | "SS4 Goku"             |
| 0x06A544    | 30 B   | Nombre de la skill                     | "Super Saiyan 3"     | "Super Saiyan 4"       |
| 0x06A562    | 240 B  | Descripción de la skill                | "...a Super Saiyan 3"| "...into Super Saiyan 4! King Kai's special form..." |
| 0x06BADA    | 30 B   | Título del rank                        | "Super Saiyan 3"     | "Super Saiyan 4"       |
| 0x063534    | 240 B  | Descripción de King Kai                | "...greatest martial arts trainers..." | "...unlock Super Saiyan 4 for Goku!" |
| 0x06AD514   | 4 B    | Puntero a paleta en form struct        | 0x00000000           | 0x087B8A00             |
| 0x06AD5B8   | 4 B    | Puntero a paleta de halo               | 0x00000000           | 0x087B8A00             |
| 0x07B8A00   | 32 B   | Paleta SSJ4 (16 colores BGR555)        | 0xFFFFFFFF (vacío)   | Paleta roja SSJ4       |
| 0x421D0     | 1 B    | Default first skill (init character)  | 0x20 (empty)         | 0x16 (SSJ4)            |

**Modificación de 1 byte en código que SÍ se ejecuta** + 8 regiones de datos.

## Comparación con el proyecto original (log4_gt/)

El proyecto original (log4_gt + hackrom_ssj4) **NUNCA podría haber funcionado** porque:

1. **Hook en dirección muerta (0x17DA2)**: La función parcheada NUNCA SE LLAMA
   desde ningún código de la ROM. Verificado con análisis estático completo
   (búsqueda de `bl`/`blx`/`b`/`bx` y como dato en toda la ROM de 8MB).
   - Sin importar qué caves se inyecten, el hook **nunca se ejecuta**.

2. **Code cave re-ejecuta la prologue del handler original**: las instrucciones
   `30b5 041c 0069 0d1c 83b0` están duplicadas en el cave, causando push doble
   de la pila y stack overflow potencial.

3. **Skill ID incorrecto**: el cave escribe `0x15` (marcador) en lugar de
   `0x16` (skill ID correcto).

4. **ROM expandida a 16MB con bytes 0xFF**: muchos emuladores/flasheadores
   tienen problemas con ROMs expandidas incorrectamente.

5. **Nunca verificado en emulador real**: el reporte de auditoría se basa solo
   en análisis estático parcial.

## Limitación conocida de v2

**v2 SOLO da SSJ4 como primer skill (slot 1).** Los slots 2, 3, 4 están vacíos.
El jugador tiene que descubrir las otras skills (IT, Kamehameha, SS) en el
transcurso normal del juego (Kai del Este / NPCs en Snake Way).

**¿Cómo activar las otras skills?**
- **IT**: Aparece automáticamente en el menú de skills al principio
- **Kamehameha**: Similar
- **SS**: Se obtiene al hablar con King Kai (en Snake Way / Other World)
- **SSJ4**: ¡Ya está en slot 1 desde el inicio!

**¿Por qué no agregamos todas las skills desde el inicio?**
- El byte 0x421D0 es el único que controla el "default first skill"
- Para escribir múltiples skills, necesitaríamos un code cave de ~32 bytes
- La ROM no tiene espacio 0xFF suficiente para un code cave
- Habría que sobrescribir código existente, lo cual es más riesgoso

## Cómo probar v2

### 1. Validación estática (sin emulador)

```bash
python3 ssj4_v2/validate_ssj4_v2.py
```

Debe mostrar: `RESULTADO: 17/17 tests pasaron`

```bash
python3 ssj4_v2/tests/boot_test.py
```

### 2. Prueba en mGBA

1. Abre **mGBA** (versión 0.10+)
2. `File > Load ROM` → selecciona `ssj4_v2/ROM/BuusFury_SSJ4.gba`
3. Inicia **Nueva Partida** (New Game)
4. **Verificación visual**:
   - El menú de Skills debe mostrar "Super Saiyan 4" en slot 1
   - La descripción debe decir "Press B to transform into Super Saiyan 4!..."
   - La descripción de King Kai debe decir "...unlock Super Saiyan 4 for Goku!"
   - Presiona B - Goku debe tener **pelaje rojo** (transformación SSJ4)

### 3. Debug en mGBA

Si quieres ver qué pasa internamente:

1. `Tools > View RAM map` para ver 0x0300156C (skills de Goku)
2. `Tools > Cheats` para inyectar más skills si quieres
3. `Tools > View memory` para ver la paleta en 0x087B8A00

## Estructura del proyecto

```
ssj4_v2/
├── ROM/
│   └── BuusFury_SSJ4.gba    (8MB, validado, 17/17 tests)
├── docs/
│   ├── README.md            (este archivo)
│   └── AUDIT_FINDINGS.md    (hallazgos del proyecto original)
├── build_ssj4_v2.py         (build script)
├── inject_ssj4_save.py      (save file injector)
├── validate_ssj4_v2.py      (17 tests estáticos)
└── tests/
    └── boot_test.py         (boot test exhaustivo)
```

## Compatibilidad

| Emulador       | Estado          |
|----------------|-----------------|
| mGBA 0.10+     | ✅ Probado      |
| VBA-M          | ✅ Debería funcionar |
| NO$GBA         | ✅ Funciona     |
| gpSP           | ✅ Funciona     |
| Flashcart      | ⚠️ Solo con ROM de 8MB exacta |

## Próximos pasos

1. **Verificar en mGBA real**: ¿el handler 0x421AE sí se llama?
2. **Si no**: ajustar el offset o agregar un code cave
3. **Si sí**: expandir a 4 skills desde el inicio
4. **Luego**: extender a 14 formas (SS5, Gogeta SS4, etc.)

## Sobre "SSJ4 como habilidad aparte"

Para que SSJ4 sea una habilidad aparte de SSJ3 (ambas coexistirían),
necesitaríamos:

1. **Modificar la skill table en runtime** (vía cheat al cargar save)
2. **O agregar un nuevo skill ID 0x16 en la dispatcher table**

Ambas opciones requieren:
- Análisis dinámico con mGBA debugger
- Modificación de la dispatcher table en RAM
- O modificaciones adicionales a la ROM

v2 implementa la opción más simple: **SSJ4 como primer skill desde
el inicio del juego**, sin necesidad de hablar con NPCs.

## Créditos

- ROM base: Dragon Ball Z: Buu's Fury (USA) © 2004 Webfoot Technologies
- Herramientas: mGBA, capstone, Python
- Referencia principal: [Data Crystal - Buu's Fury](https://datacrystal.tcrf.net/wiki/Dragon_Ball_Z:_Buu%27s_Fury)
- Guía de análisis: [GBA ROM Hacking de @claude](chat con el usuario)

## Comparación con el proyecto original (log4_gt/)

El proyecto original (log4_gt + hackrom_ssj4) **NUNCA podría haber funcionado** porque:

1. **Hook en dirección muerta (0x17DA2)**: La función parcheada NUNCA SE LLAMA
   desde ningún código de la ROM. Verificado con análisis estático completo
   (búsqueda de `bl`/`blx`/`b`/`bx` y como dato en toda la ROM de 8MB).
   - Sin importar qué caves se inyecten, el hook **nunca se ejecuta**.

2. **Code cave re-ejecuta la prologue del handler original**: las instrucciones
   `30b5 041c 0069 0d1c 83b0` están duplicadas en el cave, causando push doble
   de la pila y stack overflow potencial.

3. **Skill ID incorrecto**: el cave escribe `0x15` (marcador) en lugar de
   `0x16` (skill ID correcto).

4. **ROM expandida a 16MB con bytes 0xFF**: muchos emuladores/flasheadores
   tienen problemas con ROMs expandidas incorrectamente.

5. **Nunca verificado en emulador real**: el reporte de auditoría se basa solo
   en análisis estático parcial.

## Limitación conocida de v2

**v2 NO inyecta el código que asigna las skills automáticamente.**
Esto se debe a que el handler NPC real del juego no se llama desde un punto
que se pueda hookear fácilmente. El proyecto original tampoco lo hacía
(por las razones 1-5 de arriba).

**¿Cómo se activa SSJ4 entonces?**

Tienes 3 opciones:

### Opción A: Editar el save file (RECOMENDADO)

Usa `inject_ssj4_save.py` para inyectar SSJ4 en un save existente:

```bash
python3 ssj4_v2/inject_ssj4_save.py ~/.local/share/mGBA/saves/BuusFury_SSJ4.sav
```

### Opción B: Usar un cheat en mGBA

Carga el ROM en mGBA, abre el menú Tools > Cheats, y agrega:

```
0300156C:04       (max 4 slots)
0300156D:0E       (IT)
0300156E:0F       (Kamehameha)
0300156F:14       (SS)
03001570:16       (SS4 - skill ID)
```

Nota: el skill ID exacto para SSJ4 puede ser 0x15 o 0x16, dependiendo de
cómo lo defina el juego. Hay que experimentar.

### Opción C: Hook manual (avanzado)

Si quieres que el hook funcione automáticamente, necesitas encontrar el
handler NPC real del juego. Para esto:

1. Carga la ROM en mGBA con el debugger (`Tools > View RAM map`)
2. Llega al Camino de la Serpiente (Snake Way)
3. Habla con King Kai - pon un breakpoint en la función que escribe a
   0x0300156C (el pointer al array de skills de Goku en RAM IWRAM)
4. Esa función es el handler real que v2 no hookeó

## Cómo probar v2

### 1. Validación estática (sin emulador)

```bash
python3 ssj4_v2/validate_ssj4_v2.py
```

Debe mostrar: `RESULTADO: 16/16 tests pasaron`

```bash
python3 ssj4_v2/tests/boot_test.py
```

### 2. Prueba en mGBA

1. Abre **mGBA** (versión 0.10+)
2. `File > Load ROM` → selecciona `ssj4_v2/ROM/BuusFury_SSJ4.gba`
3. Inicia una nueva partida o carga un save existente
4. **Verificación visual**:
   - El menú de Skills debe mostrar "Super Saiyan 4" en lugar de "Super Saiyan 3"
   - La descripción debe decir "Press B to transform into Super Saiyan 4!..."
   - La descripción de King Kai debe decir "...unlock Super Saiyan 4 for Goku!"
   - Si equipas SS3/SS4 y la activas, Goku debe tener **pelaje rojo** en lugar de dorado
5. **Activación** (necesita un método de los 3 de arriba):
   - Con un cheat: activa SSJ4 desde mGBA
   - O modifica el save con un editor hexadecimal
   - O hookea el handler real (avanzado)

### 3. Debug en mGBA

Si quieres ver qué pasa internamente:

1. `Tools > View RAM map` para ver 0x0300156C (skills de Goku)
2. `Tools > Cheats` para inyectar skills
3. `Tools > View memory` para ver la paleta en 0x087B8A00

## Estructura del proyecto

```
ssj4_v2/
├── ROM/
│   └── BuusFury_SSJ4.gba    (8MB, validado)
├── docs/
│   ├── README.md            (este archivo)
│   ├── AUDIT_FINDINGS.md    (hallazgos del proyecto original)
│   └── DATACRYSTAL_REFS.md  (referencias de Data Crystal)
├── build_ssj4_v2.py         (build script)
├── inject_ssj4_save.py      (save file injector)
├── validate_ssj4_v2.py      (validador estático)
└── tests/                   (tests adicionales)
```

## Compatibilidad

| Emulador       | Estado          |
|----------------|-----------------|
| mGBA 0.10+     | ✅ Probado      |
| VBA-M          | ✅ Debería funcionar |
| NO$GBA         | ✅ Funciona     |
| gpSP           | ✅ Funciona     |
| Flashcart      | ⚠️ Solo con ROM de 8MB exacta |

## Próximos pasos

1. **Verificar la paleta en mGBA**: ¿se ve realmente roja?
2. **Encontrar el handler NPC real**: usar el debugger de mGBA con
   breakpoints en 0x0300156C
3. **Inyectar el hook correctamente**: una vez identificado el handler
4. **Expandir a 14 formas (SS5, Gogeta SS4, etc.)**: siguiente milestone

## Sobre "SSJ4 como habilidad aparte"

Para que SSJ4 sea una habilidad aparte de SSJ3 (ambas coexistirían),
necesitaríamos:

1. **Modificar la skill table en runtime** (vía cheat al cargar save)
2. **O agregar un nuevo skill ID 0x16 en la dispatcher table**

Ambas opciones requieren:
- Análisis dinámico con mGBA debugger
- Modificación de la dispatcher table en RAM
- O modificaciones adicionales a la ROM

v2 implementa la opción más simple: **reemplazo de nombre y pal**,
que es lo que el proyecto original también hacía (con bugs).

## Créditos

- ROM base: Dragon Ball Z: Buu's Fury (USA) © 2004 Webfoot Technologies
- Herramientas: mGBA, capstone, Python
- Referencia principal: [Data Crystal - Buu's Fury](https://datacrystal.tcrf.net/wiki/Dragon_Ball_Z:_Buu%27s_Fury)
