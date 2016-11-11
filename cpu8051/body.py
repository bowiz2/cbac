import cbac
from cbac.core.compound import Register
from cbac.core import mc_command
from cbac.unit.statements import *
from cbac import CBA
from cbac import std_unit

class MemoryFetcher(cbac.Unit):
    """
    Fetches the next byte to a register
    """
    def __init__(self, cpu):
        super(MemoryFetcher, self).__init__()
        self.cpu = cpu

    def architecture(self):
        self.read_unit
        PassParameters(self.increment_unit, self.accumulator),
        self.increment_unit.shell.activate(),
        self.increment_unit.callback_pivot.shell.tp(self.procedure(
                self.increment_unit.output.shell.copy(self.accumulator),
                self.done_opcode.shell.activate()
            ))

class Cpu8051(cbac.Unit):
    """
    represents a rCPU with the 8051 architecture.
    """
    @cbac.unit.auto_synthesis
    def __init__(self):
        super(Cpu8051, self).__init__(bits=8)
        self.ip_register = self.add_compound(Register(8))
        self.general_registers = [self.add_compound(Register(8)) for _ in xrange(8)]
        self.accumulator = self.add_compound(Register(self.bits))
        self.opcode = self.add_compound(Register(self.bits))

        self.increment_unit = self.add_unit(cbac.std_unit.IncrementUnit)
        # this register is signaled when the opcode operation is complete.
        self.done_opcode = self.add_compound(Register(1))

        self.access_unit = std_unit.MemoryAccessUnit()
        self.write_unit = self.add_unit(std_unit.WriteUnit(8, self.access_unit))
        self.read_unit = self.add_unit(std_unit.ReadUnit(8, self.access_unit))

    def architecture(self):

        yield mc_command.say("hello and welcome!")

        yield If(self.opcode_is(0x00)).then(
            self.done_opcode.shell.activate()
        )

        # MOV A, RX
        base = 0xE8
        for i in xrange(base, base+8):
            yield If(self.opcode.shell.testforblocks(self.constant_factory(i))).then(
                self.accumulator.shell.copy(self.general_registers[i - base]),
                self.done_opcode.shell.activate()
            )

        base = 0xF8
        for i in xrange(base, base+8):
            yield If(self.opcode_is(i)).then(
                self.general_registers[i - base].shell.copy(self.accumulator),
                self.done_opcode.shell.activate()
            )
        # INC RX
        base = 0x08
        for i in xrange(base, base+8):
            yield If(self.opcode_is(i)).then(
                PassParameters(self.increment_unit, self.general_registers[i - base]),
                self.increment_unit.shell.activate(),
                self.increment_unit.callback_pivot.shell.tp(self.procedure(
                        self.increment_unit.output.shell.copy(self.general_registers[i - base]),
                        self.done_opcode.shell.activate()
                    )
                )
            )
        # TODO: fix code duplication.
        yield If(self.opcode_is(0x04)).then(
            PassParameters(self.increment_unit, self.accumulator),
            self.increment_unit.shell.activate(),
            self.increment_unit.callback_pivot.shell.tp(self.procedure(
                    self.increment_unit.output.shell.copy(self.accumulator),
                    self.done_opcode.shell.activate()
                ))
        )

    def procedure(self, *commands):
        return self.add_compound(CBA(*commands))

    def opcode_is(self, value):
        return self.opcode.shell.testforblocks(self.constant_factory(value))