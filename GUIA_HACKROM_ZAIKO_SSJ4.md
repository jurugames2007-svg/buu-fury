# Dragon Ball Z: Buu's Fury — Post-Game Zaiko (Xicor) & GT Super Saiyan 4 DLC

Hackrom completa / expansión para **Dragon Ball Z: Buu's Fury (USA)** (GBA) que añade:
1. **Contenido Post-Game tras derrotar a Kid Buu**: Encuentro con el superjefe secreto **Zaiko (Xicor)** en el **bosque del Distrito 439** (un poco más lejos de fuera de la casa donde inicia la historia de **Gohan Adulto**).
2. **Zaiko es mucho más fuerte que Kid Buu** (Nivel 200, 99,999 HP, estadísticas muy superiores al Kid Buu original).
3. **Mejora gráfica en sprites y retratos**:
   - Retratos al estilo GBA (128x144, 16 colores): **SSJ4 Goku** (pelaje rojo, cabello salvaje negro/rojo, ojos dorados) superior a SSJ3, y **Zaiko** (cabello plateado, cuernos verdes de Kaioshin, ojos carmesí).
   - Sprites al estilo **Webfoot** de Buu's Fury: proporciones chibi, contornos negros nítidos, paletas indexadas estrictas de 16 colores.
4. **Habilidad Super Saiyan 4 desde el inicio/Other World**: Hablando con el NPC de **Kaiosama del Este (East Kai)** en el **Camino de la Serpiente (Snake Way)**, obtienes la habilidad y transformación de **Super Saiyan 4** (ID de forma 1, slot independiente del SSJ3 original).

---

## 1. Archivos principales del proyecto

| Archivo / Carpeta | Descripción |
| :--- | :--- |
| `dbz_gba_sprite_tool.py` | Herramienta en Python (Pygame + PIL) adaptada de tu código para generar sprites de DBZ al estilo Buu's Fury con paletas estrictas de 16 colores y exportación nativa GBA 4bpp/15-bit BGR. |
| `generate_improved_portraits.py` | Generador de portraits de 128x144 para **Base, SSJ1, SSJ3, SSJ4 y Zaiko**, junto al gráfico comparativo de jerarquía. |
| `generated_assets/ssj4_goku/` | Spritesheets, animaciones individuales, paletas `.pal` y datos binarios `.bin` (4bpp GBA) de Goku SSJ4. |
| `generated_assets/zaiko_af/` | Spritesheets, animaciones individuales, paletas y datos binarios `.bin` del jefe Zaiko (Xicor). |
| `log4_gt/datasheets/zaiko_postgame_boss.json` | Ficha técnica / Datasheet completa del enemigo Zaiko con comparación de stats vs Kid Buu y lore del postgame. |
| `log4_gt/datasheets/GDD_GT_DLC.json` | Documento de diseño del juego (GDD) con el árbol de formas, habilidades, sagas GT y el encuentro secreto AF de Zaiko. |
| `log4_gt/dialogues/zaiko_forest_postgame.txt` | Diálogos de Gohan Adulto vs Zaiko en el bosque y de Kaiosama del Este en Snake Way. |
| `log4_gt/portraits/` | Todos los retratos actualizados de Goku (Base, SSJ1, SSJ3, SSJ4) y del enemigo Zaiko. |
| `log4_gt/ui_icons/` | Iconos del menú de habilidades, cara del NPC Zaiko e insignias de saga AF / GT. |
| `hackrom_ssj4/patches/cambios_aplicados.json` | Registro de parches y offsets de inyección en la ROM. |

---

## 2. Ficha Técnica / Datasheet del Jefe Post-Game: Zaiko (Xicor)

```json
{
  "boss_name": "Zaiko (Xicor)",
  "title": "Post-Game Ultimate Adversary — AF DLC",
  "location": {
    "map_name": "East District 439 (Bosque fuera de la casa de Gohan Adulto)",
    "chapter": "Post-Game (Accesible después de haber derrotado a Kid Buu)",
    "description": "Ubicado en la espesura oeste del bosque de la casa de Goku y Gohan, un poco más lejos de donde comienza el capítulo de Gohan Adulto en Buu's Fury."
  },
  "stat_comparison_vs_kid_buu": {
    "kid_buu_vanilla": {
      "level": 140,
      "hp": 32000,
      "strength": 150,
      "defense": 140,
      "speed": 135
    },
    "zaiko_postgame_boss": {
      "level": 200,
      "hp": 99999,
      "strength": 350,
      "defense": 320,
      "speed": 280,
      "power_multiplier": "3.1x HP, 2.3x Ataque, 2.3x Defensa"
    }
  },
  "dialogue_preview": [
    "Zaiko: ¿Así que este es el famoso planeta Tierra... y tú eres el hijo del guerrero más poderoso, Son Goku?",
    "Gohan: ¿Quién eres tú? ¡Tu Ki es gigantesco... jamás había sentido una energía tan abrumadora, ni siquiera con Kid Buu!",
    "Zaiko: Mi nombre es Zaiko. Llevo en mis venas la sangre de tu padre Goku y el poder supremo de los Kaioshin... ¡Kid Buu no era más que un monstruo primitivo!",
    "Zaiko: ¡Muéstrame el verdadero poder de los Saiyajin! ¡Ni siquiera el Super Saiyan 4 podría hacerme un rasguño!"
  ]
}
```

---

## 3. Jerarquía y Retratos (Portraits)

* La jerarquía oficial del menú y combate es:
  $$\text{SSJ4 (ID 1)} > \text{SSJ3 (ID 5, original intacto)} > \text{SSJ1 (ID 3)} > \text{Base (ID 0)}$$
* El portrait de **Super Saiyan 4** (`portrait_ssj4.png`) se distingue del dorado SSJ3 por su **pelaje rojo carmesí**, contorno de ojos rojo característico, pupila dorada e imponente cabellera salvaje negra y rojiza.
* El portrait de **Zaiko** (`portrait_zaiko.png`) presenta cabello plateado estilo Super Saiyan 5, cuernos/espinas verdes de Kaioshin en el mentón, túnica oscura y ojos carmesí.
* Puedes consultar la comparativa en un solo gráfico dentro del archivo `log4_gt/portraits/HIERARCHY_SS4_SS3_SS1_BASE.png`.

---

## 4. Instrucciones de uso para el generador en Python (`dbz_gba_sprite_tool.py`)

Si deseas generar o personalizar nuevos sprites para tus datasheets con el script mejorado:
```bash
# Ejecutar el generador para crear spritesheets y archivos GBA .bin / .pal
python3 dbz_gba_sprite_tool.py

# Ejecutar el generador de retratos e íconos de interfaz
python3 generate_improved_portraits.py
python3 generate_ui_icons.py
```

---

## 5. Instrucciones para jugar el Hackrom en mGBA

1. Abre tu emulador **mGBA**.
2. Carga la ROM modificada principal: `log4_gt/ROM/LegacyOfGoku4_GT_DLC.gba` (o el parche en `hackrom_ssj4/ROM/DBZ_Buus_Fury_SSJ4_HACK.gba`).
3. **Para desbloquear Super Saiyan 4 al inicio**:
   - Inicia partida y llega al **Camino de la Serpiente (Snake Way)** en el Otro Mundo.
   - Habla con el NPC de **Kaiosama del Este (East Kai)** situado junto al camino.
   - Recibirás la habilidad y transformación **Super Saiyan 4**. Abre tu menú de Skills, equipa **Super Saiyan 4** y presiona **B** en el juego para transformar a Goku con su paleta y retrato mejorados.
4. **Para el combate Post-Game contra Zaiko**:
   - Tras derrotar a **Kid Buu** en la historia principal, dirígete al mapa inicial de **Gohan Adulto** (Distrito Este 439).
   - Camina un poco más lejos de fuera de su casa, hacia el **claro profundo del bosque** a la izquierda.
   - Habla con **Zaiko** para iniciar su diálogo y enfrentarte al enemigo más poderoso del post-game.
