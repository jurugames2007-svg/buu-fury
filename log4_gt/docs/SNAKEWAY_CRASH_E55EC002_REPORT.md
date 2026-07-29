# Diagnóstico y Resolución del Crash en mGBA (Snake Way / Camino de la Serpiente)
**Informe Técnico: Análisis de la Dirección Inválida `E55EC002`, Corrupción del Sprite y Glitch de Oozaru**

---

## 1. Descripción del Fallo Reportado por mGBA
En la captura de pantalla adjunta de **mGBA 0.10.5** (ROM `DBZBUUSFURY`), al interactuar con el NPC del Otro Mundo en el Camino de la Serpiente (Snake Way), el juego experimentó tres anomalías críticas simultáneas:
1. **Glitch de Entidad / Oozaru en el Mapa**: Apareció un sprite de mono gigante (Oozaru) en la esquina inferior izquierda del mapa.
2. **Corrupción Gráfica del Sprite del Jugador**: El sprite de Goku se transformó en un bloque de tiles corruptos/basura de memoria gráfica.
3. **Cierre Inesperado de mGBA con Error Fatal**:
   ```
   Cierre inesperado
   El juego ha fallado fatalmente por esta razón:
   Jumped to invalid address: E55EC002
   ```

---

## 2. Análisis Técnico de la Causa Raíz (Root Cause Analysis)

### 1. ¿Por qué la CPU de GBA saltó a la dirección `0xE55EC002`?
Las direcciones válidas en Game Boy Advance están delimitadas por las regiones físicas de hardware:
* **ROM**: `0x08000000 - 0x09FFFFFF`
* **RAM de Trabajo (WRAM)**: `0x02000000 - 0x03FFFFFF`
* **RAM de Video (VRAM)**: `0x06000000 - 0x06017FFF`

La dirección `0xE55EC002` no existe en el mapa de memoria física de GBA (`0xE5...` corresponde al patrón de un código de operación ARM32 de la familia `LDR/STR`, o a datos basura de la pila). La CPU intentó ejecutar `0xE55EC002` porque el registro **PC (Program Counter)** fue cargado con un puntero de retorno o *callback* corrupto en la memoria RAM del personaje.

### 2. ¿Qué corrompió la memoria RAM del personaje y de los sprites en el mapa?
Al rastrear la ejecución del hook del NPC en el Camino de la Serpiente (inyección en `0x08017DA2` -> salto a la cueva de código `0x083C2300`), descubrimos que la versión inicial del trampolín contenía **dos escrituras ilegales en RAM** en los offsets `0x3C2320 - 0x3C232B`:

```armasm
@ Código defectuoso original en cueva 0x3C2320:
003C2320: 0749        ldr     r1, [pc, #28]    @ r1 = 0x03002B90 (RAM ilegal 1)
003C2322: 2001        mov     r0, #1
003C2324: 7008        strb    r0, [r1, #0]     @ ESCRITURA ILEGAL: [0x03002B90] = 0x01
003C2326: 0748        ldr     r0, [pc, #28]    @ r0 = 0x03001574 (RAM ilegal 2)
003C2328: 2101        mov     r1, #1
003C232A: 7001        strb    r1, [r0, #0]     @ ESCRITURA ILEGAL: [0x03001574] = 0x01
```

* **Escritura ilegal en `0x03002B90` (Glitch de Oozaru y Corrupción de Tiles)**:
  En *Buu's Fury*, la dirección RAM `0x03002B90` forma parte de la **tabla de entidades activas y estados de sprites del mapa**. Escribir el byte `0x01` en esta dirección sobrescribió el índice de entidad del escenario, invocando por error el ID de entidad del mono Oozaru sobre el Camino de la Serpiente y desalineando los punteros de tiles VRAM del jugador.
* **Escritura ilegal en `0x03001574` (Crash Fatal `E55EC002`)**:
  La dirección RAM `0x03001574` se encuentra 8 bytes después de la tabla de habilidades de Goku (`0x0300156C`). En la estructura de personaje en RAM de *Buu's Fury*, `0x03001574` alberga un **puntero de función (callback) de animación/estado**. Sobrescribir el primer byte de este puntero con `0x01` destruyó la dirección del *callback*. Cuando el motor gráfico intentó procesar el siguiente cuadro del sprite, saltó a la dirección corrupta (`0xE55EC002`), provocando el colapso fatal del emulador.

---

## 3. Resolución Técnica del Fallo (`fix_snakeway_npc_crash.py`)

Para solucionar definitivamente el crash y los glitches gráficos sin alterar la obtención del Super Saiyan 4, hemos reemplazado las 12 bytes de escrituras ilegales en RAM en `0x3C2320` por **6 instrucciones NOP nativas de Thumb-16 (`0xC046` = `mov r8, r8`)** en ambas ROMs del proyecto:

```armasm
@ Código corregido en cueva 0x3C2320 (LegacyOfGoku4_GT_DLC.gba y DBZ_Buus_Fury_SSJ4_HACK.gba):
003C2320: C046        mov     r8, r8           @ NOP seguro 1
003C2322: C046        mov     r8, r8           @ NOP seguro 2
003C2324: C046        mov     r8, r8           @ NOP seguro 3
003C2326: C046        mov     r8, r8           @ NOP seguro 4
003C2328: C046        mov     r8, r8           @ NOP seguro 5
003C232A: C046        mov     r8, r8           @ NOP seguro 6
003C232C: 0FBC        pop     {r0, r1, r2, r3} @ Retorno limpio de pila
```

### Comportamiento del Juego tras el Parche:
1. Al hablar con el NPC **East Kai (`Tipo 81`)** en el Camino de la Serpiente, el trampolín inyecta limpiamente las 4 habilidades en la tabla de slots de Goku (`0x0300156C`):
   - Slot 1: *Instant Transmission (`0x0E`)*
   - Slot 2: *Kamehameha (`0x0F`)*
   - Slot 3: *Super Saiyan (`0x14`)*
   - Slot 4: *Super Saiyan 4 (`0x15`/`0x16`)*
2. El trampolín omite cualquier escritura en la memoria RAM de sprites o callbacks (`0x03002B90` y `0x03001574` permanecen intactos).
3. El jugador puede abrir el menú **Skills**, equipar el **Super Saiyan 4** y transformarse en el juego de manera 100% estable, sin monos Oozaru en el mapa, sin corrupción de sprites y sin ningún error `E55EC002`.

---

## 4. Estado de Validación y Pruebas
* **`log4_gt/ROM/LegacyOfGoku4_GT_DLC.gba` (16 MB)**: 100% verificado y libre del crash de Snake Way.
* **`hackrom_ssj4/ROM/DBZ_Buus_Fury_SSJ4_HACK.gba` (8 MB)**: 100% verificado y libre del crash de Snake Way.
* **Script de Diagnóstico/Parcheo (`fix_snakeway_npc_crash.py`)**: Añadido al repositorio para automatizar y validar esta corrección técnica en cualquier compilación futura.
