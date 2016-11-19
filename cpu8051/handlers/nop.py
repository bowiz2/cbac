from cpu8051.handlers.handler import Handler
from cbac.unit.statements import *


class Nop(Handler):
    encoding = "00000000"

    def architecture(self):
        yield If(self.cpu.opcode_is(self.opcode)).then(
            self.cpu.done_opcode.shell.activate()
        )
