from compound import CBA
from compound import Memory
from unit import Unit


class NotUnit(Unit):
    def __init__(self, bits=8):
        #TODO: re-write to new format.
        super(NotUnit, self).__init__()
        self.bits = bits
        self.input = Memory(size=bits)
        self.output = Memory(size=bits)

        commands = []

        for a_block, o_block, in zip(self.input.blocks, self.output.blocks):
            # note that the eq is overriden.
            commands.append(a_block.shell == False)
            commands.append(o_block.shell.activate())
            commands.append(a_block.shell == True)
            commands.append(o_block.shell.deactivate())

        self.cba = CBA(*commands)

        self.compounds = [self.input, self.output, self.cba]
