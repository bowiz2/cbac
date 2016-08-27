from cbac.unit.unit_base import Unit
from cbac.unit.statements import If

class OrUnit(Unit):
    def __init__(self, bits=8):
        # TODO: re-write to new format
        super(OrUnit, self).__init__(bits)
        self.input_a = self.create_input(self.bits)
        self.input_b = self.create_input(self.bits)
        self.output = self.create_output(self.bits)

        self.synthesis()

    def main_logic_commands(self):
        for a_block, b_block, o_block, in zip(self.input_a.blocks, self.input_b.blocks, self.output.blocks):
            yield If(a_block.shell == True).then(o_block.shell.activate())
            yield If(b_block.shell == True).then(o_block.shell.activate())

