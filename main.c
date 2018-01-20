//
// RISC-V Software based self-test
//
// Author:  Luca Sasselli
// Rev:     3
//

extern int rf_march_c(void);
extern int csr_march_c(void);
extern int hwloop_test(void);
extern int insn_test(void);


int main(){

    rf_march_c();      // Test Register File
    csr_march_c();     // Test CSR
    hwloop_test();     // Test Hardware Loops
    insn_test();       // Test Instructions

    return 0;
}
