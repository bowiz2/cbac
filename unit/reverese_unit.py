from compound import CBA
from compound import Memory
from unit import Unit


class ReverseUnit(Unit):
    """
    Reverses the given blocks.
    """

    def __init__(self, bits=8):
        # TODO: re-write to new format.
        super(ReverseUnit, self).__init__()
        self.bits = bits
        self.input_a = Memory(size=bits)
        self.output = Memory(size=bits)
        commands = []
        commands.append(self.output.shell.reset())

        for index in xrange(self.bits):
            commands.append(self.input_a.blocks[index].shell == True)
            commands.append(self.output.blocks[self.bits - index - 1].shell.activate())

        self.cba = CBA(*commands)

        self.compounds = [self.input_a, self.output, self.cba]
