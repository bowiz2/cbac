from cpu8051.handlers.handler import Handler
from cbac.unit.statements import *


class MovARx(Handler):
    """
    MOV A, RX
    """
    encoding = "11101rrr"

    def architecture(self):
        yield mc_command.say("Mov A Rx")
        for i in self.opcodes:
            yield If(self.cpu.opcode_is(i)).then(
                self.cpu.accumulator.shell.copy(self.get_register(i)),
                self.cpu.done_opcode.shell.activate()
            )


class MovRxA(Handler):
    """
    MOV RX, A
    """
    encoding = "11111rrr"

    def architecture(self):
        yield mc_command.say("Mov Rx A")
        for i in self.opcodes:
            yield If(self.cpu.opcode_is(i)).then(
                self.get_register(i).shell.copy(self.cpu.accumulator),
                self.cpu.done_opcode.shell.activate()
            )


class MovRxData(Handler):
    """
    MOV RX, data
    """
    encoding = "01111rrr"

    def architecture(self):
        for i in self.opcodes:
            yield If(self.cpu.opcode_is(i)).then(
                self.cpu.second_fetcher.shell.activate(),
                self.cpu.second_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
                    self.cpu.process_registers[1].shell.copy(self.get_register(i)),
                    self.cpu.done_opcode.shell.activate()
                ))
            )


class MovRxAddr(Handler):
    """
    MOV RX, @iram addr
    """
    encoding = "10101rrr"

    def architecture(self):
        for i in self.opcodes:
            yield If(self.cpu.opcode_is(i)).then(
                self.cpu.address_fetcher.shell.activate(),
                self.cpu.address_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
                    self.cpu.read_unit.shell.activate(),
                    self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
                        self.cpu.read_unit.read_output.shell.copy(self.get_register(i)),
                        self.cpu.done_opcode.shell.activate())
                    )
                ))
            )
