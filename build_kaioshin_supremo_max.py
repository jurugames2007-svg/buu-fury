#!/usr/bin/env python3
"""Build the Kaioshin Supremo early-game reward ROM for Buu's Fury (USA).

The patch reuses the four King Kai map entities already present on Snake Way.
Their dialogue is replaced by the Supreme Kai reward dialogue.  The NPC hook
writes the documented Goku RAM fields on interaction: XP (level cap), HP/EP,
and STR/POW/END/SPD.  It also gives the existing four skill slots.

This deliberately stays an 8 MiB ROM and only uses unused 0xFF space for the
NPC dialogue/script data and Thumb routine.
"""
from pathlib import Path
import hashlib
import struct

BASE = Path("Dragon Ball Z - Buu's Fury (USA).gba")
OUT = Path("ROM/BuusFury_Kaioshin_Supremo_MAX.gba")
SIZE = 8 * 1024 * 1024

# Existing Snake Way King Kai entity dialogue-pointer fields.  All four are
# changed so the reward remains available regardless of the Snake Way variant.
NPC_DIALOGUE_FIELDS = (0x74CD4, 0x74F34, 0x74F5C, 0x7529C)
DIALOGUE_TABLE = 0x7B8D10
DIALOGUE_STRINGS = (0x7B8B20, 0x7B8B94, 0x7B8C10, 0x7B8CA0)
CAVE = 0x3C2300
STAT_ROUTINE = 0x3C2360


def gba_ptr(offset: int) -> bytes:
    return struct.pack("<I", 0x08000000 + offset)


def thumb_bl(source: int, target: int) -> bytes:
    """Encode a Thumb-1 BL at ROM offsets *source* -> *target*."""
    offset = target - (source + 4)
    if offset & 1 or not -(1 << 24) <= offset < (1 << 24):
        raise ValueError("BL target out of range")
    value = offset & 0x01FFFFFF
    s = (value >> 24) & 1
    i1 = (value >> 23) & 1
    i2 = (value >> 22) & 1
    imm10 = (value >> 12) & 0x3FF
    imm11 = (value >> 1) & 0x7FF
    j1 = ((~i1) ^ s) & 1
    j2 = ((~i2) ^ s) & 1
    first = 0xF000 | (s << 10) | imm10
    second = 0xF800 | (j1 << 13) | (j2 << 11) | imm11
    return struct.pack("<HH", first, second)


def utf16_slot(text: str, size: int) -> bytes:
    data = text.encode("utf-16-le") + b"\0\0"
    if len(data) > size:
        raise ValueError(f"Dialogue does not fit: {text!r}")
    return data + b"\0" * (size - len(data))


def build_stat_routine(address: int) -> bytes:
    """Thumb routine writing documented Goku fields at 0x03001576.

    XP is set to 0x7fffffff; the original level routine clamps this to its
    native maximum (level 200).  The four allocatable stats use their byte
    maximum (255), while HP/EP are filled to 0xffff.
    """
    # push {lr}; ldr r0,=Goku HP; ldr r1,=0xffff; store HP/EP;
    # r0 += 14 -> XP; ldr r1,=0x7fffffff; store XP; r0 += 4 -> STR;
    # write four 0xff stats; pop {pc}.
    code = bytearray()
    code += bytes.fromhex("00b5")
    ldr_goku_pos = len(code); code += b"\0\0"
    ldr_hp_pos = len(code); code += b"\0\0"
    code += bytes.fromhex("018041808180c180")
    code += bytes.fromhex("0e30")
    ldr_xp_pos = len(code); code += b"\0\0"
    code += bytes.fromhex("0160")
    code += bytes.fromhex("0430ff21017041708170c17000bd")
    while len(code) % 4:
        code += b"\0"
    literals = (0x03001576, 0x0000FFFF, 0x7FFFFFFF)
    literal_offsets = []
    for literal in literals:
        literal_offsets.append(len(code))
        code += struct.pack("<I", literal)

    def ldr_literal(pos: int, reg: int, literal_pos: int) -> None:
        pc = (address + pos + 4) & ~3
        delta = address + literal_pos - pc
        if delta < 0 or delta % 4 or delta > 1020:
            raise AssertionError("literal is out of Thumb LDR range")
        struct.pack_into("<H", code, pos, 0x4800 | (reg << 8) | (delta // 4))

    ldr_literal(ldr_goku_pos, 0, literal_offsets[0])
    ldr_literal(ldr_hp_pos, 1, literal_offsets[1])
    ldr_literal(ldr_xp_pos, 1, literal_offsets[2])
    return bytes(code)


def main() -> None:
    if not BASE.exists():
        raise SystemExit(f"Missing base ROM: {BASE}")
    rom = bytearray(BASE.read_bytes())
    if len(rom) != SIZE:
        raise SystemExit(f"Unexpected base size: {len(rom)} (expected {SIZE})")

    # Safe NPC trampoline: existing type 0x51 (King Kai / Supreme Kai slot)
    # grants the four skills.  The BL invokes our max-stat reward before the
    # original NPC handler prologue is replayed.
    cave = bytearray.fromhex(
        "0fb4031c1969512910d10c48042101700e2141700f2181701421c17015210171"
    )
    # The prior sequence ends at 0x3c2320.  Replace its obsolete flag writes
    # with our routine call, then restore registers and execute original code.
    cave += thumb_bl(CAVE + len(cave), STAT_ROUTINE)
    cave += bytes.fromhex("c046c046c046c046")
    cave += bytes.fromhex("0fbc30b5041c00690d1c83b0034b1847")
    # Literals used by the trampoline.  The first LDR at 0x3c230a reads
    # the skill-slot base from 0x3c233c; the final LDR resumes Thumb code.
    cave += struct.pack("<I", 0x0300156C)
    cave += b"\0\0\0\0\0\0\0\0"
    cave += struct.pack("<I", 0x08017DAD)  # Thumb resume after original prologue
    rom[CAVE:CAVE + len(cave)] = cave
    routine = build_stat_routine(STAT_ROUTINE)
    rom[STAT_ROUTINE:STAT_ROUTINE + len(routine)] = routine
    # Hook the NPC handler to the trampoline.
    rom[0x17DA2:0x17DA2 + 10] = bytes.fromhex("014b1847000001233c08")

    # Four short lines and the same compact dialogue sequence format used by
    # the existing project.  ASCII avoids changing the game's font table.
    texts = (
        "Supreme Kai: I have awaited you, Goku.",
        "Supreme Kai: I grant you my ultimate blessing.",
        "Your level, HP, EP and all stats are now at maximum.",
        "Use this divine power with wisdom, Saiyan.",
    )
    for off, text, size in zip(DIALOGUE_STRINGS, texts, (0x74, 0x7C, 0x90, 0x70)):
        rom[off:off + size] = utf16_slot(text, size)

    # Dialogue command records; each record points to one of the four lines.
    for i, string_off in enumerate(DIALOGUE_STRINGS):
        record = bytearray(16)
        record[:4] = bytes.fromhex("01000557")
        record[4:8] = gba_ptr(string_off)
        if i < 3:
            record[8:12] = gba_ptr(DIALOGUE_TABLE + (i + 1) * 16)
        rom[DIALOGUE_TABLE + i * 16:DIALOGUE_TABLE + (i + 1) * 16] = record
    for field in NPC_DIALOGUE_FIELDS:
        rom[field:field + 4] = gba_ptr(DIALOGUE_TABLE)

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_bytes(rom)
    print(f"Wrote {OUT} ({len(rom)} bytes)")
    print("SHA-256:", hashlib.sha256(rom).hexdigest())


if __name__ == "__main__":
    main()
