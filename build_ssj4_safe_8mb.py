#!/usr/bin/env python3
"""Build the conservative 8 MiB SSJ4 presentation patch.

It intentionally contains no hook, RAM write, code cave, pointer rewrite, asset
injection, or ROM expansion. It renames the existing SSJ3 entries to SSJ4 while
reusing the game's native SSJ3 mechanics. This is a safe, reversible baseline,
not a claim of a new transformation implementation.
"""
from pathlib import Path
import hashlib

BASE = Path("Dragon Ball Z - Buu's Fury (USA).gba")
OUT = Path("hackrom_ssj4/ROM/DBZ_Buus_Fury_SSJ4_SAFE_8MB.gba")
# Each source string has the same UTF-16LE layout; only ASCII '3' becomes '4'.
PATCHES = {
    0x583FA: (0x33, 0x34, "form name: SS3 Goku -> SS4 Goku"),
    0x6A55E: (0x33, 0x34, "skill name: Super Saiyan 3 -> Super Saiyan 4"),
    0x6BAF4: (0x33, 0x34, "rank title: Super Saiyan 3 -> Super Saiyan 4"),
}

def main() -> int:
    rom = bytearray(BASE.read_bytes())
    if len(rom) != 0x800000:
        raise SystemExit(f"base must be exactly 8 MiB; got {len(rom)} bytes")
    for offset, (before, after, label) in PATCHES.items():
        if rom[offset] != before:
            raise SystemExit(f"refusing to patch {label}: 0x{offset:X} is {rom[offset]:02X}, expected {before:02X}")
        rom[offset] = after
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(rom)
    print(f"wrote {OUT} ({len(rom)} bytes)")
    print("sha256=" + hashlib.sha256(rom).hexdigest())
    print("This build is presentation-only and retains native SSJ3 behavior.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
