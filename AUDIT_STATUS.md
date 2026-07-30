# Estado honesto de auditoría — SSJ4 / expansión

**Estado actual: FAIL — no distribuir como ROM funcional ni como base de expansión.**

Este archivo reemplaza las afirmaciones no verificadas de “100%”, “crash-free” y
“300/300”. La presencia de assets o de un archivo binario no prueba que el engine
los use.

## Evidencia reproducible (2026-07-30)

- Base: `Dragon Ball Z - Buu's Fury (USA).gba`, 8,388,608 bytes.
- Hack publicado: `hackrom_ssj4/ROM/DBZ_Buus_Fury_SSJ4_HACK.gba`, **16,777,234
  bytes**, no 16,777,216. Por tanto no tiene una geometría limpia de 16 MiB y no
  puede aprobar el requisito de ROM de 8 MiB.
- El diff base→hack modifica 7,562,660 bytes dentro de los primeros 8 MiB y añade
  1,092,121 bytes no-`FF` después de 8 MiB. No es un patch mínimo ni tiene una
  allowlist verificable.
- El hook de `0x17DA2` y la cueva `0x3C2300` no tienen evidencia de xrefs,
  ejecución en runtime, preservación de registros ni prueba en mGBA. El script
  que los escribe no es evidencia de que sean seguros.
- Los mapas, sprites, audio y AI se copian a offsets, pero el build no instala ni
  valida tablas/punteros del engine para alcanzarlos. Se consideran **assets no
  conectados**, no features.
- No hay mGBA/no$gba instalado en este entorno, ni log/trace/savestate de una
  ejecución. Boot, save/load, menú, combate y transformación son BLOQUEANTES.

## Decisión de implementación (dos etapas)

1. **SSJ4 estable de 8 MiB:** partir de la ROM base, permitir solo una lista de
   cambios documentada; localizar tablas reales mediante desensamblado y demostrar
   en mGBA el skill, UI, transformación y save. No instalar hooks hasta que haya
   xrefs y un trace de ejecución.
2. **Expansión de 16 MiB:** copiar la ROM de 8 MiB a exactamente `0x1000000`,
   documentar free space y header; implementar un único vertical slice conectado
   (NPC/evento → skill nativa → UI/RAM → save) antes de maps/AI/audio. Cada
   puntero nuevo debe estar conectado a una tabla del engine y pasar pruebas de
   boot/regresión.

## Comando de integridad

```sh
python3 validate_ssj4_integrity.py \
  "Dragon Ball Z - Buu's Fury (USA).gba" \
  hackrom_ssj4/ROM/DBZ_Buus_Fury_SSJ4_HACK.gba
```

El comando está diseñado para fallar si el tamaño o la allowlist no son válidos.
No interpreta un `PASS` estático como prueba de runtime.
