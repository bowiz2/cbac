import cpu8051.opcode
from cpu8051.handlers.handler import *


class Add(Handler):

    @property
    def logic_unit(self):
        return self.cpu.adder_unit


class AddARx(Add, ARxHandler):
    """
    ADD A, RX
    """
    opcode_set = cpu8051.opcode.add_a_rx


class AddADirect(Add, ADirectHandler):
    """
    ADD A, direct
    """
    opcode_set = cpu8051.opcode.add_a_rx


class AddARi(Add, ARiHandler):
    """
    ADD A, @Ri
    """
    opcode_set = cpu8051.opcode.add_a_ri


class AddAData(Add, ADataHandler):
    """
    ADD A, data
    """
    opcode_set = cpu8051.opcode.add_a_data


add_handlers = [AddADirect, AddARx, AddAData, AddARi]