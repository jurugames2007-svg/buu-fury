@ ==============================================================================
@ ai_whis_trial.s — Whis Divine Master Trial Ultra Instinct Auto-Dodge Check
@ ==============================================================================
    .thumb
    .syntax unified
    .global AI_Whis_Main

AI_Whis_Main:
    push    {r4-r6, lr}
    mov     r4, r0                  @ r4 = Whis Struct
    
    @ Check Player Current Form ID (RAM 0x02024A00)
    ldr     r5, =0x02024A00
    ldrb    r6, [r5, #0x04]         @ r6 = Player Form ID
    cmp     r6, #6                  @ Is Player in Super Saiyan God (ID 6)?
    beq     Allow_Hit
    cmp     r6, #0x1B               @ Is Player in Gogeta SSJ4 (ID 0x1B)?
    beq     Allow_Hit

    @ Ultra Instinct Auto-Dodge -> Evade 100% of damage
    mov     r0, #1
    strb    r0, [r4, #0x22]         @ Dodge Flag = TRUE
    b       AI_Whis_End

Allow_Hit:
    mov     r0, #0
    strb    r0, [r4, #0x22]         @ Dodge Flag = FALSE

AI_Whis_End:
    pop     {r4-r6, pc}
