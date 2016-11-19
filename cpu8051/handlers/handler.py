import cbac


class Handler(cbac.unit.Unit):
    """
    Handles a specific opcode in the cpu.
    """
    encoding = ""

    @cbac.unit.auto_synthesis
    def __init__(self, cpu_body):
        super(Handler, self).__init__(bits=cpu_body.bits)
        self.cpu = cpu_body

    @property
    def _formatted_encoding(self):
        return self._pad(self.encoding.lower())

    @property
    def opcodes(self):
        """
        :return: Which opcodes this handler handles.
        """
        min_range = int(self.encoding.replace('r', '0'), 2)
        max_range = int(self.encoding.replace('r', '1'), 2)
        return xrange(min_range, max_range + 1)

    @property
    def opcode(self):
        """
        :return: The opcode this handler handles.
        """
        assert len(self.opcodes) == 0, "This handler handles more then one opcode. please use 'opcodes' instead."
        return self.opcodes[0]

    def match(self, opcode):
        """
        Check if an opcode is matching the encoding of this handler.
        """
        opcode_bits = self._pad(bin(opcode)[2:])
        for opcode_bit, encoding_bit in zip(opcode_bits, self._formatted_encoding):
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
        for value_bit, encoding_bit in zip(value_bits, self._formatted_encoding):
            if encoding_bit == arg_sign:
                arg_bits += value_bit
        return int(arg_bits, 2)

    def get_register(self, value):
        """
        :return: get the register encoded in the opcode.
        """
        return self.cpu.general_registers[self.get_arg(value, 'r')]

    def _pad(self, bit_string):
        while len(bit_string) < self.bits:
            bit_string = '0' + bit_string

        return bit_string

    def architecture(self):
        pass
