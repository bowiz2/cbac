"""
!WARNING! Diamond inheritance is in-place.
"""
import cpu8051.opcode
from cpu8051.handlers.add import _AddHandler, AddARxHandler, AddADirectHandler, AddARiHandler, AddADataHandler


class _AddWithCarryHandler(_AddHandler):
    """
    Wraps a handle, but adds the carry to the adder_unit.
    """
    wrapped_handler = None

    def architecture(self):
        yield self.cpu.carry_present_sys_flag.shell.copy(self.adder.carry.ports[0])
        for yield_out in super(_AddHandler, self).architecture():
            yield yield_out


class AddcARxHandler(_AddWithCarryHandler, AddARxHandler):
    """
    ADDC A, RX
    """
    opcode_set = cpu8051.opcode.addc_a_rx


class AddcADirectHandler(_AddWithCarryHandler, AddADirectHandler):
    """
    ADDC A, direct
    """
    opcode_set = cpu8051.opcode.addc_a_direct


class AddcARiHandler(_AddWithCarryHandler, AddARiHandler):
    """
    ADDC A, @Ri
    """
    opcode_set = cpu8051.opcode.addc_a_ri


class AddcADataHandler(_AddWithCarryHandler, AddADataHandler):
    """
    ADDC A, data
    """
    opcode_set = cpu8051.opcode.addc_a_data


addc_handlers = [AddcADirectHandler, AddcARxHandler, AddcADataHandler, AddcARiHandler]