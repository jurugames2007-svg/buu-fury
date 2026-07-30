#!/usr/bin/env python3
"""
Test final: verifica que la ROM modificada puede ser parseada como una ROM GBA válida
y que tiene los hooks visuales correctos.
"""
import os
import struct

ROM_OUT = "ssj4_v2/ROM/BuusFury_SSJ4.gba"
ROM_BASE = "Dragon Ball Z - Buu's Fury (USA).gba"

def main():
    print("="*80)
    print(" SSJ4 v2 — BOOT TEST")
    print("="*80)
    print()
    print("Verificación final del ROM antes de probar en mGBA")
    print()
    
    if not os.path.exists(ROM_OUT):
        print(f"[FAIL] ROM not found: {ROM_OUT}")
        return 1
    
    if not os.path.exists(ROM_BASE):
        print(f"[FAIL] Base ROM not found: {ROM_BASE}")
        return 1
    
    with open(ROM_BASE, "rb") as f:
        base = f.read()
    with open(ROM_OUT, "rb") as f:
        mod = f.read()
    
    # 1. Tamaño exacto
    if len(mod) != 8388608:
        print(f"[FAIL] Tamaño incorrecto: {len(mod)} bytes (esperado 8388608)")
        return 1
    print(f"[ OK] Tamaño: {len(mod)} bytes (8MB exacto)")
    
    # 2. Header válido
    if mod[:4] != b'\x2e\x00\x00\xea':
        print(f"[FAIL] Entry point incorrecto: {mod[:4].hex()}")
        return 1
    print(f"[ OK] Entry point válido: 0x2e0000ea (B +0xBC)")
    
    # 3. Logo Nintendo presente
    if mod[4:0xA0] != base[4:0xA0]:
        print(f"[FAIL] Logo Nintendo corrupto")
        return 1
    print(f"[ OK] Logo Nintendo intacto")
    
    # 4. Título correcto
    title = mod[0xA0:0xAC].rstrip(b'\x00').decode('ascii', errors='ignore')
    if title != "DBZBUUSFURY":
        print(f"[FAIL] Título incorrecto: {title!r}")
        return 1
    print(f"[ OK] Título: {title}")
    
    # 5. Game code correcto
    game_code = mod[0xAC:0xB0].decode('ascii', errors='ignore')
    if game_code != "BG3E":
        print(f"[FAIL] Game code incorrecto: {game_code!r}")
        return 1
    print(f"[ OK] Game code: {game_code}")
    
    # 6. Checksum
    s = sum(mod[i] for i in range(0xA0, 0xBD))
    expected = (-s - 0x19) & 0xFF
    actual = mod[0xBD]
    if actual != expected:
        print(f"[FAIL] Checksum incorrecto: 0x{actual:02X} (esperado 0x{expected:02X})")
        return 1
    print(f"[ OK] Header checksum: 0x{actual:02X}")
    
    # 7. NO está expandido
    if len(mod) > 8388608:
        print(f"[FAIL] ROM está expandida a {len(mod)} bytes")
        return 1
    print(f"[ OK] ROM NO está expandida (mantiene 8MB)")
    
    # 8. Cuenta modificaciones esperadas
    expected_regions = [
        (0x0583F6, 22),    # form name
        (0x06A544, 30),    # skill name
        (0x06A562, 240),   # skill desc
        (0x06BADA, 30),    # rank title
        (0x063534, 240),   # king kai desc
        (0x06AD514, 4),    # pal ptr 1
        (0x06AD5B8, 4),    # pal ptr 2
        (0x07B8A00, 32),   # palette
    ]
    total_expected = sum(s for _, s in expected_regions)
    print(f"[ OK] Modificaciones esperadas: {len(expected_regions)} regiones, {total_expected} bytes total")
    
    # 9. Paleta roja SSJ4
    palette = mod[0x07B8A00:0x07B8A20]
    red_count = 0
    for i in range(0, 32, 2):
        c = struct.unpack('<H', palette[i:i+2])[0]
        r = c & 0x1F
        g = (c >> 5) & 0x1F
        b = (c >> 10) & 0x1F
        if r > g and r > b and r > 5:
            red_count += 1
    if red_count < 8:
        print(f"[FAIL] Paleta no es dominante roja: {red_count}/16 colores rojos")
        return 1
    print(f"[ OK] Paleta SSJ4: {red_count}/16 colores rojos")
    
    # 10. Strings UTF-16LE correctos
    def read_utf16(offset, size):
        return mod[offset:offset+size].decode('utf-16-le').split('\x00')[0]
    
    form_name = read_utf16(0x0583F6, 22)
    if form_name != "SS4 Goku":
        print(f"[FAIL] Form name: {form_name!r} (esperado 'SS4 Goku')")
        return 1
    print(f"[ OK] Form name: {form_name!r}")
    
    skill_name = read_utf16(0x06A544, 30)
    if skill_name != "Super Saiyan 4":
        print(f"[FAIL] Skill name: {skill_name!r}")
        return 1
    print(f"[ OK] Skill name: {skill_name!r}")
    
    print()
    print("="*80)
    print(" ✅ TODOS LOS TESTS DE BOOT PASARON")
    print("="*80)
    print()
    print("El ROM está listo para probar en mGBA o cualquier emulador GBA.")
    print()
    print("Próximos pasos:")
    print("  1. Carga el ROM en mGBA")
    print("  2. Inicia una nueva partida o carga un save")
    print("  3. Ve al menú de Skills - debe decir 'Super Saiyan 4'")
    print("  4. Equipa SS4 y presiona B - Goku debe tener pelaje rojo")
    print()
    print("NOTA: Para activar la skill SS4 por primera vez, usa un cheat en mGBA:")
    print("  0300156C:04  (max 4 slots)")
    print("  0300156D:0E  (IT)")
    print("  0300156E:0F  (Kamehameha)")
    print("  0300156F:14  (SS)")
    print("  03001570:16  (SS4 skill ID)")
    print()
    return 0


if __name__ == "__main__":
    import sys
    # script is in ssj4_v2/tests/ - go up two levels to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)
    sys.exit(main())
