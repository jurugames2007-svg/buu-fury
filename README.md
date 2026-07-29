# The Legacy of Goku 4 — Dragon Ball GT DLC

ROM expansion for **Dragon Ball Z: Buu's Fury (USA)** that adds a **Dragon Ball GT** path with **Super Saiyan 4** as a **separate form slot** (SS3 stays 100% original).

## Play this

| File | Description |
|------|-------------|
| [`log4_gt/ROM/LegacyOfGoku4_GT_DLC.gba`](log4_gt/ROM/LegacyOfGoku4_GT_DLC.gba) | **Main ROM (16 MB)** |
| [`LegacyOfGoku4_GT_DLC.zip`](LegacyOfGoku4_GT_DLC.zip) | Full package (ROM + assets + GDD) |
| `Dragon Ball Z - Buu's Fury (USA).gba` | Clean base ROM (vanilla) |

### How to start

1. Open **mGBA** (or another GBA emulator)
2. Load `log4_gt/ROM/LegacyOfGoku4_GT_DLC.gba`
3. **New Game** → reach **Snake Way** (Other World)
4. Talk to the extra **East Kai** NPC (King Kai is still there, unchanged)
5. You unlock the **SSJ4** path (form ID 1) and starter skills
6. **SS3 remains fully original** (name, skill, palette, struct)

### Form ladder

**SS4 (form 1) > SS3 (form 5, original) > SS1 (form 3) > Base (form 0)**

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

## Package layout (`log4_gt/`)

```
log4_gt/
├── ROM/LegacyOfGoku4_GT_DLC.gba
├── spritesheets/Goku_SSJ4_GT_Sheet.png
├── portraits/   (SS4 > SS3 > SS1 > Base hierarchy)
├── ui_icons/    (SS4, 10x Kamehameha, Dragon Fist, East Kai, GT saga)
├── datasheets/  GDD_GT_DLC.json, DESIGN.md
├── dialogues/   east_kai_snakeway.txt
├── tests/       CHECKLIST.md
└── docs/REPORT.txt
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
