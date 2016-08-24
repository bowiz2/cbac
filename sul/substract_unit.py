from cbac.unit.unit_base import Unit
from cbac.unit.statements import STDCall

from sul import NegateUnit, FullAdderUnit


class SubtractUnit(Unit):
    def __init__(self, bits=8, negate_unit=None, full_adder=None):
        super(SubtractUnit, self).__init__(bits)

        # == Here you declare all your memory slots.
        if negate_unit is None:
            negate_unit = NegateUnit(self.bits)

        if full_adder is None:
            full_adder = FullAdderUnit(self.bits)

        assert negate_unit.bits == self.bits
        assert full_adder.bits == self.bits

        self.full_adder = self.add_unit(full_adder)
        self.negate_unit = self.add_unit(negate_unit)

        self.input_a = self.create_input(self.bits)
        self.input_b = self.create_input(self.bits)
        self.output = self.create_output(self.bits)
        # ==
        self.synthesis()

    def main_logic_commands(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        yield STDCall(self.negate_unit, self.input_b)
        yield STDCall(self.full_adder, self.input_a, self.negate_unit.output)
        yield self.full_adder.output.shell.copy(self.output)
