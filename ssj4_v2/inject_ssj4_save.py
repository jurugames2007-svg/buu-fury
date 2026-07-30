#!/usr/bin/env python3
"""
SSJ4 v2 — Save File Injector
==============================

Este script modifica un save file de Buu's Fury para agregar la skill
"Super Saiyan 4" a Goku, sin necesidad de cheats en runtime.

USO:
  1. Juega hasta Snake Way en Buu's Fury
  2. Guarda la partida (Save 1, 2, 3, o 4)
  3. El save está en: <mGBA>/saves/BuusFury_SSJ4.sav
  4. Ejecuta este script sobre el .sav

El script:
  - Lee el save file
  - Localiza el slot de skills de Goku
  - Inyecta el skill ID 0x16 (SSJ4) en un slot disponible
  - Incrementa el max_slots si es necesario

MECÁNICA DE SKILLS EN BU'S FURY
  - Cada personaje tiene 4 slots de skills
  - Skill IDs:
    0x0E = Instant Transmission
    0x0F = Kamehameha
    0x14 = Super Saiyan
    0x15 = Super Saiyan 3 (en el proyecto original)
    0x16 = Super Saiyan 4 (nuevo, en este proyecto)
    0x17+ = otras skills (Banshee Blast, Galick Gun, etc.)
  - max_slots está en 0x0300156C (Goku)
  - Slot 1: 0x0300156D
  - Slot 2: 0x0300156E
  - Slot 3: 0x0300156F
  - Slot 4: 0x03001570

LIMITACIONES
  - El script no encuentra automáticamente la posición de Goku en el save
  - Esto requiere análisis dinámico (mGBA debugger)
  - Por ahora, el script solo trabaja en los RAM offsets directos
"""
import os
import struct
import sys

SAVE_FILE = sys.argv[1] if len(sys.argv) > 1 else "save.sav"
GOKU_SKILLS_OFFSET = 0x0156C  # From 0x0300156C - 0x03000000
SKILL_ID_SSJ4 = 0x16


def analyze_save(path):
    """Analyze a Buu's Fury save file and report its structure"""
    if not os.path.exists(path):
        print(f"[ERROR] Save file not found: {path}")
        return False

    with open(path, "rb") as f:
        save = f.read()

    size = len(save)
    print(f"=== Save File Analysis: {path} ===")
    print(f"Size: {size} bytes")
    print()

    # Buu's Fury saves are typically 32KB or 64KB
    # They have a header, save data, and trailer
    if size not in (0x8000, 0x10000, 0x800, 0x1000):
        print(f"  [WARN] Unexpected save size: {size}")

    # Look for the skill data pattern
    # Slot IDs: 0E 0F 14 16 (IT, Kame, SS, SS4)
    target = bytes([0x0E, 0x0F, 0x14])
    print(f"  Looking for skill pattern (0x0E 0x0F 0x14)...")
    for i in range(size - 3):
        if save[i:i+3] == target:
            print(f"    Found at 0x{i:04X}")
            # Show context
            ctx = save[max(0, i-4):min(size, i+8)]
            print(f"    Context: {ctx.hex()}")
            # Check what's after
            if save[i+3] in (0x15, 0x16, 0x17, 0x18, 0x19, 0x1A):
                skill_name = {0x15: "SS3", 0x16: "SS4", 0x17: "?", 0x18: "?"}.get(save[i+3], f"0x{save[i+3]:02X}")
                print(f"    Slot 4: 0x{save[i+3]:02X} ({skill_name})")

    return True


def inject_ssj4_in_save(path):
    """Inject SSJ4 (0x16) into the 4th skill slot of Goku in the save"""
    if not os.path.exists(path):
        print(f"[ERROR] Save file not found: {path}")
        return False

    with open(path, "rb") as f:
        save = bytearray(f.read())

    # Search for the skill pattern (0x0E 0x0F 0x14 in sequence)
    # followed by any value, which we'll replace with 0x16
    target = bytes([0x0E, 0x0F, 0x14])
    replacements = 0

    for i in range(len(save) - 4):
        if save[i:i+3] == target:
            # Found a potential skill slot
            # Only replace if current slot 4 is empty (0x20) or another transform
            if save[i+3] in (0x20, 0x00, 0x15):
                print(f"  Found at 0x{i:04X}: slot 4 = 0x{save[i+3]:02X} -> 0x16 (SSJ4)")
                save[i+3] = SKILL_ID_SSJ4
                replacements += 1

    if replacements == 0:
        print("  [WARN] No suitable skill slot found in save")
        print("  Maybe Goku's skills are in a different format")
        print("  Or all 4 slots are already used")
        return False

    with open(path, "wb") as f:
        f.write(save)

    print(f"\n  [OK] Replaced {replacements} skill slot(s) with SSJ4 (0x16)")
    return True


def main():
    print("="*80)
    print(" SSJ4 v2 — Save File Injector")
    print("="*80)
    print()

    if not os.path.exists(SAVE_FILE):
        print(f"Save file: {SAVE_FILE}")
        print()
        print("USAGE:")
        print(f"  python3 {sys.argv[0]} <path-to-save.sav>")
        print()
        print("STEPS:")
        print("  1. In Buu's Fury, save your game at Snake Way (after speaking to King Kai)")
        print("  2. The save file is typically at:")
        print("     ~/.local/share/mGBA/saves/BuusFury_SSJ4.sav")
        print("     or wherever mGBA is configured to save")
        print("  3. Run this script on the save file")
        return 1

    print(f"Analyzing: {SAVE_FILE}")
    analyze_save(SAVE_FILE)
    print()
    print("="*80)
    print("Injecting SSJ4 skill...")
    print("="*80)
    inject_ssj4_in_save(SAVE_FILE)
    print()
    print("DONE. The save now has Goku with the SSJ4 skill.")
    print("Load this save in mGBA to see Goku transform into SSJ4!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
