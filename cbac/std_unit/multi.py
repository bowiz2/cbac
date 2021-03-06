"""Holds example unit"""
from cbac.unit import auto_synthesis
from cbac.unit.statements import *
from cbac.unit.unit_base import Unit
from cbac import std_logic
from cbac.std_unit.full_adder import RippleCarryFullAdderArray
from cbac.std_unit.shift_unit import ShiftUnit


class MultiUnit(Unit):
    """
    This is a hardwere multiplication unit.
    I wrote this unit when I was drunk.
    """

    # Don't forget to synthesis, It will synthesis you unit after the constructor. You can also do it manually.
    # By calling self.synthesis()
    @auto_synthesis
    def __init__(self, bits=8, input_a=std_logic.InputRegister, input_b=std_logic.InputRegister,
                 adder_class=RippleCarryFullAdderArray, inline_adder=True):
        super(MultiUnit, self).__init__(bits)

        self.input_a = self.add_input(input_a)
        self.input_b = self.add_input(input_b)

        # TODO: dependency injection
        self.shift_results = [self.add(std_logic.OutputRegister(self.bits * 2)) for _ in xrange(self.bits)]
        self.shifters = [
            self.add_unit(ShiftUnit(self.bits, i, inp=self.input_a, output=self.shift_results[i], no_reset=True)) for i
            in xrange(1, self.bits)]

        # Not we are not synthesizing them yet.
        self.adder = self.add_unit(adder_class(self.bits * 2))
        self.inline_adder = inline_adder

    def architecture(self):
        """
        Here you declare the commands of the main logic. each command must be yielded out.
        Each statement which is yielded out will be parsed.
        you can read about the statement which can be used here in the cbac.unit.statement module.
        """
        for outputs in [shifter.outputs for shifter in self.shifters]:
            for output in outputs:
                output.shell.reset()

        for i, port in enumerate(self.input_b.ports):
            if i == 0:
                yield If(port.shell == True).then(self.input_a.shell.copy(self.shift_results[i]))
            elif i > 0:
                yield If(port.shell == True).then(
                    InlineCall(self.shifters[i - 1])
                )

        for inputs in [shifter.inputs for shifter in self.shifters]:
            for input in inputs:
                input.shell.reset()

        for i in xrange(self.bits - 1):
            if i == 0:
                yield self.shift_results[i].shell.copy(self.adder.input_a)
                yield self.shift_results[i + 1].shell.copy(self.adder.input_b)
            else:
                yield self.adder.output.shell.copy(self.adder.input_b)
                yield self.shift_results[i + 1].shell.copy(self.adder.input_a)

            if self.inline_adder:
                yield InlineCall(self.adder)
            else:
                yield MainLogicJump(self.adder)
                # for adder in self.adders:
                #     yield MainLogicJump(adder)
