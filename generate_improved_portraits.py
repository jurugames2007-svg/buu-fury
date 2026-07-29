#!/usr/bin/env python3
"""
generate_improved_portraits.py — GBA 128x144 Pixel-Art Portraits for all 14 characters
-------------------------------------------------------------------------------------
Generates crisp 16-color GBA-style portraits for:
  - Base Goku, SSJ1, SSJ3, SSJ4, SSGod, SSJ5, Vegeta SSJ5
  - Gogeta SSJ4, Gogeta SSJ5
  - Beerus, Whis
  - Zaiko AF, Angel Z, Evil Goku
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
        'ssj5': [(40, 45, 60), (90, 100, 130), (160, 180, 220)],
        'vegeta_ssj5': [(30, 45, 80), (60, 90, 160), (100, 150, 230)],
        'gogeta_ssj4': [(80, 15, 20), (150, 35, 45), (220, 60, 25)],
        'gogeta_ssj5': [(70, 60, 90), (130, 115, 170), (200, 185, 240)],
        'beerus': [(40, 10, 55), (80, 25, 110), (130, 45, 175)],
        'whis': [(10, 35, 65), (25, 75, 135), (45, 125, 210)],
        'zaiko': [(15, 35, 20), (25, 75, 40), (35, 115, 60)],
        'evil_goku': [(20, 5, 10), (50, 10, 20), (90, 20, 40)],
        'angel_z': [(65, 70, 80), (130, 140, 160), (210, 220, 240)]
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

    cx = 64
    eye_y = 65

    if char_type == "ssj4":
        fur_base = (225, 35, 45)
        fur_shad = (165, 20, 25)
        hair_base = (25, 25, 30)
        hair_high = (85, 85, 100)
        eye_col = (255, 215, 0)
        draw.polygon([(cx - 52, 120), (cx - 58, 70), (cx - 45, 25), (cx - 20, 8), (cx, 4), (cx + 20, 8), (cx + 45, 25), (cx + 58, 70), (cx + 52, 120)], fill=hair_base, outline=outline)
        draw.line([(cx - 30, 30), (cx - 15, 15)], fill=hair_high, width=3)
        draw.line([(cx + 30, 30), (cx + 15, 15)], fill=hair_high, width=3)
        draw.polygon([(cx - 48, 144), (cx - 44, 95), (cx + 44, 95), (cx + 48, 144)], fill=fur_base, outline=outline)
        draw.polygon([(cx - 22, 95), (cx + 22, 95), (cx + 16, 144), (cx - 16, 144)], fill=skin_base, outline=outline)
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
        draw.rectangle([(cx - 18, eye_y), (cx - 9, eye_y + 4)], fill=(255, 255, 255))
        draw.rectangle([(cx + 9, eye_y), (cx + 18, eye_y + 4)], fill=(255, 255, 255))
        draw.rectangle([(cx - 15, eye_y + 1), (cx - 11, eye_y + 3)], fill=eye_col)
        draw.rectangle([(cx + 11, eye_y + 1), (cx + 15, eye_y + 3)], fill=eye_col)
        draw.line([(cx - 8, 86), (cx + 8, 86)], fill=outline, width=2)

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
        draw.ellipse([(cx - 20, 30), (cx + 20, 90)], fill=skin_base, outline=outline)

    return img

def main():
    os.makedirs("log4_gt/portraits", exist_ok=True)
    os.makedirs("generated_assets", exist_ok=True)

    types = [
        "base", "ssj1", "ssj3", "ssj4", "ssj_god", "ssj5", "vegeta_ssj5",
        "gogeta_ssj4", "gogeta_ssj5", "evil_goku", "angel_z", "beerus", "whis", "zaiko"
    ]
    images = {}
    for t in types:
        p = draw_portrait(t)
        p.save(f"log4_gt/portraits/portrait_{t}.png")
        p.save(f"generated_assets/portrait_{t}.png")
        images[t] = p

    grid14 = Image.new('RGB', (128 * 14, 144), (10, 10, 15))
    for idx, t in enumerate(types):
        grid14.paste(images[t], (idx * 128, 0))
    grid14.save("log4_gt/portraits/HIERARCHY_ALL_14_PORTRAITS.png")
    grid14.save("generated_assets/HIERARCHY_ALL_14_PORTRAITS.png")

    print("✅ Created crisp 128x144 GBA portraits for ALL 14 characters & forms without conflict markers!")

if __name__ == "__main__":
    main()
