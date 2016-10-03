from test_sul import SULTestCase
from cbac.unit.vision import AndXBit
from test.decorators import named_schematic


class TestVision(SULTestCase):
    @named_schematic
    def test_a(self):
        a = AndXBit(8)
        self.block_space.add_unit(a)
