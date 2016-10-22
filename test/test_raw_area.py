from test_std_unit import StdUnitTestCase
from test.decorators import named_schematic
from pymclevel import MCSchematic


class TestRawArea(StdUnitTestCase):
    @named_schematic
    def test_schematic(self):
        self.block_space.add(MCSchematic(filename="../schem/az_caps_compressed.schematic"))
