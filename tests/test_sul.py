from unittest import TestCase

import cbac.assembler
import sul
from cbac.blockspace import BlockSpace
from decorators import save_schematic


class SULTestCase(TestCase):
    """
    Test the standard unit library.
    """

    def setUp(self):
        self.block_space = BlockSpace((100, 100, 100))

    @save_schematic
    def tearDown(self):
        self.block_space.pack()
        self.block_space.shrink()
        schematic = cbac.assembler.build(self.block_space)
        return schematic


class TestBitwiseUnits(SULTestCase):
    def test_or(self):
        self.block_space.add_unit(sul.OrUnit(8))

    def test_not(self):
        self.block_space.add_unit(sul.NotUnit(4))

    def test_reverse(self):
        self.block_space.add_unit(sul.ReverseUnit(4))

    def test_and(self):
        self.block_space.add_unit(sul.AndUnit(4))

    def test_nand(self):
        self.block_space.add_unit(sul.NandUnit(4))

    def test_shift(self):
        self.block_space.add_unit(sul.ShiftUnit(8))

    def test_incrament(self):
        self.block_space.add_unit(sul.IncrementUnit(4))

    def test_xor(self):
        self.block_space.add_unit(sul.XorUnit(4))

    def test_xnor(self):
        self.block_space.add_unit(sul.XnorUnit(4))

    def test_fulladder(self):
        self.block_space.add_unit(sul.FullAdderUnit(4))

    def test_negate_unit(self):
        self.block_space.add_unit(sul.NegateUnit(4))

    def test_subtract_unit(self):
        self.block_space.add_unit(sul.SubtractUnit(4))


class TestSULMemory(SULTestCase):
    def test_memory_access(self):
        self.block_space.add_unit(sul.MemoryAccessUnit(8))

    def test_memory_read(self):
        """
        Test read unit
        """
        access_unit = sul.MemoryAccessUnit(8)
        read_unit = sul.ReadUnit(8, access_unit)
        self.block_space.add_unit(read_unit)

    def test_memory_write(self):
        """
        Test WriteUnit
        """
        access_unit = sul.MemoryAccessUnit(8)
        write_unit = sul.WriteUnit(8, access_unit)
        self.block_space.add_unit(write_unit)

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
