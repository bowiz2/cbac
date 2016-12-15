import logging


class OpcodeSet(object):
    """
    Represents a set of opcodes with a specific encoding.
    for example all the opcodes of MOV RX A)
    """

    def __init__(self, encoding, set_size=8):
        assert len(encoding) <= set_size
        if len(encoding) != set_size:
            logging.warning("Attention! your encoding size is smaller then the set size. This is not recommended.")

        self.set_size = set_size
        self._encoding = encoding

    @property
    def encoding(self):
        """
        :return: General representation of what is this opcode set looks like.
        """
        return self._pad(self._encoding.lower())

    def all(self):
        """
        Return all the opcode values of this opcode set.
        :return:
        """
        min_range = int(self.encoding.replace('r', '0'), 2)
        max_range = int(self.encoding.replace('r', '1'), 2)
        return range(min_range, max_range + 1)

    def match(self, opcode):
        """
        Check if an opcode is matching the encoding of this set.
        """
        opcode_bits = self._pad(bin(opcode)[2:])
        for opcode_bit, encoding_bit in zip(opcode_bits, self.encoding):
            if encoding_bit in ['1', '0']:
                if opcode_bit is not encoding_bit:
                    return False
        return True

    def get_arg(self, value, arg_sign):
        """
        Get the arg value of a given opcode value. based of the encoding of the handler.
        For example
        we have encoding 0xx0111
        to get the arg x of the opcode 0b0110111
        the result will be 0b11 (3)

        not that arg_sign is not case sensitive.
        """
        arg_sign = arg_sign.lower()

        value_bits = self._pad(bin(value)[2:])
        arg_bits = ""
        for value_bit, encoding_bit in zip(value_bits, self.encoding):
            if encoding_bit == arg_sign:
                arg_bits += value_bit
        return int(arg_bits, 2)

    def _pad(self, bit_string):
        padsize = self.set_size - len(bit_string)
        assert padsize >= 0, "Your bit string is too big."
        return bit_string + ("0" * padsize)

    def get_single(self, r=0):
        """
        :return: get value of an opcode at the r positon.
        """
        return self.all()[r]

# Meaning of Oprands
# ==================
# rx - Working register R0-R7
# addr - 128 internal RAM locations, any l/O port, control or status register
# ri - Indirect internal or external RAM location addressed by register R0 or R1
# data - 8-bit constant included in instruction
# data16 - 16-bit constant included as bytes 2 and 3 of instruction
# bit - 128 software flags, any bitaddressable l/O pin, control or status bit
# a - Accumulator

nop = OpcodeSet("00000000")

mov_a_rx = OpcodeSet("11101rrr")
mov_rx_a = OpcodeSet("11111rrr")
mov_rx_data = OpcodeSet("01111rrr")
mov_rx_addr = OpcodeSet("10101rrr")

# INC
inc_a = OpcodeSet("00000100")
int_addr = OpcodeSet("00000101")
inc_rx = OpcodeSet("00001rrr")

# ADD
add_a_rx = OpcodeSet("00101rrr")
add_a_addr = OpcodeSet("00100101")
add_a_ri = OpcodeSet("0010011r")
add_a_data = OpcodeSet("00100100")

# ADDC
addc_a_rx = OpcodeSet("00111rrr")
addc_a_direct = OpcodeSet("00110101")
addc_a_ri = OpcodeSet("0011011r")
addc_a_data = OpcodeSet("00110100")

#AJMP
ajmp_addr11 = OpcodeSet("rrr00001")

#ANL
anl_a_rx = OpcodeSet("01011rrr")
anl_a_direct = OpcodeSet("01010101")
anl_a_ri = OpcodeSet("0101011r")
anl_a_data = OpcodeSet("01010100")
anl_direct_a = OpcodeSet("01010101")
anl_direct_data = OpcodeSet("01010011")
anl_c_bit = OpcodeSet("10000010")
anl_c_sbit = OpcodeSet("10110000")

# CJNE
cnje_a_direct_rel = OpcodeSet("10110101")
cnje_a_data_rel = OpcodeSet("10110100")
cnje_rx_data_rel = OpcodeSet("10111rrr")
cnje_ri_data_rel = OpcodeSet("1011011r")

# CLR
clr_a = OpcodeSet("11100100")
clr_c = OpcodeSet("11000011")
clr_bit = OpcodeSet("11000010")

# CPL
cpl_a = OpcodeSet("11110100")
cpl_c = OpcodeSet("10110011")
cpl_bit = OpcodeSet("10110010")

da_a = OpcodeSet("11010100")


declared_opcodes = filter(lambda x: isinstance(x, OpcodeSet), globals().values())

