from cpu8051.opcode import *
from cpu8051.handlers.handler import Handler
from cbac.unit.statements import *


class Nop(Handler):
    opcode_set = nop

    def handle(self, _=None):
        yield self.cpu.done_opcode.shell.activate()
