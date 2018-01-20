# vim:ft=riscv32asm

.globl  fail
.globl  csr_march_c
.type   csr_march_c , @function

csr_march_c:
    # Write 0
    csrw 0x341,x0
    csrw 0x780,x0
    csrw 0x781,x0
    csrw 0x782,x0
    csrw 0x783,x0
    csrw 0x784,x0
    csrw 0x785,x0
    csrw 0x786,x0
    csrw 0x787,x0
    csrw 0x788,x0
    csrw 0x789,x0
    csrw 0x78a,x0
    csrw 0x78b,x0

    # Read 0 write 1
    li a1,-1
    csrr a0,0x341
    bne x0,a0,fail
    csrw 0x341,a1
    csrr a0,0x780
    bne x0,a0,fail
    csrw 0x780,a1
    csrr a0,0x781
    bne x0,a0,fail
    csrw 0x781,a1
    csrr a0,0x782
    bne x0,a0,fail
    csrw 0x782,a1
    csrr a0,0x783
    bne x0,a0,fail
    csrw 0x783,a1
    csrr a0,0x784
    bne x0,a0,fail
    csrw 0x784,a1
    csrr a0,0x785
    bne x0,a0,fail
    csrw 0x785,a1
    csrr a0,0x786
    bne x0,a0,fail
    csrw 0x786,a1
    csrr a0,0x787
    bne x0,a0,fail
    csrw 0x787,a1
    csrr a0,0x788
    bne x0,a0,fail
    csrw 0x788,a1
    csrr a0,0x789
    bne x0,a0,fail
    csrw 0x789,a1
    csrr a0,0x78a
    bne x0,a0,fail
    csrw 0x78a,a1
    csrr a0,0x78b
    bne x0,a0,fail
    csrw 0x78b,a1

    # Read 1 write 0
    li a1,-1
    csrr a0,0x341
    bne a1,a0,fail
    csrw 0x341,x0
    csrr a0,0x780
    bne a1,a0,fail
    csrw 0x780,x0
    csrr a0,0x781
    bne a1,a0,fail
    csrw 0x781,x0
    csrr a0,0x782
    bne a1,a0,fail
    csrw 0x782,x0
    csrr a0,0x783
    bne a1,a0,fail
    csrw 0x783,x0
    csrr a0,0x784
    bne a1,a0,fail
    csrw 0x784,x0
    csrr a0,0x785
    bne a1,a0,fail
    csrw 0x785,x0
    csrr a0,0x786
    bne a1,a0,fail
    csrw 0x786,x0
    csrr a0,0x787
    bne a1,a0,fail
    csrw 0x787,x0
    csrr a0,0x788
    bne a1,a0,fail
    csrw 0x788,x0
    csrr a0,0x789
    bne a1,a0,fail
    csrw 0x789,x0
    csrr a0,0x78a
    bne a1,a0,fail
    csrw 0x78a,x0
    csrr a0,0x78b
    bne a1,a0,fail
    csrw 0x78b,x0

    # Read 0
    csrr a0,0x341
    bne x0,a0,fail
    csrr a0,0x780
    bne x0,a0,fail
    csrr a0,0x781
    bne x0,a0,fail
    csrr a0,0x782
    bne x0,a0,fail
    csrr a0,0x783
    bne x0,a0,fail
    csrr a0,0x784
    bne x0,a0,fail
    csrr a0,0x785
    bne x0,a0,fail
    csrr a0,0x786
    bne x0,a0,fail
    csrr a0,0x787
    bne x0,a0,fail
    csrr a0,0x788
    bne x0,a0,fail
    csrr a0,0x789
    bne x0,a0,fail
    csrr a0,0x78a
    bne x0,a0,fail
    csrr a0,0x78b
    bne x0,a0,fail

    
    jr ra
