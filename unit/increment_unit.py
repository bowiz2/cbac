from unit import Unit
from compound import Memory


class IncrementUnit(Unit):
    def __init__(self, bits):
        super(IncrementUnit, self).__init__(bits)
        # in the carry we will remember the addition.
        self.flags = self.add_compound(Memory(2))
        self.carry_in = self.flags.blocks[0]
        self.carry_out = self.flags.blocks[1]
        self.input = self.create_input(self.bits)
        self.output = self.create_output(self.bits)
        self.generate_main_point_entry()

    def main_logic_commands(self):
        yield self.flags.activate()
        for inp_block, out_block in zip(self.input.blocks, self.output.blocks):

            yield inp_block.shell == True
            yield self.carry_in.shell == True
            yield self.carry_out.shell.activate()

            yield inp_block.shell == True
            yield self.carry_in.shell == False
            yield out_block.shell.activate()

            yield inp_block.shell == False
            yield self.carry_in.shell == True
            yield out_block.shell.activate()

            yield self.carry_out.shell.move(self.carry_in)
            yield self.carry_out.shell.deactivate()