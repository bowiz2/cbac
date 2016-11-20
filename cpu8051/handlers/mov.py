from cpu8051.handlers.handler import Handler
from cpu8051.opcode import *


class MovARx(Handler):
    """
    MOV A, RX
    """
    opcode_set = mov_a_rx

    def handle(self, i=None):
        yield self.cpu.accumulator.shell.copy(self.get_register(i)),
        yield self.cpu.done_opcode.shell.activate()


class MovRxA(Handler):
    """
    MOV RX, A
    """
    opcode_set = mov_rx_a

    def handle(self, i=None):
        yield self.get_register(i).shell.copy(self.cpu.accumulator)
        yield self.cpu.done_opcode.shell.activate()


class MovRxData(Handler):
    """
    MOV RX, data
    """
    opcode_set = mov_rx_data

    def handle(self, i=None):
        yield self.cpu.second_fetcher.shell.activate(),
        yield self.cpu.second_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
            self.cpu.process_registers[1].shell.copy(self.get_register(i)),
            self.cpu.done_opcode.shell.activate()
        ))


class MovRxAddr(Handler):
    """
    MOV RX, @iram addr
    """
    opcode_set = mov_rx_addr

    def handle(self, i=None):
        yield self.cpu.address_fetcher.shell.activate(),
        yield self.cpu.address_fetcher.callback_pivot.shell.tp(self.cpu.procedure(
            self.cpu.read_unit.shell.activate(),
            self.cpu.read_unit.callback_pivot.shell.tp(self.cpu.procedure(
                self.cpu.read_unit.read_output.shell.copy(self.get_register(i)),
                self.cpu.done_opcode.shell.activate())
            )
        ))


__all__ = ["MovRxAddr", "MovRxData", "MovARx", "MovRxA"]
