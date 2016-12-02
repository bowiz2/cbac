import cpu8051.opcode
from cpu8051.handlers.mode import ARxMode, ADirectMode, ARiMode, ADataMode
from cpu8051.handlers.add import Add
from cpu8051.handlers.handler import *


class Addc(Add):
    """
    Wraps a handle, but adds the carry to the adder_unit.
    """
    def make_logic(self, register_a=None, register_b=None):
        yield self.cpu.carry_present_sys_flag.shell.copy(self.cpu.adder_unit.carry.ports[0])
        for yield_out in super(Addc, self).make_logic(register_a):
            yield yield_out


class AddcARxMode(Addc, ARxMode):
    """
    ADDC A, RX
    """
    opcode_set = cpu8051.opcode.addc_a_rx


class AddcADirectMode(Addc, ADirectMode):
    """
    ADDC A, direct
    """
    opcode_set = cpu8051.opcode.addc_a_direct


class AddcARiMode(Addc, ARiMode):
    """
    ADDC A, @Ri
    """
    opcode_set = cpu8051.opcode.addc_a_ri


class AddcADataMode(Addc, ADataMode):
    """
    ADDC A, data
    """
    opcode_set = cpu8051.opcode.addc_a_data


addc_handlers = [AddcADirectMode, AddcARxMode, AddcADataMode, AddcARiMode]