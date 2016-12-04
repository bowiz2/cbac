from cpu8051.handlers.handler import ModeHandler
from cpu8051.handlers.mode import AMode, RxMode, RiMode, DirectMode
from cpu8051.opcode import *


class _Inc(ModeHandler):
    """
    BASE Inc Handler.
    """

    @property
    def logic_unit(self):
        return self.cpu.increment_unit


class IncAHandler(_Inc, AMode):
    """
    INC A
    """
    opcode_set = inc_a


class IncRxHandler(_Inc, RxMode):
    """
    INC Rx
    """
    opcode_set = inc_rx


class IncRiHandler(_Inc, RiMode):
    """
    INC @Ri
    """
    opcode_set = inc_ri


class IncDirectHandler(_Inc, DirectMode):
    """
    INC direct
    """
    opcode_set = inc_direct
