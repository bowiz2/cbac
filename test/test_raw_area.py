from test_std_unit import StdUnitTestCase
from test.decorators import named_schematic
import cbac


class TestRawArea(StdUnitTestCase):
    @named_schematic
    def test_schematic(self):
        self.block_space.add(cbac.schematics.charsets.AZ_CAPS)
