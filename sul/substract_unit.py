from cbac.unit import auto_synthesis
from cbac.unit.statements import InlineCall
from cbac.unit.unit_base import Unit
from cbac import std_logic
from sul.negate_unit import NegateUnit
from sul.full_adder import RippleCarryFullAdderArray


class SubtractUnit(Unit):
    """
    Simple bitwise substract unit.
    substract one register from another.
    """

    @auto_synthesis
    def __init__(self, bits=8, input_a=std_logic.InputRegister, input_b=std_logic.InputRegister,
                 output=std_logic.OutputRegister, negator=NegateUnit, adder=RippleCarryFullAdderArray):
        super(SubtractUnit, self).__init__(bits)
        self.adder = self.add_unit(adder)
        self.negator = self.add_unit(negator)

        self.input_a = self.add(input_a)
        self.input_b = self.add(input_b)
        self.output = self.add(output)

    def architecture(self):
        # First negate the first oprand.
        yield InlineCall(self.negator, self.input_b)
        # Then call the adder using the result of the negator as the second oprand.
        yield InlineCall(self.adder, self.input_a, self.negator.output)
        yield self.adder.output.shell.copy(self.output)
