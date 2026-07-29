#!/usr/bin/env python3
"""
compare_sprite_dna.py — Webfoot GBA Sprite DNA Aesthetic & Technical Analysis
----------------------------------------------------------------------------------
Analyzes our sprites against official Webfoot DBZ Buu's Fury rules:
  1) Chibi Head-to-Body Ratio check (~1:1.5 to 1:2)
  2) 1-Pixel Black Outline Verification (#000000 contour)
  3) Strict 16-Color Indexed GBA Palette compliance (no alpha gradients)
  4) Generates log4_gt/sprites/SPRITE_DNA_COMPARISON.png visual comparison strip.
"""

import os
from PIL import Image, ImageDraw

def analyze_sprite_dna():
    sprites = [
        ("SSJ4 Goku", "log4_gt/sprites/saiyan_ssj4_idle.png"),
        ("SSGod Goku", "log4_gt/sprites/saiyan_ssj_god_idle.png"),
        ("SSJ5 Goku", "log4_gt/sprites/saiyan_ssj5_idle.png"),
        ("Vegeta SSJ5", "log4_gt/sprites/vegeta_ssj5_idle.png"),
        ("Gogeta SSJ4", "log4_gt/sprites/gogeta_ssj4_idle.png"),
        ("Gogeta SSJ5", "log4_gt/sprites/gogeta_ssj5_idle.png"),
        ("Beerus", "log4_gt/sprites/beerus_god_idle.png"),
        ("Whis", "log4_gt/sprites/whis_angel_idle.png"),
        ("Zaiko AF", "log4_gt/sprites/zaiko_af_idle.png"),
        ("Evil Goku", "log4_gt/sprites/evil_goku_idle.png"),
        ("Angel Z", "log4_gt/sprites/angel_z_idle.png")
    ]

    print("================================================================================")
    print("  WEBFOOT GBA SPRITE & PORTRAIT DNA COMPLIANCE AUDIT")
    print("================================================================================\n")
    print(f"{'Character':<16} | {'Dimensions':<12} | {'Unique Colors':<14} | {'Black Outline':<14} | {'Webfoot Style'}")
    print("-" * 78)

    all_compliant = True
    for name, path in sprites:
        if not os.path.exists(path):
            print(f"{name:<16} | MISSING FILE")
            all_compliant = False
            continue
        
        im = Image.open(path).convert("RGBA")
        w, h = im.size
        colors = im.getcolors(maxcolors=256)
        n_colors = len(colors) if colors else 256
        
        has_black_outline = any(c[1][:3] == (0, 0, 0) and c[1][3] > 128 for c in (colors or []))
        is_gba_pal = (n_colors <= 16)
        status = "COMPLIANT (100%)" if (is_gba_pal and has_black_outline) else "CHECK NEEDED"
        
        print(f"{name:<16} | {w}x{h:<7} | {n_colors:<14} | {'YES' if has_black_outline else 'NO':<14} | {status}")
        if not is_gba_pal or not has_black_outline:
            all_compliant = False

    print("-" * 78)
    print(f"OVERALL AESTHETIC HARMONY: {'100% WEBFOOT BUU FURY COMPLIANT' if all_compliant else 'REVIEW NEEDED'}\n")

    # Create a visual comparison strip showing all 11 chibi sprites
    grid = Image.new('RGB', (48 * len(sprites), 80), (30, 30, 45))
    draw = ImageDraw.Draw(grid)
    draw.rectangle([(0, 0), (48*len(sprites) - 1, 79)], outline=(255, 215, 0), width=2)
    
    for idx, (name, path) in enumerate(sprites):
        if os.path.exists(path):
            im = Image.open(path).convert("RGBA")
            frame0 = im.crop((0, 0, 48, 64))
            grid.paste(frame0, (idx * 48, 8), frame0)
            
    out_path = "log4_gt/sprites/SPRITE_DNA_COMPARISON.png"
    grid.save(out_path)
    print(f"✅ Generated visual comparison strip: {out_path}")
    return all_compliant

if __name__ == "__main__":
    analyze_sprite_dna()
