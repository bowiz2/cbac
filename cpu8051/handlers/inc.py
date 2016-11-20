from cpu8051.handlers.handler import Handler
from cbac.unit.statements import *
from cpu8051.opcode import *


class IncA(Handler):
    """
    INC A
    """
    opcode_set = inc_a

    def handle(self, _=None):
        yield PassParameters(self.cpu.increment_unit, self.cpu.accumulator)
        yield self.cpu.increment_unit.shell.activate()
        yield self.cpu.increment_unit.callback_pivot.shell.tp(self.cpu.procedure(
            self.cpu.increment_unit.output.shell.copy(self.cpu.accumulator),
            self.cpu.done_opcode.shell.activate()
        ))


class IncAddr(Handler):
    """
    INC iram addr
    """
    opcode_set = int_addr

    def handle(self, _=None):
        yield self.cpu.address_fetcher.shell.activate(),
        yield self.cpu.address_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
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


class IncRx(Handler):
    """
    INC RX
    """
    opcode_set = inc_rx

    def handle(self, i=None):
        yield PassParameters(self.cpu.increment_unit, self.get_register(i)),
        yield self.cpu.increment_unit.shell.activate(),
        yield self.cpu.increment_unit.callback_pivot.shell.tp(self.cpu.procedure(
            self.cpu.increment_unit.output.shell.copy(self.get_register(i)),
            self.cpu.done_opcode.shell.activate()
        ))


__all__ = ["IncAddr", "IncRx", "IncA"]
