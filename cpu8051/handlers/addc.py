import cpu8051.opcode
from cpu8051.handlers.handler import Handler
from cpu8051.handlers.add import AddARxHandler, AddADirectHandler, AddARiHandler, AddADataHandler
from cbac.unit.statements import If


class _AddWithCarryHandler(Handler):
    """
    Wraps a handle, but adds the carry to the adder_unit.
    """
    wrapped_handler = None

    def handle(self, opcode_value=None):
        self.cpu.carry_present_sys_flag.shell.copy(self.cpu.adder_unit.carry.ports[0])
        for yield_out in self.wrapped_handler.handle(opcode_value):
            yield yield_out


class AddcARxHandler(_AddWithCarryHandler):
    """
    ADDC A, RX
    """
    opcode_set = cpu8051.opcode.addc_a_rx
    wrapped_handler = AddARxHandler


class AddcADirectHandler(_AddWithCarryHandler):
    """
    ADDC A, direct
    """
    opcode_set = cpu8051.opcode.addc_a_direct
    wrapped_handler = AddADirectHandler


class AddcARiHandler(_AddWithCarryHandler):
    """
    ADDC A, @Ri
    """
    opcode_set = cpu8051.opcode.addc_a_ri
    wrapped_handler = AddARiHandler


class AddcADataHandler(_AddWithCarryHandler):
    """
    ADDC A, data
    """
    opcode_set = cpu8051.opcode.addc_a_data
    wrapped_handler = AddADataHandler


addc_handlers = [AddcADirectHandler, AddcARxHandler, AddcADataHandler, AddcARiHandler]