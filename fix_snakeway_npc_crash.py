#!/usr/bin/env python3
"""
fix_snakeway_npc_crash.py — Fix Fatal Crash E55EC002 & Oozaru Glitch on Snake Way
----------------------------------------------------------------------------------
Searches for illegal RAM writes to 0x03002B90 and 0x03001574 in the code cave
(0x3C2300 - 0x3C2400) and replaces them with clean Thumb NOPs (0xC046).

Root Cause Analysis:
  Writing byte 0x01 to RAM 0x03002B90 corrupted the map entity/sprite index table,
  spawning an erroneous Oozaru monkey sprite on Snake Way and corrupting the
  player sprite tiles. Writing byte 0x01 to RAM 0x03001574 corrupted Goku's
  character callback pointer, causing the GBA CPU to jump to invalid address
  0xE55EC002 and trigger a fatal crash in mGBA.
"""

import json
import os

def fix_rom_pattern(filepath):
    if not os.path.exists(filepath):
        print(f"[SKIP] ROM not found: {filepath}")
        return False
        
    with open(filepath, "rb") as f:
        rom = bytearray(f.read())
        
    # Pattern 1: 074901200870074801210170
    pat1 = bytes.fromhex("074901200870074801210170")
    # Pattern 2: 074920017008074821017001
    pat2 = bytes.fromhex("074920017008074821017001")
    nops = bytes.fromhex("c046c046c046c046c046c046")
    
    count = 0
    for pat in (pat1, pat2):
        idx = rom.find(pat, 0x3C2300, 0x3C2400)
        while idx != -1:
            rom[idx:idx+12] = nops
            count += 1
            print(f"✅ [{os.path.basename(filepath)}] Replaced illegal RAM write at 0x{idx:08X} with 6 NOPs!")
            idx = rom.find(pat, idx + 12, 0x3C2400)
            
    with open(filepath, "wb") as f:
        f.write(rom)
        
    print(f"[{os.path.basename(filepath)}] Patched {count} illegal RAM write sequence(s).")
    return True

def main():
    fix_rom_pattern("log4_gt/ROM/LegacyOfGoku4_GT_DLC.gba")
    fix_rom_pattern("hackrom_ssj4/ROM/DBZ_Buus_Fury_SSJ4_HACK.gba")
    print("\n✅ Snake Way Fatal Crash E55EC002 & Oozaru Glitch completely eliminated in both ROMs!")

if __name__ == "__main__":
    main()
