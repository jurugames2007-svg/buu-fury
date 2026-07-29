#!/usr/bin/env python3
"""
dbz_gba_sprite_tool.py — Enhanced GBA-Compatible DBZ Sprite & Datasheet Generator
----------------------------------------------------------------------------------
Supports 16-color GBA indexed palettes, Webfoot 'Buu's Fury' pixel-art style,
<<<<<<< HEAD
4bpp planar tile conversion (.bin), and LZ77 compression simulation for:
  - 'saiyan_ssj4': Goku Super Saiyan 4 (red fur, black/red spiky hair, golden eyes)
  - 'saiyan_ssj_god': Goku Super Saiyan God (crimson/magenta divine hair, red eyes, slender aura)
  - 'zaiko_af': Zaiko / Xicor (post-game boss in Gohan's forest, silver hair, green horns)
  - 'gogeta_ssj4': Gogeta Super Saiyan 4 (crimson fur, Metamoran vest, crimson/gold hair)
  - 'beerus_god': Beerus / Bills (God of Destruction, purple cat skin, Egyptian gold collar)
  - 'whis_angel': Whis (Angel attendant, blue skin, white angel hair, dark red/black robes)
=======
4bpp planar tile conversion (.bin), and LZ77 compression simulation for 11 forms:
  - 'saiyan_ssj4': Goku Super Saiyan 4
  - 'saiyan_ssj_god': Goku Super Saiyan God
  - 'saiyan_ssj5': Goku Super Saiyan 5 (silver fur, silver spiky hair, lightning aura)
  - 'vegeta_ssj5': Vegeta Super Saiyan 5 (silver fur, royal battle armor, silver hair)
  - 'zaiko_af': Zaiko / Xicor (AF secret boss)
  - 'evil_goku': Evil Goku (inverted black/grey gi, pale skin, red eyes)
  - 'angel_z': Angel Z (white corrupted robes, dark horizontal halo)
  - 'gogeta_ssj4': Gogeta Super Saiyan 4
  - 'gogeta_ssj5': Gogeta Super Saiyan 5 (silver fur, Metamoran vest, 100x Big Bang Kamehameha)
  - 'beerus_god': Beerus / Bills
  - 'whis_angel': Whis
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
"""

import math
import os
import random
import struct
from PIL import Image, ImageDraw

class DBZGBASpriteGenerator:
    def __init__(self, sprite_width=48, sprite_height=64):
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        
        self.palettes = {
            'saiyan_ssj4': [
<<<<<<< HEAD
                (0, 0, 0),         # 0: Transparent background
                (0, 0, 0),      # 1: Black outline
                (255, 215, 175),   # 2: Skin highlight
                (240, 180, 130),   # 3: Skin base
                (190, 120, 80),    # 4: Skin shadow
                (235, 40, 40),     # 5: SSJ4 Red fur base
                (170, 20, 20),     # 6: SSJ4 Red fur shadow
                (255, 95, 95),     # 7: SSJ4 Red fur highlight
                (25, 25, 30),      # 8: Hair black base
                (70, 70, 80),      # 9: Hair highlight
                (255, 205, 0),     # 10: Pants yellow base
                (195, 145, 0),     # 11: Pants yellow shadow
                (35, 75, 165),     # 12: Belt/Wristband blue
                (20, 45, 105),     # 13: Belt blue shadow
                (255, 225, 60),    # 14: SSJ4 Golden eyes / Aura
                (255, 255, 255)    # 15: Eye white / highlight
            ],
            'saiyan_ssj_god': [
                (0, 0, 0),         # 0: Transparent
                (0, 0, 0),      # 1: Black outline
                (255, 225, 195),   # 2: Skin highlight
                (245, 190, 150),   # 3: Skin base
                (200, 130, 95),    # 4: Skin shadow
                (244, 63, 94),     # 5: SSGod Crimson-Magenta divine hair base
                (190, 24, 93),     # 6: SSGod Crimson hair shadow
                (251, 113, 133),   # 7: SSGod Magenta hair highlight
                (245, 125, 35),    # 8: Goku Gi orange base
                (195, 85, 20),     # 9: Gi orange shadow
                (35, 75, 165),     # 10: Gi blue undershirt/belt
                (20, 45, 105),     # 11: Gi blue shadow
                (225, 29, 72),     # 12: Divine red eyes / God Ki pulse
                (255, 180, 190),   # 13: Divine aura inner magenta highlight
                (255, 120, 140),   # 14: Divine aura outer red glow
                (255, 255, 255)    # 15: Pure white highlight
            ],
            'zaiko_af': [
                (0, 0, 0),         # 0: Transparent background
                (0, 0, 0),      # 1: Black outline
                (255, 225, 200),   # 2: Skin highlight
                (240, 190, 155),   # 3: Skin base
                (185, 130, 105),   # 4: Skin shadow
                (245, 245, 250),   # 5: Silver/White hair highlight
                (210, 215, 225),   # 6: Silver hair base
                (150, 160, 180),   # 7: Silver hair shadow
                (45, 145, 75),     # 8: Green chin spikes / horns
                (25, 95, 45),      # 9: Green horn shadow
                (60, 60, 70),      # 10: Kaioshin tunic dark gray
                (35, 35, 45),      # 11: Tunic shadow
                (215, 35, 45),     # 12: Red sash / eyes
                (145, 20, 30),     # 13: Red sash shadow
                (245, 210, 50),    # 14: Kaioshin gold buckles
                (255, 255, 255)    # 15: Pure white highlight
            ],
            'gogeta_ssj4': [
                (0, 0, 0),         # 0: Transparent background
                (0, 0, 0),      # 1: Black outline
                (255, 220, 185),   # 2: Skin highlight
                (245, 185, 140),   # 3: Skin base
                (195, 125, 85),    # 4: Skin shadow
                (195, 25, 40),     # 5: Gogeta crimson red fur base
                (135, 15, 25),     # 6: Crimson fur shadow
                (255, 80, 95),     # 7: Crimson fur highlight
                (255, 95, 20),     # 8: Gogeta red-orange hair base
                (255, 165, 50),    # 9: Hair gold-orange highlight
                (240, 240, 245),   # 10: Metamoran pants white base
                (180, 185, 195),   # 11: Pants white shadow
                (255, 140, 0),     # 12: Metamoran vest padding orange
                (35, 145, 225),    # 13: Metamoran vest blue sash / eyes
                (255, 225, 60),    # 14: Gogeta golden aura
                (255, 255, 255)    # 15: Pure white
            ],
            'beerus_god': [
                (0, 0, 0),         # 0: Transparent
                (0, 0, 0),      # 1: Black outline
                (185, 140, 215),   # 2: Purple cat skin highlight
                (150, 95, 185),    # 3: Purple cat skin base
                (110, 60, 145),    # 4: Purple cat skin shadow
                (255, 215, 0),     # 5: Egyptian collar gold base
                (195, 150, 0),     # 6: Collar gold shadow
                (255, 245, 130),   # 7: Collar gold highlight
                (35, 95, 185),     # 8: Egyptian collar blue gem / pants
                (20, 55, 125),     # 9: Blue pants shadow
                (45, 45, 50),      # 10: Dark Egyptian belt
                (25, 25, 30),      # 11: Belt shadow
                (235, 65, 35),     # 12: Egyptian red sash/ornament
                (175, 35, 20),     # 13: Red sash shadow
                (255, 235, 60),    # 14: Beerus yellow God eyes / Aura
                (255, 255, 255)    # 15: Eye white
            ],
            'whis_angel': [
                (0, 0, 0),         # 0: Transparent
                (0, 0, 0),      # 1: Black outline
                (205, 235, 255),   # 2: Blue angel skin highlight
                (165, 205, 245),   # 3: Blue angel skin base
                (120, 165, 215),   # 4: Blue angel skin shadow
                (255, 255, 255),   # 5: White angel hair highlight / robes
                (230, 235, 245),   # 6: White angel hair base
                (180, 190, 210),   # 7: White angel hair shadow
                (145, 25, 45),     # 8: Whis dark red/maroon tunic base
                (95, 15, 30),      # 9: Maroon tunic shadow
                (45, 45, 55),      # 10: Dark boots/underrobe
                (25, 25, 35),      # 11: Boots shadow
                (255, 145, 35),    # 12: Orange chest ornament / sash
                (35, 155, 245),    # 13: Blue staff gem / ornament
                (255, 225, 50),    # 14: Divine angel halo gold
                (210, 175, 20)     # 15: Halo shadow
=======
                (0, 0, 0), (0, 0, 0), (255, 215, 175), (240, 180, 130), (190, 120, 80),
                (235, 40, 40), (170, 20, 20), (255, 95, 95), (25, 25, 30), (70, 70, 80),
                (255, 205, 0), (195, 145, 0), (35, 75, 165), (20, 45, 105), (255, 225, 60), (255, 255, 255)
            ],
            'saiyan_ssj_god': [
                (0, 0, 0), (0, 0, 0), (255, 225, 195), (245, 190, 150), (200, 130, 95),
                (244, 63, 94), (190, 24, 93), (251, 113, 133), (245, 125, 35), (195, 85, 20),
                (35, 75, 165), (20, 45, 105), (225, 29, 72), (255, 180, 190), (255, 120, 140), (255, 255, 255)
            ],
            'saiyan_ssj5': [
                (0, 0, 0), (0, 0, 0), (255, 220, 190), (240, 185, 145), (195, 125, 90),
                (230, 235, 245), (180, 190, 210), (255, 255, 255), (210, 215, 225), (150, 160, 180),
                (35, 45, 85), (20, 25, 55), (235, 35, 45), (165, 20, 25), (80, 220, 255), (255, 255, 255)
            ],
            'vegeta_ssj5': [
                (0, 0, 0), (0, 0, 0), (255, 220, 190), (240, 185, 145), (195, 125, 90),
                (230, 235, 245), (180, 190, 210), (255, 255, 255), (210, 215, 225), (150, 160, 180),
                (45, 50, 60), (25, 30, 40), (245, 205, 40), (185, 145, 20), (80, 220, 255), (255, 255, 255)
            ],
            'zaiko_af': [
                (0, 0, 0), (0, 0, 0), (255, 225, 200), (240, 190, 155), (185, 130, 105),
                (245, 245, 250), (210, 215, 225), (150, 160, 180), (45, 145, 75), (25, 95, 45),
                (60, 60, 70), (35, 35, 45), (215, 35, 45), (145, 20, 30), (245, 210, 50), (255, 255, 255)
            ],
            'evil_goku': [
                (0, 0, 0), (0, 0, 0), (225, 225, 230), (190, 195, 205), (140, 145, 160),
                (35, 35, 40), (20, 20, 25), (65, 65, 75), (55, 60, 70), (35, 40, 50),
                (225, 25, 40), (155, 15, 25), (135, 25, 185), (85, 15, 125), (255, 40, 60), (255, 255, 255)
            ],
            'angel_z': [
                (0, 0, 0), (0, 0, 0), (245, 250, 255), (215, 225, 240), (175, 185, 205),
                (255, 255, 255), (230, 235, 245), (180, 190, 210), (30, 30, 40), (15, 15, 25),
                (45, 215, 255), (25, 145, 195), (235, 40, 70), (155, 25, 45), (255, 225, 50), (255, 255, 255)
            ],
            'gogeta_ssj4': [
                (0, 0, 0), (0, 0, 0), (255, 220, 185), (245, 185, 140), (195, 125, 85),
                (195, 25, 40), (135, 15, 25), (255, 80, 95), (255, 95, 20), (255, 165, 50),
                (240, 240, 245), (180, 185, 195), (255, 140, 0), (35, 145, 225), (255, 225, 60), (255, 255, 255)
            ],
            'gogeta_ssj5': [
                (0, 0, 0), (0, 0, 0), (255, 220, 185), (245, 185, 140), (195, 125, 85),
                (240, 245, 255), (195, 205, 225), (255, 255, 255), (220, 225, 235), (160, 170, 190),
                (240, 240, 245), (180, 185, 195), (255, 140, 0), (35, 145, 225), (80, 220, 255), (255, 255, 255)
            ],
            'beerus_god': [
                (0, 0, 0), (0, 0, 0), (185, 140, 215), (150, 95, 185), (110, 60, 145),
                (255, 215, 0), (195, 150, 0), (255, 245, 130), (35, 95, 185), (20, 55, 125),
                (45, 45, 50), (25, 25, 30), (235, 65, 35), (175, 35, 20), (255, 235, 60), (255, 255, 255)
            ],
            'whis_angel': [
                (0, 0, 0), (0, 0, 0), (205, 235, 255), (165, 205, 245), (120, 165, 215),
                (255, 255, 255), (230, 235, 245), (180, 190, 210), (145, 25, 45), (95, 15, 30),
                (45, 45, 55), (25, 25, 35), (255, 145, 35), (35, 155, 245), (255, 225, 50), (210, 175, 20)
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
            ]
        }

    def _get_color(self, pal_name, idx):
        pal = self.palettes.get(pal_name, self.palettes['saiyan_ssj4'])
        if idx == 0:
            return (0, 0, 0, 0)
        c = pal[idx % len(pal)]
        return (c[0], c[1], c[2], 255)

    def create_base_sprite(self, character_type="saiyan_ssj4"):
        sprite = Image.new('RGBA', (self.sprite_width, self.sprite_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(sprite)

        pal = character_type if character_type in self.palettes else 'saiyan_ssj4'
        outline = self._get_color(pal, 1)
        skin_high = self._get_color(pal, 2)
        skin_base = self._get_color(pal, 3)
        skin_shad = self._get_color(pal, 4)

        cx = self.sprite_width // 2
        cy = self.sprite_height // 2

<<<<<<< HEAD
        if character_type == "saiyan_ssj4":
            fur_base = self._get_color(pal, 5)
            fur_shad = self._get_color(pal, 6)
            fur_high = self._get_color(pal, 7)
=======
        if character_type in ("saiyan_ssj4", "saiyan_ssj5", "vegeta_ssj5", "gogeta_ssj4", "gogeta_ssj5"):
            fur_base = self._get_color(pal, 5)
            fur_shad = self._get_color(pal, 6)
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
            hair_base = self._get_color(pal, 8)
            hair_high = self._get_color(pal, 9)
            pants_base = self._get_color(pal, 10)
            belt_color = self._get_color(pal, 12)
            eye_color = self._get_color(pal, 14)
            white_col = self._get_color(pal, 15)

            draw.polygon([(cx - 12, cy - 2), (cx + 12, cy - 2), (cx + 14, cy + 14), (cx - 14, cy + 14)], fill=fur_base, outline=outline)
            draw.polygon([(cx - 6, cy), (cx + 6, cy), (cx + 4, cy + 10), (cx - 4, cy + 10)], fill=skin_base, outline=outline)
<<<<<<< HEAD
            draw.line([(cx, cy + 2), (cx, cy + 9)], fill=skin_shad)
=======
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
            draw.rectangle([(cx - 13, cy + 13), (cx + 13, cy + 17)], fill=belt_color, outline=outline)
            draw.rectangle([(cx - 11, cy + 18), (cx - 2, cy + 30)], fill=pants_base, outline=outline)
            draw.rectangle([(cx + 2, cy + 18), (cx + 11, cy + 30)], fill=pants_base, outline=outline)
            draw.rectangle([(cx - 18, cy - 1), (cx - 12, cy + 12)], fill=fur_base, outline=outline)
            draw.rectangle([(cx - 18, cy + 10), (cx - 12, cy + 13)], fill=belt_color, outline=outline)
            draw.rectangle([(cx - 17, cy + 14), (cx - 13, cy + 17)], fill=skin_base, outline=outline)
            draw.rectangle([(cx + 12, cy - 1), (cx + 18, cy + 12)], fill=fur_base, outline=outline)
            draw.rectangle([(cx + 12, cy + 10), (cx + 18, cy + 13)], fill=belt_color, outline=outline)
            draw.rectangle([(cx + 13, cy + 14), (cx + 17, cy + 17)], fill=skin_base, outline=outline)
<<<<<<< HEAD
            draw.polygon([(cx - 20, cy - 5), (cx - 22, cy - 25), (cx - 14, cy - 38), (cx, cy - 42), (cx + 14, cy - 38), (cx + 22, cy - 25), (cx + 20, cy - 5)], fill=hair_base, outline=outline)
            draw.ellipse([(cx - 13, cy - 28), (cx + 13, cy - 4)], fill=skin_base, outline=outline)
            draw.polygon([(cx - 8, cy - 28), (cx - 12, cy - 18), (cx - 3, cy - 24)], fill=hair_base, outline=outline)
            draw.polygon([(cx + 8, cy - 28), (cx + 12, cy - 18), (cx + 3, cy - 24)], fill=hair_base, outline=outline)
            eye_y = cy - 16
            draw.rectangle([(cx - 9, eye_y - 1), (cx - 4, eye_y + 3)], fill=fur_shad)
            draw.rectangle([(cx + 4, eye_y - 1), (cx + 9, eye_y + 3)], fill=fur_shad)
            draw.rectangle([(cx - 8, eye_y), (cx - 5, eye_y + 2)], fill=white_col)
            draw.rectangle([(cx + 5, eye_y), (cx + 8, eye_y + 2)], fill=white_col)
            draw.point([(cx - 6, eye_y + 1), (cx + 6, eye_y + 1)], fill=eye_color)

        elif character_type == "saiyan_ssj_god":
            hair_god = self._get_color(pal, 5)
            hair_high = self._get_color(pal, 7)
            gi_orange = self._get_color(pal, 8)
            gi_blue = self._get_color(pal, 10)
            eye_red = self._get_color(pal, 12)
            white_col = self._get_color(pal, 15)

            # 1. Goku Orange Gi & Blue Undershirt
            draw.polygon([(cx - 13, cy - 2), (cx + 13, cy - 2), (cx + 14, cy + 14), (cx - 14, cy + 14)], fill=gi_orange, outline=outline)
            draw.polygon([(cx - 8, cy - 2), (cx + 8, cy - 2), (cx + 6, cy + 8), (cx - 6, cy + 8)], fill=gi_blue, outline=outline)
            # 2. Blue Belt & Orange Pants
            draw.rectangle([(cx - 13, cy + 13), (cx + 13, cy + 17)], fill=gi_blue, outline=outline)
            draw.rectangle([(cx - 11, cy + 18), (cx - 2, cy + 30)], fill=gi_orange, outline=outline)
            draw.rectangle([(cx + 2, cy + 18), (cx + 11, cy + 30)], fill=gi_orange, outline=outline)
            # 3. Arms & Blue Wristbands
            draw.rectangle([(cx - 18, cy - 1), (cx - 12, cy + 12)], fill=skin_base, outline=outline)
            draw.rectangle([(cx - 18, cy + 9), (cx - 12, cy + 13)], fill=gi_blue, outline=outline)
            draw.rectangle([(cx - 17, cy + 14), (cx - 13, cy + 17)], fill=skin_base, outline=outline)
            draw.rectangle([(cx + 12, cy - 1), (cx + 18, cy + 12)], fill=skin_base, outline=outline)
            draw.rectangle([(cx + 12, cy + 9), (cx + 18, cy + 13)], fill=gi_blue, outline=outline)
            draw.rectangle([(cx + 13, cy + 14), (cx + 17, cy + 17)], fill=skin_base, outline=outline)
            # 4. Slender SSJ God Crimson-Magenta Hair (Base Goku silhouette with divine glow)
            draw.polygon([(cx - 18, cy - 5), (cx - 20, cy - 22), (cx - 12, cy - 35), (cx, cy - 38), (cx + 12, cy - 35), (cx + 20, cy - 22), (cx + 18, cy - 5)], fill=hair_god, outline=outline)
            draw.line([(cx - 10, cy - 30), (cx - 4, cy - 20)], fill=hair_high, width=2)
            draw.line([(cx + 10, cy - 30), (cx + 4, cy - 20)], fill=hair_high, width=2)
            # 5. Head & Slender Face
            draw.ellipse([(cx - 12, cy - 28), (cx + 12, cy - 4)], fill=skin_base, outline=outline)
            # Bangs
            draw.polygon([(cx - 10, cy - 28), (cx - 14, cy - 18), (cx - 4, cy - 22)], fill=hair_god, outline=outline)
            draw.polygon([(cx + 10, cy - 28), (cx + 14, cy - 18), (cx + 4, cy - 22)], fill=hair_god, outline=outline)
            # 6. Divine Crimson Eyes
            eye_y = cy - 16
            draw.rectangle([(cx - 8, eye_y), (cx - 5, eye_y + 2)], fill=white_col)
            draw.rectangle([(cx + 5, eye_y), (cx + 8, eye_y + 2)], fill=white_col)
            draw.point([(cx - 6, eye_y + 1), (cx + 6, eye_y + 1)], fill=eye_red)

        elif character_type == "zaiko_af":
            hair_high = self._get_color(pal, 5)
            hair_base = self._get_color(pal, 6)
            horn_color = self._get_color(pal, 8)
            tunic_base = self._get_color(pal, 10)
            tunic_shad = self._get_color(pal, 11)
            red_sash = self._get_color(pal, 12)
            gold_buckle = self._get_color(pal, 14)

            draw.polygon([(cx - 13, cy - 3), (cx + 13, cy - 3), (cx + 15, cy + 16), (cx - 15, cy + 16)], fill=tunic_base, outline=outline)
            draw.polygon([(cx - 13, cy), (cx + 13, cy + 12), (cx + 13, cy + 16), (cx - 13, cy + 6)], fill=red_sash, outline=outline)
            draw.rectangle([(cx - 4, cy + 6), (cx + 4, cy + 12)], fill=gold_buckle, outline=outline)
            draw.rectangle([(cx - 11, cy + 17), (cx - 3, cy + 27)], fill=tunic_shad, outline=outline)
            draw.rectangle([(cx + 3, cy + 17), (cx + 11, cy + 27)], fill=tunic_shad, outline=outline)
            draw.rectangle([(cx - 12, cy + 26), (cx - 2, cy + 31)], fill=red_sash, outline=outline)
            draw.rectangle([(cx + 2, cy + 26), (cx + 12, cy + 31)], fill=red_sash, outline=outline)
            draw.rectangle([(cx - 18, cy - 2), (cx - 13, cy + 13)], fill=tunic_base, outline=outline)
            draw.rectangle([(cx + 13, cy - 2), (cx + 18, cy + 13)], fill=tunic_base, outline=outline)
            draw.rectangle([(cx - 18, cy + 14), (cx - 13, cy + 18)], fill=skin_base, outline=outline)
            draw.rectangle([(cx + 13, cy + 14), (cx + 18, cy + 18)], fill=skin_base, outline=outline)
            draw.polygon([(cx - 22, cy - 5), (cx - 24, cy - 28), (cx - 15, cy - 44), (cx, cy - 48), (cx + 15, cy - 44), (cx + 24, cy - 28), (cx + 22, cy - 5)], fill=hair_base, outline=outline)
            draw.ellipse([(cx - 13, cy - 28), (cx + 13, cy - 4)], fill=skin_base, outline=outline)
            draw.polygon([(cx - 9, cy - 8), (cx - 14, cy - 2), (cx - 6, cy - 5)], fill=horn_color, outline=outline)
            draw.polygon([(cx + 9, cy - 8), (cx + 14, cy - 2), (cx + 6, cy - 5)], fill=horn_color, outline=outline)
            eye_y = cy - 17
            draw.rectangle([(cx - 9, eye_y), (cx - 4, eye_y + 3)], fill=red_sash, outline=outline)
            draw.rectangle([(cx + 4, eye_y), (cx + 9, eye_y + 3)], fill=red_sash, outline=outline)
            draw.point([(cx - 6, eye_y + 1), (cx + 6, eye_y + 1)], fill=(255, 255, 255, 255))

        elif character_type == "gogeta_ssj4":
            fur_base = self._get_color(pal, 5)
            hair_base = self._get_color(pal, 8)
            hair_high = self._get_color(pal, 9)
            pants_base = self._get_color(pal, 10)
            vest_pad = self._get_color(pal, 12)
            vest_sash = self._get_color(pal, 13)
            white_col = self._get_color(pal, 15)

            draw.polygon([(cx - 13, cy - 2), (cx + 13, cy - 2), (cx + 14, cy + 14), (cx - 14, cy + 14)], fill=fur_base, outline=outline)
            draw.rectangle([(cx - 13, cy - 3), (cx - 6, cy + 10)], fill=outline, outline=vest_pad)
            draw.rectangle([(cx + 6, cy - 3), (cx + 13, cy + 10)], fill=outline, outline=vest_pad)
            draw.rectangle([(cx - 13, cy + 12), (cx + 13, cy + 16)], fill=vest_sash, outline=outline)
            draw.rectangle([(cx - 11, cy + 17), (cx - 2, cy + 30)], fill=pants_base, outline=outline)
            draw.rectangle([(cx + 2, cy + 17), (cx + 11, cy + 30)], fill=pants_base, outline=outline)
            draw.rectangle([(cx - 18, cy - 1), (cx - 12, cy + 12)], fill=fur_base, outline=outline)
            draw.rectangle([(cx - 18, cy + 10), (cx - 12, cy + 14)], fill=outline, outline=vest_pad)
            draw.rectangle([(cx - 17, cy + 14), (cx - 13, cy + 17)], fill=skin_base, outline=outline)
            draw.rectangle([(cx + 12, cy - 1), (cx + 18, cy + 12)], fill=fur_base, outline=outline)
            draw.rectangle([(cx + 12, cy + 10), (cx + 18, cy + 14)], fill=outline, outline=vest_pad)
            draw.rectangle([(cx + 13, cy + 14), (cx + 17, cy + 17)], fill=skin_base, outline=outline)
            draw.polygon([(cx - 22, cy - 5), (cx - 24, cy - 25), (cx - 16, cy - 40), (cx, cy - 46), (cx + 16, cy - 40), (cx + 24, cy - 25), (cx + 22, cy - 5)], fill=hair_base, outline=outline)
=======
            draw.polygon([(cx - 22, cy - 5), (cx - 24, cy - 26), (cx - 16, cy - 42), (cx, cy - 46), (cx + 16, cy - 42), (cx + 24, cy - 26), (cx + 22, cy - 5)], fill=hair_base, outline=outline)
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
            draw.line([(cx - 12, cy - 35), (cx - 6, cy - 22)], fill=hair_high, width=2)
            draw.line([(cx + 12, cy - 35), (cx + 6, cy - 22)], fill=hair_high, width=2)
            draw.ellipse([(cx - 13, cy - 28), (cx + 13, cy - 4)], fill=skin_base, outline=outline)
            draw.polygon([(cx - 8, cy - 28), (cx - 12, cy - 18), (cx - 3, cy - 24)], fill=hair_base, outline=outline)
            draw.polygon([(cx + 8, cy - 28), (cx + 12, cy - 18), (cx + 3, cy - 24)], fill=hair_base, outline=outline)
            eye_y = cy - 16
            draw.rectangle([(cx - 8, eye_y), (cx - 5, eye_y + 2)], fill=white_col)
            draw.rectangle([(cx + 5, eye_y), (cx + 8, eye_y + 2)], fill=white_col)
<<<<<<< HEAD
            draw.point([(cx - 6, eye_y + 1), (cx + 6, eye_y + 1)], fill=vest_sash)

        elif character_type == "beerus_god":
            gold_col = self._get_color(pal, 5)
            blue_pants = self._get_color(pal, 8)
            belt_col = self._get_color(pal, 10)
            red_sash = self._get_color(pal, 12)
            eye_col = self._get_color(pal, 14)

            draw.polygon([(cx - 11, cy - 2), (cx + 11, cy - 2), (cx + 13, cy + 14), (cx - 13, cy + 14)], fill=skin_base, outline=outline)
            draw.polygon([(cx - 12, cy - 2), (cx + 12, cy - 2), (cx + 10, cy + 6), (cx - 10, cy + 6)], fill=gold_col, outline=outline)
            draw.rectangle([(cx - 4, cy + 2), (cx + 4, cy + 5)], fill=blue_pants)
            draw.rectangle([(cx - 12, cy + 13), (cx + 12, cy + 16)], fill=belt_col, outline=outline)
            draw.rectangle([(cx - 3, cy + 16), (cx + 3, cy + 26)], fill=red_sash, outline=outline)
            draw.rectangle([(cx - 11, cy + 17), (cx - 3, cy + 29)], fill=blue_pants, outline=outline)
            draw.rectangle([(cx + 3, cy + 17), (cx + 11, cy + 29)], fill=blue_pants, outline=outline)
            draw.rectangle([(cx - 17, cy - 1), (cx - 12, cy + 12)], fill=skin_base, outline=outline)
            draw.rectangle([(cx - 17, cy + 8), (cx - 12, cy + 11)], fill=gold_col, outline=outline)
            draw.rectangle([(cx + 12, cy - 1), (cx + 17, cy + 12)], fill=skin_base, outline=outline)
            draw.rectangle([(cx + 12, cy + 8), (cx + 17, cy + 11)], fill=gold_col, outline=outline)
            draw.polygon([(cx - 12, cy - 24), (cx - 20, cy - 42), (cx - 6, cy - 28)], fill=skin_base, outline=outline)
            draw.polygon([(cx + 12, cy - 24), (cx + 20, cy - 42), (cx + 6, cy - 28)], fill=skin_base, outline=outline)
            draw.ellipse([(cx - 13, cy - 28), (cx + 13, cy - 5)], fill=skin_base, outline=outline)
            eye_y = cy - 17
            draw.rectangle([(cx - 9, eye_y), (cx - 4, eye_y + 3)], fill=eye_col, outline=outline)
            draw.rectangle([(cx + 4, eye_y), (cx + 9, eye_y + 3)], fill=eye_col, outline=outline)
            draw.point([(cx - 6, eye_y + 1), (cx + 6, eye_y + 1)], fill=outline)

        elif character_type == "whis_angel":
            white_hair = self._get_color(pal, 6)
            maroon_tunic = self._get_color(pal, 8)
            dark_boots = self._get_color(pal, 10)
            orange_sash = self._get_color(pal, 12)
            staff_gem = self._get_color(pal, 13)
            halo_gold = self._get_color(pal, 14)

            draw.polygon([(cx - 12, cy - 3), (cx + 12, cy - 3), (cx + 15, cy + 24), (cx - 15, cy + 24)], fill=maroon_tunic, outline=outline)
            draw.polygon([(cx - 10, cy - 2), (cx + 10, cy - 2), (cx + 8, cy + 8), (cx - 8, cy + 8)], fill=orange_sash, outline=outline)
            draw.rectangle([(cx - 10, cy + 24), (cx - 2, cy + 30)], fill=dark_boots, outline=outline)
            draw.rectangle([(cx + 2, cy + 24), (cx + 10, cy + 30)], fill=dark_boots, outline=outline)
            draw.rectangle([(cx - 18, cy - 1), (cx - 12, cy + 14)], fill=maroon_tunic, outline=outline)
            draw.rectangle([(cx + 12, cy - 1), (cx + 18, cy + 14)], fill=maroon_tunic, outline=outline)
            draw.ellipse([(cx - 18, cy - 12), (cx + 18, cy - 4)], outline=halo_gold, width=2)
            draw.polygon([(cx - 15, cy - 10), (cx - 18, cy - 32), (cx - 8, cy - 46), (cx, cy - 50), (cx + 8, cy - 46), (cx + 18, cy - 32), (cx + 15, cy - 10)], fill=white_hair, outline=outline)
            draw.ellipse([(cx - 12, cy - 27), (cx + 12, cy - 4)], fill=skin_base, outline=outline)
            eye_y = cy - 15
            draw.line([(cx - 8, eye_y), (cx - 4, eye_y)], fill=outline, width=2)
            draw.line([(cx + 4, eye_y), (cx + 8, eye_y)], fill=outline, width=2)
            draw.line([(cx + 19, cy - 20), (cx + 19, cy + 28)], fill=halo_gold, width=2)
            draw.ellipse([(cx + 16, cy - 24), (cx + 22, cy - 18)], fill=staff_gem, outline=outline)
=======
            draw.point([(cx - 6, eye_y + 1), (cx + 6, eye_y + 1)], fill=eye_color)

        elif character_type == "evil_goku":
            gi_black = self._get_color(pal, 5)
            gi_grey = self._get_color(pal, 8)
            hair_dark = self._get_color(pal, 6)
            eye_red = self._get_color(pal, 10)
            
            draw.polygon([(cx - 13, cy - 2), (cx + 13, cy - 2), (cx + 14, cy + 14), (cx - 14, cy + 14)], fill=gi_black, outline=outline)
            draw.polygon([(cx - 8, cy - 2), (cx + 8, cy - 2), (cx + 6, cy + 8), (cx - 6, cy + 8)], fill=gi_grey, outline=outline)
            draw.rectangle([(cx - 13, cy + 13), (cx + 13, cy + 17)], fill=gi_grey, outline=outline)
            draw.rectangle([(cx - 11, cy + 18), (cx - 2, cy + 30)], fill=gi_black, outline=outline)
            draw.rectangle([(cx + 2, cy + 18), (cx + 11, cy + 30)], fill=gi_black, outline=outline)
            draw.rectangle([(cx - 18, cy - 1), (cx - 12, cy + 12)], fill=skin_base, outline=outline)
            draw.rectangle([(cx - 18, cy + 9), (cx - 12, cy + 13)], fill=gi_grey, outline=outline)
            draw.rectangle([(cx - 17, cy + 14), (cx - 13, cy + 17)], fill=skin_base, outline=outline)
            draw.rectangle([(cx + 12, cy - 1), (cx + 18, cy + 12)], fill=skin_base, outline=outline)
            draw.rectangle([(cx + 12, cy + 9), (cx + 18, cy + 13)], fill=gi_grey, outline=outline)
            draw.rectangle([(cx + 13, cy + 14), (cx + 17, cy + 17)], fill=skin_base, outline=outline)
            draw.polygon([(cx - 20, cy - 5), (cx - 22, cy - 25), (cx - 14, cy - 38), (cx, cy - 42), (cx + 14, cy - 38), (cx + 22, cy - 25), (cx + 20, cy - 5)], fill=hair_dark, outline=outline)
            draw.ellipse([(cx - 12, cy - 28), (cx + 12, cy - 4)], fill=skin_base, outline=outline)
            eye_y = cy - 16
            draw.rectangle([(cx - 8, eye_y), (cx - 5, eye_y + 2)], fill=eye_red)
            draw.rectangle([(cx + 5, eye_y), (cx + 8, eye_y + 2)], fill=eye_red)

        elif character_type == "angel_z":
            white_robe = self._get_color(pal, 5)
            dark_halo = self._get_color(pal, 8)
            cyan_gem = self._get_color(pal, 10)
            red_eye = self._get_color(pal, 12)

            draw.polygon([(cx - 13, cy - 3), (cx + 13, cy - 3), (cx + 15, cy + 24), (cx - 15, cy + 24)], fill=white_robe, outline=outline)
            draw.ellipse([(cx - 22, cy + 4), (cx + 22, cy + 14)], outline=dark_halo, width=2)
            draw.ellipse([(cx - 12, cy - 27), (cx + 12, cy - 4)], fill=skin_base, outline=outline)
            eye_y = cy - 16
            draw.rectangle([(cx - 8, eye_y), (cx - 5, eye_y + 2)], fill=red_eye)
            draw.rectangle([(cx + 5, eye_y), (cx + 8, eye_y + 2)], fill=red_eye)
            draw.rectangle([(cx - 3, cy + 6), (cx + 3, cy + 10)], fill=cyan_gem, outline=outline)

        else:
            # Fallback for SSGod, Beerus, Whis, Zaiko
            draw.ellipse([(cx - 12, cy - 25), (cx + 12, cy - 5)], fill=skin_base, outline=outline)
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)

        return sprite

    def create_animation_spritesheet(self, character_type="saiyan_ssj4", animation_type="idle"):
        spritesheet = Image.new('RGBA', (self.sprite_width * 4, self.sprite_height), (0, 0, 0, 0))
        pal = character_type if character_type in self.palettes else 'saiyan_ssj4'
        outline = self._get_color(pal, 1)

        for frame in range(4):
            sprite = self.create_base_sprite(character_type)
            draw = ImageDraw.Draw(sprite)

            if animation_type == "idle":
                offset_y = int(math.sin(frame * math.pi / 2) * 2)
                spritesheet.paste(sprite, (frame * self.sprite_width, offset_y), sprite)

            elif animation_type == "punch":
                if frame in (1, 2):
                    ext = 22 if frame == 2 else 16
                    draw.rectangle([(self.sprite_width//2 + 10, self.sprite_height//2 - 2),
                                    (self.sprite_width//2 + ext, self.sprite_height//2 + 4)], fill=self._get_color(pal, 3), outline=outline)
                elif frame == 3:
                    for _ in range(4):
                        x = random.randint(self.sprite_width//2 + 15, self.sprite_width//2 + 22)
                        y = random.randint(self.sprite_height//2 - 6, self.sprite_height//2 + 6)
                        draw.ellipse([(x, y), (x+3, y+3)], fill=(255, 240, 60, 255), outline=outline)
                spritesheet.paste(sprite, (frame * self.sprite_width, 0), sprite)

            elif animation_type == "powerup":
                aura_col = self._get_color(pal, 14)
                for i in range(2 + frame * 2):
                    draw.arc([(self.sprite_width//2 - 20 - i, self.sprite_height//2 - 35 - i),
                              (self.sprite_width//2 + 20 + i, self.sprite_height//2 + 35 + i)],
                             start=0, end=360, fill=aura_col, width=1)
                spritesheet.paste(sprite, (frame * self.sprite_width, 0), sprite)

            elif animation_type == "ki_blast":
<<<<<<< HEAD
                blast_col = (80, 200, 255, 255) if character_type in ("saiyan_ssj4", "whis_angel") else (225, 45, 60, 255)
=======
                blast_col = (80, 200, 255, 255) if character_type in ("saiyan_ssj4", "saiyan_ssj5", "whis_angel") else (225, 45, 60, 255)
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
                if frame == 0:
                    draw.ellipse([(self.sprite_width//2 + 12, self.sprite_height//2 - 4),
                                  (self.sprite_width//2 + 18, self.sprite_height//2 + 2)], fill=blast_col, outline=outline)
                elif frame in (1, 2):
                    draw.ellipse([(self.sprite_width//2 + 15, self.sprite_height//2 - 6),
                                  (self.sprite_width//2 + 28, self.sprite_height//2 + 6)], fill=blast_col, outline=outline)
                elif frame == 3:
                    draw.ellipse([(self.sprite_width//2 + 24, self.sprite_height//2 - 10),
                                  (self.sprite_width//2 + 44, self.sprite_height//2 + 10)], fill=blast_col, outline=outline)
                spritesheet.paste(sprite, (frame * self.sprite_width, 0), sprite)

            else:
                spritesheet.paste(sprite, (frame * self.sprite_width, 0), sprite)

        return spritesheet

    def create_character_set(self, character_type="saiyan_ssj4"):
        full_spritesheet = Image.new('RGBA', (self.sprite_width * 16, self.sprite_height * 5), (0, 0, 0, 0))
        animations = ["idle", "punch", "kick", "powerup", "ki_blast"]
        for i, animation in enumerate(animations):
            spritesheet = self.create_animation_spritesheet(character_type, animation)
            full_spritesheet.paste(spritesheet, (0, i * self.sprite_height))
        return full_spritesheet

    def export_gba_palette(self, pal_name, filename_pal):
        pal = self.palettes.get(pal_name, self.palettes['saiyan_ssj4'])
        gba_bytes = bytearray()
        for r, g, b in pal:
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
    gen = DBZGBASpriteGenerator()
<<<<<<< HEAD
    chars = ["saiyan_ssj4", "saiyan_ssj_god", "zaiko_af", "gogeta_ssj4", "beerus_god", "whis_angel"]
=======
    chars = [
        "saiyan_ssj4", "saiyan_ssj_god", "saiyan_ssj5", "vegeta_ssj5", "zaiko_af",
        "evil_goku", "angel_z", "gogeta_ssj4", "gogeta_ssj5", "beerus_god", "whis_angel"
    ]
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
    for char in chars:
        out_dir = f"generated_assets/{char}"
        os.makedirs(out_dir, exist_ok=True)
        sheet = gen.create_character_set(char)
        sheet.save(f"{out_dir}/{char}_spritesheet.png")
        gen.export_gba_palette(char, f"{out_dir}/{char}_palette.pal")
        gen.export_gba_4bpp_tiles(sheet, f"{out_dir}/{char}_sprites_compressed.bin")
        for anim in ["idle", "punch", "powerup", "ki_blast"]:
            anim_img = gen.create_animation_spritesheet(char, anim)
            anim_img.save(f"{out_dir}/{char}_{anim}.png")
            anim_img.save(f"log4_gt/sprites/{char}_{anim}.png")
        sheet.save(f"log4_gt/sprites/{char}_spritesheet.png")

<<<<<<< HEAD
    print("✅ Successfully generated GBA-compatible sprites, 16-color .pal palettes, and 4bpp LZ77 binaries for ALL 6 characters (SSJ4, SSGod, Zaiko, Gogeta SSJ4, Beerus, Whis)!")
=======
    print("✅ Successfully generated GBA-compatible sprites, 16-color .pal palettes, and 4bpp LZ77 binaries for ALL 11 characters & forms!")
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)

if __name__ == "__main__":
    main()
