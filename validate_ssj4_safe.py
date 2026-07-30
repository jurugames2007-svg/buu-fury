#!/usr/bin/env python3
"""Complete static validator for the audited 8 MiB SSJ4 presentation baseline.

This validates only claims that can be proven from two ROM files.  It exits with
failure for the old expanded artifact and never treats static success as emulator
or gameplay proof.
"""
from __future__ import annotations
import argparse, hashlib, json, sys, zlib
from pathlib import Path
from validate_ssj4_integrity import GBA_LOGO, header_checksum, ROM_8M

PATCHES = (
    (0x583FA, 0x33, 0x34, "form label: SS3 Goku → SS4 Goku"),
    (0x6A55E, 0x33, 0x34, "skill label: Super Saiyan 3 → Super Saiyan 4"),
    (0x6BAF4, 0x33, 0x34, "rank label: Super Saiyan 3 → Super Saiyan 4"),
)
TEXT_EXPECTED = ((0x583F6, "SS4 Goku"), (0x6A544, "Super Saiyan 4"), (0x6BADA, "Super Saiyan 4"))

def fail(message: str) -> None:
    print(f"FAIL: {message}")

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--base', type=Path, default=Path("Dragon Ball Z - Buu's Fury (USA).gba"))
    ap.add_argument('--hack', type=Path, default=Path("hackrom_ssj4/ROM/DBZ_Buus_Fury_SSJ4_SAFE_8MB.gba"))
    ap.add_argument('--manifest', type=Path, default=Path("hackrom_ssj4/patches/ssj4_safe_8mb_manifest.json"))
    args=ap.parse_args()
    base=args.base.read_bytes(); hack=args.hack.read_bytes(); passed=True
    for label, rom in (("base",base),("hack",hack)):
        print(f"{label}: {len(rom)} bytes | crc32={zlib.crc32(rom)&0xffffffff:08X} | sha256={hashlib.sha256(rom).hexdigest()}")
        if len(rom) != ROM_8M: fail(f"{label} must be 0x800000 bytes"); passed=False
        if rom[4:0xA0] != GBA_LOGO: fail(f"{label} Nintendo logo differs"); passed=False
        if rom[0xBD] != header_checksum(rom): fail(f"{label} header checksum invalid"); passed=False
        if rom[0xAC:0xB0] != b"BG3E": fail(f"{label} game code is not BG3E"); passed=False
    if len(base) != len(hack): return 1
    changed=[i for i,(a,b) in enumerate(zip(base,hack)) if a != b]
    expected={offset for offset,_,_,_ in PATCHES}
    if set(changed) != expected:
        fail(f"changed offsets {', '.join(hex(x) for x in changed)} do not equal strict allowlist")
        passed=False
    for offset,before,after,label in PATCHES:
        if base[offset] != before or hack[offset] != after:
            fail(f"0x{offset:06X}: invalid bytes for {label}"); passed=False
        else: print(f"PASS: 0x{offset:06X} {label}")
    for offset,want in TEXT_EXPECTED:
        got=hack[offset:offset+64].decode('utf-16le','replace').split('\0')[0]
        if got != want: fail(f"0x{offset:06X}: text {got!r}, expected {want!r}"); passed=False
    try:
        manifest=json.loads(args.manifest.read_text(encoding='utf-8'))
        if manifest.get('feature_status') != 'presentation-only':
            fail('manifest must explicitly retain presentation-only status'); passed=False
    except (OSError,json.JSONDecodeError) as exc:
        fail(f'manifest unavailable/invalid: {exc}'); passed=False
    print('RESULT:', 'PASS (static presentation baseline only)' if passed else 'FAIL')
    if passed:
        print('RUNTIME STATUS: NOT VERIFIED — boot, transform, battle, map, save/load and new SSJ4 mechanics require mGBA/no$gba evidence.')
    return 0 if passed else 1
if __name__ == '__main__': sys.exit(main())
