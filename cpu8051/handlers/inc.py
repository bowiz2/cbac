from cpu8051.handlers.handler import Handler
from cbac.unit.statements import *

class IncA(Handler):
    """
    INC A
    """
    encoding = "00000100"

    def architecture(self):
        # TODO: fix code duplication.
        # INC A
        yield If(self.cpu.opcode_is(self.opcode)).then(
            PassParameters(self.cpu.increment_unit, self.cpu.accumulator),
            self.cpu.increment_unit.shell.activate(),
            self.cpu.increment_unit.callback_pivot.shell.tp(self.cpu.procedure(
                    self.cpu.increment_unit.output.shell.copy(self.cpu.accumulator),
                    self.cpu.done_opcode.shell.activate()
                )))
class IncAddr(Handler):
    """
    INC iram addr
    """
    encoding = "00000101"

    def architecture(self):
        yield If(self.cpu.opcode_is(self.opcode)).then(
            self.cpu.address_fetcher.shell.activate(),
            self.cpu.address_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
                self.cpu.read_unit.shell.activate(),
                self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
                    self.cpu.read_unit.read_output.shell.copy(self.cpu.increment_unit.input),
                    self.cpu.increment_unit.shell.activate(),
                    self.cpu.increment_unit.callback_pivot.shell.tp(self.cpu.procedure(
                        self.cpu.increment_unit.output.shell.store_to_temp(),
                        self.cpu.read_unit.memory_access_unit.pivot.shell.load_from_temp(self.cpu.increment_unit.output),
                        self.cpu.done_opcode.shell.activate()
                    ))
                ))
            ))
        )
class IncRx(Handler):
    """
    INC RX
    """
    encoding = "00001rrr"

    def architecture(self):
        for i in self.opcodes:
            yield If(self.cpu.opcode_is(i)).then(
                PassParameters(self.cpu.increment_unit, self.get_register(i)),
                self.cpu.increment_unit.shell.activate(),
                self.cpu.increment_unit.callback_pivot.shell.tp(self.cpu.procedure(
                        self.cpu.increment_unit.output.shell.copy(self.get_register(i)),
                        self.cpu.done_opcode.shell.activate()
                    )
                )
            )