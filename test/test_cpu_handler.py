from unittest import TestCase
from cpu8051.opcode import OpcodeSet
from test_std_unit import StdUnitTestCase, named_schematic
from cpu8051.body import Cpu8051
from cpu8051 import handlers

MAX_VALUE = 255


class TestOpcodeSet(TestCase):
    def setUp(self):
        self.subject = OpcodeSet("01rr", 8)

    def test_opcodes(self):
        self.assertEquals(max(self.subject.all()), 7)
        self.assertEquals(min(self.subject.all()), 4)

    def test_get_register(self):
        self.assertEquals(self.subject.get_arg(0b0111, 'r'), 0b11)

    def test_match(self):
        self.assertTrue(self.subject.match(0b0101))
        self.assertTrue(self.subject.match(0b0111))
        self.assertFalse(self.subject.match(0b1111))


class TestCpuHandler(StdUnitTestCase):
    def setUp(self):
        super(TestCpuHandler, self).setUp()
        self.cpu = Cpu8051(auto_synthesis=False)
        self.memory = [0] * 256
        self.handler = None  # type: handlers.handler.Handler
        self.cpu.ip_register.set_initial_value(1)

    def tearDown(self):
        self.block_space.add_unit(self.handler)
        self.block_space.add_unit(self.cpu)

        self.cpu.opcode.set_initial_value(self.handler.opcode_set.get_single())

        self.cpu.set_initial_memory(self.memory)
        super(TestCpuHandler, self).tearDown()


class TestMovHandlers(TestCpuHandler):
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


class TestAddHandlers(TestCpuHandler):
    A_INIT_VALUE = 5
    SECOND_OPRAND_VALUE = 3

    def setUp(self):
        super(TestAddHandlers, self).setUp()
        self.cpu.accumulator.set_initial_value(self.A_INIT_VALUE)

    @named_schematic
    def test_add_a_rx(self):
        self.handler = handlers.AddARxHandler(self.cpu, debug=True)
        self.cpu.general_registers[0].set_initial_value(self.SECOND_OPRAND_VALUE)

    @named_schematic
    def test_add_a_direct(self):
        self.handler = handlers.AddADirectHandler(self.cpu, debug=True)
        addr = 255
        self.memory[addr] = self.SECOND_OPRAND_VALUE
        self.memory[self.cpu.ip_register._value] = addr

    @named_schematic
    def test_add_a_ri(self):
        self.handler = handlers.AddARiHandler(self.cpu, debug=True)
        addr = 255
        self.memory[addr] = self.SECOND_OPRAND_VALUE
        self.cpu.general_registers[0].set_initial_value(addr)

    @named_schematic
    def test_add_a_data(self):
        self.handler = handlers.AddADataHandler(self.cpu, debug=True)
        self.memory[self.cpu.ip_register._value] = self.SECOND_OPRAND_VALUE


class TestAddcHandlers(TestCpuHandler):
    A_INIT_VALUE = 4
    SECOND_OPRAND_VALUE = 3

    def setUp(self):
        super(TestAddcHandlers, self).setUp()
        self.cpu.flags_register.set_initial_value(1)
        self.cpu.accumulator.set_initial_value(self.A_INIT_VALUE)

    @named_schematic
    def test_addc_a_rx(self):

        self.handler = handlers.AddcARxHandler(self.cpu, debug=True)
        self.cpu.general_registers[0].set_initial_value(self.SECOND_OPRAND_VALUE)

    @named_schematic
    def test_addc_a_direct(self):
        self.handler = handlers.AddcADirectHandler(self.cpu, debug=True)
        addr = 255
        self.memory[addr] = self.SECOND_OPRAND_VALUE
        self.memory[self.cpu.ip_register._value] = addr