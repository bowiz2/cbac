from cbac.unit.unit_base import Unit
from cbac.unit.statements import *
from cbac.unit import std_logic, auto_synthesis


class IncrementLogic(Unit):
    """
    Logic of increment of one bit.
    """
    @auto_synthesis
    def __init__(self, a=std_logic.In, s=std_logic.Out, cin=std_logic.In, cout=std_logic.Out):
        super(IncrementLogic, self).__init__()
        self.a = self.add(a)
        self.s = self.add(s)
        self.cin = self.add(cin)
        self.cout = self.add(cout)

    def architecture(self):
        yield If((self.a.shell == True) & (self.cin.shell == True)).then(self.cout.shell.activate())
        yield If((self.a.shell == False) & (self.cin.shell == True)).then(self.s.shell.activate())
        yield If((self.a.shell == True) & (self.cin.shell == False)).then(self.s.shell.activate())


class IncrementUnit(Unit):
    """
    Increments a register by 1.
    """
    @auto_synthesis
    def __init__(self, bits, inp=std_logic.InputRegister, output=std_logic.OutputRegister, carry_out=None):
        super(IncrementUnit, self).__init__(bits)
        self.input = self.add(inp)
        self.output = self.add(output)
        self.carry_out = self.add(carry_out)
        # in the carry we will remember the addition.
        self._carry = self.add(std_logic.InputRegister(self.bits + 1))
        self.incrementer_logic = self.add(IncrementLogic)

    def architecture(self):
        yield self._carry.ports[0].shell.activate()
        yield map(self.incrementer_logic, self.input.ports, self.output.ports, self._carry.ports[:-1], self._carry.ports[1:])

