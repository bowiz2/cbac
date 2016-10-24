"""
Test the units which are shipped in the sul package.
"""
from unittest import TestCase
import cbac
from cbac import assembler, BlockSpace
from cbac import std_unit
from cbac.unit import Unit
from cbac.unit.statements import *
from test.decorators import named_schematic
import cbac


class StdUnitTestCase(TestCase):
    """
    Test the standard unit library.
    """

    def setUp(self):
        self.schematic_path = "test_schematic.schematic"
        self.block_space = BlockSpace((100, 100, 100))

    def tearDown(self):
        self.block_space.pack()
        self.block_space.shrink()
        schematic = assembler.build(self.block_space)
        schematic.saveToFile(self.schematic_path)


class TestBitwiseUnits(StdUnitTestCase):
    @named_schematic
    def test_xxx(self):
        my_class = std_unit.NotGate.Array()
        self.block_space.add_unit(my_class(4))

    @named_schematic
    def test_or(self):
        self.block_space.add_unit(std_unit.OrGate.Array(4))

    @named_schematic
    def test_not(self):
        self.block_space.add_unit(std_unit.NotGate.Array(4))

    @named_schematic
    def test_reverse(self):
        self.block_space.add_unit(std_unit.ReverseUnit(4))

    @named_schematic
    def test_and(self):
        self.block_space.add_unit(std_unit.AndGate.Array(4))

    @named_schematic
    def test_nand(self):
        self.block_space.add_unit(std_unit.NandGate.Array(4))

    @named_schematic
    def test_incrament(self):
        self.block_space.add_unit(std_unit.IncrementUnit(4))

    @named_schematic
    def test_xor(self):
        self.block_space.add_unit(std_unit.XorGate.Array(4))

    @named_schematic
    def test_xnor(self):
        self.block_space.add_unit(std_unit.XnorGate.Array(4))

    @named_schematic
    def test_fulladder(self):
        inp = cbac.std_logic.InputRegister(3)
        output = cbac.std_logic.OutputRegister(2)
        self.block_space.add(inp, output)
        self.block_space.add_unit(
            std_unit.FullAdderUnit(inp.ports[0], inp.ports[1], output.ports[0], inp.ports[2], output.ports[1]))

    @named_schematic
    def test_ripple_carry_adder(self):
        self.block_space.add_unit(std_unit.full_adder.RippleCarryFullAdderArray(4))

    @named_schematic
    def test_negate_unit(self):
        self.block_space.add_unit(std_unit.NegateUnit(4))

    @named_schematic
    def test_subtract_unit(self):
        self.block_space.add_unit(std_unit.SubtractUnit(4))

    @named_schematic
    def test_listener(self):
        from cbac.core.compound import Register
        my_register = Register(2)
        self.block_space.add(my_register)
        self.block_space.add_unit(std_unit.IsActiveListener(my_register.blocks[0], my_register.blocks[1]))

    @named_schematic
    def test_shift(self):
        self.block_space.add_unit(std_unit.ShiftUnit(8, 1))
        self.block_space.add_unit(std_unit.ShiftUnit(8, 7))

    @named_schematic
    def test_multi(self):
        self.block_space.add_unit((std_unit.MultiUnit(2, inline_adder=True)))


class TestGate(TestCase):
    """Test the gate framework"""

    def test_naming(self):
        self.assertEqual(std_unit.NotGate.Array().__name__, "NotGateArray")

    def test_permutation(self):
        """
        check if
            my_array_class = MyGate.Array()
            array_instance = my_array_class(8)
        is equal to
            array_instance = MyGate.Array()(8)
        is equal to
            array_instance = MyGate.Array(8)
        """
        MyGate = std_unit.NotGate
        my_array_class = MyGate.Array()
        array_instance = my_array_class(8)
        self.assertEqual(array_instance.bits, 8)
        array_instance = MyGate.Array()(8)
        self.assertEqual(array_instance.bits, 8)
        array_instance = MyGate.Array(8)
        self.assertEqual(array_instance.bits, 8)


class TestStdUnitMemory(StdUnitTestCase):
    @named_schematic
    def test_memory_access(self):
        self.block_space.add_unit(std_unit.MemoryAccessUnit())

    @named_schematic
    def test_memory_read(self):
        """
        Test read unit
        """
        access_unit = std_unit.MemoryAccessUnit()
        read_unit = std_unit.ReadUnit(8, access_unit)
        self.block_space.add_unit(read_unit)

    @named_schematic
    def test_memory_write(self):
        """
        Test WriteUnit
        """
        access_unit = std_unit.MemoryAccessUnit()
        write_unit = std_unit.WriteUnit(8, access_unit)
        self.block_space.add_unit(write_unit)

    @named_schematic
    def test_read_write_shared(self):
        """
        Test the read and the write sharing the same memory box.
        """
        access_unit = std_unit.MemoryAccessUnit()
        write_unit = std_unit.WriteUnit(8, access_unit)
        read_unit = std_unit.ReadUnit(8, access_unit)
        self.block_space.add_unit(access_unit)
        self.block_space.add_unit(write_unit)
        self.block_space.add_unit(read_unit)

    @named_schematic
    def test_weird_memory_shared(self):
        access_unit = std_unit.MemoryAccessUnit((4, 1, 2), (4, 1, 4))
        self.block_space.add_unit(access_unit)


class Filler(Unit):
    """
    Used to test the functionality of a given unit by iterating in minecraft-time over all the register values.
    See use in test integration and test screen.
    """

    def __init__(self, bits, incrementer, writer):
        super(Filler, self).__init__(bits)
        # == Here you declare all your memory slots.
        self.writer = self.add_unit(writer)
        self.incrementer = self.add_unit(incrementer)
        # ==
        self.synthesis()

    def architecture(self):
        """
        main logic commands.
        :return:
        """
        yield InlineCall(self.writer, self.incrementer.output, self.incrementer.output)
        yield InlineCall(self.incrementer, self.incrementer.output)


# class TestIntegration(SULTestCase):
#     @named_schematic
#     def test_write_increment(self):
#         access_unit = std_unit.MemoryAccessUnit()
#         write_unit = std_unit.WriteUnit(8, access_unit)
#         increment_unit = std_unit.IncrementUnit(8)
#         filler = Filler(8, increment_unit, write_unit)
#
#         self.block_space.add_unit(access_unit)
#         self.block_space.add_unit(write_unit)
#         self.block_space.add_unit(increment_unit)
#         self.block_space.add_unit(filler)


class TestScreen(StdUnitTestCase):
    @named_schematic
    def test_basic_screen(self):
        screen_access = std_unit.MemoryAccessUnit(
            (16, 1, 16), (6, 1, 8),
            cbac.schematics.screen.BLACK_SCREEN_128x128)
        screen = std_unit.ScreenUnit(cbac.schematics.charsets.ASCII, screen_access)
        incrementer = std_unit.IncrementUnit(8)
        filler = Filler(8, incrementer, screen)
        self.block_space.add_unit(filler)
        self.block_space.add_unit(incrementer)
        self.block_space.add_unit(screen_access)
        self.block_space.add_unit(screen)


class TestSubRegisterOperation(StdUnitTestCase):
    @named_schematic
    def test_slice(self):
        my_Register = cbac.Register(8)
        self.block_space.add(my_Register)
        self.block_space.add(cbac.CBA(
            my_Register.slice(xrange(2, 5)).shell.set_max_value()
        ))


class TestMisc(StdUnitTestCase):

    @named_schematic
    def test_view_detector(self):
        self.block_space.size = (20, 200, 20)
        self.block_space.add_unit(std_unit.ViewDetectorVerticalUnit(cbac.Player(all_players=True)))

    @named_schematic
    def test_view_detector_horizontal(self):
        self.block_space.size = (20, 200, 20)
        self.block_space.add_unit(std_unit.ViewDetectorHorizonatlUnit(cbac.Player(all_players=True)))
