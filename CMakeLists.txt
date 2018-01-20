set(SOURCES fail.S insn_test.S mem_test.S rf_march_c.S csr_march_c.S main.c)
add_application(rv_polito    "${SOURCES}" LABELS riscv_tests)

