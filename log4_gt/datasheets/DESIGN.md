# The Legacy of Goku 4 — GT DLC Design

## Activation
Walk **Snake Way** at game start → talk to **East Kai** (new NPC, does not replace King Kai).

## Forms (no interference)
| Priority | Form | Slot | Status |
|----------|------|------|--------|
| 1 (strongest) | **Super Saiyan 4** | Form ID **1** (GT slot) | NEW |
| 2 | Super Saiyan 3 | Form ID 5 | **ORIGINAL restored** |
| 3 | Super Saiyan | Form ID 3 | Original |
| 4 | Base | Form ID 0 | Original |

## Skills after East Kai
- Instant Transmission, Kamehameha, Super Saiyan
- Super Saiyan 4 (enters form 1)
- Planned kit: **10x Kamehameha**, **Dragon Fist** (data + icons ready)

## GT Sagas (mission structure)
### 1. Grand Tour (eps 1-16)
Exploration, Black Star balls, Imecka, Luud, M2.
### 2. Baby (eps 17-40)
Possession arc, Golden Oozaru, **SSJ4 birth**, Baby defeat.
### 3. Super 17 (eps 41-47)
Hell siege, Super 17, **Dragon Fist**.
### 4. Shadow Dragons (eps 48-64)
Boss rush, Omega Shenron, Gogeta SSJ4, Universal Spirit Bomb.

## How SSJ4 works in-engine
- Separate character struct (form 1), full SSJ3-class animations
- Unique red-fur palette (SS3 gold palette untouched)
- Unlock ONLY by East Kai on Snakeway (type-check in hook)
- Talking again re-applies SSJ4 form if you switched away
