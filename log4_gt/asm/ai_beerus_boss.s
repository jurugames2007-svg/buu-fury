@ ==============================================================================
@ ai_beerus_boss.s — God of Destruction Beerus 3-Phase Boss AI (Thumb / ARM7)
@ Target ROM: Dragon Ball Z: Buu's Fury (USA) — Hooked at Enemy AI Table (0x0807XXXX)
@ ==============================================================================
    .thumb
    .syntax unified
    .global AI_Beerus_Main

AI_Beerus_Main:
    push    {r4-r7, lr}
    mov     r4, r0                  @ r4 = Pointer to Beerus Enemy Struct
    ldr     r1, [r4, #0x24]         @ r1 = Current HP
    ldr     r2, [r4, #0x28]         @ r2 = Max HP
    
    @ Check Phase 3 Threshold (< 25% HP) -> Trigger Telegraphed Hakai
    lsr     r3, r2, #2              @ r3 = Max HP / 4 (25% threshold)
    cmp     r1, r3
    blt     Phase3_Hakai_Telegraph

    @ Check Phase 2 Threshold (< 50% HP) -> Z-Axis Flight + Cataclysmic Orbs
    lsr     r3, r2, #1              @ r3 = Max HP / 2 (50% threshold)
    cmp     r1, r3
    blt     Phase2_BulletHell

Phase1_Melee_Teleport:
    mov     r0, #1                  @ AI State = High-Speed Melee
    bl      Execute_Teleport_Strike
    b       AI_Beerus_End

Phase2_BulletHell:
    mov     r0, #0x20               @ Elevate Z-axis (+32 pixels height)
    strb    r0, [r4, #0x12]
    mov     r0, #0x5C               @ Skill ID = Cataclysmic Orb (0x5C)
    bl      Spawn_BulletHell_Orbs
    b       AI_Beerus_End

Phase3_Hakai_Telegraph:
    @ 1. Display 2-second visual Telegraph around Beerus
    mov     r0, #0xFF               @ Red Telegraph Aura color
    strb    r0, [r4, #0x1E]
    
    @ 2. Check if Player has Beerus's Pudding Active (RAM flag 0x0202E500)
    ldr     r5, =0x0202E500         @ r5 = Player Active Buffs RAM
    ldrb    r6, [r5, #0x08]         @ r6 = Pudding Divine Shield flag
    cmp     r6, #1
    beq     Hakai_Nullified

    @ 3. Execute Hakai (0x5A) -> Instant KO if unprotected
    mov     r0, #0x5A               @ Skill ID = Hakai
    bl      Execute_Destruction_Wave
    b       AI_Beerus_End

Hakai_Nullified:
    @ Pudding Shield active -> Hakai damage reduced by 100%
    mov     r0, #0
    bl      Execute_Destruction_Wave

AI_Beerus_End:
    pop     {r4-r7, pc}
