from cbac.unit.decorators import auto_synthesis
from cbac.unit.statements import InlineCall
from cbac.unit.unit_base import Unit
from cbac import std_logic
from sul.increment_unit import IncrementUnit
from sul.not_gate import NotGate


class NegateUnit(Unit):
    """
    Negate a number using 2s compliment.
    """

    @auto_synthesis
    def __init__(self, bits=8, inp=std_logic.InputRegister, output=std_logic.OutputRegister, notter=NotGate.Array(),
                 incrementer=IncrementUnit):
        super(NegateUnit, self).__init__(bits)
        # == Here you declare all your memory slots.

        self.notter = self.add_unit(notter)
        self.incrementer = self.add_unit(incrementer)
        self.inp = self.add_input(inp)
        self.output = self.add_output(output)

    def architecture(self):
        # == Here you declare the commands wof the main logic. each command must be yielded out.
        yield InlineCall(self.notter, self.inp)
        yield InlineCall(self.incrementer, self.notter.outputs[0])
        yield self.incrementer.output.shell.copy(self.output)
