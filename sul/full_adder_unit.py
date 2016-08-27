from cbac.unit.statements import Conditional
from cbac.unit.unit_base import Unit


class FullAdderUnit(Unit):
    def __init__(self, bits=8, carry_flag=None):
        """
        :param bits: size of the full adder in bits
        :param carry_flag: The flag which will be set if there was a carry.
        """
        super(FullAdderUnit, self).__init__(bits)
        # == Here you declare all your memory slots.
        self.input_a = self.create_input(self.bits)
        self.input_b = self.create_input(self.bits)
        self.carry = self.create_input(self.bits + 1)
        self.output = self.create_output(self.bits)
        self.carry_flag = None
        # ==
        self.synthesis()

    def main_logic_commands(self):
        # TODO: If statement include
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        for i, a, b, cin, cout, s in zip(xrange(self.bits), self.input_a.blocks, self.input_b.blocks,
                                         self.carry.blocks[:-1], self.carry.blocks[1:], self.output.blocks):
            yield a.shell == False
            yield b.shell == False
            yield cin.shell == True
            yield Conditional(
                s.shell.activate()
            )
            yield a.shell == False
            yield b.shell == True
            yield cin.shell == False
            yield Conditional(
                s.shell.activate()
            )
            yield a.shell == False
            yield b.shell == True
            yield cin.shell == True
            yield Conditional(
                cout.shell.activate()
            )
            yield a.shell == True
            yield b.shell == False
            yield cin.shell == False
            yield Conditional(
                s.shell.activate()
            )
            yield a.shell == True
            yield b.shell == False
            yield cin.shell == True
            yield Conditional(
                cout.shell.activate()
            )
            yield a.shell == True
            yield b.shell == True
            yield cin.shell == False
            yield Conditional(
                cout.shell.activate()
            )
            yield a.shell == True
            yield b.shell == True
            yield cin.shell == True
            yield Conditional(
                cout.shell.activate(),
                s.shell.activate()
            )
        if self.carry_flag is not None:
            self.carry.blocks[-1].copy(self.carry_flag)
