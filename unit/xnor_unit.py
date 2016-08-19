from unit_base import Unit


class XnorUnit(Unit):
    def __init__(self, bits=8):
        super(XnorUnit, self).__init__(bits)
        # == Here you declare all your memory slots.
        self.input_a = self.create_input(self.bits)
        self.input_b = self.create_input(self.bits)
        self.output = self.create_output(self.bits)
        # ==
        self.generate_main_logic_cbas()

    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        for inp_block_a, inp_block_b, out_block in zip(self.input_a.blocks, self.input_b.blocks, self.output.blocks):
            yield inp_block_a.shell == False
            yield inp_block_b.shell == False
            yield out_block.shell.activate()
            yield inp_block_a.shell == True
            yield inp_block_b.shell == True
            yield out_block.shell.activate()
