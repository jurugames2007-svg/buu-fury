#!/usr/bin/env python3
"""Fail-closed integrity audit for the Buu's Fury SSJ4 ROM artifacts.

This checker deliberately does not claim that a ROM boots or that a feature works.
Those claims need a recorded emulator run.  It reports the exact diff, ROM geometry,
GBA header/logo/checksum, and validates a declared allowlist of changed ranges.
"""
from __future__ import annotations
import argparse, hashlib, sys
from pathlib import Path

GBA_LOGO = bytes.fromhex(
    "24ffae51699aa2213d84820a84e409ad11248b98c0817f21a352be199309ce20"
    "10464a4af82731ec58c7e83382e3cebf85f4df94ce4b09c194568ac01372a7fc"
    "9f844d73a3ca9a615897a327fc039876231dc7610304ae56bf38840040a70e6f"
    "9100000000000000000000000000000000000000000000000000000000000000"
)
ROM_8M = 8 * 1024 * 1024

def header_checksum(data: bytes) -> int:
    value = 0
    for byte in data[0xA0:0xBD]:
        value = (value - byte - 1) & 0xFF
    return value

def ranges(changed: list[int]):
    if not changed: return []
    out=[]; start=prev=changed[0]
    for p in changed[1:]:
        if p != prev + 1:
            out.append((start, prev + 1)); start=p
        prev=p
    out.append((start, prev + 1)); return out

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('base', type=Path); ap.add_argument('hack', type=Path)
    ap.add_argument('--allow', action='append', default=[], metavar='START:END',
                    help='permitted changed ROM-offset range, hexadecimal accepted')
    args=ap.parse_args()
    base=args.base.read_bytes(); hack=args.hack.read_bytes()
    ok=True
    for label,data in [('base',base),('hack',hack)]:
        print(f'{label}: size={len(data)} sha256={hashlib.sha256(data).hexdigest()}')
        if len(data) != ROM_8M:
            print(f'FAIL: {label} is not exactly 8 MiB (0x800000).'); ok=False
        if data[4:0xA0] != GBA_LOGO:
            print(f'FAIL: {label} has an invalid Nintendo logo.'); ok=False
        actual=header_checksum(data)
        if data[0xBD] != actual:
            print(f'FAIL: {label} header checksum is {data[0xBD]:02X}; computed {actual:02X}.'); ok=False
        title = data[0xA0:0xAC].rstrip(bytes([0])).decode("ascii", "replace")
        code = data[0xAC:0xB0].decode("ascii", "replace")
        print(f'  title={title!r} code={code!r} header_checksum={data[0xBD]:02X}')
    if len(base) != len(hack):
        print('FAIL: byte-level diff is undefined because ROM sizes differ.')
        return 1
    changed=[i for i,(a,b) in enumerate(zip(base,hack)) if a != b]
    blocks=ranges(changed)
    print(f'changed_bytes={len(changed)} changed_ranges={len(blocks)}')
    for start,end in blocks:
        print(f'  0x{start:06X}-0x{end-1:06X} ({end-start} bytes)')
    allowed=[]
    for item in args.allow:
        a,b=item.split(':',1); allowed.append((int(a,0),int(b,0)))
    if allowed:
        unexpected=[p for p in changed if not any(a <= p < b for a,b in allowed)]
        if unexpected:
            print(f'FAIL: {len(unexpected)} changed bytes fall outside declared allowlist; first=0x{unexpected[0]:X}')
            ok=False
    else:
        print('FAIL: no diff allowlist supplied (fail-closed).')
        ok=False
    return 0 if ok else 1
if __name__ == '__main__': sys.exit(main())
