from unit import Unit
from compound import Memory, Constant
from compound import CBA


class OrUnit(Unit):
    def __init__(self, bits=8):
        self.bits = bits
        self.input_a = Memory(size=bits)
        self.input_b = Memory(size=bits)
        self.output = Memory(size=bits)

        commands = list()

        for a_block, b_block, o_block, in zip(self.input_a.blocks, self.input_b.blocks, self.output.blocks):
            # note that the eq is overriden.
            commands.append(a_block.shell == True)
            commands.append(o_block.shell.activate())
            commands.append(b_block.shell == True)
            commands.append(o_block.shell.activate())

        self.cba = CBA(*commands)

        self.compounds = [self.input_a, self.input_b, self.output, self.cba]