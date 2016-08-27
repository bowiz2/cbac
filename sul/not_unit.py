from cbac.unit.unit_base import Unit


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
            yield a_block.shell == False
            yield o_block.shell.activate()
            yield a_block.shell == True
            yield o_block.shell.deactivate()
