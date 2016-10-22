from cbac.unit import auto_synthesis
from cbac.unit.statements import If
from cbac.unit.unit_base import Unit
from cbac import std_logic


class ReverseUnit(Unit):
    """
    Bitwise reverse the content of a register.
    """

    @auto_synthesis
    def __init__(self, bits=8, inp=std_logic.InputRegister, output=std_logic.OutputRegister):
        super(ReverseUnit, self).__init__(bits)
        self.input = self.add_input(inp)
        self.output = self.add_output(output)

    def architecture(self):
        for index in xrange(self.bits):
            yield If(self.input.ports[index].shell == True).then(
                self.output.ports[self.bits - index - 1].shell.activate()
            )
