from cpu8051.handlers import ModeHandler
from cpu8051.handlers.mode import *


class Dec(ModeHandler):
    @property
    def logic_unit(self):
        return self.cpu.adder_unit

    def make_logic(self, register_a=None, register_b=None):
        yield self.cpu.constant_factory(-1).shell.copy(self.logic_unit.input_b)
        for yield_out in super(Dec, self).make_logic(register_a):
            yield yield_out


