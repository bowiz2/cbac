"""Holds example unit"""
from cbac.unit.unit_base import Unit
from cbac.unit import std_logic, auto_synthesis


class ShiftUnit(Unit):
    """
    This is an example of a basic structure of a command block array unit.
    """

    @auto_synthesis
    def __init__(self, bits=8, times=1, inp=std_logic.InputRegister, output=std_logic.OutputRegister, carry_out=None,
                 register_work=None, no_reset=False):
        """
        :param bits: size of the input and the output.
        :param times: how many times to shift the input.
        :param inp: input register.
        :param output: output register.
        :param carry_out: Pass port which will be set true if the shifted out bit is true.
        :param register_work: On this register all the operations will be preformed.
        """
        super(ShiftUnit, self).__init__(bits, no_reset=no_reset)

        if not register_work:
            register_work = std_logic.InputRegister(self.bits + times)

        self.input = self.add_input(inp)
        self.output = self.add_output(output)

        # On this register all the operations will be preformed.
        self.register_work = self.add_input(register_work)
        # This is the register to which the input will be copied.
        self.register_target = self.register_work.slice(xrange(times, self.bits + times))
        # From this register the output will be copied.
        self.register_product = self.register_work.slice(xrange(min(self.output.size, self.register_work.size)))

        self.carry_out = self.add(carry_out)

    def architecture(self):
        """
        Here you declare the commands of the main logic. each command must be yielded out.
        Each statement which is yielded out will be parsed.
        you can read about the statement which can be used here in the cbac.unit.statement module.
        """
        yield self.input.shell.copy(self.register_target)
        yield self.register_product.shell.copy(self.output)
        if self.carry_out:
            yield self.register_work.ports[self.bits + 1].shell.copy(self.carry_out)
