#!/usr/bin/env python3
"""
generate_ui_icons.py — UI Badges, Items & Saga Banners for Legacy of Goku 4 Expansion
-------------------------------------------------------------------------------------
Creates 32x32 and 64x32 UI icons for:
  - Food & Items: Pudín de Bills, Copa Helada de Whis, Fruta del Árbol del Poder
  - NPCs & Bosses: Beerus, Whis, Zaiko
  - Skills: Gogeta SSJ4 Big Bang Kamehameha x100, SSGod God Kamehameha
  - Map Banners: Planeta de Bills, Saga AF Postgame
"""

from PIL import Image, ImageDraw
import os

def make_icon(filename, bg_col, draw_func):
    img = Image.new('RGB', (32, 32), bg_col)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (31, 31)], outline=(255, 215, 0), width=1)
    draw_func(draw)
    img.save(filename)

def make_banner(filename, bg_col, title_col):
    img = Image.new('RGB', (64, 32), bg_col)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (63, 31)], outline=(255, 215, 0), width=1)
    draw.rectangle([(4, 8), (60, 23)], fill=title_col)
    draw.rectangle([(16, 12), (24, 20)], fill=(255, 255, 255))
    draw.rectangle([(38, 12), (46, 20)], fill=(255, 255, 255))
    img.save(filename)

def main():
    os.makedirs("log4_gt/ui_icons", exist_ok=True)

    # 1. Pudín de Bills (Beerus's Pudding)
    make_icon("log4_gt/ui_icons/item_beerus_pudding.png", (30, 10, 40), lambda d: [
        d.ellipse([(6, 12), (26, 26)], fill=(255, 215, 120), outline=(0, 0, 0)),
        d.rectangle([(10, 8), (22, 14)], fill=(180, 50, 40), outline=(0, 0, 0))
    ])

    # 2. Copa Helada de Whis (Whis's Sundae)
    make_icon("log4_gt/ui_icons/item_whis_sundae.png", (10, 30, 60), lambda d: [
        d.polygon([(8, 12), (24, 12), (18, 28), (14, 28)], fill=(220, 240, 255), outline=(0, 0, 0)),
        d.ellipse([(10, 6), (22, 16)], fill=(255, 120, 150), outline=(0, 0, 0)),
        d.ellipse([(14, 4), (18, 8)], fill=(255, 40, 40))
    ])

    # 3. Fruta del Árbol del Poder (Tree of Might Fruit)
    make_icon("log4_gt/ui_icons/item_tree_of_might_fruit.png", (20, 45, 20), lambda d: [
        d.ellipse([(6, 8), (26, 26)], fill=(195, 35, 50), outline=(0, 0, 0)),
        d.rectangle([(14, 4), (18, 10)], fill=(100, 60, 30)),
        d.polygon([(16, 6), (22, 4), (20, 10)], fill=(40, 180, 60))
    ])

    # 4. Gogeta SSJ4 Skill Icon
    make_icon("log4_gt/ui_icons/icon_gogeta_ssj4.png", (50, 10, 15), lambda d: [
        d.ellipse([(6, 6), (26, 26)], fill=(80, 200, 255), outline=(255, 215, 0)),
        d.ellipse([(12, 12), (20, 20)], fill=(255, 255, 255))
    ])

    # 5. Super Saiyan God Skill Icon
    make_icon("log4_gt/ui_icons/icon_ssj_god.png", (65, 10, 30), lambda d: [
        d.ellipse([(6, 6), (26, 26)], fill=(244, 63, 94), outline=(255, 215, 0)),
        d.ellipse([(12, 12), (20, 20)], fill=(255, 180, 200))
    ])

    # 6. Beerus NPC badge
    make_icon("log4_gt/ui_icons/npc_beerus.png", (40, 10, 55), lambda d: [
        d.polygon([(6, 10), (16, 26), (26, 10)], fill=(150, 95, 185), outline=(0, 0, 0)),
        d.polygon([(6, 10), (10, 2), (14, 10)], fill=(150, 95, 185)),
        d.polygon([(18, 10), (22, 2), (26, 10)], fill=(150, 95, 185)),
        d.rectangle([(10, 14), (13, 16)], fill=(255, 235, 60)),
        d.rectangle([(19, 14), (22, 16)], fill=(255, 235, 60))
    ])

    # 7. Whis NPC badge
    make_icon("log4_gt/ui_icons/npc_whis.png", (10, 35, 65), lambda d: [
        d.ellipse([(8, 8), (24, 26)], fill=(175, 215, 250), outline=(0, 0, 0)),
        d.ellipse([(10, 4), (22, 10)], outline=(255, 225, 50), width=2),
        d.polygon([(10, 8), (16, 4), (22, 8)], fill=(245, 248, 255))
    ])

    # 8. Zaiko NPC badge
    make_icon("log4_gt/ui_icons/npc_zaiko.png", (15, 35, 20), lambda d: [
        d.polygon([(8, 10), (16, 26), (24, 10)], fill=(240, 190, 155), outline=(0, 0, 0)),
        d.polygon([(10, 18), (14, 24), (18, 18)], fill=(45, 155, 75)),
        d.rectangle([(11, 14), (14, 16)], fill=(235, 30, 40)),
        d.rectangle([(18, 14), (21, 16)], fill=(235, 30, 40))
    ])

    # 9. Banners
    make_banner("log4_gt/ui_icons/saga_beerus_planet.png", (30, 15, 50), (180, 130, 255))
    make_banner("log4_gt/ui_icons/saga_af_postgame.png", (20, 20, 30), (150, 20, 30))

    print("✅ Created UI icons for all new items, food, shops, skills, and Beerus/Whis/Zaiko/SSGod NPCs!")

if __name__ == "__main__":
    main()
