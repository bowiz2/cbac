import logging

NOP = 0x0C
INC_A = 0x04
INC_IRAM = 0x05


class OpcodeSet(object):
    """
    Represents a set of opcodes with a specific encoding.
    for example all the opcodes of MOV RX A)
    """

    def __init__(self, encoding, set_size):
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
        return xrange(min_range, max_range + 1)

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
        while len(bit_string) < self.set_size:
            bit_string = '0' + bit_string

        return bit_string
