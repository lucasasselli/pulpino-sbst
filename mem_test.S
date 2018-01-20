# vim:ft=riscv32asm:foldmethod=marker:foldlevel=0

MEM_ITER=32

.comm	mem_dump MEM_ITER*4,4
.text
.align	2
.globl  mem_test
.type   mem_test , @function

mem_test:

    ################################################## 
    # DEEP ADDRESS TEST
    ################################################## 
    # {{{
    li a0,1
    lp.setupi x1,MEM_ITER,deep_loop
    slli a0,a0,1
    add a1,x0,a0
    lui a3,%hi(mem_dump)
    addi a3,a3,%lo(mem_dump)
    lp.setupi x0,MEM_ITER,deep_loop
    lw a2,0(a1)
    sw a2,0(a3)
    add a3,a3,4
deep_loop:
    addi a1,a1,4
    jr ra
    # }}}
