import cpu8051.opcode
from cpu8051.handlers.handler import *
from cpu8051.handlers.mode import ARxMode, ADirectMode, ARiMode, ADataMode


class _Add(ModeHandler):
    uses_adder = True
    @property
    def logic_unit(self):
        return self.cpu.adder_unit


class AddARxHandler(_Add, ARxMode):
    """
    ADD A, RX
    """
    opcode_set = cpu8051.opcode.add_a_rx


class AddADirectHandler(_Add, ADirectMode):
    """
    ADD A, direct
    """
    opcode_set = cpu8051.opcode.add_a_rx


class AddARiHandler(_Add, ARiMode):
    """
    ADD A, @Ri
    """
    opcode_set = cpu8051.opcode.add_a_ri


class AddADataHandler(_Add, ADataMode):
    """
    ADD A, data
    """
    opcode_set = cpu8051.opcode.add_a_data


add_handlers = [AddADirectHandler, AddARxHandler, AddADataHandler, AddARiHandler]