@ ==============================================================================
@ ai_zaiko_boss.s — AF Secret Boss Zaiko High-Speed Afterimage & Dimension Ripper
@ ==============================================================================
    .thumb
    .syntax unified
    .global AI_Zaiko_Main

AI_Zaiko_Main:
    push    {r4, lr}
    mov     r4, r0                  @ r4 = Zaiko Struct
    
    @ High-speed dash with afterimage trail
    mov     r0, #5                  @ Speed boost multiplier
    strb    r0, [r4, #0x0E]
    mov     r0, #0x4D               @ Skill ID = Dimension Ripper
    bl      Execute_Afterimage_Strike
    
    pop     {r4, pc}
