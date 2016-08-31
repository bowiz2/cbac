from cbac.unit.unit_base import Unit
from cbac.unit.statements import If


class NotUnit(Unit):
    def __init__(self, bits=8):
        # TODO: re-write to new format.
        super(NotUnit, self).__init__()
        self.bits = bits
        self.input = self.create_input(self.bits)
        self.output = self.create_output(self.bits)
        self.synthesis()

    def main_logic_commands(self):
        for a_block, o_block, in zip(self.input.blocks, self.output.blocks):
            # note that the eq is overriden.
            yield If(a_block.shell == False).then(o_block.shell.activate())
            yield If(a_block.shell == True).then(o_block.shell.deactivate())
