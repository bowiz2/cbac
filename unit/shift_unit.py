import math

from compound import Memory
from constants.block_id import EMPTY_BLOCK, FALSE_BLOCK
from unit import Unit


class ShiftUnit(Unit):
    def __init__(self, bits):
        super(ShiftUnit, self).__init__()
        self.bits = bits
        # here will be saved the value you want to shift. and the shifting will accure on it.
        self.buffer_register = self.add_compound(Memory(bits * 2))
        self.operation_register = self.add_input(self.buffer_register.get_sub_memory(xrange(bits)))
        self.output = self.create_output(bits)
        self.input_shift_size = self.create_input(int(math.ceil(math.log(bits, 2))))
        self.generate_main_point_entry()

    def main_logic_commands(self):
        for i, shift_block in enumerate(self.input_shift_size.blocks):
            yield shift_block.shell == True
            yield self.operation_register.shell.move(self.operation_register.blocks[2 ** i])
        yield self.operation_register.shell.move(self.output)
        yield self.output.shell.replace(EMPTY_BLOCK, FALSE_BLOCK)
