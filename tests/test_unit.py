from unittest import TestCase
from unit import ReverseUnit, NotUnit, OrUnit
import assembler
from blockspace import BlockSpace
import unit

from .decorators import save_schematic


class TestUnit(TestCase):
    @save_schematic
    def test_or(self):
        u = unit.OrUnit(4)
        block_space = BlockSpace((30, 10, 30), *u.compounds)
        schematic = assembler.build(block_space)
        return schematic

    @save_schematic
    def test_not(self):
        u = NotUnit(4)
        block_space = BlockSpace((30, 10, 30), *u.compounds)
        schematic = assembler.build(block_space)
        return schematic

    @save_schematic
    def test_reverse(self):
        u = ReverseUnit(4)
        block_space = BlockSpace((30, 10, 30), *u.compounds)
        schematic = assembler.build(block_space)
        return schematic
