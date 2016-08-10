from unittest import TestCase
from unit import ReverseUnit, NotUnit, OrUnit
import assembler
from blockspace import BlockSpace
import unit
from .const import SCHEMATIC_FORMAT


class TestUnit(TestCase):
    def test_or(self):
        u = unit.OrUnit(4)
        block_space = BlockSpace((30, 10, 30), *u.compounds)
        schematic = assembler.build(block_space)
        schematic.saveToFile(
            SCHEMATIC_FORMAT.format(self.__class__.__name__, self.test_or.__name__))

    def test_not(self):
        u = NotUnit(4)
        block_space = BlockSpace((30, 10, 30), *u.compounds)
        schematic = assembler.build(block_space)
        schematic.saveToFile(
            SCHEMATIC_FORMAT.format(self.__class__.__name__, self.test_not.__name__))


    def test_reverse(self):
        u = ReverseUnit(4)
        block_space = BlockSpace((30, 10, 30), *u.compounds)
        schematic = assembler.build(block_space)
        schematic.saveToFile(
            SCHEMATIC_FORMAT.format(self.__class__.__name__, self.test_reverse.__name__))
