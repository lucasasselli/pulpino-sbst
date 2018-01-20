# vim:ft=riscv32asm

HWLOOP_ITER=32
.comm	mem_dump HWLOOP_ITER*4,4
.text
.align	2
.globl  hwloop_test
.type   hwloop_test , @function
hwloop_test:
    li a0,1
    lp.setupi x1,HWLOOP_ITER,hwloop0
    slli a0,a0,1
    add a1,x0,a0
    lui a3,%hi(mem_dump)
    addi a3,a3,%lo(mem_dump)
    lp.setupi x0,HWLOOP_ITER,hwloop0
    lw a2,0(a1)
    sw a2,0(a3)
    add a3,a3,4
hwloop0:
    addi a1,a1,4
    jr ra
