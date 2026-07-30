# Política de assets y atribución

## Regla de distribución

El ejecutable solo incluirá assets que puedan redistribuirse legalmente:

1. Arte, música, SFX, fuentes y UI originales creados para el proyecto.
2. Assets fanmade entregados por el titular o con una licencia explícita que permita su uso y redistribución.
3. Recursos con licencia compatible, conservando atribución y condiciones.

## Material de referencia

Los juegos de GBA, capturas, videos y sprites comerciales pueden consultarse de manera privada para estudiar lectura visual, escala, color, timing y diseño de combate. No se copiarán ni empaquetarán sus ROMs, código, tiles, música, diálogos, mapas, sprites o binarios en el ejecutable.

## Registro obligatorio por asset

Todo recurso incorporado deberá figurar en `assets/ASSET_MANIFEST.json` con:

- Identificador y ruta.
- Autor o fuente.
- Licencia/permisos.
- Fecha de incorporación.
- Si requiere atribución y texto exacto.
- Estado: `approved`, `needs_permission` o `reference_only`.

Un asset `needs_permission` o `reference_only` no entra al build.

## Estilo visual buscado

- Pixel art 16-bit moderno, siluetas claras y animación fluida.
- Paletas limitadas por personaje/zona, no por limitación de hardware.
- Retratos expresivos de alta resolución y UI nítida.
- Sprites originales con equivalentes funcionales para: idle, caminar, correr, golpe, ki, daño, derribo, transformación y vuelo.

## Contenido narrativo

GT y las líneas AF aportadas por el usuario se usarán como base de adaptación. Antes de publicar, se revisarán nombres, texto, arte y audio para comprobar derechos de uso y diferenciar claramente contenido fan de cualquier material oficial.
