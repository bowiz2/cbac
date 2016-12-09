from cpu8051.handlers.handler import ModeHandler
from cpu8051.handlers.mode import ConditionJumpRelMode, JumpRelMode
from cpu8051.opcode import *


class JmpRelHandler(ModeHandler, JumpRelMode):
    """
    JMP rel
    """
    opcode_set = OpcodeSet("00000001")


class JzRelHandler(ModeHandler, ConditionJumpRelMode):
    """
    JZ rel
    """
    opcode_set = jz_rel

    @property
    def condition(self):
        """
        :return: Check if accumulator is zero command
        """
        return [self.cpu.accumulator.shell == self.constant_factory(0)]


class JnzRelHandler(ModeHandler, ConditionJumpRelMode):
    """
    JNZ rel
    """
    opcode_set = jnz_rel

    @property
    def condition(self):
        """
        :return: Check if accumulator is not zero command
        """
        return self.cpu.accumulator.shell != self.constant_factory(0)


class JcRelHandler(ModeHandler, ConditionJumpRelMode):
    """
    JC rel
    """
    opcode_set = jc_rel

    @property
    def condition(self):
        """
        :return: Check carry flag set command
        """
        return self.cpu.carry_flag.shell == True,


class JncRelHandler(ModeHandler, ConditionJumpRelMode):
    """
    JNC rel
    """
    opcode_set = jnc_rel

    @property
    def condition(self):
        """
        :return: Check if carry flag not set command.
        """
        return self.cpu.carry_flag.shell != True
