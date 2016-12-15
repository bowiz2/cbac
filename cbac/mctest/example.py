from cbac import HardwareConstant
from mctest import McTestCase, mctest, assertEquals
from cbac.std_unit import IncrementUnit
from mctest.statements import STDCall


class Sample(McTestCase):
    word_size = 4

    @mctest
    def test_ram(self):
        increment = self.add_unit(IncrementUnit)
        yield assertEquals(increment.output, self.constant_factory(0))
        yield STDCall(increment, self.constant_factory(4))
        yield assertEquals(increment.output, self.constant_factory(5))
