#!/usr/bin/env python3
"""Static reconnaissance for Buu's Fury form-data candidates.

This is intentionally read-only.  It produces evidence to guide a future,
emulator-verified form patch; it is not a replacement for runtime xrefs.
"""
from pathlib import Path
import struct

ROM = Path("Dragon Ball Z - Buu's Fury (USA).gba")
FORM_NAME_POINTER = 0x6BEC0
FORM_RECORD_POINTERS = 0x6B6D70
SSJ3_NAME = 0x583F6
SSJ3_RECORD = 0x6AD510

def ptr(rom, off): return struct.unpack_from('<I', rom, off)[0]
def text(rom, off): return rom[off:off+64].decode('utf-16le', 'replace').split('\0')[0]
def main():
    rom=ROM.read_bytes()
    print('Form-name pointer table around SSJ3:')
    for i in range(-3,4):
        off=FORM_NAME_POINTER + i*4
        target=ptr(rom,off)-0x08000000
        print(f'  [{i:+d}] table=0x{off:06X} -> 0x{target:06X}: {text(rom,target)!r}')
    print('\nCandidate form-record pointer table around 0x6AD510:')
    hits=[]
    needle=struct.pack('<I',0x08000000+SSJ3_RECORD)
    pos=0
    while True:
        pos=rom.find(needle,pos)
        if pos<0: break
        hits.append(pos); pos+=1
    for hit in hits:
        print(f'  reference at 0x{hit:06X} (table index {(hit-FORM_RECORD_POINTERS)//4:+d})')
    print('\nCandidate record 0x6AD510 (first 32 bytes):')
    print('  ' + rom[SSJ3_RECORD:SSJ3_RECORD+32].hex())
    print('\nStatus: pointer tables are observed statically only. Do not edit a record or add a form until')
    print('a debugger proves which table index is selected during SSJ3 transformation and which fields are consumed.')
if __name__=='__main__': main()
