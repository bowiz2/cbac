from unit_base import Unit


class NandUnit(Unit):
    def __init__(self, bits=8):
        super(NandUnit, self).__init__(bits)
        # == Here you declare all your memory slots.
        self.input_a = self.create_input(self.bits)
        self.input_b = self.create_input(self.bits)
        self.output = self.create_output(self.bits)
        # ==
        self.generate_main_logic_cbas()

    def on_entry_init_commands(self):
        """
        Makes the outputs to be max values by default
        """
        for output in self.outputs:
            yield output.shell.set_max_value()

    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        for a_block, b_block, o_block, in zip(self.input_a.blocks, self.input_b.blocks, self.output.blocks):
            # note that the eq is overriden.
            yield a_block.shell == True
            yield b_block.shell == True
            yield o_block.shell.deactivate()
