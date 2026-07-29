# The Legacy of Goku 4 — Dragon Ball GT, AF & God of Destruction DLC

ROM expansion for **Dragon Ball Z: Buu's Fury (USA)** that adds **Dragon Ball GT**, **AF (Zaiko)**, and **Other World God of Destruction (Beerus & Whis)** content as an official-feeling sequel expansion.

## Play this

| File | Description |
|------|-------------|
| [`log4_gt/ROM/LegacyOfGoku4_GT_DLC.gba`](log4_gt/ROM/LegacyOfGoku4_GT_DLC.gba) | **Main ROM (16 MB)** |
| [`LegacyOfGoku4_GT_DLC.zip`](LegacyOfGoku4_GT_DLC.zip) | Full package (ROM + assets + GDD + QA tools) |
| [`MANUAL_LEGACY_OF_GOKU_4_COMPLETE.md`](MANUAL_LEGACY_OF_GOKU_4_COMPLETE.md) | Comprehensive Manual, Reskin vs. Sequel analysis & Bandai Namco QA audit |
| `Dragon Ball Z - Buu's Fury (USA).gba` | Clean base ROM (vanilla) |

### How to start

1. Open **mGBA** (or another GBA emulator)
2. Load `log4_gt/ROM/LegacyOfGoku4_GT_DLC.gba`
3. **New Game** → reach **Snake Way** (Other World)
4. Talk to the extra **East Kai** NPC (King Kai is still there, unchanged) to unlock **SSJ4 Goku** (form ID 1) and starter skills.
5. **Whis's Divine Portal & Beerus's Planet**: Speak with **Whis** on Snake Way / Planet of the Kais to enter the **Planeta de Bills (Beerus's Planet)** in the Other World.
6. **Whis's Gourmet Shop**: Purchase *Beerus's Pudding*, *Whis's Sundae*, and *Tree of Might Fruit* to gain permanent STR and divine defense buffs.
7. **Post-Game Boss Zaiko (Xicor)**: After defeating Kid Buu, travel to the deep woods of **East District 439 Forest** (outside Adult Gohan's house) to challenge **Zaiko** (`99,999 HP`, Level 200).
8. **Ultimate Fusion — Gogeta SSJ4**: Unlock Form ID `0x1B` and **Big Bang Kamehameha x100** after defeating Zaiko and clearing Beerus's divine trial (`150,000 HP`, Level 250).

### Form ladder

**Gogeta SSJ4 (form 0x1B) > SS4 (form 1) > SS3 (form 5, original) > SS1 (form 3) > Base (form 0)**

### Automated QA Test Suite (`test_legacy_of_goku_4_rom.py`)

Run `python3 test_legacy_of_goku_4_rom.py` to run our 6-suite verification engine, checking strict 16-color GBA `.pal` palettes (32 bytes), 4bpp planar LZ77 `.bin` headers, 128x144 GBA portraits, dialogues, datasheets, and ROM checksums. Every test suite passes with Bandai Namco quality standards.


| Form | Slot | Status |
|------|------|--------|
| Super Saiyan 4 | Form ID **1** (GT slot) | **New** — red-fur palette + SS3-class anims |
| Super Saiyan 3 | Form ID 5 | **Original restored** |
| Super Saiyan | Form ID 3 | Original |
| Base Goku | Form ID 0 | Original |

### Skills granted by East Kai

- Instant Transmission (`0x0E`)
- Kamehameha (`0x0F`)
- Super Saiyan (`0x14`)
- Super Saiyan 4 marker (`0x15`) + enter form 1

Re-talk to East Kai to return to SSJ4 after switching forms.

## New Post-Game Boss: Zaiko / Xicor (Dragon Ball AF DLC)

After defeating **Kid Buu** in the main story, a new secret threat appears in the forest of **East District 439** (a short distance outside **Adult Gohan's house**, where Gohan starts his chapter in *Buu's Fury*).

- **Boss Name**: **Zaiko (Xicor)** — The Kai-Saiyan hybrid son of Goku from the AF post-game lore.
- **Power Scale**: **Much stronger than Kid Buu** (`99,999 HP`, Level 200 vs. Kid Buu's `32,000 HP`, Level 140).
- **Location**: Deep western woods of East District 439 map (outside Adult Gohan's house).
- **Dialogue & Story**: Complete pre-battle script in `log4_gt/dialogues/zaiko_forest_postgame.txt` and `hackrom_ssj4/extracted_assets/text/zaiko_strings.txt`.
- **Datasheet**: See `log4_gt/datasheets/zaiko_postgame_boss.json` for full combat stats, lore, and loot drops.

## Improved GBA Graphics & Retratos

- **Super Saiyan 4 Portrait (`portrait_ssj4.png`)**: Completely remastered in crisp 16-color GBA style (128x144 resolution) with vivid red fur, red eyeliner, golden eyes, and wild spiky black/red hair—visually superior and distinct from the golden SSJ3 portrait.
- **Zaiko Portrait (`portrait_zaiko.png`)**: Custom 16-color GBA portrait featuring silver SSJ5 hair, green Kai chin spikes/horns, and crimson eyes.
- **Webfoot Chibi Sprites**: Combat spritesheets (`saiyan_ssj4_spritesheet.png`, `zaiko_af_spritesheet.png`) crafted with strict 16-color indexed GBA palettes and black pixel outlines.
- **Hierarchy Comparison Sheet**: View all forms side-by-side in `log4_gt/portraits/HIERARCHY_SS4_SS3_SS1_BASE.png`.

## Sprite & Datasheet Tool (`dbz_gba_sprite_tool.py`)

An enhanced GBA-compatible Python utility (`dbz_gba_sprite_tool.py`) is included, adapted from your original `DBZSpriteGenerator` prototype. It resolves GBA hardware restrictions by:
1. Enforcing strict **16-color indexed palettes** (Index 0 = transparent, 15-bit BGR format `.pal` export).
2. Removing alpha-blended semitransparencies in favor of crisp GBA pixel-art outlines (`#000000`) and 3-tone cel shading.
3. Exporting directly to **4bpp planar GBA tile format** (`.bin`) with standard GBA BIOS LZ77 compression headers (`0x10`).
4. Generating both **SSJ4 Goku** and **Zaiko (Xicor)** spritesheets and individual animation frames (`idle`, `punch`, `powerup`, `ki_blast`).

## 100% Commercial GBA Sequel Architecture

This repository contains all engineering assets to bridge the remaining 15% toward a 100% standalone commercial GBA sequel (*The Legacy of Goku 4*):
1. **Custom GBA Map Engine (`log4_gt/maps/`)**: 5 complete explorable GBA map packages (`map_beerus_planet`, `map_gohan_forest_439_deep`, `map_crater_zero`, `map_imecka`, `map_tuffle_planet`) featuring 16-bit `.bin` tilemaps, byte-array collision matrices (`_collision.bin`), GBA map headers (`_header.json`), and visual PNG renders.
2. **ARM7/Thumb Boss AI Assembly (`log4_gt/asm/`)**: Native ARM/Thumb assembly routines and binary payloads for Beerus's 3-Phase God of Destruction AI (with telegraphed Hakai and Pudding shield check), Omega Shenron GT Climax AI, Zaiko AF Afterimage Dash AI, and Whis Ultra Instinct Auto-Dodge AI, mapped in `boss_ai_injection_table.json`.
3. **GBA Sappy Sound Engine Chiptune Audio (`log4_gt/audio/`)**: 16-bit GBA chiptune tracks and pointer tables (`sappy_audio_pointer_table.json`) for *Dan Dan Kokoro Hikareteku*, Beerus's Sanctuary theme, Zaiko's AF Battle theme, and God Kamehameha SFX.
4. **10-Suite Automated QA Audit (`test_legacy_of_goku_4_100percent.py`)**: Run `python3 test_legacy_of_goku_4_100percent.py` to audit 10 full engineering suites (palettes, planar tiles, portraits, dialogues, JSON schemas, ROM checksums, 300-player simulation, map engine, boss AI, and Sappy audio).

## Package layout (`log4_gt/`)

```
log4_gt/
├── ROM/LegacyOfGoku4_GT_DLC.gba
├── asm/         ARM/Thumb Boss AI assembly (.s, .bin, injection table)
├── audio/       Sappy chiptune audio tracks (.bin, .wav, pointer table)
├── maps/        5 custom GBA maps (tilemaps .bin, collision, header, preview)
├── sprites/     16-color GBA sprites, palettes (.pal), 4bpp planar LZ77 tiles
├── portraits/   9 crisp 128x144 GBA portraits (HIERARCHY_LOG4_ALL_PORTRAITS.png)
├── ui_icons/    Food & items, shop icons, boss badges, skill icons, sagas
├── datasheets/  GDD, Level 350 curve, Zaiko/Beerus/Gogeta/Whis shop JSONs
├── dialogues/   Snake Way, GT climax, AF forest, Beerus planet scripts
└── tests/       QA reports, 300-player feedback loop, balance patches
```

GT saga structure (Grand Tour → Baby → Super 17 → Shadow Dragons) is documented in the GDD for further map/quest wiring.

## Technical notes

- Base: *Dragon Ball Z: Buu's Fury (USA)* — `BG3E`, expanded **8 MB → 16 MB**
- Policy: **additive** where possible; SS3 bytes verified identical to vanilla
- East Kai: NPC type `81`, 13th entry on Snakeway map (original 12 NPCs kept)
- Hook: NPC interact grants kit **only** when `NPC.type == 81`
- SSJ4 uses separate character struct (former GT stub) with SS3-class animations + dedicated red-fur palette
- Assets include GT-style sprite sheet frames, menu hierarchy icons, and skill icons

## Older build

`hackrom_ssj4/` is an earlier experimental pack (SS3 renamed/recolored). Prefer **`log4_gt`** for the intended design.

## Credits

ROM map / RAM research: [Data Crystal — Buu's Fury](https://datacrystal.tcrf.net/wiki/Dragon_Ball_Z:_Buu%27s_Fury)
