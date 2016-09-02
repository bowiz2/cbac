from unittest import TestCase

import cbac.assembler
import sul
from cbac.blockspace import BlockSpace


from decorators import named_schematic
from cbac.unit import Unit
from cbac.unit.statements import *



class SULTestCase(TestCase):
    """
    Test the standard unit library.
    """

    def setUp(self):
        self.schematic_path = "test_schematic.schematic"
        self.block_space = BlockSpace((100, 100, 100))


    def tearDown(self):
        self.block_space.pack()
        self.block_space.shrink()
        schematic = cbac.assembler.build(self.block_space)
        schematic.saveToFile(self.schematic_path)


class TestBitwiseUnits(SULTestCase):
    @named_schematic
    def test_or(self):
        self.block_space.add_unit(sul.OrUnit(8))

    @named_schematic
    def test_not(self):
        self.block_space.add_unit(sul.NotUnit(4))

    @named_schematic
    def test_reverse(self):
        self.block_space.add_unit(sul.ReverseUnit(4))

    @named_schematic
    def test_and(self):
        self.block_space.add_unit(sul.AndUnit(4))

    @named_schematic
    def test_nand(self):
        self.block_space.add_unit(sul.NandUnit(4))

    @named_schematic
    def test_shift(self):
        self.block_space.add_unit(sul.ShiftUnit(8))

    @named_schematic
    def test_incrament(self):
        self.block_space.add_unit(sul.IncrementUnit(4))

    @named_schematic
    def test_xor(self):
        self.block_space.add_unit(sul.XorUnit(4))

    @named_schematic
    def test_xnor(self):
        self.block_space.add_unit(sul.XnorUnit(4))

    @named_schematic
    def test_fulladder(self):
        self.block_space.add_unit(sul.FullAdderUnit(4))

    @named_schematic
    def test_negate_unit(self):
        self.block_space.add_unit(sul.NegateUnit(4))

    @named_schematic
    def test_subtract_unit(self):
        self.block_space.add_unit(sul.SubtractUnit(4))


class TestConcepts(SULTestCase):
    @named_schematic
    def test_callback(self):
        self.block_space.add_unit(sul.CallbackUnit(4))


class TestSULMemory(SULTestCase):
    @named_schematic
    def test_memory_access(self):
        self.block_space.add_unit(sul.MemoryAccessUnit(8))

    @named_schematic
    def test_memory_read(self):
        """
        Test read unit
        """
        access_unit = sul.MemoryAccessUnit(8)
        read_unit = sul.ReadUnit(8, access_unit)
        self.block_space.add_unit(read_unit)

    @named_schematic
    def test_memory_write(self):
        """
        Test WriteUnit
        """
        access_unit = sul.MemoryAccessUnit(8)
        write_unit = sul.WriteUnit(8, access_unit)
        self.block_space.add_unit(write_unit)

    @named_schematic
    def test_read_write_shared(self):
        """
        Test the read and the write sharing the same memory box.
        """
        access_unit = sul.MemoryAccessUnit(8)
        write_unit = sul.WriteUnit(8, access_unit)
        read_unit = sul.ReadUnit(8, access_unit)
        self.block_space.add_unit(access_unit)
        self.block_space.add_unit(write_unit)
        self.block_space.add_unit(read_unit)


class Filler(Unit):
    def __init__(self, bits, incrementer, writer):
        super(Filler, self).__init__(bits)
        # == Here you declare all your memory slots.
        self.writer = self.add_unit(writer)
        self.incrementer = self.add_unit(incrementer)
        # ==
        self.synthesis()

    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        yield InlineCall(self.writer, self.incrementer.output, self.incrementer.output)
        yield InlineCall(self.incrementer, self.incrementer.output)


class TestIntegration(SULTestCase):

    @named_schematic
    def test_write_increment(self):
        access_unit = sul.MemoryAccessUnit(8)
        write_unit = sul.WriteUnit(8, access_unit)
        increment_unit = sul.IncrementUnit(8)
        filler = Filler(8, increment_unit, write_unit)

        self.block_space.add_unit(access_unit)
        self.block_space.add_unit(write_unit)
        self.block_space.add_unit(increment_unit)
        self.block_space.add_unit(filler)
