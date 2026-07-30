# Hallazgos del Proyecto Original (log4_gt + hackrom_ssj4)

Documento de auditoría técnica que documenta los problemas encontrados
en el proyecto original y por qué nunca pudo haber funcionado.

## Resumen ejecutivo

El proyecto original (carpeta `log4_gt/` y `hackrom_ssj4/`) intenta inyectar
la transformación **Super Saiyan 4** en el juego **Dragon Ball Z: Buu's Fury**
vía un hook de código en una función de la ROM.

**El hook nunca se ejecuta.** Por lo tanto, sin importar cuántas líneas de
código o cuántos assets se hayan creado, la ROM no puede inyectar las skills
de SSJ4.

## Hallazgo #1: Hook en código muerto (CRÍTICO)

**Ubicación del hook:** `0x17DA2` (10 bytes)

**Función parcheada:** Empieza en `0x17DA2` con `push {r4, r5, lr}`

**Análisis estático:**

```
$ Buscar todas las llamadas a 0x17DA2 en los 8MB de la ROM base
$ Incluyendo: bl, blx, b, bx, y referencias como dato (4-byte value)
$ Resultado: 0 referencias encontradas
```

**Conclusión:** La función en 0x17DA2 **no es llamada desde ningún código**
en la ROM de 8MB. El hook está parchando código huérfano.

**Verificación adicional:**

```
$ Buscar 0x0817DA2 como data (4-byte little-endian)
$ Resultado: 0 referencias
```

**Conclusión:** La dirección tampoco se usa como puntero a función en
ninguna tabla de handlers.

## Hallazgo #2: Code cave re-ejecuta prologue (BUG ESTRUCTURAL)

**Ubicación del cave:** `0x3C2300`

**Contenido del cave (primeras 32 instrucciones):**

```arm
push {r0, r1, r2, r3}            ; guarda caller state (16 bytes)
adds r3, r0, #0                  ; r3 = entity
ldr r1, [r3, #0x10]              ; r1 = entity->type
cmp r1, #0x51                    ; compare with 0x51 (King Kai?)
bne +0x20                        ; if not, skip
ldr r0, [pc, #0x30]              ; r0 = 0x0300156C (RAM addr)
movs r1, #4                      ; r1 = 4
strb r1, [r0]                    ; 0x0300156C = 4
movs r1, #0xE                    ; r1 = IT
strb r1, [r0, #1]
movs r1, #0xF                    ; r1 = Kame
strb r1, [r0, #2]
movs r1, #0x14                   ; r1 = SS
strb r1, [r0, #3]
movs r1, #0x15                   ; r1 = SS4 marker (NO 0x16!)
strb r1, [r0, #4]
... 6 NOPs (mov r8, r8) ...
pop {r0, r1, r2, r3}             ; restaura caller state
push {r4, r5, lr}                ; <-- DUPLICATE prologue!
adds r4, r0, #0
ldr r0, [r0, #0x10]
adds r5, r1, #0
sub sp, #0xc
ldr r3, [pc, #0xc]               ; r3 = 0x0300156C ???!!!
bx r3                            ; <-- bx to RAM address!
```

**Bug #2.1:** El `bx r3` salta a la dirección 0x0300156C, que es RAM.
Pero después del pop, el `push {r4, r5, lr}` RE-EMPUJA LR. Si el hook
se ejecutara (cosa que no ocurre), causaría stack corruption.

**Bug #2.2:** El `bx r3` debería saltar a la dirección de retorno del
handler original (0x08017DAD), no a una dirección RAM. Esto se hizo
incorrectamente.

**Bug #2.3:** Después de la prologue duplicada, el código entra a
0x08017DAD que es la continuación de la función original DESPUÉS del
prologue. Pero como ya ejecutamos la prologue dos veces, la pila tiene
24 bytes de más, y la función original intenta retornar usando una
dirección LR incorrecta.

## Hallazgo #3: Skill ID incorrecto (BUG DE DATOS)

**Esperado según el audit:** Skill ID `0x16` para "Super Saiyan 4"

**Real en el cave:** Skill ID `0x15`

**Análisis:**

El cave escribe:
```
strb r1, [r0, #4]    ; offset 0x4 de 0x0300156C = 0x03001570
                      ; r1 = 0x15
```

Pero el audit report del proyecto original dice que debería ser `0x16`.
Esto significa que el cave está escribiendo el ID de "marcador SS4" en
lugar del "skill ID SS4" en el slot de skill.

## Hallazgo #4: ROM expandida incorrectamente

**Tamaño del proyecto original:** 16,777,234 bytes (16MB expandido)

**Esperado por GBA:** Múltiplos de 2: 8MB, 16MB, 32MB

**Real:** 16,777,234 ≠ 16,777,216 (16MB exacto). Es 18 bytes de más.

**Análisis:**

El script de inyección:
1. Lee la ROM base (8MB)
2. Extiende con `\xFF * (16MB - 8MB)` = 8,388,608 bytes de 0xFF
3. Inyecta código en cave

Pero el script también escribe strings de longitud variable en regiones
que pueden extenderse más allá de los 8MB originales si no se verifica
el tamaño.

**Resultado:** La ROM tiene 18 bytes extra (probablemente un bug de
encoding UTF-16LE sin contar el null terminator), lo cual puede
causar problemas en flasheadores y algunos emuladores.

## Hallazgo #5: Sin verificación dinámica

**Reporte de auditoría del proyecto original:** "FUNCTIONAL" con OK=74, WARN=3

**Análisis:** El reporte verifica:
- Header GBA (✓ correcto)
- Encoding del hook (✓ correcto)
- Cave bytes (✓ correcto)
- Patrones de string (✓ correcto)
- "Idempotencia" (✓ claimed, pero el cave no es idempotente!)

**NO verifica:**
- Que la función hookeada se llame
- Que la ROM boote en un emulador
- Que la skill SS4 esté realmente disponible
- Que la transformación visual funcione
- Que no haya crashes

## Hallazgo #6: Reporte afirma cosas falsas

**Reporte dice:** "FUNCTIONAL" - "BOOT → NPC TALK → SKILLS GRANTED → TRANSFORM"

**Realidad:**
- BOOT funciona (header válido)
- NPC TALK es teóricamente OK (cave tiene la lógica)
- SKILLS GRANTED **nunca se ejecuta** (Hallazgo #1)
- TRANSFORM nunca ocurre

## Comparación v1 vs v2

| Aspecto                      | Proyecto Original | SSJ4 v2 |
|------------------------------|-------------------|---------|
| Hook en código que se ejecuta| ❌ Hook en código muerto | ✅ No inyecta código |
| Tamaño de la ROM             | 16MB (corrupto)   | ✅ 8MB exacto |
| Header preservado            | ✅                | ✅      |
| Code caves                   | 1 (con bugs)      | ✅ 0   |
| Escrituras a RAM peligrosas  | Potencialmente 2  | ✅ 0   |
| Validación estática          | Parcial (74 OK)   | ✅ 16/16 + boot test |
| ROM verificada en emulador   | ❌ Nunca          | ⚠️ Pendiente de prueba local |
| Skill grant funciona         | ❌ Nunca podría  | ⚠️ Requiere cheat/save edit |
| Paleta SSJ4                  | ❌ Colores random  | ✅ Roja dominante |
| Strings limpios              | ❌ Overflows      | ✅ Truncados a tamaño fijo |
| Documentación honesta        | ❌ AUDIT 100% OK  | ✅ Limitaciones explícitas |

## Lo que el proyecto original hizo BIEN

A pesar de los bugs, el proyecto original:
- Identificó correctamente la estructura de pal ptrs en 0x6AD510+0x4 y +0xA8
- Identificó correctamente la ubicación de la paleta (0x7B8A00)
- Identificó los offsets de strings UTF-16LE correctamente
- Documentó la arquitectura esperada del ROM hack
- Creó un audit script que verifica muchos aspectos técnicos

## Recomendación

**No usar el proyecto original como está.** El hook no funciona.

**Usar SSJ4 v2 como base.** Es estáticamente válido y solo requiere
que el usuario active la skill de SSJ4 con un cheat o editando el save.
