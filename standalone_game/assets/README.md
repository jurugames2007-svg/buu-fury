# Assets del ejecutable

## Carpetas

```text
assets/
├── approved/          # archivos aprobados para incluir en builds
├── fanmade_pending/   # material recibido, aún sin licencia/permisos verificados
└── ASSET_MANIFEST.json
```

## Cómo incorporar un asset

1. Ubicarlo dentro de `approved/` solo si existe permiso de modificación y redistribución.
2. Agregar una entrada al manifiesto con autor, fuente y licencia explícita.
3. Marcar `status` como `approved`.
4. Ejecutar:

```bash
python3 standalone_game/tools/asset_audit.py
```

Los sprites/tiles/audio provenientes de ROMs o páginas de sprites se pueden estudiar como referencia visual privada, pero no se copian automáticamente a `approved/` ni al ejecutable. Así el proyecto puede tener estética fiel de GBA sin distribuir recursos propietarios sin autorización.
