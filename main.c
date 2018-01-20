//
// RISC-V Software based self-test
//
// Author:  Luca Sasselli
// Rev:     4
//

extern int rf_march_c(void);
extern int csr_march_c(void);
extern int mem_test(void);
extern int insn_test(void);


int main(){

    rf_march_c();  // Test Register File
    csr_march_c(); // Test CSR
    mem_test();    // Test Hardware Loops
    insn_test();   // Test Instructions

    return 0;
}
