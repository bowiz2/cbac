"""
Holds AND unit.
"""
from cbac.unit.statements import If
from cbac.unit import Unit


class AndUnit(Unit):
    """
    This unit takes two memories, makes an AND logic function between them and store it to the output memory.
    """

    def __init__(self, bits=8):
        super(AndUnit, self).__init__()
        self.bits = bits
        self.input_a = self.create_input(self.bits)
        self.input_b = self.create_input(self.bits)
        self.output = self.create_output(self.bits)

        self.synthesis()

    def main_logic_commands(self):
        """
        Describes the AND logic.
        """
        for a_block, b_block, o_block, in zip(self.input_a.blocks, self.input_b.blocks, self.output.blocks):
            # note that the eq is overriden.
            yield If(
                (a_block.shell == True) & (b_block.shell == True)
            ).then(
                o_block.shell.activate()
            )
