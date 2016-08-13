from compound import CBA
from compound import Memory
from unit import Unit


class OrUnit(Unit):
    def __init__(self, bits=8):
        # TODO: re-write to new format
        super(OrUnit, self).__init__()
        self.bits = bits
        self.input_a = Memory(size=bits)
        self.input_b = Memory(size=bits)
        self.output = Memory(size=bits)

        commands = list()

        commands.append(self.input_a.shell.reset())
        commands.append(self.input_b.shell.reset())

        for a_block, b_block, o_block, in zip(self.input_a.blocks, self.input_b.blocks, self.output.blocks):
            # note that the eq is overriden.
            commands.append(a_block.shell == True)
            commands.append(o_block.shell.activate())
            commands.append(b_block.shell == True)
            commands.append(o_block.shell.activate())

        self.cba = CBA(*commands)

        self.compounds = [self.input_a, self.input_b, self.output, self.cba]
