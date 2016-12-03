from cpu8051.handlers.handler import ModeHandler
from cpu8051.handlers.mode import ARxMode, ADirectMode, ARiMode, ADataMode, DirectAMode, DirectDataMode
import cpu8051


class _Orl(ModeHandler):
    @property
    def logic_unit(self):
        return self.cpu.or_unit


class OrlARxHandler(_Orl, ARxMode):
    """
    ORL A, RX
    """
    opcode_set = cpu8051.opcode.orl_a_rx


class OrlARiHandler(_Orl, ARiMode):
    """
    ORL A, @Ri
    """
    opcode_set = cpu8051.opcode.orl_a_ri


class OrlADirectHandler(_Orl, ADirectMode):
    """
    ORL A, direct
    """
    opcode_set = cpu8051.opcode.orl_a_direct


class OrlADataHandler(_Orl, ADataMode):
    """
    ORL A, #data
    """
    opcode_set = cpu8051.opcode.orl_a_data


class OrlDirectA(_Orl, DirectAMode):
    """
    ORL direct, A
    """
    opcode_set = cpu8051.opcode.orl_direct_a


class OrlDirectData(_Orl, DirectDataMode):
    """
    ORL direct, #data
    """
    opcode_set = cpu8051.opcode.orl_direct_data