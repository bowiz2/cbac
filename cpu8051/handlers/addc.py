"""
!WARNING! Diamond inheritance is in-place.
"""
import cpu8051.opcode
from cpu8051.handlers.add import AddHandler, AddARxHandler, AddADirectHandler, AddARiHandler, AddADataHandler


class UseCarry(AddHandler):
    """
    Wraps a handle, but adds the carry to the adder_unit.
    """
    wrapped_handler = None

    def architecture(self):
        yield self.cpu.carry_present_sys_flag.shell.copy(self.adder.carry.ports[0])
        for yield_out in super(AddHandler, self).architecture():
            yield yield_out


class AddcARx(UseCarry, AddARxHandler):
    """
    ADDC A, RX
    """
    opcode_set = cpu8051.opcode.addc_a_rx


class AddcADirect(UseCarry, AddADirectHandler):
    """
    ADDC A, direct
    """
    opcode_set = cpu8051.opcode.addc_a_direct


class AddcARi(UseCarry, AddARiHandler):
    """
    ADDC A, @Ri
    """
    opcode_set = cpu8051.opcode.addc_a_ri


class AddcAData(UseCarry, AddADataHandler):
    """
    ADDC A, data
    """
    opcode_set = cpu8051.opcode.addc_a_data


addc_handlers = [AddcADirect, AddcARx, AddcAData, AddcARi]