from compound import CBA
from compound import Memory
from unit import Unit


class NotUnit(Unit):
    def __init__(self, bits=8):
        self.bits = bits
        self.input_a = Memory(size=bits)
        self.output = Memory(size=bits)

        commands = []

        for a_block, o_block, in zip(self.input_a.blocks, self.output.blocks):
            # note that the eq is overriden.
            commands.append(a_block.shell == False)
            commands.append(o_block.shell.activate())
            commands.append(a_block.shell == True)
            commands.append(o_block.shell.deactivate())

        self.cba = CBA(*commands)

        self.compounds = [self.input_a, self.output, self.cba]
