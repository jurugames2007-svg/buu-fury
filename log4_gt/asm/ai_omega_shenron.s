@ ==============================================================================
@ ai_omega_shenron.s — GT Shadow Dragons Climax AI & Gogeta SSJ4 Unlock Check
@ ==============================================================================
    .thumb
    .syntax unified
    .global AI_OmegaShenron_Main

AI_OmegaShenron_Main:
    push    {r4-r6, lr}
    mov     r4, r0                  @ r4 = Omega Shenron Struct
    
    @ 1. Spawn Negative Energy Lightning Storm around Player
    bl      Spawn_Negative_Lightning_Storm
    
    @ 2. Check if Goku & Vegeta are in Party -> Enable Metamoran Fusion Option
    ldr     r5, =0x02024E00         @ Party state RAM
    ldrb    r6, [r5, #0x10]         @ Fusion Available Flag
    mov     r0, #1
    strb    r0, [r5, #0x10]         @ Enable Gogeta SSJ4 (Form ID 0x1B) unlock
    
    pop     {r4-r6, pc}
