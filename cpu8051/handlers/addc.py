import cpu8051.opcode
from cpu8051.handlers.handler import *
from cpu8051.handlers.add import Add


class Addc(Add):
    """
    Wraps a handle, but adds the carry to the adder_unit.
    """
    def architecture(self):
        yield self.cpu.carry_present_sys_flag.shell.copy(self.cpu.adder_unit.carry.ports[0])
        for yield_out in super(Addc, self).architecture():
            yield yield_out


class AddcARxHandler(Addc, ARxHandler):
    """
    ADDC A, RX
    """
    opcode_set = cpu8051.opcode.addc_a_rx


class AddcADirectHandler(Addc, ADirectHandler):
    """
    ADDC A, direct
    """
    opcode_set = cpu8051.opcode.addc_a_direct


class AddcARiHandler(Addc, ARiHandler):
    """
    ADDC A, @Ri
    """
    opcode_set = cpu8051.opcode.addc_a_ri


class AddcADataHandler(Addc, ADataHandler):
    """
    ADDC A, data
    """
    opcode_set = cpu8051.opcode.addc_a_data


addc_handlers = [AddcADirectHandler, AddcARxHandler, AddcADataHandler, AddcARiHandler]