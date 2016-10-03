from test_sul import SULTestCase
from cbac.unit.vision import LogicArray
from test.decorators import named_schematic


class TestVision(SULTestCase):
    @named_schematic
    def test_a(self):
        a = LogicArray(8, auto_synthesis=False)
        a.synthesis()
        self.block_space.add_unit(a)