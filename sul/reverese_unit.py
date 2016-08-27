from cbac.unit.unit_base import Unit
from cbac.unit.statements import If


class ReverseUnit(Unit):
    """
    Reverses the given blocks.
    """

    def __init__(self, bits=8):
        # TODO: re-write to new format.
        super(ReverseUnit, self).__init__()
        self.bits = bits
        self.input_a = self.create_input(self.bits)
        self.output = self.create_output(self.bits)

        self.synthesis()

    def main_logic_commands(self):
        for index in xrange(self.bits):
            yield If(
                self.input_a.blocks[index].shell == True
            ).then(
                self.output.blocks[self.bits - index - 1].shell.activate()
            )

