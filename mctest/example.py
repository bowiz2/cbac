from cbac import Constant
from mctest.case import McTestCase
from mctest.assertion import assertEquals
from sul import IncrementUnit
from cbac.unit.statements import STDCall


class Sample(McTestCase):
    def test_ram(self):
        increment = IncrementUnit(4)
        self.add_unit(increment)
        num0 = Constant(0, 4)
        num4 = Constant(4, 4)
        num5 = Constant(5, 4)
        self.blockspace.add(num0)
        self.blockspace.add(num4)
        self.blockspace.add(num5)
        yield assertEquals(increment.output, num0)
        yield STDCall(increment, num4)
        yield assertEquals(increment.output, num5)


s = Sample()
s.build("C:/temp/example.schematic")
