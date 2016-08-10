from compound import CBA
from compound import Memory
from unit import Unit


class ReverseUnit(Unit):
    """
    Reverses the given blocks.
    """

    def __init__(self, blockspace, bits=8):
        super(ReverseUnit, self).__init__(blockspace)
        self.bits = bits
        self.input_a = Memory(size=bits)
        self.output = Memory(size=bits)
        commands = list()
        last = self.input_a.blocks[self.bits - 1]
        for index in xrange(self.bits, 0, -1):
            self.input_a.blocks[index] = self.input_a.blocks[index - 1]
        self.input_a.blocks[0] = last

        for a_block, o_block, in zip(self.input_a.blocks, self.output.blocks):
            # note that the eq is overriden.
            commands.append(a_block.shell == False)
            commands.append(o_block.shell.deactivate())
            commands.append(a_block.shell == True)
            commands.append(o_block.shell.activate())

        self.cba = CBA(*commands)

        self.compounds = [self.input_a, self.output, self.cba]
