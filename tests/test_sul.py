from unittest import TestCase

import cbac.assembler
import sul
from cbac.blockspace import BlockSpace
from decorators import save_schematic


def sample_schematic(unit_class, size, blockspace_size=(30, 10, 30)):
    u = unit_class(size)
    block_space = BlockSpace(blockspace_size)
    block_space.add_unit(u)
    block_space.pack()
    block_space.shrink()
    schematic = cbac.assembler.build(block_space)
    return schematic
# TODO: rewrite test for fixure for each unit.
class TestSUL(TestCase):
    """
    Test the standard unit library.
    """


    @save_schematic
    def test_or(self):
        return sample_schematic(sul.OrUnit, 4)

    @save_schematic
    def test_not(self):
        return sample_schematic(sul.NotUnit, 4)

    @save_schematic
    def test_reverse(self):
        return sample_schematic(sul.ReverseUnit, 4)

    @save_schematic
    def test_and(self):
        return sample_schematic(sul.AndUnit, 4)

    @save_schematic
    def test_nand(self):
        return sample_schematic(sul.NandUnit, 4)

    @save_schematic
    def test_shift(self):
        return sample_schematic(sul.ShiftUnit, 8)

    @save_schematic
    def test_incrament(self):
        return sample_schematic(sul.IncrementUnit, 4, (100, 100, 100))

    @save_schematic
    def test_callback(self):
        return sample_schematic(sul.CallbackUnit, 4)

    @save_schematic
    def test_xor(self):
        return sample_schematic(sul.XorUnit, 4)

    @save_schematic
    def test_xnor(self):
        return sample_schematic(sul.XnorUnit, 4)

    @save_schematic
    def test_fulladder(self):
        return sample_schematic(sul.FullAdderUnit, 4, (200, 200, 200))

    @save_schematic
    def test_negate_unit(self):
        return sample_schematic(sul.NegateUnit, 4)

    @save_schematic
    def test_subtract_unit(self):
        return sample_schematic(sul.SubtractUnit, 4)


class TestSULMemory(TestCase):


    @save_schematic
    def test_memory_access(self):

        return sample_schematic(sul.MemoryAccessUnit, 8)

    @save_schematic
    def test_memory_read(self):
        access_unit = sul.MemoryAccessUnit(8)
        u = sul.ReadUnit(8, access_unit)
        block_space = BlockSpace((200,200,200))
        block_space.add_unit(u)
        block_space.pack()
        block_space.shrink()
        schematic = cbac.assembler.build(block_space)
        return schematic

    @save_schematic
    def test_memory_write(self):
        access_unit = sul.MemoryAccessUnit(8)
        u = sul.WriteUnit(8, access_unit)
        block_space = BlockSpace((200, 200, 200))
        block_space.add_unit(u)
        block_space.pack()
        block_space.shrink()
        schematic = cbac.assembler.build(block_space)
        return schematic