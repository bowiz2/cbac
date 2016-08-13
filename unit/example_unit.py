from unit import Unit


class ExampleUnit(Unit):
    def __init__(self, bits=8):
        super(ExampleUnit, self).__init__(bits)
        # == Here you declare all your memory slots.
        self.my_input = self.create_input(self.bits)
        self.my_output = self.create_output(self.bits)
        # ==
        self.generate_main_logic_cbas()

    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        yield self.my_input.shell.move(self.my_output)
