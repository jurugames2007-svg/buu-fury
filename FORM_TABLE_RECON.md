# Reconocimiento de tablas de formas — evidencia estática

La ROM base contiene una tabla de punteros de nombres de formas en `0x06BEC0`.
La entrada que apunta a `SS3 Goku` (`0x080583F6`) está en esa tabla. Esto prueba
la localización de presentación, no la lógica de transformación.

También existe una referencia única a `0x086AD510` en `0x06B6D94`, dentro de una
tabla contigua de punteros a registros (`0x06B6D70` en adelante). El registro
candidato comienza en `0x06AD510` y mide al menos 32 bytes; su layout y su índice
para SSJ3 **no están verificados**.

## Qué está permitido concluir

- Renombrar SS3 en los tres textos del build seguro sólo modifica UI/texto.
- El antiguo parche que escribe una “paleta” en `0x7B8A00` no demuestra que una
  forma la lea: esa zona estaba libre (`FF`) y no había puntero validado del engine.
- Es plausible que `0x06B6D70` sea una tabla relevante, pero no se puede editar
  con seguridad sin observar su lectura durante una transformación.

## Próxima prueba obligatoria

En mGBA con símbolos/trace:

1. Iniciar una partida con Goku y transformar a SSJ3.
2. Poner watchpoint de lectura en `0x0806B6D94` y en `0x0806AD510`.
3. Registrar PC, registros y el índice de tabla cuando se lea.
4. Repetir al abrir menú de skills y al cargar un save.
5. Sólo después identificar el campo de sprite, paleta, stats y coste; añadir una
   entrada SSJ4 mediante un patch con allowlist y un test de save/load.

`inspect_form_tables.py` genera las direcciones y textos para reproducir esta
reconstrucción sin modificar la ROM.
