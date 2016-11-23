from test_std_unit import StdUnitTestCase, named_schematic
from cpu8051.body import Cpu8051
from cpu8051 import opcode
from cpu8051 import handlers

MAX_VALUE = 255


class TestCpuHandelrs(StdUnitTestCase):
    def setUp(self):
        super(TestCpuHandelrs, self).setUp()
        self.cpu = Cpu8051(auto_synthesis=False)
        self.memory = [0] * 256
        self.handler = None  # type: handlers.handler.Handler
        self.after_first_fetch = True

    def tearDown(self):
        self.block_space.add_unit(self.handler)
        self.block_space.add_unit(self.cpu)

        if self.after_first_fetch:
            self.cpu.ip_register.set_initial_value(1)

        self.cpu.opcode.set_initial_value(self.handler.opcode_set.get_single())

        self.cpu.set_initial_memory(self.memory)
        super(TestCpuHandelrs, self).tearDown()

    @named_schematic
    def test_mov_rx_a(self):
        self.handler = handlers.mov.MovRxA(self.cpu, debug=True)
        self.cpu.accumulator.set_initial_value(MAX_VALUE)

    @named_schematic
    def test_mov_a_rx(self):
        self.handler = handlers.mov.MovARx(self.cpu, debug=True)
        self.cpu.general_registers[0].set_initial_value(MAX_VALUE)

    @named_schematic
    def test_mov_rx_data(self):
        self.handler = handlers.mov.MovRxData(self.cpu, debug=True)
        self.memory[self.cpu.ip_register._value] = MAX_VALUE

    @named_schematic
    def test_mov_rx_addr(self):
        self.handler = handlers.mov.MovRxAddr(self.cpu, debug=True)
        addr = 255
        self.memory[addr] = 0b10101010
        self.memory[self.cpu.ip_register._value] = addr