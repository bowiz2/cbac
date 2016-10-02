from cbac.compound import Register
from cbac.unit.unit_base import Unit
from cbac.unit.statements import *


class IncrementUnit(Unit):
    def __init__(self, bits):
        super(IncrementUnit, self).__init__(bits)
        # in the carry we will remember the addition.
        self.flags = self.add_compound(Register(2))
        self.carry_in = self.flags.blocks[0]
        self.carry_out = self.flags.blocks[1]
        self.input = self.create_input(self.bits)
        self.output = self.create_output(self.bits)
        self.synthesis()

    def main_logic_commands(self):
        # TODO: If statement include
        yield self.carry_in.shell.activate()
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
            yield Debug("/say Incrementer {0}/{1} completed.".format(
                self.input.blocks.index(inp_block) + 1, len(self.input.blocks)
            ))

        yield Debug("/say Increment complete successfully.")
