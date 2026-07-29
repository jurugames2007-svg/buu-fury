#!/usr/bin/env python3
"""
<<<<<<< HEAD
generate_improved_portraits.py — GBA 128x144 Pixel-Art Portraits for all characters
-------------------------------------------------------------------------------------
Generates crisp 16-color GBA-style portraits for:
  - Base Goku
  - Super Saiyan 1
  - Super Saiyan 3 (original intact)
  - Super Saiyan 4 (with red fur, golden eyes, red eyeliner, wild mane)
  - Super Saiyan God (SSGod, crimson-magenta divine hair, calm red God eyes)
  - Gogeta Super Saiyan 4 (Metamoran vest, crimson fur, crimson/gold hair)
  - Beerus / Bills (God of Destruction, purple cat skin, Egyptian gold collar)
  - Whis (Angel attendant, blue skin, white hair, halo)
  - Zaiko / Xicor (Post-game boss, silver hair, green chin horns, red eyes)
=======
generate_improved_portraits.py — GBA 128x144 Pixel-Art Portraits for all 14 characters
-------------------------------------------------------------------------------------
Generates crisp 16-color GBA-style portraits for:
  - Base Goku, SSJ1, SSJ3, SSJ4, SSGod, SSJ5, Vegeta SSJ5
  - Gogeta SSJ4, Gogeta SSJ5
  - Beerus, Whis
  - Zaiko AF, Angel Z, Evil Goku
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
"""

from PIL import Image, ImageDraw
import os

def draw_portrait_background(draw, width=128, height=144, bg_type="ssj4"):
    colors = {
        'base': [(10, 20, 50), (20, 40, 90), (30, 60, 130)],
        'ssj1': [(60, 45, 0), (120, 90, 0), (180, 140, 10)],
        'ssj3': [(70, 30, 0), (140, 65, 0), (210, 110, 0)],
        'ssj4': [(65, 10, 15), (135, 20, 30), (200, 35, 50)],
        'ssj_god': [(85, 10, 35), (160, 25, 65), (235, 50, 95)],
<<<<<<< HEAD
        'gogeta_ssj4': [(80, 15, 20), (150, 35, 45), (220, 60, 25)],
        'beerus': [(40, 10, 55), (80, 25, 110), (130, 45, 175)],
        'whis': [(10, 35, 65), (25, 75, 135), (45, 125, 210)],
        'zaiko': [(15, 35, 20), (25, 75, 40), (35, 115, 60)]
=======
        'ssj5': [(40, 45, 60), (90, 100, 130), (160, 180, 220)],
        'vegeta_ssj5': [(30, 45, 80), (60, 90, 160), (100, 150, 230)],
        'gogeta_ssj4': [(80, 15, 20), (150, 35, 45), (220, 60, 25)],
        'gogeta_ssj5': [(70, 60, 90), (130, 115, 170), (200, 185, 240)],
        'beerus': [(40, 10, 55), (80, 25, 110), (130, 45, 175)],
        'whis': [(10, 35, 65), (25, 75, 135), (45, 125, 210)],
        'zaiko': [(15, 35, 20), (25, 75, 40), (35, 115, 60)],
        'evil_goku': [(20, 5, 10), (50, 10, 20), (90, 20, 40)],
        'angel_z': [(65, 70, 80), (130, 140, 160), (210, 220, 240)]
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
    }
    pal = colors.get(bg_type, colors['ssj4'])
    for y in range(height):
        ratio = y / height
        col = pal[0] if ratio < 0.35 else (pal[1] if ratio < 0.7 else pal[2])
        draw.line([(0, y), (width, y)], fill=col)

    draw.rectangle([(0, 0), (width-1, height-1)], outline=(255, 215, 0), width=2)
    draw.rectangle([(2, 2), (width-3, height-3)], outline=(0, 0, 0), width=1)

def draw_portrait(char_type="ssj4"):
    img = Image.new('RGB', (128, 144), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_portrait_background(draw, 128, 144, char_type)
    
    outline = (0, 0, 0)
    skin_base = (245, 185, 140)
    skin_shad = (200, 130, 90)
<<<<<<< HEAD
    skin_high = (255, 220, 190)
=======
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)

    cx = 64
    eye_y = 65

    if char_type == "ssj4":
        fur_base = (225, 35, 45)
        fur_shad = (165, 20, 25)
<<<<<<< HEAD
        fur_high = (255, 85, 95)
        hair_base = (25, 25, 30)
        hair_high = (85, 85, 100)
        eye_col = (255, 215, 0)

=======
        hair_base = (25, 25, 30)
        hair_high = (85, 85, 100)
        eye_col = (255, 215, 0)
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
        draw.polygon([(cx - 52, 120), (cx - 58, 70), (cx - 45, 25), (cx - 20, 8), (cx, 4), (cx + 20, 8), (cx + 45, 25), (cx + 58, 70), (cx + 52, 120)], fill=hair_base, outline=outline)
        draw.line([(cx - 30, 30), (cx - 15, 15)], fill=hair_high, width=3)
        draw.line([(cx + 30, 30), (cx + 15, 15)], fill=hair_high, width=3)
        draw.polygon([(cx - 48, 144), (cx - 44, 95), (cx + 44, 95), (cx + 48, 144)], fill=fur_base, outline=outline)
        draw.polygon([(cx - 22, 95), (cx + 22, 95), (cx + 16, 144), (cx - 16, 144)], fill=skin_base, outline=outline)
<<<<<<< HEAD
        draw.line([(cx, 105), (cx, 138)], fill=skin_shad, width=2)
=======
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
        draw.polygon([(cx - 14, 95), (cx - 14, 75), (cx + 14, 75), (cx + 14, 95)], fill=skin_shad, outline=outline)
        draw.polygon([(cx - 26, 45), (cx - 28, 70), (cx - 16, 92), (cx, 98), (cx + 16, 92), (cx + 28, 70), (cx + 26, 45)], fill=skin_base, outline=outline)
        draw.polygon([(cx - 26, 45), (cx - 35, 75), (cx - 20, 65)], fill=hair_base, outline=outline)
        draw.polygon([(cx + 26, 45), (cx + 35, 75), (cx + 20, 65)], fill=hair_base, outline=outline)
        draw.rectangle([(cx - 20, eye_y - 3), (cx - 8, eye_y + 5)], fill=fur_shad)
        draw.rectangle([(cx + 8, eye_y - 3), (cx + 20, eye_y + 5)], fill=fur_shad)
        draw.rectangle([(cx - 18, eye_y), (cx - 9, eye_y + 4)], fill=(255, 255, 255))
        draw.rectangle([(cx + 9, eye_y), (cx + 18, eye_y + 4)], fill=(255, 255, 255))
        draw.rectangle([(cx - 15, eye_y + 1), (cx - 11, eye_y + 3)], fill=eye_col)
        draw.rectangle([(cx + 11, eye_y + 1), (cx + 15, eye_y + 3)], fill=eye_col)
        draw.line([(cx - 8, 86), (cx + 8, 86)], fill=outline, width=2)

<<<<<<< HEAD
    elif char_type == "ssj_god":
        hair_god = (244, 63, 94)
        hair_high = (251, 113, 133)
        gi_col = (245, 120, 25)
        eye_red = (225, 29, 72)

        # Slender SSJ God Magenta Hair
        draw.polygon([(cx - 44, 80), (cx - 46, 45), (cx - 28, 15), (cx, 8), (cx + 28, 15), (cx + 46, 45), (cx + 44, 80)], fill=hair_god, outline=outline)
        draw.line([(cx - 20, 25), (cx - 8, 15)], fill=hair_high, width=3)
        draw.line([(cx + 20, 25), (cx + 8, 15)], fill=hair_high, width=3)
        # Orange Gi & Blue Undershirt
        draw.polygon([(cx - 44, 144), (cx - 40, 95), (cx + 40, 95), (cx + 44, 144)], fill=gi_col, outline=outline)
        draw.polygon([(cx - 18, 95), (cx + 18, 95), (cx + 14, 144), (cx - 14, 144)], fill=(35, 70, 165), outline=outline)
        draw.polygon([(cx - 14, 95), (cx - 14, 75), (cx + 14, 75), (cx + 14, 95)], fill=skin_shad, outline=outline)
        # Slender Face
        draw.polygon([(cx - 25, 45), (cx - 27, 70), (cx - 15, 92), (cx, 98), (cx + 15, 92), (cx + 27, 70), (cx + 25, 45)], fill=skin_base, outline=outline)
        draw.polygon([(cx - 20, 45), (cx - 26, 68), (cx - 13, 58)], fill=hair_god, outline=outline)
        draw.polygon([(cx + 20, 45), (cx + 26, 68), (cx + 13, 58)], fill=hair_god, outline=outline)
        # Divine Crimson God Eyes
        draw.rectangle([(cx - 18, eye_y), (cx - 9, eye_y + 4)], fill=(255, 255, 255))
        draw.rectangle([(cx + 9, eye_y), (cx + 18, eye_y + 4)], fill=(255, 255, 255))
        draw.rectangle([(cx - 15, eye_y + 1), (cx - 11, eye_y + 3)], fill=eye_red)
        draw.rectangle([(cx + 11, eye_y + 1), (cx + 15, eye_y + 3)], fill=eye_red)
        draw.line([(cx - 8, 86), (cx + 8, 86)], fill=outline, width=2)

    elif char_type == "gogeta_ssj4":
        fur_base = (195, 25, 40)
        hair_base = (240, 60, 20)
        hair_high = (255, 175, 45)
        vest_pad = (255, 140, 0)
        vest_blue = (35, 145, 225)

        draw.polygon([(cx - 56, 120), (cx - 60, 70), (cx - 48, 22), (cx - 22, 6), (cx, 3), (cx + 22, 6), (cx + 48, 22), (cx + 60, 70), (cx + 56, 120)], fill=hair_base, outline=outline)
        draw.line([(cx - 32, 28), (cx - 15, 14)], fill=hair_high, width=3)
        draw.line([(cx + 32, 28), (cx + 15, 14)], fill=hair_high, width=3)
        draw.polygon([(cx - 48, 144), (cx - 42, 95), (cx + 42, 95), (cx + 48, 144)], fill=(20, 20, 25), outline=outline)
        draw.polygon([(cx - 44, 110), (cx - 24, 95), (cx - 20, 108), (cx - 38, 120)], fill=vest_pad, outline=outline)
        draw.polygon([(cx + 44, 110), (cx + 24, 95), (cx + 20, 108), (cx + 38, 120)], fill=vest_pad, outline=outline)
        draw.polygon([(cx - 22, 95), (cx + 22, 95), (cx + 16, 144), (cx - 16, 144)], fill=fur_base, outline=outline)
        draw.polygon([(cx - 12, 100), (cx + 12, 100), (cx + 10, 144), (cx - 10, 144)], fill=skin_base, outline=outline)
        draw.polygon([(cx - 14, 95), (cx - 14, 75), (cx + 14, 75), (cx + 14, 95)], fill=skin_shad, outline=outline)
        draw.polygon([(cx - 26, 45), (cx - 28, 70), (cx - 16, 92), (cx, 98), (cx + 16, 92), (cx + 28, 70), (cx + 26, 45)], fill=skin_base, outline=outline)
        draw.polygon([(cx - 24, 45), (cx - 32, 72), (cx - 18, 62)], fill=hair_base, outline=outline)
        draw.polygon([(cx + 24, 45), (cx + 32, 72), (cx + 18, 62)], fill=hair_base, outline=outline)
        draw.rectangle([(cx - 20, eye_y - 2), (cx - 8, eye_y + 4)], fill=(120, 15, 25))
        draw.rectangle([(cx + 8, eye_y - 2), (cx + 20, eye_y + 4)], fill=(120, 15, 25))
        draw.rectangle([(cx - 18, eye_y), (cx - 9, eye_y + 3)], fill=(255, 255, 255))
        draw.rectangle([(cx + 9, eye_y), (cx + 18, eye_y + 3)], fill=(255, 255, 255))
        draw.rectangle([(cx - 15, eye_y + 1), (cx - 11, eye_y + 3)], fill=vest_blue)
        draw.rectangle([(cx + 11, eye_y + 1), (cx + 15, eye_y + 3)], fill=vest_blue)
        draw.line([(cx - 8, 86), (cx + 8, 86)], fill=outline, width=2)

    elif char_type == "beerus":
        cat_base = (150, 95, 185)
        cat_shad = (110, 60, 145)
        gold_col = (255, 215, 0)
        blue_gem = (35, 95, 185)
        eye_col = (255, 235, 60)

        draw.polygon([(cx - 22, 60), (cx - 52, 10), (cx - 12, 35)], fill=cat_base, outline=outline)
        draw.polygon([(cx + 22, 60), (cx + 52, 10), (cx + 12, 35)], fill=cat_base, outline=outline)
        draw.polygon([(cx - 48, 144), (cx - 36, 95), (cx + 36, 95), (cx + 48, 144)], fill=gold_col, outline=outline)
        draw.polygon([(cx - 18, 98), (cx, 115), (cx + 18, 98), (cx, 102)], fill=blue_gem, outline=outline)
        draw.polygon([(cx - 12, 95), (cx - 12, 75), (cx + 12, 75), (cx + 12, 95)], fill=cat_shad, outline=outline)
        draw.polygon([(cx - 26, 45), (cx - 28, 70), (cx - 16, 92), (cx, 98), (cx + 16, 92), (cx + 28, 70), (cx + 26, 45)], fill=cat_base, outline=outline)
        draw.rectangle([(cx - 20, eye_y - 2), (cx - 8, eye_y + 4)], fill=(0, 0, 0))
        draw.rectangle([(cx + 8, eye_y - 2), (cx + 20, eye_y + 4)], fill=(0, 0, 0))
        draw.rectangle([(cx - 18, eye_y), (cx - 9, eye_y + 3)], fill=eye_col)
        draw.rectangle([(cx + 9, eye_y), (cx + 18, eye_y + 3)], fill=eye_col)
        draw.point([(cx - 14, eye_y + 1), (cx + 14, eye_y + 1)], fill=(0, 0, 0))
        draw.line([(cx - 8, 86), (cx + 8, 86)], fill=outline, width=2)

    elif char_type == "whis":
        angel_skin = (175, 215, 250)
        angel_shad = (130, 175, 220)
        hair_white = (245, 248, 255)
        tunic_red = (145, 25, 45)
        halo_gold = (255, 225, 50)

        draw.polygon([(cx - 48, 144), (cx - 36, 95), (cx + 36, 95), (cx + 48, 144)], fill=tunic_red, outline=outline)
        draw.ellipse([(cx - 24, 85), (cx + 24, 100)], outline=halo_gold, width=3)
        draw.polygon([(cx - 30, 60), (cx - 25, 10), (cx, 5), (cx + 25, 10), (cx + 30, 60)], fill=hair_white, outline=outline)
        draw.polygon([(cx - 12, 95), (cx - 12, 75), (cx + 12, 75), (cx + 12, 95)], fill=angel_shad, outline=outline)
        draw.polygon([(cx - 22, 45), (cx - 24, 70), (cx - 14, 92), (cx, 98), (cx + 14, 92), (cx + 24, 70), (cx + 22, 45)], fill=angel_skin, outline=outline)
        draw.line([(cx - 16, eye_y + 2), (cx - 8, eye_y + 2)], fill=outline, width=2)
        draw.line([(cx + 8, eye_y + 2), (cx + 16, eye_y + 2)], fill=outline, width=2)
        draw.arc([(cx - 8, 82), (cx + 8, 92)], start=20, end=160, fill=outline, width=2)

    elif char_type == "zaiko":
        hair_base = (220, 225, 235)
        eye_col = (235, 30, 40)
        horn_col = (45, 155, 75)
        tunic_col = (50, 50, 65)

        draw.polygon([(cx - 56, 110), (cx - 60, 60), (cx - 50, 15), (cx - 25, 4), (cx, 2), (cx + 25, 4), (cx + 50, 15), (cx + 60, 60), (cx + 56, 110)], fill=hair_base, outline=outline)
        draw.polygon([(cx - 48, 144), (cx - 42, 98), (cx + 42, 98), (cx + 48, 144)], fill=tunic_col, outline=outline)
        draw.polygon([(cx - 24, 98), (cx, 115), (cx + 24, 98), (cx, 88)], fill=(195, 30, 40), outline=outline)
        draw.polygon([(cx - 14, 95), (cx - 14, 75), (cx + 14, 75), (cx + 14, 95)], fill=skin_shad, outline=outline)
        draw.polygon([(cx - 26, 45), (cx - 28, 70), (cx - 16, 92), (cx, 98), (cx + 16, 92), (cx + 28, 70), (cx + 26, 45)], fill=skin_base, outline=outline)
        draw.polygon([(cx - 18, 85), (cx - 25, 96), (cx - 12, 90)], fill=horn_col, outline=outline)
        draw.polygon([(cx + 18, 85), (cx + 25, 96), (cx + 12, 90)], fill=horn_col, outline=outline)
        draw.polygon([(cx - 8, 92), (cx - 14, 104), (cx - 4, 96)], fill=horn_col, outline=outline)
        draw.polygon([(cx + 8, 92), (cx + 14, 104), (cx + 4, 96)], fill=horn_col, outline=outline)
        draw.rectangle([(cx - 20, eye_y - 2), (cx - 8, eye_y + 4)], fill=(0, 0, 0))
        draw.rectangle([(cx + 8, eye_y - 2), (cx + 20, eye_y + 4)], fill=(0, 0, 0))
        draw.rectangle([(cx - 18, eye_y), (cx - 9, eye_y + 3)], fill=eye_col)
        draw.rectangle([(cx + 9, eye_y), (cx + 18, eye_y + 3)], fill=eye_col)
        draw.line([(cx - 8, 85), (cx + 10, 83)], fill=outline, width=2)

    elif char_type == "ssj3":
        hair_base = (255, 215, 0)
        gi_col = (245, 120, 25)
        eye_col = (40, 160, 150)
        draw.polygon([(cx - 56, 140), (cx - 50, 70), (cx - 40, 20), (cx, 10), (cx + 40, 20), (cx + 50, 70), (cx + 56, 140)], fill=hair_base, outline=outline)
        draw.polygon([(cx - 44, 144), (cx - 40, 95), (cx + 40, 95), (cx + 44, 144)], fill=gi_col, outline=outline)
        draw.polygon([(cx - 18, 95), (cx + 18, 95), (cx + 14, 144), (cx - 14, 144)], fill=(35, 70, 165), outline=outline)
        draw.polygon([(cx - 14, 95), (cx - 14, 75), (cx + 14, 75), (cx + 14, 95)], fill=skin_shad, outline=outline)
        draw.polygon([(cx - 26, 45), (cx - 28, 70), (cx - 16, 92), (cx, 98), (cx + 16, 92), (cx + 28, 70), (cx + 26, 45)], fill=skin_base, outline=outline)
        draw.line([(cx - 22, 58), (cx - 8, 62)], fill=skin_shad, width=3)
        draw.line([(cx + 8, 62), (cx + 22, 58)], fill=skin_shad, width=3)
=======
    elif char_type in ("ssj5", "vegeta_ssj5", "gogeta_ssj5"):
        fur_silver = (220, 225, 235)
        hair_silver = (245, 248, 255)
        eye_col = (235, 35, 45) if char_type == "ssj5" else ((80, 220, 255) if char_type == "vegeta_ssj5" else (255, 215, 0))
        draw.polygon([(cx - 56, 120), (cx - 60, 70), (cx - 48, 22), (cx - 22, 6), (cx, 3), (cx + 22, 6), (cx + 48, 22), (cx + 60, 70), (cx + 56, 120)], fill=hair_silver, outline=outline)
        draw.polygon([(cx - 48, 144), (cx - 44, 95), (cx + 44, 95), (cx + 48, 144)], fill=fur_silver, outline=outline)
        draw.polygon([(cx - 22, 95), (cx + 22, 95), (cx + 16, 144), (cx - 16, 144)], fill=skin_base, outline=outline)
        draw.polygon([(cx - 14, 95), (cx - 14, 75), (cx + 14, 75), (cx + 14, 95)], fill=skin_shad, outline=outline)
        draw.polygon([(cx - 26, 45), (cx - 28, 70), (cx - 16, 92), (cx, 98), (cx + 16, 92), (cx + 28, 70), (cx + 26, 45)], fill=skin_base, outline=outline)
        draw.polygon([(cx - 26, 45), (cx - 35, 75), (cx - 20, 65)], fill=hair_silver, outline=outline)
        draw.polygon([(cx + 26, 45), (cx + 35, 75), (cx + 20, 65)], fill=hair_silver, outline=outline)
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
        draw.rectangle([(cx - 18, eye_y), (cx - 9, eye_y + 4)], fill=(255, 255, 255))
        draw.rectangle([(cx + 9, eye_y), (cx + 18, eye_y + 4)], fill=(255, 255, 255))
        draw.rectangle([(cx - 15, eye_y + 1), (cx - 11, eye_y + 3)], fill=eye_col)
        draw.rectangle([(cx + 11, eye_y + 1), (cx + 15, eye_y + 3)], fill=eye_col)
        draw.line([(cx - 8, 86), (cx + 8, 86)], fill=outline, width=2)

<<<<<<< HEAD
    elif char_type in ("ssj1", "base"):
        hair_base = (255, 215, 0) if char_type == "ssj1" else (25, 25, 30)
        eye_col = (40, 160, 150) if char_type == "ssj1" else (25, 25, 30)
        gi_col = (245, 120, 25)
        draw.polygon([(cx - 45, 80), (cx - 48, 45), (cx - 30, 15), (cx, 8), (cx + 30, 15), (cx + 48, 45), (cx + 45, 80)], fill=hair_base, outline=outline)
        draw.polygon([(cx - 44, 144), (cx - 40, 95), (cx + 40, 95), (cx + 44, 144)], fill=gi_col, outline=outline)
        draw.polygon([(cx - 18, 95), (cx + 18, 95), (cx + 14, 144), (cx - 14, 144)], fill=(35, 70, 165), outline=outline)
        draw.polygon([(cx - 14, 95), (cx - 14, 75), (cx + 14, 75), (cx + 14, 95)], fill=skin_shad, outline=outline)
        draw.polygon([(cx - 26, 45), (cx - 28, 70), (cx - 16, 92), (cx, 98), (cx + 16, 92), (cx + 28, 70), (cx + 26, 45)], fill=skin_base, outline=outline)
        draw.polygon([(cx - 22, 45), (cx - 28, 68), (cx - 14, 58)], fill=hair_base, outline=outline)
        draw.polygon([(cx + 22, 45), (cx + 28, 68), (cx + 14, 58)], fill=hair_base, outline=outline)
        draw.rectangle([(cx - 18, eye_y), (cx - 9, eye_y + 4)], fill=(255, 255, 255))
        draw.rectangle([(cx + 9, eye_y), (cx + 18, eye_y + 4)], fill=(255, 255, 255))
        draw.rectangle([(cx - 15, eye_y + 1), (cx - 11, eye_y + 3)], fill=eye_col)
        draw.rectangle([(cx + 11, eye_y + 1), (cx + 15, eye_y + 3)], fill=eye_col)
        draw.line([(cx - 8, 86), (cx + 8, 86)], fill=outline, width=2)

=======
    elif char_type == "evil_goku":
        skin_pale = (225, 225, 230)
        gi_dark = (25, 25, 30)
        eye_red = (235, 25, 40)
        draw.polygon([(cx - 48, 80), (cx - 50, 45), (cx - 30, 15), (cx, 8), (cx + 30, 15), (cx + 50, 45), (cx + 48, 80)], fill=(35, 35, 40), outline=outline)
        draw.polygon([(cx - 44, 144), (cx - 40, 95), (cx + 40, 95), (cx + 44, 144)], fill=gi_dark, outline=outline)
        draw.polygon([(cx - 14, 95), (cx - 14, 75), (cx + 14, 75), (cx + 14, 95)], fill=(180, 180, 190), outline=outline)
        draw.polygon([(cx - 26, 45), (cx - 28, 70), (cx - 16, 92), (cx, 98), (cx + 16, 92), (cx + 28, 70), (cx + 26, 45)], fill=skin_pale, outline=outline)
        draw.rectangle([(cx - 18, eye_y), (cx - 9, eye_y + 4)], fill=eye_red)
        draw.rectangle([(cx + 9, eye_y), (cx + 18, eye_y + 4)], fill=eye_red)
        draw.line([(cx - 8, 86), (cx + 8, 86)], fill=outline, width=2)

    elif char_type == "angel_z":
        white_robe = (245, 250, 255)
        dark_halo = (25, 25, 35)
        eye_red = (235, 40, 60)
        draw.polygon([(cx - 48, 144), (cx - 36, 95), (cx + 36, 95), (cx + 48, 144)], fill=white_robe, outline=outline)
        draw.ellipse([(cx - 28, 80), (cx + 28, 96)], outline=dark_halo, width=3)
        draw.polygon([(cx - 26, 45), (cx - 28, 70), (cx - 16, 92), (cx, 98), (cx + 16, 92), (cx + 28, 70), (cx + 26, 45)], fill=skin_base, outline=outline)
        draw.rectangle([(cx - 18, eye_y), (cx - 9, eye_y + 4)], fill=eye_red)
        draw.rectangle([(cx + 9, eye_y), (cx + 18, eye_y + 4)], fill=eye_red)

    else:
        # Fallback to standard Base portrait
        draw.ellipse([(cx - 20, 30), (cx + 20, 90)], fill=skin_base, outline=outline)

>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
    return img

def main():
    os.makedirs("log4_gt/portraits", exist_ok=True)
    os.makedirs("generated_assets", exist_ok=True)

<<<<<<< HEAD
    types = ["base", "ssj1", "ssj3", "ssj4", "ssj_god", "gogeta_ssj4", "beerus", "whis", "zaiko"]
=======
    types = [
        "base", "ssj1", "ssj3", "ssj4", "ssj_god", "ssj5", "vegeta_ssj5",
        "gogeta_ssj4", "gogeta_ssj5", "evil_goku", "angel_z", "beerus", "whis", "zaiko"
    ]
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)
    images = {}
    for t in types:
        p = draw_portrait(t)
        p.save(f"log4_gt/portraits/portrait_{t}.png")
        p.save(f"generated_assets/portrait_{t}.png")
        images[t] = p

<<<<<<< HEAD
    # 9-portrait comparison grid (1152x144)
    grid9 = Image.new('RGB', (128 * 9, 144), (10, 10, 15))
    for idx, t in enumerate(types):
        grid9.paste(images[t], (idx * 128, 0))
    grid9.save("log4_gt/portraits/HIERARCHY_LOG4_ALL_PORTRAITS.png")
    grid9.save("generated_assets/HIERARCHY_LOG4_ALL_PORTRAITS.png")

    print("✅ Created crisp 128x144 GBA portraits for Base, SSJ1, SSJ3, SSJ4, SSGod, Gogeta SSJ4, Beerus, Whis, and Zaiko!")
=======
    # 14-portrait comparison grid (1792x144)
    grid14 = Image.new('RGB', (128 * 14, 144), (10, 10, 15))
    for idx, t in enumerate(types):
        grid14.paste(images[t], (idx * 128, 0))
    grid14.save("log4_gt/portraits/HIERARCHY_ALL_14_PORTRAITS.png")
    grid14.save("generated_assets/HIERARCHY_ALL_14_PORTRAITS.png")

    print("✅ Created crisp 128x144 GBA portraits for ALL 14 characters & forms and saved HIERARCHY_ALL_14_PORTRAITS.png!")
>>>>>>> 78b1596 (Integrate Complete GT and AF Absolute Legacy Design Manual, 14-form roster, and GBA compatibility architecture)

if __name__ == "__main__":
    main()
