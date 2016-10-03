from test_sul import SULTestCase
from simple_array import SimpleArray
from test.decorators import named_schematic


class TestVision(SULTestCase):
    @named_schematic
    def test_a(self):
        a = SimpleArray(8, auto_synthesis=False)
        a.synthesis()
        self.block_space.add_unit(a)