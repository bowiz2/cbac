from unittest import TestCase

import assembler
from blockspace import BlockSpace
from unit import OrUnit, NotUnit
from .const import SCHEMATIC_FORMAT


class TestUnit(TestCase):
    def test_or(self):
        u = OrUnit(4)
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
