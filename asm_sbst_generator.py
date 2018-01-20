from random import randint

TYPE_RR = 0
TYPE_R = 1
TYPE_RI = 2
TYPE_RS = 3
TYPE_RRS = 4
TYPE_RSS = 5
TYPE_R6 = 6
TYPE_6 = 7

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

TEMPLATE_6  = ('    lui x2,%hi(outputs)\n'
               '    addi x2,x2,%lo(outputs)\n'
               '    lp.setupi x0,<<ITERS>>,insn_loop<<INDEX>>\n'
               '    lw <<ra>>,0(x1)\n'
               '    <<OPCODE>> <<rd>>,<<IMM>>\n'
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
            print "No prefix set!"
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
            tmp = TEMPLATE_R
            tmp = tmp.replace("<<INDEX>>", str(self.index))
            tmp = tmp.replace("<<OPCODE>>", opcode)
            tmp = tmp.replace("<<ITERS>>", str(self.iter))
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
            self.body_str += tmp
        elif insn_type == TYPE_RR:
            tmp = TEMPLATE_RR
            tmp = tmp.replace("<<INDEX>>", str(self.index))
            tmp = tmp.replace("<<OPCODE>>", opcode)
            tmp = tmp.replace("<<ITERS>>", str(self.iter))
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
            tmp = tmp.replace("<<rb>>", get_reg(self.index+2, compressed))
            self.body_str += tmp
        elif insn_type == TYPE_RI:
            if signed:
                imm = str(randint(-2048, 2047))
            else:
                imm = str(randint(0, 4095))
            tmp = TEMPLATE_RI
            tmp = tmp.replace("<<INDEX>>", str(self.index))
            tmp = tmp.replace("<<OPCODE>>", opcode)
            tmp = tmp.replace("<<ITERS>>", str(self.iter))
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
            tmp = tmp.replace("<<IMM>>", imm)
            self.body_str += tmp
        elif insn_type == TYPE_RSS:
            imm1 = str(randint(0, 31))
            imm2 = str(randint(0, 31))
            tmp = TEMPLATE_RSS
            tmp = tmp.replace("<<INDEX>>", str(self.index))
            tmp = tmp.replace("<<OPCODE>>", opcode)
            tmp = tmp.replace("<<ITERS>>", str(self.iter))
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
            tmp = tmp.replace("<<IMM1>>", imm1)
            tmp = tmp.replace("<<IMM2>>", imm2)
            self.body_str += tmp
        elif insn_type == TYPE_RS:
            imm = str(randint(0, 31))
            tmp = TEMPLATE_RI
            tmp = tmp.replace("<<INDEX>>", str(self.index))
            tmp = tmp.replace("<<OPCODE>>", opcode)
            tmp = tmp.replace("<<ITERS>>", str(self.iter))
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
            tmp = tmp.replace("<<IMM>>", imm)
        elif insn_type == TYPE_RRS:
            imm = str(randint(0, 31))
            tmp = TEMPLATE_RRS
            tmp = tmp.replace("<<INDEX>>", str(self.index))
            tmp = tmp.replace("<<OPCODE>>", opcode)
            tmp = tmp.replace("<<ITERS>>", str(self.iter))
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
            tmp = tmp.replace("<<rb>>", get_reg(self.index+2, compressed))
            tmp = tmp.replace("<<IMM>>", imm)
            self.body_str += tmp
        elif insn_type == TYPE_R6:
            if signed:
                imm = str(randint(-32,31))
            else:
                imm = str(randint(0,63))
            tmp = TEMPLATE_RI
            tmp = tmp.replace("<<INDEX>>", str(self.index))
            tmp = tmp.replace("<<OPCODE>>", opcode)
            tmp = tmp.replace("<<ITERS>>", str(self.iter))
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<ra>>", get_reg(self.index+1, compressed))
            tmp = tmp.replace("<<IMM>>", imm)
            self.body_str += tmp
        elif insn_type == TYPE_6:
            if signed:
                imm = str(randint(-32,31))
            else:
                imm = str(randint(0,63))
            tmp = TEMPLATE_6
            tmp = tmp.replace("<<INDEX>>", str(self.index))
            tmp = tmp.replace("<<OPCODE>>", opcode)
            tmp = tmp.replace("<<ITERS>>", str(self.iter))
            tmp = tmp.replace("<<rd>>", get_reg(self.index, compressed))
            tmp = tmp.replace("<<IMM>>", imm)
            self.body_str += tmp
        else:
            print "Error! Unknown type for opcode " + opcode
            exit()
        self.index += 1

    def get_body(self):
        # Generate config
        config = ""
        for block in self.block_list:
            config += "#define " + block + "_TEST\n"
        config += "\n"
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
            max_iter = x


# Read template
sbst = SBST("template_asm.txt")

sbst.block_begin("Base Instruction Set", "RV32I")
sbst.set_iterations(16)
sbst.add_instr("auipc", TYPE_RI)
sbst.add_instr("lui", TYPE_RI)
sbst.add_instr("addi", TYPE_RI)
sbst.add_instr("slti", TYPE_RS)
sbst.add_instr("sltiu", TYPE_RS)
sbst.add_instr("xori", TYPE_RI)
sbst.add_instr("ori", TYPE_RI)
sbst.add_instr("andi", TYPE_RI)
sbst.add_instr("slli", TYPE_RS)
sbst.add_instr("srli", TYPE_RS)
sbst.add_instr("srai", TYPE_RS)
sbst.add_instr("add", TYPE_RR)
sbst.add_instr("sub", TYPE_RR)
sbst.add_instr("sll", TYPE_RR)
sbst.add_instr("slt", TYPE_RR)
sbst.add_instr("sltu", TYPE_RR)
sbst.add_instr("xor", TYPE_RR)
sbst.add_instr("srl", TYPE_RR)
sbst.add_instr("sra", TYPE_RR)
sbst.add_instr("or", TYPE_RR)
sbst.add_instr("and", TYPE_RR)
sbst.add_instr("rdcycle", TYPE_R)
sbst.add_instr("rdcycleh", TYPE_R)
sbst.add_instr("rdtime", TYPE_R)
sbst.add_instr("rdtimeh", TYPE_R)
sbst.add_instr("rdinstret", TYPE_R)
sbst.add_instr("rdinstreth", TYPE_R)
sbst.block_end()

sbst.block_begin("Standard Extension", "RV32M")
sbst.set_iterations(16)
sbst.add_instr("mul", TYPE_RR)
sbst.add_instr("mulh", TYPE_RR)
sbst.add_instr("mulhsu", TYPE_RR)
sbst.add_instr("mulhu", TYPE_RR)
sbst.add_instr("div", TYPE_RR)
sbst.add_instr("divu", TYPE_RR)
sbst.add_instr("rem", TYPE_RR)
sbst.add_instr("remu", TYPE_RR)
sbst.block_end()

sbst.block_begin("ALU Bitwise Extension", "RVCY_ALU1")
sbst.set_iterations(4)
sbst.add_instr("p.extract", TYPE_RSS)
sbst.add_instr("p.extractu", TYPE_RSS)
sbst.add_instr("p.insert", TYPE_RSS)
sbst.add_instr("p.bclr", TYPE_RSS)
sbst.add_instr("p.bset", TYPE_RSS)
sbst.add_instr("p.extractr", TYPE_RR)
sbst.add_instr("p.extractur", TYPE_RR)
sbst.add_instr("p.insertr", TYPE_RR)
sbst.add_instr("p.bclrr", TYPE_RR)
sbst.add_instr("p.bsetr", TYPE_RR)
sbst.add_instr("p.ror", TYPE_RR)
sbst.add_instr("p.ff1", TYPE_R)
sbst.add_instr("p.fl1", TYPE_R)
sbst.add_instr("p.clb", TYPE_R)
sbst.add_instr("p.cnt", TYPE_R)
sbst.block_end()

sbst.block_begin("ALU General Extension", "RVCY_ALU2")
sbst.set_iterations(4)
sbst.add_instr("p.abs", TYPE_R)
sbst.add_instr("p.slet", TYPE_RR)
sbst.add_instr("p.sletu", TYPE_RR)
sbst.add_instr("p.min", TYPE_RR)
sbst.add_instr("p.minu", TYPE_RR)
sbst.add_instr("p.max", TYPE_RR)
sbst.add_instr("p.maxu", TYPE_RR)
sbst.add_instr("p.exths", TYPE_R)
sbst.add_instr("p.exthz", TYPE_R)
sbst.add_instr("p.extbs", TYPE_R)
sbst.add_instr("p.extbz", TYPE_R)
sbst.add_instr("p.clip", TYPE_RS)
sbst.add_instr("p.clipr", TYPE_RR)
sbst.add_instr("p.clipu", TYPE_RS)
sbst.add_instr("p.clipur", TYPE_RR)
sbst.add_instr("p.addN", TYPE_RRS)
sbst.add_instr("p.adduN", TYPE_RRS)
sbst.add_instr("p.addRN", TYPE_RRS)
sbst.add_instr("p.adduRN", TYPE_RRS)
sbst.add_instr("p.subN", TYPE_RRS)
sbst.add_instr("p.subuN", TYPE_RRS)
sbst.add_instr("p.subRN", TYPE_RRS)
sbst.add_instr("p.subuRN", TYPE_RRS)
sbst.add_instr("p.addNr", TYPE_RR)
sbst.add_instr("p.adduNr", TYPE_RR)
sbst.add_instr("p.addRNr", TYPE_RR)
sbst.add_instr("p.adduRNr", TYPE_RR)
sbst.add_instr("p.subNr", TYPE_RR)
sbst.add_instr("p.subuNr", TYPE_RR)
sbst.add_instr("p.subRNr", TYPE_RR)
sbst.add_instr("p.subuRNr", TYPE_RR)
sbst.block_end()

sbst.block_begin("MAC Extension", "RVCY_MAC")
sbst.set_iterations(4)
sbst.add_instr("p.mac", TYPE_RR)
sbst.add_instr("p.msu", TYPE_RR)
sbst.add_instr("p.muls", TYPE_RR)
sbst.add_instr("p.mulhhs", TYPE_RR)
sbst.add_instr("p.mulsN", TYPE_RRS)
sbst.add_instr("p.mulhhsN", TYPE_RRS)
sbst.add_instr("p.mulsRN", TYPE_RRS)
sbst.add_instr("p.mulhhsRN", TYPE_RRS)
sbst.add_instr("p.mulu", TYPE_RR)
sbst.add_instr("p.mulhhu", TYPE_RR)
sbst.add_instr("p.muluN", TYPE_RRS)
sbst.add_instr("p.mulhhuN", TYPE_RRS)
sbst.add_instr("p.muluRN", TYPE_RRS)
sbst.add_instr("p.mulhhuRN", TYPE_RRS)
sbst.add_instr("p.macsN", TYPE_RRS)
sbst.add_instr("p.machhsN", TYPE_RRS)
sbst.add_instr("p.macsRN", TYPE_RRS)
sbst.add_instr("p.machhsRN", TYPE_RRS)
sbst.add_instr("p.macuN", TYPE_RRS)
sbst.add_instr("p.machhuN", TYPE_RRS)
sbst.add_instr("p.macuRN", TYPE_RRS)
sbst.add_instr("p.machhuRN", TYPE_RRS)
sbst.block_end()

sbst.block_begin("Vectorial Extension", "RVCY_VEC1")
sbst.set_iterations(4)
sbst.add_instr("pv.add.h", TYPE_RR)
sbst.add_instr("pv.add.sc.h", TYPE_RR)
sbst.add_instr("pv.add.sci.h", TYPE_R6)
sbst.add_instr("pv.add.b", TYPE_RR)
sbst.add_instr("pv.add.sc.b", TYPE_RR)
sbst.add_instr("pv.add.sci.b", TYPE_R6)
sbst.add_instr("pv.sub.h", TYPE_RR)
sbst.add_instr("pv.sub.sc.h", TYPE_RR)
sbst.add_instr("pv.sub.sci.h", TYPE_R6)
sbst.add_instr("pv.sub.b", TYPE_RR)
sbst.add_instr("pv.sub.sc.b", TYPE_RR)
sbst.add_instr("pv.sub.sci.b", TYPE_R6)
sbst.add_instr("pv.avg.h", TYPE_RR)
sbst.add_instr("pv.avg.sc.h", TYPE_RR)
sbst.add_instr("pv.avg.sci.h", TYPE_R6)
sbst.add_instr("pv.avg.b", TYPE_RR)
sbst.add_instr("pv.avg.sc.b", TYPE_RR)
sbst.add_instr("pv.avg.sci.b", TYPE_R6)
sbst.add_instr("pv.avgu.h", TYPE_RR)
sbst.add_instr("pv.avgu.sc.h", TYPE_RR)
sbst.add_instr("pv.avgu.sci.h", TYPE_R6, False)
sbst.add_instr("pv.avgu.b", TYPE_RR)
sbst.add_instr("pv.avgu.sc.b", TYPE_RR)
sbst.add_instr("pv.avgu.sci.b", TYPE_R6, False)
sbst.add_instr("pv.min.h", TYPE_RR)
sbst.add_instr("pv.min.sc.h", TYPE_RR)
sbst.add_instr("pv.min.sci.h", TYPE_R6)
sbst.add_instr("pv.min.b", TYPE_RR)
sbst.add_instr("pv.min.sc.b", TYPE_RR)
sbst.add_instr("pv.min.sci.b", TYPE_R6)
sbst.add_instr("pv.minu.h", TYPE_RR)
sbst.add_instr("pv.minu.sc.h", TYPE_RR)
sbst.add_instr("pv.minu.sci.h", TYPE_R6, False)
sbst.add_instr("pv.minu.b", TYPE_RR)
sbst.add_instr("pv.minu.sc.b", TYPE_RR)
sbst.add_instr("pv.minu.sci.b", TYPE_R6, False)
sbst.add_instr("pv.max.h", TYPE_RR)
sbst.add_instr("pv.max.sc.h", TYPE_RR)
sbst.add_instr("pv.max.sci.h", TYPE_R6)
sbst.add_instr("pv.max.b", TYPE_RR)
sbst.add_instr("pv.max.sc.b", TYPE_RR)
sbst.add_instr("pv.max.sci.b", TYPE_R6)
sbst.add_instr("pv.maxu.h", TYPE_RR)
sbst.add_instr("pv.maxu.sc.h", TYPE_RR)
sbst.add_instr("pv.maxu.sci.h", TYPE_R6, False)
sbst.add_instr("pv.maxu.b", TYPE_RR)
sbst.add_instr("pv.maxu.sc.b", TYPE_RR)
sbst.add_instr("pv.maxu.sci.b", TYPE_R6, False)
sbst.add_instr("pv.srl.h", TYPE_RR)
sbst.add_instr("pv.srl.sc.h", TYPE_RR)
sbst.add_instr("pv.srl.sci.h", TYPE_RS)
sbst.add_instr("pv.srl.b", TYPE_RR)
sbst.add_instr("pv.srl.sc.b", TYPE_RR)
sbst.add_instr("pv.srl.sci.b", TYPE_RS)
sbst.add_instr("pv.sra.h", TYPE_RR)
sbst.add_instr("pv.sra.sc.h", TYPE_RR)
sbst.add_instr("pv.sra.sci.h", TYPE_RS)
sbst.add_instr("pv.sra.b", TYPE_RR)
sbst.add_instr("pv.sra.sc.b", TYPE_RR)
sbst.add_instr("pv.sra.sci.b", TYPE_RS)
sbst.add_instr("pv.sll.h", TYPE_RR)
sbst.add_instr("pv.sll.sc.h", TYPE_RR)
sbst.add_instr("pv.sll.sci.h", TYPE_RS)
sbst.add_instr("pv.sll.b", TYPE_RR)
sbst.add_instr("pv.sll.sc.b", TYPE_RR)
sbst.add_instr("pv.sll.sci.b", TYPE_RS)
sbst.add_instr("pv.or.h", TYPE_RR)
sbst.add_instr("pv.or.sc.h", TYPE_RR)
sbst.add_instr("pv.or.sci.h", TYPE_R6)
sbst.add_instr("pv.or.b", TYPE_RR)
sbst.add_instr("pv.or.sc.b", TYPE_RR)
sbst.add_instr("pv.or.sci.b", TYPE_R6)
sbst.add_instr("pv.xor.h", TYPE_RR)
sbst.add_instr("pv.xor.sc.h", TYPE_RR)
sbst.add_instr("pv.xor.sci.h", TYPE_R6)
sbst.add_instr("pv.xor.b", TYPE_RR)
sbst.add_instr("pv.xor.sc.b", TYPE_RR)
sbst.add_instr("pv.xor.sci.b", TYPE_R6)
sbst.add_instr("pv.and.h", TYPE_RR)
sbst.add_instr("pv.and.sc.h", TYPE_RR)
sbst.add_instr("pv.and.sci.h", TYPE_R6)
sbst.add_instr("pv.and.b", TYPE_RR)
sbst.add_instr("pv.and.sc.b", TYPE_RR)
sbst.add_instr("pv.and.sci.b", TYPE_R6)
sbst.add_instr("pv.abs.h", TYPE_R)
sbst.add_instr("pv.abs.b", TYPE_R)
# sbst.add_instr("pv.extract.h", TYPE_6, False)
# sbst.add_instr("pv.extract.b", TYPE_6, False)
# sbst.add_instr("pv.extractu.h", TYPE_6, False)
# sbst.add_instr("pv.extractu.b", TYPE_6, False)
# sbst.add_instr("pv.insert.h", TYPE_6, False)
# sbst.add_instr("pv.insert.b", TYPE_6, False)
sbst.add_instr("pv.dotup.h", TYPE_RR)
sbst.add_instr("pv.dotup.sc.h", TYPE_RR)
sbst.add_instr("pv.dotup.sci.h", TYPE_R6, False)
sbst.add_instr("pv.dotup.b", TYPE_RR)
sbst.add_instr("pv.dotup.sc.b", TYPE_RR)
sbst.add_instr("pv.dotup.sci.b", TYPE_R6, False)
sbst.add_instr("pv.dotusp.h", TYPE_RR)
sbst.add_instr("pv.dotusp.sc.h", TYPE_RR)
sbst.add_instr("pv.dotusp.sci.h", TYPE_RS)
sbst.add_instr("pv.dotusp.b", TYPE_RR)
sbst.add_instr("pv.dotusp.sc.b", TYPE_RR)
sbst.add_instr("pv.dotusp.sci.b", TYPE_RS)
sbst.add_instr("pv.dotsp.h", TYPE_RR)
sbst.add_instr("pv.dotsp.sc.h", TYPE_RR)
sbst.add_instr("pv.dotsp.sci.h", TYPE_R6)
sbst.add_instr("pv.dotsp.b", TYPE_RR)
sbst.add_instr("pv.dotsp.sc.b", TYPE_RR)
sbst.add_instr("pv.dotsp.sci.b", TYPE_R6)
sbst.add_instr("pv.sdotup.h", TYPE_RR)
sbst.add_instr("pv.sdotup.sc.h", TYPE_RR)
sbst.add_instr("pv.sdotup.sci.h", TYPE_R6, False)
sbst.add_instr("pv.sdotup.b", TYPE_RR)
sbst.add_instr("pv.sdotup.sc.b", TYPE_RR)
sbst.add_instr("pv.sdotup.sci.b", TYPE_R6, False)
sbst.add_instr("pv.sdotusp.h", TYPE_RR)
sbst.add_instr("pv.sdotusp.sc.h", TYPE_RR)
sbst.add_instr("pv.sdotusp.sci.h", TYPE_RS)
sbst.add_instr("pv.sdotusp.b", TYPE_RR)
sbst.add_instr("pv.sdotusp.sc.b", TYPE_RR)
sbst.add_instr("pv.sdotusp.sci.b", TYPE_RS)
sbst.add_instr("pv.sdotsp.h", TYPE_RR)
sbst.add_instr("pv.sdotsp.sc.h", TYPE_RR)
sbst.add_instr("pv.sdotsp.sci.h", TYPE_R6)
sbst.add_instr("pv.sdotsp.b", TYPE_RR)
sbst.add_instr("pv.sdotsp.sc.b", TYPE_RR)
sbst.add_instr("pv.sdotsp.sci.b", TYPE_R6)
sbst.add_instr("pv.shuffle.h", TYPE_RR)
sbst.add_instr("pv.shuffle.sci.h", TYPE_R6, False)
sbst.add_instr("pv.shuffle.b", TYPE_RR)
sbst.add_instr("pv.shuffleI0.sci.b", TYPE_R6, False)
sbst.add_instr("pv.shuffleI1.sci.b", TYPE_R6, False)
sbst.add_instr("pv.shuffleI2.sci.b", TYPE_R6, False)
sbst.add_instr("pv.shuffleI3.sci.b", TYPE_R6, False)
sbst.add_instr("pv.shuffle2.h", TYPE_RR)
sbst.add_instr("pv.shuffle2.b", TYPE_RR)
sbst.add_instr("pv.pack.h", TYPE_RR)
sbst.add_instr("pv.packhi.b", TYPE_RR)
sbst.add_instr("pv.packlo.b", TYPE_RR)
sbst.block_end()

sbst.block_begin("Vectorial Comparison Extension", "RVCY_VEC2")
sbst.set_iterations(4)
sbst.add_instr("pv.cmpeq.h", TYPE_RR)
sbst.add_instr("pv.cmpeq.sc.h", TYPE_RR)
sbst.add_instr("pv.cmpeq.sci.h", TYPE_RS)
sbst.add_instr("pv.cmpeq.b", TYPE_RR)
sbst.add_instr("pv.cmpeq.sc.b", TYPE_RR)
sbst.add_instr("pv.cmpne.sci.b", TYPE_RS)
sbst.add_instr("pv.cmpne.h", TYPE_RR)
sbst.add_instr("pv.cmpne.sc.h", TYPE_RR)
sbst.add_instr("pv.cmpne.sci.h", TYPE_RS)
sbst.add_instr("pv.cmpne.b", TYPE_RR)
sbst.add_instr("pv.cmpne.sc.b", TYPE_RR)
sbst.add_instr("pv.cmpne.sci.b", TYPE_RS)
sbst.add_instr("pv.cmpgt.h", TYPE_RR)
sbst.add_instr("pv.cmpgt.sc.h", TYPE_RR)
sbst.add_instr("pv.cmpgt.sci.h", TYPE_RS)
sbst.add_instr("pv.cmpgt.b", TYPE_RR)
sbst.add_instr("pv.cmpgt.sc.b", TYPE_RR)
sbst.add_instr("pv.cmpgt.sci.b", TYPE_RS)
sbst.add_instr("pv.cmpge.h", TYPE_RR)
sbst.add_instr("pv.cmpge.sc.h", TYPE_RR)
sbst.add_instr("pv.cmpge.sci.h", TYPE_RS)
sbst.add_instr("pv.cmpge.b", TYPE_RR)
sbst.add_instr("pv.cmpge.sc.b", TYPE_RR)
sbst.add_instr("pv.cmpge.sci.b", TYPE_RS)
sbst.add_instr("pv.cmplt.h", TYPE_RR)
sbst.add_instr("pv.cmplt.sc.h", TYPE_RR)
sbst.add_instr("pv.cmplt.sci.h", TYPE_RS)
sbst.add_instr("pv.cmplt.b", TYPE_RR)
sbst.add_instr("pv.cmplt.sc.b", TYPE_RR)
sbst.add_instr("pv.cmplt.sci.b", TYPE_RS)
sbst.add_instr("pv.cmple.h", TYPE_RR)
sbst.add_instr("pv.cmple.sc.h", TYPE_RR)
sbst.add_instr("pv.cmple.sci.h", TYPE_RS)
sbst.add_instr("pv.cmple.b", TYPE_RR)
sbst.add_instr("pv.cmple.sc.b", TYPE_RR)
sbst.add_instr("pv.cmple.sci.b", TYPE_RS)
sbst.add_instr("pv.cmpgtu.h", TYPE_RR)
sbst.add_instr("pv.cmpgtu.sc.h", TYPE_RR)
sbst.add_instr("pv.cmpgtu.sci.h", TYPE_RS)
sbst.add_instr("pv.cmpgtu.b", TYPE_RR)
sbst.add_instr("pv.cmpgtu.sc.b", TYPE_RR)
sbst.add_instr("pv.cmpgtu.sci.b", TYPE_RS)
sbst.add_instr("pv.cmpgeu.h", TYPE_RR)
sbst.add_instr("pv.cmpgeu.sc.h", TYPE_RR)
sbst.add_instr("pv.cmpgeu.sci.h", TYPE_RS)
sbst.add_instr("pv.cmpgeu.b", TYPE_RR)
sbst.add_instr("pv.cmpgeu.sc.b", TYPE_RR)
sbst.add_instr("pv.cmpgeu.sci.b", TYPE_RS)
sbst.add_instr("pv.cmpltu.h", TYPE_RR)
sbst.add_instr("pv.cmpltu.sc.h", TYPE_RR)
sbst.add_instr("pv.cmpltu.sci.h", TYPE_RS)
sbst.add_instr("pv.cmpltu.b", TYPE_RR)
sbst.add_instr("pv.cmpltu.sc.b", TYPE_RR)
sbst.add_instr("pv.cmpltu.sci.b", TYPE_RS)
sbst.add_instr("pv.cmpleu.h", TYPE_RR)
sbst.add_instr("pv.cmpleu.sc.h", TYPE_RR)
sbst.add_instr("pv.cmpleu.sci.h", TYPE_RS)
sbst.add_instr("pv.cmpleu.b", TYPE_RR)
sbst.add_instr("pv.cmpleu.sc.b", TYPE_RR)
sbst.add_instr("pv.cmpleu.sci.b", TYPE_RS)
sbst.block_end()

with open("insn_test.S", "w") as text_file:
    text_file.write(sbst.get_body())
