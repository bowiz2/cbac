import cpu8051.opcode
from cpu8051.handlers.mode import ARxMode, ADirectMode, ARiMode, ADataMode
from cpu8051.handlers.add import _Add
from cpu8051.handlers.handler import *


class Addc(_Add):
    """
    Wraps a handle, but adds the carry to the adder_unit.
    """

    def make_logic(self, register_a=None, register_b=None):
        yield self.cpu.carry_present_sys_flag.shell.copy(self.cpu.adder_unit.carry.ports[0])
        for yield_out in super(Addc, self).make_logic(register_a):
            yield yield_out


class AddcARxHandler(Addc, ARxMode):
    """
    ADDC A, RX
    """
    opcode_set = cpu8051.opcode.addc_a_rx


class AddcADirectHandler(Addc, ADirectMode):
    """
    ADDC A, direct
    """
    opcode_set = cpu8051.opcode.addc_a_direct


class AddcARiHandler(Addc, ARiMode):
    """
    ADDC A, @Ri
    """
    opcode_set = cpu8051.opcode.addc_a_ri


class AddcADataHandler(Addc, ADataMode):
    """
    ADDC A, data
    """
    opcode_set = cpu8051.opcode.addc_a_data


all_handlers = [AddcADirectHandler, AddcARxHandler, AddcADataHandler, AddcARiHandler]
