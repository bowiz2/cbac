from cpu8051.handlers.handler import Handler
from cbac.unit.statements import *


class MovARx(Handler):
    """
    MOV A, RX
    """
    @property
    def encoding(self):
        return "11101rrr"

    def architecture(self):
        yield mc_command.say("This is mov")
        for i in self.opcodes:
            yield If(self.cpu.opcode_is(i)).then(
                self.cpu.accumulator.shell.copy(self.get_register(i)),
                self.cpu.done_opcode.shell.activate()
            )


class MovRxA(Handler):
    """
    MOV RX, A
    """

    @property
    def encoding(self):
        return "11111rrr"

    def architecture(self):
        yield mc_command.say("This is mov")
        for i in self.opcodes:
            yield If(self.cpu.opcode_is(i)).then(
                self.get_register(i).shell.copy(self.cpu.accumulator),
                self.cpu.done_opcode.shell.activate()
            )