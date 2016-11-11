from test_std_unit import StdUnitTestCase, named_schematic
from cpu8051.body import Cpu8051


class TestCpu(StdUnitTestCase):
    @named_schematic
    def test_body(self):
        self.block_space.add_unit(Cpu8051())
