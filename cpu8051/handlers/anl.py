import cpu8051.opcode
from cpu8051.handlers.mode import ARxMode, ADirectMode, ARiMode, ADataMode
from cpu8051.handlers.handler import *
from cpu8051.handlers.mode import DirectDataMode, DirectAMode


class Anl(ModeHandler):
    uses_and_unit = True
    @property
    def logic_unit(self):
        return self.cpu.and_unit


class AnlARxHandler(Anl, ARxMode):
    opcode_set = cpu8051.opcode.anl_a_rx


class AnlARiHandler(Anl, ARiMode):
    opcode_set = cpu8051.opcode.anl_a_ri


class AnlADirectHandler(Anl, ADirectMode):
    opcode_set = cpu8051.opcode.anl_a_direct


class AnlADataHandler(Anl, ADataMode):
    opcode_set = cpu8051.opcode.anl_a_data


class AnlDirectA(Anl, DirectAMode):
    opcode_set = cpu8051.opcode.anl_direct_a


class AnlDirectData(Anl, DirectDataMode):
    opcode_set = cpu8051.opcode.anl_direct_data