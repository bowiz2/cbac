import cpu8051.opcode
from cpu8051.handlers.handler import *


class AddHandler(Handler):

    @property
    def logic_unit(self):
        return self.cpu.adder_unit


class AddARxHandler(AddHandler, AbstractARxHandler):
    """
    ADD A, RX
    """
    opcode_set = cpu8051.opcode.add_a_rx


class AddADirectHandler(AddHandler, AbstractADirectHandler):
    """
    ADD A, direct
    """
    opcode_set = cpu8051.opcode.add_a_rx


class AddARiHandler(AddHandler, AbstractARiHandler):
    """
    ADD A, @Ri
    """
    opcode_set = cpu8051.opcode.add_a_ri


class AddADataHandler(AddHandler, AbstractADataHandler):
    """
    ADD A, data
    """
    opcode_set = cpu8051.opcode.add_a_data


add_handlers = [AddADirectHandler, AddARxHandler, AddADataHandler, AddARiHandler]