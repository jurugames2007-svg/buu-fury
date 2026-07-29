#!/usr/bin/env python3
"""
build_gba_maps_100percent.py — Custom GBA Map Engine & Compiler (Pillar 1 of 100%)
----------------------------------------------------------------------------------
Generates complete GBA map packages (Tilemaps, Collision Matrices, Map Headers,
and visual PNG renders) for 5 custom explorable maps:
  1) map_beerus_planet         : Beerus's Temple & Whis's Training Courtyard (64x64 tiles)
  2) map_gohan_forest_439_deep : Deep Western Forest of East District 439 (64x64 tiles)
  3) map_crater_zero           : Crater Zero GT Climax Arena (32x32 tiles)
  4) map_imecka                : Planet Imecka Grand Tour Marketplace (64x64 tiles)
  5) map_tuffle_planet         : New Planet Plant / Tuffle Planet Arena (64x64 tiles)
"""

import os
import json
import struct
from PIL import Image, ImageDraw

class GBAMapCompiler:
    def __init__(self, output_dir="log4_gt/maps"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_map(self, map_id, name, width_tiles, height_tiles, theme, bg_col, wall_col, floor_col, portal_col):
        # 1. Generate GBA Background Tilemap (.bin)
        # In GBA BG tilemaps, each entry is 2 bytes: tile index (10 bits), flip (2 bits), palette (4 bits)
        tilemap_bytes = bytearray()
        collision_bytes = bytearray()
        
        # We also render a visual PNG image (each tile is 8x8 pixels)
        img_w = width_tiles * 8
        img_h = height_tiles * 8
        img = Image.new('RGB', (img_w, img_h), bg_col)
        draw = ImageDraw.Draw(img)

        for ty in range(height_tiles):
            for tx in range(width_tiles):
                is_border = (tx == 0 or ty == 0 or tx == width_tiles - 1 or ty == height_tiles - 1)
                is_portal = (ty == height_tiles - 1 and (width_tiles//2 - 2 <= tx <= width_tiles//2 + 2))
                is_pillar_or_tree = False
                
                # Add obstacles/pillars depending on theme
                if not is_border and not is_portal:
                    if theme == "divine_temple" and (tx % 8 == 0 and ty % 8 == 0 and ty > 10):
                        is_pillar_or_tree = True
                    elif theme == "dense_forest" and ((tx * ty) % 11 == 0 and ty < height_tiles - 10):
                        is_pillar_or_tree = True
                    elif theme == "crater_wasteland" and ((tx + ty) % 9 == 0 and ty > 5):
                        is_pillar_or_tree = True

                # Tile & Collision assignment
                if is_portal:
                    tile_idx = 0x0100 # Portal tile
                    collision = 0x02  # 0x02 = Portal / Trigger zone
                    col_rgb = portal_col
                elif is_border or is_pillar_or_tree:
                    tile_idx = 0x0001 # Solid wall/tree/pillar tile
                    collision = 0x01  # 0x01 = Solid obstacle
                    col_rgb = wall_col
                else:
                    tile_idx = 0x0000 # Walkable floor tile
                    collision = 0x00  # 0x00 = Walkable floor
                    col_rgb = floor_col

                # Pack 16-bit GBA tilemap word (tile_idx | palette_idx << 12)
                word = tile_idx | (1 << 12)
                tilemap_bytes.extend(struct.pack('<H', word))
                collision_bytes.append(collision)

                # Draw to visual PNG preview
                x0, y0 = tx * 8, ty * 8
                draw.rectangle([(x0, y0), (x0 + 7, y0 + 7)], fill=col_rgb)
                if is_pillar_or_tree:
                    draw.rectangle([(x0 + 2, y0 + 2), (x0 + 5, y0 + 5)], fill=bg_col)
                elif is_portal:
                    draw.ellipse([(x0 + 1, y0 + 1), (x0 + 6, y0 + 6)], fill=(255, 255, 255))

        # Save files
        base_path = os.path.join(self.output_dir, map_id)
        with open(base_path + ".bin", "wb") as f:
            f.write(tilemap_bytes)
        with open(base_path + "_collision.bin", "wb") as f:
            f.write(collision_bytes)
        img.save(base_path + "_preview.png")

        # Create GBA Map Header Struct (.json)
        header_data = {
            "map_id": map_id,
            "name": name,
            "dimensions": {"width_tiles": width_tiles, "height_tiles": height_tiles},
            "tileset_offset": "0x08A00000",
            "palette_offset": "0x08A10000",
            "tilemap_file": f"{map_id}.bin",
            "collision_file": f"{map_id}_collision.bin",
            "preview_image": f"{map_id}_preview.png",
            "music_track_id": 0x8A if theme == "divine_temple" else (0x8C if theme == "dense_forest" else 0x8B),
            "npcs": [
                {"name": "Whis", "type": 82, "pos_x": width_tiles // 2, "pos_y": 15} if theme == "divine_temple" else
                {"name": "Zaiko (Boss)", "type": 95, "pos_x": width_tiles // 2, "pos_y": height_tiles // 3} if theme == "dense_forest" else
                {"name": "Omega Shenron", "type": 96, "pos_x": width_tiles // 2, "pos_y": height_tiles // 2}
            ],
            "triggers": [
                {"type": "portal", "target_map": "Snakeway", "zone_y": height_tiles - 1}
            ]
        }
        with open(base_path + "_header.json", "w", encoding="utf-8") as f:
            json.dump(header_data, f, indent=2)

        print(f"✅ Generated 100% GBA Map Package for {name} ({width_tiles}x{height_tiles} tiles)")
        return len(tilemap_bytes)

def main():
    compiler = GBAMapCompiler()
    
    # 1. Beerus's Planet (Divine Temple & Whis Training Courtyard)
    compiler.generate_map("map_beerus_planet", "Planeta de Bills (Other World)", 64, 64, 
                          "divine_temple", (40, 10, 55), (255, 215, 0), (130, 95, 185), (80, 200, 255))
    
    # 2. Deep East District 439 Forest (Zaiko's Lair outside Gohan's house)
    compiler.generate_map("map_gohan_forest_439_deep", "Bosque Oeste Distrito 439 (Zaiko Boss Map)", 64, 64,
                          "dense_forest", (15, 35, 20), (35, 75, 40), (45, 95, 55), (255, 215, 50))

    # 3. Crater Zero (Omega Shenron GT Climax Arena)
    compiler.generate_map("map_crater_zero", "Cráter Cero (GT Shadow Dragons Climax)", 32, 32,
                          "crater_wasteland", (30, 25, 35), (80, 70, 90), (120, 110, 130), (255, 100, 50))

    # 4. Planet Imecka (Grand Tour Marketplace)
    compiler.generate_map("map_imecka", "Planeta Imecka (Grand Tour)", 64, 64,
                          "divine_temple", (25, 45, 65), (100, 150, 180), (180, 210, 230), (255, 225, 60))

    # 5. New Planet Plant / Tuffle Planet
    compiler.generate_map("map_tuffle_planet", "Nuevo Planeta Plant (Baby Saga Arena)", 64, 64,
                          "crater_wasteland", (50, 20, 25), (150, 50, 60), (200, 90, 100), (255, 215, 0))

    print("\n✅ All 5 Custom GBA Explorable Maps compiled successfully!")

if __name__ == "__main__":
    main()
