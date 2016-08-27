from cbac.unit.statements import STDCall
from cbac.unit.unit_base import Unit
from increment_unit import IncrementUnit
from not_unit import NotUnit


class NegateUnit(Unit):
    def __init__(self, bits=8, not_unit=None, increment_unit=None):
        super(NegateUnit, self).__init__(bits)
        # == Here you declare all your memory slots.

        if not_unit is None:
            not_unit = NotUnit(self.bits)
        if increment_unit is None:
            increment_unit = IncrementUnit(self.bits)

        assert not_unit.bits == self.bits
        assert increment_unit.bits == self.bits

        self.not_unit = self.add_unit(not_unit)
        self.increment_unit = self.add_unit(increment_unit)
        self.input = self.create_input(self.bits)
        self.output = self.create_output(self.bits)
        # ==
        self.synthesis()

    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        yield STDCall(self.not_unit, self.input)
        yield STDCall(self.increment_unit, self.not_unit.output)
        yield self.increment_unit.output.shell.copy(self.output)
