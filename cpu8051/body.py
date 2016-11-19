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

    def architecture(self):
        yield mc_command.say("hello and welcome!")
        yield MainLogicJump(self.add_unit(MemoryFetcher(self, self.process_registers[0])))
        yield mc_command.say("After first fetch!")
        yield InlineCall(cpu8051.handlers.mov.MovRxA)
        yield InlineCall(cpu8051.handlers.mov.MovARx)
        yield InlineCall(cpu8051.handlers.mov.MovRxAddr)
        yield InlineCall(cpu8051.handlers.mov.MovRxData)
        # # NOP
        # yield mc_command.say("after increment")
        # yield If(self.opcode_is(0x00)).then(
        #     self.done_opcode.shell.activate()
        # )

        # # TODO: fix code duplication.
        # # INC A
        # yield If(self.opcode_is(0x04)).then(
        #     PassParameters(self.increment_unit, self.accumulator),
        #     self.increment_unit.shell.activate(),
        #     self.increment_unit.callback_pivot.shell.tp(self.procedure(
        #             self.increment_unit.output.shell.copy(self.accumulator),
        #             self.done_opcode.shell.activate()
        #         ))
        # )
        # INC iram addr
        # yield If(self.opcode_is(INC_IRAM)).then(
        #     self.address_fetcher.shell.activate(),
        #     self.address_fetcher.callback_pivot.shell.tp(self.procedure(
        #         self.read_unit.shell.activate(),
        #         self.read_unit.callback_pivot.shell.tp(self.procedure(
        #             self.read_unit.read_output.shell.copy(self.increment_unit.input),
        #             self.increment_unit.shell.activate(),
        #             self.increment_unit.callback_pivot.shell.tp(self.procedure(
        #                 self.increment_unit.output.shell.store_to_temp(),
        #                 self.read_unit.memory_access_unit.pivot.shell.load_from_temp(self.increment_unit.output),
        #                 self.done_opcode.shell.activate()
        #             ))
        #         ))
        #     ))
        # )

        # # INC RX
        # base = 0x08
        # for i in xrange(base, base+8):
        #     yield If(self.opcode_is(i)).then(
        #         PassParameters(self.increment_unit, self.general_registers[i - base]),
        #         self.increment_unit.shell.activate(),
        #         self.increment_unit.callback_pivot.shell.tp(self.procedure(
        #                 self.increment_unit.output.shell.copy(self.general_registers[i - base]),
        #                 self.done_opcode.shell.activate()
        #             )
        #         )
        #     )

        yield InlineCall(cpu8051.handlers.mov.MovRxA)

    def opcode_is(self, value):
        return self.opcode.shell.testforblocks(self.constant_factory(value))

# class Mov(cbac.Unit):
#     @cbac.unit.auto_callback
#     def __init__(self):
