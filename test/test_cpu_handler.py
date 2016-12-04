from unittest import TestCase

from cpu8051.handlers.jmp import JZHandler
from cpu8051.handlers.mode import AMode, DirectMode, DirectDataMode
from cpu8051.opcode import OpcodeSet, declared_opcodes
from test_std_unit import StdUnitTestCase, named_schematic
from cpu8051.body import Cpu8051
from cpu8051 import handlers
import collections

MAX_VALUE = 255

class TestModeHandlers(TestCase):
    def test_bytes(self):
        self.assertEqual(AMode().bytes, 1)
        self.assertEqual(DirectMode().bytes, 2)
        self.assertEqual(DirectDataMode().bytes, 3)

def duplicates(l):
    return [item for item, count in collections.Counter(l).items() if count > 1]


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

    def test_sanity(self):
        op_values = []
        for opcode in declared_opcodes:
            op_values += [opcode.get_single()]
        dups = duplicates(op_values)
        error = ""
        for dup in dups:
            error += "Duplicates for {} are:\n".format(bin(dup))
            for opcode in declared_opcodes:
                if opcode.match(dup):
                    error += "\t" + opcode.encoding + "\n"

        assert len(dups) is 0, "There are opcode duplicates.\n" + error


class TestCpuHandler(StdUnitTestCase):
    cpu = Cpu8051(auto_synthesis=False)

    def setUp(self):
        super(TestCpuHandler, self).setUp()
        self.memory = [0] * 256
        self.handler = None  # type: handlers.handler.Handler
        self._next_fetched_byte = 1
        self.cpu.ip_register.set_initial_value(self._next_fetched_byte)

    def tearDown(self):
        blacklist = []

        if not self.handler.uses_adder:
            blacklist.append(self.cpu.adder_unit)

        if not self.handler.uses_and_unit:
            blacklist.append(self.cpu.and_unit)

        if not self.handler.uses_memory:
            blacklist += self.cpu.memory_units

        self.cpu.build_blacklist = blacklist

        self.block_space.add_unit(self.handler)
        self.block_space.add_unit(self.cpu)

        self.cpu.opcode.set_initial_value(self.handler.opcode_set.get_single())

        self.cpu.set_initial_memory(self.memory)
        super(TestCpuHandler, self).tearDown()

    @property
    def next_fetched_byte(self):
        """
        The next byte index which will be fetched.
        :return:
        """
        to_ret = self._next_fetched_byte
        self._next_fetched_byte += 1
        return to_ret


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
        self.cpu.sys_flags.set_initial_value(1)  # set the include carry flag to 1
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

    @named_schematic
    def test_addc_a_ri(self):
        self.handler = handlers.AddcARiHandler(self.cpu, debug=True)
        addr = 255
        self.memory[addr] = self.SECOND_OPRAND_VALUE
        self.cpu.general_registers[0].set_initial_value(addr)

    @named_schematic
    def test_addc_a_data(self):
        self.handler = handlers.AddcADataHandler(self.cpu, debug=True)
        self.memory[self.cpu.ip_register._value] = self.SECOND_OPRAND_VALUE


class TestAnlHanlders(TestCpuHandler):
    # TODO: implement the rest of the handler.
    @named_schematic
    def test_anl_a_rx(self):
        self.handler = handlers.AnlARxHandler(self.cpu, debug=True)
        self.cpu.accumulator.set_initial_value(0b00001111)
        self.cpu.general_registers[0].set_initial_value(0b00111100)

    @named_schematic
    def test_anl_direct_a(self):
        self.handler = handlers.AnlDirectA(self.cpu, debug=True)
        self.cpu.accumulator.set_initial_value(0b00111100)
        addr = 255
        self.memory[addr] = 0b00001111
        self.cpu.general_registers[0].set_initial_value(addr)

class TestDecHandlers(TestCpuHandler):
    @named_schematic
    def test_dec_a(self):
        self.handler = handlers.DecAHandler(self.cpu, debug=True)
        self.cpu.accumulator.set_initial_value(4)

class TestJmp(TestCpuHandler):
    @named_schematic
    def test_jz(self):
        self.handler = JZHandler(self.cpu, debug=True)
        self.memory[self.next_fetched_byte] = MAX_VALUE
