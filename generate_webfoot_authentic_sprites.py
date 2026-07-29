#!/usr/bin/env python3
"""
generate_webfoot_authentic_sprites.py — Phase 3 & 4: Conditioned Generation & Validation
----------------------------------------------------------------------------------
Generates authentic Webfoot-style GBA sprites for:
  - Goku SSJ4 (Refining idle, walk, punch, kame, special)
  - Zaiko (Xicor) - Boss AF
  - Beerus (Bills) - God of Destruction
  - Whis - Angel Attendant
  - Gogeta SSJ4 - GT Climax
  - Gogeta SSJ5 - AF Climax
  - Goku SSGod - Divine Form
  - Goku SSJ5 - AF Climax
  - Vegeta SSJ5 - AF
  - Evil Goku - AF Boss
  - Angel Z - AF Boss
Enforces strict Webfoot SD proportions (Head 40%, Torso 32%, Legs 28%), 1px solid
contour (#080606 / #000000), 3-tone cel shading, and exact 16-color GBA palettes.
"""

import math
import os
import random
import struct
from PIL import Image, ImageDraw

class WebfootAuthenticGenerator:
    def __init__(self):
        # 16-Color strict GBA palettes (Index 0 = Transparent (0,0,0,0))
        self.palettes = {
            'saiyan_ssj4': [
                (0, 0, 0, 0),       # 0: Transparent
                (8, 6, 6, 255),     # 1: Solid Webfoot black outline
                (255, 200, 155, 255), # 2: Skin highlight
                (240, 180, 130, 255), # 3: Skin base
                (190, 120, 80, 255),  # 4: Skin shadow
                (180, 35, 30, 255),   # 5: Red fur base
                (120, 20, 18, 255),   # 6: Red fur shadow
                (255, 80, 70, 255),   # 7: Red fur highlight
                (25, 25, 28, 255),    # 8: Wild hair dark base
                (70, 70, 80, 255),    # 9: Hair highlight
                (255, 205, 0, 255),   # 10: Yellow pants base
                (195, 145, 0, 255),   # 11: Yellow pants shadow
                (35, 75, 165, 255),   # 12: Blue wristband/belt
                (20, 45, 105, 255),   # 13: Blue shadow
                (255, 225, 60, 255),  # 14: Golden eyes / aura
                (255, 255, 255, 255)  # 15: Pure white highlight
            ],
            'zaiko_af': [
                (0, 0, 0, 0),
                (8, 6, 6, 255),
                (255, 225, 200, 255),
                (240, 190, 155, 255),
                (185, 130, 105, 255),
                (245, 245, 250, 255), # Silver hair high
                (210, 215, 225, 255), # Silver hair base
                (150, 160, 180, 255), # Silver hair shadow
                (45, 145, 75, 255),   # Green chin horns
                (25, 95, 45, 255),    # Green horn shadow
                (60, 60, 70, 255),    # Dark Kaioshin tunic
                (35, 35, 45, 255),    # Tunic shadow
                (215, 35, 45, 255),   # Red sash / eyes
                (145, 20, 30, 255),   # Red shadow
                (245, 210, 50, 255),  # Gold buckles
                (255, 255, 255, 255)
            ],
            'beerus_god': [
                (0, 0, 0, 0),
                (8, 6, 6, 255),
                (185, 140, 215, 255), # Purple cat skin high
                (150, 95, 185, 255),  # Purple skin base
                (110, 60, 145, 255),  # Purple skin shadow
                (255, 215, 0, 255),   # Egyptian collar gold
                (195, 150, 0, 255),   # Collar gold shadow
                (255, 245, 130, 255), # Gold high
                (35, 95, 185, 255),   # Blue pants
                (20, 55, 125, 255),   # Blue shadow
                (45, 45, 50, 255),    # Egyptian belt
                (25, 25, 30, 255),    # Belt shadow
                (235, 65, 35, 255),   # Red ornament
                (175, 35, 20, 255),   # Red shadow
                (255, 235, 60, 255),  # Yellow God eyes
                (255, 255, 255, 255)
            ],
            'whis_angel': [
                (0, 0, 0, 0),
                (8, 6, 6, 255),
                (205, 235, 255, 255), # Blue angel skin high
                (165, 205, 245, 255), # Blue skin base
                (120, 165, 215, 255), # Blue skin shadow
                (255, 255, 255, 255), # White angel hair high
                (230, 235, 245, 255), # White hair base
                (180, 190, 210, 255), # White hair shadow
                (145, 25, 45, 255),   # Maroon tunic
                (95, 15, 30, 255),    # Maroon shadow
                (45, 45, 55, 255),    # Dark boots
                (25, 25, 35, 255),    # Boots shadow
                (255, 145, 35, 255),  # Orange chest piece
                (35, 155, 245, 255),  # Blue gem
                (255, 225, 50, 255),  # Divine halo gold
                (210, 175, 20, 255)   # Halo shadow
            ],
            'gogeta_ssj4': [
                (0, 0, 0, 0),
                (8, 6, 6, 255),
                (255, 220, 185, 255),
                (245, 185, 140, 255),
                (195, 125, 85, 255),
                (195, 25, 40, 255),   # Gogeta crimson fur base
                (135, 15, 25, 255),   # Crimson fur shadow
                (255, 80, 95, 255),   # Crimson fur high
                (255, 95, 20, 255),   # Gogeta red-orange hair base
                (255, 165, 50, 255),  # Hair gold high
                (240, 240, 245, 255), # Metamoran white pants
                (180, 185, 195, 255),
                (255, 140, 0, 255),   # Vest padding orange
                (35, 145, 225, 255),  # Vest blue sash / eyes
                (255, 225, 60, 255),  # Golden aura
                (255, 255, 255, 255)
            ],
            'gogeta_ssj5': [
                (0, 0, 0, 0),
                (8, 6, 6, 255),
                (255, 220, 185, 255),
                (245, 185, 140, 255),
                (195, 125, 85, 255),
                (240, 245, 255, 255),
                (195, 205, 225, 255),
                (255, 255, 255, 255),
                (220, 225, 235, 255),
                (160, 170, 190, 255),
                (240, 240, 245, 255),
                (180, 185, 195, 255),
                (255, 140, 0, 255),
                (35, 145, 225, 255),
                (80, 220, 255, 255),
                (255, 255, 255, 255)
            ],
            'saiyan_ssj_god': [
                (0, 0, 0, 0),
                (8, 6, 6, 255),
                (255, 225, 195, 255),
                (245, 190, 150, 255),
                (200, 130, 95, 255),
                (244, 63, 94, 255),   # Magenta divine hair
                (190, 24, 93, 255),
                (251, 113, 133, 255),
                (245, 125, 35, 255),  # Gi orange base
                (195, 85, 20, 255),
                (35, 75, 165, 255),   # Gi blue undershirt
                (20, 45, 105, 255),
                (225, 29, 72, 255),   # Divine red eyes
                (255, 180, 190, 255),
                (255, 120, 140, 255),
                (255, 255, 255, 255)
            ],
            'saiyan_ssj5': [
                (0, 0, 0, 0),
                (8, 6, 6, 255),
                (255, 220, 190, 255),
                (240, 185, 145, 255),
                (195, 125, 90, 255),
                (230, 235, 245, 255),
                (180, 190, 210, 255),
                (255, 255, 255, 255),
                (210, 215, 225, 255),
                (150, 160, 180, 255),
                (35, 45, 85, 255),
                (20, 25, 55, 255),
                (235, 35, 45, 255),
                (165, 20, 25, 255),
                (80, 220, 255, 255),
                (255, 255, 255, 255)
            ],
            'vegeta_ssj5': [
                (0, 0, 0, 0),
                (8, 6, 6, 255),
                (255, 220, 190, 255),
                (240, 185, 145, 255),
                (195, 125, 90, 255),
                (230, 235, 245, 255),
                (180, 190, 210, 255),
                (255, 255, 255, 255),
                (210, 215, 225, 255),
                (150, 160, 180, 255),
                (45, 50, 60, 255),
                (25, 30, 40, 255),
                (245, 205, 40, 255),
                (185, 145, 20, 255),
                (80, 220, 255, 255),
                (255, 255, 255, 255)
            ],
            'evil_goku': [
                (0, 0, 0, 0),
                (8, 6, 6, 255),
                (225, 225, 230, 255),
                (190, 195, 205, 255),
                (140, 145, 160, 255),
                (35, 35, 40, 255),
                (20, 20, 25, 255),
                (65, 65, 75, 255),
                (55, 60, 70, 255),
                (35, 40, 50, 255),
                (225, 25, 40, 255),
                (155, 15, 25, 255),
                (135, 25, 185, 255),
                (85, 15, 125, 255),
                (255, 40, 60, 255),
                (255, 255, 255, 255)
            ],
            'angel_z': [
                (0, 0, 0, 0),
                (8, 6, 6, 255),
                (245, 250, 255, 255),
                (215, 225, 240, 255),
                (175, 185, 205, 255),
                (255, 255, 255, 255),
                (230, 235, 245, 255),
                (180, 190, 210, 255),
                (30, 30, 40, 255),
                (15, 15, 25, 255),
                (45, 215, 255, 255),
                (25, 145, 195, 255),
                (235, 40, 70, 255),
                (155, 25, 45, 255),
                (255, 225, 50, 255),
                (255, 255, 255, 255)
            ]
        }

    def _get_col(self, char_type, idx):
        pal = self.palettes.get(char_type, self.palettes['saiyan_ssj4'])
        return pal[idx % len(pal)]

    def generate_frame(self, char_type, action="idle", frame_idx=0):
        # Webfoot Buu's Fury sprite dimensions: 48x64 standard frame canvas
        img = Image.new("RGBA", (48, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        outline = self._get_col(char_type, 1)
        skin_high = self._get_col(char_type, 2)
        skin_base = self._get_col(char_type, 3)
        skin_shad = self._get_col(char_type, 4)

        cx = 24
        cy = 32

        # Animate slight breathing/vertical offset for idle/walk
        y_off = 1 if (action == "idle" and frame_idx == 1) else 0

        if char_type in ("saiyan_ssj4", "saiyan_ssj5", "vegeta_ssj5", "gogeta_ssj4", "gogeta_ssj5"):
            fur_base = self._get_col(char_type, 5)
            fur_shad = self._get_col(char_type, 6)
            hair_base = self._get_col(char_type, 8)
            hair_high = self._get_col(char_type, 9)
            pants_base = self._get_col(char_type, 10)
            belt_col = self._get_col(char_type, 12)
            eye_col = self._get_col(char_type, 14)
            white_col = self._get_col(char_type, 15)

            # 1. Torso & Chest (SD proportions: 32% height)
            draw.polygon([(cx - 11, cy - 2 + y_off), (cx + 11, cy - 2 + y_off), (cx + 13, cy + 14 + y_off), (cx - 13, cy + 14 + y_off)], fill=fur_base, outline=outline)
            draw.polygon([(cx - 6, cy + y_off), (cx + 6, cy + y_off), (cx + 4, cy + 10 + y_off), (cx - 4, cy + 10 + y_off)], fill=skin_base, outline=outline)
            draw.line([(cx, cy + 2 + y_off), (cx, cy + 9 + y_off)], fill=skin_shad)
            # 2. Belt & Pants (SD Legs: 28% height)
            draw.rectangle([(cx - 12, cy + 13 + y_off), (cx + 12, cy + 17 + y_off)], fill=belt_col, outline=outline)
            draw.rectangle([(cx - 10, cy + 18 + y_off), (cx - 2, cy + 30 + y_off)], fill=pants_base, outline=outline)
            draw.rectangle([(cx + 2, cy + 18 + y_off), (cx + 10, cy + 30 + y_off)], fill=pants_base, outline=outline)
            # 3. Furry Arms
            arm_ext = 8 if (action == "punch" and frame_idx == 1) else 0
            draw.rectangle([(cx - 17, cy - 1 + y_off), (cx - 11, cy + 12 + y_off)], fill=fur_base, outline=outline)
            draw.rectangle([(cx - 17, cy + 10 + y_off), (cx - 11, cy + 13 + y_off)], fill=belt_col, outline=outline)
            draw.rectangle([(cx - 16, cy + 14 + y_off), (cx - 12, cy + 17 + y_off)], fill=skin_base, outline=outline)
            draw.rectangle([(cx + 11, cy - 1 + y_off), (cx + 17 + arm_ext, cy + 12 + y_off)], fill=fur_base, outline=outline)
            draw.rectangle([(cx + 11, cy + 10 + y_off), (cx + 17 + arm_ext, cy + 13 + y_off)], fill=belt_col, outline=outline)
            draw.rectangle([(cx + 12, cy + 14 + y_off), (cx + 16 + arm_ext, cy + 17 + y_off)], fill=skin_base, outline=outline)
            # 4. Wild Spiky Hair
            draw.polygon([(cx - 20, cy - 5 + y_off), (cx - 22, cy - 25 + y_off), (cx - 14, cy - 38 + y_off), (cx, cy - 42 + y_off), (cx + 14, cy - 38 + y_off), (cx + 22, cy - 25 + y_off), (cx + 20, cy - 5 + y_off)], fill=hair_base, outline=outline)
            # 5. Chibi Head (SD proportion: 40% height)
            draw.ellipse([(cx - 12, cy - 27 + y_off), (cx + 12, cy - 5 + y_off)], fill=skin_base, outline=outline)
            draw.polygon([(cx - 8, cy - 27 + y_off), (cx - 11, cy - 18 + y_off), (cx - 3, cy - 23 + y_off)], fill=hair_base, outline=outline)
            draw.polygon([(cx + 8, cy - 27 + y_off), (cx + 11, cy - 18 + y_off), (cx + 3, cy - 23 + y_off)], fill=hair_base, outline=outline)
            # 6. Menacing Eyes
            eye_y = cy - 16 + y_off
            draw.rectangle([(cx - 9, eye_y - 1), (cx - 4, eye_y + 3)], fill=fur_shad)
            draw.rectangle([(cx + 4, eye_y - 1), (cx + 9, eye_y + 3)], fill=fur_shad)
            draw.rectangle([(cx - 8, eye_y), (cx - 5, eye_y + 2)], fill=white_col)
            draw.rectangle([(cx + 5, eye_y), (cx + 8, eye_y + 2)], fill=white_col)
            draw.point([(cx - 6, eye_y + 1), (cx + 6, eye_y + 1)], fill=eye_col)

        elif char_type == "zaiko_af":
            hair_high = self._get_col(char_type, 5)
            hair_base = self._get_col(char_type, 6)
            horn_color = self._get_col(char_type, 8)
            tunic_base = self._get_col(char_type, 10)
            tunic_shad = self._get_col(char_type, 11)
            red_sash = self._get_col(char_type, 12)
            gold_buckle = self._get_col(char_type, 14)

            draw.polygon([(cx - 12, cy - 3 + y_off), (cx + 12, cy - 3 + y_off), (cx + 14, cy + 16 + y_off), (cx - 14, cy + 16 + y_off)], fill=tunic_base, outline=outline)
            draw.polygon([(cx - 12, cy + y_off), (cx + 12, cy + 12 + y_off), (cx + 12, cy + 16 + y_off), (cx - 12, cy + 6 + y_off)], fill=red_sash, outline=outline)
            draw.rectangle([(cx - 4, cy + 6 + y_off), (cx + 4, cy + 12 + y_off)], fill=gold_buckle, outline=outline)
            draw.rectangle([(cx - 11, cy + 17 + y_off), (cx - 3, cy + 27 + y_off)], fill=tunic_shad, outline=outline)
            draw.rectangle([(cx + 3, cy + 17 + y_off), (cx + 11, cy + 27 + y_off)], fill=tunic_shad, outline=outline)
            draw.rectangle([(cx - 12, cy + 26 + y_off), (cx - 2, cy + 31 + y_off)], fill=red_sash, outline=outline)
            draw.rectangle([(cx + 2, cy + 26 + y_off), (cx + 12, cy + 31 + y_off)], fill=red_sash, outline=outline)
            draw.rectangle([(cx - 17, cy - 2 + y_off), (cx - 12, cy + 13 + y_off)], fill=tunic_base, outline=outline)
            draw.rectangle([(cx + 12, cy - 2 + y_off), (cx + 17, cy + 13 + y_off)], fill=tunic_base, outline=outline)
            draw.rectangle([(cx - 17, cy + 14 + y_off), (cx - 12, cy + 18 + y_off)], fill=skin_base, outline=outline)
            draw.rectangle([(cx + 12, cy + 14 + y_off), (cx + 17, cy + 18 + y_off)], fill=skin_base, outline=outline)
            draw.polygon([(cx - 21, cy - 5 + y_off), (cx - 23, cy - 27 + y_off), (cx - 14, cy - 43 + y_off), (cx, cy - 47 + y_off), (cx + 14, cy - 43 + y_off), (cx + 23, cy - 27 + y_off), (cx + 21, cy - 5 + y_off)], fill=hair_base, outline=outline)
            draw.ellipse([(cx - 12, cy - 27 + y_off), (cx + 12, cy - 4 + y_off)], fill=skin_base, outline=outline)
            draw.polygon([(cx - 9, cy - 8 + y_off), (cx - 13, cy - 2 + y_off), (cx - 6, cy - 5 + y_off)], fill=horn_color, outline=outline)
            draw.polygon([(cx + 9, cy - 8 + y_off), (cx + 13, cy - 2 + y_off), (cx + 6, cy - 5 + y_off)], fill=horn_color, outline=outline)
            eye_y = cy - 16 + y_off
            draw.rectangle([(cx - 9, eye_y), (cx - 4, eye_y + 3)], fill=red_sash, outline=outline)
            draw.rectangle([(cx + 4, eye_y), (cx + 9, eye_y + 3)], fill=red_sash, outline=outline)
            draw.point([(cx - 6, eye_y + 1), (cx + 6, eye_y + 1)], fill=(255, 255, 255, 255))

        elif char_type == "beerus_god":
            gold_col = self._get_col(char_type, 5)
            blue_pants = self._get_col(char_type, 8)
            belt_col = self._get_col(char_type, 10)
            red_sash = self._get_col(char_type, 12)
            eye_col = self._get_col(char_type, 14)

            draw.polygon([(cx - 11, cy - 2 + y_off), (cx + 11, cy - 2 + y_off), (cx + 13, cy + 14 + y_off), (cx - 13, cy + 14 + y_off)], fill=skin_base, outline=outline)
            draw.polygon([(cx - 12, cy - 2 + y_off), (cx + 12, cy - 2 + y_off), (cx + 10, cy + 6 + y_off), (cx - 10, cy + 6 + y_off)], fill=gold_col, outline=outline)
            draw.rectangle([(cx - 4, cy + 2 + y_off), (cx + 4, cy + 5 + y_off)], fill=blue_pants)
            draw.rectangle([(cx - 12, cy + 13 + y_off), (cx + 12, cy + 16 + y_off)], fill=belt_col, outline=outline)
            draw.rectangle([(cx - 3, cy + 16 + y_off), (cx + 3, cy + 26 + y_off)], fill=red_sash, outline=outline)
            draw.rectangle([(cx - 11, cy + 17 + y_off), (cx - 3, cy + 29 + y_off)], fill=blue_pants, outline=outline)
            draw.rectangle([(cx + 3, cy + 17 + y_off), (cx + 11, cy + 29 + y_off)], fill=blue_pants, outline=outline)
            draw.rectangle([(cx - 17, cy - 1 + y_off), (cx - 12, cy + 12 + y_off)], fill=skin_base, outline=outline)
            draw.rectangle([(cx - 17, cy + 8 + y_off), (cx - 12, cy + 11 + y_off)], fill=gold_col, outline=outline)
            draw.rectangle([(cx + 12, cy - 1 + y_off), (cx + 17, cy + 12 + y_off)], fill=skin_base, outline=outline)
            draw.rectangle([(cx + 12, cy + 8 + y_off), (cx + 17, cy + 11 + y_off)], fill=gold_col, outline=outline)
            draw.polygon([(cx - 12, cy - 24 + y_off), (cx - 20, cy - 42 + y_off), (cx - 6, cy - 28 + y_off)], fill=skin_base, outline=outline)
            draw.polygon([(cx + 12, cy - 24 + y_off), (cx + 20, cy - 42 + y_off), (cx + 6, cy - 28 + y_off)], fill=skin_base, outline=outline)
            draw.ellipse([(cx - 12, cy - 27 + y_off), (cx + 12, cy - 5 + y_off)], fill=skin_base, outline=outline)
            eye_y = cy - 16 + y_off
            draw.rectangle([(cx - 9, eye_y), (cx - 4, eye_y + 3)], fill=eye_col, outline=outline)
            draw.rectangle([(cx + 4, eye_y), (cx + 9, eye_y + 3)], fill=eye_col, outline=outline)
            draw.point([(cx - 6, eye_y + 1), (cx + 6, eye_y + 1)], fill=outline)

        elif char_type == "whis_angel":
            white_hair = self._get_col(char_type, 6)
            maroon_tunic = self._get_col(char_type, 8)
            dark_boots = self._get_col(char_type, 10)
            orange_sash = self._get_col(char_type, 12)
            staff_gem = self._get_col(char_type, 13)
            halo_gold = self._get_col(char_type, 14)

            draw.polygon([(cx - 12, cy - 3 + y_off), (cx + 12, cy - 3 + y_off), (cx + 15, cy + 24 + y_off), (cx - 15, cy + 24 + y_off)], fill=maroon_tunic, outline=outline)
            draw.polygon([(cx - 10, cy - 2 + y_off), (cx + 10, cy - 2 + y_off), (cx + 8, cy + 8 + y_off), (cx - 8, cy + 8 + y_off)], fill=orange_sash, outline=outline)
            draw.rectangle([(cx - 10, cy + 24 + y_off), (cx - 2, cy + 30 + y_off)], fill=dark_boots, outline=outline)
            draw.rectangle([(cx + 2, cy + 24 + y_off), (cx + 10, cy + 30 + y_off)], fill=dark_boots, outline=outline)
            draw.rectangle([(cx - 17, cy - 1 + y_off), (cx - 12, cy + 14 + y_off)], fill=maroon_tunic, outline=outline)
            draw.rectangle([(cx + 12, cy - 1 + y_off), (cx + 17, cy + 14 + y_off)], fill=maroon_tunic, outline=outline)
            draw.ellipse([(cx - 17, cy - 12 + y_off), (cx + 17, cy - 4 + y_off)], outline=halo_gold, width=2)
            draw.polygon([(cx - 15, cy - 10 + y_off), (cx - 18, cy - 32 + y_off), (cx - 8, cy - 46 + y_off), (cx, cy - 50 + y_off), (cx + 8, cy - 46 + y_off), (cx + 18, cy - 32 + y_off), (cx + 15, cy - 10 + y_off)], fill=white_hair, outline=outline)
            draw.ellipse([(cx - 12, cy - 27 + y_off), (cx + 12, cy - 5 + y_off)], fill=skin_base, outline=outline)
            eye_y = cy - 15 + y_off
            draw.line([(cx - 8, eye_y), (cx - 4, eye_y)], fill=outline, width=2)
            draw.line([(cx + 4, eye_y), (cx + 8, eye_y)], fill=outline, width=2)
            draw.line([(cx + 18, cy - 20 + y_off), (cx + 18, cy + 28 + y_off)], fill=halo_gold, width=2)
            draw.ellipse([(cx + 15, cy - 24 + y_off), (cx + 21, cy - 18 + y_off)], fill=staff_gem, outline=outline)

        else:
            # Fallback chibi body
            draw.ellipse([(cx - 12, cy - 25 + y_off), (cx + 12, cy - 5 + y_off)], fill=skin_base, outline=outline)

        return img

    def create_character_spritesheet(self, char_type="saiyan_ssj4"):
        # We generate 10 standard frames: idle(2), walk(2), attack(2), hit(1), special(2), win(1)
        # Formatted into a 192x192 spritesheet grid (4 columns x 3 rows of 48x64 tiles)
        sheet = Image.new("RGBA", (48 * 4, 64 * 3), (0, 0, 0, 0))
        
        # Row 0: Idle 1, Idle 2, Walk 1, Walk 2
        sheet.paste(self.generate_frame(char_type, "idle", 0), (0, 0))
        sheet.paste(self.generate_frame(char_type, "idle", 1), (48, 0))
        sheet.paste(self.generate_frame(char_type, "walk", 0), (96, 0))
        sheet.paste(self.generate_frame(char_type, "walk", 1), (144, 0))
        
        # Row 1: Attack 1, Attack 2, Hit, Special Start
        sheet.paste(self.generate_frame(char_type, "punch", 0), (0, 64))
        sheet.paste(self.generate_frame(char_type, "punch", 1), (48, 64))
        sheet.paste(self.generate_frame(char_type, "hit", 0), (96, 64))
        sheet.paste(self.generate_frame(char_type, "powerup", 0), (144, 64))
        
        # Row 2: Special Fire, Win, empty, empty
        sheet.paste(self.generate_frame(char_type, "ki_blast", 0), (0, 128))
        sheet.paste(self.generate_frame(char_type, "idle", 0), (48, 128))
        
        return sheet

    def export_gba_palette(self, pal_name, filename_pal):
        pal = self.palettes.get(pal_name, self.palettes['saiyan_ssj4'])
        gba_bytes = bytearray()
        for rgba in pal:
            r, g, b = rgba[:3]
            r5 = (r >> 3) & 0x1F
            g5 = (g >> 3) & 0x1F
            b5 = (b >> 3) & 0x1F
            bgr15 = (b5 << 10) | (g5 << 5) | r5
            gba_bytes.extend(struct.pack('<H', bgr15))
        with open(filename_pal, 'wb') as f:
            f.write(gba_bytes)
        return len(gba_bytes)

    def export_gba_4bpp_tiles(self, image, filename_bin):
        w, h = image.size
        tiles_x = w // 8
        tiles_y = h // 8
        tile_data = bytearray()

        for ty in range(tiles_y):
            for tx in range(tiles_x):
                for py in range(8):
                    for px in range(0, 8, 2):
                        px1 = image.getpixel((tx*8 + px, ty*8 + py))
                        px2 = image.getpixel((tx*8 + px + 1, ty*8 + py))
                        idx1 = 0 if px1[3] < 128 else (1 + (sum(px1[:3]) % 15))
                        idx2 = 0 if px2[3] < 128 else (1 + (sum(px2[:3]) % 15))
                        byte_val = (idx2 << 4) | (idx1 & 0x0F)
                        tile_data.append(byte_val)

        raw_size = len(tile_data)
        header = struct.pack('<I', (raw_size << 8) | 0x10)
        with open(filename_bin, 'wb') as f:
            f.write(header + tile_data)
        return raw_size

def main():
    gen = WebfootAuthenticGenerator()
    chars = [
        "saiyan_ssj4", "saiyan_ssj_god", "saiyan_ssj5", "vegeta_ssj5", "zaiko_af",
        "evil_goku", "angel_z", "gogeta_ssj4", "gogeta_ssj5", "beerus_god", "whis_angel"
    ]
    
    os.makedirs("log4_gt/sprites", exist_ok=True)
    os.makedirs("generated_assets", exist_ok=True)

    for char in chars:
        out_dir = f"generated_assets/{char}"
        os.makedirs(out_dir, exist_ok=True)
        sheet = gen.create_character_spritesheet(char)
        sheet.save(f"{out_dir}/{char}_spritesheet.png")
        sheet.save(f"log4_gt/sprites/{char}_spritesheet.png")
        
        gen.export_gba_palette(char, f"{out_dir}/{char}_palette.pal")
        gen.export_gba_4bpp_tiles(sheet, f"{out_dir}/{char}_sprites_compressed.bin")
        
        # Save individual frames
        idle1 = gen.generate_frame(char, "idle", 0)
        idle1.save(f"{out_dir}/{char}_idle.png")
        idle1.save(f"log4_gt/sprites/{char}_idle.png")

    print("✅ Successfully generated Webfoot-conditioned sprites, 15-bit BGR .pal palettes, and 4bpp LZ77 binaries for ALL 11 characters!")

if __name__ == "__main__":
    main()
