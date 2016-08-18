from unittest import TestCase

import assembler
from blockspace import BlockSpace
from unit import ReverseUnit, NotUnit, AndUnit, OrUnit, ShiftUnit, IncrementUnit, CallbackUnit, XorUnit, NandUnit, \
    XnorUnit, FullAdderUnit, TimerUnit
from .decorators import save_schematic


class TestUnit(TestCase):
    @staticmethod
    def sample_schematic(unit_class, size, blockspace_size=(30, 10, 30)):
        u = unit_class(size)
        block_space = BlockSpace(blockspace_size)
        block_space.add_unit(u)
        block_space.pack()
        block_space.shrink()
        schematic = assembler.build(block_space)
        return schematic

    @save_schematic
    def test_or(self):
        return self.sample_schematic(OrUnit, 4)

    @save_schematic
    def test_not(self):
        return self.sample_schematic(NotUnit, 4)

    @save_schematic
    def test_reverse(self):
        return self.sample_schematic(ReverseUnit, 4)

    @save_schematic
    def test_and(self):
        return self.sample_schematic(AndUnit, 4)

    @save_schematic
    def test_nand(self):
        return self.sample_schematic(NandUnit, 4)

    @save_schematic
    def test_shift(self):
        return self.sample_schematic(ShiftUnit, 8)

    @save_schematic
    def test_incrament(self):
        return self.sample_schematic(IncrementUnit, 4, (100, 100, 100))

    @save_schematic
    def test_callback(self):
        return self.sample_schematic(CallbackUnit, 4)

    @save_schematic
    def test_xor(self):
        return self.sample_schematic(XorUnit, 4)

    @save_schematic
    def test_xnor(self):
        return self.sample_schematic(XnorUnit, 4)

    @save_schematic
    def test_fulladder(self):
        return self.sample_schematic(FullAdderUnit, 4, (200, 200, 200))


    @save_schematic
    def test_timer(self):
        return self.sample_schematic(TimerUnit, 1000)
