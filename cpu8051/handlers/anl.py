import cpu8051.opcode
from cpu8051.handlers.mode import ARxMode, ADirectMode, ARiMode, ADataMode
from cpu8051.handlers.handler import *
from cpu8051.handlers.mode import DirectDataMode, DirectAMode


class _Anl(ModeHandler):
    uses_and_unit = True

    @property
    def logic_unit(self):
        return self.cpu.and_unit


class AnlARxHandler(_Anl, ARxMode):
    """
    ANL A, RX
    """
    opcode_set = cpu8051.opcode.anl_a_rx


class AnlARiHandler(_Anl, ARiMode):
    """
    ANL A, @Ri
    """
    opcode_set = cpu8051.opcode.anl_a_ri


class AnlADirectHandler(_Anl, ADirectMode):
    """
    ANL A, direct
    """
    opcode_set = cpu8051.opcode.anl_a_direct


class AnlADataHandler(_Anl, ADataMode):
    """
    ANL A, #data
    """
    opcode_set = cpu8051.opcode.anl_a_data


class AnlDirectA(_Anl, DirectAMode):
    """
    ANL direct, A
    """
    opcode_set = cpu8051.opcode.anl_direct_a


class AnlDirectData(_Anl, DirectDataMode):
    """
    ANL direct, #data
    """
    opcode_set = cpu8051.opcode.anl_direct_data


all_handlers = [AnlARxHandler, AnlDirectA, AnlADataHandler, AnlADirectHandler, AnlARiHandler, AnlDirectData]