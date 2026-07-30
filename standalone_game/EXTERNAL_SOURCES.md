# Registro de fuentes externas propuestas

Este registro conserva las fuentes de referencia aportadas para el proyecto. Una URL de sprites o una página de extracción **no equivale** a una licencia de redistribución para incluir esos archivos en un ejecutable.

| Fuente | Uso permitido dentro del flujo actual | Estado de incorporación |
|---|---|---|
| The Spriters Resource — Legacy/Buu's Fury/GT | Referencia visual y de cobertura de animaciones | `reference_only` |
| Sprite Database — Legacy/Buu's Fury | Referencia de catálogo | `reference_only` |
| Data Crystal / TCRF | Investigación de diseño, datos y documentación de sistemas | `reference_only` |
| GameFAQs scripts | Referencia de estructura narrativa | `reference_only` |
| Dragon Ball Customs | Candidato solo si el autor/licencia permite redistribución | `needs_permission` |
| Assets ya presentes en `generated_assets/` | Candidato; requiere autoría/licencia en manifest antes del build | `needs_permission` |

## Procedimiento de incorporación

1. Registrar archivo, autor, URL de origen y licencia en `assets/ASSET_MANIFEST.json`.
2. Confirmar explícitamente permiso de modificación y redistribución en el ejecutable.
3. Convertir a formato de proyecto (PNG, tileset, portrait, SFX) sin incluir datos de ROM.
4. Ejecutar validación de tamaño, transparencia, paleta, metadatos y atribución.
5. Marcar `approved` solo después de completar los pasos anteriores.

Hasta entonces, el prototipo usa gráficos provisionales dibujados por código y no incorpora contenido descargado de esas páginas.
