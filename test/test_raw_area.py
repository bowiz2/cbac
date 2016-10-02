from test_sul import SULTestCase
from test.decorators import named_schematic
from pymclevel import MCSchematic


class TestRawArea(SULTestCase):
    @named_schematic
    def test_schematic(self):
        self.block_space.add(MCSchematic(filename="../schem/az_caps_compressed.schematic"))
