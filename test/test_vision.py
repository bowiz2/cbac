from test_sul import SULTestCase
from sul.simple_array import SimpleArray
from sul.and_unit import AndGate
from test.decorators import named_schematic


class TestVision(SULTestCase):
    @named_schematic
    def test_a(self):
        a = SimpleArray(AndGate, 8)
        self.block_space.add_unit(a)