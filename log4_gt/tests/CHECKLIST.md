# Automated verification checklist

## Structural (passed by builder)
- [x] SS3 struct/name/skill/palette == original
- [x] Form 1 has SSJ3 anims + SSJ4 palette
- [x] Hook only grants on NPC type 81
- [x] Snakeway keeps 12 original NPCs + East Kai
- [x] Checksum valid
- [x] 16MB ROM

## Manual mGBA tests
1. Boot ROM — title screen OK
2. New Game — Other World / Snake Way
3. Find East Kai (sprite East Kai, not King Kai)
4. Talk — skills granted, form becomes SSJ4 (red fur)
5. Menu Skills — Super Saiyan present; SS3 skill still named Super Saiyan 3
6. Transform SS (skill) — gold SS1 works
7. Transform SS3 — long hair gold SS3 works (NOT red)
8. Re-talk East Kai — return to SSJ4 red fur
9. King Kai dialogue still normal text
10. No crash after 10 NPC talks
