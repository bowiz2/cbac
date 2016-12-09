from cpu8051.handlers.handler import ModeHandler
from cpu8051.handlers.mode import *
from cpu8051.opcode import *


class Dec(ModeHandler):
    uses_adder = True

    @property
    def logic_unit(self):
        return self.cpu.adder_unit

    def make_logic(self, register_a=None, register_b=None):
        yield self.cpu.constant_factory(-1).shell.copy(self.logic_unit.input_b)
        for yield_out in super(Dec, self).make_logic(register_a):
            yield yield_out


class DecAHandler(Dec, AMode):
    opcode_set = dec_a


class DecRxHandler(Dec, RxMode):
    opcode_set = dec_rx


class DecRiHandler(Dec, RiMode):
    opcode_set = dec_ri


class DecDirectHandler(Dec, DirectMode):
    opcode_set = dec_direct

all_handles = [DecAHandler, DecDirectHandler, DecRiHandler, DecRxHandler, DecDirectHandler]