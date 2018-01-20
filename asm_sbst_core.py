import logging
from random import randint

TYPE_RR = 0
TYPE_R = 1
TYPE_RI = 2
TYPE_RS = 3
TYPE_RRS = 4
TYPE_RSS = 5
TYPE_R6 = 6
TYPE_I = 7
TYPE_6 = 8
TYPE_D = 9

DEFAULT_ITER = 4

TEMPLATE_RR = ('    lui x1,%hi(inputs)\n'
               '    addi x1,x1,%lo(inputs)\n'
               '    lui x2,%hi(outputs)\n'
               '    addi x2,x2,%lo(outputs)\n'
               '    lp.setupi x0,<<ITERS>>,insn_loop<<INDEX>>\n'
               '    lw <<ra>>,0(x1)\n'
               '    lw <<rb>>,4(x1)\n'
               '    addi x1,x1,4\n'
               '    <<OPCODE>> <<rd>>,<<ra>>,<<rb>>\n'
               '    p.sw <<rd>>,0(x2)\n'
               'insn_loop<<INDEX>>:\n'
               '    addi x2,x2,4\n\n')

TEMPLATE_R  = ('    lui x1,%hi(inputs)\n'
               '    addi x1,x1,%lo(inputs)\n'
               '    lui x2,%hi(outputs)\n'
               '    addi x2,x2,%lo(outputs)\n'
               '    lp.setupi x0,<<ITERS>>,insn_loop<<INDEX>>\n'
               '    lw <<ra>>,0(x1)\n'
               '    addi x1,x1,4\n'
               '    <<OPCODE>> <<rd>>,<<ra>>\n'
               '    p.sw <<rd>>,0(x2)\n'
               'insn_loop<<INDEX>>:\n'
               '    addi x2,x2,4\n\n')

TEMPLATE_RI = ('    lui x1,%hi(inputs)\n'
               '    addi x1,x1,%lo(inputs)\n'
               '    lui x2,%hi(outputs)\n'
               '    addi x2,x2,%lo(outputs)\n'
               '    lp.setupi x0,<<ITERS>>,insn_loop<<INDEX>>\n'
               '    lw <<ra>>,0(x1)\n'
               '    addi x1,x1,4\n'
               '    <<OPCODE>> <<rd>>,<<ra>>,<<IMM>>\n'
               '    p.sw <<rd>>,0(x2)\n'
               'insn_loop<<INDEX>>:\n'
               '    addi x2,x2,4\n\n')

TEMPLATE_RSS= ('    lui x1,%hi(inputs)\n'
               '    addi x1,x1,%lo(inputs)\n'
               '    lui x2,%hi(outputs)\n'
               '    addi x2,x2,%lo(outputs)\n'
               '    lp.setupi x0,<<ITERS>>,insn_loop<<INDEX>>\n'
               '    lw <<ra>>,0(x1)\n'
               '    addi x1,x1,4\n'
               '    <<OPCODE>> <<rd>>,<<ra>>,<<IMM1>>,<<IMM2>>\n'
               '    p.sw <<rd>>,0(x2)\n'
               'insn_loop<<INDEX>>:\n'
               '    addi x2,x2,4\n\n')

TEMPLATE_RRS= ('    lui x1,%hi(inputs)\n'
               '    addi x1,x1,%lo(inputs)\n'
               '    lui x2,%hi(outputs)\n'
               '    addi x2,x2,%lo(outputs)\n'
               '    lp.setupi x0,<<ITERS>>,insn_loop<<INDEX>>\n'
               '    lw <<ra>>,0(x1)\n'
               '    lw <<rb>>,4(x1)\n'
               '    addi x1,x1,4\n'
               '    <<OPCODE>> <<rd>>,<<ra>>,<<rb>>,<<IMM>>\n'
               '    p.sw <<rd>>,0(x2)\n'
               'insn_loop<<INDEX>>:\n'
               '    addi x2,x2,4\n\n')

TEMPLATE_I  = ('    lui x2,%hi(outputs)\n'
               '    addi x2,x2,%lo(outputs)\n'
               '    lp.setupi x0,<<ITERS>>,insn_loop<<INDEX>>\n'
               '    <<OPCODE>> <<rd>>,<<IMM>>\n'
               '    p.sw <<rd>>,0(x2)\n'
               'insn_loop<<INDEX>>:\n'
               '    addi x2,x2,4\n\n')

TEMPLATE_D  = ('    lui x2,%hi(outputs)\n'
               '    addi x2,x2,%lo(outputs)\n'
               '    lp.setupi x0,<<ITERS>>,insn_loop<<INDEX>>\n'
               '    <<OPCODE>> <<rd>>\n'
               '    p.sw <<rd>>,0(x2)\n'
               'insn_loop<<INDEX>>:\n'
               '    addi x2,x2,4\n\n')

BLOCK_HEADER = ('    ##################################################\n'
                '    ##    <<BLOCK>>\n'
                '    ##################################################\n'
                '    # {{{\n'
                '#ifdef <<PREFIX>>_TEST\n\n')

BLOCK_FOOTER = ('#endif\n'
                '    # }}}\n\n')

STD_REGS = ["x3","x4","x5","x6","x7","x8","x9","x10","x11","x12","x13","x14","x15","x16","x17","x18","x19","x20","x21","x22","x23","x24","x25","x26","x27","x28","x29","x30","x31"]
CMP_REGS = ["x8","x9","x10","x11","x12","x13","x14","x15"]

def get_reg(index, compressed):
    if not compressed:
        x = index % len(STD_REGS)
        return STD_REGS[x]
    else:
        x = index % len(CMP_REGS)
        return CMP_REGS[x]

class SBST():
    def __init__(self, template_file):
        self.body_str = ""
        self.template_str = open(template_file, 'r').read()
        self.block_list = list()
        self.index = 0
        self.iter = DEFAULT_ITER
        self.max_iter = DEFAULT_ITER

    def __get_prefix(self):
        if self.curr_prefix:
            return self.curr_prefix
        else:
            logging.error("Prefix not set!")
            exit()

    def block_begin(self, name, prefix):
        header_str = BLOCK_HEADER.replace("<<BLOCK>>", name)
        header_str = header_str.replace("<<PREFIX>>", prefix)
        self.body_str += header_str
        self.curr_prefix = prefix
        self.block_list.append(prefix)

    def block_end(self):
        self.body_str += BLOCK_FOOTER
        self.curr_prefix = None

    def add_instr(self, opcode, insn_type, signed=True, compressed=False):
        if insn_type == TYPE_R:
            # Register-Register instruction
            tmp = TEMPLATE_R
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
        elif insn_type == TYPE_RR:
            tmp = TEMPLATE_RR
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
            tmp = tmp.replace("<<rb>>", get_reg(self.index+2, compressed))
        elif insn_type == TYPE_RI:
            # Register-Immediate instruction
            if signed:
                imm = str(randint(-2**11, 2*11-1))
            else:
                imm = str(randint(0, 2**12-1))
            tmp = TEMPLATE_RI
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
            tmp = tmp.replace("<<IMM>>", imm)
        elif insn_type == TYPE_RSS:
            # Register-ShortImm-ShortImm instruction
            imm1 = str(randint(0, 31))
            imm2 = str(randint(0, 31))
            tmp = TEMPLATE_RSS
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
            tmp = tmp.replace("<<IMM1>>", imm1)
            tmp = tmp.replace("<<IMM2>>", imm2)
        elif insn_type == TYPE_RS:
            # Register-ShortImm instruction
            imm = str(randint(0, 31))
            tmp = TEMPLATE_RI
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
            tmp = tmp.replace("<<IMM>>", imm)
        elif insn_type == TYPE_RRS:
            # Register-Register-ShortImm instruction
            imm = str(randint(0, 31))
            tmp = TEMPLATE_RRS
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
            tmp = tmp.replace("<<rb>>", get_reg(self.index+2, compressed))
            tmp = tmp.replace("<<IMM>>", imm)
        elif insn_type == TYPE_R6:
            # Register-6Imm instruction
            if signed:
                imm = str(randint(-2**5,2**5-1))
            else:
                imm = str(randint(0,2**6-1))
            tmp = TEMPLATE_RI
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
            tmp = tmp.replace("<<IMM>>", imm)
        elif insn_type == TYPE_6:
            # 6Imm instruction
            if signed:
                imm = str(randint(-2**5,2**5-1))
            else:
                imm = str(randint(0,2**6-1))
            tmp = TEMPLATE_I
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<IMM>>", imm)
        elif insn_type == TYPE_I:
            # Immediate instruction
            if signed:
                imm = str(randint(-2**11, 2*11-1))
            else:
                imm = str(randint(0, 2**12-1))
            tmp = TEMPLATE_I
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<IMM>>", imm)
        elif insn_type == TYPE_D:
            # Destination only istruction
            tmp = TEMPLATE_D
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
        else:
            logging.error("Instruction %s is of unknown type %d", opcode, insn_type)
            exit()

        # Check that something was added
        if not tmp:
            logging.error("Instruction %s not parsed correctly!", opcode)
            exit()

        tmp = tmp.replace("<<INDEX>>", str(self.index))
        tmp = tmp.replace("<<OPCODE>>", opcode)
        tmp = tmp.replace("<<ITERS>>", str(self.iter))

        self.body_str += tmp
        self.index += 1

    def get_body(self):
        # Generate config
        config = ""
        for block in self.block_list:
            config += "#define " + block + "_TEST\n"
        tmp = self.template_str.replace("<<CONFIG>>", config)
        # Generate inputs
        inputs_cnt = self.max_iter+1
        inputs = ""
        for i in range(0,inputs_cnt):
            inputs+="    .word " + str(randint(0,2**32-1)) + "\n"
        tmp = tmp.replace("<<INPUTS>>", inputs)
        tmp = tmp.replace("<<INPUTS_SIZE>>", str(inputs_cnt*4))
        return tmp.replace("<<BODY>>", self.body_str)

    def set_iterations(self, x):
        self.iter = x
        if x > self.max_iter:
            self.max_iter = x
