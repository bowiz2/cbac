import cbac
from cbac import std_unit
from cbac.core.compound import Register
from cbac.unit.statements import *
from cpu8051.opcode import *
import cpu8051.handlers


class MemoryFetcher(cbac.Unit):
    """
    Fetches the next byte to a register
    """

    @cbac.unit.auto_synthesis
    def __init__(self, cpu, fetch_destination):
        super(MemoryFetcher, self).__init__()
        self.cpu = cpu
        self.fetch_destination = fetch_destination

    def architecture(self):
        yield self.cpu.ip_register.shell.copy(self.cpu.read_unit.address_input)
        yield MainLogicJump(self.cpu.read_unit)
        yield self.cpu.read_unit.read_output.shell.copy(self.fetch_destination)
        yield self.cpu.ip_register.shell.copy(self.cpu.increment_unit.input)
        yield MainLogicJump(self.cpu.increment_unit)
        yield self.cpu.increment_unit.output.shell.copy(self.cpu.ip_register)


class Cpu8051(cbac.Unit):
    """
    represents a rCPU with the 8051 architecture.
    """

    @cbac.unit.auto_synthesis
    def __init__(self, data=None):
        if not data:
            data = [0] * 256
        super(Cpu8051, self).__init__(bits=8)
        self.ip_register = self.add_compound(Register(8))
        self.process_registers = [self.add_compound(Register(8)) for _ in xrange(2)]
        self.general_registers = [self.add_compound(Register(8)) for _ in xrange(8)]
        self.accumulator = self.add_compound(Register(self.bits))
        self.opcode = self.process_registers[0]

        self.increment_unit = self.add_unit(cbac.std_unit.IncrementUnit)

        self.adder_unit = self.add_unit(cbac.std_unit.RippleCarryFullAdderArray)

        # this register is signaled when the opcode operation is complete.
        self.done_opcode = self.add_compound(Register(1))

        self.access_unit = self.add_unit(std_unit.MemoryAccessUnit(memory_dump=std_unit.MemoryDump(data)))

        self.write_unit = self.add_unit(std_unit.WriteUnit(8, self.access_unit))
        self.read_unit = self.add_unit(std_unit.ReadUnit(8, self.access_unit))

        self.second_fetcher = self.add_unit(MemoryFetcher(self, self.process_registers[1]))

        self.address_fetcher = self.add_unit(MemoryFetcher(self, self.read_unit.address_input))

        self.pivot_reset = self.procedure(
            mc_command.say("Pivot Reset"),
            *[pivot.shell.summon(self.callback_pivot_home) for pivot in cbac.core.mcentity.pivot.Pivot._all]
        )

    def set_initial_memory(self, data):
        """
        Sets the initial memory of the cpu.
        """
        dump=
        self.cpu.add_compound()
        self.access_unit.raw_memory = self.access_unit.add_compound(

        )

    def architecture(self):
        yield mc_command.say("hello and welcome!")
        yield MainLogicJump(self.add_unit(MemoryFetcher(self, self.process_registers[0])))
        yield mc_command.say("After first fetch!")

        yield InlineCall(self.add_unit(cpu8051.handlers.nop.Nop()))

        yield InlineCall(self.add_unit(cpu8051.handlers.mov.MovARx()))
        yield InlineCall(self.add_unit(cpu8051.handlers.mov.MovRxA()))
        yield InlineCall(self.add_unit(cpu8051.handlers.mov.MovRxData()))
        yield InlineCall(self.add_unit(cpu8051.handlers.mov.MovRxAddr()))

        yield InlineCall(self.add_unit(cpu8051.handlers.inc.IncRx()))
        yield InlineCall(self.add_unit(cpu8051.handlers.inc.IncA()))
        yield InlineCall(self.add_unit(cpu8051.handlers.inc.IncAddr()))

    def opcode_is(self, value):
        return self.opcode.shell.testforblocks(self.constant_factory(value))

# class Mov(cbac.Unit):
#     @cbac.unit.auto_callback
#     def __init__(self):
