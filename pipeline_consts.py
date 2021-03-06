from alu import ALU
from decs import WORD

"""
    pipe line registers
"""


def validate_n_bit_tuple(c, n):
    if not (type(c) == tuple and len(c) == n):
        raise Exception("Invalid %d bit tuple" % n)


def validate_word_tuple(c):
    validate_n_bit_tuple(c, WORD)

NOOP = [int(c) for c in "00000000000000000000000000000000"]

class IF_ID:

    def __init__(self):
        self.pc = ALU.int_to_n_bit_binary(0)
        self.inst = tuple(NOOP)

    def set_pc(self, pc):
        validate_word_tuple(pc)

        self.pc = pc

    def set_inst(self, inst):
        validate_word_tuple(inst)
        self.inst = inst


class ID_EX:

    def __init__(self):
        self.pc = ALU.int_to_n_bit_binary(0)
        self.rd1 = ALU.int_to_n_bit_binary(0)
        self.rd2 = ALU.int_to_n_bit_binary(0)
        self.rs = ALU.int_to_n_bit_binary(0, 5)
        self.rt = ALU.int_to_n_bit_binary(0, 5)
        self.inst_imm = ALU.int_to_n_bit_binary(0, 16)
        self.inst_20_16 = ALU.int_to_n_bit_binary(0, 5)
        self.inst_rd = ALU.int_to_n_bit_binary(0, 5)

        self.wb_control = WB_CONTROL()
        self.mem_control = MEM_CONTROL()
        self.ex_control = EX_CONTROL()

    def set_pc(self, pc):
        validate_word_tuple(pc)
        self.pc = pc

    def set_rs(self, rs):
        validate_n_bit_tuple(rs, 5)
        self.rs = rs

    def set_rt(self, rt):
        validate_n_bit_tuple(rt, 5)
        self.rt = rt

    def set_rd1(self, rd1):
        validate_word_tuple(rd1)
        self.rd1 = rd1

    def set_rd2(self, rd2):
        validate_word_tuple(rd2)
        self.rd2 = rd2

    def set_inst_imm(self, i):
        validate_n_bit_tuple(i, WORD)
        self.inst_imm = i

    def set_inst_20_16(self, i):
        validate_n_bit_tuple(i, 5)
        self.inst_20_16 = i

    def set_inst_rd(self, i):
        validate_n_bit_tuple(i, 5)
        self.inst_rd = i


class EX_MEM:

    def __init__(self):
        self.pc = 0
        self.jump_target = ALU.int_to_n_bit_binary(0)
        self.alu_zero_flag = True
        self.alu_result = ALU.int_to_n_bit_binary(0)
        self.rd2 = ALU.int_to_n_bit_binary(0)
        self.reg_dest = ALU.int_to_n_bit_binary(0, 5)

        self.wb_control = WB_CONTROL()
        self.mem_control = MEM_CONTROL()

    def set_jump_target(self, jt):
        validate_n_bit_tuple(jt, WORD)
        self.jump_target = jt

    def set_alu_zero_flag(self, alu_zero_flag):
        self.alu_zero_flag = alu_zero_flag

    def set_alu_result(self, alu_result):
        validate_n_bit_tuple(alu_result, WORD)
        self.alu_result = alu_result

    def set_rd2(self, rd2):
        validate_n_bit_tuple(rd2, WORD)
        self.rd2 = rd2

    def set_reg_dest(self, reg_dest):
        validate_n_bit_tuple(reg_dest, 5)
        self.reg_dest = reg_dest


class MEM_WB:

    def __init__(self):
        self.alu_result = ALU.int_to_n_bit_binary(0)
        self.read_data = ALU.int_to_n_bit_binary(0)
        self.reg_dest = ALU.int_to_n_bit_binary(0, 5)

        self.wb_control = WB_CONTROL()

    def set_alu_result(self, alu_result):
        validate_word_tuple(alu_result)
        self.alu_result = alu_result

    def set_read_data(self, read_data):
        validate_word_tuple(read_data)
        self.read_data = read_data

    def set_reg_dest(self, reg_dest):
        validate_n_bit_tuple(reg_dest, 5)
        self.reg_dest = reg_dest


"""
    pipe line controls
"""


class WB_CONTROL:

    def __init__(self):
        self.MemToReg = False
        self.RegWrite = False


class MEM_CONTROL:

    def __init__(self):
        self.Branch = False
        self.MemRead = False
        self.MemWrite = False


class EX_CONTROL:

    def __init__(self):
        self.ALUSource = 'rs'
        self.RegDst = 'rd'
        self.ALUOp = '00'
