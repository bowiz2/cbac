from cpu8051.handlers.handler import ModeHandler
from cpu8051.handlers.mode import ConditionJumpRelMode
from cpu8051.opcode import *


class JZ(ModeHandler, ConditionJumpRelMode):
    @property
    def condition(self):
        return self.cpu.accumulator.shell == self.constant_factory(0)


class JC(ModeHandler, ConditionJumpRelMode):
    opcode_set = jz_rel
    @property
    def condition(self):
        return self.cpu.carry_flag.shell == True